import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s3'
NAR = json.load(open(f'{D}/beats.json'))
Q = '’'

def own(ctx, owner, thing, x, y, k, size=40, oc=None, note=None, nc=None):
    """owner (with apostrophe) -> owned thing, arrow from owner to thing"""
    if k <= 0: return
    oc = oc or C['green']
    wo = twidth(ctx, owner, size)
    text(ctx, owner, x, y, size, oc, k); text(ctx, thing, x + wo + 20, y, size, C['ink'], k, 'l', False)
    tw = twidth(ctx, thing, size, False)
    text(ctx, 'OWNER', x + wo / 2, y + 40, 18, oc, k, 'c'); text(ctx, 'OWNED', x + wo + 20 + tw / 2, y + 40, 18, C['mute'], k, 'c')
    if note: text(ctx, note, x + wo + tw + 60, y, 26, nc or C['mute'], k, 'l', False)

def s_hook(ctx, b, p, t):
    text(ctx, 'Apostrophes', 100, 210, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'and pronouns', 104, 268, 34, C['mute'], seg(p, .05, .2), bold=False)
    text(ctx, Q, 900, 420, 260, C['yel'], seg(p, .2, .5), 'c')
    text(ctx, 'goes on the OWNER', 100, 400, 40, C['green'], seg(p, .45, .7))
    text(ctx, 'never on the thing owned', 100, 460, 32, C['red'], seg(p, .65, .9), 'l', False)

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Is the next word OWNED?', C['yel']), ('No → no apostrophe', C['mute']), ('Yes → count the owners', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_one(ctx, b, p, t):
    chip(ctx, 'One owner: ' + Q + 's', C['green'])
    own(ctx, 'author' + Q + 's', 'political writings', 120, 250, 1 if b else seg(p, .1, .5), 44, note='one author' if not b else None)
    if b:
        rich(ctx, [('authors' + Q, C['red']), (' political ', C['ink']), ('writings' + Q, C['red'])], 120, 420, 40, seg(p, 0, .3))
        trap(ctx, 120, 460, 600, 'One author. Writings own nothing.', 'Never mark the thing owned ✗', seg(p, .35, .8))

def s_many(ctx, b, p, t):
    chip(ctx, 'Count the owners', C['blue'])
    rows = [('plants' + Q, 'genetic profiles', 'many, ends in s → s' + Q, C['green']),
            ('children' + Q + 's', 'books', 'many, no s → ' + Q + 's', C['green']),
            ('scientists', 'collected samples', 'nothing owned → no ' + Q, C['blue'])][:b + 1]
    for i, (o, th, n, c) in enumerate(rows):
        k = 1 if i < b else seg(p, .05, .45)
        if i == 2:
            if k > 0:
                text(ctx, o, 120, 200 + i * 130, 38, c, k); text(ctx, th, 120 + twidth(ctx, o, 38) + 20, 200 + i * 130, 38, C['ink'], k, 'l', False)
                text(ctx, n, 760, 200 + i * 130, 26, c, k, 'l', False)
        else:
            own(ctx, o, th, 120, 200 + i * 130, k, 38)
            text(ctx, n, 760, 200 + i * 130, 26, C['green'], k, 'l', False)
    if b == 1: text(ctx, 'childrens' + Q + ' is not a word ✗', 120, 520, 28, C['red'], seg(p, .55, .85))

def s_pron(ctx, b, p, t):
    chip(ctx, 'Pronouns never use ' + Q + ' to own', C['red'])
    if b == 0:
        for i, (a, c_, d) in enumerate([('its', 'it' + Q + 's', 'it is'), ('their', 'they' + Q + 're', 'they are'), ('whose', 'who' + Q + 's', 'who is')]):
            k = seg(p, .1 + i * .2, .3 + i * .2)
            text(ctx, a, 200, 220 + i * 100, 44, C['green'], k); text(ctx, '= owns', 360, 220 + i * 100, 28, C['mute'], k, 'l', False)
            text(ctx, c_, 640, 220 + i * 100, 44, C['org'], k); text(ctx, '= ' + d, 830, 220 + i * 100, 28, C['mute'], k, 'l', False)
        return
    passage(ctx, [('A butterfly flapping', None, None), ('it is', C['red'], 'hl'), ('wings...', None, None)], 120, 180, 900, 36, seg(p, 0, .3))
    text(ctx, 'nonsense ✗', 120, 360, 34, C['red'], seg(p, .3, .5))
    rich(ctx, [('→  ', C['mute']), ('its', C['green']), (' wings', C['ink'])], 120, 440, 46, seg(p, .55, .85))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    passage(ctx, [('Two paintings are similar in', None, None), ('their' if b else '', C['green'], 'blank'), ('use of large canvases.', None, None)], 80, 110, 1120, 30, 1 if b else seg(p, 0, .4))
    choices(ctx, ['they' + Q + 're', 'their', 'there', 'their' + Q], 80, 260, 360, 1 if b else seg(p, .45, .95), 1 if b else None, (0, 2, 3) if b else ())
    if b == 1:
        text(ctx, 'similar in "they are" use?  ✗', 500, 320, 30, C['red'], seg(p, 0, .4))
        text(ctx, 'the paintings OWN the use → their', 500, 380, 30, C['green'], seg(p, .45, .85))
    if b == 2: trap(ctx, 500, 320, 640, 'their' + Q + ' is never correct.', 'Pronouns never take ' + Q + ' to own ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('The three', None, None), ('students' + Q if b else '', C['green'], 'blank'), ('projects were displayed.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [('student' + Q + 's', C['ink']), ('     or     ', C['mute']), ('students' + Q, C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    rich(ctx, [('3 owners, ends in s  →  ', C['ink']), ('s' + Q, C['green'])], 100, 330, 38, seg(p, .1, .5))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Is the next word owned?', C['yel']), ('One: ' + Q + 's.  Many: s' + Q, C['green']), ('Pronouns never use ' + Q + ' to own', C['red'])])

SC = dict(hook=s_hook, method=s_method, one=s_one, many=s_many, pron=s_pron, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'method', 'one', 'one', 'many', 'many', 'many', 'pron', 'pron', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', method='The method', one='One owner', many='Many owners', pron='Pronouns', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Apostrophes', s_hook, {12: 5.0, 14: 1.5}, CH)
