import json,subprocess,sys,glob,os,wave
from PIL import Image
mp4=sys.argv[1];wd=sys.argv[2];tag=sys.argv[3]
T=json.load(open(mp4.replace('.mp4',' - timings.json')))
os.makedirs('chk/'+tag,exist_ok=True)
pts=[1.0]
for i,t in enumerate(T):
    w=wave.open(f'{wd}/{i}.wav');pts.append(t['start']+w.getnframes()/w.getframerate()*0.95)
for k,p in enumerate(pts):subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(p),'-i',mp4,'-frames:v','1','-vf','scale=300:-1',f'chk/{tag}/{k:02d}.jpg'])
fs=sorted(glob.glob(f'chk/{tag}/[0-9]*.jpg'));n=len(fs);rows=(n+4)//5
g=Image.new('RGB',(5*301,rows*170),'white')
for j,f in enumerate(fs):g.paste(Image.open(f),((j%5)*301,(j//5)*170))
g.save(f'chk/{tag}_sheet.jpg',quality=80);print(n)
