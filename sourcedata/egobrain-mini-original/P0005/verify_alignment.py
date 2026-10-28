#!/usr/bin/env python3
"""Independent cross-modality alignment check -- no dependency on the
release pipeline, just this file + manifest.json + the segment data you
downloaded. Two checks:

1. Durations (fast). For every segment, computes each present modality's
   own real covered duration (video: ffprobe; audio: wav frame count /
   sample rate; IMU: timestamp range; EEG: sample count / 200Hz) and flags
   any segment where they disagree by more than --tol seconds.

2. Motion (a few minutes per subject; skip with --durations-only). Equal
   durations alone do not show that two streams line up: a stream that
   began one second late would still be the right length. So this check
   finds the same physical movements in each stream and compares when
   they happen:
       video  frame-to-frame change in the lower two thirds of the ego
              view, where the hands are
       IMU    angular speed, all four sensors together and each one
              on its own
       EEG    movement artifacts: 1-15 Hz activity in eeg/raw.npy
   Each stream's motion curve is slid against the video's, and the shift
   with the best match is that segment's lag (+ = the stream shows a
   movement later than the video does). Segments with too little movement
   for a clear match are left out. A single segment's lag scatters by a
   few tenths of a second, so the verdict uses the subject's median lag
   and passes when |median| <= --motion-tol (default 0.2 s).

Requires: numpy, pandas + pyarrow (for imu.parquet), ffmpeg/ffprobe on
PATH. Everything else is Python standard library.

Usage:
    pip install numpy pandas pyarrow
    python verify_alignment.py /path/to/P00NN --tol 0.1
    python verify_alignment.py /path/to/P00NN --durations-only   # skip the motion check
    python verify_alignment.py /path/to/P00NN --verbose          # also list every segment's lag
    # /path/to/P00NN is any subject folder containing manifest.json,
    # e.g. the folder you downloaded from HuggingFace.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import wave

EEG_HZ = 200  # sample rate of eeg/clean.npy, fixed for every segment
RAW_EEG_HZ = 256  # sample rate of eeg/raw.npy
GRID_HZ = 20  # motion curves are compared on this time grid
MAX_LAG = 4.0  # seconds searched either way
MIN_SEGMENT = 45.0  # shorter segments rarely hold enough movement
MIN_MATCH = 0.2  # correlation a segment's best match must reach to count
MIN_SEGMENTS = 5  # a subject needs this many usable segments for a verdict
FRAME_W, FRAME_H = 160, 90  # video is decoded at this size for the motion curve


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / w.getframerate()


def phase_key(seg_id):
    for p in ("phase1", "phase2", "phase3"):
        if f"_{p}_" in seg_id:
            return p
    raise ValueError(f"can't find phase in segment id: {seg_id}")


def compute_spans(seg_dir, mp):
    import numpy as np

    spans = {}
    # Driven by this segment's own modality_presence, so the script reports
    # exactly the cameras and microphones this release publishes.
    for view, label in [(k[len("video_"):], k[len("video_"):].capitalize())
                        for k in sorted(mp) if k.startswith("video_")]:
        if mp.get(f"video_{view}"):
            p = os.path.join(seg_dir, "video", f"{view}.mp4")
            if os.path.exists(p):
                spans[label] = ffprobe_duration(p)
    for view, label in [(k[len("audio_"):], "Audio-" + k[len("audio_"):].capitalize())
                        for k in sorted(mp) if k.startswith("audio_")]:
        if mp.get(f"audio_{view}"):
            p = os.path.join(seg_dir, "audio", f"{view}.wav")
            if os.path.exists(p):
                spans[label] = wav_duration(p)
    if mp.get("imu"):
        p = os.path.join(seg_dir, "imu", "imu.parquet")
        if os.path.exists(p):
            import pandas as pd
            df = pd.read_parquet(p)
            if len(df):
                spans["IMU"] = float(df["ts"].max() - df["ts"].min())
    if mp.get("eeg"):
        p = os.path.join(seg_dir, "eeg", "clean.npy")
        if os.path.exists(p):
            arr = np.load(p)
            spans["EEG"] = arr.shape[-1] / EEG_HZ
    return spans


# ------------------------------------------------------------------ motion


def smooth(x, seconds):
    import numpy as np
    k = max(1, int(round(seconds * GRID_HZ)))
    return np.convolve(x, np.ones(k) / k, mode="same")


def zscore(x):
    return (x - x.mean()) / (x.std() + 1e-12)


def standardize(x):
    """Light smoothing, slow trend removed, unit variance."""
    import numpy as np
    x = smooth(np.asarray(x, dtype=np.float64), 0.3)
    if len(x) > 2 * 10 * GRID_HZ:
        x = x - smooth(x, 10.0)
    return zscore(x)


def video_fps(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=avg_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    num, _, den = out.partition("/")
    return float(num) / float(den or 1)


def video_motion(path, grid, cache_dir=None):
    """Mean absolute change between consecutive frames, lower two thirds of the view."""
    import numpy as np
    key = None
    if cache_dir:
        key = os.path.join(cache_dir, f"{os.path.basename(os.path.dirname(os.path.dirname(path)))}"
                                      f"_{os.path.getsize(path)}.npy")
        if os.path.exists(key):
            saved = np.load(key)
            fps, diff = saved[0], saved[1:]
            return np.interp(grid, (np.arange(len(diff)) + 0.5) / fps, diff)
    fps = video_fps(path)
    size = FRAME_W * FRAME_H
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-i", path, "-vf",
         f"scale={FRAME_W}:{FRAME_H},format=gray", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
    )
    diffs, prev = [], None
    while True:                                          # 1000 frames at a time, to keep memory flat
        buf = proc.stdout.read(size * 1000)
        n = len(buf) // size
        if n == 0:
            break
        frames = np.frombuffer(buf[:n * size], dtype=np.uint8).reshape(n, FRAME_H, FRAME_W)
        frames = frames[:, FRAME_H // 3:, :].astype(np.int16)
        if prev is not None:
            frames = np.concatenate([prev, frames])
        diffs.append(np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2)))
        prev = frames[-1:]
    proc.stdout.close()
    if proc.wait() != 0 or not diffs:
        return None
    diff = np.concatenate(diffs)
    if len(diff) < 60:
        return None
    if key:
        os.makedirs(cache_dir, exist_ok=True)
        np.save(key, np.concatenate([[fps], diff]))
    return np.interp(grid, (np.arange(len(diff)) + 0.5) / fps, diff)


def eeg_motion(path, grid):
    """Movement artifacts: 1-15 Hz amplitude, averaged over channels."""
    import numpy as np
    x = np.load(path, mmap_mode="r")
    n = x.shape[-1]
    if n < RAW_EEG_HZ * 10:
        return None
    f = np.fft.rfftfreq(n, 1.0 / RAW_EEG_HZ)
    keep = (f >= 1.0) & (f <= 15.0)
    env = np.zeros(n)
    for c in range(0, x.shape[0], 8):                    # a few channels at a time
        block = np.asarray(x[c:c + 8], dtype=np.float64)
        spec = np.fft.rfft(block - block.mean(axis=1, keepdims=True), axis=1)
        spec[:, ~keep] = 0
        env += np.abs(np.fft.irfft(spec, n=n, axis=1)).sum(axis=0)
    env /= x.shape[0]
    k = int(RAW_EEG_HZ * 0.25)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    return np.interp(grid, np.arange(n) / RAW_EEG_HZ, env)


GYRO_COLUMNS = ("GyroX_dps", "GyroY_dps", "GyroZ_dps")
SENSOR_PLACES = {"imu_1": "left wrist", "imu_2": "left upper arm",
                 "imu_3": "right wrist", "imu_4": "right upper arm"}


def imu_motion(path, start_ts, grid):
    """Angular speed of every sensor, each standardized: the average of all, and each on its own."""
    import numpy as np
    import pandas as pd
    df = pd.read_parquet(path)
    if "is_padded" in df.columns:
        df = df[~df["is_padded"].astype(bool)]
    curves = {}
    for dev, g in df.groupby("device"):
        if len(g) < 50 or not all(c in g.columns for c in GYRO_COLUMNS):
            continue
        t = g["ts"].to_numpy(dtype=np.float64) - start_ts
        speed = np.sqrt(sum(g[c].to_numpy(dtype=np.float64) ** 2 for c in GYRO_COLUMNS))
        order = np.argsort(t, kind="stable")
        curves[dev] = zscore(np.interp(grid, t[order], speed[order]))
    if not curves:
        return None, {}
    return np.mean(list(curves.values()), axis=0), curves


def best_lag(ref, other):
    """Shift of `other` against `ref` with the best match (+ = later), and how good the match is."""
    import numpy as np
    n = min(len(ref), len(other))
    lags = np.arange(-int(MAX_LAG * GRID_HZ), int(MAX_LAG * GRID_HZ) + 1)
    r = np.array([np.mean(ref[max(0, -l):n - max(0, l)] * other[max(0, l):n - max(0, -l)])
                  for l in lags])
    k = int(np.argmax(r))
    if k == 0 or k == len(r) - 1:
        return None, float(r[k])                         # best match at the search limit: no clear answer
    # parabola through the peak and its two neighbours, for a lag finer than one grid step
    den = r[k - 1] - 2 * r[k] + r[k + 1]
    frac = min(0.5, max(-0.5, 0.5 * (r[k - 1] - r[k + 1]) / den)) if den < 0 else 0.0
    return float((lags[k] + frac) / GRID_HZ), float(r[k])


def motion_lags(seg_dir, meta, mp, cache_dir=None):
    import numpy as np
    out = {}
    dur = meta.get("duration_sec", 0)
    video = os.path.join(seg_dir, "video", "ego.mp4")
    if dur < MIN_SEGMENT or not mp.get("video_ego") or not os.path.exists(video):
        return out
    grid = (np.arange(int(dur * GRID_HZ)) + 0.5) / GRID_HZ
    v = video_motion(video, grid, cache_dir)
    if v is None:
        return out
    v = standardize(v)
    raw = os.path.join(seg_dir, "eeg", "raw.npy")
    if mp.get("eeg") and os.path.exists(raw):
        e = eeg_motion(raw, grid)
        if e is not None:
            out["EEG"] = best_lag(v, standardize(e))
    imu = os.path.join(seg_dir, "imu", "imu.parquet")
    if mp.get("imu") and os.path.exists(imu):
        m, per_sensor = imu_motion(imu, meta["start_ts"], grid)
        if m is None:
            out["IMU"] = (None, -1.0)                    # present but unreadable: reported, never skipped
        else:
            out["IMU"] = best_lag(v, standardize(m))
            for dev, curve in per_sensor.items():
                out[f"IMU {dev}"] = best_lag(v, standardize(curve))
    return out


def motion_report(per_segment, tol, verbose):
    import numpy as np
    print("Motion check (+ = the stream shows a movement later than the video does)")
    failed = False
    sensors = sorted({k for _, r in per_segment for k in r if k.startswith("IMU ")})
    for stream in ["EEG", "IMU"] + sensors:
        rows = [(sid, r[stream]) for sid, r in per_segment if stream in r]
        if not rows:
            continue
        good = [lag for _, (lag, match) in rows if lag is not None and match >= MIN_MATCH]
        unreadable = sum(1 for _, (lag, match) in rows if match < 0)
        if stream == "IMU" and unreadable == len(rows):
            failed = True
            print(f"  IMU vs video   not measured: no {'/'.join(GYRO_COLUMNS)} columns in imu.parquet   FAIL")
            continue
        if stream.startswith("IMU "):
            dev = stream[4:]
            label = f"    {dev} ({SENSOR_PLACES.get(dev, 'sensor')})"
            head = f"{label:<30s}{len(good):3d} of {len(rows):3d}"
        else:
            head = f"  {stream} vs video   {len(good):3d} of {len(rows):3d} segments with a clear match"
        if len(good) < MIN_SEGMENTS:
            print(f"{head}   too few for a verdict")
        else:
            med = float(np.median(good))
            q1, q3 = np.percentile(good, [25, 75])
            ok = abs(med) <= tol
            failed |= not ok
            print(f"{head}   median {med:+.2f}s   (middle half {q1:+.2f}..{q3:+.2f}s)   "
                  f"{'PASS' if ok else 'FAIL'} (|median| <= {tol}s)")
        if verbose:
            for sid, (lag, match) in rows:
                lag_s = "   --  " if lag is None else f"{lag:+6.2f}s"
                use = "" if lag is not None and match >= MIN_MATCH else "  (not used: no clear match)"
                print(f"      {sid:55s} {lag_s}  match {match:.2f}{use}")
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject_dir", help="path to a P00NN folder containing manifest.json")
    ap.add_argument("--tol", type=float, default=0.1,
                    help="flag if max-min modality span exceeds this many seconds (default 0.1)")
    ap.add_argument("--durations-only", action="store_true",
                    help="skip the motion check (no video decoding)")
    ap.add_argument("--motion-tol", type=float, default=0.2,
                    help="motion check passes when |median lag| is at most this many seconds (default 0.2)")
    ap.add_argument("--verbose", action="store_true", help="list every segment's motion lag")
    ap.add_argument("--cache", default=None,
                    help="optional folder for the decoded video motion curves, to make re-runs fast")
    args = ap.parse_args()

    manifest = json.load(open(os.path.join(args.subject_dir, "manifest.json")))
    seg_root = os.path.join(args.subject_dir, "segments")
    if not args.durations_only and shutil.which("ffmpeg") is None:
        print("ffmpeg not found on PATH: running the duration check only\n")
        args.durations_only = True

    checked = 0
    flagged = []
    motion = []
    for seg in manifest["segments"]:
        sid = seg["segment_id"]
        pk = phase_key(sid)
        seg_dir = os.path.join(seg_root, pk, sid)
        mp = seg.get("modality_presence", {})

        spans = compute_spans(seg_dir, mp)
        if not spans:
            continue
        checked += 1
        lo, hi = min(spans.values()), max(spans.values())
        if hi - lo > args.tol:
            flagged.append((sid, spans, hi - lo))
        if not args.durations_only:
            meta_path = os.path.join(seg_dir, "meta.json")
            if os.path.exists(meta_path):
                motion.append((sid, motion_lags(seg_dir, json.load(open(meta_path)), mp, args.cache)))

    subject = manifest.get("subject_id", os.path.basename(args.subject_dir.rstrip("/")))
    print(f"{subject}: {checked} segments checked, {len(flagged)} flagged (tol={args.tol}s)\n")
    for sid, spans, gap in flagged:
        note = ""
        meta_path = os.path.join(seg_root, phase_key(sid), sid, "meta.json")
        if os.path.exists(meta_path):
            meta = json.load(open(meta_path))
            if meta.get("imu_padding"):
                note = "  (segment has documented IMU padding -- check meta.json[\'imu_padding\'] before treating this as a bug)"
        print(f"  {sid}  spread={gap:.3f}s{note}")
        for k, v in sorted(spans.items(), key=lambda kv: kv[1]):
            print(f"      {k:12s} {v:.3f}s")

    motion_failed = False
    if motion:
        if flagged:
            print()
        motion_failed = motion_report(motion, args.motion_tol, args.verbose)

    sys.exit(1 if flagged or motion_failed else 0)


if __name__ == "__main__":
    main()
