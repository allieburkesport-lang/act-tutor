# Build a chalkboard video script module (script_<lid>.py) from the lesson data.
import json,re,sys,html,random
from num2words import num2words
L=json.load(open('lessons_full.json'));MH=json.load(open('mh.json'))
B=json.load(open('/home/claude/act-tutor/sat/drill-zone/bank.json'))
LESSONS_OF={"lin1":["m1","m4"],"lin2":["t1"],"linf":["t1","a3"],"sys":["a2"],"ineq":["a5"],"equiv":["t2"],"nleq":["a1","a4"],"nlf":["t2","a1","a3"],"ratio":["a6"],"pct":["m2"],"data1":["d1"],"data2":["d3"],"prob":["d2"],"infer":["m2"],"claims":["d3"],"area":["t3","e1"],"lat":["e2"],"trig":["t3"],"circ":["t3"],"wic":["r1"],"tsp":["r5"],"cross":["r5"],"cid":["r2"],"coe":["r4"],"inf":["r3"],"bound":["s1","s4"],"fss":["s5","g3"],"trans":["s6"],"syn":["r6"]}
def plain(h,br=' '):
    h=re.sub(r'<sup>(.*?)</sup>',r'^\1',h or '');h=re.sub(r'<br\s*/?>',br,h);h=re.sub(r'<div class="stem">',br,h);h=re.sub(r'</?[a-zA-Z][^>]*>','',h);h=html.unescape(h).replace('[[','').replace(']]','')
    h=re.sub(r'\s*\((?:[^()]*?(?:practice test|Practice Test|[Yy]our |Nov\b|Patrick|Bluebook|Q\d)[^()]*)\)','',h)
    return re.sub(r'\s+',' ',h).strip()
def generic(t):
    return not re.search(r'Practice Test|practice test|Nov \d|Patrick|\bmin \d+ sec|Module \d',t)
def nw(n):
    s=n.replace(',','')
    if '.' in s:
        a,b=s.split('.');return (num2words(int(a)) if a else 'zero')+' point '+' '.join(num2words(int(c)) for c in b)
    return num2words(int(s))
