import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a5'
NAR = json.load(open(f'{D}/beats.json'))

def nl(ctx, lo, hi, k, y=470, x0=160, x1=1120):
    if k <= 0: return None
    line(ctx, x0, y, x1, y, C['mute'], 3, k)
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    for v in range(lo, hi + 1):
        line(ctx, X(v), y - 8, X(v), y + 8, C['mute'], 2, 1, k); text(ctx, str(v).replace('-', '−'), X(v), y + 36, 20, C['mute'], k, 'c', False)
    return X
def ray(ctx, X, v, left, closed, c, k, y=470, lo=None, hi=None):
    if k <= 0: return
    end = X(lo) if left else X(hi)
    line(ctx, X(v), y, X(v) + (end - X(v)) * k, y, c, 8, 1)
    if closed: disc(ctx, X(v), y, 12, c, 1)
    else: arc(ctx, X(v), y, 11, 0, 2 * math.pi, c, 4, 1); disc(ctx, X(v), y, 7, C['bg'], 1)

def s_hook(ctx, b, p, t):
    text(ctx, 'Inequalities', 100, 200, 70, C['ink'], seg(p, 0, .12))
    for i, s in enumerate(['<', '>', '≤', '≥']):
        k = seg(p, .15 + i * .08, .3 + i * .08)
        rrect(ctx, 100 + i * 150, 260, 120, 110, 16, fill=C['bg2'], stroke=C['blue'], a=k, lw=3); text(ctx, s, 160 + i * 150, 336, 60, C['blue'], k, 'c')
    rrect(ctx, 100, 430, 900, 90, 16, fill=C['bg2'], stroke=C['red'], a=seg(p, .6, .8), lw=3)
    text(ctx, 'Divide by a NEGATIVE → FLIP the sign', 130, 488, 36, C['red'], seg(p, .65, .85))

def s_words(ctx, b, p, t):
    chip(ctx, 'Trap words → symbols', C['yel'])
    rows = [('at least', '≥', C['green']), ('at most / no more than', '≤', C['blue']), ('more than', '>', C['green']), ('fewer / less than', '<', C['blue'])]
    for i, (w, s, c) in enumerate(rows):
        k = seg(p, .1 + i * .2, .28 + i * .2)
        text(ctx, w, 200, 210 + i * 90, 38, C['ink'], k); text(ctx, s, 900, 214 + i * 90, 56, c, k, 'c')

def s_drive(ctx, b, p, t):
    chip(ctx, '"At least" includes the number', C['green'])
    if b == 0:
        text(ctx, 'at least 16 = 16 or more', 160, 230, 44, C['green'], seg(p, 0, .4))
        X = nl(ctx, 12, 22, seg(p, .3, .5));
        if X: ray(ctx, X, 16, False, True, C['green'], seg(p, .5, .9), lo=12, hi=22)
        text(ctx, '16 counts ✓', 160, 330, 32, C['green'], seg(p, .7, .9)); return
    rich(ctx, [('a ≥ 16', C['green'])], 160, 230, 56, seg(p, 0, .3))
    X = nl(ctx, 12, 22, 1); ray(ctx, X, 16, False, True, C['green'], 1, lo=12, hi=22)
    rich(ctx, [('a > 16', C['red']), ('  → a 16-year-old can\'t drive?  ✗', C['mute'])], 160, 320, 32, seg(p, .45, .8))

def s_flip(ctx, b, p, t):
    chip(ctx, 'Flip for a negative', C['red'])
    rich(ctx, [('−2x > 8', C['ink'])], 160, 210, 48, 1 if b else seg(p, 0, .2))
    rich(ctx, [('÷ (−2)', C['red']), ('  →  flip  →  ', C['ink']), ('x < −4', C['green'])], 160, 290, 44, 1 if b else seg(p, .3, .8))
    X = nl(ctx, -8, 2, 1 if b else seg(p, .6, .8))
    if X and b == 0: ray(ctx, X, -4, True, False, C['green'], seg(p, .8, 1), lo=-8, hi=2)
    if X and b == 1:
        ray(ctx, X, -4, True, False, C['green'], 1, lo=-8, hi=2)
        trap(ctx, 640, 320, 560, 'Didn\'t flip? Test x = 0.', '−2(0) > 8?  0 > 8 is false ✗', p)

def s_test(ctx, b, p, t):
    chip(ctx, 'Test a point', C['blue'])
    G = Graph(700, 140, 460, 400, (-1, 4), (-1, 8)); G.axes(ctx, seg(p, 0, .2))
    k = seg(p, .1, .4)
    if k > 0:
        ctx.move_to(G.X(-1), G.Y(-1)); ctx.line_to(G.X(3.5), G.Y(8)); ctx.line_to(G.X(-1), G.Y(8)); ctx.close_path(); col(ctx, C['blue'], .15 * k); ctx.fill()
    G.plot(ctx, lambda x: 2 * x + 1, C['blue'], 4, k)
    G.dot(ctx, 1, 4, C['yel'], seg(p, .35, .5), 10); text(ctx, '(1, 4)', G.X(1) + 16, G.Y(4) - 10, 24, C['yel'], seg(p, .35, .5))
    rich(ctx, [('y > 2x + 1', C['blue'])], 80, 220, 40, seg(p, .2, .4))
    rich(ctx, [('2(1) + 1 = 3', C['ink'])], 80, 300, 34, seg(p, .45, .65))
    rich(ctx, [('4 > 3  ✓  yes', C['green'])], 80, 370, 38, seg(p, .7, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'In 12x + 19y ≤ 300, what does 19y mean?', 80, 145, 28, C['ink'], 1 if b else seg(p, 0, .5))
    if b >= 1:
        rich(ctx, [('19', C['org']), (' = cost of ONE y item', C['ink'])], 80, 250, 34, 1 if b > 1 else seg(p, 0, .3))
        rich(ctx, [('y', C['blue']), (' = HOW MANY y items', C['ink'])], 80, 310, 34, 1 if b > 1 else seg(p, .25, .5))
        answer(ctx, '19y = total $ spent on y items', 80, 345, 520, 1 if b > 1 else seg(p, .6, .9))
    if b == 2: trap(ctx, 660, 230, 520, '19y is NOT the number of items.', 'That\'s just y. 19y is money ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    rich(ctx, [('Solve  −3x ≤ 12', C['ink'])], 120, 230, 48, 1 if b else seg(p, 0, .4))
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 340, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('÷ (−3)', C['red']), ('  →  flip  →  ', C['ink']), ('x ≥ −4', C['green'])], 120, 320, 40, seg(p, 0, .5))
    X = nl(ctx, -8, 2, seg(p, .4, .6))
    if X: ray(ctx, X, -4, False, True, C['green'], seg(p, .6, .9), lo=-8, hi=2)

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('at least = ≥', C['green']), ('at most / no more than = ≤', C['blue']), ('÷ by a negative → FLIP', C['red'])])

SC = dict(hook=s_hook, words=s_words, drive=s_drive, flip=s_flip, test=s_test, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'words', 'drive', 'drive', 'flip', 'flip', 'test', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', words='Trap words', drive='"At least"', flip='Flip the sign', test='Test a point', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Inequalities', s_hook, {10: 5.0, 12: 1.5}, CH)
