import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/r6'
NAR = json.load(open(f'{D}/beats.json'))

def goal(ctx, s, k, y=110):
    if k <= 0: return
    rrect(ctx, 80, y, 1120, 70, 14, fill=C['bg2'], stroke=C['yel'], a=k, lw=3)
    text(ctx, 'GOAL', 100, y + 44, 22, C['yel'], k); text(ctx, s, 190, y + 46, 32, C['ink'], k)
    line(ctx, 190, y + 54, 190 + twidth(ctx, s, 32), y + 54, C['yel'], 3, seg(k, .5, 1))
def opt(ctx, s, y, k, ok=None, tag='', size=25):
    if k <= 0: return
    c = C['green'] if ok else C['red'] if ok is False else C['mute']
    w = max(860, twidth(ctx, s, size, False) + 44)
    rrect(ctx, 80, y, w, 64, 12, fill=C['bg2'], stroke=c, a=k, lw=3 if ok is not None else 1)
    text(ctx, s, 100, y + 42, size, C['green'] if ok else C['ink'], k, 'l', False)
    if tag: text(ctx, tag, 100 + w, y + 42, 24, c, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Notes Questions', 100, 210, 66, C['ink'], seg(p, 0, .12))
    text(ctx, 'Do EXACTLY the goal', 102, 270, 32, C['yel'], seg(p, .1, .3))
    k = seg(p, .25, .45)
    rrect(ctx, 100, 320, 460, 260, 14, fill=C['bg2'], stroke=C['mute'], a=k, lw=1)
    text(ctx, 'NOTES', 124, 356, 18, C['mute'], k)
    for i in range(4): text(ctx, '•', 124, 400 + i * 44, 26, C['mute'], k); rrect(ctx, 150, 386 + i * 44, [360, 300, 340, 260][i], 14, 7, fill=C['mute'], a=.4 * k)
    for i in range(4):
        kk_ = seg(p, .5 + i * .1, .62 + i * .1)
        rrect(ctx, 640, 330 + i * 64, 520, 52, 10, fill=C['bg2'], stroke=C['green'] if i == 2 else C['mute'], a=kk_, lw=3 if i == 2 else 1)
        text(ctx, 'true ✓' if i != 2 else 'true ✓  + does the goal', 660, 364 + i * 64, 22, C['green'] if i == 2 else C['mute'], kk_, 'l', False)

def s_order(ctx, b, p, t):
    chip(ctx, 'Like a restaurant order', C['blue'])
    rrect(ctx, 160, 200, 380, 120, 16, fill=C['bg2'], stroke=C['yel'], a=seg(p, 0, .3), lw=3)
    text(ctx, 'ORDER:  pizza', 350, 274, 40, C['yel'], seg(p, 0, .3), 'c')
    rrect(ctx, 700, 200, 420, 120, 16, fill=C['bg2'], stroke=C['red'], a=seg(p, .4, .7), lw=3)
    text(ctx, 'a perfect salad', 910, 274, 36, C['ink'], seg(p, .4, .7), 'c')
    text(ctx, 'great food, WRONG order ✗', 910, 380, 30, C['red'], seg(p, .65, .9), 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Skip the notes at first', C['mute']), ('Underline the goal', C['yel']), ('Each choice: does it DO that goal?', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_age(ctx, b, p, t):
    chip(ctx, 'Emphasize something', C['green'])
    goal(ctx, "emphasize the library's age", 1 if b else seg(p, 0, .3))
    opt(ctx, 'Founded in 1800, it is the oldest federal cultural institution.', 230, 1 if b else seg(p, .3, .6), True, 'AGE ✓')
    if b: opt(ctx, 'It holds more than 170 million items.', 320, seg(p, .1, .4), False, 'SIZE, not age')

def s_num(ctx, b, p, t):
    chip(ctx, 'Specify a number', C['purple'] if 'purple' in C else C['blue'])
    goal(ctx, 'specify the number of faces', 1 if b else seg(p, 0, .3))
    opt(ctx, 'A regular octahedron has eight triangular faces.', 230, 1 if b else seg(p, .3, .6), True, 'NUMBER ✓')
    if b: opt(ctx, 'It has fewer faces than a dodecahedron.', 320, seg(p, .1, .4), False, 'comparison')

def s_simdiff(ctx, b, p, t):
    chip(ctx, 'Similarity vs. difference', C['blue'])
    if b == 0:
        goal(ctx, 'emphasize a similarity', seg(p, 0, .25))
        passage(ctx, [('Like bats,', C['green'], 'hl'), ('dolphins find food by using echoes.', None, None)], 80, 220, 1120, 32, seg(p, .3, .6))
        text(ctx, '"like" = alike', 100, 400, 34, C['green'], seg(p, .65, .9)); return
    goal(ctx, 'emphasize a difference', seg(p, 0, .2))
    passage(ctx, [('Venus reaches about 465°C,', None, None), ('while', C['green'], 'hl'), ('Earth averages about 15°C.', None, None)], 80, 220, 1120, 32, seg(p, .15, .45))
    text(ctx, 'two things compared ✓', 100, 400, 32, C['green'], seg(p, .4, .6))
    opt(ctx, 'Venus is the hottest planet.', 440, seg(p, .7, .9), False, 'only ONE thing')

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    goal(ctx, 'introduce Mary Anning to a new audience', 1 if b else seg(p, 0, .4))
    A = 'Mary Anning, a self-taught English fossil hunter, found the first ichthyosaur skeleton.'
    B = 'Mary Anning found the first ichthyosaur skeleton.'
    if b >= 1:
        opt(ctx, A, 230, 1 if b > 1 else seg(p, 0, .3), True, '', 22)
        if b == 1: passage(ctx, [('a self-taught English fossil hunter', C['green'], 'hl')], 80, 330, 620, 28, seg(p, .4, .7))
        if b == 1: text(ctx, '= tells a stranger who she is', 100, 460, 28, C['green'], seg(p, .6, .9))
    if b >= 2:
        opt(ctx, B, 320, seg(p, 0, .3), False, 'no intro')
        trap(ctx, 80, 420, 640, 'True, but assumes you know her.', 'New audience needs an intro ✗', seg(p, .4, .9))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    goal(ctx, "explain the study's outcome", 1 if b else seg(p, 0, .3))
    opt(ctx, 'A   Researchers turned to gene therapy.', 230, 1 if b else seg(p, .3, .5), False if b else None, 'only what they TRIED' if b else '')
    opt(ctx, 'B   Researchers arrived at a treatment that could restore smell.', 320, 1 if b else seg(p, .45, .65), True if b else None, 'OUTCOME ✓' if b else '', 23)
    if b == 0: text(ctx, '⏸  Pause and pick', 100, 470, 34, C['yel'], seg(p, .8, .95))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Underline the goal first', C['yel']), ('All choices are true. Not enough.', C['red']), ('Pick the one that DOES the goal', C['green'])])

SC = dict(hook=s_hook, order=s_order, method=s_method, age=s_age, num=s_num, simdiff=s_simdiff, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'order', 'method', 'age', 'age', 'num', 'num', 'simdiff', 'simdiff', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', order='Do the order', method='The method', age='Emphasize', num='Specify a number', simdiff='Similarity vs. difference', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Notes questions', s_hook, {12: 5.0, 14: 1.5}, CH)
