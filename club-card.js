/* クラブカードの描画。検索ページ（search.html）と、地域ページの生成
   （build-area-pages.mjs）の両方がこの1ファイルを使う。
   2箇所に同じHTMLを書くと、片方だけ直して見た目がズレるため。

   ブラウザ： <script src="/club-card.js"> で window.ChibiCard が生える
   Node    ： ファイルを読んで new Function('window', src) で評価して使う */
(function (root) {
  'use strict';

function esc(s){return (s==null?'':String(s)).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function svgIcon(stroke,inner){ return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="'+stroke+'" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'+inner+'</svg>'; }
  function sportIcon(sp){
    sp=sp||'';
    function has(){ for(var i=0;i<arguments.length;i++){ if(sp.indexOf(arguments[i])>=0) return true; } return false; }
    if(has('サッカー','フットボール','フラッグ')) return svgIcon('#6BAAEF','<circle cx="12" cy="12" r="9"/><polygon points="12,8 15,10.2 13.8,13.8 10.2,13.8 9,10.2"/>');
    if(has('バスケ'))                              return svgIcon('#F5A24B','<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.6 5.6c3.2 3.2 9.6 9.6 12.8 12.8M18.4 5.6C15.2 8.8 8.8 15.2 5.6 18.4"/>');
    if(has('野球','ベースボール'))                  return svgIcon('#E8884A','<circle cx="12" cy="12" r="9"/><path d="M7 5.2c2.6 2.8 4.4 7.4 4.4 13.6M17 5.2c-2.6 2.8-4.4 7.4-4.4 13.6"/>');
    if(has('バレー'))                              return svgIcon('#FFC83F','<circle cx="12" cy="12" r="9"/><path d="M12 3a18 18 0 010 18M3.4 9c5 1 11.6 4 16.2 9M3.4 15c5-1 11.6-4 16.2-9"/>');
    if(has('テニス'))                              return svgIcon('#5BD6A0','<ellipse cx="10" cy="8.5" rx="5" ry="6"/><path d="M6.6 13.2 3.5 19.5M7 6l6 5"/>');
    if(has('水泳','スイミング'))                    return svgIcon('#3FB6D6','<circle cx="15" cy="6" r="2"/><path d="M3 16c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 6 0M4 12l5-3 3 2"/>');
    if(has('バトン')) return svgIcon('#FF7FB6','<circle cx="6.5" cy="17.5" r="2.2"/><circle cx="17.5" cy="6.5" r="2.2"/><path d="M8 16 L16 8"/><path d="M19.5 4.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6z"/>');
    if(has('ダブルダッチ')) return svgIcon('#C98BFF','<path d="M5 4.5c-2.6 4-2.6 11 0 15"/><path d="M19 4.5c2.6 4 2.6 11 0 15"/><circle cx="12" cy="7.5" r="2"/><path d="M12 9.5v5l-2 5M12 14.5l2 5"/>');
    if(has('マルチ')) return svgIcon('#2a6fdb','<circle cx="9" cy="9" r="4.6"/><circle cx="15" cy="15" r="4.6"/>');
    if(has('柔術')) return svgIcon('#7B8CE8','<path d="M3 11h7l2 2 2-2h7"/><path d="M10 11l-1.5 6M14 11l1.5 6"/>');
    if(has('レスリング','相撲')) return svgIcon('#7B8CE8','<circle cx="8" cy="6.5" r="2.2"/><circle cx="16" cy="6.5" r="2.2"/><path d="M8 8.7c0 2 1.6 3.3 4 3.3s4-1.3 4-3.3"/><path d="M6 19c0-3 1-5 2.5-5M18 19c0-3-1-5-2.5-5"/>');
    if(has('空手','テコンドー')) return svgIcon('#7B8CE8','<circle cx="11" cy="5" r="2"/><path d="M11 7l-1 6M10 13l-3 5M10 13l5-1M11 10l5 3"/>');
    if(has('スキー')) return svgIcon('#58b7d8','<circle cx="16.5" cy="5" r="1.8"/><path d="M4 18 L18 8 M7 19.5 L21 9.5"/>');
    if(has('スノーボード','スノボ')) return svgIcon('#e8884a','<rect x="9.5" y="3.5" width="5" height="17" rx="2.5" transform="rotate(32 12 12)"/><circle cx="6.5" cy="9" r="1.4"/><circle cx="17.5" cy="15" r="1.4"/>');
    if(has('サーフィン')) return svgIcon('#3FB6D6','<path d="M4.5 19.5c7.5-1.5 12-9.5 15.5-15.5C14 5.5 6.5 11.5 4.5 19.5z"/><path d="M4.5 19.5l2.8-2.8"/>');
    if(has('カヌー')) return svgIcon('#b04ae8','<path d="M3 14c3.5 3 14 3 18 0"/><path d="M8 5l8 12M16 5L8 17"/>');
    if(has('ダンス','チア','バトン'))               return svgIcon('#FF7FB6','<circle cx="13" cy="5" r="2"/><path d="M13 7l-2 6M11 13l-3.5 5M11 13l4 2M13 9l4-1"/>');
    if(has('空手','柔道','柔術','剣道','テコンドー','武道','レスリング','相撲')) return svgIcon('#7B8CE8','<circle cx="12" cy="5" r="2"/><path d="M12 7v5l4 2M12 12l-4 2M8 20l4-4 4 4"/>');
    if(has('体操','運動','マルチ','リズム','体育','陸上','ダブルダッチ')) return svgIcon('#C98BFF','<circle cx="12" cy="5" r="2"/><path d="M12 7v6M8 9.5l8 1.5M9 19l3-6 3 6"/>');
    return svgIcon('#9aa3ad','<path d="M12 3.5l2.4 4.9 5.4.8-3.9 3.8.9 5.4L12 17.8l-4.8 2.6.9-5.4L4.2 9.2l5.4-.8z"/>');
  }
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
    return '<div style="width:100%;'+extra+'display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,'+a.c+'2e,'+a.c+'14);">'
      +'<svg width="'+(iconSize||72)+'" height="'+(iconSize||72)+'" viewBox="0 0 24 24" fill="none" stroke="'+a.c+'" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" style="opacity:.9;">'+a.i+'</svg></div>';
  }
  function card(t){
    var pref=(t.pref||'').replace(/[都道府県]$/,'');
    var area=[t.pref,t.city].filter(Boolean).join('・');
    var pos=(t.photo_url && Array.isArray(t.photo_positions) && t.photo_positions[0])?t.photo_positions[0]:'50% 50%';
    var media=t.photo_url ? '<img src="'+esc(t.photo_url)+'" alt="'+esc(t.name)+'" loading="lazy" decoding="async" style="width:100%;aspect-ratio:4/3;object-fit:cover;object-position:'+pos+';display:block;border-radius:0 0 12px 12px;">' : sportPlaceholder(t.sport,'aspect-ratio:4/3;border-radius:0 0 12px 12px;');
    return '<a href="club.html?id='+esc(t.id)+'" class="club-card" data-pref="'+esc(pref)+'" data-city="'+esc(t.city||'')+'" data-sport="'+esc(t.sport)+'" data-mood="'+esc((t.moods||[]).join(','))+'" style="display:flex;flex-direction:column;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #e6e9ed;box-shadow:0 2px 8px rgba(20,28,38,.08);text-decoration:none;color:#1f2a37;">'
      +media
      +'<div style="padding:11px 13px 14px;flex:1;display:flex;flex-direction:column;">'
      +'<div style="display:inline-flex;align-items:center;gap:6px;margin-bottom:5px;"><span style="width:22px;height:22px;border-radius:50%;background:#f1f3f6;display:flex;align-items:center;justify-content:center;font-size:13px;">'+sportIcon(t.sport)+'</span><span style="font-size:12px;font-weight:600;color:#7b8492;">'+esc(t.sport)+'</span></div>'
      +'<h3 class="cc-cardname" style="margin:0 0 5px;font-family:\'Zen Maru Gothic\',sans-serif;font-size:16px;font-weight:800;color:#1f2a37;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;word-break:break-word;">'+esc(t.name)+'</h3>'
      +'<div style="display:flex;align-items:center;gap:5px;font-size:12px;color:#7b8492;margin-bottom:8px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9aa3ad" stroke-width="1.9" style="flex:0 0 13px;"><path d="M12 21s-7-5.5-7-11a7 7 0 1 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.3"/></svg><span style="flex:1;min-width:0;overflow:hidden;white-space:nowrap;-webkit-mask-image:linear-gradient(90deg,#000 80%,transparent);mask-image:linear-gradient(90deg,#000 80%,transparent);">'+esc(area)+'</span></div>'
      +(t.description?'<div class="cc-carddesc" style="font-size:11.5px;line-height:1.55;color:#5b6573;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">'+esc(t.description)+'</div>':'')
      +'<div style="display:flex;align-items:center;gap:14px;font-size:12px;font-weight:700;color:#3a4452;margin-top:auto;padding-top:10px;">'
        +'<span style="display:inline-flex;align-items:center;gap:4px;"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#c7ccd3" stroke-width="2"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>'+(t.likes||0)+'</span>'
        +'<span class="sr-cmt-btn" data-id="'+esc(t.id)+'" title="コメントを見る・書く" style="display:inline-flex;align-items:center;gap:4px;cursor:pointer;"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7b8492" stroke-width="1.9"><path d="M21 11.5a8.5 8.5 0 0 1-12.2 7.7L3 21l1.8-5.8A8.5 8.5 0 1 1 21 11.5z"/></svg>'+(t.comments||0)+'</span>'
      +'</div>'
      +'</div></a>';
  }
  root.ChibiCard = { esc: esc, sportArt: sportArt, sportPlaceholder: sportPlaceholder, card: card };
})(typeof window !== 'undefined' ? window : globalThis);
