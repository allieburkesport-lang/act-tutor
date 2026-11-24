/* ---------- HELM Precalc plan (shared by the Precalc page and the HELM homepage) ----------
   ASU MAT 170 College Precalculus, section OD26_28. On-demand course, no due dates.
   Pace chosen Nov 24, 2026:
     1 hr a day through Dec 5 (SAT day; Nov 25 and Nov 27 added Nov 24), 1 hr 30 min a day from Dec 6,
     2 hr a day over Christmas break (Dec 19 - Jan 5), 7 days a week.
     Off: Nov 26 (Thanksgiving), Dec 24-26, Dec 31 - Jan 1, and Jan 8-12 (away).
   Goal: grades on the books for USNA before Jan 31 (Unit A, Unit B, Midterm).
   Edit PACE / OFF below if the plan changes; every date on the site re-flows by itself. */
(function () {
  const START = '2026-11-24';
  const OFF = ['2026-11-26', '2026-12-24', '2026-12-25', '2026-12-26', '2026-12-31', '2027-01-01',
    '2027-01-08', '2027-01-09', '2027-01-10', '2027-01-11', '2027-01-12'];
  const OFF_WHY = { '2026-11-26': 'Thanksgiving', '2026-12-24': 'Christmas Eve', '2026-12-25': 'Christmas', '2026-12-26': 'Christmas break',
    '2026-12-31': 'New Year’s Eve', '2027-01-01': 'New Year’s Day', '2027-01-08': 'Away', '2027-01-09': 'Away', '2027-01-10': 'Away', '2027-01-11': 'Away', '2027-01-12': 'Away' };
  function minutesFor(iso) {
    if (iso < START || OFF.includes(iso)) return 0;
    if (iso <= '2026-12-05') return 60;
    if (iso >= '2026-12-19' && iso <= '2027-01-05') return 120;
    return 90;
  }

  /* Every step of the course, in order, with ASU's estimated hours (135 total).
     g = graded item: weight is its share of the course grade. */
  const UNITS = [
    { id: 'setup', name: 'Setup', full: 'Setup · unlock the course' },
    { id: 'A', name: 'Unit A', full: 'Unit A · Algebra & Equation Review' },
    { id: 'B', name: 'Unit B', full: 'Unit B · Graphs & Functions' },
    { id: 'M', name: 'Midterm', full: 'Midterm Exam · Units A + B' },
    { id: 'C', name: 'Unit C', full: 'Unit C · Polynomial, Rational, Exponential & Log' },
    { id: 'D', name: 'Unit D', full: 'Unit D · Trigonometry' },
    { id: 'F', name: 'Final', full: 'Final Exam · Units A–D' }
  ];
  const T = (id, u, h, n, d, g) => ({ id, u, h, n, d: d || '', g: g || null });
  const TASKS = [
    T('s1', 'setup', 1, 'Welcome module: intake survey, course tour, meet the Math Support Team', 'Canvas → Modules → Welcome, items 1–3.'),
    T('s2', 'setup', 1.5, 'Syllabus review → Syllabus Quiz to 100%', 'Nothing in the course unlocks until this quiz is at 100%. Unlimited retries.'),
    T('s3', 'setup', 1, 'Get Organized + ALEKS intro. Make a brand-new ALEKS account', 'Welcome items 5–7. The syllabus says make a new ALEKS account even if you think you have one.'),
    T('s4', 'setup', 1.5, 'ALEKS Initial Knowledge Check', 'Do it alone, no guessing, no help. Every topic it says you know is removed from the course, so a lucky guess means a topic you never study.'),
    T('a1', 'A', 1, 'Read the Unit A Student Guide; look over your ALEKS pie', ''),
    T('a2', 'A', 2, 'Exponents, including rational exponents', ''),
    T('a3', 'A', 2.5, 'Simplify: exponents, square roots, monomials, polynomials', ''),
    T('a4', 'A', 2.5, 'Factor: polynomials and quadratics', ''),
    T('a5', 'A', 2, 'Solve for a variable, including in terms of other variables', ''),
    T('a6', 'A', 2, 'Solve & graph: absolute value, linear, quadratic, radical, rational', 'At 70% of Unit A topics learned, the Unit A Quiz unlocks.'),
    T('aq', 'A', 2, 'UNIT A QUIZ: retake until 100%', '16 questions, 120 min, unlimited attempts. On a retake you only redo the ones you missed. Worth 10% of the grade.', { w: 10, key: 'qa' }),
    T('ah', 'A', 0.5, 'Honorlock Practice Quiz (unlocks both exams)', 'Test the webcam, mic and Chrome extension now, not the night before the Midterm.'),
    T('b1', 'B', 0.5, 'Read the Unit B Student Guide', ''),
    T('b2', 'B', 2.5, 'Relations vs functions, vertical line test, domain & range', ''),
    T('b3', 'B', 3, 'Evaluate & graph: absolute value and quadratic functions', ''),
    T('b4', 'B', 3, 'Evaluate & graph: polynomial and piecewise functions', ''),
    T('b5', 'B', 3, 'Evaluate & graph: rational functions', ''),
    T('b6', 'B', 3, 'Linear functions: identify, build, graph, real-world models', ''),
    T('b7', 'B', 3, 'Translating & transforming functions', ''),
    T('b8', 'B', 2, 'Difference quotient: linear, quadratic, rational', ''),
    T('b9', 'B', 1.5, 'Composite functions + real-world use', ''),
    T('b10', 'B', 1.5, 'Inverse functions: graphs and algebra', ''),
    T('bq', 'B', 2, 'UNIT B QUIZ: retake until 100%', '16 questions, 120 min, unlimited attempts. Worth 10% of the grade.', { w: 10, key: 'qb' }),
    T('m1', 'M', 2, 'Midterm Student Guide + work the Midterm Study Guide', ''),
    T('m2', 'M', 2, 'Midterm Practice Quiz v1: review every miss in ALEKS', 'Practice quizzes have the same number of questions as the real exam (17).'),
    T('m3', 'M', 1, 'Midterm Practice Quiz v2 + drill weak topics', ''),
    T('mx', 'M', 2, 'MIDTERM EXAM: attempt 1 (Honorlock)', '17 questions, 120 min, proctored. 2 attempts, the higher score counts. Worth 20% of the grade. Read the exam report after.', { w: 20, key: 'mid' }),
    T('my', 'M', 1, 'Midterm attempt 2, only if below target', 'Keeps the higher of the two scores.'),
    T('c1', 'C', 0.5, 'Read the Unit C Student Guide', ''),
    T('c2', 'C', 2.5, 'Complex numbers; complex roots of quadratics', ''),
    T('c3', 'C', 3, 'Graph quadratics: vertex, axis of symmetry, intercepts', ''),
    T('c4', 'C', 2, 'Polynomial long division', ''),
    T('c5', 'C', 2, 'Synthetic division', ''),
    T('c6', 'C', 2.5, 'Polynomials: end behavior', ''),
    T('c7', 'C', 2.5, 'Polynomials: intercepts, multiplicity, sketching', ''),
    T('c8', 'C', 2.5, 'Rational functions: domain, range, intercepts', ''),
    T('c9', 'C', 3, 'Rational functions: asymptotes and full graphs', ''),
    T('c10', 'C', 2.5, 'Exponential functions: evaluate, graph, asymptotes', ''),
    T('c11', 'C', 2, 'Exponential models: growth, decay, compound interest', ''),
    T('c12', 'C', 2.5, 'Logarithms: evaluate, properties, expand/condense, graph', ''),
    T('c13', 'C', 2.5, 'Solve exponential & logarithmic equations', ''),
    T('cq', 'C', 2, 'UNIT C QUIZ: retake until 100%', 'Worth 10% of the grade.', { w: 10, key: 'qc' }),
    T('d1', 'D', 0.5, 'Read the Unit D Student Guide', ''),
    T('d2', 'D', 2.5, 'Angle measure: degrees, minutes, seconds, radians', ''),
    T('d3', 'D', 2.5, 'Arc length, central angle, points on a circle', ''),
    T('d4', 'D', 3, 'Right triangle trig: Pythagorean Theorem, trig ratios', ''),
    T('d5', 'D', 2.5, 'Right triangle real-world problems', ''),
    T('d6', 'D', 3.5, 'Unit circle & exact values at special angles', ''),
    T('d7', 'D', 2, 'Approximate values; calculator degree vs radian mode', ''),
    T('d8', 'D', 2.5, 'Reference angles: degrees and radians', ''),
    T('d9', 'D', 3, 'All six trig values; quadrant signs', ''),
    T('d10', 'D', 3, 'Graph sine and cosine', ''),
    T('d11', 'D', 2.5, 'Graph tangent, cotangent, secant, cosecant', ''),
    T('d12', 'D', 3, 'Amplitude, period, phase shift', ''),
    T('d13', 'D', 2, 'Sinusoidal real-world models', ''),
    T('d14', 'D', 2.5, 'Inverse trig functions', ''),
    T('d15', 'D', 2, 'Composites with inverse trig', ''),
    T('d16', 'D', 3, 'Verify & simplify trig identities', ''),
    T('d17', 'D', 3, 'Sum/difference and double-angle identities', ''),
    T('d18', 'D', 3, 'Solve trig equations + real-world problems', ''),
    T('dq', 'D', 2, 'UNIT D QUIZ: retake until 100%', 'Worth 10% of the grade.', { w: 10, key: 'qd' }),
    T('f1', 'F', 2, 'Final Student Guide + work the Final Study Guide', ''),
    T('f2', 'F', 2, 'Final Practice Quiz v1 (all 4 units): review every miss', ''),
    T('f3', 'F', 1.5, 'Re-run the Unit A and B Quizzes as review', ''),
    T('f4', 'F', 1.5, 'Final Practice Quiz v2 + drill weak topics', ''),
    T('fx', 'F', 2, 'FINAL EXAM: attempt 1 (Honorlock)', '20 questions, 120 min, proctored. 2 attempts, higher counts. Worth 40% of the grade.', { w: 40, key: 'fin' }),
    T('fy', 'F', 1, 'Final attempt 2, only if below target', ''),
    T('fz', 'F', 0.5, 'End-of-course survey + submit Proctoring Review for Exams', 'The support team has to certify the proctoring review before you can apply for credit. It can take up to 5 business days.')
  ];
  const GNAME = { qa: 'Unit A Quiz', qb: 'Unit B Quiz', mid: 'Midterm Exam', qc: 'Unit C Quiz', qd: 'Unit D Quiz', fin: 'Final Exam' };
  const GRADED = TASKS.filter((t) => t.g).map((t) => ({ key: t.g.key, task: t.id, w: t.g.w, name: GNAME[t.g.key] }));

  const pad = (n) => String(n).padStart(2, '0');
  const isoOf = (dt) => dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate());
  const parse = (iso) => { const [y, m, d] = iso.split('-').map(Number); return new Date(y, m - 1, d); };
  const next = (iso) => { const d = parse(iso); d.setDate(d.getDate() + 1); return isoOf(d); };

  /* Lay every task onto the calendar by the planned minutes per day. */
  const DAYS = {};           // iso -> { min, tasks: [ids] }
  const DUE = {};            // task id -> planned finish date
  (function build() {
    let iso = START, i = 0, left = TASKS[0].h * 60, guard = 0;
    while (i < TASKS.length && guard++ < 800) {
      let m = minutesFor(iso);
      if (m) {
        DAYS[iso] = { min: m, tasks: [] };
        while (m > 0 && i < TASKS.length) {
          if (!DAYS[iso].tasks.includes(TASKS[i].id)) DAYS[iso].tasks.push(TASKS[i].id);
          const use = Math.min(m, left); m -= use; left -= use;
          if (left <= 0.001) { DUE[TASKS[i].id] = iso; i++; if (i < TASKS.length) left = TASKS[i].h * 60; }
        }
      }
      iso = next(iso);
    }
  })();

  const byId = Object.fromEntries(TASKS.map((t) => [t.id, t]));
  const fmtMin = (m) => { const h = Math.floor(m / 60), r = Math.round(m % 60); return h && r ? h + ' hr ' + r + ' min' : h ? h + (h === 1 ? ' hr' : ' hr') : r + ' min'; };

  window.HELM_PRECALC = {
    START, OFF, OFF_WHY, UNITS, TASKS, GRADED, DAYS, DUE, byId, minutesFor, fmtMin, isoOf, parse, next,
    USNA_DEADLINE: '2027-01-31',
    TOTAL_HOURS: TASKS.reduce((a, t) => a + t.h, 0),
    LINKS: {
      canvas: 'https://asuce.instructure.com/courses/9336',
      modules: 'https://asuce.instructure.com/courses/9336/modules',
      grades: 'https://asuce.instructure.com/courses/9336/grades',
      syllabus: 'https://learning-asu.simplesyllabus.com/en-US/doc/gke4uqfyu/?mode=view',
      aleks: 'https://www.aleks.com/',
      desmos: 'https://www.desmos.com/calculator',
      support: 'https://linktr.ee/mathsupport'
    },
    dayFor(iso) { return DAYS[iso] || { min: 0, tasks: [] }; }
  };
})();
