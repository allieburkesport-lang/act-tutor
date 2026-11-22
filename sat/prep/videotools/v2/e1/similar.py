import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/e1'
NAR = json.load(open(f'{D}/beats.json'))

def tri(ctx, x, y, s, c, k, labels=None, lc=None, fill=.15):
    # right triangle, legs 4 (base) and 3 (height) units, s px per unit, bottom-left at (x, y)
    if k <= 0: return
    P = [(x, y), (x + 4 * s, y), (x, y - 3 * s)]
    ctx.move_to(*P[0]); [ctx.line_to(*q) for q in P[1:]]; ctx.close_path()
    col(ctx, c, fill * k); ctx.fill_preserve(); col(ctx, c, k); ctx.set_line_width(4); ctx.stroke()
    if labels:
        a, b, h = labels; lc = lc or C['ink']
        text(ctx, a, x - 16, y - 1.5 * s + 10, 26, lc, k, 'r')
        text(ctx, b, x + 2 * s, y + 34, 26, lc, k, 'c')
        text(ctx, h, x + 2 * s + 18, y - 1.5 * s - 8, 26, lc, k)
def sq(ctx, x, y, s, c, k, grid=0):
    if k <= 0: return
    rrect(ctx, x, y - s, s, s, 4, fill=None, stroke=c, a=k, lw=4)
    for i in range(1, grid):
        line(ctx, x + i * s / grid, y - s, x + i * s / grid, y, c, 1.5, 1, .5 * k); line(ctx, x, y - i * s / grid, x + s, y - i * s / grid, c, 1.5, 1, .5 * k)
