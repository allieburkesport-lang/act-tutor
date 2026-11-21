#!/usr/bin/env python3
"""Fresh math drill questions in the same format, phrasing and step style as bank.json
(which mirrors the College Board question bank). Each template below matches a template
in qform.py, so Show me how / formula cards work for every new question.

    python3 mathgen.py [target_per_skill]      (default 80)

Adds questions to ../bank.json until every math skill has `target` questions.
Never changes or removes an existing question, never duplicates question text."""
import json, random, re, sys, math, os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, '..', 'bank.json')
R = random.Random(20261121)

# ---------- formatting ----------
def N(n):
    """number with a real minus sign and thousands commas"""
    if isinstance(n, Fr):
        if n.denominator == 1: return N(n.numerator)
        return ('−' if n < 0 else '') + f'{abs(n.numerator)}/{n.denominator}'
    if isinstance(n, float):
        if abs(n - round(n)) < 1e-9: return N(int(round(n)))
        s = f'{abs(n):,.4f}'.rstrip('0').rstrip('.')
        return ('−' if n < 0 else '') + s
    s = f'{abs(n):,}'
    return ('−' if n < 0 else '') + s
def P(n): return str(n) if n >= 0 else '−' + str(-n)        # plain (no commas), e.g. coordinates
def sg(n): return f' + {P(n)}' if n >= 0 else f' − {P(-n)}'  # " + 5" / " − 5"
def cx(c, v='x'):
    if c == 1: return v
    if c == -1: return '−' + v
    return f'{P(c)}{v}'
def fr(a, b=1):
    f = Fr(a, b); return N(f)
def sup(t): return f'<sup>{t}</sup>'

def fx(v):
    if isinstance(v, (int, Fr)) and not isinstance(v, bool): v = N(v)
    v = str(v)
    v = re.sub(r'(\d+)/(\d+)π', r'\1π/\2', v)          # 121/8π → 121π/8 (College Board style)
    v = re.sub(r'(^|[\s(−-])1π', r'\1π', v)
    return v.replace('-', '−') if re.fullmatch(r'-[\d.,/]+', v) else v
def mk(diff, q, tool, steps, trap, ans, wrongs, fopts, fok, grid=False):
    ans = fx(ans); steps = [fx(x) for x in steps]; wrongs = [fx(w) for w in wrongs]
    find = list(fopts); right = find[fok]; R.shuffle(find)
    d = dict(diff=diff, q=q, tool=tool, steps=steps, trap=trap, find={'opts': find, 'ok': find.index(right)})
    if grid:
        d['grid'] = [ans.replace(',', '')]; d['show'] = ans; return d
    ws = []
    for w in wrongs:
        w = str(w)
        if w != ans and w not in ws: ws.append(w)
    if len(ws) < 3: return None
    ch = ws[:3]; pos = R.randrange(4); ch.insert(pos, ans)
    d['ch'] = ch; d['ans'] = pos; return d

G = {}  # skill -> list of generator functions
def gen(skill):
    def d(fn): G.setdefault(skill, []).append(fn); return fn
    return d
ri = R.randint
def pick(*a): return R.choice(a)

# ======================= lin1 =======================
@gen('lin1')
def _():
    a, x, b = ri(2, 9), ri(2, 12), ri(3, 30); c = a * x + b
    return mk('E', f'If {a}x + {b} = {c}, what is the value of x?',
        f'By hand is faster (2 steps). Desmos: graph y = {a}x + {b} and y = {c}, click the crossing.',
        [f'Subtract {b} from both sides: {a}x = {c - b}', f'Divide both sides by {a}: x = {x}', f'Check: {a}({x}) + {b} = {c} ✓'],
        f'{c - b} is {a}x, not x. Finish the last step.', x, [c - b, a, x + b, N(Fr(c + b, a))],
        [f'{a}x', 'x', 'the whole left side'], 1)
@gen('lin1')
def _():
    a, b = ri(3, 7), ri(1, 6); c = ri(1, a - 1); x = R.choice([v for v in range(-4, 9) if v not in (0, b)])
    d = a * (x - b) - c * x
    if d == 0: return None
    rhs = cx(c) + sg(d)
    wrong = Fr(d + b, a - c)  # forgot to distribute to the second term
    return mk('M', f'{a}(x − {b}) = {rhs}<br>What value of x is the solution to the equation above?',
        'Desmos: type both sides as y = … and click where they cross.',
        [f'Distribute: {a}x − {a * b} = {c}x{sg(d)}', f'Subtract {c}x from both sides: {a - c}x − {a * b} = {P(d)}',
         f'Add {a * b}: {a - c}x = {P(d + a * b)}', f'Divide by {a - c}: x = {P(x)}'],
        f'Distribute to BOTH terms: {a}(x − {b}) = {a}x − {a * b}, not {a}x − {b}.', N(x),
        [N(wrong), N(-x), N(x + b), N(Fr(d, a - c)), N(x + 2)], ['x − ' + str(b), 'the right side', 'x'], 2)
JOBS = [('plumber', 'service call'), ('tutor', 'booking fee'), ('moving company', 'truck fee'), ('electrician', 'trip charge'),
        ('dog walker', 'sign-up fee'), ('mechanic', 'diagnostic fee'), ('photographer', 'setup fee'), ('landscaper', 'equipment fee'),
        ('cleaning service', 'travel fee'), ('carpenter', 'service call'), ('DJ', 'setup fee'), ('painter', 'supply fee')]
def art(w): return 'An' if w[0] in 'aeiouAEIOU' else 'A'
@gen('lin1')
def _():
    job, fee = R.choice(JOBS); f, r, h = 5 * ri(4, 18), 5 * ri(3, 13), ri(2, 10); T = f + r * h
    return mk('M', f"{art(job)} {job} charges a {fee} of ${f} plus ${r} per hour. A customer's bill was ${T}. For how many hours did the {job} work?",
        'By hand: one subtraction, one division.',
        [f'Equation: {f} + {r}h = {T}', f'Subtract the {fee}: {r}h = {T - f}', f'Divide by {r}: h = {h}'],
        f'Take away the one-time {fee} first. {T} ÷ {r} forgets it.', h,
        [N(round(T / r, 1)), N(round((T + f) / r, 1)), h + 1, h - 1], ['the number of hours', 'the total bill', 'the cost per hour'], 0)
@gen('lin1')
def _():
    a, b, x, k = ri(2, 6), ri(1, 9), ri(2, 10), ri(2, 4); c = a * x + b
    return mk('H', f'If {a}x + {b} = {c}, what is the value of {k * a}x + {k * b}?', 'Fastest: notice the shortcut. No Desmos needed.',
        [f'{k * a}x + {k * b} is exactly {k} × ({a}x + {b})', f'So it equals {k} × {c} = {k * c}', f'(Check the long way: x = {x}, and {k * a}({x}) + {k * b} = {k * c})'],
        f'x = {x} is NOT the answer. They asked for {k * a}x + {k * b}.', k * c, [x, a * x, k * a * x, c + k], ['x', f'{k * a}x + {k * b}', f'{a}x'], 1)
@gen('lin1')
def _():
    p, m = ri(2, 9), ri(2, 9); n = ri(1, 30)
    if m * p == n: return None
    return mk('H', f'In the equation k(x + {p}) = {m}x + {n}, k is a constant. If the equation has <b>no solution</b>, what is the value of k?',
        'Rule: same x-number + different constant = no solution. Desmos check: slider for k, look for parallel lines.',
        [f'Distribute: kx + {p}k = {m}x + {n}', f'No solution means the x-numbers match: k = {m}', f'Then the constants must differ: {p}({m}) = {p * m} ≠ {n} ✓'],
        'Matching x-numbers AND matching constants = infinitely many, not none.', m, [N(Fr(n, p)), N(-m), p * m, n],
        ['x', 'the number that makes infinitely many solutions', 'k, the number that makes NO solution'], 2)

# ======================= lin2 =======================
ITEMS = [('pens', 'notebooks'), ('muffins', 'bagels'), ('small candles', 'large candles'), ('bus tickets', 'train tickets'),
         ('stickers', 'posters'), ('apples', 'melons'), ('postcards', 'stamps sheets'), ('tulip bulbs', 'rose bushes'),
         ('erasers', 'binders'), ('granola bars', 'smoothies'), ('paperback books', 'hardcover books'), ('cups of coffee', 'sandwiches')]
@gen('lin2')
def _():
    i1, i2 = R.choice(ITEMS); a, b = ri(2, 9), ri(3, 15); x, y = ri(2, 12), ri(2, 9)
    if a == b: return None
    T = a * x + b * y
    return mk('E', f'The equation {a}x + {b}y = {T} represents the total cost, in dollars, of x {i1} and y {i2}. If {y} {i2} were bought, how many {i1} were bought?',
        'By hand: plug in y, then solve.', [f'Plug in y = {y}: {a}x + {b}({y}) = {T}', f'{a}x + {b * y} = {T}', f'{a}x = {a * x}', f'x = {x}'],
        f'Multiply {b} × {y} before subtracting.', x, [N(Fr(T - b, a)), N(Fr(T, a)), y, a * x, x + y],
        [f'y, the number of {i2}', f'x, the number of {i1}', 'the total cost'], 1)
@gen('lin2')
def _():
    a = R.choice([4, 5, 6, 8, 10, 12]); b = a * R.choice([2, 3, 4, 5]); x, y = ri(3, 20), ri(2, 12); T = a * x + b * y
    return mk('M', f'A shipment of {T} books is packed in small boxes that hold {a} books each and large boxes that hold {b} books each. Which equation shows this, if x is the number of small boxes and y is the number of large boxes?',
        'By hand: (books per box) × (number of boxes), then add.',
        [f'Small boxes: x boxes × {a} books = {a}x', f'Large boxes: y boxes × {b} books = {b}y', f'Together: {a}x + {b}y = {T}'],
        'Match each number to ITS box. Swapping them is the most common miss.', f'{a}x + {b}y = {T}',
        [f'{b}x + {a}y = {T}', f'x + y = {T}', f'{a}x = {b}y + {T}', f'{a}x − {b}y = {T}'],
        ['the number of boxes', 'the number of large boxes', 'an equation for the total number of books'], 2)
FORMS = [('d = rt', 't', 't = d/r', ['t = dr', 't = r/d', 't = d − r']),
         ('A = bh/2', 'h', 'h = 2A/b', ['h = A/(2b)', 'h = 2Ab', 'h = Ab/2']),
         ('F = ma', 'a', 'a = F/m', ['a = Fm', 'a = m/F', 'a = F − m']),
         ('K = mv²/2', 'm', 'm = 2K/v²', ['m = Kv²/2', 'm = 2v²/K', 'm = K/(2v²)']),
         ('P = W/t', 't', 't = W/P', ['t = PW', 't = P/W', 't = W − P']),
         ('V = IR', 'I', 'I = V/R', ['I = VR', 'I = R/V', 'I = V − R']),
         ('D = m/V', 'V', 'V = m/D', ['V = mD', 'V = D/m', 'V = m − D']),
         ('y = mx + b', 'x', 'x = (y − b)/m', ['x = y/m − b', 'x = (y + b)/m', 'x = m(y − b)']),
         ('C = 2πr', 'r', 'r = C/(2π)', ['r = 2πC', 'r = Cπ/2', 'r = 2C/π']),
         ('v = u + at', 'a', 'a = (v − u)/t', ['a = v/t − u', 'a = (v + u)/t', 'a = t(v − u)']),
         ('P = 2L + 2W', 'L', 'L = (P − 2W)/2', ['L = P − W', 'L = (P − W)/2', 'L = P/2 − 2W']),
         ('A = P(1 + rt)', 'P', 'P = A/(1 + rt)', ['P = A − rt', 'P = A(1 + rt)', 'P = A/rt − 1']),
         ('E = mc²', 'm', 'm = E/c²', ['m = Ec²', 'm = c²/E', 'm = E − c²']),
         ('p = mv', 'v', 'v = p/m', ['v = pm', 'v = m/p', 'v = p − m']),
         ('Q = mcT', 'c', 'c = Q/(mT)', ['c = QmT', 'c = mT/Q', 'c = Qm/T']),
         ('S = 180(n − 2)', 'n', 'n = S/180 + 2', ['n = S/180 − 2', 'n = (S − 2)/180', 'n = 180S + 2'])]
@gen('lin2')
def _():
    f, v, a, w = R.choice(FORMS)
    return mk('H', f'The formula {f} is used in science class. Which equation correctly shows {v} in terms of the other variables?',
        'Desmos check: pick numbers for the other letters and test each choice.',
        [f'Goal: get {v} alone on one side.', 'Undo the operations in reverse order: adding first, then multiplying/dividing.', f'Result: {a}', 'Check with easy numbers: plug them in both versions.'],
        'Whatever was dividing moves up; whatever was multiplying moves down.', a, w, [f'{v} by itself', f'{f.split(" =")[0]} by itself', 'a number'], 0)
