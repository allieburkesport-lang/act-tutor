"""Test Desmos setups in a real (headless) Desmos calculator.

It loads the real HELM page (sat/prep/sat.html), so every line goes through the same
conversion Patrick's screen uses, then draws it in Desmos.

Usage: python3 desmos_test.py setups.json
setups.json = {"<question id>": {"how": "...", "ex": [...], "b": {...}, "nm": true, "nt": true}, ...}
Prints one line per setup (OK or the Desmos errors) and exits 1 if any failed.
Also flags setups that break the approved format (no how text, no nm/nt, no labeled point or text note).
"""
import json, sys, os, subprocess
from playwright.sync_api import sync_playwright

KEY = "b421d86fb1ac4ece8976ec06f2d31884"
JS = "/tmp/desmos_api.js"
if not os.path.exists(JS):
    subprocess.run(["curl", "-sL", "-m", "60", "-o", JS,
                    f"https://www.desmos.com/api/v1.12/calculator.js?apiKey={KEY}"], check=True)

setups = json.load(open(sys.argv[1]))
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "prep", "sat.html")
RUN = r"""async all => {
  const box = document.createElement('div'); box.style.cssText = 'width:900px;height:600px';
  document.body.appendChild(box);
  await dsLoad();
  const c = Desmos.GraphingCalculator(box, {keypad:false});
  const out = {};
  for (const [id, sp] of Object.entries(all)) {
    DSET[id] = sp;
    let h = '';
    try { h = desmosSol({id, skill:'linf', q:'', ch:['a','b','c','d'], ans:0, steps:[]}, {d:[], c:[]}); }
    catch (e) { out[id] = ['site render error: ' + e.message]; continue; }
    const m = h.match(/data-spec='([^']*)'/);
    if (!m) { out[id] = ['site did not build a Desmos card']; continue; }
    const tx = document.createElement('textarea'); tx.innerHTML = m[1]; const spec = JSON.parse(tx.value);
    c.setBlank();
    spec.ex.forEach((e, k) => { const {note, solve, ...x} = e; c.setExpression(Object.assign({id: 'e' + k}, x)); });
    await new Promise(r => setTimeout(r, 150));
    const an = c.expressionAnalysis || {};
    out[id] = Object.entries(an).filter(([k, v]) => v.isError)
      .map(([k, v]) => (v.errorMessage || '') + ' | ' + ((spec.ex[+k.slice(1)] || {}).latex || ''));
  }
  return out;
}"""
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page()
    pg.route("**/desmos.com/api/**", lambda r: r.fulfill(path=JS, content_type="application/javascript"))
    # embed.js sends a top-level visit to the framed page and auth.js asks for sign-in: neither is needed here
    pg.route("**/embed.js*", lambda r: r.fulfill(body="", content_type="application/javascript"))
    pg.route("**/auth.js*", lambda r: r.fulfill(body="window.HELM_AUTH=new Promise(()=>{});", content_type="application/javascript"))
    pg.goto("file://" + os.path.abspath(SITE))
    pg.wait_for_function("typeof desmosSol === 'function' && typeof DSET !== 'undefined'", timeout=60000)
    res = pg.evaluate(RUN, setups)
    b.close()

for qid, sp in setups.items():
    probs = list(res.get(qid, []))
    if not (sp.get("how") or "").strip():
        probs.append("format: no how paragraph")
    if not (sp.get("nm") and sp.get("nt")):
        probs.append("format: needs nm:true and nt:true")
    ex = sp.get("ex") or []
    if not any(isinstance(e, dict) and (e.get("showLabel") or e.get("type") in ("text", "table")) for e in ex) \
            and not any(isinstance(e, str) and "~" in e for e in ex):
        print("WARN", qid, "no labeled point, table or text note (fine only for a simple computing line)")
    if probs:
        bad += 1
        print("FAIL", qid, "; ".join(probs))
    else:
        print("OK  ", qid)
print(len(setups), "tested,", bad, "failed")
sys.exit(1 if bad else 0)
