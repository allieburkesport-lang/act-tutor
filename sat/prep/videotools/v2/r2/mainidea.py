import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/r2'
NAR = json.load(open(f'{D}/beats.json'))

def five(ctx, s, x, y, k):
    if k <= 0: return
    rrect(ctx, x, y, twidth(ctx, s, 32) + 200, 64, 32, fill=C['bg2'], stroke=C['yel'], a=k, lw=3)
    text(ctx, '5 words:', x + 22, y + 42, 22, C['mute'], k, 'l', False); text(ctx, s, x + 130, y + 43, 32, C['yel'], k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Main Idea', 100, 220, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'The point of the WHOLE text', 102, 280, 30, C['mute'], seg(p, .1, .3), bold=False)
    # puzzle: 4 pieces making one picture
    for i in range(4):
        k = seg(p, .3 + i * .1, .45 + i * .1); x = 760 + (i % 2) * 170; y = 180 + (i // 2) * 170
        rrect(ctx, x, y, 160, 160, 14, fill=C['bg2'], stroke=C['blue'], a=k, lw=3); text(ctx, 'detail', x + 80, y + 90, 22, C['mute'], k, 'c', False)
    k = seg(p, .75, .95)
    rrect(ctx, 750, 170, 350, 350, 20, stroke=C['yel'], a=k, lw=5); text(ctx, 'MAIN IDEA', 925, 560, 32, C['yel'], k, 'c')

def s_headline(ctx, b, p, t):
    chip(ctx, 'Main idea = the headline', C['blue'])
    k = seg(p, 0, .3)
    rrect(ctx, 260, 140, 760, 400, 16, fill=C['bg2'], stroke=C['mute'], a=k, lw=1)
    rrect(ctx, 290, 170, 700, 80, 10, stroke=C['yel'], a=seg(p, .2, .45), lw=4)
    text(ctx, 'HEADLINE', 640, 222, 40, C['yel'], seg(p, .2, .45), 'c')
    for i in range(5): rrect(ctx, 300, 280 + i * 44, [660, 600, 680, 540, 620][i], 16, 8, fill=C['mute'], a=.4 * k)
    k2 = seg(p, .55, .8)
    rrect(ctx, 296, 362, 610, 26, 8, stroke=C['red'], a=k2, lw=3); text(ctx, 'one detail ≠ main idea', 640, 585, 28, C['red'], k2, 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    if b == 0:
        five(ctx, 'the point of the whole text', 200, 220, seg(p, .1, .4))
        text(ctx, 'BEFORE you look at the choices', 200, 360, 32, C['ink'], seg(p, .45, .75)); return
    for i, (a, d, c) in enumerate([('Too small', 'just one detail', C['org']), ('Too extreme', 'goes further than the text', C['red']), ('Never said', 'not in the text at all', C['mute'])]):
        k = seg(p, .1 + i * .25, .3 + i * .25)
        rrect(ctx, 160, 170 + i * 120, 960, 90, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, '✗  ' + a, 200, 228 + i * 120, 34, c, k); text(ctx, d, 600, 228 + i * 120, 30, C['ink'], k, 'l', False)

def s_turn_words(ctx, b, p, t):
    chip(ctx, 'Watch for the turn', C['green'])
    for i, w_ in enumerate(['However,', 'But', 'A new study']):
        k = seg(p, .1 + i * .2, .3 + i * .2)
        rrect(ctx, 140 + i * 340, 230, 300, 90, 45, fill=C['bg2'], stroke=C['green'], a=k, lw=3); text(ctx, w_, 290 + i * 340, 287, 34, C['green'], k, 'c')
    text(ctx, '↓  main idea usually comes next', 640, 420, 34, C['yel'], seg(p, .7, .9), 'c')

def s_cave(ctx, b, p, t):
    chip(ctx, 'Old belief → new finding', C['blue'])
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('People thought the cave\'s humming was random.', None, None), ('However, a study found', C['green'], hl), ('that wind blowing through one opening causes it.', None, None)], 100, 140, 1080, 32, 1 if b else seg(p, 0, .5))
    if b >= 1: five(ctx, "wind causes the cave's hum", 100, 330, 1 if b > 1 else seg(p, .3, .6))
    if b == 2:
        rrect(ctx, 100, 430, 640, 60, 10, fill=C['bg2'], stroke=C['red'], a=seg(p, 0, .3), lw=2)
        text(ctx, 'Visitors have always feared the cave.', 120, 470, 26, C['ink'], seg(p, 0, .3), 'l', False)
        line(ctx, 115, 462, 560, 462, C['red'], 3, seg(p, .3, .5))
        text(ctx, 'NEVER SAID', 780, 470, 32, C['red'], seg(p, .35, .55))

def s_herbal(ctx, b, p, t):
    chip(ctx, '"Some think X. However, Y."', C['blue'])
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('Earlier historians saw an old herbal book as a simple guide.', None, None), ('However, one historian sees it as both practical and moral.', C['green'], hl)], 100, 140, 1080, 32, 1 if b else seg(p, 0, .5))
    if b == 1:
        five(ctx, 'more than a simple guide', 100, 330, seg(p, .05, .35))
        trap(ctx, 100, 430, 640, '"Earlier historians were right"', 'Picks the setup, not the point ✗', seg(p, .55, 1))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('Monarch butterflies fly 3,000 miles each fall.', None, None), ('No single butterfly makes the whole round trip; it takes several generations.', C['green'], hl)], 80, 100, 1120, 28, 1 if b else seg(p, 0, .5))
    if b >= 1: five(ctx, 'the trip takes generations', 80, 230, 1 if b > 1 else seg(p, 0, .4))
    opts = ['Monarchs prefer warm weather.', 'The migration takes several generations.', 'Each monarch flies 3,000 miles twice.', 'Monarchs are the fastest butterflies.']
    choices(ctx, opts, 80, 320, 720, 1 if b >= 1 else 0 if b == 0 else 1, 1 if b == 2 else None, (2,) if b == 2 else (), 24, 58)
    if b == 2: text(ctx, 'C contradicts the text', 830, 470, 26, C['red'], seg(p, .3, .6))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('The first gummy candies looked very different. Changes over time helped them evolve into today\'s form.', None, None)], 100, 150, 1080, 32, 1 if b else seg(p, 0, .5))
    if b == 0:
        text(ctx, '⏸  Pause. Main idea in 5 words?', 120, 360, 34, C['yel'], seg(p, .6, .8)); return
    five(ctx, 'the candy changed over time', 100, 300, seg(p, .05, .35))
    trap(ctx, 100, 400, 680, '"Would be unrecognizable today"', 'Too extreme: text says "different" ✗', seg(p, .45, .9))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Main idea covers the WHOLE text', C['yel']), ('Look right after the turn', C['green']), ('Cross out: too small, too extreme, never said', C['red'])])

SC = dict(hook=s_hook, headline=s_headline, method=s_method, turnw=s_turn_words, cave=s_cave, herbal=s_herbal, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'headline', 'method', 'method', 'turnw', 'cave', 'cave', 'cave', 'herbal', 'herbal', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', headline='The headline', method='The method', turnw='Watch for the turn', cave='Old belief, new finding', herbal='"However" texts', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Main idea', s_hook, {13: 5.0, 15: 1.5}, CH)
