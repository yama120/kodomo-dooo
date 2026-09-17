<script>
/* ============ 設定・共通 ============ */
var API='https://api.chibispo.com';
var SB_URL='https://emkpkomrgknzrmxqbrvx.supabase.co';
var SB_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ';
var SESSION_KEY='sb-lite-emkpkomrgknzrmxqbrvx.supabase.co-auth';
var PLAT={instagram:'Instagram',threads:'Threads',youtube:'YouTube',tiktok:'TikTok',x:'X'};
var PLAT_COLOR={instagram:'#d6336c',threads:'#1f2430',youtube:'#c4302b',tiktok:'#00b4b4',x:'#54606e'};
var TYPE_COLOR={'募集告知':'#E43B4D','試合・成長':'#2a6fdb','練習風景':'#1f8a5b','コーチ・人柄':'#6b5bd2','お知らせ':'#8a93a0','その他':'#b8bec6'};
var KIND_LABEL={poster:'ポスター',flyer:'チラシ',sns:'SNS',referral:'紹介カード',web:'自クラブHP',other:'その他'};
var RESERVED={'chibispo-feature':'チビスポ特集・マガジン'};
var $=function(s){return document.querySelector(s);};
var esc=function(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
var fmtN=function(n){return Number(n||0).toLocaleString('ja-JP');};
var CLUB=(new URLSearchParams(location.search).get('club')||'').trim();
var DEMO=new URLSearchParams(location.search).has('demo');
var D=null;         // /api/dashboard の応答（デモ時は demoData()）
var CH='all';       // 投稿タブの媒体
function ym(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');}
function monthsBack(n){var a=[],now=new Date();for(var i=n-1;i>=0;i--){var dt=new Date(now.getFullYear(),now.getMonth()-i,1);a.push({key:ym(dt),label:(dt.getMonth()+1)+'月'});}return a;}
function thisMonday(){var d=new Date();var day=(d.getDay()+6)%7;d.setDate(d.getDate()-day);d.setHours(0,0,0,0);return d;}
function isoDate(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}

/* ============ 認証（club-mypage と同じ localStorage セッションを使う） ============ */
var __refreshing=null;
function session(){try{return JSON.parse(localStorage.getItem(SESSION_KEY)||'null');}catch(e){return null;}}
function token(){var s=session();return s&&s.access_token||null;}
function tokenExpired(){var s=session();if(!s||!s.expires_at)return false;return (s.expires_at-30)*1000<Date.now();}
function refreshSession(){
  var s=session(); if(!s||!s.refresh_token)return Promise.resolve(null);
  if(__refreshing)return __refreshing;
  __refreshing=fetch(SB_URL+'/auth/v1/token?grant_type=refresh_token',{method:'POST',headers:{'Content-Type':'application/json',apikey:SB_KEY},body:JSON.stringify({refresh_token:s.refresh_token})})
    .then(function(r){return r.ok?r.json():null;}).then(function(j){__refreshing=null;if(!j||!j.access_token)return null;
      var ns={access_token:j.access_token,refresh_token:j.refresh_token||s.refresh_token,expires_at:j.expires_in?Math.floor(Date.now()/1000)+j.expires_in:j.expires_at,user:j.user||s.user};
      try{localStorage.setItem(SESSION_KEY,JSON.stringify(ns));}catch(e){} return j.access_token;})
    .catch(function(){__refreshing=null;return null;});
  return __refreshing;
}
function ensureToken(){var t=token();if(!t)return Promise.resolve(null);if(!tokenExpired())return Promise.resolve(t);return refreshSession().then(function(n){return n||t;});}
function authFetch(url,opt){opt=opt||{};return ensureToken().then(function(t){if(!t)return null;var o=Object.assign({},opt);o.headers=Object.assign({},opt.headers||{},{Authorization:'Bearer '+t});
  return fetch(url,o).then(function(r){if(r.status!==401)return r;return refreshSession().then(function(n){if(!n)return r;var o2=Object.assign({},opt);o2.headers=Object.assign({},opt.headers||{},{Authorization:'Bearer '+n});return fetch(url,o2);});});});}
function api(path,body){return authFetch(API+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.assign({club:CLUB},body||{}))}).then(function(r){return r?r.json():{error:'session_expired'};});}