def cube(ctx, x, y, s, c, k):
    if k <= 0: return
    d = s * .4
    rrect(ctx, x, y - s, s, s, 2, stroke=c, a=k, lw=3)
    for (a, b) in [((x, y - s), (x + d, y - s - d)), ((x + s, y - s), (x + s + d, y - s - d)), ((x + s, y), (x + s + d, y - d))]:
        line(ctx, *a, *b, c, 3, 1, k)
    line(ctx, x + d, y - s - d, x + s + d, y - s - d, c, 3, 1, k); line(ctx, x + s + d, y - s - d, x + s + d, y - d, c, 3, 1, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Similar Shapes', 100, 220, 66, C['ink'], seg(p, 0, .12))
    text(ctx, 'Same shape. Different size.', 102, 280, 30, C['mute'], seg(p, .1, .3), bold=False)
    tri(ctx, 130, 560, 40, C['blue'], seg(p, .2, .4))
    tri(ctx, 420, 560, 70, C['org'], seg(p, .35, .6))
    rich(ctx, [('× k', C['yel'])], 330, 470, 44, seg(p, .55, .75))
    rich(ctx, [('k', C['yel']), (' = scale factor', C['ink'])], 820, 420, 36, seg(p, .7, .9))

def s_photo(ctx, b, p, t):
    chip(ctx, 'Zoom a photo 2×', C['blue'])
    sq(ctx, 200, 500, 140, C['blue'], 1, 1); text(ctx, '1 × 1', 270, 540, 26, C['mute'], 1, 'c')
    k = seg(p, .15, .5); s = lerp(140, 280, k)
    sq(ctx, 520, 500, s, C['org'], 1, 2 if k > .95 else 1)
    text(ctx, 'sides × 2', 900, 280, 34, C['org'], seg(p, .3, .5))
    text(ctx, 'space × 4', 900, 350, 40, C['yel'], seg(p, .65, .85))
    text(ctx, '4 little squares fit', 900, 400, 24, C['mute'], seg(p, .75, .95), bold=False)

def s_rule(ctx, b, p, t):
    chip(ctx, 'The one rule', C['yel'])
    rows = [('Length / Perimeter', '× k', '1 dimension', C['blue']), ('Area', '× k²', '2 dimensions', C['green']), ('Volume', '× k³', '3 dimensions', C['org'])]
    for i, (a, m, d, c) in enumerate(rows):
        k = seg(p, .1 + i * .25, .3 + i * .25) if b == 0 else 1
        rrect(ctx, 200, 170 + i * 120, 880, 90, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, a, 240, 228 + i * 120, 34, C['ink'], k); text(ctx, m, 760, 228 + i * 120, 44, c, k, 'c')
        if b == 1: text(ctx, d, 1050, 228 + i * 120, 24, C['mute'], seg(p, .1 + i * .25, .3 + i * .25), 'r', False)

def s_sides(ctx, b, p, t):
    chip(ctx, 'Sides: × k', C['blue'])
    tri(ctx, 140, 470, 45, C['blue'], 1 if b else seg(p, 0, .2), ('3', '4', '5'))
    text(ctx, '× 2', 400, 330, 44, C['yel'], 1 if b else seg(p, .25, .45))
    tri(ctx, 560, 560, 90, C['org'], 1 if b else seg(p, .4, .7), ('6', '8', '10'), C['org'])
    if b: trap(ctx, 820, 160, 420, 'Said 5, 6, 7? That\'s +2.', 'Similar = multiply ✗', p)

def s_area(ctx, b, p, t):
    chip(ctx, 'Area: × k²', C['green'])
    write(ctx, 'Area 10, scaled by 3. New area?', 120, 220, 38, C['ink'], seg(p, 0, .3) if b == 0 else 1)
    rich(ctx, [('k = 3  →  k² = ', C['ink']), ('9', C['green'])], 120, 310, 40, seg(p, .35, .6) if b == 0 else 1)
    rich(ctx, [('10 × 9 = ', C['ink']), ('90', C['green'])], 120, 380, 44, seg(p, .6, .85) if b == 0 else 1)
    if b: trap(ctx, 120, 420, 560, 'Said 30? You used k.', 'Area needs k² ✗', p)
    sq(ctx, 820, 470, 75, C['blue'], 1); sq(ctx, 960, 470, 225, C['green'], seg(p, .4, .7) if b == 0 else 1, 3)

def s_vol(ctx, b, p, t):
    chip(ctx, 'Volume: × k³', C['org'])
    if b == 0:
        text(ctx, 'Box scaled by 2', 120, 220, 40, C['ink'], seg(p, 0, .2))
        rich(ctx, [('k³ = 2³ = ', C['ink']), ('8', C['org'])], 120, 300, 48, seg(p, .35, .65))
        text(ctx, '8 times the volume', 120, 360, 30, C['org'], seg(p, .6, .85))
        cube(ctx, 680, 480, 90, C['blue'], seg(p, .1, .3)); cube(ctx, 880, 520, 180, C['org'], seg(p, .4, .7)); return
    rows = [('length', 'k¹', '1D', C['blue']), ('area', 'k²', '2D', C['green']), ('volume', 'k³', '3D', C['org'])]
    for i, (a, m, d, c) in enumerate(rows):
        k = seg(p, .05 + i * .28, .25 + i * .28)
        rich(ctx, [(d + '  ', C['mute']), (a + '  →  ', C['ink']), (m, c)], 360, 240 + i * 100, 52, k)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 90, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'Two similar shapes have areas 25 and 9.', 80, 138, 24, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    write(ctx, 'What is the ratio of their sides?', 80, 172, 24, C['yel'], seg(p, .4, .7) if b == 0 else 1)
    if b >= 1:
        k = 1 if b > 1 else seg(p, 0, .3)
        rich(ctx, [('area ratio uses k²  →  take ', C['ink']), ('√', C['yel'])], 80, 270, 32, k)
        rich(ctx, [('√25 : √9  =  ', C['ink']), ('5 : 3', C['green'])], 80, 340, 44, 1 if b > 1 else seg(p, .35, .7))
        answer(ctx, 'Sides: 5 : 3', 80, 380, 320, 1 if b > 1 else seg(p, .7, .95))
    if b >= 2: trap(ctx, 520, 380, 600, '25 : 9 is the AREA ratio.', 'Square root back to sides ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'Two similar cubes have sides 2 and 6.', 120, 210, 38, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'How many times bigger is the volume?', 120, 265, 34, C['yel'], seg(p, .3, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 360, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('k = 6 ÷ 2 = 3', C['ink'])], 120, 350, 34, seg(p, 0, .3))
    rich(ctx, [('k³ = 3³ = ', C['ink']), ('27', C['green'])], 120, 410, 40, seg(p, .25, .5))
    trap(ctx, 120, 445, 560, 'Said 9? That\'s area (k²).', 'Volume needs k³ ✗', seg(p, .6, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Similar = multiply every side by k', C['yel']), ('Area × k²,  volume × k³', C['green']), ('Area back to sides: square root', C['blue'])])

SC = dict(hook=s_hook, photo=s_photo, rule=s_rule, sides=s_sides, area=s_area, vol=s_vol, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'photo', 'rule', 'sides', 'sides', 'area', 'area', 'vol', 'vol', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea: scale factor k', photo='Zoom a photo', rule='k, k², k³', sides='Sides', area='Area', vol='Volume', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Similar shapes', s_hook, {12: 5.0, 14: 1.5}, CH)
