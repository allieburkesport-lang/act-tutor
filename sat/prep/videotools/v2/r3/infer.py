import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/r3'
NAR = json.load(open(f'{D}/beats.json'))

def bad(ctx, s, tag, x, y, w, k, c=None):
    if k <= 0: return
    c = c or C['red']
    rrect(ctx, x, y, w, 60, 10, fill=C['bg2'], stroke=c, a=k, lw=2)
    text(ctx, s, x + 20, y + 40, 24, C['ink'], k, 'l', False)
    line(ctx, x + 14, y + 32, x + 24 + twidth(ctx, s, 24, False), y + 32, C['red'], 3, seg(k, .5, 1))
    text(ctx, tag, x + w + 24, y + 42, 28, c, k)
def good(ctx, s, x, y, k, size=32):
    if k <= 0: return
    w = twidth(ctx, '✓ ' + s, size) + 44
    rrect(ctx, x, y, w, 66, 12, fill=C['bg2'], stroke=C['green'], a=k, lw=3); text(ctx, '✓ ' + s, x + 20, y + 44, size, C['green'], k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Inferences', 100, 220, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'Finish the thought with what the facts PROVE', 102, 280, 28, C['mute'], seg(p, .1, .3), bold=False)
    passage(ctx, [('Facts, facts, facts. This suggests that', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 100, 350, 800, 34, seg(p, .35, .6))
    text(ctx, '?', 1000, 430, 120, C['yel'], seg(p, .7, .9), 'c')

def s_judge(ctx, b, p, t):
    chip(ctx, 'Think like a judge', C['blue'])
    k = seg(p, 0, .25)
    # gavel
    rrect(ctx, 220, 300, 200, 60, 12, fill=C['org'], a=k); rrect(ctx, 305, 360, 30, 160, 8, fill=C['org'], a=k)
    rrect(ctx, 160, 530, 320, 24, 8, fill=C['mute'], a=k)
    text(ctx, 'Only what the evidence shows', 580, 300, 34, C['green'], seg(p, .25, .45))
    text(ctx, '✗  no outside ideas', 580, 380, 32, C['red'], seg(p, .5, .7))
    text(ctx, '✗  no going further', 580, 440, 32, C['red'], seg(p, .65, .85))

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Underline the facts', C['blue']), ('Ask: what do they PROVE?', C['green']), ('Cross out: outside, too far, flipped', C['red'])], 200, 240, p, .05, .95, 38, 100)

def s_fungus(ctx, b, p, t):
    chip(ctx, '"This suggests that..."', C['green'])
    hl = 'hl' if b >= 1 else None
    fill = 'the fungus may help plants in dry conditions' if b >= 1 else ''
    passage(ctx, [('Plants with a certain fungus had', None, None), ('fewer wilted leaves during a dry month.', C['green'], hl), ('This suggests that', None, None), (fill, C['green'], 'blank'), ('.', None, None)], 100, 130, 1080, 30, 1 if b else seg(p, 0, .5))
    if b == 1:
        rich(ctx, [('soft word: ', C['mute']), ('may', C['yel'])], 120, 360, 34, seg(p, .65, .9))
    if b >= 2: bad(ctx, 'the fungus makes plants grow taller', 'OUTSIDE THE TEXT', 100, 340, 560, 1 if b > 2 else seg(p, 0, .4))
    if b >= 3: bad(ctx, 'plants produce twice as many tomatoes', 'GOES TOO FAR', 100, 430, 560, seg(p, 0, .4))

def s_light(ctx, b, p, t):
    chip(ctx, 'Watch for flipped facts', C['org'])
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('Scientists turned light into light', None, None), ('7 times higher in frequency.', C['green'], hl), ('This proves that', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 100, 130, 1080, 32, 1 if b else seg(p, 0, .5))
    if b >= 1:
        rich(ctx, [('low', C['blue']), ('  →  ', C['ink']), ('HIGH', C['org'])], 120, 340, 46, seg(p, 0, .3))
        good(ctx, 'low-frequency light can become much higher', 100, 380, seg(p, .1, .4), 28)
        bad(ctx, 'high-frequency light improves the material', 'BACKWARDS', 100, 480, 600, seg(p, .55, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    hl = 'hl' if b >= 1 else None
    fill = 'such writings' if b >= 1 else ''
    passage(ctx, [('No Roman', None, None), ('writings', C['green'], hl), ('mention some mysterious bronze objects. Finding', None, None), (fill, C['green'], 'blank'), ('could solve the mystery.', None, None)], 80, 110, 1120, 30, 1 if b else seg(p, 0, .5))
    choices(ctx, ['more of the objects', 'such writings', 'older coins', 'a larger museum'], 80, 270, 460, 1 if b >= 1 else seg(p, .55, .95), 1 if b >= 1 else None, (0, 2, 3) if b >= 1 else ())
    if b >= 1: text(ctx, 'missing: a WRITTEN explanation', 600, 320, 30, C['green'], 1 if b > 1 else seg(p, 0, .3))
    if b == 2: trap(ctx, 600, 360, 560, 'More objects?', 'Still no explanation. Fix the gap ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('Students who used flashcards scored higher on a vocabulary quiz. This suggests that', None, None), ('', C['yel'], 'blank'), ('.', None, None)], 100, 120, 1080, 30, 1 if b else seg(p, 0, .3))
    if b == 0:
        rrect(ctx, 100, 290, 780, 60, 10, fill=C['bg2'], stroke=C['mute'], a=seg(p, .35, .5), lw=1); text(ctx, 'A   flashcards may help vocabulary', 120, 330, 26, C['ink'], seg(p, .35, .5), 'l', False)
        rrect(ctx, 100, 370, 780, 60, 10, fill=C['bg2'], stroke=C['mute'], a=seg(p, .45, .6), lw=1); text(ctx, 'B   flashcards make students smarter in every subject', 120, 410, 26, C['ink'], seg(p, .45, .6), 'l', False)
        text(ctx, '⏸  Pause and pick', 120, 500, 34, C['yel'], seg(p, .75, .9)); return
    good(ctx, 'A  flashcards may help vocabulary', 100, 290, seg(p, 0, .3), 28)
    bad(ctx, 'B  smarter in every subject', 'GOES TOO FAR', 100, 390, 460, seg(p, .4, .8))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Underline the facts', C['blue']), ('Pick only what they PROVE', C['green']), ('No outside, too far, or flipped', C['red'])])

SC = dict(hook=s_hook, judge=s_judge, method=s_method, fungus=s_fungus, light=s_light, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'judge', 'method', 'fungus', 'fungus', 'fungus', 'fungus', 'light', 'light', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', judge='Think like a judge', method='The method', fungus='"This suggests that"', light='Flipped facts', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Inferences', s_hook, {12: 5.0, 14: 1.5}, CH)