DRAIN = [('number of gallons of water left in a tank', 'gallons used', 'days', 'day'), ('number of dollars left on a gift card', 'dollars spent', 'coffees bought', 'coffee'),
         ('number of feet of a climber above the ground', 'feet descended', 'minutes', 'minute'), ('number of pages left to read', 'pages read', 'days', 'day'),
         ('number of dollars still owed on a loan', 'dollars paid', 'months', 'month'), ('number of liters of fuel in a generator', 'liters used', 'hours', 'hour'),
         ('number of seats still open on a flight', 'seats booked', 'hours since booking opened', 'hour'), ('number of tickets left for a concert', 'tickets sold', 'hours', 'hour'),
         ('number of minutes left on a phone card', 'minutes used', 'days', 'day'), ('number of pounds of birdseed left in a feeder', 'pounds eaten', 'weeks', 'week'),
         ('number of meters of a diver below the surface', 'meters risen', 'seconds', 'second'), ('number of cookies left in a jar', 'cookies eaten', 'days', 'day')]
@gen('lin2')
def _():
    th, used, units, u1 = R.choice(DRAIN); r = ri(2, 15); A = r * ri(8, 60)
    start = th.replace('number of ', 'number of ', 1)
    if R.random() < 0.7:
        return mk('H', f'The equation y = {A} − {r}x gives the {th} after x {units}. What is the best interpretation of {A} in this context?',
            'No math: the number alone (no x) is the starting value.', ['Set x = 0 (the start).', f'y = {A} − {r}(0) = {A}', f'So {A} is the starting amount.'],
            f'{r} is the rate. The lone number is the start.', f'The {start} at the start',
            [f'The {used} each {u1}', f'The number of {units} until it reaches 0', f'The {start} after 1 {u1}'],
            ['the slope', 'the value of x', f'what the number {A} means'], 2)
    return mk('H', f'The equation y = {A} − {r}x gives the {th} after x {units}. What is the best interpretation of {r} in this context?',
        'No math: the number multiplied by x is the change for each 1 of x.', [f'The number with x is the rate: {r}.', f'Each time x goes up 1, y goes down by {r}.', f'So {r} is the {used} each {u1}.'],
        f'{A} is the start. The number with x is the rate.', f'The {used} each {u1}',
        [f'The {start} at the start', f'The number of {units} until it reaches 0', f'The {start} after {r} {units}'],
        ['the starting value', 'the value of x', f'what the number {r} means'], 2)

# ======================= linf =======================
@gen('linf')
def _():
    m = R.choice([v for v in range(-9, 10) if v not in (0, 1, -1)]); b, k = ri(1, 20), R.choice([v for v in range(-6, 10) if v])
    v = m * k + b
    return mk('E', f'The function f is defined by f(x) = {P(m)}x + {b}. What is the value of f({P(k)})?', f'Desmos: type f(x)=… then f({P(k)}).',
        [f'Replace x with {P(k)}: {P(m)}({P(k)}) + {b}', f'= {P(m * k)} + {b} = {P(v)}'], f'f({P(k)}) means plug {P(k)} IN for x.', N(v),
        [N(m * k - b), N(m + b + k), N(m * (k + b)), N(-v)], [f'the x that makes f(x) = {P(k)}', f'the output f({P(k)})', 'the slope'], 1)
@gen('linf')
def _():
    x1, y1 = ri(-6, 6), ri(-9, 9); run = R.choice([1, 2, 3, 4]); m = R.choice([v for v in range(-5, 6) if v]) * R.choice([1, 1, Fr(1, run)])
    x2 = x1 + run * R.choice([1, 2]); y2 = y1 + m * (x2 - x1)
    if Fr(y2).denominator != 1 or (x1, y1) == (x2, y2): return None
    y2 = int(y2); rise = y2 - y1; rn = x2 - x1; m = Fr(rise, rn)
    return mk('M', f'A line passes through the points ({P(x1)}, {P(y1)}) and ({P(x2)}, {P(y2)}). What is the slope of the line?',
        'By hand: (y₂ − y₁) ÷ (x₂ − x₁). Desmos: type both points in a table and fit y1~mx1+b.',
        [f'Rise: {P(y2)} − ({P(y1)}) = {P(rise)}', f'Run: {P(x2)} − ({P(x1)}) = {P(rn)}', f'Slope = {P(rise)}/{P(rn)} = {N(m)}'],
        'Rise is the y-change on TOP. Run (x-change) on the bottom.', N(m),
        [N(1 / m) if m else '0', N(-m), N(-1 / m) if m else '1', N(Fr(rise, x2 + x1)) if x2 + x1 else N(m + 1)],
        ['the y-intercept', 'the run', 'the slope (rise over run)'], 2)
@gen('linf')
def _():
    m = R.choice([v for v in range(-6, 7) if v not in (0,)]); b = ri(-9, 12)
    rows = ''.join(f'<tr><td>{x}</td><td>{P(m * x + b)}</td></tr>' for x in range(4))
    f = lambda mm, bb: f'f(x) = {cx(mm)}{sg(bb)}' if bb else f'f(x) = {cx(mm)}'
    return mk('M', f"The table shows values of the linear function f.<table class='qt'><tr><th>x</th><th>f(x)</th></tr>{rows}</table>Which equation defines f?",
        'Desmos: put the table in, then y1 ~ m x1 + b gives m and b.',
        [f'Starting value: when x = 0, f(x) = {P(b)}. So b = {P(b)}.', f'Each step right, f(x) changes by {P(m)}. So m = {P(m)}.', f'{f(m, b)}'],
        'The x = 0 row is the y-intercept. Do not use the x = 1 row.', f(m, b),
        [f(b, m) if b not in (0,) else f(m, m), f(m, m + b), f(m + b, 0) if m + b not in (0,) else f(-m, b), f(-m, b)],
        ['the equation (slope and starting value)', 'f(3)', 'the slope only'], 0)
@gen('linf')
def _():
    m, b = R.choice([v for v in range(-6, 7) if v]), ri(-12, 12); p = ri(-4, 2); q = p + ri(2, 6); t = q + ri(1, 5)
    fp, fq, ft = m * p + b, m * q + b, m * t + b
    return mk('H', f'For the linear function f, f({P(p)}) = {P(fp)} and f({P(q)}) = {P(fq)}. What is the value of f({P(t)})?',
        'Desmos: type the two points in a table and use y1~mx1+b, then plug in.',
        [f'Slope: ({P(fq)} − {P(fp)}) ÷ ({P(q)} − {P(p)}) = {P(m)}', f'Start: f(0) = {P(b)}', f'f(x) = {cx(m)}{sg(b) if b else ""}', f'f({P(t)}) = {P(m)}({P(t)}){sg(b) if b else ""} = {P(ft)}'],
        'Find the slope AND the start before plugging in.', N(ft), [N(m * t), N(fq + m), N(ft - b - b) if b else N(ft + 3), N(fq + t)],
        ['the slope', f'f({P(t)})', 'f(0)'], 1)
@gen('linf')
def _():
    A, B = ri(1, 12), ri(2, 19); C = ri(4, 40)
    if math.gcd(A, B) != 1: return None
    return mk('H', f'Line p is defined by {A}x + {B}y = {C}. Line q is perpendicular to line p. What is the slope of line q?',
        'Rule: in Ax + By = C, slope = −A/B. Perpendicular = flip it, flip the sign.',
        [f'Slope of p = −A/B = {N(Fr(-A, B))}', f'Perpendicular: flip it ({N(Fr(B, A))}) and flip the sign (− becomes +)', f'Slope of q = {N(Fr(B, A))}'],
        '−A/B is line p. The question wants line q: flip it, flip the sign.', N(Fr(B, A)), [N(Fr(-A, B)), N(Fr(-B, A)), N(Fr(A, B))],
        ['the slope of p', 'the y-intercept of p', 'the slope of q (the perpendicular line)'], 2)

# ======================= sys =======================
@gen('sys')
def _():
    x, y, m = ri(-6, 6), ri(-6, 8), ri(2, 5); b = y - m * x
    if b == 0 or x == y: return None
    c = x + y
    return mk('E', f'y = {m}x{sg(b)}<br>x + y = {P(c)}<br>What is the solution (x, y) to the system of equations above?',
        'Desmos: type both equations, click the crossing point.',
        [f'Replace y in the second equation: x + ({m}x{sg(b)}) = {P(c)}', f'{m + 1}x = {P(c - b)} → x = {P(x)}', f'y = {m}({P(x)}){sg(b)} = {P(y)}'],
        'Order matters: (x, y). Swapped coordinates are a planted trap.', f'({P(x)}, {P(y)})',
        [f'({P(y)}, {P(x)})', f'({P(x)}, {P(-y)})' if y else f'({P(x)}, 1)', f'({P(x + 1)}, {P(y - 1)})', f'({P(-x)}, {P(y)})'],
        ['x only', 'the point (x, y) where both are true', 'the slope'], 1)
@gen('sys')
def _():
    pa, pc = ri(8, 20), ri(4, 12); a, c = ri(10, 60), ri(10, 60)
    if pa <= pc or a == c: return None
    n, T = a + c, pa * a + pc * c
    what = R.choice(['child', 'adult'])
    if what == 'child':
        return mk('M', f'A theater sold {n} tickets for ${N(T)}. Adult tickets cost ${pa} and child tickets cost ${pc}. How many child tickets were sold?',
            f'Desmos: x + y = {n} and {pa}x + {pc}y = {T}, click the crossing. Read the CHILD value.',
            [f'a + c = {n} and {pa}a + {pc}c = {T}', f'a = {n} − c, so {pa}({n} − c) + {pc}c = {T}', f'{pa * n} − {pa - pc}c = {T} → c = {c}', f'Check: adults = {a}; {pa}({a}) + {pc}({c}) = {T} ✓'],
            f'{a} is the adult count. Circle CHILD before you click.', c, [a, c + 1, c - 1, n - c + 2], ['the number of adult tickets', 'the total money', 'the number of child tickets'], 2)
    return mk('M', f'A theater sold {n} tickets for ${N(T)}. Adult tickets cost ${pa} and child tickets cost ${pc}. How many adult tickets were sold?',
        f'Desmos: x + y = {n} and {pa}x + {pc}y = {T}, click the crossing. Read the ADULT value.',
        [f'a + c = {n} and {pa}a + {pc}c = {T}', f'c = {n} − a, so {pa}a + {pc}({n} − a) = {T}', f'{pa - pc}a + {pc * n} = {T} → a = {a}', f'Check: children = {c}; {pa}({a}) + {pc}({c}) = {T} ✓'],
        f'{c} is the child count. Circle ADULT before you click.', a, [c, a + 1, a - 1, n - a + 2], ['the number of child tickets', 'the total money', 'the number of adult tickets'], 2)
@gen('sys')
def _():
    x, y = ri(1, 9), ri(1, 9); a, b, d = ri(1, 6), ri(1, 6), ri(1, 6)
    c1, c2 = a * x + b * y, d * x - b * y
    A = '' if a == 1 else str(a); D = '' if d == 1 else str(d); Bs = '' if b == 1 else str(b)
    if a == 1 or b == 1: return None
    return mk('M', f'{A}x + {Bs}y = {c1}<br>{D}x − {Bs}y = {P(c2)}<br>If (x, y) is the solution to the system, what is the value of x + y?',
        'Desmos: graph both, click the crossing, then ADD the two numbers.',
        [f'Add the equations (the y terms cancel): {a + d}x = {c1 + c2} → x = {x}', f'Plug back in: {a}({x}) + {b}y = {c1} → y = {y}', f'x + y = {x + y}'],
        f'x = {x} is only halfway. They asked for x + y.', x + y, [x, y, x * y, abs(x - y) + (1 if x == y else 0), x + y + 2],
        ['x', 'x + y', 'y'], 1)
@gen('sys')
def _():
    D, E = ri(2, 9), ri(2, 9); B = E * ri(1, 4)
    if (D * B) % E: return None
    a = D * B // E; C, F = ri(1, 20), ri(1, 20)
    if Fr(C, B) == Fr(F, E): return None
    return mk('H', f'ax + {B}y = {C}<br>{D}x + {E}y = {F}<br>In the system above, a is a constant. For what value of a does the system have <b>no solution</b>?',
        'Desmos: slider for a; find when the lines never cross (parallel).',
        [f'Parallel lines have equal slopes. Slope of line 2: {N(Fr(-D, E))}', f'Slope of line 1 is −a/{B}. Set −a/{B} = {N(Fr(-D, E))} and solve: a = {a}', f'Check the lines are not the same: {N(Fr(C, B))} ≠ {N(Fr(F, E))} ✓'],
        'No solution = SAME slope, DIFFERENT line.', a, [-a, D, B, E, a + D], ['x', 'the y-intercept', 'a, so the lines are parallel'], 2)
