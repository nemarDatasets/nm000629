---
license: cc-by-nc-4.0
pretty_name: EgoBrain-Mini
tags:
  - eeg
  - egocentric-video
  - brain-computer-interface
  - multimodal
  - imu
  - motion-capture
  - audio
  - neuroscience
  - video
  - timeseries
language:
  - en
size_categories:
  - 1K<n<10K
configs:
  - config_name: default
    data_files:
      - split: train
        path: browse/segments.parquet
extra_gated_fields:
  First Name: text
  Last Name: text
  Email: text
  Affiliation: text
  Position (PhD/Master/Faculty/Industry): text
  Country: country
  Personal or Lab Website (optional): text

  How did you learn about the EgoBrain-Mini project?: text
  What do you plan to use EgoBrain-Mini for?: text
  Why are you interested in our EgoBrain-Mini Project?: text

  I confirm this dataset will only be used for research purposes: checkbox
  I agree not to redistribute the dataset: checkbox
  I agree not to attempt re-identification of any participant: checkbox
  I agree to properly cite the EgoBrain paper and dataset: checkbox
---
<p align="center">
  <img src="assets/egobrain_mosaic.jpg" alt="EgoBrain spelled out in 3,070 first-person frames from the release, over real EEG from the same recordings" width="100%">
</p>

<div align="center">
<h1> <b>[ICLR 2026]</b> <br> EgoBrain: Synergizing Minds and Eyes For Human Action Understanding </h1>
<h3><span style="background: linear-gradient(104deg, rgba(255,225,0,0.1) 0.9%, rgba(255,225,0,0.6) 2.4%, rgba(255,225,0,0.6) 96.5%, rgba(255,225,0,0.1) 98.5%); padding: 0.15em 0.5em; border-radius: 4px;">EgoBrain-Mini — lightweight, fast, and fully synchronized</span></h3>
<p align="center">
<b>40</b> subjects &nbsp;·&nbsp; <b>1,562</b> sub-actions &nbsp;·&nbsp; <b>63</b> hours <sub>(61 + 2 calibration)</sub> &nbsp;·&nbsp; <b>4</b> synchronised modalities &nbsp;·&nbsp; <b>27</b> everyday activities
</p>

<a href="https://lin-nie.github.io/EgoBrain/"><img src="https://img.shields.io/badge/Project_Page-green" alt="Project Page"></a>
<a href="https://www.arxiv.org/abs/2506.01353" target="_blank" rel="noopener noreferrer"> <img src="https://img.shields.io/badge/Paper-arXiv:2506.01353-DodgerBlue.svg?style=plastic" alt="Paper PDF"></a>
<a href=""> <img src="https://img.shields.io/badge/Demo-blue" alt="Demo"></a>


