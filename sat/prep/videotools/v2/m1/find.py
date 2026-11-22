import sys; sys.path.insert(0, '/home/claude/v2')
from strat import *
D = '/home/claude/v2/m1'
Q1 = 'If 3x + 2 = 29, what is x − 5?'
Q2 = 'A circle has area 49π. What is its diameter?'
Q3 = ['1,200 students took a test and 92% passed.', 'How many did NOT pass?']
S = [
 dict(kind='title', title='Define FIND', sub='Know the exact thing they ask for', big=[('FIND: ________', C['yel']), ('then stop when you reach it', C['green'])], ch='The big idea'),
 dict(kind='big', chip='Know where you\'re going', lines=[('START   →   →   →   ★', C['yel'], 52), ('know the destination', C['blue'], 40), ('or you stop at the wrong place', C['red'], 32)]),
 dict(kind='rows', chip='Often ONE STEP PAST x', cc=C['org'], rows=[('x − 5', 'not x', C['org']), ('2x', 'not x', C['org']), ('diameter', 'not radius', C['org']), ('did NOT pass', 'not passed', C['org'])], ch='One step past x'),
 dict(kind='steps', steps=[('Read the last line twice', C['blue']), ('Write FIND: the exact thing', C['yel']), ('Solve, then check: did I answer FIND?', C['green'])], ch='The method'),
 dict(kind='q', chip='Asks for an expression', q=Q1, newq=True, find='x − 5', newfind=True, work=['3x = 27  →  x = 9', [('9 − 5 = ', C['ink']), ('4', C['green'])]], ch='Examples'),
 dict(kind='q', chip='Asks for an expression', q=Q1, find='x − 5', work=['3x = 27  →  x = 9', [('9 − 5 = ', C['ink']), ('4', C['green'])]], old=2, trap=('Clicked 9? That\'s x.', 'FIND was x − 5 ✗')),
 dict(kind='q', chip='Diameter, not radius', q=Q2, newq=True, find='diameter', newfind=True, work=['r² = 49  →  r = 7', [('d = 2r = ', C['ink']), ('14', C['green'])]]),
 dict(kind='q', chip='Diameter, not radius', q=Q2, find='diameter', work=['r² = 49  →  r = 7', [('d = 2r = ', C['ink']), ('14', C['green'])]], old=2, trap=('7 is the radius: a trap choice.', 'Diameter = 2 × radius ✗')),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=Q3, newq=True, ch='SAT question'),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=Q3, find='did NOT pass', newfind=True, work=['100% − 92% = 8%', [('0.08 × 1,200 = ', C['ink']), ('96', C['green'])]]),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=Q3, find='did NOT pass', work=['100% − 92% = 8%', [('0.08 × 1,200 = ', C['ink']), ('96', C['green'])]], old=2, trap=('1,104 is the number who PASSED.', 'Answers the opposite question ✗')),
 dict(kind='q', chip='Your turn', cc=C['yel'], q='If x ÷ 4 = 3, what is 2x?', newq=True, pause='Pause and solve', ch='Your turn'),
 dict(kind='q', chip='Your turn', cc=C['yel'], q='If x ÷ 4 = 3, what is 2x?', find='2x', newfind=True, work=['x = 12', [('2x = ', C['ink']), ('24', C['green'])]], trap=('12 is one step short.', 'FIND was 2x ✗'), trap_at=(540, 250)),
 dict(kind='recap', items=[('Read the last line twice', C['blue']), ('Write FIND first', C['yel']), ('Stop at the FIND, not at x', C['green'])], ch='Lock it in'),
]
if __name__ == '__main__':
    build(D, 'SAT Strategy · Define FIND', S, {11: 5.0, 13: 1.5})
