"""Lazy benchmark-style Mini multimodal adapter using real neuralset Audio/Eeg events.
BEP044 catalog resolution and explicit recording/file time mapping; AV frames use actual PTS.
No automatic download, hidden resampling, inference of physical synchrony or full media preloading.
"""
import csv
import json
import math
import time
from pathlib import Path
import numpy as np
import torch
import av
from PIL import Image
from neuralset.events import etypes as E


def safe_path(root,relative):
    root=Path(root).resolve()
    if not isinstance(relative,str) or not relative or '\\' in relative or ':' in relative or any(ord(c)<32 or ord(c)==127 for c in relative):
        raise ValueError('ambiguous/non-POSIX relative media path')
    p=Path(relative)
    if p.is_absolute() or '..' in p.parts:raise ValueError('unsafe relative media path')
    p=(root/p).resolve()
    if not p.is_relative_to(root):raise ValueError('media path escapes root')
    if not p.is_file():raise FileNotFoundError(p)
    return p


def read_tsv(p):
    with Path(p).open() as f:return list(csv.DictReader(f,delimiter='\t'))


class MiniStimulusDataset(torch.utils.data.Dataset):
    """getitem -> {'eeg','audio','video','video_times','label','subject','segment_id'}.
    EEG [C,T] volts, audio [T,C] float32, video [F,C,H,W] uint8. Windows remain within
    common duration. Frame requests at fixed offsets sample native frames by PTS, not resampled video.
    Neuralset EEG returns lazy MNE Raw; neuralset Audio handles offset/duration partial reads.
    """
    def __init__(self,root,window_s=1.,frames_per_second=2,max_records=None):
        self.root=Path(root);self.window_s=float(window_s);self.fps=int(frames_per_second)
        if not math.isfinite(window_s) or not math.isfinite(frames_per_second) or window_s<=0 or frames_per_second<=0:
            raise ValueError('finite positive window/frame rate required')
        self.records=read_tsv(self.root/'benchmark_index.tsv')
        if max_records and len(self.records)>max_records:
            # Sample across the full Mini inventory, not only the first participant.
            positions=np.linspace(0,len(self.records)-1,max_records,dtype=int)
            self.records=[self.records[i] for i in positions]
        self.catalog={}
        for r in read_tsv(self.root/'stimuli/stimuli.tsv'):
            if r['stimulus_id'] in self.catalog:raise ValueError('duplicate stimulus id')
            self.catalog[r['stimulus_id']]=r
        self.windows=[]
        for i,r in enumerate(self.records):
            if r.get('media_role')!='recorded_experience_not_presented_stimulus':
                raise ValueError('Mini reader requires explicit recorded-experience mode/profile')
            for k in ('audio','video'):
                c=self.catalog[r[k+'_id']]
                if c['filename']!=r[k+'_file']:raise ValueError('catalog/event path disagreement')
                safe_path(self.root/'stimuli',c['filename'])
            # Keep benchmark smoke bounded, while checking beginning/middle/end of each selected recording.
            duration=float(r['duration'])
            if not math.isfinite(duration) or duration<0:raise ValueError('invalid common duration')
            if duration<self.window_s:continue
            for start in sorted({0.,max(0.,duration/2-self.window_s/2),max(0.,duration-self.window_s-1/256)}):
                # align EEG reads to a native sample index, then use that same time for audio/video.
                self.windows.append((i,math.floor(start*256)/256))
        if not self.windows:raise ValueError('no windows fit common stream coverage')

    def __len__(self):return len(self.windows)

    def __getitem__(self,index):
        i,start=self.windows[index];r=self.records[i];duration=self.window_s;timeline=r['segment_id']
        eeg_path=safe_path(self.root,r['eeg_file']);audio_path=safe_path(self.root/'stimuli',r['audio_file']);video_path=safe_path(self.root/'stimuli',r['video_file'])
        ev=E.Eeg(start=start,timeline=timeline,subject=r['subject'],filepath=str(eeg_path),offset=start,duration=duration,frequency=256.)
        raw=ev.read()
        try:eeg=torch.from_numpy(raw.get_data().astype(np.float32))
        finally:raw.close()
        sound=E.Audio(start=start,timeline=timeline,filepath=str(audio_path),offset=start,duration=duration,frequency=16000.)
        audio=sound.read()
        requests=start+np.arange(round(duration*self.fps))/self.fps
        frames=[];pts=[]
        with av.open(str(video_path)) as container:
            stream=container.streams.video[0]
            origin=int(stream.start_time or 0)
            container.seek(origin+int(start/float(stream.time_base)),stream=stream,backward=True)
            wanted=0
            for frame in container.decode(stream):
                if frame.pts is None:continue
                stamp=float((frame.pts-origin)*stream.time_base)
                while wanted<len(requests) and stamp+1e-9>=requests[wanted]:
                    im=frame.to_image().resize((160,90),Image.Resampling.BILINEAR)
                    frames.append(np.asarray(im).transpose(2,0,1).copy());pts.append(stamp);wanted+=1
                if wanted==len(requests):break
        if len(frames)!=len(requests):raise ValueError('video ended before requested common interval')
        events=read_tsv(safe_path(self.root,r['events_file']))
        overlap=[event for event in events if float(event['onset']) < start+duration and float(event['onset'])+float(event['duration']) > start]
        bad=any(event['trial_type'].startswith('bad_') for event in overlap)
        redacted=any(event['trial_type'].startswith('video_redacted') for event in overlap)
        return dict(eeg=eeg,audio=audio,video=torch.from_numpy(np.stack(frames)),
                    has_bad_eeg=bad,has_redacted_media=redacted,
                    video_times=torch.tensor(pts,dtype=torch.float64),requested_video_times=torch.tensor(requests,dtype=torch.float64),
                    label=r['task'],subject=r['subject'],segment_id=timeline,start=start,duration=duration,
                    media_role=r['media_role'],eeg_path=str(eeg_path),audio_path=str(audio_path),video_path=str(video_path))


