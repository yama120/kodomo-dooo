# shared.js v2：旧 shared.js（_build/src/shared.v1.js）の共通機能（ChibiPlan / Chibi / ChibiAuth / 地域・お気に入り / いいね同期）を残し、
# ヘッダー・フッター・メニューを新デザイン（prod_common の HEADER_HTML / SHEET_HTML / FOOTER_HTML）に差し替える
import os,re,json,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
src=open(D+'_build/src/shared.v1.js',encoding='utf-8').read()

def cut(s,start,end,repl):
    a=s.index(start); b=s.index(end,a); return s[:a]+repl+s[b:]

# 1) CSS：ヘッダー系は chrome.css に移したので最小限だけ残す
NEW_CSS='''  var CSS = `
    .cc-hidden{ display:none !important; }
    html{ scroll-behavior:smooth; }
    @media (max-width: 768px){
      input:not([type="checkbox"]):not([type="radio"]), select, textarea { font-size:16px !important; }
    }
  `;
'''
src=cut(src,'  var CSS = `','  /* ---------- ヘッダー ---------- */',NEW_CSS+'\n')

# 2) ヘッダー／シート／フッター（生成物を JSON 文字列で埋め込む）
TPL=('  /* ---------- ヘッダー・メニュー・フッター（生成物：_build/src/prod_shared.py。直接編集しない） ---------- */\n'
     '  var CHROME_V = '+json.dumps(C.V)+';\n'
     '  var FONT_URL = '+json.dumps(C.FONT_URL)+';\n'
     '  var HEADER = '+json.dumps(C.HEADER_HTML,ensure_ascii=False)+';\n'
     '  var SHEET = '+json.dumps(C.SHEET_HTML,ensure_ascii=False)+';\n'
     '  var FOOTER = '+json.dumps(C.FOOTER_HTML,ensure_ascii=False)+';\n')
src=cut(src,'  /* ---------- ヘッダー ---------- */','  /* =======================================================================\n     チビスポ Phase1',TPL+'\n')

# 3) お気に入り：新カード（a.nc[data-id]）を先に、旧カード（a.club-card）は残す
NEW_FAVS='''  function decorateFavs() {
    /* 新カード（club-card.js v2 / a.nc）：右上の♡と下の♡数の両方でお気に入りを切り替える */
    document.querySelectorAll('a.nc[data-id]').forEach(function (card) {
      if (card.__favBound) return;
      var id = card.getAttribute('data-id');
      var nameEl = card.querySelector('.nc-name');
      var name = card.getAttribute('data-name') || (nameEl ? nameEl.textContent.trim() : '');
      var favBtn = card.querySelector('.nc-fav'), lk = card.querySelector('.nc-foot .lk');
      var img = card.querySelector('img');
      function render() {
        var on = Chibi.isFav(id);
        if (favBtn) favBtn.classList.toggle('on', on);
        if (lk) lk.classList.toggle('on', on);
      }
      function toggle(e) {
        e.preventDefault(); e.stopPropagation();
        Chibi.toggleFav({ id: id, name: name, area: card.getAttribute('data-area') || '', href: card.getAttribute('href') || '#', img: img ? (img.getAttribute('src') || '') : '' });
        render();
      }
      if (favBtn) { favBtn.setAttribute('title', 'お気に入り'); favBtn.addEventListener('click', toggle); }
      if (lk) { lk.style.cursor = 'pointer'; lk.addEventListener('click', toggle); }
      card.__favBound = true; card.__favRender = render; render();
    });
    /* 旧カード（まだ置き換えていないページ用） */
    document.querySelectorAll('a.club-card:not(.nc)').forEach(function (card) {
      if (card.__favBound) return;
      var h = card.querySelector('h3');
      var name = h ? h.textContent.trim() : '';
      if (!name) return;
      var heartSvg = null, svgs = card.querySelectorAll('svg');
      for (var i = 0; i < svgs.length; i++) {
        var p = svgs[i].querySelector('path');
        if (p && (p.getAttribute('d') || '').indexOf('M12 20.3') === 0) { heartSvg = svgs[i]; break; }
      }
      if (!heartSvg) return;
      var likeEl = heartSvg.parentElement;
      var img = card.querySelector('img');
      var area = '';
      card.querySelectorAll('span').forEach(function (el) {
        if (!area && el.children.length === 0) { var t = el.textContent.trim(); if (/[都道府県市区町村]/.test(t) && t.length <= 30) area = t; }
      });
      var hrefVal = card.getAttribute('href') || '';
      var idMatch = /[?&]id=([^&]+)/.exec(hrefVal);
      var id = idMatch ? decodeURIComponent(idMatch[1]) : ('club-' + encodeURIComponent(name));
      function render() {
        var fav = Chibi.isFav(id);
        if (fav) { heartSvg.setAttribute('fill', '#E43B4D'); heartSvg.removeAttribute('stroke'); }
        else { heartSvg.setAttribute('fill', 'none'); heartSvg.setAttribute('stroke', '#9aa3ad'); heartSvg.setAttribute('stroke-width', '1.9'); }
      }
      likeEl.style.cursor = 'pointer'; likeEl.setAttribute('title', 'お気に入り');
      likeEl.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        Chibi.toggleFav({ id: id, name: name, area: area, href: hrefVal || '#', img: img ? img.getAttribute('src') : '' });
        render();
      });
      card.__favBound = true; card.__favRender = render; render();
    });
  }
'''
src=cut(src,'  function decorateFavs() {','  // 非同期でカードが増えても自動でお気に入りを結線',NEW_FAVS)
src=src.replace("document.querySelectorAll('a.club-card').forEach(function (c) { if (c.__favRender) c.__favRender(); });",
                "document.querySelectorAll('a.club-card, a.nc').forEach(function (c) { if (c.__favRender) c.__favRender(); });")
