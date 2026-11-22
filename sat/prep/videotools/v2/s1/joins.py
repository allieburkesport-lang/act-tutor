import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s1'
NAR = json.load(open(f'{D}/beats.json'))

def join(ctx, L, M, R, y, k, mc=None, tags=None, size=30, x=80):
    """Draw 'L M R' on one line; M in big colored type. tags=(lt, rt) labels under each side."""
    if k <= 0: return
    mc = mc or C['yel']
    wl = twidth(ctx, L, size, False); wm = twidth(ctx, M, size + 8) if M.strip() else 30
    text(ctx, L, x, y, size, C['ink'], k, 'l', False)
    if M.strip(): text(ctx, M, x + wl + 4, y, size + 8, mc, k)
    else: rrect(ctx, x + wl + 6, y - size, 18, size + 6, 4, stroke=mc, a=k, lw=2)
    text(ctx, R, x + wl + wm + 14, y, size, C['ink'], k, 'l', False)
    if tags:
        for (lab, xx, ww, ok) in [(tags[0], x, wl, tags[0] == 'FULL'), (tags[1], x + wl + wm + 14, twidth(ctx, R, size, False), tags[1] == 'FULL')]:
            if not lab: continue
            c = C['green'] if ok else C['org']
            line(ctx, xx, y + 14, xx + ww, y + 14, c, 3, 1, k); text(ctx, lab, xx + ww / 2, y + 44, 20, c, k, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Joining Two Sentences', 100, 200, 62, C['ink'], seg(p, 0, .12))
    text(ctx, 'who + did = full sentence', 102, 260, 30, C['mute'], seg(p, .1, .3), bold=False)
    join(ctx, 'The volcano erupted', ' ? ', 'crops failed.', 400, seg(p, .35, .6), C['yel'], ('FULL', 'FULL'), 40, 120)
    text(ctx, 'needs a STRONG joiner', 120, 540, 36, C['yel'], seg(p, .75, .95))

def s_three(ctx, b, p, t):
    chip(ctx, 'The 3 strong joiners', C['green'])
    for i, (sym, lab) in enumerate([('.', 'period'), (';', 'semicolon'), (', + FANBOYS', 'comma + for, and, nor, but, or, yet, so')]):
        k = seg(p, .05 + i * .25, .25 + i * .25)
        rrect(ctx, 140, 160 + i * 130, 1000, 100, 16, fill=C['bg2'], stroke=C['green'], a=k, lw=3)
        text(ctx, sym, 190, 228 + i * 130, 54 if i < 2 else 36, C['green'], k); text(ctx, lab, 470 if i < 2 else 460, 224 + i * 130, 30 if i < 2 else 26, C['ink'], k, 'l', False)

def s_hat(ctx, b, p, t):
    chip(ctx, 'Picture it', C['blue'])
    k = seg(p, 0, .3)
    text(ctx, ';', 340, 400, 200, C['green'], k, 'c')
    rrect(ctx, 290, 190, 100, 20, 4, fill=C['org'], a=k); rrect(ctx, 310, 140, 60, 56, 8, fill=C['org'], a=k)
    text(ctx, 'a period wearing a hat', 340, 520, 30, C['green'], k, 'c')
    k2 = seg(p, .45, .75)
    rrect(ctx, 700, 330, 160, 30, 6, fill=C['mute'], a=k2); rrect(ctx, 920, 345, 160, 30, 6, fill=C['mute'], a=k2)
    text(ctx, ',', 890, 330, 80, C['red'], k2, 'c')
    text(ctx, 'comma alone = broken bridge', 890, 520, 30, C['red'], k2, 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Find where the two parts meet', C['blue']), ('Cover each side: FULL or not?', C['yel']), ('Full + full → strong joiner', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_period(ctx, b, p, t):
    chip(ctx, 'Full + full', C['green'])
    if b == 0:
        join(ctx, 'The volcano erupted in 1815', '.', 'Crops failed across Europe the next year.', 260, seg(p, 0, .4), C['green'], ('FULL', 'FULL'), 28)
        text(ctx, '✓ period works', 80, 400, 34, C['green'], seg(p, .7, .9)); return
    join(ctx, 'The volcano erupted in 1815', '.', 'Crops failed across Europe the next year.', 220, 1, C['green'], None, 28)
    if b >= 1:
        join(ctx, 'The volcano erupted in 1815', ',', 'crops failed across Europe...', 330, 1 if b > 1 else seg(p, 0, .3), C['red'], None, 28)
        text(ctx, '✗ COMMA SPLICE', 900, 330, 26, C['red'], 1 if b > 1 else seg(p, .3, .6))
    if b >= 2:
        join(ctx, 'The plan improved national parks', ' ', 'it rebuilt roads...', 440, seg(p, 0, .3), C['red'], None, 28)
        text(ctx, '✗ RUN-ON', 900, 440, 26, C['red'], seg(p, .4, .7))

def s_fanboys(ctx, b, p, t):
    chip(ctx, 'Comma + FANBOYS  vs.  however', C['blue'])
    join(ctx, 'The first trial looked promising', ', but', 'the drug failed later.', 220, 1 if b else seg(p, 0, .4), C['green'], None, 28)
    text(ctx, 'comma BEFORE but', 80, 280, 26, C['green'], 1 if b else seg(p, .5, .8))
    if b:
        join(ctx, 'The trial looked promising', '; however,', 'the drug failed.', 400, seg(p, .2, .5), C['green'], None, 28)
        text(ctx, 'however is NOT a FANBOYS word → needs ;', 80, 460, 26, C['yel'], seg(p, .55, .85))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('The plan was simple', None, None), ('', C['yel'], 'blank'), ('the team would map the cave first.', None, None)], 80, 110, 1120, 30, seg(p, 0, .4))
        choices(ctx, [',', ':', '(nothing)', ', and'], 80, 260, 360, seg(p, .45, .95)); return
    if b == 1:
        join(ctx, 'The plan was simple', ':', 'the team would map the cave first.', 180, 1, C['green'], ('FULL', 'FULL'), 30)
        text(ctx, '✓ colon needs a FULL sentence before it', 80, 320, 30, C['green'], seg(p, .65, .9)); return
    join(ctx, 'While one requires oxygen', ',', 'both are forms of respiration.', 180, 1, C['green'], ('STARTER', 'FULL'), 30)
    trap(ctx, 80, 300, 640, 'One side NOT full? Rules change.', 'Starter part takes just a comma ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('The poet was nervous', None, None), ('', C['yel'], 'blank'), ('her reading went well.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [(', but', C['ink']), ('     or     ', C['mute']), ('; but', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    join(ctx, 'The poet was nervous', ', but', 'her reading went well.', 330, seg(p, 0, .3), C['green'], None, 32)
    trap(ctx, 80, 380, 600, '; but  doubles up.', 'The semicolon already joins ✗', seg(p, .4, .9))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Full + full: . or ; or , + FANBOYS', C['green']), ('Comma alone = comma splice', C['red']), ('however needs a semicolon', C['yel'])])

SC = dict(hook=s_hook, three=s_three, hat=s_hat, method=s_method, period=s_period, fanboys=s_fanboys, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'three', 'hat', 'method', 'period', 'period', 'period', 'fanboys', 'fanboys', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', three='3 strong joiners', hat='Picture it', method='The method', period='Splices and run-ons', fanboys='FANBOYS vs. however', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Joining sentences', s_hook, {12: 5.0, 14: 1.5}, CH)
