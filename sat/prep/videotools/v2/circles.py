import sys, math, json
sys.path.insert(0, '/home/claude/v2')
from engine import *
PI = math.pi
NAR = json.load(open('/home/claude/v2/circ/beats.json'))

def dog(ctx, x, y, s=1, face=1):
    disc(ctx, x, y, 15 * s, C['org']); disc(ctx, x + 13 * s * face, y - 9 * s, 10 * s, C['org'])
    disc(ctx, x + 17 * s * face, y - 11 * s, 2.2 * s, (0.1, 0.1, 0.1))
    col(ctx, C['brown']); ctx.new_sub_path(); ctx.arc(x + 8 * s * face, y - 16 * s, 5 * s, 0, 2 * PI); ctx.fill()
def stake(ctx, x, y):
    rrect(ctx, x - 5, y - 5, 10, 10, 2, fill=C['brown']); disc(ctx, x, y, 3, C['ink'])
def brace_label(ctx, x1, y1, x2, y2, s, c, k, off=18, size=26):
    if k <= 0: return
    nx, ny = -(y2 - y1), x2 - x1; L = math.hypot(nx, ny); nx, ny = nx / L * off, ny / L * off
    line(ctx, x1 + nx, y1 + ny, x2 + nx, y2 + ny, c, 2, k)
    line(ctx, x1, y1, x1 + nx * 1.3, y1 + ny * 1.3, c, 2, k); line(ctx, x2, y2, x2 + nx * 1.3, y2 + ny * 1.3, c, 2, k)
    text(ctx, s, (x1 + x2) / 2 + nx * 2.4, (y1 + y2) / 2 + ny * 2.4 + 9, size, c, clamp(k * 2), 'c')
def chip(ctx, s, c):
    w = twidth(ctx, s, 15) + 26; rrect(ctx, 28, 58, w, 30, 15, fill=C['bg2'], stroke=c, lw=1.5); text(ctx, s, 41, 78, 15, c)

# ---------- scenes ----------
def s_hook(ctx, b, p, t):
    cx, cy, R = 860, 330, 170
    text(ctx, 'Circles', 110, 270, 84, C['ink'], seg(p, 0, .15))
    text(ctx, 'Find r. The circle tells you', 112, 330, 30, C['mute'], seg(p, .15, .3), bold=False)
    text(ctx, 'everything else.', 112, 370, 30, C['mute'], seg(p, .2, .35), bold=False)
    arc(ctx, cx, cy, R, -PI / 2, 3 * PI / 2, C['ink'], 5, seg(p, .05, .5))
    disc(ctx, cx, cy, 6, C['blue'], seg(p, .4, .5))
    line(ctx, cx, cy, cx + R, cy, C['blue'], 6, seg(p, .5, .75))
    text(ctx, 'r', cx + R / 2, cy - 18, 44, C['blue'], seg(p, .7, .85), 'c')
    for i, (s, c) in enumerate([('d = 2r', C['green']), ('C = 2πr', C['org']), ('A = πr²', C['pur'])]):
        text(ctx, s, 110 + i * 190, 470, 32, c, seg(p, .75 + i * .07, .85 + i * .07))

