/* "Desmos or calculator?" cards, shared by the dashboard and the lessons. Steps open one at a time. */
let TOOLS=null, TS={};
const toolsReady=fetch('tools.json').then(r=>r.json()).then(j=>{TOOLS=j;return j}).catch(()=>null);
const tEsc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function toolHTML(card,key,open){
  if(!TOOLS||!card||!TOOLS.M[card.m])return '';
  const M=TOOLS.M[card.m], st=TS[key]||(TS[key]={open:!!open,n:1,alt:false,an:1,how:false,hn:1}); st.card=card;
  const icon=M.tool==='Desmos'?'📈':M.tool==='By hand'?'✏️':'🧮';
  let h=`<div class="tcard" style="border:2px solid #7b4fa0;border-radius:8px;padding:10px 12px;margin:10px 0;background:#fff">
   <div style="font-size:12px;font-weight:700;letter-spacing:1px;color:#5a3290">DESMOS OR CALCULATOR?</div>
   <div style="margin:4px 0"><b>${icon} Best: ${tEsc(M.tool)}</b>${M.tool!=='By hand'?' · '+tEsc(M.name):''}<br><span style="color:#4a5568">${tEsc(card.why||'')}</span></div>`+(flyable(card)?`<button data-tc="fly|${key}" style="font:inherit;font-weight:700;font-size:14px;padding:5px 12px;margin:2px 0 6px;border:2px solid #1f2a44;border-radius:8px;background:#1f2a44;color:#fff;cursor:pointer">${FLY.key===key?'✓ Showing on the right':'👁 See it on the screen →'}</button>`:'');
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
  if(act==='fly'){FLY.key===key?flyClose():flyOpen(key);if(typeof render==='function')render();return}if(act==='open')st.open=true;if(act==='next')st.n++;if(act==='alt')st.alt=true;if(act==='anext')st.an++;if(act==='how')st.how=true;if(act==='hn')st.hn++;
  if(typeof render==='function')render(); if(FLY.key===key)flyDraw();},true);

