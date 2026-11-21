# python3 split.py <lid> : scene audio in <lid>/scene_<n>.mp3 -> per-line wavs <lid>/wav/<i>.wav + check report
import sys,os,re,json,importlib,difflib,subprocess,wave
import numpy as np
sys.path.insert(0,'.');lid=sys.argv[1];S=importlib.import_module('script_'+lid)
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
os.makedirs(f'{lid}/wav',exist_ok=True)
def norm(t):
    t=t.lower().replace('-',' ');t=re.sub(r"[^a-z0-9' ]"," ",t);return t.split()
from num2words import num2words
def pre(t):
    from gen_script import nw
    t=re.sub(r'\b(19\d\d|20\d\d)\b(?![.,]\d)',lambda m:num2words(int(m.group(1)),to='year'),t)
    t=re.sub(r'(\d)%',r'\1 percent',t)
    t=re.sub(r'(\d)([a-z])\b',r'\1 \2',t)
    return re.sub(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d*\.\d+|\d+',lambda m:' '+nw(m.group(0) if not m.group(0).startswith('.') else '0'+m.group(0))+' ',t)
def normh(t):
    out=[]
    for w in norm(pre(t)):
        w2=w.replace("'",'')
        if re.fullmatch(r'\d+',w2):out+=norm(num2words(int(w2)))
        else:out.append({'pie':'pi'}.get(w2,w2))
    return out
idx=0;report=[]
for si,sc in enumerate(S.SCENES):
    src=f'{lid}/scene_{si}.mp3';wv=f'{lid}/scene_{si}.wav'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-ar','16000','-ac','1',wv],check=True)
    w=wave.open(wv);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768;dur=len(x)/16000
    segs,_=m.transcribe(x,language='en',word_timestamps=True,beam_size=5)
    words=[];
    for s in segs:
        for ww in s.words:
            for t in normh(ww.word):words.append((t,ww.start,ww.end))
    hyp=[w[0] for w in words]
    ref=[];owner=[]
    for li,l in enumerate(sc['lines']):
        toks=[{'pie':'pi'}.get(t.replace("'",''),t.replace("'",'')) for t in norm(l[0])];ref+=toks;owner+=[li]*len(toks)
    sm=difflib.SequenceMatcher(None,ref,hyp,autojunk=False);r=sm.ratio()
    # global alignment (edit distance) so repeated phrases map in order
    n,mm=len(ref),len(hyp);D=np.zeros((n+1,mm+1),np.int32);D[:,0]=np.arange(n+1);D[0,:]=np.arange(mm+1)
    for i in range(1,n+1):
        for j in range(1,mm+1):
            D[i,j]=min(D[i-1,j]+1,D[i,j-1]+1,D[i-1,j-1]+(0 if ref[i-1]==hyp[j-1] else 1))
    amap={};i,j=n,mm
    while i>0 and j>0:
        if D[i,j]==D[i-1,j-1]+(0 if ref[i-1]==hyp[j-1] else 1):amap[i-1]=j-1;i-=1;j-=1
        elif D[i,j]==D[i-1,j]+1:i-=1
        else:j-=1
    starts=[];L=len(sc['lines'])
    for li in range(L):
        ri=[k for k,o in enumerate(owner) if o==li]
        ex=[amap[k] for k in ri if k in amap and ref[k]==hyp[amap[k]]]
        starts.append(words[ex[0]][1] if ex and len(ex)>=0.4*len(ri) else None)
    starts[0]=0.0
    # fill gaps by text length between known neighbours
    lens=[len(l[0]) for l in sc['lines']]
    k=0
    while k<L:
        if starts[k] is None:
            a=k-1;b=k
            while b<L and starts[b] is None:b+=1
            t0=starts[a];t1=starts[b] if b<L else dur
            # time from a's start to b's start shared by chars of lines a..b-1
            tot=sum(lens[a:b]);acc=lens[a]
            for q in range(k,b):starts[q]=t0+(t1-t0)*acc/tot;acc+=lens[q]
            k=b
        else:k+=1
    for q in range(1,L):
        if starts[q]<=starts[q-1]:starts[q]=starts[q-1]+0.3
    bounds=[max(0,s-0.08) for s in starts]+[dur]
    for li in range(len(sc['lines'])):
        a,b=bounds[li],bounds[li+1]
        seg=x[int(a*16000):int(b*16000)]
        with wave.open(f'{lid}/wav/{idx+li}.wav','wb') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(16000);o.writeframes((np.clip(seg,-1,1)*32767).astype(np.int16).tobytes())
        # per-line check
        lr=[t for k,t in enumerate(ref) if owner[k]==li];lh=[w[0] for w in words if a-0.05<=w[1]<b-0.05]
        rr=difflib.SequenceMatcher(None,lr,lh,autojunk=False).ratio()
        if rr<0.8:report.append((si,idx+li,round(rr,2),' '.join(lr),' '.join(lh)))
    idx+=len(sc['lines'])
    if r<0.9:report.append((si,'scene',round(r,2),'',''))
for r in report:print(r)
print('lines',idx,'flags',len(report))
