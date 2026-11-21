#!/usr/bin/env python3
"""Harder math questions modeled on the College Board question bank's Medium/Hard items
(structure and stems only; every question is original). Adds `per` new questions per template.
    python3 hardgen.py [per_template]   (default 12)"""
import sys, os, json, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathgen import mk, N, P, sg, cx, sup, quad, lin, R, ri, Fr, BANK

H = {}
def gen(skill):
    def d(fn): H.setdefault(skill, []).append(fn); return fn
    return d

# ---------------- nonlinear functions ----------------
@gen('nlf')
def _():
    P0 = R.choice([200, 250, 400, 500, 800, 1200, 1500]); k = R.choice([2, 3, 4, 5, 6, 10]); r = R.choice([5, 10, 15, 20, 25, 40, 50]); b = 1 + r / 100
    return mk('H', f'The function f is defined by f(x) = {N(P0)}({b:g}){sup(f"x/{k}")}. By what percent does the value of f(x) increase for every increase of x by {k}?',
        f'Desmos: type f(x) = {P0}({b:g})^(x/{k}), then f({k}) ÷ f(0).',
        [f'Increase x by {k}: the exponent x/{k} goes up by exactly 1', f'So f(x) is multiplied by {b:g} one time', f'{b:g} = 1 + {r / 100:g}, so the value grows by {r}%'],
        f'{b:g} is the growth FACTOR. The percent is the part after the 1: {r}%.', r, [], ['the growth factor', 'the percent increase', 'the starting value'], 1, grid=True)
@gen('nlf')
def _():
    p, q = ri(-9, 12), ri(-9, 12)
    if p == q or (p + q) % 2: return None
    v = (p + q) // 2
    return mk('H', f'The function f is defined by f(x) = {lin(p)}{lin(q)}. For what value of x does f(x) reach its minimum?',
        f'Desmos: graph y = {lin(p)}{lin(q)} and click the lowest point; read the x-value.',
        [f'The zeros are x = {P(p)} and x = {P(q)}', 'A parabola is symmetric, so its lowest point is exactly halfway between the zeros', f'({P(p)} + {P(q)}) ÷ 2 = {P(v)}'],
        f'They asked for the x-value of the minimum, not the minimum value of f(x).', P(v), [], ['the minimum value of f(x)', 'the x-value where f is lowest', 'the zeros'], 1, grid=True)
@gen('nlf')
def _():
    a, r = R.choice([2, 3, 4, 5, 6, 8, 10, 12]), R.choice([2, 3, 4, 5])
    return mk('M', f'The first term of a sequence is {a}. Each term after the first is {r} times the preceding term. If w represents the nth term of the sequence, which equation gives w in terms of n?',
        'Rule: nth term = first term × (ratio)^(n − 1).',
        [f'First term: {a}. Each step multiplies by {r}.', f'Term 1 has 0 multiplications, term 2 has 1, so term n has n − 1', f'w = {a}({r}){sup("n − 1")}'],
        'The first term is not multiplied yet, so the exponent is n − 1, not n.', f'w = {a}({r}){sup("n − 1")}',
        [f'w = {a}({r}){sup("n")}', f'w = {r}({a}){sup("n − 1")}', f'w = {a} + {r}(n − 1)'], ['the 2nd term', 'an equation for the nth term', 'the ratio'], 1)
@gen('nlf')
def _():
    a, b, c = R.choice([2, 3, 4, 5, 6, 8, 10, 20]), R.choice([0.5, 1.5, 2, 3, 0.8, 1.2]), R.choice([v for v in range(-9, 13) if v])
    return mk('M', f'The function f is defined by f(x) = {a}({b:g}){sup("x")}{sg(c)}. What is the y-intercept of the graph of y = f(x) in the xy-plane?',
        f'Desmos: type f(x) = {a}({b:g})^x {"+" if c > 0 else "−"} {abs(c)} and click where it crosses the y-axis.',
        ['The y-intercept is where x = 0', f'({b:g})^0 = 1, so f(0) = {a}(1){sg(c)}', f'f(0) = {P(a + c)}, so the y-intercept is (0, {P(a + c)})'],
        f'Anything to the 0 power is 1, so the y-intercept is NOT just {a}. Add the {P(c)}.', f'(0, {P(a + c)})',
        [f'(0, {a})', f'(0, {P(c)})', f'(0, {N(round(a * b + c, 2))})', f'({P(a + c)}, 0)'], ['the x-intercept', 'the y-intercept (x = 0)', 'the growth factor'], 1)
