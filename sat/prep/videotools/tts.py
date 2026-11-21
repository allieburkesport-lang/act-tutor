# one narration request per board (scene): python3 tts.py <lid> [scene indexes...]
import sys,json,importlib;sys.path.insert(0,'.')
S=importlib.import_module('script_'+sys.argv[1])
only=[int(x) for x in sys.argv[2:]] or list(range(len(S.SCENES)))
V='3c2b83c0-2e0a-5ae8-998a-a5fe71b7eccd'
print(json.dumps([{'index':i,'params':{'model':'text2speech_v2','prompt':' '.join(l[0] for l in S.SCENES[i]['lines']),'voice_id':V,'voice_type':'preset','variant':'seed_speech'}} for i in only],ensure_ascii=False))