def s_leash(ctx, b, p, t):
    chip(ctx, 'The dog on a leash', C['blue'])
    cx, cy, R = 640, 345, 200
    stake(ctx, cx, cy)
    if b == 0:
        k = seg(p, .3, 1); ang = -PI / 2 + 2 * PI * k
        arc(ctx, cx, cy, R, -PI / 2, -PI / 2 + 2 * PI, C['ink'], 4, k)
        dx, dy = cx + R * math.cos(ang), cy + R * math.sin(ang)
        line(ctx, cx, cy, dx, dy, C['blue'], 3, seg(p, 0, .15))
        if p > .05: dog(ctx, dx, dy, 1.2, 1 if math.cos(ang + PI / 2) >= 0 else -1)
        text(ctx, 'stake', cx, cy + 32, 18, C['mute'], seg(p, 0, .1), 'c', False)
        return
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 4)
    if b == 1:
        text(ctx, 'center', cx, cy + 34, 22, C['blue'], seg(p, .1, .25), 'c')
        for i in range(8):
            a = -PI / 2 + i * PI / 4
            line(ctx, cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), C['blue'], 3, seg(p, .35 + i * .07, .45 + i * .07))
            if i: text(ctx, 'r', cx + R * .62 * math.cos(a) + 12, cy + R * .62 * math.sin(a) - 6, 24, C['blue'], seg(p, .4 + i * .07, .5 + i * .07), 'c')
        dog(ctx, cx, cy - R, 1.2)
        text(ctx, 'r', cx + 16, cy - R / 2, 34, C['blue'], seg(p, .2, .35))
        label_box(ctx, 'Definition', [('radius r = center to edge', C['blue'])], 860, 120, 380, C['blue'], seg(p, .25, .5), 24)
        return
    # b == 2: diameter
    line(ctx, cx, cy, cx, cy - R, C['blue'], 3); dog(ctx, cx, cy - R, 1.2)
    line(ctx, cx, cy, cx, cy + R, C['blue'], 3, seg(p, 0, .3)); dog(ctx, cx, cy + R, 1.2) if p > .25 else None
    line(ctx, cx, cy - R, cx, cy + R, C['green'], 7, seg(p, .4, .65))
    text(ctx, 'r', cx + 16, cy - R / 2, 30, C['blue'], 1); text(ctx, 'r', cx + 16, cy + R / 2 + 10, 30, C['blue'], seg(p, .3, .4))
    brace_label(ctx, cx - 30, cy + R, cx - 30, cy - R, '', C['green'], seg(p, .55, .75))
    text(ctx, 'd = 2r', cx - 290, cy + 12, 44, C['green'], seg(p, .7, .85), 'c')
    label_box(ctx, 'Definition', [('diameter d = all the way across = 2r', C['green'])], 820, 120, 420, C['green'], seg(p, .6, .85), 22)

def s_circ(ctx, b, p, t):
    chip(ctx, 'Distance around: circumference', C['org'])
    R = 105; cy = 300; x0 = 300; L = 2 * PI * R
    floor = cy + R
    if b == 0:
        k = seg(p, .15, 1); ang = PI / 2 + 2 * PI * k
        arc(ctx, x0, cy, R, 0, 2 * PI, C['ink'], 3)
        arc(ctx, x0, cy, R, PI / 2, PI / 2 + 2 * PI, C['org'], 7, k)
        dog(ctx, x0 + R * math.cos(ang), cy + R * math.sin(ang), 1)
        label_box(ctx, 'Definition', [('circumference C = distance around', C['org'])], 560, 150, 440, C['org'], seg(p, .3, .6), 24)
        return
    line(ctx, x0 - 40, floor, x0 + L + 80, floor, C['grid'], 2)
    th = 2 * PI * (seg(p, .05, .95) if b == 1 else 1)
    wx = x0 + th * R
    line(ctx, x0, floor, wx, floor, C['org'], 7)
    if b == 1 or th < 2 * PI - 1e-3:
        arc(ctx, wx, cy, R, 0, 2 * PI, C['ink'], 2, 1, .5)
        if th < 2 * PI - 1e-3: arc(ctx, wx, cy, R, PI / 2 + th, PI / 2 + 2 * PI, C['org'], 7)
        disc(ctx, wx, cy, 4, C['ink'])
    text(ctx, 'C', x0 + L / 2, floor + 40, 30, C['org'], 1 if b > 1 else seg(p, .9, 1), 'c')
    if b >= 2:
        arc(ctx, x0 + L + R + 40, cy, R, 0, 2 * PI, C['ink'], 2, 1, .45, [6, 6])
        line(ctx, x0 + L + R + 40, cy - R, x0 + L + R + 40, cy + R, C['green'], 6, seg(p, 0, .1) if b == 2 else 1)
        text(ctx, 'd', x0 + L + R + 56, cy + 8, 30, C['green'], seg(p, 0, .1) if b == 2 else 1)
        d = 2 * R; kk = p if b == 2 else 1
        for i in range(3):
            k = seg(kk, .05 + i * .15, .18 + i * .15)
            line(ctx, x0 + i * d + 2, floor - 30, x0 + i * d + d - 2, floor - 30, C['green'], 8, k)
            text(ctx, f'{i + 1} d', x0 + i * d + d / 2, floor - 46, 24, C['green'], k, 'c')
        k = seg(kk, .55, .65)
        line(ctx, x0 + 3 * d, floor - 30, x0 + L, floor - 30, C['yel'], 8, k)
        text(ctx, '+ a bit', x0 + 3 * d + 30, floor - 74, 20, C['yel'], k, 'c')
        text(ctx, 'π ≈ 3.14 diameters', x0 + L / 2, floor + 88, 38, C['yel'], seg(kk, .7, .85), 'c')
    if b >= 3:
        rrect(ctx, 360, 525, 560, 76, 14, fill=C['bg2'], stroke=C['pur'], a=seg(p, 0, .15))
        rich(ctx, [('C = π d', C['pur']), ('   =   ', C['mute']), ('2 π r', C['pur'])], 640, 576, 44, seg(p, .1, .7), 'c')

