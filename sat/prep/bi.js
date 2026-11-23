/* ---------- STATS v2: Looker-style BI dashboard for #/stats (replaces drawStats from stats.js) ----------
   One record set feeds every number: HELM first tries (1 row per question), Blueprint daily section totals (dated),
   and Blueprint skill totals (undated, Nov 6–20). Cross-filters, drill-down, inspector drawer with search, sort and CSV. */
const BI = {cmp: true, pq: '', range: 'today', from: '', to: '', src: {helm: true, bp: true}, f: {}, gran: 'day', dark: false, sort: {k: 'lost', d: -1}, drawer: null, dq: '', dsort: {k: 'date', d: -1}};
const BI_BP_FROM = '2026-08-31', BI_BP_TO = '2026-11-20';
const BI_LEVELS = [['sec', 'Section'], ['dom', 'Domain'], ['skill', 'Skill'], ['diff', 'Difficulty']];
const BI_SEC = {Math: 'Math', English: 'Reading & Writing'};
const BI_DIFF = {E: 'Easy', M: 'Medium', H: 'Hard'};
const HC = {navy: '#4F46E5', navyL: '#A5B4FC', gold: '#0D9488', goldL: '#99F6E4', steel: '#A1A1AA', green: '#10B981', amber: '#F59E0B', rose: '#F43F5E', ink: '#09090B', violet: '#7C3AED', blue: '#2563EB'};

