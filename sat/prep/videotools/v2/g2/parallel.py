import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/g2'
NAR = json.load(open(f'{D}/beats.json'))

def items(ctx, lead, its, tail, y, k, bad=None, size=30, x=80, form=None):
    """lead text, list items (each boxed), tail; bad = index of mismatched item"""
    if k <= 0: return
    text(ctx, lead, x, y, size, C['ink'], k, 'l', False); xx = x + twidth(ctx, lead, size, False) + 12
    for i, s in enumerate(its):
        kk_ = seg(k, i * .2, i * .2 + .4)
        c = C['red'] if bad == i else C['green']
        w = twidth(ctx, s, size)
        rrect(ctx, xx - 6, y - size - 4, w + 12, size + 16, 8, stroke=c, a=kk_, lw=3); text(ctx, s, xx, y, size, c, kk_)
        xx += w + 16
        if i < len(its) - 1:
            sep = ', and' if i == len(its) - 2 and len(its) > 2 else (',' if len(its) > 2 else '')
            if sep: text(ctx, sep, xx - 6, y, size, C['ink'], kk_, 'l', False); xx += twidth(ctx, sep, size, False) + 6
    if tail: text(ctx, tail, xx, y, size, C['ink'], k, 'l', False)
    if form: text(ctx, form, x, y + 50, 24, C['yel'], k, 'l', False)

def s_hook(ctx, b, p, t):
    text(ctx, 'Lists & Pairs Match', 100, 200, 66, C['ink'], seg(p, 0, .12))
    text(ctx, 'Same form for every item', 102, 260, 30, C['mute'], seg(p, .1, .3), bold=False)
    for i, f in enumerate(['-ing', '-ing', '-ing']):
        k = seg(p, .35 + i * .12, .5 + i * .12)
        rrect(ctx, 120 + i * 220, 360, 190, 110, 16, fill=C['bg2'], stroke=C['green'], a=k, lw=3); text(ctx, f, 215 + i * 220, 432, 44, C['green'], k, 'c')
    k = seg(p, .75, .9)
    rrect(ctx, 800, 360, 190, 110, 16, fill=C['bg2'], stroke=C['red'], a=k, lw=3); text(ctx, 'to + verb', 895, 428, 32, C['red'], k, 'c')
    text(ctx, '✗', 895, 530, 50, C['red'], k, 'c')

def s_domino(ctx, b, p, t):
    chip(ctx, 'Matching dominoes', C['blue'])
    for i in range(6):
        k = seg(p, i * .08, i * .08 + .2); x = 160 + i * 160
        if i == 4: rrect(ctx, x, 260, 110, 110, 14, fill=C['red'], a=k)
        else: rrect(ctx, x + 25, 200, 60, 170, 10, fill=C['blue'], a=k)
    text(ctx, 'one different shape breaks the row', 640, 480, 32, C['red'], seg(p, .6, .85), 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Find the other items', C['blue']), ('Check their form', C['yel']), ('Make the blank match', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_ing(ctx, b, p, t):
    chip(ctx, '-ing list', C['green'])
    items(ctx, 'spent days', ['measuring', 'photographing', 'sampling'], 'the coral.', 230, 1 if b else seg(p, 0, .7), form='all -ing ✓')
    if b: items(ctx, 'spent days', ['measuring', 'photographing', 'to sample'], '', 400, seg(p, 0, .4), 2, form='breaks the pattern ✗')

def s_more(ctx, b, p, t):
    chip(ctx, 'Plain verbs and nouns', C['blue'])
    items(ctx, 'told the hikers to', ['stretch', 'drink', 'rest'], '', 220, 1 if b else seg(p, .1, .6), form='one "to" covers all: plain verbs ✓')
    if b:
        items(ctx, 'needed', ['soil', 'seeds', 'a light source'], '', 380, seg(p, 0, .4), form='all things ✓')
        text(ctx, '"lighting the plants" = an action in a list of things ✗', 80, 500, 26, C['red'], seg(p, .55, .85), 'l', False)

def s_pairs(ctx, b, p, t):
    chip(ctx, 'Pairs count too', C['org'])
    for i, (a, c_) in enumerate([('not only', 'but also'), ('both', 'and'), ('either', 'or')]):
        k = seg(p, .1 + i * .2, .3 + i * .2)
        text(ctx, a + '  ___', 200, 220 + i * 90, 36, C['org'], k); text(ctx, c_ + '  ___', 640, 220 + i * 90, 36, C['org'], k)
    text(ctx, 'the two blanks must match', 640, 520, 32, C['yel'], seg(p, .75, .95), 'c')

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('The new library is not only larger but also', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 80, 110, 1120, 30, seg(p, 0, .4))
        choices(ctx, ['quieter', 'it is quieter'], 80, 260, 400, seg(p, .5, .9)); return
    items(ctx, 'not only', ['larger'], '', 230, 1, form=None); items(ctx, 'but also', ['quieter'], '', 230, 1, x=500)
    text(ctx, 'both describing words ✓', 80, 290, 28, C['green'], 1 if b == 2 else seg(p, .4, .7))
    if b == 2:
        items(ctx, 'but also', ['it is quieter'], '', 400, seg(p, 0, .3), 0, x=80)
        trap(ctx, 520, 360, 600, '"it is quieter" adds a new sentence part.', 'Doesn\'t match "larger" ✗', seg(p, .3, .8))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('She enjoys hiking, swimming, and', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [('to read', C['ink']), ('     or     ', C['mute']), ('reading', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    items(ctx, 'enjoys', ['hiking', 'swimming', 'reading'], '', 330, seg(p, 0, .6), form='all -ing ✓')

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Find the other items', C['blue']), ('Check their form', C['yel']), ('Make the blank match', C['green'])])

SC = dict(hook=s_hook, domino=s_domino, method=s_method, ing=s_ing, more=s_more, pairs=s_pairs, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'domino', 'method', 'ing', 'ing', 'more', 'more', 'pairs', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', domino='Matching shapes', method='The method', ing='-ing lists', more='Verbs and nouns', pairs='Pairs', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Parallel lists', s_hook, {11: 5.0, 13: 1.5}, CH)
