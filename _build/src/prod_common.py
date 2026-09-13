# 本番ページ生成の共通部品（2026-09-13〜）
#  - site.css   : 新デザイン全体の CSS（新ページが <link> で読む）
#  - chrome.css : ヘッダー・フッター・シートだけの CSS（shared.js が旧ページにも注入する）
#  - prodpage() : 本番ページの雛形（meta・GA4・フォント・site.css・ヘッダー/フッター直書き・shared.js）
import re,os,sys,json
P=os.path.dirname(os.path.abspath(__file__))+'/'
sys.path.insert(0,P)
import header_v2 as H
D=os.path.expanduser('~/kodomo-dooo-deploy/')
V='20260913'   # キャッシュ破り（site.css / chrome.css / shared.js / club-card.js）
LINKS=dict(home='index.html',search='search.html',map='map.html',about='about.html',partner='partner.html',fav='mypage.html#fav',clubmy='club-mypage.html',login='login.html',mypage='mypage.html',listing='listing.html',magazine='magazine.html',faq='faq.html',contact='contact.html',terms='legal.html#terms',privacy='legal.html#privacy',logo='assets/logo-sm.png')

top=open(D+'video-hero-preview.html',encoding='utf-8').read()
BASE_CSS=top[top.index('<style>')+7:top.index('</style>')]

def strip_preview(css):
    """スキン切替・設計メモなどプレビュー専用の CSS を落とし、BRIGHT を既定に畳む"""
    css=re.sub(r'body\[data-skin="(stadium|magazine|editorial)"\]\{[^}]*\}\n?','',css)   # 複数行のトークン塊
    out=[]
    for line in css.split('\n'):
        t=line.strip()
        if re.match(r'^body\[data-skin="(stadium|magazine|editorial)"\]',t): continue
        if re.match(r'^(#skins|#noteBtn|\.note\b|body\.notes)',t): continue
        if t.startswith('/* ===================== SKIN SWITCH'): continue
        line=line.replace('body[data-skin="bright"] ','')
        if line.startswith('header{'): line='header.site-hd{'+line[7:]
        out.append(line)
    return '\n'.join(out)

def block(css,start,end):
    a=css.index(start); b=css.index(end,a); return css[a:b]

SITE=strip_preview(BASE_CSS)
club_css=strip_preview(open(P+'page.css',encoding='utf-8').read())
bp=open(P+'build_pages.py',encoding='utf-8').read()
COMMON=strip_preview(bp[bp.index("COMMON='''")+10:bp.index("'''",bp.index("COMMON='''")+10)])
EXTRA='''
/* ---- 本番で足した分 ---- */
a.nc{color:inherit}
.nc-name{margin:0 0 5px}
.nc-fav.on svg{fill:var(--accent);stroke:var(--accent)}
.nc-ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.nc-ph svg{width:56px;height:56px;fill:none;stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round;opacity:.9}
'''
SITE_CSS='/* チビスポ 新デザイン共通CSS（生成物：_build/src/prod_common.py。直接編集しない） */\n'+SITE+club_css+COMMON+EXTRA

TOKENS=block(SITE,'/* ===================== TOKENS','/* ===================== MOTION')
HEAD_CSS=block(SITE,'/* ===================== HEADER','/* ===================== QUIZ BAND')
FOOT_CSS=block(SITE,'/* ===================== FOOTER','/* ===================== CLUB WALL')
CHROME_CSS=('/* チビスポ ヘッダー・フッター・メニュー（生成物：_build/src/prod_common.py。shared.js が旧ページにも注入する） */\n'
    +re.sub(r'\n\*\{box-sizing:border-box\}\nhtml,body\{[^}]*\}\nbody\{[^}]*\}\nimg,video\{[^}]*\}\na\{[^}]*\}\n\.wrap\{[^}]*\}','',TOKENS)
    +'.site-hd *,.site-ft *,.sheet *,.sh-bd{box-sizing:border-box}\n'
    '.site-hd,.site-ft,.sheet{font-family:var(--f);color:var(--ink);-webkit-font-smoothing:antialiased}\n'
    '.site-hd a,.site-ft a,.sheet a{color:inherit;text-decoration:none}\n'
    '.site-hd img,.site-ft img{display:block;max-width:100%}\n'
    '.site-hd .wrap,.site-ft .wrap{max-width:1180px;margin:0 auto;padding:0 20px}\n'
    +HEAD_CSS+FOOT_CSS)

