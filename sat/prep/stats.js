/* ---------- STATS: BI dashboard (#/stats, #/stats/<skill>, #/stats/sec:Math) ---------- */
const ST = {period: 'day', from: '', to: '', sec: 'all', bp: true, site: true};
const SITE_NAME = 'HELM';
const SCOL = {Math: '#4F46E5', English: '#0D9488'};
let CH = [];
function dkey(d) { return d.toLocaleDateString('en-CA') }
function firstTries() {  // SAT rules: the first time he ever saw each question, answered with no help (see isScored in sat.html)
  const out = [];
  LOG.forEach(x => { const q = QBY[x.id]; if (!q || !SK2[q.skill]) return; if (!isScored(x)) return; out.push(Object.assign({q, s: SK2[q.skill]}, x)) });
  return out.sort((a, b) => a.ts - b.ts)
}
function rangeOf(per) {  // [fromKey, toKey] inclusive
  const t = new Date(); t.setHours(0, 0, 0, 0); const today = dkey(t);
  if (per === 'all') return ['0000', '9999'];
  if (per === 'custom') return [ST.from || '0000', ST.to || today];
  const n = per === 'day' ? 1 : +per; const f = new Date(t); f.setDate(f.getDate() - (n - 1)); return [dkey(f), today]
}
function inPeriod(rows, per) { const [a, b] = rangeOf(per); return rows.filter(r => r.day >= a && r.day <= b) }
function prevPeriod(rows, per) {
  if (per === 'all') return []; const [a, b] = rangeOf(per); const A = new Date(a + 'T12:00'), B = new Date(b + 'T12:00'); const n = Math.round((B - A) / 864e5) + 1;
  const pa = new Date(A); pa.setDate(pa.getDate() - n); const pb = new Date(A); pb.setDate(pb.getDate() - 1); return rows.filter(r => r.day >= dkey(pa) && r.day <= dkey(pb))
}
const pct = (rows) => rows.length ? Math.round(100 * rows.filter(r => r.ok).length / rows.length) : null;
const avgSec = rows => { const t = rows.filter(r => r.sec > 0 && r.sec < 1800); return t.length ? Math.round(t.reduce((a, r) => a + r.sec, 0) / t.length) : null };
const paceOf = rows => rows.length ? Math.round(rows.reduce((a, r) => a + PACE[r.s.sec], 0) / rows.length) : null;
const mmss = s => s == null ? '—' : Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
function delta(now, prev) { if (now == null || prev == null) return ''; const d = now - prev; return `<span style="font-size:14px;font-weight:700;color:${d >= 0 ? '#15803d' : '#b91c1c'}">${d >= 0 ? '▲' : '▼'} ${Math.abs(d)}${typeof now === 'number' && now <= 100 ? ' pts' : ''}</span>` }
function kpi(lab, val, sub, extra) { return `<div class="card stat"><div class="l">${lab}</div><div class="v hd">${val}</div><div style="font-size:13px;color:var(--mute);margin-top:2px">${sub || ''} ${extra || ''}</div></div>` }
function bucketKey(day, gran) { if (gran === 'day') return day; const d = new Date(day + 'T12:00'); const m = new Date(d); m.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return dkey(m) }
function series(rows, gran) {
  const b = {}; rows.forEach(r => { const k = bucketKey(r.day, gran); (b[k] = b[k] || []).push(r) });
  const keys = Object.keys(b).sort();
  return {keys, lab: keys.map(k => { const d = new Date(k + 'T12:00'); return (gran === 'week' ? 'wk of ' : '') + d.toLocaleDateString('en-US', {month: 'short', day: 'numeric'}) }),
    acc: keys.map(k => pct(b[k])), m: keys.map(k => b[k].filter(r => r.s.sec === 'Math').length), e: keys.map(k => b[k].filter(r => r.s.sec !== 'Math').length),
    accM: keys.map(k => pct(b[k].filter(r => r.s.sec === 'Math'))), accE: keys.map(k => pct(b[k].filter(r => r.s.sec !== 'Math')))}
}
function chart(id, cfg) { const el = document.getElementById(id); if (!el || typeof Chart === 'undefined') return; CH.push(new Chart(el, cfg)) }
function killCharts() { CH.forEach(c => { try { c.destroy() } catch (e) {} }); CH = [] }
function chartTheme() { if (typeof Chart === 'undefined' || Chart._helm) return; Chart._helm = 1; const D = Chart.defaults;
  D.font.family = "'Helvetica Neue',Helvetica,Arial,sans-serif"; D.font.size = 12; D.color = '#64748B'; D.borderColor = '#EEF2F6';
  D.plugins.legend.labels.usePointStyle = true; D.plugins.legend.labels.boxWidth = 8; D.plugins.legend.labels.padding = 14;
  Object.assign(D.plugins.tooltip, {backgroundColor: '#0F172A', titleColor: '#fff', bodyColor: '#E2E8F0', padding: 10, cornerRadius: 8, displayColors: true, boxPadding: 4, titleFont: {weight: '700'}});
  D.elements.bar.borderRadius = 4; D.elements.line.borderWidth = 2.5; D.elements.point.radius = 3; D.elements.point.hoverRadius = 5;
  D.scale.grid.color = 'rgba(161,161,170,.4)'; D.scale.border = {display: false, dash: [3, 3]};
  D.plugins.legend.position = 'top'; D.plugins.legend.align = 'end';
  D.animation.duration = 150; D.animation.easing = 'easeOutQuad' }
