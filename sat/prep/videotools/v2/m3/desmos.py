import sys; sys.path.insert(0, '/home/claude/v2')
from strat import *
D = '/home/claude/v2/m3'

def _graph(ctx, s, p):
    chip(ctx, s['chip'], s.get('cc', C['blue']))
    rrect(ctx, 60, 110, 420, 440, 14, fill=C['bg2'], stroke=C['mute'], lw=1)
    text(ctx, 'Desmos', 80, 146, 20, C['green'], 1)
    for i, (e, c) in enumerate(s['eqs']):
        rrect(ctx, 76, 166 + i * 70, 388, 58, 8, fill=C['bg'], stroke=c, lw=2, a=seg(p, .05 + i * .1, .2 + i * .1))
        text(ctx, e, 92, 204 + i * 70, 22, C['ink'], seg(p, .05 + i * .1, .2 + i * .1), 'l', False)
    G = Graph(540, 110, 660, 440, s['xr'], s['yr']); G.axes(ctx, 1)
    for i, (f, c) in enumerate(s['fs']): G.plot(ctx, f, c, 4, seg(p, .2 + i * .15, .5 + i * .15))
    for (x, y, lab) in s.get('pts', []):
        k = seg(p, .6, .8); G.dot(ctx, x, y, C['yel'], k, 10)
        text(ctx, lab, G.X(x) + 14, G.Y(y) - 14, 24, C['yel'], k)
    if s.get('note'): text(ctx, s['note'], 80, 520, 26, C['green'], seg(p, .7, .9))
    if s.get('trap'): trap(ctx, 76, 380, 400, s['trap'][0], s['trap'][1], p, 18)
KIND['graph'] = _graph

EQ = ('y = 0.10(9) + 0.20x', C['blue']), ('y = 0.17(9 + x)', C['org'])
FS = [(lambda x: 0.9 + 0.2 * x, C['blue']), (lambda x: 0.17 * (9 + x), C['org'])]
Z = [(lambda x: x * x - x - 12, C['blue'])]
S = [
 dict(kind='title', title='Input: Put It in Desmos', sub='Don\'t solve in your head', big=[('type it  →  click it  →  done', C['green'])], ch='The big idea'),
 dict(kind='rows', chip='Desmos can...', cc=C['green'], rows=[('solve equations', 'where two graphs cross', C['blue']), ('find zeros', 'where it crosses the x-axis', C['org']), ('find min / max', 'click the vertex', C['green'])]),
 dict(kind='steps', steps=[('Can you type it? Type it.', C['blue']), ('Click the gray points Desmos shows', C['yel']), ('No mental math = no slips', C['green'])], ch='The method'),
 dict(kind='graph', chip='Solve: left = y1, right = y2', eqs=list(EQ), fs=FS, xr=(0, 30), yr=(0, 8), pts=[], note='where they cross = the answer', ch='Solve an equation'),
 dict(kind='graph', chip='Solve: left = y1, right = y2', eqs=list(EQ), fs=FS, xr=(0, 30), yr=(0, 8), pts=[(21, 5.1, 'x = 21')]),
 dict(kind='graph', chip='Solve: left = y1, right = y2', eqs=list(EQ), fs=FS, xr=(0, 30), yr=(0, 8), pts=[(21, 5.1, 'x = 21')], trap=('22 = a mental-math slip.', 'Desmos doesn\'t slip ✗')),
 dict(kind='graph', chip='Min or max: click the vertex', cc=C['green'], eqs=[('y = x² − 8.5x + 20', C['blue'])], fs=[(lambda x: x * x - 8.5 * x + 20, C['blue'])], xr=(0, 9), yr=(0, 22), pts=[(4.25, 1.94, '(4.25, 1.94)')], note='not a whole number!', ch='Min and max'),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q='What are the zeros of y = x² − x − 12?', newq=True, ch='SAT question'),
 dict(kind='graph', chip='SAT-style question', cc=C['yel'], eqs=[('y = x² − x − 12', C['blue'])], fs=Z, xr=(-6, 6), yr=(-14, 10), pts=[(4, 0, 'x = 4'), (-3, 0, 'x = −3')], note='zeros: 4 and −3'),
 dict(kind='graph', chip='SAT-style question', cc=C['yel'], eqs=[('y = x² − x − 12', C['blue'])], fs=Z, xr=(-6, 6), yr=(-14, 10), pts=[(4, 0, 'x = 4'), (-3, 0, 'x = −3')], trap=('3 and −4: signs flipped.', '9 − 3 − 12 = −6, not 0 ✗')),
 dict(kind='q', chip='Your turn', cc=C['yel'], q='A parabola has zeros at 2 and 10. What is the x-value of the vertex?', newq=True, pause='Pause and solve', ch='Your turn'),
 dict(kind='q', chip='Your turn', cc=C['yel'], q='A parabola has zeros at 2 and 10. What is the x-value of the vertex?', work=['vertex = halfway between the zeros', [('(2 + 10) ÷ 2 = ', C['ink']), ('6', C['green'])]], trap=('10 − 2 = 8 is the distance.', 'Average the zeros ✗'), trap_at=(100, 340)),
 dict(kind='recap', items=[('Type it in Desmos', C['green']), ('Click the points it shows', C['yel']), ('No math in your head', C['red'])], ch='Lock it in'),
]
if __name__ == '__main__':
    build(D, 'SAT Strategy · Desmos', S, {10: 5.0, 12: 1.5})
