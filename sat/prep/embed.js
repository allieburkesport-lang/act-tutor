/* HELM shell (Allie, Nov 23): SAT Helm runs inside the HELM site (index.html) so the HELM left menu stays on every page.
   When this page is inside that frame: hide its own top bar / sidebar, keep the HELM address bar in step,
   and send links to other HELM pages to the top window. Opened on its own, nothing changes. */
(function () {
  if (window.top === window.self) {   // opened on its own (old bookmark / email link): open it inside HELM instead
    if (/\/prep\/sat\.html$/.test(location.pathname)) location.replace('./' + (location.hash || '#/'));
    else if (/\/drill-zone\/report\.html$/.test(location.pathname)) location.replace('../prep/#report');
    return;
  }
  var R = document.documentElement; R.classList.add('in-helm');
  var st = document.createElement('style');
  st.textContent = '.helm-who{display:none!important}html.in-helm header.top{display:none!important}html.in-helm .bi .side2{display:none!important}html.in-helm .bi .shell2{grid-template-columns:minmax(0,1fr)!important}html.in-helm .bi .side2+*{min-width:0}html.in-helm .bi .shell2{min-height:0!important}';
  (document.head || R).appendChild(st);
  var T; try { T = window.top.location.href && window.top } catch (e) { return }
  var base = T.location.pathname;
  var sync = function () { if (/\/sat\.html$/.test(location.pathname)) { try { T.history.replaceState(null, '', base + (location.hash || '#/')); T.HELM_FRAME_SYNC && T.HELM_FRAME_SYNC(location.hash || '#/') } catch (e) {} } };
  addEventListener('hashchange', sync); sync();
  // One scrollbar: the frame grows to fit the page, so the whole HELM window scrolls (drill screens keep a full-window frame with their own footer).
  var fit = function () { try {
    var f = T.document.getElementById('appframe'); if (!f) return;
    var top = f.getBoundingClientRect().top + T.scrollY, full = Math.max(400, T.innerHeight - top);
    var drill = !!document.querySelector('.dr');
    var h = drill ? full : Math.max(full, document.body.scrollHeight);
    if (Math.abs((parseFloat(f.style.height) || 0) - h) > 2) f.style.height = h + 'px';
    R.style.overflowY = drill ? '' : 'hidden';
  } catch (e) {} };
  try { new ResizeObserver(fit).observe(document.body || R) } catch (e) {}
  addEventListener('load', fit); setInterval(fit, 1000);
  addEventListener('hashchange', function () { try { T.scrollTo(0, 0) } catch (e) {} setTimeout(fit, 50) });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a || a.target === '_blank' || e.defaultPrevented) return;
    var h = a.getAttribute('href') || ''; if (h.charAt(0) === '#') return;
    var u; try { u = new URL(a.href) } catch (x) { return } if (u.origin !== location.origin) return;
    e.preventDefault();
    if (/\/sat\.html$/.test(u.pathname)) { if (u.pathname === location.pathname) location.hash = u.hash || '#/'; else T.location.hash = u.hash || '#/'; return }
    if (/\/drill-zone\/report\.html$/.test(u.pathname)) { T.location.hash = '#report'; return }
    T.location.href = u.href;
  }, true);
})();
