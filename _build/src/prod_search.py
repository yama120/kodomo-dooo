# 検索結果 v2 本番（search.html）。地域ページ（/clubs/…）の雛形でもある（build-area-pages.mjs が読む）
#   目印：<!-- __CRUMBS__ -->（パンくず・紹介文の差し込み位置）／<h1 id="sr-h1">検索結果</h1>／.sr-cards／.sr-count／<b class="sr-n">／#sr-related
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
bp=open(P+'build_pages.py',encoding='utf-8').read()
search_css=C.strip_preview(bp[bp.index("search_css='''")+14:bp.index("'''",bp.index("search_css='''")+14)])
v2=C.strip_preview(open(P+'search_v2_css.css',encoding='utf-8').read())
v2=v2[:v2.index('/* プレビュー用の切替パネル')]+v2[v2.index('/* スマホ：種目名'):]   # #demo を落とす
css=search_css+v2+'''
/* ---- 本番の補い ---- */
#sr-veil{position:fixed;inset:0;background:var(--bg);z-index:50;display:flex;align-items:center;justify-content:center;transition:opacity .25s}
#sr-veil i{width:28px;height:28px;border:3px solid var(--line);border-top-color:var(--accent);border-radius:50%;animation:srspin .8s linear infinite}
@keyframes srspin{to{transform:rotate(360deg)}}
.s-head .bc{font-size:11.5px;font-weight:700;color:var(--sub);display:flex;gap:5px;flex-wrap:wrap;margin-bottom:12px}
.s-head .bc a{color:var(--sub)}
.s-lead{font-size:13px;font-weight:700;color:var(--sub);line-height:1.9;margin:10px 0 0}
.sr-count{display:none}
#sr-empty{margin:0 0 22px;border:1.5px dashed var(--line);padding:26px 18px;text-align:center;border-radius:var(--r)}
#sr-empty .t{font-family:var(--fh);font-size:17px;font-weight:900;margin-bottom:6px}
#sr-empty p{margin:0 0 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
#sr-empty .btn{font-size:13px;padding:11px 18px;margin:2px 4px;cursor:pointer;border:0}
#sr-empty[hidden],#sr-near-label[hidden],#sr-rec-sec[hidden],#sr-comp-sec[hidden],#sr-mood-wrap[hidden]{display:none}
.news.mag{counter-reset:c 0}
#sr-near-label{display:flex;flex-direction:column;gap:2px;margin:0 0 14px;padding-left:12px;border-left:3px solid var(--accent)}
#sr-near-label .t{font-family:var(--fh);font-weight:900;font-size:15px}
#sr-near-label .s{font-size:12px;font-weight:700;color:var(--sub)}
.sr-backdrop{position:fixed;inset:0;background:rgba(15,21,30,.45);z-index:45;opacity:0;pointer-events:none;transition:opacity .2s}
.sr-backdrop.on{opacity:1;pointer-events:auto}
@media(max-width:899px){
  .fside{position:fixed;left:0;right:0;bottom:0;z-index:46;max-height:86vh;overflow-y:auto;background:var(--card);border:1px solid var(--line);border-radius:var(--r) var(--r) 0 0;padding:16px 18px calc(24px + env(safe-area-inset-bottom));transform:translateY(110%);transition:transform .3s cubic-bezier(.32,.72,0,1);display:block}
  .fside.open{transform:none}
  .fside.mag{border-top:1px solid var(--line)}
  .fside .close{display:flex;justify-content:flex-end}
  .fside .close button{border:0;background:transparent;font-size:24px;line-height:1;color:var(--sub);cursor:pointer;padding:2px 6px}
}
@media(min-width:900px){.fside .close{display:none}}
.pager.mag a{cursor:pointer}
.pager.mag a.dis{opacity:.35;cursor:default}
.seo2{margin-top:10px}
.seo2 .row a{border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--ink)}
.seo2 .row a small{color:var(--sub);font-size:11px;margin-left:2px}
.mag-strip{display:grid;gap:12px;margin-top:8px}
.mag-strip a{display:grid;grid-template-columns:96px 1fr;gap:12px;align-items:center;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--card)}
.mag-strip img{width:96px;height:72px;object-fit:cover;display:block}
.mag-strip .t{font-family:var(--fh);font-size:13px;font-weight:900;line-height:1.5;padding-right:12px}
@media(min-width:760px){.mag-strip{grid-template-columns:repeat(2,1fr)}}
.ads .a{cursor:pointer}
'''
body='''<div id="sr-veil"><i></i></div>
<main>
<section class="sec s-head nobg" id="sr-head" data-bg="CLUBS">
  <div class="wrap">
    <!-- __CRUMBS__ -->
    <div class="eyebrow" id="sr-eyebrow">CLUBS</div>
    <div class="s-h1">
      <h1 id="sr-h1">検索結果</h1>
      <div class="s-cnt"><span><b class="sr-n">0</b><small>CLUBS</small></span></div>
    </div>
    <div class="sr-count" hidden>検索結果：<span>0</span> 件</div>
    <div class="s-tools">
      <button class="ftog" type="button" id="sr-filter-open"><svg viewBox="0 0 24 24"><path d="M3 5h18M6 12h12M10 19h4"/></svg>条件検索</button>
      <span class="sp"></span>
      <span class="vsw"><a class="on" href="search.html">一覧</a><a id="sr-mapbtn" href="map.html">地図</a></span>
    </div>
  </div>
</section>
<div class="sr-backdrop" id="sr-backdrop"></div>
<div class="wrap">
  <div class="slay">
  <aside class="fside mag" id="fside">
    <div class="close"><button type="button" id="sr-side-close-btn" aria-label="閉じる">&times;</button></div>
    <div class="eyebrow">FILTER</div>
    <div class="ttl">条件検索</div>
    <div class="lb">フリーワード</div><input id="sr-kw" type="text" placeholder="例）クラブ名、種目、市区町村">
    <div class="lb">地域</div><select id="sr-pref"><option value="">都道府県を選択</option></select><select id="sr-city" disabled><option value="">市区町村を選択</option></select>
    <div class="lb">種目（カテゴリ）</div><select id="sr-sport"><option value="">すべての種目</option></select>
    <div class="lb">対象年齢</div><div class="ages"><span class="sr-age" data-age="未就学">未就学</span><span class="sr-age" data-age="小学生">小学生</span><span class="sr-age" data-age="中学生">中学生</span></div>
    <div id="sr-mood-wrap" hidden><div class="lb">雰囲気</div><div id="sr-mood-list"></div></div>
    <div class="lb">こだわり条件</div>
    <label class="sr-chk" data-k="trial"><i></i>体験OK</label><label class="sr-chk" data-k="heijitsu"><i></i>平日開催</label><label class="sr-chk" data-k="doyo"><i></i>土日開催</label><label class="sr-chk" data-k="girls"><i></i>女の子歓迎</label>
    <div class="lb">月謝</div>
    <label class="sr-fee" data-v="3"><i class="r"></i>〜3,000円</label><label class="sr-fee" data-v="5"><i class="r"></i>〜5,000円</label><label class="sr-fee" data-v="8"><i class="r"></i>〜8,000円</label><label class="sr-fee" data-v="10"><i class="r"></i>〜10,000円</label><label class="sr-fee on" data-v="none"><i class="r on"></i>指定しない</label>
    <a class="apply" href="#" id="sr-apply">この条件で表示</a><a class="clear" href="#" id="sr-clear">条件をクリア</a>
  </aside>
  <div class="sres">
    <div id="sr-empty" hidden>
      <div class="t" id="sr-empty-title">条件に合うクラブが見つかりませんでした</div>
      <p id="sr-empty-cond"></p>
      <a class="btn" id="sr-empty-clear" href="/search.html">条件をクリアして探す</a>
      <button class="btn ghost" id="sr-empty-region" type="button">地域を変える</button>
    </div>
    <div id="sr-near-label" hidden><span class="t" id="sr-near-title">条件に近いクラブ</span><span class="s" id="sr-near-sub">条件を一部ゆるめて表示しています</span></div>
    <div class="news mag sr-cards">
    </div>
    <div class="pager mag" id="sr-pagination"></div>
  </div>
  </div>
</div>
<section class="sec sec-alt pr" id="sr-rec-sec" hidden>
  <div class="wrap">
    <div class="eyebrow">PICK UP</div>
    <div class="sec-h"><h2>おすすめ<em>クラブ</em><span class="pr-lb">PR</span></h2><span class="more">いま募集しているクラブ</span></div>
    <div class="rec" id="sr-rec"></div>
  </div>
</section>
<section class="sec pr" id="sr-comp-sec" hidden>
  <div class="wrap">
    <div class="eyebrow">LOCAL PARTNERS</div>
    <div class="sec-h"><h2>地域の<em>おすすめ</em>企業<span class="pr-lb">PR</span></h2><span class="more">子育て世帯に向けて</span></div>
    <div class="ads" id="sr-companies"></div>
    <div class="ads-more">この枠に掲載する事業者の方は <a href="service-ads.html">掲載のご案内</a> へ。</div>
  </div>
</section>
<section class="sec pr">
  <div class="wrap">
    <div class="eyebrow">MAGAZINE</div>
    <div class="sec-h"><h2>はじめての<em>クラブ選び</em>に</h2><a class="more" href="magazine.html">マガジンをすべて見る ›</a></div>
    <div class="mag-strip">
      <a href="magazine-4.html"><img src="assets/mag-4.jpg" alt="" loading="lazy"><div class="t">「うちの子に合うクラブ」の見つけ方・5つの視点</div></a>
      <a href="magazine-3.html"><img src="assets/mag-3.jpg" alt="" loading="lazy"><div class="t">運動が苦手な子でも、楽しく続く習い事の見つけ方</div></a>
      <a href="magazine-2.html"><img src="assets/mag-2.jpg" alt="" loading="lazy"><div class="t">年齢別・おすすめの運動と「やりすぎ注意」な運動</div></a>
      <a href="magazine-1.html"><img src="assets/mag-1.jpg" alt="" loading="lazy"><div class="t">6歳までの運動が、脳を育てる。幼児期に大切にしたい「多様な動き」</div></a>
    </div>
  </div>
</section>
<div class="wrap">
  <div id="sr-related"></div>
  <div style="height:40px"></div>
</div>
</main>'''
js=r'''<script>
(function(){
  function veilOff(){ var v=document.getElementById('sr-veil'); if(!v) return; v.style.opacity='0'; setTimeout(function(){ v.remove(); },260); }
  window._srVeilOff=veilOff; setTimeout(veilOff,4000);
  /* 条件検索のドロワー（タブレット以下） */
  var side=document.getElementById('fside'), bd=document.getElementById('sr-backdrop');
  function drawer(o){ if(side) side.classList.toggle('open',o); if(bd) bd.classList.toggle('on',o); }
  var ob=document.getElementById('sr-filter-open'), cb=document.getElementById('sr-side-close-btn'), ap=document.getElementById('sr-apply');
  if(ob) ob.addEventListener('click',function(){ drawer(true); });
  if(bd) bd.addEventListener('click',function(){ drawer(false); });
  if(cb) cb.addEventListener('click',function(){ drawer(false); });
  if(ap) ap.addEventListener('click',function(e){ e.preventDefault(); drawer(false); });

  if(!window.supabase){ veilOff(); return; }
  var SUPABASE_URL='https://emkpkomrgknzrmxqbrvx.supabase.co';
  var SUPABASE_KEY='__ANON__';
  var db=supabase.createClient(SUPABASE_URL,SUPABASE_KEY);
  var grid=document.querySelector('.sr-cards'); if(!grid) return;
  var esc=ChibiCard.esc, card=ChibiCard.card;

  // 💬クリックでそのクラブのコメント欄へ
  grid.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('.sr-cmt-btn'); if(!b) return;
    e.preventDefault(); e.stopPropagation();
    location.href = '/club.html?id=' + encodeURIComponent(b.getAttribute('data-id')) + '#comments';
  });

  var TEAM_COLS='id,name,sport,pref,city,address,age_groups,days,fee,fee_num,trial,girls_welcome,female_instructor,description,photo_url,photo_positions,moods,plan,plan_expires_at,created_at,video_url';
  /* 地域ページ（/clubs/…）は生成時に window.__AREA_INIT で地域が決まっているので最初からその地域ぶんだけ取る */
  var _area = window.__AREA_INIT || {};
  function teamsQuery(){
    var q = db.from('teams').select(TEAM_COLS).eq('status','approved');
    if(_area.prefFull) q = q.eq('pref', _area.prefFull);
    if(_area.city) q = q.eq('city', _area.city);
    return q.order('created_at',{ascending:false});
  }
  function stripPref(p){ return String(p||'').replace(/[都道府県]$/,''); }

  teamsQuery().then(function(res){
    if(res.error){ console.warn('[chibispo] teams読込エラー:', res.error); veilOff(); return; }
    var teams=(res.data||[]);
    var scoped = !!(_area.prefFull || _area.city), loadingAll=false;
    function outOfScope(){
      if(!scoped) return false;
      if(_area.city) return !st.city || st.city !== _area.city || (st.pref && stripPref(st.pref)!==stripPref(_area.pref||st.pref));
      return !st.pref || stripPref(st.pref) !== stripPref(_area.pref);
    }
    function loadAll(after){
      if(!scoped || loadingAll) return false;
      loadingAll = true;
      db.from('teams').select(TEAM_COLS).eq('status','approved').order('created_at',{ascending:false}).then(function(r2){
        loadingAll = false;
        if(r2.error || !r2.data){ return; }
        scoped = false; teams = r2.data;
        refreshCities(); refreshSports();
        if(typeof after === 'function') after();
      });
      return true;
    }
    if(!teams.length && !scoped){ veilOff(); return; }
    var WEEKDAYS=['月','火','水','木','金'];
    var _p=new URLSearchParams(location.search);
    var elKw=document.getElementById('sr-kw'), elPref=document.getElementById('sr-pref'), elCity=document.getElementById('sr-city'), elSport=document.getElementById('sr-sport');
    var countEl=document.querySelector('.sr-count span'), countBig=document.querySelector('.sr-n');
    var emptyEl=document.getElementById('sr-empty'), nearLabel=document.getElementById('sr-near-label');
    var st={ kw:'', pref:'', city:'', sport:'', ages:{}, moods:{}, chk:{}, fee:'none' };

    function uniqSorted(arr){ var s={}; arr.forEach(function(v){ if(v) s[v]=1; }); return Object.keys(s).sort(function(a,b){return a.localeCompare(b,'ja');}); }
    function fillSelect(sel, vals, placeholder){
      if(!sel) return; var cur=sel.value;
      sel.innerHTML='<option value="">'+placeholder+'</option>'+vals.map(function(v){return '<option value="'+v.replace(/"/g,'')+'">'+v+'</option>';}).join('');
      sel.value=cur;
    }
    var hasCities = (typeof CITIES!=='undefined');
    var prefList = hasCities ? Object.keys(CITIES) : uniqSorted(teams.map(function(t){return t.pref;}));
    fillSelect(elPref, prefList, '都道府県を選択');
    function refreshSports(){
      if(!elSport) return;
      var inArea = teams.filter(function(t){
        if(st.pref && stripPref(t.pref)!==stripPref(st.pref)) return false;
        if(st.city && t.city!==st.city) return false;
        return true;
      });
      var count={}; inArea.forEach(function(t){ if(t.sport) count[t.sport]=(count[t.sport]||0)+1; });
      var names=Object.keys(count).sort(function(a,b){return a.localeCompare(b,'ja');});
      if(st.sport && names.indexOf(st.sport)<0) names.push(st.sport);
      var cur=st.sport;
      elSport.innerHTML='<option value="">すべての種目</option>'+names.map(function(v){ return '<option value="'+v.replace(/"/g,'')+'">'+v+'（'+(count[v]||0)+'）</option>'; }).join('');
      elSport.value=cur;
    }
    refreshSports();
    function refreshCities(){
      if(!elCity) return;
      if(!st.pref){ elCity.innerHTML='<option value="">市区町村を選択</option>'; elCity.disabled=true; st.city=''; return; }
      var base = hasCities ? (CITIES[st.pref]||[]).slice() : [];
      var teamCities = teams.filter(function(t){return stripPref(t.pref)===stripPref(st.pref);}).map(function(t){return t.city;}).filter(Boolean);
      var seen={}, cities=[];
      base.concat(teamCities).forEach(function(c){ if(c && !seen[c]){ seen[c]=1; cities.push(c); } });
      fillSelect(elCity, cities, '市区町村を選択'); elCity.disabled=false;
    }
    /* 雰囲気タグ：実データに moods があるときだけ出す */
    (function(){
      var all={}; teams.forEach(function(t){ (t.moods||[]).forEach(function(m){ if(m) all[m]=1; }); });
      var names=Object.keys(all); var wrap=document.getElementById('sr-mood-wrap'), list=document.getElementById('sr-mood-list');
      if(!names.length || !wrap || !list) return;
      list.innerHTML=names.map(function(m){ return '<span class="chip sr-mood" data-mood="'+esc(m)+'">'+esc(m)+'</span>'; }).join('');
      wrap.hidden=false;
    })();

    function matchTeam(t){
      if(st.kw){ var hay=[t.name,t.sport,t.pref,t.city,t.address].join(' ').toLowerCase(); if(hay.indexOf(st.kw.toLowerCase())<0) return false; }
      if(st.pref && stripPref(t.pref)!==stripPref(st.pref)) return false;
      if(st.city && t.city!==st.city) return false;
      if(st.sport && t.sport!==st.sport) return false;
      var ages=Object.keys(st.ages).filter(function(k){return st.ages[k];});
      if(ages.length){ var ag=t.age_groups||[]; if(!ages.some(function(a){return ag.indexOf(a)>=0;})) return false; }
      var moods=Object.keys(st.moods).filter(function(k){return st.moods[k];});
      if(moods.length){ var tm=t.moods||[]; if(!moods.some(function(m){return tm.indexOf(m)>=0;})) return false; }
      if(st.chk.trial && !t.trial) return false;
      if(st.chk.girls && !t.girls_welcome) return false;
      var days=t.days||[];
      if(st.chk.heijitsu && !days.some(function(d){return WEEKDAYS.indexOf(d)>=0;})) return false;
      if(st.chk.doyo && !(days.indexOf('土')>=0||days.indexOf('日')>=0)) return false;
      if(st.fee!=='none'){ var lim=Number(st.fee)*1000; if(!(t.fee_num!=null && Number(t.fee_num)<=lim)) return false; }
      return true;
    }
    function planSort(list){ return (window.ChibiPlan && window.ChibiPlan.sort) ? window.ChibiPlan.sort(list) : list; }
    var PER_PAGE=12, curPage=1, curList=[];
    var pagEl=document.getElementById('sr-pagination');
    function renderPage(){
      var total=curList.length, pages=Math.max(1,Math.ceil(total/PER_PAGE));
      if(curPage>pages) curPage=pages;
      var start=(curPage-1)*PER_PAGE;
      grid.innerHTML=curList.slice(start,start+PER_PAGE).map(function(t){ return card(t); }).join('');
      var sec=document.querySelector('.sres'); if(sec && curPage>1){ sec.scrollIntoView({behavior:'smooth',block:'start'}); }
      renderPagination(pages);
    }
    function pageBtn(label,page,opts){
      opts=opts||{};
      var el=document.createElement('a'); el.textContent=label;
      if(opts.active) el.className='on'; else if(opts.disabled) el.className='dis';
      if(!opts.active && !opts.disabled && page){ el.href='#'; el.addEventListener('click',function(e){ e.preventDefault(); curPage=page; renderPage(); }); }
      return el;
    }
    function renderPagination(pages){
      if(!pagEl) return; pagEl.innerHTML='';
      if(pages<=1) return;
      pagEl.appendChild(pageBtn('‹ PREV', curPage-1, {disabled:curPage<=1}));
      var nums=[];
      for(var p=1;p<=pages;p++){ if(p===1||p===pages||(p>=curPage-1&&p<=curPage+1)) nums.push(p); else if(nums[nums.length-1]!=='…') nums.push('…'); }
      nums.forEach(function(n){ if(n==='…'){ var d=document.createElement('span'); d.textContent='…'; pagEl.appendChild(d); } else { pagEl.appendChild(pageBtn((n<10?'0':'')+n, n, {active:n===curPage})); } });
      pagEl.appendChild(pageBtn('NEXT ›', curPage+1, {disabled:curPage>=pages}));
    }
    var mapBtn=document.getElementById('sr-mapbtn');
    function updateMapLink(){
      if(!mapBtn) return;
      var q=[];
      if(st.kw) q.push('kw='+encodeURIComponent(st.kw));
      if(st.pref) q.push('pref='+encodeURIComponent(st.pref));
      if(st.city) q.push('city='+encodeURIComponent(st.city));
      if(st.sport) q.push('sport='+encodeURIComponent(st.sport));
      var ages=Object.keys(st.ages).filter(function(k){return st.ages[k];});
      if(ages.length) q.push('ages='+encodeURIComponent(ages.join(',')));
      if(st.chk.trial) q.push('trial=1'); if(st.chk.girls) q.push('girls=1'); if(st.chk.heijitsu) q.push('heijitsu=1'); if(st.chk.doyo) q.push('doyo=1');
      if(st.fee && st.fee!=='none') q.push('fee='+encodeURIComponent(st.fee));
      mapBtn.href = '/map.html'+(q.length?('?'+q.join('&')):'');
    }
    var urlSyncReady=false;
    function syncUrl(hits){
      if(!urlSyncReady) return;
      if(!window.history || !history.replaceState || !window.ChibiRomaji) return;
      var R=window.ChibiRomaji, path='/clubs/';
      try{
        if(hits>0 && st.pref){
          var pk=Object.keys(R.PREF).filter(function(k){return stripPref(k)===stripPref(st.pref);})[0];
          if(pk){ path+=R.PREF[pk]+'/'; if(st.city && R.CITY[st.city]) path+=R.CITY[st.city]+'/'; if(st.sport && R.SPORT[st.sport]) path+='sport/'+R.SPORT[st.sport]+'/'; }
        }
      }catch(e){ path='/clubs/'; }
      var q=[];
      if(path==='/clubs/'){
        if(st.pref) q.push('pref='+encodeURIComponent(st.pref));
        if(st.city) q.push('city='+encodeURIComponent(st.city));
        if(st.sport) q.push('sport='+encodeURIComponent(st.sport));
      } else if(st.sport && path.indexOf('/sport/')<0){ q.push('sport='+encodeURIComponent(st.sport)); }
      if(st.kw) q.push('kw='+encodeURIComponent(st.kw));
      ['trial','heijitsu','doyo','girls'].forEach(function(k){ if(st.chk[k]) q.push(k+'=1'); });
      var ages=Object.keys(st.ages).filter(function(k){return st.ages[k];});
      if(ages.length) q.push('age='+encodeURIComponent(ages.join(',')));
      if(st.fee && st.fee!=='none') q.push('fee='+st.fee);
      var url=path+(q.length?('?'+q.join('&')):'');
      if(url!==location.pathname+location.search) history.replaceState(null,'',url);
      var m=document.querySelector('meta[name="robots"]');
      if(q.length){ if(!m){ m=document.createElement('meta'); m.name='robots'; document.head.appendChild(m); } m.content='noindex,follow'; }
      else if(m && m.content.indexOf('noindex')>=0 && !window.__SEARCH_PAGE){ m.remove(); }
    }
    /* 見出し・件数・背景の英字（地域×種目）を、いまの条件に合わせる */
    var head=document.getElementById('sr-head'), h1=document.getElementById('sr-h1'), eb=document.getElementById('sr-eyebrow');
    function en(kind,jp){
      var R=window.ChibiRomaji||{}; var m=R[kind]||{}; var k=jp;
      if(kind==='PREF'){ k=Object.keys(m).filter(function(x){return stripPref(x)===stripPref(jp);})[0]||jp; }
      var v=m[k]; return v ? String(v).replace(/-/g,' ').toUpperCase() : '';
    }
    function fitBg(text){
      if(!head || !window.ChibiBg) return;
      var bg=ChibiBg.set(head,text); if(!bg) return;
      var mobile=innerWidth<760, W=head.clientWidth-(mobile?20:8);
      var MIN=mobile?44:104, MAX=Math.floor(Math.min(196,innerWidth*0.165));
      bg.style.fontSize='100px'; bg.style.width='max-content';
      var tw=bg.offsetWidth-(mobile?20:0); bg.style.width='';
      var f=Math.floor(100*W/Math.max(1,tw)*0.985);
      bg.style.fontSize=Math.max(MIN,Math.min(f,MAX))+'px';
    }
    function updateHeading(hits){
      var area=st.city || st.pref || '';
      var label, title;
      if(!area && !st.sport){ label='子どものスポーツクラブを探す'; title='子ども向けスポーツクラブ・習い事を探す｜チビスポ'; }
      else if(st.sport){ var a=area||'全国'; label=esc(a)+'の<em>'+esc(st.sport)+'</em>クラブ'; title=a+'の子ども向け'+st.sport+'クラブ・スクール'+hits+'件｜チビスポ'; }
      else { label=esc(area)+'の<em>スポーツ</em>クラブ'; title=area+'の子ども向けスポーツクラブ・習い事'+hits+'件｜チビスポ'; }
      if(h1 && h1.innerHTML!==label) h1.innerHTML=label;
      if(document.title!==title) document.title=title;
      var e1=st.city ? en('CITY',st.city) : (st.pref ? en('PREF',st.pref) : ''), e2=st.sport ? en('SPORT',st.sport) : '';
      var bgText=[e1,e2].filter(Boolean).join(' ') || 'CLUBS';
      if(eb) eb.textContent=bgText;
      fitBg(bgText);
      if(countBig) countBig.textContent=hits;
    }
    var bgTimer=null; addEventListener('resize',function(){ clearTimeout(bgTimer); bgTimer=setTimeout(function(){ fitBg(eb?eb.textContent:'CLUBS'); },120); },{passive:true});

    function apply(){
      if(outOfScope() && loadAll(apply)) return;
      var matched=teams.filter(matchTeam); curPage=1;
      updateMapLink(); syncUrl(matched.length); updateHeading(matched.length);
      if(countEl) countEl.textContent=matched.length;
      if(matched.length){
        if(emptyEl) emptyEl.hidden=true; if(nearLabel) nearLabel.hidden=true;
        curList=planSort(matched); renderPage(); return;
      }
      if(loadAll(apply)) return;
      var prefCount = st.pref ? teams.filter(function(t){ return stripPref(t.pref)===stripPref(st.pref); }).length : -1;
      var regionOnly = (prefCount === 0);
      if(emptyEl){
        emptyEl.hidden=false;
        var et=document.getElementById('sr-empty-title'), ec=document.getElementById('sr-empty-cond'), clr=document.getElementById('sr-empty-clear'), rgn=document.getElementById('sr-empty-region');
        if(regionOnly){
          if(et) et.textContent=st.pref+'には、まだ載っているクラブがありません';
          if(ec) ec.textContent='チビスポは掲載クラブを増やしています。'+st.pref+'のクラブが載ったらここに表示されます。';
          if(clr) clr.style.display='none'; if(rgn) rgn.style.display='inline-block';
        }else{
          if(et) et.textContent='この条件のクラブは、まだ載っていません';
          if(ec) ec.textContent=(st.pref? st.pref+'で、こ':'こ')+'の条件に一致するクラブはありませんでした。条件を変えてお試しください。';
          if(clr) clr.style.display='inline-block'; if(rgn) rgn.style.display='none';
        }
      }
      var fb=[], label='';
      if(st.pref){ fb=teams.filter(function(t){return stripPref(t.pref)===stripPref(st.pref);}); if(fb.length) label=st.pref+'の他のクラブ'; }
      if(!fb.length && st.sport){ fb=teams.filter(function(t){return t.sport===st.sport;}); if(fb.length) label='近くの'+st.sport+'のクラブ'; }
      if(!fb.length){ fb=teams.slice(); label='他の地域のおすすめクラブ'; }
      if(nearLabel){ nearLabel.hidden=false;
        var t1=document.getElementById('sr-near-title'); if(t1) t1.textContent=label;
        var s1=document.getElementById('sr-near-sub'); if(s1) s1.textContent = regionOnly ? '参考までに、他の地域のクラブをご紹介します' : 'ご希望の条件では見つからなかったため、近いクラブをご紹介します';
      }
      curList=planSort(fb); renderPage();
    }

    var _init = window.__AREA_INIT || {};
    if(_init.pref && !_p.get('pref')) _p.set('pref', _init.pref);
    if(_init.city && !_p.get('city')) _p.set('city', _init.city);
    if(_init.sport && !_p.get('sport')) _p.set('sport', _init.sport);
    if(_p.get('sport')){
      var sp=_p.get('sport');
      var all=uniqSorted(teams.map(function(t){return t.sport;}));
      st.sport = all.indexOf(sp)>=0 ? sp : (all.filter(function(v){return v.indexOf(sp)>=0||sp.indexOf(v)>=0;})[0]||'');
      if(elSport) elSport.value=st.sport;
    }
    if(_p.get('pref')){ var pp=_p.get('pref'); st.pref = prefList.filter(function(k){return k===pp||stripPref(k)===stripPref(pp);})[0]||pp; if(elPref) elPref.value=st.pref; }
    if(!_p.get('pref') && !_p.get('city') && window.Chibi){
      var rPref=Chibi.getRegionPref&&Chibi.getRegionPref(), rCity=Chibi.getRegionCity&&Chibi.getRegionCity();
      if(rPref){ st.pref = prefList.filter(function(k){return k===rPref||stripPref(k)===stripPref(rPref);})[0]||rPref; if(elPref) elPref.value=st.pref; }
      if(rCity && !_p.get('city')) { st.city=rCity; }
    }
    refreshCities();
    if(_p.get('city')){ st.city=_p.get('city'); if(elCity) elCity.value=st.city; }
    else if(st.city && elCity){ elCity.value=st.city; }
    refreshSports();
    if(_p.get('kw') && elKw){ st.kw=_p.get('kw'); elKw.value=st.kw; }
    ['trial','heijitsu','doyo','girls'].forEach(function(k){
      var on = _p.get(k)==='1' || (k==='trial' && _p.get('taiken')==='1'); if(!on) return;
      st.chk[k]=true; var b=document.querySelector('.sr-chk[data-k="'+k+'"]'); if(b){ b.classList.add('on'); var i=b.querySelector('i'); if(i) i.classList.add('on'); }
    });
    if(_p.get('age')){ _p.get('age').split(',').forEach(function(a){ a=a.trim(); if(!a) return; st.ages[a]=true; var b=document.querySelector('.sr-age[data-age="'+a+'"]'); if(b) b.classList.add('on'); }); }
    if(_p.get('fee') && ['3','5','8','10','none'].indexOf(_p.get('fee'))>=0){ st.fee=_p.get('fee'); document.querySelectorAll('.sr-fee').forEach(function(b){ var on=b.dataset.v===st.fee; b.classList.toggle('on',on); var i=b.querySelector('i'); if(i) i.classList.toggle('on',on); }); }
    if(_p.get('mood')){ st.moods[_p.get('mood')]=true; }

    ['change','click','input'].forEach(function(ev){ document.addEventListener(ev, function(){ urlSyncReady=true; }, true); });
    if(elKw) elKw.addEventListener('input', function(){ st.kw=elKw.value.trim(); apply(); });
    if(elPref) elPref.addEventListener('change', function(){ st.pref=elPref.value; st.city=''; if(elCity) elCity.value=''; refreshCities(); refreshSports(); apply(); });
    if(elCity) elCity.addEventListener('change', function(){ st.city=elCity.value; refreshSports(); apply(); });
    if(elSport) elSport.addEventListener('change', function(){ st.sport=elSport.value; refreshSports(); apply(); });
    document.querySelectorAll('.sr-age').forEach(function(b){ b.addEventListener('click',function(){ var a=b.dataset.age; st.ages[a]=!st.ages[a]; b.classList.toggle('on',st.ages[a]); apply(); }); });
    document.addEventListener('click',function(e){ var b=e.target.closest&&e.target.closest('#sr-mood-list .sr-mood'); if(!b) return; var m=b.dataset.mood; st.moods[m]=!st.moods[m]; b.classList.toggle('on',st.moods[m]); apply(); });
    document.querySelectorAll('.sr-chk').forEach(function(b){ b.addEventListener('click',function(){ var k=b.dataset.k; st.chk[k]=!st.chk[k]; b.classList.toggle('on',st.chk[k]); var i=b.querySelector('i'); if(i) i.classList.toggle('on',st.chk[k]); apply(); }); });
    document.querySelectorAll('.sr-fee').forEach(function(b){ b.addEventListener('click',function(){ st.fee=b.dataset.v; document.querySelectorAll('.sr-fee').forEach(function(x){ var on=x===b; x.classList.toggle('on',on); var i=x.querySelector('i'); if(i) i.classList.toggle('on',on); }); apply(); }); });
    function doClear(){
      st={ kw:'', pref:'', city:'', sport:'', ages:{}, moods:{}, chk:{}, fee:'none' };
      if(elKw) elKw.value=''; if(elPref) elPref.value=''; if(elSport) elSport.value=''; refreshCities();
      document.querySelectorAll('.sr-age,.sr-mood,.sr-chk,.sr-chk i').forEach(function(x){x.classList.remove('on');});
      document.querySelectorAll('.sr-fee').forEach(function(x){ var on=x.dataset.v==='none'; x.classList.toggle('on',on); var i=x.querySelector('i'); if(i) i.classList.toggle('on',on); });
      apply(); window.scrollTo({top:0,behavior:'smooth'});
    }
    var clearBtn=document.getElementById('sr-clear'); if(clearBtn) clearBtn.addEventListener('click',function(e){ e.preventDefault(); doClear(); });
    var emptyClear=document.getElementById('sr-empty-clear'); if(emptyClear) emptyClear.addEventListener('click',function(e){ e.preventDefault(); doClear(); });
    var emptyRegion=document.getElementById('sr-empty-region'); if(emptyRegion) emptyRegion.addEventListener('click',function(){ if(typeof window.showRegionPopup==='function') window.showRegionPopup(true); else doClear(); });
    document.addEventListener('chibi:region',function(){
      if(!window.Chibi) return;
      var np=Chibi.getRegionPref&&Chibi.getRegionPref(), nc=Chibi.getRegionCity&&Chibi.getRegionCity();
      st.pref = np ? (prefList.filter(function(k){return k===np||stripPref(k)===stripPref(np);})[0]||np) : '';
      if(elPref) elPref.value=st.pref; refreshCities(); st.city = nc || ''; if(elCity) elCity.value=st.city;
      apply(); window.scrollTo({top:0,behavior:'smooth'});
    });

    apply(); veilOff();

    db.from('comments').select('team_id').eq('status','visible').then(function(rc){
      if(rc.error||!rc.data) return;
      var cm={}; rc.data.forEach(function(r){ cm[r.team_id]=(cm[r.team_id]||0)+1; });
      teams.forEach(function(t){ t.comments = cm[t.id]||0; }); apply();
    });
    db.from('likes').select('team_id').then(function(rl){
      if(rl.error||!rl.data) return;
      var lk={}; rl.data.forEach(function(r){ lk[r.team_id]=(lk[r.team_id]||0)+1; });
      teams.forEach(function(t){ t.likes = lk[t.id]||0; }); apply();
    });
    /* おすすめクラブ（PR）：有料プランのクラブがあるときだけ枠を出す */
    var paid=teams.filter(function(t){ return ChibiCard.isPaid(t); });
    if(scoped && !paid.length){ /* 地域ぶんしか持っていない：全国から探す */
      Promise.all([db.from('teams').select(TEAM_COLS).eq('status','approved').eq('plan','pr'),db.from('teams').select(TEAM_COLS).eq('status','approved').eq('plan','pr-plus')]).then(function(rs){ var l=[]; rs.forEach(function(r){ if(!r.error&&r.data) l=l.concat(r.data); }); showRec(l.filter(ChibiCard.isPaid)); }).catch(function(){});
    } else showRec(paid);
    function showRec(list){
      var sec=document.getElementById('sr-rec-sec'), g=document.getElementById('sr-rec'); if(!sec||!g||!list.length) return;
      g.innerHTML=(window.ChibiPlan?ChibiPlan.sort(list):list).slice(0,4).map(function(t){ return card(t,{pr:true}); }).join(''); sec.hidden=false;
    }
  });

  /* 地域のおすすめ企業（companies）：読めなければ枠ごと出さない */
  (function(){
    var _q=new URLSearchParams(location.search), _a=window.__AREA_INIT||{};
    var aPref=_q.get('pref')||_a.pref||'', aCity=_q.get('city')||_a.city||'';
    function compCard(c){
      var ini=(c.name||'?').charAt(0);
      var loc=c.online?'オンラインショップ':esc(c.city||c.pref||'');
      return '<a class="a" href="'+esc(c.page_url||'#')+'">'+(c.banner_url?'<img class="lg" src="'+esc(c.banner_url)+'" alt="" style="object-fit:cover">':'<div class="lg">'+esc(ini)+'</div>')+'<div class="t">'+esc(c.name)+'<small>'+esc(c.tagline||c.category||'')+(loc?' ・ '+loc:'')+'</small></div></a>';
    }
    db.from('companies').select('*').eq('status','active').then(function(rc){
      if(rc.error||!rc.data||!rc.data.length) return;
      var now=new Date();
      var comps=rc.data.filter(function(c){ if(c.plan_expires_at && new Date(c.plan_expires_at)<now) return false; if(c.online) return true; if(aPref) return stripPref(c.pref)===stripPref(aPref); return true; });
      comps.sort(function(a,b){ return (a.online?1:0)-(b.online?1:0) || ((aCity&&b.city===aCity?1:0)-(aCity&&a.city===aCity?1:0)) || ((a.sort_order||0)-(b.sort_order||0)); });
      var g=document.getElementById('sr-companies'), sec=document.getElementById('sr-comp-sec');
      if(g && sec && comps.length){ g.innerHTML=comps.slice(0,4).map(compCard).join(''); sec.hidden=false; }
    });
  })();
})();
</script>'''
anon=re.search(r"SB_KEY = '([^']+)'",open(C.D+'shared.js',encoding='utf-8').read()).group(1)
js=js.replace('__ANON__',anon)
head='''<base href="/">
<!-- 絞り込み結果はURLの組み合わせが無限に増え、地域ページ（/clubs/…）と中身が重複する。
     Airbnbも絞り込みUI（/s/…）を noindex にして、SEOは地域ページ側に寄せている -->
<script>window.__SEARCH_PAGE=1;</script>
'''
C.prodpage('search.html','検索結果｜チビスポ','地域・種目・条件から、お子さんに合う子ども向けスポーツクラブ・習い事を探せます。',body,css=css,js=js,head=head,supabase=True,noindex=True,scripts=('club-card.js?v='+C.V,'romaji.js?v=20260802','cities.js?v=20260731b','site.js?v='+C.V))
