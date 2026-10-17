# 特集（category-*.html）と種目紹介（sport-*.html）本番：旧ページの本文をそのまま prodpage に載せ替える
import os,re,sys,glob,html as H
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
names=sorted(os.path.basename(f) for f in glob.glob(Lg.L+'category-*.html')+glob.glob(Lg.L+'sport-*.html'))
for name in names:
    s=Lg.load(name)
    css=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.sp-pg')
    body=Lg.body(s)
    body=Lg.PACIFICO.sub(Lg.EYEBROW,body)
    # description が無いページは、ヒーローの説明文から
    hero_p=re.search(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>',body,re.S)
    desc=Lg.desc(s) or (H.unescape(re.sub(r'<[^>]+>','',hero_p.group(1))).strip() if hero_p else '')
    assert desc, name
    BODY='<main class="sp-pg">\n'+body+'\n</main>'
    CSS='.sp-pg{background:#f6f7f9;color:#1f2a37}\n'+css
    out=C.prodpage(name,Lg.title(s),desc,BODY,css=CSS,head=Lg.FONT_EXTRA)
    Lg.check(name,out,must_not=('Pacifico','shared.js?v=20261005'))
