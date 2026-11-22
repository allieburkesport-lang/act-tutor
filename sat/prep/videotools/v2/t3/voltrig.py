import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/t3'
NAR = json.load(open(f'{D}/beats.json'))

def ellipse(ctx, cx, cy, rx, ry, c, w=3, k=1, fill=None, fa=.25, dash=None):
    if k <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(rx, ry); ctx.new_sub_path(); ctx.arc(0, 0, 1, 0, 2 * PI); ctx.restore()
    if fill: col(ctx, fill, fa * k); ctx.fill_preserve()
    col(ctx, c, k); ctx.set_line_width(w); ctx.set_dash(dash or []); ctx.stroke(); ctx.set_dash([])
def cylinder(ctx, cx, top, bot, rx, c, k=1, layers=0):
    ry = rx * .3
    if layers:
        for i in range(layers):
            y = bot - (bot - top) * (i + 1) / layers
            if seg(k, i / layers, (i + 1) / layers) > 0: ellipse(ctx, cx, y, rx, ry, C['pizza'], 2, 1, C['pizza'], .5)
        return
    ellipse(ctx, cx, bot, rx, ry, c, 3, k, c, .15); line(ctx, cx - rx, top, cx - rx, bot, c, 3, k); line(ctx, cx + rx, top, cx + rx, bot, c, 3, k); ellipse(ctx, cx, top, rx, ry, c, 3, k, c, .2)
