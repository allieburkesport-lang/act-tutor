import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/r1'
NAR = json.load(open(f'{D}/beats.json'))

def myword(ctx, s, x, y, k):
    if k <= 0: return
    text(ctx, 'my word:', x, y, 24, C['mute'], k, 'l', False)
    text(ctx, s, x + 110, y, 30, C['yel'], k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Words in Context', 100, 210, 66, C['ink'], seg(p, 0, .12))
    text(ctx, 'The clue picks the word. Not the fanciest word.', 102, 270, 28, C['mute'], seg(p, .1, .3), bold=False)
    passage(ctx, [('The plan was', None, None), ('', C['yel'], 'blank'), (': every part had been tested.', None, None)], 100, 340, 820, 34, seg(p, .3, .5))
    for i, (w_, c) in enumerate([('fancy?', C['red']), ('clue!', C['green'])]):
        k = seg(p, .55 + i * .2, .7 + i * .2)
        rrect(ctx, 960, 340 + i * 90, 220, 66, 33, fill=C['bg2'], stroke=c, a=k, lw=3); text(ctx, w_, 1070, 384 + i * 90, 30, c, k, 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Cover the choices', C['blue']), ('Find the clue', C['green']), ('Say your own simple word', C['yel']), ('Pick the closest match', C['org'])], 220, 220, p, .05, .95, 38, 90)

def s_ex1(ctx, b, p, t):
    chip(ctx, 'Example clue', C['green'])
    fill = 'unrest' if b else ''
    hl = 'hl' if b else None
    passage(ctx, [('Foreign problems led to', None, None), (fill, C['green'], 'blank'), ('within Russia. For instance,', None, None), ('protests broke out.', C['green'], hl)], 100, 160, 1080, 34, 1 if b else seg(p, 0, .4))
    if b:
        myword(ctx, 'trouble', 120, 400, seg(p, .3, .55))
        rich(ctx, [('→  ', C['mute']), ('unrest', C['green'])], 120, 470, 40, seg(p, .65, .9))

def s_kinds(ctx, b, p, t):
    chip(ctx, 'Kinds of clues', C['blue'])
    rows = [(':  colon', 'explains what came before', C['blue']), ('whereas / unlike', 'flip to the OPPOSITE', C['red']), ('effect', 'tells you the cause', C['green'])]
    for i, (a, d, c) in enumerate(rows):
        k = seg(p, .1 + i * .25, .3 + i * .25)
        rrect(ctx, 160, 180 + i * 120, 960, 90, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, a, 200, 238 + i * 120, 34, c, k); text(ctx, d, 600, 238 + i * 120, 30, C['ink'], k, 'l', False)

def s_unlike(ctx, b, p, t):
    chip(ctx, '"Unlike" clue = opposite', C['red'])
    fill = 'reserved' if b >= 1 else ''
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('Unlike', C['red'], hl), ('her', None, None), ('outspoken', C['red'], hl), ('colleagues, the physicist was', None, None), (fill, C['green'], 'blank'), (', rarely speaking to reporters.', None, None)], 100, 160, 1080, 34, 1 if b else seg(p, 0, .4))
    if b >= 1:
        rich(ctx, [('opposite of outspoken  →  ', C['ink'])], 120, 400, 30, 1 if b > 1 else seg(p, 0, .3))
        myword(ctx, 'quiet', 520, 400, 1 if b > 1 else seg(p, .3, .5))
        rich(ctx, [('→  ', C['mute']), ('reserved', C['green'])], 120, 460, 40, 1 if b > 1 else seg(p, .6, .85))
    if b == 2: trap(ctx, 600, 440, 560, 'Boastful = SAME as outspoken.', '"Unlike" needs the opposite ✗', p)

def s_effect(ctx, b, p, t):
    chip(ctx, 'Effect clue', C['green'])
    fill = 'undermined' if b else ''
    hl = 'hl' if b else None
    passage(ctx, [('The new evidence', None, None), (fill, C['green'], 'blank'), ('the old theory;', None, None), ('researchers could no longer accept it.', C['green'], hl)], 100, 160, 1080, 34, 1 if b else seg(p, 0, .4))
    if b:
        myword(ctx, 'weakened', 120, 400, seg(p, .1, .35))
        rich(ctx, [('→  ', C['mute']), ('undermined', C['green'])], 120, 460, 40, seg(p, .35, .6))
        rich(ctx, [('confirmed', C['red']), ('  = the exact opposite ✗', C['mute'])], 120, 530, 30, seg(p, .7, .9))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    fill = 'sound' if b >= 1 else ''
    hl = 'hl' if b >= 1 else None
    passage(ctx, [('The architect\'s plan was', None, None), (fill, C['green'], 'blank'), (':', None, None), ('every part had been tested.', C['green'], hl)], 80, 110, 1120, 32, 1 if b else seg(p, 0, .4))
    choices(ctx, ['noisy', 'sound', 'loud', 'silent'], 80, 260, 420, 1 if b else seg(p, .5, .95), 1 if b >= 1 else None, (0, 2, 3) if b >= 1 else ())
    if b >= 1:
        myword(ctx, 'solid', 580, 300, 1 if b > 1 else seg(p, .2, .45))
        write(ctx, 'sound = sensible, reliable', 580, 360, 30, C['green'], 1 if b > 1 else seg(p, .5, .8))
    if b == 2: trap(ctx, 580, 400, 600, 'Common word, unusual meaning.', 'Use the meaning the clue supports ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    fill = 'twofold' if b else ''
    hl = 'hl' if b else None
    passage(ctx, [('The play served a', None, None), (fill, C['green'], 'blank'), ('purpose:', None, None), ('it criticized one thing and showed an alternative.', C['green'], hl)], 100, 160, 1080, 34, 1 if b else seg(p, 0, .4))
    if b == 0:
        text(ctx, '⏸  Pause. Say your own word first.', 120, 420, 34, C['yel'], seg(p, .6, .8)); return
    myword(ctx, 'two-part', 120, 400, seg(p, .1, .3))
    rich(ctx, [('→  ', C['mute']), ('twofold', C['green'])], 120, 460, 40, seg(p, .3, .5))
    trap(ctx, 600, 400, 520, 'External? Sounds smart.', 'Nothing about "outside" ✗', seg(p, .6, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Cover the choices, find the clue', C['green']), ('Say your own simple word', C['yel']), ('Fancy ≠ correct', C['red'])])

SC = dict(hook=s_hook, method=s_method, ex1=s_ex1, kinds=s_kinds, unlike=s_unlike, effect=s_effect, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'method', 'ex1', 'ex1', 'kinds', 'unlike', 'unlike', 'unlike', 'effect', 'effect', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', method='The method', ex1='Find the clue', kinds='Kinds of clues', unlike='"Unlike" clues', effect='Effect clues', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Words in context', s_hook, {13: 5.0, 15: 1.5}, CH)