function ensureChartJs(cb0) { const cb = () => { chartTheme(); cb0() }; if (typeof Chart !== 'undefined') return cb(); const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js'; s.onload = cb; s.onerror = cb; document.head.appendChild(s) }
function filters() {
  const b = (k, v, t) => `<button class="btn sm ${ST[k] === v ? '' : 'g'}" data-st="${k}:${v}">${t}</button>`;
  return `<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center"><div style="display:flex;gap:6px;align-items:center"><span style="font-size:13px;color:var(--mute);font-weight:600">PERIOD</span><select id="stper" style="font:inherit;font-weight:600;padding:8px 10px;border:1px solid #d1d5db;border-radius:10px;background:#fff">${[['day', 'Today'], ['7', 'Last 7 days'], ['14', 'Last 14 days'], ['30', 'Last 30 days'], ['all', 'All time'], ['custom', 'Custom dates…']].map(([v, t]) => `<option value="${v}" ${ST.period === v ? 'selected' : ''}>${t}</option>`).join('')}</select>
   ${ST.period === 'custom' ? `<input type="date" id="stfrom" value="${ST.from}" style="font:inherit;padding:6px 8px;border:1px solid #d1d5db;border-radius:10px"> to <input type="date" id="stto" value="${ST.to || dkey(new Date())}" style="font:inherit;padding:6px 8px;border:1px solid #d1d5db;border-radius:10px">` : ''}</div>
   <div style="display:flex;gap:6px;align-items:center"><span style="font-size:13px;color:var(--mute);font-weight:600">DATA</span><button class="btn sm ${ST.site ? '' : 'g'}" data-src="site">${ST.site ? '☑' : '☐'} ${SITE_NAME}</button><button class="btn sm ${ST.bp ? '' : 'g'}" data-src="bp">${ST.bp ? '☑' : '☐'} Blueprint</button></div>
   <div style="display:flex;gap:6px;align-items:center"><span style="font-size:13px;color:var(--mute);font-weight:600">SECTION</span>${b('sec', 'all', 'Both')}${b('sec', 'Math', 'Math')}${b('sec', 'English', 'Reading & Writing')}</div></div>`
}
function statsPage(arg) {
  killCharts(); if (arg && arg !== 'sec:Math' && arg !== 'sec:English') return ensureChartJs(() => skillStats(arg));
  if (arg) ST.sec = arg.slice(4);
  ensureChartJs(drawStats)
}
function drawStats() {
  killCharts();
  let all = firstTries(); if (ST.sec !== 'all') all = all.filter(r => r.s.sec === ST.sec);
  const rows = ST.site ? inPeriod(all, ST.period) : [], prev = ST.site ? prevPeriod(all, ST.period) : [];
  const acc = pct(rows), pacc = pct(prev), avg = avgSec(rows), pace = paceOf(rows);
  const days = new Set(all.map(r => r.day)); let streak = 0; const d = new Date(); while (days.has(dkey(d))) { streak++; d.setDate(d.getDate() - 1) }
  const skills = BANK.skills.filter(s => ST.sec === 'all' || s.sec === ST.sec);
  const useBpCat = ST.bp && ST.period === 'all';  // Blueprint category totals have no dates
  const per = skills.map(s => { const r = rows.filter(x => x.q.skill === s.id), b = BPS[s.id] || {n: 0, ok: 0}; const sn = r.length, sok = r.filter(x => x.ok).length; const n = sn + (useBpCat ? b.n : 0), ok = sok + (useBpCat ? b.ok : 0);
    return {s, n, ok, acc: n ? Math.round(100 * ok / n) : null, sn, sok, sacc: sn ? Math.round(100 * sok / sn) : null, base: b.n ? Math.round(100 * b.ok / b.n) : null, bn: b.n, avg: avgSec(r)} });
  const strong = per.filter(p => p.n >= 3 && p.acc >= 70).length;
  const gran = 'day';
  const [from, upto] = rangeOf(ST.period);
  const bpd = (!ST.bp || typeof BPD === 'undefined' ? [] : BPD).filter(x => x.day >= from && x.day <= upto).map(x => ({day: x.day, n: ST.sec === 'all' ? x.n : ST.sec === 'Math' ? (x.math ? x.math.n : 0) : (x.rw ? x.rw.n : 0), acc: ST.sec === 'all' ? x.acc : ST.sec === 'Math' ? (x.math ? x.math.acc : null) : (x.rw ? x.rw.acc : null)})).filter(x => x.n);
  const dz = series(rows, 'day'); const days2 = [...new Set([...dz.keys, ...bpd.map(x => x.day)])].sort();
  const pick = (arr) => days2.map(d => { const i = dz.keys.indexOf(d); return i < 0 ? null : arr[i] });
  const se = {lab: days2.map(k => new Date(k + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'})), accM: pick(dz.accM), accE: pick(dz.accE), m: pick(dz.m).map(x => x || 0), e: pick(dz.e).map(x => x || 0),
    bpA: days2.map(d => { const x = bpd.find(y => y.day === d); return x ? x.acc : null }), bpN: days2.map(d => { const x = bpd.find(y => y.day === d); return x ? x.n : 0 })};
  const bpTot = bpd.reduce((a, x) => a + x.n, 0), bpOk = Math.round(bpd.reduce((a, x) => a + x.n * (x.acc || 0) / 100, 0));
  const sOk = rows.filter(r => r.ok).length, tot = rows.length + bpTot, tOk = sOk + bpOk, tAcc = tot ? Math.round(100 * tOk / tot) : null;
  se.comb = days2.map((d, i) => { const sr = rows.filter(r => r.day === d), x = bpd.find(y => y.day === d); const n = sr.length + (x ? x.n : 0); return n ? Math.round(100 * (sr.filter(r => r.ok).length + (x ? x.n * (x.acc || 0) / 100 : 0)) / n) : null });
  const diff = ['E', 'M', 'H'].map(k => ({k, M: pct(rows.filter(r => r.q.diff === k && r.s.sec === 'Math')), E: pct(rows.filter(r => r.q.diff === k && r.s.sec !== 'Math')), n: rows.filter(r => r.q.diff === k).length}));
  // week x skill heat
  const wks = [...new Set(all.map(r => bucketKey(r.day, 'week')))].sort().slice(-6);
  const heat = skills.map(s => ({s, cells: wks.map(w => { const r = all.filter(x => x.q.skill === s.id && bucketKey(x.day, 'week') === w); return {n: r.length, a: pct(r)} })})).filter(h => h.cells.some(c => c.n));
  const hc = a => a == null ? '#f3f4f6' : a < 50 ? '#fde2e2' : a < 70 ? '#FFEDD5' : '#dcfce7';
  const order = per.filter(p => p.n).sort((a, b) => a.acc - b.acc || (b.s.share || 0) - (a.s.share || 0));
  const missed = rows.filter(r => !r.ok).slice(-12).reverse();
  app().innerHTML = topbar('stats') + `<div class="page" style="gap:18px"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;align-items:flex-end"><div><h1 class="hd" style="margin:0;font-size:30px">Stats</h1><div style="color:var(--mute);font-size:14px">Scored like the SAT: one try, no help. Only the first time he ever answers a question counts, and only if he didn't open help first. Retries and help are tracked separately under “When he used help.” Click any category to see why.</div></div>${filters()}</div>
   ${scoresBlock()}
   <section class="stats" style="grid-template-columns:repeat(6,minmax(0,1fr))">
    ${kpi('Questions', tot, [ST.site ? SITE_NAME + ' ' + rows.length : '', ST.bp ? 'Blueprint ' + bpTot : ''].filter(Boolean).join(' · '))}
    ${kpi('Right on first try', tAcc == null ? '—' : tAcc + '%', ST.site && ST.bp ? 'combined' : ST.site ? SITE_NAME : 'Blueprint', ST.site && !ST.bp ? delta(acc, pacc) : '')}
    ${kpi('Right / wrong', tot ? `${tOk} / ${tot - tOk}` : '—', '')}
    ${kpi('Avg time / question', mmss(avg), 'SAT pace ' + mmss(pace), avg && pace ? (avg <= pace ? '<span style="color:#15803d;font-weight:700">on pace</span>' : '<span style="color:#b91c1c;font-weight:700">slow</span>') : '')}
    ${kpi('Strong categories', strong + ' / ' + skills.length, '70%+ with 3+ questions')}
    ${kpi('By source', `<span style="font-size:20px">${ST.site ? SITE_NAME + ' ' + (acc == null ? '—' : acc + '%') : ''}${ST.site && ST.bp ? '<br>' : ''}${ST.bp ? 'Blueprint ' + (bpTot ? Math.round(100 * bpOk / bpTot) + '%' : '—') : ''}</span>`, '')}
   </section>
   <div class="cols" style="grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)">
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Accuracy over time</h2><div style="height:260px"><canvas id="c1"></canvas></div></section>
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Questions per ${gran}</h2><div style="height:260px"><canvas id="c2"></canvas></div></section>
   </div>
   <div class="cols" style="grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)">
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 2px;font-size:19px">By category <span style="font-size:13px;color:var(--mute);font-weight:500">· weakest first · bar = ${ST.site && useBpCat ? 'combined' : ST.site ? SITE_NAME : 'Blueprint'}${ST.bp && !useBpCat ? ' (Blueprint categories are all-time only)' : ''} · ◆ = Blueprint · click a bar</span></h2><div style="height:${Math.max(220, 30 * order.length + 40)}px"><canvas id="c3"></canvas></div></section>
    <div style="display:flex;flex-direction:column;gap:18px">
     <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">By difficulty <span style="font-size:13px;color:var(--mute);font-weight:500">· ${SITE_NAME} only (Blueprint gives no per-question data)</span></h2><div style="height:200px"><canvas id="c4"></canvas></div></section>
     <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Time per question vs SAT pace <span style="font-size:13px;color:var(--mute);font-weight:500">· ${SITE_NAME} only</span></h2><div style="height:${Math.max(180, 24 * order.length)}px"><canvas id="c5"></canvas></div></section>
    </div>
   </div>
   <section class="card" style="padding:16px 18px;overflow-x:auto"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Category × week <span style="font-size:13px;color:var(--mute);font-weight:500">red under 50% · yellow 50–69% · green 70%+</span></h2>
    ${heat.length ? `<table class="rep"><thead><tr><th>Category</th>${wks.map(w => `<th>wk of ${new Date(w + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'})}</th>`).join('')}</tr></thead><tbody>${heat.map(h => `<tr style="cursor:pointer" data-go="#/stats/${h.s.id}"><td><b>${esc(h.s.name)}</b></td>${h.cells.map(c => `<td style="background:${hc(c.a)};text-align:center;font-weight:700">${c.n ? c.a + '%<div style="font-size:11px;font-weight:500;color:var(--mute)">' + c.n + ' Qs</div>' : ''}</td>`).join('')}</tr>`).join('')}</tbody></table>` : '<div style="color:var(--mute)">No practice yet in this view.</div>'}</section>
   <section class="card" style="padding:16px 18px;overflow-x:auto"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Every category</h2>
    <table class="rep"><thead><tr><th>Category</th><th>Section</th><th>% of SAT (est.)</th><th>Qs</th><th>Right</th><th>Wrong</th><th>Score</th><th>${SITE_NAME}</th><th>Blueprint</th><th>Change</th><th>Avg time</th><th></th></tr></thead><tbody>
    ${per.sort((a, b) => (b.s.share || 0) - (a.s.share || 0)).map(p => { const lv = level(p.acc, p.n); return `<tr style="cursor:pointer" data-go="#/stats/${p.s.id}"><td><b>${esc(p.s.name)}</b></td><td>${p.s.sec === 'Math' ? 'Math' : 'R&W'}</td><td>${Math.round(p.s.share || 0)}%</td><td>${p.n}</td><td style="color:#15803d;font-weight:700">${p.ok}</td><td style="color:#b91c1c;font-weight:700">${p.n - p.ok}</td><td>${p.n ? `<span class="pill" style="color:${lv[1]};background:${lv[2]}">${p.acc}%</span>` : '—'}</td><td>${p.sacc == null ? '—' : p.sacc + '% <span style="color:var(--mute);font-size:12px">(' + p.sn + ')</span>'}</td><td>${p.base == null ? '—' : p.base + '% <span style="color:var(--mute);font-size:12px">(' + p.bn + ')</span>'}</td><td>${p.sn && p.base != null ? delta(p.sacc, p.base) : ''}</td><td>${mmss(p.avg)}</td><td><button class="btn g sm" data-go="#/stats/${p.s.id}">Details →</button></td></tr>` }).join('')}</tbody></table></section>
   ${helpSection(null)}
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Latest misses</h2>${missed.length ? missed.map(missRow).join('') : '<div style="color:var(--mute)">None in this period.</div>'}</section>
  </div>`;
  window.scrollTo(0, 0);
  const tick = {font: {family: "'Helvetica Neue',Helvetica,Arial,sans-serif", size: 12}};
  scoresChart();
  chart('c1', {type: 'line', data: {labels: se.lab, datasets: [
    ST.site && ST.sec !== 'English' ? {label: 'Math', data: se.accM, borderColor: SCOL.Math, backgroundColor: SCOL.Math, tension: .3, spanGaps: true} : null,
    ST.site && ST.sec !== 'Math' ? {label: 'Reading & Writing', data: se.accE, borderColor: SCOL.English, backgroundColor: SCOL.English, tension: .3, spanGaps: true} : null,
    ST.bp ? {label: 'Blueprint', data: se.bpA, borderColor: '#9ca3af', backgroundColor: '#9ca3af', borderDash: [4, 4], tension: .3, spanGaps: true} : null,
    ST.bp && ST.site ? {label: 'Combined', data: se.comb, borderColor: '#111827', backgroundColor: '#111827', borderWidth: 3, tension: .3, spanGaps: true} : null,
    {label: 'Goal (1300 ≈ 75%)', data: se.lab.map(() => 75), borderColor: '#64748B', borderDash: [6, 6], pointRadius: 0}].filter(Boolean)},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('c2', {type: 'bar', data: {labels: se.lab, datasets: [ST.sec !== 'English' ? {label: 'Math', data: se.m, backgroundColor: SCOL.Math} : null, ST.sec !== 'Math' ? {label: 'Reading & Writing', data: se.e, backgroundColor: SCOL.English} : null, ST.bp ? {label: 'Blueprint', data: se.bpN, backgroundColor: '#cbd5e1'} : null].filter(Boolean)},
    options: {maintainAspectRatio: false, scales: {x: {stacked: true, ticks: tick}, y: {stacked: true, ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('c3', {type: 'bar', data: {labels: order.map(p => p.s.name), datasets: [
    {label: 'Now', data: order.map(p => p.acc), backgroundColor: order.map(p => p.acc < 50 ? '#f87171' : p.acc < 70 ? '#FB923C' : '#4ade80')},
    {label: 'Blueprint before', type: 'scatter', order: 0, data: order.filter(p => p.base != null).map(p => ({x: p.base, y: p.s.name})), backgroundColor: '#111827', pointStyle: 'rectRot', pointRadius: 6}]},
    options: {indexAxis: 'y', maintainAspectRatio: false, scales: {x: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, y: {ticks: tick}}, plugins: {legend: {display: false}, tooltip: {callbacks: {label: c => c.datasetIndex ? 'Blueprint before: ' + c.raw.x + '%' : `Now: ${c.raw}% (${order[c.dataIndex].ok}/${order[c.dataIndex].n})`}}},
      onClick: (e, els) => { if (els.length) location.hash = '#/stats/' + order[els[0].index].s.id }}});
  chart('c4', {type: 'bar', data: {labels: ['Easy', 'Medium', 'Hard'], datasets: [ST.sec !== 'English' ? {label: 'Math', data: diff.map(d => d.M), backgroundColor: SCOL.Math} : null, ST.sec !== 'Math' ? {label: 'Reading & Writing', data: diff.map(d => d.E), backgroundColor: SCOL.English} : null].filter(Boolean)},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {labels: tick}}}});
  const tt = order.filter(p => p.avg != null);
  chart('c5', {type: 'bar', data: {labels: tt.map(p => p.s.name), datasets: [{label: 'His avg (sec)', order: 1, data: tt.map(p => p.avg), backgroundColor: tt.map(p => p.avg > PACE[p.s.sec] ? '#fb923c' : '#4ade80')}, {label: 'SAT pace', type: 'scatter', order: 0, data: tt.map(p => ({x: PACE[p.s.sec], y: p.s.name})), backgroundColor: '#111827', pointStyle: 'line', pointRadius: 10, borderWidth: 3, borderColor: '#111827'}]},
    options: {indexAxis: 'y', maintainAspectRatio: false, scales: {x: {ticks: {...tick, callback: v => v + 's'}}, y: {ticks: tick}}, plugins: {legend: {display: false}}, onClick: (e, els) => { if (els.length) location.hash = '#/stats/' + tt[els[0].index].s.id }}});
}
function missRow(r) {
  const q = r.q; const ans = q.ch ? q.ch[q.ans] : (q.show || (q.grid || [])[0]);
  return `<details class="miss" style="border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin-bottom:8px;background:#fff"><summary style="cursor:pointer;display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="pill" style="background:#fde2e2;color:#b91c1c">✗ missed</span><b>${esc(r.s.name)}</b><span style="color:var(--mute);font-size:13px">${new Date(r.ts).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} · ${DIFF[q.diff]} · ${mmss(r.sec)}</span><span style="flex:1;min-width:200px;color:var(--ink);font-size:14px">${esc(plain(q.q).slice(0, 110))}…</span></summary>
   <div style="margin-top:10px;display:grid;gap:8px"><div style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:16px">${q.q}</div>
   <div><span style="color:#b91c1c;font-weight:700">He picked:</span> ${r.picked ? r.picked : '(not recorded)'} &nbsp; <span style="color:#15803d;font-weight:700">Right answer:</span> ${ans || ''}</div>
   <div class="box b-blue"><div class="lab">How to do it</div><div class="c">${q.steps.map((s, i) => (i + 1) + '. ' + esc(s)).join('<br>')}</div></div>${q.trap ? `<div class="box b-red"><div class="lab">Trap</div><div class="c">${esc(q.trap)}</div></div>` : ''}
   <div><button class="btn sm" data-go="#/drill/ids:${q.id}">Try it again</button></div></div></details>`
}
function skillStats(id) {
  killCharts(); const s = SK2[id]; if (!s) return drawStats(); loadTutorQ(() => { if (location.hash.includes(id)) skillStats(id) });
  const all = firstTries().filter(r => r.q.skill === id), rows = ST.site ? inPeriod(all, ST.period) : [];
  const acc = pct(rows), b = BPS[id] || {n: 0, ok: 0}, base = b.n ? Math.round(100 * b.ok / b.n) : null, avg = avgSec(rows);
  const se = series(rows, 'day');
  const diff = ['E', 'M', 'H'].map(k => { const r = rows.filter(x => x.q.diff === k); return {k, n: r.length, ok: r.filter(x => x.ok).length, a: pct(r)} });
  // question-type breakdown (same template = same kind of question)
  const kinds = {}; rows.forEach(r => { const t = (typeof QT !== 'undefined' && QT[r.q.id] != null) ? QT[r.q.id] : 'x'; const nm = (typeof QF !== 'undefined' && QF[r.q.id] && QF[r.q.id][0]) ? QF[r.q.id][0].n : 'Questions'; (kinds[t] = kinds[t] || {nm, r: []}).r.push(r) });
  const kl = Object.values(kinds).map(k => ({nm: k.nm, n: k.r.length, ok: k.r.filter(x => x.ok).length, a: pct(k.r), ex: k.r[0].q})).sort((a, b) => a.a - b.a);
  const traps = {}; rows.filter(r => !r.ok && r.q.trap).forEach(r => traps[r.q.trap] = (traps[r.q.trap] || 0) + 1);
  const tl = Object.entries(traps).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const missed = rows.filter(r => !r.ok).reverse(), right = rows.filter(r => r.ok).reverse();
  const why = [];
  if (rows.length < 5) why.push('Only ' + rows.length + ' questions so far, so this score can still swing a lot.');
  const hard = diff.find(d => d.k === 'H'), easy = diff.find(d => d.k === 'E');
  if (easy.n >= 2 && easy.a < 70) why.push(`Easy questions are only ${easy.a}%: the basics of this skill still need work. Start with Learn it.`);
  if (hard.n >= 2 && hard.a < 50) why.push(`Hard questions are ${hard.a}%: most points are lost on the harder versions.`);
  if (avg && avg > PACE[s.sec] * 1.5) why.push(`He takes ${mmss(avg)} per question, much slower than SAT pace (${mmss(PACE[s.sec])}).`);
  if (avg && avg < PACE[s.sec] * .4 && acc != null && acc < 60) why.push(`He answers in ${mmss(avg)} on average, very fast for this many misses: he may be rushing.`);
  if (kl.length > 1 && kl[0].a != null && kl[0].a < 50) why.push(`Weakest kind: “${kl[0].nm}” at ${kl[0].a}% (${kl[0].ok}/${kl[0].n}).`);
  if (tl.length) why.push(`Most common trap: “${tl[0][0]}” (${tl[0][1]}×).`);
  const lv = level(acc, rows.length);
  app().innerHTML = topbar('stats') + `<div class="page" style="gap:18px"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;align-items:flex-end"><div><a href="#/stats">← All stats</a><h1 class="hd" style="margin:4px 0 0;font-size:30px">${esc(s.name)}</h1><div style="color:var(--mute);font-size:14px">${s.sec === 'Math' ? 'Math' : 'Reading & Writing'} · about ${Math.round(s.share || 0)}% of the section (est.)</div></div>${filters()}</div>
   <section class="stats" style="grid-template-columns:repeat(5,minmax(0,1fr))">
    ${(() => { const sn = rows.length, so = rows.filter(r => r.ok).length, bn = ST.bp ? b.n : 0, bo = ST.bp ? b.ok : 0, n = sn + bn, c = n ? Math.round(100 * (so + bo) / n) : null, l2 = level(c, n); return kpi(ST.site && ST.bp ? 'Combined score' : ST.site ? SITE_NAME + ' score' : 'Blueprint score', c == null ? '—' : `<span style="color:${l2[1]}">${c}%</span>`, `${so + bo} right of ${n}`) })()}
    ${kpi(ST.site ? SITE_NAME + ' only' : 'Blueprint', ST.site ? (acc == null ? '—' : acc + '%') : (base == null ? '—' : base + '%'), ST.site ? rows.filter(r => r.ok).length + ' of ' + rows.length : (b.n ? b.ok + ' of ' + b.n : ''))}
    ${kpi('Blueprint before', base == null ? '—' : base + '%', b.n ? `${b.ok} of ${b.n}` : '', acc != null && base != null ? delta(acc, base) : '')}
        ${kpi('Avg time / question', mmss(avg), 'SAT pace ' + mmss(PACE[s.sec]))}
    ${kpi('Next step', `<span style="font-size:18px">${acc == null || acc < 50 ? 'Learn it, then drill' : acc < 70 ? 'Drill + redo misses' : 'Keep it warm'}</span>`, '')}
   </section>
   ${(() => { const r = winsData().rows.find(x => x.s.id === id); if (!r) return ''; return `<section class="card" style="padding:14px 18px;border-left:6px solid #15803d"><h2 class="hd" style="margin:0 0 4px;font-size:19px">What this is worth on the SAT</h2><div style="font-size:15px;line-height:1.55">The SAT will have about <b>${r.nq}</b> of these. At ${r.acc == null ? 'no data yet' : Math.round(100 * r.acc) + '%'}, Patrick is on track to get <b>${r.right == null ? '?' : r.right} of ${r.nq}</b>. ${r.steps.length ? r.steps.slice(0, 4).map((x, i) => `${i === r.steps.length - 1 ? 'All ' + r.nq : x.k + ' more'} right = <b style="color:#15803d">+${x.g}</b> (${x.tot})`).join(' · ') + (r.steps.length > 4 ? ` · All ${r.nq} = <b style="color:#15803d">+${r.pts}</b> (${(Math.round((winsData().now.total + r.pts) / 10) * 10)})` : '') : 'He is on track for all of them ✓'}</div></section>` })()}
   <section class="card" style="padding:16px 18px;border-left:6px solid #b91c1c"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Why the score is ${acc == null ? '—' : acc + '%'}</h2>${why.length ? `<ul style="margin:0;padding-left:20px;display:grid;gap:6px">${why.map(w => `<li>${esc(w)}</li>`).join('')}</ul>` : '<div>Nothing stands out. Keep practicing.</div>'}
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">${missed.length ? `<button class="btn" data-go="#/drill/ids:${[...new Set(missed.map(r => r.q.id))].join(',')}">Redo the ${new Set(missed.map(r => r.q.id)).size} missed</button>` : ''}<button class="btn o" data-go="#/drill/${id}">Drill 10 more</button><button class="btn g" data-go="#/learn/${id}">Learn it</button><button class="btn g" data-go="#/video/${id}">▶ Video</button></div></section>
   <div class="cols" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr)">
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Accuracy over time</h2><div style="height:240px"><canvas id="k1"></canvas></div></section>
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">By difficulty</h2><div style="height:240px"><canvas id="k2"></canvas></div></section>
   </div>
   ${kl.length ? `<section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">By kind of question</h2><table class="rep"><thead><tr><th>Kind</th><th>Qs</th><th>Right</th><th>Score</th><th>Example</th></tr></thead><tbody>${kl.map(k => { const l = level(k.a, k.n); return `<tr><td><b>${esc(k.nm)}</b></td><td>${k.n}</td><td>${k.ok}</td><td><span class="pill" style="color:${l[1]};background:${l[2]}">${k.a}%</span></td><td style="font-size:13px;color:var(--mute)">${esc(plain(k.ex.q).slice(0, 90))}…</td></tr>` }).join('')}</tbody></table></section>` : ''}
   ${tl.length ? `<section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Traps he fell for</h2>${tl.map(([t, n]) => `<div style="display:flex;gap:10px;padding:6px 0;border-top:1px solid #f1f2f4"><span class="pill" style="background:#fde2e2;color:#b91c1c">${n}×</span>${esc(t)}</div>`).join('')}</section>` : ''}
   ${helpSection(id)}
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Every missed question <span style="font-size:13px;color:var(--mute);font-weight:500">click to see his answer, the right one, and how to do it</span></h2>${missed.length ? missed.map(missRow).join('') : '<div style="color:var(--mute)">No misses in this period.</div>'}</section>
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Right on the first try (${right.length})</h2>${right.slice(0, 30).map(r => `<div style="display:flex;gap:10px;padding:6px 0;border-top:1px solid #f1f2f4;font-size:14px"><span class="pill" style="background:#dcfce7;color:#15803d">✓</span><span style="color:var(--mute)">${new Date(r.ts).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} · ${DIFF[r.q.diff]} · ${mmss(r.sec)}</span>${esc(plain(r.q.q).slice(0, 110))}…</div>`).join('') || '<div style="color:var(--mute)">None yet.</div>'}</section>
  </div>`;
  window.scrollTo(0, 0);
  const tick = {font: {family: "'Helvetica Neue',Helvetica,Arial,sans-serif", size: 12}};
  chart('k1', {type: 'line', data: {labels: se.lab, datasets: [{label: 'Accuracy', data: se.acc, borderColor: SCOL[s.sec] || SCOL.Math, backgroundColor: SCOL[s.sec] || SCOL.Math, pointRadius: 5, tension: .3, spanGaps: true}, ...(base != null ? [{label: 'Blueprint before', data: se.lab.map(() => base), borderColor: '#111827', borderDash: [5, 5], pointRadius: 0}] : []), {label: 'Goal 75%', data: se.lab.map(() => 75), borderColor: '#64748B', borderDash: [6, 6], pointRadius: 0}]},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('k2', {type: 'bar', data: {labels: diff.map(d => ({E: 'Easy', M: 'Medium', H: 'Hard'})[d.k] + ` (${d.ok}/${d.n})`), datasets: [{label: 'Accuracy', data: diff.map(d => d.a), backgroundColor: diff.map(d => d.a == null ? '#e5e7eb' : d.a < 50 ? '#f87171' : d.a < 70 ? '#FB923C' : '#4ade80')}]},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {display: false}}}});
}
document.addEventListener('click', e => { const t = e.target.closest('[data-src]'); if (t) { const k = t.dataset.src; ST[k] = !ST[k]; if (!ST.bp && !ST.site) ST[k === 'bp' ? 'site' : 'bp'] = true; const h = decodeURIComponent(location.hash.slice(1)); const a = h.split('/')[2]; if (a && SK2[a]) skillStats(a); else drawStats(); return } const b = e.target.closest('[data-st]'); if (!b) return; const [k, v] = b.dataset.st.split(':'); ST[k] = v; const h = decodeURIComponent(location.hash.slice(1)); const a = h.split('/')[2]; if (a && SK2[a]) skillStats(a); else drawStats() });

function stRedraw() { const h = decodeURIComponent(location.hash.slice(1)); const a = h.split('/')[2]; if (a && SK2[a]) skillStats(a); else drawStats() }
document.addEventListener('change', e => {
  if (e.target.id === 'stper') { ST.period = e.target.value; if (ST.period === 'custom' && !ST.from) { const d = new Date(); d.setDate(d.getDate() - 13); ST.from = dkey(d); ST.to = dkey(new Date()) } stRedraw() }
  if (e.target.id === 'stfrom') { ST.from = e.target.value; stRedraw() }
  if (e.target.id === 'stto') { ST.to = e.target.value; stRedraw() }
});

// ---------- Scores: official SATs + where he is trending ----------
function superscore() { const bm = SAT_OFFICIAL.reduce((a, o) => o.Math > a.Math ? o : a), br = SAT_OFFICIAL.reduce((a, o) => o['R&W'] > a['R&W'] ? o : a); return {Math: bm.Math, 'R&W': br['R&W'], total: bm.Math + br['R&W'], mFrom: bm.label, rFrom: br.label} }
function scoreDays() { return [...new Set(LOG.filter(x => x.first).map(x => x.day))].sort() }
function scoresBlock() {
  const L = SAT_LAST(), t = new Date(); const tk = dkey(t), now = proj(tk), days = scoreDays(), prevD = days.filter(d => d < tk).pop(), prev = prevD ? proj(prevD) : null;
  const arrow = (a, b) => a > b ? `<span style="color:#15803d">▲ +${a - b}</span>` : a < b ? `<span style="color:#c2410c">▼ ${a - b}</span>` : '<span style="color:var(--mute)">±0</span>';
  const box = (lab, v, last, sub) => `<div class="card" style="padding:14px 16px;${lab === 'Combined' ? 'border:2px solid #1e3a8a' : ''}"><div style="font-size:13px;color:var(--mute);font-weight:600">${lab} (projected)</div>
    <div class="hd" style="font-size:${lab === 'Combined' ? 44 : 36}px;font-weight:800;line-height:1.1">${v}</div><div style="font-size:13px">${arrow(v, last)} vs. best superscore (${last})</div>${sub ? `<div style="font-size:13px;color:var(--mute)">${sub}</div>` : ''}</div>`;
  const SS = superscore(), offi = `<tr style="background:#f5f3ff"><td><b>Superscore</b><div style="font-size:12px;color:var(--mute)">best Math (${esc(SS.mFrom)}) + best R&W (${esc(SS.rFrom)})</div></td><td>${SS.Math}</td><td>${SS['R&W']}</td><td><b>${SS.total}</b></td><td>—</td></tr>` + SAT_OFFICIAL.slice().reverse().map(o => `<tr><td><b>${esc(o.label)}, ${o.date.slice(0, 4)}</b></td><td>${o.Math}</td><td>${o['R&W']}</td><td><b>${o.total}</b></td><td>${o.pct && o.pct.total ? o.pct.total + 'th' : '—'}</td></tr>`).join('');
  return `<div class="blks"><section class="card blk"><div class="blkh"><h2 class="hd">Projected SAT score</h2><span>As of right now · goal ${GOAL} on Dec 5 · ${now.total >= GOAL ? '<b style="color:#15803d">on target</b>' : `<b>${GOAL - now.total}</b> points to go`}${prev ? ` · since yesterday ${arrow(now.total, prev.total)}` : ''}</span></div>
   <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">${(() => { const B = superscore(); return box('Math', now.Math, B.Math) + box('Reading & Writing', now['R&W'], B['R&W']) + box('Combined', now.total, B.total, `Goal ${GOAL}`) })()}</div></section>
   ${(() => { const P = now.parts, row = (k, lab) => `<tr><td><b>${lab}</b></td><td>${P[k].off}</td><td>${P[k].prac} <span style="font-size:12px;color:var(--mute)">(${P[k].bp} Blueprint + ${P[k].sp} HELM questions)</span></td><td>${Math.round(100 * (1 - P[k].wp))}% / ${Math.round(100 * P[k].wp)}%</td><td><b>${P[k].val}</b></td></tr>`;
     return `<section class="card blk"><div class="blkh"><h2 class="hd">How the projection is built</h2><span>all the data: official SATs + Blueprint + HELM</span></div>
     <div style="overflow-x:auto"><table class="rep" style="width:100%"><thead><tr><th>Section</th><th>Official SATs (Nov 7 counts 50%, Oct 3 30%, Sep 12 20%)</th><th>Practice accuracy → score</th><th>Weight (official / practice)</th><th>Projected</th></tr></thead><tbody>${row('Math', 'Math')}${row('R&W', 'Reading & Writing')}</tbody></table></div></section>` })()}
   <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:16px;align-items:stretch">
    <section class="card blk"><div class="blkh"><h2 class="hd">Official SAT scores</h2><span>his real tests + superscore</span></div><table class="rep" style="width:100%"><thead><tr><th>Test</th><th>Math</th><th>R&W</th><th>Total</th><th>Percentile</th></tr></thead><tbody>${offi}</tbody></table></section>
    <section class="card blk"><div class="blkh"><h2 class="hd">Score trend</h2><span>official SATs, then the daily projection</span></div><div style="height:260px"><canvas id="c0"></canvas></div><div style="font-size:12px;color:var(--mute)">Dark bars = official SATs. Darkest = superscore (best Math + best R&W, the number many colleges look at). Light bars = HELM projection for that day. The dashed line is the trend through every point, carried to Dec 5.</div></section></div>
   ${winsBlock()}
   <section class="card blk"><div class="blkh"><h2 class="hd">College Board performance by domain</h2><span>score band for each part of the test · green = better than the last test, orange = lower</span></div>
   <div style="overflow-x:auto"><table class="rep" style="width:100%"><thead><tr><th>Domain</th>${SAT_OFFICIAL.map(o => `<th>${esc(o.label)}</th>`).join('')}</tr></thead><tbody>${SAT_DOM.map(([sec, k, nm]) => `<tr><td><b>${nm}</b> <span style="font-size:12px;color:var(--mute)">${sec}</span></td>${SAT_OFFICIAL.map((o, i) => { const v = o.dom[k], pv = i ? SAT_OFFICIAL[i - 1].dom[k] : null, lo = x => +String(x).split('–')[0]; const c = pv == null || lo(v) === lo(pv) ? '' : lo(v) > lo(pv) ? 'color:#15803d;font-weight:700' : 'color:#c2410c;font-weight:700'; return `<td style="${c}">${v}</td>` }).join('')}</tr>`).join('')}</tbody></table></div>
   <div style="font-size:12px;color:var(--mute);margin-top:8px">The projection is an estimate, not an official score. It blends all of his official SATs with his practice accuracy on every Blueprint and HELM question (first tries), with each category weighted by how often it shows up on the SAT. The more he practices, the more the practice side counts (up to 60%). The real test is adaptive, so read it as a direction.</div></section></div>`
}
function scoresChart() {
  // stacked bars: Math (blue) + Reading & Writing (orange) = total; dashed trendline fitted to every point and carried to test day
  const L = SAT_LAST(), days = scoreDays().filter(d => d > L.date);
  const pts = SAT_OFFICIAL.map(o => ({d: o.date, l: o.label + ' SAT', M: o.Math, R: o['R&W'], off: true})).concat(days.map(d => { const p = proj(d); return {d, l: new Date(d + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'}) + ' (proj.)', M: p.Math, R: p['R&W']} }));
  const TEST = '2026-12-05', x = d => (new Date(d + 'T12:00') - new Date(pts[0].d + 'T12:00')) / 864e5, n = pts.length;
  const xs = pts.map(p => x(p.d)), ys = pts.map(p => p.M + p.R), mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
  const sxx = xs.reduce((a, v) => a + (v - mx) ** 2, 0), slope = sxx ? xs.reduce((a, v, i) => a + (v - mx) * (ys[i] - my), 0) / sxx : 0, fit = v => Math.round(my + slope * (v - mx));
  const SS = superscore(), k = SAT_OFFICIAL.length;   // superscore bar goes right after the official tests; the trendline skips it
  pts.splice(k, 0, {l: 'Superscore', M: SS.Math, R: SS['R&W'], ss: true}); xs.splice(k, 0, null);
  const labels = pts.map(p => p.l).concat(['Dec 5 test (trend)']), trend = xs.map(v => v == null ? null : fit(v)).concat([fit(x(TEST))]);
  chart('c0', {data: {labels, datasets: [
    {type: 'bar', label: 'Math', data: pts.map(p => p.M).concat([null]), backgroundColor: pts.map(p => p.ss ? '#312E81' : p.off ? '#4F46E5' : '#A5B4FC').concat(['#000']), borderRadius: 4, stack: 's', order: 2},
    {type: 'bar', label: 'Reading & Writing', data: pts.map(p => p.R).concat([null]), backgroundColor: pts.map(p => p.ss ? '#0F766E' : p.off ? '#0D9488' : '#99F6E4').concat(['#000']), borderRadius: 4, stack: 's', order: 2},
    {type: 'line', label: `Trend (${slope >= 0 ? '+' : ''}${Math.round(slope * 7)} pts/week)`, data: trend, borderColor: (typeof BI !== 'undefined' && BI.dark) ? '#e2e8f0' : '#111827', borderDash: [6, 4], borderWidth: 2, pointRadius: trend.map((_, i) => i === trend.length - 1 ? 6 : 0), pointBackgroundColor: (typeof BI !== 'undefined' && BI.dark) ? '#e2e8f0' : '#111827', order: 0, stack: 'trend', spanGaps: true},
    {type: 'line', label: 'Goal ' + GOAL, data: labels.map(() => GOAL), borderColor: '#10B981', borderWidth: 2, borderDash: [2, 3], pointRadius: 0, order: 1, stack: 'goal'}]},
    options: {maintainAspectRatio: false, plugins: {legend: {position: 'bottom'}, tooltip: {callbacks: {footer: it => { const i = it[0].dataIndex; return i < pts.length ? 'Total: ' + (pts[i].M + pts[i].R) : '' }}}},
      scales: {x: {stacked: true}, y: {stacked: true, min: 0, suggestedMax: 1400, ticks: {callback: v => String(v)}, title: {display: true, text: 'SAT score'}}}}})
}

// ---------- When he used help: retries + help never count toward the score, they show whether the help works ----------
// Episode = the first day he saw a question. It "needed help" if his first answer was wrong or he opened help before answering.
// Tutor chats (Supabase tutor_messages) count as help even if he never answered again after asking (Allie, Nov 23)
let TUTOR_Q = null;
function loadTutorQ(redraw) { if (TUTOR_Q || !window.HELM_SB || loadTutorQ.busy) return; loadTutorQ.busy = 1;
  window.HELM_SB.from('tutor_messages').select('question_id,role,created_at').eq('role', 'student').limit(5000).then(({data}) => {
    TUTOR_Q = {}; (data || []).forEach(m => { if (m.question_id) (TUTOR_Q[m.question_id] = TUTOR_Q[m.question_id] || []).push(Date.parse(m.created_at)) }); if (redraw) redraw() }, () => { TUTOR_Q = {} }) }
function helpEpisodes(skillId) {
  if (typeof HELPN === 'object' && !HELPN.tutor) HELPN.tutor = 'Ask the tutor';
  const byQ = {};
  LOG.forEach(x => { const q = QBY[x.id]; if (!q || !SK2[q.skill]) return; if (skillId && q.skill !== skillId) return; if (!skillId && ST.sec !== 'all' && SK2[q.skill].sec !== ST.sec) return; (byQ[x.id] = byQ[x.id] || []).push(x) });
  const eps = [];
  Object.values(byQ).forEach(xs => {
    xs.sort((a, b) => a.ts - b.ts); const f = xs.find(x => (x.attempt || 1) === 1) || xs[0]; const day = xs.filter(x => x.day === f.day && x.ts >= f.ts);
    const tq = ((TUTOR_Q || {})[f.id] || []).filter(ts => new Date(ts).toLocaleDateString('en-CA') === f.day);
    const pre = realHelp([...(f.helpFirst || (f.coached ? ['show'] : [])), ...(tq.some(ts => ts < f.ts) ? ['tutor'] : [])]); const firstOk = !!f.ok && !pre.length;
    if (firstOk) return;  // clean first-try right: nothing to learn from here
    const used = realHelp([...new Set(day.flatMap(x => x.help || []).concat(pre, tq.length ? ['tutor'] : []))]);
    const okRow = day.find(x => x.ok); const q = QBY[f.id];
    eps.push({id: f.id, q, s: SK2[q.skill], day: f.day, ts: f.ts, end: okRow ? okRow.ts : day[day.length - 1].ts, wrongFirst: !f.ok, pre, used, solved: !!okRow, tries: day.length});
  });
  // Did it stick? The next NEW question of the same skill he answered under SAT rules, after fixing this one with help
  const scored = firstTries();
  eps.forEach(e => { if (!e.solved || !e.used.length) return; const n = scored.find(r => r.q.skill === e.q.skill && r.ts > e.end && r.id !== e.id); e.next = n ? !!n.ok : null; e.nextId = n ? n.id : null });
  return eps.sort((a, b) => a.ts - b.ts);
}
function helpSection(skillId, rg) {  // rg = [fromDay, toDay] from the BI dashboard; otherwise the Stats period
  const inRg = rows => rg ? rows.filter(r => r.day >= rg[0] && r.day <= rg[1]) : inPeriod(rows, ST.period);
  const eps = inRg(helpEpisodes(skillId)); if (!rg && !ST.site) return '';
  const head = `<h2 class="hd" style="margin:0 0 2px;font-size:19px">When he used help <span style="font-size:13px;color:var(--mute);font-weight:500">· not part of the score · shows whether the help is working</span></h2>`;
  if (!eps.length) return `<section class="card" style="padding:16px 18px">${head}<div style="color:var(--mute);margin-top:6px">No misses or help used in this period. Every question was answered on the first try with no help.</div></section>`;
  const withHelp = eps.filter(e => e.used.length), fixedHelp = withHelp.filter(e => e.solved), own = eps.filter(e => !e.used.length && e.solved);
  const pv = LOG.filter(x => x.chk && (x.attempt || 1) === 1 && QBY[x.id] && (skillId ? QBY[x.id].skill === skillId : (ST.sec === 'all' || SK2[QBY[x.id].skill].sec === ST.sec)));
  const pvR = inRg(pv), pvOk = pvR.filter(x => isScored(x) && x.ok);
  const stuck = eps.filter(e => !e.solved && e.used.length), stickN = eps.filter(e => e.next != null), stickOk = stickN.filter(e => e.next);
  const types = Object.keys(HELPN).map(k => { const es = eps.filter(e => e.used.includes(k)), sn = es.filter(e => e.next != null); return {k, n: es.length, fix: es.filter(e => e.solved).length, sn: sn.length, sok: sn.filter(e => e.next).length} }).filter(x => x.n).sort((a, b) => b.fix / b.n - a.fix / a.n || b.n - a.n);
  const rate = (a, b) => b ? Math.round(100 * a / b) + '%' : '—';
  const col = (a, b) => !b ? 'var(--ink)' : a / b < .5 ? '#b91c1c' : a / b < .7 ? '#b45309' : '#15803d';
  const best = types.filter(t => t.n >= 3)[0], worst = types.filter(t => t.n >= 3).slice(-1)[0];
  const tips = [];
  if (best) tips.push(`<b>${esc(HELPN[best.k])}</b> works best for him: he got ${best.fix} of ${best.n} right after using it. Point him there first when he's stuck.`);
  if (worst && best && worst.k !== best.k && worst.fix / worst.n < .6) tips.push(`<b>${esc(HELPN[worst.k])}</b> helps least (${worst.fix} of ${worst.n}).`);
  if (stickN.length >= 3) tips.push(stickOk.length / stickN.length >= .6 ? `It's sticking: after fixing a miss with help, he got the next new question right ${stickOk.length} of ${stickN.length} times.` : `Not sticking yet: after fixing a miss with help, he got the next new question right only ${stickOk.length} of ${stickN.length} times. He may be following the steps without owning them. Have him redo the miss later with no help.`);
  if (stuck.length) tips.push(`${stuck.length} question${stuck.length > 1 ? 's' : ''} he never got right, even with help. Go over these with him.`);
  if (!withHelp.length) tips.push('He has not opened any help on these yet. Encourage Show me how or the video after a miss.');
  const big = (lab, a, b, sub) => `<div><div style="font-size:13px;color:var(--mute)">${lab}</div><div class="hd" style="font-size:28px;font-weight:800;color:${col(a, b)}">${b ? Math.round(100 * a / b) + '%' : '—'}</div><div style="font-size:13px;color:var(--mute)">${sub}</div></div>`;
  const qline = e => `<div style="display:flex;gap:10px;align-items:center;padding:6px 0;border-top:1px solid #f1f2f4;font-size:14px;flex-wrap:wrap"><span class="pill" style="background:#fde2e2;color:#b91c1c">never right</span>${skillId ? '' : `<b>${esc(e.s.name)}</b>`}<span style="color:var(--mute)">${new Date(e.ts).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} · ${DIFF[e.q.diff]} · ${e.tries} tr${e.tries > 1 ? 'ies' : 'y'}${e.used.length ? ' · used ' + e.used.map(h => HELPN[h] || h).join(', ') : ' · no help opened'}</span><span style="flex:1;min-width:180px">${esc(plain(e.q.q).slice(0, 90))}${plain(e.q.q).length > 90 ? '…' : ''}</span><a href="#/look/${e.id}">Look at it</a></div>`;
  return `<section class="card" style="padding:16px 18px;border-left:6px solid #1e40af">${head}
   <div style="display:flex;gap:34px;flex-wrap:wrap;margin:12px 0 10px">
    ${big('Fix rate with help', fixedHelp.length, withHelp.length, `${fixedHelp.length} of ${withHelp.length} got right after help`)}
    ${big('Did it stick?', stickOk.length, stickN.length, `next new question right: ${stickOk.length} of ${stickN.length}`)}
    ${pvR.length ? big('Prove it questions', pvOk.length, pvR.length, `right with no help: ${pvOk.length} of ${pvR.length}`) : ''}
    <div><div style="font-size:13px;color:var(--mute)">Fixed on his own</div><div class="hd" style="font-size:28px;font-weight:800">${own.length}</div><div style="font-size:13px;color:var(--mute)">retried right, no help</div></div>
    <div><div style="font-size:13px;color:var(--mute)">Stuck</div><div class="hd" style="font-size:28px;font-weight:800;color:${stuck.length ? '#b91c1c' : '#15803d'}">${stuck.length}</div><div style="font-size:13px;color:var(--mute)">never right, even with help</div></div>
   </div>
   ${tips.length ? `<div class="box b-yel" style="margin:4px 0 12px"><div class="lab">What this tells you</div><ul style="margin:4px 0 0;padding-left:20px;display:grid;gap:4px">${tips.map(x => `<li>${x}</li>`).join('')}</ul></div>` : ''}
   ${types.length ? `<div style="overflow-x:auto"><table class="rep"><thead><tr><th>Help</th><th>Used on</th><th>Got it right after</th><th>Fix rate</th><th>Next new one right</th></tr></thead><tbody>${types.map(t => `<tr><td><b>${esc(HELPN[t.k] || t.k)}</b></td><td>${t.n} Qs</td><td>${t.fix}</td><td style="font-weight:700;color:${col(t.fix, t.n)}">${rate(t.fix, t.n)}</td><td>${t.sn ? `<b style="color:${col(t.sok, t.sn)}">${t.sok} of ${t.sn}</b>` : '<span style="color:var(--mute)">—</span>'}</td></tr>`).join('')}</tbody></table></div>` : ''}
   ${stuck.length ? `<h3 class="hd" style="margin:14px 0 4px;font-size:16px">Stuck: go over these with him</h3>${stuck.slice(-10).reverse().map(qline).join('')}${stuck.length > 1 ? `<div style="margin-top:10px"><button class="btn sm" data-go="#/drill/ids:${stuck.map(e => e.id).join(',')}">Redo the ${stuck.length} stuck questions</button></div>` : ''}` : ''}
   <div style="font-size:12px;color:var(--mute);margin-top:10px">Counts questions he missed on the first try or opened help on before answering. "Did it stick?" = after fixing one with help, was the next new question of that skill right on the first try with no help. "Prove it" = the 1–3 new questions of the same kind he gets right after fixing one with help. Desmos and the reference sheet are on the real SAT, so they don't count as help. Help tracking began mid-November, so older misses may show "no help opened."</div></section>`;
}

// ---------- Where the points are (Allie, Nov 23): per category, how many SAT questions, how many he's on track to get, and what each extra one is worth ----------
const SAT_QN = {Math: 44, English: 54};   // questions per section on the digital SAT
function winsData() {
  const now = proj(dkey(new Date()));
  const rows = Object.values(SK2).map(s => {
    const N = SAT_QN[s.sec], nq = Math.max(1, Math.round((s.share || 0) / 100 * N)), a = skAcc(s.id, dkey(new Date()));
    const acc = a == null ? null : a, right = acc == null ? null : Math.min(nq, Math.round(acc * nq)), ppq = 600 / N, miss = right == null ? nq : nq - right;
    const steps = []; for (let k = 1; k <= miss; k++) { const sec = s.sec === 'Math' ? 'Math' : 'R&W', cap = 800 - now[sec], g = Math.min(cap, Math.round(k * ppq)); steps.push({k, g, tot: Math.round((now.total + g) / 10) * 10}) }
    return {s, nq, acc, right, miss, ppq, steps, pts: steps.length ? steps[steps.length - 1].g : 0};
  }).filter(r => r.s.share).sort((a, b) => b.pts - a.pts || b.nq - a.nq);
  return {now, rows};
}
function winsBlock() {
  const {now, rows} = winsData(); if (!rows.length) return '';
  const top = rows.filter(r => r.pts > 0).slice(0, 3);
  const t3 = top.reduce((a, r) => a + r.pts, 0), t3Tot = Math.round((now.total + t3) / 10) * 10;
  const fmtPts = g => `<b style="color:#15803d">+${g}</b>`;
  const stepTxt = r => !r.steps.length ? '<span style="color:#15803d;font-weight:700">On track for all of them ✓ Keep it warm.</span>' :
    r.steps.slice(0, 4).map((x, i) => `${i === r.steps.length - 1 ? `all ${r.nq}` : `${x.k} more`} = ${fmtPts(x.g)} <span style="color:var(--mute)">(${x.tot})</span>`).join(' · ') +
    (r.steps.length > 4 ? ` · all ${r.nq} = ${fmtPts(r.pts)} <span style="color:var(--mute)">(${(Math.round((now.total + r.pts) / 10) * 10)})</span>` : '');
  const say = r => `The SAT will have about <b>${r.nq}</b> ${esc(r.s.name.toLowerCase())} question${r.nq > 1 ? 's' : ''}. At ${r.acc == null ? 'no data yet' : Math.round(100 * r.acc) + '%'}, you're on track to get <b>${r.right == null ? '?' : r.right} of ${r.nq}</b> right. ${r.steps.length ? `Get 1 more right and that's about <b>+${r.steps[0].g} points</b> (${r.steps[0].tot}). Get all ${r.nq} and it's <b>+${r.pts}</b> (${(Math.round((now.total + r.pts) / 10) * 10)}).` : 'You are already getting all of them.'}`;
  // Simple view (Allie, Nov 23): what each category is worth, what he got on the real SAT (estimated), what he gets in HELM, and what's still up for grabs
  const DOMK = {'Information & Ideas': 'ii', 'Craft & Structure': 'cs', 'Expression of Ideas': 'eoi', 'Grammar (Conventions)': 'sec', 'Advanced Math': 'adv', 'Algebra': 'alg', 'Geometry & Trig': 'geo', 'Problem-Solving & Data': 'psda'};
  const LS = SAT_LAST(), FTs = firstTries(), BESTS = r => satCatEst(r, 'best');
  const satEst = r => { const b = LS.dom[DOMK[r.s.dom]]; if (!b) return null; const [a, z] = String(b).split('–').map(Number), mid = (a + (z || a)) / 2; return Math.max(0, Math.min(r.nq, Math.round((mid - 200) / 600 * r.nq))) };
  const sideCol = (sec, lab) => {
    const ppq = 600 / SAT_QN[sec];
    const rs = rows.map(r => { const h = FTs.filter(x => x.q.skill === r.s.id), hr = h.length >= 3 ? Math.round(h.filter(x => x.ok).length / h.length * r.nq) : null, bs = BESTS(r), s = bs ? bs.n : null, sd = bs ? bs.d : '', now = hr != null ? hr : r.right;
      return {...r, worth: Math.round(r.nq * ppq), sat: s, satD: sd, helm: hr, hn: h.length, grab: Math.round((r.nq - (now || 0)) * ppq)} }).filter(r => r.s.sec === sec).sort((a, b) => b.grab - a.grab);
    const bar = (k, n, c) => `<span style="display:inline-block;width:90px;height:8px;border-radius:999px;background:#EEF0F3;overflow:hidden;vertical-align:middle"><i style="display:block;height:100%;width:${n ? Math.round(100 * k / n) : 0}%;background:${c};border-radius:999px"></i></span>`;
    const line = (lab2, k, r, c) => `<div style="display:grid;grid-template-columns:165px 96px minmax(0,1fr);gap:8px;align-items:center;font-size:14px;margin-top:4px;white-space:nowrap"><span style="color:var(--mute)">${lab2}</span>${k == null ? '<span></span><span style="color:var(--mute)">no data yet</span>' : `${bar(k, r.nq, c)}<span><b>${k} of ${r.nq}</b> right = <b>${Math.round(k * ppq)}</b> of ${r.worth} pts</span>`}</div>`;
    return `<div class="subcard">
     <div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px"><div style="font-size:17px;font-weight:700">${lab}</div><div style="font-size:13px;color:var(--mute)">${SAT_QN[sec]} questions · each one ≈ <b style="color:var(--ink)">${Math.round(ppq)} points</b></div></div>
     ${rs.map((r, i) => `<a href="#/stats/${r.s.id}" style="display:block;padding:12px 0;border-bottom:1px solid var(--line2);text-decoration:none;color:var(--ink)">
       <div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px"><div><b style="font-size:15px">${esc(r.s.name)}</b> <span class="fp-meta">· <b>${Math.round(r.s.share || 0)}%</b> of SAT ${sec === 'Math' ? 'Math' : 'R&W'} · <b>${r.nq}</b> question${r.nq > 1 ? 's' : ''} · <b>≈ ${r.worth}</b> of 800 points</span></div>
        <div style="text-align:right;white-space:nowrap">${r.steps.length ? '' : '<span style="color:#047857;font-weight:700">✓ getting them all</span>'}</div></div>
       ${line(`Best SAT (${esc(r.satD || LS.label)}, est.)`, r.sat, r, '#A1A1AA')}${r.helm != null ? line('HELM now', r.helm, r, '#2563EB') : line('Practice now', r.right, r, '#2563EB')}
       ${(() => { const SSx = superscore(), b = r.sat != null ? r.sat : (r.right || 0), left = r.nq - b; if (left <= 0) return '<div class="mv"><span class="mvl">He got all of these on his best SAT. Keep them.</span></div>';
         const st = Array.from({length: Math.min(3, left)}, (_, i) => i + 1); const chip = (k, lab) => `<span class="mvc"><b>${lab}</b> → <b class="t">${Math.round(SSx.total + k * ppq)}</b> <span>+${Math.round(k * ppq)}</span></span>`;
         return `<div class="mv"><span class="mvl">Right answers beyond his SAT (${b} of ${r.nq}) lift his best SAT <b>${SSx.total}</b> to:</span>${st.map(k => chip(k, k + ' more')).join('')}${left > 3 ? chip(left, 'all ' + r.nq) : ''}</div>` })()}</a>`).join('')}
    </div>` };
  return `<section class="card blk"><div class="blkh"><h2 class="hd">Where the points are</h2><span>For each category: how many SAT questions it has, how he did on his best SAT, how he does in HELM now, and what his superscore becomes if he gets 1, 2 or 3 more of them right · biggest wins first</span></div>
   <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:16px">${sideCol('Math', 'Math')}${sideCol('English', 'Reading & Writing')}</div>
   <div style="font-size:12px;color:var(--mute);margin-top:8px">“SAT, est.”: the College Board report only gives a score range for each part of the test (like Advanced Math), not a count per category, so this is estimated from his best College Board score range for the part each category belongs to. “HELM now”: his first-try accuracy in HELM (no help) applied to that category's questions on the SAT; shown once he has 3+ questions; until then “Practice now” uses HELM + Blueprint together. “1 more → 1060 (+14)” = his new superscore if he gets one more question in that category right than he did on his best SAT. Each extra Math question ≈ +14 points, each Reading & Writing question ≈ +11.</div>
   <details style="margin-top:12px"><summary style="cursor:pointer;font-size:14px;font-weight:600;color:var(--blue)">See the full breakdown: every category, step by step</summary><div style="margin-top:10px">
   <h3 class="hd" style="margin:16px 0 6px;font-size:16px">Step by step <span style="font-size:13px;color:var(--mute);font-weight:500">biggest wins first · each extra Math question ≈ +${Math.round(600 / 44)} points, each Reading &amp; Writing question ≈ +${Math.round(600 / 54)}</span></h3>
   ${top.length ? `<div class="box b-yel" style="margin-bottom:10px"><div class="lab">Your biggest wins, Patrick</div><ul style="margin:6px 0 0;padding-left:20px;display:grid;gap:6px;font-size:15px;line-height:1.5">${top.map(r => `<li><b>${esc(r.s.name)}:</b> ${say(r)}</li>`).join('')}</ul>
    <div style="margin-top:8px;font-size:15px">Master all three and your projected score goes from <b>${now.total}</b> to about <b style="color:#15803d">${t3Tot}</b>${t3Tot >= GOAL ? ` · that's your ${GOAL} goal ✓` : ` · ${GOAL - t3Tot} short of ${GOAL}, so add the next ones on the list`}.</div></div>` : ''}
   ${(() => {
     const DOMK = {'Information & Ideas': 'ii', 'Craft & Structure': 'cs', 'Expression of Ideas': 'eoi', 'Grammar (Conventions)': 'sec', 'Advanced Math': 'adv', 'Algebra': 'alg', 'Geometry & Trig': 'geo', 'Problem-Solving & Data': 'psda'};
     const lo = b => +String(b || '0').split('–')[0], FT = firstTries(), r10 = v => Math.round(v / 10) * 10, SS = superscore();
     const bestDom = dom => { const k = DOMK[dom]; if (!k) return null; let best = null; SAT_OFFICIAL.forEach(o => { const v = o.dom[k]; if (v && (!best || lo(v) > lo(best.v))) best = {v, d: o.label} }); return best ? {...best, last: SAT_LAST().dom[k]} : null };
     const sc = (r, g) => { const k = r.s.sec === 'Math' ? 'Math' : 'R&W', s = Math.min(800, r10(now[k] + g)); return `<div style="font-size:16px;font-weight:700;color:#047857">+${g} pts</div><div style="font-size:13px;color:var(--ink);white-space:nowrap">${k} <b>${s}</b> · Total <b>${r10(now.total + g)}</b></div>` };
     const pc = (ok, n) => n ? `<b>${Math.round(100 * ok / n)}%</b> <span style="color:var(--mute);font-size:12px">${ok}/${n}</span>` : '<span style="color:var(--mute)">—</span>';
     const head = (sec, lab) => { const k = sec === 'Math' ? 'Math' : 'R&W'; return `<tr><td colspan="8" style="background:#F4F4F5!important;padding:12px!important;border-top:2px solid #D4D4D8!important"><span style="font-size:16px;font-weight:700">${lab}</span> <span style="font-size:13px;color:var(--mute);margin-left:10px">best official SAT <b style="color:var(--ink)">${SS[k]}</b> (${esc(sec === 'Math' ? SS.mFrom : SS.rFrom)}) · last SAT <b style="color:var(--ink)">${SAT_LAST()[k]}</b> · projected now <b style="color:var(--ink)">${now[k]}</b> · total now <b style="color:var(--ink)">${now.total}</b></span></td></tr>` };
     const row = r => { const h = FT.filter(x => x.q.skill === r.s.id), hok = h.filter(x => x.ok).length, b = BPS[r.s.id] || {n: 0, ok: 0}, bd = bestDom(r.s.dom);
       return `<tr><td><a href="#/stats/${r.s.id}" style="color:var(--ink);text-decoration:none"><b style="font-size:15px">${esc(r.s.name)}</b></a><div style="font-size:12px;color:var(--mute)">${Math.round(r.s.share || 0)}% of section · ${r.nq} questions · ≈ ${Math.round(r.nq * 600 / SAT_QN[r.s.sec])} of 800 pts</div></td>
        <td>${bd ? `<b>${bd.v}</b> <span style="color:var(--mute);font-size:12px">best (${bd.d})</span><div style="font-size:12px;color:var(--mute)">${esc(r.s.dom)} · last ${bd.last}</div>` : '—'}</td>
        <td>${pc(hok, h.length)}</td><td>${pc(b.ok, b.n)}</td>
        <td><b style="font-size:15px">${r.right == null ? '?' : r.right} of ${r.nq}</b><div style="font-size:12px;color:var(--mute)">${r.acc == null ? 'no data yet' : Math.round(100 * r.acc) + '% combined'}</div></td>
        <td>${r.pts ? `<b style="font-size:15px;color:#047857">+${r.pts}</b>` : '<span style="color:#047857;font-weight:700">✓ all</span>'}</td>
        <td>${r.steps.length ? sc(r, r.steps[0].g) : '—'}</td><td>${r.steps.length > 1 ? sc(r, r.pts) : r.steps.length ? '<span style="color:var(--mute);font-size:13px">same as +1</span>' : '—'}</td></tr>` };
     const grp = sec => rows.filter(r => r.s.sec === sec).sort((a, b) => b.pts - a.pts).map(row).join('');
     return `<div style="overflow-x:auto"><table class="rep" style="width:100%;font-size:14px"><thead><tr><th>Category</th><th>Official SAT (domain band)</th><th>HELM (first try)</th><th>Blueprint</th><th>On track on the SAT</th><th>Points left</th><th>Get 1 more right</th><th>Get all of them right</th></tr></thead>
      <tbody>${head('Math', 'Math')}${grp('Math')}${head('English', 'Reading & Writing')}${grp('English')}</tbody></table></div>
      <div style="font-size:12px;color:var(--mute);margin-top:6px">College Board score reports only give a score band for each domain (like Advanced Math), not for each category, so "Official SAT" shows the domain that category belongs to: his best band and his latest one. "Get 1 more / all right" adds those points to today's projection and shows the new section score and total.</div>`
   })()}
   <div style="font-size:12px;color:var(--mute);margin-top:6px">Rough guide, not an official score. Question counts = the category's share of the section × ${SAT_QN.Math} Math or ${SAT_QN.English} R&amp;W questions. Accuracy = Blueprint + HELM first tries (no help). Points ≈ 600 ÷ questions in the section, added to today's projection (${now.total}); totals rounded to the nearest 10 like real SAT scores. The real SAT is adaptive and scaled, so the exact points can move a little.</div></div></details></section>`;
}

// ---------- Easiest wins first (Allie, Nov 23): not enough time to master everything, so rank by points he can REALISTICALLY add × how close he already is ----------
function quickWins() {
  const {now, rows} = winsData(), FT = firstTries(), days = Math.max(0, Math.round((new Date(TEST + 'T08:00') - new Date()) / 864e5));
  const out = rows.filter(r => r.steps.length).map(r => {
    const id = r.s.id, acc = r.acc == null ? .4 : r.acc, b = BPS[id] || {n: 0, ok: 0}, bp = b.n ? b.ok / b.n : null;
    const h = FT.filter(x => x.q.skill === id), hr = h.slice(-10), hAcc = hr.length >= 4 ? hr.filter(x => x.ok).length / hr.length : null;
    const eps = helpEpisodes(id).filter(e => e.used.length), fix = eps.length >= 3 ? eps.filter(e => e.solved).length / eps.length : null;
    const st = eps.filter(e => e.next != null), stick = st.length >= 2 ? st.filter(e => e.next).length / st.length : null;
    const easy = h.filter(x => x.q.diff === 'E'), easyAcc = easy.length >= 2 ? easy.filter(x => x.ok).length / easy.length : null;
    const goal = Math.max(1, Math.min(r.miss, Math.round(.8 * r.nq) - (r.right || 0)));   // realistic: up to ~80% of these questions
    const gain = r.steps[goal - 1].g;
    let ease = acc, why = [];
    if (acc >= .5) why.push(`he already gets about ${Math.round(100 * acc)}% right, so ${goal === 1 ? 'one more question' : goal + ' more questions'} per test is close`);
    else if (acc < .35) { ease -= .1; why.push(`only ${Math.round(100 * acc)}% right so far, so the basics need work first`) }
    else why.push(`he gets about ${Math.round(100 * acc)}% right now, so ${goal} more per test is a stretch but doable`);
    if (hAcc != null && bp != null && hAcc - bp >= .1) { ease += .1; why.push(`he's improving: last ${hr.length} on HELM ${Math.round(100 * hAcc)}% vs Blueprint ${Math.round(100 * bp)}%`) }
    if (hAcc != null && bp != null && bp - hAcc >= .15) { ease -= .05; why.push(`slipping lately: last ${hr.length} on HELM ${Math.round(100 * hAcc)}% vs Blueprint ${Math.round(100 * bp)}%`) }
    if (fix != null && fix >= .7) { ease += .08; why.push(`help works here: he fixed ${eps.filter(e => e.solved).length} of ${eps.length} after using it`) }
    if (stick != null && stick >= .6) { ease += .07; why.push('and it sticks on the next new question') }
    if (stick != null && stick < .4) { ease -= .05; why.push('but it is not sticking yet on new questions') }
    if (easyAcc != null && easyAcc >= .75 && acc < .7) { ease += .05; why.push('he gets the easy ones, so it is the medium/hard versions that cost him') }
    if (r.nq >= 5) why.unshift(`big category: about ${r.nq} questions on the test`);
    if (r.nq <= 2) why.push(`only about ${r.nq} on the test, so less payoff`);
    ease = Math.max(.05, Math.min(1, ease));
    return {...r, goal, gain, ease, score: gain * ease * ease, why, tot: Math.round((now.total + gain) / 10) * 10};
  }).sort((a, b) => b.score - a.score);
  return {now, days, list: out};
}
function quickWinsBlock() {
  const {now, days, list} = quickWins(); if (!list.length) return '';
  const pick = list.slice(0, 4), park = list.filter(r => !pick.includes(r) && (r.ease < .4 || r.nq <= 1)).sort((a, b) => a.score - b.score).slice(0, 4);
  const sum = pick.reduce((a, r) => a + r.gain, 0), tot = Math.round((now.total + sum) / 10) * 10;
  const lab = e => e >= .55 ? ['Close', '#15803d', '#dcfce7'] : e >= .4 ? ['Within reach', '#1e40af', '#e8efff'] : ['Stretch', '#9a3412', '#fff1e6'];
  return `<section class="card blk"><div class="blkh"><h2 class="hd">Easiest wins first</h2><span>${days} days to the test · he can't master everything, so start where he's closest and it's worth the most</span></div>
   <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px">
   ${pick.map((r, i) => { const l = lab(r.ease); return `<div class="card" style="padding:12px 14px;border-top:4px solid ${l[1]}"><div style="display:flex;justify-content:space-between;align-items:center;gap:6px"><span style="font-size:13px;color:var(--mute);font-weight:700">#${i + 1}</span><span class="pill" style="color:${l[1]};background:${l[2]}">${l[0]}</span></div>
     <div class="hd" style="font-size:17px;font-weight:700;margin:4px 0">${esc(r.s.name)}</div>
     <div style="font-size:14px">Now <b>${r.right == null ? '?' : r.right} of ${r.nq}</b> → aim for <b>${(r.right || 0) + r.goal} of ${r.nq}</b> = <b style="color:#15803d">+${r.gain} points</b></div>
     <ul style="margin:6px 0 8px;padding-left:18px;font-size:13px;color:var(--ink);display:grid;gap:2px">${r.why.slice(0, 4).map(w => `<li>${esc(w[0].toUpperCase() + w.slice(1))}</li>`).join('')}</ul>
     <div style="display:flex;gap:6px"><button class="btn sm" data-go="#/learn/${r.s.id}">Learn it</button><button class="btn sm o" data-go="#/drill/${r.s.id}">Drill</button></div></div>` }).join('')}</div>
   <div class="box b-yel" style="margin-top:10px"><div class="lab">The plan</div><div class="c" style="font-size:15px">Focus on these ${pick.length} first. Hitting those targets is worth about <b style="color:#15803d">+${sum} points</b>, taking his projection from <b>${now.total}</b> to about <b>${tot}</b>${tot >= GOAL ? ` (the ${GOAL} goal ✓)` : ''}. ${days >= 8 ? 'With ' + days + ' days left: two per day, Learn it then Drill, and use the review days to come back to them.' : 'With only ' + days + ' days left, stay on these and skip new topics.'}${park.length ? `<br><span style="color:var(--mute)">Leave for later: ${park.map(r => esc(r.s.name)).join(', ')} (harder for him right now or very few questions on the test).</span>` : ''}</div></div>
   <div style="font-size:12px;color:var(--mute);margin-top:6px">How this is ranked: realistic points (getting to about 80% of that category's questions) × how close he is. "Close" counts his accuracy, whether his recent HELM work is above his Blueprint, whether help fixes his misses there and sticks on the next new question, and whether he already gets the easy versions. It updates every time he practices.</div></section>`;
}

// Estimated right answers on an official SAT for a category, from the College Board score band of its domain (reports give no per-category counts)
const DOMK2 = {'Information & Ideas': 'ii', 'Craft & Structure': 'cs', 'Expression of Ideas': 'eoi', 'Grammar (Conventions)': 'sec', 'Advanced Math': 'adv', 'Algebra': 'alg', 'Geometry & Trig': 'geo', 'Problem-Solving & Data': 'psda'};
function satCatEst(r, which) {  // which: 'best' | 'last'
  const k = DOMK2[r.s.dom]; if (!k) return null; const lo = b => +String(b || '0').split('–')[0];
  const tests = which === 'last' ? [SAT_LAST()] : SAT_OFFICIAL.slice(); let best = null; tests.forEach(o => { const v = o.dom[k]; if (v && (!best || lo(v) > lo(best.v))) best = {v, d: o.label} });
  if (!best) return null; const [a, z] = String(best.v).split('–').map(Number), mid = (a + (z || a)) / 2;
  return {n: Math.max(0, Math.min(r.nq, Math.round((mid - 200) / 600 * r.nq))), d: best.d, band: best.v} }
// ---------- Plan to 1300 (Allie, Nov 23): master 8 categories, nothing else ----------
function focusPlanBlock(compact) {
  // Baseline = his best official SAT (superscore: best Math + best R&W). Every lift starts from what he got on his best SAT in that category (Allie, Nov 23).
  const F = PLAN && PLAN.focus ? PLAN.focus.skills : ['nlf', 'linf', 'nleq', 'lin2', 'bound', 'fss', 'trans', 'syn'];
  const {now, rows} = winsData(), SS = superscore(), r10 = v => Math.round(v);
  const fr = F.map(id => rows.find(r => r.s.id === id)).filter(Boolean).map(r => { const B = satCatEst(r, 'best'), base = B ? B.n : (r.right || 0), ppq = 600 / SAT_QN[r.s.sec];
    const goal = Math.min(r.nq, Math.max(base + 1, r.nq <= 3 ? r.nq : Math.round(.8 * r.nq)));
    return {...r, B, base, ppq, goal, gGoal: Math.round((goal - base) * ppq), gAll: Math.round((r.nq - base) * ppq)} });
  const secBest = sec => sec === 'Math' ? SS.Math : SS['R&W'];
  const secTo = (sec, key) => Math.min(800, r10(secBest(sec) + fr.filter(r => r.s.sec === sec).reduce((a, r) => a + r[key], 0)));
  const totGoal = secTo('Math', 'gGoal') + secTo('English', 'gGoal'), totAll = secTo('Math', 'gAll') + secTo('English', 'gAll'), nQ = fr.reduce((a, r) => a + r.nq, 0);
  const days = Math.max(0, Math.round((new Date(TEST + 'T08:00') - new Date()) / 864e5));
  const when = id => (PLAN && PLAN.days || []).filter(d => d.date >= dkey(new Date()) && (d.learn || []).includes(id)).map(d => new Date(d.date + 'T12:00').toLocaleDateString('en-US', {weekday: 'short', month: 'short', day: 'numeric'}));
  const WHY = {nlf: 'Biggest Math category; Desmos graphing solves many', linf: 'Slope and intercept rules: same few patterns every time', nleq: 'Desmos: graph both sides, read the intersection', lin2: 'Desmos or one rule: plug in the point',
    bound: 'Punctuation rules: learn them once, apply every time', fss: 'Grammar rules (verb, pronoun, agreement): pure rules', trans: 'Logic words: same-direction vs. opposite-direction', syn: 'Strategy: read the goal, pick the choice that does exactly it'};
  const CATC = ['#7C3AED', '#EA580C', '#DB2777', '#0891B2', '#92400E', '#C026D3', '#9F1239', '#334155'];   // identity colors (never blue/green: those mean goal/master)
  const pct = v => Math.max(0, Math.min(100, (v - 400) / (1600 - 400) * 100));
  const big = (lab, v, sub, c) => `<div class="fp-k"><div class="fp-kl">${lab}</div><div class="fp-kv" style="color:${c}">${v}</div><div class="fp-ks">${sub}</div></div>`;
  const col = (sec, lab) => { const rs = fr.filter(r => r.s.sec === sec), b = secBest(sec);
    return `<div class="fp-col"><div class="fp-ch"><div><div class="fp-ct">${lab}</div><div class="fp-cs">${rs.length} focus categories · best SAT ${b} (${esc(sec === 'Math' ? SS.mFrom : SS.rFrom)})</div></div>
      <div style="text-align:right"><div class="fp-big">${b} <span style="color:#A1A1AA;font-weight:500">→</span> <span style="color:#1D4ED8">${secTo(sec, 'gGoal')}</span> <span style="color:#A1A1AA;font-weight:500">→</span> <span style="color:#047857">${secTo(sec, 'gAll')}</span></div><div class="fp-cs">best SAT → <b style="color:#1D4ED8">at goal</b> → <b style="color:#047857">mastered</b></div></div></div>
     ${rs.map(r => { const w = when(r.s.id), n = r.right || 0, ci = F.indexOf(r.s.id), cc = CATC[ci % CATC.length];
       return `<a href="#/stats/${r.s.id}" class="fp-row" style="--cc:${cc}">
       <div class="fp-rt"><span class="fp-rn"><span class="fp-badge">${ci + 1}</span>${esc(r.s.name)}</span><span class="fp-meta"><b>${Math.round(r.s.share || 0)}%</b> of SAT ${sec === 'Math' ? 'Math' : 'R&W'} · <b>${r.nq}</b> questions · <b>≈ ${Math.round(r.nq * r.ppq)}</b> of 800 points · each ≈ ${Math.round(r.ppq)}</span></div>
       <div class="fp-bar"><i style="width:${100 * n / r.nq}%"></i><u style="left:${100 * r.base / r.nq}%" title="Best SAT (est.)"></u><s style="left:${100 * r.goal / r.nq}%"></s><em style="left:100%"></em></div>
       <div class="fp-cnt"><span><i class="k0"></i>Best SAT${r.B ? ` (${esc(r.B.d)}, est.)` : ''}: <b>${r.base} of ${r.nq}</b></span><span><i class="k1"></i>HELM/practice now: <b>${n} of ${r.nq}</b></span><span class="gl"><i class="k2"></i>Goal: <b>${r.goal} of ${r.nq}</b></span><span class="ms"><i class="k3"></i>Master: <b>${r.nq} of ${r.nq}</b></span></div>
       <div class="fp-lift"><div><span class="lb">Lift over his best SAT (${SS.total})</span><span class="gl">goal <b>+${r.gGoal}</b> → ${r10(SS.total + r.gGoal)}</span><span class="ms">master <b>+${r.gAll}</b> → ${r10(SS.total + r.gAll)}</span></div></div>
       <div class="fp-why">${esc(WHY[r.s.id] || '')}</div>
       ${w.length && !compact ? `<div class="fp-when">${w.map(x => `<span>${x}</span>`).join('')}<span class="rv">+ daily review</span></div>` : ''}</a>` }).join('')}</div>` };
  return `<section class="card blk fp"><div class="blkh"><h2 class="hd">Plan to ${GOAL}: master these 8, nothing else</h2><span>${days} days left · ${nQ} of 98 SAT questions (about half the test) · every daily set drills only these · all lifts start from his best SAT</span></div>
   <div class="fp-ks3">${big('Best SAT (superscore)', SS.total, `Math ${SS.Math} (${esc(SS.mFrom)}) + R&W ${SS['R&W']} (${esc(SS.rFrom)}) · projected today ${now.total}`, 'var(--ink)')}${big('Hit the goal on all 8', totGoal, `<span class="fp-up" style="background:#DBEAFE;color:#1D4ED8">+${totGoal - SS.total} over best SAT</span> about 80% right`, '#1D4ED8')}${big('Master all 8', totAll, `<span class="fp-up">+${totAll - SS.total} over best SAT</span> every question right`, '#047857')}</div>
   <div class="fp-track"><div class="fp-tb"><i style="width:${pct(SS.total)}%"></i><b style="left:${pct(totGoal)}%"></b><b style="left:${pct(totAll)}%;background:#047857"></b><em style="left:${pct(GOAL)}%"></em></div>
    <div class="fp-tl2"><span><i style="background:#2563EB"></i>Best SAT <b>${SS.total}</b></span><span class="gl"><i style="background:#1D4ED8;width:4px;height:16px;border-radius:2px"></i>Goal on all 8 <b>${totGoal}</b></span><span class="ms"><i style="background:#047857;width:4px;height:16px;border-radius:2px"></i>Master all 8 <b>${totAll}</b></span><span><i style="border-left:2px dashed #047857;width:0;height:16px;border-radius:0"></i>Target <b>${GOAL}</b></span><span style="color:var(--mute)">scale 400–1600</span></div></div>
   <div class="fp-cols">${col('Math', 'Math')}${col('English', 'Reading & Writing')}</div>
   ${compact ? '' : `<div class="box b-yel" style="margin-top:16px"><div class="lab">How he works it every day</div><div class="c" style="font-size:15px"><b>1.</b> Learn it (5 min) for the day's skills → <b>2.</b> Drill: first try with no help. Desmos and the reference sheet are allowed, like on the SAT → <b>3.</b> After any miss: Show me how, then <b>Prove it</b> (2 new ones right in a row) → <b>4.</b> Daily review: every focus skill, his weakest ones get more. A skill is "mastered" at 80% on the first try over 10+ questions.</div></div>
   <div style="font-size:13px;color:var(--mute);margin-top:8px">Baseline = his superscore (best Math + best Reading & Writing across all his official SATs). "Best SAT" per category is estimated from the College Board score range for that part of the test on his best test (reports don't give a count per category). Each extra right answer ≈ +14 points in Math, +11 in Reading & Writing; section scores cap at 800. Why these 8: most questions on the test × how close he already is × how fast they can be learned. Words in context is left out on purpose: vocabulary doesn't move much in ${days} days.</div>`}</section>`;
}

// ---------- Path to 1300 (Allie, Nov 23): one plain instruction per row, running score from his best SAT ----------
function pathSteps() {
  const F = PLAN && PLAN.focus ? PLAN.focus.skills : ['nlf', 'linf', 'nleq', 'lin2', 'bound', 'fss', 'trans', 'syn'];
  const EXTRA = ['inf', 'coe', 'wic'].filter(id => SK2[id] && !F.includes(id));
  const {rows} = winsData(), SS = superscore(), FT = firstTries();
  const cat = id => { const r = rows.find(x => x.s.id === id); if (!r) return null; const B = satCatEst(r, 'best'), base = B ? B.n : (r.right || 0), ppq = 600 / SAT_QN[r.s.sec];
    const goal = Math.min(r.nq, Math.max(base + 1, r.nq <= 3 ? r.nq : Math.round(.8 * r.nq))); return {r, base, ppq, goal} };
  const steps = []; const add = (c, from, to, phase) => { if (!c || to <= from) return; steps.push({c, from, to, n: to - from, pts: Math.round((to - from) * c.ppq), phase}) };
  const fc = F.map(cat).filter(Boolean);
  fc.slice().sort((a, b) => (b.goal - b.base) * b.ppq - (a.goal - a.base) * a.ppq).forEach(c => add(c, c.base, c.goal, 'goal'));
  fc.slice().sort((a, b) => b.ppq - a.ppq).forEach(c => add(c, c.goal, c.r.nq, 'master'));
  EXTRA.map(cat).filter(Boolean).forEach(c => add(c, c.base, c.r.nq, 'extra'));
  // running score with section caps, stop once past the goal
  let m = SS.Math, e = SS['R&W']; const out = [];
  for (let s of steps) { if (m + e >= GOAL) break; const before = m + e;
    if (before + s.pts > GOAL && s.n > 1) { const k = Math.max(1, Math.ceil((GOAL - before) / s.c.ppq)); if (k < s.n) s = {...s, n: k, to: s.from + k, pts: Math.round(k * s.c.ppq)} }
    if (s.c.r.s.sec === 'Math') m = Math.min(800, m + s.pts); else e = Math.min(800, e + s.pts);
    // in HELM, is he already getting that many right? (6+ first tries in this skill)
    const h = FT.filter(x => x.q.skill === s.c.r.s.id), hn = h.length, hacc = hn ? h.filter(x => x.ok).length / hn : 0;
    out.push({...s, gain: m + e - before, score: m + e, m, e, done: hn >= 6 && Math.round(hacc * s.c.r.nq) >= s.to, hn, hacc}) }
  return {SS, steps: out};
}
function pathBlock(withDetails) {
  const {SS, steps} = pathSteps(); if (!steps.length) return '';
  const last = steps[steps.length - 1].score, need = GOAL - SS.total;
  const row = (s, i) => { const nm = esc(s.c.r.s.name), reach = s.score >= GOAL;
    return `<tr class="${s.done ? 'dn' : ''} ${reach ? 'hit' : ''}"><td class="pn">${s.done ? '✓' : i + 1}</td>
     <td class="pd"><b>Get ${s.n} more ${nm} right</b><div>${s.phase === 'master' ? `all ${s.to} of ${s.c.r.nq} (finishing this category)` : `${s.to} of ${s.c.r.nq} right · his best SAT: ${s.from} of ${s.c.r.nq}`}${s.phase === 'extra' ? ' · extra category to close the gap' : ''}${s.done ? ' · <span class="ok">already doing this in HELM</span>' : ''}</div></td>
     <td class="pp">+${s.gain}</td><td class="ps">${s.score}${reach ? ' ✓' : ''}<div class="psec">Math ${s.m} · R&amp;W ${s.e}</div></td>
     <td class="pb"><a class="btn sm ${s.done ? 'g' : ''}" href="#/drill/${s.c.r.s.id}">Practice</a></td></tr>` };
  return `<section class="card blk path"><div class="blkh"><h2 class="hd">Your path to ${GOAL}</h2><span>Start from your best SAT. Each row is one thing to do on test day. Work top to bottom.</span></div>
   <div class="ph"><div><span>Best SAT</span><b>${SS.total}</b></div><div><span>Goal</span><b>${GOAL}</b></div><div><span>Points needed</span><b class="g">+${need}</b></div></div>
   <table class="pt"><thead><tr><th></th><th>On test day…</th><th>Points</th><th>Your score (Math + R&amp;W)</th><th></th></tr></thead><tbody>${steps.map(row).join('')}</tbody></table>
   ${last < GOAL ? `<div class="pnote">These steps reach about <b>${last}</b>. The rest comes from small categories not listed here.</div>` : ''}
   <div class="pnote">Each extra right answer is worth about 14 points in Math and 11 in Reading &amp; Writing; exact points shown; the real SAT rounds scores to the nearest 10. ✓ = HELM shows he's already getting that many right (6+ practice questions).${withDetails ? '' : ' Details on the <a href="#/stats">Stats page</a>.'}</div>
   ${withDetails ? `<details class="pdet"><summary>How we figured this out</summary><div style="margin-top:12px">${focusPlanBlock(false)}</div></details>` : ''}</section>`;
}
