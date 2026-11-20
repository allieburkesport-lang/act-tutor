#!/usr/bin/env python3
"""Patrick's SAT daily plan (to Sat Dec 5, 2026).
Reads his answers from Supabase + blueprint.json, re-works future days, writes
../plan.json (used by the dashboard) and plan_artifact.html (the pinned plan page).
Run: python3 plan_update.py   (no arguments; safe to re-run any time)"""
import json, os, datetime, urllib.request, collections, html
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); DZ = os.path.dirname(HERE)
SITE = 'https://allieburkesport-lang.github.io/act-tutor/sat/drill-zone/'
SB = 'https://wsoevgmculmcnxymivbp.supabase.co/rest/v1/answers'
KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indzb2V2Z21jdWxtY254eW1pdmJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ3OTIwMTAsImV4cCI6MjExMDM2ODAxMH0.wl408Zf5rJjh-uhPbPuykvUtETHinQXQdttAJPvn1Jk'
TZ = ZoneInfo('America/New_York')
TEST = datetime.date(2026, 12, 5)

# Every SAT concept -> the Drill Zone lessons that teach it
LESSONS = {'lin1':['m1','m4'],'lin2':['t1'],'linf':['t1','a3'],'sys':['a2'],'ineq':['a5'],'equiv':['t2'],'nleq':['a1','a4'],'nlf':['t2','a1','a3'],
 'ratio':['a6'],'pct':['m2'],'data1':['d1'],'data2':['d3'],'prob':['d2'],'infer':['m2'],'claims':['d3'],'area':['t3','e1'],'lat':['e2'],'trig':['t3'],'circ':['t3'],
 'wic':['r1'],'tsp':['r5'],'cross':['r5'],'cid':['r2'],'coe':['r4'],'inf':['r3'],'bound':['s1','s2','s4'],'fss':['s3','s5','g1','g2','g3'],'trans':['s6'],'syn':['r6']}
LTITLE = {'s1':'Sentences','s2':'No wall','s3':'Apostrophes','s4':'Pairs','s5':'Subject X-ray','s6':'CARE transitions','r1':'Words in context','r2':'Main idea','r3':'Inferences','r4':'Evidence','r5':'Purpose + two texts','r6':'Notes questions',
 'm1':'Define FIND','m2':'Trap words','m4':'Verify','t1':'Lines and slope','t2':'Exponents','t3':'Circles, volume, trig','a1':'Quadratics','a2':'Systems','a3':'Functions','a4':'Absolute value','a5':'Inequalities','a6':'Ratios and units','d1':'Mean and median','d2':'Probability','d3':'Scatterplots','e1':'Similar shapes','e2':'Angles','g1':'Modifiers','g2':'Lists','g3':'Verb tense'}
# % of its section on the SAT (domain % from College Board, split by question-bank share)
SHARE = {'wic':15.5,'tsp':8.9,'cross':3.6,'cid':6.5,'coe':13.0,'inf':6.6,'bound':13.2,'fss':12.8,'syn':10.3,'trans':9.7,'lin1':6.4,'lin2':7.4,'linf':9.7,'sys':7.2,'ineq':4.4,'equiv':7.5,'nleq':10.7,'nlf':16.8,
 'ratio':3.3,'pct':3.0,'data1':3.0,'data2':2.5,'prob':1.7,'infer':1.0,'claims':0.4,'area':4.7,'lat':4.4,'trig':3.0,'circ':2.9}