@gen('sys')
def _():
    x, y, a = ri(1, 8), ri(-5, 9), ri(2, 6); c = a * x + y; d = x - y
    if c <= 0 or x == y: return None
    return mk('M', f'{a}x + y = {c}<br>x − y = {P(d)}<br>What is the value of y in the solution to the system?', 'Desmos: click the crossing; read the second number.',
        [f'Add the equations: {a + 1}x = {c + d} → x = {x}', f'{x} − y = {P(d)} → y = {P(y)}'], 'Read the y-value, not x.', N(y),
        [N(x), N(x + y), N(-y) if y else '1', N(c - x)], ['y', 'x', 'x + y'], 0)

# ======================= ineq =======================
@gen('ineq')
def _():
    a, b, k = ri(2, 9), ri(1, 20), ri(-3, 12); c = a * k - b
    return mk('E', f'Which inequality is equivalent to {a}x − {b} > {P(c)}?', f'Solve like an equation. Desmos: graph y = {a}x − {b} and y = {P(c)}; where is the line above?',
        [f'Add {b}: {a}x > {P(c + b)}', f'Divide by {a} (positive, so the sign stays): x > {P(k)}'], 'Only flip the sign when you multiply or divide by a NEGATIVE.',
        f'x > {P(k)}', [f'x < {P(k)}', f'x > {N(Fr(c - b, a))}', f'x > {P(c + b)}', f'x < {P(-k)}'], ['the value of x', 'x by itself, with the right sign', f'{a}x'], 1)
@gen('ineq')
def _():
    a, k = ri(2, 9), R.choice([v for v in range(-6, 7) if v]); c = ri(5, 40); b = c + a * k
    if b <= 0: return None
    return mk('M', f'Which values of x satisfy −{a}x + {b} ≤ {c}?', 'By hand, then test a number like x = 0 in the original.',
        [f'Subtract {b}: −{a}x ≤ {P(c - b)}', f'Divide by −{a} and FLIP the sign: x ≥ {P(k)}', f'Check x = {P(k + 1)}: −{a}({P(k + 1)}) + {b} = {P(-a * (k + 1) + b)} ≤ {c} ✓'],
        'Dividing by a negative flips ≤ to ≥.', f'x ≥ {P(k)}', [f'x ≤ {P(k)}', f'x ≥ {P(-k)}', f'x ≤ {P(-k)}'], ['one value of x', 'the slope', 'the solution set with the right sign'], 2)
NAMES = ['Jordan', 'Maya', 'Luis', 'Priya', 'Owen', 'Keisha', 'Mateo', 'Hana', 'Andre', 'Zoe', 'Ravi', 'Lena']
@gen('ineq')
def _():
    f, r = 5 * ri(4, 12), ri(3, 15); g = ri(3, 20); extra = ri(1, r - 1); B = f + r * g + extra; nm = R.choice(NAMES)
    q = Fr(B - f, r)
    return mk('M', f'A phone plan costs ${f} per month plus ${r} for each gigabyte (GB) of data. {nm} wants to spend at most ${B} this month. What is the greatest whole number of GB {nm} can use?',
        'By hand: (budget − fee) ÷ rate, then round DOWN.',
        [f'{f} + {r}g ≤ {B}', f'{r}g ≤ {B - f}', f'g ≤ {N(round(float(q), 2))}', f'Greatest whole number: {g} (round down; {g + 1} would go over)'],
        'At most = round DOWN, even if the decimal is .9.', g, [], ['the greatest whole number of GB', 'the total cost', 'the exact (decimal) answer'], 0, grid=True)
TRIPS = ['waits w minutes for a train, then rides it for', 'spends w minutes warming up, then runs for', 'reads for w minutes, then writes for',
         'rides a bus for w minutes, then walks for', 'bikes for w minutes, then swims for', 'studies for w minutes, then takes a break for',
         'drives for w minutes, then walks for', 'waits w minutes for a ferry, then rides it for', 'stretches for w minutes, then lifts weights for',
         'cooks for w minutes, then cleans up for']
@gen('ineq')
def _():
    t, n = R.choice(TRIPS), ri(4, 30); T = n + ri(5, 40)
    return mk('H', f"Sam {t} {n} minutes. Sam's trip took more than {T} minutes in total. Which inequality represents this?",
        'Words to math: "then" = add; "more than … in total" = >.', [f'Total = first part + second part = w + {n}', f'"More than {T}" means >', f'w + {n} > {T}'],
        'Two parts of one trip ADD. Subtracting is the planted trap.', f'w + {n} > {T}', [f'w − {n} > {T}', f'w + {n} < {T}', f'{n}w > {T}', f'w > {T} + {n}'],
        ['the value of w', 'an inequality for the total', 'the difference'], 1)
@gen('ineq')
def _():
    m, b = R.choice([v for v in range(-4, 5) if v]), ri(-5, 5)
    line = f'{cx(m)}{sg(b)}' if b else cx(m)
    x0 = ri(-3, 3); good = (x0, m * x0 + b + ri(1, 4))
    x1 = ri(-3, 3); on = (x1, m * x1 + b)
    bad = [(x, m * x + b - ri(1, 4)) for x in R.sample(range(-3, 4), 2)]
    pts = lambda p: f'({P(p[0])}, {P(p[1])})'
    if len({pts(good), pts(on), pts(bad[0]), pts(bad[1])}) < 4: return None
    return mk('H', f'Which point (x, y) is a solution to the inequality y > {line}?',
        'Desmos: type the inequality; the right point sits in the shaded area (not on a dashed line).',
        [f'Plug each point in: is y bigger than {line}?', f'{pts(good)}: {P(good[1])} > {P(m * good[0] + b)} ✓', 'A point ON the line does not count for >.'],
        'On the line is NOT a solution for > (only for ≥).', pts(good), [pts(on), pts(bad[0]), pts(bad[1])], ['a point on the line', 'the slope', 'the point that makes it TRUE'], 2)

# ======================= equiv =======================
def quad(b, c, v='x'):
    s = f'{v}²'
    if b: s += (' + ' if b > 0 else ' − ') + (v if abs(b) == 1 else f'{abs(b)}{v}')
    if c: s += sg(c)
    return s
def lin(r, v='x'): return f'({v} − {r})' if r > 0 else f'({v} + {-r})'   # factor for zero r
@gen('equiv')
def _():
    p, q = R.choice([v for v in range(-9, 10) if v]), R.choice([v for v in range(-9, 10) if v])
    if p + q == 0 or p == q: return None
    f1 = f'(x{sg(p)})(x{sg(q)})'
    return mk('E', f'Which expression is equivalent to {f1}?', 'Desmos: graph y = the original and y = each choice; the one that lies exactly on top is right.',
        ['First × first: x · x = x²', f'Outer + inner: {cx(q)} + {cx(p)} → {cx(p + q)}'.replace('+ −', '− '), f'Last × last: ({P(p)})({P(q)}) = {P(p * q)}', f'Answer: {quad(p + q, p * q)}'],
        'Middle term = ADD the two numbers; last term = MULTIPLY them.', quad(p + q, p * q),
        [quad(p * q, p + q), quad(0, p * q), quad(p + q, -p * q), quad(-(p + q), p * q)], ['the value of x', 'the expanded expression', 'the factored form'], 1)
@gen('equiv')
def _():
    r1, r2 = R.choice([v for v in range(-9, 10) if v]), R.choice([v for v in range(-9, 10) if v])
    if r1 == r2 or r1 + r2 == 0: return None
    b, c = -(r1 + r2), r1 * r2
    return mk('M', f'Which expression is a factor of {quad(b, c)}?', f'Desmos: graph y = {quad(b, c)}; the x-intercepts are {P(r1)} and {P(r2)}, so the factors are {lin(r1)} and {lin(r2)}.',
        [f'Find two numbers that multiply to {P(c)} and add to {P(b)}: {P(-r1)} and {P(-r2)}', f'Factors: {lin(r1)}{lin(r2)}', f'Only {lin(r1)[1:-1]} is a choice.'],
        'A zero of p means a factor of (x − p): watch the sign.', lin(r1)[1:-1],
        [lin(-r1)[1:-1], lin(-r2)[1:-1] if -r2 != r1 else f'x{sg(c)}', f'x{sg(c)}', f'x{sg(b)}' if b else 'x + 1'], ['a zero of the expression', 'the constant term', 'a factor (x − zero)'], 2)
@gen('equiv')
def _():
    k = ri(2, 15)
    return mk('M', f'Which expression is equivalent to x² − {k * k}?', 'Desmos: graph the original and each choice; look for the exact overlap.',
        ['Pattern: a² − b² = (a − b)(a + b)', f'a = x and b = {k}', f'Answer: (x − {k})(x + {k})'], 'A squared binomial (a − b)² has a middle term. Difference of squares does not.',
        f'(x − {k})(x + {k})', [f'(x − {k})²', f'(x − {k * k})(x + 1)', f'(x + {k})²'], ['the factored form', 'the value of x', 'the expanded form'], 0)
@gen('equiv')
def _():
    a, b, c = ri(2, 9), ri(2, 6), ri(2, 9); e = a * b + c
    return mk('M', f'Which expression is equivalent to (x{sup(a)}){sup(b)} · x{sup(c)}, where x > 0?', 'Rules: power of a power → multiply; same base times same base → add.',
        [f'(x^{a})^{b}: multiply the exponents: x^{a * b}', f'x^{a * b} · x^{c}: add the exponents: x^{e}'], 'Power to a power MULTIPLIES. Multiplying two powers ADDS.',
        'x' + sup(e), ['x' + sup(a + b + c), 'x' + sup(a * b * c), 'x' + sup((a + b) * c), 'x' + sup(a * b)], ['the single power of x', 'the value of x', 'the base'], 0)
@gen('equiv')
def _():
    a, q = ri(2, 5), ri(2, 5); p, r = R.choice([v for v in range(-7, 8) if v]), R.choice([v for v in range(-7, 8) if v])
    A, Bc, C = a * q, a * r + p * q, p * r
    if Bc == 0: return None
    lhs = f'(ax{sg(p)})({q}x{sg(r)})'; rhs = f'{A}x²{sg(Bc)}x{sg(C)}'.replace(' 1x', ' x')
    return mk('H', f'{lhs} = {rhs}<br>In the equation above, a is a constant. What is the value of a?', 'Match the x² terms; Desmos check: slider for a until the graphs overlap.',
        [f'Multiply the first terms: ax times {q}x = {q}a·x²', f'Match the x² coefficient: {q}a = {A}', f'Divide: a = {a}', f'Check the middle term: {a}({P(r)}) + ({P(p)})({q}) = {P(Bc)} ✓'],
        f'{A} is the whole x² number. a is only part of it.', a, [A, N(Bc), a + 1, q, N(C)], ['the x² coefficient', 'the constant a', 'the middle coefficient'], 1)
@gen('equiv')
def _():
    n, nm = R.choice([(3, 'cube'), (4, 'fourth'), (5, 'fifth')]); m = R.choice([v for v in range(2, 12) if math.gcd(v, n) == 1])
    return mk('H', f'Which expression is equivalent to the {nm} root of x{sup(m)}, for x > 0?', 'Rule: the root number goes on the BOTTOM of the fraction exponent.',
        [f'The {nm} root = power 1/{n}', f'(x^{m})^(1/{n}) = x^({m}/{n})'], 'Power on top, root on the bottom ("power over root").',
        'x' + sup(f'{m}/{n}'), ['x' + sup(f'{n}/{m}'), 'x' + sup(m * n), 'x' + sup(m - n), 'x' + sup(m + n)], ['the value of x', 'the root number', 'a single power of x'], 2)

# ======================= nleq =======================
@gen('nleq')
def _():
    k, a = ri(2, 15), ri(1, 40); b = k * k + a
    return mk('E', f'What is the positive solution to x² + {a} = {b}?', f'Desmos: graph y = x² + {a} and y = {b}; click the right-side crossing.',
        [f'Subtract {a}: x² = {k * k}', f'Square root: x = ±{k}', f'Positive solution: {k}'], f'{k * k} is x², not x.', k,
        [k * k, N(Fr(k * k, 2)), a, b], ['x²', 'the positive x', 'both solutions'], 1)
