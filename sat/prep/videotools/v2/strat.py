"""Spec-driven template for strategy videos. Each beat is one spec dict; scenes are generated per beat."""
from rw import *

def _q(ctx, s, p):
    """question card with progressive work lines"""
    chip(ctx, s.get('chip', ''), s.get('cc', C['blue']))
    y = 100
    if s.get('q'):
        lines_ = s['q'] if isinstance(s['q'], list) else [s['q']]
        h = 30 + 38 * len(lines_)
        rrect(ctx, 60, y, 1160, h, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
        for i, ln in enumerate(lines_):
            c = C['yel'] if i == len(lines_) - 1 and s.get('askhl', True) and len(lines_) > 1 else C['ink']
            write(ctx, ln, 80, y + 46 + i * 38, 26, c, seg(p, 0, .35) if s.get('newq') else 1)
        y += h + 30
    if s.get('find'):
        k = seg(p, .05, .3) if s.get('newfind') else 1
        rrect(ctx, 80, y, twidth(ctx, 'FIND: ' + s['find'], 32) + 40, 60, 12, fill=C['bg2'], stroke=C['yel'], a=k, lw=3)
        text(ctx, 'FIND: ' + s['find'], 100, y + 41, 32, C['yel'], k); y += 90
    W_ = s.get('work', []); old = s.get('old', 0)
    for i, parts in enumerate(W_):
        k = 1 if i < old else seg(p, .1 + (i - old) * .25, .35 + (i - old) * .25)
        if isinstance(parts, str): parts = [(parts, C['ink'])]
        rich(ctx, parts, 100, y + 30, 32, k); y += 62
    if s.get('ans'):
        answer(ctx, s['ans'], 100, y, max(300, twidth(ctx, s['ans'], 32) + 60), seg(p, .55, .85) if s.get('newans') else 1); y += 90
    if s.get('trap'):
        tx, ty = s.get('trap_at', (100, y + 10 if not s.get('ans') else y))
        trap(ctx, tx, ty, 640, s['trap'][0], s['trap'][1], p if s.get('newtrap', True) else 1)
    if s.get('pause'):
        text(ctx, '⏸  ' + s['pause'], 100, max(y + 40, 380), 34, C['yel'], seg(p, .6, .8))

def _title(ctx, s, p):
    text(ctx, s['title'], 100, 210, 70, C['ink'], seg(p, 0, .12))
    text(ctx, s['sub'], 102, 270, 30, C['mute'], seg(p, .1, .3), bold=False)
    for i, (txt, c) in enumerate(s.get('big', [])):
        text(ctx, txt, 100, 380 + i * 70, 44, c, seg(p, .35 + i * .2, .55 + i * .2))

def _big(ctx, s, p):
    chip(ctx, s.get('chip', ''), s.get('cc', C['blue']))
    for i, (txt, c, size) in enumerate(s['lines']):
        text(ctx, txt, 640, 220 + i * 90, size, c, seg(p, .05 + i * .22, .25 + i * .22), 'c')

def _steps(ctx, s, p):
    chip(ctx, s.get('chip', 'The method'), C['yel'])
    steps(ctx, s['steps'], 200, 240, p, .05, .95, 36, 100)

def _rows(ctx, s, p):
    chip(ctx, s.get('chip', ''), s.get('cc', C['blue']))
    for i, (a, d, c) in enumerate(s['rows']):
        k = seg(p, .05 + i * .2, .25 + i * .2)
        rrect(ctx, 120, 160 + i * 110, 1040, 84, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, a, 150, 214 + i * 110, 32, c, k); text(ctx, d, 560, 214 + i * 110, 28, C['ink'], k, 'l', False)

def _recap(ctx, s, p):
    recap(ctx, p, s['items'])

KIND = dict(q=_q, title=_title, big=_big, steps=_steps, rows=_rows, recap=_recap)

def build(D, header, specs, pads):
    NAR = json.load(open(f'{D}/beats.json'))
    assert len(NAR) == len(specs), (len(NAR), len(specs))
    PLAN, SC, CH = [], {}, {}
    for i, s in enumerate(specs):
        n = f'k{i:02d}'; PLAN.append(n)
        SC[n] = (lambda s_: (lambda ctx, b, p, t: KIND[s_['kind']](ctx, s_, p)))(s)
        if s.get('ch'): CH[n] = s['ch']
    run(D, NAR, PLAN, SC, header, SC['k00'], pads, CH)