(function css() {
  const s = document.createElement('style'); s.textContent = `
  .bi{--bg:#FAFAFA;--card:#FFFFFF;--bd:#E4E4E7;--tx:#09090B;--mu:#71717A;--ac:#2563EB;--ac2:#0D9488;--up:#10B981;--dn:#F43F5E;--hv:#F4F4F5;--mono:'Geist Mono','JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;color:var(--tx);font-variant-numeric:tabular-nums}
  .bi.dark{--bg:#09090B;--card:#121215;--bd:#27272A;--tx:#FAFAFA;--mu:#A1A1AA;--ac:#3B82F6;--hv:#18181B}
  .bi.dark,.bi.dark .page{background:var(--bg)}
  .bi .bc{background:var(--card);border:1px solid var(--bd);border-radius:16px;box-shadow:0 1px 2px rgba(15,23,42,.04),0 1px 3px rgba(15,23,42,.06)}
  .bi .ctl{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  .bi .ctl select,.bi .ctl input{font:inherit;font-size:14px;padding:7px 10px;border:1px solid var(--bd);border-radius:10px;background:var(--card);color:var(--tx)}
  .bi .seg{display:inline-flex;border:1px solid var(--bd);border-radius:10px;overflow:hidden}
  .bi .seg button{border:0;background:var(--card);color:var(--mu);padding:7px 12px;font:inherit;font-size:13px;font-weight:600;cursor:pointer}
  .bi .seg button.on{background:var(--ac);color:#fff}
  .bi .lab{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--mu)}
  .bi .pills{position:sticky;top:0;z-index:20;display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:10px 14px;background:var(--bg);border-bottom:1px solid var(--bd)}
  .bi .pill2{display:inline-flex;gap:6px;align-items:center;background:#eef2ff;color:#1e3a8a;border:1px solid #c7d2fe;border-radius:999px;padding:4px 10px;font-size:13px;font-weight:600}
  .bi.dark .pill2{background:#1e293b;color:#bfdbfe;border-color:#334155}
  .bi .pill2 button{border:0;background:none;color:inherit;cursor:pointer;font-size:14px;padding:0}
  .bi .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
  .bi .kpi{position:relative;overflow:hidden;padding:16px 18px;cursor:pointer}
  .bi .kpi{transition:border-color .15s,box-shadow .15s,transform .15s}.bi .kpi:hover{border-color:#93C5FD;box-shadow:0 8px 24px rgba(15,23,42,.08);transform:translateY(-1px)}
  .bi .kpi .v{font-size:32px;font-weight:700;letter-spacing:-.02em;line-height:1.1;position:relative}
  .bi .kpi svg{position:absolute;left:0;right:0;bottom:0;width:100%;height:46px;opacity:.35}
  .bi .badge{display:inline-flex;align-items:center;gap:3px;border-radius:999px;padding:2px 8px;font-size:12px;font-weight:700}
  .bi .badge.up{background:#d1fae5;color:#065f46}.bi .badge.dn{background:#ffe4e6;color:#9f1239}.bi .badge.eq{background:var(--hv);color:var(--mu)}
  .bi .t2{display:grid;grid-template-columns:minmax(0,65fr) minmax(0,35fr);gap:14px}
  .bi table.pv{width:100%;border-collapse:collapse;font-size:14px}
  .bi table.pv th{position:sticky;top:0;background:var(--card);text-align:left;font-size:12px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:1px solid var(--bd);cursor:pointer;white-space:nowrap}
  .bi table.pv td{padding:8px 10px;border-bottom:1px solid var(--bd);white-space:nowrap}
  .bi table.pv tr:hover td{background:var(--hv)}
  .bi table.pv td.c{cursor:pointer}
  .bi .cb{position:relative;min-width:110px}.bi .cb i{position:absolute;left:0;top:50%;height:18px;transform:translateY(-50%);border-radius:4px;opacity:.22}.bi .cb span{position:relative;padding-left:6px;font-weight:700}
  .bi .drw{position:fixed;top:0;right:0;bottom:0;width:min(760px,96vw);background:var(--card);color:var(--tx);border-left:1px solid var(--bd);box-shadow:-12px 0 32px rgba(15,23,42,.18);z-index:9000;display:flex;flex-direction:column;transform:translateX(100%);transition:transform .22s ease}
  .bi .drw.open{transform:none}
  .bi .scrim{position:fixed;inset:0;background:rgba(15,23,42,.35);z-index:8999}
  .bi .drw .hd2{padding:16px 18px;border-bottom:1px solid var(--bd);display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
  .bi .drw .bd{overflow:auto;flex:1}
  .bi .xbtn{border:1px solid var(--bd);background:var(--card);color:var(--tx);border-radius:10px;padding:6px 10px;cursor:pointer;font:inherit;font-size:13px;font-weight:600}
  .bi .xbtn.pr{background:var(--ac);border-color:var(--ac);color:#fff}
  .bi.dark{--mute:#94a3b8;--line:#1e293b}
  .bi.dark .card{background:var(--card)!important;border-color:var(--bd)!important;color:var(--tx)}
  .bi.dark table.rep th,.bi.dark table.rep td{border-color:var(--bd)!important;color:var(--tx)}
  .bi.dark tr[style*="f5f3ff"]{background:#1e1b4b!important}
  .bi.dark .hd{color:var(--tx)}
  .bi .tsp{display:inline-block;width:96px;height:26px;vertical-align:middle;margin-right:6px}.bi .tsp svg{width:100%;height:100%;display:block}
  .bi .trd{padding:14px 18px;border-bottom:1px solid var(--bd)}
  @media(max-width:900px){.bi .kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.bi .t2{grid-template-columns:1fr}}
  /* ===== Executive BI spec (Allie, Nov 23): neutral chrome, hairlines not shadows, color only for data ===== */
  .bi,.bi .page{background:var(--bg)}
  body:has(#bi){background:var(--bg)}
  body:has(#bi) .top{position:static;box-shadow:none}
  .bi .page{max-width:1680px;gap:16px!important;padding-top:0}
  .bi .bc,.bi .card{background:var(--card)!important;border:1px solid var(--bd)!important;border-radius:12px!important;box-shadow:none!important}
  .bi .bc{padding:20px 22px!important}
  .bi .lab,.bi .ch{font-size:13px;font-weight:500;letter-spacing:0;text-transform:none;color:var(--mu)}
  .bi .ch b{color:var(--tx);font-size:17px;font-weight:700;letter-spacing:-.01em}.bi .ch{margin-bottom:2px}
  .bi .ch2{font-size:12px;color:var(--mu);margin-top:2px}
  .bi .num,.bi .kpi .v,.bi table.pv td:not(:first-child),.bi .rk .val{font-family:var(--mono);font-variant-numeric:tabular-nums}
  .bi .kpi .v{font-size:30px!important;font-weight:600!important;letter-spacing:-.03em!important;margin-top:10px;color:var(--tx)}
  .bi .kpi svg{height:40px;opacity:1}
  .bi .kpi:hover{transform:none;box-shadow:none;border-color:#A1A1AA!important}
  .bi .info{display:inline-grid;place-items:center;width:15px;height:15px;border-radius:50%;border:1px solid var(--bd);font-size:10px;color:var(--mu);margin-left:4px;cursor:help;vertical-align:1px}
  .bi .badge{font-family:var(--mono);font-weight:600;font-size:12px}
  .bi .badge.up{background:#ECFDF5;color:#047857}.bi .badge.dn{background:#FFF1F2;color:#BE123C}
  .bi.dark .badge.up{background:rgba(16,185,129,.14);color:#34D399}.bi.dark .badge.dn{background:rgba(244,63,94,.14);color:#FB7185}
  .bi .cbar{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--bd);margin:0 -32px;padding:14px 32px;display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center;justify-content:space-between}
  .bi .cbar h1{font-size:20px!important;font-weight:600!important;letter-spacing:-.02em;margin:0}
  .bi .cbar .sub{font-size:12px;color:var(--mu)}
  .bi .tgl{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--tx);cursor:pointer;user-select:none;border:1px solid var(--bd);border-radius:8px;padding:6px 10px;background:var(--card)}
  .bi .tgl i{width:26px;height:16px;border-radius:999px;background:#D4D4D8;position:relative;transition:background .15s}.bi .tgl i:after{content:'';position:absolute;top:2px;left:2px;width:12px;height:12px;border-radius:50%;background:#fff;transition:left .15s}
  .bi .tgl.on i{background:var(--ac)}.bi .tgl.on i:after{left:12px}
  .bi .xbtn{border-radius:8px}.bi .xbtn.pr{background:var(--tx);border-color:var(--tx);color:var(--card)}
  .bi .ctl select,.bi .ctl input{border-radius:8px}
  .bi .seg{border-radius:8px;background:var(--hv);border:0;padding:2px}.bi .seg button{background:transparent;border-radius:6px;padding:5px 10px}.bi .seg button.on{background:var(--card);color:var(--tx);box-shadow:0 0 0 1px var(--bd)}
  .bi .pills{position:static;background:transparent;border:0;padding:0}
  .bi .pill2{background:var(--card);color:var(--tx);border:1px solid var(--bd);font-weight:500}
  .bi .t2{grid-template-columns:minmax(0,2fr) minmax(0,1fr)!important;gap:16px}
  .bi .kpis{gap:16px}
  .bi .rk{display:grid;gap:12px;margin-top:14px}
  .bi .rk .it{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;align-items:center;cursor:pointer;padding:6px 8px;margin:0 -8px;border-radius:8px}
  .bi .rk .it:hover{background:var(--hv)}
  .bi .rk .nm{font-size:13px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bi .rk .val{font-size:13px;font-weight:600;text-align:right;white-space:nowrap}.bi .rk .val span{color:var(--mu);font-weight:400;margin-left:6px}
  .bi .rk .tr{grid-column:1/-1;height:6px;border-radius:999px;background:var(--hv);overflow:hidden}.bi .rk .tr i{display:block;height:100%;border-radius:999px}
  .bi .dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:8px;vertical-align:1px}
  .bi table.pv th{background:var(--card);font-size:12px;font-weight:500;color:var(--mu);border-bottom:1px solid var(--bd)}
  .bi table.pv td{border-bottom:1px solid var(--bd);font-size:13px}
  .bi .srch{font:inherit;font-size:13px;padding:7px 10px 7px 30px;border:1px solid var(--bd);border-radius:8px;background:var(--card) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='none' stroke='%2371717A' stroke-width='2'%3E%3Ccircle cx='6' cy='6' r='4.5'/%3E%3Cpath d='M9.5 9.5 13 13'/%3E%3C/svg%3E") no-repeat 10px 50%;color:var(--tx);min-width:220px}
  .bi .gtip{position:absolute;pointer-events:none;z-index:60;min-width:180px;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,.72);backdrop-filter:blur(14px) saturate(160%);border:1px solid rgba(228,228,231,.9);box-shadow:0 10px 30px rgba(9,9,11,.12);font-size:12px;color:#09090B;transition:opacity .12s}
  .bi.dark .gtip{background:rgba(18,18,21,.72);border-color:rgba(63,63,70,.9);color:#FAFAFA}
  .bi .gtip .tt{font-weight:600;margin-bottom:6px}.bi .gtip .rw{display:flex;justify-content:space-between;gap:16px;margin-top:3px}.bi .gtip .rw b{font-family:var(--mono);font-weight:600}.bi .gtip .rw i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px}
  .bi .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#09090B;color:#fff;padding:10px 14px;border-radius:8px;font-size:13px;z-index:9999}
  .bi button,.bi .xbtn,.bi .bc,.bi .kpi,.bi .rk .it,.bi .pill2,.bi .tgl,.bi table.pv td,.bi .seg button{transition:background-color 150ms ease-out,border-color 150ms ease-out,color 150ms ease-out,opacity 150ms ease-out}
  .bi [data-bi]:focus-visible,.bi select:focus-visible,.bi input:focus-visible{outline:2px solid var(--ac);outline-offset:2px;border-radius:8px}
  .bi section h2.hd,.bi section h3.hd{font-size:17px!important;font-weight:700!important;letter-spacing:-.01em;color:var(--tx)}
  .bi .bc,.bi .card.blk,.bi .subcard{border-color:#D4D4D8!important}
  .bi.dark .bc,.bi.dark .card.blk,.bi.dark .subcard{border-color:#3F3F46!important;background:var(--card)!important}
  .bi .blkh{border-color:var(--bd)}
  .bi section h2.hd span,.bi section h3.hd span{font-size:12px!important;font-weight:400!important;color:var(--mu)!important}
  .bi section .hd[style*="font-size:28px"],.bi section .hd[style*="font-size:22px"],.bi section .hd[style*="font-size:40px"],.bi section .hd[style*="font-size:44px"],.bi section .hd[style*="font-size:36px"]{font-family:var(--mono);font-weight:600!important;letter-spacing:-.03em}
  .bi .box .lab{text-transform:none;letter-spacing:0;font-size:13px;font-weight:600}
  @media(max-width:1100px){.bi .t2{grid-template-columns:1fr!important}}
  @media(max-width:760px){.bi .cbar{margin:0 -14px;padding:12px 14px}}`;
  document.head.appendChild(s);
  if (!document.getElementById('bi-mono')) { const l = document.createElement('link'); l.id = 'bi-mono'; l.rel = 'stylesheet'; l.href = 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap'; document.head.appendChild(l) }
})();

// ---------- the one dataset ----------
function biRecords() {
  const R = [];
  if (BI.src.helm) firstTries().forEach(r => { const q = r.q, s = r.s;
    R.push({src: 'HELM', date: r.day, sec: BI_SEC[s.sec], dom: s.dom || '—', skill: s.name, skillId: s.id, diff: BI_DIFF[q.diff] || '—', n: 1, ok: r.ok ? 1 : 0, secs: r.sec > 0 && r.sec < 1800 ? r.sec : null,
      pace: PACE[s.sec], qid: q.id, question: plain(q.q), picked: r.picked || '', answer: q.ch ? q.ch[q.ans] : (q.show || (q.grid || [])[0] || ''), trap: q.trap || '', share: s.share || 0}) });
  if (BI.src.bp) {
    (BPD || []).forEach(d => { const parts = [['Math', d.math], ['Reading & Writing', d.rw]]; let used = 0, usedOk = 0;
      parts.forEach(([sec, p]) => { if (p && p.n) { const ok = Math.round(p.n * p.acc / 100); used += p.n; usedOk += ok; R.push({src: 'Blueprint', date: d.day, sec, dom: 'Blueprint (not itemized)', skill: 'Blueprint daily work', diff: '—', n: p.n, ok, secs: null, kind: 'daily', week: !!d.week}) } });
      const rest = (d.n || 0) - used; if (rest > 0) R.push({src: 'Blueprint', date: d.day, sec: 'Mixed', dom: 'Blueprint course quizzes', skill: 'Blueprint course quizzes', diff: '—', n: rest, ok: Math.max(0, Math.round(d.n * d.acc / 100) - usedOk), secs: null, kind: 'daily', week: !!d.week}) });
    Object.entries(BPS || {}).forEach(([id, b]) => { const s = SK2[id]; if (!s || !b.n) return;
      R.push({src: 'Blueprint', date: null, sec: BI_SEC[s.sec], dom: s.dom || '—', skill: s.name, skillId: id, diff: '—', n: b.n, ok: b.ok, secs: null, kind: 'skill', share: s.share || 0}) });
  }
  return R
}
function biRange() { if (BI.range === 'custom') return [BI.from || '0000', BI.to || dkey(new Date())]; return rangeOf(BI.range === 'today' ? 'day' : BI.range) }
function biPrevRange() { if (BI.range === 'all') return null; const [a, b] = biRange(), A = new Date(a + 'T12:00'), B = new Date(b + 'T12:00'), n = Math.round((B - A) / 864e5) + 1, pa = new Date(A), pb = new Date(A); pa.setDate(pa.getDate() - n); pb.setDate(pb.getDate() - 1); return [dkey(pa), dkey(pb)] }
const biBpSkillOk = ([a, b]) => a <= BI_BP_FROM && b >= BI_BP_TO;   // undated Blueprint skill totals count only when the whole Nov 6–20 window is inside the range
function biBucket(d, g) { if (!d) return null; if (g === 'day') return d; if (g === 'month') return d.slice(0, 7); return bucketKey(d, 'week') }
function biFilter(R, range, opt = {}) {
  const [a, b] = range, f = BI.f;
  return R.filter(r => {
    if (r.kind === 'skill') { if (opt.dated || !biBpSkillOk(range) || f.date || f.diff) return false } else if (!r.date || r.date < a || r.date > b) return false;
    if (r.kind === 'daily' && opt.items) return false;
    for (const [k] of BI_LEVELS) if (f[k] && r[k] !== f[k]) return false;
    if (f.date && biBucket(r.date, f.dateG) !== f.date) return false;
    return true })
}
function biAgg(rows) { const n = rows.reduce((a, r) => a + r.n, 0), ok = rows.reduce((a, r) => a + r.ok, 0), t = rows.filter(r => r.secs != null);
  return {n, ok, wrong: n - ok, acc: n ? Math.round(100 * ok / n) : null, secs: t.length ? Math.round(t.reduce((a, r) => a + r.secs, 0) / t.length) : null, pace: t.length ? Math.round(t.reduce((a, r) => a + r.pace, 0) / t.length) : null} }
function biLevel() { const f = BI.f; return f.skill ? 'diff' : f.dom ? 'skill' : f.sec ? 'dom' : 'sec' }
function biDays([a, b]) { const out = [], d = new Date((a === '0000' ? (BPD[0] || {}).day || dkey(new Date()) : a) + 'T12:00'), e = new Date((b === '9999' ? dkey(new Date()) : b) + 'T12:00'); while (d <= e && out.length < 400) { out.push(dkey(d)); d.setDate(d.getDate() + 1) } return out }
function spark(vals, col) { const v = vals.filter(x => x != null); if (v.length < 2) return ''; const lo = Math.min(...v), hi = Math.max(...v), W = 200, H = 46;
  const pts = vals.map((x, i) => x == null ? null : [i * W / (vals.length - 1), H - 4 - (hi === lo ? (H - 8) / 2 : (x - lo) / (hi - lo) * (H - 8))]).filter(Boolean);
  const gid = 'sg' + Math.random().toString(36).slice(2, 8);
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none"><defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity=".22"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient></defs><polygon points="0,${H} ${pts.map(p => p.join(',')).join(' ')} ${W},${H}" fill="url(#${gid})"/><polyline points="${pts.map(p => p.join(',')).join(' ')}" fill="none" stroke="${col}" stroke-width="1.75" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></svg>` }
function badge(now, prev, unit = '', invert = false) { if (now == null || prev == null) return '<span class="badge eq">no comparison</span>'; const d = now - prev; if (!d) return '<span class="badge eq">± 0</span>';
  const good = invert ? d < 0 : d > 0; return `<span class="badge ${good ? 'up' : 'dn'}">${d > 0 ? '▲' : '▼'} ${Math.abs(d)}${unit}</span>` }

// ---------- page ----------
function drawStats() {
  loadTutorQ(() => { if (document.getElementById('bi')) drawStats() });
  killCharts(); const R = biRecords(), rg = biRange(), pr = biPrevRange();
  const rows = biFilter(R, rg), dated = biFilter(R, rg, {dated: true}), prev = pr ? biFilter(R, pr, {dated: true}) : null;
  const A = biAgg(dated), P = prev ? biAgg(prev) : null, days = biDays(rg).slice(-30);
  const perDay = days.map(d => biAgg(dated.filter(r => r.date === d)));
  const endDay = rg[1] === '9999' ? dkey(new Date()) : rg[1] > dkey(new Date()) ? dkey(new Date()) : rg[1];
  const pjNow = proj(endDay), pjPrev = pr ? proj(pr[1]) : null, pjSpark = days.filter((d, i) => i % Math.ceil(days.length / 15 || 1) === 0 || i === days.length - 1).map(d => proj(d).total);
  const lv = biLevel(), lvName = BI_LEVELS.find(x => x[0] === lv)[1];
  const rangeTxt = BI.range === 'all' ? 'All time' : rg[0] === rg[1] ? new Date(rg[0] + 'T12:00').toLocaleDateString('en-US', {weekday: 'short', month: 'short', day: 'numeric'}) : `${new Date(rg[0] + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} – ${new Date(rg[1] + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'})}`;
  const pills = [...BI_LEVELS.filter(([k]) => BI.f[k]).map(([k, n]) => [k, `${n}: ${BI.f[k]}`]), ...(BI.f.date ? [['date', `${BI.f.dateG === 'month' ? 'Month' : BI.f.dateG === 'week' ? 'Week of' : 'Day'}: ${BI.f.dateL}`]] : [])];
  const KINFO = {acc: 'Share of questions he got right on the first try with no help, like the real SAT. Click to see every question.', n: 'HELM questions (first time he saw them) plus Blueprint questions in this range.', time: 'Average seconds per HELM question vs. the SAT pace for that section. Lower is better.', proj: 'Estimated SAT score from his official tests + practice accuracy, compared with his best superscore.'};
  const kpi = (id, lab, val, sub, b, sp, col) => `<div class="bc kpi" data-bi="kpi:${id}"><div class="lab" style="position:relative">${lab}<span class="info" title="${esc(KINFO[id] || '')}">i</span></div><div class="v">${val}</div><div style="position:relative;display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0 34px;font-size:12px;color:var(--mu)">${BI.cmp || id === 'proj' ? b : ''}<span>${sub}</span></div>${spark(sp, col)}</div>`;
  const prevTxt = !BI.cmp ? '' : P ? 'vs. previous period' : 'all time';
  app().innerHTML = topbar('stats') + `<div class="bi ${BI.dark ? 'dark' : ''}" id="bi"><div class="page" style="gap:16px">
   <div class="cbar"><div><h1 class="hd">Stats</h1><div class="sub">HELM first tries (no help) + Blueprint · ${rangeTxt}</div></div>
    <div class="ctl"><select id="bi-range" aria-label="Date range">${[['today', 'Today'], ['7', 'Last 7 days'], ['14', 'Last 14 days'], ['30', 'Last 30 days'], ['all', 'All time'], ['custom', 'Custom…']].map(([v, t]) => `<option value="${v}" ${BI.range === v ? 'selected' : ''}>${t}</option>`).join('')}</select>
     ${BI.range === 'custom' ? `<input type="date" id="bi-from" value="${BI.from}"><span style="color:var(--mu)">to</span><input type="date" id="bi-to" value="${BI.to || dkey(new Date())}">` : ''}
     <span class="tgl ${BI.cmp && BI.range !== 'all' ? 'on' : ''}" data-bi="cmp" role="switch" aria-checked="${BI.cmp}"><i></i>vs. previous period</span>
     <select id="bi-sec" aria-label="Section"><option value="">Both sections</option>${['Math', 'Reading & Writing'].map(s => `<option ${BI.f.sec === s ? 'selected' : ''}>${s}</option>`).join('')}</select>
     <div class="seg" aria-label="Data source"><button class="${BI.src.helm ? 'on' : ''}" data-bi="src:helm">HELM</button><button class="${BI.src.bp ? 'on' : ''}" data-bi="src:bp">Blueprint</button></div>
     <button class="xbtn" data-bi="dark" title="Dark / light mode">${BI.dark ? '☀' : '☾'}</button>
     <button class="xbtn" data-bi="share">Share</button><button class="xbtn pr" data-bi="export">Export CSV</button></div>
    ${pills.length ? `<div class="pills" style="flex-basis:100%">${pills.map(([k, t], i) => `${i ? '<span style="color:var(--mu)">›</span>' : ''}<span class="pill2">${esc(t)}<button data-bi="unf:${k}" aria-label="Remove filter">✕</button></span>`).join('')}<button class="xbtn" data-bi="reset" style="padding:3px 8px;font-size:12px">Clear all</button></div>` : ''}</div>
   <div class="stitle" style="margin-top:6px">Practice at a glance</div>
   <div class="kpis">
    ${kpi('acc', 'Right on first try', A.acc == null ? '—' : A.acc + '%', `${A.ok} of ${A.n} · ${prevTxt}`, badge(A.acc, P && P.acc, ' pts'), perDay.map(x => x.acc), HC.navy)}
    ${kpi('n', 'Questions answered', A.n.toLocaleString(), prevTxt, badge(A.n, P && P.n), perDay.map(x => x.n), HC.blue)}
    ${kpi('time', 'Avg time per question', mmss(A.secs), A.pace ? `SAT pace ${mmss(A.pace)} · HELM only` : 'HELM only', badge(A.secs, P && P.secs, 's', true), perDay.map(x => x.secs), HC.steel)}
    ${(() => { const SS = superscore(); return kpi('proj', 'Projected SAT', pjNow.total.toLocaleString(), `vs. best superscore ${SS.total.toLocaleString()} · Math ${pjNow.Math} · R&W ${pjNow['R&W']}`, badge(pjNow.total, SS.total), pjSpark, HC.green) })()}
   </div>
   <div class="t2">
    <section class="bc" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap"><div><div class="ch"><b>Questions and accuracy over time</b></div><div class="ch2">% right on the first try vs. the 75% goal · gray bars = questions answered · click a point to filter that ${BI.gran}</div></div>
     <div class="seg">${['day', 'week', 'month'].map(g => `<button class="${BI.gran === g ? 'on' : ''}" data-bi="gran:${g}">${({day: 'Daily', week: 'Weekly', month: 'Monthly'})[g]}</button>`).join('')}</div></div><div style="height:300px;margin-top:8px"><canvas id="bi-t"></canvas></div></section>
    <section class="bc" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><div><div class="ch"><b>Accuracy by ${lvName.toLowerCase()}</b></div><div class="ch2">${lv === 'diff' ? 'HELM only (Blueprint has no difficulty)' : 'Weakest first · click a row to drill in: Section › Domain › Skill › Difficulty'}</div></div>
     ${lv !== 'sec' ? `<button class="xbtn" data-bi="back">← Back to ${BI_LEVELS[BI_LEVELS.findIndex(x => x[0] === lv) - 1][1]}</button>` : ''}</div><div id="bi-rk-wrap"></div></section>
   </div>
   <div class="stitle">Skills</div>
   <section class="bc" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px"><div class="ch"><b>Every skill</b></div>
     <div class="ch2">Click a header to sort · click a row to see its questions · <b>Points at stake</b> = SAT points still being lost in that skill (share of section × % wrong × 600)</div></div>
    <div style="margin-top:12px"><input class="srch" id="bi-pq" placeholder="Search skills" value="${esc(BI.pq)}" autocomplete="off"></div><div style="overflow:auto;max-height:560px;margin-top:10px" id="bi-pv"></div></section>
   <div class="stitle">Help and tutor</div>
   <div class="bi-help">${BI.src.helm ? helpSection(null, rg) : ''}</div>
   <section class="bc" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px"><div class="ch"><b>What he asked the tutor</b></div>
     <div style="font-size:13px;color:var(--mu)">Every question Patrick took to "Ask the tutor" in this date range, with his exact words · whether he got it right after, and how he did on new questions of that skill afterwards (first try, no help) · the nightly plan uses these to add look-alike questions and a new explanation the next two days</div></div><div id="bi-tutor" style="margin-top:8px;color:var(--mu);font-size:14px">Loading…</div></section>
   <div class="stitle">Day by day</div>
   <section class="bc" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px"><div class="ch"><b>Day by day: Blueprint and HELM</b></div>
     <div style="font-size:13px;color:var(--mu)">First tries only · click a day to filter the whole page</div></div><div style="overflow:auto;margin-top:8px" id="bi-days"></div></section>
   <div class="stitle">Scores and projection</div>${scoresBlock()}
  </div><div id="bi-drw"></div></div>`;
  biTrend(rows); biRank(rows, lv); biDaysTable(R); biPivot(R, rg); if (BI.drawer) biOpen(BI.drawer, true);
  scoresChart(); biTutor(rg)
}

function biColors() { return BI.dark ? {tick: '#94a3b8', grid: '#1e293b'} : {tick: '#64748b', grid: '#eef2f7'} }
function biTrend(rows) {
  const g = BI.gran, dated = rows.filter(r => r.date), keys = [...new Set(dated.map(r => biBucket(r.date, g)))].sort(), C = biColors();
  const lab = k => g === 'month' ? new Date(k + '-15T12:00').toLocaleDateString('en-US', {month: 'short', year: 'numeric'}) : (g === 'week' ? 'wk ' : '') + new Date(k + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'});
  const sum = (k, f) => dated.filter(r => biBucket(r.date, g) === k && f(r)).reduce((a, r) => a + r.n, 0);
  const acc = k => biAgg(dated.filter(r => biBucket(r.date, g) === k)).acc;
  const qn = keys.map(k => sum(k, () => true)), aAll = keys.map(acc);
  const aM = keys.map(k => biAgg(dated.filter(r => biBucket(r.date, g) === k && r.sec === 'Math')).acc), aE = keys.map(k => biAgg(dated.filter(r => biBucket(r.date, g) === k && r.sec === 'Reading & Writing')).acc);
  const grad = c => { const {ctx, chartArea: a} = c.chart; if (!a) return 'rgba(37,99,235,.12)'; const gr = ctx.createLinearGradient(0, a.top, 0, a.bottom); gr.addColorStop(0, 'rgba(37,99,235,.22)'); gr.addColorStop(1, 'rgba(37,99,235,0)'); return gr };
  chart('bi-t', {data: {labels: keys.map(lab), datasets: [
    {type: 'line', label: 'Overall % right', data: aAll, borderColor: HC.blue, backgroundColor: grad, fill: 'origin', borderWidth: 2.5, cubicInterpolationMode: 'monotone', pointRadius: aAll.length > 20 ? 0 : 3, pointBackgroundColor: HC.blue, yAxisID: 'y2', order: 1, spanGaps: true},
    {type: 'line', label: 'Math', data: aM, borderColor: HC.navy, borderWidth: 1.75, cubicInterpolationMode: 'monotone', pointRadius: 0, yAxisID: 'y2', order: 2, spanGaps: true},
    {type: 'line', label: 'Reading & Writing', data: aE, borderColor: HC.gold, borderWidth: 1.75, cubicInterpolationMode: 'monotone', pointRadius: 0, yAxisID: 'y2', order: 2, spanGaps: true},
    {type: 'line', label: 'Goal 75% (≈1300)', data: keys.map(() => 75), borderColor: '#A1A1AA', borderDash: [5, 5], borderWidth: 1.25, pointRadius: 0, yAxisID: 'y2', order: 3},
    {type: 'bar', label: 'Questions', data: qn, backgroundColor: BI.dark ? 'rgba(161,161,170,.18)' : 'rgba(161,161,170,.22)', borderRadius: 3, yAxisID: 'y', order: 4, maxBarThickness: 28}]},
    options: {maintainAspectRatio: false, interaction: {mode: 'index', intersect: false},
      plugins: {legend: {position: 'top', align: 'end', labels: {color: C.tick, usePointStyle: true, pointStyle: 'line', boxWidth: 18, font: {size: 12}}}, tooltip: {enabled: false, external: biGlassTip(i => {
        const pv = i > 0 ? aAll[i - 1] : null, d = aAll[i] != null && pv != null ? aAll[i] - pv : null;
        return {title: keys.map(lab)[i], rows: [['Overall % right', aAll[i] == null ? '—' : aAll[i] + '%', HC.blue], ['Math', aM[i] == null ? '—' : aM[i] + '%', HC.navy], ['Reading & Writing', aE[i] == null ? '—' : aE[i] + '%', HC.gold], ['Questions', qn[i], '#A1A1AA']],
          foot: d == null ? '' : `${d >= 0 ? '▲' : '▼'} ${Math.abs(d)} pts vs. previous ${g}`, good: d >= 0} })}},
      scales: {x: {ticks: {color: C.tick, maxRotation: 0, autoSkip: true}, grid: {display: false}}, y: {position: 'right', beginAtZero: true, ticks: {color: C.tick, precision: 0}, grid: {display: false}, title: {display: true, text: 'Questions', color: C.tick, font: {size: 11}}},
        y2: {position: 'left', min: 0, max: 100, ticks: {color: C.tick, callback: v => v + '%', stepSize: 25}, grid: {color: BI.dark ? 'rgba(63,63,70,.4)' : 'rgba(161,161,170,.4)'}, border: {display: false, dash: [3, 3]}}},
      onClick: (e, els) => { if (!els.length) return; const k = keys[els[0].index]; BI.f.date = k; BI.f.dateG = g; BI.f.dateL = lab(k); setTimeout(drawStats) }}})
}
// glassmorphism tooltip (HTML, follows the cursor inside the card)
function biGlassTip(build) {
  return ({chart: c, tooltip: tp}) => {
    const host = c.canvas.parentNode; host.style.position = 'relative'; let el = host.querySelector('.gtip');
    if (!el) { el = document.createElement('div'); el.className = 'gtip'; host.appendChild(el) }
    if (tp.opacity === 0 || !tp.dataPoints || !tp.dataPoints.length) { el.style.opacity = 0; return }
    const d = build(tp.dataPoints[0].dataIndex);
    el.innerHTML = `<div class="tt">${esc(d.title)}</div>${d.rows.map(([n, v, c]) => `<div class="rw"><span><i style="background:${c}"></i>${esc(n)}</span><b>${v}</b></div>`).join('')}${d.foot ? `<div style="margin-top:6px;font-weight:600;color:${d.good ? '#047857' : '#BE123C'}">${d.foot}</div>` : ''}`;
    el.style.opacity = 1; const x = tp.caretX + 14, w = el.offsetWidth; el.style.left = (x + w > host.clientWidth ? tp.caretX - w - 14 : x) + 'px'; el.style.top = Math.max(0, tp.caretY - 20) + 'px'
  }
}
const BI_LBL = {id: 'bilbl', afterDatasetsDraw(c) { const ctx = c.ctx, ds = c.data.datasets[0], meta = c.getDatasetMeta(0); ctx.save(); ctx.font = '600 12px system-ui'; ctx.textBaseline = 'middle';
  meta.data.forEach((bar, i) => { const t = c.data.extra[i]; ctx.fillStyle = BI.dark ? '#e2e8f0' : '#0f172a'; ctx.fillText(t, Math.min(bar.x + 6, c.chartArea.right - ctx.measureText(t).width - 2), bar.y) }); ctx.restore() }};
function biRank(rows, lv) {
  // when Blueprint skill totals are in play, use them (not the day totals) so Blueprint is never counted twice
  if (rows.some(r => r.kind === 'skill')) rows = rows.filter(r => r.kind !== 'daily');
  const items = lv === 'diff' ? rows.filter(r => r.src === 'HELM') : rows, grp = {};
  items.forEach(r => { (grp[r[lv]] = grp[r[lv]] || []).push(r) });
  let ks = Object.keys(grp).map(k => ({k, ...biAgg(grp[k])})).filter(x => x.n);
  if (lv === 'diff') ks.sort((a, b) => 'EasyMediumHard'.indexOf(a.k) - 'EasyMediumHard'.indexOf(b.k)); else ks.sort((a, b) => (a.acc ?? 0) - (b.acc ?? 0));
  const wrap = document.getElementById('bi-rk-wrap'); if (!wrap) return;
  if (!ks.length) { wrap.innerHTML = '<div style="color:var(--mu);padding:20px 0;font-size:13px">No questions in this range yet.</div>'; return }
  const col = x => x.acc >= 70 ? HC.green : x.acc >= 50 ? HC.amber : HC.rose, tot = ks.reduce((a, x) => a + x.n, 0);
  BI.rk = ks.map(x => x.k);
  wrap.innerHTML = `<div class="rk">${ks.map((x, i) => `<div class="it" data-bi="rank:${i}" title="${lv === 'diff' ? 'See these questions' : 'Drill into ' + esc(x.k)}"><div class="nm"><span class="dot" style="background:${col(x)}"></span>${esc(x.k)}</div><div class="val">${x.acc}%<span>${x.ok}/${x.n} · ${Math.round(100 * x.n / tot)}%</span></div><div class="tr"><i style="width:${Math.max(2, x.acc)}%;background:${col(x)}"></i></div></div>`).join('')}</div>
   <div class="ch2" style="margin-top:12px"><span class="dot" style="background:${HC.green}"></span>70%+ <span class="dot" style="background:${HC.amber};margin-left:10px"></span>50–69% <span class="dot" style="background:${HC.rose};margin-left:10px"></span>under 50% · right side = right/asked · share of questions</div>`;
  BI.rkLv = lv
}
// ---------- per-skill trend (all-time HELM first tries for one skill) ----------
function biSkillTrend(R, skill, gran) {
  const sk = Object.values(SK2).find(x => x.name === skill), id = sk && sk.id, useBp = BI.src.bp && id;
  const h = R.filter(r => r.src === 'HELM' && r.skill === skill && r.date).map(r => ({date: r.date, ok: r.ok, src: 'HELM'}));
  // Blueprint: per-question records from the daily report PDFs (BPI), plus Aug 31–Oct 31 = Blueprint's Aug 31–Nov 7 skill total minus the Nov 1–7 questions it itemizes
  const bi = useBp && typeof BPI !== 'undefined' ? BPI.filter(x => x.skill === id).map(x => ({date: x.day, ok: x.ok, src: 'Blueprint'})) : [];
  const hist = useBp && typeof BPH !== 'undefined' && BPH[id] ? BPH[id] : null, pre = bi.filter(x => x.date <= '2026-11-07');
  const early0 = hist ? {lab: 'BP Aug 31–Oct 31', n: hist.n - pre.length, ok: Math.max(0, hist.ok - pre.filter(x => x.ok).length)} : null;
  const bpp = early0 && early0.n > 0 ? [Object.assign(early0, {acc: Math.round(100 * Math.min(early0.ok, early0.n) / early0.n)})] : [];
  const all = [...bi, ...h].sort((x, y) => x.date < y.date ? -1 : x.date > y.date ? 1 : (x.src === 'Blueprint' ? -1 : 1));
  const days = new Set(all.map(r => r.date)).size, g = gran || (days > 14 ? 'week' : 'day');
  const keys = [...new Set(all.map(r => biBucket(r.date, g)))].sort();
  const lab = k => (g === 'week' ? 'wk ' : '') + new Date(k + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'});
  const agg = (k, src) => { const x = all.filter(r => biBucket(r.date, g) === k && (!src || r.src === src)); return {n: x.length, acc: x.length ? Math.round(100 * x.filter(r => r.ok).length / x.length) : null} };
  let run = 0, ok = 0; const cum = [];
  bpp.forEach(p => { run += p.n; ok += Math.min(p.ok, p.n); cum.push(Math.round(100 * ok / run)) });
  keys.forEach(k => { all.filter(r => biBucket(r.date, g) === k).forEach(r => { run++; ok += r.ok }); cum.push(Math.round(100 * ok / run)) });
  const pad = bpp.map(() => null), n = all.length, m = Math.max(3, Math.floor(n / 3));
  const span = rs => { const f = d => new Date(d + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'}), a = rs[0].date, z = rs[rs.length - 1].date; return a === z ? f(a) : f(a) + '–' + f(z) };
  const part = rs => ({acc: Math.round(100 * rs.filter(r => r.ok).length / rs.length), n: rs.length, lab: `${rs.length} Qs ${span(rs)}`});
  const first = n >= 6 ? part(all.slice(0, m)) : null, last = n >= 6 ? part(all.slice(-m)) : n >= 3 ? part(all) : null;
  const startP = bpp.length ? {lab: 'Blueprint Aug 31–Oct 31 (' + bpp[0].n + ' Qs)', acc: bpp[0].acc} : first ? {lab: 'first ' + first.lab, acc: first.acc} : null;
  const endP = last ? {lab: (n >= 6 ? 'last ' : 'all ') + last.lab, acc: last.acc} : null;
  const hh = h.length >= 6 ? [part(h.slice(0, Math.max(3, Math.floor(h.length / 3)))), part(h.slice(-Math.max(3, Math.floor(h.length / 3))))] : null;
  return {g, nb: bpp.length, nbi: bi.length, n, nh: h.length, lab: [...bpp.map(p => p.lab), ...keys.map(lab)],
    early: bpp.map(p => p.acc).concat(keys.map(() => null)), bpAcc: [...pad, ...keys.map(k => agg(k, 'Blueprint').acc)], acc: [...pad, ...keys.map(k => agg(k, 'HELM').acc)],
    all: [...bpp.map(p => p.acc), ...keys.map(k => agg(k).acc)], cntB: [...bpp.map(p => p.n), ...keys.map(k => agg(k, 'Blueprint').n)], cntH: [...pad.map(() => 0), ...keys.map(k => agg(k, 'HELM').n)],
    cum, startP, endP, chg: startP && endP ? endP.acc - startP.acc : null, hh}
}
function biTrendBlock(skill) {
  const T = biSkillTrend(biRecords(), skill, BI.tgran), chg = c => c == null ? '' : `<span class="badge ${c > 0 ? 'up' : c < 0 ? 'dn' : 'eq'}">${c > 0 ? '▲' : c < 0 ? '▼' : '±'} ${Math.abs(c)} pts</span>`;
  if (!T.n && !T.nb) return `<div class="trd"><div class="lab">Trend over time</div><div style="color:var(--mu);font-size:14px;margin-top:4px">No HELM or Blueprint questions in this skill yet.</div></div>`;
  return `<div class="trd"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><div><div class="lab">Trend over time · Blueprint + HELM · all time</div>
    <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:4px;font-size:14px">
    ${T.chg != null ? `<span>${esc(T.startP.lab)} <b>${T.startP.acc}%</b> → ${esc(T.endP.lab)} <b>${T.endP.acc}%</b> ${chg(T.chg)}</span>` : `<span style="color:var(--mu)">Not enough questions yet to show a change</span>`}
    ${T.hh ? `<span style="color:var(--mu)">HELM only: ${T.hh[0].acc}% → ${T.hh[1].acc}% ${chg(T.hh[1].acc - T.hh[0].acc)}</span>` : ''}</div>
    <div style="font-size:12px;color:var(--mu);margin-top:2px">${T.nbi} Blueprint + ${T.nh} HELM questions with dates${T.nb ? ' · first point = Blueprint Aug 31–Oct 31 total' : ''} · Blueprint course quizzes have no skill tag; Nov 8 & 12 reports not in Drive</div></div>
    ${T.n ? `<div class="seg">${['day', 'week'].map(g => `<button class="${T.g === g ? 'on' : ''}" data-bi="tgran:${g}">${g === 'day' ? 'Daily' : 'Weekly'}</button>`).join('')}</div>` : ''}</div>
    <div style="height:230px;margin-top:8px"><canvas id="bi-tc"></canvas></div></div>`
}
function biTrendChart(skill) {
  if (BI.tc) { try { BI.tc.destroy() } catch (x) {} BI.tc = null }
  const el = document.getElementById('bi-tc'); if (!el || typeof Chart === 'undefined') return;
  const T = biSkillTrend(biRecords(), skill, BI.tgran), C = biColors();
  const dot = a => a == null ? HC.steel : a >= 70 ? HC.green : a >= 50 ? HC.amber : HC.rose;
  BI.tc = new Chart(el, {data: {labels: T.lab, datasets: [
    {type: 'bar', label: 'Blueprint Qs', data: T.cntB, backgroundColor: BI.dark ? '#334155' : '#cbd5e1', borderRadius: 4, stack: 'q', yAxisID: 'y2', order: 3},
    {type: 'bar', label: 'HELM Qs', data: T.cntH, backgroundColor: BI.dark ? '#1e3a5f' : '#dbe4f0', borderRadius: 4, stack: 'q', yAxisID: 'y2', order: 3},
    ...(T.nb ? [{type: 'line', label: 'Blueprint Aug 31–Oct 31', data: T.early, borderColor: HC.steel, backgroundColor: T.early.map(dot), pointStyle: 'rectRot', pointRadius: 9, showLine: false, yAxisID: 'y', order: 1}] : []),
    ...(T.nbi ? [{type: 'line', label: 'Blueprint % right', data: T.bpAcc, borderColor: HC.steel, borderDash: [5, 4], backgroundColor: T.bpAcc.map(dot), pointStyle: 'rectRot', pointRadius: 7, pointHoverRadius: 9, borderWidth: 2, spanGaps: true, yAxisID: 'y', order: 1}] : []),
    ...(T.nh ? [{type: 'line', label: 'HELM % right', data: T.acc, borderColor: HC.navy, backgroundColor: T.acc.map(dot), pointRadius: 6, pointHoverRadius: 8, borderWidth: 2, tension: .3, spanGaps: true, yAxisID: 'y', order: 1}] : []),
    {type: 'line', label: 'Running total %', data: T.cum, borderColor: HC.gold, borderWidth: 2, borderDash: [4, 3], pointRadius: 0, tension: .3, yAxisID: 'y', order: 2},
    {type: 'line', label: 'Goal 75%', data: T.lab.map(() => 75), borderColor: HC.green, borderDash: [6, 6], borderWidth: 1.5, pointRadius: 0, yAxisID: 'y', order: 5}]},
    options: {maintainAspectRatio: false, interaction: {mode: 'index', intersect: false},
      plugins: {legend: {position: 'bottom', labels: {color: C.tick, boxWidth: 14, font: {size: 11}}}, tooltip: {callbacks: {label: c => c.dataset.label + ': ' + c.raw + (c.dataset.yAxisID === 'y' ? '%' : '')}}},
      scales: {y: {min: 0, max: 100, ticks: {color: C.tick, callback: v => v + '%'}, grid: {color: C.grid}}, y2: {position: 'right', stacked: true, beginAtZero: true, ticks: {color: C.tick, precision: 0}, grid: {drawOnChartArea: false}, title: {display: true, text: 'Qs', color: C.tick}}, x: {stacked: true, ticks: {color: C.tick}, grid: {display: false}}}}})
}
function biPivot(R, rg) {
  const rows = biFilter(R, rg).filter(r => r.kind !== 'daily' && (!BI.pq || r.skill.toLowerCase().includes(BI.pq.toLowerCase()))), pr = biPrevRange(), prev = pr ? biFilter(R, pr, {dated: true}).filter(r => r.kind !== 'daily') : [], g = {};
  rows.forEach(r => { (g[r.skill] = g[r.skill] || []).push(r) });
  const list = Object.keys(g).map(k => { const a = biAgg(g[k]), h = biAgg(g[k].filter(r => r.src === 'HELM')), b = biAgg(g[k].filter(r => r.src === 'Blueprint')), r0 = g[k][0], pa = biAgg(prev.filter(r => r.skill === k));
    const dm = ['Easy', 'Medium', 'Hard'].map(d => { const x = g[k].filter(r => r.diff === d); return [d, x.length, x.filter(r => r.ok).length] });
    return {dm, skill: k, sec: r0.sec, dom: r0.dom, share: r0.share || 0, n: a.n, ok: a.ok, wrong: a.wrong, acc: a.acc, helm: h.acc, bp: b.acc, secs: a.secs, pace: a.pace, chg: pa.acc != null && a.acc != null ? a.acc - pa.acc : null, lost: a.acc == null ? 0 : Math.round(600 * (r0.share || 0) / 100 * (100 - a.acc) / 100), ...(t => ({trend: t.chg, tsp: spark(t.all, (t.chg ?? 0) >= 0 ? HC.green : HC.rose)}))(biSkillTrend(R, k)), ...(id => ({bp: BI.src.bp && id && BPS[id] && BPS[id].n ? Math.round(100 * BPS[id].ok / BPS[id].n) : null, bpn: id && BPS[id] ? BPS[id].n : 0}))(r0.skillId)} });
  const S = BI.sort; list.sort((a, b) => { const x = a[S.k], y = b[S.k]; if (x == null) return 1; if (y == null) return -1; return (typeof x === 'string' ? x.localeCompare(y) : x - y) * S.d });
  const maxLost = Math.max(1, ...list.map(x => x.lost));
  const H = [['skill', 'Skill'], ['sec', 'Section'], ['share', '% of section'], ['n', 'Qs'], ['ok', 'Right'], ['wrong', 'Wrong'], ['acc', 'Accuracy'], ['helm', 'HELM'], ['bp', 'Blueprint (all)'], ['chg', 'vs. prev.'], ['trend', 'Trend (all time)'], ['dm', 'Difficulty (right / asked)'], ['secs', 'Avg time'], ['lost', 'Points at stake'], ['go', '']];
  const el = document.getElementById('bi-pv'); if (!el) return;
  if (!list.length) { el.innerHTML = '<div style="color:var(--mu);padding:16px 0">No skill-level records in this range. (Blueprint skill totals appear when the range covers Aug 31–Nov 20, e.g. All time.)</div>'; return }
  const accCol = a => a == null ? HC.steel : a >= 70 ? HC.green : a >= 50 ? HC.amber : HC.rose;
  el.innerHTML = `<table class="pv"><thead><tr>${H.map(([k, t]) => k === 'go' || k === 'dm' ? `<th>${t}</th>` : `<th data-bi="sort:${k}">${t}${S.k === k ? (S.d > 0 ? ' ▲' : ' ▼') : ''}</th>`).join('')}</tr></thead><tbody>${list.map(x => `<tr data-bi="row:${esc(x.skill)}" style="cursor:pointer" title="See every question in this skill">
    <td class="c" data-bi="row:${esc(x.skill)}"><span class="dot" style="background:${accCol(x.acc)}" title="${x.acc == null ? 'no data' : x.acc >= 70 ? 'Strong' : x.acc >= 50 ? 'Getting there' : 'Needs work'}"></span><b>${esc(x.skill)}</b><div style="font-size:12px;color:var(--mu);margin-left:15px">${esc(x.dom)}</div></td><td>${x.sec === 'Reading & Writing' ? 'R&W' : x.sec}</td><td>${x.share ? Math.round(x.share) + '%' : '—'}</td>
    <td class="c" data-bi="row:${esc(x.skill)}">${x.n}</td><td class="c" data-bi="row:${esc(x.skill)}|ok" style="color:var(--up);font-weight:700">${x.ok}</td><td class="c" data-bi="row:${esc(x.skill)}|wrong" style="color:var(--dn);font-weight:700">${x.wrong}</td>
    <td class="cb c" data-bi="row:${esc(x.skill)}"><i style="width:${x.acc ?? 0}%;background:${accCol(x.acc)}"></i><span style="color:${accCol(x.acc)}">${x.acc == null ? '—' : x.acc + '%'}</span></td>
    <td>${x.helm == null ? '—' : x.helm + '%'}</td><td title="Blueprint, Aug 31–Nov 20 (no dates)">${x.bp == null ? '—' : x.bp + '% <span style="color:var(--mu);font-size:12px">(' + x.bpn + ')</span>'}</td><td>${x.chg == null ? '—' : `<span style="color:${x.chg >= 0 ? 'var(--up)' : 'var(--dn)'};font-weight:700">${x.chg > 0 ? '▲' : x.chg < 0 ? '▼' : ''} ${Math.abs(x.chg)}</span>`}</td>
    <td>${x.dm.filter(d => d[1]).length ? x.dm.filter(d => d[1]).map(([d, n, ok]) => `<span class="badge" style="margin-right:4px;background:${d === 'Easy' ? '#dcfce7' : d === 'Medium' ? '#FFEDD5' : '#fee2e2'};color:${d === 'Easy' ? '#166534' : d === 'Medium' ? '#92400e' : '#991b1b'}">${d[0]} ${ok}/${n}</span>`).join('') : '<span style="color:var(--mu);font-size:12px">Blueprint only</span>'}</td>
    <td>${x.secs == null ? '—' : `<span style="color:${x.secs > x.pace ? 'var(--dn)' : 'var(--up)'}">${mmss(x.secs)}</span>`}</td>
    <td class="cb"><i style="width:${100 * x.lost / maxLost}%;background:${HC.rose}"></i><span>${x.lost}</span></td><td><span class="xbtn" style="white-space:nowrap">Questions ›</span></td></tr>`).join('')}</tbody></table>`
}

// ---------- inspector drawer ----------
function biOpen(spec, keep) {
  BI.drawer = spec; if (!keep) { BI.dq = ''; }
  const R = biRecords(), rg = biRange(); let rows = biFilter(R, rg), title = 'Records behind this view';
  if (spec.t === 'kpi') { rows = biFilter(R, rg, {dated: true}); title = {acc: 'Right on first try', n: 'Questions answered', time: 'Time per question (HELM)', proj: 'Projected SAT: the records it uses'}[spec.k]; if (spec.k === 'time') rows = rows.filter(r => r.secs != null) }
  if (spec.t === 'row') { rows = rows.filter(r => r.skill === spec.skill); if (spec.only === 'ok') rows = rows.filter(r => r.ok === r.n); if (spec.only === 'wrong') rows = rows.filter(r => r.ok < r.n); title = spec.skill + (spec.only ? (spec.only === 'ok' ? ': right' : ': missed') : '') }
  const q = BI.dq.toLowerCase(); if (q) rows = rows.filter(r => [r.date, r.src, r.sec, r.dom, r.skill, r.diff, r.question, r.picked].join(' ').toLowerCase().includes(q));
  const S = BI.dsort; rows = rows.slice().sort((a, b) => { const x = a[S.k] ?? '', y = b[S.k] ?? ''; return (typeof x === 'number' && typeof y === 'number' ? x - y : String(x).localeCompare(String(y))) * S.d });
  BI.drows = rows; const A = biAgg(rows);
  const H = [['date', 'Date'], ['src', 'Source'], ['sec', 'Section'], ['skill', 'Skill'], ['diff', 'Diff.'], ['n', 'Qs'], ['ok', 'Right'], ['secs', 'Time'], ['question', 'Question']];
  const host = document.getElementById('bi-drw'); if (!host) return;
  host.innerHTML = `<div class="scrim" data-bi="close"></div><aside class="drw" role="dialog" aria-label="${esc(title)}"><div class="hd2"><div><div class="lab">Explore from here</div><div class="hd" style="font-size:20px;font-weight:800">${esc(title)}</div>
    ${(() => { const h = rows.filter(r => r.src === 'HELM'); if (!h.length) return ''; return `<div style="display:flex;gap:6px;margin:6px 0 2px;flex-wrap:wrap">${['Easy', 'Medium', 'Hard'].map(d => { const x = h.filter(r => r.diff === d); return `<span class="badge" style="background:${d === 'Easy' ? '#dcfce7' : d === 'Medium' ? '#FFEDD5' : '#fee2e2'};color:${d === 'Easy' ? '#166534' : d === 'Medium' ? '#92400e' : '#991b1b'}">${d}: ${x.filter(r => r.ok).length}/${x.length} right</span>` }).join('')}</div>` })()}
    <div style="font-size:13px;color:var(--mu)">${rows.length} records · ${A.n} questions · ${A.acc == null ? '—' : A.acc + '% right'}${Object.keys(BI.f).filter(k => BI_LEVELS.some(l => l[0] === k) || k === 'date').length ? ' · dashboard filters applied' : ''}</div></div>
    <div style="display:flex;gap:8px"><button class="xbtn pr" data-bi="csv">⬇ Export to CSV</button><button class="xbtn" data-bi="close" aria-label="Close">✕</button></div></div>
    ${spec.t === 'row' ? biTrendBlock(spec.skill) : ''}
    <div style="padding:10px 18px;border-bottom:1px solid var(--bd)"><input id="bi-dq" placeholder="Search records (skill, date, question text…)" value="${esc(BI.dq)}" style="width:100%;font:inherit;padding:9px 12px;border:1px solid var(--bd);border-radius:10px;background:var(--card);color:var(--tx)"></div>
    <div class="bd"><table class="pv"><thead><tr>${H.map(([k, t]) => `<th data-bi="dsort:${k}">${t}${S.k === k ? (S.d > 0 ? ' ▲' : ' ▼') : ''}</th>`).join('')}</tr></thead><tbody>
    ${rows.slice(0, 500).map((r, i) => `<tr${r.qid ? ` class="c" data-bi="dq:${i}" style="cursor:pointer"` : ''}><td>${r.date ? (r.week ? 'Week of ' + r.date : r.date) : 'Aug 31–Nov 20'}</td><td>${r.src}${r.kind === 'skill' ? ' <span style="color:var(--mu);font-size:12px">(skill total)</span>' : r.kind === 'daily' ? ` <span style="color:var(--mu);font-size:12px">(${r.week ? 'week' : 'day'} total)</span>` : ''}</td><td>${r.sec === 'Reading & Writing' ? 'R&W' : r.sec}</td><td>${esc(r.skill)}</td><td>${r.diff}</td><td>${r.n}</td>
      <td style="font-weight:700;color:${r.ok === r.n ? 'var(--up)' : r.ok === 0 ? 'var(--dn)' : 'var(--tx)'}">${r.n === 1 ? (r.ok ? '✓' : '✗') : r.ok}</td><td>${r.secs == null ? '—' : mmss(r.secs)}</td><td style="white-space:normal;min-width:240px;font-size:13px">${r.question ? esc(r.question.slice(0, 120)) + (r.question.length > 120 ? '…' : '') : '<span style="color:var(--mu)">not itemized by Blueprint</span>'}</td></tr>
      ${r.qid && BI.dopen === i ? `<tr><td colspan="9" style="white-space:normal;background:var(--hv)"><div style="display:grid;gap:6px;padding:4px 0"><div><b style="color:var(--dn)">He picked:</b> ${r.picked || '(not recorded)'} &nbsp; <b style="color:var(--up)">Right answer:</b> ${r.answer}</div>
        <div style="font-size:13px">${(QBY[r.qid].steps || []).map((s, j) => (j + 1) + '. ' + esc(s)).join('<br>')}</div>${r.trap ? `<div style="font-size:13px"><b style="color:var(--dn)">Trap:</b> ${esc(r.trap)}</div>` : ''}<div><button class="btn sm" data-go="#/drill/ids:${r.qid}">Try it again</button></div></div></td></tr>` : ''}`).join('')}
    </tbody></table>${rows.length > 500 ? `<div style="padding:10px 18px;color:var(--mu)">Showing the first 500. Export to CSV for all ${rows.length}.</div>` : ''}${!rows.length ? '<div style="padding:18px;color:var(--mu)">No records match.</div>' : ''}</div></aside>`;
  requestAnimationFrame(() => { const d = host.querySelector('.drw'); if (d) d.classList.add('open') });
  if (spec.t === 'row') biTrendChart(spec.skill); else if (BI.tc) { try { BI.tc.destroy() } catch (x) {} BI.tc = null }
  const inp = document.getElementById('bi-dq'); if (inp && keep && BI.dfocus) { inp.focus(); inp.setSelectionRange(inp.value.length, inp.value.length) }
}
function biCsv() {
  const cols = ['date', 'src', 'sec', 'dom', 'skill', 'diff', 'n', 'ok', 'secs', 'qid', 'question', 'picked', 'answer'], q = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const csv = [cols.join(',')].concat((BI.drows || []).map(r => cols.map(c => q(c === 'date' && !r.date ? 'Aug 31-Nov 20 (Blueprint skill total)' : r[c])).join(','))).join('\n');
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], {type: 'text/csv'})); a.download = `helm-stats-${dkey(new Date())}.csv`; document.body.appendChild(a); a.click(); a.remove()
}

document.addEventListener('click', e => {
  const t = e.target.closest('[data-bi]'); if (!t || !document.getElementById('bi')) return; const [a, ...rest] = t.dataset.bi.split(':'), v = rest.join(':');
  if (a === 'src') { BI.src[v] = !BI.src[v]; if (!BI.src.helm && !BI.src.bp) BI.src[v === 'bp' ? 'helm' : 'bp'] = true; return drawStats() }
  if (a === 'reset') { BI.f = {}; BI.range = 'today'; BI.src = {helm: true, bp: true}; BI.drawer = null; return drawStats() }
  if (a === 'dark') { BI.dark = !BI.dark; try { localStorage.setItem('bi_dark', BI.dark ? '1' : '') } catch (x) {} return drawStats() }
  if (a === 'gran') { BI.gran = v; return drawStats() }
  if (a === 'unf') { if (v === 'date') { delete BI.f.date; delete BI.f.dateG; delete BI.f.dateL } else { const i = BI_LEVELS.findIndex(x => x[0] === v); BI_LEVELS.slice(i).forEach(([k]) => delete BI.f[k]) } return drawStats() }
  if (a === 'back') { const lv = biLevel(), i = BI_LEVELS.findIndex(x => x[0] === lv); delete BI.f[BI_LEVELS[i - 1][0]]; return drawStats() }
  if (a === 'sort') { BI.sort = {k: v, d: BI.sort.k === v ? -BI.sort.d : (v === 'skill' || v === 'sec' ? 1 : -1)}; return biPivot(biRecords(), biRange()) }
  if (a === 'kpi') { BI.dopen = null; return biOpen({t: 'kpi', k: v}) }
  if (a === 'row') { BI.dopen = null; const [sk, only] = v.split('|'); return biOpen({t: 'row', skill: sk, only}) }
  if (a === 'close') { BI.drawer = null; BI.dopen = null; const d = document.querySelector('#bi-drw .drw'); if (d) d.classList.remove('open'); setTimeout(() => { const h = document.getElementById('bi-drw'); if (h && !BI.drawer) h.innerHTML = '' }, 220); return }
  if (a === 'csv') return biCsv();
  if (a === 'cmp') { BI.cmp = !BI.cmp; return drawStats() }
  if (a === 'rank') { const k = (BI.rk || [])[+v]; if (k == null) return; if (BI.rkLv === 'diff') { BI.f.diff = k; return biOpen({t: 'filter'}) } BI.f[BI.rkLv] = k; return drawStats() }
  if (a === 'export') { BI.drows = biFilter(biRecords(), biRange()); return biCsv() }
  if (a === 'share') { const u = location.href; const done = () => { const d = document.createElement('div'); d.className = 'toast'; d.textContent = 'Link copied'; document.getElementById('bi').appendChild(d); setTimeout(() => d.remove(), 1600) };
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(done, done); else done(); return }
  if (a === 'tgran') { BI.tgran = v; return biOpen(BI.drawer, true) }
  if (a === 'dsort') { BI.dsort = {k: v, d: BI.dsort.k === v ? -BI.dsort.d : 1}; return biOpen(BI.drawer, true) }
  if (a === 'dq') { BI.dopen = BI.dopen === +v ? null : +v; BI.dfocus = false; return biOpen(BI.drawer, true) }
}, true);
document.addEventListener('change', e => {
  if (!document.getElementById('bi')) return; const id = e.target.id;
  if (id === 'bi-range') { BI.range = e.target.value; if (BI.range === 'custom' && !BI.from) { const d = new Date(); d.setDate(d.getDate() - 13); BI.from = dkey(d); BI.to = dkey(new Date()) } drawStats() }
  if (id === 'bi-from') { BI.from = e.target.value; drawStats() } if (id === 'bi-to') { BI.to = e.target.value; drawStats() }
  if (id === 'bi-sec') { const v = e.target.value; ['sec', 'dom', 'skill', 'diff'].forEach(k => delete BI.f[k]); if (v) BI.f.sec = v; drawStats() }
}, true);
document.addEventListener('input', e => { if (e.target.id === 'bi-pq') { BI.pq = e.target.value; return biPivot(biRecords(), biRange()) } if (e.target.id === 'bi-dq') { BI.dq = e.target.value; BI.dfocus = true; biOpen(BI.drawer, true) } });
function biA11y() { document.querySelectorAll('#bi [data-bi]:not(button):not(select):not(input)').forEach(el => { if (!el.hasAttribute('tabindex')) { el.tabIndex = 0; if (!el.getAttribute('role')) el.setAttribute('role', 'button') } }) }
new MutationObserver(() => { if (document.getElementById('bi')) biA11y() }).observe(document.documentElement, {childList: true, subtree: true});
document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('#bi [data-bi]:not(button):not(select):not(input)')) { e.preventDefault(); e.target.click() } });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && BI.drawer && document.getElementById('bi')) { BI.drawer = null; const h = document.getElementById('bi-drw'); if (h) h.innerHTML = '' } });
try { BI.dark = !!localStorage.getItem('bi_dark') } catch (x) {}

