/* 凛 こども空手教室 — デザイン04「凛と」統合版 Vanilla JS */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var pref = window.matchMedia('(prefers-reduced-motion: reduce)');
  var motion = !pref.matches;

  /* ---------- 出現（.reveal と .label に合図） ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  $$('.reveal, .label').forEach(function (el) { io.observe(el); });

  /* ---------- 稽古の流れ：朱の線が伸びる ---------- */
  var flow = $('#flowline');
  if (flow) {
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { flow.style.setProperty('--fp', 1); fio.disconnect(); } });
    }, { threshold: 0.3 });
    fio.observe(flow);
  }

  /* ---------- 数字（静かに数える） ---------- */
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function fmt(n, el) { return (el && el.hasAttribute('data-plain')) ? String(n) : n.toLocaleString('ja-JP'); }
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var el = e.target, to = parseInt(el.getAttribute('data-count'), 10) || 0;
      if (!motion || to === 0) { el.textContent = fmt(to, el); return; }
      var t0 = null, dur = 1400;
      requestAnimationFrame(function tick(now) {
        if (t0 === null) t0 = now;
        var p = Math.max(0, Math.min(1, (now - t0) / dur));
        el.textContent = fmt(Math.round(to * easeOut(p)), el);
        if (p < 1) requestAnimationFrame(tick); else el.textContent = fmt(to, el);
      });
    });
  }, { threshold: 0.5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- スクロール連動：ナビ／ヒーロー視差／「始」の漂い／固定CTA ---------- */
  var nav = $('#nav'), fixbar = $('#fixbar'), hero = $('#hero'), kanji = $('.kanji');
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset, vh = window.innerHeight;
    var docH = document.documentElement.scrollHeight - vh;
    nav.classList.toggle('is-solid', y > 60);
    if (fixbar) fixbar.classList.toggle('is-show', y > vh * 0.6 && y < docH - 200);
    if (!motion) return;
    if (hero) {
      var p = Math.max(0, Math.min(1, y / hero.offsetHeight));
      hero.style.setProperty('--py', (p * 55).toFixed(1) + 'px');
      hero.style.setProperty('--cy', (p * 110).toFixed(1) + 'px');
    }
    if (kanji) {
      var r = kanji.getBoundingClientRect(); var c = r.top + r.height / 2 - vh / 2;
      kanji.style.setProperty('--ky', (-c * 0.12).toFixed(1) + 'px');
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();

  /* ---------- 動きを止める（ハーネス／reduced-motion 用。画面には出さない） ---------- */
  var mbtn = $('#motion');
  function syncMotion() {
    document.body.classList.toggle('motion-paused', !motion);
    if (mbtn) { mbtn.textContent = motion ? '動きを止める' : '動きを再開'; mbtn.setAttribute('aria-pressed', String(!motion)); }
    if (!motion) {
      $$('.reveal, .label').forEach(function (el) { el.classList.add('is-in'); });
      if (flow) flow.style.setProperty('--fp', 1);
      $$('[data-count]').forEach(function (el) { el.textContent = fmt(parseInt(el.getAttribute('data-count'), 10) || 0, el); });
      if (hero) { hero.style.setProperty('--py', '0px'); hero.style.setProperty('--cy', '0px'); }
      if (kanji) kanji.style.setProperty('--ky', '0px');
    }
    update();
  }
  if (mbtn) mbtn.addEventListener('click', function () { motion = !motion; syncMotion(); });
  pref.addEventListener('change', function () { motion = !pref.matches; syncMotion(); });
  if (!motion) syncMotion();

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

  /* ---------- トースト・デモリンク・フォーム（本番では送信先につなぐ） ---------- */
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
