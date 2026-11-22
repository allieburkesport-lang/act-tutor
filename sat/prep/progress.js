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