src=src.replace("document.querySelectorAll('.cc-mood-tag[data-mood]').forEach(function (el) {","document.querySelectorAll('.cc-mood-tag[data-mood], .nc-tags span[data-mood]').forEach(function (el) {")

# 4) init：chrome.css と書体を読み、ヘッダー／フッターが無いページにだけ注入。シートは全ページ
NEW_INIT='''  /* ---------- ボトムシート（ハンバーガー） ---------- */
  function bindSheet() {
    var bd = document.getElementById('shBd'), sh = document.getElementById('sheet'), open = false;
    if (!bd || !sh) return;
    function set(v) { open = v; bd.classList.toggle('on', v); sh.classList.toggle('on', v); document.documentElement.style.overflow = v ? 'hidden' : ''; }
    document.querySelectorAll('.hd-burger').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); set(!open); }); });
    bd.addEventListener('click', function () { set(false); });
    var x = sh.querySelector('.sh-x'); if (x) x.addEventListener('click', function () { set(false); });
    sh.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }
  /* いま開いているページのナビに下線。地域ページ（/clubs/…）は「クラブを探す」 */
  function markActiveNav() {
    var here = (location.pathname.split('/').pop() || 'index.html');
    if (/^\\/clubs\\//.test(location.pathname)) here = 'search.html';
    document.querySelectorAll('.hd-nav a').forEach(function (a) {
      if ((a.getAttribute('href') || '').split('?')[0].split('#')[0] === here) a.classList.add('on');
    });
  }
  function ensureChrome() {
    var head = document.head;
    if (!document.querySelector('link[href^="site.css"]') && !document.getElementById('cc-chrome-css')) {
      var l = document.createElement('link'); l.id = 'cc-chrome-css'; l.rel = 'stylesheet'; l.href = 'chrome.css?v=' + CHROME_V; head.appendChild(l);
    }
    if (!document.querySelector('link[href*="Zen+Kaku+Gothic+New"]')) {
      var f = document.createElement('link'); f.rel = 'stylesheet'; f.href = FONT_URL; head.appendChild(f);
    }
    var style = document.createElement('style'); style.id = 'cc-shared-style'; style.textContent = CSS; head.appendChild(style);
  }

  function init() {
    ensureChrome();
    if (!document.querySelector('header.site-hd')) document.body.insertAdjacentHTML('afterbegin', HEADER);
    if (!document.querySelector('footer.site-ft')) document.body.insertAdjacentHTML('beforeend', FOOTER);
    if (!document.getElementById('sheet')) document.body.insertAdjacentHTML('beforeend', SHEET);
    bindSheet();
    markActiveNav();
    bindHover(document);
    initFeatures();
    updateAuthUI();
  }

'''
src=cut(src,'  function init() {','  // supabase-lite.js が未読込なら動的に読み込む',NEW_INIT)

# 5) ログイン表示：body.auth-in と .hd-in の行き先・アバター。旧ページの cc-auth-* も引き続き切り替える
NEW_AUTH='''  function applyAuthUI(prof) {
    var loggedIn = !!prof;
    var target = (prof && prof.role === 'club') ? 'club-mypage.html' : 'mypage.html';
    var name = loggedIn ? (prof.display_name || (prof.email ? prof.email.split('@')[0] : 'M')) : '';
    var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
    var col = AUTH_AV_COLORS[h % AUTH_AV_COLORS.length];
    var ini = (name.charAt(0) || 'M').toUpperCase().replace(/[<>&"]/g, '');
    document.body.classList.toggle('auth-in', loggedIn);
    /* ログイン中で、まだ地域を選んでいなければ、登録した地域を既定にする */
    try {
      if (loggedIn && (prof.pref || prof.city) && !Chibi.getRegionPref() && !Chibi.getRegionCity()) {
        Chibi.setRegionParts(prof.pref || '', prof.city || '');
      }
    } catch (e) {}
    document.querySelectorAll('.hd-in').forEach(function (el) {
      el.setAttribute('href', target);
      var av = el.querySelector('.hd-av');
      if (av && loggedIn) { av.textContent = ini; av.style.background = col[0]; av.style.color = col[1]; }
    });
    /* まだ置き換えていないページ本文の導線（cc-auth-out / cc-auth-in） */
    document.querySelectorAll('.cc-auth-out').forEach(function (el) { el.classList.toggle('cc-hidden', loggedIn); });
    document.querySelectorAll('.cc-auth-in').forEach(function (el) { el.classList.toggle('cc-hidden', !loggedIn); el.setAttribute('href', target); });
  }
'''
src=cut(src,'  function applyAuthUI(prof) {','  function updateAuthUI() {',NEW_AUTH)


