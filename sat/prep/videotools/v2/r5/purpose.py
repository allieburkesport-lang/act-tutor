import sys; sys.path.insert(0, '/home/claude/v2')
from common import *
D = '/home/claude/v2/r5'
NAR = json.load(open(f'{D}/beats.json'))

def card(ctx, x, y, w, h, title, c, k, lines=(), size=24):
    if k <= 0: return
    rrect(ctx, x, y, w, h, 14, fill=C['bg2'], stroke=c, a=k, lw=3)
    if title: text(ctx, title, x + 20, y + 32, 16, c, k)
    for i, (s, cc) in enumerate(lines): text(ctx, s, x + 20, y + 70 + i * (size + 12), size, cc, k, 'l', False)
def bubble(ctx, x, y, w, h, c, k, tail_left=True):
    if k <= 0: return
    rrect(ctx, x, y, w, h, 22, fill=C['bg2'], stroke=c, a=k, lw=3)
    tx = x + 50 if tail_left else x + w - 50
    col(ctx, c, k); ctx.move_to(tx - 14, y + h); ctx.line_to(tx, y + h + 26); ctx.line_to(tx + 14, y + h); ctx.close_path(); ctx.fill()
def person(ctx, x, y, c, k, s=1):
    if k <= 0: return
    disc(ctx, x, y, 26 * s, c, k); rrect(ctx, x - 34 * s, y + 32 * s, 68 * s, 80 * s, 26 * s, fill=c, a=k)
def hammer(ctx, x, y, k):
    if k <= 0: return
    rrect(ctx, x - 8, y, 16, 150, 6, fill=C['brown'], a=k)
    rrect(ctx, x - 50, y - 30, 100, 40, 8, fill=C['mute'], a=k)
def xout(ctx, x, y, w, k): line(ctx, x, y, x + w, y - 6, C['red'], 4, k)

def s_hook(ctx, b, p, t):
    text(ctx, 'Purpose & Two Texts', 100, 230, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'Why did the author write it?', 102, 290, 30, C['mute'], seg(p, .1, .3), bold=False)
    for i, (v, c) in enumerate([('to challenge', C['red']), ('to explain', C['blue']), ('to compare', C['green']), ('to describe', C['yel'])]):
        k = seg(p, .35 + i * .12, .5 + i * .12); w = twidth(ctx, v, 30) + 40
        rrect(ctx, 100 + [0, 270, 520, 790][i], 380, w, 60, 30, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, v, 120 + [0, 270, 520, 790][i], 420, 30, c, k)
    text(ctx, 'Answer with a VERB.', 100, 530, 38, C['yel'], seg(p, .85, 1))

def s_tool(ctx, b, p, t):
    chip(ctx, 'Purpose = the job of the text', C['blue'])
    if b == 0:
        hammer(ctx, 260, 260, seg(p, 0, .2))
        text(ctx, "job: to pound nails", 200, 470, 30, C['mute'], seg(p, .15, .35), 'l', False)
        card(ctx, 560, 200, 600, 300, 'A TEXT', C['blue'], seg(p, .35, .5))
        for i, (v, c) in enumerate([('to explain', C['blue']), ('to challenge', C['red']), ('to compare', C['green']), ('to describe', C['yel'])]):
            text(ctx, 'job:  ' + v, 600, 290 + i * 52, 32, c, seg(p, .5 + i * .1, .6 + i * .1))
        return
    if b == 1:
        text(ctx, 'Before you read the choices,', 640, 220, 36, C['ink'], seg(p, 0, .3), 'c')
        text(ctx, 'say the job as a verb:', 640, 270, 36, C['ink'], seg(p, .1, .4), 'c')
        for i, (v, c) in enumerate([('To challenge.', C['red']), ('To explain.', C['blue']), ('To compare.', C['green'])]):
            text(ctx, v, 640, 370 + i * 64, 46, c, seg(p, .35 + i * .2, .5 + i * .2), 'c')
        return
    # b == 2 : whole text, not one sentence
    card(ctx, 280, 150, 720, 330, 'THE WHOLE TEXT', C['green'], 1)
    for i in range(5):
        c = C['red'] if i == 2 else C['mute']
        rrect(ctx, 320, 210 + i * 50, 640 - (i % 2) * 120, 18, 9, fill=c, a=seg(p, i * .05, i * .05 + .2) * (.9 if i == 2 else .5))
    text(ctx, 'one sentence ✗', 990, 268, 26, C['red'], seg(p, .35, .55))
    text(ctx, 'the whole thing ✓', 640, 540, 40, C['green'], seg(p, .6, .85), 'c')

