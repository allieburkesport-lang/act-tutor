import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/d1'
NAR = json.load(open(f'{D}/beats.json'))

def nline(ctx, x0, x1, y, lo, hi, k, step=None):
    line(ctx, x0, y, x1, y, C['mute'], 2, k)
    step = step or max(1, (hi - lo) // 10)
    v = lo
    while v <= hi:
        X = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        line(ctx, X, y - 6, X, y + 6, C['mute'], 2, 1, k); text(ctx, str(v), X, y + 30, 18, C['mute'], k, 'c', False); v += step
def pts(ctx, x0, x1, y, lo, hi, vals, c, k, r=12):
    for i, v in enumerate(vals):
        kk_ = seg(k, i / len(vals) * .7, i / len(vals) * .7 + .3)
        if kk_ > 0: disc(ctx, x0 + (v - lo) / (hi - lo) * (x1 - x0), y - 22, r, c, kk_)
def marker(ctx, x0, x1, y, lo, hi, v, lab, c, k, up=True):
    if k <= 0: return
    X = x0 + (v - lo) / (hi - lo) * (x1 - x0)
    line(ctx, X, y - 80, X, y + 2, c, 3, 1, k)
    text(ctx, lab, X, y - 92, 24, c, k, 'c')
def chips(ctx, vals, x, y, k, hi=None, w=110):
    for i, v in enumerate(vals):
        kk_ = seg(k, i * .12, i * .12 + .3)
        if kk_ <= 0: continue
        c = C['yel'] if hi == i else C['blue']
        rrect(ctx, x + i * (w + 16), y, w, 70, 12, fill=C['bg2'], stroke=c, a=kk_, lw=3)
        text(ctx, str(v), x + i * (w + 16) + w / 2, y + 47, 34, c, kk_, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Mean, Median & Spread', 100, 220, 62, C['ink'], seg(p, 0, .12))
    for i, (a, d, c) in enumerate([('Mean', 'the average', C['blue']), ('Median', 'the middle', C['green']), ('Spread', 'how far apart', C['org'])]):
        k = seg(p, .15 + i * .22, .35 + i * .22)
        rrect(ctx, 100 + i * 370, 330, 330, 150, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, a, 265 + i * 370, 395, 40, c, k, 'c'); text(ctx, d, 265 + i * 370, 445, 26, C['ink'], k, 'c', False)

def s_line(ctx, b, p, t):
    chip(ctx, 'Lined up by height', C['blue'])
    H = [120, 150, 160, 175, 230]
    for i, h in enumerate(H):
        k = seg(p, i * .08, i * .08 + .25); x = 260 + i * 170; c = C['green'] if i == 2 else C['blue']
        disc(ctx, x, 560 - h - 22, 20, c, k); rrect(ctx, x - 24, 560 - h, 48, h, 10, fill=c, a=k * .8)
    line(ctx, 200, 560, 1080, 560, C['mute'], 2, seg(p, 0, .2))
    text(ctx, 'median = the middle one', 600, 160, 32, C['green'], seg(p, .6, .8), 'c')
    line(ctx, 600, 175, 600, 360, C['green'], 3, seg(p, .65, .85))

def s_mm(ctx, b, p, t):
    chip(ctx, 'Find the mean and median', C['blue'])
    chips(ctx, [4, 8, 9, 11, 18], 300, 170, 1 if b else seg(p, 0, .4), 2 if b else None)
    if b == 0:
        rich(ctx, [('4 + 8 + 9 + 11 + 18 = 50', C['ink'])], 300, 330, 34, seg(p, .4, .6))
        rich(ctx, [('mean = 50 ÷ 5 = ', C['ink']), ('10', C['blue'])], 300, 400, 40, seg(p, .65, .9)); return
    rich(ctx, [('mean = ', C['ink']), ('10', C['blue'])], 300, 330, 40, 1)
    rich(ctx, [('median = middle = ', C['ink']), ('9', C['green'])], 300, 400, 40, seg(p, .3, .6) if b == 1 else 1)
    if b == 2: trap(ctx, 300, 430, 660, 'Unsorted list? SORT first.', 'Then pick the middle ✗', p)

def s_out(ctx, b, p, t):
    chip(ctx, 'Outlier: add 100', C['red'])
    x0, x1, y = 120, 1160, 470
    nline(ctx, x0, x1, y, 0, 100, 1, 10)
    pts(ctx, x0, x1, y, 0, 100, [4, 8, 9, 11, 18], C['blue'], 1)
    pts(ctx, x0, x1, y, 0, 100, [100], C['red'], seg(p, 0, .2) if b == 0 else 1)
    if b == 0:
        rich(ctx, [('mean: 10  →  150 ÷ 6 = ', C['ink']), ('25', C['blue']), ('   (moved 15)', C['red'])], 120, 220, 34, seg(p, .2, .55))
        marker(ctx, x0, x1, y, 0, 100, 10, '', C['mute'], seg(p, .3, .5)); marker(ctx, x0, x1, y, 0, 100, 25, 'mean 25', C['blue'], seg(p, .55, .85)); return
    rich(ctx, [('mean: 10  →  ', C['ink']), ('25', C['blue']), ('   (moved 15)', C['red'])], 120, 220, 34, 1)
    rich(ctx, [('median: 9  →  (9 + 11) ÷ 2 = ', C['ink']), ('10', C['green']), ('   (moved 1)', C['green'])], 120, 280, 34, seg(p, 0, .35))
    marker(ctx, x0, x1, y, 0, 100, 25, 'mean 25', C['blue'], 1); marker(ctx, x0, x1, y, 0, 100, 10, 'median 10', C['green'], seg(p, .3, .5))
    text(ctx, 'Outliers drag the MEAN', 640, 600, 30, C['yel'], seg(p, .65, .9), 'c')

def s_spread(ctx, b, p, t):
    chip(ctx, 'Spread = distance apart', C['org'])
    x0, x1 = 160, 1120
    if b == 0:
        rich(ctx, [('range = max − min', C['org'])], 160, 190, 34, seg(p, 0, .25))
        rich(ctx, [('SD = typical distance from the mean', C['org'])], 160, 240, 30, seg(p, .2, .45))
        text(ctx, 'small spread', 160, 330, 24, C['green'], seg(p, .55, .7), bold=False)
        nline(ctx, x0, x1, 410, 0, 20, seg(p, .55, .7), 2); pts(ctx, x0, x1, 410, 0, 20, [8.5, 9.5, 10, 10.5, 11.5], C['green'], seg(p, .6, .8))
        text(ctx, 'big spread', 160, 490, 24, C['red'], seg(p, .7, .85), bold=False)
        nline(ctx, x0, x1, 570, 0, 20, seg(p, .7, .85), 2); pts(ctx, x0, x1, 570, 0, 20, [1, 4, 9, 13, 17, 20], C['red'], seg(p, .75, .95)); return
    sh = 5 * seg(p, .15, .5)
    text(ctx, 'add 5 to every value', 160, 190, 34, C['ink'], 1)
    nline(ctx, x0, x1, 400, 0, 30, 1, 5)
    pts(ctx, x0, x1, 400, 0, 30, [v + sh for v in (4, 8, 9, 11, 18)], C['blue'], 1)
    rich(ctx, [('mean + 5,   spread ', C['ink']), ('no change', C['green'])], 160, 520, 36, seg(p, .55, .8))
    text(ctx, 'range: 14 → 14', 160, 570, 26, C['mute'], seg(p, .7, .9), bold=False)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 90, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'The mean of 4 tests is 85. After a 5th test, the mean is 86.', 80, 138, 24, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    write(ctx, 'What was the 5th score?', 80, 172, 24, C['yel'], seg(p, .4, .7) if b == 0 else 1)
    if b >= 1:
        k = 1 if b > 1 else seg(p, 0, .4)
        rich(ctx, [('old total = 4 × 85 = ', C['ink']), ('340', C['blue'])], 80, 270, 34, k)
        rich(ctx, [('new total = 5 × 86 = ', C['ink']), ('430', C['blue'])], 80, 330, 34, 1 if b > 1 else seg(p, .45, .85))
    if b >= 2:
        rich(ctx, [('5th score = 430 − 340 = ', C['ink']), ('90', C['green'])], 80, 400, 38, 1 if b > 2 else seg(p, 0, .5))
        answer(ctx, 'Answer: 90', 80, 430, 260, 1 if b > 2 else seg(p, .5, .9))
    if b >= 3: trap(ctx, 420, 430, 620, '86 is the new MEAN, not the score.', 'Use totals ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'Data: 2, 3, 3, 5, 20', 120, 210, 40, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'Which is bigger: mean or median?', 120, 265, 34, C['yel'], seg(p, .3, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 360, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('mean = 33 ÷ 5 = ', C['ink']), ('6.6', C['blue'])], 120, 350, 34, seg(p, 0, .3))
    rich(ctx, [('median = ', C['ink']), ('3', C['green'])], 120, 405, 34, seg(p, .25, .5))
    rich(ctx, [('The mean. 20 pulls it up.', C['yel'])], 120, 465, 34, seg(p, .55, .85))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Sort first, then find the median', C['green']), ('Outliers move the mean, not the median', C['red']), ('Missing value? Use totals', C['blue'])])

SC = dict(hook=s_hook, line=s_line, mm=s_mm, out=s_out, spread=s_spread, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'line', 'mm', 'mm', 'mm', 'out', 'out', 'spread', 'spread', 'sat', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', line='Mean vs. median', mm='Find mean and median', out='Outliers', spread='Spread', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Statistics', s_hook, {13: 5.0, 15: 1.5}, CH)
