import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/t1'
NAR = json.load(open(f'{D}/beats.json'))

def s_hook(ctx, b, p, t):
    text(ctx, 'Lines', 100, 230, 84, C['ink'], seg(p, 0, .12))
    text(ctx, 'Slope = how steep.  Intercept = where it crosses.', 102, 290, 28, C['mute'], seg(p, .1, .3), bold=False)
    G = Graph(660, 300, 520, 300, (-3, 6), (-2, 8)); G.axes(ctx, seg(p, .2, .35))
    G.plot(ctx, lambda x: 1.2 * x + 2, C['blue'], 5, seg(p, .3, .6))
    G.dot(ctx, 0, 2, C['yel'], seg(p, .6, .75))
    text(ctx, 'intercept', G.X(0) + 14, G.Y(2) + 32, 22, C['yel'], seg(p, .65, .8))
    line(ctx, G.X(2), G.Y(4.4), G.X(4), G.Y(4.4), C['org'], 3, seg(p, .7, .8)); line(ctx, G.X(4), G.Y(4.4), G.X(4), G.Y(6.8), C['green'], 3, seg(p, .78, .88))
    text(ctx, 'slope', G.X(4) + 14, G.Y(5.6), 22, C['green'], seg(p, .82, .95))

def s_slope(ctx, b, p, t):
    chip(ctx, 'Slope = rise ÷ run', C['green'])
    G = Graph(120, 130, 520, 440, (0, 5), (0, 13)); G.axes(ctx, 1)
    G.plot(ctx, lambda x: 3 * x + 2, C['blue'], 4, seg(p, 0, .3) if b == 0 else 1)
    # stairs
    k = seg(p, .25, .55) if b == 0 else 1
    G.dot(ctx, 1, 5, C['ink'], k); G.dot(ctx, 3, 11, C['ink'], k)
    text(ctx, '(1, 5)', G.X(1) + 14, G.Y(5) + 26, 22, C['ink'], k); text(ctx, '(3, 11)', G.X(3) - 14, G.Y(11) - 12, 22, C['ink'], k, 'r')
    k2 = seg(p, .45, .7) if b == 0 else 1
    line(ctx, G.X(1), G.Y(5), G.X(3), G.Y(5), C['org'], 5, k2); text(ctx, 'run 2', G.X(2), G.Y(5) + 34, 26, C['org'], k2, 'c')
    line(ctx, G.X(3), G.Y(5), G.X(3), G.Y(11), C['green'], 5, seg(p, .55, .8) if b == 0 else 1); text(ctx, 'rise 6', G.X(3) + 14, G.Y(8), 26, C['green'], seg(p, .6, .85) if b == 0 else 1)
    rich(ctx, [('slope = ', C['ink']), ('rise', C['green']), (' ÷ ', C['ink']), ('run', C['org'])], 720, 250, 40, seg(p, .1, .3) if b == 0 else 1)
    rich(ctx, [('6', C['green']), (' ÷ ', C['ink']), ('2', C['org']), (' = ', C['ink']), ('3', C['blue'])], 720, 330, 50, seg(p, .75, .95) if b == 0 else 1)
    if b == 1: trap(ctx, 720, 400, 460, '2 is only the run.', 'Slope = rise ÷ run ✗', p)

def s_forms(ctx, b, p, t):
    chip(ctx, 'Reading a line\'s equation', C['blue'])
    if b == 0:
        rich(ctx, [('y = ', C['ink']), ('m', C['green']), ('x + ', C['ink']), ('b', C['yel'])], 640, 230, 70, seg(p, 0, .25), 'c')
        rich(ctx, [('m', C['green']), (' = slope', C['ink'])], 400, 340, 36, seg(p, .25, .5), 'c')
        rich(ctx, [('b', C['yel']), (' = y-intercept (start)', C['ink'])], 860, 340, 36, seg(p, .45, .7), 'c')
        G = Graph(440, 380, 400, 200, (-2, 5), (-1, 6)); G.axes(ctx, seg(p, .6, .7), 0); G.plot(ctx, lambda x: x + 2, C['blue'], 4, seg(p, .65, .9)); G.dot(ctx, 0, 2, C['yel'], seg(p, .85, 1))
        return
    if b == 1:
        text(ctx, '3x + 4y = 12', 640, 200, 50, C['ink'], seg(p, 0, .15), 'c')
        rows = [('4y = −3x + 12', C['ink']), ('y = −¾x + 3', C['ink'])]
        for i, (s, c) in enumerate(rows): text(ctx, s, 640, 290 + i * 70, 44, c, seg(p, .2 + i * .25, .4 + i * .25), 'c')
        rich(ctx, [('slope = ', C['ink']), ('−¾', C['green'])], 640, 450, 50, seg(p, .75, .95), 'c')
        return
    text(ctx, 'x-intercept: set y = 0', 640, 200, 44, C['yel'], seg(p, 0, .2), 'c')
    rows = ['0 = 7x + 14', '−14 = 7x', 'x = −2']
    for i, s in enumerate(rows): text(ctx, s, 640, 290 + i * 66, 44, C['green'] if i == 2 else C['ink'], seg(p, .2 + i * .22, .4 + i * .22), 'c')