/* ---------- Fly-out picture panel: what the Desmos / TI-84 Evo screen looks like ---------- */
const FLY={key:null};
function flyable(card){if(!TOOLS||!card)return false;const M=TOOLS.M[card.m];return (M&&M.tool!=='By hand')||(card.alt&&TOOLS.M[card.alt]&&TOOLS.M[card.alt].tool!=='By hand');}
(function(){const st=document.createElement('style');st.textContent=`
#flyp{position:fixed;top:0;right:0;height:100vh;width:min(500px,42vw);background:#fff;border-left:4px solid #7b4fa0;box-shadow:-8px 0 24px rgba(31,42,68,.18);z-index:50;overflow-y:auto;transform:translateX(105%);transition:transform .3s ease;padding:16px 18px 40px;font-family:inherit;color:#1f2a44}
#flyp.on{transform:none}#flyp.wide{width:min(900px,56vw)}body.flyon.flywide .wrap{margin-right:calc(min(900px,56vw) + 16px)!important}#flyp iframe{width:100%;height:calc(100vh - 90px);border:2px solid #cbd5e1;border-radius:8px}
body.flyon .wrap{margin-right:calc(min(500px,42vw) + 16px)!important;margin-left:16px!important}
#flyp h3{margin:0 0 2px;font-size:20px}#flyp .sub{color:#4a5568;font-size:14px;margin-bottom:10px}
#flyp .x{position:absolute;top:10px;right:12px;font:inherit;font-size:20px;font-weight:700;border:2px solid #1f2a44;border-radius:8px;background:#fff;width:38px;height:38px;cursor:pointer}
.fl-lab{font-size:12px;font-weight:800;letter-spacing:1.3px;color:#5a3290;margin:14px 0 6px;text-transform:uppercase}
.fl-step{display:flex;gap:8px;margin:5px 0;padding:6px 8px;border-radius:8px;border:1.5px solid #e2e8f0}.fl-step.now{border:2.5px solid #7b4fa0;background:#f6f1fc}.fl-step.later{opacity:.45}
.fl-step .n{min-width:24px;height:24px;border-radius:50%;border:2px solid #7b4fa0;color:#5a3290;font-weight:700;display:inline-flex;align-items:center;justify-content:center;font-size:13px}
.ds{border:2px solid #1f2a44;border-radius:10px;overflow:hidden}
.ds-top{background:#f4f2ec;font-size:12px;font-weight:700;padding:5px 10px;border-bottom:1.5px solid #cbd5e1;color:#4a5568}
.ds-ex{display:flex;align-items:center;gap:8px;border-bottom:1px solid #e2e8f0;padding:7px 10px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:15px}
.ds-ex .ln{color:#94a3b8;font-size:12px;min-width:14px}.ds-ex .dot{width:12px;height:12px;border-radius:50%;flex:0 0 12px}
.ds-ex .val{margin-left:auto;color:#5a3290;font-weight:700}
.ti{background:#2b2f36;border-radius:22px;padding:16px 16px 18px;color:#fff}
.ti-scr{background:#c9d4c3;color:#111;border-radius:6px;padding:8px 10px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:15px;min-height:96px;border:3px solid #111}
.ti-scr .r{text-align:right;font-weight:700}
.ti-keys{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;align-items:center}
.kc{display:inline-flex;align-items:center;justify-content:center;min-width:42px;height:32px;padding:0 8px;border-radius:7px;background:#3d434d;border:2px solid #575e6a;color:#fff;font-weight:700;font-size:14px;box-shadow:0 3px 0 #15181c;font-family:inherit}
.kc.y{background:#e9edf3;color:#1f2a44;border-color:#cbd5e1;box-shadow:0 3px 0 #94a3b8}.kc.b{background:#2f6fb5;border-color:#1f4e8a}
.kc.num{background:#5b6270}.kc.soft{background:#7b4fa0;border-color:#5a3290}
.ti-type{font-family:ui-monospace,Menlo,Consolas,monospace;background:#fff;color:#1f2a44;border-radius:6px;padding:3px 8px;font-size:14px}
#flyp .st{display:flex;gap:10px;align-items:flex-start;margin:8px 0;font-size:16px}#flyp .st .n{flex:0 0 26px;height:26px;border-radius:50%;background:#1f2a44;color:#fff;font-weight:700;font-size:13px;display:grid;place-items:center}
#flyp .box{margin-top:44px;font-size:16px}#flyp .step{font-size:16px}
@media (max-width:1000px){#flyp{width:92vw}body.flyon .wrap{margin-right:auto!important}}`;document.head.appendChild(st);
 const p=document.createElement('aside');p.id='flyp';p.setAttribute('aria-label','Calculator picture');document.addEventListener('DOMContentLoaded',()=>document.body.appendChild(p));if(document.body)document.body.appendChild(p);})();
function flyOpen(key){FLY.key=key;document.body.classList.add('flyon');flyDraw();document.getElementById('flyp').classList.add('on');}
function flyHTML(html){const p=document.getElementById('flyp');if(!p)return;FLY.key='__html';FLY.dismissed=false;document.body.classList.add('flyon');p.innerHTML='<button class="x" aria-label="Close">✕</button>'+html;p.classList.add('on');}
function flyFrame(url,title,tabs){const p=document.getElementById('flyp');if(!p)return;FLY.key='__frame';document.body.classList.add('flyon','flywide');p.classList.add('wide');
 p.innerHTML='<button class="x" aria-label="Close">✕</button><div style="font-size:12px;font-weight:800;letter-spacing:1.3px;color:#5a3290;margin:4px 0 6px">'+tEsc(title)+'</div>'+(tabs&&tabs.length>1?'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px">'+tabs.map(t=>'<button data-ffu="'+tEsc(t[1])+'" style="font:inherit;font-size:13px;font-weight:700;padding:3px 10px;border:2px solid #1f2a44;border-radius:8px;background:#fff;cursor:pointer">'+tEsc(t[0])+'</button>').join('')+'</div>':'')+'<iframe src="'+url+'" title="'+tEsc(title)+'"></iframe>';p.classList.add('on');}
