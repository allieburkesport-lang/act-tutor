import sys, random; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/d2'
NAR = json.load(open(f'{D}/beats.json'))

def bag(ctx, cx, cy, counts, k=1, hl=None, dim=None, seed=3, R=170):
    """draw a bag with marbles; counts = [(n, color, name)]"""
    if k <= 0: return
    col(ctx, C['brown'], k * .35); ctx.new_sub_path(); ctx.arc(cx, cy, R, 0, 2 * PI); ctx.fill()
    arc(ctx, cx, cy, R, 0, 2 * PI, C['brown'], 4, k)
    rnd = random.Random(seed); pts = []
    while len(pts) < sum(n for n, _, _ in counts):
        x, y = rnd.uniform(-R + 22, R - 22), rnd.uniform(-R + 22, R - 22)
        if x * x + y * y < (R - 24) ** 2 and all((x - a) ** 2 + (y - b) ** 2 > 30 ** 2 for a, b in pts): pts.append((x, y))
    i = 0
    for n, c, name in counts:
        for _ in range(n):
            a = 1 if (hl is None or name == hl) else .25
            if dim and name in dim: a = .25
            disc(ctx, cx + pts[i][0], cy + pts[i][1], 13, c, k * a); i += 1
def frac(ctx, top, bot, x, y, size, ct, cb, k=1):
    w = max(twidth(ctx, top, size), twidth(ctx, bot, size)) + 16
    text(ctx, top, x, y - 12, size, ct, k, 'c'); line(ctx, x - w / 2, y, x + w / 2, y, C['ink'], 3, k); text(ctx, bot, x, y + size + 4, size, cb, k, 'c')

