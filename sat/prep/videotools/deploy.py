# deploy.py <lid> <mp4> : copy video to the site and register chapters
import sys,json,shutil,importlib
sys.path.insert(0,'/home/claude/chalk');lid,mp4=sys.argv[1],sys.argv[2]
S=importlib.import_module('script_'+lid)
V='/home/claude/act-tutor/sat/prep/videos/'
shutil.copy(mp4,V+lid+'.mp4');shutil.copy(mp4.replace('.mp4',' - Thumbnail.jpg'),V+lid+'.jpg')
T=json.load(open(mp4.replace('.mp4',' - timings.json')));ch=[[0,'Start']];seen=set()
for t in T:
    if t['scene'] not in seen:
        seen.add(t['scene'])
        if t['scene']>0:ch.append([int(t['start']),S.SCENES[t['scene']]['title']])
J=json.load(open(V+'videos.json'));J[lid]=dict(src=f'videos/{lid}.mp4',poster=f'videos/{lid}.jpg',chapters=ch)
json.dump(J,open(V+'videos.json','w'),indent=0,ensure_ascii=False);print('ok',lid,len(ch),'chapters')
