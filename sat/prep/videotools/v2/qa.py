# usage: python3 qa.py DIR  -> whisper check of every line + frame sheet from the video
import sys, json, re, subprocess, numpy as np
from faster_whisper import WhisperModel
from PIL import Image
D = sys.argv[1]; N = json.load(open(f'{D}/beats.json')); m = WhisperModel('base.en', compute_type='int8')
W2N = {'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}
def norm(s): return [w for w in re.sub(r'[^a-z ]', ' ', s.lower()).split()]
bad = 0
for i, t in enumerate(N):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{D}/wav/{i}.wav', '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.int16).astype(np.float32) / 32768); h = ' '.join(s.text for s in segs)
    a = [w for w in norm(t) if not re.fullmatch(r'(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|point|and|zero|million)', w)]
    b = norm(h); miss = [w for w in a if w not in b]
    if len(miss) > 1: bad += 1; print(i, 'MISSING', miss, '|', h)
print('lines checked:', len(N), 'problems:', bad)
T = json.load(open(f'{D}/timing.json')); ims = []
for i, (s, d) in enumerate(zip(T['starts'], T['durs'])):
    f = f'{D}/st/v{i:02d}.png'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{s + d * .85:.2f}', '-i', f'{D}/video.mp4', '-frames:v', '1', f]); ims.append(Image.open(f).resize((320, 180)))
c = Image.new('RGB', (1280, 180 * ((len(ims) + 3) // 4)))
for i, im in enumerate(ims): c.paste(im, ((i % 4) * 320, (i // 4) * 180))
c.save(f'{D}/vsheet.png'); print('dur', round(sum(T['durs']), 1))
