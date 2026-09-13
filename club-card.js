/* クラブカードの描画（v2・2026-09-13 新デザイン）。検索ページ（search.html）・TOP・地域ページの生成
   （build-area-pages.mjs）が同じこの1ファイルを使う。見た目は site.css の .nc 系。

   ブラウザ： <script src="/club-card.js"> で window.ChibiCard が生える
   Node    ： ファイルを読んで new Function('window', src) で評価して使う
   ★お気に入り（♡）とコメント（💬）の結線は shared.js（decorateFavs / .sr-cmt-btn） */
(function (root) {
  'use strict';
  function esc(s){return (s==null?'':String(s)).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  var HEART='<svg viewBox="0 0 24 24"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>';
  var CMT='<svg viewBox="0 0 24 24"><path d="M21 11.5a8.5 8.5 0 0 1-12.2 7.7L3 21l1.8-5.8A8.5 8.5 0 1 1 21 11.5z"/></svg>';
  var PIN='<svg class="pin" viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 1 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.3"/></svg>';
  function sportArt(sp){
    sp=sp||'';
    function has(){ for(var i=0;i<arguments.length;i++){ if(sp.indexOf(arguments[i])>=0) return true; } return false; }
    if(has('サッカー','フットボール','フラッグ')) return {c:'#6BAAEF',i:'<circle cx="12" cy="12" r="9"/><polygon points="12,8 15,10.2 13.8,13.8 10.2,13.8 9,10.2"/>'};
    if(has('バスケ'))                              return {c:'#F5A24B',i:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.6 5.6c3.2 3.2 9.6 9.6 12.8 12.8M18.4 5.6C15.2 8.8 8.8 15.2 5.6 18.4"/>'};
    if(has('野球','ベースボール'))                  return {c:'#E8884A',i:'<circle cx="12" cy="12" r="9"/><path d="M7 5.2c2.6 2.8 4.4 7.4 4.4 13.6M17 5.2c-2.6 2.8-4.4 7.4-4.4 13.6"/>'};
    if(has('バレー'))                              return {c:'#FFC83F',i:'<circle cx="12" cy="12" r="9"/><path d="M12 3a18 18 0 010 18M3.4 9c5 1 11.6 4 16.2 9M3.4 15c5-1 11.6-4 16.2-9"/>'};
    if(has('テニス'))                              return {c:'#5BD6A0',i:'<ellipse cx="10" cy="8.5" rx="5" ry="6"/><path d="M6.6 13.2 3.5 19.5M7 6l6 5"/>'};
    if(has('水泳','スイミング'))                    return {c:'#3FB6D6',i:'<circle cx="15" cy="6" r="2"/><path d="M3 16c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 6 0M4 12l5-3 3 2"/>'};
    if(has('バトン')) return {c:'#FF7FB6',i:'<circle cx="6.5" cy="17.5" r="2.2"/><circle cx="17.5" cy="6.5" r="2.2"/><path d="M8 16 L16 8"/><path d="M19.5 4.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6z"/>'};
    if(has('ダブルダッチ')) return {c:'#C98BFF',i:'<path d="M5 4.5c-2.6 4-2.6 11 0 15"/><path d="M19 4.5c2.6 4 2.6 11 0 15"/><circle cx="12" cy="7.5" r="2"/><path d="M12 9.5v5l-2 5M12 14.5l2 5"/>'};
    if(has('マルチ')) return {c:'#2a6fdb',i:'<circle cx="9" cy="9" r="4.6"/><circle cx="15" cy="15" r="4.6"/>'};
    if(has('柔術')) return {c:'#7B8CE8',i:'<path d="M3 11h7l2 2 2-2h7"/><path d="M10 11l-1.5 6M14 11l1.5 6"/>'};
    if(has('レスリング','相撲')) return {c:'#7B8CE8',i:'<circle cx="8" cy="6.5" r="2.2"/><circle cx="16" cy="6.5" r="2.2"/><path d="M8 8.7c0 2 1.6 3.3 4 3.3s4-1.3 4-3.3"/><path d="M6 19c0-3 1-5 2.5-5M18 19c0-3-1-5-2.5-5"/>'};
    if(has('空手','テコンドー')) return {c:'#7B8CE8',i:'<circle cx="11" cy="5" r="2"/><path d="M11 7l-1 6M10 13l-3 5M10 13l5-1M11 10l5 3"/>'};
    if(has('スキー')) return {c:'#58b7d8',i:'<circle cx="16.5" cy="5" r="1.8"/><path d="M4 18 L18 8 M7 19.5 L21 9.5"/>'};
    if(has('スノーボード','スノボ')) return {c:'#e8884a',i:'<rect x="9.5" y="3.5" width="5" height="17" rx="2.5" transform="rotate(32 12 12)"/><circle cx="6.5" cy="9" r="1.4"/><circle cx="17.5" cy="15" r="1.4"/>'};
    if(has('サーフィン')) return {c:'#3FB6D6',i:'<path d="M4.5 19.5c7.5-1.5 12-9.5 15.5-15.5C14 5.5 6.5 11.5 4.5 19.5z"/><path d="M4.5 19.5l2.8-2.8"/>'};
    if(has('カヌー')) return {c:'#b04ae8',i:'<path d="M3 14c3.5 3 14 3 18 0"/><path d="M8 5l8 12M16 5L8 17"/>'};
    if(has('ダンス','チア','バトン'))               return {c:'#FF7FB6',i:'<circle cx="13" cy="5" r="2"/><path d="M13 7l-2 6M11 13l-3.5 5M11 13l4 2M13 9l4-1"/>'};
    if(has('空手','柔道','柔術','剣道','テコンドー','武道','レスリング','相撲')) return {c:'#7B8CE8',i:'<circle cx="12" cy="5" r="2"/><path d="M12 7v5l4 2M12 12l-4 2M8 20l4-4 4 4"/>'};
    if(has('体操','運動','マルチ','リズム','体育','陸上','ダブルダッチ')) return {c:'#C98BFF',i:'<circle cx="12" cy="5" r="2"/><path d="M12 7v6M8 9.5l8 1.5M9 19l3-6 3 6"/>'};
    return {c:'#9aa3ad',i:'<path d="M12 3.5l2.4 4.9 5.4.8-3.9 3.8.9 5.4L12 17.8l-4.8 2.6.9-5.4L4.2 9.2l5.4-.8z"/>'};
  }
  function sportPlaceholder(sp, extra, iconSize){
    var a=sportArt(sp);
    return '<div class="nc-ph" style="'+(extra||'')+'background:linear-gradient(135deg,'+a.c+'2e,'+a.c+'14);">'
      +'<svg viewBox="0 0 24 24" fill="none" stroke="'+a.c+'"'+(iconSize?' style="width:'+iconSize+'px;height:'+iconSize+'px"':'')+'>'+a.i+'</svg></div>';
  }
  function badge(sp){ var a=sportArt(sp); return '<span class="sb" style="background:'+a.c+'"><svg viewBox="0 0 24 24">'+a.i+'</svg></span>'; }
  function isPaid(t){ if(!t||!t.plan||t.plan==='free') return false; if(t.plan_expires_at && new Date(t.plan_expires_at)<new Date()) return false; return true; }
  function isNew(t){ if(!t||!t.created_at) return false; var d=(Date.now()-new Date(t.created_at).getTime())/86400000; return d>=0 && d<=14; }
  function tags(t){
    var a=[];
    if(t.trial) a.push({t:'体験OK'});
    if(t.girls_welcome) a.push({t:'女の子歓迎'});
    if(t.female_instructor) a.push({t:'女性指導者あり'});
    (Array.isArray(t.moods)?t.moods:[]).forEach(function(m){ if(m) a.push({t:m,m:m}); });
    return a.slice(0,3);
  }
  function card(t, opts){
    opts=opts||{};
    var area=[t.pref,t.city].filter(Boolean).join(' ');
    var pos=(t.photo_url && Array.isArray(t.photo_positions) && t.photo_positions[0])?t.photo_positions[0]:'50% 50%';
    var media=t.photo_url ? '<img src="'+esc(t.photo_url)+'" alt="'+esc(t.name)+'" loading="lazy" decoding="async" style="object-position:'+esc(pos)+'">' : sportPlaceholder(t.sport);
    var desc=(t.description||'').replace(/\s+/g,' ').trim();
    var tg=tags(t);
    var moods=(Array.isArray(t.moods)?t.moods:[]).join(',');
    return '<a href="/club.html?id='+esc(t.id)+'" class="club-card nc" data-id="'+esc(t.id)+'" data-name="'+esc(t.name)+'" data-area="'+esc(area)+'" data-pref="'+esc((t.pref||'').replace(/[都道府県]$/,''))+'" data-city="'+esc(t.city||'')+'" data-sport="'+esc(t.sport)+'" data-mood="'+esc(moods)+'">'
      +'<div class="nc-img">'+media
        +((opts.isNew!=null?opts.isNew:isNew(t))?'<span class="nc-new">新着</span>':'')
        +((opts.pr!=null?opts.pr:isPaid(t))?'<span class="nc-pr">PR</span>':'')
        +'<span class="nc-fav" role="button" aria-label="お気に入り">'+HEART+'</span>'
        +(t.video_url?'<span class="nc-vid">▶ 動画</span>':'')
      +'</div>'
      +'<div class="nc-b">'
        +'<div class="nc-top">'+badge(t.sport)+'<span class="sp">'+esc(t.sport)+'</span></div>'
        +'<h3 class="nc-name">'+esc(t.name)+'</h3>'
        +'<div class="nc-area">'+PIN+esc(area)+'</div>'
        +(desc?'<div class="nc-desc">'+esc(desc)+'</div>':'')
        +(tg.length?'<div class="nc-tags">'+tg.map(function(x){return '<span'+(x.m?' data-mood="'+esc(x.m)+'"':'')+'>'+esc(x.t)+'</span>';}).join('')+'</div>':'')
        +'<div class="nc-foot"><span class="lk">'+HEART+(t.likes||0)+'</span><span class="cm sr-cmt-btn" data-id="'+esc(t.id)+'" title="コメントを見る・書く">'+CMT+(t.comments||0)+'</span></div>'
      +'</div></a>';
  }
  root.ChibiCard = { esc: esc, sportArt: sportArt, sportPlaceholder: sportPlaceholder, badge: badge, isPaid: isPaid, isNew: isNew, card: card, HEART: HEART, CMT: CMT, PIN: PIN };
})(typeof window !== 'undefined' ? window : globalThis);
