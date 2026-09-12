/* チビスポ クラブHP見本 共通：色を選ぶ（3色切替）
   使い方：<script src="theme-picker.js" defer data-themes='[{"id":"a","name":"…","sw":["#hex","#hex"]},…]'></script>
   ・<html data-theme="b"> を付け替える。色の定義は各サイトの style.css の html[data-theme="…"] に置く
   ・URL ?theme=b で開ける（営業で見せるとき用）。選択は localStorage にパスごとに記憶
   ・見本用のUIなので、本番化ではこの script タグを外すだけでよい */
(function () {
  'use strict';
  var me = document.currentScript; if (!me) return;
  var themes; try { themes = JSON.parse(me.getAttribute('data-themes') || '[]'); } catch (e) { themes = []; }
  if (themes.length < 2) return;
  var KEY = 'chibispo-theme:' + location.pathname;
  var q = new URLSearchParams(location.search).get('theme');
  var saved = null; try { saved = localStorage.getItem(KEY); } catch (e) {}
  var cur = themes.some(function (t) { return t.id === q; }) ? q : (themes.some(function (t) { return t.id === saved; }) ? saved : themes[0].id);

  var css = '.tp{position:fixed;right:16px;bottom:16px;z-index:80;font-family:"Noto Sans JP","Hiragino Sans",system-ui,sans-serif;font-size:12px;line-height:1;color:#1c1c1c}'
    + '.tp__btn{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid rgba(0,0,0,.22);border-radius:8px;padding:9px 12px 9px 9px;box-shadow:0 8px 24px -12px rgba(0,0,0,.35);cursor:pointer;font:inherit;color:inherit}'
    + '.tp__dot{width:16px;height:16px;border-radius:50%;background:linear-gradient(135deg,var(--tp1) 50%,var(--tp2) 50%);border:1px solid rgba(0,0,0,.15)}'
    + '.tp__pop{position:absolute;right:0;bottom:calc(100% + 8px);background:#fff;border:1px solid rgba(0,0,0,.18);border-radius:10px;padding:8px;box-shadow:0 16px 40px -16px rgba(0,0,0,.4);display:none;min-width:168px}'
    + '.tp.is-open .tp__pop{display:block}'
    + '.tp__lab{font-size:10px;letter-spacing:.14em;color:#777;padding:4px 8px 6px}'
    + '.tp__it{display:flex;align-items:center;gap:10px;width:100%;padding:8px;border-radius:8px;cursor:pointer;font:inherit;color:inherit;background:none;border:0;text-align:left}'
    + '.tp__it:hover{background:#f2f2f2}.tp__it[aria-checked="true"]{background:#111;color:#fff}'
    + '.tp__it .tp__dot{width:20px;height:20px}'
    + '@media(max-width:760px){.tp{bottom:calc(76px + env(safe-area-inset-bottom) + 12px);right:12px}}'
    + '@media print{.tp{display:none}}';
  var st = document.createElement('style'); st.textContent = css + animCss; document.head.appendChild(st);

  var animCss = 'html.tp-anim, html.tp-anim *, html.tp-anim *::before, html.tp-anim *::after{transition:background-color .6s ease, color .6s ease, border-color .6s ease, box-shadow .6s ease, fill .6s ease !important}'
    + '.tp__ripple{position:fixed;left:0;top:0;width:24px;height:24px;margin:-12px 0 0 -12px;border-radius:50%;pointer-events:none;z-index:79;opacity:.42;transform:scale(0);animation:tpRipple .9s cubic-bezier(.2,.7,.2,1) forwards}'
    + '@keyframes tpRipple{to{transform:scale(160);opacity:0}}';
  function setTheme(id) {
    if (id === themes[0].id) document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', id);
  }
  function apply(id, save, ev) {
    cur = id;
    var t = themes.filter(function (x) { return x.id === id; })[0];
    if (save) {
      try { localStorage.setItem(KEY, id); } catch (e) {}
      /* 波紋：ボタンの位置から新しい差し色が広がり、その裏で色がなめらかに変わる */
      var rp = document.createElement('span'); rp.className = 'tp__ripple'; rp.style.background = t.sw[1];
      var x = ev && ev.clientX ? ev.clientX : (window.innerWidth - 40), y = ev && ev.clientY ? ev.clientY : (window.innerHeight - 40);
      rp.style.left = x + 'px'; rp.style.top = y + 'px'; document.body.appendChild(rp);
      setTimeout(function () { rp.remove(); }, 1000);
      document.documentElement.classList.add('tp-anim');
      setTimeout(function () { setTheme(id); }, 120);
      setTimeout(function () { document.documentElement.classList.remove('tp-anim'); }, 900);
    } else { setTheme(id); }
    if (btnDot) { btnDot.style.setProperty('--tp1', t.sw[0]); btnDot.style.setProperty('--tp2', t.sw[1]); }
    if (btnTxt) btnTxt.textContent = t.name;
    items.forEach(function (b) { b.setAttribute('aria-checked', String(b.getAttribute('data-id') === id)); });
  }
  var btnDot = null, btnTxt = null, items = [];
  apply(cur, false);

  function build() {
    var root = document.createElement('div'); root.className = 'tp';
    var btn = document.createElement('button'); btn.className = 'tp__btn'; btn.type = 'button'; btn.setAttribute('aria-haspopup', 'listbox'); btn.setAttribute('aria-expanded', 'false');
    btnDot = document.createElement('span'); btnDot.className = 'tp__dot'; btnTxt = document.createElement('span');
    btn.appendChild(btnDot); btn.appendChild(document.createTextNode('色を選ぶ：')); btn.appendChild(btnTxt);
    var pop = document.createElement('div'); pop.className = 'tp__pop'; pop.setAttribute('role', 'listbox');
    var lab = document.createElement('div'); lab.className = 'tp__lab'; lab.textContent = 'COLOR'; pop.appendChild(lab);
    themes.forEach(function (t) {
      var it = document.createElement('button'); it.type = 'button'; it.className = 'tp__it'; it.setAttribute('role', 'option'); it.setAttribute('data-id', t.id);
      var d = document.createElement('span'); d.className = 'tp__dot'; d.style.setProperty('--tp1', t.sw[0]); d.style.setProperty('--tp2', t.sw[1]);
      it.appendChild(d); it.appendChild(document.createTextNode(t.name));
      it.addEventListener('click', function (ev) { apply(t.id, true, ev); root.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); });
      pop.appendChild(it); items.push(it);
    });
    btn.addEventListener('click', function () { var o = !root.classList.contains('is-open'); root.classList.toggle('is-open', o); btn.setAttribute('aria-expanded', String(o)); });
    document.addEventListener('click', function (e) { if (!root.contains(e.target)) { root.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { root.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); } });
    root.appendChild(btn); root.appendChild(pop); document.body.appendChild(root);
    apply(cur, false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
