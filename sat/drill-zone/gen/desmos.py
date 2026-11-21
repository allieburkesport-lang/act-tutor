#!/usr/bin/env python3
"""Fill in Desmos keystrokes for every math question that has none in qhelp.json.
qhelp[id] = {d: [lines to type], c: [TI-84 keys], n: note}. Only empty 'd' lists are filled."""
import json, re, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, '..', 'bank.json')))
HP = os.path.join(HERE, '..', '..', 'prep', 'qhelp.json')
H = json.load(open(HP))
MATH = {s['id'] for s in B['skills'] if s['sec'] == 'Math'}
def plain(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<br\s*/?>', ' ', re.sub(r'<(?!br)[^>]+>', ' ', h)))).strip()
def cells(h): return [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', h)]
def num(s): return s.replace('−', '-').replace(',', '')
def dz(s): return s.replace('−', '-')

def build(q):
    p, s, sk = plain(q['q']), q['steps'], q['skill']
    m = re.search(r'circumference of a circle is (\d+)π', p)
    if m: return [f'Type {m[1]}π/π'], f'C = πd, so the diameter is C ÷ π = {m[1]}. Desmos just confirms it.'
    if sk == 'data1' and 'pets' in p:
        c = cells(q['q']); vals = c[1:6]; fr = c[7:12]; L = []
        for v, f in zip(vals, fr): L += [v] * int(f)
        return [f'Type L = [{",".join(L)}]', 'Type median(L)'], 'Each pet number is typed once for every student who has it (the frequency). Desmos gives the median.'
    if 'online group' in p:
        c = cells(q['q']); xs, ys = c[1:5], [num(v) for v in c[6:10]]
        return ['Click + › table. Put the weeks in x₁: ' + ', '.join(xs), 'Put the numbers in y₁: ' + ', '.join(ys), 'Type y₁ ~ m x₁ + b', 'Type y₁ ~ a·b^(x₁)'], \
            'Look at R² under each line. The model with R² = 1 (or the closest to 1) fits the data.'
    if 'linear function f' in p and 'table' in q['q']:
        c = cells(q['q']); xs = c[2::2][:4]; ys = [num(v) for v in c[3::2][:4]]
        return ['Click + › table. x₁: ' + ', '.join(xs), 'y₁: ' + ', '.join(ys), 'Type y₁ ~ m x₁ + b'], 'Desmos shows m (slope) and b (start). Plug them into f(x) = mx + b and match the choice.'
    m = re.search(r'factor of (x².*?)\?', p)
    if m: return [f'Type y = {dz(m[1])}'], 'Click where the graph crosses the x-axis. A crossing at x = p means the factor is (x − p): flip the sign.'
    m = re.match(r'(\(ax.*?\)\(.*?\)) = (.*?) In the equation above', p)
    if m: return [f'Type y = {dz(m[1])}', f'Type y = {dz(m[2])}', 'Click "add slider" for a'], 'Slide a until the two graphs lie exactly on top of each other. That value of a is the answer.'
    m = re.search(r'costs \$(\d+) per month plus \$(\d+) for each gigabyte.*?\$(\d+)', p)
    if m: return [f'Type {m[1]} + {m[2]}x ≤ {m[3]}', f'Type ({m[3]} - {m[1]})/{m[2]}'], 'The shading stops at that decimal. Round DOWN to the last whole number inside the shading.'
    m = re.search(r'Sam .* (\d+) minutes\. Sam.s trip took more than (\d+)', p)
    if m: return [f'Type w + {m[1]} > {m[2]}', f'Type w - {m[1]} > {m[2]}'], f'Check with a real number: if w = {int(m[2]) - int(m[1]) + 1}, the trip is {int(m[2]) + 1} minutes, which IS more than {m[2]}. Only the "+" version is true for it. Parts of a trip add.'
    m = re.search(r'inequality (y > .*?)\?', p)
    if m:
        return [f'Type {dz(m[1])}'] + [f'Type {dz(c)}' for c in q['ch']], 'The right answer is the point inside the shaded area. A point ON the dashed line does not count.'
    m = re.search(r'charges .* \$(\d+) plus \$(\d+) per hour.*\$(\d+)', p)
    if m: return [f'Type y = {m[1]} + {m[2]}x', f'Type y = {m[3]}'], 'Click where the two lines cross. The x-value is the number of hours.'
    m = re.search(r'theater sold ([\d,]+) tickets for \$([\d,]+)\. Adult tickets cost \$(\d+) and child tickets cost \$(\d+)', p)
    if m: return [f'Type x + y = {num(m[1])}', f'Type {m[3]}x + {m[4]}y = {num(m[2])}'], 'Click the crossing point. x = adult tickets, y = child tickets. Read the one the question asks for.'
    m = re.search(r'shipment of (\d+) books .* hold (\d+) books each .* hold (\d+) books each', p)
    if m: return [f'Type {m[2]}x + {m[3]}y = {m[1]}', f'Type x = 2', 'Click the crossing to see y'], f'Check: 2 small boxes ({2 * int(m[2])} books) plus that many large boxes should give {m[1]} books. If you swapped the numbers, it will not work out.'
    m = re.search(r'The formula (.+?) is used in science class.*shows (\w) in terms', p)
    if m:
        return ['Pick easy numbers for every letter except ' + m[2] + ' (for example 2, 3, 5)', 'Type the original formula with those numbers and solve for ' + m[2],
                'Type each answer choice with the same numbers'], 'The right choice gives the same value of ' + m[2] + ' as the original formula.'
    if sk == 'prob' or sk == 'infer' and re.search(r'random sample of (\d+) students', p):
        last = s[-1]; mm = re.search(r'(\d[\d,]*/\d[\d,]*|\d[\d.,]* × [\d,]+)', last)
        if mm: return [f'Type {num(mm[1]).replace("×", "*")}'], 'Compare the decimal Desmos gives with the decimal of each answer choice.'
    m = re.search(r'moves at (\d+) feet per second.*?(\d+) minutes?', p)
    if m: return [f'Type {m[1]} * 60 * {m[2]}'], 'Seconds in a minute = 60.'
    if 'angle Y is the right angle' in p:
        f = re.search(r'What is (sin|cos|tan)\(W\)', p)[1]; r = re.search(r'= (\d+/\d+)', s[1])[1]
        return [f'Type {r}'] + [f'Type {c}' for c in q['ch']], f'{f.upper()} = {s[0].split("= ")[1]}. Match the decimal of {r} to a choice.'
    if '30°−60°−90°' in p:
        x = re.search(r'x = (\d+)', s[0])[1]; return [f'Type 2*{x}'], 'In a 30-60-90 triangle the hypotenuse is 2 × the short leg (the side across from 30°).'
    if 'isosceles right triangle' in p:
        x = re.search(r'x = (\d+)', s[0])[1]; return [f'Type {x}√2'] + [f'Type {dz(c)}' for c in q['ch']], 'In a 45-45-90 triangle the hypotenuse is leg × √2. Match the decimal.'
    m = re.search(r'sin\((\d+)°\) = (\d+)/(\d+)\. What is cos\((\d+)°\)', p)
    if m: return ['Click the wrench › switch to Degrees', f'Type sin({m[1]})', f'Type cos({m[4]})'], f'Both lines show the SAME decimal. That proves sin({m[1]}°) = cos({m[4]}°), because {m[1]}° + {m[4]}° = 90°. The decimal will not be {m[2]}/{m[3]} (the test makes up the triangle), so do not match it to a choice. Just use the rule: cos({m[4]}°) = sin({m[1]}°) = {m[2]}/{m[3]}.'
    m = re.search(r'measures (\d*)π/(\d+) radians', p)
    if m: return [f'Type {m[1] or 1}*180/{m[2]}'], 'Replace π with 180°. Desmos gives the degrees.'
    m = re.search(r'One angle measures (\d+)°\. What is the measure of its same-side interior', p) or re.search(r'measures (\d+)°\. What is the measure of the angle next to it', p)
    if m: return [f'Type 180 - {m[1]}'], 'These two angles add to 180°.'
    if sk == 'lat' and ('directly across' in p or 'corresponding' in p):
        a = re.search(r'measures (\d+)°', p)[1]; return [f'No typing needed: the answer is the same angle, {a}°'], 'Vertical (across) angles and corresponding angles are EQUAL. Desmos is not needed, but you can check: 180 − ' + a + ' is the OTHER angle size, which is the trap.'
    if sk == 'infer' or sk == 'claims':
        return [], ''
    return None

added, left = 0, []
for q in B['qs']:
    if q['skill'] not in MATH: continue
    h = H.setdefault(q['id'], {'d': [], 'c': [], 'n': ''})
    if h.get('d'): continue
    r = build(q)
    if r is None: left.append(q['id']); continue
    d, n = r
    if d: h['d'] = d; h['n'] = n; added += 1
json.dump(H, open(HP, 'w'), ensure_ascii=False)
print('filled', added, 'still empty (rule questions)', len([1 for q in B['qs'] if q['skill'] in MATH and not H[q['id']].get('d')]), 'unhandled', left[:20])
