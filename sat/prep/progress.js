/* ---------- HELM progress + photo uploads (shared by every HELM page) ----------
   Progress is saved on this device right away AND in Supabase (table helm_progress),
   so it follows Patrick to any phone or computer he signs in on.
   Photos go to the private Supabase bucket "helm-photos", in his own folder.

   HELM_PROGRESS.get(key, fallback)        -> value saved on this device
   HELM_PROGRESS.pull(key)                 -> Promise: newest value from Supabase (also saved locally)
   HELM_PROGRESS.put(key, value)           -> save locally + to Supabase
   HELM_PROGRESS.merge(key, obj)           -> shallow-merge obj into the saved value
   HELM_PROGRESS.upload(folder, files, onStep) -> Promise<number of photos uploaded>
   HELM_PROGRESS.count(folder)             -> Promise<number of photos already in that folder>
*/
(function () {
  const LKEY = (k) => 'helm.p.' + k;
  const local = {
    get(k, d) { try { const v = localStorage.getItem(LKEY(k)); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(LKEY(k), JSON.stringify(v)); } catch (e) {} }
  };
  const ready = () => (window.HELM_AUTH ? window.HELM_AUTH : Promise.reject(new Error('not signed in'))).then((s) => ({ sb: window.HELM_SB, uid: s.user.id }));
  const pending = {};

  const P = {
    get: (k, d) => local.get(k, d),
    async pull(k) {
      try {
        const { sb } = await ready();
        const { data, error } = await sb.from('helm_progress').select('value').eq('key', k).maybeSingle();
        if (error) throw error;
        if (data) { local.set(k, data.value); return data.value; }
      } catch (e) {}
      return local.get(k, null);
    },
    put(k, v) {
      local.set(k, v);
      clearTimeout(pending[k]);
      pending[k] = setTimeout(async () => {
        try { const { sb } = await ready(); await sb.from('helm_progress').upsert({ key: k, value: v, updated_at: new Date().toISOString() }, { onConflict: 'user_id,key' }); } catch (e) {}
      }, 400);
      return v;
    },
    merge(k, obj) { return P.put(k, Object.assign({}, local.get(k, {}), obj)); },
    async upload(folder, files, onStep) {
      const { sb, uid } = await ready();
      let n = 0;
      for (const f of Array.from(files)) {
        const ext = ((f.name || '').split('.').pop() || 'jpg').toLowerCase().replace(/[^a-z0-9]/g, '') || 'jpg';
        const path = `${uid}/${folder}/${Date.now()}-${n}.${ext}`;
        const { error } = await sb.storage.from('helm-photos').upload(path, f, { contentType: f.type || 'image/jpeg', upsert: false });
        if (error) throw error;
        n++; if (onStep) onStep(n, files.length);
      }
      return n;
    },
    async count(folder) {
      try {
        const { sb, uid } = await ready();
        const { data, error } = await sb.storage.from('helm-photos').list(`${uid}/${folder}`, { limit: 100 });
        if (error) throw error;
        return (data || []).filter((x) => x.name && !x.name.startsWith('.')).length;
      } catch (e) { return null; }
    }
  };
  window.HELM_PROGRESS = P;
})();

/* ---------- "Patrick errors and questions" (Allie, Nov 26) ----------
   A Report a problem button in the HELM menu (or bottom-right on pages without one). Patrick pastes or picks a screenshot,
   adds a note, and it is saved to his account as helm_progress key "report:<time>" (status "new").
   An hourly scheduled task reads the new reports, fixes HELM, and sets status "fixed" with a short note shown here. */
