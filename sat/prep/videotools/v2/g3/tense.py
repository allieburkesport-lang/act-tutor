import sys; sys.path.insert(0, '/home/claude/v2')
from rw import *
D = '/home/claude/v2/g3'
NAR = json.load(open(f'{D}/beats.json'))

def stamp(ctx, s, x, y, k, c=None):
    if k <= 0: return
    c = c or C['org']; w = twidth(ctx, s, 26) + 30
    rrect(ctx, x, y - 32, w, 44, 22, fill=C['bg2'], stroke=c, a=k, lw=3); text(ctx, '⏱ ' + s if False else s, x + 15, y, 26, c, k)
    return w

def tl(ctx, k, marks):
    """timeline with marks: list of (pos 0..1, label, color, kind) kind 'dot' or 'span' (pos=(a,b))"""
    if k <= 0: return
    x0, x1, y = 160, 1120, 470
    line(ctx, x0, y, x1, y, C['mute'], 3, k)
    text(ctx, 'past', x0, y + 40, 22, C['mute'], k, 'l', False); text(ctx, 'NOW', x1, y + 40, 22, C['yel'], k, 'r'); disc(ctx, x1, y, 8, C['yel'], k)
    for m in marks:
        pos, lab, c, kind = m
        if kind == 'span':
            a, b_ = pos; line(ctx, x0 + (x1 - x0) * a, y - 20, x0 + (x1 - x0) * b_, y - 20, c, 8, k)
            text(ctx, lab, x0 + (x1 - x0) * (a + b_) / 2, y - 40, 22, c, k, 'c')
        else:
            X = x0 + (x1 - x0) * pos; disc(ctx, X, y, 10, c, k); text(ctx, lab, X, y - 26, 22, c, k, 'c')

def s_hook(ctx, b, p, t):
    text(ctx, 'Verb Tense', 100, 200, 70, C['ink'], seg(p, 0, .12))
    text(ctx, 'Find the time clue, then match the verb', 102, 260, 30, C['mute'], seg(p, .1, .3), bold=False)
    for i, (s, v) in enumerate([('In 1969', 'landed'), ('Since 2020', 'has won'), ('By the time ... arrived', 'had ended')]):
        k = seg(p, .3 + i * .2, .5 + i * .2)
        w = stamp(ctx, s, 100, 350 + i * 80, k) or 0
        text(ctx, '→  ' + v, 140 + w, 350 + i * 80, 30, C['green'], k)

def s_photo(ctx, b, p, t):
    chip(ctx, 'Read the time stamp', C['blue'])
    k = seg(p, 0, .3)
    rrect(ctx, 400, 160, 480, 320, 16, fill=C['bg2'], stroke=C['ink'], a=k, lw=4)
    rrect(ctx, 430, 190, 420, 230, 8, fill=C['blue'], a=.25 * k)
    text(ctx, 'JUL 20 1969', 820, 455, 26, C['org'], seg(p, .35, .6), 'r')
    text(ctx, 'when is this happening?', 640, 560, 32, C['yel'], seg(p, .6, .85), 'c')

def s_method(ctx, b, p, t):
    chip(ctx, 'The method', C['yel'])
    steps(ctx, [('Circle the time clue', C['org']), ('date · since · by the time · other verbs', C['mute']), ('Pick the tense that matches', C['green'])], 200, 240, p, .05, .95, 36, 100)

