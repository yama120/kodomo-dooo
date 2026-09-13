(function(){
  var id=new URLSearchParams(location.search).get('id');
  var SB='https://emkpkomrgknzrmxqbrvx.supabase.co', ANON='__ANON__';
  function veilOff(){ var v=document.getElementById('cd-veil'); if(!v) return; v.style.opacity='0'; setTimeout(function(){ v.remove(); },260); }
  setTimeout(veilOff,4000);
  function el(x){ return document.getElementById(x); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function setText(idn,v){ var e=el(idn); if(e&&v!=null) e.textContent=v; }
  function yen(n){ return '¥'+Number(n).toLocaleString('ja-JP'); }
  if(!id || !window.supabase){ veilOff(); location.replace('search.html'); return; }
  var db=supabase.createClient(SB,ANON);

  /* ---- モーダル ---- */
  function modal(idn,o){ var m=el(idn); if(!m) return; m.style.display=o?'flex':'none'; document.body.classList.toggle('cd-lock',!!o); }

  /* ---- お気に入り（上のハートと♡数、Chibi と同期） ---- */
  var favData={id:id,name:'',area:'',img:'',href:'club.html?id='+encodeURIComponent(id)};
  function renderFav(){ var on=window.Chibi&&Chibi.isFav(id); [el('cd-fav'),el('cd-like-top')].forEach(function(b){ if(b) b.classList.toggle('on',!!on); }); }
  function toggleFav(e){ e.preventDefault(); if(!window.Chibi) return; Chibi.toggleFav(favData); renderFav(); var n=el('cd-like-n'); if(n){ var v=parseInt(n.textContent,10)||0; n.textContent=Math.max(0,v+(Chibi.isFav(id)?1:-1)); } }
  [el('cd-fav'),el('cd-like-top')].forEach(function(b){ if(b) b.addEventListener('click',toggleFav); });
  document.addEventListener('chibi:favs',renderFav);

  /* ---- 追従バー：最初のCTAを過ぎたら出す（2つ目のCTAが見えたら隠す） ---- */
  (function(){ var st=el('sticky'),c1=document.querySelector('.cta1'),c2=el('cta2'); if(!st||!c1||!('IntersectionObserver' in window)) return;
    var past1=false,see2=false; function upd(){ st.classList.toggle('on',past1&&!see2); }
    new IntersectionObserver(function(e){ past1=!e[0].isIntersecting&&e[0].boundingClientRect.top<0; upd(); },{threshold:0}).observe(c1);
    if(c2) new IntersectionObserver(function(e){ see2=e[0].isIntersecting; upd(); },{threshold:.2}).observe(c2);
  })();

  var COLS='id,name,sport,pref,city,address,venue,age_groups,age_min,days,fee,fee_num,admission_fee_num,trial,girls_welcome,female_instructor,description,photo_url,photos,photo_positions,logo_url,logo_position,website_url,line_url,instagram,twitter,moods,points,recommended_for,courses,plan,plan_expires_at,status,created_at,trial_fee,member_count,cost_items,style,staff,video_url,postal_code,address1,address2,editor_headline,editor_note';
  db.from('teams').select(COLS).eq('id',id).eq('status','approved').single().then(function(res){
    if(res.error||!res.data){ console.warn('[chibispo] クラブ取得失敗',res&&res.error); veilOff(); document.title='クラブが見つかりません｜チビスポ'; setText('cd-name','このクラブは見つかりませんでした'); return; }
    var t=res.data; window._cdTeam=t;
    favData.name=t.name||''; favData.area=[t.pref,t.city].filter(Boolean).join(' '); favData.img=t.photo_url||''; renderFav();
    var paid=window.ChibiCard&&ChibiCard.isPaid(t);
    var area=[t.pref,t.city].filter(Boolean).join(' ');
    var addrFull=[t.pref,t.city,t.address1||t.address,t.address2].filter(Boolean).join(' ');
    document.title=(t.name||'クラブ')+'｜チビスポ';

    /* SEO：1ファイル使い回しなので、ここで canonical・説明・構造化データを入れる */
    (function(){
      var head=document.head;
      var desc=[esc(t.name)+'（'+area+'）の'+esc(t.sport||'スポーツ')+'クラブ。',(t.age_groups&&t.age_groups.length)?'対象は'+t.age_groups.join('・')+'。':'',(t.fee_num!=null)?(Number(t.fee_num)===0?'月謝は無料。':'月謝は'+yen(t.fee_num)+'〜。'):'',(t.days&&t.days.length)?t.days.join('・')+'曜に活動。':'',t.trial?'体験・見学を受け付けています。':''].join('').slice(0,150);
      function meta(sel,attr,val,content){ var e=head.querySelector(sel); if(!e){ e=document.createElement('meta'); e.setAttribute(attr,val); head.appendChild(e); } e.setAttribute('content',content); }
      var canon=head.querySelector('link[rel="canonical"]'); if(!canon){ canon=document.createElement('link'); canon.rel='canonical'; head.appendChild(canon); }
      canon.href='https://chibispo.com/club.html?id='+encodeURIComponent(t.id);
      meta('meta[name="description"]','name','description',desc);
      meta('meta[property="og:title"]','property','og:title',esc(t.name)+'｜チビスポ');
      meta('meta[property="og:description"]','property','og:description',desc);
      meta('meta[property="og:url"]','property','og:url',canon.href);
      if(t.photo_url) meta('meta[property="og:image"]','property','og:image',t.photo_url);
      var ld={'@context':'https://schema.org','@type':'SportsActivityLocation',name:t.name,url:canon.href,description:desc,address:{'@type':'PostalAddress',addressCountry:'JP',addressRegion:t.pref||undefined,addressLocality:t.city||undefined,streetAddress:(t.address1||t.address)||undefined}};
      if(t.photo_url) ld.image=t.photo_url; if(t.website_url) ld.sameAs=[t.website_url];
      if(t.fee_num!=null) ld.priceRange=Number(t.fee_num)===0?'無料':yen(t.fee_num)+'〜/月';
      var sc=document.createElement('script'); sc.type='application/ld+json'; sc.textContent=JSON.stringify(ld); head.appendChild(sc);
    })();

    /* ---- ヒーロー（動画があれば動画、なければ写真） ---- */
    var photos=(Array.isArray(t.photos)&&t.photos.length)?t.photos.slice():(t.photo_url?[t.photo_url]:[]);
    var limit=paid?7:1; photos=photos.slice(0,limit);
    var positions=Array.isArray(t.photo_positions)?t.photo_positions:[];
    function posOf(i){ return positions[i]||'50% 50%'; }
    var hero=el('cd-hero');
    function ytId(u){ var m=String(u||'').match(/(?:youtu\.be\/|v=|shorts\/|embed\/)([A-Za-z0-9_-]{6,})/); return m?m[1]:null; }
    var yt=ytId(t.video_url);
    if(hero){
      if(yt) hero.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+yt+'?rel=0&modestbranding=1" title="クラブ紹介動画" loading="lazy" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
      else if(photos.length) hero.innerHTML='<img id="cd-main-photo" src="'+esc(photos[0])+'" alt="'+esc(t.name)+'" style="object-position:'+esc(posOf(0))+'" fetchpriority="high">';
      else hero.innerHTML=ChibiCard.sportPlaceholder(t.sport,'aspect-ratio:16/9;',96);
    }
    /* ---- 見出し ---- */
    setText('cd-name',t.name); setText('cd-bc-name',t.name); setText('cd-sticky-name',t.name);
    var stSub=el('cd-sticky-sub'); if(stSub) stSub.textContent=t.trial?('体験'+(t.trial_fee?'は'+t.trial_fee:'は無料')+'・受付中'):'見学・体験は要相談';
    setText('cd-sport',t.sport||'');
    var si=el('cd-sport-icon'); if(si&&t.sport) si.outerHTML=ChibiCard.badge(t.sport);
    var logo=el('cd-logo'); if(logo){ if(t.logo_url) logo.innerHTML='<img src="'+esc(t.logo_url)+'" alt="" style="object-position:'+esc(t.logo_position||'50% 50%')+'">'; else logo.textContent=(t.name||'ク').charAt(0); }
    setText('cd-area',area);
    var mw=el('cd-map-link-wrap'), ml=el('cd-map-link'); var q=addrFull||area;
    if(mw&&ml&&q){ ml.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(q); mw.hidden=false; }
    (function(){ var prefS=String(t.pref||'').replace(/[都道府県]$/,''); var bp=el('cd-bc-pref'),bc=el('cd-bc-city'),s2=el('cd-bc-sep2');
      if(bp){ if(t.pref){ bp.textContent=t.pref; bp.href='/search.html?pref='+encodeURIComponent(prefS); } else bp.hidden=true; }
      if(bc){ if(t.city){ bc.textContent=t.city; bc.href='/search.html?pref='+encodeURIComponent(prefS)+'&city='+encodeURIComponent(t.city); } else { bc.hidden=true; if(s2) s2.hidden=true; } }
      var nm=el('cd-near-more'); if(nm&&t.pref) nm.href='/search.html?pref='+encodeURIComponent(prefS)+(t.city?'&city='+encodeURIComponent(t.city):'');
    })();
    /* ---- 編集部の一言（有料・登録があるときだけ） ---- */
    if(paid&&t.editor_headline){ setText('cd-epick-h',t.editor_headline); setText('cd-epick-p',t.editor_note||''); el('cd-epick').hidden=false; }
    /* ---- 基本情報 ---- */
    (function(){
      var rows=[];
      function row(dt,dd,small){ rows.push('<div><dt>'+dt+'</dt><dd>'+dd+(small?'<small>'+small+'</small>':'')+'</dd></div>'); }
      if(t.fee_num!=null){ row('月謝',Number(t.fee_num)===0?'無料':Number(t.fee_num).toLocaleString('ja-JP'),Number(t.fee_num)===0?'':'円'); }
      else if(t.fee){ row('月謝',esc(t.fee)); }
      if(t.admission_fee_num!=null){ row('入会金',Number(t.admission_fee_num)===0?'なし':Number(t.admission_fee_num).toLocaleString('ja-JP'),Number(t.admission_fee_num)===0?'':'円'); }
      var days=Array.isArray(t.days)?t.days.filter(Boolean):[];
      if(days.length) row('活動曜日',esc(days.join('・')),'週'+days.length);
      var ageMin=String(t.age_min||'').replace(/[〜～~ー\-\s]+$/,''); var groups=(t.age_groups||[]).slice(); var ages='';
      if(ageMin){ var pi=groups.indexOf('未就学'); if(pi>=0){ groups[pi]='未就学（'+ageMin+'〜）'; ages=groups.join('・'); } else ages=groups.length?(groups.join('・')+'（'+ageMin+'〜）'):(ageMin+'〜'); } else ages=groups.join('・');
      if(ages) row('対象年齢',esc(ages));
      if(t.trial!=null) row('体験',t.trial?'受付中':'要相談',t.trial?esc(t.trial_fee||'無料'):'');
      if(t.member_count) row('在籍',Number(t.member_count).toLocaleString('ja-JP'),'人');
      var sp=el('cd-spec'); if(sp){ sp.innerHTML=rows.join(''); if(!rows.length) sp.hidden=true; }
    })();
    /* ---- スタイル（5段階） ---- */
    (function(){ var s=t.style; if(!s||typeof s!=='object') return; var L=[['strict','きびしい','のびのび'],['win','勝ち重視','楽しさ重視'],['select','実力で選ぶ','全員が出る'],['practice','練習が多い','少ない'],['gender','男の子が多い','女の子が多い']];
      var html=L.filter(function(r){ return s[r[0]]>=1&&s[r[0]]<=5; }).map(function(r){ return '<div class="r"><span>'+r[1]+'</span><div class="bar"><i style="left:'+((s[r[0]]-1)*25)+'%"></i></div><span>'+r[2]+'</span></div>'; }).join('');
      if(html){ el('cd-style-scale').innerHTML=html; el('cd-style').hidden=false; }
    })();
    /* ---- タグ（雰囲気＋事実） ---- */
    (function(){ var tags=[]; var days=t.days||[];
      (Array.isArray(t.moods)?t.moods:[]).forEach(function(m){ if(m) tags.push('<span class="ctag mood" data-mood="'+esc(m)+'">'+esc(m)+'</span>'); });
      if(t.trial) tags.push('<span class="ctag">体験OK</span>');
      if(days.indexOf('土')>=0||days.indexOf('日')>=0) tags.push('<span class="ctag">土日開催</span>');
      if(['月','火','水','木','金'].some(function(d){return days.indexOf(d)>=0;})) tags.push('<span class="ctag">平日開催</span>');
      if(t.girls_welcome) tags.push('<span class="ctag">女の子歓迎</span>');
      if(t.female_instructor) tags.push('<span class="ctag">女性指導者あり</span>');
      if((t.age_groups||[]).indexOf('未就学')>=0) tags.push('<span class="ctag">未就学から</span>');
      var w=el('cd-tags'); if(w){ w.innerHTML=tags.join(''); if(!tags.length) w.hidden=true; }
    })();
    /* ---- 写真（2枚以上のとき） ---- */
    if(photos.length>1){ el('cd-photo-rail').innerHTML=photos.map(function(p,i){ return '<div class="card card-m" data-i="'+i+'"><div class="card-v"><img src="'+esc(p)+'" alt="" loading="lazy" style="object-position:'+esc(posOf(i))+'"></div></div>'; }).join(''); el('cd-photos').hidden=false;
      el('cd-photo-rail').addEventListener('click',function(e){ var c=e.target.closest('.card'); if(!c) return; var m=el('cd-main-photo'); if(m){ m.src=photos[+c.dataset.i]; m.style.objectPosition=posOf(+c.dataset.i); window.scrollTo({top:0,behavior:'smooth'}); } }); }
    /* ---- 紹介文・おすすめ ---- */
    if(t.description&&String(t.description).trim()){ el('cd-desc').textContent=String(t.description).replace(/\*\*/g,''); el('cd-desc-blk').hidden=false; }
    var pts=(Array.isArray(t.points)?t.points.filter(Boolean):[]); if(pts.length){ el('cd-points-list').innerHTML=pts.map(function(p){ return '<li>'+esc(p)+'</li>'; }).join(''); el('cd-points').hidden=false; }
    var rec=(Array.isArray(t.recommended_for)?t.recommended_for.filter(Boolean):[]); if(rec.length){ el('cd-recommend-list').innerHTML=rec.map(function(p){ return '<li>'+esc(p)+'</li>'; }).join(''); el('cd-recommend').hidden=false; }
    if(!pts.length||!rec.length){ var g=el('cd-grid-rr'); if(g) g.style.gridTemplateColumns='1fr'; }
    /* ---- コーチ・スタッフ ---- */
    (function(){ var st=Array.isArray(t.staff)?t.staff.filter(function(s){ return s&&s.name; }):[]; if(!st.length) return;
      el('cd-staff-list').innerHTML=st.slice(0,4).map(function(s){ return '<div class="s">'+(s.photo_url?'<img src="'+esc(s.photo_url)+'" alt="" loading="lazy">':'')+'<div><div class="n">'+esc(s.name)+'</div>'+(s.role?'<div class="rl">'+esc(s.role)+'</div>':'')+(s.comment?'<p>'+esc(s.comment)+'</p>':'')+'</div></div>'; }).join(''); el('cd-staff').hidden=false; })();
    /* ---- コース ---- */
    (function(){ var cs=Array.isArray(t.courses)?t.courses:[]; if(!cs.length) return;
      el('cd-course-body').innerHTML=cs.map(function(c){ var dt=esc(c.day)+(c.time?' '+esc(c.time):''); var raw=String(c.fee==null?'':c.fee).trim(); var f=(raw!==''&&/^[\d,]+$/.test(raw))?yen(raw.replace(/,/g,'')):esc(c.fee); return '<tr><td><b>'+esc(c.name)+'</b></td><td>'+esc(c.age)+'</td><td>'+dt+'</td><td>'+f+'</td></tr>'; }).join(''); el('cd-course').hidden=false; })();
    /* ---- 費用の内訳（月謝・入会金・登録された内訳） ---- */
    (function(){ var items=Array.isArray(t.cost_items)?t.cost_items.filter(function(x){ return x&&x.name; }):[]; if(!items.length&&t.admission_fee_num==null) return;
      var rows=[]; if(t.fee_num!=null) rows.push(['月謝',Number(t.fee_num)===0?'無料':yen(t.fee_num),'']);
      if(t.admission_fee_num!=null) rows.push(['入会金',Number(t.admission_fee_num)===0?'なし':yen(t.admission_fee_num),'']);
      items.forEach(function(x){ rows.push([x.name,(x.amount!=null&&x.amount!=='')?(/^[\d,]+$/.test(String(x.amount))?yen(String(x.amount).replace(/,/g,'')):esc(x.amount)):'—',x.note||'']); });
      el('cd-fee-table').innerHTML=rows.map(function(r){ return '<tr><td>'+esc(r[0])+(r[2]?'<small>'+esc(r[2])+'</small>':'')+'</td><td>'+r[1]+'</td></tr>'; }).join(''); el('cd-fees').hidden=false; })();
    /* ---- 地図 ---- */
    (function(){ var qq=addrFull||area; var at=el('cd-map-addr-text'); if(at&&qq) at.textContent=qq;
      if(t.venue){ setText('cd-venue',t.venue); el('cd-venue-wrap').hidden=false; }
      var em=el('cd-map-embed'); if(em){ if(qq) em.innerHTML='<iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="地図" src="https://maps.google.com/maps?q='+encodeURIComponent(qq)+'&z=15&output=embed"></iframe>'; else em.textContent='住所が登録されていません'; }
      var gm=el('cd-map-gmap'); if(gm&&qq){ gm.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(qq); gm.hidden=false; } })();
    /* ---- 公式リンク ---- */
    (function(){ var l=[]; if(t.website_url) l.push('<a href="'+esc(t.website_url)+'" target="_blank" rel="noopener">公式サイト</a>'); if(t.instagram) l.push('<a href="https://instagram.com/'+esc(String(t.instagram).replace(/^@/,''))+'" target="_blank" rel="noopener">Instagram</a>'); if(t.line_url) l.push('<a href="'+esc(t.line_url)+'" target="_blank" rel="noopener">LINE</a>'); if(t.twitter) l.push('<a href="https://x.com/'+esc(String(t.twitter).replace(/^@/,''))+'" target="_blank" rel="noopener">X</a>');
      if(l.length){ el('cd-links').innerHTML=l.join(''); el('cd-links-blk').hidden=false; } })();
    veilOff();

    /* ---- 近くのクラブ（同じ都道府県・同じ市区町村を優先） ---- */
    if(t.pref){ db.from('teams').select('id,name,sport,pref,city,description,photo_url,photo_positions,age_groups,days,fee,fee_num,trial,girls_welcome,female_instructor,moods,plan,plan_expires_at,created_at,video_url').eq('status','approved').eq('pref',t.pref).then(function(r2){
      var others=((r2&&r2.data)||[]).filter(function(o){ return o.id!==t.id; });
      var pr=function(o){ return (window.ChibiPlan&&ChibiPlan.rank)?ChibiPlan.rank(o):0; };
      var sorted=others.slice().sort(function(a,b){ return (b.city===t.city?1:0)-(a.city===t.city?1:0) || pr(b)-pr(a); });
      if(sorted.length){ el('cd-club').innerHTML=sorted.slice(0,4).map(function(o){ return ChibiCard.card(o); }).join(''); el('cd-near-sec').hidden=false; }
    }); }
    /* ---- 地域のおすすめ企業 ---- */
    db.from('companies').select('*').eq('status','active').then(function(rc){
      if(rc.error||!rc.data||!rc.data.length) return; var now=new Date();
      var comps=rc.data.filter(function(c){ if(c.plan_expires_at&&new Date(c.plan_expires_at)<now) return false; return c.online||(c.pref&&c.pref===t.pref); });
      comps.sort(function(a,b){ return (a.online?1:0)-(b.online?1:0) || (b.city===t.city?1:0)-(a.city===t.city?1:0) || ((a.sort_order||0)-(b.sort_order||0)); });
      if(!comps.length) return;
      el('cd-companies').innerHTML=comps.slice(0,4).map(function(c){ var ini=(c.name||'?').charAt(0); var loc=c.online?'オンラインショップ':esc(c.city||c.pref||''); return '<a class="a" href="'+esc(c.page_url||'#')+'">'+(c.banner_url?'<img class="lg" src="'+esc(c.banner_url)+'" alt="" style="object-fit:cover">':'<div class="lg">'+esc(ini)+'</div>')+'<div class="t">'+esc(c.name)+'<small>'+esc(c.tagline||c.category||'')+(loc?' ・ '+loc:'')+'</small></div></a>'; }).join(''); el('cd-comp-sec').hidden=false;
    });
    /* ---- いいね数 ---- */
    db.from('likes').select('team_id').eq('team_id',id).then(function(r){ if(!r.error&&r.data){ var n=el('cd-like-n'); if(n) n.textContent=r.data.length; } });
  });

  /* ===== 体験申込み（trial_requests。旧ページの方式をそのまま） ===== */
  (function(){
    var TEAM_ID=id, exp='';
    var openBtns=[el('cd-trial-open'),el('cd-trial-open-top'),el('cd-trial-open-sticky')].filter(Boolean);
    if(!el('cd-trial-modal')||!openBtns.length) return;
    function show(o){ modal('cd-trial-modal',o); if(o){ el('cd-trial-form').style.display='block'; el('cd-trial-done').style.display='none'; } }
    function loadMe(){ var A=window.ChibiAuth; if(!A||!A.ready()) return Promise.resolve(null); var d=A.client(); if(!d) return Promise.resolve(null);
      return d.auth.getSession().then(function(r){ var ses=r&&r.data&&r.data.session; if(!ses) return null; window._cdMyToken=ses.access_token; window._cdMyUid=ses.user&&ses.user.id; window._cdMyEmail=ses.user&&ses.user.email; return ses; }).catch(function(){ return null; }); }
    openBtns.forEach(function(btn){ btn.addEventListener('click',function(e){ e.preventDefault();
      var tm=window._cdTeam||{}; el('cd-trial-team').textContent=tm.name?tm.name+' への体験申込みです。':'';
      loadMe().then(function(ses){ if(!ses){ alert('体験申込にはログインが必要です。クラブとのやり取りをお届けするために、会員登録（無料）をお願いします。'); location.href='/login.html?next='+encodeURIComponent(location.pathname+location.search); return; } var w=el('tr-email-wrap'); if(w) w.style.display='none'; show(true); });
    }); });
    el('cd-trial-close').addEventListener('click',function(){ show(false); });
    el('cd-trial-done-close').addEventListener('click',function(){ show(false); });
    el('cd-trial-modal').addEventListener('click',function(e){ if(e.target===el('cd-trial-modal')) show(false); });
    document.querySelectorAll('.tr-exp-opt').forEach(function(b){ b.addEventListener('click',function(){ exp=b.dataset.v; document.querySelectorAll('.tr-exp-opt').forEach(function(x){ x.classList.toggle('on',x===b); }); }); });
    /* 質問だけ（trial_requests type='question'） */
    (function(){ var am=el('cd-ask-modal'), ab=el('cd-ask-open'); if(!am||!ab) return;
      var QUICK=['見学はできますか？','何歳から入れますか？','体験の持ち物を知りたいです','月謝以外に費用はかかりますか？'];
      var qw=el('cd-ask-quick'); qw.innerHTML=QUICK.map(function(q){ return '<button type="button" data-q="'+q+'">'+q+'</button>'; }).join('');
      qw.querySelectorAll('[data-q]').forEach(function(b){ b.addEventListener('click',function(){ var ta=el('cd-ask-body'); var v=b.getAttribute('data-q'); ta.value=ta.value?(ta.value+'\n'+v):v; }); });
      function showAsk(o){ modal('cd-ask-modal',o); if(o){ el('cd-ask-form').style.display='block'; el('cd-ask-done').style.display='none'; } }
      ab.addEventListener('click',function(e){ e.preventDefault(); loadMe().then(function(ses){ if(!ses){ alert('質問にはログインが必要です。クラブからの返信をお届けするために、会員登録（無料）をお願いします。'); location.href='/login.html?next='+encodeURIComponent(location.pathname+location.search); return; } showAsk(true); }); });
      el('cd-ask-close').addEventListener('click',function(){ showAsk(false); });
      am.addEventListener('click',function(e){ if(e.target===am) showAsk(false); });
      el('cd-ask-send').addEventListener('click',function(){
        var body=el('cd-ask-body').value.trim(); var errEl=el('cd-ask-err'); errEl.style.display='none';
        if(!body){ errEl.style.display='block'; errEl.textContent='質問内容を入力してください。'; return; }
        var btn=el('cd-ask-send'); btn.disabled=true; btn.textContent='送信中...';
        var tok=window._cdMyToken, uid=window._cdMyUid, mail=window._cdMyEmail;
        fetch(SB+'/rest/v1/trial_requests?select=id',{method:'POST',headers:{apikey:ANON,Authorization:'Bearer '+tok,'Content-Type':'application/json',Prefer:'return=representation'},body:JSON.stringify({team_id:TEAM_ID,type:'question',parent_name:'保護者',parent_email:mail,user_id:uid,message:body})})
        .then(function(r){ btn.disabled=false; btn.textContent='質問を送る'; if(!r.ok){ errEl.style.display='block'; errEl.textContent='送信に失敗しました。時間をおいてお試しください。'; return; }
          return r.json().then(function(rows){ var tid=(rows&&rows[0]&&rows[0].id)||null; el('cd-ask-form').style.display='none'; el('cd-ask-done').style.display='block';
            if(tid) fetch(SB+'/rest/v1/trial_messages',{method:'POST',headers:{apikey:ANON,Authorization:'Bearer '+tok,'Content-Type':'application/json',Prefer:'return=minimal'},body:JSON.stringify({trial_id:tid,sender_role:'parent',sender_id:uid,body:body})}).catch(function(){});
            var tm=window._cdTeam||{};
            fetch(SB+'/functions/v1/send-trial-notify',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ANON},body:JSON.stringify({type:'question',team_id:TEAM_ID,team_name:tm.name||'',team_email:null,sport:tm.sport||'',pref:tm.pref||'',city:tm.city||'',parent_name:'保護者',parent_email:mail,message:body})}).catch(function(){});
          });
        }).catch(function(){ btn.disabled=false; btn.textContent='質問を送る'; errEl.style.display='block'; errEl.textContent='通信エラーが発生しました。'; });
      });
    })();
    el('tr-submit').addEventListener('click',function(){
      var err=el('tr-err'); function fail(t){ err.style.display='block'; err.textContent=t; } err.style.display='none';
      var grade=el('tr-grade').value, name=el('tr-name').value.trim(), child=el('tr-child').value.trim(), kana=el('tr-kana').value.trim();
      var email=(window._cdMyEmail||el('tr-email').value.trim());
      if(!child) return fail('お子さまのお名前を入力してください。'); if(!grade) return fail('お子さまの学年を選択してください。'); if(!name) return fail('保護者のお名前を入力してください。');
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return fail('メールアドレスの形式が正しくありません。');
      var childLabel=kana?(child+'（'+kana+'）'):child; var btn=el('tr-submit'); btn.disabled=true; btn.textContent='送信中...';
      var myTok=window._cdMyToken||null, wantRow=!!myTok;
      fetch(SB+'/rest/v1/trial_requests'+(wantRow?'?select=id':''),{method:'POST',headers:{apikey:ANON,Authorization:'Bearer '+(myTok||ANON),'Content-Type':'application/json',Prefer:wantRow?'return=representation':'return=minimal'},
        body:JSON.stringify({team_id:TEAM_ID,child_name:childLabel,child_grade:grade,experience_level:exp||null,preferred_date_1:el('tr-date1').value.trim()||null,preferred_date_2:el('tr-date2').value.trim()||null,parent_name:name,parent_email:email,user_id:window._cdMyUid||null,message:el('tr-msg').value.trim()||null})
      }).then(function(r){ btn.disabled=false; btn.textContent='この内容で申し込む';
        if(!r.ok){ fail('送信に失敗しました。時間をおいて再度お試しください。'); return; }
        el('cd-trial-form').style.display='none'; el('cd-trial-done').style.display='block';
        if(myTok){ el('cd-trial-chat').style.display='inline-block'; el('cd-trial-done-msg').textContent='このままクラブとメッセージでやり取りできます。'; }
        else { el('cd-trial-signup').style.display='inline-block'; el('cd-trial-done-msg').innerHTML='クラブから連絡が届くまでお待ちください。<br>会員登録すると、メールを使わずこの画面上でやり取りできます。'; }
        if(wantRow){ r.json().then(function(rows){ var tid=(rows&&rows[0]&&rows[0].id)||null; if(!tid) return; var lines=['体験を申し込みました。','お子さま：'+childLabel+'（'+grade+'）']; if(el('tr-date1').value.trim()) lines.push('希望日：'+el('tr-date1').value.trim()); if(el('tr-msg').value.trim()) lines.push('\n'+el('tr-msg').value.trim());
          fetch(SB+'/rest/v1/trial_messages',{method:'POST',headers:{apikey:ANON,Authorization:'Bearer '+myTok,'Content-Type':'application/json',Prefer:'return=minimal'},body:JSON.stringify({trial_id:tid,sender_role:'parent',sender_id:window._cdMyUid,body:lines.join('\n')})}).catch(function(){}); }).catch(function(){}); }
        try{ var tm=window._cdTeam||{};
          fetch(SB+'/functions/v1/send-trial-notify',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+ANON},body:JSON.stringify({type:'trial',team_name:tm.name||'',team_email:null,team_instagram:tm.instagram||null,sport:tm.sport||'',pref:tm.pref||'',city:tm.city||'',parent_name:name,parent_email:email,team_id:TEAM_ID,child_name:childLabel,child_name_kana:kana||null,child_age:null,child_grade:grade,message:el('tr-msg').value.trim()||null})}).catch(function(err){ console.warn('通知メール送信失敗:',err); });
        }catch(_){}
      }).catch(function(){ btn.disabled=false; btn.textContent='この内容で申し込む'; fail('通信エラーが発生しました。時間をおいて再度お試しください。'); });
    });
  })();

  /* ===== 口コミ・コメント ===== */
  (function(){
    var A=window.ChibiAuth, TEAM_ID=id, myUserId=null, myNick='';
    function fmtDate(s){ try{ var d=new Date(s); return d.getFullYear()+'/'+(d.getMonth()+1)+'/'+d.getDate(); }catch(e){ return ''; } }
    function renderList(rows){
      var list=el('cd-cmt-list'), empty=el('cd-cmt-empty'); setText('cd-cmt-count',rows.length); setText('cd-cmt-n',rows.length);
      if(!rows.length){ list.innerHTML=''; empty.hidden=false; return; } empty.hidden=true;
      list.innerHTML=rows.map(function(c){ return '<div class="rev"><div class="top"><span class="av">'+esc((c.nickname||'匿').charAt(0))+'</span><span class="nm">'+esc(c.nickname||'匿名')+'</span><span class="dt">'+fmtDate(c.created_at)+'</span></div><p>'+esc(c.body)+'</p><div class="rep"><button class="cd-cmt-report" type="button" data-id="'+esc(c.id)+'">⚑ 通報</button></div></div>'; }).join('');
      list.querySelectorAll('.cd-cmt-report').forEach(function(b){ b.addEventListener('click',function(){ if(!confirm('このコメントを通報しますか？')) return; db.rpc('report_comment',{cid:b.getAttribute('data-id')}).then(function(){ b.textContent='通報しました'; b.disabled=true; }); }); });
    }
    function load(){ db.from('comments').select('*').eq('team_id',TEAM_ID).eq('status','visible').order('created_at',{ascending:false}).then(function(res){ if(res.error){ console.warn('[chibispo] comments load error',res.error); return; } renderList(res.data||[]); }); }
    function setupForm(){
      if(!A||!A.ready()){ el('cd-cmt-login').hidden=false; return; }
      A.getProfile().then(function(prof){
        if(!prof){ el('cd-cmt-login').hidden=false; return; }
        myUserId=prof.id; myNick=prof.display_name||(prof.email?prof.email.split('@')[0]:'ゲスト');
        el('cd-cmt-form').hidden=false; setText('cd-cmt-nick',myNick); setText('cd-cmt-avatar',myNick.charAt(0));
        el('cd-cmt-submit').addEventListener('click',function(){
          var body=el('cd-cmt-body').value.trim(), msg=el('cd-cmt-msg');
          if(!body){ msg.style.color='#b3232e'; msg.textContent='コメントを入力してください。'; return; }
          var ng=window.ChibiCommentGuard&&ChibiCommentGuard.check(body); if(ng){ msg.style.color='#b3232e'; msg.textContent=ng; return; }
          el('cd-cmt-submit').disabled=true;
          db.from('comments').insert({team_id:TEAM_ID,user_id:myUserId,nickname:myNick,body:body},{returning:'id,status'}).then(function(res){
            el('cd-cmt-submit').disabled=false;
            if(res.error){ msg.style.color='#b3232e'; msg.textContent='投稿に失敗しました。時間をおいて再度お試しください。'; return; }
            var ins=Array.isArray(res.data)?res.data[0]:res.data; el('cd-cmt-body').value='';
            if(ins&&ins.status==='hidden'){ msg.style.color='#b3232e'; msg.textContent='不適切な表現が含まれるため非表示になりました。'; }
            else { msg.style.color='#1f8a5b'; msg.textContent='投稿しました。'; }
            load();
          });
        });
      }).catch(function(){ el('cd-cmt-login').hidden=false; });
    }
    function boot(){ load(); setupForm(); if(location.hash==='#comments'){ setTimeout(function(){ var s=el('cd-comments'); if(s) s.scrollIntoView({behavior:'smooth',block:'start'}); },400); } }
    if(window.ChibiAuth){ boot(); } else { var w=setInterval(function(){ if(window.ChibiAuth){ clearInterval(w); A=window.ChibiAuth; boot(); } },100); }
  })();
})();
