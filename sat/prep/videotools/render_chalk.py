# Chalkboard teacher video renderer. usage: python3 render_chalk.py script_module out.mp4
import sys,os,json,math,subprocess,wave,importlib,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from teacher import teacher
sys.path.insert(0,'.');S=importlib.import_module(sys.argv[1]);OUT=sys.argv[2]
W,H,FPS=1280,720,24
FD='/home/claude/chalk/fonts/'
def F(sz,b=False):return ImageFont.truetype(FD+('Kalam-Bold.ttf' if b else 'Kalam-Regular.ttf'),sz)
CAPF=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else F(24)
COL={'w':(245,245,235),'b':(140,197,255),'g':(155,229,155),'y':(255,230,109),'r':(255,138,128),'p':(212,165,255),'o':(255,170,90)}
NAME={'b':'RULE','g':'EXAMPLE','y':'REMEMBER','r':'TRAP','p':'MATH'}
# ---------- board background ----------
def board():
    rng=np.random.default_rng(3);base=np.zeros((H,W,3),np.float32)+np.array([38,52,46],np.float32)
    base+=rng.normal(0,4,(H,W,1));yy,xx=np.mgrid[0:H,0:W];v=1-0.35*(((xx-W/2)/(W/1.3))**2+((yy-H/2)/(H/1.3))**2)
    base*=v[...,None];im=Image.fromarray(np.clip(base,0,255).astype(np.uint8))
    d=ImageDraw.Draw(im);fr=(122,80,42)
    for t in range(18):d.rectangle((t,t,W-1-t,H-1-t),outline=tuple(int(c*(0.8+0.2*math.sin(t/3))) for c in fr))
    d.rectangle((18,18,W-19,H-19),outline=(20,28,24),width=2)
    # chalk smudges
    sm=Image.new('L',(W,H),0);sd=ImageDraw.Draw(sm)
    for _ in range(14):x,y=rng.integers(60,W-60),rng.integers(60,H-100);sd.ellipse((x-90,y-20,x+90,y+20),fill=int(rng.integers(6,14)))
    sm=sm.filter(ImageFilter.GaussianBlur(25));im=Image.composite(Image.new('RGB',(W,H),(200,210,200)),im,sm)
    # color key
    d=ImageDraw.Draw(im);x=W-40;f=F(17)
    for k in ['o','p','r','y','g','b']:
        t=NAME.get(k,'CARRIED');tw=d.textlength(t,font=f);x-=tw+28;d.ellipse((x,36,x+12,48),fill=COL[k]);d.text((x+16,29),t,font=f,fill=COL[k])
    return im.convert('RGBA')
BASE=board()
# ---------- text with inline orange ----------
def segs(text,col):
    out=[];pos=0
    for m in re.finditer(r'\{o\|([^}]*)\}',text):
        if m.start()>pos:out.append((text[pos:m.start()],col))
        out.append((m.group(1),'o'));pos=m.end()
    if pos<len(text):out.append((text[pos:],col))
    return out
def item_img(it,maxw=880):
    kind,text,sz=it;text=text.replace('⅓','1/3').replace('  →  ',', so ').replace(' → ',', so ').replace('→','so');f=F(sz,True);col=kind
    sg=segs(text,col);# measure / wrap simply on full string width
    tmp=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    total=sum(tmp.textlength(t,font=f) for t,_ in sg)
    while total>maxw and sz>24:sz-=2;f=F(sz,True);total=sum(tmp.textlength(t,font=f) for t,_ in sg)
    hgt=int(sz*1.45);im=Image.new('RGBA',(int(total)+20,hgt+10),(0,0,0,0));d=ImageDraw.Draw(im);x=4
    for t,c in sg:
        d.text((x+1,3),t,font=f,fill=COL[c]+(90,));d.text((x,2),t,font=f,fill=COL[c]+(255,))
        if c=='o' and t.strip():tw=d.textlength(t,font=f);d.line((x,hgt-4,x+tw,hgt-4),fill=COL['o']+(255,),width=3)
        x+=d.textlength(t,font=f)
    # chalk texture: knock out speckles
    a=np.array(im);rng=np.random.default_rng(len(text));mask=rng.random(a.shape[:2])<0.10;a[mask,3]=(a[mask,3]*0.45).astype(np.uint8)
    return Image.fromarray(a)