def wedge_at(ctx, ax, ay, R, phi, half, fill, a=1):
    ctx.move_to(ax, ay); ctx.arc(ax, ay, R, phi - half, phi + half); ctx.close_path()
    col(ctx, fill, a); ctx.fill_preserve(); col(ctx, C['crust']); ctx.set_line_width(2); ctx.stroke()
    col(ctx, C['crust']); ctx.set_line_width(6); ctx.new_sub_path(); ctx.arc(ax, ay, R - 3, phi - half, phi + half); ctx.stroke()
def s_area(ctx, b, p, t):
    chip(ctx, 'Space inside: area', C['pur'])
    cx, cy, R, N = 300, 320, 150, 16; al = 2 * PI / N; w = R * al
    xs, y0 = 640, 210
    k = 0 if b == 0 else (seg(p, .05, .9) if b == 1 else 1)
    if b == 0:
        disc(ctx, cx, cy, R, C['pizza'], seg(p, 0, .2)); arc(ctx, cx, cy, R - 3, 0, 2 * PI, C['crust'], 7, seg(p, 0, .2))
        for i in range(N):
            a = i * al
            line(ctx, cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), C['crust'], 2, seg(p, .3 + i * .035, .36 + i * .035))
        label_box(ctx, 'Definition', [('area A = space inside', C['pur'])], 560, 150, 360, C['pur'], seg(p, .1, .4), 24)
        return
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 2, 1, .25, [6, 6])
    for i in range(N):
        phi0 = i * al + al / 2
        j = i // 2
        if i % 2 == 0: tx, ty, tphi = xs + j * w, y0, PI / 2
        else: tx, ty, tphi = xs + j * w + w / 2, y0 + R, -PI / 2
        d = (tphi - phi0 + PI) % (2 * PI) - PI
        ki = ease(clamp((k - i * .02) / .7))
        wedge_at(ctx, lerp(cx, tx, ki), lerp(cy, ty, ki), R, phi0 + d * ki, al / 2, C['pizza'])
    if b >= 2:
        kk = p if b == 2 else 1
        brace_label(ctx, xs - 34, y0 + R, xs - 34, y0, '', C['blue'], seg(kk, .05, .3))
        text(ctx, 'r', xs - 70, y0 + R / 2 + 12, 40, C['blue'], seg(kk, .2, .35), 'c')
        bx1, bx2 = xs - w / 2, xs + 8 * w - w / 2
        line(ctx, bx1, y0 + R + 30, bx2, y0 + R + 30, C['org'], 3, seg(kk, .4, .7))
        text(ctx, 'half the crust = ½ × 2πr = πr', (bx1 + bx2) / 2, y0 + R + 68, 28, C['org'], seg(kk, .55, .8), 'c')
    if b >= 3:
        rrect(ctx, 520, 470, 640, 84, 14, fill=C['bg2'], stroke=C['pur'], a=seg(p, 0, .15))
        rich(ctx, [('A = ', C['pur']), ('πr', C['org']), (' × ', C['mute']), ('r', C['blue']), ('  =  ', C['mute']), ('πr²', C['pur'])], 840, 526, 46, seg(p, .1, .75), 'c')

def s_twist(ctx, b, p, t):
    chip(ctx, 'Plot twist', C['red'])
    def sq_circle(cx, cy, r, n, k, lab):
        arc(ctx, cx, cy, r, 0, 2 * PI, C['ink'], 3, k)
        line(ctx, cx, cy, cx + r, cy, C['blue'], 4, k)
        text(ctx, lab, cx + r / 2, cy - 12, 24, C['blue'], k, 'c')
        u = r / n
        for i in range(n):
            for j in range(n):
                kk = seg(k, .3 + (i * n + j) * .05, .45 + (i * n + j) * .05)
                if kk > 0: rrect(ctx, cx + i * u + 2, cy - r + j * u + 2, u - 4, u - 4, 4, fill=C['pur'], a=.35 * kk + .1, stroke=C['pur'])
    kb = p if b == 0 else 1
    sq_circle(250, 380, 80, 1, seg(kb, 0, .3), 'r = 1')
    text(ctx, '1 square', 250 + 40, 480, 22, C['pur'], seg(kb, .3, .45), 'c')
    sq_circle(640, 400, 160, 2, seg(kb, .35, .75), 'r = 2')
    text(ctx, 'double r  →  4 squares!', 640, 605, 28, C['yel'], seg(kb, .7, .9), 'c')
    if b >= 1:
        rrect(ctx, 900, 160, 330, 260, 16, fill=C['bg2'], stroke=C['yel'], a=seg(p, 0, .1))
        rich(ctx, [('r × 2 → area × 2² = ', C['ink']), ('4', C['yel'])], 1065, 230, 28, seg(p, .1, .45), 'c')
        rich(ctx, [('r × 3 → area × 3² = ', C['ink']), ('9', C['yel'])], 1065, 300, 28, seg(p, .5, .85), 'c')
        text(ctx, 'because r is SQUARED', 1065, 370, 22, C['red'], seg(p, .2, .4), 'c')

