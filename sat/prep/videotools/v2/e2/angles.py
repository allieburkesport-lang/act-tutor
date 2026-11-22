import sys, math, json
sys.path.insert(0, '/home/claude/v2')
from engine import *
PI = math.pi
D = '/home/claude/v2/e2'
NAR = json.load(open(f'{D}/beats.json'))
rad = math.radians

def P(cx, cy, deg, r):  # point at math angle deg (counter-clockwise), screen y down
    return cx + r * math.cos(rad(deg)), cy - r * math.sin(rad(deg))
def ray(ctx, cx, cy, deg, r, c, w=4, k=1):
    x, y = P(cx, cy, deg, r); line(ctx, cx, cy, x, y, c, w, k)
def amark(ctx, cx, cy, d0, d1, r, c, k=1, lab=None, lr=None, size=24, fill=True):
    """angle mark from math deg d0 to d1 (d1 > d0)"""
    if k <= 0: return
    if fill: wedge(ctx, cx, cy, r, -rad(d0 + (d1 - d0) * k), -rad(d0), c, .22 * clamp(k * 2))
    arc(ctx, cx, cy, r, -rad(d1), -rad(d0), c, 3, k)
    if lab:
        mx, my = P(cx, cy, (d0 + d1) / 2, lr or r + 26)
        text(ctx, lab, mx, my + 9, size, c, clamp(k * 2 - .6), 'c')
def chip(ctx, s, c):
    w = twidth(ctx, s, 15) + 26; rrect(ctx, 28, 58, w, 30, 15, fill=C['bg2'], stroke=c, lw=1.5); text(ctx, s, 41, 78, 15, c)
def trap(ctx, x, y, w, l1, l2, k):
    rrect(ctx, x, y, w, 110, 12, fill=(0.25, 0.08, 0.08), stroke=C['red'], a=seg(k, 0, .2))
    text(ctx, 'TRAP', x + 20, y + 28, 15, C['red'], seg(k, 0, .2))
    text(ctx, l1, x + 20, y + 62, 21, C['ink'], seg(k, .15, .4))
    text(ctx, l2, x + 20, y + 94, 21, C['red'], seg(k, .35, .6))

# ---------- scenes ----------
def s_hook(ctx, b, p, t):
    text(ctx, 'Angles', 110, 250, 84, C['ink'], seg(p, 0, .12))
    text(ctx, 'Three ideas solve them all.', 112, 310, 30, C['mute'], seg(p, .1, .25), bold=False)
    for i, (big, small, c) in enumerate([('180', 'line or triangle', C['blue']), ('90', 'right angle', C['org']), ('=', 'equal angles', C['green'])]):
        k = seg(p, .3 + i * .15, .45 + i * .15)
        rrect(ctx, 110 + i * 230, 380, 200, 150, 18, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, big, 210 + i * 230, 470, 64, c, k, 'c'); text(ctx, small, 210 + i * 230, 510, 19, C['mute'], k, 'c', False)
    cx, cy = 960, 330
    line(ctx, 800, cy, 1120, cy, C['ink'], 4, seg(p, .05, .3))
    ray(ctx, cx, cy, 55, 170, C['ink'], 4, seg(p, .25, .45))
    amark(ctx, cx, cy, 0, 55, 60, C['yel'], seg(p, .4, .6))
    amark(ctx, cx, cy, 55, 180, 46, C['blue'], seg(p, .5, .7))