def smoke(root,out,max_records=6):
    import hashlib
    import importlib.metadata
    import resource
    import soundfile as sf
    from torch.utils.data import DataLoader
    root=Path(root);out=Path(out);out.mkdir(exist_ok=True,parents=True)
    started=time.perf_counter();ds=MiniStimulusDataset(root,max_records=max_records);index_seconds=time.perf_counter()-started
    rows=[];worst_frame_error=0
    for k in range(len(ds)):
        t=time.perf_counter();batch=ds[k];lat=time.perf_counter()-t
        i,start=ds.windows[k];rec=ds.records[i]
        # Independent direct source slices verify the actual neuralset partial reads.
        proof=json.loads((root.parent/(root.name+'-reader-source.json')).read_text())
        rawroot=Path(proof['RawRoot']);src=rawroot/rec['subject'].removeprefix('sub-')/'segments/phase2'/rec['segment_id']
        data=np.load(src/'eeg/raw.npy',mmap_mode='r');n=round(ds.window_s*256);a=round(start*256)
        np.testing.assert_allclose(batch['eeg'].numpy(),data[:,a:a+n]*1e-6,rtol=2e-6,atol=1e-10)
        direct,sr=sf.read(src/'audio/ego.wav',start=round(start*16000),frames=round(ds.window_s*16000),always_2d=True,dtype='float32')
        assert sr==16000;np.testing.assert_array_equal(batch['audio'].numpy(),direct)
        error=(batch['video_times']-batch['requested_video_times']).numpy()
        meta=json.loads(safe_path(root/'stimuli',rec['video_file']).with_suffix('.json').read_text())
        assert np.all(error>=-1e-8) and np.max(error)<=1/meta['VideoFrameRate']+.002
        worst_frame_error=max(worst_frame_error,float(np.max(error)))
        rows.append(dict(segment=rec['segment_id'],start=start,seconds=lat,eeg_shape=list(batch['eeg'].shape),
                         audio_shape=list(batch['audio'].shape),video_shape=list(batch['video'].shape),frame_error_s=float(np.max(error)),
                         has_bad_eeg=batch['has_bad_eeg'],has_redacted_media=batch['has_redacted_media']))
        print('STIM_READER_WINDOW_OK',k+1,'/',len(ds),'s',round(lat,3),flush=True)
    # Actual torch batching over real neuralset reads, no model downloads/training.
    t=time.perf_counter();loader=DataLoader(ds,batch_size=min(4,len(ds)),shuffle=False,num_workers=0)
    batch=next(iter(loader));batch_seconds=time.perf_counter()-t
    # Exercise the existing neuralset Video.read API as well, rather than claiming only format compatibility.
    rec=ds.records[ds.windows[0][0]];vpath=safe_path(root/'stimuli',rec['video_file'])
    meta=json.loads(vpath.with_suffix('.json').read_text());t=time.perf_counter()
    video=E.Video(start=0.,timeline=rec['segment_id'],filepath=str(vpath),offset=0.,duration=1.,frequency=meta['VideoFrameRate'])
    clip=video.read()
    try:
        rgb=clip.get_frame(.25)
        assert rgb.ndim==3 and rgb.shape[-1]==3 and rgb.size>0
        neuralset_video_shape=list(rgb.shape)
    finally:clip.close()
    neuralset_video_seconds=time.perf_counter()-t
    versions={k:importlib.metadata.version(k) for k in ('torch','neuralset','av','soundfile','moviepy','mne')}
    with Path(E.__file__).open('rb') as f:api_hash=hashlib.file_digest(f,'sha256').hexdigest()
    result=dict(verdict='PASS',records=len(ds.records),windows=len(ds),index_seconds=index_seconds,
                per_window_seconds=[r['seconds'] for r in rows],median_seconds=float(np.median([r['seconds'] for r in rows])),
                worst_frame_selection_error_s=worst_frame_error,batch_seconds=batch_seconds,
                batch_shapes={k:list(v.shape) for k,v in batch.items() if isinstance(v,torch.Tensor)},
                neuralset_video_shape=neuralset_video_shape,neuralset_video_seconds=neuralset_video_seconds,
                peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,versions=versions,
                neuralset_etypes_sha256=api_hash,
                limits='File/index synchrony and decode selection checked; not independent physical cross-modal calibration. Latencies are sampled warm/cold filesystem observations, not whole-corpus throughput.')
    (out/'reader-smoke.json').write_text(json.dumps(result,indent=2));(out/'reader-windows.json').write_text(json.dumps(rows,indent=2))
    print('STIM_READER_PASS',json.dumps(result),flush=True)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--out',required=True);p.add_argument('--max-records',type=int,default=6)
    a=p.parse_args();smoke(a.root,a.out,a.max_records)
