import json,sys,re,os
from faster_whisper import WhisperModel
sys.path.insert(0,'.');import importlib;S=importlib.import_module(sys.argv[1])
L=[l[0] for sc in S.SCENES for l in sc['lines']]
m=WhisperModel('base.en',device='cpu',compute_type='int8')
W={'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten','12':'twelve'}
def norm(t):
    t=t.lower().replace('π','pi');t=re.sub(r"[^a-z0-9 ]"," ",t)
    return [W.get(w,w) for w in t.split()]
bad=[]
for i,l in enumerate(L):
    f=f'wav/{i}.wav'
    if not os.path.exists(f):bad.append((i,'missing'));continue
    import wave,numpy as np
    w=wave.open(f);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(x,language='en');h=' '.join(x.text for x in segs)
    a,b=norm(l),norm(h)
    import difflib;r=difflib.SequenceMatcher(None,a,b).ratio()
    if r<0.85:bad.append((i,round(r,2),l,h))
print('lines',len(L));[print(x) for x in bad]