def title_img(t):return item_img(('w',t,46))
# ---------- audio timeline ----------
def wav_dur(p):w=wave.open(p);return w.getnframes()/w.getframerate()
os.makedirs('build',exist_ok=True)
lines=[];t=2.6 # thumbnail intro 2.6 s
for si,sc in enumerate(S.SCENES):
    t+=0.5
    for li,(say,it) in enumerate(sc['lines']):
        idx=len(lines);p=f'wav/{idx}.wav';d=wav_dur(p)
        lines.append(dict(scene=si,say=say,it=it,start=t,dur=d,wav=p));t+=d+0.45
    t+=0.4
TOTAL=t+1.5
# build narration track
sr=16000;track=np.zeros(int(TOTAL*sr)+sr,np.float32)
for L in lines:
    w=wave.open(L['wav']);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768;s=int(L['start']*sr);track[s:s+len(x)]+=x
env=np.abs(track);win=int(sr/FPS)
def mouth_at(tt):
    s=int(tt*sr);seg=env[s:s+win];return float(min(1,(seg.mean() if len(seg) else 0)*9))
with wave.open('build/narr.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(track,-1,1)*32767).astype(np.int16).tobytes())
# ---------- layout per scene ----------
LEFT,TOP=60,130
def layout(si):
    y=TOP;pos=[]
    for it in S.SCENES[si].get('pre',[]):
        im=item_img(it);PRE.setdefault(si,[]).append((im,(LEFT,y)));y+=im.height+14
    for L in [l for l in lines if l['scene']==si]:
        it=L['it']
        if it is None or it[0] in ('x','ok'):pos.append(None);continue
        if it[0]=='choices':
            ims=[item_img(('w',f'{"ABCD"[k]})  {c}',44)) for k,c in enumerate(it[1])];hs=[]
            for im in ims:hs.append((LEFT+20,y));y+=im.height+6
            pos.append(('choices',ims,hs));continue
        im=item_img(it);pos.append(('item',im,(LEFT,y)));y+=im.height+14
    return pos
PRE={}
LAY={si:layout(si) for si in range(len(S.SCENES))}
TIT={si:title_img(sc['title']) for si,sc in enumerate(S.SCENES)}
# ---------- caption ----------
def caption(img,text):
    d=ImageDraw.Draw(img);words=text.split();rows=[];cur=''
    for wd in words:
        if d.textlength(cur+' '+wd,font=CAPF)>W-420:rows.append(cur);cur=wd
        else:cur=(cur+' '+wd).strip()
    rows.append(cur);rows=rows[-2:];hh=18+30*len(rows)
    ov=Image.new('RGBA',(W,hh),(0,0,0,170));img.alpha_composite(ov,(0,H-hh))
    for k,r in enumerate(rows):d.text((40,H-hh+10+30*k),r,font=CAPF,fill=(255,255,255))
# ---------- thumbnail ----------
def thumb():
    im=BASE.copy();d=ImageDraw.Draw(im)
    d.text((70,90),'SAT MATH',font=F(46,True),fill=COL['y'])
    yy=170
    for ln in S.TOPIC.split('\n'):d.text((70,yy),ln,font=F(104,True),fill=COL['w']);yy+=125
    d.text((74,yy+20),'Formulas · worked examples · traps',font=F(34),fill=COL['g'])
    tch=teacher(0.2,False,1.0).resize((390,468));im.alpha_composite(tch,(W-430,H-470))
    return im
TH=thumb();TH.convert('RGB').save(OUT.replace('.mp4',' - Thumbnail.jpg'),quality=92)
# ---------- frames ----------
def write_frac(L):
    it=L['it'];wt=min(L['dur']*0.75,0.6+0.045*len(str(it[1]) if it else '0'));return wt
proc=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','build/narr.wav',
  '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart','build/body.mp4'],stdin=subprocess.PIPE)
