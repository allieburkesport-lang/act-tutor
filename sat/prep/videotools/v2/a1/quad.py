import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a1'
NAR = json.load(open(f'{D}/beats.json'))

def s_hook(ctx, b, p, t):
    text(ctx, 'Quadratics', 100, 230, 80, C['ink'], seg(p, 0, .12))
    text(ctx, 'Pick the form that shows what you need.', 102, 290, 28, C['mute'], seg(p, .1, .3), bold=False)
    G = Graph(700, 120, 480, 440, (-4, 6), (-5, 9)); G.axes(ctx, seg(p, .2, .35))
    G.plot(ctx, lambda x: (x - 1) ** 2 - 4, C['pur'], 5, seg(p, .3, .75))
    G.dot(ctx, 1, -4, C['yel'], seg(p, .7, .85)); G.dot(ctx, -1, 0, C['green'], seg(p, .75, .9)); G.dot(ctx, 3, 0, C['green'], seg(p, .75, .9)); G.dot(ctx, 0, -3, C['blue'], seg(p, .8, .95))
    for i, (s, c) in enumerate([('zeros', C['green']), ('vertex', C['yel']), ('y-intercept', C['blue'])]):
        text(ctx, '• ' + s, 110, 380 + i * 52, 34, c, seg(p, .6 + i * .1, .75 + i * .1))

def s_ball(ctx, b, p, t):
    chip(ctx, 'The path of a thrown ball', C['org'])
    G = Graph(140, 110, 1000, 430, (-1, 9), (-1, 6))
    line(ctx, 100, G.Y(0), 1180, G.Y(0), C['green'], 4)  # ground
    f = lambda x: -0.3 * (x - 4) ** 2 + 4.8
    k = seg(p, 0, .5); G.plot(ctx, f, C['org'], 4, k)
    x = lerp(0, 8, k); disc(ctx, G.X(x), G.Y(max(0, f(x))), 16, C['org'])
    G.dot(ctx, 4, 4.8, C['yel'], seg(p, .5, .65), 10); text(ctx, 'vertex (top point)', G.X(4), G.Y(4.8) - 26, 26, C['yel'], seg(p, .5, .65), 'c')
    for z in (0, 8): G.dot(ctx, z, 0, C['green'], seg(p, .7, .85), 10)
    text(ctx, 'zero', G.X(0), G.Y(0) + 40, 26, C['green'], seg(p, .75, .9), 'c'); text(ctx, 'zero', G.X(8), G.Y(0) + 40, 26, C['green'], seg(p, .75, .9), 'c')

def form_card(ctx, i, k, hl=False):
    names = [('STANDARD', 'y = ax² + bx + c', 'shows the y-intercept', C['blue']),
             ('FACTORED', 'y = a(x − p)(x − q)', 'shows the zeros', C['green']),
             ('VERTEX', 'y = a(x − h)² + k', 'shows the vertex', C['yel'])]
    lab, f, sh, c = names[i]; y = 130 + i * 150
    rrect(ctx, 60, y, 520, 128, 16, fill=C['bg2'], stroke=c, a=k, lw=5 if hl else 2)
    text(ctx, lab, 84, y + 30, 16, c, k); text(ctx, f, 84, y + 76, 34, C['ink'], k); text(ctx, sh, 84, y + 110, 22, c, k, 'l', False)
def s_forms(ctx, b, p, t):
    chip(ctx, 'Three forms, three camera angles', C['pur'])
    for i in range(3):
        k = seg(p, .15 + i * .25, .35 + i * .25) if b == 0 else 1
        form_card(ctx, i, k, hl=(b == 1 and i == 0) or (b in (2, 3) and i == 1) or (b in (4, 5) and i == 2))
    if b == 0: return
    G = Graph(660, 120, 540, 300, (-3, 9), (-3, 12))
    if b == 1:
        G.axes(ctx, 1, 0); G.plot(ctx, lambda x: x * x - 6 * x + 8, C['blue'], 4, seg(p, 0, .4))
        text(ctx, 'y = x² − 6x + 8', 690, 480, 30, C['ink'], seg(p, .1, .3))
        G.dot(ctx, 0, 8, C['blue'], seg(p, .5, .7)); text(ctx, '(0, 8)', G.X(0) - 14, G.Y(8), 26, C['blue'], seg(p, .55, .75), 'r')
        rich(ctx, [('x = 0  →  y = ', C['ink']), ('8', C['blue']), (' = c', C['mute'])], 690, 530, 30, seg(p, .65, .9))
        return
    if b in (2, 3):
        f = lambda x: 2 * (x - 3) * (x + 5) / 2.2
        G = Graph(660, 120, 540, 280, (-7, 6), (-18, 10)); G.axes(ctx, 1, 0); G.plot(ctx, f, C['green'], 4, seg(p, 0, .4) if b == 2 else 1)
        text(ctx, 'y = 2(x − 3)(x + 5)', 690, 430, 30, C['ink'], kk(b, 2, p, 0, .3))
        G.dot(ctx, 3, 0, C['green'], kk(b, 2, p, .5, .7)); G.dot(ctx, -5, 0, C['green'], kk(b, 2, p, .55, .75))
        text(ctx, '3', G.X(3), G.Y(0) - 18, 28, C['green'], kk(b, 2, p, .55, .75), 'c'); text(ctx, '−5', G.X(-5), G.Y(0) - 18, 28, C['green'], kk(b, 2, p, .6, .8), 'c')
        if b == 3:
            rich(ctx, [('x − 3', C['ink']), ('  →  ', C['mute']), ('+3', C['green'])], 690, 480, 32, seg(p, 0, .35))
            rich(ctx, [('x + 5', C['ink']), ('  →  ', C['mute']), ('−5', C['green'])], 690, 530, 32, seg(p, .3, .6))
            text(ctx, 'signs flip!', 1010, 505, 30, C['red'], seg(p, .65, .85))
        return
    # b in (4,5): vertex form
    G = Graph(660, 120, 540, 280, (-2, 9), (-2, 20)); G.axes(ctx, 1, 0)
    G.plot(ctx, lambda x: (x - 4) ** 2 + 7, C['yel'], 4, seg(p, 0, .4) if b == 4 else 1)
    text(ctx, 'y = (x − 4)² + 7', 690, 440, 30, C['ink'], kk(b, 4, p, 0, .3))
    G.dot(ctx, 4, 7, C['yel'], kk(b, 4, p, .5, .7)); text(ctx, '(4, 7)', G.X(4) + 16, G.Y(7) + 34, 28, C['yel'], kk(b, 4, p, .55, .75))
    if b == 4: rich(ctx, [('h = ', C['ink']), ('+4', C['yel']), ('  (sign flips)   k = ', C['ink']), ('7', C['yel'])], 690, 530, 26, seg(p, .65, .9))
    if b == 5:
        rrect(ctx, 690, 470, 490, 76, 14, fill=C['bg2'], stroke=C['yel'], a=seg(p, .1, .3), lw=3)
        rich(ctx, [('standard form vertex:  x = ', C['ink']), ('−b / 2a', C['yel'])], 710, 520, 28, seg(p, .2, .6))

