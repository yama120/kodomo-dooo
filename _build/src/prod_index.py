# TOP 本番（index.html）：プレビュー（video-hero-preview.html）の節を本番の導線・実データに置き換える
import os,re,sys,json,urllib.request
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
top=open(D+'video-hero-preview.html',encoding='utf-8').read()
body=top[top.index('<body'):top.index('<div id="skins">')]
body=body[body.index('</header>')+9:]                       # ヘッダーは prodpage が付ける
body=body[:body.index('<footer')]                            # フッターも
body=re.sub(r'<div class="note"[^>]*>.*?</div>\n?','',body,flags=re.S)
secs=re.findall(r'<section class="[^"]*"[^>]*>.*?</section>',body,re.S)
assert len(secs)==14, len(secs)
sec=dict(hero=0,reels=1,picks=2,new=3,sports=4,quiz=5,themes=6,moments=7,beg=8,feat=9,app=10,svc=11,cta=12,seo=13)
S={k:secs[v] for k,v in sec.items()}

# 実データ（生成時に1回）：地域・種目のリンク用
ANON=re.search(r"SB_KEY = '([^']+)'",open(D+'shared.js',encoding='utf-8').read()).group(1)
def sb(path):
    req=urllib.request.Request('https://emkpkomrgknzrmxqbrvx.supabase.co/rest/v1/'+path,headers={'apikey':ANON,'Authorization':'Bearer '+ANON})
    return json.load(urllib.request.urlopen(req,timeout=30))
teams=sb('teams?select=pref,city,sport&status=eq.approved')
rom=open(D+'romaji.js',encoding='utf-8').read()
def jsmap(name):
    m=re.search(r'const %s = \{(.*?)\n\};'%name,rom,re.S); d={}
    for k,v in re.findall(r'["\']([^"\']+)["\']\s*:\s*["\']([^"\']+)["\']',m.group(1)): d[k]=v
    return d
PREF,SPORT=jsmap('PREF'),jsmap('SPORT')
from collections import Counter
pc=Counter(t['pref'] for t in teams if t.get('pref')); sc=Counter(t['sport'] for t in teams if t.get('sport'))

# ---- hero ----
h=S['hero']
h=h.replace('<div class="sb-row"><input placeholder="世田谷区, サッカー, 体験OK"><button>検索</button></div>',
            '<form class="sb-row" action="search.html" method="get"><input name="kw" placeholder="クラブ名、市区町村、種目" aria-label="クラブを探す"><button type="submit">検索</button></form>')
