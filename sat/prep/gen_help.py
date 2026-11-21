import json,re
B=json.load(open('/home/claude/act-tutor/sat/drill-zone/bank.json'))
MATH={s['id'] for s in B['skills'] if s['sec']=='Math'}
NUM=r'[0-9][0-9,]*(?:\.[0-9]+)?|\.[0-9]+'
def pyexpr(e):
    s=e.replace('−','-').replace('×','*').replace('÷','/').replace('·','*').replace(',','').replace('²','**2').replace('³','**3').replace('π','pi')
    s=re.sub(r'√\s*\(','sqrt(',s);s=re.sub(r'√\s*(\d+(?:\.\d+)?)',r'sqrt(\1)',s)
    s=re.sub(r'(\d|\)|pi)\s*\(',r'\1*(',s);s=re.sub(r'(\d|\))\s*pi',r'\1*pi',s)
    return s
from math import sqrt,pi
def ev(e):
    try:
        v=eval(pyexpr(e),{'sqrt':sqrt,'pi':pi,'__builtins__':{}});return float(v)
    except Exception:return None
def num(r):
    r=r.strip().replace(',','').replace('−','-')
    m=re.match(r'^(-?\d+(?:\.\d+)?)(?:\s*/\s*(\d+))?',r)
    if not m:return None
    return float(m.group(1))/(float(m.group(2)) if m.group(2) else 1)
ARITH=re.compile(r'((?:[−\-]?\(?\s*(?:'+NUM+r')\s*\)?(?:²|³)?\s*(?:[+−\-×÷*/·]\s*\(?\s*[−\-]?(?:'+NUM+r'|π)\s*\)?(?:²|³)?\s*)+)|√\s*\d+|\(\s*[−\-]?\d+\s*\)²)\s*=\s*([−\-]?(?:'+NUM+r')(?:\s*/\s*\d+)?)')
def arith_lines(steps):
    out=[]
    for st in steps:
        t=st.split(': ',1)[-1] if ': ' in st[:60] else st
        for m in ARITH.finditer(t):
            e=m.group(1).strip().rstrip('=').strip();r=m.group(2).strip()
            if not re.search(r'[+−\-×÷*/²√·]',e.lstrip('−-')):continue
            v=ev(e);n=num(r)
            if v is None or n is None or abs(v-n)>1e-6*max(1,abs(n)):continue
            out.append((e,r))
    seen=set();res=[]
    for e,r in out:
        if e not in seen:seen.add(e);res.append((e,r))
    return res
def desmos_from_tool(tool):
    m=re.search(r'Desmos[^:]*:\s*(.+)',tool)
    if not m:return []
    t=m.group(1)
    t=re.split(r';|, click|, then click|\. Read|, read|, the one|— ',t)[0]
    t=re.sub(r'^(graph|type|put|solve)\s+','',t.strip(),flags=re.I)
    parts=re.split(r'\s+and\s+|,\s*then\s+|\s+then\s+',t)
    out=[]
    for p in parts:
        p=re.sub(r'^(graph|type|solve)\s+','',p.strip(),flags=re.I).strip(' .')
        p=p.replace('^','^')
        if re.search(r'[0-9x]',p) and re.search(r'[=(\[]|[+−×÷*/^]',p) and len(p)<70 and not re.search(r'\b(each|choice|the|it|both|table)\b',p):out.append(p)
    return out
def keys(expr):
    e=expr.replace(' ','').replace(',','');out=[];i=0
    while i<len(e):
        c=e[i]
        if c in '0123456789.':
            j=i
            while j<len(e) and e[j] in '0123456789.':j+=1
            out.append(e[i:j]);i=j;continue
        out.append({'π':'2nd ÷ (π)','√':'2nd x² (√)','²':'x²','³':'^ 3','·':'×'}.get(c,('(−)' if c in '−-' and (i==0 or e[i-1] in '(×÷+−-*/') else c)))
        i+=1
    return ' › '.join(out+['enter'])
H={}
for q in B['qs']:
    if q['skill'] not in MATH:continue
    ar=arith_lines(q['steps']);dl=desmos_from_tool(q['tool'])
    d=[];c=[]
    for e in dl:d.append('Type '+e)
    for e,r in ar:
        d.append('Type '+e);c+=['Type '+e+': '+keys(e),'= '+r]
    H[q['id']]=dict(d=d,c=c)
json.dump(H,open('/home/claude/act-tutor/sat/prep/qhelp.json','w'),ensure_ascii=False,separators=(',',':'))
nd=sum(1 for v in H.values() if v['d']);nc=sum(1 for v in H.values() if v['c'])
print(len(H),'with desmos',nd,'with calc',nc)
import random;random.seed(5)
for k in random.sample(list(H),14):print(k,H[k]['d'])
none=[k for k,v in H.items() if not v['d']]
import collections;print(collections.Counter(k.rsplit('-',1)[0] for k in none))