def s_light(ctx, b, p, t):
    chip(ctx, 'How many solutions? b² − 4ac', C['red'])
    text(ctx, 'b² − 4ac', 300, 220, 64, C['ink'], seg(p, 0, .3) if b == 0 else 1, 'c')
    rrect(ctx, 220, 260, 160, 360, 30, fill=(0.08, 0.08, 0.1), stroke=C['mute'], a=seg(p, .3, .5) if b == 0 else 1)
    lights = [(C['green'], 'positive', '2 solutions'), (C['yel'], 'zero', '1 solution'), (C['red'], 'negative', '0 solutions')]
    G = [Graph(560, 140 + i * 170, 220, 140, (-3, 3), (-3, 5)) for i in range(3)]
    fs = [lambda x: x * x - 2, lambda x: x * x, lambda x: x * x + 1.5]
    for i, (c, s, n) in enumerate(lights):
        on = 0 if b == 0 else seg(p, .1 + i * .28, .25 + i * .28)
        disc(ctx, 300, 320 + i * 110, 42, c, .25 + .75 * on if b else .25 * (seg(p, .3, .5)))
        if b:
            G[i].axes(ctx, on, 0); G[i].plot(ctx, fs[i], c, 3, on)
            text(ctx, s, 820, 205 + i * 170, 30, c, on); text(ctx, n, 820, 245 + i * 170, 30, C['ink'], on)

def s_sat(ctx, b, p, t):
    question(ctx, 'How many real solutions does  x² + 4x + 5 = 0  have?', seg(p, 0, .5) if b == 0 else 1, 26)
    rows = [(1, [('Step 1  ', C['mute']), ('a = 1,  b = 4,  c = 5', C['ink'])]),
            (2, [('Step 2  ', C['mute']), ('4² − 4(1)(5) = 16 − 20 = ', C['ink']), ('−4', C['red'])]),
            (3, [('Step 3  ', C['mute']), ('negative  →  ', C['ink']), ('0 real solutions', C['green'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 80, 250 + i * 70, 32, kk(b, bb, p, 0, .6))
    G = Graph(800, 200, 380, 300, (-5, 2), (-2, 8))
    if b >= 3:
        G.axes(ctx, kk(b, 3, p, .2, .4)); G.plot(ctx, lambda x: x * x + 4 * x + 5, C['pur'], 4, kk(b, 3, p, .3, .8))
        text(ctx, 'Desmos: never touches the x-axis', 990, 530, 20, C['mute'], kk(b, 3, p, .6, .9), 'c', False)
        answer(ctx, 'Answer: 0', 80, 470, 260, kk(b, 3, p, .7, .9))
    if b >= 4: trap(ctx, 360, 455, 420, 'Not every quadratic has 2 answers.', 'Check the sign first ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'y = 2x² − 12x + 1', 120, 230, 48, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'What is the x-coordinate of the vertex?', 120, 290, 30, C['ink'], seg(p, .2, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('x = −b / 2a = −(−12) / (2·2) = 12 / 4 = ', C['ink']), ('3', C['green'])], 120, 380, 34, seg(p, 0, .4))
    trap(ctx, 120, 420, 640, 'Got −3? The double negative: −(−12) = +12', 'Watch the signs ✗', seg(p, .5, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Factored → zeros (signs flip)', C['green']), ('Vertex form → vertex (h, k)', C['yel']), ('b² − 4ac counts the solutions', C['red'])])

SC = dict(hook=s_hook, ball=s_ball, forms=s_forms, light=s_light, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'ball'] + ['forms'] * 6 + ['light'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea', ball='Parabola: vertex and zeros', forms='Three forms', light='Discriminant: traffic light', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Quadratics', s_hook, {15: 5.0, 17: 1.5}, CH)