@gen('nleq')
def _():
    r1, r2 = R.choice([v for v in range(-9, 10) if v]), R.choice([v for v in range(-9, 10) if v])
    if r1 == r2: return None
    b, c = -(r1 + r2), r1 * r2
    if b == 0 or c == 0: return None
    eq = quad(b, c) + ' = 0'; fac = f'{lin(r1)}{lin(r2)} = 0'
    kind = R.choice(['sum', 'prod', 'pos'])
    if kind == 'sum':
        return mk('M', f'What is the sum of the solutions to {eq}?', 'Desmos: graph it, click both x-intercepts, then add them.',
            [f'Factor: {fac}', f'Solutions: x = {P(r1)} and x = {P(r2)}', f'Sum: {P(r1)} + ({P(r2)}) = {P(r1 + r2)}'], 'Add the two answers after you find them.',
            N(r1 + r2), [N(b), N(c), N(max(r1, r2)), N(-c)], ['the larger solution', 'the product of the solutions', 'the SUM of both solutions'], 2)
    if kind == 'prod':
        return mk('M', f'What is the product of the solutions to {eq}?', 'Desmos: graph it, click both x-intercepts, then multiply them.',
            [f'Factor: {fac}', f'Solutions: x = {P(r1)} and x = {P(r2)}', f'Product: ({P(r1)})({P(r2)}) = {P(c)}'], 'Multiply the two answers after you find them.',
            N(c), [N(r1 + r2), N(-c), N(b), N(max(r1, r2))], ['the larger solution', 'the SUM of the solutions', 'the PRODUCT of both solutions'], 2)
    if (r1 > 0) == (r2 > 0): return None
    pos, neg = max(r1, r2), min(r1, r2)
    return mk('M', f'If x > 0, what is the solution to {eq}?', 'Desmos: graph it and click the x-intercept on the right of 0.',
        [f'Factor: {fac}', f'Solutions: x = {P(r1)} and x = {P(r2)}', f'Only {pos} is greater than 0.'], 'The factor (x − 3) gives x = +3. Flip the sign in the factor.',
        pos, [N(neg), N(-pos), N(-neg) if -neg != pos else N(pos + 1), N(abs(c))], ['both solutions', 'the positive solution', 'the factors'], 1)
@gen('nleq')
def _():
    h, k = ri(1, 8), ri(1, 9); c = R.choice([-k - ri(1, 5), -k, -k + ri(1, 8)])
    n = 'exactly two' if c > -k else 'exactly one' if c == -k else 'zero'
    third = (f'Above the vertex: 2 crossings.' if c > -k else 'It touches the vertex: 1 crossing.' if c == -k else 'Below the vertex: 0 crossings.')
    return mk('M', f'y = (x + {h})² − {k}<br>y = {P(c)}<br>How many solutions does the system of equations above have?', 'Desmos: type both and COUNT the crossings.',
        [f'The parabola opens up and its lowest point (vertex) is at y = −{k}.', f'The flat line is at y = {P(c)}.', third],
        'A parabola can cross a flat line 0, 1 or 2 times, never infinitely many.', n,
        [x for x in ['zero', 'exactly one', 'exactly two', 'infinitely many'] if x != n], ['the x-values', 'how many crossing points', 'the vertex'], 1)
@gen('nleq')
def _():
    k = ri(2, 12); c = k * k; g = R.choice(['greatest', 'least']); v = 2 * k - 1 if g == 'greatest' else -(2 * k - 1)
    return mk('H', f'x² + bx + {c} = 0<br>In the equation above, b is a constant. If the equation has <b>no real solutions</b>, what is the {g} possible integer value of b?',
        'Discriminant rule. Desmos check: slider for b; the graph must stay above the x-axis.',
        ['No real solutions: b² − 4ac < 0', f'Plug in a = 1, c = {c}: b² − {4 * c} < 0', f'b² < {4 * c}, so −{2 * k} < b < {2 * k}',
         f'Edge check: b = {P(2 * k if v > 0 else -2 * k)} gives exactly ONE solution, so it does not count', f'{g.capitalize()} integer: {P(v)}'],
        f'The edge number {P(2 * k if v > 0 else -2 * k)} gives one solution. Step one integer inside.', P(v), [], ['x', f'the {g} integer b', 'the edge value of b'], 1, grid=True)
@gen('nleq')
def _():
    r, s = ri(2, 9), -ri(1, 8)
    m, n = r + s, -r * s
    if m < 1: return None
    return mk('H', f'y = x²<br>y = {"" if m == 1 else m}x + {n}<br>If (x, y) is a solution to the system and x > 0, what is the value of y?',
        'Desmos: graph both and click the crossing with x > 0. Read the y-value.',
        [f'Set them equal: x² = {m}x + {n}', f'x² − {m}x − {n} = 0', f'Positive solution: x = {r}', f'y = x² = {r * r}'],
        f'x = {r} is not the answer; they asked for y.', r * r, [r, n, 2 * r, s * s if s * s != r * r else r + n], ['x', 'the number of solutions', 'y (the second number)'], 2)

# ======================= nlf =======================
@gen('nlf')
def _():
    a, b, k = ri(2, 6), ri(1, 20), R.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
    v = a * k * k - b
    return mk('E', f'f(x) = {a}x² − {b}. What is the value of f({P(k)})?', f'Desmos: type f(x) = {a}x^2 − {b}, then f({P(k)}).',
        [f'Square first: ({P(k)})² = {k * k}', f'Multiply: {a} × {k * k} = {a * k * k}', f'Add: {a * k * k} − {b} = {P(v)}'],
        f'({P(k)})² is positive {k * k}. Square before you multiply.', N(v), [N(-v), N(a * k - b), N((a * k) ** 2 - b), N(a * k * k + b)], ['the x-intercept', f'f({P(k)})', 'the vertex'], 1)
@gen('nlf')
def _():
    P0 = R.choice([1200, 1500, 2400, 2800, 3500, 4200, 5600, 6400, 8000, 9500, 12000, 15000]); r = ri(2, 12); up = R.random() < 0.5
    yr = ri(2010, 2024); place = R.choice(['town', 'city', 'village', 'county'])
    f = f'{1 + r / 100:.2f}' if up else f'{1 - r / 100:.2f}'; o = f'{1 - r / 100:.2f}' if up else f'{1 + r / 100:.2f}'
    rr = f'0.{r:02d}'
    return mk('M', f"A {place}'s population was {N(P0)} in {yr}. It {'in' if up else 'de'}creases by {r}% each year. Which function gives the population t years after {yr}?",
        'Rule: start × (1 ± rate)^t.', [f'Start value: {N(P0)}', f'{"Grow" if up else "Shrink"} {r}%: factor = 1 {"+" if up else "−"} {rr} = {f}', f'P(t) = {N(P0)}({f})^t'],
        'The factor is 1 ' + ('+' if up else '−') + ' rate, not just ' + rr + '.', f'P(t) = {N(P0)}({f}){sup("t")}',
        [f'P(t) = {N(P0)}({rr}){sup("t")}', f'P(t) = {N(P0)} {"+" if up else "−"} {r}t', f'P(t) = {N(P0)}({o}){sup("t")}'],
        ['the population in one year', 'the percent', 'the model (start × factor^t)'], 2)
@gen('nlf')
def _():
    a = R.choice([-3, -2, -1, 1, 2, 3, 4]); h, k = ri(1, 9), ri(1, 12); sgn = R.choice([1, -1]); K = sgn * k
    mx = 'maximum' if a < 0 else 'minimum'; A = '−' if a == -1 else '' if a == 1 else P(a)
    if h == k: return None
    return mk('M', f'f(x) = {A}(x − {h})²{sg(K)}. What is the {mx} value of f(x)?', 'Desmos: graph it and click the vertex; read the y-value.',
        ['Vertex form: a(x − h)² + k has vertex (h, k)', f'Here h = {h} and k = {P(K)}', f'The {mx} VALUE is the y-value: {P(K)}'],
        f'The {mx} VALUE is y = {P(K)}, not x = {h}.', N(K), [N(h), N(-K), N(-h), N(K + a)], [f'the {mx} y-value', 'the x where it happens', 'the y-intercept'], 0)
@gen('nlf')
def _():
    opts = [(1000, '0.5', 0.5), (2000, '0.5', 0.5), (1000, '1.1', 1.1), (5000, '1.2', 1.2), (800, '1.5', 1.5), (2500, '0.8', 0.8), (10000, '0.9', 0.9),
            (400, '2', 2), (1600, '0.75', 0.75), (3000, '1.1', 1.1), (6400, '0.5', 0.5), (1250, '1.2', 1.2)]
    P0, fs, fv = R.choice(opts); n = R.choice([2, 3])
    v = P0 * fv ** n
    if abs(v - round(v)) > 1e-6: return None
    v = int(round(v))
    return mk('H', f'The value, in dollars, of an investment t years after it was made is V(t) = {N(P0)}({fs}){sup("t")}. What is the value, in dollars, after {n} years?',
        f'Desmos: type V(t) = …, then V({n}).', [f'Factor^{n}: ({fs})^{n} = {N(round(fv ** n, 6))}', f'Multiply by the start: {N(P0)} × {N(round(fv ** n, 6))} = {N(v)}'],
        'Raise the factor to the power FIRST, then multiply.', N(v), [], ['the starting value', f'V({n}) in dollars', 'the yearly change'], 1, grid=True)
def vform(b, c):  # x² + bx + c as (x + b/2)² + (c − b²/4)
    h = Fr(b, 2); k = c - h * h
    hs = (' + ' if h > 0 else ' − ') + N(abs(h)); ks = (' + ' if k > 0 else ' − ') + N(abs(k)) if k else ''
    return f'(x{hs})²{ks}'
@gen('nlf')
def _():
    p, q = R.choice([v for v in range(-8, 9) if v]), R.choice([v for v in range(-8, 9) if v])
    if p == q or p + q == 0: return None
    b, c = p + q, p * q; fac = f'(x{sg(p)})(x{sg(q)})'
    if R.random() < 0.5:
        return mk('H', f'Which equivalent form of f(x) = {fac} displays the y-intercept of the graph as a constant or coefficient?',
            f'Desmos check: y-intercept is (0, {P(c)}). Which form has {P(c)} visible as a number?',
            ['Standard form ax² + bx + c shows c = the y-intercept.', f'Expand: {fac} = {quad(b, c)}', f'{P(c)} is visible as the constant.'],
            'All four are equal. The question asks which one DISPLAYS it.', f'f(x) = {quad(b, c)}',
            [f'f(x) = {fac}', f'f(x) = {vform(b, c)}', f'f(x) = (x{sg(p)})x{sg(q)}(x{sg(p)})'.replace('+ 1(', '+ (').replace('− 1(', '− (')],
            ['the y-intercept number', 'the zeros', 'the form that SHOWS the y-intercept'], 2)
    return mk('H', f'Which equivalent form of f(x) = {quad(b, c)} displays the x-intercepts of the graph as constants or coefficients?',
        f'Desmos check: the x-intercepts are {P(-p)} and {P(-q)}.',
        ['Factored form a(x − r)(x − s) shows the zeros r and s.', f'Factor: {quad(b, c)} = {fac}', f'Zeros: {P(-p)} and {P(-q)}'],
        'Vertex form shows the vertex; standard shows the y-intercept; factored shows the zeros.', f'f(x) = {fac}',
        [f'f(x) = {quad(b, c)}', f'f(x) = {vform(b, c)}', f'f(x) = x(x{sg(b)}){sg(c)}'], ['the vertex', 'the y-intercept', 'the form that SHOWS the x-intercepts'], 2)

# ======================= ratio =======================
@gen('ratio')
def _():
    r, h, k = ri(30, 70), ri(2, 8), ri(3, 12)
    if h == k: return None
    d = r * h
    return mk('E', f'A car travels {d} miles in {h} hours at a constant speed. At this speed, how many miles will it travel in {k} hours?', 'By hand: find the unit rate first.',
        [f'Unit rate: {d} ÷ {h} = {r} miles per hour', f'Multiply by the hours: {r} × {k} = {N(r * k)} miles'], f'{r} is the speed, not the distance.', N(r * k),
        [r, N(d * k), N(r * (k - 1)), N(d + k)], ['the speed (miles per hour)', f'the miles in {k} hours', f'the hours for {d} miles'], 1)
@gen('ratio')
def _():
    f, m = ri(2, 25), R.choice([1, 1, 2, 3, 5])
    mn = 'minute' if m == 1 else 'minutes'; s = 60 * m
    return mk('M', f'A conveyor belt moves at {f} feet per second. How many feet does it move in {m} {mn}?', f'By hand: {m} {mn} = {s} seconds.',
        [f'{m} {mn} = {s} seconds', f'{f} feet each second × {s} seconds = {N(f * s)} feet'], 'There are 60 seconds in a minute, not 12 (inches in a foot).', N(f * s),
        [N(f * 12 * m), N(Fr(f, 60)), N(f * 3600 * m), N(f * m)], ['feet per second', f'seconds in {m} {mn}', f'feet in {m} {mn}'], 2)
@gen('ratio')
def _():
    a, b = ri(1, 4), R.choice([4, 6, 8, 10, 12]); c = b * R.choice([Fr(1, 2), Fr(3, 2), 2, Fr(5, 2), 3]); c = int(c) if Fr(c).denominator == 1 else None
    if not c or c == b: return None
    x = Fr(a * c, b)
    xs = N(float(x)) if x.denominator in (1, 2, 4, 5) else N(x)
    return mk('M', f'A recipe uses {a} cups of flour to make {b} muffins. How many cups of flour are needed to make {c} muffins?', 'By hand: set up a proportion and cross multiply.',
        [f'{a}/{b} = x/{c}', f'Cross multiply: {b}x = {a} × {c} = {a * c}', f'x = {xs}'], 'Keep the same order on both sides: cups over muffins.', xs,
        [N(a * c), N(a + c - b), N(float(Fr(b * c, a))) if Fr(b * c, a).denominator in (1, 2) else N(Fr(b * c, a)), N(float(x) + 1)], [f'cups for {c} muffins', 'muffins per cup', 'the scale factor'], 0)
