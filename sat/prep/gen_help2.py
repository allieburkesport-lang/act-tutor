import json,re,html
exec(open('/home/claude/sat/prep/gen_help.py').read().split('H={}')[0])
def plain(h):
    h=re.sub(r'<br\s*/?>','\n',h);h=re.sub(r'<[^>]+>',' ',h);return html.unescape(h)
MC=r'[0-9xy()+−\-×÷*/^²³.|√π ]'
EQ=re.compile(r'((?:[fgh]\(x\)|y)\s*=\s*'+MC+r'+|'+MC+r'*[0-9x]'+MC+r'*(?:=|≤|≥|<|>)'+MC+r'+)')
def is_num_expr(p):
    p=p.strip()
    if not re.fullmatch(r'[0-9.,()+−\-×÷*/²³√π ]+',p):return False
    if re.fullmatch(r'[−\-]?[0-9.,]+',p):return False
    if re.fullmatch(r'[0-9]+\s*/\s*[0-9]+',p):return False
    if not re.search(r'[0-9]',p):return False
    return ev(p) is not None
def fmt(v):
    return str(int(round(v))) if abs(v-round(v))<1e-9 else f'{v:.4f}'.rstrip('0').rstrip('.')
def build(q):
    pq=plain(q['q']);lines=[];calc=[];note=''
    # 1) equations / functions written in the question
    for ln in re.split(r'\n|(?<=[?.])\s',pq):
        for m in EQ.finditer(ln):
            e=m.group(1).strip().strip('.,?')
            if not re.search(r'[xy]',e) or e.startswith('('):continue
            if re.fullmatch(r'[xy]\s*[<>≤≥=]\s*[−\-]?\d+',e):continue
            if len(e)<5:continue
            lines.append('Type '+e)
    fm=re.search(r'\b([fgh])\((−?\d+(?:\.\d+)?)\)',pq)
    if fm and any(l.startswith('Type '+fm.group(1)+'(x)') for l in lines):lines.append(f'Type {fm.group(1)}({fm.group(2)})')
    # 2) equivalent-expression questions: original + each choice
    m=re.search(r'equivalent to (.+?)\?',pq)
    if m and q.get('ch') and re.search(r'x',m.group(1)):
        lines=['Type y = '+m.group(1).strip()]+[f'Type y = {c}   (choice {"ABCD"[i]})' for i,c in enumerate(q['ch'])];note='The choice whose graph lies exactly on top of the first one is right.'
    # 3) data sets
    dm=re.search(r'data set(?: is|:)\s*([0-9 ,.]+[0-9])',pq)
    if dm:
        arr=re.sub(r'\s+','',dm.group(1));lines+=[f'Type mean([{arr}])',f'Type median([{arr}])']
    # 4) a one-letter equation from the steps (plug-in questions)
    if q['skill']!='sys' and not any(re.search(r'x',l[5:]) and not re.search(r'y',l[5:]) for l in lines):
        for st in q['steps']:
            t=st.split(': ',1)[-1].strip()
            if re.fullmatch(MC+r'*x'+MC+r'*=\s*[−\-]?[0-9.]+',t) and not re.search(r'y',t) and len(t)>6 and re.search(r'[0-9]\s*x|\(',t):lines.append('Type '+t);break
    # 5) arithmetic in the steps (Desmos and calculator)
    for st in q['steps']:
        t=st.split(': ',1)[-1] if ': ' in st[:60] else st
        for piece in re.split(r'=|→|,\s*so\b',t):
            p=piece.strip().rstrip('.')
            p=re.sub(r'^[A-Za-z ]+:\s*','',p)
            if re.fullmatch(r'[0-9.,]+\s*π',p):continue
            if is_num_expr(p) and re.search(r'[+−\-×÷*/²√π(]',p.lstrip('−-')) and not re.fullmatch(r'\(?[−\-]?\d+\)?',p):
                v=ev(p);r=fmt(v)
                if 'π' in p:
                    k=v/pi;r=f'{fmt(v)}  (= {fmt(k)}π)'
                lines.append('Type '+p);p2=re.sub(r'(?<=\d),(?=\d{3})','',p);calc+=['Type '+p2+': '+keys(p2),'= '+r]
    # dedupe
    lines=[re.sub(r'(?<=\d),(?=\d{3})','',l) for l in lines]
    seen=set();d=[]
    for l in lines:
        if l not in seen:seen.add(l);d.append(l)
    seen=set();c=[]
    for i in range(0,len(calc),2):
        if calc[i] not in seen:seen.add(calc[i]);c+=calc[i:i+2]
    if q['skill']=='equiv':c=[];d=[l for l in d if 'y =' in l]
    return dict(d=d[:8],c=c[:10],n=note)
H={q['id']:build(q) for q in B['qs'] if q['skill'] in MATH}
json.dump(H,open('/home/claude/act-tutor/sat/prep/qhelp.json','w'),ensure_ascii=False,separators=(',',':'))
import collections
print('desmos',sum(1 for v in H.values() if v['d']),'calc',sum(1 for v in H.values() if v['c']),'of',len(H))
print(collections.Counter(k.rsplit('-',1)[0] for k,v in H.items() if not v['d']))
import random;random.seed(11)
Q={q['id']:q for q in B['qs']}
for k in random.sample(list(H),25):print(k,'|',plain(Q[k]['q'])[:70].replace('\n',' '),'|',H[k]['d'],'|',H[k]['c'][1::2])