nf=int(TOTAL*FPS);cache={}
for fi in range(nf):
    tt=fi/FPS
    if tt<2.6:proc.stdin.write(TH.convert('RGB').tobytes());continue
    cur=[l for l in lines if l['start']-0.5<=tt] ;L=cur[-1] if cur else lines[0];si=L['scene']
    sl=[l for l in lines if l['scene']==si];lay=LAY[si]
    key=(si,)
    im=BASE.copy();im.alpha_composite(TIT[si],(LEFT,62))
    for pim,pxy in PRE.get(si,[]):im.alpha_composite(pim,pxy)
    writing=False;wx=wy=None
    for k,l2 in enumerate(sl):
        if l2['start']>tt:break
        p=lay[k];it=l2['it'];el=tt-l2['start'];fr=min(1,max(0,el/write_frac(l2))) if it else 1
        if p is None:
            if it and it[0] in ('x','ok'):
                ci=it[1];cp=[q for q in lay if q and q[0]=='choices'][-1];x,y=cp[2][ci];cim=cp[1][ci]
                d=ImageDraw.Draw(im);f2=min(1,el/0.7)
                if it[0]=='x':
                    d.line((x,y+cim.height//2,x+int(cim.width*f2),y+cim.height//2),fill=COL['r'],width=6)
                    if f2>=1:d.text((x+cim.width+14,y+6),'X',font=F(40,True),fill=COL['r'])
                else:
                    d.rounded_rectangle((x-12,y-4,x-12+int((cim.width+24)*f2),y+cim.height+2),12,outline=COL['g'],width=5)
                if f2<1:writing=True;wx,wy=x+int(cim.width*f2),y+cim.height//2
            continue
        if p[0]=='item':
            img,(x,y)=p[1],p[2];w=int(img.width*fr)
            if w>0:im.alpha_composite(img.crop((0,0,w,img.height)),(x,y))
            if fr<1:writing=True;wx,wy=x+w,y+img.height//2
        else:
            ims,hs=p[1],p[2];n=len(ims);tot=fr*n
            for j in range(n):
                f3=min(1,max(0,tot-j));w=int(ims[j].width*f3)
                if w>0:im.alpha_composite(ims[j].crop((0,0,w,ims[j].height)),hs[j])
                if 0<f3<1:writing=True;wx,wy=hs[j][0]+w,hs[j][1]+ims[j].height//2
    if writing and wx is not None:
        g=Image.new('RGBA',(60,60),(0,0,0,0));gd=ImageDraw.Draw(g);gd.ellipse((10,10,50,50),fill=(255,240,150,110));g=g.filter(ImageFilter.GaussianBlur(6));im.alpha_composite(g,(wx-30,wy-30))
        ImageDraw.Draw(im).ellipse((wx-5,wy-5,wx+5,wy+5),fill=(255,250,200))
    speaking=L['start']<=tt<=L['start']+L['dur']
    m=mouth_at(tt) if speaking else 0;blink=(fi%84)<3;bob=int(3*math.sin(tt*2.2))
    tch=teacher(m,blink,1.0 if writing else 0.0,bob);im.alpha_composite(tch,(W-310,H-372-0))
    if speaking or tt<L['start']+L['dur']+0.45:caption(im,L['say'])
    proc.stdin.write(im.convert('RGB').tobytes())
proc.stdin.close();proc.wait()
# embed cover art
subprocess.run(['ffmpeg','-loglevel','error','-y','-i','build/body.mp4','-i',OUT.replace('.mp4',' - Thumbnail.jpg'),'-map','0','-map','1','-c','copy','-c:v:1','mjpeg','-disposition:v:1','attached_pic','-movflags','+faststart',OUT],check=True)
json.dump([dict(i=i,start=round(l['start'],2),say=l['say'],scene=l['scene']) for i,l in enumerate(lines)],open(OUT.replace('.mp4',' - timings.json'),'w'),indent=0)
print('done',round(TOTAL,1),'s')