def s_perp(ctx, b, p, t):
    chip(ctx, 'Perpendicular: flip and switch', C['pur'])
    G = Graph(140, 140, 440, 440, (-5, 5), (-5, 5)); G.axes(ctx, 1)
    G.plot(ctx, lambda x: 2 / 3 * x, C['blue'], 4, seg(p, 0, .3)); G.plot(ctx, lambda x: -1.5 * x, C['org'], 4, seg(p, .5, .8))
    rrect(ctx, G.X(0) - 0, G.Y(0) - 0, 0, 0, 0)
    rich(ctx, [('2/3', C['blue'])], 760, 270, 54, seg(p, .1, .3))
    text(ctx, 'flip →  3/2', 760, 350, 40, C['ink'], seg(p, .35, .55))
    rich(ctx, [('switch →  ', C['ink']), ('−3/2', C['org'])], 760, 420, 40, seg(p, .55, .75))
    text(ctx, 'meet at 90°', 760, 500, 30, C['green'], seg(p, .8, 1))

def s_sol(ctx, b, p, t):
    chip(ctx, 'How many solutions?', C['org'])
    if b == 0:
        G = Graph(390, 150, 500, 420, (-5, 5), (-5, 5)); G.axes(ctx, seg(p, .1, .4))
        G.plot(ctx, lambda x: x + 1, C['blue'], 4, seg(p, .3, .7)); G.plot(ctx, lambda x: -0.5 * x + 2, C['org'], 4, seg(p, .5, .9)); return
    cases = [('ONE', 'they cross', lambda x: x, lambda x: -x + 1, C['green']),
             ('NONE', 'parallel: same slope,\ndifferent intercept', lambda x: x + 1.5, lambda x: x - 1.5, C['red']),
             ('INFINITE', 'same line', lambda x: .7 * x, lambda x: .7 * x, C['yel'])]
    for i, (big, small, f1, f2, c) in enumerate(cases):
        k = seg(p, .05 + i * .3, .3 + i * .3)
        G = Graph(110 + i * 380, 160, 300, 260, (-4, 4), (-4, 4)); G.axes(ctx, k, 0)
        G.plot(ctx, f1, C['blue'], 4, k); G.plot(ctx, f2, C['org'] if i < 2 else C['yel'], 4 if i < 2 else 8, k, ) if i < 2 else G.plot(ctx, f2, C['yel'], 3, k)
        text(ctx, big, 260 + i * 380, 480, 40, c, k, 'c')
        for j, s in enumerate(small.split('\n')): text(ctx, s, 260 + i * 380, 520 + j * 30, 22, C['mute'], k, 'c', False)

def s_sat(ctx, b, p, t):
    question(ctx, 'A line has slope −4. What is the slope of a line perpendicular to it?', seg(p, 0, .5) if b == 0 else 1, 26)
    rows = [(1, [('Step 1  ', C['mute']), ('−4 = ', C['ink']), ('−4/1', C['blue'])]),
            (2, [('Step 2  ', C['mute']), ('flip: ', C['ink']), ('−1/4', C['pur'])]),
            (3, [('Step 3  ', C['mute']), ('switch: ', C['ink']), ('+1/4', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 120, 260 + i * 76, 40, kk(b, bb, p, 0, .6))
    if b >= 3:
        answer(ctx, 'Answer: 1/4', 120, 470, 260, kk(b, 3, p, .45, .7))
        text(ctx, 'check: −4 × ¼ = −1 ✓', 420, 512, 26, C['mute'], kk(b, 3, p, .7, .95), 'l', False)
    if b >= 4: trap(ctx, 700, 250, 500, '4 only switched the sign:', '−4 × 4 = −16, not −1 ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, '3(x + 2) = 3x + 6', 120, 230, 48, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'How many solutions?', 120, 290, 32, C['ink'], seg(p, .2, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('3x + 6 = 3x + 6', C['ink']), ('  → identical', C['mute'])], 120, 370, 36, seg(p, 0, .3))
    rich(ctx, [('infinitely many', C['green'])], 120, 430, 40, seg(p, .25, .5))
    trap(ctx, 120, 460, 560, 'Said "one"? Try x = 0 and x = 5.', 'Both work ✗', seg(p, .55, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Slope = rise ÷ run', C['green']), ('Perpendicular: flip and switch', C['pur']), ('Same slope, new intercept → no solution', C['red'])])

SC = dict(hook=s_hook, slope=s_slope, forms=s_forms, perp=s_perp, sol=s_sol, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['slope'] * 2 + ['forms'] * 3 + ['perp'] + ['sol'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: slope and intercept', slope='Slope: rise over run', forms='Reading equations and intercepts', perp='Perpendicular: flip and switch', sol='How many solutions', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Lines', s_hook, {14: 5.0, 16: 1.5}, CH)
