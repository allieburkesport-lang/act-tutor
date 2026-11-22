import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s4'
NAR = json.load(open(f'{D}/beats.json'))

def sent(ctx, parts, x, y, k, size=30, lift=0):
    """parts: list of (text, kind) kind: 'n' normal, 'x' extra info, 'm' mark (str shown big), 'bad' red mark, 'gap' missing mark"""
    if k <= 0: return
    xx = x
    for s, kind in parts:
        if kind == 'n':
            text(ctx, s, xx, y, size, C['ink'], k, 'l', False); xx += twidth(ctx, s, size, False)
        elif kind == 'x':
            w = twidth(ctx, s, size, False)
            rrect(ctx, xx - 4, y - size - 2 - lift, w + 8, size + 14, 6, fill=C['blue'], a=.18 * k)
            text(ctx, s, xx, y - lift, size, C['blue'], k * (1 - .6 * (lift > 0)), 'l', False); xx += w
        elif kind in ('m', 'bad'):
            c = C['green'] if kind == 'm' else C['red']
            text(ctx, s, xx + 2, y, size + 10, c, k); xx += twidth(ctx, s, size + 10) + 6
        elif kind == 'gap':
            rrect(ctx, xx + 4, y - size, 16, size + 6, 4, stroke=C['red'], a=k, lw=2); xx += 26
        xx += 8

def sock(ctx, x, y, c, k, s=1, flip=False):
    if k <= 0: return
    d = -1 if flip else 1
    rrect(ctx, x, y, 40 * s, 90 * s, 10, fill=c, a=k)
    rrect(ctx, x if not flip else x - 30 * s, y + 70 * s, 70 * s, 34 * s, 14, fill=c, a=k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Pairs', 100, 210, 72, C['ink'], seg(p, 0, .12))
    text(ctx, 'Matching marks around extra info', 102, 270, 30, C['mute'], seg(p, .1, .3), bold=False)
    sent(ctx, [('The observatory', 'n'), ('(', 'm'), ('built in 1897', 'x'), (')', 'm'), ('houses a telescope.', 'n')], 100, 420, seg(p, .3, .6), 34)
    text(ctx, 'can be lifted out', 330, 500, 26, C['blue'], seg(p, .65, .9), 'l', False)

def s_socks(ctx, b, p, t):
    chip(ctx, 'Like socks', C['blue'])
    for i, (a, c, ok) in enumerate([(', ,', C['green'], True), ('— —', C['green'], True), ('( )', C['green'], True)]):
        k = seg(p, .05 + i * .12, .2 + i * .12)
        sock(ctx, 140 + i * 160, 170, c, k, .9); sock(ctx, 200 + i * 160, 170, c, k, .9)
        text(ctx, a, 175 + i * 160, 300, 34, C['ink'], k, 'c')
    k = seg(p, .55, .7)
    sock(ctx, 760, 170, C['red'], k, .9); text(ctx, 'one sock', 790, 300, 26, C['red'], k, 'c')
    k = seg(p, .7, .85)
    sock(ctx, 940, 170, C['blue'], k, .9); sock(ctx, 1000, 170, C['org'], k, .9); text(ctx, 'mixed', 990, 300, 26, C['red'], k, 'c')
    text(ctx, '✗', 790, 380, 50, C['red'], seg(p, .6, .75), 'c'); text(ctx, '✗', 990, 380, 50, C['red'], seg(p, .8, .95), 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Find the mark already there', C['blue']), ('The blank must MATCH it', C['green']), ('Lift-out test: still a sentence?', C['yel'])], 200, 240, p, .05, .95, 38, 100)

def s_commas(ctx, b, p, t):
    chip(ctx, 'Two commas', C['green'])
    sent(ctx, [('A rare isotope', 'n'), (',', 'm'), ('carbon-13', 'x'), (',', 'm'), ('builds up in bears.', 'n')], 100, 260, 1 if b else seg(p, 0, .4), 34, 0)
    if b == 0:
        sent(ctx, [('A rare isotope', 'n'), ('builds up in bears.', 'n')], 100, 380, seg(p, .6, .85), 34)
        text(ctx, '✓ still works without it', 100, 450, 28, C['green'], seg(p, .75, .95)); return
    sent(ctx, [('A rare isotope', 'n'), (',', 'm'), ('carbon-13', 'x'), ('', 'gap'), ('builds up in bears.', 'n')], 100, 380, seg(p, 0, .3), 34)
    text(ctx, '✗ ONE SOCK: never closed', 100, 450, 28, C['red'], seg(p, .35, .65))

def s_dashes(ctx, b, p, t):
    chip(ctx, 'Two dashes', C['green'])
    sent(ctx, [('chloroplasts', 'n'), ('—', 'm'), ('the organs that make energy', 'x'), ('—', 'm'), ('reshuffled.', 'n')], 80, 260, 1 if b else seg(p, 0, .5), 32)
    if b:
        sent(ctx, [('chloroplasts', 'n'), (',', 'bad'), ('the organs that make energy', 'x'), ('—', 'bad'), ('reshuffled.', 'n')], 80, 380, seg(p, 0, .3), 32)
        text(ctx, '✗ MIXED SOCKS', 80, 450, 28, C['red'], seg(p, .35, .65))

def s_edge(ctx, b, p, t):
    chip(ctx, 'Extra info at the edge', C['blue'])
    sent(ctx, [('A self-taught fossil hunter', 'x'), (',', 'm'), ('Mary Anning made discoveries.', 'n')], 80, 260, seg(p, .3, .7), 32)
    text(ctx, 'sentence edge = the other sock', 80, 360, 28, C['yel'], seg(p, .65, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('The Library of Congress, which was founded in 1800', None, None), ('', C['yel'], 'blank'), ('holds millions of books.', None, None)], 80, 110, 1120, 30, seg(p, 0, .5))
        choices(ctx, [',', '—', ';', '(no punctuation)'], 80, 260, 400, seg(p, .5, .95)); return
    sent(ctx, [('The Library of Congress', 'n'), (',', 'm'), ('which was founded in 1800', 'x'), (',', 'm'), ('holds books.', 'n')], 80, 200, 1, 30)
    choices(ctx, [',', '—', ';', '(no punctuation)'], 80, 260, 400, 1, 0, (1, 2, 3))
    if b == 1: text(ctx, 'opened with a comma → close with a comma', 520, 320, 28, C['green'], seg(p, .2, .6))
    if b == 2: trap(ctx, 520, 300, 640, 'Nothing = one sock. Dash = mixed.', 'Match what\'s already there ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('The observatory (built in 1897)', None, None), ('', C['yel'], 'blank'), ('houses a huge telescope.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [(',', C['ink']), ('     or     ', C['mute']), ('(nothing)', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    rich(ctx, [('✓ nothing', C['green'])], 100, 330, 44, seg(p, 0, .3))
    trap(ctx, 80, 380, 640, 'A comma walls off "observatory"', 'from its verb "houses" ✗', seg(p, .3, .8))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Extra info can be lifted out', C['blue']), ('Match the mark already there', C['green']), ('Never one sock, never mixed', C['red'])])

SC = dict(hook=s_hook, socks=s_socks, method=s_method, commas=s_commas, dashes=s_dashes, edge=s_edge, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'socks', 'method', 'commas', 'commas', 'dashes', 'dashes', 'edge', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', socks='Like socks', method='The method', commas='Two commas', dashes='Two dashes', edge='At the edge', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Pairs', s_hook, {11: 5.0, 13: 1.5}, CH)
