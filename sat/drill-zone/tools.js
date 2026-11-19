/* "Desmos or calculator?" cards, shared by the dashboard and the lessons. Steps open one at a time. */
let TOOLS=null, TS={};
const toolsReady=fetch('tools.json').then(r=>r.json()).then(j=>{TOOLS=j;return j}).catch(()=>null);
const tEsc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function toolHTML(card,key,open){
  if(!TOOLS||!card||!TOOLS.M[card.m])return '';
  const M=TOOLS.M[card.m], st=TS[key]||(TS[key]={open:!!open,n:1,alt:false,an:1,how:false,hn:1});
  const icon=M.tool==='Desmos'?'📈':M.tool==='By hand'?'✏️':'🧮';
  let h=`<div class="tcard" style="border:2px solid #7b4fa0;border-radius:8px;padding:10px 12px;margin:10px 0;background:#fff">
   <div style="font-size:12px;font-weight:700;letter-spacing:1px;color:#5a3290">DESMOS OR CALCULATOR?</div>
   <div style="margin:4px 0"><b>${icon} Best: ${tEsc(M.tool)}</b>${M.tool!=='By hand'?' · '+tEsc(M.name):''}<br><span style="color:#4a5568">${tEsc(card.why||'')}</span></div>`;
  if(!st.open)return h+`<button class="tbtn" data-tc="open|${key}" style="font:inherit;font-weight:700;padding:6px 12px;border:2px solid #7b4fa0;border-radius:8px;background:#eee6f7;color:#5a3290;cursor:pointer">Show me how, step by step</button></div>`;
  const steps=(card.steps&&card.steps.length)?card.steps:M.steps;
  const list=(arr,n,kind)=>arr.map((s,i)=>i<n?`<div style="display:flex;gap:8px;margin:5px 0"><span style="min-width:24px;height:24px;border-radius:50%;border:2px solid #7b4fa0;color:#5a3290;font-weight:700;display:inline-flex;align-items:center;justify-content:center;font-size:13px">${i+1}</span><span>${tEsc(s)}</span></div>`:'').join('')+
    (n<arr.length?`<button data-tc="${kind}|${key}" style="font:inherit;font-size:14px;font-weight:700;padding:4px 10px;border:2px solid #7b4fa0;border-radius:8px;background:#fff;color:#5a3290;cursor:pointer">I did step ${n} ✓ · show step ${n+1}</button>`:`<div style="color:#1f6b40;font-weight:700;margin-top:4px">✓ That's every step.</div>`);
  h+=list(steps,st.n,'next');
  if(card.steps&&card.steps.length&&M.tool!=='By hand'){
    h+=st.how?`<div style="margin-top:8px;padding-top:6px;border-top:1px dashed #cbd5e1"><b>Which buttons? · ${tEsc(M.name)}</b>${list(M.steps,st.hn,'hn')}</div>`
      :`<div style="margin-top:6px"><button data-tc="how|${key}" style="font:inherit;font-size:13px;padding:3px 9px;border:1.5px solid #7b4fa0;border-radius:8px;background:#fff;color:#5a3290;cursor:pointer">Which buttons do I press?</button></div>`;}
  if(card.alt&&TOOLS.M[card.alt]){const A=TOOLS.M[card.alt];
    h+=st.alt?`<div style="margin-top:8px;padding-top:6px;border-top:1px dashed #cbd5e1"><b>Other way: ${tEsc(A.tool)} · ${tEsc(A.name)}</b>${list(A.steps,st.an,'anext')}</div>`
      :`<div style="margin-top:6px"><button data-tc="alt|${key}" style="font:inherit;font-size:13px;padding:3px 9px;border:1.5px solid #cbd5e1;border-radius:8px;background:#fff;color:#1f2a44;cursor:pointer">Other way: ${tEsc(A.tool)}</button></div>`;}
  return h+'</div>';
}
document.addEventListener('click',e=>{const b=e.target.closest('[data-tc]');if(!b)return;e.stopPropagation();
  const [act,...k]=b.dataset.tc.split('|'),key=k.join('|'),st=TS[key];if(!st)return;
  if(act==='open')st.open=true;if(act==='next')st.n++;if(act==='alt')st.alt=true;if(act==='anext')st.an++;if(act==='how')st.how=true;if(act==='hn')st.hn++;
  if(typeof render==='function')render();},true);
