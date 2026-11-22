import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/a2'
NAR = json.load(open(f'{D}/beats.json'))

def clue(ctx, x, y, w, s, c, k):
    if k <= 0: return
    rrect(ctx, x, y, w, 70, 12, fill=C['bg2'], stroke=c, a=k, lw=3)
    text(ctx, s, x + w / 2, y + 46, 30, c, k, 'c')
def marbles(ctx, x, y, n, c, k, cols=10, r=11, gap=28):
    for i in range(n):
        kk_ = seg(k, i / max(n, 1) * .8, i / max(n, 1) * .8 + .2)
        if kk_ > 0: disc(ctx, x + (i % cols) * gap, y + (i // cols) * gap, r, c, kk_)

def s_hook(ctx, b, p, t):
    text(ctx, 'Systems of Equations', 100, 230, 66, C['ink'], seg(p, 0, .12))
    text(ctx, 'Two clues. One answer.', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    clue(ctx, 110, 360, 330, 'clue 1:  x + y = 10', C['blue'], seg(p, .25, .4))
    clue(ctx, 110, 450, 330, 'clue 2:  x − y = 4', C['org'], seg(p, .4, .55))
    G = Graph(680, 300, 480, 300, (0, 12), (-2, 11)); G.axes(ctx, seg(p, .3, .45))
    G.plot(ctx, lambda x: 10 - x, C['blue'], 4, seg(p, .4, .7)); G.plot(ctx, lambda x: x - 4, C['org'], 4, seg(p, .55, .85))
    G.dot(ctx, 7, 3, C['yel'], seg(p, .85, 1), 10); text(ctx, '(7, 3)', G.X(7) - 38, G.Y(3) - 60, 26, C['yel'], seg(p, .85, 1))

def s_graph(ctx, b, p, t):
    chip(ctx, 'The answer = where the lines cross', C['yel'])
    G = Graph(200, 130, 520, 450, (0, 12), (-2, 11)); G.axes(ctx, 1)
    G.plot(ctx, lambda x: 10 - x, C['blue'], 4, seg(p, 0, .3)); G.plot(ctx, lambda x: x - 4, C['org'], 4, seg(p, .2, .5))
    G.dot(ctx, 7, 3, C['yel'], seg(p, .55, .7), 11)
    text(ctx, 'x + y = 10', G.X(1.2), G.Y(9.6), 24, C['blue'], seg(p, .1, .3)); text(ctx, 'x − y = 4', G.X(9.6), G.Y(4.2), 24, C['org'], seg(p, .3, .5))
    rich(ctx, [('(7, 3)', C['yel'])], 800, 280, 48, seg(p, .6, .75))
    rich(ctx, [('7 + 3 = 10 ✓', C['blue'])], 800, 350, 32, seg(p, .7, .85)); rich(ctx, [('7 − 3 = 4 ✓', C['org'])], 800, 400, 32, seg(p, .8, .95))
    text(ctx, 'makes BOTH true', 800, 460, 30, C['green'], seg(p, .85, 1))

def s_words(ctx, b, p, t):
    chip(ctx, 'Word problems → two equations', C['blue'])
    if b == 0:
        clue(ctx, 180, 220, 400, 'HOW MANY  (count)', C['blue'], seg(p, .2, .45))
        clue(ctx, 700, 220, 400, 'HOW MUCH  ($, weight)', C['green'], seg(p, .45, .7))
        text(ctx, 'tickets, people, items', 380, 340, 24, C['mute'], seg(p, .35, .55), 'c', False); text(ctx, 'total cost, total weight', 900, 340, 24, C['mute'], seg(p, .6, .8), 'c', False)
        return
    text(ctx, '"4 times as many blue as red"', 640, 180, 36, C['ink'], 1 if b > 1 else seg(p, 0, .3), 'c')
    rich(ctx, [('b', C['blue']), (' = 4', C['ink']), ('r', C['red'])], 640, 250, 48, 1 if b > 1 else seg(p, .35, .7), 'c')
    marbles(ctx, 120, 320, 7, C['red'], 1 if b > 1 else seg(p, .5, .8), 7)
    marbles(ctx, 380, 320, 28, C['blue'], 1 if b > 1 else seg(p, .6, 1), 14)
    if b >= 2:
        rich(ctx, [('4r + r = 35  →  5r = 35  →  ', C['ink']), ('r = 7', C['red']), (',  ', C['ink']), ('b = 28', C['blue'])], 640, 470, 32, kk(b, 2, p, 0, .7), 'c')
    if b >= 3: trap(ctx, 340, 495, 600, '7 is RED. They asked for blue.', 'Answer what they asked for ✗', p)

def s_elim(ctx, b, p, t):
    chip(ctx, 'Elimination: add to cancel', C['org'])
    text(ctx, 'x + y = 10', 640, 220, 48, C['ink'], 1 if b else seg(p, 0, .2), 'c')
    text(ctx, 'x − y = 4', 640, 290, 48, C['ink'], 1 if b else seg(p, .1, .3), 'c')
    line(ctx, 480, 320, 800, 320, C['ink'], 3, 1 if b else seg(p, .35, .5))
    if b == 0:
        k = seg(p, .5, .75)
        line(ctx, 606, 228, 646, 188, C['red'], 4, k); line(ctx, 606, 298, 646, 258, C['red'], 4, k)
        text(ctx, '+y and −y cancel', 900, 260, 28, C['red'], k); return
    rich(ctx, [('2x = 14', C['ink'])], 640, 380, 48, seg(p, 0, .3), 'c')
    rich(ctx, [('x = 7', C['green']), (',  ', C['ink']), ('y = 3', C['blue'])], 640, 460, 48, seg(p, .35, .8), 'c')

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 100, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, 'Adult tickets cost $12 and child tickets cost $8. Twenty tickets were sold for $200.', 80, 140, 23, C['ink'], seg(p, 0, .5) if b == 0 else 1)
    write(ctx, 'How many adult tickets were sold?', 80, 178, 23, C['yel'], seg(p, .4, .7) if b == 0 else 1)
    rows = [(1, [('Step 1  how many:  ', C['mute']), ('a + c = 20', C['blue']), ('  →  c = 20 − a', C['ink'])]),
            (2, [('Step 2  how much:  ', C['mute']), ('12a + 8c = 200', C['green'])]),
            (3, [('Step 3  ', C['mute']), ('12a + 8(20 − a) = 200  →  4a + 160 = 200  →  ', C['ink']), ('a = 10', C['yel'])])]
    for i, (bb, parts) in enumerate(rows):
        if b >= bb: rich(ctx, parts, 80, 270 + i * 66, 28, kk(b, bb, p, 0, .7))
    if b >= 4:
        rich(ctx, [('check: 10 × $12 = $120,  10 × $8 = $80,  total ', C['mute']), ('$200 ✓', C['green'])], 80, 480, 26, seg(p, 0, .7))
        answer(ctx, 'Answer: 10 adult tickets', 80, 510, 400, seg(p, .6, .9))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    write(ctx, 'x + y = 10   and   x − y = 4', 120, 230, 44, C['ink'], seg(p, 0, .4) if b == 0 else 1)
    write(ctx, 'What is y?', 120, 290, 34, C['yel'], seg(p, .3, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and solve', 120, 380, 34, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('add: 2x = 14  →  x = 7', C['ink'])], 120, 370, 34, seg(p, 0, .3))
    rich(ctx, [('7 + y = 10  →  ', C['ink']), ('y = 3', C['green'])], 120, 425, 38, seg(p, .25, .5))
    trap(ctx, 120, 455, 560, 'Said 7? That\'s x.', 'Read what they asked for ✗', seg(p, .6, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('The answer makes BOTH equations true', C['yel']), ('One equation counts, one totals', C['blue']), ('Answer exactly what they asked for', C['green'])])

SC = dict(hook=s_hook, graph=s_graph, words=s_words, elim=s_elim, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'graph'] + ['words'] * 4 + ['elim'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: two clues', graph='Where the lines cross', words='Words to equations', elim='Elimination', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Math · Systems', s_hook, {13: 5.0, 15: 1.5}, CH)
