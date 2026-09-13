/* =========================================================================
   チビスポ 共通ヘッダー / フッター コンポーネント（v2・2026-09-13 新デザイン）
   ★ヘッダー・フッター・メニューの HTML は _build/src/prod_shared.py が生成して埋め込む。
     文言やリンクを変えるときは header_v2.py / prod_common.py を直して python3 prod_shared.py を流す。
   - 全ページ共通。このファイル1つを直せば全ページのヘッダー・フッターが変わる。
   - 各ページは <script src="shared.js"></script> を </body> 直前に置くだけ。
   - ヘッダー / ボトムシートメニュー / 下部タブバー / フッター を body に注入する。
   ========================================================================= */
(function () {
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

  /* ---------- 掲載プランによる表示順（クラブ一覧を出す全ページで共通） ----------
     プロ＝最上位、スタンダード＝上位、フリー＝通常。期限切れはフリー扱い。
     teams.plan の実値は free / pr / pr-plus の3つだけ。
     並べ替えは安定ソートなので、同じランクの中の並び（新着順・距離順）は
     呼び出し側のまま保たれる。順序を変えたい一覧は必ずここを通すこと。 */
  window.ChibiPlan = {
    rank: function (t) {
      if (!t || !t.plan || t.plan === 'free') return 0;
      if (t.plan_expires_at && new Date(t.plan_expires_at) < new Date()) return 0;
      return t.plan === 'pr-plus' ? 2 : 1;
    },
    sort: function (list) {
      return (list || []).slice().sort(function (a, b) {
        return window.ChibiPlan.rank(b) - window.ChibiPlan.rank(a);
      });
    }
  };

  /* ---------- 共通CSS（ヘッダー・メニュー・下部バー・フッターのレスポンシブ） ---------- */
  var CSS = `
    .cc-hidden{ display:none !important; }
    html{ scroll-behavior:smooth; }
    @media (max-width: 768px){
      input:not([type="checkbox"]):not([type="radio"]), select, textarea { font-size:16px !important; }
    }
  `;

  /* ---------- ヘッダー・メニュー・フッター（生成物：_build/src/prod_shared.py。直接編集しない） ---------- */
  var CHROME_V = "20260925";
  var FONT_URL = "https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@700;900&family=Zen+Old+Mincho:wght@600;900&family=Anton&display=swap";
  var HEADER = "<header class=\"site-hd\">\n  <div class=\"wrap hd\">\n    <a class=\"logo\" href=\"index.html\"><img class=\"lg-w\" src=\"assets/logo-wide.webp?v=2\" alt=\"チビスポ｜地域スポーツを、もっと身近に。\" width=\"700\" height=\"220\"><img class=\"lg-s\" src=\"assets/logo-sm.webp?v=2\" alt=\"チビスポ\" width=\"336\" height=\"96\"><span class=\"logo-tg\">地域スポーツを、もっと身近に。</span></a>\n    <nav class=\"hd-nav\">\n      <a href=\"search.html\">クラブを探す</a>\n      <a href=\"map.html\">地図から探す</a>\n      <a href=\"about.html\">チビスポとは</a>\n      <a href=\"partner.html\">クラブ・事業者の方へ</a>\n    </nav>\n    <div class=\"hd-r\">\n      <a class=\"hd-ic\" href=\"mypage.html#fav\"><svg viewBox=\"0 0 24 24\"><path d=\"M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9z\"/></svg><span>お気に入り</span></a>\n      <a class=\"hd-ic hd-out\" href=\"club-mypage.html\"><svg viewBox=\"0 0 24 24\"><path d=\"M3 20h18\"/><path d=\"M5 20V9l7-5 7 5v11\"/><path d=\"M10 20v-5h4v5\"/></svg><span>クラブログイン</span></a>\n      <a class=\"hd-ic hd-out\" href=\"login.html\"><svg viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"8\" r=\"3.6\"/><path d=\"M4.5 20a7.5 7.5 0 0 1 15 0\"/></svg><span>ログイン</span></a>\n      <a class=\"hd-ic hd-in\" href=\"mypage.html\"><span class=\"hd-av\">M</span><span>マイページ</span></a>\n      <a class=\"hd-cta\" href=\"listing.html\">クラブを載せる</a>\n      <button class=\"hd-burger\" type=\"button\" aria-label=\"メニューを開く\"><span></span><span></span><span></span></button>\n    </div>\n  </div>\n</header>";
  var SHEET = "<div class=\"sh-bd\" id=\"shBd\"></div><div class=\"sheet\" id=\"sheet\" role=\"dialog\" aria-label=\"メニュー\"><div class=\"sh-hd\"><img src=\"assets/logo-sm.webp?v=2\" alt=\"チビスポ\" width=\"336\" height=\"96\"><button class=\"sh-x\" type=\"button\" aria-label=\"閉じる\">&times;</button></div><div class=\"sh-grid\"><a href=\"search.html\"><svg viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"6.5\"/><path d=\"M16 16l4.5 4.5\"/></svg><span>クラブを探す</span></a><a href=\"map.html\"><svg viewBox=\"0 0 24 24\"><path d=\"M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z\"/><circle cx=\"12\" cy=\"10\" r=\"2.6\"/></svg><span>地図から探す</span></a><a href=\"magazine.html\"><svg viewBox=\"0 0 24 24\"><path d=\"M4 5h7a2 2 0 0 1 2 2v13a1.5 1.5 0 0 0-1.5-1.5H4z\"/><path d=\"M20 5h-7a2 2 0 0 0-2 2v13a1.5 1.5 0 0 1 1.5-1.5H20z\"/></svg><span>マガジン</span></a><a href=\"mypage.html#fav\"><svg viewBox=\"0 0 24 24\"><path d=\"M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9z\"/></svg><span>お気に入り</span></a><a href=\"about.html\"><svg viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M12 11v5\"/><circle cx=\"12\" cy=\"8\" r=\".6\"/></svg><span>チビスポとは</span></a><a href=\"faq.html\"><svg viewBox=\"0 0 24 24\"><path d=\"M4 5h16v11H9l-5 4z\"/><path d=\"M12 8v3\"/><circle cx=\"12\" cy=\"13.5\" r=\".6\"/></svg><span>よくある質問</span></a><a href=\"contact.html\"><svg viewBox=\"0 0 24 24\"><rect x=\"3\" y=\"5\" width=\"18\" height=\"14\" rx=\"2\"/><path d=\"M3 7l9 6 9-6\"/></svg><span>お問い合わせ</span></a><a href=\"partner.html\"><svg viewBox=\"0 0 24 24\"><path d=\"M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16\"/><path d=\"M15 10h4a1 1 0 0 1 1 1v10\"/><path d=\"M8 8h3M8 12h3M8 16h3M4 21h16\"/></svg><span>クラブ・<br>事業者の方へ</span></a></div><a class=\"sh-btn pri\" href=\"listing.html\">クラブを載せる（無料から）</a><a class=\"sh-btn hd-out\" href=\"login.html\">一般（保護者）ログイン / 会員登録</a><a class=\"sh-btn hd-out\" href=\"club-mypage.html\">クラブ運営者ログイン（掲載・管理）</a><a class=\"sh-btn hd-in\" href=\"mypage.html\">マイページ</a><div class=\"sh-ft\"><a href=\"legal.html#terms\">利用規約</a><a href=\"legal.html#privacy\">プライバシーポリシー</a></div></div>";
  var FOOTER = "<footer class=\"site-ft\">\n  <div class=\"wrap ft\">\n    <div class=\"ft-l\">\n      <div class=\"ft-logo\">チビ<span>スポ</span></div>\n      <p>チビスポは、地域・種目・雰囲気から、お子さまに合うスポーツクラブが見つかるサービスです。地図で近くから探せて、体験の申込みもそのまま。</p>\n      <div class=\"ft-sns\">\n        <a href=\"https://www.instagram.com/chibi_spo\" target=\"_blank\" rel=\"noopener\">Instagram</a><a href=\"https://www.threads.com/@chibi_spo\" target=\"_blank\" rel=\"noopener\">Threads</a>\n      </div>\n    </div>\n    <div class=\"ft-r\">\n      <div class=\"ft-app\">\n        <img src=\"assets/app-hero/app-icon-512.webp\" alt=\"チビスポ\">\n        <div class=\"tx\">アプリなら新着の<br>クラブ情報が早く届く！</div>\n        <a class=\"btn\" href=\"https://apps.apple.com/jp/app/id6797169414\" target=\"_blank\" rel=\"noopener\" data-app-store-cta>アプリを開く</a>\n      </div>\n      <div class=\"ft-links\">\n        <a href=\"about.html\">チビスポとは</a><a href=\"faq.html\">よくある質問</a><a href=\"legal.html#terms\">利用規約</a><a href=\"legal.html#privacy\">プライバシーポリシー</a><a href=\"contact.html\">お問い合わせ</a><a href=\"partner.html\">クラブ・事業者の方へ</a>\n      </div>\n    </div>\n  </div>\n  <div class=\"wrap ft-note\">© 2026 Chibispo All Rights Reserved.</div>\n</footer>";

  /* =======================================================================
     チビスポ Phase1：地域パーソナライズ ＋ お気に入り（localStorage・無料）
     - バックエンド不要。端末ローカルに保存。
     - 将来アカウント化（Supabase等）する際は、ここのデータを移行すればよい。
     ======================================================================= */
  var Chibi = (function () {
    var R_KEY = 'chibi_region', F_KEY = 'chibi_favs';
    var REGIONS = ['名古屋市', '豊田市', '岡崎市', '一宮市', '春日井市', '刈谷市', '安城市', '豊橋市'];
    function readJSON(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
    function writeJSON(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
    return {
      REGIONS: REGIONS,
      getRegion: function () { try { return localStorage.getItem(R_KEY) || ''; } catch (e) { return ''; } },
      setRegion: function (v) {
        try { localStorage.setItem(R_KEY, v); } catch (e) {}
        document.dispatchEvent(new CustomEvent('chibi:region', { detail: v }));
      },
      // 都道府県・市区町村を分けて保存（検索/地図のプリフィル用）
      getRegionPref: function () { try { return localStorage.getItem('chibi_region_pref') || ''; } catch (e) { return ''; } },
      getRegionCity: function () { try { return localStorage.getItem('chibi_region_city') || ''; } catch (e) { return ''; } },
      setRegionParts: function (pref, city) {
        try { localStorage.setItem('chibi_region_pref', pref || ''); localStorage.setItem('chibi_region_city', city || ''); } catch (e) {}
        var disp = city || pref || '';
        try { localStorage.setItem(R_KEY, disp); } catch (e) {}
        document.dispatchEvent(new CustomEvent('chibi:region', { detail: disp }));
      },
      getFavs: function () { return readJSON(F_KEY) || []; },
      isFav: function (id) { return this.getFavs().some(function (f) { return f.id === id; }); },
      toggleFav: function (obj) {
        var a = this.getFavs();
        var i = -1, n;
        for (n = 0; n < a.length; n++) { if (a[n].id === obj.id) { i = n; break; } }
        if (i >= 0) { a.splice(i, 1); } else { a.unshift(obj); }
        writeJSON(F_KEY, a);
        document.dispatchEvent(new CustomEvent('chibi:favs', { detail: { id: obj.id, added: i < 0 } }));
        return i < 0;
      },
      removeFav: function (id) {
        var a = this.getFavs().filter(function (f) { return f.id !== id; });
        writeJSON(F_KEY, a);
        document.dispatchEvent(new CustomEvent('chibi:favs', { detail: { id: id, added: false } }));
      }
    };
  })();
  window.Chibi = Chibi;

  /* =======================================================================
     ChibiAuth：認証の共通ヘルパー（一般ユーザー/クラブ共通）
     - 使うページは shared.js より前に supabase-lite.js を読み込むこと
     - profiles テーブル（role: parent/club）と連携。SQLは db-profiles.sql
     ======================================================================= */
  var ChibiAuth = (function () {
    var SB_URL = 'https://emkpkomrgknzrmxqbrvx.supabase.co';
    var SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ';
    var _db = null, _profileCache = null;
    function db() { if (_db) return _db; if (!window.supabase) return null; _db = window.supabase.createClient(SB_URL, SB_KEY); return _db; }
    return {
      ready: function () { return !!db(); },
      client: db,
      // 一般ユーザー/クラブ サインアップ（role と表示名・地域を metadata に載せる）
      signUp: function (email, password, opts) {
        opts = opts || {}; var d = db(); if (!d) return Promise.reject(new Error('Supabase未読込'));
        var full = opts.full_name || [opts.last_name, opts.first_name].filter(Boolean).join(' ');
        return d.auth.signUp({ email: email, password: password, options: { data: {
          role: opts.role || 'parent',
          last_name: opts.last_name || '',
          first_name: opts.first_name || '',
          full_name: full,
          display_name: opts.display_name || '',
          pref: opts.pref || '',
          city: opts.city || '',
          region: [opts.pref, opts.city].filter(Boolean).join(' ') || opts.region || ''
        } } });
      },
      signIn: function (email, password) { var d = db(); if (!d) return Promise.reject(new Error('Supabase未読込')); return d.auth.signInWithPassword({ email: email, password: password }); },
      signInWithGoogle: function (redirectTo) { var d = db(); if (!d) return Promise.reject(new Error('Supabase未読込')); return d.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: redirectTo || location.href } }); },
      resetPassword: function (email, redirectTo) { var d = db(); if (!d) return Promise.reject(new Error('Supabase未読込')); return d.auth.resetPasswordForEmail(email, { redirectTo: redirectTo }); },
      signOut: function () { _profileCache = null; var d = db(); if (!d) return Promise.resolve(); return d.auth.signOut(); },
      getUser: function () { var d = db(); if (!d) return Promise.resolve(null); return d.auth.getUser().then(function (r) { return (r.data && r.data.user) || null; }); },
      // ログインユーザーの profile（role 等）。未ログインは null
      getProfile: function () {
        var d = db(); if (!d) return Promise.resolve(null);
        return d.auth.getUser().then(function (r) {
          var u = r.data && r.data.user; if (!u) { _profileCache = null; return null; }
          return d.from('profiles').select('*').eq('id', u.id).single().then(function (p) {
            var prof = (p && p.data) || { id: u.id, role: (u.user_metadata && u.user_metadata.role) || 'parent' };
            prof.email = u.email;
            _profileCache = prof;
            return prof;
          }).catch(function () { return { id: u.id, email: u.email, role: (u.user_metadata && u.user_metadata.role) || 'parent' }; });
        });
      },
      onChange: function (cb) { var d = db(); if (!d) return; d.auth.onAuthStateChange(function (ev, sess) { _profileCache = null; cb(ev, sess); }); },
      // ログイン中のユーザーが掲載チームを持つ＝クラブ運営者か（roleに依存しない確実な判定）
      hasTeam: function () {
        var d = db(); if (!d) return Promise.resolve(false);
        return d.auth.getUser().then(function (r) {
          var u = r.data && r.data.user; if (!u) return false;
          return d.from('teams').select('id').eq('user_id', u.id)
            .then(function (res) { return !!(res.data && res.data.length); })
            .catch(function () { return false; });
        }).catch(function () { return false; });
      }
    };
  })();
  window.ChibiAuth = ChibiAuth;

  var FEATURE_CSS = `
    /* お気に入りハート（カードに自動付与） */
    /* 地域選択ポップアップ */
    #cc-region-pop{ position:fixed; inset:0; z-index:2000; display:flex; align-items:center; justify-content:center; padding:20px; background:rgba(15,21,30,.5); }
    #cc-region-pop .cc-rp-card{ background:#fff; border-radius:20px; max-width:420px; width:100%; padding:26px 24px 22px; box-shadow:0 20px 60px rgba(0,0,0,.3); }
    #cc-region-pop .cc-rp-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin:18px 0 6px; }
    #cc-region-pop .cc-rp-grid button{ font-family:inherit; font-size:14px; font-weight:700; color:#2b3340; background:#f4f6f8; border:1.5px solid #e6e9ed; border-radius:12px; padding:13px 0; cursor:pointer; transition:all .12s; }
    #cc-region-pop .cc-rp-grid button:hover{ border-color:#2a6fdb; color:#2a6fdb; background:#f2f7ff; }
  `;

  function fillRegionNames() {
    var r = Chibi.getRegion();
    document.querySelectorAll('.cc-region-name').forEach(function (el) {
      el.textContent = r || 'お近く';
    });
    document.querySelectorAll('[data-region-show]').forEach(function (el) {
      el.style.display = r ? '' : 'none';
    });
  }

  // cities.js（全国の都道府県→市区町村）を必要時に読み込む
  function ensureCities(cb) {
    if (typeof CITIES !== 'undefined') { cb(); return; }
    var s = document.createElement('script'); s.src = 'cities.js';
    s.onload = function () { cb(); }; s.onerror = function () { cb(); };
    document.head.appendChild(s);
  }
  function showRegionPopup(force) {
    if (!force && Chibi.getRegion()) return;
    if (document.getElementById('cc-region-pop')) return;
    ensureCities(function () { buildRegionPopup(); });
  }
  function buildRegionPopup() {
    var hasCities = (typeof CITIES !== 'undefined');
    var selStyle = 'width:100%;appearance:none;-webkit-appearance:none;border:1.5px solid #e6e9ed;border-radius:12px;padding:13px 14px;font-family:inherit;font-size:14px;font-weight:700;color:#2b3340;background:#f4f6f8;cursor:pointer;';
    var body;
    if (hasCities) {
      var prefOpts = '<option value="">都道府県を選択</option>' + Object.keys(CITIES).map(function (p) { return '<option value="' + p + '">' + p + '</option>'; }).join('');
      body = '<select id="cc-rp-pref" style="' + selStyle + '">' + prefOpts + '</select>' +
        '<select id="cc-rp-city" style="' + selStyle + 'margin-top:10px;" disabled><option value="">市区町村を選択</option></select>' +
        '<button id="cc-rp-save" style="width:100%;margin-top:14px;background:#2a6fdb;color:#fff;border:none;border-radius:12px;padding:14px 0;font-size:15px;font-weight:800;font-family:inherit;cursor:pointer;">この地域にする</button>';
    } else {
      body = '<div class="cc-rp-grid">' + Chibi.REGIONS.map(function (r) { return '<button data-r="' + r + '">' + r + '</button>'; }).join('') + '</div>';
    }
    var html = '<div id="cc-region-pop"><div class="cc-rp-card">' +
      '<div style="font-family:\'Zen Maru Gothic\',sans-serif;font-size:19px;font-weight:900;color:#1f2a37;">お住まいの地域を選んでください</div>' +
      '<div style="font-size:12.5px;color:#8a93a0;margin:6px 0 18px;line-height:1.7;">選んだ地域のおすすめクラブ・地域企業を優先して表示します。あとから変更できます。</div>' +
      body +
      '<button data-skip="1" style="display:block;width:100%;margin-top:10px;background:none;border:none;color:#9aa3ad;font-size:13px;font-weight:600;cursor:pointer;padding:8px;">あとで選ぶ</button>' +
      '</div></div>';
    document.body.insertAdjacentHTML('beforeend', html);
    var pop = document.getElementById('cc-region-pop');
    // 既存地域を初期選択
    if (hasCities) {
      var pf = document.getElementById('cc-rp-pref'), ct = document.getElementById('cc-rp-city');
      function fillCity() {
        if (!pf.value) { ct.innerHTML = '<option value="">市区町村を選択</option>'; ct.disabled = true; return; }
        ct.innerHTML = '<option value="">市区町村を選択（任意）</option>' + (CITIES[pf.value] || []).map(function (c) { return '<option value="' + c + '">' + c + '</option>'; }).join('');
        ct.disabled = false;
      }
      var curPref = Chibi.getRegionPref(), curCity = Chibi.getRegionCity();
      if (curPref) { pf.value = curPref; fillCity(); if (curCity) ct.value = curCity; }
      pf.addEventListener('change', fillCity);
      document.getElementById('cc-rp-save').addEventListener('click', function () {
        if (!pf.value) { pf.style.borderColor = '#e0344c'; return; }
        Chibi.setRegionParts(pf.value, ct.value);
        fillRegionNames(); pop.remove();
      });
    }
    pop.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) { if (e.target === pop) pop.remove(); return; }
      if (b.getAttribute('data-skip')) { pop.remove(); return; }
      if (b.getAttribute('data-r')) { Chibi.setRegionParts('', b.getAttribute('data-r')); fillRegionNames(); pop.remove(); }
    });
  }
  window.showRegionPopup = showRegionPopup;

  // カードの「♡＋数字（いいね）」を、お気に入りトグルにする（右上の角ハートは廃止）。
  // すべての .club-card で共通。地図の詳細パネル（cc-detail-fav）と同じ挙動。
  function decorateFavs() {
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
  // 非同期でカードが増えても自動でお気に入りを結線
  var _favObserver = null;
  function watchFavs() {
    if (_favObserver || !window.MutationObserver) return;
    var t;
    _favObserver = new MutationObserver(function () { clearTimeout(t); t = setTimeout(decorateFavs, 120); });
    _favObserver.observe(document.body, { childList: true, subtree: true });
  }
  // お気に入りが変わったら、表示中の全カードのハートを更新
  document.addEventListener('chibi:favs', function () {
    document.querySelectorAll('a.club-card, a.nc').forEach(function (c) { if (c.__favRender) c.__favRender(); });
  });

  // カード上の雰囲気タグ（.cc-mood-tag[data-mood]）をクリック → その雰囲気で検索
  function bindMoodTags() {
    document.querySelectorAll('.cc-mood-tag[data-mood], .nc-tags span[data-mood]').forEach(function (el) {
      if (el.__moodBound) return;
      el.__moodBound = true;
      el.style.cursor = 'pointer';
      el.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var m = el.getAttribute('data-mood');
        if (m) location.href = 'search.html?mood=' + encodeURIComponent(m);
      });
    });
  }

  function initFeatures() {
    var fstyle = document.createElement('style');
    fstyle.id = 'cc-feature-style';
    fstyle.textContent = FEATURE_CSS;
    document.head.appendChild(fstyle);
    fillRegionNames();
    decorateFavs();
    watchFavs();
    bindMoodTags();
    // 地域変更リンク（class="cc-region-change"）クリックでポップアップ再表示
    document.querySelectorAll('.cc-region-change').forEach(function (el) {
      el.addEventListener('click', function (e) { e.preventDefault(); showRegionPopup(true); });
    });
    // 初回訪問時の地域ポップアップは廃止（地域選択は条件検索の都道府県で行う）。
    // 地域変更は .cc-region-change（マイページ等）からのみ手動で開ける。
  }

  /* ---------- style-hover シム（注入したノード内のみ） ---------- */
  function bindHover(root) {
    if (!root) return;
    root.querySelectorAll('[style-hover]').forEach(function (el) {
      if (el.__ccHover) return;                  // 二重バインド防止
      el.__ccHover = true;
      var base = el.getAttribute('style') || '';
      var hover = el.getAttribute('style-hover') || '';
      var on = function () { el.setAttribute('style', base + ';' + hover); };
      var off = function () { el.setAttribute('style', base); };
      el.addEventListener('mouseenter', on);
      el.addEventListener('mouseleave', off);
      // キーボードで辿っている人にも同じ反応を返す
      el.addEventListener('focus', on);
      el.addEventListener('blur', off);
    });
  }

  /* ---------- ボトムシート（ハンバーガー） ---------- */
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
    if (/^\/clubs\//.test(location.pathname)) here = 'search.html';
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

  // supabase-lite.js が未読込なら動的に読み込む
  function ensureSupabase(cb) {
    if (window.supabase) { cb(); return; }
    var s = document.createElement('script');
    s.src = 'supabase-lite.js';
    s.onload = function () { cb(); };
    s.onerror = function () {};
    document.head.appendChild(s);
  }
  var AUTH_AV_COLORS = [['#eef4ff','#2563eb'],['#fef0f5','#e0447f'],['#effaf3','#1f8a5b'],['#fff6e8','#d97316'],['#f4effd','#7b5cd6'],['#eafafa','#0e8f97']];
  function applyAuthUI(prof) {
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
  function updateAuthUI() {
    if (!window.ChibiAuth) return;
    ensureSupabase(function () {
      if (!ChibiAuth.ready()) return;
      ChibiAuth.getProfile().then(function (prof) { applyAuthUI(prof); if (prof) syncLikes(prof.id); }).catch(function () {});
      // 同一ページでのログイン/ログアウトにも追従
      ChibiAuth.onChange(function () { ChibiAuth.getProfile().then(function (prof) { applyAuthUI(prof); if (prof) syncLikes(prof.id); }).catch(function () {}); });
    });
  }

  /* ---------- いいね（likes）のDB同期 ----------
     ログインユーザーの♡はDBにも記録し、カードの♡数に実数が出る。
     未ログインの♡は端末内のお気に入りのみ（数にはカウントされない）。 */
  function syncLikes(uid) {
    if (!window.ChibiAuth || !ChibiAuth.ready()) return;
    var db = ChibiAuth.client(); if (!db) return;
    // 端末に保存済みのお気に入りを一度だけDBへ反映（重複はunique制約で無視）
    var key = 'chibi_likes_synced_' + uid;
    try {
      if (!localStorage.getItem(key)) {
        (window.Chibi ? Chibi.getFavs() : []).forEach(function (f) {
          if (f && f.id) db.from('likes').insert({ team_id: f.id, user_id: uid }).then(function(){}).catch(function(){});
        });
        localStorage.setItem(key, '1');
      }
    } catch (e) {}
  }
  document.addEventListener('chibi:favs', function (e) {
    if (!e.detail || !e.detail.id || !window.ChibiAuth || !ChibiAuth.ready()) return;
    ChibiAuth.getUser().then(function (u) {
      if (!u) return; // 未ログインはローカルのみ
      var db = ChibiAuth.client();
      if (e.detail.added) db.from('likes').insert({ team_id: e.detail.id, user_id: u.id }).then(function(){}).catch(function(){});
      else db.from('likes').delete().eq('team_id', e.detail.id); // RLSで自分の行のみ削除される
    }).catch(function () {});
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