h=re.sub(r'<div class="sb-tab">(<svg.*?</svg>)エリア</div>',r'<a class="sb-tab" href="search.html">\1エリア</a>',h,flags=re.S)
h=re.sub(r'<div class="sb-tab">(<svg.*?</svg>)種目</div>',r'<a class="sb-tab" href="search.html#sr-sport">\1種目</a>',h,flags=re.S)
h=re.sub(r'<div class="sb-tab">(<svg.*?</svg>)こだわり</div>',r'<a class="sb-tab" href="search.html?trial=1">\1こだわり</a>',h,flags=re.S)
h=h.replace('href="shindan-preview.html" data-quiz','href="search.html" data-quiz').replace('href="service-listing-preview.html"','href="listing.html"')
h=h.replace('<img src="assets/preview-video/jp-soccer-dribble.jpg" alt="">','<img src="assets/preview-video/jp-soccer-dribble.jpg" alt="" fetchpriority="high">')
S['hero']=h
# ---- 30秒でわかるクラブ（仮：動画はまだ無いので写真で） ----
r=S['reels']
r=re.sub(r'<div class="rail">.*?</div>\n  </div>\n</section>','<div class="rail" id="tp-reels"></div>\n  </div>\n</section>',r,flags=re.S)
r=r.replace('<span class="more">すべて見る ›</span>','<a class="more" href="search.html">すべて見る ›</a>')
r=r.replace('写真と文字では分からない「雰囲気」を、動画で。','写真と文字では分からない「雰囲気」を、動画で。<small class="soon-note">動画は準備中。いまは写真でご紹介しています。</small>')
S['reels']=r
# ---- 編集部おすすめ（仮：写真と紹介文がそろっているクラブから） ----
p=S['picks']
p=re.sub(r'<div class="grid">.*?</div>\n  </div>\n</section>','<div class="grid" id="tp-picks"></div>\n  </div>\n</section>',p,flags=re.S)
p=p.replace('<span class="more">もっと見る ›</span>','<a class="more" href="search.html">もっと見る ›</a>')
p=p.replace('ここが気になった、という理由があるクラブだけ。その理由を、見出しにしています。','いま知ってほしいクラブを、編集部がピックアップ。')
S['picks']=p
# ---- 新しく載ったクラブ（実データ） ----
n=S['new']
n=re.sub(r'<div class="news">.*?</div>\n  </div>\n</section>','<div class="news" id="tp-new"></div>\n  </div>\n</section>',n,flags=re.S)
n=n.replace('<span class="more">すべて見る ›</span>','<a class="more" href="search.html">すべて見る ›</a>').replace('今週、あたらしく参加してくれたクラブです。','あたらしく参加してくれたクラブです。')
S['new']=n
# ---- スポーツジャンル（件数は実データ） ----
sp=S['sports']
sp=sp.replace('<span class="more">すべての種目 ›</span>','<a class="more" href="search.html">すべての種目 ›</a>')
for k,idv,href in [('王道スポーツ','royal','category-royal.html'),('個人スポーツ','personal','category-personal.html'),('自然・アウトドア','outdoor','category-outdoor.html'),('マイナースポーツ','minor','category-minor.html')]:
    sp=re.sub(r'<div class="c">(<img[^>]*>)<div class="t"><div class="k">'+re.escape(k)+r'</div><span class="n">[^<]*</span>',
              r'<a class="c" href="'+href+r'">\1<div class="t"><div class="k">'+k+r'</div><span class="n" id="tp-gen-'+idv+r'">–</span>',sp)
sp=re.sub(r'(<a class="c" href="category-[a-z]+\.html">.*?</div></div>)</div>',r'\1</a>',sp,flags=re.S)
sp=re.sub(r'<div class="chips">.*?</div>\n  </div>\n</section>','<div class="chips" id="tp-chips"></div>\n  </div>\n</section>',sp,flags=re.S)
S['sports']=sp
# ---- 3問診断 ----
S['quiz']=S['quiz'].replace('href="shindan-preview.html" data-quiz','href="search.html" data-quiz')
# ---- テーマから探す（写真のマーキーは実クラブの写真で） ----
th=S['themes']
th=re.sub(r'<div class="mq-t">.*?</div>\n    </div>','<div class="mq-t" id="tp-themes"></div>\n    </div>',th,flags=re.S)
th=th.replace('<span class="more">すべて見る ›</span>','<a class="more" href="search.html">すべて見る ›</a>').replace('検索では出てこないクラブとの出会いを。','いま載っているクラブの練習風景です。気になった写真から、クラブへ。')
S['themes']=th
# ---- はじめての方へ（実在の記事） ----
b=S['beg']
b=b.replace('<span class="more">記事をすべて見る ›</span>','<a class="more" href="magazine.html">記事をすべて見る ›</a>')
b=re.sub(r'<div class="jb">(.*?)</div>\n    <div class="arts">',r'<a class="jb" href="about.html">\1</a>\n    <div class="arts">',b,flags=re.S)
b=re.sub(r'<div class="arts">.*?</div>\n  </div>\n</section>',
 '<div class="arts">\n'
 '      <a class="art" href="magazine-4.html"><div class="b"><h3>「うちの子に合うクラブ」の見つけ方・5つの視点</h3><div class="m"><b>クラブ選び</b>2026/07/04</div></div><img src="assets/mag-4.jpg" alt="" loading="lazy"></a>\n'
 '      <a class="art" href="magazine-3.html"><div class="b"><h3>運動が苦手な子でも、楽しく続く習い事の見つけ方</h3><div class="m"><b>はじめて</b>2026/07/03</div></div><img src="assets/mag-3.jpg" alt="" loading="lazy"></a>\n'
 '    </div>\n  </div>\n</section>',b,flags=re.S)