@gen('nlf')
def _():
    h, k = ri(-5, 6), ri(-9, 9); a = R.choice([-3, -2, -1, 1, 2, 3, 4]); x1 = h + R.choice([-3, -2, -1, 1, 2, 3]); y1 = a * (x1 - h) ** 2 + k
    return mk('H', f'The graph of the quadratic function f has its vertex at ({P(h)}, {P(k)}) and passes through the point ({P(x1)}, {P(y1)}). If f(x) = a(x − h)² + k, what is the value of a?',
        f'Desmos: type y = a(x − ({P(h)}))² + ({P(k)}), add a slider for a, and slide until the graph passes through ({P(x1)}, {P(y1)}).',
        [f'Vertex (h, k) = ({P(h)}, {P(k)}): f(x) = a(x − ({P(h)}))² + ({P(k)})', f'Plug in the point: {P(y1)} = a({P(x1)} − ({P(h)}))² + ({P(k)})', f'{P(y1 - k)} = a({(x1 - h) ** 2})', f'a = {P(a)}'],
        'Plug in the OTHER point, not the vertex. The vertex alone cannot tell you a.', P(a), [], ['the vertex', 'the constant a (the stretch)', 'the y-intercept'], 1, grid=True)

# ---------------- nonlinear equations ----------------
@gen('nleq')
def _():
    k = ri(2, 12); c = k * k
    return mk('H', f'x² + bx + {c} = 0<br>In the given equation, b is a positive constant. The equation has exactly one real solution. What is the value of b?',
        'Discriminant rule. Desmos check: slider for b; the graph should just touch the x-axis.',
        ['Exactly one real solution: b² − 4ac = 0', f'b² − 4(1)({c}) = 0 → b² = {4 * c}', f'b is positive: b = √{4 * c} = {2 * k}'],
        f'One solution means the discriminant equals 0, not less than 0.', 2 * k, [], ['x', 'the value of b for ONE solution', 'the number of solutions'], 1, grid=True)
@gen('nleq')
def _():
    m = 2 * ri(1, 5) * R.choice([1, -1]); c = ri(-6, 10); bb = Fr(c) - Fr(m * m, 4)
    return mk('H', f'In the xy-plane, a line with equation y = {cx(m)} + b, where b is a constant, intersects the parabola y = x²{sg(c) if c else ""} at exactly one point. What is the value of b?',
        f'Desmos: graph y = x²{sg(c) if c else ""} and y = {cx(m)} + b with a slider for b. Slide until the line just touches the parabola.',
        [f'Set them equal: x²{sg(c) if c else ""} = {cx(m)} + b', f'x² {"−" if m > 0 else "+"} {abs(m)}x + ({P(c)} − b) = 0', 'Exactly one point: discriminant = 0', f'{m * m} − 4({P(c)} − b) = 0 → b = {N(bb)}'],
        'Exactly one intersection = discriminant 0.', N(bb), [], ['the x-value of the point', 'b, so the line touches once', 'the slope'], 1, grid=True)
@gen('nleq')
def _():
    r = ri(3, 12); b = ri(1, r - 1); s = r - b; a = s * s - r
    if a <= 0: return None
    other = 2 * b + 1 - r
    if other - b >= 0 or other + a < 0: return None
    return mk('H', f'√(x + {a}) = x − {b}<br>What is the solution to the given equation?', f'Desmos: graph y = √(x + {a}) and y = x − {b}; click the crossing point.',
        [f'Square both sides: x + {a} = (x − {b})² = x² − {2 * b}x + {b * b}', f'x² − {2 * b + 1}x + {b * b - a} = 0 → x = {r} or x = {P(other)}', f'Check x = {P(other)}: the right side is {P(other - b)}, negative, but a square root is never negative. Reject it.', f'Solution: x = {r}'],
        'Squaring can add a fake solution. Plug both back in.', r, [P(other), f'{r} and {P(other)}', 'There is no solution.'], ['every value from squaring', 'the solution that checks', 'the extra (fake) solution'], 1)