# Base schedule (Allie approved the dashboard plan on Nov 19; Nov 20 rebuilt as concept + drills + cumulative review)
# kind: learn | test | off | light | weak | final | sat
BASE = [
 ('2026-11-19','learn',['nlf','nleq','fss'],"Nonlinear functions + quadratics + grammar forms"),
 ('2026-11-20','learn',['trig','circ','trans'],""),
 ('2026-11-21','test',[],"Practice Test 3 in Bluebook (full test, timed). Send the score report afterward."),
 ('2026-11-22','learn',['nleq','prob','cid'],"Catch-up for Tue Nov 17 (USMMA visit)"),
 ('2026-11-23','learn',['ratio','pct','bound'],""),
 ('2026-11-24','learn',['linf','lin2','wic'],""),
 ('2026-11-25','learn',['area','lat','syn'],""),
 ('2026-11-26','off',[],"Thanksgiving: off"),
 ('2026-11-27','light',[],"Light day: review + redo my misses (about 30 min)"),
 ('2026-11-28','test',[],"Practice Test 4 in Bluebook (full test, timed). Send the score report afterward."),
 ('2026-11-29','learn',['data1','data2','inf'],""),
 ('2026-11-30','learn',['sys','ineq','coe'],""),
 ('2026-12-01','learn',['lin1','equiv','tsp','cross'],"Also: download the exam in Bluebook and charge the laptop"),
 ('2026-12-02','weak',['infer','claims'],"Small topics + his 2 weakest concepts so far"),
 ('2026-12-03','weak',[],"His weakest concepts + mixed set at SAT pace"),
 ('2026-12-04','light',[],"Light: redo my misses, pack the bag, early bed"),
 ('2026-12-05','sat',[],"SAT · check in by 7:45 AM"),
]
MATH = {'lin1','lin2','linf','sys','ineq','equiv','nleq','nlf','ratio','pct','data1','data2','prob','infer','claims','area','lat','trig','circ'}

def get_rows():
    rows, off = [], 0
    while True:
        url = f"{SB}?student=ilike.patrick*&select=created_at,kind,concept_id,correct,first_try,attempt&order=created_at.asc&offset={off}&limit=1000"
        req = urllib.request.Request(url, headers={'apikey': KEY, 'Authorization': 'Bearer ' + KEY})
        part = json.load(urllib.request.urlopen(req, timeout=30)); rows += part
        if len(part) < 1000: return rows
        off += 1000