document.addEventListener('click',e=>{const b=e.target.closest('[data-ffu]');if(b){const f=document.querySelector('#flyp iframe');if(f)f.src=b.dataset.ffu;}});
function flyClose(){document.body.classList.remove('flywide');const pp=document.getElementById('flyp');if(pp)pp.classList.remove('wide');if(FLY.key==='__html')FLY.dismissed=true;FLY.key=null;document.body.classList.remove('flyon');const p=document.getElementById('flyp');if(p)p.classList.remove('on');}
document.addEventListener('click',e=>{if(e.target.closest('#flyp .x')){flyClose();if(typeof render==='function')render();}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&FLY.key){flyClose();if(typeof render==='function')render();}});

/* math text -> JS function of x */
function toFn(t){let s=String(t).replace(/−/g,'-').replace(/[×·]/g,'*').replace(/÷/g,'/').replace(/²/g,'^2').replace(/³/g,'^3').replace(/π/g,'(PI)').replace(/√\s*\(/g,'sqrt(').replace(/√\s*(\d+(\.\d+)?)/g,'sqrt($1)');
 s=s.replace(/(\d|\)|x)\s*(?=\(|x|sqrt|\(PI\))/g,'$1*').replace(/\^/g,'**');
 if(/[^0-9x+\-*/().\sA-Za-z]/.test(s.replace(/sqrt|PI|abs/g,'')))return null;
 if(/[a-wyzA-Z]/.test(s.replace(/sqrt|PI|abs/g,'')))return null;
 try{const f=new Function('x','const {sqrt,PI,abs}=Math;return '+s);const v=f(1.234);return isFinite(v)?f:null}catch(e){return null}}
function toFnXY(t){let s=String(t).replace(/−/g,'-').replace(/[×·]/g,'*').replace(/÷/g,'/').replace(/²/g,'^2');s=s.replace(/(\d|\)|x|y)\s*(?=\(|x|y)/g,'$1*').replace(/\^/g,'**');if(/[^0-9xy+\-*/().\s]/.test(s))return null;try{const f=new Function('x','y','return '+s);return isFinite(f(1.1,2.2))?f:null}catch(e){return null}}
function parseDesmos(steps){const lines=[];
 steps.forEach(st=>{let m=st.match(/(?:Type|type)\s+(.+?)(?:\s*→.*)?$/);if(!m)return;let t=m[1].replace(/[.,;]\s*$/,'').replace(/\s+\((?=[^()]*[a-z]{3})[^()]*\)$/,'').trim();
  const stat=t.match(/^(mean|median)\(\[([^\]]+)\]\)/);
  if(stat){const a=stat[2].split(',').map(Number).sort((p,q)=>p-q);const v=stat[1]==='mean'?a.reduce((p,q)=>p+q,0)/a.length:(a.length%2?a[(a.length-1)/2]:(a[a.length/2-1]+a[a.length/2])/2);lines.push({txt:t,val:'= '+(+v.toFixed(4))});return;}
  const parts=t.split(/=(?![=])/);
  if(parts.length===2){const L=parts[0].trim(),R=parts[1].trim();
    if(/^(y|f\(x\)|g\(x\))$/.test(L)){const f=toFn(R);lines.push({txt:t,f});return;}
    const fl=toFn(L),fr=toFn(R);if(fl&&fr&&/x/.test(L+R)){lines.push({txt:'y = '+L,f:fl});lines.push({txt:'y = '+R,f:fr});return;}}
  if(parts.length===2&&/y/.test(t)&&!/[<>≤≥]/.test(t)){const g=toFnXY(parts[0]+'-('+parts[1]+')');if(g){const f=x=>{const a=g(x,0),b=g(x,1);return -a/(b-a)};if(isFinite(f(1.3))){lines.push({txt:t,f});return;}}}
  if(/[<>≤≥]/.test(t)){lines.push({txt:t});return;}
  const f=toFn(t);if(f&&!/x/.test(t)){lines.push({txt:t,val:'= '+(+f(0).toFixed(4))});return;}
  if(f)lines.push({txt:'y = '+t,f});else lines.push({txt:t});});
 return lines;}
