import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a6'
NAR = json.load(open(f'{D}/beats.json'))

def glass(ctx, x, y, w, h, fill_k, c, a=1, label=None):
    if a <= 0: return
    hh = h * clamp(fill_k)
    rrect(ctx, x, y + h - hh, w, hh, 6, fill=c, a=a * .85)
    rrect(ctx, x, y, w, h, 8, stroke=C['ink'], a=a, lw=3)
    if label: text(ctx, label, x + w / 2, y + h + 30, 20, C['mute'], a, 'c', False)
def cups(ctx, x, y, n, c, k, size=34, gap=44):
    for i in range(n):
        kk_ = seg(k, i / n, (i + 1) / n)
        if kk_ > 0: glass(ctx, x + i * gap, y, size, size * 1.3, kk_, c, kk_)
def frac(ctx, top, bot, x, y, size, ctop, cbot, k=1, w=None):
    w = w or max(twidth(ctx, top, size), twidth(ctx, bot, size)) + 16
    text(ctx, top, x, y - 12, size, ctop, k, 'c'); line(ctx, x - w / 2, y, x + w / 2, y, C['ink'], 3, k); text(ctx, bot, x, y + size + 4, size, cbot, k, 'c')
def strike(ctx, x1, y, x2, k): line(ctx, x1, y, x2, y - 6, C['red'], 4, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Ratios & Rates', 100, 240, 76, C['ink'], seg(p, 0, .12))
    text(ctx, 'Line up the units. Let them cancel.', 102, 300, 30, C['mute'], seg(p, .1, .3), bold=False)
    frac(ctx, 'miles', 'hour', 300, 470, 40, C['blue'], C['org'], seg(p, .3, .45))
    text(ctx, '×', 420, 488, 44, C['ink'], seg(p, .45, .55), 'c')
    frac(ctx, 'hour', 'minutes', 560, 470, 40, C['org'], C['green'], seg(p, .5, .65))
    strike(ctx, 262, 518, 338, seg(p, .7, .8)); strike(ctx, 515, 454, 605, seg(p, .75, .85))
    text(ctx, '=', 700, 488, 44, C['ink'], seg(p, .85, .95), 'c')
    frac(ctx, 'miles', 'minutes', 820, 470, 40, C['blue'], C['green'], seg(p, .88, 1))

def s_ratio(ctx, b, p, t):
    chip(ctx, 'A ratio compares two amounts', C['blue'])
    rows = [(3, 4, '3 : 4'), (6, 8, '6 : 8'), (9, 12, '9 : 12')]
    for r, (j, w, lab) in enumerate(rows):
        if r > 0 and b < 1: break
        k = seg(p, 0, .6) if (b == 0 and r == 0) else (seg(p, (r - 1) * .4, (r - 1) * .4 + .4) if b == 1 else 1)
        y = 150 + r * 150
        text(ctx, 'lemon', 90, y + 40, 20, C['yel'], k); cups(ctx, 170, y, j, C['yel'], k, 30, 38)
        text(ctx, 'water', 90, y + 100, 20, C['blue'], k); cups(ctx, 170, y + 60, w, C['blue'], k, 30, 38)
        text(ctx, lab, 860, y + 85, 48, C['ink'], seg(k, .6, 1))
    if b == 0: text(ctx, 'lemon : water', 860, 140, 22, C['mute'], seg(p, .6, .9), 'l', False)
    if b == 1: text(ctx, 'same taste ✓', 1000, 610, 28, C['green'], seg(p, .85, 1), 'c')

def s_rate(ctx, b, p, t):
    chip(ctx, 'A rate = per ONE', C['org'])
    text(ctx, '60 miles per hour', 640, 260, 60, C['ink'], seg(p, 0, .3), 'c')
    frac(ctx, '60 miles', '1 hour', 640, 410, 48, C['blue'], C['org'], seg(p, .3, .6))
    text(ctx, '"per" means "for every 1"', 640, 560, 30, C['yel'], seg(p, .6, .85), 'c')

def s_prop(ctx, b, p, t):
    chip(ctx, 'Proportion: two equal ratios', C['pur'])
    text(ctx, '3 cups flour  →  4 servings', 90, 180, 34, C['ink'], kk(b, 0, p, 0, .4))
    text(ctx, '? cups flour  →  10 servings', 90, 235, 34, C['ink'], kk(b, 0, p, .4, .8))
    if b >= 1:
        k = kk(b, 1, p, 0, .8)
        text(ctx, 'cups', 160, 345, 22, C['yel'], k, 'c'); text(ctx, 'servings', 160, 455, 22, C['blue'], k, 'c')
        frac(ctx, '3', '4', 300, 400, 54, C['yel'], C['blue'], k)
        text(ctx, '=', 390, 418, 54, C['ink'], k, 'c')
        frac(ctx, 'c', '10', 480, 400, 54, C['yel'], C['blue'], k)
    if b >= 2:
        k = kk(b, 2, p, 0, .3)
        line(ctx, 315, 360, 470, 450, C['pur'], 3, k, .7, [8, 6]); line(ctx, 315, 450, 470, 360, C['pur'], 3, k, .7, [8, 6])
        rich(ctx, [('4c = 3 × 10 = 30', C['ink'])], 640, 360, 40, kk(b, 2, p, .2, .5))
        rich(ctx, [('c = 30 ÷ 4 = ', C['ink']), ('7.5 cups', C['green'])], 640, 430, 40, kk(b, 2, p, .5, .8))
        answer(ctx, 'Answer: 7.5 cups', 90, 520, 340, kk(b, 2, p, .8, 1))
    if b >= 3: trap(ctx, 640, 500, 600, '3/4 = 10/c puts cups on the bottom → 13.3', 'Same units top, same units bottom ✗', p)

def piece(ctx, s, x, y, c, k, crossed=0):
    w = twidth(ctx, s, 30) + 30
    rrect(ctx, x - w / 2, y - 30, w, 44, 10, fill=C['bg2'], stroke=c, a=k, lw=2)
    text(ctx, s, x, y + 2, 30, c, k, 'c')
    if crossed: line(ctx, x - w / 2 - 6, y + 10, x + w / 2 + 6, y - 24, C['red'], 4, crossed)
def s_units(ctx, b, p, t):
    chip(ctx, 'Units are puzzle pieces', C['green'])
    if b == 0:
        piece(ctx, '36 inches', 260, 300, C['blue'], seg(p, 0, .2))
        text(ctx, '×', 420, 310, 44, C['ink'], seg(p, .2, .3), 'c')
        piece(ctx, '1 foot', 560, 260, C['green'], seg(p, .3, .45)); line(ctx, 480, 300, 640, 300, C['ink'], 3, seg(p, .3, .45)); piece(ctx, '12 inches', 560, 350, C['blue'], seg(p, .35, .5))
        piece(ctx, '36 inches', 260, 300, C['blue'], 1 if p > .2 else 0, seg(p, .6, .75)); piece(ctx, '12 inches', 560, 350, C['blue'], 1 if p > .5 else 0, seg(p, .65, .8))
        rich(ctx, [('= ', C['ink']), ('3 feet', C['green'])], 700, 310, 44, seg(p, .82, 1))
        return
    piece(ctx, '12 inches', 640, 260, C['blue'], 1); line(ctx, 540, 300, 740, 300, C['ink'], 3); piece(ctx, '1 foot', 640, 350, C['green'], 1)
    rich(ctx, [('= ', C['ink']), ('1', C['yel'])], 780, 315, 54, seg(p, .2, .45))
    text(ctx, 'Same amount, new units.', 640, 470, 32, C['yel'], seg(p, .55, .85), 'c')

def s_split(ctx, b, p, t):
    chip(ctx, 'Split by a ratio: add the parts', C['org'])
    text(ctx, 'Share 40 candies in the ratio 3 : 5', 640, 150, 36, C['ink'], kk(b, 0, p, 0, .5), 'c')
    # 8 boxes = parts
    k1 = kk(b, 1, p, 0, .5)
    for i in range(8):
        c = C['blue'] if i < 3 else C['org']; x = 260 + i * 95
        rrect(ctx, x, 230, 80, 80, 12, fill=C['bg2'], stroke=c, a=k1, lw=3)
        if b >= 1: text(ctx, '5', x + 40, 283, 34, c, kk(b, 1, p, .55, .8), 'c')
    if b >= 1:
        rich(ctx, [('3 + 5 = ', C['ink']), ('8 parts', C['yel']), ('    40 ÷ 8 = ', C['ink']), ('5 per part', C['yel'])], 640, 380, 32, kk(b, 1, p, .3, .9), 'c')
    if b >= 2:
        k = kk(b, 2, p, 0, .5)
        rich(ctx, [('3 × 5 = ', C['ink']), ('15', C['blue']), ('      5 × 5 = ', C['ink']), ('25', C['org'])], 640, 460, 38, k, 'c')
        rich(ctx, [('check: 15 + 25 = 40 ✓', C['green'])], 640, 530, 30, kk(b, 2, p, .6, .9), 'c')

def s_sat(ctx, b, p, t):
    question(ctx, 'A car travels at 60 miles per hour. What is its speed in feet per second?', seg(p, 0, .5) if b == 0 else 1)
    k0 = (1 if b > 0 else seg(p, .5, .9)) if b < 4 else 0
    text(ctx, 'have: miles / hour', 90, 230, 26, C['mute'], k0, 'l', False); text(ctx, 'want: feet / second', 90, 270, 26, C['yel'], k0, 'l', False)
    if b >= 1:
        k = kk(b, 1, p, 0, .5)
        frac(ctx, '60 miles', '1 hour', 470, 360, 30, C['blue'], C['org'], k); text(ctx, '×', 590, 375, 34, C['ink'], k, 'c')
        frac(ctx, '5,280 feet', '1 mile', 710, 360, 30, C['green'], C['blue'], k)
        strike(ctx, 410, 346, 530, kk(b, 1, p, .4, .6)); strike(ctx, 665, 396, 755, kk(b, 1, p, .45, .65))
        rich(ctx, [('= ', C['ink']), ('316,800 feet per hour', C['green'])], 470, 470, 30, kk(b, 1, p, .6, 1))
    if b >= 2:
        k = kk(b, 2, p, 0, .6)
        text(ctx, '×', 840, 375, 34, C['ink'], k, 'c'); frac(ctx, '1 hour', '3,600 sec', 960, 360, 30, C['org'], C['pur'], k)
        strike(ctx, 425, 396, 515, kk(b, 2, p, .5, .7)); strike(ctx, 915, 346, 1005, kk(b, 2, p, .55, .75))
    if b >= 3:
        rich(ctx, [('316,800 ÷ 3,600 = ', C['ink']), ('88 feet per second', C['green'])], 470, 540, 30, kk(b, 3, p, 0, .5))
        answer(ctx, 'Answer: 88 ft/sec', 880, 450, 330, kk(b, 3, p, .6, .85))
    if b >= 4: trap(ctx, 60, 185, 400, 'Changed only one unit?', 'Check BOTH units: ft and sec ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'A car goes 45 miles per hour for 2.5 hours.', 120, 220, 34, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'How far does it go?', 120, 270, 34, C['ink'], seg(p, .2, .5) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 370, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('distance = rate × time', C['blue'])], 120, 360, 34, seg(p, 0, .3))
    rich(ctx, [('45 × 2.5 = ', C['ink']), ('112.5 miles', C['green'])], 120, 420, 40, seg(p, .2, .5))
    trap(ctx, 680, 330, 520, '45 ÷ 2.5 = 18 divided instead', 'Distance MULTIPLIES ✗', seg(p, .55, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Line up the units', C['blue']), ('Same units top, same units bottom', C['yel']), ('Add the parts before you split', C['org'])])

SC = dict(hook=s_hook, ratio=s_ratio, rate=s_rate, prop=s_prop, units=s_units, split=s_split, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['ratio'] * 2 + ['rate'] + ['prop'] * 4 + ['units'] * 2 + ['split'] * 3 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: line up the units', ratio='Ratios: lemonade', rate='Rates: per one', prop='Proportions', units='Unit conversions', split='Splitting by a ratio', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Ratios & Rates', s_hook, {18: 5.0, 20: 1.5}, CH)