S['beg']=b
# ---- 特徴から探す（検索の条件に対応するものだけ） ----
S['feat']='''<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-h"><h2><em>特徴</em>から探す</h2></div>
    <div class="sec-sub">気になるところだけで、絞れます。</div>
    <div class="tagrow"><div class="lb">対象</div><div class="tagwrap">
      <a class="tagpill" href="search.html?age=未就学">未就学から</a><a class="tagpill" href="search.html?age=小学生">小学生</a><a class="tagpill" href="search.html?age=中学生">中学生</a><a class="tagpill" href="search.html?girls=1">女の子歓迎</a></div></div>
    <div class="tagrow"><div class="lb">活動</div><div class="tagwrap">
      <a class="tagpill" href="search.html?doyo=1">土日に活動</a><a class="tagpill" href="search.html?heijitsu=1">平日に活動</a></div></div>
    <div class="tagrow"><div class="lb">費用・体験</div><div class="tagwrap">
      <a class="tagpill" href="search.html?fee=3">月謝3,000円以下</a><a class="tagpill" href="search.html?fee=5">月謝5,000円以下</a><a class="tagpill" href="search.html?fee=10">月謝10,000円以下</a><a class="tagpill" href="search.html?trial=1">体験OK</a></div></div>
  </div>
</section>'''
# ---- 地図・アプリ ----
a=S['app']
a=a.replace('<a class="b1" href="#">地図で探す</a>','<a class="b1" href="map.html">地図で探す</a>').replace('<a class="b2" href="#">アプリで使う</a>','<a class="b2" href="https://apps.apple.com/jp/app/id6797169414" target="_blank" rel="noopener" data-app-store-cta>アプリで使う</a>')
a=a.replace('ブラウザでそのまま使えます。「ホーム画面に追加」するとアプリになります。<br>iOS / Android アプリは準備中です。','ブラウザでそのまま使えます。iPhone アプリは App Store で公開中。<br>Android アプリは準備中です。')
S['app']=a
# ---- サービス ----
v=S['svc']
v=re.sub(r'<div class="c"><img src="assets/preview-video/px-3448250.jpg" alt=""><div class="b"><h3>クラブを探す</h3>(.*?)<span class="a">詳しく見る ›</span></div></div>',
         r'<a class="c" href="search.html"><img src="assets/preview-video/px-3448250.jpg" alt=""><div class="b"><h3>クラブを探す</h3>\1<span class="a">詳しく見る ›</span></div></a>',v,flags=re.S)
v=re.sub(r'<div class="c"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><div class="b"><h3>クラブの選び方</h3>(.*?)<span class="a">詳しく見る ›</span></div></div>',
         r'<a class="c" href="magazine-4.html"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><div class="b"><h3>クラブの選び方</h3>\1<span class="a">詳しく見る ›</span></div></a>',v,flags=re.S)
for a_,b_ in [('service-listing-preview.html','listing.html'),('partner-preview.html#s02','partner.html#s02'),('service-sns-preview.html','service-sns.html'),('service-ads-preview.html','service-ads.html'),('partner-preview.html#apply','contact.html?who=club')]:
    v=v.replace('href="%s"'%a_,'href="%s"'%b_)
S['svc']=v
# ---- クラブ向けCTA（動画は準備中） ----
c=S['cta'].replace('<a href="#">新入団募集シーズンパックを見る</a>','<a href="partner.html#s02">準備中・お知らせを受け取る ›</a>')
S['cta']=c
# ---- 地域・種目（実データ・ビルド時に焼く） ----
def prefslug(p): return PREF.get(p) or PREF.get(p.rstrip('都道府県'))
pref_links=''.join('<a href="/clubs/%s/">%s</a>'%(prefslug(p),p) for p,n in pc.most_common() if prefslug(p))
sport_links=''.join('<a href="search.html?sport=%s">%s</a>'%(urllib.parse.quote(s_),s_) for s_,n in sc.most_common(14))
cond_links='<a href="search.html?trial=1">体験OK</a><a href="search.html?girls=1">女の子歓迎</a><a href="search.html?age=未就学">未就学から</a><a href="search.html?doyo=1">土日に活動</a><a href="search.html?heijitsu=1">平日に活動</a><a href="search.html?fee=5">月謝5,000円以下</a>'
S['seo']='''<section class="sec sec-alt seo">
  <div class="wrap">
    <h3>地域から探す</h3>
    <div class="row">%s</div>
    <h3>種目から探す</h3>
    <div class="row">%s</div>
    <h3>こだわりから探す</h3>
    <div class="row">%s</div>
  </div>
</section>'''%(pref_links,sport_links,cond_links)

