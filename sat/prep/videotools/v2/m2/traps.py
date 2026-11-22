import sys; sys.path.insert(0, '/home/claude/v2')
from strat import *
D = '/home/claude/v2/m2'
QP = 'A price rose from $40 to $50. What is the percent increase?'
QS = ['There are 12 inches in a foot.', 'How many square feet is 1,584 square inches?']
QG = ['A plan costs $30 for the first GB and $8 for each ADDITIONAL GB.', 'What do 5 GB cost?']
QT = ['A population went from 200 to 250.', 'What is the percent increase?']
S = [
 dict(kind='title', title='Read the Trap Words', sub='Small words that change the math', big=[('increase · square · additional · not', C['yel'])], ch='The big idea'),
 dict(kind='big', chip='Potholes', cc=C['red'], lines=[('⚠  trap words = potholes', C['red'], 44), ('spot them BEFORE you drive over them', C['ink'], 32), ('skip the word → land on the trap answer', C['yel'], 30)]),
 dict(kind='q', chip='Percent increase', q=QP, newq=True, work=['change = 50 − 40 = 10', [('10 ÷ ', C['ink']), ('40', C['yel']), (' (old) = ', C['ink']), ('25%', C['green'])]], ch='Percent change'),
 dict(kind='q', chip='Percent increase', q=QP, work=['change = 50 − 40 = 10', [('10 ÷ ', C['ink']), ('40', C['yel']), (' (old) = ', C['ink']), ('25%', C['green'])]], old=2, trap=('10 ÷ 50 = 20% divides by the NEW price.', 'Always divide by the OLD value ✗')),
 dict(kind='q', chip='Increase vs. total', q='A value grows from t to 3.47t. By what percent did it INCREASE?', newq=True, work=[[('3.47t = ', C['ink']), ('347% of t', C['mute'])], [('extra part = 2.47t  →  ', C['ink']), ('247% more', C['green'])]]),
 dict(kind='rows', chip='Square units', cc=C['org'], rows=[('1 ft', '= 12 in', C['blue']), ('1 sq ft', '= 12 × 12 = 144 sq in', C['org'])], ch='Square units'),
 dict(kind='q', chip='Square units', cc=C['org'], q=QS, newq=True, work=[[('1,584 ÷ ', C['ink']), ('144', C['org']), (' = ', C['ink']), ('11 sq ft', C['green'])]], trap=('1,584 ÷ 12 = 132 is the trap.', 'Square units use 12 × 12 ✗'), trap_at=(100, 330)),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QG, newq=True, ch='SAT question'),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QG, work=['first GB: $30', [('ADDITIONAL = 4 more:  4 × $8 = $32', C['ink'])], [('$30 + $32 = ', C['ink']), ('$62', C['green'])]]),
 dict(kind='q', chip='SAT-style question', cc=C['yel'], q=QG, work=['first GB: $30', [('ADDITIONAL = 4 more:  4 × $8 = $32', C['ink'])], [('$30 + $32 = ', C['ink']), ('$62', C['green'])]], old=3, trap=('30 + 8 × 5 = $70 charges all 5.', 'First GB counted twice ✗'), trap_at=(640, 380)),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=QT, newq=True, pause='Pause and solve', ch='Your turn'),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=QT, work=['change = 50', [('50 ÷ ', C['ink']), ('200', C['yel']), (' (old) = ', C['ink']), ('25%', C['green'])]], trap=('50 ÷ 250 = 20% is the trap.', 'Divide by the OLD value ✗'), trap_at=(560, 240)),
 dict(kind='recap', items=[('Underline the trap words', C['red']), ('% change ÷ the OLD value', C['blue']), ('Square units: 12 × 12 = 144', C['org'])], ch='Lock it in'),
]
if __name__ == '__main__':
    build(D, 'SAT Strategy · Trap words', S, {10: 5.0, 12: 1.5})