HEADER_HTML=H.header_html(LINKS)+'</header>'
SHEET_HTML=H.sheet_html(LINKS)
FOOTER_HTML='''<footer class="site-ft">
  <div class="wrap ft">
    <div class="ft-l">
      <div class="ft-logo">チビ<span>スポ</span></div>
      <p>チビスポは、地域・種目・雰囲気から、お子さまに合うスポーツクラブが見つかるサービスです。地図で近くから探せて、体験の申込みもそのまま。</p>
      <div class="ft-sns">
        <a href="https://www.instagram.com/chibi_spo" target="_blank" rel="noopener">Instagram</a><a href="https://www.threads.com/@chibi_spo" target="_blank" rel="noopener">Threads</a>
      </div>
    </div>
    <div class="ft-r">
      <div class="ft-app">
        <img src="assets/app-hero/app-icon-512.webp" alt="チビスポ">
        <div class="tx">アプリなら新着の<br>クラブ情報が早く届く！</div>
        <a class="btn" href="https://apps.apple.com/jp/app/id6797169414" target="_blank" rel="noopener" data-app-store-cta>アプリを開く</a>
      </div>
      <div class="ft-links">
        <a href="about.html">チビスポとは</a><a href="faq.html">よくある質問</a><a href="legal.html#terms">利用規約</a><a href="legal.html#privacy">プライバシーポリシー</a><a href="contact.html">お問い合わせ</a><a href="partner.html">クラブ・事業者の方へ</a>
      </div>
    </div>
  </div>
  <div class="wrap ft-note">© 2026 Chibispo All Rights Reserved.</div>
</footer>'''

FONT_URL='https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@700;900&family=Zen+Old+Mincho:wght@600;900&family=Anton&display=swap'
HEAD_COMMON='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ffffff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="チビスポ">
<script>if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){})})}</script>
'''
GA='''<!-- GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5ZBBNYC37Y"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-5ZBBNYC37Y');
</script>
'''
def esc(s): return (s or '').replace('&','&amp;').replace('"','&quot;').replace('<','&lt;')
def prodpage(fname,title,desc,body,css='',js='',head='',supabase=False,noindex=False,og_image='https://chibispo.com/assets/ogp.jpg?v=1',canonical=None,bodyclass='',scripts=()):
    url='https://chibispo.com/'+('' if fname=='index.html' else fname)
    html=('<!DOCTYPE html>\n<html lang="ja">\n<head>\n'+HEAD_COMMON
      +'<title>'+esc(title)+'</title>\n<meta name="description" content="'+esc(desc)+'">\n'
      +('<meta name="robots" content="noindex,nofollow">\n' if noindex else '<link rel="canonical" href="'+(canonical or url)+'">\n')
      +'<meta property="og:type" content="website">\n<meta property="og:site_name" content="チビスポ">\n<meta property="og:title" content="'+esc(title)+'">\n<meta property="og:description" content="'+esc(desc)+'">\n<meta property="og:url" content="'+(canonical or url)+'">\n<meta property="og:image" content="'+og_image+'">\n<meta name="twitter:card" content="summary_large_image">\n'
      +'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="'+FONT_URL+'" rel="stylesheet">\n'
      +'<link rel="stylesheet" href="site.css?v='+V+'">\n'
      +('<style>'+css+'</style>\n' if css else '')+head+GA+'</head>\n'
      +'<body'+(' class="'+bodyclass+'"' if bodyclass else '')+'>\n'+HEADER_HTML+'\n'+body+'\n'+FOOTER_HTML+'\n'
      +('<script src="supabase-lite.js?v=20260731"></script>\n' if supabase else '')
      +''.join('<script src="%s"></script>\n'%s for s in scripts)
      +'<script src="shared.js?v='+V+'"></script>\n'+js+'\n</body>\n</html>')
    open(D+fname,'w',encoding='utf-8').write(html)
    o=len(re.findall(r'<div\b',html)); c=len(re.findall(r'</div>',html))
    miss=[m for m in set(re.findall(r'src="(assets/[^"?]+)',html)) if not os.path.exists(D+m)]
    print(f'{fname}: {len(html)//1024}KB div差={o-c} missing={miss}')
    return html

if __name__=='__main__':
    open(D+'site.css','w',encoding='utf-8').write(SITE_CSS)
    open(D+'chrome.css','w',encoding='utf-8').write(CHROME_CSS)
    print('site.css',len(SITE_CSS)//1024,'KB / chrome.css',len(CHROME_CSS)//1024,'KB')
    for bad in ['data-skin="stadium"','#skins','#noteBtn','.note{']:
        print(' ',bad,'残り:',SITE_CSS.count(bad),CHROME_CSS.count(bad))
