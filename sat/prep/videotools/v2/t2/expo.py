import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/t2'
NAR = json.load(open(f'{D}/beats.json'))

def bars(ctx, x0, base, vals, c, k, w=60, gap=22, scale=6, labels=True):
    for i, v in enumerate(vals):
        kk_ = seg(k, i / len(vals), (i + 1) / len(vals))
        if kk_ <= 0: continue
        h = v * scale * kk_
        rrect(ctx, x0 + i * (w + gap), base - h, w, h, 6, fill=c, a=.85)
        if labels: text(ctx, str(v), x0 + i * (w + gap) + w / 2, base - h - 12, 24, c, kk_, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Exponents & Growth', 100, 230, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'Linear adds. Exponential multiplies.', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    G = Graph(660, 330, 520, 270, (0, 5), (0, 34)); G.axes(ctx, seg(p, .2, .35), 0)
    G.plot(ctx, lambda x: 2 + 4 * x, C['blue'], 5, seg(p, .3, .6)); G.plot(ctx, lambda x: 2 ** (x + 1), C['org'], 5, seg(p, .45, .8))
    text(ctx, '+ same amount', 110, 420, 34, C['blue'], seg(p, .35, .55)); text(ctx, '× same number', 110, 480, 34, C['org'], seg(p, .5, .7))
    text(ctx, 'linear', G.X(4.6), G.Y(21), 22, C['blue'], seg(p, .55, .7), 'c'); text(ctx, 'exponential', G.X(3.6), G.Y(30), 22, C['org'], seg(p, .75, .9), 'c')

def s_two(ctx, b, p, t):
    chip(ctx, 'Linear vs exponential', C['blue'])
    k0 = 1 if b else seg(p, .1, .9)
    text(ctx, 'LINEAR: save $10 a week', 120, 170, 28, C['blue'], 1 if b else seg(p, 0, .2))
    bars(ctx, 140, 520, [10, 20, 30, 40], C['blue'], k0, 70, 26, 7.5)
    for i in range(3): text(ctx, '+10', 140 + i * 96 + 82, 560, 22, C['blue'], k0, 'c')
    if b >= 1:
        text(ctx, 'EXPONENTIAL: a rumor', 700, 170, 28, C['org'], seg(p, 0, .2))
        bars(ctx, 720, 520, [2, 4, 8, 16], C['org'], seg(p, .1, .9), 70, 26, 18.75)
        for i in range(3): text(ctx, '×2', 720 + i * 96 + 82, 560, 22, C['org'], seg(p, .1, .9), 'c')

def s_form(ctx, b, p, t):
    chip(ctx, 'y = a · bˣ', C['pur'])
    rich(ctx, [('y = ', C['ink']), ('a', C['blue']), (' · ', C['ink']), ('b', C['org']), ('ˣ', C['org'])], 640, 210, 70, 1 if b else seg(p, 0, .2), 'c')
    if b == 0:
        rich(ctx, [('a', C['blue']), (' = start', C['ink'])], 340, 320, 36, seg(p, .2, .4), 'c')
        rich(ctx, [('b', C['org']), (' = multiply by each step', C['ink'])], 860, 320, 36, seg(p, .35, .55), 'c')
        rich(ctx, [('b > 1  →  grows', C['green'])], 340, 430, 36, seg(p, .6, .8), 'c'); rich(ctx, [('b < 1  →  shrinks', C['red'])], 860, 430, 36, seg(p, .75, .95), 'c')
        return
    if b in (1, 2):
        rich(ctx, [('500 · ', C['ink']), ('0.85', C['org']), ('ˣ', C['org'])], 640, 300, 48, 1 if b == 2 else seg(p, 0, .2), 'c')
        # bar showing 85% left
        k = 1 if b == 2 else seg(p, .2, .6)
        rrect(ctx, 290, 360, 700, 60, 10, fill=C['bg2'], stroke=C['mute'], lw=2, a=k)
        rrect(ctx, 290, 360, 700 * .85 * k, 60, 10, fill=C['green'], a=.75 * k)
        text(ctx, '85% left', 290 + 300, 400, 28, C['bg'], k, 'c'); text(ctx, '15% lost', 990 - 52, 400, 22, C['red'], k, 'c')
        rich(ctx, [('decreases ', C['ink']), ('15%', C['red']), (' each step', C['ink'])], 640, 480, 38, 1 if b == 2 else seg(p, .6, .9), 'c')
        if b == 2: trap(ctx, 340, 510, 600, '0.85 = what REMAINS (85%).', 'Loss = 1 − 0.85 = 15% ✗', p)
        return
    rich(ctx, [('300 · 2', C['ink']), ('t/4', C['org'])], 640, 300, 54, seg(p, 0, .2), 'c')
    rich(ctx, [('t/4 = 1  when  ', C['ink']), ('t = 4', C['green'])], 640, 390, 40, seg(p, .25, .55), 'c')
    text(ctx, 'doubles every 4 (not 8)', 640, 470, 38, C['green'], seg(p, .55, .85), 'c')

def s_table(ctx, b, p, t):
    chip(ctx, 'Test a table: divide neighbors', C['green'])
    if b == 0:
        vals = [3, 6, 12, 24]
        for i, v in enumerate(vals):
            rrect(ctx, 260 + i * 200, 220, 140, 90, 14, fill=C['bg2'], stroke=C['ink'], a=seg(p, i * .1, i * .1 + .15), lw=2)
            text(ctx, str(v), 330 + i * 200, 282, 44, C['ink'], seg(p, i * .1, i * .1 + .15), 'c')
            if i: text(ctx, '÷ = 2', 230 + i * 200, 360, 26, C['org'], seg(p, .35 + i * .12, .5 + i * .12), 'c')
        text(ctx, 'same ratio → exponential', 640, 460, 40, C['green'], seg(p, .8, 1), 'c')
        return
    rich(ctx, [('(x³)²', C['ink']), (' = x', C['ink']), ('³ˣ²', C['org']), (' = ', C['ink']), ('x⁶', C['green'])], 640, 300, 64, seg(p, .1, .5), 'c')
    text(ctx, 'power of a power → MULTIPLY exponents', 640, 400, 32, C['org'], seg(p, .5, .8), 'c')
    text(ctx, '(x³ · x³ = x⁶, not x⁵)', 640, 450, 26, C['mute'], seg(p, .7, .95), 'c', False)

def s_sat(ctx, b, p, t):
    question(ctx, 'Which expression is equivalent to  6x² + 9x ?', seg(p, 0, .5) if b == 0 else 1, 28)
    rows = [(1, [('Step 1  ', C['mute']), ('common factor: ', C['ink']), ('3x', C['blue'])]),
            (2, [('Step 2  ', C['mute']), ('6x² ÷ 3x = ', C['ink']), ('2x', C['org']), ('     9x ÷ 3x = ', C['ink']), ('3', C['org'])]),
            (3, [('Step 3  ', C['mute']), ('3x', C['blue']), ('(', C['ink']), ('2x', C['org']), (' + ', C['ink']), ('3', C['org']), (')', C['ink'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 120, 260 + i * 76, 38, kk(b, bb, p, 0, .6))
    if b >= 3:
        answer(ctx, 'Answer: 3x(2x + 3)', 120, 470, 360, kk(b, 3, p, .5, .75))
        text(ctx, 'check: 3x·2x + 3x·3 = 6x² + 9x ✓', 120, 572, 24, C['mute'], kk(b, 3, p, .75, 1), 'l', False)
    if b >= 4: trap(ctx, 640, 440, 520, '3x(2x + 9) → 3x·9 = 27x ✗', 'Divide EVERY term by 3x', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'V = 200 · 1.06ᵗ', 120, 230, 48, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'By what percent does it grow each year?', 120, 290, 30, C['ink'], seg(p, .2, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('1.06 − 1 = 0.06  →  ', C['ink']), ('grows 6%', C['green'])], 120, 380, 38, seg(p, 0, .35))
    trap(ctx, 120, 420, 640, '106% is what you KEEP, not the growth.', 'Growth = b − 1 ✗', seg(p, .55, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Linear adds, exponential multiplies', C['blue']), ('Base b: grow (b > 1) or shrink (b < 1)', C['org']), ('Factor out what EVERY term shares', C['green'])])

SC = dict(hook=s_hook, two=s_two, form=s_form, table=s_table, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['two'] * 2 + ['form'] * 4 + ['table'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: add vs multiply', two='Saving vs a rumor', form='a · bˣ: growth and decay', table='Tables and power rules', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Exponents & Growth', s_hook, {14: 5.0, 16: 1.5}, CH)
