import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/d3'
NAR = json.load(open(f'{D}/beats.json'))
PTS = [(1, 45), (1.5, 41), (2, 47), (3, 46), (3.5, 51), (4, 48), (5, 54), (6, 60), (6.5, 53), (7, 59), (8, 58), (8.5, 64), (9, 61)]
f = lambda x: 2.5 * x + 40

def plot(ctx, k_pts=1, k_line=1, x0=640, y0=130, w=560, h=420, hi=None):
    G = Graph(x0, y0, w, h, (0, 10), (30, 70)); G.axes(ctx, 1)
    text(ctx, 'hours', x0 + w - 60, y0 + h + 34, 20, C['mute'], 1, 'l', False); text(ctx, 'score', x0 - 8, y0 - 12, 20, C['mute'], 1, 'l', False)
    for i, (x, y) in enumerate(PTS):
        kk_ = seg(k_pts, i / len(PTS) * .7, i / len(PTS) * .7 + .3)
        if kk_ > 0: G.dot(ctx, x, y, C['blue'], kk_, 7)
    G.plot(ctx, f, C['yel'], 4, k_line)
    return G

def s_hook(ctx, b, p, t):
    text(ctx, 'Scatterplots', 80, 220, 62, C['ink'], seg(p, 0, .12))
    text(ctx, '& Residuals', 80, 290, 48, C['mute'], seg(p, .05, .2))
    text(ctx, 'What do the numbers mean?', 82, 360, 28, C['yel'], seg(p, .6, .85), bold=False)
    plot(ctx, seg(p, .1, .5), seg(p, .45, .75))

def s_model(ctx, b, p, t):
    chip(ctx, 'The model', C['yel'])
    plot(ctx)
    k1 = 1 if b else seg(p, 0, .4)
    rich(ctx, [('y = ', C['ink']), ('2.5', C['org']), ('x + ', C['ink']), ('40', C['green'])], 80, 220, 52, k1)
    text(ctx, 'x = hours,  y = score', 80, 280, 26, C['mute'], 1 if b else seg(p, .5, .8), bold=False)
    if b == 1:
        rich(ctx, [('slope 2.5', C['org'])], 80, 360, 36, seg(p, 0, .2))
        write(ctx, '+2.5 points per', 80, 410, 28, C['ink'], seg(p, .45, .7)); write(ctx, '1 more hour', 80, 448, 28, C['ink'], seg(p, .5, .75))
    if b == 2:
        rich(ctx, [('intercept 40', C['green'])], 80, 360, 36, seg(p, 0, .2))
        write(ctx, 'score at 0 hours', 80, 410, 28, C['ink'], seg(p, .35, .6))
        G = Graph(640, 130, 560, 420, (0, 10), (30, 70)); G.dot(ctx, 0, 40, C['green'], seg(p, .3, .5), 11)
    if b == 3:
        rich(ctx, [('slope', C['org']), (' = rate', C['ink'])], 80, 360, 34, 1)
        rich(ctx, [('intercept', C['green']), (' = start (x = 0)', C['ink'])], 80, 410, 34, 1)
        trap(ctx, 80, 440, 500, 'Don\'t swap them.', 'Rate ≠ starting value ✗', p)
    if b == 1:
        G = Graph(640, 130, 560, 420, (0, 10), (30, 70)); k = seg(p, .3, .6)
        line(ctx, G.X(4), G.Y(f(4)), G.X(5), G.Y(f(4)), C['org'], 3, k); line(ctx, G.X(5), G.Y(f(4)), G.X(5), G.Y(f(5)), C['org'], 3, k)
        text(ctx, '1', G.X(4.5), G.Y(f(4)) + 26, 20, C['org'], k, 'c'); text(ctx, '2.5', G.X(5) + 10, G.Y(f(4.5)) + 6, 20, C['org'], k)

def s_pred(ctx, b, p, t):
    chip(ctx, 'Predict', C['blue'])
    G = plot(ctx)
    rich(ctx, [('x = 6', C['ink'])], 80, 210, 36, 1 if b else seg(p, 0, .2))
    rich(ctx, [('2.5 × 6 = 15', C['ink'])], 80, 270, 36, 1 if b else seg(p, .25, .5))
    rich(ctx, [('15 + 40 = ', C['ink']), ('55', C['green'])], 80, 330, 40, 1 if b else seg(p, .55, .8))
    k = 1 if b else seg(p, .55, .85)
    line(ctx, G.X(6), G.Y(30), G.X(6), G.Y(55), C['green'], 2, k, dash=[6, 6]); G.dot(ctx, 6, 55, C['green'], k, 10)
    if b: trap(ctx, 80, 380, 480, 'Said 15? Forgot the intercept.', 'Always add b ✗', p)