@gen('ratio')
def _():
    p, q = ri(1, 7), ri(2, 9)
    if p == q or math.gcd(p, q) != 1: return None
    u = ri(3, 12); T = (p + q) * u
    return mk('H', f'The ratio of boys to girls in a club is {p} to {q}. The club has {T} members. How many girls are in the club?', 'By hand: add the parts, divide, multiply.',
        [f'Total parts: {p} + {q} = {p + q}', f'One part: {T} ÷ {p + q} = {u}', f'Girls: {q} × {u} = {q * u}'], 'Divide by the TOTAL parts, not by one side of the ratio.', q * u,
        [p * u, u, T - q, N(Fr(T, q)) if T % q == 0 else T - p], ['the number of boys', 'the number of girls', 'the total'], 1)
@gen('ratio')
def _():
    d = R.choice([1.5, 2.5, 2.7, 4, 7.8, 8.9, 10.5, 11.3, 19.3, 0.8]); v = R.choice([20, 40, 50, 60, 80, 100, 120, 200, 250]); g = round(d * v, 4)
    return mk('H', f'A metal has a density of {d:g} grams per cubic centimeter. What is the mass, in kilograms, of a {v} cubic centimeter block of the metal? (1 kilogram = 1,000 grams)',
        'By hand: density × volume, then convert units.', [f'Mass in grams: {d:g} × {v} = {N(g)} g', f'Convert: {N(g)} ÷ 1,000 = {N(round(g / 1000, 6))} kg'],
        'The question asks for kilograms. Grams is one step short.', N(round(g / 1000, 6)), [N(g), N(round(g / 100, 6)), N(round(v / d / 1000, 4)), N(round(g / 10, 6))],
        ['the mass in grams', 'the volume', 'the mass in KILOGRAMS'], 2)

# ======================= pct =======================
@gen('pct')
def _():
    p = R.choice([5, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75, 80, 85]); n = 20 * ri(3, 60); v = Fr(p * n, 100)
    if v.denominator != 1: return None
    return mk('E', f'What is {p}% of {N(n)}?', f'Desmos: type {p}% of {n} or {p / 100:g} × {n}.', [f'{p}% = {p / 100:g}', f'{p / 100:g} × {N(n)} = {N(v)}'], '"Of" means multiply.',
        N(v), [N(n - v), N(p * n), N(Fr(n, p)), N(v + p)], [f'what percent {N(n)} is', f'{p}% of {N(n)}', f'{N(n)} minus {p}%'], 1)
@gen('pct')
def _():
    a = 20 * ri(2, 20); p = R.choice([10, 20, 25, 30, 40, 50, 60, 75]); up = R.random() < 0.65
    b = a + a * p // 100 if up else a - a * p // 100
    if (a * p) % 100 or b <= 0: return None
    ch = abs(b - a); w = 'increase' if up else 'decrease'
    return mk('M', f'The price of an item changed from ${a} to ${b}. What is the percent {w}?', 'Rule: change ÷ OLD × 100 ("divide by old").',
        [f'Change: {max(a, b)} − {min(a, b)} = {ch}', f'Divide by the OLD price: {ch} ÷ {a} = {ch / a:g}', f'× 100 = {p}%'], 'Divide by the OLD number, not the new one.', f'{p}%',
        [f'{N(round(ch / b * 100, 1))}%', f'{ch}%', f'{100 + p if up else 100 - p}%'], ['the change in dollars', 'the new price', f'the percent {w}'], 2)
@gen('pct')
def _():
    c = 20 * ri(3, 25); p1, p2 = R.choice([10, 20, 25, 30, 40, 50]), R.choice([10, 20, 25, 50])
    s1 = Fr(c * (100 - p1), 100); s2 = s1 * Fr(100 - p2, 100)
    if s2.denominator != 1 or s1.denominator != 1: return None
    item = R.choice(['jacket', 'pair of boots', 'backpack', 'lamp', 'bike helmet', 'tennis racket'])
    return mk('M', f'A {item} costs ${c}. It is marked down {p1}%, and then the sale price is marked down another {p2}%. What is the final price?',
        f'Desmos: {c}(1 − {p1 / 100:g})(1 − {p2 / 100:g}).', [f'First markdown: {c} × {(100 - p1) / 100:g} = {N(s1)}', f'Second markdown: {N(s1)} × {(100 - p2) / 100:g} = {N(s2)}'],
        f'Two markdowns do NOT add to {p1 + p2}%. The second one is taken off the smaller price.', f'${N(s2)}',
        [f'${N(Fr(c * (100 - p1 - p2), 100))}' if p1 + p2 < 100 else '$0', f'${N(s1)}', f'${N(c - s2)}'], ['the final price', 'the total percent off', 'the first sale price'], 0)
@gen('pct')
def _():
    p = R.choice([10, 20, 25, 30, 40, 50, 60, 75]); o = 20 * ri(2, 20); s = Fr(o * (100 - p), 100)
    if s.denominator != 1: return None
    s = int(s); wrong = round(s * (1 + p / 100), 2)
    return mk('H', f'After a {p}% discount, a pair of shoes costs ${s}. What was the original price?', f'Desmos: solve x(1 − {p / 100:g}) = {s}.',
        [f'Sale = original × (1 − {p / 100:g})', f'{s} = x × {(100 - p) / 100:g}', f'x = {s} ÷ {(100 - p) / 100:g} = {o}'], f'Adding {p}% back to the sale price does NOT undo the discount.',
        f'${o}', [f'${wrong:.2f}' if wrong != int(wrong) else f'${int(wrong)}', f'${s + p}', f'${N(Fr(s * 100, p))}' if (s * 100) % p == 0 else f'${o + 10}'],
        ['the discount in dollars', 'the ORIGINAL price', 'the sale price'], 1)
@gen('pct')
def _():
    n = 100 * ri(4, 30); p, q = R.choice([10, 20, 25, 30, 40, 50]), R.choice([10, 20, 25, 40, 50])
    a = Fr(n * p, 100); b = a * Fr(q, 100)
    if b.denominator != 1 or p == q: return None
    return mk('H', f'A school has {N(n)} students. {p}% of them play a sport, and {q}% of the students who play a sport play more than one. How many students play more than one sport?',
        f'Desmos: {n} × {p / 100:g} × {q / 100:g}.', [f'Play a sport: {N(n)} × {p / 100:g} = {N(a)}', f'More than one: {N(a)} × {q / 100:g} = {N(b)}'],
        f'{q}% is a percent of the athletes, not of the whole school.', N(b), [N(a), N(Fr(n * q, 100)), N(Fr(n * (p + q), 100)), N(b + 1)],
        ['students who play a sport', 'the percent', 'students who play MORE than one sport'], 2)

# ======================= data1 =======================
@gen('data1')
def _():
    xs = sorted(R.sample(range(1, 40), 4)); m = ri(8, 30); last = 5 * m - sum(xs)
    if last <= 0 or last in xs: return None
    xs.append(last); xs.sort(); med = xs[2]
    if med == m: return None
    return mk('E', f'What is the mean of the data set: {", ".join(map(str, xs))}?', f'Desmos: mean([{",".join(map(str, xs))}]).',
        [f'Add: {" + ".join(map(str, xs))} = {sum(xs)}', f'Divide by 5 numbers: {sum(xs)} ÷ 5 = {m}'], 'Mean = average. Median = middle.', m,
        [med, N(Fr(sum(xs), 4)), xs[-1] - xs[0], m + 2], ['the median', 'the mean (average)', 'the range'], 1)
@gen('data1')
def _():
    xs = R.sample(range(1, 50), 6); s = sorted(xs); med = Fr(s[2] + s[3], 2)
    if med.denominator != 1: return None
    return mk('M', f'What is the median of the data set: {", ".join(map(str, xs))}?', f'Desmos: median([{",".join(map(str, xs))}]).',
        [f'Put in order: {", ".join(map(str, s))}', f'6 numbers, so average the 2 middle ones: ({s[2]} + {s[3]}) ÷ 2 = {N(med)}'], 'Sort the numbers FIRST.', N(med),
        [xs[2], xs[3], N(Fr(sum(xs), 6)), s[2]], ['the mean', 'the middle number of the list as written', 'the median'], 2)
@gen('data1')
def _():
    nm = R.choice(['Ana', 'Leo', 'Priya', 'Marcus', 'Jada', 'Theo', 'Sofia', 'Eli', 'Nadia', 'Caleb'])
    xs = [ri(60, 98) for _ in range(4)]; M = ri(75, 92); need = 5 * M - sum(xs)
    if not 50 <= need <= 100: return None
    pn = 'she' if nm in ('Ana', 'Priya', 'Jada', 'Sofia', 'Nadia') else 'he'; pp = 'her' if pn == 'she' else 'his'
    return mk('M', f"{nm}'s first four test scores are {', '.join(map(str, xs))}. What score does {pn} need on the fifth test for {pp} mean score to be {M}?",
        f'By hand: target × 5 − sum so far. Desmos check: mean([{",".join(map(str, xs))},{need}]).',
        [f'Total needed: {M} × 5 = {5 * M}', f'Sum so far: {sum(xs)}', f'Fifth score: {5 * M} − {sum(xs)} = {need}'], 'Use the TOTAL needed, not the average of the scores.', need, [],
        ['the fifth score', 'the current mean', 'the total of all five'], 0, grid=True)
@gen('data1')
def _():
    base = sorted(R.sample(range(10, 40), 6)); hi = R.random() < 0.7
    if hi:
        o = ri(85, 140); xs = base + [o]
        steps = [f'{o} is far above the rest: an outlier.', 'Removing a big outlier pulls the MEAN down a lot.', 'The median moves at most a little (it only shifts one spot).', 'Spread (standard deviation) gets smaller.']
        ans = 'The mean decreases, and the median decreases slightly or stays close.'
        wr = ['The mean increases, and the median increases.', 'The mean stays the same, and the median decreases.', 'Both the mean and the standard deviation increase.']
    else:
        o = ri(0, 3); xs = [o] + [b + 30 for b in base]
        steps = [f'{o} is far below the rest: an outlier.', 'Removing a very small outlier pulls the MEAN up a lot.', 'The median moves at most a little (it only shifts one spot).', 'Spread (standard deviation) gets smaller.']
        ans = 'The mean increases, and the median increases slightly or stays close.'
        wr = ['The mean decreases, and the median decreases.', 'The mean stays the same, and the median increases.', 'Both the mean and the standard deviation increase.']
    return mk('H', f'A data set is {", ".join(map(str, xs))}. If the value {o} is removed, which statement is true?', f'Desmos check: mean and median with and without {o}.',
        steps, 'Outliers move the mean a lot and the median very little.', ans, wr, ['the new mean', 'how the mean and median change', 'the outlier'], 1)
