#!/usr/bin/env python3
"""Per-question formula / rule cards for the math drill questions.
Writes act-tutor/sat/prep/qform.json: {qid: [card,...]}
card = {n: name, eq: formula or rule, ref: 'ref' (on SAT reference sheet) | 'learn' (memorize) | 'rule',
        l: [[letter, meaning, value-in-this-question], ...]}
Every math question must match exactly one template below (the script fails otherwise)."""
import json, re, html, sys
B = json.load(open('/home/claude/act-tutor/sat/drill-zone/bank.json'))
MATH = {s['id'] for s in B['skills'] if s['sec'] == 'Math'}
def plain(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()
def nums(t): return re.findall(r'−?-?\d[\d,]*(?:\.\d+)?', t)
def F(n, eq, ref, l=()): return dict(n=n, eq=eq, ref=ref, l=[[a, b, ('unknown' if c == a or c == 'x' else c)] for a, b, c in l])
def R(n, eq): return F(n, eq, 'rule')

T = []   # (skill, regex, builder)
def t(skill, rx):
    def d(fn): T.append((skill, re.compile(rx, re.S), fn)); return fn
    return d

# ---------- lin1 ----------
@t('lin1', r'^If (\d+)x \+ (\d+) = (\d+), what is the value of x\?')
def _(m, q, s): return [R('Solve for x', 'Undo + or − first, then undo × or ÷. Do the same thing to both sides.'),
    F('The equation', 'ax + b = c', 'rule', [('x', 'the unknown number', 'what we find'), ('a', 'number in front of x', m[1]), ('b', 'number added', m[2]), ('c', 'the total', m[3])])]
@t('lin1', r'^(\d+)\(x − (\d+)\) = ')
def _(m, q, s): return [R('Distribute', 'a(x − b) = ax − ab: multiply the outside number by EACH term inside.'),
    R('Solve for x', 'Get the x terms on one side, the plain numbers on the other, then divide.')]
@t('lin1', r'charges .* \$(\d+) plus \$(\d+) per hour.*\$(\d+)')
def _(m, q, s): return [F('Total cost', 'total = fixed fee + rate × hours', 'learn', [('fixed fee', 'paid once', '$' + m[1]), ('rate', 'cost per hour', '$' + m[2]), ('h', 'hours worked', 'what we find'), ('total', 'the bill', '$' + m[3])])]
@t('lin1', r'^If (\d+)x \+ (\d+) = (\d+), what is the value of (\d+)x \+ (\d+)\?')
def _(m, q, s): return [R('Spot the multiple', f'{m[4]}x + {m[5]} is a multiple of {m[1]}x + {m[2]}. Multiply the whole equation instead of solving for x.')]
@t('lin1', r'k\(x \+ (\d+)\) = (\d+)x \+ (\d+).*no solution')
def _(m, q, s): return [R('No solution', 'A linear equation has NO solution when the x-terms match but the plain numbers do not.'),
    R('Distribute', 'k(x + b) = kx + kb')]
# ---------- lin2 ----------
@t('lin2', r'The equation (\d+)x \+ (\d+)y = (\d+) represents the total cost')
def _(m, q, s): return [F('Total cost equation', 'ax + by = total', 'rule', [('x', 'how many of the first item', 'what we find'), ('y', 'how many of the second item', re.search(r'y = (\d+)', s[0])[1]), ('a, b', 'price of each item', f'{m[1]}, {m[2]}'), ('total', 'total cost', m[3])])]
@t('lin2', r'shipment of (\d+) books .* hold (\d+) books each .* hold (\d+) books each')
def _(m, q, s): return [F('Total from two groups', '(per small box)·x + (per large box)·y = total', 'rule', [('x', 'number of small boxes', 'x'), ('y', 'number of large boxes', 'y'), ('per box', 'books in each box', f'{m[2]} and {m[3]}'), ('total', 'all the books', m[1])])]
@t('lin2', r'The formula (.+?) is used in science class')
def _(m, q, s): return [R('Rearrange a formula', 'Get the target letter alone: undo + and − first, then × and ÷, doing the same thing to both sides.')]
@t('lin2', r'The equation y = (\d+) − (\d+)x gives')
def _(m, q, s): return [F('Linear model', 'y = b + mx', 'learn', [('b', 'the starting amount (when x = 0)', m[1]), ('m', 'change for each 1 of x (here it goes down)', '−' + m[2]), ('x', 'the input', 'x')])]
# ---------- linf ----------
@t('linf', r'f\(x\) = (−?\d+)x \+ (\d+)\. What is the value of f\((−?\d+)\)')
def _(m, q, s): return [F('Evaluate a function', 'f(x) = mx + b → replace every x with the number', 'rule', [('x', 'the input', m[3]), ('m', 'number in front of x', m[1]), ('b', 'number added', m[2])])]
@t('linf', r'passes through the points \((−?\d+), (−?\d+)\) and \((−?\d+), (−?\d+)\)')
def _(m, q, s): return [F('Slope from two points', 'm = (y₂ − y₁) ÷ (x₂ − x₁)', 'learn', [('m', 'slope = rise ÷ run', 'what we find'), ('(x₁, y₁)', 'first point', f'({m[1]}, {m[2]})'), ('(x₂, y₂)', 'second point', f'({m[3]}, {m[4]})')])]
@t('linf', r'The table shows values of the linear function f')
def _(m, q, s): return [F('Slope-intercept form', 'f(x) = mx + b', 'learn', [('b', 'f(x) when x = 0 (the start)', re.search(r'So b = (−?\d+)', s[0])[1]), ('m', 'how much f(x) changes each time x goes up 1', re.search(r'So m = (−?\d+)', s[1])[1])])]
@t('linf', r'For the linear function f, f\((−?\d+)\) = (−?\d+) and f\((−?\d+)\) = (−?\d+)')
def _(m, q, s): return [F('Slope from two points', 'm = (y₂ − y₁) ÷ (x₂ − x₁)', 'learn', [('(x₁, y₁)', 'first point', f'({m[1]}, {m[2]})'), ('(x₂, y₂)', 'second point', f'({m[3]}, {m[4]})')]),
    F('Slope-intercept form', 'f(x) = mx + b', 'learn', [('m', 'slope', 'from step 1'), ('b', 'f(0), the start', 'from step 2')])]
@t('linf', r'Line p is defined by (\d+)x \+ (\d+)y = (\d+)\. Line q is perpendicular')
def _(m, q, s): return [F('Slope of Ax + By = C', 'm = −A ÷ B', 'learn', [('A', 'number in front of x', m[1]), ('B', 'number in front of y', m[2])]),
    R('Perpendicular slopes', 'Flip the fraction and change the sign (negative reciprocal).')]
# ---------- sys ----------
@t('sys', r'^y = (−?\d+)x [+−] \d+ x \+ y = ')
def _(m, q, s): return [R('Substitution', 'The first equation says what y equals. Put that whole expression in for y in the second equation.')]
@t('sys', r'theater sold ([\d,]+) tickets for \$([\d,]+)\. Adult tickets cost \$(\d+) and child tickets cost \$(\d+)')
def _(m, q, s): return [F('Count equation', 'a + c = total tickets', 'rule', [('a', 'adult tickets', 'a'), ('c', 'child tickets', 'c'), ('total', 'tickets sold', m[1])]),
    F('Money equation', '(adult price)a + (child price)c = total money', 'rule', [('prices', 'adult, child', f'${m[3]}, ${m[4]}'), ('total money', 'all ticket sales', '$' + m[2])])]
@t('sys', r'^\d+x \+ \d+y = \d+ (\d+)?x − \d+y = −?\d+ If')
def _(m, q, s):
    c = re.search(r'\+ (\d+)y', q)[1]
    return [R('Elimination', f'Add the two equations: +{c}y and −{c}y cancel, leaving only x.')]
@t('sys', r'^ax \+ (\d+)y = (\d+) (\d+)x \+ (\d+)y = (\d+) In the system above')
def _(m, q, s): return [F('Slope of Ax + By = C', 'm = −A ÷ B', 'learn', [('A', 'number in front of x', f'a and {m[3]}'), ('B', 'number in front of y', f'{m[1]} and {m[4]}')]),
    R('No solution', 'Parallel lines (same slope, different line) never cross, so the system has no solution.')]
@t('sys', r'^\d+x \+ y = \d+ x − y = −?\d+ What is the value of y')
def _(m, q, s): return [R('Elimination', 'Add the two equations: +y and −y cancel, leaving only x.')]
# ---------- ineq ----------
@t('ineq', r'Which inequality is equivalent to (\d+)x − (\d+) > (−?\d+)\?')
def _(m, q, s): return [R('Solve an inequality', 'Solve it like an equation. Dividing by a POSITIVE number keeps the sign.')]
@t('ineq', r'Which values of x satisfy −(\d+)x \+ (\d+) ≤ (\d+)\?')
def _(m, q, s): return [R('Flip rule', 'When you multiply or divide by a NEGATIVE number, flip the inequality sign.')]
@t('ineq', r'phone plan costs \$(\d+) per month plus \$(\d+) for each gigabyte .*?\$(\d+)')
def _(m, q, s): return [F('Cost inequality', 'fixed cost + rate × g ≤ budget', 'rule', [('fixed cost', 'monthly charge', '$' + m[1]), ('rate', 'cost per GB', '$' + m[2]), ('g', 'GB of data', 'what we find'), ('budget', 'the most to spend', '$' + m[3])])]
@t('ineq', r'^Sam .* w minutes.* (\d+) minutes\. Sam.s trip took more than (\d+)')
def _(m, q, s): return [F('Total time', 'first part + second part > total', 'rule', [('w', 'first part (minutes)', 'w'), ('second part', 'minutes', m[1]), ('more than', 'means >', m[2])])]
@t('ineq', r'is a solution to the inequality y > ')
def _(m, q, s): return [R('Test a point', 'Plug the point’s x and y into the inequality. It works only if the statement is true. On the line does not count for >.')]
# ---------- equiv ----------
@t('equiv', r'^Which expression is equivalent to \(x [+−] \d+\)\(x [+−] \d+\)\?')
def _(m, q, s): return [R('FOIL', '(x + a)(x + b) = x² + (a + b)x + ab: First, Outer + Inner, Last.')]
@t('equiv', r'^Which expression is a factor of x²')
def _(m, q, s): return [R('Factor x² + bx + c', 'Find two numbers that multiply to c and add to b. They go in (x + _)(x + _).')]
@t('equiv', r'^Which expression is equivalent to x² − (\d+)\?')
def _(m, q, s): return [F('Difference of squares', 'a² − b² = (a − b)(a + b)', 'learn', [('a', 'square root of the first term', 'x'), ('b', 'square root of the second number', re.search(r'b = (\d+)', ' '.join(s))[1])])]
@t('equiv', r'^Which expression is equivalent to \(x')
def _(m, q, s): return [R('Power of a power', '(xᵃ)ᵇ = xᵃᵇ: multiply the exponents.'), R('Same base, multiply', 'xᵃ · xᵇ = xᵃ⁺ᵇ: add the exponents.')]
@t('equiv', r'^\(ax [+−] \d+\)\((\d+)x [+−] \d+\) = ')
def _(m, q, s): return [R('Match coefficients', 'Two equal polynomials have the same number in front of x², of x, and alone.'), R('FOIL', 'First terms multiply to the x² term.')]
@t('equiv', r'is equivalent to the (fourth|cube|fifth) root of x')
def _(m, q, s): return [F('Root as a power', 'ⁿ√(xᵐ) = x^(m/n)', 'learn', [('n', 'which root', {'fourth': '4', 'cube': '3', 'fifth': '5'}[m[1]]), ('m', 'the power inside', 'the exponent on x')])]
# ---------- nleq ----------
@t('nleq', r'positive solution to x² \+ (\d+) = (\d+)\?')
def _(m, q, s): return [R('Undo a square', 'Get x² alone, then take the square root of both sides: x = ± √(number).')]
@t('nleq', r'(sum of the solutions|solution to x² [−+] (?:\d*)x [+−] \d+ = 0|product of the solutions)')
def _(m, q, s): return [R('Factor x² + bx + c = 0', 'Find two numbers that multiply to c and add to b. Set each factor = 0.')]
@t('nleq', r'^y = \(x \+ (\d+)\)² − (\d+) y = (−?\d+) How many solutions')
def _(m, q, s): return [F('Vertex form', 'y = (x − h)² + k', 'learn', [('k', 'lowest point of the parabola (the vertex y)', '−' + m[2]), ('line', 'the flat line', 'y = ' + m[3])]),
    R('Count crossings', 'Line above the vertex: 2. At the vertex: 1. Below: 0.')]
@t('nleq', r'x² \+ bx \+ (\d+) = 0 In the equation above, b is a constant')
def _(m, q, s): return [F('Discriminant', 'b² − 4ac', 'learn', [('a', 'number in front of x²', '1'), ('b', 'number in front of x', 'b'), ('c', 'plain number', m[1]), ('< 0', 'no real solutions', ''), ('= 0', 'one solution', '')])]
@t('nleq', r'^y = x² y = (\d+)?x \+ (\d+) If')
def _(m, q, s): return [R('Set equal', 'Both equations equal y, so set x² = the other side. Move everything to one side and factor.')]
# ---------- nlf ----------
@t('nlf', r'^f\(x\) = (\d+)x² − (\d+)\. What is the value of f\((−?\d+)\)')
def _(m, q, s): return [R('Order of operations', 'Square first, then multiply, then subtract. (−a)² is positive.'), F('The function', f'f(x) = {m[1]}x² − {m[2]}', 'rule', [('x', 'the input', m[3])])]
@t('nlf', r'population was ([\d,]+) in \d+\. It (de|in)creases by (\d+)% each year')
def _(m, q, s): return [F('Exponential growth/decay', 'P(t) = start × (1 ± r)ᵗ', 'learn', [('start', 'amount at t = 0', m[1]), ('r', 'percent as a decimal', str(int(m[3]) / 100)), ('±', '+ for increase, − for decrease', '−' if m[2] == 'de' else '+'), ('t', 'years', 't')])]
@t('nlf', r'^f\(x\) = (−?\d*)\(x − (\d+)\)² ([+−]) (\d+)\. What is the (max|min)imum')
def _(m, q, s): return [F('Vertex form', 'f(x) = a(x − h)² + k', 'learn', [('(h, k)', 'the vertex', f"({m[2]}, {'−' if m[3]=='−' else ''}{m[4]})"), ('k', 'the max or min VALUE', ('−' if m[3] == '−' else '') + m[4]), ('a', 'positive: opens up (min). negative: opens down (max)', {'': '1', '−': '−1'}.get(m[1], m[1]))])]
@t('nlf', r'The value, in dollars, of an investment')
def _(m, q, s): return [R('Evaluate an exponential', 'Do the power first, then multiply by the starting value.')]
@t('nlf', r'^Which equivalent form of f\(x\) = .* displays the y-intercept')
def _(m, q, s): return [F('Standard form', 'f(x) = ax² + bx + c', 'learn', [('c', 'the y-intercept (value when x = 0)', 'visible after expanding')])]
@t('nlf', r'^Which equivalent form of f\(x\) = .* displays the x-intercepts')
def _(m, q, s): return [F('Factored form', 'f(x) = a(x − r)(x − s)', 'learn', [('r, s', 'the x-intercepts (zeros)', 'from factoring')])]
# ---------- ratio ----------
@t('ratio', r'car travels (\d+) miles in (\d+) hours.*?(\d+) hours')
def _(m, q, s): return [F('Distance, rate, time', 'distance = rate × time', 'learn', [('rate', 'miles per hour = miles ÷ hours', f'{m[1]} ÷ {m[2]}'), ('time', 'hours asked about', m[3])])]
@t('ratio', r'moves at (\d+) feet per second.*?(\d+) minutes?')
def _(m, q, s): return [F('Unit conversion', '1 minute = 60 seconds', 'learn'), F('Distance', 'distance = rate × time', 'learn', [('rate', 'feet per second', m[1]), ('time', 'seconds', f'{m[2]} × 60')])]
@t('ratio', r'recipe uses (\d+) cups of flour to make (\d+) muffins.*?(\d+) muffins')
def _(m, q, s): return [F('Proportion', 'a/b = x/d → cross multiply', 'learn', [('a/b', 'cups per muffins (known)', f'{m[1]}/{m[2]}'), ('x', 'cups we need', 'x'), ('d', 'muffins asked about', m[3])])]
@t('ratio', r'ratio of boys to girls in a club is (\d+) to (\d+)\. The club has (\d+) members')
def _(m, q, s): return [R('Ratio parts', 'Add the parts, divide the total by the parts to get one part, then multiply.'), F('One part', 'total ÷ (sum of parts)', 'rule', [('parts', 'boys + girls', f'{m[1]} + {m[2]}'), ('total', 'members', m[3])])]
@t('ratio', r'density of ([\d.]+) grams per cubic centimeter.*?(\d+) cubic centimeter')
def _(m, q, s): return [F('Density', 'mass = density × volume', 'learn', [('density', 'grams per cm³', m[1]), ('volume', 'cm³', m[2])]), F('Unit conversion', '1 kg = 1,000 g', 'learn')]
# ---------- pct ----------
@t('pct', r'^What is (\d+)% of ([\d,]+)\?')
def _(m, q, s): return [F('Percent of', 'p% of N = (p ÷ 100) × N', 'learn', [('p', 'the percent', m[1]), ('N', 'the whole', m[2])])]
@t('pct', r'changed from \$(\d+) to \$(\d+)\. What is the percent (in|de)crease')
def _(m, q, s): return [F('Percent change', '% change = (new − old) ÷ old × 100', 'learn', [('old', 'starting price', '$' + m[1]), ('new', 'ending price', '$' + m[2])])]
@t('pct', r'costs \$(\d+)\. It is marked down (\d+)%, and then the sale price is marked down (?:another )?(\d+)%')
def _(m, q, s): return [F('Percent off', 'new = old × (1 − p ÷ 100)', 'learn', [('old', 'price before each markdown', '$' + m[1]), ('p', 'each markdown', f'{m[2]}%, then {m[3]}%')]), R('Two discounts', 'Apply them one after the other. Never add the percents.')]
@t('pct', r'After a (\d+)% discount, a pair of shoes costs \$(\d+)')
def _(m, q, s): return [F('Percent off', 'sale = original × (1 − p ÷ 100)', 'learn', [('p', 'the discount', m[1] + '%'), ('sale', 'price after discount', '$' + m[2]), ('original', 'what we find', 'x')])]
@t('pct', r'school has ([\d,]+) students\. (\d+)% of them play a sport, and (\d+)%')
def _(m, q, s): return [F('Percent of', 'p% of N = (p ÷ 100) × N', 'learn', [('N first', 'all students', m[1]), ('p first', 'play a sport', m[2] + '%'), ('p second', 'of THOSE players', m[3] + '%')])]
# ---------- data1 ----------
@t('data1', r'^What is the mean of the data set')
def _(m, q, s): return [F('Mean (average)', 'mean = sum ÷ how many numbers', 'learn')]
@t('data1', r'^What is the median of the data set')
def _(m, q, s): return [R('Median', 'Put the numbers in order. The middle one is the median. With an even count, average the two middle numbers.')]
@t('data1', r'first four test scores are .*?mean score to be (\d+)')
def _(m, q, s): return [F('Mean (average)', 'mean = sum ÷ how many numbers → sum = mean × how many', 'learn', [('mean', 'the average she wants', m[1]), ('how many', 'tests', '5')])]
@t('data1', r'If the value (\d+) is removed')
def _(m, q, s): return [R('Outliers', 'Removing a far-out value changes the MEAN a lot and the MEDIAN only a little.')]
@t('data1', r'how many pets each student')
def _(m, q, s): return [R('Median from a table', 'Add the frequencies, find the middle position, then count across until you reach it.')]
# ---------- data2 ----------
@t('data2', r'line of best fit for a scatterplot is y = ([\d.]+)x \+ (\d+).*?(\d+) hours')
def _(m, q, s): return [F('Line of best fit', 'y = mx + b', 'learn', [('m', 'slope', m[1]), ('b', 'start', m[2]), ('x', 'the input', re.search(r'x = ([\d.]+)', s[0])[1])])]
@t('data2', r'^A line of best fit is y = ([\d.]+)x \+ (\d+)')
def _(m, q, s): return [F('Slope means', 'm = the predicted change in y for each 1 more x', 'learn', [('m', 'slope', m[1])])]
@t('data2', r'line of best fit for a data set is y = (\d+)x \+ (\d+)\. One data point is \((\d+), (\d+)\)')
def _(m, q, s): return [F('Residual', 'residual = actual − predicted', 'learn', [('actual', 'the real y of the point', m[4]), ('predicted', 'the line’s y at x = ' + m[3], f'{m[1]}({m[3]}) + {m[2]}')])]
@t('data2', r'online group')
def _(m, q, s): return [R('Linear or exponential', 'Same DIFFERENCE each step = linear. Same RATIO (multiply by the same number) = exponential.')]
# ---------- prob ----------
@t('prob', r'bag has (\d+) red, (\d+) blue, and (\d+) green')
def _(m, q, s): return [F('Probability', 'P = favorable ÷ total', 'learn', [('favorable', 'blue marbles', m[2]), ('total', 'all marbles', f'{m[1]} + {m[2]} + {m[3]}')])]
@t('prob', r'The table shows students. lunch choices')
def _(m, q, s): return [F('Conditional probability', 'P = (count in the group you want) ÷ (total of the "given" group only)', 'learn'), R('Given', 'Only look at the row or column named after "who chose …".')]
@t('prob', r'box of (\d+) light bulbs, (\d+) are defective')
def _(m, q, s): return [F('Probability', 'P = favorable ÷ total', 'learn', [('favorable', 'good bulbs = total − defective', f'{m[1]} − {m[2]}'), ('total', 'all bulbs', m[1])])]
@t('prob', r'probability that a randomly chosen customer buys a drink is (\d+)/(\d+)\. Out of (\d+)')
def _(m, q, s): return [F('Expected number', 'expected = probability × number of tries', 'learn', [('probability', 'chance each customer buys', f'{m[1]}/{m[2]}'), ('number', 'customers', m[3])])]
# ---------- infer ----------
@t('infer', r'random sample of (\d+) students at a university with ([\d,]+) students')
def _(m, q, s): return [F('Estimate from a sample', 'estimate = (sample fraction) × population', 'learn', [('sample fraction', 'yes answers ÷ sample size', '÷ ' + m[1]), ('population', 'all students', m[2])])]
@t('infer', r'estimates that (\d+)% .* margin of error of (\d+)')
def _(m, q, s): return [F('Margin of error', 'plausible range = estimate − margin to estimate + margin', 'learn', [('estimate', 'survey result', m[1] + '%'), ('margin', 'margin of error', m[2] + '%')])]
@t('infer', r'^A researcher estimates the')
def _(m, q, s): return [R('Margin of error', 'A bigger random sample gives a smaller margin of error.')]
@t('infer', r'^A random sample of people from one')
def _(m, q, s): return [R('Generalize', 'Results only apply to the group the random sample came from.')]
# ---------- claims ----------
@t('claims', r'(selected|survey of|wants to know)')
def _(m, q, s): return [R('Cause vs. association', 'Random ASSIGNMENT → can say cause. Random SAMPLE → can generalize to that population. People choosing their own group → association only.')]
# ---------- area ----------
@t('area', r'rectangle has a length of (\d+) inches and a width of (\d+) inches\. What is its (perimeter|area)')
def _(m, q, s):
    if m[3] == 'area': return [F('Area of a rectangle', 'A = ℓw', 'ref', [('ℓ', 'length', m[1]), ('w', 'width', m[2])])]
    return [F('Perimeter of a rectangle', 'P = 2(ℓ + w)', 'learn', [('ℓ', 'length', m[1]), ('w', 'width', m[2])])]
@t('area', r'cylinder has a radius of (\d+) centimeters and a height of (\d+)')
def _(m, q, s): return [F('Volume of a cylinder', 'V = πr²h', 'ref', [('r', 'radius', m[1]), ('h', 'height', m[2])])]
@t('area', r'similar triangles have corresponding sides in the ratio (\d+) to (\d+)\. The (?:area of the )?smaller.*?(\d+)')
def _(m, q, s): return [F('Area scale rule', 'new area = old area × k²', 'learn', [('k', 'side scale factor', f'{m[2]} ÷ {m[1]}'), ('old area', 'smaller triangle', m[3])])]
@t('area', r'cube-shaped box has a volume of (\d+) cubic feet')
def _(m, q, s): return [F('Volume scale rule', 'new volume = old volume × k³', 'learn', [('k', 'length scale factor', re.search(r'factor: (\d+)', s[0])[1]), ('old volume', 'first box', m[1])])]
@t('area', r'sphere has a diameter of (\d+) inches')
def _(m, q, s): return [F('Volume of a sphere', 'V = (4/3)πr³', 'ref', [('r', 'radius = half the diameter', f'{m[1]} ÷ 2')])]
# ---------- lat ----------
@t('lat', r'angle A measures (\d+)° and angle B measures (\d+)°')
def _(m, q, s): return [F('Triangle angle sum', 'A + B + C = 180°', 'ref', [('A', 'angle A', m[1] + '°'), ('B', 'angle B', m[2] + '°'), ('C', 'what we find', '')])]
@t('lat', r'Two lines intersect. One of the angles formed measures (\d+)°\. What is the measure of the angle (directly across|next to it)')
def _(m, q, s):
    if m[2] == 'next to it': return [R('Angles on a straight line', 'Two angles side by side on a straight line add to 180°.'), F('Linear pair', 'angle 1 + angle 2 = 180°', 'learn', [('angle 1', 'the given angle', m[1] + '°')])]
    return [R('Vertical angles', 'Angles straight across from each other are EQUAL.')]
@t('lat', r'parallel and are cut by a transversal\. One angle measures (\d+)°\. What is the measure of its (same-side interior|corresponding)')
def _(m, q, s):
    if m[2] == 'corresponding': return [R('Corresponding angles', 'Same position at each parallel line (both top-left, for example): they are EQUAL.')]
    return [R('Same-side interior angles', 'Between the parallel lines, on the same side of the transversal: they add to 180°.'), F('Supplementary', 'angle 1 + angle 2 = 180°', 'learn', [('angle 1', 'the given angle', m[1] + '°')])]
@t('lat', r'two interior angles measure (\d+)° and (\d+)°.*exterior')
def _(m, q, s): return [F('Exterior angle', 'exterior angle = sum of the two far interior angles', 'learn', [('far angles', 'the two given angles', f'{m[1]}° and {m[2]}°')])]
@t('lat', r'Triangles PQR and STU are similar')
def _(m, q, s):
    g = re.search(r'PQ = (\d+), QR = (\d+), and ST = (\d+)', q)
    return [F('Similar triangles', 'new side = old side × scale factor', 'learn', [('scale factor', 'matching sides: ST ÷ PQ', f'{g[3]} ÷ {g[1]}'), ('old side', 'QR (matches TU)', g[2])])]
# ---------- trig ----------
@t('trig', r'right triangle has legs of length (\d+) and (\d+)\. What is the length of the hypotenuse')
def _(m, q, s): return [F('Pythagorean theorem', 'a² + b² = c²', 'ref', [('a', 'one leg (a side touching the right angle)', m[1]), ('b', 'the other leg', m[2]), ('c', 'the hypotenuse (longest side, across from the right angle)', 'what we find')])]
@t('trig', r'angle Y is the right angle')
def _(m, q, s):
    fn = re.search(r'(SIN|COS|TAN) =', ' '.join(s))[1]
    eq = {'SIN': 'sin = opposite ÷ hypotenuse', 'COS': 'cos = adjacent ÷ hypotenuse', 'TAN': 'tan = opposite ÷ adjacent'}[fn]
    g = re.search(r'opposite angle W has length (\d+), the side adjacent to angle W has length (\d+), and the hypotenuse has length (\d+)', q)
    L = {'SIN': [('opposite', 'side across from angle W', g[1]), ('hypotenuse', 'longest side, across from the right angle', g[3])],
         'COS': [('adjacent', 'side next to angle W (not the hypotenuse)', g[2]), ('hypotenuse', 'longest side, across from the right angle', g[3])],
         'TAN': [('opposite', 'side across from angle W', g[1]), ('adjacent', 'side next to angle W (not the hypotenuse)', g[2])]}[fn]
    return [F('SOH-CAH-TOA', eq, 'learn', L)]
@t('trig', r'In a 30°−60°−90° triangle')
def _(m, q, s): return [F('30-60-90 triangle', 'sides x, x√3, 2x', 'ref', [('x', 'short leg (across from 30°)', re.search(r'x = (\d+)', s[0])[1]), ('2x', 'hypotenuse', ''), ('x√3', 'long leg (across from 60°)', '')])]
@t('trig', r'isosceles right triangle')
def _(m, q, s): return [F('45-45-90 triangle', 'sides x, x, x√2', 'ref', [('x', 'each leg', re.search(r'x = (\d+)', s[0])[1]), ('x√2', 'hypotenuse', '')])]
@t('trig', r'sin\((\d+)°\) = (\d+)/(\d+)\. What is cos\((\d+)°\)')
def _(m, q, s): return [R('Complementary angles', 'If two angles add to 90°, sin of one = cos of the other.')]
@t('trig', r'radians\. What is its measure in degrees')
def _(m, q, s): return [F('Radians to degrees', 'π radians = 180°', 'ref')]
# ---------- circ ----------
@t('circ', r'circle has a radius of (\d+)\. What is its area')
def _(m, q, s): return [F('Area of a circle', 'A = πr²', 'ref', [('r', 'radius', m[1])])]
@t('circ', r'circumference of a circle is (\d+)π inches')
def _(m, q, s): return [F('Circumference', 'C = πd  (same as 2πr)', 'ref', [('C', 'circumference', m[1] + 'π'), ('d', 'diameter', 'what we find')])]
@t('circ', r'radius of (\d+)\. A central angle measures (\d+)°\. What is the (a|s)')
def _(m, q, s):
    if m[3] == 'a': return [F('Arc length', 'arc = (angle ÷ 360) × 2πr', 'learn', [('angle', 'central angle', m[2] + '°'), ('r', 'radius', m[1])])]
    return [F('Sector area', 'sector = (angle ÷ 360) × πr²', 'learn', [('angle', 'central angle', m[2] + '°'), ('r', 'radius', m[1])])]
@t('circ', r'The equation of a circle in the xy-plane')
def _(m, q, s): return [F('Circle equation', '(x − h)² + (y − k)² = r²', 'learn', [('(h, k)', 'the center', ''), ('r', 'radius', 'what we find')]), R('Complete the square', 'Take half the x-number, square it, and add it to both sides. Same for y.')]
@t('circ', r'tangent to a circle with center O at point T\. The radius OT is (\d+)\. .*TP = (\d+)')
def _(m, q, s): return [R('Tangent rule', 'A tangent line meets the radius at a right angle, so OTP is a right triangle.'),
    F('Pythagorean theorem', 'a² + b² = c²', 'ref', [('a', 'radius OT (a leg)', m[1]), ('b', 'TP (the other leg)', m[2]), ('c', 'OP (the hypotenuse)', 'what we find')])]

# ---------- harder College Board-style templates (hardgen.py) ----------
@t('nlf', r'f\(x\) = ([\d,]+)\(([\d.]+)\) x/(\d+) \. By what percent')
def _(m, q, s): return [F('Exponential growth', 'f(x) = a(b)^(x/k)', 'learn', [('a', 'starting value', m[1]), ('b', 'growth factor each time x goes up by k', m[2]), ('k', 'how much x must grow for one multiply', m[3])]), R('Factor to percent', 'growth factor b = 1 + r, so the percent increase is (b − 1) × 100.')]
@t('nlf', r'f\(x\) = \(x [+−] \d+\)\(x [+−] \d+\)\. For what value of x does f\(x\) reach its minimum')
def _(m, q, s): return [R('Symmetry of a parabola', 'The vertex is exactly halfway between the two zeros: x = (r + s) ÷ 2.'), F('Factored form', 'f(x) = (x − r)(x − s)', 'learn', [('r, s', 'the zeros', 'read from the factors (flip the signs)')])]
@t('nlf', r'first term of a sequence is (\d+)\. Each term after the first is (\d+) times')
def _(m, q, s): return [F('Geometric sequence', 'nth term = a(r)^(n − 1)', 'learn', [('a', 'first term', m[1]), ('r', 'multiplier each step', m[2]), ('n', 'which term', 'n')])]
@t('nlf', r'f\(x\) = (\d+)\(([\d.]+)\) x ([+−]) (\d+)\. What is the y-intercept')
def _(m, q, s): return [R('y-intercept', 'Set x = 0. Any number to the 0 power is 1.'), F('Exponential function', 'f(x) = a(b)^x + c', 'learn', [('a', 'number in front', m[1]), ('b', 'growth factor', m[2]), ('c', 'number added', ('−' if m[3] == '−' else '') + m[4])])]
@t('nlf', r'vertex at \((−?\d+), (−?\d+)\) and passes through the point \((−?\d+), (−?\d+)\)')
def _(m, q, s): return [F('Vertex form', 'f(x) = a(x − h)² + k', 'learn', [('(h, k)', 'the vertex', f'({m[1]}, {m[2]})'), ('a', 'the stretch (what we find)', 'what we find'), ('(x, y)', 'the other point', f'({m[3]}, {m[4]})')])]
@t('nleq', r'x² \+ bx \+ (\d+) = 0 In the given equation, b is a positive constant\. The equation has exactly one real solution')
def _(m, q, s): return [F('Discriminant', 'b² − 4ac', 'learn', [('a', 'number in front of x²', '1'), ('b', 'number in front of x', 'what we find'), ('c', 'constant', m[1])]), R('Exactly one solution', 'One real solution happens when b² − 4ac = 0.')]
@t('nleq', r'line with equation y = .* intersects the parabola y = x² .* exactly one point')
def _(m, q, s): return [R('Set equal', 'Where two graphs meet, their y-values are equal: set the two right sides equal.'), F('Discriminant', 'b² − 4ac', 'learn', [('= 0', 'exactly one intersection', '')])]
@t('nleq', r'^√\(x \+ (\d+)\) = x − (\d+)')
def _(m, q, s): return [R('Square both sides', 'Undo a square root by squaring both sides. Then solve the quadratic.'), R('Check for fake solutions', 'Plug every answer back in. A square root can never equal a negative number.')]
@t('nleq', r'^\(x − (\d+)\)\(x \+ (\d+)\) = (\d+) What is the sum')
def _(m, q, s): return [R('Move everything to one side', 'Expand, then subtract so the equation equals 0.'), F('Sum of solutions', 'sum = −b ÷ a', 'learn', [('a', 'number in front of x²', '1'), ('b', 'number in front of x', 'after expanding')])]
@t('linf', r'modeled .* as a linear function of .* was ([\d,]+) when .* was (\d+), and ([\d,]+) when .* was (\d+)\. Based on the model')
def _(m, q, s): return [F('Slope from two points', 'm = (y₂ − y₁) ÷ (x₂ − x₁)', 'learn', [('(x₁, y₁)', 'first data point', f'({m[2]}, {m[1]})'), ('(x₂, y₂)', 'second data point', f'({m[4]}, {m[3]})')]), F('Point-slope', 'y = y₁ + m(x − x₁)', 'learn')]
@t('linf', r'charges \$(\d+) for the first (?:hour|\d+ hours) of work plus \$(\d+) for each additional hour')
def _(m, q, s): return [F('Piecewise cost', 'C = (first block) + rate × (h − hours in block)', 'learn', [('first block', 'cost of the first hours', '$' + m[1]), ('rate', 'cost per extra hour', '$' + m[2]), ('h', 'total hours', 'h')])]
@t('linf', r'f\(x\) = \((\d+)/(\d+)\)x .* If x increased by (\d+), by how much did f\(x\) increase')
def _(m, q, s): return [F('Change in a linear function', 'change in f = slope × change in x', 'learn', [('slope', 'number in front of x', f'{m[1]}/{m[2]}'), ('change in x', 'how much x went up', m[3])])]
@t('linf', r'h is defined as h\(x\) = f\(x\) − g\(x\)')
def _(m, q, s): return [R('Subtract functions', 'h(x) = f(x) − g(x): subtract every term of g, then combine like terms.'), R('x-intercept', 'Set h(x) = 0 and solve for x.')]
@t('sys', r'^\d+x \+ \d+y = \d+ ax \+ \d+y = \d+ In the given system .* infinitely many solutions')
def _(m, q, s): return [R('Infinitely many solutions', 'The two equations are the SAME line: one is a multiple of the other in every term.')]
@t('sys', r'store sells .* for \$([\d.]+) each and .* for \$([\d.]+) each\. A customer bought (\d+) items in total for \$([\d,.]+)')
def _(m, q, s): return [F('Count equation', 'x + y = total items', 'rule', [('total items', '', m[3])]), F('Money equation', 'price₁·x + price₂·y = total cost', 'rule', [('prices', '', f'${m[1]} and ${m[2]}'), ('total cost', '', '$' + m[4])])]
@t('pct', r'If (\d+)% of a number is ([\d,]+), what is (\d+)% of the number')
def _(m, q, s): return [F('Percent of a number', 'part = (percent ÷ 100) × whole', 'learn', [('percent', 'the first percent', m[1] + '%'), ('part', 'that part', m[2]), ('whole', 'the number', 'find first')])]
@t('pct', r'increased by (\d+)%\. Later, the new price was decreased by (\d+)%')
def _(m, q, s): return [F('Percent change in a row', 'final = original × (1 + a) × (1 − b)', 'learn', [('a', 'increase', m[1] + '%'), ('b', 'decrease', m[2] + '%')]), R('Use 100', 'Start with $100 so the final price IS the percent.')]

out, miss, tpl = {}, [], {}
for q in B['qs']:
    if q['skill'] not in MATH: continue
    p = plain(q['q']); hit = None
    for ti, (sk, rx, fn) in enumerate(T):
        if sk != q['skill']: continue
        m = rx.search(p)
        if m: hit = fn(m, p, q['steps']); tpl[q['id']] = ti; break
    if hit is None: miss.append((q['id'], p[:120]))
    else: out[q['id']] = hit
json.dump(out, open('/home/claude/act-tutor/sat/prep/qform.json', 'w'), ensure_ascii=False, indent=0)
json.dump(tpl, open('/home/claude/act-tutor/sat/prep/qtpl.json', 'w'))
print('cards for', len(out), 'questions; unmatched', len(miss))
for x in miss: print(' MISS', *x)
if '--dump' in sys.argv:
    for q in B['qs']:
        if q['id'] in out:
            print(f"\n{q['id']} | {plain(q['q'])[:150]}\n   steps: {' || '.join(q['steps'])[:200]}")
            for c in out[q['id']]: print('   ', c['ref'], '|', c['n'], '|', c['eq'], '|', '; '.join(f'{a}={c}' for a, b, c in c['l']))
