/* ============================================================
 * feature-track.js — チビスポ特集・マガジン用の自動計測スクリプト
 *
 *  特集/マガジン記事の中で、クラブ詳細ページへのリンクを普通に貼るだけで、
 *  自動で計測リンク（/go/<clubId>/chibispo-feature）に書き換える。
 *  → クラブ側の作業ゼロで「特集経由の流入」が計測される。
 *
 *  使い方：特集ページの</body>直前に
 *    <script src="feature-track.js"></script>
 *  を入れるだけ。記事内のクラブへのリンクは
 *    <a href="club.html?id=<UUID>">…</a>   （通常どおり）
 *  と書けば、読み込み時に計測リンクへ自動変換される。
 * ============================================================ */
(function () {
  var TRACK = "https://chibispo-tracking.hyogo120.workers.dev";
  var SLUG = "chibispo-feature"; // ダッシュボードで「チビスポ特集・マガジン」として認識される予約スラッグ
  function rewrite() {
    var links = document.querySelectorAll('a[href*="club.html?id="], a[href*="club.html?id="i]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (a.getAttribute("data-no-track") != null) continue; // 計測したくないリンクは data-no-track を付ける
      var href = a.getAttribute("href") || "";
      var m = href.match(/club\.html\?id=([0-9A-Za-z-]+)/i);
      if (!m) continue;
      a.setAttribute("href", TRACK + "/go/" + encodeURIComponent(m[1]) + "/" + SLUG);
      a.setAttribute("data-tracked", "1");
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", rewrite);
  else rewrite();
})();
