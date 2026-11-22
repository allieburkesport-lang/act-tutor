import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s2'
NAR = json.load(open(f'{D}/beats.json'))

def pair(ctx, a, b_, la, lb, y, k, x=80, size=32, wall=None):
    """two word groups with labels and a 'holding hands' link between them; wall = punctuation shown as red wall"""
    if k <= 0: return
    wa = twidth(ctx, a, size, False); gap = 70
    text(ctx, a, x, y, size, C['ink'], k, 'l', False)
    text(ctx, b_, x + wa + gap, y, size, C['ink'], k, 'l', False)
    line(ctx, x, y + 14, x + wa, y + 14, C['blue'], 3, 1, k); text(ctx, la, x + wa / 2, y + 44, 22, C['blue'], k, 'c')
    wb = twidth(ctx, b_, size, False)
    line(ctx, x + wa + gap, y + 14, x + wa + gap + wb, y + 14, C['green'], 3, 1, k); text(ctx, lb, x + wa + gap + wb / 2, y + 44, 22, C['green'], k, 'c')
    mx = x + wa + gap / 2
    if wall:
        rrect(ctx, mx - 8, y - size - 6, 16, size + 26, 4, fill=C['red'], a=k); text(ctx, wall, mx, y - size - 14, 30, C['red'], k, 'c')
    else:
        arc(ctx, mx, y - size / 2, 20, math.pi * 1.1, math.pi * 1.9, C['yel'], 3, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'No Wall', 100, 210, 72, C['ink'], seg(p, 0, .12))
    text(ctx, 'No punctuation between words that belong together', 102, 270, 28, C['mute'], seg(p, .1, .3), bold=False)
    for i, s in enumerate([',', ':', ';', '—']):
        k = seg(p, .35 + i * .1, .5 + i * .1)
        rrect(ctx, 140 + i * 160, 360, 120, 120, 16, fill=C['bg2'], stroke=C['red'], a=k, lw=3); text(ctx, s, 200 + i * 160, 440, 60, C['red'], k, 'c')
        line(ctx, 150 + i * 160, 470, 250 + i * 160, 370, C['red'], 4, seg(p, .8, .95))

def s_hands(ctx, b, p, t):
    chip(ctx, 'Holding hands', C['blue'])
    k = seg(p, 0, .3)
    for x, c in ((420, C['blue']), (860, C['green'])):
        disc(ctx, x, 260, 40, c, k); rrect(ctx, x - 44, 306, 88, 140, 30, fill=c, a=k)
    line(ctx, 464, 360, 816, 360, C['yel'], 6, seg(p, .15, .4))
    k2 = seg(p, .55, .8)
    rrect(ctx, 630, 220, 20, 280, 4, fill=C['red'], a=k2)
    text(ctx, 'punctuation = a wall ✗', 640, 560, 34, C['red'], k2, 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Choices differ only by , : or nothing?', C['blue']), ('Do the two sides belong together?', C['yel']), ('Yes → NO punctuation', C['green'])], 200, 240, p, .05, .95, 36, 100)

def s_whodid(ctx, b, p, t):
    chip(ctx, 'Who + did', C['blue'])
    pair(ctx, 'The scientists who studied the reef', 'published their results.', 'WHO', 'DID', 260, 1 if b else seg(p, .1, .5))
    if b:
        pair(ctx, 'The scientists who studied the reef', 'published their results.', 'WHO', 'DID', 420, seg(p, 0, .3), wall=',')
        text(ctx, '✗ splits who from did', 80, 520, 30, C['red'], seg(p, .4, .7))

def s_pairs(ctx, b, p, t):
    chip(ctx, 'More pairs that hold hands', C['green'])
    rows = [('signed', 'the treaty', 'DID', 'WHAT', ':'), ('Entomologist', 'Heather Grab', 'TITLE', 'NAME', ','), ('The study found', 'that sleep helps.', 'VERB', 'THAT', ',')][:b + 1]
    for i, (a, bb, la, lb, w) in enumerate(rows):
        k = 1 if i < b else seg(p, 0, .4)
        pair(ctx, a, bb, la, lb, 220 + i * 140, k, 120)
        text(ctx, 'no ' + w, 900, 220 + i * 140, 30, C['red'], 1 if i < b else seg(p, .4, .7))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('The scientists who studied the reef', None, None), ('', C['yel'], 'blank'), ('published their results.', None, None)], 80, 110, 1120, 30, seg(p, 0, .4))
        choices(ctx, [',', ':', ';', '(no punctuation)'], 80, 260, 400, seg(p, .45, .95)); return
    pair(ctx, 'The scientists who studied the reef', 'published their results.', 'WHO', 'DID', 220, 1, 80)
    choices(ctx, [',', ':', ';', '(no punctuation)'], 80, 300, 400, 1, 3, (0, 1, 2))
    if b == 2: trap(ctx, 560, 320, 600, 'Long who? Still no comma.', 'Length doesn\'t matter ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('writers such as', None, None), ('', C['yel'], 'blank'), ('Zora Neale Hurston and Langston Hughes', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [(':', C['ink']), ('     or     ', C['mute']), ('(nothing)', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    rich(ctx, [('✓ nothing', C['green'])], 100, 330, 44, seg(p, 0, .3))
    trap(ctx, 80, 380, 600, '"such as" already does the colon\'s job.', 'Adding : doubles up ✗', seg(p, .3, .8))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Words that belong together hold hands', C['yel']), ('Never split who from did', C['blue']), ('In doubt? Do they belong together?', C['green'])])

SC = dict(hook=s_hook, hands=s_hands, method=s_method, whodid=s_whodid, pairs=s_pairs, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'hands', 'method', 'whodid', 'whodid', 'pairs', 'pairs', 'pairs', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', hands='Holding hands', method='The method', whodid='Who + did', pairs='More pairs', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · No wall', s_hook, {11: 5.0, 13: 1.5}, CH)
