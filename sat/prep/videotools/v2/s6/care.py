import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s6'
NAR = json.load(open(f'{D}/beats.json'))
G = [('C', 'Contrast', 'however', C['red']), ('A', 'Add', 'moreover', C['blue']), ('R', 'Result', 'therefore', C['green']), ('E', 'Example', 'for example', C['org'])]

def badge(ctx, L, x, y, k, big=False):
    if k <= 0: return
    c = {g[0]: g[3] for g in G}[L]; r = 34 if big else 24
    disc(ctx, x, y, r, c, k); text(ctx, L, x, y + (12 if big else 9), 34 if big else 24, C['bg'], k, 'c')

def two(ctx, s1, s2, tw, y, k, tc=C['yel'], size=28):
    passage(ctx, [(s1, None, None), (tw, tc, 'blank'), (s2, None, None)], 80, y, 1120, size, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Transitions', 100, 200, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'How does sentence 2 connect to sentence 1?', 102, 260, 28, C['mute'], seg(p, .1, .3), bold=False)
    k = seg(p, .3, .6)
    rrect(ctx, 100, 360, 360, 120, 16, fill=C['bg2'], stroke=C['mute'], a=k, lw=2); text(ctx, 'Sentence 1', 280, 430, 30, C['ink'], k, 'c')
    rrect(ctx, 820, 360, 360, 120, 16, fill=C['bg2'], stroke=C['mute'], a=k, lw=2); text(ctx, 'Sentence 2', 1000, 430, 30, C['ink'], k, 'c')
    k2 = seg(p, .55, .85)
    arc(ctx, 640, 470, 180, math.pi * 1.15, math.pi * 1.85, C['yel'], 6, k2)
    text(ctx, 'bridge word', 640, 340, 30, C['yel'], k2, 'c')

def s_care(ctx, b, p, t):
    chip(ctx, 'Do you CARE?', C['yel'])
    for i, (L, name, ex, c) in enumerate(G):
        k = seg(p, .1 + i * .2, .28 + i * .2)
        rrect(ctx, 100 + i * 275, 200, 250, 280, 18, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, L, 225 + i * 275, 300, 80, c, k, 'c'); text(ctx, name, 225 + i * 275, 370, 32, C['ink'], k, 'c')
        text(ctx, ex, 225 + i * 275, 430, 24, C['mute'], k, 'c', False)

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Cover the choices', C['mute']), ('Decide C, A, R or E', C['yel']), ('Pick a word from THAT group', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_ex(ctx, b, p, t):
    if b < 2:
        chip(ctx, 'C · contrast', C['red'])
        two(ctx, 'The first trial looked promising.', 'the drug failed in the larger study.', 'However,' if b == 0 and p > .7 or b == 1 else '', 140, 1, C['red'])
        rich(ctx, [('promising  →  failed  =  a turn', C['ink'])], 100, 320, 32, 1 if b else seg(p, .3, .55))
        badge(ctx, 'C', 120, 400, 1 if b else seg(p, .55, .7), True)
        if b == 1: trap(ctx, 200, 380, 640, '"Therefore" is a RESULT word.', 'Promising didn\'t CAUSE failure ✗', seg(p, .1, .6))
        return
    chip(ctx, 'A · add', C['blue'])
    two(ctx, 'Bees pollinate many crops.', 'they produce honey and wax.', 'Moreover,' if p > .7 else '', 140, 1, C['blue'])
    rich(ctx, [('one more point, same side', C['ink'])], 100, 320, 32, seg(p, .35, .6))
    badge(ctx, 'A', 120, 400, seg(p, .6, .75), True)

def s_flav(ctx, b, p, t):
    chip(ctx, 'Contrast flavors', C['red'])
    if b == 0:
        for i, (w, d) in enumerate([('Instead', 'a replacement'), ('Nonetheless', 'still true anyway'), ('Granted', 'admits a weakness')]):
            k = seg(p, .15 + i * .25, .35 + i * .25)
            badge(ctx, 'C', 150, 225 + i * 110, k); text(ctx, w, 200, 236 + i * 110, 40, C['red'], k); text(ctx, d, 560, 236 + i * 110, 32, C['ink'], k, 'l', False)
        return
    two(ctx, 'The new plan has worked well.', 'it is expensive.', 'Granted,' if p > .7 else '', 140, 1, C['red'])
    text(ctx, 'admit a downside, main point stands', 100, 320, 30, C['ink'], seg(p, .3, .6), 'l', False)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    two(ctx, '"Third spaces" have sparked enormous new interest.', 'the idea dates back to 1989.', 'Nonetheless,' if b else '', 100, 1 if b else seg(p, 0, .4), C['red'], 26)
    choices(ctx, ['Furthermore,', 'Therefore,', 'Nonetheless,', 'For example,'], 80, 270, 400, 1 if b else seg(p, .55, .95), 2 if b else None, (0, 1, 3) if b else ())
    if b == 1:
        text(ctx, 'new interest  vs.  old idea', 520, 320, 30, C['ink'], seg(p, 0, .3)); badge(ctx, 'C', 545, 380, seg(p, .3, .5)); text(ctx, 'still true anyway', 585, 389, 28, C['red'], seg(p, .35, .6))
    if b == 2: trap(ctx, 520, 300, 640, '"Furthermore" is an ADD word.', 'It misses the turn ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    two(ctx, 'The road was icy.', 'the school closed for the day.', 'Therefore,' if b else '', 130, 1 if b else seg(p, 0, .3), C['green'], 32)
    if b == 0:
        for i, (L, *_r) in enumerate(G): badge(ctx, L, 140 + i * 90, 360, seg(p, .4 + i * .08, .55 + i * .08), True)
        text(ctx, '⏸  Pause and pick', 100, 460, 34, C['yel'], seg(p, .8, .95)); return
    badge(ctx, 'R', 140, 360, seg(p, 0, .3), True)
    text(ctx, 'Result: icy → closed', 200, 372, 34, C['green'], seg(p, .1, .4))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Decide C, A, R or E first', C['yel']), ('Pick from THAT group', C['green']), ('Smart-sounding ≠ correct', C['red'])])

SC = dict(hook=s_hook, care=s_care, method=s_method, ex=s_ex, flav=s_flav, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'care', 'method', 'ex', 'ex', 'ex', 'flav', 'flav', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', care='C · A · R · E', method='The method', ex='Contrast and add', flav='Contrast flavors', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Transitions', s_hook, {11: 5.0, 13: 1.5}, CH)