def s_arc(ctx, b, p, t):
    chip(ctx, 'Arcs and sectors = a fraction of the circle', C['green'])
    cx, cy, R = 420, 355, 185
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 3)
    a0, a1 = -PI / 2, -PI / 2 + PI / 3
    kb = p if b == 0 else 1
    k = seg(kb, .2, .5)
    if k > 0: wedge(ctx, cx, cy, R, a0, lerp(a0, a1, k), C['pur'], .45)
    arc(ctx, cx, cy, R, a0, a1, C['org'], 9, seg(kb, .1, .4))
    text(ctx, 'arc = part of the crust', 700, 220, 28, C['org'], seg(kb, .1, .35))
    text(ctx, 'sector = one slice', 700, 270, 28, C['pur'], seg(kb, .35, .6))
    line(ctx, cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), C['ink'], 2, k)
    line(ctx, cx, cy, cx + R * math.cos(a1), cy + R * math.sin(a1), C['ink'], 2, k)
    if b >= 1:
        arc(ctx, cx, cy, 46, a0, a1, C['yel'], 3, seg(p, 0, .2)); text(ctx, '60°', cx + 34, cy - 66, 24, C['yel'], seg(p, .1, .25))
        for i in range(2, 6):
            a = -PI / 2 + i * PI / 3
            line(ctx, cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), C['mute'], 2, seg(p, .2 + i * .06, .3 + i * .06), 1, [6, 6])
        line(ctx, cx, cy, cx + R * math.cos(-PI / 2 + PI / 3 * 1), cy + R * math.sin(-PI / 2 + PI / 3), C['mute'], 2, 1, 1, [6, 6])
        rrect(ctx, 690, 330, 520, 150, 16, fill=C['bg2'], stroke=C['green'], a=seg(p, .3, .4))
        text(ctx, 'FRACTION OF THE CIRCLE', 712, 358, 14, C['green'], seg(p, .3, .4))
        rich(ctx, [('angle', C['yel']), (' ÷ ', C['mute']), ('360', C['ink']), ('  =  ', C['mute']), ('60', C['yel']), (' ÷ ', C['mute']), ('360', C['ink']), (' = ', C['mute']), ('1/6', C['org'])], 950, 410, 30, seg(p, .4, .8), 'c')
        text(ctx, 'a full turn = 360°', 950, 455, 20, C['mute'], seg(p, .7, .9), 'c', False)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'A circle has a radius of 6. A central angle measures 60°. What is the arc length?', 80, 145, 25, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    cx, cy, R = 270, 400, 150
    kb = p if b == 0 else 1
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 3, seg(kb, .3, .6))
    a0, a1 = -PI / 2, -PI / 2 + PI / 3
    line(ctx, cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), C['blue'], 4, seg(kb, .55, .7))
    text(ctx, '6', cx - 20, cy - R / 2, 28, C['blue'], seg(kb, .6, .75))
    line(ctx, cx, cy, cx + R * math.cos(a1), cy + R * math.sin(a1), C['ink'], 3, seg(kb, .65, .8))
    arc(ctx, cx, cy, 40, a0, a1, C['yel'], 3, seg(kb, .75, .9)); text(ctx, '60°', cx + 26, cy - 52, 22, C['yel'], seg(kb, .8, .95))
    rows = [(1, [('Step 1  ', C['mute']), ('fraction = 60 ÷ 360 = ', C['ink']), ('1/6', C['org'])]),
            (2, [('Step 2  ', C['mute']), ('C = 2πr = 2π(6) = ', C['ink']), ('12π', C['org'])]),
            (3, [('Step 3  ', C['mute']), ('arc = ', C['ink']), ('1/6', C['org']), (' × ', C['ink']), ('12π', C['org']), (' = ', C['ink']), ('2π', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 500, 250 + i * 70, 32, seg(p, 0, .7) if b == bb else 1)
    if b >= 2: arc(ctx, cx, cy, R, 0, 2 * PI, C['org'], 3, seg(p, .2, .8) if b == 2 else 1, .5)
    if b >= 3:
        arc(ctx, cx, cy, R, a0, a1, C['green'], 10, seg(p, .5, .8) if b == 3 else 1)
        rrect(ctx, 500, 455, 300, 64, 12, fill=C['bg2'], stroke=C['green'], a=seg(p, .7, .85) if b == 3 else 1)
        text(ctx, 'Answer: 2π', 650, 498, 32, C['green'], seg(p, .75, .9) if b == 3 else 1, 'c')
    if b >= 4:
        rrect(ctx, 830, 440, 400, 110, 12, fill=(0.25, 0.08, 0.08), stroke=C['red'], a=seg(p, 0, .2))
        text(ctx, 'TRAP', 850, 468, 15, C['red'], seg(p, 0, .2))
        text(ctx, 'πr² = 36π is the AREA,', 850, 502, 24, C['ink'], seg(p, .15, .4))
        text(ctx, 'not the arc length ✗', 850, 534, 24, C['red'], seg(p, .35, .6))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    cx, cy, R = 330, 360, 150
    arc(ctx, cx, cy, R, 0, 2 * PI, C['ink'], 4, seg(p, 0, .3) if b == 0 else 1)
    line(ctx, cx, cy, cx + R, cy, C['blue'], 4, seg(p, .2, .4) if b == 0 else 1); text(ctx, 'r = 5', cx + R / 2, cy - 14, 28, C['blue'], 1 if b else seg(p, .3, .45), 'c')
    text(ctx, 'Area = ?', 640, 260, 54, C['ink'], 1 if b else seg(p, .3, .5))
    if b == 0:
        text(ctx, '❚❚  Pause and solve', 640, 340, 30, C['yel'], seg(p, .5, .7))
        if p >= 1:
            rem = max(0, 4 - (t - (t - 0)))  # placeholder; ring drawn by time below
    if b == 1:
        rich(ctx, [('A = πr² = π(5)² = ', C['pur']), ('25π', C['green'])], 640, 360, 44, seg(p, 0, .5))
        rrect(ctx, 640, 420, 520, 90, 12, fill=(0.25, 0.08, 0.08), stroke=C['red'], a=seg(p, .55, .7))
        text(ctx, 'TRAP', 660, 448, 15, C['red'], seg(p, .55, .7))
        text(ctx, '10π = 2π(5) is the circumference ✗', 660, 484, 24, C['ink'], seg(p, .6, .85))

def s_recap(ctx, b, p, t):
    text(ctx, 'Lock it in', 640, 150, 54, C['ink'], seg(p, 0, .1), 'c')
    for i, (n, s, c) in enumerate([('1', 'Find r first', C['blue']), ('2', 'Around:  C = 2πr', C['org']), ('3', 'Inside:  A = πr²', C['pur'])]):
        k = seg(p, .15 + i * .25, .3 + i * .25)
        rrect(ctx, 300, 210 + i * 100, 680, 80, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        disc(ctx, 345, 250 + i * 100, 22, c, k); text(ctx, n, 345, 259 + i * 100, 24, C['bg'], k, 'c')
        text(ctx, s, 390, 262 + i * 100, 36, c, k)

SC = dict(hook=s_hook, leash=s_leash, circ=s_circ, area=s_area, twist=s_twist, arc=s_arc, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['leash'] * 3 + ['circ'] * 4 + ['area'] * 4 + ['twist'] * 2 + ['arc'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
BEATS = list(zip(PLAN, NAR))
if __name__ == '__main__':
    if sys.argv[1:] == ['stills']:
        import cairo
        cnt = {}
        for i, (n, _) in enumerate(BEATS):
            b = cnt.get(n, 0); cnt[n] = b + 1
            for pp in (.5, 1):
                surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); background(ctx); SC[n](ctx, b, pp, 3); caption(ctx, NAR[i][:120])
                surf.write_to_png(f'/home/claude/v2/circ/still_{i:02d}_{int(pp*10)}.png')
    else:
        durs, starts = render(BEATS, SC, sys.argv[1], 'SAT Math · Circles', '/home/claude/v2/circ/wav', pads={21: 5.0, 23: 1.5})
        json.dump(dict(durs=durs, starts=starts), open('/home/claude/v2/circ/timing.json', 'w'))
        thumb(s_hook, 0, '/home/claude/v2/circ/thumb.png')
