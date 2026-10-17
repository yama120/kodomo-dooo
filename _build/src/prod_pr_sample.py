# 企業紹介記事の見本（pr-sample*.html）本番：旧ページ（_build/src/legacy/）の本文をそのまま prodpage に。営業時に見せるサンプル 4 本
import os,re,sys,glob
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
DESC='チビスポの企業紹介ページ（PR記事）の掲載イメージ。地域のお店・企業を、クラブを探している保護者に取材記事の形で届けます。※実在の店舗ではないサンプルです。'
for f in sorted(glob.glob(Lg.L+'pr-sample*.html')):
    name=os.path.basename(f); s=Lg.load(name)
    CSS='.prs-pg{background:#fff;color:#23303a;line-height:1.95}\n'+Lg.scope_css('\n'.join(Lg.head_styles(s)),'.prs-pg')
    out=C.prodpage(name,Lg.title(s),Lg.desc(s,DESC),'<main class="prs-pg">\n'+Lg.body(s)+'\n</main>',css=CSS,head=Lg.FONT_EXTRA)
    Lg.check(name,out,must_have=('pr-h2','service-ads.html'),must_not=('recruit-pr.html',))
