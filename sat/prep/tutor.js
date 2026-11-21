/* ---------- SAT HELM: sign-in + "Ask the tutor" live chat ----------
   Backend (already live in Supabase project sat-prep): auth user, helm_members, tutor_messages, Edge Function tutor-chat.
   The Claude API key lives only in Supabase secrets; the site never sees it. */
(function () {
  const css = document.createElement('style');
  css.textContent = `
  .tl-card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.08);padding:28px;width:min(400px,92vw);display:flex;flex-direction:column;gap:12px}
  .tl-card label{font-size:13px;font-weight:600;color:#334155}.tl-card input{font:inherit;font-size:16px;padding:11px 12px;border:1px solid #cbd5e1;border-radius:10px;width:100%;box-sizing:border-box}
  .tl-card .tl-row{display:flex;gap:8px;align-items:center;border:0;padding:0;margin:0}.tl-err{color:#be123c;font-size:14px;min-height:18px}
  .tl-btn{font:inherit;font-weight:700;border:0;border-radius:10px;padding:12px 16px;background:#13315C;color:#fff;cursor:pointer}
  .tl-btn.g{background:#fff;color:#13315C;border:1px solid #cbd5e1}
  .tc{position:fixed;top:0;right:0;bottom:0;width:min(440px,100vw);background:#fff;border-left:1px solid #e2e8f0;box-shadow:-12px 0 30px rgba(15,23,42,.12);z-index:9500;display:flex;flex-direction:column;font-family:Helvetica,Arial,sans-serif}
  @media(max-width:700px){.tc{top:auto;height:78vh;width:100vw;border-left:0;border-top:1px solid #e2e8f0;border-radius:16px 16px 0 0}}
  .tc-h{padding:14px 16px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;gap:8px}
  .tc-m{flex:1;overflow:auto;padding:14px 16px;display:flex;flex-direction:column;gap:10px;background:#f8fafc}
  .tc-b{max-width:88%;padding:10px 12px;border-radius:14px;font-size:15px;line-height:1.45;white-space:pre-wrap;word-wrap:break-word}
  .tc-b.s{align-self:flex-end;background:#13315C;color:#fff;border-bottom-right-radius:4px}.tc-b.t{align-self:flex-start;background:#fff;border:1px solid #e2e8f0;border-bottom-left-radius:4px}
  .tc-b.e{align-self:center;background:#fff1f2;color:#9f1239;border:1px solid #fecdd3;font-size:14px}
  .tc-f{display:flex;gap:8px;padding:12px;border-top:1px solid #e2e8f0}.tc-f textarea{flex:1;font:inherit;font-size:15px;padding:10px;border:1px solid #cbd5e1;border-radius:10px;resize:none;height:46px}
  .tc-fig{background:#fff;border:1px solid #cbd5e1;border-radius:12px;padding:8px;margin-top:8px;cursor:zoom-in}.tc-fig svg{width:100%;height:auto;max-height:260px;display:block}
  .tc-fig .tc-big{font:inherit;font-size:13px;font-weight:700;color:#13315C;background:#EEF2F7;border:0;border-radius:8px;padding:5px 10px;margin-top:6px;cursor:pointer}
  .tc-ov{position:fixed;inset:0;background:rgba(15,23,42,.55);z-index:9700;display:flex;align-items:center;justify-content:center;padding:20px}
  .tc-ov>div{background:#fff;border-radius:16px;padding:18px;width:min(900px,96vw);max-height:92vh;overflow:auto;box-shadow:0 20px 50px rgba(0,0,0,.3)}.tc-ov svg{width:100%;height:auto;max-height:72vh;display:block}
  .tc-who{display:inline-flex;align-items:center;gap:8px;border:1px solid #cbd5e1;border-radius:999px;padding:4px 12px 4px 4px;font-size:14px;font-weight:600;color:#0f172a;background:#fff;text-decoration:none!important}
  .tc-who i{width:26px;height:26px;border-radius:50%;background:#13315C;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-style:normal;font-weight:800;font-size:13px}.tc-who b{color:#047857;font-weight:600;font-size:12px}
  .tc-chips{display:flex;gap:6px;flex-wrap:wrap;padding:0 16px 10px;background:#f8fafc}.tc-chips button{font:inherit;font-size:13px;border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:5px 10px;cursor:pointer}`;
  document.head.appendChild(css);

  // sign-in itself is in auth.js; here: Sign out link + turn on the private question bundles
  let sb = null, session = null;
  function whoName() { const u = session && session.user; if (!u) return ''; const m = u.user_metadata || {}; const n = m.name || m.full_name || (u.email || '').split('@')[0].replace(/[^a-z]+.*$/i, ''); return n ? n[0].toUpperCase() + n.slice(1) : 'you' }
  function signOutLink() {
    const nav = document.querySelector('header.top nav'); if (!nav || nav.querySelector('[data-signout]')) return;
    const n = whoName(); if (!n) return;
    const w = document.createElement('span'); w.className = 'tc-who'; w.title = 'Signed in as ' + (session.user.email || n); w.innerHTML = `<i>${n[0]}</i><span>${n}<br><b>● Signed in</b></span>`;
    const a = document.createElement('a'); a.href = '#'; a.textContent = 'Sign out'; a.dataset.signout = '1';
    a.onclick = e => { e.preventDefault(); window.HELM_SIGNOUT() }; nav.appendChild(w); nav.appendChild(a);
  }
  let unlocking = false;
  async function autoUnlock() {
    if (unlocking || typeof unlockBP !== 'function') return; if (typeof BPR !== 'undefined' && BPR.length) return; unlocking = true;
    try { const {data} = await sb.from('helm_members').select('unlock_code').maybeSingle(); if (data && data.unlock_code && await unlockBP(data.unlock_code) && typeof D !== 'undefined' && !D && typeof route === 'function') route() } catch (e) {}
    unlocking = false }
  if (window.HELM_AUTH) window.HELM_AUTH.then(async s => { session = s; sb = window.HELM_SB; try { const r = await sb.auth.getUser(); if (r.data && r.data.user) session = {...s, user: r.data.user} } catch (e) {} signOutLink(); autoUnlock() });

  // ---------- "Ask the tutor" ----------
  try { if (typeof HELPN === 'object') HELPN.tutor = 'Ask the tutor' } catch (e) {}
  const L4 = ['A', 'B', 'C', 'D'];
  const pl = h => (typeof plain === 'function' ? plain(h) : String(h).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
  const pretty = t => t.replace(/\^2\b/g, '²').replace(/\^3\b/g, '³').replace(/sqrt\(([^()]*)\)/g, '√($1)').replace(/\*\*(.+?)\*\*/g, '$1');
  function cid(qid) { const k = 'tc_' + qid + '_' + new Date().toLocaleDateString('en-CA'); let v = localStorage.getItem(k); if (!v) { v = crypto.randomUUID(); localStorage.setItem(k, v) } return v }
  function ctx() {
    const q = cur(), st = D.st[D.i], sk = SK2[q.skill] || {};
    const tried = (st.tried || []).map(t => typeof t === 'number' ? L4[t] : String(t)).join(', then ');
    const usedShow = [...(st.hb || []), ...(st.ha || [])].includes('show') || (st.shown || 0) > 0;
    const h = (typeof QH === 'object' && QH[q.id]) || {};
    return {
      skill: sk.name || q.skill, difficulty: (typeof DIFF === 'object' && DIFF[q.diff]) || q.diff, text: pl(q.q),
      choices: q.ch ? q.ch.map((c, j) => `${L4[j]}) ${pl(c)}`) : undefined,
      correct: q.ch ? `${L4[q.ans]}) ${pl(q.ch[q.ans])}` : String(q.show || (q.grid || [])[0] || ''),
      student_answer: tried, steps_shown: usedShow ? (q.steps || []).map((x, i) => `${i + 1}. ${pl(x)}`).join(' ') : '',
      desmos: (h.d || []).join(' | ') + (h.n ? ' — ' + h.n : '')
    };
  }
  // drawings: the tutor may send one <svg> picture; it is cleaned (no scripts or links) and can open big
  function cleanSvg(src) {
    try { const d = new DOMParser().parseFromString(src, 'image/svg+xml'), r = d.documentElement; if (!r || r.nodeName.toLowerCase() !== 'svg' || d.querySelector('parsererror')) return null;
      r.querySelectorAll('script,foreignObject,iframe,image,a,use,style').forEach(x => x.remove());
      [r, ...r.querySelectorAll('*')].forEach(el => [...el.attributes].forEach(at => { if (/^on/i.test(at.name) || /href/i.test(at.name) || /javascript:/i.test(at.value)) el.removeAttribute(at.name) }));
      if (!r.getAttribute('viewBox')) r.setAttribute('viewBox', `0 0 ${parseFloat(r.getAttribute('width')) || 400} ${parseFloat(r.getAttribute('height')) || 300}`);
      r.removeAttribute('width'); r.removeAttribute('height'); r.setAttribute('font-family', 'Helvetica,Arial,sans-serif'); return r.outerHTML } catch (e) { return null } }
  function bigPic(svg, caption) {
    const o = document.createElement('div'); o.className = 'tc-ov'; o.innerHTML = `<div><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><b style="font-size:17px">${caption || 'Picture'}</b><button class="tl-btn g" aria-label="Close">✕ Close</button></div>${svg}<div style="font-size:13px;color:#64748b;margin-top:8px">Close this to keep asking the tutor questions.</div></div>`;
    o.onclick = e => { if (e.target === o || e.target.closest('button')) o.remove() }; document.body.appendChild(o) }
  function bubble(box, role, text) {
    const b = document.createElement('div'); b.className = 'tc-b ' + role; let svg = null;
    if (role === 't') { const m = text.match(/<svg[\s\S]*?<\/svg>/i); if (m) { svg = cleanSvg(m[0]); text = text.replace(/```(?:svg|html|xml)?\s*<svg[\s\S]*?<\/svg>\s*```|<svg[\s\S]*?<\/svg>/i, '').trim() } b.textContent = pretty(text) } else b.textContent = text;
    if (svg) { const f = document.createElement('div'); f.className = 'tc-fig'; f.innerHTML = svg + '<button class="tc-big" type="button">⤢ Open big</button>'; f.onclick = () => bigPic(svg, 'Tutor drawing'); b.appendChild(f) }
    box.appendChild(b); box.scrollTop = box.scrollHeight; return b }
  // One chat per question: the tutor only ever sees THIS question and THIS question's messages.
  // If Patrick moves to another question with the chat open, the chat switches to the new question (fresh, nothing from the old one is sent).
  let chatFor = null;
  // ---- Tutor = Patrick's own Claude (Allie's account), in the "Patrick SAT Tutor" project. No API credits are used. ----
  // HELM saves what he asks (for the Stats page and the nightly follow-up), then opens a new Claude chat in the project with the question filled in.
  const TUTOR_PROJECT = window.HELM_TUTOR_PROJECT || '';   // claude.ai project id (set in tutor-config.js)
  function claudeText(q, st, ask) {
    const L = ['A', 'B', 'C', 'D'], c = ctx(), fig = /class="cbfig"|<img|<svg/.test(q.q) || (typeof figFor === 'function' && figFor(q));
    return [`SAT HELM question ${D.i + 1} · ${c.skill} · ${c.difficulty}`, '', c.text, fig ? '(This question has a picture. If you need it, ask me to describe it, or draw your own from the numbers.)' : '',
      c.choices ? c.choices.join('\n') : '(Fill-in answer)', '', `Correct answer: ${c.correct}`, `My answer(s) so far: ${c.student_answer || 'none yet'}`,
      c.steps_shown ? `Steps I already saw: ${c.steps_shown}` : '', c.desmos ? `Desmos tip on file: ${c.desmos}` : '', '', `What's confusing me: ${ask}`,
      '', 'Tutor me on this one question with your project rules: one hint at a time, and draw a labeled picture if it helps.'].filter((x, i, a) => x !== '' || a[i - 1] !== '').join('\n').slice(0, 6000);
  }
  async function openChat(switched) {
    if (typeof D === 'undefined' || !D) return;
    const q = cur(), st = D.st[D.i]; chatFor = q.id;
    if (!switched) { const key = st.tried && st.tried.length ? 'ha' : 'hb'; st[key] = st[key] || []; if (!st[key].includes('tutor')) st[key].push('tutor') }
    let p = document.querySelector('.tc'); if (p) p.remove();
    p = document.createElement('div'); p.className = 'tc'; p.setAttribute('role', 'dialog'); p.setAttribute('aria-label', 'Ask the tutor');
    p.innerHTML = `<div class="tc-h"><div><div style="font-weight:800;font-size:18px">Ask the tutor</div><div style="font-size:13px;color:#64748b">Question ${D.i + 1} · ${pl((SK2[q.skill] || {}).name || '')}</div></div><button class="tl-btn g" data-tcx="1" aria-label="Close">✕</button></div>
      <div class="tc-m"><div class="tc-b t">What's confusing you about question ${D.i + 1}? Type it, or tap one below. Your tutor opens in Claude with this question ready to go.</div><div class="tc-prev"></div></div>
      <div class="tc-chips">${['I don\'t know where to start', 'Draw me a picture', 'Why is my answer wrong?', 'Show me the Desmos way', 'Explain it another way'].map(t => `<button data-tcq="${t}">${t}</button>`).join('')}</div>
      <form class="tc-f"><textarea placeholder="What's confusing you?" aria-label="Your question"></textarea><button class="tl-btn" type="submit">Open tutor</button></form>`;
    document.body.appendChild(p);
    const ta = p.querySelector('textarea'), id = cid(q.id), prev = p.querySelector('.tc-prev');
    if (sb && session) { const {data} = await sb.from('tutor_messages').select('content,created_at').eq('conversation_id', id).eq('role', 'student').order('created_at', {ascending: true});
      if (data && data.length) prev.innerHTML = `<div style="font-size:12px;color:#64748b;margin:6px 0 4px">You already asked about this question today:</div>` + data.map(m => `<div class="tc-b s" style="margin-left:auto;margin-bottom:6px">${esc(m.content)}</div>`).join('') }
    const go = async text => {
      text = (text || '').trim(); if (!text) { ta.focus(); return }
      const prompt = claudeText(q, st, text);
      const url = 'https://claude.ai/new?q=' + encodeURIComponent(prompt) + (TUTOR_PROJECT ? '&project=' + encodeURIComponent(TUTOR_PROJECT) : '');
      const w = window.open(url, '_blank');  // open first (inside the click) so the browser allows the new tab
      try { await navigator.clipboard.writeText(prompt) } catch (e) {}
      if (sb && session) try { await sb.from('tutor_messages').insert({user_id: session.user.id, conversation_id: id, question_id: q.id, skill: (SK2[q.skill] || {}).name || q.skill, role: 'student', content: text.slice(0, 2000)}) } catch (e) {}
      prev.insertAdjacentHTML('beforeend', `<div class="tc-b s" style="margin-left:auto;margin-bottom:6px">${esc(text)}</div>`); ta.value = '';
      const m = p.querySelector('.tc-m'); m.insertAdjacentHTML('beforeend', `<div class="tc-b t">${w ? 'Your tutor opened in a new tab (Claude › Patrick SAT Tutor). Press Enter there to send. Keep chatting there as long as you want.' : 'Your browser blocked the new tab. Allow pop-ups for this site, then tap Open tutor again.'}<br><span style="font-size:12px;color:#64748b">The question is also copied, so you can paste it if the box is empty.</span></div>`); m.scrollTop = m.scrollHeight;
    };
    p.querySelector('form').onsubmit = e => { e.preventDefault(); go(ta.value) };
    ta.onkeydown = e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); go(ta.value) } };
    p.querySelectorAll('[data-tcq]').forEach(b => b.onclick = () => go(b.dataset.tcq));
    p.querySelector('[data-tcx]').onclick = () => { p.remove(); chatFor = null };
    setTimeout(() => ta.focus(), 50);
  }
  // add the button to every question's help row, and a nudge under "Show me how"
  new MutationObserver(() => {
    const help = document.querySelector('.dr .help');
    if (help && !help.querySelector('[data-tutor]')) { const b = document.createElement('button'); b.className = 'b'; b.dataset.tutor = '1'; b.textContent = 'Ask the tutor'; help.appendChild(b) }
    document.querySelectorAll('.dr .box.b-blue').forEach(x => { const side = x.parentElement; if (side && !side.querySelector('[data-tutor2]') && /Show me how/.test(side.textContent.slice(0, 40))) { const d = document.createElement('div'); d.dataset.tutor2 = '1'; d.className = 'box b-green'; d.innerHTML = '<div class="lab">Still confused?</div><div class="c"><button class="btn sm" data-tutor="1">Ask the tutor</button></div>'; side.appendChild(d) } });
    if (!document.querySelector('.dr')) { const p = document.querySelector('.tc'); if (p) p.remove(); chatFor = null }
    else if (chatFor && document.querySelector('.tc') && typeof D !== 'undefined' && D && cur() && cur().id !== chatFor) { chatFor = cur().id; openChat(true) }
    signOutLink();
  }).observe(document.body, {childList: true, subtree: true});
  document.addEventListener('click', e => { if (e.target.closest('[data-tutor]')) { e.preventDefault(); openChat() } }, true);
})();
