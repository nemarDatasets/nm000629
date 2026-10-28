# EgoBrain-Mini — private BIDS conversion with original source

40 participants, 1,562 Phase-2 action segments, 32-channel EEG at 256 Hz (63.0028 raw EEG hours), four IMU sensors,
16 kHz microphone audio and egocentric video. CC-BY-NC-4.0, non-commercial research only; original access and no-redistribution
terms remain in force. Cite Lin et al., EgoBrain: Synergizing Minds and Eyes For Human Action Understanding, ICLR 2026,
arXiv:2506.01353; https://huggingface.co/datasets/ut-vision/EgoBrain-Mini and https://lin-nie.github.io/EgoBrain/.

## Contents and source fidelity
- sub-*/eeg: native Mini raw EEG in BrainVision float32, unchanged microvolt values and native 256 Hz. All values checked
  against original arrays; no conversion filtering, resampling or rereferencing. Original EDF labels were empirically checked
  against Mini waveforms for all participants. No source EDFs from full EgoBrain are deposited.
- sub-*/motion: separate native sensor streams, logger-relative timing, actual per-device rates, padding provenance and
  quality flags. No source samples are silently removed.
- sub-*/beh: original recorded audio and audiovisual clips, technical metadata and scans linkage. Redaction windows retained.
- derivatives/egobrain-clean: unchanged author-processed arrays. Their channel labels use the explicitly documented same-order
  processing inference; this is not a new clean-array waveform claim.
- stimuli/: experimental BEP044-shaped recorded-experience catalog; BEP047-shaped subject media. These proposals are open,
  not accepted released schemas. Recorded experience is not a claim of externally presented experimental stimuli. Canonical
  events use experience references; standard stimulus aliases are an opt-in benchmark compatibility table under code/.
- sourcedata/egobrain-mini-original/: the COMPLETE 17,520-path Mini source copy, with documented participant-clock shifts and disabled
  LFS packaging attributes. Signal/media bytes remain unchanged; original and deposited hashes are recorded separately.
- code/: tested reader adapter/example and dependency information for EEG/audio/video partial reads and Torch batching.

## Privacy and access — private only
BIDS acquisition times are de-identified to an artificial epoch, and the deposited source metadata uses a documented per-participant shift
to January 1900; exact unmodified originals and shift key remain on Voyager, outside the deposit. Source audio contains voices and video may contain identifying context/bystanders. Original author
redactions are preserved; no claim of full media anonymization is made. This upload is a PRIVATE author-review copy under
Bruno's authorization, not a public release. The authors' review is required before online/public availability. Never request
publication from this lane. Source-copy transformations are explicit and auditable; review any remaining screening findings.

## Synchronization and validation scope
Use the source-released EEG-anchored clip origin and actual media timestamps. Partial reads are bounded to common measured
coverage; no independent physical synchronization calibration is asserted. Core BIDS validation and pinned-proposal profile
checks are distinct; ignored experimental media are not a released-schema compliance claim. No electrode coordinates are
invented and recording reference stays n/a pending author confirmation. Keep all provenance and source quality/redaction flags.

Source viewer comments: two subject-linked recording-day strings are omitted in the 40 shared-script copies; executable JavaScript is unchanged. See the per-file transformation manifest.
