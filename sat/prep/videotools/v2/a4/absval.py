import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a4'
NAR = json.load(open(f'{D}/beats.json'))

def nl(ctx, lo, hi, k, y=430, x0=140, x1=1140):
    if k <= 0: return None
    line(ctx, x0, y, x1, y, C['mute'], 3, k)
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    for v in range(lo, hi + 1):
        line(ctx, X(v), y - 8, X(v), y + 8, C['mute'], 2, 1, k); text(ctx, str(v).replace('-', '−'), X(v), y + 36, 20, C['mute'], k, 'c', False)
    return X
def hop(ctx, X, a, b, y, c, k, lab=None, up=60):
    if k <= 0: return
    xa, xb = X(a), X(b); mx = (xa + xb) / 2; r = abs(xb - xa) / 2
    ctx.save(); ctx.translate(mx, y); ctx.scale(1, up / max(r, 1))
    arc(ctx, 0, 0, r, math.pi, math.pi + math.pi * k if xb > xa else math.pi, c, 4, 1) if xb > xa else arc(ctx, 0, 0, r, 2 * math.pi - math.pi * k, 2 * math.pi, c, 4, 1)
    ctx.restore()
    if lab and k > .9: text(ctx, lab, mx, y - up - 12, 24, c, 1, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Absolute Value', 100, 200, 66, C['ink'], seg(p, 0, .12))
    text(ctx, '|x| = distance from 0', 102, 260, 32, C['mute'], seg(p, .1, .3), bold=False)
    X = nl(ctx, -6, 6, seg(p, .2, .4))
    if X:
        disc(ctx, X(0), 430, 10, C['yel'], seg(p, .3, .45))
        hop(ctx, X, 0, 5, 430, C['green'], seg(p, .4, .65), '|5| = 5'); hop(ctx, X, -5, 0, 430, C['blue'], seg(p, .6, .85), '|−5| = 5')
        disc(ctx, X(5), 430, 10, C['green'], seg(p, .6, .7)); disc(ctx, X(-5), 430, 10, C['blue'], seg(p, .8, .9))

def s_home(ctx, b, p, t):
    chip(ctx, 'Distance from home', C['blue'])
    X = nl(ctx, -6, 6, 1)
    k = seg(p, 0, .2)
    rrect(ctx, X(0) - 30, 330, 60, 50, 6, fill=C['yel'], a=k); ctx.move_to(X(0) - 40, 335); ctx.line_to(X(0), 295); ctx.line_to(X(0) + 40, 335); ctx.close_path(); col(ctx, C['yel'], k); ctx.fill()
    hop(ctx, X, 0, 5, 430, C['green'], seg(p, .25, .5), '5 blocks east'); hop(ctx, X, -5, 0, 430, C['green'], seg(p, .5, .75), '5 blocks west')
    text(ctx, 'either way: 5 from home', 640, 570, 32, C['yel'], seg(p, .75, .95), 'c')

def s_rule(ctx, b, p, t):
    chip(ctx, '|x − a| = b', C['yel'])
    rich(ctx, [('|x − ', C['ink']), ('a', C['yel']), ('| = ', C['ink']), ('b', C['green'])], 160, 240, 60, seg(p, 0, .3))
    rich(ctx, [('x is ', C['ink']), ('b', C['green']), (' away from ', C['ink']), ('a', C['yel']), (', either direction', C['ink'])], 160, 330, 36, seg(p, .3, .6))
    text(ctx, '→ ALWAYS write two equations', 160, 430, 36, C['yel'], seg(p, .65, .9))

def s_ex(ctx, b, p, t):
    chip(ctx, 'Two answers', C['green'])
    rich(ctx, [('|x − 3| = 5', C['ink'])], 120, 190, 48, 1)
    X = nl(ctx, -4, 10, 1, 470)
    disc(ctx, X(3), 470, 10, C['yel'], 1); text(ctx, 'home = 3', X(3), 520, 20, C['yel'], 1, 'c')
    k = 1 if b else seg(p, .2, .7)
    hop(ctx, X, 3, 8, 470, C['green'], k, '+5'); hop(ctx, X, -2, 3, 470, C['blue'], k, '−5')
    disc(ctx, X(8), 470, 11, C['green'], k); disc(ctx, X(-2), 470, 11, C['blue'], k)
    if b >= 1:
        rich(ctx, [('x − 3 = 5  →  ', C['ink']), ('x = 8', C['green'])], 640, 180, 32, 1 if b > 1 else seg(p, .1, .4))
        rich(ctx, [('x − 3 = −5  →  ', C['ink']), ('x = −2', C['blue'])], 640, 240, 32, 1 if b > 1 else seg(p, .45, .8))
    if b == 2: trap(ctx, 120, 260, 480, 'Said "8" only? Missed a side.', '|−2 − 3| = 5 ✓ too ✗', p)

def s_special(ctx, b, p, t):
    chip(ctx, 'Special cases', C['org'])
    rich(ctx, [('|x + 4| = −2', C['ink'])], 140, 230, 48, 1 if b else seg(p, 0, .3))
    text(ctx, 'distance can\'t be negative → NO solution', 140, 300, 32, C['red'], 1 if b else seg(p, .4, .8))
    if b:
        rich(ctx, [('|x − 5| = 0', C['ink'])], 140, 420, 48, seg(p, 0, .3))
        text(ctx, 'zero has no other side → x = 5 only', 140, 490, 32, C['green'], seg(p, .35, .75))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'A temperature t stays within 2 degrees of 70. Which inequality?', 80, 145, 26, C['ink'], 1 if b else seg(p, 0, .5))
    X = nl(ctx, 64, 76, 1 if b else seg(p, .5, .8), 470)
    if X and b >= 1:
        k = 1 if b > 1 else seg(p, .4, .8)
        line(ctx, X(68), 470, X(72), 470, C['green'], 10, k); disc(ctx, X(68), 470, 10, C['green'], k); disc(ctx, X(72), 470, 10, C['green'], k)
        disc(ctx, X(70), 470, 8, C['yel'], k)
        rich(ctx, [('distance from 70: ', C['ink']), ('|t − 70|', C['yel'])], 80, 230, 32, 1 if b > 1 else seg(p, 0, .3))
        rich(ctx, [('within 2 = at most 2:  ', C['ink']), ('|t − 70| ≤ 2', C['green'])], 80, 290, 34, 1 if b > 1 else seg(p, .3, .6))
    if b == 2: trap(ctx, 640, 210, 560, '≥ 2 means AT LEAST 2 away.', '80 would fit. Not "within" ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    rich(ctx, [('Solve  |x + 1| = 4', C['ink'])], 120, 230, 48, 1 if b else seg(p, 0, .4))
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 340, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('x + 1 = 4  →  ', C['ink']), ('x = 3', C['green'])], 120, 320, 34, seg(p, 0, .3))
    rich(ctx, [('x + 1 = −4  →  ', C['ink']), ('x = −5', C['blue'])], 120, 380, 34, seg(p, .3, .6))
    answer(ctx, 'x = 3 or x = −5', 120, 410, 340, seg(p, .65, .9))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Absolute value = distance', C['yel']), ('Two equations, one per side', C['green']), ('= negative → no solution', C['red'])])

SC = dict(hook=s_hook, home=s_home, rule=s_rule, ex=s_ex, special=s_special, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'home', 'rule', 'ex', 'ex', 'ex', 'special', 'special', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', home='Distance from home', rule='Two equations', ex='Two answers', special='Special cases', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Absolute value', s_hook, {11: 5.0, 13: 1.5}, CH)
