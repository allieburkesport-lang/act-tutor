/* ---------- SAT HELM: sign-in + "Ask the tutor" live chat ----------
   Backend (already live in Supabase project sat-prep): auth user, helm_members, tutor_messages, Edge Function tutor-chat.
   The Claude API key lives only in Supabase secrets; the site never sees it. */
(function () {
  const URL_ = 'https://wsoevgmculmcnxymivbp.supabase.co', KEY = 'sb_publishable_ncTnyRItcb1Ww_FUSpMlew_uv-7gPg_';
  let sb = null, session = null;
  const css = document.createElement('style');
  css.textContent = `
  .tl-wrap{position:fixed;inset:0;z-index:10000;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-family:Helvetica,Arial,sans-serif}
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
  .tc-chips{display:flex;gap:6px;flex-wrap:wrap;padding:0 16px 10px;background:#f8fafc}.tc-chips button{font:inherit;font-size:13px;border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:5px 10px;cursor:pointer}`;
  document.head.appendChild(css);

  // ---------- sign-in gate ----------
  function loginCard() {
    if (document.querySelector('.tl-wrap')) return;
    const w = document.createElement('div'); w.className = 'tl-wrap';
    w.innerHTML = `<form class="tl-card" autocomplete="on"><img src="helm-logo.png" alt="SAT HELM" style="height:64px;width:auto;align-self:center">
      <div style="font-size:15px;color:#475569;text-align:center">Sign in to start practicing</div>
      <div><label for="tl-e">Email</label><input id="tl-e" type="email" autocomplete="username" required></div>
      <div><label for="tl-p">Password</label><div class="tl-row"><input id="tl-p" type="password" autocomplete="current-password" required><button type="button" class="tl-btn g" id="tl-show">Show</button></div></div>
      <div class="tl-err" id="tl-err"></div><button class="tl-btn" type="submit">Sign in</button></form>`;
    document.body.appendChild(w);
    w.querySelector('#tl-show').onclick = () => { const p = w.querySelector('#tl-p'); p.type = p.type === 'password' ? 'text' : 'password'; w.querySelector('#tl-show').textContent = p.type === 'password' ? 'Show' : 'Hide' };
    w.querySelector('form').onsubmit = async ev => { ev.preventDefault(); const err = w.querySelector('#tl-err'); err.textContent = 'Signing in…';
      const {error} = await sb.auth.signInWithPassword({email: w.querySelector('#tl-e').value.trim(), password: w.querySelector('#tl-p').value});
      if (error) { err.textContent = 'Email or password is wrong'; return } w.remove() };
  }
  function signOutLink() {
    const nav = document.querySelector('header.top nav'); if (!nav || nav.querySelector('[data-signout]') || !session) return;
    const a = document.createElement('a'); a.href = '#'; a.textContent = 'Sign out'; a.dataset.signout = '1';
    a.onclick = async e => { e.preventDefault(); await sb.auth.signOut(); session = null; loginCard() }; nav.appendChild(a);
  }
  // signing in turns on the official College Board questions and Blueprint misses (no separate unlock link needed)
  let unlocking = false;
  async function autoUnlock() {
    if (unlocking || typeof unlockBP !== 'function') return; if (typeof BPR !== 'undefined' && BPR.length) return; unlocking = true;
    try { const {data} = await sb.from('helm_members').select('unlock_code').maybeSingle(); if (data && data.unlock_code && await unlockBP(data.unlock_code) && typeof D !== 'undefined' && !D && typeof route === 'function') route() } catch (e) {}
    unlocking = false }
  function boot() {
    if (!window.supabase) return;  // CDN unreachable: leave the site usable
    sb = window.supabase.createClient(URL_, KEY, {auth: {persistSession: true, autoRefreshToken: true}});
    window.HELM_SB = sb;
    sb.auth.getSession().then(({data}) => { session = data.session; if (!session) loginCard(); else { signOutLink(); autoUnlock() } });
    sb.auth.onAuthStateChange((_e, s) => { session = s; if (s) { const w = document.querySelector('.tl-wrap'); if (w) w.remove(); signOutLink(); autoUnlock() } });
  }
  const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2'; s.onload = boot; document.head.appendChild(s);

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
  function bubble(box, role, text) { const b = document.createElement('div'); b.className = 'tc-b ' + role; b.textContent = role === 't' ? pretty(text) : text; box.appendChild(b); box.scrollTop = box.scrollHeight; return b }
  async function openChat() {
    if (typeof D === 'undefined' || !D) return;
    const q = cur(), st = D.st[D.i]; const key = st.tried && st.tried.length ? 'ha' : 'hb'; st[key] = st[key] || []; if (!st[key].includes('tutor')) st[key].push('tutor');
    let p = document.querySelector('.tc'); if (p) p.remove();
    p = document.createElement('div'); p.className = 'tc'; p.setAttribute('role', 'dialog'); p.setAttribute('aria-label', 'Ask the tutor');
    p.innerHTML = `<div class="tc-h"><div><div style="font-weight:800;font-size:18px">Ask the tutor</div><div style="font-size:13px;color:#64748b">About question ${D.i + 1} · ${pl((SK2[q.skill] || {}).name || '')}</div></div><button class="tl-btn g" data-tcx="1" aria-label="Close">✕</button></div>
      <div class="tc-m"></div><div class="tc-chips">${['I don\'t know where to start', 'Why is my answer wrong?', 'Show me the Desmos way', 'Explain it another way'].map(t => `<button data-tcq="${t}">${t}</button>`).join('')}</div>
      <form class="tc-f"><textarea placeholder="Type your question… (Enter to send)" aria-label="Your message"></textarea><button class="tl-btn" type="submit">Send</button></form>`;
    document.body.appendChild(p);
    const box = p.querySelector('.tc-m'), ta = p.querySelector('textarea'), id = cid(q.id);
    if (!sb || !session) { bubble(box, 'e', 'Please sign in to use the tutor.'); if (sb) loginCard(); return }
    const {data} = await sb.from('tutor_messages').select('role,content').eq('conversation_id', id).order('created_at', {ascending: true});
    (data || []).forEach(m => bubble(box, m.role === 'tutor' ? 't' : 's', m.content));
    if (!data || !data.length) bubble(box, 't', 'Hi Patrick. What part of this question is confusing? Tell me what you tried, even if it was a guess.');
    const send = async text => {
      text = (text || '').trim(); if (!text) return; ta.value = ''; bubble(box, 's', text); const wait = bubble(box, 't', 'Tutor is thinking…');
      const {data: r, error} = await sb.functions.invoke('tutor-chat', {body: {conversation_id: id, question_id: q.id, message: text, question: ctx()}});
      wait.remove();
      if (error) { let msg = 'The tutor could not answer right now.'; try { const j = await error.context.json(); if (j && j.error) msg = j.error } catch (e) {} bubble(box, 'e', msg); return }
      bubble(box, 't', (r && r.reply) || (r && r.error) || 'Can you say that another way?');
    };
    p.querySelector('form').onsubmit = e => { e.preventDefault(); send(ta.value) };
    ta.onkeydown = e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(ta.value) } };
    p.querySelectorAll('[data-tcq]').forEach(b => b.onclick = () => send(b.dataset.tcq));
    p.querySelector('[data-tcx]').onclick = () => p.remove();
    setTimeout(() => ta.focus(), 50);
  }
  // add the button to every question's help row, and a nudge under "Show me how"
  new MutationObserver(() => {
    const help = document.querySelector('.dr .help');
    if (help && !help.querySelector('[data-tutor]')) { const b = document.createElement('button'); b.className = 'b'; b.dataset.tutor = '1'; b.textContent = 'Ask the tutor'; help.appendChild(b) }
    document.querySelectorAll('.dr .box.b-blue').forEach(x => { const side = x.parentElement; if (side && !side.querySelector('[data-tutor2]') && /Show me how/.test(side.textContent.slice(0, 40))) { const d = document.createElement('div'); d.dataset.tutor2 = '1'; d.className = 'box b-green'; d.innerHTML = '<div class="lab">Still confused?</div><div class="c"><button class="btn sm" data-tutor="1">Ask the tutor</button></div>'; side.appendChild(d) } });
    if (!document.querySelector('.dr')) { const p = document.querySelector('.tc'); if (p) p.remove() }
    signOutLink();
  }).observe(document.body, {childList: true, subtree: true});
  document.addEventListener('click', e => { if (e.target.closest('[data-tutor]')) { e.preventDefault(); openChat() } }, true);
})();