def s_line(ctx, b, p, t):
    chip(ctx, 'A straight line = 180°', C['blue'])
    cx, cy = 640, 420
    line(ctx, 300, cy, 980, cy, C['ink'], 5)
    disc(ctx, cx, cy, 7, C['ink'])
    if b == 0:
        k = seg(p, .25, .85); ang = 180 * k
        rrect(ctx, 960, cy - 230, 22, 230, 3, fill=C['bg2'], stroke=C['mute'], lw=1)  # wall
        amark(ctx, cx, cy, 0, max(.1, ang), 70, C['blue'], 1 if k > 0 else 0)
        x, y = P(cx, cy, ang, 300); line(ctx, cx, cy, x, y, C['org'], 12)  # the door
        disc(ctx, x, y, 7, C['yel'])
        text(ctx, 'door', *P(cx, cy, ang, 330), 20, C['org'], seg(p, 0, .15), 'c')
        text(ctx, f'{round(ang)}°', cx, cy - 110, 54, C['blue'], seg(p, .25, .35), 'c')
        return
    ang = 50
    ray(ctx, cx, cy, ang, 280, C['ink'], 4, seg(p, 0, .25))
    amark(ctx, cx, cy, 0, ang, 80, C['yel'], seg(p, .55, .75), '50°', 120)
    amark(ctx, cx, cy, ang, 180, 60, C['blue'], seg(p, .45, .65), '130°', 110)
    rich(ctx, [('130°', C['blue']), (' + ', C['ink']), ('50°', C['yel']), (' = 180°', C['ink'])], 640, 560, 40, seg(p, .7, .95), 'c')

def s_vert(ctx, b, p, t):
    chip(ctx, 'Vertical angles are equal', C['green'])
    cx, cy = 640, 370
    if b == 0:
        th = 30 + 30 * (0.5 - 0.5 * math.cos(t * 1.6))  # scissors open and close
    else:
        th = 40
    for d in (th / 2, 180 + th / 2, -th / 2, 180 - th / 2):
        pass
    ray(ctx, cx, cy, th / 2, 300, C['ink'], 5); ray(ctx, cx, cy, 180 + th / 2, 300, C['ink'], 5)
    ray(ctx, cx, cy, -th / 2, 300, C['ink'], 5); ray(ctx, cx, cy, 180 - th / 2, 300, C['ink'], 5)
    disc(ctx, cx, cy, 8, C['yel'])
    if b == 0:
        amark(ctx, cx, cy, -th / 2, th / 2, 80, C['green'], 1)
        amark(ctx, cx, cy, 180 - th / 2, 180 + th / 2, 80, C['green'], 1)
        text(ctx, f'{round(th)}°', cx + 120, cy + 9, 30, C['green'], 1, 'c')
        text(ctx, f'{round(th)}°', cx - 120, cy + 9, 30, C['green'], 1, 'c')
        text(ctx, 'scissors', cx, cy + 250, 22, C['mute'], seg(p, 0, .2), 'c', False)
        return
    amark(ctx, cx, cy, -20, 20, 80, C['green'], seg(p, 0, .2), '40°', 125, 30)
    amark(ctx, cx, cy, 160, 200, 80, C['green'], seg(p, .1, .3), '40°', 125, 30)
    amark(ctx, cx, cy, 20, 160, 60, C['org'], seg(p, .5, .7), '140°', 105, 28)
    amark(ctx, cx, cy, 200, 340, 60, C['org'], seg(p, .6, .8), '140°', 105, 28)
    label_box(ctx, 'Rule', [('across = equal', C['green'])], 60, 120, 300, C['green'], seg(p, .25, .45), 26)
    label_box(ctx, 'Rule', [('side by side = 180', C['org'])], 920, 120, 320, C['org'], seg(p, .75, .9), 26)

TA, TB, TC = (330, 480), (620, 200), (820, 480)  # triangle: angles A=?, B, C
def tri_angles():
    def ang(p, q, r):
        a1 = math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])); a2 = math.degrees(math.atan2(-(r[1] - p[1]), r[0] - p[0]))
        lo, hi = sorted([a1 % 360, a2 % 360])
        return (lo, hi) if hi - lo < 180 else (hi, lo + 360)
    return ang(TA, TB, TC), ang(TB, TA, TC), ang(TC, TA, TB)
