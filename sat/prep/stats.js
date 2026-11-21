/* ---------- STATS: BI dashboard (#/stats, #/stats/<skill>, #/stats/sec:Math) ---------- */
const ST = {period: 'day', from: '', to: '', sec: 'all', bp: true, site: true};
const SITE_NAME = 'HELM';
const SCOL = {Math: '#1e3a8a', English: '#0f766e'};
let CH = [];
function dkey(d) { return d.toLocaleDateString('en-CA') }
function firstTries() {  // one row per question per day: the first attempt that day
  const seen = {}, out = [];
  LOG.forEach(x => { const q = QBY[x.id]; if (!q || !SK2[q.skill]) return; if ((x.attempt || 1) !== 1) return; const k = x.id + '|' + x.day; if (seen[k]) return; seen[k] = 1; out.push(Object.assign({q, s: SK2[q.skill]}, x)) });
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
function ensureChartJs(cb) { if (typeof Chart !== 'undefined') return cb(); const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js'; s.onload = cb; s.onerror = cb; document.head.appendChild(s) }
function filters() {
  const b = (k, v, t) => `<button class="btn sm ${ST[k] === v ? '' : 'g'}" data-st="${k}:${v}">${t}</button>`;
  return `<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center"><div style="display:flex;gap:6px;align-items:center"><span style="font-size:13px;color:var(--mute);font-weight:600">PERIOD</span><select id="stper" style="font:inherit;font-weight:600;padding:8px 10px;border:1px solid #d1d5db;border-radius:10px;background:#fff">${[['day', 'Today'], ['7', 'Last 7 days'], ['14', 'Last 14 days'], ['30', 'Last 30 days'], ['all', 'All time'], ['custom', 'Custom dates…']].map(([v, t]) => `<option value="${v}" ${ST.period === v ? 'selected' : ''}>${t}</option>`).join('')}</select>
   ${ST.period === 'custom' ? `<input type="date" id="stfrom" value="${ST.from}" style="font:inherit;padding:6px 8px;border:1px solid #d1d5db;border-radius:10px"> to <input type="date" id="stto" value="${ST.to || dkey(new Date())}" style="font:inherit;padding:6px 8px;border:1px solid #d1d5db;border-radius:10px">` : ''}</div>
   <div style="display:flex;gap:6px;align-items:center"><span style="font-size:13px;color:var(--mute);font-weight:600">DATA</span><button class="btn sm ${ST.site ? '' : 'g'}" data-src="site">${ST.site ? '☑' : '☐'} ${SITE_NAME}</button><button class="btn sm ${ST.bp ? '' : 'g'}" data-src="bp">${ST.bp ? '☑' : '☐'} 1500 Blueprint</button></div>
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
  const hc = a => a == null ? '#f3f4f6' : a < 50 ? '#fde2e2' : a < 70 ? '#fef3c7' : '#dcfce7';
  const order = per.filter(p => p.n).sort((a, b) => a.acc - b.acc || (b.s.share || 0) - (a.s.share || 0));
  const missed = rows.filter(r => !r.ok).slice(-12).reverse();
  app().innerHTML = topbar('stats') + `<div class="page" style="gap:18px"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;align-items:flex-end"><div><h1 class="hd" style="margin:0;font-size:30px">Stats</h1><div style="color:var(--mute);font-size:14px">First try on each question, on this site plus his 1500 Blueprint days. Click any category to see why.</div></div>${filters()}</div>
   ${scoresBlock()}
   <section class="stats" style="grid-template-columns:repeat(6,minmax(0,1fr))">
    ${kpi('Questions', tot, [ST.site ? SITE_NAME + ' ' + rows.length : '', ST.bp ? 'Blueprint ' + bpTot : ''].filter(Boolean).join(' · '))}
    ${kpi('Right on first try', tAcc == null ? '—' : tAcc + '%', ST.site && ST.bp ? 'combined' : ST.site ? SITE_NAME : '1500 Blueprint', ST.site && !ST.bp ? delta(acc, pacc) : '')}
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
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Latest misses</h2>${missed.length ? missed.map(missRow).join('') : '<div style="color:var(--mute)">None in this period.</div>'}</section>
  </div>`;
  window.scrollTo(0, 0);
  const tick = {font: {family: 'Inter', size: 12}};
  scoresChart();
  chart('c1', {type: 'line', data: {labels: se.lab, datasets: [
    ST.site && ST.sec !== 'English' ? {label: 'Math', data: se.accM, borderColor: SCOL.Math, backgroundColor: SCOL.Math, tension: .3, spanGaps: true} : null,
    ST.site && ST.sec !== 'Math' ? {label: 'Reading & Writing', data: se.accE, borderColor: SCOL.English, backgroundColor: SCOL.English, tension: .3, spanGaps: true} : null,
    ST.bp ? {label: '1500 Blueprint', data: se.bpA, borderColor: '#9ca3af', backgroundColor: '#9ca3af', borderDash: [4, 4], tension: .3, spanGaps: true} : null,
    ST.bp && ST.site ? {label: 'Combined', data: se.comb, borderColor: '#111827', backgroundColor: '#111827', borderWidth: 3, tension: .3, spanGaps: true} : null,
    {label: 'Goal (1300 ≈ 75%)', data: se.lab.map(() => 75), borderColor: '#ca8a04', borderDash: [6, 6], pointRadius: 0}].filter(Boolean)},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('c2', {type: 'bar', data: {labels: se.lab, datasets: [ST.sec !== 'English' ? {label: 'Math', data: se.m, backgroundColor: SCOL.Math} : null, ST.sec !== 'Math' ? {label: 'Reading & Writing', data: se.e, backgroundColor: SCOL.English} : null, ST.bp ? {label: '1500 Blueprint', data: se.bpN, backgroundColor: '#cbd5e1'} : null].filter(Boolean)},
    options: {maintainAspectRatio: false, scales: {x: {stacked: true, ticks: tick}, y: {stacked: true, ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('c3', {type: 'bar', data: {labels: order.map(p => p.s.name), datasets: [
    {label: 'Now', data: order.map(p => p.acc), backgroundColor: order.map(p => p.acc < 50 ? '#f87171' : p.acc < 70 ? '#fbbf24' : '#4ade80')},
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
   <div style="margin-top:10px;display:grid;gap:8px"><div style="font-family:'Source Serif 4',Georgia,serif;font-size:16px">${q.q}</div>
   <div><span style="color:#b91c1c;font-weight:700">He picked:</span> ${r.picked ? r.picked : '(not recorded)'} &nbsp; <span style="color:#15803d;font-weight:700">Right answer:</span> ${ans || ''}</div>
   <div class="box b-blue"><div class="lab">How to do it</div><div class="c">${q.steps.map((s, i) => (i + 1) + '. ' + esc(s)).join('<br>')}</div></div>${q.trap ? `<div class="box b-red"><div class="lab">Trap</div><div class="c">${esc(q.trap)}</div></div>` : ''}
   <div><button class="btn sm" data-go="#/drill/ids:${q.id}">Try it again</button></div></div></details>`
}
function skillStats(id) {
  killCharts(); const s = SK2[id]; if (!s) return drawStats();
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
    ${kpi(ST.site ? SITE_NAME + ' only' : '1500 Blueprint', ST.site ? (acc == null ? '—' : acc + '%') : (base == null ? '—' : base + '%'), ST.site ? rows.filter(r => r.ok).length + ' of ' + rows.length : (b.n ? b.ok + ' of ' + b.n : ''))}
    ${kpi('1500 Blueprint before', base == null ? '—' : base + '%', b.n ? `${b.ok} of ${b.n}` : '', acc != null && base != null ? delta(acc, base) : '')}
        ${kpi('Avg time / question', mmss(avg), 'SAT pace ' + mmss(PACE[s.sec]))}
    ${kpi('Next step', `<span style="font-size:18px">${acc == null || acc < 50 ? 'Learn it, then drill' : acc < 70 ? 'Drill + redo misses' : 'Keep it warm'}</span>`, '')}
   </section>
   <section class="card" style="padding:16px 18px;border-left:6px solid #b91c1c"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Why the score is ${acc == null ? '—' : acc + '%'}</h2>${why.length ? `<ul style="margin:0;padding-left:20px;display:grid;gap:6px">${why.map(w => `<li>${esc(w)}</li>`).join('')}</ul>` : '<div>Nothing stands out. Keep practicing.</div>'}
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">${missed.length ? `<button class="btn" data-go="#/drill/ids:${[...new Set(missed.map(r => r.q.id))].join(',')}">Redo the ${new Set(missed.map(r => r.q.id)).size} missed</button>` : ''}<button class="btn o" data-go="#/drill/${id}">Drill 10 more</button><button class="btn g" data-go="#/learn/${id}">Learn it</button><button class="btn g" data-go="#/video/${id}">▶ Video</button></div></section>
   <div class="cols" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr)">
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">Accuracy over time</h2><div style="height:240px"><canvas id="k1"></canvas></div></section>
    <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 6px;font-size:19px">By difficulty</h2><div style="height:240px"><canvas id="k2"></canvas></div></section>
   </div>
   ${kl.length ? `<section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">By kind of question</h2><table class="rep"><thead><tr><th>Kind</th><th>Qs</th><th>Right</th><th>Score</th><th>Example</th></tr></thead><tbody>${kl.map(k => { const l = level(k.a, k.n); return `<tr><td><b>${esc(k.nm)}</b></td><td>${k.n}</td><td>${k.ok}</td><td><span class="pill" style="color:${l[1]};background:${l[2]}">${k.a}%</span></td><td style="font-size:13px;color:var(--mute)">${esc(plain(k.ex.q).slice(0, 90))}…</td></tr>` }).join('')}</tbody></table></section>` : ''}
   ${tl.length ? `<section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Traps he fell for</h2>${tl.map(([t, n]) => `<div style="display:flex;gap:10px;padding:6px 0;border-top:1px solid #f1f2f4"><span class="pill" style="background:#fde2e2;color:#b91c1c">${n}×</span>${esc(t)}</div>`).join('')}</section>` : ''}
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Every missed question <span style="font-size:13px;color:var(--mute);font-weight:500">click to see his answer, the right one, and how to do it</span></h2>${missed.length ? missed.map(missRow).join('') : '<div style="color:var(--mute)">No misses in this period.</div>'}</section>
   <section class="card" style="padding:16px 18px"><h2 class="hd" style="margin:0 0 8px;font-size:19px">Right on the first try (${right.length})</h2>${right.slice(0, 30).map(r => `<div style="display:flex;gap:10px;padding:6px 0;border-top:1px solid #f1f2f4;font-size:14px"><span class="pill" style="background:#dcfce7;color:#15803d">✓</span><span style="color:var(--mute)">${new Date(r.ts).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} · ${DIFF[r.q.diff]} · ${mmss(r.sec)}</span>${esc(plain(r.q.q).slice(0, 110))}…</div>`).join('') || '<div style="color:var(--mute)">None yet.</div>'}</section>
  </div>`;
  window.scrollTo(0, 0);
  const tick = {font: {family: 'Inter', size: 12}};
  chart('k1', {type: 'line', data: {labels: se.lab, datasets: [{label: 'Accuracy', data: se.acc, borderColor: SCOL[s.sec] || SCOL.Math, backgroundColor: SCOL[s.sec] || SCOL.Math, pointRadius: 5, tension: .3, spanGaps: true}, ...(base != null ? [{label: 'Blueprint before', data: se.lab.map(() => base), borderColor: '#111827', borderDash: [5, 5], pointRadius: 0}] : []), {label: 'Goal 75%', data: se.lab.map(() => 75), borderColor: '#ca8a04', borderDash: [6, 6], pointRadius: 0}]},
    options: {maintainAspectRatio: false, scales: {y: {min: 0, max: 100, ticks: {...tick, callback: v => v + '%'}}, x: {ticks: tick}}, plugins: {legend: {labels: tick}}}});
  chart('k2', {type: 'bar', data: {labels: diff.map(d => ({E: 'Easy', M: 'Medium', H: 'Hard'})[d.k] + ` (${d.ok}/${d.n})`), datasets: [{label: 'Accuracy', data: diff.map(d => d.a), backgroundColor: diff.map(d => d.a == null ? '#e5e7eb' : d.a < 50 ? '#f87171' : d.a < 70 ? '#fbbf24' : '#4ade80')}]},
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
function scoreDays() { return [...new Set(LOG.filter(x => x.first).map(x => x.day))].sort() }
function scoresBlock() {
  const L = SAT_LAST(), t = new Date(); const tk = dkey(t), now = proj(tk), days = scoreDays(), prevD = days.filter(d => d < tk).pop(), prev = prevD ? proj(prevD) : null;
  const arrow = (a, b) => a > b ? `<span style="color:#15803d">▲ +${a - b}</span>` : a < b ? `<span style="color:#c2410c">▼ ${a - b}</span>` : '<span style="color:var(--mute)">±0</span>';
  const box = (lab, v, last, sub) => `<div class="card" style="padding:14px 16px;${lab === 'Combined' ? 'border:2px solid #1e3a8a' : ''}"><div style="font-size:13px;color:var(--mute);font-weight:600">${lab} (projected)</div>
    <div class="hd" style="font-size:${lab === 'Combined' ? 44 : 36}px;font-weight:800;line-height:1.1">${v.toLocaleString()}</div><div style="font-size:13px">${arrow(v, last)} vs. ${esc(L.label)} SAT (${last})</div>${sub ? `<div style="font-size:13px;color:var(--mute)">${sub}</div>` : ''}</div>`;
  const offi = SAT_OFFICIAL.slice().reverse().map(o => `<tr><td><b>${esc(o.label)}, ${o.date.slice(0, 4)}</b></td><td>${o.Math}</td><td>${o['R&W']}</td><td><b>${o.total.toLocaleString()}</b></td><td>${o.pct && o.pct.total ? o.pct.total + 'th' : '—'}</td></tr>`).join('');
  return `<section class="card" style="padding:16px 18px;border-left:5px solid #1e3a8a"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;align-items:baseline"><h2 class="hd" style="margin:0;font-size:24px">Scores</h2>
    <div style="font-size:13px;color:var(--mute)">As of right now · goal ${GOAL} on Dec 5 · ${now.total >= GOAL ? '<b style="color:#15803d">on target</b>' : `<b>${GOAL - now.total}</b> points to go`}${prev ? ` · since yesterday ${arrow(now.total, prev.total)}` : ''}</div></div>
   <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:12px">${box('Math', now.Math, L.Math)}${box('Reading & Writing', now['R&W'], L['R&W'])}${box('Combined', now.total, L.total, `Goal ${GOAL}`)}</div>
   ${(() => { const P = now.parts, row = (k, lab) => `<tr><td><b>${lab}</b></td><td>${P[k].off}</td><td>${P[k].prac} <span style="font-size:12px;color:var(--mute)">(${P[k].bp} Blueprint + ${P[k].sp} HELM questions)</span></td><td>${Math.round(100 * (1 - P[k].wp))}% / ${Math.round(100 * P[k].wp)}%</td><td><b>${P[k].val}</b></td></tr>`;
     return `<h3 class="hd" style="margin:14px 0 6px;font-size:17px">How the projection is built <span style="font-size:13px;color:var(--mute);font-weight:500">all the data: official SATs + 1500 Blueprint + HELM</span></h3>
     <div style="overflow-x:auto"><table class="rep" style="width:100%"><thead><tr><th>Section</th><th>Official SATs (Nov 7 counts 50%, Oct 3 30%, Sep 12 20%)</th><th>Practice accuracy → score</th><th>Weight (official / practice)</th><th>Projected</th></tr></thead><tbody>${row('Math', 'Math')}${row('R&W', 'Reading & Writing')}</tbody></table></div>` })()}
   <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:16px;margin-top:14px;align-items:start">
    <div><h3 class="hd" style="margin:0 0 6px;font-size:17px">Official SAT scores</h3><table class="rep" style="width:100%"><thead><tr><th>Test</th><th>Math</th><th>R&W</th><th>Total</th><th>Percentile</th></tr></thead><tbody>${offi}</tbody></table></div>
    <div><h3 class="hd" style="margin:0 0 6px;font-size:17px">Score trend: official SATs, then the daily projection</h3><div style="height:260px"><canvas id="c0"></canvas></div><div style="font-size:12px;color:var(--mute)">Dark bars = official SATs. Light bars = HELM projection for that day. The dashed line is the trend through every point, carried to Dec 5.</div></div></div>
   <h3 class="hd" style="margin:16px 0 6px;font-size:17px">College Board performance by domain <span style="font-size:13px;color:var(--mute);font-weight:500">score band for each part of the test · green = better than the last test, orange = lower</span></h3>
   <div style="overflow-x:auto"><table class="rep" style="width:100%"><thead><tr><th>Domain</th>${SAT_OFFICIAL.map(o => `<th>${esc(o.label)}</th>`).join('')}</tr></thead><tbody>${SAT_DOM.map(([sec, k, nm]) => `<tr><td><b>${nm}</b> <span style="font-size:12px;color:var(--mute)">${sec}</span></td>${SAT_OFFICIAL.map((o, i) => { const v = o.dom[k], pv = i ? SAT_OFFICIAL[i - 1].dom[k] : null, lo = x => +String(x).split('–')[0]; const c = pv == null || lo(v) === lo(pv) ? '' : lo(v) > lo(pv) ? 'color:#15803d;font-weight:700' : 'color:#c2410c;font-weight:700'; return `<td style="${c}">${v}</td>` }).join('')}</tr>`).join('')}</tbody></table></div>
   <div style="font-size:12px;color:var(--mute);margin-top:8px">The projection is an estimate, not an official score. It blends all of his official SATs with his practice accuracy on every 1500 Blueprint and HELM question (first tries), with each category weighted by how often it shows up on the SAT. The more he practices, the more the practice side counts (up to 60%). The real test is adaptive, so read it as a direction.</div></section>`
}
function scoresChart() {
  // stacked bars: Math (blue) + Reading & Writing (orange) = total; dashed trendline fitted to every point and carried to test day
  const L = SAT_LAST(), days = scoreDays().filter(d => d > L.date);
  const pts = SAT_OFFICIAL.map(o => ({d: o.date, l: o.label + ' SAT', M: o.Math, R: o['R&W'], off: true})).concat(days.map(d => { const p = proj(d); return {d, l: new Date(d + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'}) + ' (proj.)', M: p.Math, R: p['R&W']} }));
  const TEST = '2026-12-05', x = d => (new Date(d + 'T12:00') - new Date(pts[0].d + 'T12:00')) / 864e5, n = pts.length;
  const xs = pts.map(p => x(p.d)), ys = pts.map(p => p.M + p.R), mx = xs.reduce((a, b) => a + b, 0) / n, my = ys.reduce((a, b) => a + b, 0) / n;
  const sxx = xs.reduce((a, v) => a + (v - mx) ** 2, 0), slope = sxx ? xs.reduce((a, v, i) => a + (v - mx) * (ys[i] - my), 0) / sxx : 0, fit = v => Math.round(my + slope * (v - mx));
  const labels = pts.map(p => p.l).concat(['Dec 5 test (trend)']), trend = xs.map(fit).concat([fit(x(TEST))]);
  chart('c0', {data: {labels, datasets: [
    {type: 'bar', label: 'Math', data: pts.map(p => p.M).concat([null]), backgroundColor: pts.map(p => p.off ? '#1e3a8a' : '#60a5fa').concat(['#000']), stack: 's', order: 2},
    {type: 'bar', label: 'Reading & Writing', data: pts.map(p => p.R).concat([null]), backgroundColor: pts.map(p => p.off ? '#c2410c' : '#fdba74').concat(['#000']), stack: 's', order: 2},
    {type: 'line', label: `Trend (${slope >= 0 ? '+' : ''}${Math.round(slope * 7)} pts/week)`, data: trend, borderColor: '#111827', borderDash: [6, 4], borderWidth: 2, pointRadius: trend.map((_, i) => i === trend.length - 1 ? 6 : 0), pointBackgroundColor: '#111827', order: 0, stack: 'trend'},
    {type: 'line', label: 'Goal ' + GOAL, data: labels.map(() => GOAL), borderColor: '#15803d', borderWidth: 2, pointRadius: 0, order: 1, stack: 'goal'}]},
    options: {maintainAspectRatio: false, plugins: {legend: {position: 'bottom'}, tooltip: {callbacks: {footer: it => { const i = it[0].dataIndex; return i < pts.length ? 'Total: ' + (pts[i].M + pts[i].R) : '' }}}},
      scales: {x: {stacked: true}, y: {stacked: true, min: 0, suggestedMax: 1400, title: {display: true, text: 'SAT score'}}}}})
}
