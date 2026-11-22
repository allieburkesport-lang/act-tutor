import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/g1'
NAR = json.load(open(f'{D}/beats.json'))

def mod(ctx, opener, doer, rest, y, k, ok=True, size=30, x=80):
    """opener phrase + comma, doer (boxed green/red), rest"""
    if k <= 0: return
    c = C['green'] if ok else C['red']
    wo = twidth(ctx, opener + ',', size, False)
    rrect(ctx, x - 6, y - size - 4, wo + 2, size + 16, 8, fill=C['blue'], a=.15 * k)
    text(ctx, opener + ',', x, y, size, C['blue'], k, 'l', False)
    xd = x + wo + 14; wd = twidth(ctx, doer, size)
    rrect(ctx, xd - 6, y - size - 4, wd + 12, size + 16, 8, stroke=c, a=k, lw=3)
    text(ctx, doer, xd, y, size, c, k)
    text(ctx, rest, xd + wd + 16, y, size, C['ink'], k, 'l', False)
    # name-tag arrow
    line(ctx, x + wo / 2, y + 16, x + wo / 2, y + 34, C['blue'], 2, 1, k); line(ctx, x + wo / 2, y + 34, xd + wd / 2, y + 34, C['blue'], 2, 1, k)
    line(ctx, xd + wd / 2, y + 34, xd + wd / 2, y + 16, C['blue'], 2, 1, k)
    text(ctx, '✓ DOER' if ok else '✗ can\'t do it', xd + wd / 2, y + 60, 20, c, k, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Modifiers', 100, 200, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'The doer goes right after the comma', 102, 260, 30, C['mute'], seg(p, .1, .3), bold=False)
    mod(ctx, 'Studying the night sky', 'Maria Mitchell', 'spotted a comet.', 420, seg(p, .35, .7), True, 34, 100)

def s_tag(ctx, b, p, t):
    chip(ctx, 'A name tag', C['blue'])
    k = seg(p, 0, .3)
    rrect(ctx, 400, 180, 480, 200, 20, fill=C['bg2'], stroke=C['blue'], a=k, lw=4)
    text(ctx, 'HELLO, I was...', 640, 240, 30, C['blue'], k, 'c'); text(ctx, 'studying the sky', 640, 310, 40, C['ink'], k, 'c')
    k2 = seg(p, .45, .75)
    line(ctx, 640, 380, 640, 470, C['yel'], 4, k2)
    text(ctx, 'pin it on the word right after the comma', 640, 520, 30, C['yel'], k2, 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Choices start with different words?', C['blue']), ('Who does the opening action?', C['yel']), ('That word goes right after the comma', C['green'])], 200, 240, p, .05, .95, 36, 100)

def s_ing(ctx, b, p, t):
    chip(ctx, '-ing opening', C['green'])
    mod(ctx, 'Studying the night sky', 'Maria Mitchell', 'spotted a new comet.', 220, 1 if b else seg(p, 0, .5))
    if b:
        mod(ctx, 'Studying the night sky', 'a new comet', 'was spotted.', 400, seg(p, 0, .4), False)
        text(ctx, 'the comet is studying the sky? → DANGLING', 80, 520, 28, C['red'], seg(p, .45, .8))

def s_more(ctx, b, p, t):
    chip(ctx, 'Any opening works the same', C['blue'])
    if b == 0:
        mod(ctx, 'Built in 1884', 'the Washington Monument', 'was once the tallest.', 240, seg(p, .1, .5), True, 28); return
    mod(ctx, 'Built in 1884', 'the Washington Monument', 'was once the tallest.', 200, 1, True, 28)
    mod(ctx, 'To test the theory', 'the researchers', 'built a model.', 380, seg(p, .05, .45), True, 28)

def s_poss(ctx, b, p, t):
    chip(ctx, 'The ’s trap', C['red'])
    mod(ctx, 'Hiking through the Andes', 'the botanist’s notebook', 'filled up.', 220, seg(p, .1, .45), False, 28)
    text(ctx, 'with ’s, the NOTEBOOK is the doer', 80, 400, 30, C['red'], seg(p, .5, .7))
    text(ctx, 'notebooks don\'t hike ✗', 80, 450, 30, C['red'], seg(p, .7, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('After pleading for years,', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 80, 110, 1120, 30, seg(p, 0, .3))
        choices(ctx, ['the activists staged a sit-in protest', 'pressure on lawmakers increased'], 80, 260, 620, seg(p, .4, .9)); return
    mod(ctx, 'After pleading for years', 'the activists', 'staged a sit-in protest.', 200, 1, True, 30)
    if b == 2:
        mod(ctx, 'After pleading for years', 'pressure', 'on lawmakers increased.', 380, seg(p, 0, .4), False, 30)
        trap(ctx, 640, 440, 560, 'Pressure can\'t plead.', 'Can\'t do the action? Cross it out ✗', seg(p, .4, .9))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('As a young writer,', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 80, 120, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        choices(ctx, ['Eudora Welty worked as a photographer', 'a government agency hired Eudora Welty'], 80, 260, 660, seg(p, .35, .7))
        text(ctx, '⏸  Pause and pick', 80, 430, 34, C['yel'], seg(p, .8, .95)); return
    mod(ctx, 'As a young writer', 'Eudora Welty', 'worked as a photographer.', 300, seg(p, 0, .4), True, 30)

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Who does the opening action?', C['blue']), ('That word goes right after the comma', C['green']), ('Watch the ’s trap', C['red'])])

SC = dict(hook=s_hook, tag=s_tag, method=s_method, ing=s_ing, more=s_more, poss=s_poss, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'tag', 'method', 'ing', 'ing', 'more', 'more', 'poss', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', tag='A name tag', method='The method', ing='-ing openings', more='Other openings', poss='The ’s trap', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Modifiers', s_hook, {11: 5.0, 13: 1.5}, CH)