@gen('nleq')
def _():
    p, q, k = ri(1, 9), ri(1, 9), ri(1, 20)
    if p == q: return None
    return mk('M', f'(x − {p})(x + {q}) = {k}<br>What is the sum of the solutions to the given equation?', 'Desmos: graph y = (x − p)(x + q) and y = k, click both crossings, then add the x-values.',
        [f'Expand and move {k} over: x² + {P(q - p)}x − {p * q} − {k} = 0'.replace('+ −', '− '), 'Sum of the solutions of x² + bx + c = 0 is −b', f'Sum = {P(p - q)}'],
        f'{p} and −{q} are NOT the solutions: the right side is {k}, not 0.', N(p - q), [N(q - p), N(p + q), N(-p * q - k), N(k)], ['the product of the solutions', 'the SUM of the solutions', 'one solution'], 1)
@gen('nleq')
def _():
    a, c = R.choice([2, 3, 4, 5]), R.choice([v for v in range(-12, 13) if v])
    r1, r2 = R.sample([v for v in range(-6, 7) if v], 2)
    # a(x − r1)(x − r2) = 0 written as ax² + bx + c
    B, C = -a * (r1 + r2), a * r1 * r2
    return mk('M', f'{a}x²{sg(B)}x{sg(C)} = 0<br>What is the product of the solutions to the given equation?'.replace(' 1x', ' x').replace('+ 0x', ''),
        'Desmos: graph it, click both x-intercepts, then multiply them.', [f'Divide by {a}: x² {"−" if r1 + r2 > 0 else "+"} {abs(r1 + r2)}x {"+" if r1 * r2 > 0 else "−"} {abs(r1 * r2)} = 0', 'Product of the solutions = c ÷ a', f'{P(C)} ÷ {a} = {P(r1 * r2)}'],
        f'Divide by the leading {a} first: the product is c/a, not c.', N(r1 * r2), [N(C), N(r1 + r2), N(-r1 * r2), N(Fr(-B, a))], ['the sum', 'the PRODUCT of the solutions', 'the larger solution'], 1) if B else None

# ---------------- linear functions ----------------
CTX2 = [('the demand', 'units', 'the selling price', 'dollars per unit'), ('the number of visitors', 'visitors', 'the ticket price', 'dollars'),
        ('the amount of water in a tank', 'gallons', 'the time since the tank started draining', 'minutes')]
CTX2_UP = [('the number of members in a club', 'members', 'the time since the club opened', 'months')]
@gen('linf')
def _():
    m = R.choice([-250, -200, -150, -100, -50, -4, -2, 2, 5, 50]); y, yu, x, xu = R.choice(CTX2 if m < 0 else CTX2_UP); x1 = ri(2, 20) * (10 if abs(m) >= 50 else 1); dx = R.choice([5, 10, 20]) * (1 if abs(m) >= 50 else 1); b = abs(m) * 100 + ri(100, 2000)
    y1, x2, x3 = m * x1 + b, x1 + dx, x1 + 2 * dx + R.choice([0, 5])
    y2, y3 = m * x2 + b, m * x3 + b
    if min(y1, y2, y3) <= 0: return None
    return mk('H', f'An analyst modeled {y}, in {yu}, as a linear function of {x}, in {xu}. {y.capitalize()} was {N(y1)} when {x} was {x1}, and {N(y2)} when {x} was {x2}. Based on the model, what is {y} when {x} is {x3}?',
        'Desmos: put the two points in a table, use y₁ ~ m x₁ + b, then plug in the new x.',
        [f'Slope: ({N(y2)} − {N(y1)}) ÷ ({x2} − {x1}) = {N(m)} per 1 of {x}', f'From {x1} to {x3} is {x3 - x1}', f'{N(y1)} + {N(m)}({x3 - x1}) = {N(y3)}'],
        'Find the rate first, then move from a known point.', N(y3), [N(y3 - m), N(y2 + m * (x3 - x2) * 2), N(y1 + m * x3), N(y3 + m)], ['the slope', f'{y} at the new {x}', 'the y-intercept'], 1)
