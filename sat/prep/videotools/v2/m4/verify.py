import sys; sys.path.insert(0, '/home/claude/v2')
from strat import *
D = '/home/claude/v2/m4'
QL = 'Which line has slope −½ and passes through (4, 1)?'
QE = ['3k + 90 < 0.', 'What is the greatest possible integer k?']
QN = ['2(x + 3) = 2x + k has NO solution.', 'Which could be k?']
QT = ['x + 4 > 10.', 'What is the smallest integer x?']
S = [
 dict(kind='title', title='Verify & Check Edges', sub='Plug it back in before you click', big=[('plug in  ✓', C['green']), ('test the edge number', C['yel'])], ch='The big idea'),
 dict(kind='big', chip='Check before you hand it in', cc=C['green'], lines=[('10 seconds', C['yel'], 60), ('catches the mistakes', C['ink'], 36), ('that cost points', C['red'], 36)]),
 dict(kind='big', chip='Two choices look right?', cc=C['blue'], lines=[('A ✓?     B ✓?', C['ink'], 56), ('plug in → one fails', C['green'], 40)]),
 dict(kind='q', chip='Plug the point in', q=QL, newq=True, work=['A:  y = −½x + 1', 'B:  y = −½x + 3'], ch='Plug it in'),
 dict(kind='q', chip='Plug the point in', q=QL, work=[[('A:  −½(4) + 1 = ', C['ink']), ('−1 ✗', C['red'])], [('B:  −½(4) + 3 = ', C['ink']), ('1 ✓', C['green'])]], ans='y = −½x + 3', newans=True),
 dict(kind='q', chip='Edge numbers', cc=C['org'], q=QE, newq=True, work=['3k < −90  →  k < −30'], ch='Edge numbers'),
 dict(kind='q', chip='Edge numbers', cc=C['org'], q=QE, work=['3k < −90  →  k < −30', [('test −30:  3(−30) + 90 = 0.   0 < 0?  ', C['ink']), ('No ✗', C['red'])], [('step past the edge:  ', C['ink']), ('k = −31', C['green'])]], old=1),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QN, newq=True, ch='SAT question'),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QN, work=['left side: 2x + 6', [('k = 6  →  2x + 6 = 2x + 6  →  ', C['ink']), ('always true', C['red'])]], trap=('k = 6 gives INFINITELY many.', 'Not "no solution" ✗'), trap_at=(100, 360)),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QN, work=['left side: 2x + 6', [('k = 5  →  2x + 6 = 2x + 5  →  ', C['ink']), ('never true ✓', C['green'])]], ans='any k except 6, e.g. 5', newans=True),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=QT, newq=True, pause='Pause and solve', ch='Your turn'),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=QT, work=['x > 6', [('test 6:  10 > 10?  ', C['ink']), ('No ✗', C['red'])], [('smallest integer: ', C['ink']), ('7', C['green'])]]),
 dict(kind='recap', items=[('Plug your answer back in', C['green']), ('Test the edge number itself', C['yel']), ('< or >: the edge doesn\'t count', C['red'])], ch='Lock it in'),
]
if __name__ == '__main__':
    build(D, 'SAT Strategy · Verify', S, {10: 5.0, 12: 1.5})
