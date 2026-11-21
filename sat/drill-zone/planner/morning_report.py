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
barhtml = (f"{T0} style='margin:8px 0 0'><tr>"
           f"<td width='{fill}%' bgcolor='#FFFFFF' style='background:#FFFFFF;border-radius:6px 0 0 6px;height:14px;line-height:14px;font-size:10px'>&nbsp;</td>"
           + (f"<td width='{100-fill}%' bgcolor='#A78BFA' style='background:#A78BFA;border-radius:0 6px 6px 0;height:14px;line-height:14px;font-size:10px'>&nbsp;</td>" if fill < 100 else '') + "</tr></table>")
def pbox(v, lab): return f"<td width='33%' style='padding:3px'><div style='background:#8B5CF6;border-radius:10px;padding:8px 2px;text-align:center'><div style='font-size:24px;line-height:28px;font-weight:900;color:#fff'>{v}</div><div style='font-size:12px;font-weight:700;color:#EDE9FE'>{lab}</div></div></td>"
when = 'today' if day == datetime.datetime.now(ET).strftime('%Y-%m-%d') else pretty(day)
plan_html = (f"<div style='background:{pcol};border-radius:14px;padding:12px 14px 8px;margin:10px 0 0'>"
    f"{T0}><tr><td style='font-size:13px;font-weight:800;letter-spacing:.06em;color:#fff;text-transform:uppercase'>Daily plan · {html.escape(when)}</td>"
    f"<td align='right'><span style='background:#fff;color:{pcol};border-radius:999px;padding:3px 10px;font-size:13px;font-weight:900'>{'✓ DONE' if finished else 'NOT DONE'}</span></td></tr></table>"
    f"<div style='font-size:40px;line-height:42px;font-weight:900;color:#fff;margin-top:4px'>{pc}%<span style='font-size:18px;font-weight:800'> complete</span></div>"
    + barhtml +
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

# ================= Allie's approved design (table-based, inline CSS) =================
SHORT = {'Right triangles and trigonometry': 'Right triangles & trig', 'Probability and conditional probability': 'Probability',
         'Central ideas and details': 'Central ideas', 'Nonlinear equations and systems': 'Nonlinear equations',
         'Lines, angles and triangles': 'Lines, angles & triangles', 'Form, structure and sense': 'Form, structure & sense',
         'Ratios, rates, proportions and units': 'Ratios & rates', 'Observational studies and experiments': 'Observational studies',
         'Sample statistics and margin of error': 'Sample statistics', 'Text structure and purpose': 'Text structure'}
sn = lambda name: SHORT.get(name, name)
amp = lambda s: html.escape(s).replace(' and ', ' &amp; ')
DK, NV, GRN, RD, OR, MUT = '#0B2751', '#09244D', '#087638', '#AE2222', '#D97706', '#5B6C80'
FA = "font-family:Arial,Helvetica,sans-serif"
IC = "https://allieburkesport-lang.github.io/act-tutor/sat/drill-zone/planner/icons/"
EMO = {"plan":"🗓️","chart":"📊","doc":"📝","target":"🎯","xcirc":"❌","spark":"✨","calc":"🧮","watch":"⏱️","okbub":"✅","nobub":"❌","qbub":"💬","tgt":"🎯","check":"✔️","compass":"🧭"}
img = lambda k, sz, extra="": f"<span style='font-size:{max(14,int(sz*0.85))}px;line-height:{sz}px;{extra}'>{EMO[k]}</span>"
TB = "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'"
def short_q(qid): k, _, num = qid.rpartition('-'); return f"{sn(nm(k))} #{int(num) if num.isdigit() else num}"
def ql(qid): return f"<a href='{SITE}#/look/{qid}' style='color:#101C34;text-decoration:none'>{html.escape(short_q(qid))}</a>"
def item(left, right, rc, first): return (f"<tr><td style='padding:9px 0;{'' if first else 'border-top:1px solid #DFE4EB;'}font-size:14px;line-height:18px;color:#101C34'>{left}</td>"
                                         f"<td align='right' valign='top' style='padding:9px 0 9px 6px;{'' if first else 'border-top:1px solid #DFE4EB;'}font-size:13px;font-weight:800;color:{rc};white-space:nowrap'>{right}</td></tr>")
def metric(num, lab, c=DK, note='', ic='doc'):
    return (f"<td width='33%' valign='top' style='padding:4px'><div style='background:#FFFFFF;border:1px solid #DBE2ED;border-radius:12px;padding:10px 6px;height:56px'>"
            f"{TB} height='56'><tr><td width='26' valign='middle'>{img(ic, 22)}</td><td valign='middle' style='padding-left:5px'>"
            f"<div style='font-size:24px;line-height:27px;font-weight:800;color:{c}'>{num}</div><div style='font-size:11px;line-height:13px;font-weight:700;color:#101C34'>{lab}</div>"
            + (f"<div style='font-size:9px;color:#647287;margin-top:1px'>{note}</div>" if note else '') + "</td></tr></table></div></td>")
def bar(p, h=10, c='#0C8E40'):
    p = max(0, min(100, p)); w = max(p, 2)
    return (f"{TB} style='border-collapse:separate'><tr><td width='{w}%' bgcolor='{c}' style='background:{c};height:{h}px;font-size:1px;line-height:{h}px;border-radius:{h}px 0 0 {h}px'>&nbsp;</td>"
            + (f"<td width='{100-w}%' bgcolor='#D4DCE9' style='background:#D4DCE9;height:{h}px;font-size:1px;line-height:{h}px;border-radius:0 {h}px {h}px 0'>&nbsp;</td>" if w < 100 else '') + "</tr></table>")
def h2(t): return f"<div style='font-size:21px;font-weight:800;color:{NV};margin:20px 0 9px'>{img('chart', 22, 'margin:-3px 6px 0 0')}{t}</div>"
def panel(title, sym, bg, bub, rows_html):
    return (f"<div style='background:{bg};border-radius:14px;padding:11px 9px 9px'>"
            f"<div style='font-size:15px;line-height:20px;font-weight:800;color:#101C34;margin:0 0 8px'>{img(sym, 22, 'margin:-3px 5px 0 0')}{title}</div>"
            f"<div style='background:#FFFFFF;border-radius:11px;padding:2px 9px'>{rows_html}</div></div>")
def tk(label, text): return (f"<tr><td valign='top' width='26' style='padding:6px 0'>{img('check', 19)}</td>"
                             f"<td style='padding:6px 0;font-size:15px;line-height:21px;color:#101C34'><b>{label}:</b> {text}</td></tr>")

# hero
hero = (f"<div style='background:#063462;background-image:linear-gradient(110deg,#061D38,#063462 70%,#0A2747);border-left:6px solid #81B4D8;padding:18px 18px 16px'>{TB}><tr><td valign='middle'>"
        f"<div style='font-size:16px;font-weight:800;color:#80C3F1'>Patrick's</div>"
        f"<div style='font-size:30px;line-height:33px;font-weight:800;color:#FFFFFF;letter-spacing:-.5px;margin:2px 0 10px'>SAT HELM Report</div>"
        f"<div style='font-size:15px;color:#FFFFFF'>{pretty(day)} &nbsp;|&nbsp; Goal: <b>1300</b><br>SAT Dec&nbsp;5 · <b>{left} days</b> left</div></td><td width='70' align='right' valign='middle'>{img('compass', 64, 'opacity:.55')}</td></tr></table></div>")
# plan
if pd:
    status = ("<span style='display:inline-block;background:#E7F5ED;color:#087638;border-radius:30px;font-size:13px;font-weight:700;padding:4px 11px;margin-top:5px'>Completed</span>" if finished
              else "<span style='display:inline-block;background:#FAE7E8;color:#B32428;border-radius:30px;font-size:13px;font-weight:700;padding:4px 10px;margin-top:5px;white-space:nowrap'>Not Completed</span>")
    plan = (f"<div style='border:1px solid #D9E1EE;border-radius:16px;padding:13px 12px;background:#F7F9FC'>{TB}><tr>"
            f"<td width='46%' valign='middle' style='border-right:1px solid #CBD4E1;padding-right:8px'>{TB}><tr><td width='40' valign='middle'>{img('plan', 34)}</td><td valign='middle' style='padding-left:6px'><div style='font-size:17px;font-weight:800;color:#101C34'>Today's Plan</div>{status}</td></tr></table></td>"
            f"<td valign='middle' style='padding-left:12px'><div style='font-size:15px;color:#101C34'><span style='font-size:30px;font-weight:800;color:#071A35'>{pc}%</span> <b>Complete</b></div>"
            f"<div style='margin:6px 0'>{bar(pc, 10)}</div><div style='font-size:13px;color:#34435A'><b>{done} / {planned}</b> completed · <b>{right}</b> correct</div></td></tr></table></div>")
else: plan = ''

if n:
    acc = round(100 * ok / n); secs = round(sum(a.get('seconds') or 0 for a in F) / n)
    t0 = min(et(a['created_at']) for a in R); t1 = max(et(a['created_at']) for a in R); mins = round((t1 - t0).seconds / 60)
    summary = (h2('Summary of the Day') + f"<div style='background:#F0F3F9;border-radius:15px;padding:6px'>{TB}>"
        f"<tr>{metric(len(Q),'Questions Done',ic='doc')}{metric(f'{acc}%','Right First Try', GRN if acc>=80 else OR, ic='target')}{metric(len(wrong),'Wrong', RD, ic='xcirc')}</tr>"
        f"<tr>{metric(len(helped),'Used Help On', OR, ic='spark')}{metric(len(calc),'Used Calculator', ic='calc')}{metric(f'{secs}s','Time per Question', DK, ic='watch')}</tr></table></div>"
        f"<div style='font-size:13px;color:{MUT};margin-top:7px'>{mins} minutes on HELM &nbsp;·&nbsp; {len(asks)} tutor question{'s' if len(asks)!=1 else ''} asked</div>")
    HN2 = {k: v for k, v in HN.items()}
    hrows = ''.join(item(ql(k) + "<div style='font-size:11px;color:#5B6C80;margin-top:2px'>" + ', '.join(HN2.get(x, x) for x in sorted(Q[k]['help'] - TOOLS)) + "</div>",
                         '✓ Right' if Q[k]['first'] else '✕ Wrong', '#00833E' if Q[k]['first'] else '#C21D1D', i == 0) for i, k in enumerate(helped)) or item('None', '', MUT, True)
    wrows = ''.join(item(ql(k), 'Fixed' if Q[k]['ok'] else 'Not fixed', '#00833E' if Q[k]['ok'] else '#C21D1D', i == 0) for i, k in enumerate(wrong)) or item('None', '', MUT, True)
    panels = (f"<div style='margin-top:18px'>{panel(f'Questions He Got Help On ({len(helped)})', 'okbub', '#E7F5ED', '#239D6C', TB + '>' + hrows + '</table>')}</div>"
              f"<div style='margin-top:12px'>{panel(f'Questions He Got Wrong ({len(wrong)})', 'nobub', '#FAE8E9', '#D83D37', TB + '>' + wrows + '</table>')}</div>")
    tutor = (f"<div style='margin-top:12px'>{panel(f'What He Asked the Tutor ({len(asks)})', 'qbub', '#E9F2FC', '#24639E', TB + '>' + ''.join(item((ql(m['question_id']) + '<br>' if m.get('question_id') else '') + '“' + html.escape(m['content'][:200]) + '”', '', MUT, i == 0) for i, m in enumerate(asks)) + '</table>')}</div>") if asks else ''
    by = collections.defaultdict(lambda: [0, 0, 0])
    for a in F: v = by[a['concept_id']]; v[0] += 1; v[1] += a['correct']; v[2] += a.get('seconds') or 0
    order = sorted(by.items(), key=lambda x: (x[1][1] / x[1][0], -x[1][0]))
    def srow(k, v, first):
        p = round(100 * v[1] / v[0]); c = GRN if p >= 80 else OR if p >= 60 else RD
        bt = '' if first else 'border-top:1px solid #DCE3EB;'
        return (f"<tr><td style='padding:9px 0;{bt}font-size:13px;line-height:16px;font-weight:700;color:#101C34'>{amp(sn(nm(k)))}</td>"
                f"<td width='26%' style='padding:9px 6px;{bt}'>{bar(p, 8, '#0C8E40' if p >= 80 else OR if p >= 60 else '#C21D1D')}</td>"
                f"<td width='40' align='right' style='padding:9px 0;{bt}font-size:12px;color:#101C34;white-space:nowrap'>{v[1]}/{v[0]}</td>"
                f"<td width='44' align='right' style='padding:9px 0;{bt}font-size:16px;font-weight:800;color:{c}'>{p}%</td></tr>")
    weak5 = [x for x in order if x[1][1] < x[1][0]][:5] or order[:5]
    perfect = [k for k, v in order if v[1] == v[0] and (k, v) not in weak5]
    skills = (h2('By Skill (Weakest First)') + TB + '>' + ''.join(srow(k, v, i == 0) for i, (k, v) in enumerate(weak5)) + '</table>'
              + (f"<div style='font-size:13px;color:#101C34;margin-top:8px'><b style='color:{GRN}'>100%:</b> " + ', '.join(amp(sn(nm(k))) for k in perfect) + "</div>" if perfect else ''))
    slow = max(by.items(), key=lambda x: x[1][2] / x[1][0])
    takes = [tk('Weakest skill', f"{amp(sn(nm(order[0][0])))} ({round(100*order[0][1][1]/order[0][1][0])}%)"),
             tk('Slowest skill', f"{amp(sn(nm(slow[0])))} (~{round(slow[1][2]/slow[1][0])}s/question)"),
             tk('Speed', f"{secs}s/question (SAT pace: 70–95s)")]
    if stuck: takes.append(tk('Review next', f"{len(stuck)} unresolved missed question{'s' if len(stuck)!=1 else ''}: " + ', '.join(f"<a href='{SITE}#/look/{k}' style='color:#24639E'>{html.escape(short_q(k))}</a>" for k in stuck)))
    if pd and not finished: takes.append(tk('Plan', f"{planned - done} of {planned} planned questions still left"))
    if calc: takes.append(tk('Calculator', 'Desmos on ' + ', '.join(html.escape(short_q(k)) for k in calc)))
    day_html = plan + summary + panels + tutor + skills
else:
    takes = [tk('No work', f"No HELM questions on {pretty(day)}")]
    day_html = plan

# overall + tomorrow inside takeaways
AF = [a for a in A if (a.get('attempt') or 1) == 1]
hacc = round(100*sum(a['correct'] for a in AF)/len(AF)) if AF else 0
bpn = sum(x['n'] for x in BP['daily']); bacc = round(100*sum(x['n']*x['acc']/100 for x in BP['daily'])/bpn) if bpn else 0
takes.append(tk('Overall', f"HELM {len(AF)} questions at {hacc}% · Blueprint {bpn} at {bacc}% · Best SAT 1050 (goal 1300)"))
nd = next((d for d in P['days'] if d['date'] == nxt), None)
if nd: takes.append(tk('Tomorrow', f"{nd.get('n_questions','?')} questions: " + amp(', '.join(sn(nm(k)) for k in nd.get('learn', []))) + (' + review' if nd.get('focus_names') else '')))
takeaway = (f"<div style='margin-top:20px;border-radius:15px;padding:14px 14px 10px;background:#E9F2FC'><div style='font-size:21px;font-weight:800;color:{NV};margin:0 0 6px'>{img('tgt', 24, 'margin:-3px 6px 0 0')}Key Takeaways</div>"
            f"{TB}>{''.join(takes)}</table></div>")
btn = f"<div style='text-align:center;margin:18px 0 6px'><a href='{SITE}#/stats' style='display:inline-block;background:#063462;color:#FFFFFF;text-decoration:none;font-weight:700;font-size:15px;padding:13px 24px;border-radius:10px'>Open the Stats dashboard</a></div>"
foot = f"<div style='text-align:center;color:#66778B;font-size:12px;padding:10px 0 16px'>SAT HELM • Daily progress report • {D0.strftime('%B %-d')}<br>Tap a question to open it in practice mode (nothing is saved).</div>"
H = (f"<div style='{FA};color:#101C34;max-width:600px;margin:0 auto;-webkit-text-size-adjust:100%'>{banner}{hero}"
     f"<div style='padding:12px 10px 0'>{day_html}{takeaway}{btn}{foot}</div></div>")
import emailsafe
print(emailsafe.fix(H))