def main():
    now = datetime.datetime.now(TZ); today = now.date()
    names = {s['id']: s['name'] for s in json.load(open(os.path.join(DZ, 'bank.json')))['skills']}
    bp = json.load(open(os.path.join(DZ, 'blueprint.json')))['skills']
    try: rows = get_rows(); online = True
    except Exception as e: rows = []; online = False
    # first attempts per skill (dashboard drills, review, official warm-up)
    dz = collections.defaultdict(lambda: [0, 0]); byday = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
    for r in rows:
        if r.get('kind') not in ('bank', 'official') or (r.get('attempt') or 1) != 1: continue
        sk = r.get('concept_id')
        if sk not in SHARE: continue
        d = datetime.datetime.fromisoformat(r['created_at'].replace('Z', '+00:00')).astimezone(TZ).date().isoformat()
        dz[sk][0] += 1; dz[sk][1] += 1 if r.get('correct') else 0
        byday[d][sk][0] += 1; byday[d][sk][1] += 1 if r.get('correct') else 0
    lessons_done = collections.defaultdict(int)
    for r in rows:
        if r.get('kind') in ('drill', 'lesson'):
            d = datetime.datetime.fromisoformat(r['created_at'].replace('Z', '+00:00')).astimezone(TZ).date().isoformat()
            lessons_done[d] += 1
    def acc(sk):  # blend: Drill Zone work counts double
        n = bp.get(sk, {}).get('n', 0) + 2 * dz[sk][0]; ok = bp.get(sk, {}).get('ok', 0) + 2 * dz[sk][1]
        return (round(100 * ok / n) if n else None), bp.get(sk, {}).get('n', 0) + dz[sk][0]
    # --- re-work: concepts from past learn days he did not practise move to the next learn day
    days = [dict(date=d, kind=k, learn=list(sk), note=n) for d, k, sk, n in BASE]
    carry, changes = [], []
    START = datetime.date(2026, 11, 20)   # the plan (and the nightly re-work) starts Fri Nov 20; Nov 19 was done in 1500 Blueprint
    for day in days:
        dd = datetime.date.fromisoformat(day['date'])
        if dd < START:
            day['status'] = 'done'; continue
        if dd < today and day['kind'] in ('learn', 'weak'):
            missed = [s for s in day['learn'] if byday[day['date']][s][0] < 5]
            did = [s for s in day['learn'] if s not in missed]
            day['status'] = 'done' if not missed else ('partly' if did else 'not done')
            carry += missed
    # spread missed concepts over the next learning days (max 4 concepts on any day)
    future = [d for d in days if datetime.date.fromisoformat(d['date']) >= today and d['kind'] in ('learn', 'weak')]
    for s in carry:
        tgt = next((d for d in future if s not in d['learn'] and len(d['learn']) < 4), None)
        if tgt:
            tgt['learn'].insert(0, s); tgt.setdefault('carried', []).append(s)
            changes.append(f"{names[s]} moved to {tgt['date']} (not practised on its day)")
    for d in future:
        if d.get('carried'):
            d['note'] = (d['note'] + ' · ' if d['note'] else '') + 'Carried over: ' + ', '.join(names[s] for s in d['carried'])
    # weak days filled with his current weakest concepts (weighted by share of the test)
    def weakness(s):
        p, n = acc(s); p = 50 if p is None else p
        return (100 - p) * SHARE[s]
    ranked_m = sorted([s for s in SHARE if s in MATH], key=weakness, reverse=True)
    ranked_e = sorted([s for s in SHARE if s not in MATH], key=weakness, reverse=True)
    for day in days:
        if day['kind'] == 'weak' and datetime.date.fromisoformat(day['date']) >= today:
            base = [s for s in day['learn']]
            need_m = 2; need_e = 1
            pick = [s for s in ranked_m if s not in base][:need_m] + [s for s in ranked_e if s not in base][:need_e]
            if day['date'] == '2026-12-03': pick = ranked_m[:2] + ranked_e[:2]; base = []
            day['learn'] = (base + pick)[:4]
    # --- cumulative review: each earlier concept gets 1 question (2 if under 60%), max 12, weakest first
    seen = []
    for day in days:
        if day['kind'] in ('learn', 'weak', 'light'):
            pool = [s for s in seen if s not in day['learn']]
            pool.sort(key=lambda s: (acc(s)[0] if acc(s)[0] is not None else 50))
            # 1 question from EVERY earlier concept; weakest (<60%) get a 2nd one, review capped at 24
            rev = [[s, 1] for s in pool]; extra = 24 - len(rev)
            for r in rev:
                if extra <= 0: break
                if (acc(r[0])[0] if acc(r[0])[0] is not None else 50) < 60: r[1] = 2; extra -= 1
            day['review'] = rev
        else: day['review'] = []
        for s in day['learn']:
            if s not in seen: seen.append(s)
    # --- what to click
    for day in days:
        dd = datetime.date.fromisoformat(day['date']); d0 = day['date']
        day['label'] = dd.strftime('%a %b ') + str(dd.day)
        day['concepts'] = [dict(skill=s, name=names[s], sec='Math' if s in MATH else 'English', share=SHARE[s], acc=acc(s)[0], tried=acc(s)[1],
                                lessons=[dict(id=l, title=LTITLE[l], url=SITE + 'learn.html#' + l) for l in LESSONS[s]],
                                drill=SITE + 'index.html#go=skill:' + s) for s in day['learn']]
        day['review_url'] = SITE + 'index.html#go=review:' + ','.join(f'{s}.{n}' for s, n in day['review']) if day['review'] else ''
        day['review_names'] = [[names[s], n] for s, n in day['review']]
        day['n_questions'] = 10 * len(day['learn']) + sum(n for _, n in day['review'])
        res = byday.get(d0, {})
        q = sum(v[0] for v in res.values()); ok = sum(v[1] for v in res.values())
        day['result'] = dict(questions=q, first_try=ok, pct=round(100 * ok / q) if q else None, lessons=lessons_done.get(d0, 0),
                             by_skill={names[s]: v for s, v in res.items()}) if dd < today or q else None
    out = dict(updated=now.strftime('%a %b %-d, %-I:%M %p ET'), online=online, today=today.isoformat(), test=TEST.isoformat(),
               total_concepts=len(SHARE), math=len(MATH), english=len(SHARE) - len(MATH), changes=changes,
               skills=[dict(skill=s, name=names[s], sec='Math' if s in MATH else 'English', share=SHARE[s], acc=acc(s)[0], tried=acc(s)[1]) for s in SHARE],
               days=days)
    json.dump(out, open(os.path.join(DZ, 'plan.json'), 'w'), indent=1)
    tpl = open(os.path.join(HERE, 'plan_template.html'), encoding='utf-8').read()
    open(os.path.join(HERE, 'plan_artifact.html'), 'w', encoding='utf-8').write(tpl.replace('__PLAN__', json.dumps(out).replace('</', '<\\/')))
    print('plan updated', out['updated'], 'rows', len(rows), 'changes', changes)

if __name__ == '__main__': main()
