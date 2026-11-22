import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/s5'
NAR = json.load(open(f'{D}/beats.json'))

def xs(ctx, parts, x, y, k, size=32, kx=1):
    """parts: (text, kind) kind: 'who' green box, 'mid' crossed-out gray, 'verb' yellow, 'n' normal"""
    if k <= 0: return
    xx = x
    for s, kind in parts:
        w = twidth(ctx, s, size, kind in ('who', 'verb'))
        if kind == 'who':
            rrect(ctx, xx - 6, y - size - 4, w + 12, size + 16, 8, stroke=C['green'], a=k, lw=3); text(ctx, s, xx, y, size, C['green'], k)
            text(ctx, 'WHO', xx + w / 2, y + 36, 18, C['green'], k, 'c')
        elif kind == 'mid':
            text(ctx, s, xx, y, size, C['mute'], k * (1 - .5 * kx), 'l', False)
            line(ctx, xx, y - size / 3, xx + w * kx, y - size / 3, C['red'], 3, 1, k)
        elif kind == 'verb':
            text(ctx, s, xx, y, size, C['yel'], k)
        else:
            text(ctx, s, xx, y, size, C['ink'], k, 'l', False)
        xx += w + (20 if kind == "who" else 12)

def s_hook(ctx, b, p, t):
    text(ctx, 'Subject X-Ray', 100, 210, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'The verb matches the REAL who', 102, 270, 30, C['mute'], seg(p, .1, .3), bold=False)
    for i, (h, rows, c) in enumerate([('ONE', ['is', 'has', 'runs'], C['blue']), ('MANY', ['are', 'have', 'run'], C['org'])]):
        k = seg(p, .3 + i * .25, .5 + i * .25)
        rrect(ctx, 140 + i * 420, 330, 360, 230, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, h, 320 + i * 420, 380, 32, c, k, 'c')
        text(ctx, '  ·  '.join(rows), 320 + i * 420, 470, 38, C['ink'], k, 'c')

def s_xray(ctx, b, p, t):
    chip(ctx, 'X-ray the sentence', C['blue'])
    k = seg(p, 0, .3)
    rrect(ctx, 240, 150, 800, 300, 20, fill=C['bg2'], stroke=C['blue'], a=k, lw=4)
    xs(ctx, [('The collection', 'who'), ('of rare letters', 'mid'), ('is', 'verb'), ('kept...', 'n')], 300, 320, k, 36, seg(p, .35, .7))
    text(ctx, 'see through the middle', 640, 520, 30, C['blue'], seg(p, .6, .85), 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Choices = same verb, different forms?', C['blue']), ('Cross out the middle', C['red']), ('Find the who and COUNT it', C['green'])], 200, 240, p, .05, .95, 38, 100)

def s_of(ctx, b, p, t):
    chip(ctx, '"Of" phrase in the middle', C['blue'])
    xs(ctx, [('The collection', 'who'), ('of rare letters', 'mid'), ('is' if b == 0 else 'are', 'verb' if b == 0 else 'n'), ('kept in a vault.', 'n')], 100, 260, 1, 34, seg(p, .2, .5) if b == 0 else 1)
    if b == 0: text(ctx, 'one collection → is', 100, 380, 32, C['green'], seg(p, .6, .85))
    else: trap(ctx, 100, 360, 640, '"are" matches "letters", the nearest noun.', 'Letters is inside the of-phrase ✗', seg(p, .2, .7))

def s_more(ctx, b, p, t):
    chip(ctx, 'Counting the who', C['green'])
    rows = [([('The botanist and the chemist', 'who'), ('are', 'verb'), ('on the panel.', 'n')], 'A + B = many'),
            ([('The director', 'who'), (', along with her assistants,', 'mid'), ('is', 'verb'), ('arriving.', 'n')], '"along with" is extra'),
            ([('Each', 'who'), ('of the samples', 'mid'), ('has', 'verb'), ('a label.', 'n')], 'each = one'),
            ([('There', 'n'), ('are', 'verb'), ('three reasons', 'who'), ('.', 'n')], 'who comes AFTER the verb')]
    show = {0: [0], 1: [0, 1], 2: [2, 3]}[b]
    for j, i in enumerate(show):
        parts, note = rows[i]
        k = 1 if (b == 1 and j == 0) else seg(p, .05 + j * .35, .35 + j * .35)
        xs(ctx, parts, 80, 230 + j * 150, k, 30)
        text(ctx, note, 80, 300 + j * 150, 24, C['yel'], k, 'l', False)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    if b == 0:
        passage(ctx, [('Throat singing—a tradition with two performers—', None, None), ('', C['yel'], 'blank'), ('an advocate.', None, None)], 80, 110, 1120, 30, seg(p, 0, .5))
        choices(ctx, ['has found', 'find', 'have found', 'were finding'], 80, 260, 400, seg(p, .5, .95)); return
    xs(ctx, [('Throat singing', 'who'), ('—a tradition with two performers—', 'mid'), ('has found', 'verb'), ('an advocate.', 'n')], 80, 200, 1, 28, seg(p, 0, .4) if b == 1 else 1)
    choices(ctx, ['has found', 'find', 'have found', 'were finding'], 80, 280, 400, 1, 0, (1, 2, 3))
    if b == 1: text(ctx, 'one tradition → has', 540, 340, 30, C['green'], seg(p, .5, .8))
    if b == 2: trap(ctx, 540, 320, 640, '"two performers" is inside the dashes.', 'It\'s extra. Who = throat singing ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('The list of ingredients', None, None), ('', C['yel'], 'blank'), ('on the back of the box.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [('is', C['ink']), ('     or     ', C['mute']), ('are', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    xs(ctx, [('The list', 'who'), ('of ingredients', 'mid'), ('is', 'verb'), ('on the back of the box.', 'n')], 100, 330, seg(p, 0, .4), 32)

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Cross out the middle', C['red']), ('Find the real who and count it', C['green']), ('Never match the nearest noun', C['yel'])])

SC = dict(hook=s_hook, xray=s_xray, method=s_method, of=s_of, more=s_more, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'xray', 'method', 'of', 'of', 'more', 'more', 'more', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', xray='X-ray it', method='The method', of='"Of" phrases', more='Counting the who', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Subject-verb', s_hook, {11: 5.0, 13: 1.5}, CH)
