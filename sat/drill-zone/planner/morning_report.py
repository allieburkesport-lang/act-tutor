#!/usr/bin/env python3
"""SAT HELM morning report: builds a phone-friendly HTML email about one day of Patrick's work.
Usage: HELM_PLANNER_TOKEN=... python3 morning_report.py [YYYY-MM-DD] > report.html
Default day = yesterday (US Eastern). Reads answers + tutor questions through the token-protected
Supabase functions, plus bank.json, plan.json and blueprint.json. No API credits are used."""
import json, os, re, sys, html, datetime, collections, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); DZ = os.path.join(HERE, '..')
TOK = os.environ.get('HELM_PLANNER_TOKEN') or open(os.path.expanduser('~/.helm_planner_token')).read().strip()
URL = 'https://wsoevgmculmcnxymivbp.supabase.co/rest/v1/rpc/'
HDR = {'apikey': 'sb_publishable_ncTnyRItcb1Ww_FUSpMlew_uv-7gPg_', 'Content-Type': 'application/json'}
def rpc(name): return json.loads(urllib.request.urlopen(urllib.request.Request(URL + name, json.dumps({'tok': TOK}).encode(), HDR)).read())

ET = datetime.timezone(datetime.timedelta(hours=-5))
et = lambda s: datetime.datetime.fromisoformat(s).astimezone(ET)
day = sys.argv[1] if len(sys.argv) > 1 else (datetime.datetime.now(ET) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
banner = os.environ.get('REPORT_BANNER', '')
A = rpc('planner_answers'); T = rpc('planner_tutor')
B = json.load(open(os.path.join(DZ, 'bank.json'))); SK = {s['id']: s for s in B['skills']}
P = json.load(open(os.path.join(DZ, 'plan.json'))); BP = json.load(open(os.path.join(DZ, 'blueprint.json')))
nm = lambda k: SK.get(k, {}).get('name', k)
secn = lambda k: 'Math' if SK.get(k, {}).get('sec') == 'Math' else 'Reading & Writing'
D0 = datetime.date.fromisoformat(day); nxt = (D0 + datetime.timedelta(days=1)).isoformat()
pretty = lambda d: datetime.date.fromisoformat(d).strftime('%a, %b %-d')
test = datetime.date(2026, 12, 5); left = (test - D0).days

R = [a for a in A if et(a['created_at']).strftime('%Y-%m-%d') == day]
F = [a for a in R if (a.get('attempt') or 1) == 1]
n = len(F); ok = sum(a['correct'] for a in F)
NAVY, G, AMB, RED, MU, LN = '#1E3A8A', '#059669', '#7C3AED', '#DC2626', '#374151', '#E5E7EB'
col = lambda p: G if p >= 80 else (AMB if p >= 60 else RED)
nolink = lambda s: s.replace(':', '&#8288;:&#8288;')
FONT = 'font-family:-apple-system,Helvetica,Arial,sans-serif'
def kpi(lab, val, sub): return f"<td width='50%' style='padding:5px;vertical-align:top'><div style='border:1px solid {LN};border-radius:12px;padding:12px'><div style='font-size:12px;color:{MU}'>{lab}</div><div style='font-size:26px;line-height:30px;font-weight:800;color:{NAVY}'>{val}</div><div style='font-size:12px;color:{MU}'>{sub}</div></div></td>"
def h3(t): return f"<div style='font-size:19px;font-weight:800;color:{NAVY};margin:24px 0 8px'>{t}</div>"
li = lambda t: f"<li style='margin:0 0 8px'>{t}</li>"
ul = lambda items: f"<ul style='margin:0;padding-left:20px;font-size:15px;line-height:21px'>{''.join(li(x) for x in items)}</ul>"
def bar(p, c): return f"<div style='background:{LN};border-radius:6px;height:12px;margin:6px 0 4px'><div style='background:{c};width:{max(2,min(100,p))}%;height:12px;border-radius:6px'></div></div>"

# ---- did he finish the day's plan? ----
pd = next((d for d in P['days'] if d['date'] == day), None)
plan_html = ''
if pd:
    reset = datetime.datetime.fromtimestamp(pd['reset_at'] / 1000, datetime.timezone.utc) if pd.get('reset_at') else None
    tag = f'plan {day}'
    rows = [a for a in R if tag in (a.get('part') or '') and (not reset or datetime.datetime.fromisoformat(a['created_at']) > reset)]
    firsts = {}
    for a in sorted(rows, key=lambda a: a['created_at']): firsts.setdefault(a['question'].split(' ')[0], a)
    done = len(firsts); right = sum(a['correct'] for a in firsts.values()); planned = pd.get('n_questions') or 0
    pc = min(100, round(100 * done / planned)) if planned else 0
    c = G if pc >= 100 else AMB if done else RED
    word = 'Yes' if pc >= 100 else 'No'
    box = lambda lab, v: f"<td width='33%' align='center' style='padding:4px'><div style='border:2px solid {LN};border-radius:12px;padding:10px 4px'><div style='font-size:28px;line-height:32px;font-weight:800;color:{NAVY}'>{v}</div><div style='font-size:14px;font-weight:700;color:#334155'>{lab}</div></div></td>"
    when = 'today' if day == datetime.datetime.now(ET).strftime('%Y-%m-%d') else pretty(day)
    plan_html = (f"<div style='border:3px solid {c};border-radius:14px;padding:14px;margin:18px 0 6px'>"
        f"<div style='font-size:20px;line-height:25px;font-weight:800;color:{NAVY}'>Did he complete {'today' if when=='today' else when}’s plan? <span style='color:{c}'>{word}</span></div>"
        f"<div style='background:{LN};border-radius:10px;height:34px;margin:12px 0;overflow:hidden'><div style='background:{c};width:{max(12,pc)}%;height:34px;border-radius:10px;color:#fff;font-size:17px;font-weight:800;line-height:34px;text-align:center;white-space:nowrap'>{pc}%</div></div>"
        f"<div style='font-size:22px;font-weight:800;color:{c};text-align:center;margin-bottom:8px'>{pc}% complete</div>"
        f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0'><tr>{box('Total', planned)}{box('Completed', done)}{box('Correct', right)}</tr></table></div>")

# ---- day numbers ----
SITE = 'https://allieburkesport-lang.github.io/act-tutor/sat/prep/'
HN = {'show': 'Show me how', 'desm': 'Desmos steps', 'form': 'Formula', 'learn': 'Learn it', 'video': 'Video', 'tutor': 'Ask the tutor', 'desmos': 'Desmos calculator', 'ref': 'Reference sheet'}
TOOLS = {'desmos', 'ref'}
def qlabel(qid): k, _, num = qid.rpartition('-'); return f"{nm(k)} #{int(num) if num.isdigit() else num}"
def qlink(qid): return f"<a href='{SITE}#/look/{qid}' style='color:{NAVY};font-weight:700;text-decoration:underline'>{html.escape(qlabel(qid))}</a>"
def tile(lab, val, c=NAVY): return f"<td width='50%' style='padding:4px'><div style='border:2px solid {LN};border-radius:12px;padding:10px;text-align:center'><div style='font-size:28px;line-height:32px;font-weight:800;color:{c}'>{val}</div><div style='font-size:14px;font-weight:700;color:#334155'>{lab}</div></div></td>"
def row(left, right=''): return f"<tr><td style='padding:9px 0;border-top:1px solid {LN};font-size:15px'>{left}</td><td align='right' style='padding:9px 0;border-top:1px solid {LN};font-size:14px;font-weight:700;white-space:nowrap'>{right}</td></tr>"
tbl = lambda rows: f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0'>{rows}</table>"
asks = [m for m in T if m.get('role') == 'student' and et(m['created_at']).strftime('%Y-%m-%d') == day]
if n:
    Q = collections.OrderedDict()
    for a in sorted(R, key=lambda a: a['created_at']):
        qid = a['question'].split(' ')[0]; e = Q.setdefault(qid, {'first': None, 'help': set(), 'ok': False})
        if e['first'] is None: e['first'] = a['correct']
        e['ok'] = e['ok'] or a['correct']
        hm = re.search(r'help ([\w+]+)', a.get('part') or '')
        if hm: e['help'] |= set(hm.group(1).split('+'))
        elif 'coached' in (a.get('part') or ''): e['help'].add('show')
    for m in asks:
        if m.get('question_id') in Q: Q[m['question_id']]['help'].add('tutor')
    wrong = [k for k, e in Q.items() if e['first'] is False]
    helped = [k for k, e in Q.items() if e['help'] - TOOLS]
    calc = [k for k, e in Q.items() if e['help'] & TOOLS]
    secs = round(sum(a.get('seconds') or 0 for a in F) / n)
    t0 = min(et(a['created_at']) for a in R); t1 = max(et(a['created_at']) for a in R)
    summary = (f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='margin:6px 0 0'>"
        f"<tr>{tile('Questions done', len(Q))}{tile('Right first try', f'{round(100*ok/n)}%', col(round(100*ok/n)))}</tr>"
        f"<tr>{tile('Wrong', len(wrong), RED if wrong else G)}{tile('Used help on', len(helped), AMB if helped else G)}</tr>"
        f"<tr>{tile('Asked the tutor', len(asks))}{tile('Used calculator on', len(calc))}</tr>"
        f"<tr>{tile('Time per question', f'{secs}s')}{tile('Time on HELM', f'{round((t1-t0).seconds/60)} min')}</tr></table>")
    badge = lambda h: ' '.join(f"<span style='display:inline-block;background:#EEF2FF;border:1px solid #C7D2FE;color:#1E3A8A;border-radius:10px;padding:1px 7px;margin:2px 2px 0 0;font-size:12px;font-weight:700'>{HN.get(x,x)}</span>" for x in sorted(h))
    res = lambda k: f"<span style='color:{G if Q[k]['first'] else RED}'>{'✓ right' if Q[k]['first'] else '✗ wrong'}</span>"
    help_html = tbl(''.join(row(qlink(k) + '<br>' + badge(Q[k]['help'] - TOOLS), res(k)) for k in helped)) if helped else f"<div style='font-size:15px'>None.</div>"
    miss_html = tbl(''.join(row(qlink(k), f"<span style='color:{G if Q[k]['ok'] else RED}'>{'fixed on retry' if Q[k]['ok'] else 'not fixed'}</span>") for k in wrong)) if wrong else f"<div style='font-size:15px'>None. Every question right on the first try.</div>"
    ask_html = tbl(''.join(row((qlink(m['question_id']) + '<br>' if m.get('question_id') else '') + '“' + html.escape(m['content'][:200]) + '”') for m in asks)) if asks else f"<div style='font-size:15px'>He didn't ask the tutor anything.</div>"
    calc_html = (f"<div style='font-size:15px'>{len(calc)} question{'s' if len(calc)!=1 else ''}: " + ', '.join(qlink(k) + ' (' + ', '.join(HN[x] for x in sorted(Q[k]['help'] & TOOLS)) + ')' for k in calc) + "</div>") if calc else f"<div style='font-size:15px'>None.</div>"
    by = collections.defaultdict(lambda: [0, 0])
    for a in F: by[a['concept_id']][0] += 1; by[a['concept_id']][1] += a['correct']
    skills = tbl(''.join(row(f"<b>{nm(k)}</b> · {v[1]} of {v[0]}", f"<span style='font-size:17px;color:{col(round(100*v[1]/v[0]))}'>{round(100*v[1]/v[0])}%</span>") for k, v in sorted(by.items(), key=lambda x: (x[1][1] / x[1][0], -x[1][0]))))
    day_html = (plan_html + h3('Summary of the day') + summary
        + h3(f'Questions he got help on ({len(helped)})') + help_html
        + h3(f'Questions he got wrong ({len(wrong)})') + miss_html
        + h3(f'What he asked the tutor ({len(asks)})') + ask_html
        + h3('Calculator / reference sheet (allowed on the SAT)') + calc_html
        + h3('By skill (weakest first)') + skills
        + f"<div style='font-size:14px;margin-top:10px'>Tap any question to open it. It opens in practice mode and nothing is saved.</div>")
else:
    day_html = plan_html + f"<div style='font-size:16px;margin:14px 0'>❌ <b>No HELM work on {pretty(day)}.</b></div>"

# ---- overall so far ----
AF = [a for a in A if (a.get('attempt') or 1) == 1]
days_active = len({et(a['created_at']).strftime('%Y-%m-%d') for a in A})
bpn = sum(x['n'] for x in BP['daily']); bpok = sum(x['n'] * x['acc'] / 100 for x in BP['daily'])
ranked = sorted([s for s in P.get('skills', []) if s.get('tried') and s.get('acc') is not None], key=lambda s: s['acc'])
overall = [f"<b>HELM:</b> {len(AF)} questions over {days_active} day{'s' if days_active != 1 else ''}, {round(100*sum(a['correct'] for a in AF)/len(AF)) if AF else 0}% right on the first try.",
           f"<b>Blueprint:</b> {bpn} questions since Aug 31, {round(100*bpok/bpn) if bpn else 0}% right.",
           "<b>Weakest skills overall:</b> " + ', '.join(f"{s['name']} ({s['acc']}%)" for s in ranked[:4]) + '.',
           "<b>Strongest:</b> " + ', '.join(f"{s['name']} ({s['acc']}%)" for s in ranked[-3:][::-1]) + '.',
           "<b>Official SATs:</b> Sept 12: 1010 · Oct 3: 990 · Nov 7: 1010 (Math 520, R&amp;W 490). Superscore 1050. Goal 1300 on Dec 5."]
nd = next((d for d in P['days'] if d['date'] == nxt), None)
plan_next = ul([f"<b>New skills:</b> {', '.join(nm(k) for k in nd.get('learn', [])) or 'review day'}", f"<b>Extra practice:</b> {', '.join(nd.get('focus_names', []))}", f"About {nd.get('n_questions', '?')} questions"]) if nd else ''

H = f"""<div style="{FONT};color:#0F172A;max-width:600px;margin:0 auto;padding:0 4px;-webkit-text-size-adjust:100%">{banner}

<div style="font-size:24px;line-height:29px;font-weight:800;color:{NAVY}">Patrick · {pretty(day)}</div>
<div style="font-size:15px;font-weight:600;color:{MU};padding-bottom:10px;border-bottom:3px solid {NAVY}">SAT on Dec 5 · {left} days left · Goal 1300</div>
{day_html}
{h3('Overall so far')}{ul(overall)}
{h3('Today’s plan · ' + pretty(nxt)) + plan_next if nd else ''}
<div style="margin:24px 0 6px"><a href="https://allieburkesport-lang.github.io/act-tutor/sat/prep/#/stats" style="display:inline-block;background:{NAVY};color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;padding:12px 18px;border-radius:10px">Open the Stats dashboard</a></div>
</div>"""
print(H)