/* ============ 手入力（localStorage＝作業用・Supabase club_manual＝正本） ============ */
function hk(k){return 'chibispo_home_'+k+'_'+CLUB;}
function getNum(k,def){var v=parseInt(localStorage.getItem(hk(k))||'',10);return isNaN(v)?def:v;}
function setNum(k,v){localStorage.setItem(hk(k),String(v));}
function joinsData(){try{return JSON.parse(localStorage.getItem(hk('joins_m'))||'{}')||{};}catch(e){return{};}}
function recList(){try{return JSON.parse(localStorage.getItem(hk('records'))||'[]')||[];}catch(e){return[];}}
function isPolicy(k){return /^(🪧|📄|⚽|✏️)/.test(k||'');}
function manualCollect(){return {trial_manual:getNum('trial_manual',0),attend:getNum('attend',0),joins:getNum('joins',0),members:getNum('members',0),goal:getNum('goal',40),joins_m:joinsData(),records:recList()};}
function manualApply(m){if(!m||typeof m!=='object')return;['trial_manual','attend','joins','members','goal'].forEach(function(k){if(m[k]!=null)setNum(k,m[k]);});if(m.joins_m)localStorage.setItem(hk('joins_m'),JSON.stringify(m.joins_m));if(m.records)localStorage.setItem(hk('records'),JSON.stringify(m.records));}
var __pushT=null;
function manualPush(){if(DEMO)return;clearTimeout(__pushT);__pushT=setTimeout(function(){if(!token()||!CLUB)return;api('/api/manual/save',{data:manualCollect()}).then(function(j){if(!(j&&j.ok))console.log('[manual] save failed',j);}).catch(function(){});},1000);}
function joinsThisMonth(){var m=joinsData();return +(m[ym(new Date())]||0);}
function joinsTotal(){var m=joinsData(),s=0;Object.keys(m).forEach(function(k){s+=(+m[k]||0);});return s||getNum('joins',0);}
function joinsAvg(){var m=joinsData(),ks=Object.keys(m).filter(function(k){return /^\d{4}-\d{2}$/.test(k);}).sort();if(!ks.length)return null;var first=ks[0].split('-'),now=new Date();var n=(now.getFullYear()-+first[0])*12+(now.getMonth()+1-+first[1])+1;var s=0;ks.forEach(function(k){s+=(+m[k]||0);});return Math.round(s/Math.max(1,n)*10)/10;}

