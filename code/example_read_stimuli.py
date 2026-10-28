"""Run in the configured Voyager Job environment; no training/model download.
Usage: python example_read_stimuli.py /path/to/mini-stim-bids
The adapter reads actual Neuralset Eeg/Audio events and native-PTS video frames lazily.
"""
import sys
from torch.utils.data import DataLoader
from stimulus_reader import MiniStimulusDataset

# Manifest/catalog paths are relative and data may be relocated as one BIDS tree.
dataset=MiniStimulusDataset(sys.argv[1],window_s=1.,frames_per_second=2,max_records=8)
loader=DataLoader(dataset,batch_size=4,shuffle=False,num_workers=0)
batch=next(iter(loader))
for key in ('eeg','audio','video','video_times','has_bad_eeg','has_redacted_media'):
    print(key,batch[key].shape,batch[key].dtype)
print('subject IDs:',batch['subject'])
print('source segment IDs:',batch['segment_id'])