FR={'½':' one half ','¼':' one fourth ','¾':' three fourths ','⅓':' one third ','⅔':' two thirds '}
SUP={'²':' squared','³':' cubed','ˣ':' to the x','ᵗ':' to the t','ⁿ':' to the n','⁶':' to the sixth','⁴':' to the fourth','⁵':' to the fifth'}
APOS=False;PUNCT=True
def speak(t):
    t=re.sub(r'\bT([12])\b',lambda m:'Text '+('one' if m.group(1)=='1' else 'two'),t)
    t=re.sub(r'\bS ?([12])\b',lambda m:'sentence '+('one' if m.group(1)=='1' else 'two'),t)
    t=re.sub(r'(?<![\w])-(s|ing|ed)\b',lambda m:{'s':'s ending','ing':'i n g ending','ed':'e d ending'}[m.group(1)],t)
    t=re.sub(r'(\d),(\d{3})\b',r'\1\2',t);t=re.sub(r'(\d) ?-([a-z])',r'\1 \2',t)
    t=re.sub(r'([A-Za-z])-(\d)',r'\1 \2',re.sub(r'_{3,}',' blank ',plain(t,'. ')))
    t=re.sub(r'(\w)…(\w)',r'\1 \2',t);t=t.replace('’ … ','’ and ').replace(' … ',', ').replace('…','')
    t=re.sub(r'“(\w+) ”',r'“\1” and the words after it',t)
    t=re.sub(r'\b([A-Za-z]{2,}(?: [a-z]{2,})?)/([a-z]{2,}(?: [a-z]{2,})?)\b',r'\1 or \2',t)
    t=re.sub(r'(^|[\s,(])’s\b',r'\1apostrophe s',t);t=re.sub(r'(^|\s)s’(?=[\s,.]|$)',r'\1s apostrophe',t)
    if APOS:t=re.sub(r"(\w)['’]s\b",r'\1 apostrophe s',t);t=re.sub(r"(\w)s['’](?=[\s,.;:]|$)",r'\1s apostrophe',t) if APOS else t
    t=re.sub(r'(?<=[a-z0-9)²³ˣ]) · ([a-z0-9(]\S*)',lambda m:(' times ' if not re.match(r'[a-z]{3,}',m.group(1)) else '. ')+m.group(1),t).replace(' · ','. ')
    t=re.sub(r'\(([^()]*[+−\-][^()]*)\)²',r' \1, all squared',t)
    t=re.sub(r'\((−?[\d.]+|[a-z]),\s*(−?[\d.]+|[a-z])\)',r'point \1, \2',t)
    t=re.sub(r'\s\(([^()]*(?:\([^()]*\))?[^()]*)\)',r', \1,',t)
    t=t.replace(')(',', times (')
    t=re.sub(r'(?<=[a-eA-E0-9xy)π])\(',' times (',t)
    t=re.sub(r'\|([^|]+)\|',r' the absolute value of \1 ',t)
    t=t.replace('ft²','square feet').replace('in²','square inches');t=re.sub(r'(\d)\s*GB',r'\1 gigabytes',t).replace('GB','gigabyte')
    t=re.sub(r'(\d) in\b(?=\s+by|[,.]|$)',r'\1 inches',t)
    t=re.sub(r'\bmph\b','miles per hour',t).replace(' vs. ',' versus ').replace(' vs ',' versus ')
    t=re.sub(r'(\d+)(st|nd|rd|th)\b',lambda m:num2words(int(m.group(1)),to='ordinal'),t)
    t=re.sub(r'\b((?:\d+|[a-z]) [a-z]+) / ((?:\d+ )?[a-z]+)',r'\1 over \2',t)
    for a,b in FR.items():t=t.replace(a,b)
    for a,b in SUP.items():t=t.replace(a,b)
    t=re.sub(r'\$(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)',lambda m:nw(m.group(1))+' dollars',t)
    t=re.sub(r'\b([a-zA-Z])\(([^()]*)\)',lambda m:m.group(1)+' of '+m.group(2) if m.group(1) in 'fgPh' else m.group(0),t)
    t=re.sub(r'(^|[\s(=,:])[−\-](?=\d|[a-z]\b)',r'\1 negative ',t)
    t=re.sub(r'(\d+)\s*/\s*(\d+)',lambda m:nw(m.group(1))+' over '+nw(m.group(2)),t)
    t=re.sub(r'\b([a-z0-9]{1,3})/([a-z0-9]{1,3})\b',r'\1 over \2',t).replace(' / ',' or ')
    t=re.sub(r'(\d+)(?::| : )(\d+)',lambda m:nw(m.group(1))+' to '+nw(m.group(2)),t)
    t=re.sub(r'\b(ax|bh|bx|lw|xy|ab|ad|bc|bd|ac|mx|wh|lwh)\b',lambda m:' '.join(m.group(1)),t)
    rep=[('≠',' is not equal to '),('≤',' is less than or equal to '),('≥',' is greater than or equal to '),('<',' is less than '),('>',' is greater than '),
         ('→',', so '),('=',' equals '),('×',' times '),('÷',' divided by '),('·',' times '),('−',' minus '),('+',' plus '),('π',' pi '),('√',' the square root of '),
         ('%',' percent'),('°',' degrees'),('±',' plus or minus '),('⊥',' perpendicular'),('₁',' one'),('₂',' two'),('…','...'),('✓','')]
    for a,b in rep:t=t.replace(a,b)
    t=re.sub(r'\bft\b','feet',t)
    t=re.sub(r'\b(1[1-9]\d\d|20\d\d)\b(?![.,]\d)',lambda m:num2words(int(m.group(1)),to='year'),t)
    t=re.sub(r'(\d)\(',r'\1 times (',t)
    t=t.replace('^',' to the ')
    t=re.sub(r'(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)',lambda m:' '+nw(m.group(1))+' ',t)
    t=re.sub(r'\(\s*',' ',t);t=re.sub(r'\s*\)',' ',t)
    t=re.sub(r'\b(\w+) (x|y|r|k|h|a|b|c)\b(?= )',r'\1 \2',t)
    t=re.sub(r'\s+',' ',t).strip()
    t=re.sub(r'\s+([,.?!;:])',r'\1',t);t=re.sub(r',+',',',t);t=re.sub(r'\.{2,}','.',t).replace('?.','?');t=re.sub(r',([.?!:])',r'\1',t);t=re.sub(r'([.?!:]),',r'\1',t)
    t=t.replace(' of of ',' of ').rstrip(', ')
    if t and t[-1] not in '.?!':t+='.'
    t=re.sub(r" ([’'])s\b",r'\1s',t)
    return t[0].upper()+t[1:] if t else t