def s_desert(ctx, b, p, t):
    chip(ctx, 'Find the job', C['red'])
    card(ctx, 80, 120, 1120, 150, 'THE TEXT', C['mute'], 1 if b > 0 else seg(p, 0, .15))
    write(ctx, 'Many people think deserts are lifeless.', 110, 215, 30, C['ink'], seg(p, .1, .5) if b == 0 else 1)
    write(ctx, 'In fact, the Sonoran Desert holds 3,500 plant species.', 110, 255, 30, C['ink'], seg(p, .45, .9) if b == 0 else 1)
    if 1 <= b < 3:
        k = kk(b, 1, p, 0, .4)
        rrect(ctx, 100, 300, 520, 80, 14, fill=C['bg2'], stroke=C['blue'], a=k, lw=3); text(ctx, 'common belief', 360, 350, 30, C['blue'], k, 'c')
        text(ctx, '+', 660, 352, 46, C['ink'], kk(b, 1, p, .3, .5), 'c')
        rrect(ctx, 700, 300, 480, 80, 14, fill=C['bg2'], stroke=C['org'], a=kk(b, 1, p, .35, .6), lw=3); text(ctx, 'fact that pushes back', 940, 350, 30, C['org'], kk(b, 1, p, .35, .6), 'c')
        text(ctx, '= to challenge', 640, 440, 44, C['red'], kk(b, 1, p, .7, .95), 'c')
    if b >= 2:
        answer(ctx, 'To challenge a common view by showing variety', 160, 470, 960, kk(b, 2, p, .2, .6))
    if b >= 3:
        trap(ctx, 160, 300, 960, '"To explain how cactuses store water" is never in the text.', 'Not in the text? Cross it out ✗', p, 22)

def s_struct(ctx, b, p, t):
    chip(ctx, 'Structure = how the parts are arranged', C['org'])
    pats = [('claim', 'evidence', C['blue']), ('problem', 'solution', C['green']), ('view A', 'view B', C['red'])]
    if b == 0:
        for i, (a1, a2, c) in enumerate(pats):
            k = seg(p, .15 + i * .25, .35 + i * .25); y = 170 + i * 120
            rrect(ctx, 260, y, 280, 80, 14, fill=C['bg2'], stroke=c, a=k, lw=3); text(ctx, a1, 400, y + 50, 32, c, k, 'c')
            text(ctx, '→' if i < 2 else '⟷', 640, y + 54, 46, C['ink'], k, 'c')
            rrect(ctx, 740, y, 280, 80, 14, fill=C['bg2'], stroke=c, a=k, lw=3); text(ctx, a2, 880, y + 50, 32, c, k, 'c')
        return
    person(ctx, 300, 250, C['blue'], seg(p, 0, .2), 1.3); person(ctx, 980, 250, C['org'], seg(p, .35, .55), 1.3)
    bubble(ctx, 110, 90, 400, 100, C['blue'], seg(p, .05, .25)); text(ctx, 'Great individuals', 310, 135, 26, C['blue'], seg(p, .1, .3), 'c'); text(ctx, 'shape history.', 310, 170, 26, C['blue'], seg(p, .1, .3), 'c')
    bubble(ctx, 770, 90, 400, 100, C['org'], seg(p, .4, .6), False); text(ctx, 'No. Society', 970, 135, 26, C['org'], seg(p, .45, .65), 'c'); text(ctx, 'shapes history.', 970, 170, 26, C['org'], seg(p, .45, .65), 'c')
    text(ctx, 'Carlyle', 300, 420, 24, C['mute'], seg(p, .1, .3), 'c', False); text(ctx, 'Spencer', 980, 420, 24, C['mute'], seg(p, .45, .65), 'c', False)
    text(ctx, '⟷', 640, 330, 70, C['red'], seg(p, .65, .8), 'c')
    text(ctx, 'two opposite views', 640, 500, 40, C['red'], seg(p, .75, .95), 'c')

