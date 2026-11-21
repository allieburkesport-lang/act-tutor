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
# HELM palette
FONT = 'font-family:-apple-system,Helvetica,Arial,sans-serif'
NAVY, BLUE, PUR, G, RED, INK, GRY, LN = '#1E3A8A', '#2563EB', '#7C3AED', '#059669', '#DC2626', '#111827', '#4B5563', '#E5E7EB'
TINT = {NAVY: '#EEF2FF', PUR: '#F5F3FF', G: '#ECFDF5', RED: '#FEF2F2', BLUE: '#EFF6FF'}
col = lambda p: G if p >= 80 else (PUR if p >= 60 else RED)
nolink = lambda s: s.replace(':', '&#8288;:&#8288;').replace(' 5', '&nbsp;&#8288;5')
SITE = 'https://allieburkesport-lang.github.io/act-tutor/sat/prep/'
HN = {'show': 'Show me how', 'desm': 'Desmos steps', 'form': 'Formula', 'learn': 'Learn it', 'video': 'Video', 'tutor': 'Ask the tutor', 'desmos': 'Desmos calculator', 'ref': 'Reference sheet'}
TOOLS = {'desmos', 'ref'}
T0 = "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'"
def qlabel(qid): k, _, num = qid.rpartition('-'); return f"{nm(k)} #{int(num) if num.isdigit() else num}"
def qlink(qid): return f"<a href='{SITE}#/look/{qid}' style='color:{BLUE};font-weight:700;text-decoration:none'>{html.escape(qlabel(qid))}&nbsp;›</a>"
def section(title, c, inner, count=None):
    cnt = f"<td align='right' style='font-size:15px;font-weight:800;color:#fff'>{count}</td>" if count is not None else ''
    return (f"{T0} style='margin:14px 0 0;border:1px solid {LN};border-radius:12px;border-collapse:separate;overflow:hidden'>"
            f"<tr><td style='background:{c};padding:9px 12px'>{T0}><tr><td style='font-size:16px;font-weight:800;color:#fff'>{title}</td>{cnt}</tr></table></td></tr>"
            f"<tr><td style='padding:4px 12px 8px;background:#fff'>{inner}</td></tr></table>")
def rows(items):  # items: (left_html, right_html)
    return T0 + '>' + ''.join(f"<tr><td style='padding:8px 0;{'border-top:1px solid '+LN+';' if i else ''}font-size:15px;line-height:20px'>{l}</td><td align='right' style='padding:8px 0 8px 8px;{'border-top:1px solid '+LN+';' if i else ''}font-size:13px;font-weight:800;white-space:nowrap'>{r}</td></tr>" for i, (l, r) in enumerate(items)) + '</table>'
pill = lambda t, c: f"<span style='display:inline-block;background:{TINT.get(c,'#F3F4F6')};color:{c};border-radius:999px;padding:2px 9px;font-size:12px;font-weight:800'>{t}</span>"
none = lambda t: f"<div style='padding:8px 0;font-size:15px;color:{GRY}'>{t}</div>"
def stat(v, lab, c): return f"<td width='25%' style='padding:3px'><div style='background:{TINT.get(c,'#F3F4F6')};border-radius:10px;padding:10px 2px;text-align:center'><div style='font-size:24px;line-height:28px;font-weight:900;color:{c}'>{v}</div><div style='font-size:11px;line-height:14px;font-weight:700;color:{INK}'>{lab}</div></div></td>"

# ---- plan completion ----
pd = next((d for d in P['days'] if d['date'] == day), None)
planned = done = right = pc = 0
if pd:
    reset = datetime.datetime.fromtimestamp(pd['reset_at'] / 1000, datetime.timezone.utc) if pd.get('reset_at') else None
    tag = f'plan {day}'; firsts = {}
    for a in sorted(R, key=lambda a: a['created_at']):
        if tag in (a.get('part') or '') and (not reset or datetime.datetime.fromisoformat(a['created_at']) > reset): firsts.setdefault(a['question'].split(' ')[0], a)
    done = len(firsts); right = sum(a['correct'] for a in firsts.values()); planned = pd.get('n_questions') or 0
    pc = min(100, round(100 * done / planned)) if planned else 0
finished = pd and pc >= 100
pcol = G if finished else PUR if done else RED
fill = max(pc, 3)
barhtml = (f"{T0} style='border-collapse:separate;border-radius:8px;overflow:hidden;margin:10px 0 2px'><tr>"
           f"<td width='{fill}%' height='18' style='background:{pcol};height:18px;font-size:0;line-height:0'>&nbsp;</td>"
           + (f"<td width='{100-fill}%' height='18' style='background:#DDD6FE;height:18px;font-size:0;line-height:0'>&nbsp;</td>" if fill < 100 else '') + "</tr></table>")