def cone(ctx, cx, top, bot, rx, c, k=1, fa=.35):
    if k <= 0: return
    ry = rx * .3
    col(ctx, c, fa * k); ctx.move_to(cx, top); ctx.line_to(cx - rx, bot); ctx.line_to(cx + rx, bot); ctx.close_path(); ctx.fill()
    ellipse(ctx, cx, bot, rx, ry, c, 3, k, c, .3); line(ctx, cx, top, cx - rx, bot, c, 3, k); line(ctx, cx, top, cx + rx, bot, c, 3, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Circles, Volume & Trig', 100, 230, 60, C['ink'], seg(p, 0, .12))
    text(ctx, 'One formula from the reference sheet.', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    rrect(ctx, 100, 350, 460, 230, 16, fill=C['bg2'], stroke=C['yel'], a=seg(p, .3, .45), lw=3)
    text(ctx, 'REFERENCE SHEET', 124, 384, 16, C['yel'], seg(p, .3, .45))
    for i, s in enumerate(['A = πr²    C = 2πr', 'V = πr²h', 'V = ⅓πr²h', 'sin = cos of the other angle']):
        text(ctx, s, 124, 430 + i * 40, 26, C['ink'], seg(p, .4 + i * .1, .5 + i * .1))
    cylinder(ctx, 900, 300, 540, 80, C['blue'], seg(p, .3, .6)); cone(ctx, 1110, 300, 540, 80, C['org'], seg(p, .5, .8))

def s_circ(ctx, b, p, t):
    chip(ctx, 'Circle warm-up', C['blue'])
    cx, cy, R = 300, 360, 170
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 4); disc(ctx, cx, cy, 6, C['blue'])
    line(ctx, cx, cy, cx + R, cy, C['blue'], 4, seg(p, .3, .6) if b == 0 else 1); text(ctx, 'r = 6', cx + R / 2, cy - 16, 30, C['blue'], seg(p, .6, .8) if b == 0 else 1, 'c')
    rich(ctx, [('A = 36π', C['pur'])], 620, 220, 40, seg(p, 0, .2) if b == 0 else 1)
    rich(ctx, [('πr² = 36π  →  r² = 36  →  ', C['ink']), ('r = 6', C['blue'])], 620, 290, 32, seg(p, .2, .7) if b == 0 else 1)
    if b >= 1:
        arc(ctx, cx, cy, R, 0, 2 * PI, C['org'], 8, seg(p, 0, .4))
        rich(ctx, [('C = 2πr = 2π(6) = ', C['ink']), ('12π', C['green'])], 620, 370, 34, seg(p, .1, .5))
        trap(ctx, 620, 410, 520, '6π = πr: forgot the 2', 'C = 2πr ✗', seg(p, .55, 1))

def s_vol(ctx, b, p, t):
    chip(ctx, 'Volume', C['org'])
    cx = 320
    if b == 0:
        cylinder(ctx, cx, 200, 500, 140, C['pizza'], seg(p, 0, .6), layers=8)
        cylinder(ctx, cx, 200, 500, 140, C['blue'], seg(p, .5, .7))
        line(ctx, cx + 170, 200, cx + 170, 500, C['yel'], 3, seg(p, .6, .8)); text(ctx, 'h', cx + 190, 360, 30, C['yel'], seg(p, .6, .8))
        rich(ctx, [('V = ', C['ink']), ('πr²', C['blue']), (' × ', C['ink']), ('h', C['yel'])], 680, 330, 54, seg(p, .65, .95))
        text(ctx, 'circle area × height', 680, 390, 28, C['mute'], seg(p, .75, 1), 'l', False)
        return
    cylinder(ctx, cx, 200, 500, 140, C['blue'], 1); cone(ctx, cx, 200, 500, 140, C['org'], seg(p, 0, .4) if b == 1 else 1)
    rich(ctx, [('cylinder  V = πr²h', C['blue'])], 680, 250, 32, 1)
    if b == 1:
        rich(ctx, [('cone  V = ', C['org']), ('⅓', C['yel']), ('πr²h', C['org'])], 680, 330, 44, seg(p, .3, .7))
        text(ctx, 'a cone holds ⅓ of the cylinder', 680, 390, 26, C['mute'], seg(p, .6, .9), 'l', False); return
    rich(ctx, [('cone  V = ⅓πr²h', C['org'])], 680, 300, 32, 1)
    text(ctx, 'r = 3,  h = 8', 680, 370, 32, C['ink'], seg(p, 0, .2))
    rich(ctx, [('⅓ × π × 9 × 8 = ', C['ink']), ('24π', C['green'])], 680, 430, 36, seg(p, .15, .5))
    trap(ctx, 680, 470, 520, '72π is the CYLINDER.', 'Don\'t forget the ⅓ ✗', seg(p, .6, 1))

AV, BV, CV = (200, 520), (620, 230), (620, 520)  # angle A at left, B at top, right angle C
def tri(ctx, k=1):
    for a_, b_ in ((AV, BV), (BV, CV), (CV, AV)): line(ctx, *a_, *b_, C['ink'], 4, k)
    rrect(ctx, 584, 484, 36, 36, 0, stroke=C['mute'], lw=2, a=k)
def s_trig(ctx, b, p, t):
    chip(ctx, 'Right-triangle trig', C['pur'])
    tri(ctx)
    text(ctx, 'A', AV[0] - 30, AV[1] + 10, 30, C['yel'], 1); text(ctx, 'B', BV[0] + 14, BV[1] - 8, 30, C['green'] if b >= 2 else C['mute'], 1); text(ctx, 'C', CV[0] + 14, CV[1] + 26, 26, C['mute'], 1)
    if b in (0, 1):
        arc(ctx, *AV, 50, -0.6, 0, C['yel'], 3, 1)
        k1 = seg(p, .2, .4) if b == 0 else 1; k2 = seg(p, .45, .65) if b == 0 else 1; k3 = seg(p, .7, .9) if b == 0 else 1
        line(ctx, *BV, *CV, C['red'], 7, k1); text(ctx, 'opposite', 640, 380, 26, C['red'], k1)
        line(ctx, *AV, *CV, C['blue'], 7, k2); text(ctx, 'adjacent', 410, 560, 26, C['blue'], k2, 'c')
        line(ctx, *AV, *BV, C['pur'], 7, k3); text(ctx, 'hypotenuse', 330, 350, 26, C['pur'], k3, 'c')
        if b == 1:
            for i, (n, f, c) in enumerate([('SOH', 'sin = opp / hyp', C['red']), ('CAH', 'cos = adj / hyp', C['blue']), ('TOA', 'tan = opp / adj', C['green'])]):
                k = seg(p, i * .3, i * .3 + .25)
                rrect(ctx, 820, 180 + i * 110, 380, 86, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
                text(ctx, n, 845, 235 + i * 110, 34, c, k); text(ctx, f, 950, 235 + i * 110, 28, C['ink'], k)
        return
    # b >= 2: view from B
    arc(ctx, *BV, 50, PI / 2, PI / 2 + 0.95, C['green'], 3, 1)
    line(ctx, *BV, *CV, C['red'], 7)
    text(ctx, 'opposite A', 640, 360, 24, C['red'], 1 if b > 2 else seg(p, 0, .2))
    text(ctx, '= adjacent to B', 640, 392, 24, C['green'], 1 if b > 2 else seg(p, .3, .55))
    if b == 2: return
    rich(ctx, [('sin A', C['yel']), (' = ', C['ink']), ('cos B', C['green'])], 860, 250, 48, seg(p, 0, .3))
    text(ctx, 'A + B = 90°', 860, 320, 34, C['ink'], seg(p, .3, .5))
    rich(ctx, [('sin 40°', C['yel']), (' = ', C['ink']), ('cos 50°', C['green'])], 860, 400, 40, seg(p, .55, .85))

def s_sat(ctx, b, p, t):
    question(ctx, 'In right triangle ABC, angle C is the right angle and sin A = 33/65. What is cos B?', seg(p, 0, .5) if b == 0 else 1, 24)
    ctx.save(); ctx.translate(-100, 30); ctx.scale(.75, .75); ctx.translate(40, 60); tri(ctx, 1 if b else seg(p, .4, .7))
    text(ctx, 'A', AV[0] - 30, AV[1] + 10, 30, C['yel'], 1 if b else seg(p, .6, .8)); text(ctx, 'B', BV[0] + 14, BV[1] - 8, 30, C['green'], 1 if b else seg(p, .6, .8)); text(ctx, 'C', CV[0] + 14, CV[1] + 26, 26, C['mute'], 1 if b else seg(p, .6, .8))
    if b >= 1: text(ctx, '33', 640, 390, 30, C['red'], kk(b, 1, p, 0, .4)); text(ctx, '65', 380, 360, 30, C['pur'], kk(b, 1, p, 0, .4))
    ctx.restore()
    rows = [(1, [('Step 1  ', C['mute']), ('A + B = 90°', C['ink'])]),
            (2, [('Step 2  ', C['mute']), ('sin A = cos B', C['ink'])]),
            (3, [('Step 3  ', C['mute']), ('cos B = ', C['ink']), ('33/65', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 640, 250 + i * 66, 34, kk(b, bb, p, 0, .6))
    if b >= 3: answer(ctx, 'Answer: 33/65', 640, 440, 300, kk(b, 3, p, .6, .85))
    if b >= 4: trap(ctx, 960, 430, 290, '56/65 is cos A,', 'not cos B ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'Convert 2π/3 radians to degrees.', 120, 230, 40, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 330, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('π → 180°', C['yel'])], 120, 320, 36, seg(p, 0, .25))
    rich(ctx, [('2(180°) / 3 = 360° / 3 = ', C['ink']), ('120°', C['green'])], 120, 390, 40, seg(p, .2, .5))
    trap(ctx, 120, 430, 560, 'Got 60°? You dropped the 2.', 'It\'s 2π/3, not π/3 ✗', seg(p, .6, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Use the reference sheet', C['yel']), ('Cone = ⅓ of a cylinder', C['org']), ('sin of one acute angle = cos of the other', C['green'])])

SC = dict(hook=s_hook, circ=s_circ, vol=s_vol, trig=s_trig, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['circ'] * 2 + ['vol'] * 3 + ['trig'] * 4 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: use the reference sheet', circ='Circle warm-up', vol='Volume: cylinder and cone', trig='Trig: SOH CAH TOA, sin = cos', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Circles, Volume & Trig', s_hook, {15: 5.0, 17: 1.5}, CH)