function keyPoints(fs){const pts=[];if(fs.length>2)return pts;const xs=[];for(let x=-60;x<=60;x+=0.05)xs.push(+x.toFixed(2));
 const root=(g,a,b)=>{for(let i=0;i<60;i++){const m=(a+b)/2;(g(a)*g(m)<=0)?b=m:a=m;}return (a+b)/2;};
 const add=(x,y,kind)=>{if(isFinite(x)&&isFinite(y)&&!pts.some(p=>Math.abs(p.x-x)<1e-3))pts.push({x:Math.round(x*1000)/1000,y:Math.round(y*1000)/1000,kind});};
 if(fs.length>=2){const g=x=>fs[0](x)-fs[1](x);for(let i=1;i<xs.length;i++){const a=g(xs[i-1]),b=g(xs[i]);if(a===0)add(xs[i-1],fs[0](xs[i-1]),'cross');else if(a*b<0){const r=root(g,xs[i-1],xs[i]);add(r,fs[0](r),'cross');}}}
 else if(fs.length===1){const f=fs[0];for(let i=1;i<xs.length;i++){const a=f(xs[i-1]),b=f(xs[i]);if(a===0)add(xs[i-1],0,'zero');else if(a*b<0){add(root(f,xs[i-1],xs[i]),0,'zero');}}
   for(let i=1;i<xs.length-1;i++){const a=f(xs[i-1]),b=f(xs[i]),c=f(xs[i+1]);if((b<a&&b<=c)||(b>a&&b>=c)){let lo=xs[i-1],hi=xs[i+1];for(let k=0;k<60;k++){const m1=lo+(hi-lo)/3,m2=hi-(hi-lo)/3;((b<a)?(f(m1)<f(m2)):(f(m1)>f(m2)))?hi=m2:lo=m1;}const vx=(lo+hi)/2;add(vx,f(vx),'vertex');}}}
 return pts.slice(0,4);}
