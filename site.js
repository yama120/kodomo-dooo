/* チビスポ 新デザイン共通の動き（2026-09-13）
   - 節の背景に英字の巨大タイポ（.sec に .eyebrow があれば自動）。スクロール量で左から塗る
   - 出現アニメ（.rv → .in）
   ページ側は window.ChibiBg.set(sec, text) で背景の文字を差し替えられる（検索結果の地域×種目など） */
(function(){
  var els=[];
  function ensure(sec){
    var d=sec.querySelector(':scope > .bgw');
    if(d) return d;
    var w=sec.querySelector('.wrap'); if(!w) return null;
    d=document.createElement('div'); d.className='bgw'; d.setAttribute('aria-hidden','true');
    sec.insertBefore(d,w); els.push({el:d,sec:sec}); return d;
  }
  function set(sec,text){ var d=ensure(sec); if(!d) return null; d.textContent=text; upd(); return d; }
  function auto(){
    document.querySelectorAll('.sec').forEach(function(sec){
      if(sec.classList.contains('nobg')) return;
      var eb=sec.querySelector('.eyebrow'); var t=sec.getAttribute('data-bg')||(eb?eb.textContent.trim():'');
      if(t) set(sec,t);
    });
  }
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches, tick=false;
  function upd(){
    tick=false; if(reduce) return; var vh=innerHeight;
    els.forEach(function(o){
      var r=o.sec.getBoundingClientRect();
      if(r.bottom<-200||r.top>vh+200) return;
      var p=(vh-r.top)/(vh*0.72); p=p<0?0:p>1?1:p;
      o.el.style.setProperty('--p',(p*100).toFixed(1)+'%');
    });
  }
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});
  addEventListener('resize',upd,{passive:true});
  var TARGETS='.sec-h,.sec-sub,.rail,.grid,.gen,.news,.chips,.svc-h,.svc-g,.app,.clubcta,.jb,.arts,.wall,.seo .row';
  function showAll(){ document.querySelectorAll(TARGETS).forEach(function(el){ el.classList.add('in'); }); }
  function reveal(){
    if(!('IntersectionObserver' in window)){ showAll(); return; }
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll(TARGETS).forEach(function(el){el.classList.add('rv');io.observe(el)});
  }
  function init(){ auto(); upd(); if(/noanim=1/.test(location.search)) showAll(); else reveal(); }
  window.ChibiBg={set:set,ensure:ensure,update:upd};
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
