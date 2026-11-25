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

# SAT rules (Allie, Nov 23): a question scores only the FIRST time he ever answers it, and only if he opened no help before answering.
def _scored(rows):
    seen, out = set(), []
    for a in sorted(rows, key=lambda a: a['created_at']):
        if (a.get('attempt') or 1) != 1: continue
        q = (a.get('question') or '').split(' ')[0]
        if q in seen: continue
        seen.add(q)
        if et(a['created_at']).strftime('%Y-%m-%d') < '2026-11-22': continue  # Nov 21 warm-up never counts (Allie, Nov 23)
        hm = re.search(r'help ([a-z+]+)', a.get('part') or '')
        if 'coached' in (a.get('part') or '') or (hm and set(hm.group(1).split('+')) - {'desmos', 'ref'}): continue  # Desmos + reference sheet are SAT tools, not help
        out.append(a)
    return out
SC = _scored(A); SCID = {id(a) for a in SC}
R = [a for a in A if et(a['created_at']).strftime('%Y-%m-%d') == day]
F = [a for a in R if id(a) in SCID]
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
    done = len(firsts); right = sum(a['correct'] for a in firsts.values() if id(a) in SCID); planned = pd.get('n_questions') or 0
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
            f"<td width='46%' valign='middle' style='border-right:1px solid #CBD4E1;padding-right:8px'>{TB}><tr><td width='40' valign='middle'>{img('plan', 34)}</td><td valign='middle' style='padding-left:6px'><div style='font-size:17px;font-weight:800;color:#101C34'>Yesterday's Plan</div>{status}</td></tr></table></td>"
            f"<td valign='middle' style='padding-left:12px'><div style='font-size:15px;color:#101C34'><span style='font-size:30px;font-weight:800;color:#071A35'>{pc}%</span> <b>Complete</b></div>"
            f"<div style='margin:6px 0'>{bar(pc, 10)}</div><div style='font-size:13px;color:#34435A'><b>{done} / {planned}</b> completed · <b>{right}</b> correct</div></td></tr></table></div>")
else: plan = ''