@gen('linf')
def _():
    job = R.choice(['A window repair specialist', 'A plumber', 'An electrician', 'A tutor', 'A boat mechanic']); a, k, r = 5 * ri(10, 40), R.choice([1, 2, 3]), 5 * ri(6, 20)
    unit = 'hour' if k == 1 else f'{k} hours'
    return mk('H', f'{job} charges ${a} for the first {unit} of work plus ${r} for each additional hour. Which function gives the total cost C, in dollars, for h hours of work, where h ≥ {k}?',
        f'Desmos check: type each choice and test h = {k} (cost should be {a}) and h = {k + 1} (cost should be {a + r}).',
        [f'The first {unit} cost ${a} in total', f'Additional hours = h − {k}', f'C(h) = {a} + {r}(h − {k})'],
        f'Only the hours AFTER the first {k} cost ${r} each. Using {r}h double-charges the first {unit}.', f'C(h) = {a} + {r}(h − {k})',
        [f'C(h) = {a} + {r}h', f'C(h) = {r}(h − {k})', f'C(h) = {a} + {r}(h + {k})'], ['the cost of the first hours', 'a function for the total cost', 'the hourly rate'], 1)
@gen('linf')
def _():
    a, b = R.choice([(9, 5), (5, 9), (3, 2), (5, 2), (7, 4), (4, 3)]); n = b * ri(2, 20); c = ri(-40, 40)
    return mk('M', f'The function f is defined by f(x) = ({a}/{b})x{sg(c)}. If the value of x increases by {n}, by how much does the value of f(x) increase?',
        f'Desmos: type f(x) = ({a}/{b})x{sg(c)}, then f({n}) − f(0).', [f'The slope is {a}/{b}: each 1 more x adds {a}/{b}', f'{n} more x adds ({a}/{b})({n})', f'= {N(Fr(a * n, b))}'],
        f'The {P(c)} does not change when x changes. Only the slope matters for an increase.', N(Fr(a * n, b)), [], ['f(x) at x = ' + str(n), 'the CHANGE in f(x)', 'the y-intercept'], 1, grid=True)
@gen('linf')
def _():
    a, c = ri(2, 9), ri(-6, 6)
    if a == c: return None
    xi = ri(-6, 8); b, d = ri(-12, 12), None; d = b + (a - c) * xi
    return mk('H', f'The functions f and g are defined as f(x) = {a}x{sg(b) if b else ""} and g(x) = {cx(c) if c else "0x"}{sg(d) if d else ""}. If the function h is defined as h(x) = f(x) − g(x), what is the x-coordinate of the x-intercept of the graph of y = h(x) in the xy-plane?'.replace('0x', '0'),
        'Desmos: type f(x), g(x), then h(x) = f(x) − g(x) and click where it crosses the x-axis.',
        [f'h(x) = ({a}x{sg(b) if b else ""}) − ({cx(c) if c else "0"}{sg(d) if d else ""}) = {P(a - c)}x{sg(b - d) if b - d else ""}', 'x-intercept: set h(x) = 0', f'x = {P(xi)}'],
        'Subtract EVERY term of g, including its constant.', P(xi), [], ['h(0)', 'the x where h(x) = 0', 'the slope of h'], 1, grid=True)

# ---------------- systems ----------------
@gen('sys')
def _():
    A, B, C = ri(2, 8), ri(2, 9), ri(2, 30); k = ri(2, 4)
    return mk('H', f'{A}x + {B}y = {C}<br>ax + {k * B}y = {k * C}<br>In the given system of equations, a is a constant. If the system has infinitely many solutions, what is the value of a?',
        'Desmos: slider for a; infinitely many solutions = the two lines lie exactly on top of each other.',
        [f'The second equation must be the first one multiplied by the same number', f'{k * B} ÷ {B} = {k} and {k * C} ÷ {C} = {k}', f'So a = {k} × {A} = {k * A}'],
        'Infinitely many = SAME line (every number matches). No solution = parallel (only the x and y parts match).', k * A, [], ['x', 'a, so the lines are the same', 'the number of solutions'], 1, grid=True)