# 3.5) 未ログインのブラウザに地域を持ち越さない（検索の既定を「全国」に戻す）
BOOT = """(function () {
  'use strict';

  /* ---------- 地域の持ち越しをやめる（タブを開くたびに1回だけ判定） ----------
     未ログインなら、前に選んだ地域（localStorage）を消して「全国」から始める。
     ログイン中はそのまま。開いている間に選んだ地域は、そのセッションでは残る。 */
  (function () {
    try {
      if (sessionStorage.getItem('chibi_region_boot')) return;
      sessionStorage.setItem('chibi_region_boot', '1');
      var signedIn = false, i, k;
      for (i = 0; i < localStorage.length; i++) {
        k = localStorage.key(i);
        if (k && /^sb-.*-auth(-token)?$/.test(k)) { signedIn = true; break; }
      }
      if (!signedIn) {
        localStorage.removeItem('chibi_region_pref');
        localStorage.removeItem('chibi_region_city');
        localStorage.removeItem('chibi_region');
      }
    } catch (e) {}
  })();
"""
src=src.replace("(function () {\n  'use strict';\n", BOOT, 1)
assert 'chibi_region_boot' in src


# 3.6) 準備中サービスの「お知らせを受け取る」を waitlist に保存する（端末内に貯めるだけだった）
WL_API = """      ready: function () { return !!db(); },
      client: db,
      // 準備中サービスの「お知らせを受け取る」。unique(email,topic) なので重複は成功扱い
      joinWaitlist: function (email, topic, source) {
        return fetch(SB_URL + '/rest/v1/waitlist', {
          method: 'POST',
          headers: { 'apikey': SB_KEY, 'Authorization': 'Bearer ' + SB_KEY, 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
          body: JSON.stringify({ email: email, topic: topic || 'video', source: source || location.pathname })
        }).then(function (r) {
          if (!r.ok && r.status !== 409) throw new Error('waitlist ' + r.status);
          /* 運営に知らせる。届かなくても登録は保存済み */
          if (r.status !== 409) {
            fetch(SB_URL + '/functions/v1/notify-inquiry', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + SB_KEY },
              body: JSON.stringify({ type: 'waitlist', topic: topic || 'video', email: email, source: source || location.pathname })
            }).catch(function () {});
          }
          return true;
        });
      },
"""
src=src.replace("      ready: function () { return !!db(); },\n      client: db,\n", WL_API, 1)
assert 'joinWaitlist' in src

WL_FORM = """  /* ---------- 準備中サービスの「お知らせを受け取る」 ----------
     どのページの .soon-f でも、ここ1か所で waitlist に保存する。
     通信できなかったときだけ端末に控える（あとから拾えるように）。 */
  document.addEventListener('submit', function (e) {
    var f = e.target && e.target.closest ? e.target.closest('.soon-f') : null;
    if (!f) return;
    e.preventDefault();
    var input = f.querySelector('input[type="email"]') || f.querySelector('input');
    var em = ((input && input.value) || '').trim();
    if (!em) return;
    var topic = f.getAttribute('data-topic') || 'video';
    var btn = f.querySelector('button'); if (btn) btn.disabled = true;
    function done() {
      f.hidden = true;
      var ok = f.parentElement && f.parentElement.querySelector('.soon-ok');
      if (ok) ok.hidden = false;
    }
    function keepLocal() {
      try {
        var a = JSON.parse(localStorage.getItem('chibispo_waitlist') || '[]');
        a.push({ email: em, topic: topic, at: new Date().toISOString() });
        localStorage.setItem('chibispo_waitlist', JSON.stringify(a));
      } catch (x) {}
    }
    if (window.ChibiAuth && ChibiAuth.joinWaitlist) {
      ChibiAuth.joinWaitlist(em, topic, location.pathname).then(done).catch(function () { keepLocal(); done(); });
    } else { keepLocal(); done(); }
  }, true);

  if (document.readyState === 'loading') {"""
src=src.replace("  if (document.readyState === 'loading') {", WL_FORM, 1)
assert 'soon-f' in src

src=src.replace('''/* =========================================================================
   チビスポ 共通ヘッダー / フッター コンポーネント''','''/* =========================================================================
   チビスポ 共通ヘッダー / フッター コンポーネント（v2・2026-09-13 新デザイン）
   ★ヘッダー・フッター・メニューの HTML は _build/src/prod_shared.py が生成して埋め込む。
     文言やリンクを変えるときは header_v2.py / prod_common.py を直して python3 prod_shared.py を流す。''',1)
open(D+'shared.js','w',encoding='utf-8').write(src)
print('shared.js',len(src)//1024,'KB')