def pbox(v, lab): return f"<td width='33%' style='padding:3px'><div style='background:rgba(255,255,255,.16);border-radius:10px;padding:8px 2px;text-align:center'><div style='font-size:24px;line-height:28px;font-weight:900;color:#fff'>{v}</div><div style='font-size:12px;font-weight:700;color:#EDE9FE'>{lab}</div></div></td>"
when = 'today' if day == datetime.datetime.now(ET).strftime('%Y-%m-%d') else pretty(day)
plan_html = (f"<div style='background:{pcol};border-radius:14px;padding:14px 14px 10px;margin:12px 0 0'>"
    f"{T0}><tr><td style='font-size:13px;font-weight:800;letter-spacing:.06em;color:#fff;text-transform:uppercase'>Daily plan · {html.escape(when)}</td>"
    f"<td align='right'><span style='background:#fff;color:{pcol};border-radius:999px;padding:3px 10px;font-size:13px;font-weight:900'>{'✓ DONE' if finished else 'NOT DONE'}</span></td></tr></table>"
    f"<div style='font-size:44px;line-height:48px;font-weight:900;color:#fff;margin-top:6px'>{pc}%<span style='font-size:18px;font-weight:800'> complete</span></div>"
    + barhtml.replace(f"background:{pcol};height", "background:#FFFFFF;height").replace("#DDD6FE", "rgba(255,255,255,.28)") +
    f"{T0} style='margin-top:8px'><tr>{pbox(planned,'Planned')}{pbox(done,'Completed')}{pbox(right,'Correct')}</tr></table></div>") if pd else ''

# ---- per-question rollup ----
asks = [m for m in T if m.get('role') == 'student' and et(m['created_at']).strftime('%Y-%m-%d') == day]
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
stuck = [k for k in wrong if not Q[k]['ok']]
helped = [k for k, e in Q.items() if e['help'] - TOOLS]
calc = [k for k, e in Q.items() if e['help'] & TOOLS]

if n:
    acc = round(100 * ok / n); secs = round(sum(a.get('seconds') or 0 for a in F) / n)
    t0 = min(et(a['created_at']) for a in R); t1 = max(et(a['created_at']) for a in R)
    stats = (f"{T0} style='margin:10px 0 0'><tr>{stat(len(Q),'Questions',NAVY)}{stat(f'{acc}%','Right 1st try',col(acc))}{stat(len(wrong),'Wrong',RED if wrong else G)}{stat(len(helped),'Used help',PUR)}</tr>"
             f"<tr>{stat(len(asks),'Tutor asks',BLUE)}{stat(len(calc),'Calculator',BLUE)}{stat(f'{secs}s','Per question',NAVY)}{stat(f'{round((t1-t0).seconds/60)}m','On HELM',NAVY)}</tr></table>")
    # callout
    flags = []
    if pd and not finished: flags.append(f"Plan only <b>{pc}%</b> done: <b>{planned-done}</b> questions left")
    if stuck: flags.append(f"<b>{len(stuck)}</b> wrong question{'s' if len(stuck)!=1 else ''} never fixed")
    if secs < 45: flags.append(f"Moving fast: <b>{secs}s</b> a question (SAT pace is 70–95s)")
    by = collections.defaultdict(lambda: [0, 0])
    for a in F: by[a['concept_id']][0] += 1; by[a['concept_id']][1] += a['correct']
    weak = [(k, v) for k, v in by.items() if v[0] >= 4 and v[1] / v[0] < .8]
    for k, v in weak: flags.append(f"<b>{nm(k)}</b> at {round(100*v[1]/v[0])}%")
    callout = (f"<div style='background:#FEF2F2;border:2px solid {RED};border-radius:14px;padding:10px 14px;margin:12px 0 0'><div style='font-size:13px;font-weight:900;letter-spacing:.06em;color:{RED}'>⚠ NEEDS ATTENTION</div>"
               + ''.join(f"<div style='font-size:15px;line-height:21px;color:{INK};padding:3px 0'>• {f}</div>" for f in flags) + "</div>") if flags else \
              f"<div style='background:#ECFDF5;border:2px solid {G};border-radius:14px;padding:10px 14px;margin:12px 0 0;font-size:15px;font-weight:800;color:{G}'>✓ Great day. Nothing needs attention.</div>"
    hl = lambda h: ' '.join(pill(HN.get(x, x), PUR) for x in sorted(h))
    res = lambda k: pill('✓ right', G) if Q[k]['first'] else pill('✗ wrong', RED)
    sec_help = section('Questions he got help on', PUR, rows([(qlink(k) + '<br>' + hl(Q[k]['help'] - TOOLS), res(k)) for k in helped]) if helped else none('None.'), len(helped))
    sec_wrong = section('Questions he got wrong', RED, rows([(qlink(k), pill('fixed on retry', G) if Q[k]['ok'] else pill('not fixed', RED)) for k in wrong]) if wrong else none('None. All right on the first try.'), len(wrong))
    sec_tutor = section('What he asked the tutor', BLUE, rows([((qlink(m['question_id']) + '<br>' if m.get('question_id') else '') + '“' + html.escape(m['content'][:200]) + '”', '') for m in asks]) if asks else none("He didn't ask the tutor anything."), len(asks))
    sec_calc = section('Calculator / reference (allowed on SAT)', BLUE, rows([(qlink(k), pill(', '.join(HN[x].split()[-1] for x in sorted(Q[k]['help'] & TOOLS)), BLUE)) for k in calc]) if calc else none('None.'), len(calc))
    sec_skill = section('By skill · weakest first', NAVY, rows([(f"<b>{nm(k)}</b> <span style='color:{GRY}'>{v[1]}/{v[0]}</span>", f"<span style='font-size:16px;color:{col(round(100*v[1]/v[0]))}'>{round(100*v[1]/v[0])}%</span>") for k, v in sorted(by.items(), key=lambda x: (x[1][1] / x[1][0], -x[1][0]))]))
    day_html = plan_html + callout + stats + sec_help + sec_wrong + sec_tutor + sec_calc + sec_skill
