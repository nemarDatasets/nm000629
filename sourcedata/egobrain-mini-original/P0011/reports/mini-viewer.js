// Simplified engine for EgoBrain-Mini per-segment detail pages: ONE video
// (Ego — the only camera in this release) with EEG/IMU/audio charts on
// canvases, playhead tied to the video's own currentTime.

function initMiniViewer(cfg) {
  const video = document.getElementById("v_ego");
  const duration = cfg.duration;

  function drawBase(canvas, series, sharedScale, markStart, padRegion, excludeWindows, eegWarn) {
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);
    // eegWarn: [{start_sec, end_sec}] -- EEG-only quality flag from
    // meta.json eeg_quality_flags (eeg_reference_check.py; P0020 [recording date omitted],
    // an ear reference electrode lost contact). Amber, EEG chart only: the
    // task and the other modalities are fine, the EEG in this range is not
    // comparable to normally-referenced data.
    if (eegWarn && eegWarn.length) {
      eegWarn.forEach(win => {
        const x0 = Math.max(0, (win.start_sec / duration) * W);
        const x1 = Math.min(W, (win.end_sec / duration) * W);
        if (x1 <= x0) return;
        ctx.save();
        ctx.fillStyle = "rgba(230,150,0,0.20)";
        ctx.fillRect(x0, 0, x1 - x0, H);
        ctx.strokeStyle = "rgba(199,119,0,0.8)";
        ctx.lineWidth = 1;
        ctx.strokeRect(x0 + 0.5, 0.5, x1 - x0 - 1, H - 1);
        ctx.restore();
        const fontSize = Math.max(9, Math.round(H * 0.15));
        ctx.font = `bold ${fontSize}px ui-monospace, monospace`;
        ctx.fillStyle = "#C77700";
        const label = win.label || "⚠ EEG QUALITY";
        const tw = ctx.measureText(label).width;
        const labelX = Math.min(Math.max(x0 + 4, 4), W - tw - 4);
        ctx.fillText(label, labelX, H - 6);
      });
    }
    // excludeWindows: [{start_sec, end_sec, reason}] -- real, unaltered
    // EEG/IMU/audio data, but the human reviewer determined the subject
    // was NOT doing the task during this range (e.g. a researcher came in
    // to reattach a loose electrode). Distinct from padRegion below (a
    // device timing artifact) -- ported from sync-viewer.js, see P0008
    // [recording dates omitted].
    if (excludeWindows && excludeWindows.length) {
      excludeWindows.forEach(win => {
        const x0 = Math.max(0, (win.start_sec / duration) * W);
        const x1 = Math.min(W, (win.end_sec / duration) * W);
        if (x1 <= x0) return;
        ctx.save();
        ctx.beginPath();
        ctx.rect(x0, 0, x1 - x0, H);
        ctx.clip();
        ctx.fillStyle = "rgba(180,30,30,0.22)";
        ctx.fillRect(x0, 0, x1 - x0, H);
        ctx.strokeStyle = "rgba(180,30,30,0.5)";
        ctx.lineWidth = 1;
        const step = Math.max(6, H * 0.12);
        for (let sx = x0 - H; sx < x1 + H; sx += step) {
          ctx.beginPath();
          ctx.moveTo(sx, H);
          ctx.lineTo(sx + H, 0);
          ctx.stroke();
        }
        ctx.restore();
        const fontSize = Math.max(9, Math.round(H * 0.15));
        ctx.font = `bold ${fontSize}px ui-monospace, monospace`;
        ctx.fillStyle = "#b41e1e";
        const label = "⚠ EXCLUDE THIS RANGE";
        const tw = ctx.measureText(label).width;
        const labelX = Math.min(Math.max(x0 + 4, 4), W - tw - 4);
        ctx.fillText(label, labelX, fontSize + 3);
      });
    }
    // padRegion: {front_sec, back_sec} -- IMU is a bonus modality; a gap
    // where its own real logging started late/stopped early gets filled
    // by repeating the nearest real sample rather than shrinking the
    // core modalities (see pad_imu_to_window in extract_segments_main.py).
    // Shaded so the filler is never mistaken for a real reading.
    // A pad is only labelled when its band is actually wide enough to see.
    // The first cut of this used a fixed 0.05 s floor, which still labelled
    // P0037's phase3_012 "padded 0.3s*" -- 0.257 s of a 172 s segment is 1.5
    // pixels, so the words pointed at nothing. What matters is the drawn
    // width, not the number: the same 0.3 s is worth showing on a 10 s
    // segment (3% of the chart) and meaningless on a 172 s one.
    const PAD_MIN_PX = 2;
    const padFront = (padRegion && (padRegion.front_sec / duration) * W >= PAD_MIN_PX) ? padRegion.front_sec : 0;
    const padBack  = (padRegion && (padRegion.back_sec  / duration) * W >= PAD_MIN_PX) ? padRegion.back_sec  : 0;
    if (padFront > 0 || padBack > 0) {
      ctx.fillStyle = "rgba(224,82,82,0.14)";
      if (padFront > 0) ctx.fillRect(0, 0, (padFront / duration) * W, H);
      if (padBack > 0) {
        const w = (padBack / duration) * W;
        ctx.fillRect(W - w, 0, w, H);
      }
      const fontSize = Math.max(9, Math.round(H * 0.14));
      ctx.font = `${fontSize}px ui-monospace, monospace`;
      ctx.fillStyle = "#E05252";
      if (padFront > 0) ctx.fillText(`padded ${padFront.toFixed(1)}s*`, 4, H - 4);
      if (padBack > 0) {
        const label = `padded ${padBack.toFixed(1)}s*`;
        ctx.fillText(label, W - ctx.measureText(label).width - 4, H - 4);
      }
    }
    let globalMax = 0.001;
    if (sharedScale !== false) {
      series.forEach(({ data }) => {
        if (!data || !data.length) return;
        for (let i = 0; i < data.length; i++) if (data[i] > globalMax) globalMax = data[i];
      });
    }
    series.forEach(({ data, hz, color }) => {
      if (!data || !data.length) return;
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.4;
      const n = data.length;
      const max = sharedScale !== false ? globalMax : Math.max(...data, 0.001);
      for (let i = 0; i < n; i++) {
        const x = (i / hz) / duration * W;
        const y = H - (data[i] / max) * (H * 0.88) - H * 0.06;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    });
    if (markStart) {
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = "#FFB900";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(1, 0);
      ctx.lineTo(1, H);
      ctx.stroke();
      ctx.setLineDash([]);
      const fontSize = Math.max(10, Math.round(H * 0.16));
      ctx.font = `${fontSize}px ui-monospace, monospace`;
      ctx.fillStyle = "#FFB900";
      ctx.fillText("EEG marker", 6, fontSize + 3);
    }
    return canvas.getContext("2d").getImageData(0, 0, W, H);
  }

  const bases = {};
  function setupCanvas(id, series, sharedScale, markStart, padRegion) {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    bases[id] = { canvas, base: drawBase(canvas, series, sharedScale, markStart, padRegion, cfg.excludeWindows, id === "eegCanvas" ? cfg.eegWarnWindows : null) };
  }

  function drawPlayheads() {
    const t = video.currentTime || 0;
    Object.values(bases).forEach(({ canvas, base }) => {
      const ctx = canvas.getContext("2d");
      ctx.putImageData(base, 0, 0);
      const x = (t / duration) * canvas.width;
      ctx.beginPath();
      ctx.strokeStyle = "#00A4EF";
      ctx.lineWidth = 2;
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    });
    requestAnimationFrame(drawPlayheads);
  }

  // Chart data is passed inline (cfg.chartData), not fetched from a
  // separate JSON file — fetch() of local files is blocked by most
  // browsers' CORS policy when a page is opened directly via file://
  // (i.e. someone downloads this dataset and double-clicks the html
  // file rather than running a local server). Inlining means the page
  // works identically either way, with no setup required.
  // A modality can legitimately be absent for a segment (see
  // modality_presence in manifest.json, surfaced up front as this page's
  // status chips). Each panel is set up independently and defensively:
  // `data.imu` / `data.audio_ego` simply won't be in chartData when
  // absent, so check before indexing into it rather than letting one
  // missing key throw and silently kill every panel (and the playhead
  // loop) queued after it in this callback.
  Promise.resolve(cfg.chartData).then(data => {
    try {
      setupCanvas("eegCanvas", [
        { data: data.eeg_rms, hz: data.eeg_hz, color: "#00A4EF" },
      ], undefined, true);
    } catch (e) { console.error("eegCanvas setup failed", e); }
    try {
      if (data.imu) {
        // Each IMU unit gets its OWN rate, not the shared data.imu_hz.
        // pad_imu_to_window pads every device to the same window, so all four
        // span the full segment -- but they log at slightly different real
        // rates, so their downsampled arrays differ in length (P0037
        // phase3_012: imu_1 2724 points, imu_2/3/4 2629). With one shared hz
        // the shorter three ended 6 s before the right edge and read as a
        // dropout. n/duration maps each one across the full width, which is
        // what it actually covers.
        const imuHz = (a) => (a && a.length > 1 ? a.length / data.duration : data.imu_hz);
        setupCanvas("imuCanvas", [
          { data: data.imu.imu_1, hz: imuHz(data.imu.imu_1), color: "#7FBA00" },
          { data: data.imu.imu_2, hz: imuHz(data.imu.imu_2), color: "#FFB900" },
          { data: data.imu.imu_4, hz: imuHz(data.imu.imu_4), color: "#F25022" },
          { data: data.imu.imu_3, hz: imuHz(data.imu.imu_3), color: "#00A4EF" },
        ], undefined, false, data.imu_padding);
      }
    } catch (e) { console.error("imuCanvas setup failed", e); }
    try {
      if (data.audio_ego) {
        setupCanvas("audioCanvas", [
          { data: data.audio_ego, hz: data.audio_hz, color: "#00A4EF" },
        ]);
      }
    } catch (e) { console.error("audioCanvas setup failed", e); }
    requestAnimationFrame(drawPlayheads);
  });

  ["eegCanvas", "imuCanvas", "audioCanvas"].forEach(id => {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    canvas.addEventListener("click", e => {
      const rect = canvas.getBoundingClientRect();
      const frac = (e.clientX - rect.left) / rect.width;
      video.currentTime = frac * duration;
    });
  });
}