function biDaysTable(R) {
  const el = document.getElementById('bi-days'); if (!el) return; const rg = biRange();
  const dated = biFilter(R, rg, {dated: true}), days = [...new Set(dated.map(r => r.date))].sort().reverse();
  if (!days.length) { el.innerHTML = '<div style="color:var(--mu)">No practice in this range yet.</div>'; return }
  const ft = firstTries(), cell = a => a.n ? `<b>${a.acc}%</b> <span style="color:var(--mu);font-size:12px">${a.ok}/${a.n}</span>` : '<span style="color:var(--mu)">—</span>';
  const bar = (p, c) => `<div style="display:flex;align-items:center;gap:6px"><div style="width:70px;height:8px;border-radius:4px;background:var(--hv);overflow:hidden"><div style="width:${p}%;height:100%;background:${c}"></div></div><span>${p}%</span></div>`;
  el.innerHTML = `<table class="pv"><thead><tr><th>Day</th><th>HELM</th><th>Blueprint</th><th>Combined</th><th>Hard questions (HELM)</th><th>Right with no help (HELM)</th><th>Avg time / Q (HELM)</th></tr></thead><tbody>${days.map(d => {
    const rows = dated.filter(r => r.date === d), h = biAgg(rows.filter(r => r.src === 'HELM')), b = biAgg(rows.filter(r => r.src === 'Blueprint')), c = biAgg(rows);
    const hx = rows.filter(r => r.src === 'HELM'), hard = hx.length ? Math.round(100 * hx.filter(r => r.diff === 'Hard').length / hx.length) : null;
    const nh = ft.filter(x => x.day === d && !(x.helpFirst || []).length), nhp = nh.length ? Math.round(100 * nh.filter(x => x.ok).length / nh.length) : null;
    const isWk = rows.some(r => r.week), lab = (isWk ? 'Week of ' : '') + new Date(d + 'T12:00').toLocaleDateString('en-US', {weekday: isWk ? undefined : 'short', month: 'short', day: 'numeric'});
    return `<tr data-bi="day:${d}|${lab}" style="cursor:pointer"><td><b>${lab}</b></td><td>${cell(h)}</td><td>${cell(b)}</td><td>${cell(c)}</td><td>${hard == null ? '—' : bar(hard, HC.navy)}</td><td>${nhp == null ? '—' : bar(nhp, nhp >= 70 ? HC.green : nhp >= 50 ? HC.amber : HC.rose)}</td><td>${h.secs == null ? '—' : `<span style="color:${h.secs > h.pace ? 'var(--dn)' : 'var(--up)'}">${mmss(h.secs)}</span> <span style="color:var(--mu);font-size:12px">/ ${mmss(h.pace)}</span>`}</td></tr>` }).join('')}</tbody></table>`
}
document.addEventListener('click', e => { const t = e.target.closest('[data-bi^="day:"]'); if (!t || !document.getElementById('bi')) return; const [d, lab] = t.dataset.bi.slice(4).split('|'); BI.f.date = d; BI.f.dateG = 'day'; BI.f.dateL = lab; if (BI.range !== 'all' && !(d >= biRange()[0] && d <= biRange()[1])) BI.range = 'all'; drawStats() }, true);

