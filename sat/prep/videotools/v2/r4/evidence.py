import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/r4'
NAR = json.load(open(f'{D}/beats.json'))

def claim(ctx, parts, x, y, k, size=34):
    """parts: list of (text, color); colored parts are the claim's two halves"""
    if k <= 0: return
    rrect(ctx, x, y, 1080, 80, 14, fill=C['bg2'], stroke=C['yel'], a=k, lw=3)
    text(ctx, 'CLAIM', x + 20, y + 30, 16, C['yel'], k)
    rich(ctx, parts, x + 20, y + 64, size, k)
def ev(ctx, s, x, y, w, k, ok=None, tag='', parts=None, size=26):
    if k <= 0: return
    c = C['green'] if ok else C['red'] if ok is False else C['mute']
    rrect(ctx, x, y, w, 64, 12, fill=C['bg2'], stroke=c, a=k, lw=3 if ok is not None else 1)
    if parts: rich(ctx, parts, x + 20, y + 42, size, k)
    else: text(ctx, s, x + 20, y + 42, size, C['ink'], k, 'l', False)
    if tag: text(ctx, tag, x + w + 20, y + 42, 26, c, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Evidence', 100, 220, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'Support · Weaken · Illustrate', 102, 280, 32, C['mute'], seg(p, .1, .3), bold=False)
    for i, (v, c, sym) in enumerate([('support', C['green'], '▲'), ('weaken', C['red'], '▼'), ('illustrate', C['blue'], '◆')]):
        k = seg(p, .35 + i * .15, .5 + i * .15)
        rrect(ctx, 100 + i * 330, 360, 300, 120, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, sym + '  ' + v, 250 + i * 330, 432, 34, c, k, 'c')
    text(ctx, 'Evidence must test the CLAIM itself', 100, 560, 32, C['yel'], seg(p, .8, .95))

def s_defs(ctx, b, p, t):
    chip(ctx, 'What the verbs mean', C['blue'])
    rows = [('Claim', 'what someone says is true', C['yel']), ('Support', 'more believable', C['green']), ('Weaken', 'less believable', C['red']), ('Illustrate', 'shows it in action', C['blue'])]
    for i, (a, d, c) in enumerate(rows):
        k = seg(p, .05 + i * .2, .25 + i * .2)
        text(ctx, a, 220, 210 + i * 90, 40, c, k); text(ctx, d, 520, 210 + i * 90, 32, C['ink'], k, 'l', False)

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Say the claim in 5 words', C['yel']), ('Read the verb: support / weaken / illustrate', C['blue']), ('Answer hits BOTH parts of the claim', C['green'])], 160, 240, p, .05, .95, 36, 100)

SLEEP = [('more sleep', C['blue']), ('  →  ', C['ink']), ('fewer errors', C['org'])]
def s_sleep(ctx, b, p, t):
    chip(ctx, 'Support vs. weaken', C['green'])
    claim(ctx, SLEEP, 100, 120, 1 if b else seg(p, 0, .3))
    if b == 0:
        text(ctx, 'part 1', 140, 260, 24, C['blue'], seg(p, .5, .7)); text(ctx, 'part 2', 430, 260, 24, C['org'], seg(p, .6, .8)); return
    ev(ctx, '', 100, 280, 760, 1 if b > 1 else seg(p, 0, .4), True, 'SUPPORTS', [('9-hour sleepers', C['blue']), (' made the ', C['ink']), ('fewest errors', C['org'])])
    if b >= 2: ev(ctx, '', 100, 370, 760, 1 if b > 2 else seg(p, 0, .4), False, 'ONLY ONE PART', [('Most students ', C['ink']), ('sleep 7 hours', C['blue']), ('.', C['ink'])])
    if b >= 3: ev(ctx, '', 100, 460, 760, seg(p, 0, .5), True, 'WEAKENS', [('9-hour sleepers', C['blue']), (' made ', C['ink']), ('as many errors', C['org']), (' as 6-hour sleepers', C['ink'])])

def s_quote(ctx, b, p, t):
    chip(ctx, 'Illustrate with a quotation', C['blue'])
    claim(ctx, [('used ', C['ink']), ('humor', C['green']), (' to soften ', C['ink']), ('harsh events', C['red'])], 100, 120, 1 if b else seg(p, 0, .4))
    if b == 0:
        text(ctx, 'quote needs: a harsh event + a joke', 120, 290, 32, C['yel'], seg(p, .6, .85)); return
    passage(ctx, [('"As', None, None), ('the flood took the barn,', C['red'], 'hl'), ('Aunt Ruth complained only that', None, None), ('the cows left without saying goodbye."', C['green'], 'hl')], 100, 250, 1080, 30, seg(p, 0, .4))
    rich(ctx, [('harsh', C['red']), (' + ', C['ink']), ('humor', C['green']), ('  =  both parts ✓', C['ink'])], 120, 450, 36, seg(p, .6, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    claim(ctx, [('rainfall', C['blue']), (' affects ', C['ink']), ('tree growth', C['green'])], 100, 110, 1)
    write(ctx, 'Which data supports the claim?', 100, 240, 28, C['yel'], 1 if b else seg(p, .4, .8))
    if b >= 1:
        ev(ctx, '', 100, 280, 760, 1 if b > 1 else seg(p, 0, .4), True, 'BOTH PARTS', [('Trees in the ', C['ink']), ('wettest', C['blue']), (' region ', C['ink']), ('grew the most', C['green'])])
    if b >= 2:
        ev(ctx, 'Region C had the most trees.', 100, 370, 760, seg(p, 0, .4), False, 'OFF TOPIC')
        trap(ctx, 100, 460, 640, 'Number of trees ≠ growth.', 'True but off topic is still wrong ✗', seg(p, .4, .9))

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    claim(ctx, [('users work to ', C['ink']), ('restore the default', C['green'])], 100, 110, 1 if b else seg(p, 0, .3))
    write(ctx, 'Which quote illustrates it?', 100, 240, 28, C['yel'], 1 if b else seg(p, .3, .5))
    ev(ctx, '"I always return to the original color scheme."', 100, 280, 760, 1 if b else seg(p, .45, .6), True if b else None, 'MATCHES' if b else '')
    ev(ctx, '"Color schemes don\'t matter to me."', 100, 370, 760, 1 if b else seg(p, .6, .75), False if b else None, 'OPPOSITE' if b else '')
    if b == 0: text(ctx, '⏸  Pause and pick', 100, 500, 34, C['yel'], seg(p, .85, .95))
    else: rich(ctx, [('return to the original', C['green']), (' = ', C['ink']), ('restore the default', C['green'])], 100, 500, 30, seg(p, .3, .6))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Say the claim in 5 words', C['yel']), ('Match the verb: support / weaken / illustrate', C['blue']), ('Hit BOTH parts of the claim', C['green'])])

SC = dict(hook=s_hook, defs=s_defs, method=s_method, sleep=s_sleep, quote=s_quote, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'defs', 'method', 'sleep', 'sleep', 'sleep', 'sleep', 'quote', 'quote', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', defs='Claim and evidence', method='The method', sleep='Support vs. weaken', quote='Illustrate with a quote', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Evidence', s_hook, {12: 5.0, 14: 1.5}, CH)
