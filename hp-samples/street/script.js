/* STUDIO BOUNCE — interactions (vanilla JS, no deps) */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- 1. hero: split letters ---------- */
  $$('[data-split]').forEach(function (el, l) {
    var text = el.textContent;
    el.textContent = '';
    el.setAttribute('aria-label', text);
    Array.prototype.forEach.call(text, function (ch, i) {
      var s = document.createElement('span');
      s.className = 'ch';
      s.textContent = ch;
      s.style.setProperty('--i', i);
      s.style.setProperty('--l', l);
      s.setAttribute('aria-hidden', 'true');
      el.appendChild(s);
    });
  });

  /* ---------- 2. loader ---------- */
  var loader = $('#loader');
  var hero = $('#hero');
  function start() {
    if (loader) loader.classList.add('is-done');
    document.body.classList.remove('is-locked');
    setTimeout(function () {
      hero.classList.add('is-in');
      $$('.hero .reveal').forEach(function (el) { el.classList.add('is-in'); });
    }, reduced ? 0 : 250);
    setTimeout(function () { if (loader) loader.remove(); }, 1200);
  }
  document.body.classList.add('is-locked');
  if (reduced) { start(); }
  else {
    var done = false;
    var go = function () { if (!done) { done = true; start(); } };
    window.addEventListener('load', function () { setTimeout(go, 900); });
    setTimeout(go, 2600); // フォント待ちで止まらないための保険
  }

  /* ---------- 3. reveal on scroll ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
  $$('.reveal').forEach(function (el) { if (!el.closest('.hero')) io.observe(el); });

  /* ---------- 4. counters ---------- */
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function fmt(n) { return n.toLocaleString('ja-JP'); }
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var el = e.target, to = parseInt(el.getAttribute('data-count'), 10) || 0;
      if (reduced || to === 0) { el.textContent = fmt(to); return; }
      var t0 = null, dur = 1400;
      requestAnimationFrame(function tick(now) {
        if (t0 === null) t0 = now;
        var p = Math.max(0, Math.min(1, (now - t0) / dur));
        el.textContent = fmt(Math.round(to * easeOut(p)));
        if (p < 1) requestAnimationFrame(tick); else el.textContent = fmt(to);
      });
    });
  }, { threshold: 0.5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- 5. scroll-driven: header / progress / giant text / parallax / movie ---------- */
  var header = $('#header');
  var progress = $('#progress');
  var fixbar = $('#fixbar');
  var giants = $$('[data-giant]');
  var paras = $$('[data-parallax]');
  var movie = $('#movie');
  var movieVideo = $('#movieVideo');
  var ticking = false;

  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    var vh = window.innerHeight;
    var docH = document.documentElement.scrollHeight - vh;

    header.classList.toggle('is-solid', y > 40);
    if (progress) progress.style.setProperty('--sp', docH > 0 ? (y / docH).toFixed(4) : 0);
    if (fixbar) fixbar.classList.toggle('is-show', y > vh * 0.7 && y < docH - 300);

    if (!reduced) {
      giants.forEach(function (g) {
        var r = g.parentElement.getBoundingClientRect();
        var p = (vh - r.top) / (r.height + vh); // 0 → 1 while section crosses viewport
        g.style.setProperty('--p', Math.max(0, Math.min(1, (p - 0.1) / 0.7)).toFixed(3));
      });
      paras.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var c = r.top + r.height / 2 - vh / 2;
        el.style.setProperty('--py', (-c * parseFloat(el.getAttribute('data-parallax'))).toFixed(1) + 'px');
      });
      if (movie) {
        var mr = movie.getBoundingClientRect();
        var mp = -mr.top / (mr.height - vh);
        movie.style.setProperty('--vp', easeOut(Math.max(0, Math.min(1, mp))).toFixed(3));
      }
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();

  /* ---------- 6. video: play only when visible / sound toggle ---------- */
  if (movieVideo) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { var p = movieVideo.play(); if (p && p.catch) p.catch(function () {}); }
        else movieVideo.pause();
      });
    }, { threshold: 0.2 });
    vio.observe(movieVideo);
    var snd = $('#soundToggle');
    if (snd) snd.addEventListener('click', function () {
      movieVideo.muted = !movieVideo.muted;
      snd.textContent = movieVideo.muted ? '🔇' : '🔊';
      snd.setAttribute('aria-pressed', String(!movieVideo.muted));
    });
  }

  /* ---------- 7. mobile menu ---------- */
  var burger = $('#burger'), menu = $('#menu');
  function setMenu(open) {
    burger.classList.toggle('is-open', open);
    menu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('is-locked', open);
  }
  burger.addEventListener('click', function () { setMenu(!menu.classList.contains('is-open')); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* ---------- 8. drag-to-scroll (class cards) ---------- */
  var track = $('#clsTrack');
  if (track && window.matchMedia('(pointer:fine)').matches) {
    var down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', function (e) { down = true; moved = false; sx = e.clientX; sl = track.scrollLeft; });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (Math.abs(dx) > 4) { moved = true; track.classList.add('is-drag'); }
      track.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () { down = false; setTimeout(function () { track.classList.remove('is-drag'); }, 50); });
    track.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
  }

  /* ---------- 9. tilt (teacher cards) ---------- */
  if (window.matchMedia('(pointer:fine)').matches && !reduced) {
    $$('[data-tilt]').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateX(' + (-y * 8).toFixed(2) + 'deg) rotateY(' + (x * 10).toFixed(2) + 'deg) translateY(-4px)';
      });
      card.addEventListener('pointerleave', function () { card.style.transform = ''; });
    });
  }

  /* ---------- 10. magnetic buttons ---------- */
  if (window.matchMedia('(pointer:fine)').matches && !reduced) {
    $$('[data-magnet]').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        b.style.transform = 'translate(' + (x * 0.18).toFixed(1) + 'px,' + (y * 0.28).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }

  /* ---------- 11. schedule tabs ---------- */
  var SCHEDULE = {
    tue: [
      { t: '15:00', n: 'リトルダンス', s: '3〜5歳 ／ 45分 ／ MIKU', tag: '残り2', cls: 'is-few' },
      { t: '16:30', n: 'キッズHIPHOP（入門）', s: '小1〜小3 ／ 60分 ／ MIKU', tag: '受付中' },
      { t: '18:00', n: 'ジュニアHIPHOP', s: '小4〜中学生 ／ 60分 ／ RYO', tag: '受付中' },
      { t: '19:30', n: '選抜チーム練習', s: 'オーディション制 ／ 90分', tag: '選抜のみ' }
    ],
    wed: [
      { t: '16:30', n: 'キッズHIPHOP', s: '小1〜小3 ／ 60分 ／ MIKU', tag: '受付中' },
      { t: '18:00', n: 'ジュニアHIPHOP', s: '小4〜中学生 ／ 60分 ／ RYO', tag: '満席', cls: 'is-full' },
      { t: '19:30', n: '中学生HIPHOP', s: '中1〜中3 ／ 60分 ／ RYO', tag: '受付中' }
    ],
    thu: [
      { t: '17:00', n: 'ジャズ', s: '小3〜中学生 ／ 60分 ／ SAKI', tag: '受付中' },
      { t: '18:00', n: 'K-POPキッズ', s: '小3〜中学生 ／ 60分 ／ RYO', tag: '新設', cls: 'is-few' },
      { t: '19:30', n: 'ジャズ（上級）', s: '講師推薦 ／ 75分 ／ SAKI', tag: '推薦制' }
    ],
    fri: [
      { t: '16:30', n: 'キッズHIPHOP', s: '小1〜小3 ／ 60分 ／ RYO', tag: '残り3', cls: 'is-few' },
      { t: '18:00', n: 'ジュニアHIPHOP', s: '小4〜中学生 ／ 60分 ／ MIKU', tag: '受付中' },
      { t: '19:30', n: '中学生HIPHOP', s: '中1〜中3 ／ 60分 ／ MIKU', tag: '受付中' }
    ],
    sat: [
      { t: '10:00', n: 'リトルダンス', s: '3〜5歳 ／ 45分 ／ SAKI', tag: '受付中' },
      { t: '11:00', n: 'キッズHIPHOP（土曜）', s: '小1〜小3 ／ 60分 ／ SAKI', tag: '受付中' },
      { t: '14:00', n: 'ジャズ（土曜）', s: '小3〜中学生 ／ 60分 ／ SAKI', tag: '受付中' },
      { t: '16:00', n: 'ブレイキン', s: '小2〜中学生 ／ 60分 ／ KENTO', tag: '残り1', cls: 'is-few' },
      { t: '17:30', n: 'ブレイキン（中級）', s: '経験1年〜 ／ 60分 ／ KENTO', tag: '受付中' }
    ]
  };
  var tabs = $$('.tabs [role=tab]'), ink = $('.tabs__ink'), panel = $('#schPanel');
  function renderDay(day) {
    panel.innerHTML = SCHEDULE[day].map(function (r, i) {
      return '<div class="srow" style="--i:' + i + '"><time>' + r.t + '</time><div><b>' + r.n + '</b><small>' + r.s + '</small></div><span class="tag ' + (r.cls || '') + '">' + r.tag + '</span></div>';
    }).join('');
  }
  function selectTab(btn) {
    tabs.forEach(function (b) { b.setAttribute('aria-selected', String(b === btn)); });
    ink.style.width = btn.offsetWidth + 'px';
    ink.style.setProperty('--x', btn.offsetLeft + 'px');
    renderDay(btn.getAttribute('data-day'));
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { selectTab(b); }); });
  if (tabs.length) { selectTab(tabs[0]); window.addEventListener('resize', function () { selectTab(tabs.filter(function (b) { return b.getAttribute('aria-selected') === 'true'; })[0]); }); }

  /* ---------- 12. toast / demo links / form ---------- */
  var toast = $('#toast'), tt;
  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('is-show');
    clearTimeout(tt);
    tt = setTimeout(function () { toast.classList.remove('is-show'); }, 3200);
  }
  $$('[data-demo]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); showToast('見本サイトのため ' + a.getAttribute('data-demo') + ' は動きません。本番では実際のリンクにつなぎます。'); });
  });
  var form = $('#trialForm');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    $$('[required]', form).forEach(function (f) {
      var bad = !f.value.trim();
      f.classList.toggle('is-error', bad);
      if (bad) ok = false;
    });
    if (!ok) { showToast('お名前・年齢・連絡先を入力してください'); return; }
    showToast('（デモ）送信しました。本番ではメール／LINE通知につなぎます。');
    form.reset();
  });
})();