@gen('data1')
def _():
    thing, col = R.choice([('pets', 'Number of pets'), ('siblings', 'Number of siblings'), ('books read last month', 'Number of books'), ('hours of sleep', 'Hours of sleep')])
    vals = [1, 2, 3, 4, 5] if thing != 'hours of sleep' else [5, 6, 7, 8, 9]
    fq = [ri(1, 6) for _ in vals]; n = sum(fq)
    exp = []
    for v, f in zip(vals, fq): exp += [v] * f
    if n % 2 == 0:
        if exp[n // 2 - 1] != exp[n // 2]: return None
        mid = f'between students {n // 2} and {n // 2 + 1}'
    else: mid = f'student {(n + 1) // 2}'
    med = exp[n // 2]; mode = vals[fq.index(max(fq))]; mean = Fr(sum(exp), n)
    if mode == med or mean == med: return None
    if thing != 'pets':
        q = f"The table shows how many {thing} each student in a class has.".replace('has.', 'reported.')
    else: q = 'The table shows how many pets each student in a class has.'
    tab = f"<table class='qt'><tr><th>{col}</th>{''.join(f'<td>{v}</td>' for v in vals)}</tr><tr><th>Frequency</th>{''.join(f'<td>{f}</td>' for f in fq)}</tr></table>"
    if thing != 'pets': return None   # qform template keys on "how many pets each student"
    return mk('H', q + tab + 'What is the median number of pets?', 'By hand: count to the middle student.',
        [f'Total students: {n}', f'Middle position: {mid}', 'Count across the frequencies until you reach that spot.', f'Median = {med}'],
        'The median is a number of PETS, not a frequency.', med, [N(mean), mode, max(fq), fq[2]], ['the median frequency', 'the most common value', 'the median number of pets'], 2)

# ======================= data2 =======================
@gen('data2')
def _():
    m = R.choice([1.5, 2, 2.5, 3, 3.5, 4, 1.2, 0.8]); b = ri(20, 60); x = ri(4, 20); y = round(m * x + b, 2)
    if y > 100: return None
    return mk('E', f'The line of best fit for a scatterplot is y = {m:g}x + {b}, where x is hours studied and y is a test score. What test score does the line predict for {x} hours?',
        f'Desmos: type the line and trace to x = {x}.', [f'Plug in x = {x}: {m:g}({x}) + {b}', f'= {N(round(m * x, 2))} + {b} = {N(y)}'], 'Multiply, then add the starting value.',
        N(y), [N(round(m * x, 2)), N(round(m + b + x, 2)), N(round(m * (x + b), 2)), N(round((y - b) / m, 2) + 1)], ['the slope', 'the predicted score', 'the hours'], 1)
CTX = [('the temperature, in °F', 'cups of lemonade sold'), ('the age of a tree, in years', 'its height, in feet'), ('the number of hours a store is open', 'its sales, in hundreds of dollars'),
       ('the number of hours of practice', 'free throws made out of 50'), ('the price of a ticket, in dollars', 'the number of tickets sold'), ('the number of days since planting', 'the height of a plant, in centimeters'),
       ('the weight of a dog, in pounds', 'its daily food, in cups'), ('the distance from a city center, in miles', 'the price of a house, in thousands of dollars')]
@gen('data2')
def _():
    xd, yd = R.choice(CTX); m = R.choice([0.4, 0.6, 1.2, 1.5, 2.3, 3.4, 4.5, 0.9]); b = ri(2, 40)
    if R.random() < 0.65:
        return mk('M', f'A line of best fit is y = {m:g}x + {b}, where x is {xd} and y is {yd}. What does {m:g} mean?', 'No math: the number with x is the predicted change per 1 unit.',
            [f'y = {m:g}x + {b}: slope is {m:g}', 'Slope = change in y for each 1-unit increase in x', 'Best fit lines are predictions ("predicted"), not exact rules.'],
            '"Always" is too strong; a best-fit line only predicts.', f'For each increase of 1 in x, y is predicted to increase by {m:g}.',
            [f'When x is 0, y is predicted to be {m:g}.', f'y always equals {m:g} times x.', f'For each increase of {m:g} in x, y increases by 1.'], [f'the meaning of {m:g}', 'a predicted value', f'the meaning of {b}'], 0)
    return mk('M', f'A line of best fit is y = {m:g}x + {b}, where x is {xd} and y is {yd}. What does {b} mean?', 'No math: the number alone is the predicted value when x = 0.',
        [f'y = {m:g}x + {b}: the y-intercept is {b}', 'Set x = 0: y = ' + str(b), 'So it is the predicted y when x is 0.'],
        'The number with x is the rate; the lone number is the start.', f'When x is 0, y is predicted to be {b}.',
        [f'For each increase of 1 in x, y is predicted to increase by {b}.', f'y always equals {b} when x is 1.', f'For each increase of {b} in x, y increases by {m:g}.'], [f'the meaning of {m:g}', 'a predicted value', f'the meaning of {b}'], 2)
@gen('data2')
def _():
    m, b, x = ri(1, 6), ri(0, 15), ri(1, 12); pred = m * x + b; y = pred + R.choice([v for v in range(-9, 10) if v])
    if y <= 0: return None
    return mk('M', f'The line of best fit for a data set is y = {m}x + {b}. One data point is ({x}, {y}). What is the residual for this point (actual − predicted)?',
        'By hand: predicted first, then subtract.', [f'Predicted: {m}({x}) + {b} = {pred}', f'Residual = actual − predicted = {y} − {pred} = {P(y - pred)}'], 'Actual minus predicted, in that order.',
        N(y - pred), [N(pred - y), N(pred), N(y)], ['the predicted value', 'the actual value', 'the residual (actual − predicted)'], 2)
@gen('data2')
def _():
    s = R.choice([50, 80, 100, 120, 150, 200, 300]); kind = R.choice(['exp', 'exp', 'lin', 'dec'])
    if kind == 'exp': f = R.choice([2, 3]); v = [s * f ** i for i in range(4)]
    elif kind == 'lin': d = R.choice([20, 25, 40, 50, 60]); v = [s + d * i for i in range(4)]
    else: d = R.choice([10, 15, 20, 25]); v = [s + 3 * d - d * i for i in range(4)]
    tab = "<table class='qt'><tr><th>Week</th><td>0</td><td>1</td><td>2</td><td>3</td></tr><tr><th>Number</th>" + ''.join(f'<td>{N(x)}</td>' for x in v) + '</tr></table>'
    diffs = [v[i + 1] - v[i] for i in range(3)]; rat = [Fr(v[i + 1], v[i]) for i in range(3)]
    C = {'exp': 'Exponential growth, because the number is multiplied by the same factor each week', 'lin': 'Linear growth, because the same amount is added each week',
         'dec': 'Linear decay, because the number goes down by the same amount each week'}
    wr = [C[k] for k in C if k != kind] + ['No pattern, because the changes are random']
    return mk('H', f'The table shows the number of members in an online group.{tab}Which model best fits the data?', 'Check: subtract neighbors (same difference → linear) or divide them (same ratio → exponential).',
        [f'Differences: {", ".join(N(d) for d in diffs)}', f'Ratios: {", ".join(N(r) for r in rat)}', 'Same difference = linear. Same ratio = exponential.'],
        'Growing fast is not enough. Check differences vs. ratios.', C[kind], wr, ['the next value', 'the type of model', 'the starting value'], 1)

# ======================= prob =======================
@gen('prob')
def _():
    r, b, g = ri(2, 12), ri(2, 12), ri(2, 12); col = R.choice(['red', 'blue', 'green']); n = {'red': r, 'blue': b, 'green': g}[col]; T = r + b + g
    return mk('E', f'A bag has {r} red, {b} blue, and {g} green marbles. One marble is picked at random. What is the probability that it is {col}?', 'By hand: favorable ÷ total.',
        [f'Total: {r} + {b} + {g} = {T}', f'{col.capitalize()}: {n}', f'P({col}) = {n}/{T} = {N(Fr(n, T))}'], 'Divide by ALL the marbles, not just the others.', N(Fr(n, T)),
        [N(Fr(n, T - n)), N(Fr(T - n, T)), N(Fr(1, 3)), N(Fr(n, T + 1))], [f'the number of {col} marbles', f'P({col})', f'P(not {col})'], 1)
@gen('prob')
def _():
    jp, jt, sp, st = ri(10, 50), ri(10, 50), ri(10, 50), ri(10, 50)
    J, S, Pz, Ta, T = jp + jt, sp + st, jp + sp, jt + st, jp + jt + sp + st
    tab = (f"<table class='qt'><tr><th></th><th>Pizza</th><th>Tacos</th><th>Total</th></tr><tr><th>Juniors</th><td>{jp}</td><td>{jt}</td><td>{J}</td></tr>"
           f"<tr><th>Seniors</th><td>{sp}</td><td>{st}</td><td>{S}</td></tr><tr><th>Total</th><td>{Pz}</td><td>{Ta}</td><td>{T}</td></tr></table>")
    food, grp = R.choice(['pizza', 'tacos']), R.choice(['juniors', 'seniors'])
    cell = {('pizza', 'juniors'): jp, ('tacos', 'juniors'): jt, ('pizza', 'seniors'): sp, ('tacos', 'seniors'): st}[(food, grp)]
    ft, gt = (Pz if food == 'pizza' else Ta), (J if grp == 'juniors' else S)
    if R.random() < 0.5:
        return mk('M', f"The table shows students' lunch choices.{tab}If a student who chose {food} is chosen at random, what is the probability that the student is one of the <b>{grp}</b>?",
            'By hand: the "given" group is your new total.', [f'"A student who chose {food}" = only look at that column. Total: {ft}', f'Of those, {grp}: {cell}', f'Probability = {cell}/{ft}'],
            'The group after "if" is the denominator.', N(Fr(cell, ft)), [N(Fr(cell, gt)), N(Fr(cell, T)), N(Fr(ft, T)), N(Fr(gt, T))],
            [f'P({food} given {grp})', f'P({grp} out of everyone)', f'P({grp} GIVEN {food})'], 2)
    g1 = grp[:-1]
    return mk('M', f"The table shows students' lunch choices.{tab}If one of the {grp} is chosen at random, what is the probability that the student chose <b>{food}</b>?",
        'By hand: the "given" group is your new total.', [f'"One of the {grp}" = only look at that row. Total: {gt}', f'Of those, chose {food}: {cell}', f'Probability = {cell}/{gt}'],
        'The group after "if" is the denominator.', N(Fr(cell, gt)), [N(Fr(cell, ft)), N(Fr(cell, T)), N(Fr(gt, T)), N(Fr(ft, T))],
        [f'P({grp} given {food})', f'P({food} out of everyone)', f'P({food} GIVEN a {g1})'], 2)
@gen('prob')
def _():
    n = R.choice([20, 24, 25, 30, 40, 48, 50, 60, 80, 100]); d = ri(1, n // 2); notq = R.random() < 0.7
    if notq:
        return mk('M', f'In a box of {n} light bulbs, {d} are defective. If one bulb is chosen at random, what is the probability that it is NOT defective?', 'By hand: 1 − P(defective).',
            [f'Good bulbs: {n} − {d} = {n - d}', f'P(not defective) = {n - d}/{n} = {N(Fr(n - d, n))}'], 'Read the NOT.', N(Fr(n - d, n)),
            [N(Fr(d, n)), N(Fr(n - d, d)), N(Fr(d, n - d))], ['P(defective)', 'P(NOT defective)', 'the number of good bulbs'], 1)
    return mk('M', f'In a box of {n} light bulbs, {d} are defective. If one bulb is chosen at random, what is the probability that it is defective?', 'By hand: defective ÷ all bulbs.',
        [f'Defective: {d}', f'All bulbs: {n}', f'P(defective) = {d}/{n} = {N(Fr(d, n))}'], 'Divide by ALL the bulbs, not just the good ones.', N(Fr(d, n)),
        [N(Fr(n - d, n)), N(Fr(d, n - d)), N(Fr(n - d, d))], ['P(DEFECTIVE)', 'P(not defective)', 'the number of good bulbs'], 0)
@gen('prob')
def _():
    a, b = R.choice([(1, 5), (1, 4), (2, 5), (3, 10), (1, 8), (3, 4), (2, 3), (1, 6), (7, 20)]); n = b * ri(5, 60)
    return mk('H', f'The probability that a randomly chosen customer buys a drink is {a}/{b}. Out of {N(n)} customers, how many would you expect to buy a drink?', 'By hand: probability × number of trials.',
        [f'{a}/{b} × {N(n)} = {N(n * a // b)}'], 'Expected count = probability × total.', N(n * a // b), [], ['the probability', 'customers who do NOT buy', 'the expected number'], 2, grid=True)

# ======================= infer =======================
@gen('infer')
def _():
    s = R.choice([100, 200, 250, 400, 500, 800]); pop = 1000 * ri(3, 30); k = ri(5, s * 3 // 4)
    est = Fr(k, s) * pop
    if est.denominator != 1: return None
    act = R.choice(['bike to class', 'live on campus', 'work a part-time job', 'eat breakfast on campus', 'take an online course', 'play an intramural sport'])
    return mk('M', f'In a random sample of {s} students at a university with {N(pop)} students, {k} said they {act}. Based on the sample, about how many students at the university {act}?',
        'By hand: sample fraction × population.', [f'Sample fraction: {k}/{s} = {k / s:g}', f'{k / s:g} × {N(pop)} = {N(est)}'], 'Scale the sample up to the whole population.', N(est),
        [k, N(pop - est), N(Fr(k * pop, s * 2)), N(Fr(k * 1000, s))], ['the number in the sample', 'the estimate for the whole university', 'the sample percent'], 1)
@gen('infer')
def _():
    p, m = ri(30, 80), ri(2, 6); topic = R.choice(['voters support a new park', 'residents support a later school start time', 'shoppers prefer paper bags', 'students want a longer lunch', 'drivers support a new bike lane', 'members want the pool open later'])
    ins = p + R.choice([v for v in range(-m + 1, m) if v != 0]) if m > 1 else p
    return mk('M', f'A survey estimates that {p}% of {topic.split(" ", 1)[0]} {topic.split(" ", 1)[1]}, with a margin of error of {m} percentage points. Which value is a plausible percent of all {topic.split(" ", 1)[0]} who {topic.split(" ", 1)[1].replace("supports", "support")}?'.replace(' who support ', ' who support ').replace('who prefer', 'who prefer'),
        'By hand: plausible values are estimate ± margin.', [f'Low end: {p} − {m} = {p - m}%', f'High end: {p} + {m} = {p + m}%', f'Plausible: anything from {p - m}% to {p + m}%. {ins}% is inside.'],
        'Values outside the ± range are not plausible.', f'{ins}%', [f'{p - m - ri(2, 6)}%', f'{p + m + ri(2, 6)}%', f'{100 - p}%' if abs(100 - 2 * p) > m else f'{p + 2 * m + 5}%'],
        ['a value inside the margin of error', 'the exact true value', 'the margin of error'], 0)
TOP = ['the average height of plants in a greenhouse', 'the percent of shoppers who use coupons', 'the average commute time of employees', 'the percent of residents who recycle',
       'the average number of hours teens sleep', 'the average weight of apples in an orchard', 'the percent of voters who support a new library', 'the average price of used cars in a city',
       'the percent of students who walk to school', 'the average length of fish in a lake', 'the percent of households with a pet', 'the average time customers wait in line']
@gen('infer')
def _():
    t = R.choice(TOP)
    return mk('H', f'A researcher estimates {t} using a random sample, and the margin of error is too large. Which change would most likely make the margin of error smaller?',
        'Rule: bigger random sample → smaller margin of error.', ['Margin of error depends mostly on sample size.', 'More data = less uncertainty.', 'Volunteers make it biased, not more precise.'],
        'Smaller samples make the margin BIGGER.', 'Use a larger random sample.', ['Use a smaller random sample.', 'Survey only volunteers.', 'Report the answer as a whole number.'],
        ['what changes the estimate', 'what makes it biased', 'what shrinks the margin of error'], 2)
PLACES = [('high school', 'All students at that high school', 'Everyone in the state', 'Everyone in the country'), ('town library', 'All visitors to that town library', 'Everyone in the town', 'All library users in the country'),
          ('gym', 'All members of that gym', 'Everyone in the city', 'All gym members in the country'), ('bakery', 'All customers of that bakery', 'Everyone in the city', 'All bakery customers in the state'),
          ('soccer league', 'All players in that soccer league', 'All athletes in the state', 'Everyone in the country'), ('apartment building', 'All residents of that apartment building', 'Everyone in the city', 'All renters in the country'),
          ('hospital', 'All patients at that hospital', 'Everyone in the state', 'All patients in the country'), ('movie theater', 'All customers of that movie theater', 'Everyone in the city', 'All moviegoers in the country'),
          ('college', 'All students at that college', 'All college students in the country', 'Everyone in the state'), ('company', 'All employees of that company', 'All workers in the state', 'Everyone in the country')]
@gen('infer')
def _():
    p, ok, w1, w2 = R.choice(PLACES)
    return mk('H', f'A random sample of people from one {p} was surveyed. To which group can the results be generalized most appropriately?',
        'Rule: results apply only to the group that was randomly sampled.', [f'The sample was drawn at random from one {p}.', f'So the results apply to {ok[0].lower() + ok[1:]}.', 'Not to a bigger group that was never sampled.'],
        'You cannot generalize beyond the group that was sampled.', ok, [w1, w2, 'Only the people who answered'], ['the size of the sample', 'the group the results apply to', 'the result of the survey'], 1)

# ======================= claims =======================
TREAT = [('listening to music while studying', 'higher test scores', 'students'), ('drinking green tea before bed', 'better sleep', 'adults'),
         ('a 4-day work week', 'higher productivity', 'workers'), ('a new running shoe', 'faster mile times', 'runners'), ('a daily stretching program', 'less back pain', 'patients'),
         ('putting phones away at night', 'higher grades', 'teens'), ('a new store layout', 'more spending', 'shoppers'), ('a dashboard safety alert', 'faster braking', 'drivers'),
         ('standing desks', 'fewer sick days', 'employees'), ('a new warm-up routine', 'faster lap times', 'swimmers'), ('a daily reading app', 'larger vocabularies', 'children'),
         ('a morning walk', 'lower stress', 'nurses'), ('a free tutoring program', 'higher math scores', 'students'), ('a plant-based lunch menu', 'more energy in the afternoon', 'office workers'),
         ('a 10-minute meditation break', 'fewer mistakes', 'pilots in training'), ('a new fertilizer', 'taller tomato plants', 'gardeners')]
def cap(s): return s[0].upper() + s[1:]
@gen('claims')
def _():
    t, out, who = R.choice(TREAT); n = 20 * ri(5, 25); form = R.choice(['exp', 'obs', 'design'])
    if form == 'exp':
        return mk('M', f'A researcher selected {n} {who} at random from a large city. Half were <b>randomly assigned</b> to {t}; the other half were not. The group with {t} had {out}. Which conclusion is best supported?',
            'Rule: random ASSIGNMENT → cause. Random SAMPLE → generalize to that population.',
            ['Random sample from the city → can generalize to that city.', 'Random assignment → can say it CAUSED the difference.', 'Both → cause, for that city only.'],
            '"Everywhere" goes beyond the population that was sampled.', f'{cap(t)} likely caused {out} among {who} in that city.',
            [f'{cap(t)} causes {out} for all {who} everywhere.', 'There is a link, but no cause can be concluded.', f'The results apply only to the {n} {who} in the study.'],
            ['the result', 'what the study design allows', 'the sample size'], 1)
    if form == 'obs':
        return mk('M', f'A survey of {n} {who} found that those who chose {t} on their own had {out}. No one was assigned to a group. Which conclusion is best supported?',
            'Rule: no random assignment (observational) → link only, never cause.',
            ['People chose their own group → observational study.', 'Other differences could explain the result.', 'So: an association, not proof of cause.'],
            'Without random assignment, never pick "causes".', f'There is an association between {t} and {out}, but cause cannot be determined.',
            [f'{cap(t)} causes {out}.', f'{cap(t)} has no effect.', f'All {who} should try {t}.'], ['the result', 'the sample size', 'what the study design allows'], 2)
    return mk('M', f'A researcher wants to know whether {t} <b>causes</b> {out} for {who}. Which study design would best answer this?',
        'Rule: to show cause, randomly ASSIGN the treatment and keep a comparison group.',
        ['Cause needs an experiment.', 'Random assignment makes the groups alike except for the treatment.', 'A comparison group is required.'],
        'People choosing their own group = observational = no cause.', f'Randomly assign {who} to {t} or to no change, then compare the groups.',
        [f'Survey {who} about whether they like {t}.', f'Compare {who} who already chose {t} with those who did not.', f'Give {t} to every one of the {who} and measure the results.'],
        ['the design that shows a link', 'the result', 'the design that shows CAUSE'], 2)

# ======================= area =======================
@gen('area')
def _():
    l, w = ri(3, 25), ri(2, 20)
    if l == w: return None
    if R.random() < 0.5:
        return mk('E', f'A rectangle has a length of {l} inches and a width of {w} inches. What is its perimeter, in inches?', 'Reference sheet: A = ℓw. Perimeter = add all 4 sides.',
            ['Perimeter = 2 × (length + width)', f'2 × ({l} + {w}) = {2 * (l + w)}'], 'Area = inside (multiply). Perimeter = the edge (add).', 2 * (l + w), [l * w, l + w, 2 * l * w], ['the area', 'the perimeter', 'the diagonal'], 1)
    return mk('E', f'A rectangle has a length of {l} inches and a width of {w} inches. What is its area, in square inches?', 'Reference sheet: A = ℓw.',
        ['Area = length × width', f'{l} × {w} = {l * w}'], 'Area = inside (multiply). Perimeter = the edge (add).', l * w, [2 * (l + w), l + w, 2 * l * w], ['the AREA', 'the perimeter', 'the diagonal'], 0)
@gen('area')
def _():
    r, h = ri(2, 10), ri(2, 15)
    return mk('M', f'A cylinder has a radius of {r} centimeters and a height of {h} centimeters. What is its volume, in cubic centimeters?', 'Reference sheet: V = πr²h (it is on the test!).',
        ['V = πr²h', f'r² = {r}² = {r * r}', f'V = π({r * r})({h}) = {N(r * r * h)}π'], 'Square the radius. If you are given the diameter, halve it first.', f'{N(r * r * h)}π',
        [f'{N(2 * r * h)}π', f'{N(r * h)}π', f'{N(4 * r * r * h)}π', f'{N(r * r * h * h)}π'], ['the surface area', 'the area of the base', 'the volume'], 2)
@gen('area')
def _():
    k, A = ri(2, 6), ri(3, 25)
    return mk('M', f'Two similar triangles have corresponding sides in the ratio 1 to {k}. The smaller triangle has an area of {A} square units. What is the area of the larger triangle?',
        'Rule: sides × k → area × k², volume × k³.', [f'Side scale factor: {k}', f'Area scale factor: {k}² = {k * k}', f'Area: {A} × {k * k} = {A * k * k}'],
        f'Area grows by {k}² = {k * k}, not by {k}.', A * k * k, [A * k, A * k ** 3, A + k * k, A * 2 * k], ['the larger AREA', 'the larger side', 'the scale factor'], 0)
@gen('area')
def _():
    V, k = ri(2, 12), ri(2, 5)
    return mk('H', f'A cube-shaped box has a volume of {V} cubic feet. A second box has every edge {k} times as long. What is the volume of the second box, in cubic feet?',
        'Rule: lengths × k → volume × k³.', [f'Length scale factor: {k}', f'Volume scale factor: {k}³ = {k ** 3}', f'{V} × {k ** 3} = {V * k ** 3}'],
        'Volume uses k CUBED.', V * k ** 3, [V * k, V * k * k, V + k ** 3, k ** 3], ['the new edge length', 'the new VOLUME', 'the scale factor'], 1)
@gen('area')
def _():
    r = 3 * ri(1, 6); d = 2 * r; v = Fr(4, 3) * r ** 3
    return mk('H', f'A sphere has a diameter of {d} inches. What is its volume, in cubic inches?', 'Reference sheet: V = (4/3)πr³.',
        [f'Radius = half the diameter: {d} ÷ 2 = {r}', f'r³ = {r ** 3}', f'V = (4/3)π({r ** 3}) = {N(v)}π'], 'They gave the DIAMETER. Halve it first.', f'{N(v)}π',
        [f'{N(Fr(4, 3) * d ** 3)}π', f'{N(4 * r * r)}π', f'{N(Fr(4, 3) * r * r)}π'], ['the diameter', 'the surface area', 'the volume (use the RADIUS)'], 2)

# ======================= lat =======================
@gen('lat')
def _():
    a, b = ri(20, 100), ri(20, 100)
    if a + b >= 170: return None
    c = 180 - a - b
    return mk('E', f'In triangle ABC, angle A measures {a}° and angle B measures {b}°. What is the measure, in degrees, of angle C?', "Rule: a triangle's angles add to 180°.",
        [f'{a} + {b} = {a + b}', f'180 − {a + b} = {c}'], 'Triangles add to 180°, not 360°.', c, [360 - a - b, a + b, abs(a - b) + 1, 90 - c if c < 90 else c - 90], ['angle A + angle B', 'angle C', 'the exterior angle'], 1)
@gen('lat')
def _():
    a = ri(25, 155)
    if a == 90: return None
    if R.random() < 0.5:
        return mk('M', f'Two lines intersect. One of the angles formed measures {a}°. What is the measure of the angle directly across from it (vertical angle)?', 'Rules: vertical angles are equal; angles on a line add to 180°.',
            ['Across = vertical angles, which are EQUAL', f'Answer: {a}°'], 'Across → equal. Side by side on a line → add to 180.', f'{a}°', [f'{180 - a}°', f'{abs(90 - a)}°', f'{360 - a}°'],
            ['the angle next to it', 'a right angle', 'the angle they point to'], 2)
    return mk('M', f'Two lines intersect. One of the angles formed measures {a}°. What is the measure of the angle next to it on the same line?', 'Rules: vertical angles are equal; angles on a line add to 180°.',
        ['Side by side on a line = a linear pair, which adds to 180°', f'180 − {a} = {180 - a}°'], 'Across → equal. Side by side on a line → add to 180.', f'{180 - a}°', [f'{a}°', f'{abs(90 - a)}°', f'{360 - a}°'],
        ['the angle across from it', 'a right angle', 'the angle beside it (linear pair)'], 2)
@gen('lat')
def _():
    a = ri(25, 155)
    if a == 90: return None
    if R.random() < 0.5:
        return mk('M', f'Lines m and n are parallel and are cut by a transversal. One angle measures {a}°. What is the measure of its same-side interior angle?',
            'Parallel lines: angles are either EQUAL or add to 180°. Big looks big, small looks small.', ['Same-side interior angles are supplementary (add to 180°)', f'Answer: {180 - a}°'],
            'Only two sizes exist with parallel lines: x and 180 − x.', f'{180 - a}°', [f'{a}°', f'{360 - a}°', f'{abs(90 - a)}°'], ['the same-side interior angle', 'the vertical angle', 'the sum of the angles'], 0)
    return mk('M', f'Lines m and n are parallel and are cut by a transversal. One angle measures {a}°. What is the measure of its corresponding angle?',
        'Parallel lines: angles are either EQUAL or add to 180°. Big looks big, small looks small.', ['Corresponding angles are in the same spot at each crossing, so they are EQUAL', f'Answer: {a}°'],
        'Only two sizes exist with parallel lines: x and 180 − x.', f'{a}°', [f'{180 - a}°', f'{360 - a}°', f'{abs(90 - a)}°'], ['the corresponding angle', 'the same-side interior angle', 'the sum of the angles'], 0)
@gen('lat')
def _():
    a, b = ri(25, 85), ri(25, 85); c = 180 - a - b
    return mk('H', f'In a triangle, two interior angles measure {a}° and {b}°. What is the measure of the exterior angle next to the third angle?', 'Rule: an exterior angle = the two far interior angles added.',
        [f'Third interior angle: 180 − {a} − {b} = {c}°', f'Exterior angle: 180 − {c} = {a + b}°', f'(Shortcut: {a} + {b} = {a + b}°)'], 'The exterior angle is OUTSIDE: 180 minus the third angle.',
        f'{a + b}°', [f'{c}°', f'{360 - a - b}°', f'{abs(a - b)}°' if a != b else f'{c + 10}°'], ['the third interior angle', 'the EXTERIOR angle', 'the sum of all angles'], 1)
@gen('lat')
def _():
    pq, qr, k = ri(2, 9), ri(3, 12), ri(2, 5)
    if pq == qr: return None
    st = pq * k
    return mk('H', f'Triangles PQR and STU are similar, with P ↔ S, Q ↔ T and R ↔ U. PQ = {pq}, QR = {qr}, and ST = {st}. What is the length of TU?', 'Rule: similar shapes multiply every side by the same scale factor.',
        [f'Scale factor: ST ÷ PQ = {st} ÷ {pq} = {k}', f'TU matches QR: {qr} × {k} = {qr * k}'], 'Similar = MULTIPLY by the scale factor, not add.', qr * k,
        [qr + (st - pq), st, N(Fr(qr, k)), qr * k + k], ['ST', 'the scale factor', 'TU (matches QR)'], 2)

# ======================= trig =======================
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37), (11, 60, 61), (28, 45, 53), (33, 56, 65)]
@gen('trig')
def _():
    a, b, c = R.choice(TRIP); k = R.choice([1, 1, 2, 3]) if c < 30 else 1; a, b, c = a * k, b * k, c * k
    return mk('E', f'A right triangle has legs of length {a} and {b}. What is the length of the hypotenuse?', 'Reference sheet: a² + b² = c².',
        [f'{a}² + {b}² = {a * a} + {b * b} = {c * c}', f'c = √{c * c} = {c}'], 'Square, add, THEN take the square root.', c, [a + b, N(c * c), b - a, N(Fr(a + b, 2)) if (a + b) % 2 == 0 else b + 1],
        ['a leg', 'the hypotenuse (longest side)', 'the area'], 1)
@gen('trig')
def _():
    o, a, h = R.choice(TRIP)
    if R.random() < 0.5: o, a = a, o
    fn = R.choice(['sin', 'cos', 'tan'])
    val = {'sin': Fr(o, h), 'cos': Fr(a, h), 'tan': Fr(o, a)}[fn]; raw = {'sin': f'{o}/{h}', 'cos': f'{a}/{h}', 'tan': f'{o}/{a}'}[fn]
    word = {'sin': 'SIN = Opposite/Hypotenuse', 'cos': 'COS = Adjacent/Hypotenuse', 'tan': 'TAN = Opposite/Adjacent'}[fn]
    allv = [N(Fr(o, h)), N(Fr(a, h)), N(Fr(o, a)), N(Fr(a, o))]
    return mk('M', f'In right triangle WXY, angle Y is the right angle. The side opposite angle W has length {o}, the side adjacent to angle W has length {a}, and the hypotenuse has length {h}. What is {fn}(W)?',
        'SOH-CAH-TOA: Sin = Opp/Hyp, Cos = Adj/Hyp, Tan = Opp/Adj.', [word, f'= {raw}', f'= {N(val)}'],
        'Tan has NO hypotenuse in it. SOH-CAH-TOA.' if fn == 'tan' else 'Sin and cos both use the hypotenuse; pick the right leg. SOH-CAH-TOA.', N(val), allv,
        ['the hypotenuse', f'{fn}(W)', 'cos(W)' if fn != 'cos' else 'sin(W)'], 1)
@gen('trig')
def _():
    x = ri(2, 20)
    return mk('M', f'In a 30°−60°−90° triangle, the side opposite the 30° angle has length {x}. What is the length of the hypotenuse?', 'Reference sheet: 30-60-90 sides are x, x√3, 2x.',
        [f'Short leg (opposite 30°) = x = {x}', f'Hypotenuse = 2x = {2 * x}'], 'x√3 is the LONGER LEG, not the hypotenuse.', 2 * x, [f'{x}√3', f'{x}√2', 3 * x, N(Fr(x, 2)) if x % 2 == 0 else x + 2],
        ['the longer leg', 'the angle', 'the hypotenuse'], 2)
@gen('trig')
def _():
    x = ri(2, 20)
    return mk('M', f'An isosceles right triangle (45°−45°−90°) has legs of length {x}. What is the length of the hypotenuse?', 'Reference sheet: 45-45-90 sides are x, x, x√2.',
        [f'Legs: x = {x}', f'Hypotenuse = x√2 = {x}√2'], '√2 goes with 45-45-90; √3 goes with 30-60-90.', f'{x}√2', [2 * x, f'{x}√3', x * x], ['a leg', 'the hypotenuse', 'the area'], 1)
@gen('trig')
def _():
    o, a, h = R.choice(TRIP); A = ri(12, 78)
    if A == 45: return None
    return mk('H', f'In a right triangle, sin({A}°) = {o}/{h}. What is cos({90 - A}°)?', 'Rule: sin(x°) = cos(90° − x°) (complementary angles).',
        [f'{A}° + {90 - A}° = 90°: complementary angles', 'sin of one = cos of the other', f'cos({90 - A}°) = {o}/{h}'], 'Do not compute anything; the angles add to 90°.', f'{o}/{h}',
        [f'{a}/{h}', f'{h}/{o}', f'{o}/{a}', f'{h - o}/{h}'], [f'cos({90 - A}°)', f'cos({A}°)', f'sin({90 - A}°)'], 0)
@gen('trig')
def _():
    k, n = R.choice([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 9), (1, 10), (1, 12), (2, 3), (3, 4), (5, 6), (3, 2), (5, 4), (7, 6), (2, 5), (4, 3)])
    deg = Fr(180 * k, n)
    if deg.denominator != 1: return None
    top = 'π' if k == 1 else f'{k}π'
    return mk('H', f'An angle measures {top}/{n} radians. What is its measure in degrees?', 'Rule: π radians = 180°. Desmos may be in radian mode, so check the setting.',
        ['Replace π with 180°', f'{"" if k == 1 else f"{k} × "}180° ÷ {n} = {N(deg)}°'], f'{n} is the denominator, not the angle.', f'{N(deg)}°',
        [f'{n}°', f'{180 * n // k if (180 * n) % k == 0 else 180 * n}°', f'{N(deg * 2)}°', f'{N(Fr(90 * k, n))}°'], ['the angle in DEGREES', 'the angle in radians', 'the number n'], 0)

# ======================= circ =======================
@gen('circ')
def _():
    r = ri(2, 20)
    return mk('E', f'A circle has a radius of {r}. What is its area?', 'Reference sheet: A = πr², C = 2πr.', [f'A = πr² = π({r})²', f'= {r * r}π'],
        'Area squares r. Circumference doubles r.', f'{r * r}π', [f'{2 * r}π', f'{r}π', f'{4 * r * r}π'], ['the circumference', 'the area', 'the diameter'], 1)
@gen('circ')
def _():
    d = ri(6, 90)
    return mk('M', f'The circumference of a circle is {d}π inches. What is the diameter of the circle, in inches?', 'Rule: C = πd, so d = C ÷ π.',
        ['C = πd', f'{d}π = πd', f'd = {d}'], f'Do not type {d}π as a decimal ({d * math.pi:.1f}). They asked for the diameter: {d}.', d, [], ['the circumference', 'the radius', 'the DIAMETER'], 2, grid=True)
@gen('circ')
def _():
    r, ang = ri(2, 12), R.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 180, 240, 270, 300])
    f = Fr(ang, 360)
    if R.random() < 0.6:
        v = f * 2 * r
        return mk('M', f'A circle has a radius of {r}. A central angle measures {ang}°. What is the arc length of the part of the circle cut off by this angle?', 'Rule: fraction of the circle = angle ÷ 360.',
            [f'Fraction: {ang}/360 = {N(f)}', f'Whole circumference: {2 * r}π', f'{N(f)} × {2 * r}π = {N(v)}π'], 'Divide the angle by 360, not 180.', f'{N(v)}π'.replace('1π', 'π') if v == 1 else f'{N(v)}π',
            [f'{N(v * 2)}π', f'{N(f * r * r)}π', f'{2 * r}π', f'{N(v / 2)}π'], ['the arc length', 'the sector area', 'the whole circle'], 0)
    v = f * r * r
    return mk('M', f'A circle has a radius of {r}. A central angle measures {ang}°. What is the sector area of the part of the circle cut off by this angle?', 'Rule: fraction of the circle = angle ÷ 360.',
        [f'Fraction: {ang}/360 = {N(f)}', f'Whole area: {r * r}π', f'{N(f)} × {r * r}π = {N(v)}π'], 'Divide the angle by 360, not 180.', f'{N(v)}π',
        [f'{N(v * 2)}π', f'{N(f * 2 * r)}π', f'{r * r}π', f'{N(v / 2)}π'], ['the sector area', 'the arc length', 'the whole circle'], 0)
@gen('circ')
def _():
    h, k, r = R.choice([v for v in range(-8, 9) if v]), R.choice([v for v in range(-8, 9) if v]), ri(2, 10)
    c = h * h + k * k - r * r
    eq = f'x²{sg(-2 * h)}x + y²{sg(-2 * k)}y{sg(c) if c else ""} = 0'
    return mk('H', f'The equation of a circle in the xy-plane is {eq}. What is the radius of the circle?', 'Desmos: type the equation, read the radius off the graph. Or complete the square.',
        [f'Complete the square for x: x²{sg(-2 * h)}x → (x{sg(-h)})², add {h * h}', f'For y: y²{sg(-2 * k)}y → (y{sg(-k)})², add {k * k}',
         f'(x − h)² + (y − k)² = {h * h} + {k * k}{sg(-c)} = {r * r}', f'r = √{r * r} = {r}'], 'The right side is r². Take the square root.', r,
        [r * r, abs(c) if abs(c) not in (r, r * r) else r + 1, h * h + k * k, 2 * r], ['r²', 'the radius', 'the center'], 1)
@gen('circ')
def _():
    a, b, c = R.choice(TRIP); k = R.choice([1, 1, 2]) if c < 30 else 1; a, b, c = a * k, b * k, c * k
    if R.random() < 0.5: a, b = b, a
    return mk('H', f'A line is tangent to a circle with center O at point T. The radius OT is {a}. Point P is on the tangent line, and TP = {b}. What is the distance OP?',
        'Rule: a tangent line meets the radius at a RIGHT angle → Pythagorean theorem.', ['Radius ⟂ tangent: triangle OTP has a right angle at T', f'OP² = {a}² + {b}² = {c * c}', f'OP = {c}'],
        'Tangent + radius = right angle. That is the whole trick.', c, [a + b, abs(b - a), a * b, c + 1], ['the radius', 'TP', 'OP (from the center to P)'], 2)

# ======================= run =======================
def main():
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    B = json.load(open(BANK)); qs = B['qs']
    seen = {re.sub(r'\s+', ' ', q['q']) for q in qs}
    added = 0
    for sk in G:
        have = [q for q in qs if q['skill'] == sk]
        nums = [int(q['id'].split('-')[1]) for q in have]; nxt = max(nums) + 1
        need = target - len(have); tries = 0
        # spread new questions evenly across this skill's templates (E/M/H mix like the bank)
        while need > 0 and tries < 20000:
            tries += 1
            fn = G[sk][(tries) % len(G[sk])]
            d = fn()
            if not d: continue
            key = re.sub(r'\s+', ' ', d['q'])
            if key in seen: continue
            seen.add(key)
            d = {'id': f'{sk}-{nxt:02d}', 'skill': sk, **d}; nxt += 1
            qs.append(d); need -= 1; added += 1
        if need > 0: print('short', sk, need)
    for s in B['skills']: s['n'] = sum(1 for q in qs if q['skill'] == s['id'])
    json.dump(B, open(BANK, 'w'), ensure_ascii=False, indent=0)
    print('added', added, 'total', len(qs))
if __name__ == '__main__': main()