def s_tri(ctx, b, p, t):
    chip(ctx, 'Triangle angles add to 180°', C['blue'])
    cols = [C['blue'], C['org'], C['green']]
    if b < 2:
        k0 = seg(p, 0, .3) if b == 0 else 1
        for (a, q) in ((TA, TB), (TB, TC), (TC, TA)): line(ctx, *a, *q, C['ink'], 4, k0)
        (a0, a1), (b0, b1), (c0, c1) = tri_angles(); spans = [(a0, a1), (b0, b1), (c0, c1)]
        verts = [TA, TB, TC]
        mv = seg(p, .05, .65) if b == 1 else 0
        base = (1000, 470)  # where corners land on a line
        if b == 1: line(ctx, 860, base[1], 1180, base[1], C['ink'], 4, seg(p, 0, .2))
        start = 0
        for i, ((d0, d1), v, c) in enumerate(zip(spans, verts, cols)):
            w = d1 - d0
            x = lerp(v[0], base[0], mv); y = lerp(v[1], base[1], mv)
            r0 = lerp(d0, start, mv); r1 = r0 + w
            k = seg(p, .3 + i * .15, .45 + i * .15) if b == 0 else 1
            amark(ctx, x, y, r0, r1, 70, c, k)
            start += w
        if b == 1:
            amark(ctx, base[0], base[1], 0, 180, 110, C['yel'], seg(p, .65, .85), '180°', 140, 34)
            rich(ctx, [('●', cols[0]), (' + ', C['ink']), ('●', cols[1]), (' + ', C['ink']), ('●', cols[2]), (' = 180°', C['yel'])], 330, 590, 40, seg(p, .75, .95))
        return
    # b == 2: right triangle
    A, Bq, Cq = (360, 500), (360, 200), (820, 500)
    for (a, q) in ((A, Bq), (Bq, Cq), (Cq, A)): line(ctx, *a, *q, C['ink'], 4)
    rrect(ctx, 360, 460, 40, 40, 0, stroke=C['org'], lw=3, a=seg(p, 0, .2))
    text(ctx, '90°', 420, 450, 30, C['org'], seg(p, .05, .25))
    amark(ctx, *Bq, 270, 270 + math.degrees(math.atan2(300, 460)) * 0 + 56.9, 60, C['blue'], seg(p, .3, .5))
    amark(ctx, *Cq, 180 - 33.1, 180, 80, C['green'], seg(p, .35, .55))
    rich(ctx, [('90°', C['org']), (' + ', C['ink']), ('●', C['blue']), (' + ', C['ink']), ('●', C['green']), (' = 180°', C['ink'])], 880, 300, 36, seg(p, .45, .7))
    rich(ctx, [('so  ', C['mute']), ('●', C['blue']), (' + ', C['ink']), ('●', C['green']), (' = 90°', C['yel'])], 880, 370, 40, seg(p, .7, .95))

PY1, PY2, PCX = 270, 470, 640
TD = 62  # transversal angle (deg)
def cross_x(y): return PCX + (y - (PY1 + PY2) / 2) / -math.tan(rad(TD))
def tracks(ctx, k=1, k2=1):
    for y in (PY1, PY2):
        line(ctx, 160, y, 1120, y, C['ink'], 5, k)
    # ties
    for i in range(12):
        x = 200 + i * 80; line(ctx, x, PY1 - 14, x, PY1 + 14, C['brown'], 2, k * .7, .6); line(ctx, x, PY2 - 14, x, PY2 + 14, C['brown'], 2, k * .7, .6)
    x1, x2 = cross_x(110), cross_x(630)
    line(ctx, x1, 110, x2, 630, C['yel'], 5, k2)
def four(ctx, x, y, k, kk=None):
    """acute angles blue, obtuse orange at a crossing"""
    amark(ctx, x, y, 0, TD, 52, C['blue'], k)
    amark(ctx, x, y, 180, 180 + TD, 52, C['blue'], k)
    amark(ctx, x, y, TD, 180, 40, C['org'], kk if kk is not None else k)
    amark(ctx, x, y, 180 + TD, 360, 40, C['org'], kk if kk is not None else k)
