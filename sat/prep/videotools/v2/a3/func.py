import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a3'
NAR = json.load(open(f'{D}/beats.json'))

def machine(ctx, cx, cy, rule, k=1, glow=0):
    if k <= 0: return
    rrect(ctx, cx - 170, cy - 90, 340, 180, 22, fill=C['bg2'], stroke=C['pur'], a=k, lw=4)
    rrect(ctx, cx - 30, cy - 130, 60, 40, 8, fill=C['bg2'], stroke=C['pur'], a=k, lw=3)  # input hopper
    rrect(ctx, cx + 170, cy - 20, 50, 40, 8, fill=C['bg2'], stroke=C['pur'], a=k, lw=3)  # output chute
    for i in range(3):
        disc(ctx, cx - 120 + i * 24, cy + 60, 7, [C['red'], C['yel'], C['green']][i], k * (.4 + .6 * glow))
    text(ctx, 'f', cx - 140, cy - 55, 22, C['pur'], k)
    text(ctx, rule, cx, cy + 12, 34, C['ink'], k, 'c')
def ball(ctx, x, y, s, c, k=1):
    if k <= 0: return
    disc(ctx, x, y, 30, c, k); text(ctx, s, x, y + 10, 28, C['bg'], k, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Functions', 100, 230, 80, C['ink'], seg(p, 0, .12))
    text(ctx, 'A machine: number in, number out.', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    machine(ctx, 760, 420, '× 3, then − 5', seg(p, .2, .4), seg(p, .5, .7))
    ky = seg(p, .3, .5); ball(ctx, 760, lerp(230, 330, ky), '3', C['blue'], seg(p, .25, .35) * (1 - seg(p, .5, .55)))
    kx = seg(p, .6, .85); ball(ctx, lerp(950, 1080, kx), 420, '4', C['green'], seg(p, .6, .65))
    text(ctx, 'in', 760, 215, 22, C['blue'], seg(p, .25, .35), 'c', False); text(ctx, 'out', 1080, 480, 22, C['green'], seg(p, .7, .8), 'c', False)

def s_mach(ctx, b, p, t):
    chip(ctx, 'f(x) = 3x − 5', C['pur'])
    machine(ctx, 560, 380, '× 3, then − 5', 1, seg(p, .4, .6) if b == 1 else 0)
    if b == 0:
        rich(ctx, [('x', C['blue']), (' = what goes in', C['ink'])], 120, 200, 32, seg(p, .2, .45))
        rich(ctx, [('f(x)', C['green']), (' = what comes out', C['ink'])], 760, 200, 32, seg(p, .4, .65))
        text(ctx, 'rule: × 3, then − 5', 560, 560, 30, C['pur'], seg(p, .7, .95), 'c'); return
    ky = seg(p, 0, .3); ball(ctx, 560, lerp(170, 270, ky), '3', C['blue'], 1 - seg(p, .3, .35))
    rich(ctx, [('3 × 3 = 9', C['ink'])], 820, 210, 30, seg(p, .35, .55)); rich(ctx, [('9 − 5 = ', C['ink']), ('4', C['green'])], 820, 260, 30, seg(p, .5, .7))
    kx = seg(p, .65, .85); ball(ctx, lerp(760, 900, kx), 380, '4', C['green'], seg(p, .65, .7))
    rich(ctx, [('f(3) = ', C['ink']), ('4', C['green'])], 560, 560, 44, seg(p, .8, 1), 'c')

def s_io(ctx, b, p, t):
    chip(ctx, 'Input or output?', C['yel'])
    if b == 0:
        text(ctx, 'Are they giving you the', 640, 230, 40, C['ink'], seg(p, 0, .3), 'c')
        rich(ctx, [('INPUT', C['blue']), ('  or the  ', C['ink']), ('OUTPUT', C['green']), ('?', C['ink'])], 640, 320, 60, seg(p, .3, .7), 'c')
        rich(ctx, [('f(3)', C['blue']), (' → put 3 in', C['mute'])], 360, 450, 34, seg(p, .7, .9), 'c')
        rich(ctx, [('f(x) = 7', C['green']), (' → 7 comes out', C['mute'])], 900, 450, 34, seg(p, .75, .95), 'c')
        return
    machine(ctx, 400, 420, '× 3, then − 5', 1)
    ball(ctx, 660, 420, '7', C['green'], 1); text(ctx, '?', 400, 300, 50, C['blue'], 1, 'c')
    rows = [('3x − 5 = 7', C['ink']), ('+5:   3x = 12', C['ink']), ('÷3:   x = 4', C['green'])]
    for i, (s, c) in enumerate(rows): text(ctx, s, 760, 220 + i * 60, 36, c, kk(b, 1, p, .15 + i * .25, .35 + i * .25))
    if b >= 2: trap(ctx, 760, 420, 460, 'f(7) = 16 answers a different', 'question. 7 is the OUTPUT ✗', p)

def s_rearr(ctx, b, p, t):
    chip(ctx, 'Rearranging = unpacking a bag', C['org'])
    if b == 0:
        rrect(ctx, 160, 200, 260, 320, 30, fill=C['bg2'], stroke=C['brown'], a=seg(p, 0, .2), lw=4)
        items = [('÷ / ×', C['blue']), ('+ / −', C['org'])]
        for i, (s, c) in enumerate(items):
            rrect(ctx, 190, 420 - i * 110, 200, 80, 14, fill=c, a=seg(p, .15 + i * .15, .3 + i * .15) * .35)
            text(ctx, s, 290, 470 - i * 110, 32, c, seg(p, .15 + i * .15, .3 + i * .15), 'c')
        text(ctx, 'packed last → comes out first', 290, 570, 22, C['mute'], seg(p, .4, .6), 'c', False)
        text(ctx, '1. undo  + and −', 560, 300, 40, C['org'], seg(p, .55, .75)); text(ctx, '2. undo  × and ÷', 560, 380, 40, C['blue'], seg(p, .7, .9))
        return
    if b == 1:
        text(ctx, 'A = ½bh     Solve for h.', 640, 200, 44, C['ink'], seg(p, 0, .2), 'c')
        rich(ctx, [('× 2:   ', C['mute']), ('2A = bh', C['ink'])], 420, 310, 40, seg(p, .2, .45))
        rich(ctx, [('÷ b:   ', C['mute']), ('h = 2A / b', C['green'])], 420, 390, 44, seg(p, .5, .8))
        text(ctx, 'check with numbers: b = 4, h = 3 → A = 6 → 2(6)/4 = 3 ✓', 640, 480, 24, C['mute'], seg(p, .8, 1), 'c', False)
        return
    text(ctx, 'Shifts: f(x − 3) moves RIGHT 3', 640, 200, 40, C['ink'], seg(p, 0, .2), 'c')
    G = Graph(260, 250, 760, 300, (-5, 7), (-1, 6))
    G.axes(ctx, 1, 1); f = lambda x: 4 - (x * .8) ** 2 / 2
    G.plot(ctx, f, C['blue'], 4, 1); G.plot(ctx, lambda x: f(x - 3), C['green'], 4, seg(p, .2, .6))
    text(ctx, 'f(x)', G.X(-1.5), G.Y(3.5), 26, C['blue'], 1); text(ctx, 'f(x − 3)', G.X(4.6), G.Y(4.4), 26, C['green'], seg(p, .4, .6))
    line(ctx, G.X(0), G.Y(4.3), G.X(3), G.Y(4.3), C['yel'], 4, seg(p, .55, .8)); text(ctx, '3 right →', G.X(1.5), G.Y(4.3) - 14, 24, C['yel'], seg(p, .6, .85), 'c')

def s_sat(ctx, b, p, t):
    question(ctx, 'g(x) = ax + 2 and g(5) = 37. What is the value of a?', seg(p, 0, .5) if b == 0 else 1, 28)
    rows = [(1, [('Step 1  ', C['mute']), ('x = 5:   ', C['ink']), ('5a + 2 = 37', C['blue'])]),
            (2, [('Step 2  ', C['mute']), ('− 2:   ', C['ink']), ('5a = 35', C['org'])]),
            (3, [('Step 3  ', C['mute']), ('÷ 5:   ', C['ink']), ('a = 7', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 120, 260 + i * 76, 40, kk(b, bb, p, 0, .6))
    if b >= 3: answer(ctx, 'Answer: a = 7', 120, 480, 300, kk(b, 3, p, .6, .85))
    if b >= 4: trap(ctx, 640, 330, 520, '35 is 5a, not a.', 'Finish: divide by 5 ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'f(x) = 2x² − 19.   What is f(−4)?', 120, 230, 42, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 330, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('(−4)² = ', C['ink']), ('+16', C['green'])], 120, 320, 38, seg(p, 0, .25))
    rich(ctx, [('2(16) − 19 = 32 − 19 = ', C['ink']), ('13', C['green'])], 120, 385, 38, seg(p, .2, .45))
    trap(ctx, 120, 425, 620, 'Got −13? A negative squared is POSITIVE.', '(−4)² = +16 ✗', seg(p, .55, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('A function is a machine: in → rule → out', C['pur']), ('Ask: input or output?', C['yel']), ('Undo + and − first, then × and ÷', C['org'])])

SC = dict(hook=s_hook, mach=s_mach, io=s_io, rearr=s_rearr, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['mach'] * 2 + ['io'] * 3 + ['rearr'] * 3 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: a machine', mach='f(3): put 3 in', io='Input or output?', rearr='Rearranging and shifts', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Functions', s_hook, {14: 5.0, 16: 1.5}, CH)
