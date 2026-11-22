# usage: python3 publish.py DIR VIDEO_ID SCRIPT_NAME "commit title"
import sys, json, subprocess, shutil, os
D, vid, script, title = sys.argv[1:5]
R = '/home/claude/act-tutor/sat/prep'
shutil.copy(f'{D}/video.mp4', f'{R}/videos/{vid}.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{D}/thumb.png', '-q:v', '3', f'{R}/videos/{vid}.jpg'], check=True)
v = json.load(open(f'{R}/videos/videos.json')); v[vid].update(src=f'videos/{vid}.mp4', poster=f'videos/{vid}.jpg', chapters=json.load(open(f'{D}/chapters.json')), v2=True)
json.dump(v, open(f'{R}/videos/videos.json', 'w'), indent=1, ensure_ascii=False)
os.makedirs(f'{R}/videotools/v2/{vid}', exist_ok=True)
for f in (script, 'beats.json'): shutil.copy(f'{D}/{f}', f'{R}/videotools/v2/{vid}/{f}')
for f in ('common.py', 'engine.py', 'fetch.py', 'qa.py', 'publish.py'): shutil.copy(f'/home/claude/v2/{f}', f'{R}/videotools/v2/{f}')
sh = lambda *a: subprocess.run(a, cwd='/home/claude/act-tutor', check=True)
sh('git', 'add', f'sat/prep/videos/{vid}.mp4', f'sat/prep/videos/{vid}.jpg', 'sat/prep/videos/videos.json', 'sat/prep/videotools/v2')
sh('git', 'commit', '-qm', f'Remake: {title} video in the new animated style\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_011qG37i91ZKBgh4bTMod1hU')
sh('git', 'pull', '-q', '--rebase'); sh('git', 'push', '-q'); print('published', vid)