@gen('sys')
def _():
    p1, p2 = R.choice([(2, 5), (3, 7), (4, 9), (1.5, 4), (2.5, 6), (3, 8)]); n1, n2 = ri(5, 30), ri(5, 30)
    item = R.choice([('pens', 'markers'), ('apples', 'mangoes'), ('stamps', 'envelopes'), ('songs', 'albums')])
    T, n = round(p1 * n1 + p2 * n2, 2), n1 + n2
    Ts = f'{T:,.2f}' if T != int(T) else f'{int(T):,}'
    return mk('M', f'A store sells {item[0]} for ${p1:g} each and {item[1]} for ${p2:g} each. A customer bought {n} items in total for ${Ts}. How many {item[1]} did the customer buy?',
        f'Desmos: x + y = {n} and {p1:g}x + {p2:g}y = {T:g}, click the crossing. Read y.',
        [f'x + y = {n} and {p1:g}x + {p2:g}y = {T:g}', f'x = {n} − y, so {p1:g}({n} − y) + {p2:g}y = {T:g}', f'{p2 - p1:g}y = {round(T - p1 * n, 2):g} → y = {n2}'],
        f'{n1} is the number of {item[0]}. Circle what they asked for.', n2, [n1, n2 + 1, n - n2 + 1 if n - n2 + 1 != n1 else n2 - 1], [f'the number of {item[0]}', 'the total cost', f'the number of {item[1]}'], 2)

# ---------------- percentages ----------------
@gen('pct')
def _():
    p, n = R.choice([10, 15, 20, 25, 30, 40, 60]), 20 * ri(2, 30); val = Fr(p * n, 100); q = R.choice([50, 80, 120, 150, 175, 200, 250])
    if val.denominator != 1 or Fr(q * n, 100).denominator != 1: return None
    return mk('M', f'If {p}% of a number is {N(val)}, what is {q}% of the number?', 'By hand: find the whole number first, then take the new percent.',
        [f'{p / 100:g} × n = {N(val)} → n = {N(val)} ÷ {p / 100:g} = {N(n)}', f'{q}% of {N(n)} = {q / 100:g} × {N(n)} = {N(Fr(q * n, 100))}'],
        f'{N(val)} is only {p}% of the number. Find the whole number first.', N(Fr(q * n, 100)), [], ['the whole number', f'{q}% of the number', f'{p}% of the number'], 1, grid=True)
@gen('pct')
def _():
    a, b = R.choice([10, 20, 25, 30, 40, 50]), R.choice([10, 20, 25, 30, 40, 50]); f = (1 + a / 100) * (1 - b / 100); net = round((f - 1) * 100, 2)
    if net == 0: return None
    w = 'increase' if net > 0 else 'decrease'
    return mk('H', f'The price of a jacket was increased by {a}%. Later, the new price was decreased by {b}%. The final price is what percent {w} from the original price?',
        f'Desmos: type 100(1 + {a / 100:g})(1 − {b / 100:g}) and compare to 100.',
        [f'Use a starting price of $100', f'After +{a}%: 100 × {1 + a / 100:g} = {100 + a:g}', f'After −{b}%: {100 + a:g} × {1 - b / 100:g} = {round(100 * f, 2):g}', f'Change from 100: {abs(net):g}% {w}'],
        f'Percents do not just add: +{a}% then −{b}% is NOT {abs(a - b)}%.', f'{abs(net):g}%', [f'{abs(a - b)}%', f'{a + b}%', f'{abs(round(a * b / 100, 2)):g}%'], ['the final price', f'the percent {w}', 'the first new price'], 1)

def main():
    per = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    B = json.load(open(BANK)); qs = B['qs']; seen = {re.sub(r'\s+', ' ', q['q']) for q in qs}; added = 0
    for sk, fns in H.items():
        nums = [int(q['id'].split('-')[1]) for q in qs if q['skill'] == sk]; nxt = max(nums) + 1
        for fn in fns:
            got, tries = 0, 0
            while got < per and tries < 4000:
                tries += 1; d = fn()
                if not d: continue
                key = re.sub(r'\s+', ' ', d['q'])
                if key in seen: continue
                seen.add(key); qs.append({'id': f'{sk}-{nxt:02d}', 'skill': sk, **d}); nxt += 1; got += 1; added += 1
            if got < per: print('short', sk, fn.__name__, got)
    for s in B['skills']: s['n'] = sum(1 for q in qs if q['skill'] == s['id'])
    json.dump(B, open(BANK, 'w'), ensure_ascii=False, indent=0); print('added', added, 'total', len(qs))
if __name__ == '__main__': main()