/* ============ デモデータ（/api/dashboard と同じ形） ============ */
function demoData(){
  var now=new Date(), ms=monthsBack(6);
  var daily=[];for(var i=29;i>=0;i--){var dt=new Date(now.getTime()-i*86400000);daily.push({date:isoDate(dt),views:8+Math.round(Math.abs(Math.sin(i*1.3))*12)+(i<7?4:0)});}
  var views=daily.reduce(function(s,x){return s+x.views;},0);
  var byM={};[4,6,9,8,11,12].forEach(function(v,i){byM[ms[i].key]=v;});
  var joinsM={};[1,3,4,3,5,5].forEach(function(v,i){joinsM[ms[i].key]=v;});
  var mon=thisMonday(), stats=[];
  ['instagram','threads','youtube'].forEach(function(p){for(var w=11;w>=0;w--){var ws=new Date(mon.getTime()-w*7*86400000),we=new Date(ws.getTime()+6*86400000);
    var n=p==='instagram'?[2,2,3,2,2,3,3,2,3,3,3,4][11-w]:p==='threads'?[3,4,4,5,4,6,5,6,6,7,6,7][11-w]:[0,1,0,1,0,1,0,1,0,1,0,1][11-w];
    stats.push({platform:p,period_start:isoDate(ws),period_end:isoDate(we),post_count:n,total_views:p==='threads'?n*900:null,total_likes:n*18});}});
  var P=[['instagram','試合・成長','6年生ラストマッチの様子（保護者撮影）',112,14],['instagram','試合・成長','初ゴールの瞬間！ベンチ全員で大騒ぎ',124,9],['instagram','コーチ・人柄','コーチ紹介：山本コーチが大事にしていること',95,11],['instagram','募集告知','夏の体験会、募集開始！【7月の土曜・全4回】',58,22],['threads','コーチ・人柄','「怒らない指導」について思うこと',48,17],['instagram','募集告知','6月の体験会 受付中（土曜午前・持ち物不要）',41,8],['threads','練習風景','未経験の子が3ヶ月でできるようになること',21,6],['instagram','練習風景','雨の日の体育館練習、実は人気です',34,3],['youtube','練習風景','【密着】土曜練習の1日（ダイジェスト3分）',86,12],['threads','お知らせ','グラウンド開放日のお知らせ（7月分）',4,1],['instagram','試合・成長','市大会ベスト8！応援ありがとうございました',98,7],['threads','募集告知','新学期スタート！体験は随時受付です',30,9]];
  var posts=P.map(function(p,i){var dt=new Date(now.getTime()-(i*5+1)*86400000);return {platform:p[0],posted_at:dt.toISOString(),text:p[2],permalink:'#',media_type:'IMAGE',like_count:p[3],comments_count:p[4],post_type:p[1]};});
  return {ok:true,club:{id:'demo',name:'サンプルFC',plan:'pr-plus',pro:true},
    analytics:{range:{start:isoDate(new Date(now.getTime()-29*86400000)),end:isoDate(now),lookback_days:30},club:{views:views,users:Math.round(views*.72),sessions:Math.round(views*.85),channels:{'Organic Social':150,'Direct':96,'Organic Search':52,'Referral':34},daily:daily}},
    clicks:{range_days:30,total:0,channels:[{slug:'poster-ekimae',name:'駅前ポスター',kind:'poster',clicks:21},{slug:'instagram',name:'Instagram プロフィール',kind:'sns',clicks:96},{slug:'flyer-6',name:'体験会チラシ6月',kind:'flyer',clicks:34},{slug:'referral',name:'紹介カード',kind:'referral',clicks:6}],weekly:{}},
    post_stats:stats,posts:posts,
    trials:{total:50,joined:21,attended:44,by_month:byM,by_weekday:[1,1,2,1,4,5,2]},
    survey:{connected:true,total:15,result:{counts:{'知人の紹介':5,'チビスポで検索':4,'ポスターを見て':3,'Instagram':2,'チラシ':1},numeric:{'総合的な満足度':{avg:4.4,n:15,max:5},'指導者・コーチの対応':{avg:4.6,n:15,max:5},'友人・知人にすすめたいか':{avg:8.6,n:15,max:10,nps:47}}},form_url:'#',edit_url:'#',advice:null,quota:{refresh_used:0,refresh_limit:10,advice_used:0,advice_limit:5},benchmark:{'総合的な満足度':{avg:4.1,clubs:6},'友人・知人にすすめたいか':{avg:8.1,clubs:6,nps:31}}},
    manual:{trial_manual:0,attend:0,joins:0,members:32,goal:40,joins_m:joinsM,records:[{d:ms[2].key+'-05',k:'🪧 ポスターを掲示した',r:'',n:0,m:'駅前掲示板'},{d:ms[4].key+'-12',k:'📄 チラシを配った',r:'',n:0,m:'体験会チラシ'}]},
    ai_report:{report:[{p:'高',title:'駅前ポスターのQRを、小学校前にも',body:'駅前ポスターのQRから30日で21人がクラブページへ。体験申込12件のうち2件はここから。紙の施策で一番効いています。',why:'掲示1か所でこの数字なら、場所を増やせば倍が狙えます。場所ごとにQRを分けると効果比較ができます。'},{p:'中',title:'「試合・成長」の投稿を週1本に',body:'反応（♥＋💬）の平均が最も高いのが試合・成長系。募集告知の2.3倍です。',why:'成長系で知ってもらい、募集告知で申込へ。役割分担が数字に出ています。'},{p:'低',title:'紹介カードの配布を増やす',body:'アンケートでは「知人の紹介」が33%で1位ですが、計測リンク経由はまだ6クリック。',why:'口コミは最大の入口。QR付きカードを保護者に渡すと数えられます。'}],at:new Date(now.getTime()-3*86400000).toISOString(),quota:{used:0,limit:3}}};
}
</script>