# TOP に出さないセクション。材料がそろったら、この集合から外すだけで復活する
#   moments … まだ材料が無い
#   themes  … 「テーマから探す」。特集を組むまで非表示（2026-09-13・ユーザー指示）
HIDDEN={'moments','themes'}
ALL=['hero','reels','picks','new','sports','quiz','themes','beg','feat','app','svc','cta','seo']
order=[k for k in ALL if k not in HIDDEN]
print('非表示のセクション:',sorted(HIDDEN))
BODY='<main>\n'+'\n'.join(S[k] for k in order)+'\n</main>'
assert 'preview' not in BODY.replace('assets/preview-video','') , [m for m in re.findall(r'[a-z-]*preview[a-z-]*\.html',BODY)]

CSS='''
.soon-note{display:block;margin-top:4px;font-size:11px;font-weight:700;color:var(--sub);letter-spacing:.02em}
.sec-dark .soon-note{color:rgba(255,255,255,.6)}
.rail .card .badge.ph{background:rgba(255,255,255,.18);top:10px;right:10px;bottom:auto}
.sb-row{display:flex}
.sb-tab{cursor:pointer}
.gen a.c{color:inherit}
.tagpill{cursor:pointer}
.seo .row a{cursor:pointer}
.g-item{cursor:pointer;color:inherit}
'''
JS=r'''<script>
(function(){
  var SB='https://emkpkomrgknzrmxqbrvx.supabase.co', KEY='__ANON__';
  var esc=ChibiCard.esc;
  function q(path){ return fetch(SB+'/rest/v1/'+path,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){ return r.ok?r.json():[]; }); }
  function shuffle(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var x=a[i]; a[i]=a[j]; a[j]=x; } return a; }
  function ownerKey(t){ return t.owner_hash||t.id; }
  function oneline(s,n){ s=(s||'').replace(/\s+/g,' ').trim(); var m=s.match(/^[^。！!？?\n]{4,}?[。！!？?]/); if(m && m[0].length<=n+1) return m[0].replace(/[。]$/,''); return s.length>n ? s.slice(0,n)+'…' : s; }
  var COLS='id,name,sport,pref,city,description,photo_url,photo_positions,age_groups,days,fee,fee_num,trial,girls_welcome,female_instructor,moods,plan,plan_expires_at,created_at,owner_hash,video_url';
  q('teams?select='+COLS+'&status=eq.approved&order=created_at.desc').then(function(teams){
    if(!Array.isArray(teams)||!teams.length) return;
    var withPhoto=teams.filter(function(t){ return !!t.photo_url; });
    var uniq=[], seen={};
    shuffle(withPhoto.slice()).forEach(function(t){ var k=ownerKey(t); if(seen[k]) return; seen[k]=1; uniq.push(t); });

    /* 30秒でわかるクラブ（仮）：写真で5枚 */
    var reels=document.getElementById('tp-reels');
    if(reels){
      reels.innerHTML=uniq.slice(0,5).map(function(t){
        return '<a class="card" href="/club.html?id='+esc(t.id)+'"><div class="card-v"><img src="'+esc(t.photo_url)+'" alt="" loading="lazy"><span class="badge ph">PHOTO</span>'
          +'<div class="card-cap"><div class="hl">'+esc(oneline(t.description,30))+'</div></div></div>'
          +'<div class="card-meta"><span class="card-name">'+esc(t.name)+'</span><span class="tag">'+esc(t.sport)+'</span>'+(t.city?'<span class="tag">'+esc(t.city)+'</span>':'')+'</div></a>';
      }).join('');
    }
    /* 編集部おすすめ（仮）：写真と紹介文がそろっているクラブ 8 */
    var picks=document.getElementById('tp-picks');
    if(picks){
      var pool=uniq.filter(function(t){ return (t.description||'').length>=20; }).slice(5,13);
      if(pool.length<8) pool=uniq.slice(0,8);
      picks.innerHTML=pool.map(function(t){
        var days=Array.isArray(t.days)?t.days.length:0;
        var m=[t.sport, days?'週'+days:'', t.trial?'体験OK':(t.girls_welcome?'女の子歓迎':'')].filter(Boolean).join(' / ');
        return '<a class="g-item" href="/club.html?id='+esc(t.id)+'"><div class="g-thumb"><img src="'+esc(t.photo_url)+'" alt="" loading="lazy">'+(t.video_url?'<span class="g-vid">動画あり</span>':'')+'</div>'
          +'<div class="g-title">'+esc(oneline(t.description,24))+'</div><div class="g-meta">'+esc(t.name)+(t.city?'（'+esc(t.city)+'）':'')+'<br>'+esc(m)+'</div></a>';
      }).join('');
    }
    /* 新しく載ったクラブ：新着6 */
    var nw=document.getElementById('tp-new');
    if(nw){ nw.innerHTML=teams.slice(0,6).map(function(t){ return ChibiCard.card(t); }).join(''); }
    /* 種目：ジャンルの件数と種目チップ */
    var ROYAL=/サッカー|野球|バスケ|バレー|水泳|スイミング|テニス|卓球|フットボール/, OUT=/スキー|スノー|サーフ|カヌー|クライミング|登山|自転車/, PERS=/空手|剣道|柔道|柔術|体操|ダンス|チア|テコンドー|レスリング|陸上|バトン|太鼓|水泳|運動|体育|リズム|パーソナル|鬼ごっこ/;
    var g={royal:0,personal:0,outdoor:0,minor:0}, sc={};
    teams.forEach(function(t){ var s=t.sport||''; sc[s]=(sc[s]||0)+1; if(ROYAL.test(s)) g.royal++; else if(OUT.test(s)) g.outdoor++; else if(PERS.test(s)) g.personal++; else g.minor++; });
    Object.keys(g).forEach(function(k){ var el=document.getElementById('tp-gen-'+k); if(!el) return; el.textContent=g[k]+'クラブ'; var card=el.closest('.c'); if(card && !g[k]) card.style.display='none'; });
    var chips=document.getElementById('tp-chips');
    if(chips){
      var names=Object.keys(sc).sort(function(a,b){ return sc[b]-sc[a]; }).slice(0,16), max=sc[names[0]]||1;
      chips.innerHTML=names.map(function(s){ var r=sc[s]/max, cls=r>.6?'xl':r>.3?'l':r>.12?'m':'s'; return '<a class="chip '+cls+'" href="search.html?sport='+encodeURIComponent(s)+'">'+esc(s)+'<small>'+sc[s]+'</small></a>'; }).join('')
        +'<a class="chip more" href="search.html">すべての種目を見る ›</a>';
    }
    /* テーマ（写真のマーキー） */
    var th=document.getElementById('tp-themes');
    if(th){ var ph=uniq.slice(0,12); if(ph.length){ var one=ph.map(function(t){ return '<a class="m" href="/club.html?id='+esc(t.id)+'" title="'+esc(t.name)+'"><img src="'+esc(t.photo_url)+'" alt="" loading="lazy"></a>'; }).join(''); th.innerHTML=one+one; } }
  }).catch(function(){});
})();
</script>'''.replace('__ANON__',ANON)
C.prodpage('index.html','チビスポ｜地域×スポーツ｜子どものクラブ・習い事を見つける',
 'チビスポは、地域の子どもスポーツ・習い事クラブを探せるメディア。地域×種目×雰囲気でぴったりのクラブが見つかり、地図から探せて、体験申込もそのまま。',
 BODY,css=CSS,js=JS,supabase=False,scripts=('club-card.js?v='+C.V,'cities.js?v=20260731b','site.js?v='+C.V,'quiz.js?v='+C.V),head='<link rel="stylesheet" href="quiz.css?v='+C.V+'">\n')
