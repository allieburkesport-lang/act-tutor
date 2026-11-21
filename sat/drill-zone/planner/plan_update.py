#!/usr/bin/env python3
"""Patrick's SAT daily plan (to Sat Dec 5, 2026).
Reads his answers from Supabase + blueprint.json, re-works future days, writes
../plan.json (used by the dashboard) and plan_artifact.html (the pinned plan page).
Run: python3 plan_update.py   (no arguments; safe to re-run any time)"""
import json, os, datetime, urllib.request, collections, html
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); DZ = os.path.dirname(HERE)
SITE = 'https://allieburkesport-lang.github.io/act-tutor/sat/drill-zone/'
NEW = 'https://allieburkesport-lang.github.io/act-tutor/sat/prep/'   # the new site (Nov 21); all plan links go here
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
# % of its section on the SAT, per question type (Nov 21, 2026 research; College Board publishes only domain counts):
#  Math = Sigma Prep count of all 8 official Bluebook practice tests (PT 4-11, 528 questions, College Board's own skill labels)
#  Reading & Writing = The Test Advantage count of 57 real test forms (Jun 2023 - Dec 2025), share of 54
SHARE = {'wic':15.7,'tsp':8.7,'cross':2.0,'cid':4.3,'coe':13.5,'inf':10.2,'bound':12.4,'fss':9.4,'syn':13.1,'trans':10.7,'lin1':6.1,'lin2':7.0,'linf':10.5,'sys':7.0,'ineq':4.1,'equiv':5.5,'nleq':10.0,'nlf':16.8,'ratio':3.6,'pct':3.6,'data1':4.1,'data2':3.6,'prob':1.8,'infer':0.9,'claims':0.2,'area':4.1,'lat':5.0,'trig':3.4,'circ':3.4}
# Base schedule (Allie approved the dashboard plan on Nov 19; Nov 20 rebuilt as concept + drills + cumulative review)
# kind: learn | test | off | light | weak | final | sat
BASE = [
 ('2026-11-19','learn',['nlf','nleq','fss'],"Nonlinear functions + quadratics + grammar forms"),
 ('2026-11-20','learn',['trig','circ','trans'],""),
 ('2026-11-21','learn',['nleq','prob','cid'],"Drills today instead of Practice Test 3 (Allie, Nov 21)"),
 ('2026-11-22','learn',['ratio','pct','bound'],""),
 ('2026-11-23','learn',['linf','lin2','wic'],""),
 ('2026-11-24','learn',['area','lat','syn'],""),
 ('2026-11-25','learn',['data1','data2','inf'],""),
 ('2026-11-26','off',[],"Thanksgiving: off"),
 ('2026-11-27','light',[],"Light day: review + redo my misses (about 30 min)"),
 ('2026-11-28','test',[],"Practice Test 4 in Bluebook (full test, timed). Send the score report afterward."),
 ('2026-11-29','learn',['sys','ineq','coe'],""),
 ('2026-11-30','learn',['lin1','equiv','tsp'],""),
 ('2026-12-01','weak',[],"His weakest concepts · Also: download the exam in Bluebook and charge the laptop"),
 ('2026-12-02','weak',['infer','cross'],"Small topics + his weakest concepts (statistical claims dropped: 0 per test in the official practice tests)"),
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
    START = datetime.date(2026, 11, 20)   # the plan (and the nightly re-work) starts Fri Nov 20; Nov 19 was done in Blueprint
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
            have_e = sum(1 for x in base if x not in MATH)
            need_e = max(0, 1 - have_e); need_m = 4 - len(base) - need_e
            pick = [s for s in ranked_m if s not in base][:need_m] + [s for s in ranked_e if s not in base][:need_e]
            if day['date'] == '2026-12-03': pick = ranked_m[:3] + ranked_e[:1]; base = []
            day['learn'] = (base + pick)[:4]
    # --- cumulative review: each earlier concept gets 1 question (2 if under 60%), max 12, weakest first
    seen = []
    for day in days:
        if day['kind'] in ('learn', 'weak', 'light'):
            pool = [s for s in seen if s not in day['learn']]
            pool.sort(key=lambda s: (acc(s)[0] if acc(s)[0] is not None else 50))
            # 1 question from EVERY earlier concept; extra questions go to math first so the whole day
            # (warm-up 6 math + 4 English, new concepts, review) is about 65% math / 35% English (USNA weights math)
            rev = [[s, 1] for s in pool]
            # still-weak skills (under 60% after at least 3 tries) always come back, even before their learn day
            cand = sorted([s for s in SHARE if s not in day['learn'] and acc(s)[0] is not None and acc(s)[0] < 60 and acc(s)[1] >= 3], key=weakness, reverse=True)
            weak_now = [s for s in cand if s in MATH][:3] + [s for s in cand if s not in MATH][:1]   # his 4 biggest point-losers
            for s in weak_now:
                r = next((r for r in rev if r[0] == s), None)
                if r: r[1] = max(r[1], 2)
                else: rev.append([s, 2])
            day['focus'] = [s for s in weak_now]
            def mshare():
                m = 6 + 10 * sum(1 for x in day['learn'] if x in MATH) + sum(n for s2, n in rev if s2 in MATH)
                t = 10 + 10 * len(day['learn']) + sum(n for _, n in rev)
                return m / t, t
            CAP = 26
            a = lambda s2: acc(s2)[0] if acc(s2)[0] is not None else 50
            math_order = sorted([r for r in rev if r[0] in MATH], key=lambda r: a(r[0]))
            eng_weak = sorted([r for r in rev if r[0] not in MATH and a(r[0]) < 60], key=lambda r: a(r[0]))
            k = 0
            while sum(n for _, n in rev) < CAP and math_order:
                sh, _ = mshare()
                if sh < 0.65 or not eng_weak:
                    r = math_order[k % len(math_order)]
                    if r[1] >= 3: break
                    r[1] += 1; k += 1
                else:
                    eng_weak.pop(0)[1] += 1
            day['math_share'] = round(100 * mshare()[0])
            day['review'] = rev
        else: day['review'] = []; day['math_share'] = None; day['focus'] = []
        for s in day['learn']:
            if s not in seen: seen.append(s)
    # --- what to click
    for day in days:
        dd = datetime.date.fromisoformat(day['date']); d0 = day['date']
        day['label'] = dd.strftime('%a %b ') + str(dd.day)
        day['concepts'] = [dict(skill=s, name=names[s], sec='Math' if s in MATH else 'English', share=SHARE[s], acc=acc(s)[0], tried=acc(s)[1],
                                lessons=[dict(id=l, title=LTITLE[l], url=NEW + '#/learn/' + s) for l in LESSONS[s]],
                                drill=NEW + '#/drill/' + s) for s in day['learn']]
        day['review_url'] = NEW + '#/drill/review:' + ','.join(f'{s}.{n}' for s, n in day['review']) if day['review'] else ''
        day['day_url'] = NEW + '#/day/' + d0; day['report_url'] = NEW + '#/report/' + d0
        day['review_names'] = [[names[s], n] for s, n in day['review']]
        day['focus_names'] = [names[s] for s in day.get('focus', [])]
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
    open(os.path.join(DZ, 'plan.html'), 'w', encoding='utf-8').write(tpl.replace('__PLAN__', json.dumps(out).replace('</', '<\\/')))
    print('plan updated', out['updated'], 'rows', len(rows), 'changes', changes)

if __name__ == '__main__': main()