const COLS=['#c0392b','#2f6fb5','#2e7d4f','#7b4fa0'];
function graphSVG(lines){const fs=lines.filter(l=>l.f).map(l=>l.f);if(!fs.length)return '';const pts=keyPoints(fs);
 let xs=pts.map(p=>p.x).concat([0]),x0=Math.min(...xs),x1=Math.max(...xs);let pad=Math.max(3,(x1-x0)*0.35);x0-=pad;x1+=pad;if(x1-x0<10){const c=(x0+x1)/2;x0=c-5;x1=c+5;}
 let ys=[0].concat(pts.map(p=>p.y));for(let i=0;i<=40;i++){const x=x0+(x1-x0)*i/40;fs.forEach(f=>{const v=f(x);if(isFinite(v))ys.push(v)})}
 ys.sort((a,b)=>a-b);let y0=ys[Math.floor(ys.length*0.05)],y1=ys[Math.ceil(ys.length*0.95)-1];pts.forEach(p=>{y0=Math.min(y0,p.y);y1=Math.max(y1,p.y)});y0=Math.min(y0,0);y1=Math.max(y1,0);const yp=Math.max(2,(y1-y0)*0.18);y0-=yp;y1+=yp;
 const W=440,H=300,X=x=>(x-x0)/(x1-x0)*W,Y=y=>H-(y-y0)/(y1-y0)*H;
 const step=v=>{const r=v/8,p=Math.pow(10,Math.floor(Math.log10(r)));return [1,2,5,10].map(k=>k*p).find(k=>k>=r)};
 const sx=step(x1-x0),sy=step(y1-y0);let g='';
 for(let x=Math.ceil(x0/sx)*sx;x<=x1;x+=sx)g+=`<line x1="${X(x)}" x2="${X(x)}" y1="0" y2="${H}" stroke="#e5e9f0"/><text x="${X(x)+2}" y="${Math.min(H-4,Math.max(12,Y(0)+13))}" font-size="10" fill="#64748b">${+x.toFixed(4)}</text>`;
 for(let y=Math.ceil(y0/sy)*sy;y<=y1;y+=sy)g+=`<line y1="${Y(y)}" y2="${Y(y)}" x1="0" x2="${W}" stroke="#e5e9f0"/>${Math.abs(y)>1e-9?`<text x="${Math.min(W-30,Math.max(2,X(0)+3))}" y="${Y(y)-2}" font-size="10" fill="#64748b">${+y.toFixed(4)}</text>`:''}`;
 g+=`<line x1="${X(0)}" x2="${X(0)}" y1="0" y2="${H}" stroke="#1f2a44" stroke-width="1.5"/><line y1="${Y(0)}" y2="${Y(0)}" x1="0" x2="${W}" stroke="#1f2a44" stroke-width="1.5"/>`;
 fs.forEach((f,i)=>{let d='';for(let k=0;k<=300;k++){const x=x0+(x1-x0)*k/300,v=f(x);if(!isFinite(v))continue;const py=Math.max(-50,Math.min(H+50,Y(v)));d+=(d?'L':'M')+X(x).toFixed(1)+','+py.toFixed(1);}g+=`<path d="${d}" fill="none" stroke="${COLS[i%4]}" stroke-width="3"/>`;});
 pts.forEach(p=>{const fx=X(p.x),fy=Y(p.y),lx=fx>W-120?fx-118:fx+8;g+=`<circle cx="${fx}" cy="${fy}" r="7" fill="#64748b" stroke="#fff" stroke-width="2"/><rect x="${lx}" y="${fy-30}" width="112" height="22" rx="5" fill="#fff" stroke="#1f2a44"/><text x="${lx+56}" y="${fy-14}" text-anchor="middle" font-size="13" font-weight="700" fill="#1f2a44">(${+p.x.toFixed(3)}, ${+p.y.toFixed(3)})</text>`;});
 return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block;background:#fff">${g}</svg>`+(pts.length?`<div style="font-size:13px;padding:6px 10px;border-top:1.5px solid #cbd5e1;color:#4a5568">Gray dot = the point you click. It shows its (x, y).</div>`:'');}
function desmosPic(steps){const lines=parseDesmos(steps);if(!lines.length)return '';
 return `<div class="fl-lab">What your Desmos screen looks like</div><div class="ds"><div class="ds-top">Desmos · built into Bluebook (Calculator button, top right)</div>${lines.map((l,i)=>`<div class="ds-ex"><span class="ln">${i+1}</span>${l.f?`<span class="dot" style="background:${COLS[lines.slice(0,i).filter(z=>z.f).length%4]}"></span>`:''}<span>${tEsc(l.txt)}</span>${l.val?`<span class="val">${tEsc(l.val)}</span>`:''}</div>`).join('')}${graphSVG(lines)}</div>`;}
const KEYRX=/(2nd|enter|clear|sto→|X,T,θ,n|mode|graph|trace|y=|\(−\)|x²|n\/d|alpha|del|math|table|window|⌂|top-row key under [A-Z]+)/g;
function seqcaps(t){const m=t.match(/^Type\s+[^:]+:\s*(.+)$/);if(!m)return '';
 return (m[1].includes(' › ')?m[1].split(' › '):m[1].split(/,\s*(?![^()]*\))/)).map(ch=>{const hint=(ch.match(/\(([^)]*)\)/)||[])[1];ch=ch.replace(/\([^)]*\)/,'').trim();
  return ch.split(/\s+/).filter(Boolean).map(k=>`<span class="kc ${/^\d+$/.test(k)?'num':(k==='enter'?'':'y')}">${tEsc(k)}</span>`).join('')+(hint?`<span style="font-size:12px;color:#cbd5e1">(${tEsc(hint)})</span>`:'');}).join('<span style="color:#94a3b8">›</span>');}