def s_friends(ctx, b, p, t):
    chip(ctx, 'Two texts = two friends talking', C['green'])
    person(ctx, 220, 300, C['blue'], 1 if b else seg(p, 0, .2), 1.2); person(ctx, 1060, 300, C['org'], 1 if b else seg(p, .3, .5), 1.2)
    text(ctx, 'Text 1', 220, 470, 26, C['blue'], 1 if b else seg(p, .1, .3), 'c'); text(ctx, 'Text 2', 1060, 470, 26, C['org'], 1 if b else seg(p, .4, .6), 'c')
    bubble(ctx, 100, 140, 300, 90, C['blue'], 1 if b else seg(p, .15, .35)); text(ctx, 'Here is my point.', 250, 195, 26, C['blue'], 1 if b else seg(p, .2, .4), 'c')
    if b == 0:
        text(ctx, '→  answers  →', 640, 320, 34, C['mute'], seg(p, .55, .8), 'c', False); return
    opts = [('YES', 'agrees', C['green']), ('NO', 'disagrees', C['red']), ('YES, BUT', 'agrees + adds', C['yel'])]
    for i, (big, small, c) in enumerate(opts):
        k = seg(p, .1 + i * .25, .3 + i * .25)
        rrect(ctx, 470, 150 + i * 120, 340, 96, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        text(ctx, big, 640, 200 + i * 120, 40, c, k, 'c'); text(ctx, small, 640, 232 + i * 120, 20, C['mute'], k, 'c', False)

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    card(ctx, 60, 100, 560, 210, 'TEXT 1', C['blue'], 1 if b else seg(p, 0, .1),
         [('Children learn a language fastest', C['ink']), ('by speaking it every day.', C['ink'])], 24)
    card(ctx, 660, 100, 560, 210, 'TEXT 2', C['org'], 1 if b else seg(p, .3, .4),
         [('Daily speaking matters, but children', C['ink']), ('first need weeks of listening.', C['ink'])], 24)
    write(ctx, 'How would the author of Text 2 respond to Text 1?', 80, 360, 28, C['yel'], seg(p, .7, .95) if b == 0 else 1)
    if b >= 1:
        rich(ctx, [('Step 1  ', C['mute']), ('Text 1 point: ', C['ink']), ('speak every day', C['blue'])], 80, 420, 30, kk(b, 1, p, 0, .6))
        rrect(ctx, 72, 140, 500, 90, 10, stroke=C['blue'], lw=3, a=kk(b, 1, p, .5, .8))
    if b >= 2:
        rich(ctx, [('Step 2  ', C['mute']), ('"Daily speaking matters" = ', C['ink']), ('YES', C['green'])], 80, 470, 30, kk(b, 2, p, 0, .6))
        rrect(ctx, 672, 142, 470, 42, 10, stroke=C['green'], lw=3, a=kk(b, 2, p, .5, .8))
    if b >= 3:
        rich(ctx, [('Step 3  ', C['mute']), ('"but listen first" = ', C['ink']), ('YES, BUT', C['yel'])], 80, 520, 30, kk(b, 3, p, 0, .5))
        answer(ctx, 'It accepts the point but adds a condition', 690, 395, 530, kk(b, 3, p, .55, .85))
    if b >= 4:
        trap(ctx, 690, 478, 530, '"Completely rejects Text 1" is too extreme.', 'Text 2 said YES to speaking ✗', p, 21)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    card(ctx, 60, 110, 560, 170, 'TEXT 1', C['blue'], 1, [('One microbe survives extreme heat.', C['ink'])], 24)
    card(ctx, 660, 110, 560, 170, 'TEXT 2', C['org'], 1, [('Another microbe resists radiation', C['ink']), ('in the same way.', C['ink'])], 24)
    write(ctx, 'How does Text 2 relate to Text 1?', 80, 340, 30, C['yel'], seg(p, .3, .6) if b == 0 else 1)
    if b == 0:
        text(ctx, '⏸  Pause and decide: yes, no, or yes, but?', 80, 420, 32, C['yel'], seg(p, .6, .8)); return
    rich(ctx, [('YES, AND', C['green']), (': a similar case', C['ink'])], 80, 405, 38, seg(p, 0, .3))
    answer(ctx, 'Text 2 extends Text 1 with a comparable case', 80, 428, 700, seg(p, .2, .45))
    trap(ctx, 80, 502, 700, '"The second microbe is harmed"', 'Never said in the text ✗', seg(p, .55, 1))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Name the purpose with a verb', C['blue']), ('It must fit the WHOLE text', C['green']), ('Two texts: yes, no, or yes, but', C['yel'])])

SC = dict(hook=s_hook, tool=s_tool, desert=s_desert, struct=s_struct, friends=s_friends, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook'] + ['tool'] * 3 + ['desert'] * 4 + ['struct'] * 2 + ['friends'] * 2 + ['sat'] * 5 + ['turn'] * 2 + ['recap']
CH = dict(hook='The big idea: answer with a verb', tool='Purpose = the job of the text', desert='Example: belief + pushback', struct='Structure patterns', friends='Two texts: yes, no, yes but', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading · Purpose & Two Texts', s_hook, {17: 5.0, 19: 1.5}, CH)