**[東京大学 The University of Tokyo](https://www.ut-vision.org/) X [微軟亞洲研究院 Microsoft Research Asia](https://www.microsoft.com/en-us/research/lab/microsoft-research-asia/)**
<p>
    <a href="https://lin-nie.github.io/">Nie Lin</a>
    ·
    <a href="https://victorywys.github.io/">Yansen Wang</a>
    ·
    <a href="https://frosthan.github.io/">Dongqi Han</a>
    ·
    <a href="https://935963004.github.io/">Weibang Jiang</a>
    ·
    <a href="https://christincha.github.io/">Jingyuan Li</a>
    ·
    <a href="https://rfuruta.github.io/">Ryosuke Furuta</a>
</p>
<p>
    <a href="https://sites.google.com/ut-vision.org/ysato/">Yoichi Sato<sup>&#9993;</sup></a>
    ·
    <a href="http://recmind.cn/">Dongsheng Li<sup>&#9993;</sup></a>
</p>

<img src="assets/room.gif" width="620" alt="One recording session: the EEG cap, the head-mounted camera, the wrist bands, and the everyday objects on the desk" />

<p align="center"><a href="https://lin-nie.github.io/EgoBrain/"><b>Explore the project page &rarr;</b></a><br>
<sub>The room above is live there — tap the desk objects, the EEG cap, the camera or the wrist bands.</sub></p>
</div>

---
[![arXiv](https://img.shields.io/badge/arXiv-2506.01353-DodgerBlue.svg?style=plastic)](https://arxiv.org/pdf/2506.01353.pdf) ![License CC BY-NC-4.0](https://img.shields.io/badge/license-CC_BY--NC--4.0-DodgerBlue.svg?style=plastic)

This is **EgoBrain-Mini**, a lightweight companion release of our [ICLR 2026](https://iclr.cc/) paper
"EgoBrain: Synergizing Minds and Eyes For Human Action Understanding" — the egocentric subset
(first-person video + EEG + IMU + audio), meant as a quick
way to explore the data and its alignment before diving into the full [EgoBrain](https://huggingface.co/datasets/ut-vision/EgoBrain)
release.

[Nie (Elon) Lin](https://lin-nie.github.io/), [Yansen Wang](https://victorywys.github.io/), [Dongqi Han](https://frosthan.github.io/), [Weibang Jiang](https://935963004.github.io/), [Jingyuan Li](https://cai-mj.github.io/), [Ryosuke Furuta](https://rfuruta.github.io/), [Yoichi Sato*](https://sites.google.com/ut-vision.org/ysato/), [Dongsheng Li*](http://recmind.cn/)
(*co-corresponding authors). "[EgoBrain: Synergizing Minds and Eyes For Human Action Understanding](https://openreview.net/forum?id=DGcoJINQ7P)", [ICLR 2026](https://iclr.cc/).

## 🗺️ Contents

- [📢 News](#news)
- [📦 What's actually in the box](#in-the-box)
- [🪑 What one session looks like](#session)
- [📂 Dataset Structure](#dataset-structure)
- [⏱️ How the modalities are aligned](#alignment)
- [🔍 Explore it interactively](#explore)
- [✅ Verification](#verification)
- [⚠️ Known data issues](#known-issues)
- [🔒 Privacy](#privacy)
- [🚫 What's *not* in this release](#not-included)
- [🚀 Quick start](#quick-start)
- [⚙️ Processing](#processing)
- [📝 Citation](#citation)
- [🌟 Acknowledgement](#acknowledgement)
- [📜 License](#license)

<a id="news"></a>
## 📢 News

<div style="max-height: 160px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 8px;">

- **[2026-10-14]**: 🌐 The **project page** is live at [lin-nie.github.io/EgoBrain](https://lin-nie.github.io/EgoBrain/) — including an interactive model of the recording room: hover the desk objects, the EEG cap, the camera or the wrist bands.
- **[2026-10-13]**: 🎉 **EgoBrain-Mini is fully released.** All 40 subjects (P0001–P0040) are now available — 1,562 sub-actions, 63 hours (61 + 2 calibration), four synchronised modalities.
- **[2026-10-12]**: Second-pass review. An independent reviewer re-checked all 40 subjects against the published tree, segment by segment, including the bundled reports and the browse index.
- **[2026-10-11]**: Pre-release review across the full corpus — cross-modality timing, EEG integrity and per-sensor IMU rates re-checked for every one of the 1,562 sub-actions, not a sample.
- **[2026-10-10]**: Released Subject P0040 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-10]**: Released Subject P0039 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a lower rate — see [Known data issues](#known-issues).
- **[2026-10-10]**: Released Subject P0038 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-10]**: Released Subject P0037 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a much lower rate — see [Known data issues](#known-issues).
- **[2026-10-10]**: Released Subject P0036 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-10]**: Released Subject P0035 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a much lower rate — see [Known data issues](#known-issues).
- **[2026-10-09]**: Released Subject P0034 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-09]**: Released Subject P0033 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-09]**: Released Subject P0032 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-09]**: Released Subject P0031 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a much lower rate — see [Known data issues](#known-issues).
- **[2026-10-06]**: Released Subject P0030 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-06]**: Released Subject P0029 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a much lower rate — see [Known data issues](#known-issues).
- **[2026-10-06]**: Released Subject P0028 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-06]**: Released Subject P0027 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-06]**: Released Subject P0026 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-06]**: Released Subject P0025 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ One of its four IMU sensors logged at a much lower rate — see [Known data issues](#known-issues).
- **[2026-10-06]**: Released Subject P0024 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-04]**: Released Subject P0023 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-04]**: Released Subject P0022 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-04]**: Updated P0008: 15 of its 39 sub-actions now carry EEG quality flags (a loose electrode, twice) — see [Known data issues](#known-issues).
- **[2026-10-04]**: Released Subject P0021 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-04]**: Released Subject P0020 egocentric video + EEG + IMU + audio (Phase 2). ⚠️ In 32 of its 39 sub-actions an EEG reference electrode had lost contact — see [Known data issues](#known-issues).
- **[2026-10-03]**: Released Subject P0019 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-10-03]**: Released Subject P0018 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-27]**: Released Subject P0017 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-21]**: Released Subject P0016 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-20]**: Released Subject P0015 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-16]**: Released Subject P0014 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-14]**: Released Subject P0013 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-12]**: Released Subject P0012 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-09]**: Released Subject P0011 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-07]**: Released Subject P0010 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-06]**: Released Subject P0009 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-06]**: Released Subject P0008 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-04]**: Released Subject P0007 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-03]**: Released Subject P0006 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-02]**: Released Subject P0005 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-09-02]**: Released Subject P0004 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-08-20]**: Released Subject P0003 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-08-19]**: Released Subject P0002 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-08-19]**: Released Subject P0001 egocentric video + EEG + IMU + audio (Phase 2).
- **[2026-08-18]**: Created the Hugging Face repository for [ut-vision](https://huggingface.co/ut-vision)/[EgoBrain-Mini](https://huggingface.co/datasets/ut-vision/EgoBrain-Mini).

</div>

<a id="in-the-box"></a>
## 📦 What's actually in the box

40 subjects (P0001–P0040), 1562 real-world sub-actions (39 per subject; P0037 has 41), four
modalities — first-person video, EEG, a body-worn IMU, and audio — all recorded from **the same
person doing the same thing at the same instant**. Every one of the 1562 was verified individually,
not sampled.

<p align="center">
  <img src="assets/subjects_grid.jpg" width="100%" alt="One sub-action from each of the 40 subjects, labelled P0001-P0040, all first-person">
  <br><sub>One sub-action from each of the 40 subjects, in order P0001–P0040 — 25 different everyday activities, four from each of the ten activity groups, every frame from that subject's own first-person camera.</sub>
</p>

| Modality | File | Format | Shape | Rate / Size | Notes |
|---|---|---|---|---|---|
| 🧠 EEG (raw) | `eeg/raw.npy` | float32 array, µV | `[32, T]` | 32 channels @ **256 Hz** | Channel-selected only, otherwise unprocessed |
| 🧠 EEG (clean) | `eeg/clean.npy` | float32 array, standardized | `[32, T]` | 32 channels @ **200 Hz** | Detrended, 0.1–75 Hz bandpass + 50 Hz notch, RANSAC bad-channel interpolation, average reference, exponential-moving standardization — see [Processing](#processing) |
| 🖐️ IMU | `imu/imu.parquet` | Parquet, long format | `[T, 20]` per device | 4 body-worn sensors, **rate varies by subject/session — see `meta.json`'s `imu_hz`, don't assume a fixed number** | Left/right wrist + left/right upper arm — see [IMU columns](#imu-columns) |
| 🎙️ Audio | `audio/ego.wav` | WAV, mono PCM16 | `[T]` | **16 kHz** | The Ego camera's own microphone |
| 🎥 Video | `video/ego.mp4` | H.264 / MP4 | — | **854×480 @ ~30 fps** | First-person; a copy of its own mic audio is embedded too, but `audio/ego.wav` is the higher-fidelity source |
| 📄 Provenance | `video/ego.json` | JSON | — | — | Exact raw source chapter + frame range this clip was cut from (for traceability; raw video itself is not distributed) |

`T` is the **total sample count for that one sub-action's clip** — `duration_sec × sample_rate` — not a
separate dimension on top of the rate. For example, the 76.2 s `setup-calibration` sub-action has
`eeg/raw.npy.shape == (32, 19508)` (76.2 × 256 Hz) and `eeg/clean.npy.shape == (32, 15240)` (76.2 × 200 Hz
exactly). Since duration varies per sub-action (from ~0.3 s to ~18 min across the 1562 of them), `T` is different
for every file — it's never a fixed constant you can hard-code.

The array itself carries no metadata — it's just numbers. To go the other way (shape → duration), either
read `meta.json`'s `duration_sec` directly (the authoritative source, already used in [Quick start](#quick-start)),
or divide back out: `duration_sec ≈ T / sample_rate` (e.g. `15240 / 200 = 76.2`), since the sample rate
per file is fixed and documented above.

Every one of the 1562 sub-actions has all six of these. Nothing here is a placeholder or a partial modality.

<a id="session"></a>
## 🪑 What one session looks like

<p align="center">
  <img src="assets/egobrain.png" width="680" alt="The recording rig, the two streams it produces, the seated subject, and how one sub-action is delimited">
</p>

**(a)** The desk, and the rig: a GoPro mounted on an Emotiv EEG headset, so the camera moves with
the head and the electrodes stay put. **(b)** What that rig produces — the first-person video and the
32 EEG traces, from the same instant. **(c)** The participant, seated, with a monitor in front of them.
**(d)** How one sub-action gets its boundaries: a **screen prompt** names the task, the participant
**executes** it, then clicks **end** — and that bracket, not a human scrubbing a timeline afterwards,
is what a segment in this dataset is.

| In the figure | In the files |
|---|---|
| 🧠 The Emotiv headset | 32-channel EEG at 256 Hz — `eeg/raw.npy`, and the processed `eeg/clean.npy` at 200 Hz |
| 🎥 The GoPro on it | the first-person view — `video/ego.mp4`, and its microphone as `audio/ego.wav` |
| 🖐️ Bands on both wrists and upper arms | four body-worn IMUs — `imu/imu.parquet` |
| 🖥️ The screen prompt | the task the participant was given — `meta.json`'s `action` |
| ⏱️ Prompt → execute → end click | one sub-action's extent — `meta.json`'s `duration_sec` |

1562 of these, from 40 people, with all four streams running at once.

<a id="dataset-structure"></a>
## 📂 Dataset Structure
```
EgoBrain-Mini/
├── assets/
├── P0001/
│   ├── manifest.json                      ← index of all 39 segments + metadata
│   ├── segments/
│   │   └── phase2/
│   │       ├── P0001_phase2_000_setup-calibration/
│   │       │   ├── meta.json               ← action label, timestamps, duration, modality flags,
│   │       │   │                             and eeg_quality_flags where EEG quality is compromised
│   │       │   ├── eeg/
│   │       │   │   ├── raw.npy
│   │       │   │   └── clean.npy
│   │       │   ├── imu/
│   │       │   │   └── imu.parquet
│   │       │   ├── audio/
│   │       │   │   └── ego.wav
│   │       │   └── video/
│   │       │       ├── ego.mp4
│   │       │       ├── ego.json
│   │       │       └── redaction_windows.json  ← only present where needed, see Privacy below
│   │       └── ...                             (39 segments total, same layout)
│   └── reports/                             ← bundled, offline-first HTML report, see below
├── P0002/                                   ← same layout, 39 segments
├── ...                                      ← more subjects
└── README.md
```

`<segment_id>` looks like `P0001_phase2_022_drink-water-b` — subject, phase, sequence number, and a
human-readable action slug.

<a id="imu-columns"></a>
### IMU columns

`imu.parquet` is long-format: one row per sample, a `device` column (`imu_1`…`imu_4`) selecting which
sensor, and a `ts` column (Unix timestamp):

| Column | Meaning |
|---|---|
| `AccX_g`, `AccY_g`, `AccZ_g` | Acceleration X/Y/Z (g) |
| `GyroX_dps`, `GyroY_dps`, `GyroZ_dps` | Angular velocity X/Y/Z (degrees/second) |
| `AngleX_deg`, `AngleY_deg`, `AngleZ_deg` | Orientation angle X/Y/Z (degrees) |
| `MagX_uT`, `MagY_uT`, `MagZ_uT` | Magnetic field X/Y/Z (µT) |
| `QuatW`, `QuatX`, `QuatY`, `QuatZ` | Orientation quaternion |
| `Temperature_C` | Sensor temperature (°C) |
| `Battery_pct` | Battery level (%) |

`imu_1` = left wrist, `imu_2` = left upper arm, `imu_3` = right wrist, `imu_4` = right upper arm.

**The IMU's own sample rate is not the same across subjects*** — P0001 and P0022 onward logged at
~200 Hz (the intended setting), but P0002–P0021 logged at ~10 Hz for their entire sessions (a ~20x
difference; same hardware, a different logging configuration — P0002's raw column names were also
formatted differently, see above). Don't hard-code a rate: each segment's `meta.json` has an `imu_hz`
field computed directly from that file's own `ts` column, and that's the number to use for any
`T ↔ duration` conversion involving `imu.parquet`.

**At ~200 Hz, timestamps come in batches.** The sensors send samples to the logger in small Bluetooth
batches, and the logger stamps every sample of a batch with the batch's arrival time — so most rows
(80–90%) share the previous row's `ts`, with batches ~30–40 ms apart. The samples themselves are real
(the values change from row to row); only the per-sample time is coarse. If you need one time per
sample, spread each batch evenly up to the next batch, per device:

```python
def respace(ts, imu_hz):
    """ts: one device's timestamps, sorted. Spread each batch evenly up to the next batch."""
    ts = np.asarray(ts, float); out = ts.copy()
    starts = np.flatnonzero(np.r_[True, np.diff(ts) > 0])
    ends = np.r_[starts[1:], len(ts)]
    for a, b in zip(starts, ends):
        nxt = ts[b] if b < len(ts) else ts[a] + (b - a) / imu_hz
        out[a:b] = ts[a] + (nxt - ts[a]) * np.arange(b - a) / (b - a)
    return out

dev = imu[imu["device"] == "imu_1"].sort_values("ts", kind="stable")
t = respace(dev["ts"].to_numpy(), meta["imu_hz"])   # strictly increasing, ~imu_hz apart
```

<sub>* During early data collection (P0002–P0021), the IMU devices weren't configured to
their maximum output rate (the team was still getting familiar with the hardware) — this is why the
main EgoBrain release doesn't include IMU for those subjects at all. EgoBrain-Mini releases it anyway
rather than dropping it, since a lower-rate signal is still real, usable data — just be aware of it via
`imu_hz` rather than assuming parity with P0001 and P0022 onward. We're still looking into whether this can be backfilled
or otherwise compensated for in a future update.</sub>

<a id="alignment"></a>
## ⏱️ How the modalities are aligned

Multimodal synchronization is achieved through an **EEG-anchored, cross-modal calibration procedure**:
EEG is treated as the ground-truth clock, and every other modality's timeline is corrected to match it —
not aligned pairwise against each other. The alignment was independently re-verified for every released subject
against 100% of the published sub-actions (not a sample) before release, including an EEG interval-marker
cross-check baked directly into the bundled report's EEG chart (see below).

<a id="explore"></a>
## 🔍 Explore it interactively

**Nothing to download:** the [project page](https://lin-nie.github.io/EgoBrain/) has an interactive model of the recording
room — tap the desk objects, the EEG cap, the camera or the wrist bands to see which part of
the dataset each one stands for.

Each subject's own `<subject>/reports/` (e.g. `P0001/reports/`, `P0002/reports/`) is a self-contained,
**offline-first** HTML report — no server, no internet connection, no dependencies. Download this repo,
then just open `<subject>/reports/index.html` in a browser:

- A gallery of that subject's 39 sub-actions with thumbnails
- Per-action pages with synced video + live EEG / IMU / audio charts (drag the video, the charts scroll
  with it, and vice versa — click any chart to jump the video there)
- Plain-language explanations of what each chart actually shows and why

(HF's own file viewer won't execute the JavaScript in these pages — you do need the files on your own
machine. That's by design: it means the report works identically whether you're online or not.)

**Prefer to browse without downloading first?** The **Dataset Viewer** above (the "Data Studio" /
table tab on this page) shows every sub-action across every subject as one row — thumbnail, subject,
action label, phase, duration, and which modalities it has — before you commit to downloading anything.
It's generated from `browse/segments.parquet`, a lightweight index (thumbnails only, no video/EEG/IMU
payload) built purely for this at-a-glance browsing; the real per-segment data still lives under each
subject's own `segments/phase2/<segment_id>/` folder as described above.

<a id="verification"></a>
## ✅ Verification

Every one of the 1562 sub-actions — not a sample — was individually checked:

- **EEG integrity**: all 32 channels finite, no flat/dead channels
- **Alignment**: every sub-action's report carries the EEG hardware's own interval-marker
  timestamp drawn on its EEG chart, so the cut can be checked against the EEG's own log segment
  by segment. The alignment itself was fitted per subject and then verified frame by frame at
  independent anchors — an on-screen task banner switching against the EEG marker, plus desk-clock
  ticks where a clock is legible — and reviewed by hand for every released subject. The number of
  anchors varies by subject (five per cross-check for P0014 onward, where the anchor list is
  recorded; P0001-P0013 were verified the same way under an earlier generation of the tooling)
- **Coverage**: 1562 / 1562, no segments skipped or excluded from verification
- **EEG quality** (every released subject): two checks over the whole session — the headset's own
  contact-quality readings for its two ear reference electrodes, and the raw amplitude (a large artifact
  shared across channels, sustained above ~1 mV). Affected spans are flagged per segment — see
  [Known data issues](#known-issues)

### Check it yourself

Every subject folder ships `verify_alignment.py` — a standalone script that depends on nothing but
the files you downloaded (numpy, pandas + pyarrow, and ffmpeg on PATH), not on the pipeline that
produced them. It finds the same **physical** movements in each stream and compares when they happen.

| Stream | What it measures |
|---|---|
| 🎥 Video | frame-to-frame change in the lower two thirds of the ego view, where the hands are |
| 🖐️ IMU | angular speed, all four sensors together and each one on its own |
| 🧠 EEG | movement artifacts — 1–15 Hz activity in `eeg/raw.npy` |

Each curve is slid against the video's; the shift with the best match is that segment's lag. The
verdict uses the subject's **median** lag, since a single segment scatters by a few tenths of a second.

```bash
python P0001/verify_alignment.py P0001
```

Run over all 40 subjects on the released files, every subject passes on every stream:

| Stream vs ego video | Subjects passing | Median across subjects | Largest subject median |
|---|---|---|---|
| 🧠 EEG | **40 / 40** | −0.00 s | 0.19 s |
| 🖐️ IMU, four sensors together | **40 / 40** | −0.02 s | 0.05 s |
| `imu_1` left wrist | **40 / 40** | −0.02 s | 0.06 s |
| `imu_2` left upper arm | **40 / 40** | −0.00 s | 0.06 s |
| `imu_3` right wrist | **40 / 40** | −0.04 s | 0.07 s |
| `imu_4` right upper arm | **40 / 40** | −0.02 s | 0.14 s |

The motion check only looks at sub-actions longer than 45 s (1260 of the 1562) — shorter ones rarely
hold enough movement for a confident match. Of those it found a clear match in **1255** for the IMU
and **988** for EEG, whose movement artifact is much weaker than a gyroscope's signal. Segments
without a clear match are left out of the median rather than counted as zero.

<a id="known-issues"></a>
## ⚠️ Known data issues

Known problems in the released data. The files themselves are left unaltered; every affected range is
listed in that segment's `meta.json` (`eeg_quality_flags`) and marked in the bundled report.

| Subject | Modality | Issue | Affected range | Segments | Recommendation |
|---|---|---|---|---|---|
| P0008 | EEG | An electrode came loose twice; the signal is dominated by a 1–3 mV artifact shared across channels (normal EEG: ~0.05–0.15 mV) | `phase2_021` 1 s → `phase2_025` 249 s, and `phase2_027` 1 s → `phase2_036` 185 s | 15 of 39 | Exclude from EEG analyses |
| P0020 | EEG | An ear reference electrode (CMS/DRL) lost contact; all 32 channels are affected (alpha power ~85% lower; blinks and chewing still visible) | `phase2_007` 111.3 s → `phase2_038` 36.4 s (contact briefly back in `phase2_019`, 154.5–217.5 s) | 32 of 39 | Exclude from band-power / amplitude-based analyses |
| P0025 | IMU | One of the four sensors (`imu_3`, right wrist) logged at ~58 Hz while the other three held ~198.6 Hz — Bluetooth packet loss on that unit, not a configuration difference | The whole session | 39 of 39 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_3` as sparse, and avoid analyses that assume the four sensors share a sample grid |
| P0029 | IMU | One of the four sensors (`imu_2`, left upper arm) logged at ~62.8 Hz while the other three held ~198.6 Hz — the same Bluetooth packet loss as P0025, on a different unit | The whole session | 39 of 39 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_2` as sparse, and avoid analyses that assume the four sensors share a sample grid |
| P0031 | IMU | One of the four sensors (`imu_1`, left wrist) logged at ~61 Hz while the other three held ~198.6 Hz — the same Bluetooth packet loss as P0025 and P0029, on a different unit again | The whole session | 39 of 39 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_1` as sparse, and avoid analyses that assume the four sensors share a sample grid |
| P0035 | IMU | One of the four sensors (`imu_4`, right upper arm) logged at ~159 Hz while the other three held ~198.6 Hz — the same Bluetooth packet loss as P0025, P0029 and P0031, on a different unit again | The whole session | 39 of 39 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_4` as sparse, and avoid analyses that assume the four sensors share a sample grid |
| P0037 | IMU | One of the four sensors (`imu_1`, left wrist) logged at ~49 Hz while the other three held ~198.6 Hz — the same Bluetooth packet loss as P0025, P0029, P0031 and P0035, and the slowest case in the corpus | The whole session | 41 of 41 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_1` as sparse, and avoid analyses that assume the four sensors share a sample grid |
| P0039 | IMU | One of the four sensors (`imu_2`, left upper arm) logged at ~152 Hz (range 137–175) while the other three held ~196–199 Hz — the mildest case of the same Bluetooth packet loss as P0025, P0029, P0031, P0035 and P0037; it is listed because the gap is still large enough to break a shared sample grid | The whole session | 39 of 39 | Use `meta.json`'s `imu_hz_per_device`; treat `imu_2` as sparse, and avoid analyses that assume the four sensors share a sample grid |

For the EEG rows, video, audio and IMU are unaffected; for the IMU rows, video, audio and EEG are unaffected.

**How they were found.** The two EEG cases were caught by the headset's own contact-quality
channels together with the raw amplitude: in both, an experimenter is seen re-attaching an
electrode, and the EEG shows a sharp transient at the loss and at the re-attachment. The IMU
cases were caught by a per-subject rate check run before every release — `meta.json`'s `imu_hz`
averages the four sensors and so hides a single slow unit, while `imu_hz_per_device` exposes it:

```json
"imu_hz": 161.38,
"imu_hz_per_device": {"imu_1": 198.67, "imu_2": 198.67, "imu_3": 49.51, "imu_4": 198.67}
```

The samples a slow unit did record are real and correctly timestamped — there are simply fewer of
them. Each affected subject's bundled report carries a notice above its IMU chart, so the sparser
trace is explained where it is seen.

**Using the flags.** Segments without `eeg_quality_flags` have no known EEG issue. `rel_start` /
`rel_end` are seconds from the segment start; `issue` is `signal_quality_poor` or
`reference_contact_lost`:

```json
"eeg_quality_flags": [
  {"rel_start": 0.0, "rel_end": 154.5, "issue": "reference_contact_lost",
   "description": "...", "evidence": "..."}
]
```

To keep only unflagged EEG samples:

```python
flags = meta.get("eeg_quality_flags", [])
fs = 200                                           # clean.npy rate
keep = np.ones(eeg_clean.shape[1], bool)
for f in flags:
    keep[int(f["rel_start"] * fs):int(f["rel_end"] * fs)] = False
eeg_ok = eeg_clean[:, keep]                         # samples outside every flagged range
```

<a id="privacy"></a>
## 🔒 Privacy

131 of the 1562 sub-actions briefly show something that needed redacting — most often a laptop's own
lock screen or an app window, a hand-held phone, or earlier pages of a shared notebook being leafed
through; occasionally a bystander incidentally in frame. Rather
than blank out the whole picture for something covering a fraction of it, redaction is **region-limited
blur**: only the specific area of the frame containing the sensitive detail is blurred (strong enough
that text, faces, and names are unreadable), for only the seconds it's actually visible — the rest of
the frame, and the rest of the clip, is untouched. A small number of windows also mute audio, when the
audio itself (not just the picture) needed it. This is baked into the video at the source, not a
runtime toggle. `video/redaction_windows.json` documents exactly which seconds and which region of the
frame were affected, for transparency. Nothing else in the release is redacted.

If you come across any content in this release that you believe may reveal a subject's private
information, please contact the maintainers immediately at **nielin@iis.u-tokyo.ac.jp** and it will be
re-processed and re-uploaded.

<a id="not-included"></a>
## 🚫 What's *not* in this release

- **Raw, unprocessed video** — not distributed at all; `video/*.json` retains exact provenance
  (source file + frame range) in case higher-fidelity access is ever needed for approved use.
- Only Phase 2 (real-world action) sub-actions are included. Phases 1 and 3 (the in-lab
  calibration and resting blocks) stay in the full [EgoBrain](https://huggingface.co/datasets/ut-vision/EgoBrain) release.

<a id="quick-start"></a>
## 🚀 Quick start

```python
import json
import numpy as np
import pandas as pd

root = "P0001/segments/phase2/P0001_phase2_022_drink-water-b"

meta = json.load(open(f"{root}/meta.json"))
eeg_clean = np.load(f"{root}/eeg/clean.npy")        # [32, T] @ 200 Hz
imu = pd.read_parquet(f"{root}/imu/imu.parquet")     # long format, 4 devices

print(meta["action"], meta["duration_sec"], "sec")
print("EEG:", eeg_clean.shape)
print("IMU devices:", imu["device"].unique())
```

<a id="processing"></a>
## ⚙️ Processing

`eeg/clean.npy` is produced by (in order): linear + 6th-order detrending → 0.1–75 Hz bandpass filter →
50 Hz notch filter → resample to 200 Hz → RANSAC-based bad-channel detection and interpolation → average
reference → exponential-moving-average standardization. `eeg/raw.npy` skips all of this — it's the
channel-selected signal at its native 256 Hz, in µV.

<a id="citation"></a>
## 📝 Citation

If EgoBrain-Mini is useful in your research, please cite the paper:

```bibtex
@inproceedings{lin2026egobrain,
  title     = {EgoBrain: Synergizing Minds and Eyes For Human Action Understanding},
  author    = {Nie Lin and Yansen Wang and Dongqi Han and Weibang Jiang and
               Jingyuan Li and Ryosuke Furuta and Yoichi Sato and Dongsheng Li},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2026},
  url       = {https://arxiv.org/abs/2506.01353}
}
```

Please also mention the release you used, so results stay reproducible:

> EgoBrain-Mini (Hugging Face: `ut-vision/EgoBrain-Mini`), 40 subjects, 1,562 sub-actions.

<a id="acknowledgement"></a>
## 🌟 Acknowledgement

We sincerely thank all participants who contributed their time and effort to the data collection process.

This project was initiated and developed during Nie Lin's research internship at Microsoft Research Asia
(MSRA), and later continued at the Institute of Industrial Science (IIS), The University of Tokyo. We
thank all collaborators and mentors at MSRA and IIS for their valuable guidance and support.

We also acknowledge the support from our advisors, collaborators, and the community.

<a id="license"></a>
## 📜 License

EgoBrain-Mini is released under the **Creative Commons Attribution-NonCommercial 4.0 International
(CC BY-NC 4.0)** license.

By using this dataset, you agree to:

- Use the dataset only for **non-commercial research purposes**
- **Not redistribute** the data
- **Not attempt to identify the participant**
- Comply with applicable **ethical and data protection regulations**

If you have questions regarding licensing or usage, please contact the maintainers at
**nielin@iis.u-tokyo.ac.jp**.

License details: https://creativecommons.org/licenses/by-nc/4.0/

[![CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)
