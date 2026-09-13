# マガジン一覧＋記事7本 本番：旧ページ（_build/src/legacy/）の本文を、v2 の見た目（mag_v2 / art_v2）に載せ替える
import os,re,sys,html
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D; L=D+'_build/src/legacy/'
cap={}
def page(fname,title,body,css='',bodyattr='',extra_js=''): cap[fname]=dict(body=body,css=css,js=extra_js)
import prod_exec; g=prod_exec.load(page,('mag_v2','art_v2'))
ART_EXTRA='''
.anext{display:block;color:inherit}.art{color:inherit}
.art-body img{max-width:100%;height:auto}
/* 参考にした指針・提言 */
.art-src{border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:16px 18px;margin:30px 0 0}
.art-src .t{font-family:var(--fh);font-size:12.5px;font-weight:900;color:var(--sub);letter-spacing:.04em;margin-bottom:8px}
.art-src ul{margin:0;padding-left:18px}
.art-src li{font-size:12px;font-weight:700;color:var(--sub);line-height:2}
/* 著者（チビスポ編集部） */
.art-au{display:flex;align-items:center;gap:13px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:16px 18px;margin:14px 0 0}
.art-au .av{width:50px;height:50px;flex:0 0 50px;border-radius:50%;background:color-mix(in srgb,var(--accent) 10%,#fff);border:1px solid color-mix(in srgb,var(--accent) 25%,#fff);display:flex;align-items:center;justify-content:center}
.art-au .av img{width:34px;height:34px;display:block}
.art-au b{display:block;font-family:var(--fh);font-size:14px;font-weight:900}
.art-au p{margin:2px 0 0;font-size:12px;font-weight:700;color:var(--sub);line-height:1.75}
'''
MAG_CSS=C.strip_preview(cap['magazine-preview.html']['css']); ART_CSS=C.strip_preview(cap['article-preview.html']['css']); ART_JS=cap['article-preview.html']['js']
# ---- 旧ページから記事データ ----
CAT_EN={'はじめてのスポーツ選び':'BEGINNERS','年齢別の運動':'BY AGE','保護者の関わり':'PARENTS','からだのケア':'BODY CARE','コーチの声':'COACH'}
arts=[]
lst=open(L+'magazine.html',encoding='utf-8').read()
for n in range(1,8):
    a=open(L+'magazine-%d.html'%n,encoding='utf-8').read()
    title=html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>',a,re.S).group(1)).strip()
    desc=html.unescape(re.search(r'<meta name="description" content="([^"]*)"',a).group(1))
    date=re.search(r'>(\d{4}\.\d{2}\.\d{2})<',a).group(1)
    cats=[c for c in re.findall(r'<span[^>]*>([^<]{2,20})</span>',a[:a.index('<h1')]) if c!='PT監修']
    pt='PT監修' in a[:a.index('<h1')]
    cat=cats[-1] if cats else 'マガジン'
    img=re.search(r'<img src="(assets/mag-\d+\.jpg)"',a).group(1)
    art=re.search(r'<article[^>]*>(.*?)</article>',a,re.S).group(1)
    lead=re.search(r'^\s*<p[^>]*>(.*?)</p>',art,re.S); lead=html.unescape(re.sub(r'<[^>]+>','',lead.group(1))).strip() if lead else desc
    body=re.search(r'<div class="ar-body"[^>]*>(.*?)</div>\s*$',art,re.S).group(1)
    # 本文の末尾にある「出典」「著者」は、もとはインラインの装飾で枠を作っていた。
    # 装飾を落とすと崩れる（画像が原寸で出る）ので、ここで新デザインの部品に組み直す
    srcs=[]; author=None
    if '<!-- 出典 -->' in body:
        rest=body.split('<!-- 出典 -->',1)[1]; body=body.split('<!-- 出典 -->',1)[0]
        src_part=rest.split('<!-- 著者 -->',1)[0]
        srcs=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<li>(.*?)</li>',src_part,re.S)]
        if '<!-- 著者 -->' in rest:
            a=rest.split('<!-- 著者 -->',1)[1]
            texts=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<div[^>]*>([^<]{2,200})</div>',a)]
            texts=[t for t in texts if t]
            if texts: author=(texts[0],texts[1] if len(texts)>1 else '')
    # 旧の吹き出し（ポイント）→ blockquote
    # 「出典」の手前で切ると、本文をくるんでいた </div> が1つ余る。数を合わせる
    while len(re.findall(r'</div>',body))>len(re.findall(r'<div\b',body)):
        body=re.sub(r'</div>\s*$','',body,count=1)
    body=re.sub(r'<div class="ar-callout"[^>]*>\s*<div class="ar-callout-t"[^>]*>[^<]*</div>(.*?)</div>',lambda m:'<blockquote>'+m.group(1).strip()+'</blockquote>',body,flags=re.S)
    body=re.sub(r' style="[^"]*"','',body)
    # h2 に id（目次用）
    heads=[]; k=[0]
    def rid(m):
        k[0]+=1; heads.append(html.unescape(re.sub(r'<[^>]+>','',m.group(1)))); return '<h2 id="s%d">%s</h2>'%(k[0],m.group(1))
    body=re.sub(r'<h2[^>]*>(.*?)</h2>',rid,body,flags=re.S)
    # 一覧の抜粋
    m=re.search(r'<a href="magazine-%d\.html"[^>]*class="mg-card"[^>]*>(.*?)</a>'%n,lst,re.S) or re.search(r'<a[^>]*href="magazine-%d\.html"[^>]*>(.*?)</a>'%n,lst,re.S)
    ex=''
    if m:
        pm=re.search(r'<p[^>]*>(.*?)</p>',m.group(1),re.S); ex=html.unescape(re.sub(r'<[^>]+>','',pm.group(1))).strip() if pm else ''
    arts.append(dict(srcs=srcs,author=author,n=n,slug='magazine-%d.html'%n,title=title,desc=desc,date=date,cat=cat,pt=pt,img=img,lead=lead,body=body,heads=heads,ex=ex or desc,mins=max(3,len(re.sub(r'<[^>]+>','',body))//500)))
def esc(s): return html.escape(s,quote=True)
# ---- 一覧 ----
FEAT=[x for x in arts if x['n']==4][0]; rest=[x for x in arts if x['n']!=4]
cats=[]; [cats.append(x['cat']) for x in arts if x['cat'] not in cats]
chips='<a class="chip on" href="magazine.html" data-cat="">すべて</a>'+''.join('<a class="chip" href="#" data-cat="%s">%s</a>'%(esc(c),esc(c)) for c in cats)
mi=''.join('<a class="mi" href="%s" data-cat="%s"><img src="%s" alt="" loading="lazy"><div class="c">%s</div><h3>%s</h3><div class="d"><b>%s</b>%s</div></a>'%(x['slug'],esc(x['cat']),x['img'],CAT_EN.get(x['cat'],'MAGAZINE'),esc(x['title']),esc(x['cat']),x['date'].replace('.','/')) for x in rest)
MAG_BODY='''<main>
<section class="sec mhead nobg">
  <div class="wrap">
    <div class="big">MAGAZINE</div>
    <div class="s-h1">
      <h1>体を動かすと、<em>いいこと</em>がある。</h1>
      <div class="s-cnt"><span><b>%d</b><small>ARTICLES</small></span><span class="sep"></span><span><b>%d</b><small>TOPICS</small></span></div>
    </div>
    <div class="ld">運動が子どもに何をもたらすか、から、クラブの選び方まで。現場とエビデンスの両面から、読むと動きたくなる話を集めました。</div>
    <div class="cats" id="mgCats">%s</div>
  </div>
</section>
<div class="wrap">
  <a class="feat" href="%s" data-cat="%s"><div class="no">01</div><img src="%s" alt=""><div class="t"><div class="c">FEATURE ・ %s</div><h2>%s</h2><p>%s</p><span class="more">読む ›</span></div></a>
  <div class="mh2"><div><div class="ey">ARTICLES</div><h2>すべての<em>記事</em></h2></div><span class="more">現場とエビデンスの両面から</span></div>
  <div class="mgrid mag" id="mgGrid">%s</div>
  <div style="height:40px"></div>
</div>
</main>'''%(len(arts),len(cats),chips,FEAT['slug'],esc(FEAT['cat']),FEAT['img'],CAT_EN.get(FEAT['cat'],'MAGAZINE'),esc(FEAT['title']),esc(FEAT['ex']),mi)
MAG_JS='''<script>
(function(){var cs=document.getElementById('mgCats');if(!cs)return;cs.addEventListener('click',function(e){var a=e.target.closest('a[data-cat]');if(!a)return;e.preventDefault();var c=a.dataset.cat;cs.querySelectorAll('a').forEach(function(x){x.classList.toggle('on',x===a)});document.querySelectorAll('#mgGrid .mi, .feat').forEach(function(m){m.style.display=(!c||m.dataset.cat===c)?'':'none'})})})();
</script>'''
C.prodpage('magazine.html','マガジン｜チビスポ','スポーツの選び方、年齢別の運動発達、保護者の関わり方まで。「うちの子に合いそう」を見つけるヒントを、現場とエビデンスの両面からお届けします。',MAG_BODY,css=MAG_CSS+'\n.feat{display:grid}.mi{display:block;color:inherit}.chip{cursor:pointer}\n',js=MAG_JS,scripts=('site.js?v='+C.V,))
# ---- 記事 ----
for i,x in enumerate(arts):
    nxt=arts[(i+1)%len(arts)]; rel=[y for y in arts if y['n']!=x['n'] and y['cat']==x['cat']][:2]
    if len(rel)<2: rel=(rel+[y for y in arts if y['n']!=x['n'] and y not in rel])[:2]
    toc=''.join('<li><a href="#s%d">%s</a></li>'%(k+1,esc(h)) for k,h in enumerate(x['heads']))
    x_srcs=x['srcs']; x_author=x['author']
    url='https://chibispo.com/'+x['slug']
    BODY='''<div id="rprog"></div>
<main><div class="wrap">
  <div class="pgh"><div class="bc"><a href="index.html">ホーム</a> › <a href="magazine.html">マガジン</a> › %(cat)s</div></div>
  <div class="ahead">
    <div class="ey">%(en)s<small>%(cat)s%(pt)s</small></div>
    <h1>%(title)s</h1>
    <div class="by"><img src="assets/app-hero/app-icon-512.webp" alt=""><span><b>チビスポ編集部</b> ・ %(date)s</span><span class="rt">%(mins)d MIN READ</span></div>
  </div>
  <div class="akv"><img src="%(img)s" alt="" fetchpriority="high"></div>
  <div class="alay">
    <article class="art-body">
      <p class="lead">%(lead)s</p>
%(body)s
%(srcbox)s%(aubox)s
      <div class="acta"><div class="ey">FIND A CLUB</div><div class="t">近くのクラブを、地域と種目から探す</div><p>体験OK・未就学から・土日など、条件で絞れます。</p><a class="btn" href="search.html">クラブを探す</a></div>
      <div class="share"><span class="lb">SHARE</span><a href="https://x.com/intent/tweet?url=%(url)s&text=%(ttl)s" target="_blank" rel="noopener">X</a><a href="https://social-plugins.line.me/lineit/share?url=%(url)s" target="_blank" rel="noopener">LINE</a><a href="#" id="copyLink">リンクをコピー</a></div>
      <a class="anext" href="%(nslug)s"><div class="ey">NEXT</div><div class="c"><div><div class="k">%(ncat)s ・ %(ndate)s</div><h3>%(ntitle)s</h3></div><img src="%(nimg)s" alt="" loading="lazy"></div></a>
    </article>
    <aside class="aside">
      <div class="toc"><div class="t">CONTENTS</div><ol>%(toc)s</ol></div>
      <div class="blk" style="margin-top:28px"><h2 data-en="RELATED">関連する記事</h2>
        <div class="arts">%(rel)s</div></div>
    </aside>
  </div>
  <div style="height:40px"></div>
</div></main>'''%dict(cat=esc(x['cat']),en=CAT_EN.get(x['cat'],'MAGAZINE'),pt='（理学療法士監修）' if x['pt'] else '',title=esc(x['title']),date=x['date'],mins=x['mins'],img=x['img'],lead=esc(x['lead']),body=x['body'],
        url=url,ttl=esc(x['title']),nslug=nxt['slug'],ncat=esc(nxt['cat']),ndate=nxt['date'],ntitle=esc(nxt['title']),nimg=nxt['img'],toc=toc,
        srcbox=('<div class="art-src"><div class="t">参考にした指針・提言</div><ul>'+''.join('<li>%s</li>'%esc(x) for x in x_srcs)+'</ul></div>') if x_srcs else '',
        aubox=('<div class="art-au"><span class="av"><img src="assets/logo-mark.svg" alt="" aria-hidden="true"></span><div><b>%s</b><p>%s</p></div></div>'%(esc(x_author[0]),esc(x_author[1]))) if x_author else '',
        rel=''.join('<a class="art" href="%s"><div class="b"><h3>%s</h3><div class="m"><b>%s</b>%s</div></div><img src="%s" alt="" loading="lazy"></a>'%(y['slug'],esc(y['title']),esc(y['cat']),y['date'].replace('.','/'),y['img']) for y in rel))
    js=ART_JS.replace('</script>','''
(function(){var c=document.getElementById('copyLink');if(!c)return;c.addEventListener('click',function(e){e.preventDefault();navigator.clipboard&&navigator.clipboard.writeText(location.href).then(function(){c.textContent='コピーしました'})})})();
</script>''')
    C.prodpage(x['slug'],x['title']+'｜チビスポ マガジン',x['desc'],BODY,css=ART_CSS+ART_EXTRA,js=js,scripts=('site.js?v='+C.V,'feature-track.js'),og_image='https://chibispo.com/'+x['img'])
print('articles:',[(x['n'],x['cat'],len(x['heads'])) for x in arts])
