/* デザイン選択ページ：カードごとに3色を選ぶ。サムネがフェードで入れ替わり、見本リンクが ?theme= 付きになる */
(function () {
  'use strict';
  Array.prototype.forEach.call(document.querySelectorAll('.type[data-base]'), function (card) {
    var base = card.getAttribute('data-base');
    var img = card.querySelector('.type__shot img');
    var link = card.querySelector('.type__link');
    var cname = card.querySelector('.type__link-c');
    var btns = Array.prototype.slice.call(card.querySelectorAll('.swb'));
    var timer = null;
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.classList.contains('is-on')) return;
        var t = b.getAttribute('data-theme'), src = b.getAttribute('data-thumb');
        btns.forEach(function (o) { o.classList.toggle('is-on', o === b); o.setAttribute('aria-checked', String(o === b)); });
        if (link) link.href = base + (t === 'a' ? '' : '?theme=' + t);
        if (cname) cname.textContent = b.getAttribute('data-name');
        if (!img) return;
        var pre = new Image(); pre.src = src;              /* 先読みしてから入れ替える */
        img.classList.add('is-out'); clearTimeout(timer);
        timer = setTimeout(function () { img.src = src; img.classList.remove('is-out'); }, 280);
      });
    });
  });
})();