function keycaps(t){const sq=seqcaps(t);if(sq)return sq;const out=[];let m;KEYRX.lastIndex=0;while((m=KEYRX.exec(t))){let k=m[1];const soft=k.startsWith('top-row');out.push(`<span class="kc ${soft?'soft':(/^(2nd)$/.test(k)?'b':(k==='⌂'?'y':''))}">${tEsc(soft?k.replace('top-row key under ',''):k)}</span>`);}
 const d=t.match(/⌂,?\s*then\s*(\d)|⌂\s*(\d)/);if(d)out.splice(1,0,`<span class="kc num">${d[1]||d[2]}</span>`);return out.join('');}
function tiPic(steps,n){const scr=[];steps.forEach((s,i)=>{if(i>=n)return;const ty=s.match(/^Type\s+([^:→]+?)\s*(?::|$)/);if(ty&&!/→/.test(s)){scr.push(`<div>${tEsc(ty[1])}</div>`);return;}const m=s.match(/(?:Type\s+)?(.+?)\s*(?:enter\s*)?→\s*(.+)$/);if(m){scr.push(`<div>${tEsc(m[1].replace(/^Type\s+/,'').replace(/:\s.*$/,''))}</div><div class="r">${tEsc(m[2])}</div>`);}else{const e=s.match(/^=\s*(.+)/);if(e)scr.push(`<div class="r">${tEsc(e[1])}</div>`);}});
 return `<div class="fl-lab">What your TI-84 Evo looks like</div><div class="ti"><div class="ti-scr">${scr.slice(-4).join('')||'<span style="color:#4b5563">(the screen fills in as you do each step)</span>'}</div>
  <div style="font-size:12px;color:#cbd5e1;margin:10px 0 2px;letter-spacing:1px">KEYS FOR EACH STEP</div>
  ${steps.map((s,i)=>{const k=keycaps(s);return `<div style="display:flex;gap:8px;align-items:center;margin:6px 0;${i>=n?'opacity:.4':''}"><span style="min-width:22px;height:22px;border-radius:50%;border:2px solid #c4a8e8;color:#e9ddf8;font-weight:700;display:inline-flex;align-items:center;justify-content:center;font-size:12px">${i+1}</span><div class="ti-keys">${k||`<span class="ti-type">${tEsc(s.replace(/^Type\s+/,''))}</span>`}</div></div>`}).join('')}
  <div style="font-size:12px;color:#cbd5e1;margin-top:8px">Purple keys = the top-row key right under that word on the screen.</div></div>`;}
function flyDraw(){const p=document.getElementById('flyp');if(!p||!FLY.key||!TS[FLY.key])return;const st=TS[FLY.key],card=st.card;if(!card)return;
 let M=TOOLS.M[card.m],useAlt=false;if(M.tool==='By hand'&&card.alt&&TOOLS.M[card.alt]){M=TOOLS.M[card.alt];useAlt=true;}
 const steps=(!useAlt&&card.steps&&card.steps.length)?card.steps:M.steps;const n=useAlt?st.an:st.n;
 const picSteps=(!useAlt&&card.steps&&card.steps.length)?card.steps:M.steps;
 let h=`<button class="x" aria-label="Close">✕</button><h3>${M.tool==='Desmos'?'📈':'🧮'} ${tEsc(M.tool)}</h3><div class="sub">${tEsc(M.name)}${useAlt?' · the calculator way for this one':''}</div>`;
 h+=M.tool==='Desmos'?(desmosPic(picSteps)||desmosPic(M.steps)):tiPic(picSteps,M.tool==='TI-84 Evo'?Math.max(n,1):n);
 h+=`<div class="fl-lab">Your steps (the purple box is where you are)</div>`+steps.map((s,i)=>`<div class="fl-step ${i===n-1?'now':i>=n?'later':''}"><span class="n">${i+1}</span><span>${tEsc(s)}</span></div>`).join('');
 if(M.tool==='Desmos'||M.tool==='TI-84 Evo')h+=`<div class="fl-lab">Which buttons</div>`+M.steps.map((s,i)=>`<div class="fl-step"><span class="n">${i+1}</span><span>${tEsc(s)}</span></div>`).join('');
 p.innerHTML=h;}
