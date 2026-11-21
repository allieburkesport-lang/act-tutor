/* ---------- SAT HELM sign-in gate (every page) ----------
   Nothing on the page loads until Patrick is signed in. Sets window.HELM_SB (Supabase client), window.HELM_AUTH (promise that
   resolves with the session once signed in) and keeps window.HELM_TOKEN current for REST calls. */
(function () {
  const URL_ = 'https://wsoevgmculmcnxymivbp.supabase.co', KEY = 'sb_publishable_ncTnyRItcb1Ww_FUSpMlew_uv-7gPg_';
  const LOGO = (document.currentScript && document.currentScript.src || '').replace(/auth\.js.*$/, 'helm-logo.png');
  document.documentElement.classList.add('helm-locked');
  const css = document.createElement('style');
  css.textContent = `html.helm-locked body>*:not(.tl-wrap){visibility:hidden!important}
  .tl-wrap{position:fixed;inset:0;z-index:10000;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-family:Helvetica,Arial,sans-serif;visibility:visible!important}
  .tl-card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.08);padding:28px;width:min(400px,92vw);display:flex;flex-direction:column;gap:12px}
  .tl-card label{font-size:13px;font-weight:600;color:#334155;display:block;margin-bottom:4px}.tl-card input{font:inherit;font-size:16px;padding:11px 12px;border:1px solid #cbd5e1;border-radius:10px;width:100%;box-sizing:border-box}
  .tl-card .tl-row{display:flex;gap:8px;align-items:center}.tl-err{color:#be123c;font-size:14px;min-height:18px}
  .tl-btn{font:inherit;font-weight:700;border:0;border-radius:10px;padding:12px 16px;background:#13315C;color:#fff;cursor:pointer}
  .tl-btn.g{background:#fff;color:#13315C;border:1px solid #cbd5e1}`;
  document.head.appendChild(css);
  let resolve; window.HELM_AUTH = new Promise(r => resolve = r);
  const setH = t => { try { if (typeof H === 'object' && H && 'Authorization' in H) H.Authorization = 'Bearer ' + t } catch (e) {} };
  const unlock = s => { window.HELM_SESSION = s; window.HELM_TOKEN = s.access_token; setH(s.access_token); document.documentElement.classList.remove('helm-locked'); const w = document.querySelector('.tl-wrap'); if (w) w.remove(); resolve(s) };
  function card(sb) {
    if (document.querySelector('.tl-wrap')) return;
    const w = document.createElement('div'); w.className = 'tl-wrap';
    w.innerHTML = `<form class="tl-card" autocomplete="on"><img src="${LOGO}" alt="SAT HELM" style="height:64px;width:auto;align-self:center">
      <div style="font-size:15px;color:#475569;text-align:center">Sign in to SAT HELM</div>
      <div><label for="tl-e">Email</label><input id="tl-e" type="email" autocomplete="username" required></div>
      <div><label for="tl-p">Password</label><div class="tl-row"><input id="tl-p" type="password" autocomplete="current-password" required><button type="button" class="tl-btn g" id="tl-show">Show</button></div></div>
      <div class="tl-err" id="tl-err" role="alert"></div><button class="tl-btn" type="submit">Sign in</button></form>`;
    (document.body || document.documentElement).appendChild(w);
    w.querySelector('#tl-show').onclick = () => { const p = w.querySelector('#tl-p'); p.type = p.type === 'password' ? 'text' : 'password'; w.querySelector('#tl-show').textContent = p.type === 'password' ? 'Show' : 'Hide' };
    w.querySelector('form').onsubmit = async ev => { ev.preventDefault(); const err = w.querySelector('#tl-err'); err.textContent = 'Signing in…';
      const {data, error} = await sb.auth.signInWithPassword({email: w.querySelector('#tl-e').value.trim(), password: w.querySelector('#tl-p').value});
      if (error || !data.session) { err.textContent = 'Email or password is wrong'; return } unlock(data.session) };
  }
  function boot() {
    if (!window.supabase) { const d = document.createElement('div'); d.className = 'tl-wrap'; d.innerHTML = '<div class="tl-card">Could not reach the sign-in service. Check the internet connection and reload.</div>'; document.body.appendChild(d); return }
    const sb = window.supabase.createClient(URL_, KEY, {auth: {persistSession: true, autoRefreshToken: true}});
    window.HELM_SB = sb;
    sb.auth.onAuthStateChange((ev, s) => { if (s) { window.HELM_TOKEN = s.access_token; window.HELM_SESSION = s; setH(s.access_token) } if (ev === 'SIGNED_OUT') location.reload() });
    sb.auth.getSession().then(({data}) => data.session ? unlock(data.session) : card(sb));
  }
  window.HELM_SIGNOUT = async () => { if (window.HELM_SB) await window.HELM_SB.auth.signOut(); location.reload() };
  const go = () => { if (window.supabase) return boot(); const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2'; s.onload = boot; s.onerror = boot; document.head.appendChild(s) };
  if (document.body) go(); else document.addEventListener('DOMContentLoaded', go);
})();