(function () {
  const ready = () => (window.HELM_AUTH || Promise.reject()).then(() => window.HELM_SB);
  const css = document.createElement('style');
  css.textContent = `.rp-wrap{position:fixed;inset:0;z-index:9000;background:rgba(15,23,42,.45);display:flex;align-items:center;justify-content:center;font-family:Helvetica,Arial,sans-serif}
  .rp-card{background:#fff;border-radius:14px;padding:22px;width:min(560px,94vw);max-height:92vh;overflow:auto;display:flex;flex-direction:column;gap:12px;color:#0f172a}
  .rp-card h3{margin:0;font-size:20px;text-transform:uppercase;letter-spacing:.04em}.rp-drop{border:2px dashed #cbd5e1;border-radius:12px;padding:18px;text-align:center;color:#475569;cursor:pointer;font-size:15px}
  .rp-drop img{max-width:100%;max-height:260px;display:block;margin:0 auto}.rp-card textarea{font:inherit;font-size:16px;padding:10px;border:1px solid #cbd5e1;border-radius:10px;min-height:80px;width:100%;box-sizing:border-box}
  .rp-b{font:inherit;font-weight:700;border:0;border-radius:10px;padding:11px 16px;background:#13315C;color:#fff;cursor:pointer}.rp-b.g{background:#fff;color:#13315C;border:1px solid #cbd5e1}
  .rp-row{display:flex;gap:8px;justify-content:flex-end}.rp-msg{font-size:14px;min-height:18px}.rp-list{border-top:1px solid #e2e8f0;padding-top:10px;font-size:14px}
  .rp-list div{padding:6px 0;border-bottom:1px solid #f1f5f9}.rp-st{font-weight:700;font-size:12px;text-transform:uppercase}
  .rp-fab{position:fixed;right:16px;bottom:16px;z-index:8000;font:700 14px Helvetica,Arial,sans-serif;border:0;border-radius:999px;padding:11px 16px;background:#be123c;color:#fff;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.18)}`;
  document.head.appendChild(css);
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  // where Patrick is: this page, plus the SAT page inside it and the question on screen
  function where() {
    const w = { url: location.href };
    document.querySelectorAll('iframe').forEach(f => { try { const cw = f.contentWindow; if (!cw || !cw.location) return; w.frame = cw.location.href;
      try { const q = typeof cw.cur === 'function' && cw.cur(); if (q && q.id) w.qid = q.id } catch (e) {} } catch (e) {} });
    try { const q = typeof window.cur === 'function' && window.cur(); if (q && q.id) w.qid = q.id } catch (e) {}
    // the words and Desmos lines on screen, so the fix can be made from the report alone (the picture is for people)
    const docs = [document]; document.querySelectorAll('iframe').forEach(f => { try { if (f.contentDocument) docs.push(f.contentDocument) } catch (e) {} });
    const main = docs[docs.length - 1], body = main.querySelector('main') || main.body;
    try { w.text = (body.innerText || '').replace(/\n{3,}/g, '\n\n').slice(0, 15000) } catch (e) {}
    try { w.desmos = [...main.querySelectorAll('.dsx-live[data-spec]')].map(el => el.dataset.spec).filter(x => x && !/"pad"/.test(x)).slice(0, 4).map(x => x.slice(0, 6000)) } catch (e) {}
    return w;
  }
  function shrink(file) {
    return new Promise((res, rej) => { const img = new Image(); img.onload = () => { const k = Math.min(1, 1600 / Math.max(img.width, img.height));
      const c = document.createElement('canvas'); c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); res(c.toDataURL('image/jpeg', 0.82)) }; img.onerror = rej; img.src = URL.createObjectURL(file) });
  }
  async function list(box) {
    try { const sb = await ready(); const { data } = await sb.from('helm_progress').select('key,value').like('key', 'report:%').order('key', { ascending: false }).limit(8);
      if (!data || !data.length) { box.innerHTML = ''; return }
      box.innerHTML = '<div class="rp-st" style="color:#475569">YOUR REPORTS</div>' + data.map(r => { const v = r.value || {}, fixed = v.status === 'fixed';
        return `<div><span class="rp-st" style="color:${fixed ? '#047857' : '#b45309'}">${fixed ? 'Fixed' : 'Waiting'}</span> · ${esc(new Date(v.when || r.key.slice(7)).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }))} · ${esc(v.note || '(screenshot)')}${v.fix ? `<br><span style="color:#047857">${esc(v.fix)}</span>` : ''}</div>` }).join('');
    } catch (e) {}
  }
  function open() {
    if (document.querySelector('.rp-wrap')) return; const at = where(); let shot = null;
    const w = document.createElement('div'); w.className = 'rp-wrap';
    w.innerHTML = `<div class="rp-card" role="dialog" aria-label="Report a problem"><h3>Report a problem</h3>
      <div style="font-size:15px;color:#475569">Something wrong or confusing? Take a screenshot (Windows: <b>Win + Shift + S</b>), then paste it here with <b>Ctrl + V</b>, or tap the box to pick a photo.</div>
      <div class="rp-drop" tabindex="0">Paste or tap to add a screenshot</div><input type="file" accept="image/*" hidden>
      <textarea placeholder="What's wrong or what doesn't make sense? (optional)"></textarea>
      <div class="rp-msg" role="status"></div><div class="rp-row"><button class="rp-b g" data-x>Close</button><button class="rp-b" data-send>Send</button></div><div class="rp-list"></div></div>`;
    document.body.appendChild(w);
    const drop = w.querySelector('.rp-drop'), inp = w.querySelector('input'), msg = w.querySelector('.rp-msg');
    const take = async f => { if (!f || !/^image\//.test(f.type)) return; msg.textContent = 'Adding…'; try { shot = await shrink(f); drop.innerHTML = `<img alt="Your screenshot" src="${shot}">`; msg.textContent = '' } catch (e) { msg.textContent = 'That picture could not be read. Try another.' } };
    drop.onclick = () => inp.click(); inp.onchange = () => take(inp.files[0]);
    const paste = e => { const it = [...(e.clipboardData || {}).items || []].find(i => /^image\//.test(i.type)); if (it) { e.preventDefault(); take(it.getAsFile()) } };
    document.addEventListener('paste', paste);
    const close = () => { document.removeEventListener('paste', paste); w.remove() };
    w.querySelector('[data-x]').onclick = close; w.onclick = e => { if (e.target === w) close() };
    w.querySelector('[data-send]').onclick = async () => { const note = w.querySelector('textarea').value.trim();
      if (!shot && !note) { msg.textContent = 'Add a screenshot or a note first.'; return }
      msg.textContent = 'Sending…'; const now = new Date().toISOString();
      try { const sb = await ready(); const { error } = await sb.from('helm_progress').upsert({ key: 'report:' + now, value: Object.assign({ when: now, note, img: shot, status: 'new' }, at), updated_at: now }, { onConflict: 'user_id,key' });
        if (error) throw error; msg.innerHTML = '<span style="color:#047857;font-weight:700">Sent ✓ It will be fixed in HELM, and this list shows when it is.</span>';
        shot = null; drop.textContent = 'Paste or tap to add another screenshot'; w.querySelector('textarea').value = ''; list(w.querySelector('.rp-list'));
      } catch (e) { msg.textContent = 'Not sent. Check the internet and try again.' } };
    list(w.querySelector('.rp-list')); setTimeout(() => drop.focus(), 30);
  }
  window.HELM_REPORT = open;
  function mount() {
    if (window.top !== window) return; // inside the HELM frame the outer page has the button
    if (document.querySelector('.rp-nav,.rp-fab')) return;
    const side = document.getElementById('side-btn');
    if (side) { const b = document.createElement('button'); b.type = 'button'; b.className = 'nav rp-nav'; b.title = 'Report a problem';
      b.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#be123c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V4h11l1 3h4v9h-7l-1-3H4"></path></svg><span class="lbl" style="color:#be123c">Report a problem</span>';
      b.onclick = open; side.parentNode.insertBefore(b, side) }
    else { const b = document.createElement('button'); b.type = 'button'; b.className = 'rp-fab'; b.textContent = '⚑ Report a problem'; b.onclick = open; document.body.appendChild(b) }
  }
  (window.HELM_AUTH || Promise.resolve()).then(() => { const go = () => document.body ? mount() : setTimeout(go, 50); go() });
})();
