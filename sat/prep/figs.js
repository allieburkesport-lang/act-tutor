/* ---------- Labeled drawings for every shape question (Show me how, Formula, Learn it) ----------
   figFor(q) reads the numbers from the question and returns a picture box, or '' when the question has no shape. */
(function () {
  const NAVY = '#13315C', RED = '#C2410C', GRN = '#047857', MUTE = '#64748B', INK = '#0F172A';
  const T = (x, y, s, o = {}) => `<text x="${x}" y="${y}" font-family="Helvetica,Arial,sans-serif" font-size="${o.fs || 16}" font-weight="${o.fw || 700}" fill="${o.c || INK}" text-anchor="${o.a || 'middle'}" dominant-baseline="middle">${s}</text>`;
  const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" width="100%" style="max-width:${w}px;display:block;margin:4px auto" role="img">${body}</svg>`;
  const box = (title, pic, words) => `<div class="box" style="border:1.5px solid ${NAVY};background:#fff"><div class="lab" style="color:${NAVY}">Picture it · ${title}</div><div class="c">${pic}${words ? `<div style="font-size:14px;color:#334155;margin-top:6px">${words}</div>` : ''}</div></div>`;
  const plain = h => String(h).replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const sq = (x, y, s = 14) => `<path d="M${x} ${y - s} h${s} v${s}" fill="none" stroke="${INK}" stroke-width="2"/>`;
  // right triangle: right angle bottom-left (P0), top (P1), bottom-right (P2)
  function rightTri(o) {
    const W = 440, H = 250, A = [150, 200], B = [150, 40], C = [370, 200];
    let s = `<polygon points="${A} ${B} ${C}" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/>` + sq(A[0], A[1]);
    if (o.hiV) s += `<line x1="${A[0]}" y1="${A[1]}" x2="${B[0]}" y2="${B[1]}" stroke="${o.hiV}" stroke-width="6"/>`;
    if (o.hiH) s += `<line x1="${A[0]}" y1="${A[1]}" x2="${C[0]}" y2="${C[1]}" stroke="${o.hiH}" stroke-width="6"/>`;
    if (o.hiC) s += `<line x1="${B[0]}" y1="${B[1]}" x2="${C[0]}" y2="${C[1]}" stroke="${o.hiC}" stroke-width="6"/>`;
    s += T(A[0] - 18, A[1] + 14, o.pA || '') + T(B[0] - 4, B[1] - 18, o.pB || '') + T(C[0] + 18, C[1] + 14, o.pC || '');
    s += T(138, 120, o.v || '', {c: o.vc || NAVY, a: 'end', fs: 16}) + T(260, 226, o.h || '', {c: o.hc || NAVY, fs: 16}) + T(268, 108, o.c || '', {c: o.cc || RED, a: 'start', fs: 16});
    if (o.angB) s += T(B[0] + 16, B[1] + 44, o.angB, {fs: 14, c: MUTE}); if (o.angC) s += T(C[0] - 56, C[1] - 14, o.angC, {fs: 14, c: MUTE});
    return svg(W, H, s);
  }
  const N = s => s.replace(/,/g, '');
  function figFor(q) {
    if (!q || !q.q) return ''; const p = plain(q.q); let m;
    // ---- trig ----
    if ((m = p.match(/legs of length (\d+) and (\d+)\. What is the length of the hypotenuse/)))
      return box('right triangle', rightTri({v: m[1], h: m[2], c: 'c = ?', hiC: '#FECACA'}), `The two legs (${m[1]} and ${m[2]}) touch the square corner. The hypotenuse c is the long side across from it: a² + b² = c².`);
    if ((m = p.match(/angle Y is the right angle\. The side opposite angle W has length (\d+), the side adjacent to angle W has length (\d+), and the hypotenuse has length (\d+)\. What is (sin|cos|tan)\(W\)/))) {
      const pic = rightTri({pA: 'Y', pB: 'X', pC: 'W', v: `opposite = ${m[1]}`, h: `adjacent = ${m[2]}`, c: `hypotenuse = ${m[3]}`, hiV: m[4] !== 'cos' ? '#BFDBFE' : '', hiH: m[4] !== 'sin' ? '#BBF7D0' : '', hiC: m[4] !== 'tan' ? '#FECACA' : ''});
      const r = {sin: `SOH: sin(W) = opposite ÷ hypotenuse = ${m[1]}/${m[3]}`, cos: `CAH: cos(W) = adjacent ÷ hypotenuse = ${m[2]}/${m[3]}`, tan: `TOA: tan(W) = opposite ÷ adjacent = ${m[1]}/${m[2]}`}[m[4]];
      return box('stand at angle W', pic, `Stand at corner W. The side across from you is "opposite"; the leg touching you is "adjacent"; the longest side is the hypotenuse. ${r}.`);
    }
    if ((m = p.match(/right triangle ABC, angle C is the right angle and sin\(A\) = (\d+)\/(\d+)\. What is cos\(B\)/))) {
      const pic = rightTri({pA: 'C', pB: 'B', pC: 'A', v: `BC = ${m[1]}`, h: 'AC', c: `AB = ${m[2]}`, hiV: '#FDE68A'});
      return box('the same side, seen from two corners', pic, `Side BC (yellow) is ACROSS from A, so sin(A) = BC/AB = ${m[1]}/${m[2]}. The same side BC TOUCHES B, so cos(B) = BC/AB too. Same two sides → same fraction: cos(B) = ${m[1]}/${m[2]}.`);
    }
    if ((m = p.match(/30°−60°−90° triangle, the side opposite the 30° angle has length (\d+)/)))
      return box('30-60-90 triangle', rightTri({v: `short leg x = ${m[1]}`, h: 'long leg x√3', c: 'hyp = 2x = ?', angB: '60°', angC: '30°'}), `The short leg is across from 30°. The hypotenuse is always 2 × the short leg = 2 × ${m[1]}.`);
    if ((m = p.match(/isosceles right triangle \(45°−45°−90°\) has legs of length (\d+)/)))
      return box('45-45-90 triangle', rightTri({v: `x = ${m[1]}`, h: `x = ${m[1]}`, c: 'hypotenuse = x√2', angB: '45°', angC: '45°'}), `Both legs are equal. The hypotenuse is leg × √2 = ${m[1]}√2.`);
    // ---- circles ----
    const circ = (body, w = 320, h = 250) => svg(w, h, `<circle cx="160" cy="125" r="95" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/><circle cx="160" cy="125" r="3.5" fill="${INK}"/>` + body);
    if ((m = p.match(/circle has a radius of (\d+)\. What is its area/)))
      return box('circle', circ(`<line x1="160" y1="125" x2="255" y2="125" stroke="${RED}" stroke-width="3"/>` + T(207, 110, 'r = ' + m[1], {c: RED})), `Area = πr²: square the radius (the red line from the center to the edge).`);
    if ((m = p.match(/circumference of a circle is (\d+)π inches/)))
      return box('circle', circ(`<line x1="65" y1="125" x2="255" y2="125" stroke="${RED}" stroke-width="3"/>` + T(160, 110, 'd = ?', {c: RED}) + T(160, 238, `around the edge: C = ${m[1]}π`, {fs: 14, c: NAVY})), `The diameter goes all the way across through the center. C = πd, so d = ${m[1]}.`);
    if ((m = p.match(/radius of (\d+)\. A central angle measures (\d+)°\. What is the (arc length|sector area)/))) {
      const a = +m[2] * Math.PI / 180, x2 = 160 + 95 * Math.cos(-a), y2 = 125 + 95 * Math.sin(-a), big = +m[2] > 180 ? 1 : 0;
      const sector = m[3] === 'sector area' ? `<path d="M160 125 L255 125 A95 95 0 ${big} 0 ${x2.toFixed(1)} ${y2.toFixed(1)} Z" fill="#FDE68A" stroke="none"/>` : '';
      const arc = `<path d="M255 125 A95 95 0 ${big} 0 ${x2.toFixed(1)} ${y2.toFixed(1)}" fill="none" stroke="${RED}" stroke-width="6"/>`;
      return box(m[3], svg(320, 250, `<circle cx="160" cy="125" r="95" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/>${sector}${m[3] === 'arc length' ? arc : ''}<line x1="160" y1="125" x2="255" y2="125" stroke="${INK}" stroke-width="2.5"/><line x1="160" y1="125" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${INK}" stroke-width="2.5"/>` + T(210, 140, 'r = ' + m[1], {fs: 14}) + T(180, 112, m[2] + '°', {fs: 14, c: NAVY})),
        `${m[2]}° out of 360° is the fraction of the circle you keep. ${m[3] === 'arc length' ? 'Arc length (red) = fraction × 2πr.' : 'Sector area (yellow slice) = fraction × πr².'}`);
    }
    if ((m = p.match(/tangent to a circle with center O at point T\. The radius OT is (\d+)\. Point P is on the tangent line, and TP = (\d+)/)))
      return box('tangent line', svg(340, 260, `<circle cx="120" cy="140" r="90" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/><line x1="210" y1="20" x2="210" y2="250" stroke="${NAVY}" stroke-width="2.5"/><line x1="120" y1="140" x2="210" y2="140" stroke="${INK}" stroke-width="2.5"/><line x1="210" y1="140" x2="210" y2="40" stroke="${GRN}" stroke-width="5"/><line x1="120" y1="140" x2="210" y2="40" stroke="${RED}" stroke-width="3" stroke-dasharray="7 5"/><path d="M196 140 v-14 h14" fill="none" stroke="${INK}" stroke-width="2"/>` +
        T(108, 152, 'O') + T(226, 152, 'T') + T(226, 40, 'P') + T(165, 158, 'OT = ' + m[1], {fs: 14}) + T(262, 90, 'TP = ' + m[2], {fs: 14, c: GRN}) + T(135, 80, 'OP = ?', {fs: 14, c: RED})),
        'A tangent line touches the circle at one point and makes a right angle with the radius there. So OTP is a right triangle: OP² = OT² + TP².');
    if (/The equation of a circle in the xy-plane/.test(p))
      return box('circle on a graph', svg(300, 220, `<line x1="20" y1="110" x2="280" y2="110" stroke="${MUTE}"/><line x1="150" y1="10" x2="150" y2="210" stroke="${MUTE}"/><circle cx="185" cy="80" r="60" fill="none" stroke="${INK}" stroke-width="2.5"/><circle cx="185" cy="80" r="3.5" fill="${INK}"/><line x1="185" y1="80" x2="245" y2="80" stroke="${RED}" stroke-width="3"/>` + T(185, 66, '(h, k)', {fs: 13}) + T(215, 94, 'r', {c: RED})),
        'Completing the square turns the equation into (x − h)² + (y − k)² = r². The number on the right is r²; take its square root for the radius.');
    // ---- area / volume ----
    if ((m = p.match(/rectangle has a length of (\d+) inches and a width of (\d+) inches\. What is its (perimeter|area)/)))
      return box(m[3], svg(320, 200, `<rect x="40" y="40" width="240" height="120" fill="${m[3] === 'area' ? '#FDE68A' : '#EEF2F7'}" stroke="${m[3] === 'perimeter' ? RED : INK}" stroke-width="${m[3] === 'perimeter' ? 5 : 2.5}"/>` + T(160, 182, 'length = ' + m[1]) + T(20, 100, 'w = ' + m[2], {a: 'middle', fs: 14})),
        m[3] === 'area' ? 'Area is the space INSIDE (yellow): length × width.' : 'Perimeter is the fence AROUND the edge (red): add all 4 sides = 2 × (length + width).');
    if ((m = p.match(/cylinder has a radius of (\d+) centimeters and a height of (\d+)/)))
      return box('cylinder', svg(300, 250, `<ellipse cx="150" cy="200" rx="90" ry="25" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/><rect x="60" y="50" width="180" height="150" fill="#EEF2F7" stroke="none"/><line x1="60" y1="50" x2="60" y2="200" stroke="${INK}" stroke-width="2.5"/><line x1="240" y1="50" x2="240" y2="200" stroke="${INK}" stroke-width="2.5"/><ellipse cx="150" cy="50" rx="90" ry="25" fill="#FDE68A" stroke="${INK}" stroke-width="2.5"/><line x1="150" y1="50" x2="240" y2="50" stroke="${RED}" stroke-width="3"/>` + T(195, 38, 'r = ' + m[1], {c: RED, fs: 14}) + T(266, 125, 'h = ' + m[2], {fs: 14})),
        'Volume = (area of the circle on top, yellow) × height = πr² × h.');
    if ((m = p.match(/sphere has a diameter of (\d+) inches/)))
      return box('sphere', svg(280, 230, `<circle cx="140" cy="115" r="95" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/><ellipse cx="140" cy="115" rx="95" ry="25" fill="none" stroke="${MUTE}" stroke-dasharray="5 4"/><line x1="45" y1="115" x2="235" y2="115" stroke="${NAVY}" stroke-width="2"/><line x1="140" y1="115" x2="235" y2="115" stroke="${RED}" stroke-width="4"/>` + T(140, 100, 'd = ' + m[1], {fs: 14, c: NAVY}) + T(188, 132, 'r = ' + (+m[1] / 2), {fs: 14, c: RED})),
        `They gave the diameter (all the way across). The formula needs the radius (half of it): r = ${+m[1] / 2}. V = (4/3)πr³.`);
    if ((m = p.match(/similar triangles have corresponding sides in the ratio 1 to (\d+)\. The smaller triangle has an area of (\d+)/)))
      return box('similar triangles', svg(360, 200, `<polygon points="30,170 90,170 30,120" fill="#EEF2F7" stroke="${INK}" stroke-width="2"/><polygon points="150,180 330,180 150,30" fill="#FDE68A" stroke="${INK}" stroke-width="2"/>` + T(60, 188, 'side 1', {fs: 13}) + T(240, 196, 'side ' + m[1], {fs: 13}) + T(60, 100, 'area ' + m[2], {fs: 13}) + T(205, 120, 'area = ?', {fs: 14, c: RED})),
        `Every side is ${m[1]}× as long, so the area grows by ${m[1]}² = ${(+m[1]) ** 2} (it grows in two directions).`);
    if ((m = p.match(/cube-shaped box has a volume of (\d+) cubic feet\. A second box has every edge (\d+) times as long/))) {
      const cube = (x, y, s, f) => `<polygon points="${x},${y} ${x + s},${y} ${x + s},${y + s} ${x},${y + s}" fill="${f}" stroke="${INK}" stroke-width="2"/><polygon points="${x},${y} ${x + s * .35},${y - s * .35} ${x + s * 1.35},${y - s * .35} ${x + s},${y}" fill="#fff" stroke="${INK}" stroke-width="2"/><polygon points="${x + s},${y} ${x + s * 1.35},${y - s * .35} ${x + s * 1.35},${y + s * .65} ${x + s},${y + s}" fill="#E2E8F0" stroke="${INK}" stroke-width="2"/>`;
      return box('scaled boxes', svg(360, 220, cube(30, 150, 45, '#EEF2F7') + cube(150, 80, 120, '#FDE68A') + T(52, 208, 'V = ' + m[1], {fs: 13}) + T(210, 212, 'edges × ' + m[2] + ' → V = ?', {fs: 14, c: RED})),
        `Length, width AND height all grow ×${m[2]}, so the volume grows ${m[2]}×${m[2]}×${m[2]} = ${(+m[2]) ** 3}.`);
    }
    // ---- lines, angles, triangles ----
    if ((m = p.match(/angle A measures (\d+)° and angle B measures (\d+)°/)))
      return box('triangle', svg(320, 210, `<polygon points="40,180 280,180 120,40" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/>` + T(30, 192, 'A') + T(292, 192, 'B') + T(120, 26, 'C') + T(72, 166, m[1] + '°', {fs: 14, c: NAVY}) + T(250, 166, m[2] + '°', {fs: 14, c: NAVY}) + T(122, 66, '?', {c: RED})),
        'The three inside angles of any triangle add to 180°.');
    if ((m = p.match(/Two lines intersect\. One of the angles formed measures (\d+)°\. What is the measure of the angle (directly across|next to it)/)))
      return box('two crossing lines', svg(320, 220, `<line x1="30" y1="40" x2="290" y2="180" stroke="${INK}" stroke-width="2.5"/><line x1="30" y1="180" x2="290" y2="40" stroke="${INK}" stroke-width="2.5"/>` + T(100, 110, m[1] + '°', {fs: 15, c: NAVY}) + T(220, 110, m[2] === 'directly across' ? '?' : '', {c: RED}) + T(160, 60, m[2] === 'next to it' ? '?' : '', {c: RED})),
        m[2] === 'directly across' ? 'Angles directly across from each other (vertical angles) are EQUAL.' : 'Angles side by side on a straight line add to 180°.');
    if ((m = p.match(/parallel and are cut by a transversal\. One angle measures (\d+)°\. What is the measure of its (same-side interior|corresponding)/))) {
      const same = m[2] === 'same-side interior';
      return box('parallel lines + transversal', svg(340, 230, `<line x1="20" y1="70" x2="320" y2="70" stroke="${INK}" stroke-width="2.5"/><line x1="20" y1="160" x2="320" y2="160" stroke="${INK}" stroke-width="2.5"/><line x1="110" y1="220" x2="230" y2="10" stroke="${NAVY}" stroke-width="2.5"/>` + T(300, 58, 'm', {fs: 14, c: MUTE}) + T(300, 148, 'n', {fs: 14, c: MUTE}) +
        T(218, 84, m[1] + '°', {fs: 14, c: NAVY}) + (same ? T(185, 146, '?', {c: RED}) : T(172, 176, '?', {c: RED}))),
        same ? 'Same-side interior angles sit between the parallel lines on the same side of the transversal. They add to 180°.' : 'Corresponding angles are in the same spot at each crossing. They are EQUAL.');
    }
    if ((m = p.match(/two interior angles measure (\d+)° and (\d+)°.*exterior/)))
      return box('exterior angle', svg(340, 200, `<polygon points="40,170 230,170 110,40" fill="#EEF2F7" stroke="${INK}" stroke-width="2.5"/><line x1="230" y1="170" x2="320" y2="170" stroke="${INK}" stroke-width="2.5" stroke-dasharray="6 4"/>` + T(70, 156, m[1] + '°', {fs: 14, c: NAVY}) + T(112, 70, m[2] + '°', {fs: 14, c: NAVY}) + T(205, 156, 'third', {fs: 12, c: MUTE}) + T(262, 152, '?', {c: RED})),
        `The outside angle (red ?) and the third inside angle make a straight line (180°). Shortcut: outside angle = the two far angles added = ${m[1]} + ${m[2]}.`);
    if ((m = p.match(/PQ = (\d+), QR = (\d+), and ST = (\d+)/)))
      return box('similar triangles', svg(380, 215, `<polygon points="20,170 110,170 20,110" fill="#EEF2F7" stroke="${INK}" stroke-width="2"/><polygon points="160,185 360,185 160,50" fill="#FDE68A" stroke="${INK}" stroke-width="2"/>` + T(12, 104, 'P', {fs: 14}) + T(12, 180, 'Q', {fs: 14}) + T(120, 180, 'R', {fs: 14}) + T(150, 44, 'S', {fs: 14}) + T(150, 196, 'T', {fs: 14}) + T(370, 196, 'U', {fs: 14}) +
        T(8, 140, m[1], {fs: 13, a: 'end'}) + T(65, 186, m[2], {fs: 13}) + T(146, 118, m[3], {fs: 13, a: 'end'}) + T(260, 204, 'TU = ?', {fs: 14, c: RED})),
        `Match the letters: P↔S, Q↔T, R↔U. PQ (${m[1]}) matches ST (${m[3]}), so every side is × ${+m[3] / +m[1]}. QR matches TU.`);
    return '';
  }
  window.figFor = figFor;
})();