def s_resid(ctx, b, p, t):
    chip(ctx, 'Residual = actual − predicted', C['org'])
    G = plot(ctx)
    if b == 0:
        for (x, y) in PTS:
            c = C['green'] if y > f(x) else C['red']
            line(ctx, G.X(x), G.Y(y), G.X(x), G.Y(f(x)), c, 2, seg(p, .3, .6))
        text(ctx, 'above line → +', 80, 260, 34, C['green'], seg(p, .35, .55)); text(ctx, 'below line → −', 80, 320, 34, C['red'], seg(p, .6, .8)); return
    G.dot(ctx, 6, 55, C['mute'], 1, 9); G.dot(ctx, 6, 60, C['green'], 1, 10)
    line(ctx, G.X(6), G.Y(60), G.X(6), G.Y(55), C['green'], 4, 1)
    rich(ctx, [('actual 60', C['ink'])], 80, 220, 34, 1); rich(ctx, [('predicted 55', C['ink'])], 80, 270, 34, 1)
    rich(ctx, [('60 − 55 = ', C['ink']), ('+5', C['green'])], 80, 340, 42, seg(p, .3, .6) if b == 1 else 1)
    if b == 2: trap(ctx, 80, 380, 480, '55 − 60 = −5 is backwards.', 'Actual − predicted ✗', p)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 90, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'Compare y = 3ˣ and y = 4x + 1 for x > 0.', 80, 138, 24, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    write(ctx, 'Is the exponential always greater?', 80, 172, 24, C['yel'], seg(p, .4, .7) if b == 0 else 1)
    G = Graph(700, 230, 480, 330, (0, 3.6), (0, 30)); G.axes(ctx, seg(p, .3, .6) if b == 0 else 1)
    G.plot(ctx, lambda x: 4 * x + 1, C['blue'], 4, seg(p, .4, .8) if b == 0 else 1)
    G.plot(ctx, lambda x: 3 ** x, C['org'], 4, seg(p, .5, .9) if b == 0 else 1)
    text(ctx, '4x + 1', G.X(3.0), G.Y(16), 22, C['blue'], 1 if b else seg(p, .7, .9)); text(ctx, '3ˣ', G.X(2.8), G.Y(28), 24, C['org'], 1 if b else seg(p, .8, 1))
    if b >= 1:
        rich(ctx, [('x = 1:  3  vs  ', C['ink']), ('5', C['blue']), ('   linear wins', C['mute'])], 80, 290, 30, 1 if b > 1 else seg(p, 0, .5))
        G.dot(ctx, 1, 3, C['org'], 1 if b > 1 else seg(p, .3, .6)); G.dot(ctx, 1, 5, C['blue'], 1 if b > 1 else seg(p, .3, .6))
    if b >= 2:
        rich(ctx, [('x = 3:  ', C['ink']), ('27', C['org']), ('  vs  13', C['ink'])], 80, 350, 30, seg(p, 0, .4))
        answer(ctx, 'Eventually passes, NOT always', 80, 400, 470, seg(p, .55, .9))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'Model: y = 3x + 10', 120, 210, 40, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'Find y at x = 4. What does the 3 mean?', 120, 265, 32, C['yel'], seg(p, .3, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 360, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('3 × 4 + 10 = ', C['ink']), ('22', C['green'])], 120, 350, 38, seg(p, 0, .3))
    rich(ctx, [('3', C['org']), (' = y goes up 3 for each 1 more x', C['ink'])], 120, 415, 32, seg(p, .4, .7))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Slope: change in y per 1 more x', C['org']), ('Intercept: y when x = 0', C['green']), ('Residual = actual − predicted', C['blue'])])

SC = dict(hook=s_hook, model=s_model, pred=s_pred, resid=s_resid, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['model'] * 4 + ['pred'] * 2 + ['resid'] * 3 + ['sat'] * 3 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea', model='Slope and intercept', pred='Predict', resid='Residuals', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Scatterplots', s_hook, {13: 5.0, 15: 1.5}, CH)