else:
    day_html = plan_html + f"<div style='background:#FEF2F2;border:2px solid {RED};border-radius:14px;padding:12px 14px;margin:12px 0 0;font-size:16px;font-weight:800;color:{RED}'>⚠ No HELM work on {pretty(day)}.</div>"

# ---- overall so far ----
AF = [a for a in A if (a.get('attempt') or 1) == 1]
days_active = len({et(a['created_at']).strftime('%Y-%m-%d') for a in A})
bpn = sum(x['n'] for x in BP['daily']); bpok = sum(x['n'] * x['acc'] / 100 for x in BP['daily'])
ranked = sorted([s for s in P.get('skills', []) if s.get('tried') and s.get('acc') is not None], key=lambda s: s['acc'])
hacc = round(100*sum(a['correct'] for a in AF)/len(AF)) if AF else 0; bacc = round(100*bpok/bpn) if bpn else 0
overall = (f"{T0}><tr>{stat('1010','Latest SAT',NAVY)}{stat('1050','Superscore',NAVY)}{stat('1300','Goal',PUR)}{stat(left,'Days left',RED)}</tr>"
           f"<tr>{stat(len(AF),'HELM Qs',NAVY)}{stat(f'{hacc}%','HELM right',col(hacc))}{stat(bpn,'Blueprint Qs',NAVY)}{stat(f'{bacc}%','Blueprint right',col(bacc))}</tr></table>"
           + rows([(f"<b style='color:{RED}'>Weakest</b><br>" + ', '.join(f"{s['name']} {s['acc']}%" for s in ranked[:4]), ''),
                   (f"<b style='color:{G}'>Strongest</b><br>" + ', '.join(f"{s['name']} {s['acc']}%" for s in ranked[-3:][::-1]), '')]))
nd = next((d for d in P['days'] if d['date'] == nxt), None)
plan_next = section(f'Today’s plan · {pretty(nxt)}', G, rows([(f"<b>New:</b> {', '.join(nm(k) for k in nd.get('learn', [])) or 'review day'}", ''), (f"<b>Practice:</b> {', '.join(nd.get('focus_names', []))}", ''), (f"<b>{nd.get('n_questions','?')}</b> questions", '')]), None) if nd else ''

H = f"""<div style="{FONT};color:{INK};max-width:600px;margin:0 auto;-webkit-text-size-adjust:100%">{banner}
<div style="background:{NAVY};border-radius:14px;padding:14px 16px">
<div style="font-size:12px;font-weight:800;letter-spacing:.08em;color:#C7D2FE">SAT HELM · DAILY REPORT</div>
<div style="font-size:24px;line-height:30px;font-weight:900;color:#fff">Patrick · {pretty(day)}</div>
<div style="font-size:14px;font-weight:700;color:#E0E7FF">{left} days to the SAT · Goal 1300</div></div>
{day_html}
{section('Overall so far', NAVY, overall)}
{plan_next}
<div style="text-align:center;margin:16px 0 8px"><a href="{SITE}#/stats" style="display:inline-block;background:{NAVY};color:#ffffff;text-decoration:none;font-weight:800;font-size:15px;padding:12px 22px;border-radius:10px">Open the Stats dashboard ›</a></div>
<div style="text-align:center;font-size:12px;color:{GRY}">Tap any question to open it in practice mode. Nothing is saved.</div></div>"""
print(H)