// ---------- Tutor questions (from Supabase tutor_messages; Patrick's own rows) ----------
async function biTutor(rg) {
  const el = document.getElementById('bi-tutor'); if (!el) return;
  if (!window.HELM_SB) { el.textContent = 'Sign in to see tutor questions.'; return }
  let q = window.HELM_SB.from('tutor_messages').select('question_id,skill,role,content,created_at').order('created_at', {ascending: true}).limit(2000);
  if (rg[0] !== '0000') q = q.gte('created_at', new Date(rg[0] + 'T00:00').toISOString());
  if (rg[1] !== '9999') q = q.lt('created_at', new Date(new Date(rg[1] + 'T00:00').getTime() + 864e5).toISOString());
  const {data, error} = await q; if (!document.getElementById('bi-tutor')) return;
  if (error) { el.textContent = 'Could not load tutor questions.'; return }
  const G = {}; (data || []).forEach(m => { const day = dkey(new Date(m.created_at)), k = day + '|' + (m.question_id || '?'); (G[k] = G[k] || {day, id: m.question_id, skill: m.skill, asks: [], replies: 0, t0: Infinity}); if (m.role === 'student') { G[k].asks.push(m.content); G[k].t0 = Math.min(G[k].t0, Date.parse(m.created_at)) } else G[k].replies++ });
  const L = Object.values(G).filter(g => g.asks.length).sort((a, b) => b.day.localeCompare(a.day));
  if (!L.length) { el.innerHTML = 'No tutor questions in this date range.'; return }
  // Results (Allie, Nov 23): did he get it right after asking, and how did he do on NEW questions of that skill afterwards (SAT rules: first try, no help)
  const FT = firstTries();
  L.forEach(g => { const q = QBY[g.id]; g.sk = q ? q.skill : null; const rows = LOG.filter(x => x.id === g.id);
    g.res = rows.some(x => x.ts > g.t0 && x.ok) ? 'after' : rows.some(x => x.ts < g.t0 && x.ok) ? 'before' : 'no';
    const nx = g.sk ? FT.filter(r => r.q.skill === g.sk && r.ts > g.t0 && r.id !== g.id) : []; g.an = nx.length; g.aok = nx.filter(r => r.ok).length });
  const bySk = {}; L.forEach(g => { const k = g.sk || g.skill || 'Unknown'; const b = bySk[k] = bySk[k] || {n: 0, t0: Infinity}; b.n++; b.t0 = Math.min(b.t0, g.t0) });
  const top = Object.entries(bySk).map(([k, b]) => { const r = FT.filter(x => x.q.skill === k), be = r.filter(x => x.ts < b.t0), af = r.filter(x => x.ts > b.t0); return [k, b.n, be.length, be.filter(x => x.ok).length, af.length, af.filter(x => x.ok).length] }).sort((a, b) => b[1] - a[1]);
  const pc = (a, n) => n ? Math.round(100 * a / n) + '%' : '—', cc = (a, n) => !n ? 'var(--mu)' : a / n < .5 ? '#b91c1c' : a / n < .7 ? '#b45309' : '#15803d';
  const skn = k => SK2[k] ? SK2[k].name : k;
  const resCell = g => g.res === 'after' ? '<b style="color:#15803d">✓ Right after tutor</b>' : g.res === 'before' ? '<span style="color:#15803d">✓ Already right</span>' : '<b style="color:#b91c1c">✗ Not solved yet</b>';
  const qt = id => { const x = QBY[id]; return x ? esc(plain(x.q).slice(0, 110)) + (plain(x.q).length > 110 ? '…' : '') : '' };
  el.innerHTML = `<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">${top.map(([k, n, bn, bok, an, aok]) => `<span class="pill2">${esc(skn(k))} · asked about ${n} question${n > 1 ? 's' : ''} · before tutor <b>${pc(bok, bn)}</b> → after <b style="color:${cc(aok, an)}">${pc(aok, an)}</b> <span style="opacity:.75">(${aok} of ${an} new, first try)</span></span>`).join('')}</div>
   <table class="bt" style="width:100%;border-collapse:collapse;font-size:14px;color:var(--tx)"><thead><tr><th style="text-align:left;padding:6px">Day</th><th style="text-align:left;padding:6px">Skill</th><th style="text-align:left;padding:6px">Question</th><th style="text-align:left;padding:6px">What Patrick asked</th><th style="text-align:left;padding:6px">This question</th><th style="text-align:left;padding:6px">Same skill after</th><th style="padding:6px"></th></tr></thead><tbody>
   ${L.map(g => `<tr style="border-top:1px solid var(--ln,#e2e8f0);vertical-align:top"><td style="padding:6px;white-space:nowrap">${new Date(g.day + 'T12:00').toLocaleDateString('en-US', {month: 'short', day: 'numeric'})}</td><td style="padding:6px">${esc(g.sk ? skn(g.sk) : (g.skill || ''))}</td><td style="padding:6px;max-width:280px">${qt(g.id)}</td>
     <td style="padding:6px">${g.asks.map(a => `<div style="margin-bottom:4px">“${esc(a)}”</div>`).join('')}<div style="font-size:12px;color:var(--mu)">${g.asks.length} message${g.asks.length > 1 ? 's' : ''} · ${g.replies} tutor repl${g.replies === 1 ? 'y' : 'ies'}</div></td>
     <td style="padding:6px;white-space:nowrap">${resCell(g)}</td><td style="padding:6px;white-space:nowrap">${g.an ? `<b style="color:${cc(g.aok, g.an)}">${g.aok} of ${g.an}</b> right <div style="font-size:12px;color:var(--mu)">new questions, first try, no help</div>` : '<span style="color:var(--mu)">none yet</span>'}</td>
     <td style="padding:6px">${g.id && QBY[g.id] ? `<a href="#/drill/ids:${encodeURIComponent(g.id)}">Open</a>` : ''}</td></tr>`).join('')}</tbody></table>`;
}
