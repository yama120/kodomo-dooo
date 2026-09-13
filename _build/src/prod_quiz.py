# 3問診断（ポップアップ）を本番化：preview-quiz.js → quiz.js（地域は実データ・結果のクラブは実データ・リンクは本番）
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
s=open(D+'preview-quiz.js',encoding='utf-8').read()
# 1) サンプルカードの定数を捨てる
s=re.sub(r'var CARDS=\{.*?\};\n','',s,count=1,flags=re.S); assert 'var CARDS' not in s
# 2) 地域の質問：都道府県・市区町村（cities.js）
old_area='''if(q.type==='area'){s+='<div class="cq-sel"><select><option>東京都</option></select><select><option>世田谷区</option></select></div><a class="cq-geo" href="#">◎ 現在地から探す</a>'}'''
assert old_area in s
s=s.replace(old_area,'''if(q.type==='area'){s+='<div class="cq-sel"><select id="cq-pref"><option value="">都道府県を選択</option></select><select id="cq-city" disabled><option value="">市区町村（任意）</option></select></div><a class="cq-geo" href="map.html">◎ 現在地から地図で探す</a>'}''')
old_nx='''var nx=box.querySelector('.cq-next');if(nx)nx.addEventListener('click',function(){if(q.type==='area')ans.area=['世田谷区'];cur++;render()});'''
assert old_nx in s
s=s.replace(old_nx,'''if(q.type==='area'){
   var pf=box.querySelector('#cq-pref'),ct=box.querySelector('#cq-city'),C=(typeof CITIES!=='undefined')?CITIES:{};
   Object.keys(C).forEach(function(p){var o=document.createElement('option');o.value=p;o.textContent=p;pf.appendChild(o)});
   function fillCity(){ct.innerHTML='<option value="">市区町村（任意）</option>';var list=C[pf.value]||[];list.forEach(function(c){var o=document.createElement('option');o.value=c;o.textContent=c;ct.appendChild(o)});ct.disabled=!list.length}
   var sp=ans.areaPref||(window.Chibi&&Chibi.getRegionPref&&Chibi.getRegionPref())||'',scc=ans.areaCity||(window.Chibi&&Chibi.getRegionCity&&Chibi.getRegionCity())||'';
   if(sp&&C[sp]){pf.value=sp;fillCity();if(scc)ct.value=scc}
   pf.addEventListener('change',function(){fillCity()});
 }
 var nx=box.querySelector('.cq-next');if(nx)nx.addEventListener('click',function(){if(q.type==='area'){var pf=box.querySelector('#cq-pref'),ct=box.querySelector('#cq-city');ans.areaPref=pf?pf.value:'';ans.areaCity=ct?ct.value:'';ans.area=[ans.areaCity||ans.areaPref||'']}cur++;render()});''')
# 3) 結果：地域名・種目リンク・クラブは実データ・記事とマイページは本番
s=s.replace("var cond=['世田谷区',age,day]","var areaLabel=(ans.areaCity||ans.areaPref||'全国'),qs=(ans.areaPref?'&pref='+encodeURIComponent(ans.areaPref):'')+(ans.areaCity?'&city='+encodeURIComponent(ans.areaCity):'');\n var cond=[areaLabel,age,day]")
s=s.replace('''return '<a href="search-preview.html"><b>'+h(x[0])+'</b><small>'+h(x[1])+'</small><i>世田谷区の'+h(x[0])+'を見る ›</i></a>\'''','''return '<a href="/search.html?sport='+encodeURIComponent(x[0])+qs+'"><b>'+h(x[0])+'</b><small>'+h(x[1])+'</small><i>'+h(areaLabel)+'の'+h(x[0])+'を見る ›</i></a>\'''')
s=s.replace(''' s+='<h3>世田谷区で、いま募集しているクラブ</h3><div class="cards">'+(CARDS[r.type]||'')+'</div>';''',''' s+='<div id="cq-clubs" hidden><h3>'+h(areaLabel)+'で、いま載っているクラブ</h3><div class="cards" id="cq-cards"></div></div>';''')
s=s.replace('href="article-preview.html"','href="/magazine-4.html"').replace('''<a class="b2" href="search-preview.html">一覧で見る</a>''','''<a class="b2" href="/search.html?x='+qs+'">一覧で見る</a>''').replace("location.href='mypage-preview.html?saved=1'","location.href='/mypage.html?saved=1'")
# 結果描画のあとに実データを取る
old_tail=''' box.querySelector('.cq-redo').addEventListener('click',function(e){e.preventDefault();cur=0;render()});'''
assert old_tail in s
s=s.replace(old_tail,old_tail+'''
 (function(){
   if(!window.ChibiCard) return;
   var KEY='__ANON__', SB='https://emkpkomrgknzrmxqbrvx.supabase.co';
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
 })();''')
# 内部リンクはルート起点に（検索ページは条件を変えるとURLが /clubs/… に変わるため）
for _a,_b in [("href:'category-","href:'/category-"),("href='mypage.html?saved=1'","href='/mypage.html?saved=1'"),
              ('href="magazine-4.html"','href="/magazine-4.html"'),('href="search.html','href="/search.html'),
              ("href='search.html","href='/search.html")]:
    s=s.replace(_a,_b)
anon=re.search(r"SB_KEY = '([^']+)'",open(D+'shared.js',encoding='utf-8').read()).group(1)
s=s.replace('__ANON__',anon)
s=s.replace('demo(){open();ans={area:[\'世田谷区\'],','demo(){open();ans={areaPref:\'東京都\',areaCity:\'世田谷区\',area:[\'世田谷区\'],')
s='/* 3問診断（生成物：_build/src/prod_quiz.py が preview-quiz.js から作る。直接編集しない） */\n'+s
open(D+'quiz.js','w',encoding='utf-8').write(s)
css=open(D+'preview-quiz.css',encoding='utf-8').read()
open(D+'quiz.css','w',encoding='utf-8').write('/* 3問診断（生成物：preview-quiz.css の複製） */\n'+css)
print('quiz.js',len(s)//1024,'KB / quiz.css',len(css)//1024,'KB; preview links left:',len(re.findall(r'-preview\.html',s)))