takes = []; WINS = []; coach = ''
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
    # Tutor results (Allie, Nov 23): did he get the question right after asking, and how did he do on NEW questions of that skill afterwards (SAT rules: first try, no help)
    def tutor_after(m):
        qid = m.get('question_id'); qa = next((a for a in A if (a.get('question') or '').split(' ')[0] == qid), None)
        sk = qa.get('concept_id') if qa else None; t0 = m['created_at']
        rows = [a for a in A if a['created_at'] > t0 and (a.get('question') or '').split(' ')[0] == qid]
        res = ('✓ Right after tutor', '#00833E') if any(a['correct'] for a in rows) else (('✓ Already right', '#00833E') if qid in Q and Q[qid]['first'] else ('✕ Not solved yet', '#C21D1D'))
        nx = [a for a in SC if sk and a.get('concept_id') == sk and a['created_at'] > t0 and (a.get('question') or '').split(' ')[0] != qid]
        after = f"<div style='font-size:12px;color:#5B6C80;margin-top:3px'>{html.escape(nm(sk)) if sk else 'This skill'} since: <b style='color:#101C34'>{sum(a['correct'] for a in nx)} of {len(nx)}</b> new questions right, no help</div>" if nx else f"<div style='font-size:12px;color:#5B6C80;margin-top:3px'>No new {html.escape(nm(sk)) if sk else ''} questions since yet</div>"
        return res, after
    tg = collections.OrderedDict()
    for m in asks: tg.setdefault(m.get('question_id') or m['created_at'], []).append(m)
    trows = list(tg.items())
    def trow(i, k, ms):
        res, after = tutor_after(ms[0])
        left = (ql(ms[0]['question_id']) + '<br>' if ms[0].get('question_id') else '') + '<br>'.join('“' + html.escape(m['content'][:200]) + '”' for m in ms) + after
        return item(left, res[0], res[1], i == 0)
    tutor = (f"<div style='margin-top:12px'>{panel(f'What He Asked the Tutor ({len(trows)})', 'qbub', '#E9F2FC', '#24639E', TB + '>' + ''.join(trow(i, k, ms) for i, (k, ms) in enumerate(trows)) + '</table>')}</div>") if asks else ''
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
    # ---- Trend (Allie, Nov 25): right-first-try % per day (SAT rules) so she can see if he is getting more right ----
    byd = collections.OrderedDict()
    for a in sorted(SC, key=lambda a: a['created_at']):
        dd = et(a['created_at']).strftime('%Y-%m-%d')
        if dd > day: continue
        v = byd.setdefault(dd, [0, 0]); v[0] += 1; v[1] += a['correct']
    tdays = [(d, v) for d, v in byd.items() if v[0] >= 5][-6:]
    def trow_d(i, d, v):
        p = round(100 * v[1] / v[0]); bt = '' if i == 0 else 'border-top:1px solid #DCE3EB;'
        c = '#0C8E40' if p >= 80 else OR if p >= 60 else '#C21D1D'
        return (f"<tr><td width='70' style='padding:8px 0;{bt}font-size:13px;font-weight:{800 if d == day else 600};color:#101C34'>{datetime.date.fromisoformat(d).strftime('%a %-m/%-d')}</td>"
                f"<td style='padding:8px 6px;{bt}'>{bar(p, 8, c)}</td><td width='44' align='right' style='padding:8px 0;{bt}font-size:12px;color:#101C34'>{v[1]}/{v[0]}</td>"
                f"<td width='44' align='right' style='padding:8px 0;{bt}font-size:16px;font-weight:800;color:{c}'>{p}%</td></tr>")
    trend = ''
    if len(tdays) >= 2:
        ps = [round(100 * v[1] / v[0]) for _, v in tdays]; dlt = ps[-1] - ps[-2]
        arrow = (f"<span style='color:{GRN}'>▲ up {dlt} points</span>" if dlt > 0 else f"<span style='color:#C21D1D'>▼ down {-dlt} points</span>" if dlt < 0 else "<span>no change</span>")
        sk_tr = []
        for k in sorted({a['concept_id'] for a in F}):
            bef = [a for a in SC if a.get('concept_id') == k and et(a['created_at']).strftime('%Y-%m-%d') < day]
            now = [a for a in F if a.get('concept_id') == k]
            if len(bef) >= 3 and now:
                pb, pn = round(100 * sum(a['correct'] for a in bef) / len(bef)), round(100 * sum(a['correct'] for a in now) / len(now))
                sk_tr.append(f"{amp(sn(nm(k)))}: {pb}% before → <b style='color:{GRN if pn > pb else '#C21D1D' if pn < pb else '#101C34'}'>{pn}%</b>")
        trend = (h2('Trend · Right on First Try') + f"<div style='font-size:14px;color:#101C34;margin:-4px 0 6px'>{pretty(day)} vs. his last practice day: <b>{arrow}</b></div>"
                 + TB + '>' + ''.join(trow_d(i, d, v) for i, (d, v) in enumerate(tdays)) + '</table>'
                 + (f"<div style='font-size:13px;color:#101C34;margin-top:8px;line-height:20px'>{'<br>'.join(sk_tr)}</div>" if sk_tr else '')
                 + f"<div style='font-size:11px;color:{MUT};margin-top:6px'>SAT rules: first answer only, no help. Days with fewer than 5 questions are left out.</div>")
        takes.insert(0, tk('Trend', f"{ps[-1]}% right on first try, {'up' if dlt > 0 else 'down' if dlt < 0 else 'same as'} {abs(dlt) if dlt else ''}{' points from' if dlt else ''} {ps[-2]}% last practice day"))
    # ---- Follow-ups ("Prove it") (Allie, Nov 25): how many were added, did he get them, did he use help on them ----
    fu = collections.OrderedDict(); pl = collections.OrderedDict()
    for a in sorted(R, key=lambda a: a['created_at']):
        qid = a['question'].split(' ')[0]; part = a.get('part') or ''
        m = re.search(r'prove it (\d)', part); tgt = fu if m else pl
        e = tgt.setdefault(qid, {'first': None, 'ok': False, 'help': set(), 'k': int(m.group(1)) if m else 0, 'sk': a.get('concept_id')})
        if e['first'] is None: e['first'] = a['correct']
        e['ok'] = e['ok'] or a['correct']
        hm = re.search(r'help ([\w+]+)', part)
        if hm: e['help'] |= set(hm.group(1).split('+')) - TOOLS
        if 'coached' in part: e['help'].add('show')
    for m in asks:
        if m.get('question_id') in fu: fu[m['question_id']]['help'].add('tutor')
    follow = ''
    if fu:
        f1 = sum(1 for e in fu.values() if e['first']); fh = [k for k, e in fu.items() if e['help']]
        p1 = sum(1 for e in pl.values() if e['first']); fp, pp = round(100 * f1 / len(fu)), round(100 * p1 / len(pl)) if pl else 0
        cnt = collections.Counter(e['sk'] for e in fu.values())
        frows = ''.join(item(ql(k) + f"<div style='font-size:11px;color:#5B6C80;margin-top:2px'>Prove it {e['k']}" + (' · help: ' + ', '.join(HN.get(x, x) for x in sorted(e['help'])) if e['help'] else ' · no help') + "</div>",
                             '✓ Right' if e['first'] else ('Fixed' if e['ok'] else '✕ Wrong'), '#00833E' if e['first'] else (OR if e['ok'] else '#C21D1D'), i == 0) for i, (k, e) in enumerate(fu.items()))
        follow = (f"<div style='margin-top:12px'>{panel(f'Follow-Up Questions Added ({len(fu)})', 'spark', '#FFF4E5', OR, TB + '>' + frows + '</table>')}</div>"
                  f"<div style='font-size:13px;color:#101C34;margin-top:7px;line-height:19px'>Added on top of the plan after a miss or help: "
                  + ', '.join(f"{amp(sn(nm(k)))} {v}" for k, v in cnt.items())
                  + f".<br>Right on first try: <b>{f1} of {len(fu)} ({fp}%)</b> on follow-ups vs. <b>{p1} of {len(pl)} ({pp}%)</b> on planned questions."
                  + f"<br>Help used on follow-ups: <b>{len(fh) if fh else 'none'}</b>{' (' + ', '.join(html.escape(short_q(k)) for k in fh) + ')' if fh else ' — he did them on his own'}.</div>")
        takes.insert(1 if trend else 0, tk('Follow-ups', f"{len(fu)} added, {f1} right on first try ({fp}%), help on {len(fh) if fh else 'none'}"))
    # ---- Category breakdown (Allie, Nov 25): planned vs. first pass vs. follow-ups, change, test weight, SAT + Blueprint vs. today, insights ----
    SAT_OFF = [('Sep 12', {'alg': '550–600', 'adv': '550–600', 'psda': '470–540', 'geo': '420–460', 'ii': '490–540', 'cs': '490–540', 'eoi': '490–540', 'sec': '490–540'}),
               ('Oct 3', {'alg': '470–540', 'adv': '550–600', 'psda': '550–600', 'geo': '470–540', 'ii': '420–480', 'cs': '490–540', 'eoi': '200–360', 'sec': '420–480'}),
               ('Nov 7', {'alg': '550–600', 'adv': '470–540', 'psda': '420–460', 'geo': '610–670', 'ii': '420–480', 'cs': '420–480', 'eoi': '550–600', 'sec': '490–540'})]
    DOMK = {'Algebra': 'alg', 'Advanced Math': 'adv', 'Problem-Solving and Data Analysis': 'psda', 'Geometry and Trigonometry': 'geo', 'Information and Ideas': 'ii',
            'Craft and Structure': 'cs', 'Expression of Ideas': 'eoi', 'Standard English Conventions': 'sec'}
    def dpct(band): a, _, z = band.partition('–'); return round(((int(a) + int(z or a)) / 2 - 200) / 6)
    KINDS = [('seq', r'sequence|\bterm\b', 'sequences (the n − 1 pattern)'), ('abs', r'\||absolute', 'absolute value'),
             ('vertex', r'vertex|minimum|maximum', 'vertex form / min–max'), ('zeros', r'x-intercept|zeros?\b|roots?\b|\(x\s*[−-]\s*\d+\)\s*\(x', 'zeros & factored form'),
             ('exp', r'exponential|grow|decay|doubl|percent|%|\(\s*[01]?\.\d+\s*\)|\d\.\d\d\)', 'exponential growth & decay'),
             ('fee', r'charge|fee|cost|\$|per\b|ticket', 'word problems: fixed fee + rate'), ('consts', r'constants?\b', 'unknown constants (a, b, c)'),
             ('slope', r'slope|rate of change', 'slope / rate of change'), ('table', r'table', 'reading a table'), ('area', r'area|rectangular|length|width', 'area & dimensions'),
             ('prod', r'product|consecutive|integers', 'number word problems'), ('quad', r'²|squared|quadratic|parabola', 'quadratics'), ('graph', r'graph|xy-plane', 'reading a graph')]
    def kind(qtext):
        for k, rx, lab in KINDS:
            if re.search(rx, qtext or '', re.I): return lab
        return 'other'
    pskills = {x['skill']: x for x in P.get('skills', [])}
    mix = dict((k, n) for k, n, *_ in (pd or {}).get('mix', []))
    qrows = collections.OrderedDict()
    for a in sorted(R, key=lambda a: a['created_at']):
        qid = a['question'].split(' ')[0]; part = a.get('part') or ''
        e = qrows.setdefault(qid, {'sk': a.get('concept_id'), 'fu': bool(re.search(r'prove it \d', part)), 'first': a['correct'], 'ok': False, 'sec': a.get('seconds') or 0,
                                   'kind': kind((a.get('question') or '').split(' ', 1)[-1])})
        e['ok'] = e['ok'] or a['correct']
    cats = [k for k in list(mix) + [e['sk'] for e in qrows.values()] if any(e['sk'] == k for e in qrows.values())]
    cats = list(dict.fromkeys(cats))
    def pct(a, b): return round(100 * a / b) if b else None
    def ln(lab, val): return f"<tr><td style='padding:6px 0;border-top:1px solid #DCE3EB;font-size:13px;color:#34435A'>{lab}</td><td align='right' style='padding:6px 0;border-top:1px solid #DCE3EB;font-size:14px;color:#101C34'>{val}</td></tr>"
    def chg(d): return '—' if d is None else (f"<b style='color:{GRN}'>▲ +{d} pts</b>" if d > 0 else f"<b style='color:#C21D1D'>▼ {d} pts</b>" if d < 0 else '<b>no change</b>')
    cards = ''
    for k in cats:
        ps = pskills.get(k, {}); sec_ = SK.get(k, {}).get('sec'); N = 44 if sec_ == 'Math' else 54; share = ps.get('share') or 0; nq = round(share / 100 * N)
        fp = [e for e in qrows.values() if e['sk'] == k and not e['fu']]; fu_ = [e for e in qrows.values() if e['sk'] == k and e['fu']]
        fpr, fur = sum(e['first'] for e in fp), sum(e['first'] for e in fu_); pf, pu = pct(fpr, len(fp)), pct(fur, len(fu_))
        dom = SK.get(k, {}).get('dom') or ''; dk = DOMK.get(dom)
        sat = ' · '.join(f"{lab} {dpct(d[dk])}%" for lab, d in SAT_OFF if dk and d.get(dk)) or '—'
        bp = BP['skills'].get(k); bpp = pct(bp['ok'], bp['n']) if bp else None
        before = [a for a in SC if a.get('concept_id') == k and et(a['created_at']).strftime('%Y-%m-%d') < day]; hb = pct(sum(a['correct'] for a in before), len(before))
        allq = fp + fu_; today = pct(sum(e['first'] for e in allq), len(allq))
        # insights by kind of question
        kk = collections.OrderedDict()
        for e in fp: kk.setdefault(e['kind'], [[0, 0], [0, 0]])[0][0] += 1; kk[e['kind']][0][1] += e['first']
        for e in fu_: kk.setdefault(e['kind'], [[0, 0], [0, 0]])[1][0] += 1; kk[e['kind']][1][1] += e['first']
        ins = []
        hard = [(lab, v) for lab, v in kk.items() if lab != 'other' and v[0][0] and v[0][1] / v[0][0] < .5]
        if hard: ins.append('Struggled at first with ' + '; '.join(f"{lab} ({v[0][1]} of {v[0][0]} right)" for lab, v in hard[:3]) + '.')
        better = [(lab, v) for lab, v in kk.items() if lab != 'other' and v[1][0] and v[1][1] / v[1][0] >= .6 and (not v[0][0] or v[1][1] / v[1][0] > v[0][1] / v[0][0])]
        if better: ins.append('Improved on ' + '; '.join(f"{lab} ({v[0][1]}/{v[0][0]} → {v[1][1]}/{v[1][0]})" if v[0][0] else f"{lab} ({v[1][1]}/{v[1][0]} on follow-ups)" for lab, v in better[:3]) + '.')
        still = [(lab, v) for lab, v in kk.items() if lab != 'other' and v[1][0] and v[1][1] / v[1][0] < .6]
        if still: ins.append('Still shaky: ' + '; '.join(f"{lab} ({v[1][1]} of {v[1][0]} on follow-ups)" for lab, v in still[:3]) + '.')
        if fp and fu_:
            t1, t2 = round(sum(e['sec'] for e in fp) / len(fp)), round(sum(e['sec'] for e in fu_) / len(fu_))
            if abs(t1 - t2) >= 10: ins.append(f"{'Faster' if t2 < t1 else 'Slower'} on follow-ups: {t1}s → {t2}s per question.")
        if hb is not None and today is not None and today - hb >= 10: ins.append(f"Yesterday ({today}%) was well above his HELM average before that ({hb}%) in this category.")
        # What this category is worth (Allie, Nov 25): baseline = his best official SAT level in this domain (superscore rule); goal level for 1300 ≈ 75% right
        ppq = 600 / N; bestp = max((dpct(d[dk]) for _, d in SAT_OFF if dk and d.get(dk)), default=None)
        base_r = round((bestp if bestp is not None else (bpp or 50)) / 100 * nq); goal_r = min(nq, -(-75 * nq // 100)); gain_q = max(0, goal_r - base_r); gain = round(gain_q * ppq)
        worth = (f"Keep going: getting to the 1300 level here (<b>{goal_r} of {nq}</b> right, up from about {base_r} at his best SAT) adds about <b style='color:{GRN}'>+{gain} points</b> to his {'Math' if N == 44 else 'R&amp;W'} score."
                 if gain else f"He is already at the 1300 level here ({base_r} of {nq}). Keep it there.")
        WINS.append({'k': k, 'today': today, 'bp': bpp, 'hb': hb, 'gain': gain, 'goal_r': goal_r, 'nq': nq, 'sec': 'Math' if N == 44 else 'Reading & Writing', 'pf': pf, 'pu': pu})
        cards += (f"<div style='margin-top:12px;border:1px solid #D9E1EE;border-radius:14px;padding:11px 12px;background:#FFFFFF'>"
                  f"<div style='font-size:16px;font-weight:800;color:#101C34'>{amp(nm(k))}</div>"
                  f"<div style='font-size:12px;color:{MUT};margin:2px 0 6px'>{html.escape(dom)} · about <b>{share:g}%</b> of the {'Math' if N == 44 else 'Reading &amp; Writing'} section ≈ <b>{nq} of {N}</b> questions on the test</div>"
                  f"{TB}>"
                  + ln('Planned', f"<b>{mix.get(k, 0)}</b>")
                  + ln('First pass (did / right first try)', f"<b>{len(fp)}</b> · {fpr} right" + (f" (<b>{pf}%</b>)" if pf is not None else ''))
                  + ln('Follow-ups added (right first try)', f"<b>{len(fu_)}</b> · {fur} right" + (f" (<b>{pu}%</b>)" if pu is not None else ''))
                  + ln('Change: follow-ups vs. first pass', chg(pu - pf) if pf is not None and pu is not None else '—')
                  + ln('Overall (first try)', f"<b>{today}%</b>" if today is not None else '—')
                  + ln('HELM before that day', f"{hb}% ({len(before)} q)" if hb is not None else '—')
                  + ln('Blueprint', f"{bpp}% ({bp['n']} q)" if bp else '—')
                  + ln(f"Official SAT ({html.escape(dom)} score band)", sat)
                  + "</table>"
                  + f"<div style='margin-top:8px;background:#E7F5ED;border-radius:10px;padding:8px 10px;font-size:13px;line-height:19px;color:#101C34'>🎯 {worth}</div>"
                  + (f"<div style='margin-top:8px;background:#F7F9FC;border-radius:10px;padding:8px 10px;font-size:13px;line-height:19px;color:#101C34'><b>Insights</b><br>" + '<br>'.join('• ' + html.escape(x) for x in ins) + "</div>" if ins else '')
                  + "</div>")
    untouched = [k for k in mix if k not in cats]
    catsec = (h2('By Category · Planned vs. Follow-Ups') + cards
              + (f"<div style='font-size:13px;color:#101C34;margin-top:10px'><b>Planned but not reached:</b> " + ', '.join(f"{amp(sn(nm(k)))} ({mix[k]})" for k in untouched) + "</div>" if untouched else '')
              + f"<div style='font-size:11px;color:{MUT};margin-top:6px'>Test share = this category's share of its SAT section (44 Math / 54 Reading &amp; Writing questions). Official SAT % is estimated from the College Board score band for the whole domain, not just this category.</div>") if cats else ''
    # ---- Words of encouragement for Patrick (Allie, Nov 25): honest, based on the real numbers ----
    up = [w for w in WINS if w['today'] is not None and ((w['bp'] is not None and w['today'] > w['bp']) or (w['pf'] is not None and w['pu'] is not None and w['pu'] > w['pf']))]
    lines = []
    tps = [round(100 * v[1] / v[0]) for _, v in tdays]
    tr_up = len(tps) >= 2 and tps[-1] > tps[-2]
    if tr_up or up:
        lines.append("With all of your hard work, this is really paying off. <b>Good job!</b>")
    else:
        lines.append("Tough questions yesterday, and you kept working through them. That is exactly how scores go up. <b>Keep going!</b>")
    if tr_up: lines.append(f"You got <b>{tps[-1]}%</b> right on the first try, up <b>{tps[-1]-tps[-2]} points</b> from your last practice day.")
    for w in up[:2]:
        frm = f"{w['bp']}% on Blueprint" if w['bp'] is not None and w['today'] > w['bp'] else f"{w['pf']}% on your first pass"
        to = f"{w['today']}% yesterday" if w['bp'] is not None and w['today'] > w['bp'] else f"{w['pu']}% on the follow-ups"
        lines.append(f"<b>{amp(nm(w['k']))}</b>: from {frm} to <b>{to}</b>.")
    tot = sum(w['gain'] for w in WINS)
    gw = [w for w in WINS if w['gain']]
    if gw:
        lines.append("Keep going and your score will lift: " + '; '.join(f"getting {amp(nm(w['k']))} to the 1300 level ({w['goal_r']} of {w['nq']} on the test) is worth about <b>+{w['gain']} points</b>" for w in gw[:3])
                     + (f" — about <b>+{tot} points</b> together toward your 1300 goal." if len(gw) > 1 else " toward your 1300 goal."))
    coach = (f"<div style='margin:12px 0 0;border-radius:14px;padding:13px 14px;background:#E7F5ED;border-left:6px solid #0C8E40'>"
             f"<div style='font-size:17px;font-weight:800;color:#087638;margin-bottom:4px'>💪 Patrick, great work</div>"
             f"<div style='font-size:15px;line-height:22px;color:#101C34'>{'<br>'.join(lines)}</div></div>")
    slow = max(by.items(), key=lambda x: x[1][2] / x[1][0])
    takes += [tk('Weakest skill', f"{amp(sn(nm(order[0][0])))} ({round(100*order[0][1][1]/order[0][1][0])}%)"),
             tk('Slowest skill', f"{amp(sn(nm(slow[0])))} (~{round(slow[1][2]/slow[1][0])}s/question)"),
             tk('Speed', f"{secs}s/question (SAT pace: 70–95s)")]
    if stuck: takes.append(tk('Review next', f"{len(stuck)} unresolved missed question{'s' if len(stuck)!=1 else ''}: " + ', '.join(f"<a href='{SITE}#/look/{k}' style='color:#24639E'>{html.escape(short_q(k))}</a>" for k in stuck)))
    if pd and not finished: takes.append(tk('Plan', f"{planned - done} of {planned} planned questions still left"))
    if calc: takes.append(tk('Calculator', 'Desmos on ' + ', '.join(html.escape(short_q(k)) for k in calc)))
    day_html = coach + plan + summary + trend + catsec + panels + follow + tutor + skills
else:
    takes = [tk('No work', f"No HELM questions on {pretty(day)}")]
    day_html = plan

# overall + tomorrow inside takeaways
AF = SC
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
