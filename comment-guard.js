/* 投稿前の内容チェック。
   App Store の審査（ガイドライン1.2）は、ユーザー投稿があるアプリに
   「不適切な内容をフィルタする仕組み」を求める。通報とブロックだけでは足りない。

   ここでやるのは投稿を止めることだけで、判定はゆるくしてある。
   誤って止めると投稿できなくなるので、明らかなものだけを対象にする。
   最終的な判断は管理画面（admin.html の通報セクション）で人がやる。

   ★アプリ側にも同じ内容が chibispo-app/src/lib/commentGuard.ts にある。
     直すときは両方そろえること（リポジトリが別なので共有できない）。 */
(function (root) {
  'use strict';

  // 明らかな中傷・卑語。部分一致で見るので、短すぎる語は入れない
  var NG_WORDS = [
    '死ね', 'しね', '殺す', 'ころす', 'クズ', 'ゴミ人間', 'カス野郎',
    'バカ野郎', 'ブス', 'キモい', 'きもい', 'うざい', 'ウザい',
    '詐欺', 'ぼったくり', '訴える', '晒す', 'さらす',
  ];

  // 個人情報・宣伝とみなすもの
  var PATTERNS = [
    { re: /\d{2,4}[-ー−]\d{2,4}[-ー−]\d{3,4}/, why: '電話番号らしき数字' },
    { re: /[\w.+-]+@[\w-]+\.[\w.-]+/, why: 'メールアドレス' },
    { re: /https?:\/\/[^\s]+/i, why: 'URL' },
    { re: /(LINE|ライン)\s*(ID|アイディー)/i, why: 'LINE ID' },
  ];

  /* 戻り値：問題なければ null、あれば理由の文字列 */
  function checkComment(text) {
    var body = String(text == null ? '' : text);
    var hit = NG_WORDS.filter(function (w) { return body.indexOf(w) >= 0; });
    if (hit.length) {
      return '相手を傷つける言葉が含まれています。表現を変えてください。';
    }
    for (var i = 0; i < PATTERNS.length; i++) {
      if (PATTERNS[i].re.test(body)) {
        return PATTERNS[i].why + 'は投稿できません。連絡先のやり取りは体験申込みからお願いします。';
      }
    }
    // 同じ文字の極端な連続（荒らし対策）
    if (/(.)\1{14,}/.test(body)) return '同じ文字が続きすぎています。';
    return null;
  }

  root.ChibiCommentGuard = { check: checkComment, NG_WORDS: NG_WORDS };
})(typeof window !== 'undefined' ? window : globalThis);
