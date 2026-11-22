import sys; sys.path.insert(0, '/home/claude/v2')
from strat import *
D = '/home/claude/v2/m5'
S = [
 dict(kind='title', title='Use the Whole Clock', sub='Finished early = skipped the checking', big=[('every minute counts', C['yel'])], ch='The big idea'),
 dict(kind='big', chip='Road trip', cc=C['blue'], lines=[('Don\'t park with gas in the tank', C['ink'], 40), ('leftover time = checking fuel', C['green'], 36)]),
 dict(kind='rows', chip='Your pace', cc=C['yel'], rows=[('Math', '35 min ÷ 22 questions ≈ 1½ min each', C['blue'])], ch='Your pace'),
 dict(kind='rows', chip='Your pace', cc=C['yel'], rows=[('Math', '35 min ÷ 22 questions ≈ 1½ min each', C['blue']), ('Reading & Writing', '32 min ÷ 27 questions ≈ 1 min 10 s each', C['green'])]),
 dict(kind='rows', chip='Three rules', cc=C['green'], rows=[('1  Done early?', 'go back and VERIFY', C['green'])], ch='Three rules'),
 dict(kind='rows', chip='Three rules', cc=C['green'], rows=[('1  Done early?', 'go back and VERIFY', C['green']), ('2  Stuck > 3 min?', 'guess, flag, move on', C['org'])]),
 dict(kind='rows', chip='Three rules', cc=C['green'], rows=[('1  Done early?', 'go back and VERIFY', C['green']), ('2  Stuck > 3 min?', 'guess, flag, move on', C['org']), ('3  Never blank', 'blank = 0%,  guess ≥ 25%', C['red'])]),
 dict(kind='q', chip='SAT-style situation', cc=C['yel'], q=['10 minutes left. Every question is answered.', 'What should you do?'], newq=True, ch='SAT situation'),
 dict(kind='q', chip='SAT-style situation', cc=C['yel'], q=['10 minutes left. Every question is answered.', 'What should you do?'], work=[[('✗ ', C['red']), ('submit early', C['mute'])], [('✓ ', C['green']), ('flagged questions first, then verify the rest', C['ink'])]]),
 dict(kind='q', chip='SAT-style situation', cc=C['yel'], q=['10 minutes left. Every question is answered.', 'What should you do?'], work=[[('✗ ', C['red']), ('submit early', C['mute'])], [('✓ ', C['green']), ('flagged questions first, then verify the rest', C['ink'])]], old=2, trap=('Submitting early feels good...', 'but that time catches easy mistakes ✗')),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=['Time is almost up. Two questions are still blank.', 'What do you do?'], newq=True, pause='Pause and decide', ch='Your turn'),
 dict(kind='q', chip='Your turn', cc=C['yel'], q=['Time is almost up. Two questions are still blank.', 'What do you do?'], work=[[('✓ ', C['green']), ('guess on both, right now', C['ink'])], [('no penalty for guessing', C['mute'])]]),
 dict(kind='recap', items=[('Use every minute', C['yel']), ('Stuck > 3 min: guess, flag, move on', C['org']), ('Never leave a blank', C['red'])], ch='Lock it in'),
]
if __name__ == '__main__':
    build(D, 'SAT Strategy · Pacing', S, {10: 5.0, 12: 1.5})
