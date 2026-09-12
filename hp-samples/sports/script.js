/* きしわだベースボールクラブ — 型C（全面写真＋巨大タイポ＋落書き）Vanilla JS */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- hero：読み込み後に帯・文字・落書きを出す ---------- */
  var hero = $('#hero');
  function heroIn() { hero.classList.add('is-in'); $$('.hero .reveal').forEach(function (el) { el.classList.add('is-in'); }); }
  window.addEventListener('load', function () { setTimeout(heroIn, reduced ? 0 : 200); });
  setTimeout(heroIn, 2400);

  /* ---------- 出現（見出しのマーカー・落書きの描画も同じ合図） ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  $$('.reveal, .h2, .about__photos').forEach(function (el) { if (!el.closest('.hero')) io.observe(el); });

  /* ---------- 数字カウントアップ ---------- */
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function fmt(n) { return n.toLocaleString('ja-JP'); }
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var el = e.target, to = parseInt(el.getAttribute('data-count'), 10) || 0;
      if (reduced || to === 0) { el.textContent = fmt(to); return; }
      var t0 = null, dur = 1300;
      requestAnimationFrame(function tick(now) {
        if (t0 === null) t0 = now;
        var p = Math.max(0, Math.min(1, (now - t0) / dur));
        el.textContent = fmt(Math.round(to * easeOut(p)));
        if (p < 1) requestAnimationFrame(tick); else el.textContent = fmt(to);
      });
    });
  }, { threshold: 0.5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- スクロール連動：ナビ／写真のふわふわ視差／固定CTA ---------- */
  var nav = $('#nav'), fixbar = $('#fixbar'), floats = $$('[data-float]');
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset, vh = window.innerHeight;
    var docH = document.documentElement.scrollHeight - vh;
    nav.classList.toggle('is-solid', y > 40);
    if (fixbar) fixbar.classList.toggle('is-show', y > vh * 0.6 && y < docH - 200);
    if (!reduced) floats.forEach(function (el) {
      var r = el.getBoundingClientRect(); var c = r.top + r.height / 2 - vh / 2;
      var k = parseInt(el.getAttribute('data-float'), 10) || 1;
      el.style.setProperty('--fy', (-c * (0.04 * k)).toFixed(1) + 'px');
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();

  /* ---------- メニュー ---------- */
  var burger = $('#burger'), menu = $('#menu');
  function setMenu(open) {
    burger.classList.toggle('is-open', open); menu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('is-locked', open);
  }
  burger.addEventListener('click', function () { setMenu(!menu.classList.contains('is-open')); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* ---------- 年間費用シミュレーター ---------- */
  var PRICE = { entry: 3300, annual: 6600, uni: 16500, monthly: { tee: 3300, jr: 5500, reg: 5500 } };
  var gSel = $('#calcGrade'), sSel = $('#calcSib');
  function calc() {
    if (!gSel) return;
    var sib = sSel.value === '1', m = PRICE.monthly[gSel.value];
    var entry = sib ? 0 : PRICE.entry, monthly = (sib ? m / 2 : m) * 12;
    var total = entry + monthly + PRICE.annual + PRICE.uni;
    $('#cEntry').textContent = fmt(entry); $('#cMonthly').textContent = fmt(monthly);
    $('#cAnnual').textContent = fmt(PRICE.annual); $('#cUni').textContent = fmt(PRICE.uni);
    var t = $('#cTotal'); t.textContent = fmt(total);
    t.classList.remove('is-bump'); void t.offsetWidth; t.classList.add('is-bump');
    $('.calc__note').textContent = '2年目からは月謝と年会費のみ（年' + fmt(monthly + PRICE.annual) + '円）。';
  }
  if (gSel) { gSel.addEventListener('change', calc); sSel.addEventListener('change', calc); calc(); }

  /* ---------- トースト・デモリンク・フォーム ---------- */
  var toast = $('#toast'), tt;
  function showToast(msg) { toast.textContent = msg; toast.classList.add('is-show'); clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove('is-show'); }, 3200); }
  $$('[data-demo]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); showToast('見本サイトのため ' + a.getAttribute('data-demo') + ' は動きません。本番では実際のリンクにつなぎます。'); }); });
  var form = $('#trialForm');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    $$('[required]', form).forEach(function (f) { var bad = !f.value.trim(); f.classList.toggle('is-error', bad); if (bad) ok = false; });
    if (!ok) { showToast('お名前・学年・連絡先を入力してください'); return; }
    showToast('（デモ）送信しました。本番ではメール／LINE通知につなぎます。'); form.reset();
  });
})();