def s_rules(ctx, b, p, t):
    chip(ctx, 'Time clue → tense', C['org'])
    if b == 0:
        passage(ctx, [('In 1969,', C['org'], 'hl'), ('astronauts', None, None), ('landed', C['green'], 'blank'), ('on the moon.', None, None)], 80, 130, 1120, 32, seg(p, 0, .4))
        tl(ctx, seg(p, .4, .7), [(.2, '1969', C['org'], 'dot')]); text(ctx, 'over → past: landed', 80, 330, 30, C['green'], seg(p, .65, .9)); return
    if b in (1, 2):
        passage(ctx, [('Since 2020,', C['org'], 'hl'), ('the museum', None, None), ('has won' if b == 1 else 'won', C['green'] if b == 1 else C['red'], 'blank'), ('three awards.', None, None)], 80, 130, 1120, 32, 1 if b == 2 else seg(p, 0, .4))
        tl(ctx, 1 if b == 2 else seg(p, .35, .6), [((.55, 1), 'since → up to NOW', C['green'], 'span')])
        if b == 1: text(ctx, 'since → has / have', 80, 330, 30, C['green'], seg(p, .55, .85))
        else: trap(ctx, 80, 290, 600, 'Plain past "won" stops in the past.', 'Since needs has / have ✗', p)
        return
    if b == 3:
        passage(ctx, [('By the time the rescue team arrived,', C['org'], 'hl'), ('the storm', None, None), ('had ended', C['green'], 'blank'), ('.', None, None)], 80, 130, 1120, 32, seg(p, 0, .4))
        tl(ctx, seg(p, .35, .6), [(.3, 'storm ended', C['green'], 'dot'), (.6, 'team arrived', C['org'], 'dot')])
        text(ctx, 'had = the EARLIER of two past events', 80, 330, 30, C['green'], seg(p, .6, .85)); return
    passage(ctx, [('This tool', None, None), ('measures', C['green'], 'blank'), ('quality of life.', None, None)], 80, 130, 1120, 32, seg(p, 0, .4))
    text(ctx, 'general fact, true now → present', 80, 300, 30, C['green'], seg(p, .4, .7))

def s_sat(ctx, b, p, t):
    chip(ctx, 'SAT-style question', C['yel'])
    fill = 'was studying' if b else ''
    passage(ctx, [('The researcher', None, None), (fill, C['green'], 'blank'), ('Saturn\'s rings when she', None, None), ('made', C['org'], 'hl' if b else None), ('a discovery.', None, None)], 80, 110, 1120, 30, 1 if b else seg(p, 0, .4))
    choices(ctx, ['studies', 'was studying', 'has studied', 'will study'], 80, 260, 400, 1 if b else seg(p, .5, .95), 1 if b else None, (0, 2, 3) if b else ())
    if b == 1:
        text(ctx, '"made" = past', 540, 310, 30, C['org'], seg(p, 0, .3))
        text(ctx, 'in the middle of it → was + -ing', 540, 370, 30, C['green'], seg(p, .35, .7))
    if b == 2: trap(ctx, 540, 300, 600, '"studies" is present.', 'Clashes with past "made" ✗', p)

def s_turn(ctx, b, p, t):
    chip(ctx, 'Your turn', C['yel'])
    passage(ctx, [('Since 2010,', C['org'], 'hl' if b else None), ('the city', None, None), ('has built' if b else '', C['green'], 'blank'), ('five new parks.', None, None)], 80, 130, 1120, 32, 1 if b else seg(p, 0, .3))
    if b == 0:
        rich(ctx, [('built', C['ink']), ('     or     ', C['mute']), ('has built', C['ink'])], 100, 330, 44, seg(p, .4, .6))
        text(ctx, '⏸  Pause and pick', 100, 440, 34, C['yel'], seg(p, .7, .9)); return
    text(ctx, 'since → up to now → has built', 100, 330, 32, C['green'], seg(p, 0, .4))

def s_recap(ctx, b, p, t):
    recap(ctx, p, [('Circle the time clue', C['org']), ('Since → has / have', C['green']), ('By the time (past) → had', C['blue'])])

SC = dict(hook=s_hook, photo=s_photo, method=s_method, rules=s_rules, sat=s_sat, turn=s_turn, recap=s_recap)
PLAN = ['hook', 'photo', 'method', 'rules', 'rules', 'rules', 'rules', 'rules', 'sat', 'sat', 'sat', 'turn', 'turn', 'recap']
CH = dict(hook='The big idea', photo='Time stamp', method='The method', rules='Time clues', sat='SAT question', turn='Your turn', recap='Lock it in')
if __name__ == '__main__':
    run(D, NAR, PLAN, SC, 'SAT Reading & Writing · Verb tense', s_hook, {11: 5.0, 13: 1.5}, CH)