PN={'(':'an open parenthesis',')':'a close parenthesis','( )':'parentheses','.':'a period',';':'a semicolon',':':'a colon',',':'a comma','—':'a dash','–':'a dash','-':'a dash'}
def say_p(t):
    t=plain(t)
    if not PUNCT:return speak(re.sub(r'\s*[,;:]\s*$','',t))
    t=re.sub(r'(^|\s)([.;:,—–()-])(?=\s|$)',lambda m:m.group(1)+PN[m.group(2)],t)
    t=re.sub(r'^([;:,—])\s*',lambda m:PN[m.group(1)]+' ',t) if len(t)<25 else t
    t=re.sub(r'\s*([;:,—])$',lambda m:' then '+PN[m.group(1)],t) if len(t)<25 else t
    return speak(t)
def board(t):
    return plain(t,' ; ').replace('  ',' ').replace(' ;  ; ',' ; ')
def carried(text,car):
    for v,s in (car or []):
        if s and v in text:text=text.replace(v,'{o|'+v+'}',1)
    return text
def build(lid,num):
    global APOS,PUNCT;APOS=lid=='s3';PUNCT=lid in ('s1','s2','s3','s4')
    l=L[lid];math=l['math'];sc=[]
    title=plain(l['title']);topic=title
    intro=[("Hi everyone. Today: "+speak(title).rstrip('.')+".",('w','SAT '+('Math' if math else 'Reading and Writing'),40))]
    big=plain(l['big']);intro.append(("Here is the big idea. "+speak(big),('y','Big idea: '+big,36)))
    sc.append(dict(title=title,lines=intro))
    rules=[s for s in re.split(r'(?<=[.:])\s+(?=[A-Z])|\s+\u00b7\s+(?=[A-Z])',plain(l['defn'])) if s][:4]
    if rules:sc.append(dict(title='The rules',lines=[(speak(r),('b',r,32)) for r in rules]))
    for i,e in enumerate(l['ex'][:4] if not math else []):
        lines=[];blank=re.sub(r'\[\[(.*?)\]\]',' ______ ',e['s']);box=(re.search(r'\[\[(.*?)\]\]',e['s']) or [None,None])[1]
        lines.append((f"Example {num2words(i+1)}. "+(speak(e['d']).rstrip('.')+'. ' if e.get('d') else '')+"Here it is: "+speak(re.sub(r'\[\[(.*?)\]\]',' blank ',e['s'])),('g',board(blank),32)))
        for j,p in enumerate(e['parts']):
            who=plain(e['who'][j]) if j<len(e.get('who',[])) else ''
            tag=plain(e['tags'][j]) if j<len(e.get('tags',[])) else ''
            lines.append(((who+': ' if who else '')+say_p(p).rstrip('.')+'.'+(' That is: '+say_p(tag.replace('-ing','i n g')) if tag else ''),('w',(who+': ' if who else '')+board(p)+('     [ '+tag+' ]' if tag else ''),30)))
        why=re.sub(r'\s*\(?(Based on a real|Real) College Board question\.?\)?','',plain(e['why']))
        if box is not None and re.search(r'\[\[',e['s']):
            bx=plain(box).strip()
            lines.append(("So the answer is: "+(say_p(bx).rstrip('.') if bx else 'no punctuation at all')+'. '+speak(why),('g','Answer:  '+((bx+'   ( '+say_p(bx).rstrip('.')+' )') if PUNCT and re.search(r'[.;:,—–-]',bx) else (bx if bx else '(no punctuation)'))+'  ·  '+why,30)))
        if e.get('trap') and e['trap'].get('w'):
            rows=[plain(r[1]) for r in e['trap']['rows'] if generic(plain(r[1]))]
            why=rows[-1] if rows else ''
            lines.append(("Trap. The choice "+re.sub(r'\ba (comma|semicolon|colon|period|dash)\b',r'\1',(lambda z:z[:1].lower()+z[1:])(say_p(re.sub(r'([,;:])(?!\d)',r' \1',plain(e['trap']['w']))))).rstrip('.')+" is wrong. "+speak(why),('r','Trap: '+plain(e['trap']['w'])+(' · '+why if len(why)<60 else ''),30)))
        sc.append(dict(title=f'Example {i+1}: '+plain(e['t']),lines=lines))
    for i,e in enumerate(l['ex'][:4] if math else []):
        k=f'{lid}|{i}';mh=MH.get(k);lines=[]
        lines.append((f"Example {num2words(i+1)}. "+speak(e['s']),('g',board(e['s']),36)))
        if mh:
            f=mh['f']
            if isinstance(f,dict):lines.append((speak(f['rule']),('b',(f['rule'] if re.match(r'^[\w ]*[Rr]ule:',f['rule']) else 'Rule: '+f['rule']),30)))
            else:
                for x in f[:2]:
                    where='It is on the reference sheet.' if 'Reference' in x['frm'] else 'Learn this one. It is not on the reference sheet.'
                    lines.append(("The formula: "+speak(x['n']).rstrip('.').lower()+". "+speak(x['eq']).rstrip('.')+'. '+where,('p','Formula: '+x['eq'],34)))
        for j,p in enumerate(e['parts']):
            car=mh['c'].get(str(j+1)) if mh else None
            why=mh['w'][j] if mh and j<len(mh['w']) else None
            say=speak(why) if why else ('Step '+num2words(j+1)+'. '+speak(p))
            lines.append((say,('p' if math else 'w',carried(board(p),car),34)))
        if e.get('trap') and e['trap'].get('w'):
            rows=[plain(r[1]) for r in e['trap']['rows'] if generic(plain(r[1]))]
            why=rows[-1] if rows else ''
            lines.append(("Trap. "+speak(e['trap']['w']).rstrip('.')+" is wrong. "+speak(why),('r','Trap: '+plain(e['trap']['w'])+(' · '+why if len(why)<40 else ''),30)))
        sc.append(dict(title=f'Example {i+1}: '+plain(e['t']),lines=lines))
    # pause and pick: a bank question on this lesson's skill with short choices
    sk=[x['id'] for x in B['skills'] if x.get('lesson')==lid] or [s for s,ls in LESSONS_OF.items() if ls[0]==lid] or [s for s,ls in LESSONS_OF.items() if lid in ls]
    lim=(26,150) if math else (34,330)
    qs=[q for q in B['qs'] if q['skill'] in sk and q.get('ch') and all(len(plain(c))<=lim[0] for c in q['ch']) and len(plain(q['q']))<lim[1] and '<table' not in q['q']]
    CUSTOM={'a4':dict(q='|x + 2| = 6. What are all the solutions?',ch=['4 only','4 and −8','−4 and 8','no solution'],ans=1,steps=['x + 2 = 6 gives 4, and x + 2 = −6 gives −8'])}
    if lid in CUSTOM:qs=[dict(CUSTOM[lid],diff='M')]
    KW={'s1':r'two full sentences|run-on|comma splice|FANBOYS|independent clause','s2':r'no punctuation|never separate|between (the )?subject and|between a verb','s3':r"apostroph|possess|it’s|it's|their|whose",
        's4':r'nonessential|extra (info|detail)|lift|pair|matching|essential','s5':r'agree|singular|plural|subject','g3':r'tense|had |has |since|by the time|already|last year|\b1[89]\d\d\b','g1':r'modif|dangling|doer|right after the comma','g2':r'parallel|list|pair|match'}
    if not math and lid in KW:
        k2=[x for x in qs if re.search(KW[lid],plain(' '.join(x['steps'])+' '+x['q']),re.I)]
        if k2:qs=k2
    random.seed(lid);q=random.choice([x for x in qs if x['diff']=='M'] or qs) if qs else None
    if q:
        L2=[]
        L2.append(("Your turn. Pause the video and pick. "+speak(q['q']),('g',board(q['q']),30 if math else 26)))
        L2.append((' '.join(f"Choice {'ABCD'[k]}, {(speak(c) if math else re.sub(r'\ba (comma|semicolon|colon|period|dash)\b',r'\1',say_p(re.sub(r'([,;:])(?!\d)',r' \1',plain(c))))).rstrip('.')}." for k,c in enumerate(q['ch'])),('choices',[board(c) for c in q['ch']])))
        L2.append(("The answer is choice "+'ABCD'[q['ans']]+". "+(speak(q['steps'][-1]) if math else say_p(q['steps'][-1])),('ok',q['ans'])))
        sc.append(dict(title='Your turn: pause and pick',lines=L2))
    how=[plain(h) for h in l['how'] if plain(h)]
    sc.append(dict(title='Say it out loud',lines=[("Now say it out loud with me.",None)]+[((say_p(h) if not math else speak(h)),('y',f'{n+1}. '+h,32)) for n,h in enumerate(how)]+[("Great work, everyone.",None)]))
    out=f"TITLE={repr(('SAT Math - ' if math else 'SAT Reading and Writing - ')+title)}\nTOPIC={repr(topic)}\nKIND={repr('SAT MATH' if math else 'SAT READING + WRITING')}\nSCENES={repr(sc)}\n"
    open(f'script_{lid}.py','w').write(out)
    return sum(len(s['lines']) for s in sc)
if __name__=='__main__':
    for lid in sys.argv[1:]:print(lid,build(lid,0))
