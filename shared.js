/* =========================================================================
   チビスポ 共通ヘッダー / フッター コンポーネント
   - 全ページ共通。このファイル1つを直せば全ページのヘッダー・フッターが変わる。
   - 各ページは <script src="shared.js"></script> を </body> 直前に置くだけ。
   - ヘッダー / ボトムシートメニュー / 下部タブバー / フッター を body に注入する。
   ========================================================================= */
(function () {
  'use strict';

  /* ---------- 共通CSS（ヘッダー・メニュー・下部バー・フッターのレスポンシブ） ---------- */
  var CSS = `
    /* ログイン状態でヘッダーの導線を出し分け */
    .cc-hidden{ display:none !important; }
    /* ページ内アンカー移動をゆっくりスクロールに（全ページ共通） */
    html{ scroll-behavior:smooth; }
    /* ボトムシート開閉（クラス方式） */
    #cc-menu{ box-sizing:border-box; }
    #cc-menu.cc-open{ transform:translateY(0) !important; transition:transform .33s cubic-bezier(.32,.72,0,1) !important; }
    #cc-backdrop.cc-open{ display:block !important; }
    #cc-menu a[style*="flex-direction:column"]{ box-sizing:border-box; min-width:0; }
    #cc-menu a[style*="flex-direction:column"] svg{ flex:0 0 auto; }
    #cc-menu a[style*="flex-direction:column"] span{ overflow-wrap:anywhere; max-width:100%; }
    /* デスクトップ（1001px以上）はモバイル専用UIを無効化 */
    @media (min-width: 1001px){
      #cc-menu, #cc-backdrop { display:none !important; }
      .cc-burger { display:none !important; }
    }
    /* ヘッダー：ナビ文字・アクションラベルは途中で折り返さない */
    .cc-nav a { white-space:nowrap; }
    .cc-actions { flex-shrink:0; }
    .cc-actions .cc-icontop { flex-shrink:0; }
    .cc-actions .cc-icontop span { white-space:nowrap; }
    /* ヘッダー：中間幅は文字・アイコン・余白を縮小して全項目を表示 */
    @media (max-width: 1360px){
      header[data-screen-label="ヘッダー"] .cc-head-inner { gap:12px !important; padding-left:16px !important; padding-right:16px !important; }
      .cc-nav { gap:14px !important; }
      .cc-nav a { font-size:12.5px !important; white-space:nowrap !important; }
      .cc-nav a svg { width:16px !important; height:16px !important; }
      .cc-divider { margin:0 2px !important; }
      .cc-actions { gap:12px !important; }
      .cc-actions .cc-icontop span { font-size:10px !important; }
      .cc-actions .cc-icontop svg { width:20px !important; height:20px !important; }
      .cc-publish { padding:9px 15px !important; font-size:12.5px !important; }
    }
    /* モバイル：ヘッダーはロゴのみ、操作は下部タブバー＋ボトムシートに集約 */
    @media (max-width: 1000px){
      .cc-nav { display:none !important; }
      .cc-divider { display:none !important; }
      .cc-actions { display:none !important; }
      .cc-burger { display:none !important; }
      .cc-bottombar { display:flex !important; }
      body { padding-bottom:64px; }
      #cc-menu { bottom:64px !important; }
      header[data-screen-label="ヘッダー"] .cc-head-inner { padding:0 16px !important; gap:10px !important; }
      /* ロゴを小さめにしてサブタイトルが下に回り込まないようにする */
      .cc-logo-img { height:34px !important; }
      .cc-head-inner a[href="index.html"] span { white-space:nowrap !important; }
    }
    /* スマホ狭幅：タイルと下部バーの詰めすぎ・はみ出しを調整 */
    @media (max-width: 480px){
      .cc-logo-img { height:30px !important; }
      .cc-head-inner a[href="index.html"] span { font-size:9.5px !important; }
      #cc-menu { padding-left:12px !important; padding-right:12px !important; }
      #cc-menu > div[style*="grid-template-columns"]{ gap:8px !important; }
      #cc-menu a[style*="flex-direction:column"]{ padding:12px 2px !important; }
      #cc-menu a[style*="flex-direction:column"] span{ font-size:10px !important; line-height:1.25 !important; }
      .cc-bottombar > *{ flex:1 1 0; min-width:0; padding:0 2px; }
      .cc-bottombar span{ font-size:9.5px !important; white-space:nowrap; }
      .cc-publish { padding:9px 15px !important; font-size:12.5px !important; }
    }
    /* フッター：中間幅以下はリンクを2列に */
    @media (max-width: 820px){
      footer[data-screen-label="フッター"] [style*="grid-template-columns: repeat(4, 1fr)"] { grid-template-columns:repeat(2,1fr) !important; }
    }
    @media (max-width: 560px){
      footer[data-screen-label="フッター"] > div { gap:28px !important; }
      footer[data-screen-label="フッター"] [style*="flex: 1 1 520px"]{ flex:1 1 100% !important; }
    }
  `;

  /* ---------- ヘッダー ---------- */
  var HEADER = `
  <header data-screen-label="ヘッダー" style="position: sticky; top: 0; z-index: 1000; background: rgba(255,255,255,0.92); backdrop-filter: saturate(180%) blur(12px); -webkit-backdrop-filter: saturate(180%) blur(12px); border-bottom: 1px solid #eeeeee;">
    <div class="cc-head-inner" style="max-width: 1320px; margin: 0 auto; padding: 0 24px; height: 74px; display: flex; align-items: center; gap: 22px;">

      <a href="index.html" style="display: flex; flex-direction: column; align-items: flex-start; gap: 3px; text-decoration: none; flex: 0 0 auto; line-height: 1;">
        <img class="cc-logo-img" src="assets/logo.png" alt="チビスポ" style="height: 36px; width: auto; display: block;">
        <span style="font-size: 10px; font-weight: 700; color: #9aa3ae; letter-spacing: 0.02em; white-space: nowrap;">地域スポーツを、もっと身近に。</span>
      </a>

      <nav class="cc-nav" style="display: flex; align-items: center; gap: 24px; margin-left: auto;">
        <a href="search.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:700; color:#2b2b2b; text-decoration:none;" style-hover="color:#2a6fdb;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2a6fdb" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.2-3.2"/></svg>クラブを探す
        </a>
        <a href="map.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:700; color:#2b2b2b; text-decoration:none;" style-hover="color:#e8455f;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#e8455f" stroke-width="1.9"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>地図から探す
        </a>
        <a href="magazine.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:700; color:#2b2b2b; text-decoration:none;" style-hover="color:#1f8a5b;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1f8a5b" stroke-width="1.9"><path d="M3 5h7v15H5a2 2 0 0 1-2-2z"/><path d="M21 5h-7v15h5a2 2 0 0 0 2-2z"/></svg>マガジン
        </a>
        <a href="about.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:700; color:#2b2b2b; text-decoration:none;" style-hover="color:#e8784a;">
          <svg width="18" height="18" viewBox="0 0 24 24"><path d="M12 4 L21 20 L12 20 Z" fill="#7cb342"/><path d="M12 4 L3 20 L12 20 Z" fill="#f5c518"/></svg>チビスポとは
        </a>
        <a href="partner.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:700; color:#2b2b2b; text-decoration:none;" style-hover="color:#2a6fdb;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2a6fdb" stroke-width="1.9"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h6"/></svg>掲載・広告
        </a>
      </nav>

      <span class="cc-divider" style="width:1px; height:28px; background:#e2e5ea; flex:0 0 auto; margin:0 6px;"></span>

      <div class="cc-actions" style="display:flex; align-items:center; gap:20px;">
        <a class="cc-icontop" href="mypage.html" style="display:flex; flex-direction:column; align-items:center; gap:3px; text-decoration:none; color:#54606e;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e8455f" stroke-width="1.8"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>
          <span style="font-size:10.5px; font-weight:700;">お気に入り</span>
        </a>
        <a class="cc-icontop cc-auth-out" href="club-mypage.html" style="display:flex; flex-direction:column; align-items:center; gap:3px; text-decoration:none; color:#54606e;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2a6fdb" stroke-width="1.8"><path d="M3 21h18M6 21V8l6-4 6 4v13M10 21v-5h4v5"/></svg>
          <span style="font-size:10.5px; font-weight:700;">クラブログイン</span>
        </a>
        <a class="cc-icontop cc-auth-out" href="login.html" style="display:flex; flex-direction:column; align-items:center; gap:3px; text-decoration:none; color:#54606e;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#b04ae8" stroke-width="1.8"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/></svg>
          <span style="font-size:10.5px; font-weight:700;">一般ログイン</span>
        </a>
        <a class="cc-icontop cc-auth-in cc-hidden" href="mypage.html" style="display:flex; flex-direction:column; align-items:center; gap:3px; text-decoration:none; color:#54606e;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1f8a5b" stroke-width="1.8"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/></svg>
          <span style="font-size:10.5px; font-weight:700;">マイページ</span>
        </a>
        <a class="cc-publish" href="listing.html" style="display:inline-flex; align-items:center; gap:7px; font-size:14px; font-weight:900; color:#ffffff; text-decoration:none; background:#e8455f; border-radius:999px; padding:11px 22px; box-shadow:0 6px 16px rgba(232,69,95,0.28);" style-hover="background:#d23b53;">クラブを掲載する</a>
      </div>

      <button class="cc-burger" aria-label="メニュー" style="flex:0 0 auto; width:44px; height:44px; border-radius:50%; border:1.5px solid #e2e5ea; background:#fff; cursor:pointer; color:#2b2b2b; display:flex; align-items:center; justify-content:center;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>

    </div>
  </header>`;

  /* ---------- 背景幕 + ボトムシートメニュー ---------- */
  var MENU = `
    <div id="cc-backdrop" style="display:none; position:fixed; inset:0; background:rgba(15,21,30,.4); z-index:1290;"></div>

    <div class="cc-menu" id="cc-menu" style="position:fixed; left:0; right:0; bottom:0; margin:0 auto; width:100%; max-width:560px; background:#ffffff; border-radius:22px 22px 0 0; box-shadow:0 -10px 40px rgba(0,0,0,.18); padding:12px 18px 26px; z-index:1300; max-height:88vh; overflow-y:auto; transform:translateY(120%); transition:transform .55s cubic-bezier(.32,.72,0,1); will-change:transform;">
      <div style="width:44px; height:5px; border-radius:3px; background:#dfe3e8; margin:2px auto 16px;"></div>

      <div style="display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:11px;">
        <a href="search.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2a6fdb" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.2-3.2"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">クラブを探す</span>
        </a>
        <a href="map.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#e8455f" stroke-width="1.9"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">地図から探す</span>
        </a>
        <a href="magazine.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1f8a5b" stroke-width="1.9"><path d="M4 5h7v15H6a2 2 0 0 1-2-2z"/><path d="M20 5h-7v15h5a2 2 0 0 0 2-2z"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">マガジン</span>
        </a>
        <a href="about.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24"><path d="M12 4 L21 20 L12 20 Z" fill="#7cb342"/><path d="M12 4 L3 20 L12 20 Z" fill="#f5c518"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">チビスポとは</span>
        </a>
        <a href="mypage.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#e8455f" stroke-width="1.8"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">お気に入り</span>
        </a>
        <a href="faq.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#b04ae8" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M9.2 9a2.8 2.8 0 1 1 3.9 2.6c-.8.35-1.1.9-1.1 1.9"/><circle cx="12" cy="16.6" r=".6" fill="#b04ae8"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">よくある質問</span>
        </a>
        <a href="search.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1f8a5b" stroke-width="1.8"><path d="M12 21s-7-5.5-7-11a7 7 0 1 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.4"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">地域から探す</span>
        </a>
        <a href="search.html#sr-sport" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#e8784a" stroke-width="1.8"><circle cx="14" cy="5" r="2"/><path d="M13 8l-4 3 3 3 1 5M9 11l-4 1M12 14l4 1"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">種目（スポーツ）から探す</span>
        </a>
        <a href="search.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2a6fdb" stroke-width="1.8"><path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2.2"/><circle cx="9" cy="17" r="2.2"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">条件から探す</span>
        </a>
        <a href="partner.html" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px 4px; border:1px solid #eef0f2; border-radius:14px; text-decoration:none; color:#3a4452;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#b04ae8" stroke-width="1.8"><path d="M5 21V5l7-2 7 2v16"/><path d="M9 9h2M9 13h2M14 9h1M14 13h1"/></svg>
          <span style="font-size:11px; font-weight:700; text-align:center; line-height:1.3;">掲載をお考えの方へ</span>
        </a>
      </div>

      <a href="listing.html" style="display:block; text-align:center; background:#e8455f; color:#fff; font-size:15px; font-weight:800; border-radius:999px; padding:15px 0; margin-top:20px; text-decoration:none; box-shadow:0 6px 16px rgba(232,69,95,0.26);">チーム・クラブを掲載する</a>
      <a href="login.html" class="cc-auth-out" style="display:block; text-align:center; border:1.5px solid #e8455f; color:#e8455f; font-size:15px; font-weight:800; border-radius:999px; padding:14px 0; margin-top:11px; text-decoration:none;">一般（保護者）ログイン / 会員登録</a>
      <a href="club-mypage.html" class="cc-auth-out" style="display:block; text-align:center; border:1.5px solid #2a6fdb; color:#2a6fdb; font-size:14px; font-weight:800; border-radius:999px; padding:13px 0; margin-top:9px; text-decoration:none;">クラブ運営者ログイン（掲載・管理）</a>
      <a href="mypage.html" class="cc-auth-in cc-hidden" style="display:block; text-align:center; background:#2270e0; color:#fff; font-size:15px; font-weight:800; border-radius:999px; padding:14px 0; margin-top:11px; text-decoration:none;">マイページ</a>
    </div>`;

  /* ---------- 下部タブバー（モバイル） ---------- */
  var BOTTOMBAR = `
  <nav class="cc-bottombar" style="display:none; position:fixed; left:0; right:0; bottom:0; height:64px; background:#ffffff; border-top:1px solid #eef0f2; box-shadow:0 -2px 12px rgba(0,0,0,.06); z-index:1310; align-items:center; justify-content:space-around;">
    <a href="search.html" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:3px; color:#54606e;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M5 21V4"/><path d="M5 4h12l-2.5 4 2.5 4H5"/></svg>
      <span style="font-size:10px; font-weight:600;">クラブを探す</span>
    </a>
    <a href="search.html" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:3px; color:#54606e;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2.2"/><circle cx="9" cy="17" r="2.2"/></svg>
      <span style="font-size:10px; font-weight:600;">条件から探す</span>
    </a>
    <a href="login.html" class="cc-auth-out" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:3px; color:#54606e;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/></svg>
      <span style="font-size:10px; font-weight:600;">一般ログイン</span>
    </a>
    <a href="mypage.html" class="cc-auth-in cc-hidden" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:3px; color:#54606e;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/></svg>
      <span style="font-size:10px; font-weight:600;">マイページ</span>
    </a>
    <a href="mypage.html" style="text-decoration:none; display:flex; flex-direction:column; align-items:center; gap:3px; color:#54606e;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>
      <span style="font-size:10px; font-weight:600;">お気に入り</span>
    </a>
    <button class="cc-open-menu" aria-label="メニュー" style="background:none; border:none; cursor:pointer; display:flex; flex-direction:column; align-items:center; gap:3px; color:#e8455f;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      <span style="font-size:10px; font-weight:700;">メニュー</span>
    </button>
  </nav>`;

  /* ---------- フッター ---------- */
  var FOOTER = `
  <footer data-screen-label="フッター" style="background: #f4f4f2; padding: 52px 32px 32px;">
    <div style="max-width: 1120px; margin: 0 auto; display: flex; gap: 48px; flex-wrap: wrap; align-items: flex-start;">
      <div style="flex: 0 0 220px; display: flex; flex-direction: column; align-items: flex-start; gap: 10px;">
        <a href="index.html" style="align-self: flex-start; text-decoration: none; display: block;"><img src="assets/logo.png" alt="チビスポ" style="height: 36px; width: auto; display: block;"></a>
        <div style="font-size: 11px; font-weight: 700; color: #777777;">地域スポーツを、もっと身近に。</div>
      </div>

      <div style="flex: 1 1 520px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="font-size: 13px; font-weight: 900; color: #2b2b2b;">クラブを探す</div>
          <a href="search.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">エリアから探す</a>
          <a href="search.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">種目から探す</a>
          <a href="search.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">雰囲気から探す</a>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="font-size: 13px; font-weight: 900; color: #2b2b2b;">マガジン</div>
          <a href="magazine.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">クラブのらしさ</a>
          <a href="magazine.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">コーチの想い</a>
          <a href="magazine.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">子どもの一歩</a>
          <a href="magazine.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">はじめてのスポーツ選び</a>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="font-size: 13px; font-weight: 900; color: #2b2b2b;">サポート</div>
          <a href="faq.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">よくある質問</a>
          <a href="contact.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">お問い合わせ</a>
          <a href="legal.html#terms" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">利用規約</a>
          <a href="legal.html#privacy" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">プライバシーポリシー</a>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="font-size: 13px; font-weight: 900; color: #2b2b2b;">運営について</div>
          <a href="about.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">チビスポとは</a>
          <a href="partner.html" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">掲載・広告のご案内</a>
          <a href="listing.html#service" style="font-size: 12px; color: #777777; text-decoration: none; font-weight: 500;">ホームページ・SNS制作代行</a>
        </div>
      </div>

      <!-- SNSアイコン：チビスポ公式（Threads / Instagram） -->
      <div style="flex: 0 0 auto; display: flex; gap: 12px; align-items: center;">
        <a href="https://www.instagram.com/chibi_spo" target="_blank" rel="noopener" aria-label="チビスポ公式Instagram" style="width: 40px; height: 40px; border-radius: 50%; background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%); display: inline-flex; align-items: center; justify-content: center; text-decoration: none;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="#ffffff" stroke="none"/></svg>
        </a>
        <a href="https://www.threads.com/@chibi_spo" target="_blank" rel="noopener" aria-label="チビスポ公式Threads" style="width: 40px; height: 40px; border-radius: 50%; background: #000000; display: inline-flex; align-items: center; justify-content: center; text-decoration: none;">
          <svg width="20" height="20" viewBox="0 0 192 192" fill="#ffffff"><path d="M141.537 88.988c-.827-.396-1.667-.777-2.518-1.143-1.482-27.307-16.403-42.94-41.457-43.1h-.34c-14.986 0-27.449 6.397-35.12 18.036l13.779 9.452c5.73-8.694 14.724-10.548 21.348-10.548h.229c8.249.053 14.474 2.451 18.503 7.129 2.932 3.405 4.893 8.111 5.864 14.05-7.314-1.243-15.224-1.626-23.68-1.141-23.82 1.372-39.134 15.265-38.105 34.569.522 9.792 5.4 18.216 13.735 23.719 7.048 4.652 16.124 6.927 25.557 6.412 12.458-.683 22.231-5.436 29.049-14.127 5.178-6.6 8.453-15.153 9.899-25.93 5.937 3.583 10.337 8.298 12.767 13.966 4.132 9.635 4.373 25.468-8.546 38.376-11.319 11.308-24.925 16.2-45.488 16.351-22.809-.169-40.06-7.484-51.275-21.742C35.236 139.966 29.808 120.682 29.605 96c.203-24.682 5.631-43.966 16.133-57.317C56.954 24.425 74.204 17.11 97.013 16.94c22.975.171 40.526 7.521 52.171 21.848 5.71 7.026 10.015 15.861 12.853 26.162l16.147-4.308c-3.44-12.68-8.853-23.606-16.219-32.668C147.036 9.607 125.202.195 97.07 0h-.113C68.882.194 47.292 9.642 32.788 28.079 19.882 44.486 13.224 67.316 13.001 95.932L13 96l.001.068c.223 28.616 6.881 51.446 19.787 67.853 14.504 18.437 36.094 27.885 64.169 28.079h.113c24.96-.173 42.554-6.708 57.048-21.189 18.963-18.945 18.392-42.695 12.142-57.27-4.484-10.454-13.033-18.945-24.723-24.553zm-43.096 40.519c-10.44.588-21.286-4.098-21.821-14.135-.397-7.442 5.296-15.746 22.461-16.735 1.966-.114 3.895-.169 5.79-.169 6.235 0 12.068.606 17.371 1.765-1.978 24.702-13.58 28.713-23.801 29.274z"/></svg>
        </a>
      </div>
    </div>
    <div style="text-align: center; font-size: 11px; color: #999999; margin-top: 40px; font-weight: 500;">© 2026 Chibispo All Rights Reserved.</div>
  </footer>`;

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
    document.querySelectorAll('a.club-card').forEach(function (card) {
      if (card.__favBound) return;
      var h = card.querySelector('h3');
      var name = h ? h.textContent.trim() : '';
      if (!name) return;

      // いいねハート svg（ハートpath "M12 20.3..." を持つもの）を探す
      var heartSvg = null, svgs = card.querySelectorAll('svg');
      for (var i = 0; i < svgs.length; i++) {
        var p = svgs[i].querySelector('path');
        if (p && (p.getAttribute('d') || '').indexOf('M12 20.3') === 0) { heartSvg = svgs[i]; break; }
      }
      if (!heartSvg) return; // ♡＋数字が無いカードは対象外
      var likeEl = heartSvg.parentElement; // <span><svg/>342</span>

      var img = card.querySelector('img');
      var area = '';
      card.querySelectorAll('span').forEach(function (el) {
        if (!area && el.children.length === 0) {
          var t = el.textContent.trim();
          if (/[都道府県市区町村]/.test(t) && t.length <= 30) area = t;
        }
      });
      // お気に入りIDはクラブのUUID（href ?id=）で統一。無ければ名前ベース
      var hrefVal = card.getAttribute('href') || '';
      var idMatch = /[?&]id=([^&]+)/.exec(hrefVal);
      var id = idMatch ? decodeURIComponent(idMatch[1]) : ('club-' + encodeURIComponent(name));

      function render() {
        var fav = Chibi.isFav(id);
        if (fav) { heartSvg.setAttribute('fill', '#ff5fa2'); heartSvg.removeAttribute('stroke'); }
        else { heartSvg.setAttribute('fill', 'none'); heartSvg.setAttribute('stroke', '#9aa3ad'); heartSvg.setAttribute('stroke-width', '1.9'); }
        // 数字はDBのいいね実数（search/map側で描画）。フィードバックはハートの色で行う
      }

      likeEl.style.cursor = 'pointer';
      likeEl.setAttribute('title', 'お気に入り');
      likeEl.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        Chibi.toggleFav({
          id: id, name: name, area: area,
          href: card.getAttribute('href') || '#',
          img: img ? img.getAttribute('src') : ''
        });
        render();
      });
      card.__favBound = true;
      card.__favRender = render; // お気に入り変更時に他カードも同期できるよう保持
      render();
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
    document.querySelectorAll('a.club-card').forEach(function (c) { if (c.__favRender) c.__favRender(); });
  });

  // カード上の雰囲気タグ（.cc-mood-tag[data-mood]）をクリック → その雰囲気で検索
  function bindMoodTags() {
    document.querySelectorAll('.cc-mood-tag[data-mood]').forEach(function (el) {
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
    root.querySelectorAll('[style-hover]').forEach(function (el) {
      var base = el.getAttribute('style') || '';
      var hover = el.getAttribute('style-hover') || '';
      el.addEventListener('mouseenter', function () { el.setAttribute('style', base + ';' + hover); });
      el.addEventListener('mouseleave', function () { el.setAttribute('style', base); });
    });
  }

  function init() {
    // CSS注入
    var style = document.createElement('style');
    style.id = 'cc-shared-style';
    style.textContent = CSS;
    document.head.appendChild(style);

    // ヘッダー・メニュー・下部バーを body 先頭へ（順序維持のため逆順で afterbegin 挿入）
    document.body.insertAdjacentHTML('afterbegin', BOTTOMBAR);
    document.body.insertAdjacentHTML('afterbegin', MENU);
    document.body.insertAdjacentHTML('afterbegin', HEADER);
    // フッターを body 末尾へ
    document.body.insertAdjacentHTML('beforeend', FOOTER);

    // ホバー再現（ヘッダー・フッター内のみ）
    bindHover(document.querySelector('header[data-screen-label="ヘッダー"]'));
    bindHover(document.querySelector('footer[data-screen-label="フッター"]'));

    // ボトムシート開閉
    var menu = document.getElementById('cc-menu');
    var backdrop = document.getElementById('cc-backdrop');
    var isOpen = false;
    function setOpen(v) {
      isOpen = v;
      if (menu) menu.classList.toggle('cc-open', v);
      if (backdrop) backdrop.classList.toggle('cc-open', v);
    }
    document.querySelectorAll('.cc-burger, .cc-open-menu').forEach(function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); setOpen(!isOpen); });
    });
    if (backdrop) backdrop.addEventListener('click', function () { setOpen(false); });
    if (menu) menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });

    // Phase1 機能（地域・お気に入り）
    initFeatures();

    // ログイン状態でヘッダーの「ログイン」導線を「マイページ」に切替
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
    // アバター（ニックネーム頭文字＋名前から安定した色）
    var name = loggedIn ? (prof.display_name || (prof.email ? prof.email.split('@')[0] : 'M')) : '';
    var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
    var col = AUTH_AV_COLORS[h % AUTH_AV_COLORS.length];
    var ini = (name.charAt(0) || 'M').toUpperCase().replace(/[<>&"]/g, '');
    // ログアウト時の導線（一般ログイン・クラブログイン）
    document.querySelectorAll('.cc-auth-out').forEach(function (el) { el.classList.toggle('cc-hidden', loggedIn); });
    // ログイン時の導線：アバターアイコンに差し替え（role で行き先を振り分け）
    document.querySelectorAll('.cc-auth-in').forEach(function (el) {
      el.classList.toggle('cc-hidden', !loggedIn);
      el.setAttribute('href', target);
      if (!loggedIn) return;
      el.setAttribute('title', 'マイページ');
      if (el.classList.contains('cc-icontop')) {
        // PCヘッダー：アバターアイコンのみ
        el.innerHTML = '<span style="width:36px;height:36px;border-radius:50%;background:' + col[0] + ';color:' + col[1] + ';display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:900;box-shadow:inset 0 0 0 1.5px ' + col[1] + '22;">' + ini + '</span>';
      } else if (el.closest('.cc-bottombar')) {
        // モバイル下部バー：アバター＋小ラベル
        el.innerHTML = '<span style="width:25px;height:25px;border-radius:50%;background:' + col[0] + ';color:' + col[1] + ';display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;">' + ini + '</span><span style="font-size:10px;font-weight:600;">マイページ</span>';
      }
    });
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
