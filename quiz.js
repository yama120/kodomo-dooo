/* 3問診断（生成物：_build/src/prod_quiz.py が preview-quiz.js から作る。直接編集しない） */

(function(){
/* ---- 質問（答えはすべてクラブの登録項目か、種目の分類に落ちる） ---- */
var Q=[
 {id:'area',type:'area',ey:'WHERE',t:'どこで、探しますか。',ld:'お住まいの地域か、いまいる場所から。'},
 {id:'age',type:'one',ey:'WHO',t:'お子さんは、いまいくつですか。',ld:'クラブの対象年齢で絞ります。',o:[['未就学','年少〜年長'],['小学1〜3年'],['小学4〜6年'],['中学生']]},
 {id:'team',type:'one',ey:'STYLE',t:'遊ぶときは、どちらが多いですか。',ld:'チームで盛り上がるか、自分のペースか。',o:[['友だちと一緒に盛り上がる','',{team:2}],['ひとりで黙々と集中する','',{solo:2}],['どちらも','',{team:1,solo:1}]]},
 {id:'place',type:'one',ey:'PLACE',t:'体を動かすなら、どこが好きですか。',ld:'外・室内・水の中。',o:[['外で思いきり','',{outdoor:2}],['室内で','',{indoor:2}],['水の中','',{water:2}],['どこでも','',{outdoor:1,indoor:1}]]},
 {id:'like',type:'multi',ey:'LIKES',t:'好きなことは、どれですか。',ld:'いくつでも。近いものを選んでください。',o:[['ボールを追いかける','',{ball:2}],['走る・跳ぶ・回る','',{athletic:2}],['音楽に合わせて動く','',{rhythm:2}],['礼儀や集中を身につけたい','',{martial:2}],['みんながやっていないことに興味がある','',{rare:2}]]},
 {id:'mood',type:'one',ey:'MOOD',t:'クラブの空気は、どちらが合いそうですか。',ld:'クラブが登録している「雰囲気タグ」で絞ります。',o:[['楽しむことがいちばん','雰囲気タグ：楽しむこと',{mood:'楽しむこと'}],['本格的に上を目指したい','雰囲気タグ：本格志向',{mood:'本格志向'}],['まだわからない','',{}]]},
 {id:'day',type:'one',ey:'WHEN',t:'いつ、通えますか。',ld:'活動曜日で絞ります。',o:[['平日','放課後'],['土日'],['どちらでも']]},
 {id:'cond',type:'multi',ey:'EXTRA',t:'あれば、こだわりを。',ld:'なくても、そのまま結果へ。',o:[['女の子です','女の子歓迎のクラブ'],['女性の指導者がいる'],['入会金がない'],['まず体験したい','体験OKのクラブ']]}
];
var TYPES={
 royal:{name:'王道スポーツ',em:'王道',why:'友だちと一緒に盛り上がるのが好きで、ボールを追いかける遊びが得意。チームで勝ち負けを味わえる種目が合いそうです。',sports:[['サッカー','週1から始めやすい。地域に最も多い'],['バスケットボール','室内・少人数。ミニバスは未就学から'],['野球','土日中心。親子で通う家庭が多い']],href:'/category-royal.html'},
 personal:{name:'個人スポーツ',em:'個人',why:'自分のペースで集中するのが得意。できることが一つずつ増えるのが見える種目が合いそうです。',sports:[['水泳','全身を使い、けがが少ない'],['体操','走る・跳ぶ・回るの土台になる'],['空手・剣道','礼儀と集中を身につけたい子に']],href:'/category-personal.html'},
 outdoor:{name:'自然・アウトドア',em:'アウトドア',why:'外で思いきり体を動かすのが好き。季節や場所が変わる種目のほうが、飽きずに続きます。',sports:[['陸上','走る・跳ぶを外で。運動会が楽しみになる'],['スキー・スノーボード','冬だけの集中プログラムも'],['カヌー・サーフィン','水と外の両方が好きな子に']],href:'/category-outdoor.html'},
 minor:{name:'マイナースポーツ',em:'マイナー',why:'みんながやっていないことに興味がある子。始める人が少ないぶん、伸びるのが早く、大会にも出やすい種目です。',sports:[['ラクロス','女の子の入部が多い。中学から始める子も'],['ダブルダッチ','音楽に合わせて跳ぶ。チームで'],['マルチスポーツ','いろいろ試してから決められる']],href:'/category-minor.html'}
};
var ans={},cur=0,ov,box;
function h(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function build(){
 ov=document.createElement('div');ov.className='cq-ov';ov.innerHTML='<div class="cq" role="dialog" aria-modal="true"><button class="cq-x" aria-label="閉じる">×</button><div class="cq-body"></div></div>';
 document.body.appendChild(ov);box=ov.querySelector('.cq-body');
 ov.querySelector('.cq-x').addEventListener('click',close);ov.addEventListener('click',function(e){if(e.target===ov)close()});
}
function open(){if(!ov)build();ov.classList.add('on');document.body.classList.add('cq-lock');cur=0;ans={};render()}
function close(){ov.classList.remove('on');document.body.classList.remove('cq-lock')}
function prog(){var s='<div class="cq-prog">';for(var i=0;i<Q.length;i++)s+='<i class="'+(i<=cur?'on':'')+'"></i>';return s+'</div>'}
function render(){
 if(cur>=Q.length)return result();
 var q=Q[cur],n=('0'+(cur+1)).slice(-2),tot=('0'+Q.length).slice(-2),s=prog()+'<div class="cq-step"><div class="cq-big">'+n+'</div><div class="cq-ey">STEP '+n+' / '+tot+' ・ '+q.ey+'</div><h2>'+h(q.t)+'</h2><div class="ld">'+h(q.ld)+'</div>';
 if(q.type==='area'){s+='<div class="cq-sel"><select id="cq-pref"><option value="">都道府県を選択</option></select><select id="cq-city" disabled><option value="">市区町村（任意）</option></select></div><a class="cq-geo" href="map.html">◎ 現在地から地図で探す</a>'}
 else{var one=q.o.length>4||q.type==='multi',three=(!one&&q.o.length===3);s+='<div class="cq-opts'+(one?' one':(three?' three':''))+'">';q.o.forEach(function(o,i){var on=(ans[q.id]||[]).indexOf(i)>=0;s+='<div class="cq-opt'+(on?' on':'')+'" data-i="'+i+'">'+(q.type==='multi'?'<span class="ck"></span>':'')+h(o[0])+(o[1]?'<small>'+h(o[1])+'</small>':'')+'</div>'});s+='</div>'}
 s+='<div class="cq-nav">'+(cur>0?'<button class="cq-back">‹ もどる</button>':'<span></span>')+(q.type==='one'?'<span class="cq-hint">選ぶと次へ進みます</span>':'<button class="cq-next">'+(cur===Q.length-1?'結果を見る ›':'つぎへ ›')+'</button>')+'</div></div>';
 box.innerHTML=s;box.scrollTop=0;
 box.querySelectorAll('.cq-opt').forEach(function(el){el.addEventListener('click',function(){var i=+el.dataset.i;if(q.type==='one'){ans[q.id]=[i];box.querySelectorAll('.cq-opt').forEach(function(x){x.classList.remove('on')});el.classList.add('on');setTimeout(function(){cur++;render()},180)}else{var a=ans[q.id]||[];var k=a.indexOf(i);if(k>=0)a.splice(k,1);else a.push(i);ans[q.id]=a;el.classList.toggle('on')}})});
 if(q.type==='area'){
   var pf=box.querySelector('#cq-pref'),ct=box.querySelector('#cq-city'),C=(typeof CITIES!=='undefined')?CITIES:{};
   Object.keys(C).forEach(function(p){var o=document.createElement('option');o.value=p;o.textContent=p;pf.appendChild(o)});
   function fillCity(){ct.innerHTML='<option value="">市区町村（任意）</option>';var list=C[pf.value]||[];list.forEach(function(c){var o=document.createElement('option');o.value=c;o.textContent=c;ct.appendChild(o)});ct.disabled=!list.length}
   var sp=ans.areaPref||(window.Chibi&&Chibi.getRegionPref&&Chibi.getRegionPref())||'',scc=ans.areaCity||(window.Chibi&&Chibi.getRegionCity&&Chibi.getRegionCity())||'';
   if(sp&&C[sp]){pf.value=sp;fillCity();if(scc)ct.value=scc}
   pf.addEventListener('change',function(){fillCity()});
 }
 var nx=box.querySelector('.cq-next');if(nx)nx.addEventListener('click',function(){if(q.type==='area'){var pf=box.querySelector('#cq-pref'),ct=box.querySelector('#cq-city');ans.areaPref=pf?pf.value:'';ans.areaCity=ct?ct.value:'';ans.area=[ans.areaCity||ans.areaPref||'']}cur++;render()});
 var bk=box.querySelector('.cq-back');if(bk)bk.addEventListener('click',function(){cur=Math.max(0,cur-1);render()});
}
function score(){var sc={royal:0,personal:0,outdoor:0,minor:0},tag={};
 Q.forEach(function(q){(ans[q.id]||[]).forEach(function(i){var o=q.o&&q.o[i];if(!o||!o[2])return;Object.keys(o[2]).forEach(function(k){tag[k]=(tag[k]||0)+(typeof o[2][k]==='number'?o[2][k]:0);if(k==='mood')tag.mood=o[2][k]})})});
 sc.royal=(tag.team||0)*1.2+(tag.ball||0)*1.5+(tag.indoor||0)*.5+(tag.outdoor||0)*.5;
 sc.personal=(tag.solo||0)*1.2+(tag.martial||0)*1.5+(tag.water||0)*1.5+(tag.athletic||0)*.8+(tag.rhythm||0)*.8;
 sc.outdoor=(tag.outdoor||0)*1.3+(tag.athletic||0)*.8+(tag.rare||0)*.4+(tag.solo||0)*.4;
 sc.minor=(tag.rare||0)*2+(tag.rhythm||0)*.6+(tag.team||0)*.3;
 var best='royal';Object.keys(sc).forEach(function(k){if(sc[k]>sc[best])best=k});return {type:best,tag:tag};
}
function label(q,i){var o=Q.filter(function(x){return x.id===q})[0];return o&&o.o&&o.o[i]?o.o[i][0]:''}
function result(){
 var r=score(),T=TYPES[r.type],age=label('age',(ans.age||[1])[0]),day=label('day',(ans.day||[2])[0]);
 var areaLabel=(ans.areaCity||ans.areaPref||'全国'),qs=(ans.areaPref?'&pref='+encodeURIComponent(ans.areaPref):'')+(ans.areaCity?'&city='+encodeURIComponent(ans.areaCity):'');
 var cond=[areaLabel,age,day].concat((ans.cond||[]).map(function(i){return label('cond',i)}));if(r.tag.mood)cond.push(r.tag.mood);
 var s='<div class="cq-res"><div class="k">RESULT</div><div class="tp">お子さんに合いそうなのは、<em>'+h(T.name)+'</em>。</div><p class="why">'+h(T.why)+'</p>';
 s+='<div class="cond">'+cond.map(function(c){return '<span>'+h(c)+'</span>'}).join('')+'<a href="#" class="cq-redo">条件を変える</a></div>';
 s+='<h3>まず見てほしい種目</h3><div class="sp">'+T.sports.map(function(x){return '<a href="/search.html?sport='+encodeURIComponent(x[0])+qs+'"><b>'+h(x[0])+'</b><small>'+h(x[1])+'</small><i>'+h(areaLabel)+'の'+h(x[0])+'を見る ›</i></a>'}).join('')+'</div>';
 s+='<div id="cq-clubs" hidden><h3>'+h(areaLabel)+'で、いま載っているクラブ</h3><div class="cards" id="cq-cards"></div></div>';
 s+='<div class="save"><div class="t">この結果を、マイページに保存しますか。</div><p>保存すると、この条件に合う新しいクラブが載ったとき・体験の募集が始まったときにお知らせします。あとから条件も変えられます。</p><div class="row"><button class="b1 cq-save">保存する（無料）</button><a class="b2" href="/search.html?x='+qs+'">一覧で見る</a></div></div>';
 s+='<div class="alt">はじめてのクラブ選びなら：<a href="/magazine-4.html">「うちの子に合うクラブ」の見つけ方・5つの視点</a>／<a href="'+T.href+'">'+h(T.name)+'の種目をぜんぶ見る</a></div></div>';
 box.innerHTML=s;box.scrollTop=0;
 box.querySelector('.cq-redo').addEventListener('click',function(e){e.preventDefault();cur=0;render()});
 (function(){
   if(!window.ChibiCard) return;
   var KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ', SB='https://emkpkomrgknzrmxqbrvx.supabase.co';
   var cols='id,name,sport,pref,city,description,photo_url,photo_positions,age_groups,days,fee,fee_num,trial,girls_welcome,female_instructor,moods,plan,plan_expires_at,created_at,video_url';
   var url=SB+'/rest/v1/teams?select='+cols+'&status=eq.approved&order=created_at.desc'+(ans.areaPref?'&pref=eq.'+encodeURIComponent(ans.areaPref):'')+(ans.areaCity?'&city=eq.'+encodeURIComponent(ans.areaCity):'');
   fetch(url,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){return r.ok?r.json():[]}).then(function(list){
     if(!Array.isArray(list)||!list.length) return;
     var want=T.sports.map(function(x){return x[0]});
     var hit=list.filter(function(t){return want.some(function(w){return (t.sport||'').indexOf(w)>=0})});
     if(!hit.length) hit=list;
     var wrap=document.getElementById('cq-clubs'),g=document.getElementById('cq-cards'); if(!wrap||!g) return;
     g.innerHTML=hit.slice(0,3).map(function(t){return ChibiCard.card(t)}).join(''); wrap.hidden=false;
   }).catch(function(){});
 })();
 box.querySelector('.cq-save').addEventListener('click',function(){try{localStorage.setItem('chibispo_quiz',JSON.stringify({type:r.type,typeName:T.name,cond:cond,sports:T.sports.map(function(x){return x[0]}),at:new Date().toISOString()}))}catch(e){}location.href='/mypage.html?saved=1'});
}
window.ChibiQuiz={open:open,close:close};
document.addEventListener('click',function(e){var a=e.target.closest('[data-quiz]');if(a){e.preventDefault();open()}});
function demo(){open();ans={areaPref:'東京都',areaCity:'世田谷区',area:['世田谷区'],age:[1],team:[0],place:[0],like:[0,1],mood:[0],day:[1],cond:[3]};cur=Q.length;render()}
window.ChibiQuiz.demo=demo;
if(document.body&&document.body.dataset.quizAuto)addEventListener('load',function(){setTimeout(location.hash==='#result'?demo:open,200)});
})();
