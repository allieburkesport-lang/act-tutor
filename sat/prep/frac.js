/* ---------- Stacked fractions everywhere math is shown ----------
   Turns "A ÷ B", "−A/B", "3/4", "(y₂ − y₁) ÷ (x₂ − x₁)" into a real fraction: top, line, bottom.
   Only touches math areas (help boxes, formulas, questions, choices, lessons). Calculator and Desmos
   keystrokes ("12 › ÷ › 6", "Type 42 ÷ 0.7") keep the ÷ key because that's the button to press.
   The slash stays in the text (hidden), so copying or sending a question to the tutor still reads "A/B". */
(function () {
  const AREAS = '.box .c, .eq, .qtext, .stem, .ch .t, .passage, .step, .lesson, .lframe, .fx, [data-frac]';
  const SKIP = 'script,style,textarea,input,code,pre,svg,math,.fr,.desmos,.keys,.navgrid,.qnum,.timer,[data-nofrac]';
  const css = document.createElement('style');
  css.textContent = `.fr{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 .12em;line-height:1.1;font-size:.92em}
  .fr>.fn{padding:0 .2em .08em}.fr>.fd{padding:.08em .2em 0;border-top:.09em solid currentColor;align-self:stretch;text-align:center}
  .fr>.fs{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}`;
  (document.head || document.documentElement).appendChild(css);

  const SUB = '₀-₉⁰-⁹²³¹′';
  const NUM = `\\d+(?:[.,]\\d+)*(?:π)?|π`;
  const VAR = `[A-Za-z]{1,2}[${SUB}0-9]*(?:π)?|[A-Za-z]\\d*π`;
  const TRIG = 'Opposite|Adjacent|Hypotenuse|opposite|adjacent|hypotenuse';
  // a balanced (...) group, one level of nesting
  const PAR = `\\((?:[^()]|\\([^()]*\\))+\\)`;
  const ATOM = `(?:${PAR}|${NUM}|${TRIG}|${VAR})`;
  // a ÷ b : the bottom may be a short phrase when it ends the line ("sum ÷ how many numbers")
  const DIV = new RegExp(`(${PAR}|${NUM}|[A-Za-zπ][A-Za-z${SUB}0-9π]*)\\s*÷\\s*(${PAR}|(?:[A-Za-z][a-z]+ ){1,3}[A-Za-z][a-z]+(?=\\s*(?:$|[.,;)]))|${NUM}|${TRIG}|[A-Za-zπ][A-Za-z${SUB}0-9π]*)`, 'g');
  // a/b : both sides must look like math (numbers, 1-2 letter variables, groups, trig words), never words like and/or
  const SL = new RegExp(`(^|[^\\w/.:])(${ATOM})\\/(${ATOM})(?![\\w/]|\\.\\d)`, 'g');

  const keystroke = t => /›|^\s*Type\b|\bType\s+\S/.test(t) || /\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/.test(t) || /https?:|www\./.test(t);
  const clean = s => s.replace(/^\((.*)\)$/, (m, inner) => {  // drop outer parens: (y₂ − y₁) on top of a fraction
    let d = 0; for (let i = 0; i < inner.length; i++) { if (inner[i] === '(') d++; else if (inner[i] === ')') { d--; if (d < 0) return m } } return d === 0 ? inner : m });
  const frac = (a, b) => { const s = document.createElement('span'); s.className = 'fr';
    s.innerHTML = '<span class="fn"></span><span class="fs">/</span><span class="fd"></span>';
    s.firstChild.textContent = clean(a.trim()); s.lastChild.textContent = clean(b.trim()); return s };

  function convert(node) {
    const t = node.nodeValue; if (!t || (t.indexOf('÷') < 0 && t.indexOf('/') < 0) || keystroke(t)) return;
    const parts = []; let last = 0, any = false;
    const ms = [];
    for (const m of t.matchAll(DIV)) ms.push({i: m.index, n: m[0].length, a: m[1], b: m[2]});
    for (const m of t.matchAll(SL)) { const pre = m[1].length; ms.push({i: m.index + pre, n: m[0].length - pre, a: m[2], b: m[3]}) }
    ms.sort((x, y) => x.i - y.i);
    for (const m of ms) {
      if (m.i < last) continue;
      if (/^\d{4}$/.test(m.a) && /^\d{2,4}$/.test(m.b)) continue;     // school years like 2026/27
      parts.push(document.createTextNode(t.slice(last, m.i)), frac(m.a, m.b)); last = m.i + m.n; any = true;
    }
    if (!any) return;
    parts.push(document.createTextNode(t.slice(last)));
    const f = document.createDocumentFragment(); parts.forEach(p => f.appendChild(p)); node.parentNode.replaceChild(f, node);
  }
  function scan(root) {
    const areas = root.matches && root.matches(AREAS) ? [root] : [];
    root.querySelectorAll && root.querySelectorAll(AREAS).forEach(a => areas.push(a));
    let p = root.parentElement; while (p) { if (p.matches && p.matches(AREAS)) { areas.push(root); break } p = p.parentElement }
    for (const a of areas) {
      const w = document.createTreeWalker(a, NodeFilter.SHOW_TEXT, {acceptNode: n => n.parentElement && !n.parentElement.closest(SKIP) ? 1 : 2});
      const list = []; while (w.nextNode()) list.push(w.currentNode); list.forEach(convert);
    }
  }
  let queued = false;
  const run = () => { queued = false; scan(document.body) };
  const start = () => { run(); new MutationObserver(() => { if (!queued) { queued = true; requestAnimationFrame(run) } }).observe(document.body, {childList: true, subtree: true, characterData: true}) };
  window.HELM_FRAC = {scan, convert, DIV, SL};
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
})();