M1 = [(4, C['red'], 'red'), (6, C['blue'], 'blue'), (10, C['green'], 'green')]
def s_hook(ctx, b, p, t):
    text(ctx, 'Probability', 100, 230, 80, C['ink'], seg(p, 0, .12))
    text(ctx, 'Part on top. Total on the bottom.', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    frac(ctx, 'what you want', 'the total', 330, 450, 44, C['green'], C['yel'], seg(p, .35, .6))
    text(ctx, 'Pick the right total.', 110, 590, 34, C['yel'], seg(p, .75, .95))
    bag(ctx, 920, 380, M1, seg(p, .2, .45))

def s_bag(ctx, b, p, t):
    chip(ctx, 'Simple probability', C['blue'])
    bag(ctx, 330, 370, M1, 1, hl='blue' if b >= 2 else None)
    for i, (n, c, name) in enumerate(M1):
        text(ctx, f'{n} {name}', 580, 220 + i * 50, 34, c, seg(p, i * .15, .15 + i * .15) if b == 0 else 1)
    if b == 0:
        text(ctx, 'P(blue) = ?', 580, 420, 44, C['ink'], seg(p, .6, .85)); return
    if b >= 1:
        rich(ctx, [('total: 4 + 6 + 10 = ', C['ink']), ('20', C['yel'])], 580, 410, 34, kk(b, 1, p, 0, .6))
    if b >= 2:
        frac(ctx, '6', '20', 660, 520, 44, C['blue'], C['yel'], kk(b, 2, p, 0, .4))
        rich(ctx, [('= ', C['ink']), ('3/10', C['green'])], 720, 538, 44, kk(b, 2, p, .5, .8))
    if b >= 3: trap(ctx, 830, 240, 400, '6/14 left blue out of the total.', 'Bottom = EVERY marble ✗', p)

T = [['', 'Play', "Don't play", 'Total'], ['Grade 10', '30', '20', '50'], ['Grade 11', '15', '35', '50'], ['Total', '45', '55', '100']]
def table(ctx, x, y, k=1, spot=None, hlcell=None, cw=(170, 130, 160, 120), rh=62):
    if k <= 0: return
    xs = [x]; [xs.append(xs[-1] + w) for w in cw]
    for r in range(4):
        for c in range(4):
            cx = xs[c]; cy = y + r * rh
            dim = spot is not None and c != spot and r > 0 and c > 0
            rrect(ctx, cx + 2, cy + 2, cw[c] - 4, rh - 4, 8, fill=C['bg2'], a=k * (.4 if dim else 1))
            colr = C['mute'] if (r == 0 or c == 0) else C['ink']
            if hlcell == (r, c): colr = C['green']
            text(ctx, T[r][c], cx + cw[c] / 2, cy + rh / 2 + 10, 26, colr, k * (.35 if dim else 1), 'c', r > 0 and c > 0)
    if spot is not None:
        rrect(ctx, xs[spot] - 2, y + rh - 2, cw[spot] + 4, rh * 3 + 4, 10, stroke=C['yel'], lw=4, a=k)
    return xs
def s_table(ctx, b, p, t):
    chip(ctx, 'Two-way tables', C['org'])
    if b == 0:
        table(ctx, 330, 170, seg(p, .1, .5)); return
    if b == 1:
        table(ctx, 330, 170, 1, spot=2 if p > .45 else None)
        text(ctx, '"given that"   "of those who"   "among"', 640, 500, 30, C['yel'], seg(p, 0, .35), 'c')
        text(ctx, '= zoom in on ONE row or column', 640, 550, 32, C['ink'], seg(p, .35, .6), 'c')
        return
    text(ctx, 'Expected number = probability × how many', 640, 230, 36, C['ink'], seg(p, 0, .3), 'c')
    rich(ctx, [('1/50', C['blue']), (' = 0.02     ', C['mute']), ('0.02 × 1,500 = ', C['ink']), ('30', C['green'])], 640, 330, 40, seg(p, .35, .8), 'c')
    text(ctx, 'about 30 broken parts', 640, 420, 30, C['green'], seg(p, .8, 1), 'c', False)

def s_sat(ctx, b, p, t):
    question(ctx, "Given that a student doesn't play a sport, what is the probability the student is in grade 10?", seg(p, 0, .5) if b == 0 else 1, 23)
    spot = 2 if b >= 1 else None
    xs = table(ctx, 60, 200, 1 if b else seg(p, .4, .8), spot=spot, hlcell=(1, 2) if b >= 3 else None, cw=(150, 110, 140, 100), rh=58)
    if b >= 1: text(ctx, 'given that → this column', 300, 470, 22, C['yel'], kk(b, 1, p, .3, .6), 'c', False)
    rows = [(1, [('Step 1  ', C['mute']), ("circle \"given that\" → Don't play", C['ink'])]),
            (2, [('Step 2  ', C['mute']), ('new total = 20 + 35 = ', C['ink']), ('55', C['yel'])]),
            (3, [('Step 3  ', C['mute']), ('20 / 55 = ', C['ink']), ('4/11', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 600, 250 + i * 66, 28, kk(b, bb, p, 0, .6))
    if b >= 3: answer(ctx, 'Answer: 4/11', 600, 440, 260, kk(b, 3, p, .6, .85))
    if b >= 4: trap(ctx, 880, 430, 360, '20/100 used the whole table.', 'Bottom = 55, not 100 ✗', p)

M2 = [(12, C['red'], 'red'), (9, C['blue'], 'blue'), (6, C['green'], 'green')]
def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    bag(ctx, 300, 380, M2, 1, hl='blue' if b else None, seed=7, R=190)
    write(ctx, '12 red,  9 blue,  6 green', 600, 230, 36, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'P(blue) = ?', 600, 290, 40, C['ink'], seg(p, .2, .5) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 600, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('total = 12 + 9 + 6 = ', C['ink']), ('27', C['yel'])], 600, 370, 32, seg(p, 0, .3))
    rich(ctx, [('9 / 27 = ', C['ink']), ('1/3', C['green'])], 600, 425, 40, seg(p, .3, .55))
    trap(ctx, 600, 470, 600, 'Got 9/28? Recount: 12 + 9 + 6 = 27', 'Count every marble ✗', seg(p, .6, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Probability = part ÷ total', C['blue']), ('Count EVERY item for the total', C['yel']), ('"Given that" = one row or column', C['org'])])

SC = dict(hook=s_hook, bag=s_bag, table=s_table, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['bag'] * 4 + ['table'] * 3 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: part over total', bag='Marbles: count the total', table='Two-way tables and "given that"', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Probability', s_hook, {13: 5.0, 15: 1.5}, CH)
