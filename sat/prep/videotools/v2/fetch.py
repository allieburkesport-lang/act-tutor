# usage: python3 fetch.py DIR  (reads "idx url" lines on stdin), converts to wav
import sys, subprocess
D = sys.argv[1]
for l in sys.stdin.read().split('\n'):
    l = l.strip()
    if not l: continue
    i, u = l.split()[:2]
    subprocess.run(['curl', '-sf', '-o', f'{D}/wav/{i}.mp3', u], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{D}/wav/{i}.mp3', '-ar', '24000', '-ac', '1', f'{D}/wav/{i}.wav'], check=True)
print('ok')