def s_par(ctx, b, p, t):
    chip(ctx, 'Parallel lines repeat angles', C['org'])
    if b == 0:
        tracks(ctx, seg(p, 0, .35), seg(p, .45, .75))
        text(ctx, 'parallel', 1130, PY1 + 8, 20, C['mute'], seg(p, .2, .35), 'r', False)
        text(ctx, 'transversal', cross_x(130) + 20, 130, 24, C['yel'], seg(p, .7, .9))
        return
    tracks(ctx)
    x1, x2 = cross_x(PY1), cross_x(PY2)
    if b == 1:
        four(ctx, x1, PY1, seg(p, 0, .2))
        k = seg(p, .25, .75)
        four(ctx, lerp(x1, x2, k), lerp(PY1, PY2, k), 1 if k > 0 else 0)
        if p > .8: text(ctx, 'same angles ✓', x2 + 70, PY2 + 70, 28, C['green'], seg(p, .8, .95))
        return
    four(ctx, x1, PY1, 1); four(ctx, x2, PY2, 1)
    label_box(ctx, 'Small (acute)', [('all equal', C['blue'])], 60, 520, 260, C['blue'], seg(p, .1, .3), 26)
    label_box(ctx, 'Big (obtuse)', [('all equal', C['org'])], 340, 520, 260, C['org'], seg(p, .35, .55), 26)
    label_box(ctx, 'Together', [('small + big = 180', C['yel'])], 620, 520, 320, C['yel'], seg(p, .65, .85), 26)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'Two parallel lines are cut by a transversal. One angle is 65°. Find the obtuse angle.', 80, 145, 24, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    ox, y1, y2 = 300, 290, 450
    xa = lambda y: ox + (y - 370) / -math.tan(rad(65))
    kb = p if b == 0 else 1
    line(ctx, 90, y1, 510, y1, C['ink'], 4, seg(kb, .3, .55)); line(ctx, 90, y2, 510, y2, C['ink'], 4, seg(kb, .3, .55))
    line(ctx, xa(220), 220, xa(560), 560, C['ink'], 3, seg(kb, .45, .7))
    amark(ctx, xa(y1), y1, 0, 65, 46, C['blue'], seg(kb, .65, .85), '65°', 72)
    if b >= 1: text(ctx, 'acute ✓', 400, y1 + 40, 22, C['blue'], seg(p, .3, .6) if b == 1 else 1)
    if b == 2: amark(ctx, xa(y2), y2, 65, 180, 40, C['org'], seg(p, .1, .5) if b == 2 else 1, '?', 66, 30)
    rows = [(1, [('Step 1  ', C['mute']), ('65° is ', C['ink']), ('acute', C['blue']), (' (small)', C['mute'])]),
            (2, [('Step 2  ', C['mute']), ('small + big = ', C['ink']), ('180°', C['yel'])]),
            (3, [('Step 3  ', C['mute']), ('180 − 65 = ', C['ink']), ('115°', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 600, 260 + i * 70, 32, seg(p, 0, .7) if b == bb else 1)
    if b >= 3:
        amark(ctx, xa(y2), y2, 65, 180, 40, C['green'], 1, '115°', 70, 26)
        rrect(ctx, 600, 470, 260, 64, 12, fill=C['bg2'], stroke=C['green'], a=seg(p, .6, .8) if b == 3 else 1)
        text(ctx, 'Answer: 115°', 730, 513, 32, C['green'], seg(p, .65, .85) if b == 3 else 1, 'c')
    if b >= 4: trap(ctx, 880, 458, 380, 'Obtuse means bigger than 90°,', 'so 65° can\'t be it ✗', p)

def s_sat2(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'A triangle has angles of 50° and 60°. What is the third angle?', 80, 145, 25, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    A, Bv, Cv = (120, 520), (470, 520), (327.3, 272.9)  # angles: A=60? computed below
    kb = p if b == 0 else 1
    for (a, q) in ((A, Bv), (Bv, Cv), (Cv, A)): line(ctx, *a, *q, C['ink'], 4, seg(kb, .3, .6))
    angA = math.degrees(math.atan2(A[1] - Cv[1], Cv[0] - A[0])); angB = math.degrees(math.atan2(Bv[1] - Cv[1], Bv[0] - Cv[0]))
    amark(ctx, *A, 0, angA, 50, C['blue'], seg(kb, .55, .75), '50°', 80)
    amark(ctx, *Bv, 180 - angB, 180, 50, C['org'], seg(kb, .6, .8), '60°', 80)
    top = (270 - angB + 90, 270 + 90 - 0)
    d0 = math.degrees(math.atan2(-(A[1] - Cv[1]), A[0] - Cv[0])) % 360; d1 = math.degrees(math.atan2(-(Bv[1] - Cv[1]), Bv[0] - Cv[0])) % 360
    lo, hi = sorted([d0, d1])
    amark(ctx, *Cv, lo, hi, 40, C['green'], seg(kb, .7, .9), '?' if b < 1 else '70°', 68, 26)
    if b >= 1:
        rich(ctx, [('50 + 60 = ', C['ink']), ('110', C['yel'])], 600, 280, 36, seg(p, 0, .35))
        rich(ctx, [('180 − 110 = ', C['ink']), ('70°', C['green'])], 600, 350, 36, seg(p, .35, .7))
        rrect(ctx, 600, 390, 320, 64, 12, fill=C['bg2'], stroke=C['green'], a=seg(p, .7, .85) if b == 1 else 1)
        text(ctx, 'Answer: 70°', 760, 433, 32, C['green'], seg(p, .75, .9) if b == 1 else 1, 'c')
    if b >= 2: trap(ctx, 600, 480, 560, '110° is just the two angles added.', 'Always subtract from 180 ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    A, Bq, Cq = (120, 520), (120, 240), (520, 520)
    for (a, q) in ((A, Bq), (Bq, Cq), (Cq, A)): line(ctx, *a, *q, C['ink'], 4)
    rrect(ctx, 120, 482, 38, 38, 0, stroke=C['org'], lw=3); text(ctx, '90°', 170, 470, 24, C['org'])
    amark(ctx, *Cq, 180 - 35, 180, 70, C['blue'], 1, '35°', 100, 26)
    amark(ctx, *Bq, 270, 325, 50, C['green'], 1, '?' if b == 0 else '55°', 80, 26)
    write(ctx, 'A right triangle has a 35° angle.', 620, 250, 30, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'What is the other acute angle?', 620, 295, 30, C['ink'], seg(p, .2, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 620, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('90 − 35 = ', C['ink']), ('55°', C['green'])], 620, 380, 44, seg(p, 0, .4))
    rrect(ctx, 620, 430, 560, 100, 12, fill=(0.25, 0.08, 0.08), stroke=C['red'], a=seg(p, .5, .65))
    text(ctx, 'TRAP', 640, 458, 15, C['red'], seg(p, .5, .65))
    text(ctx, '180 − 35 = 145 forgot the right angle ✗', 640, 498, 24, C['ink'], seg(p, .55, .85))

def s_recap(ctx, b, p, t):
    text(ctx, 'Lock it in', 640, 150, 54, C['ink'], seg(p, 0, .1), 'c')
    for i, (n, s, c) in enumerate([('1', 'Line or triangle = 180°', C['blue']), ('2', 'Vertical angles are equal', C['green']), ('3', 'Parallel lines: same two angles', C['org'])]):
        k = seg(p, .12 + i * .25, .27 + i * .25)
        rrect(ctx, 260, 210 + i * 100, 760, 80, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        disc(ctx, 305, 250 + i * 100, 22, c, k); text(ctx, n, 305, 259 + i * 100, 24, C['bg'], k, 'c')
        text(ctx, s, 350, 262 + i * 100, 34, c, k)

SC = dict(hook=s_hook, line=s_line, vert=s_vert, tri=s_tri, par=s_par, sat=s_sat, sat2=s_sat2, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['line'] * 2 + ['vert'] * 2 + ['tri'] * 3 + ['par'] * 3 + ['sat'] * 5 + ['sat2'] * 3 + ['turn'] * 2 + ['recap']
assert len(PLAN) == len(NAR)
BEATS = list(zip(PLAN, NAR))
if __name__ == '__main__':
    if sys.argv[1:] == ['stills']:
        import cairo
        cnt = {}
        for i, (n, _) in enumerate(BEATS):
            b = cnt.get(n, 0); cnt[n] = b + 1
            for pp in (.5, 1):
                surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); background(ctx); SC[n](ctx, b, pp, 3); caption(ctx, NAR[i][:120])
                surf.write_to_png(f'{D}/st/{i:02d}_{int(pp*10)}.png')
    else:
        durs, starts = render(BEATS, SC, sys.argv[1], 'SAT Math · Angles', f'{D}/wav', pads={19: 5.0, 21: 1.5})
        json.dump(dict(durs=durs, starts=starts), open(f'{D}/timing.json', 'w'))
        thumb(s_hook, 0, f'{D}/thumb.png')
