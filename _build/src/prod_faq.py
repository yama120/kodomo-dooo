# よくある質問 本番：旧 faq.html（_build/src/legacy/）の本文を prodpage に載せ替える。タブ切替の JS はそのまま
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('faq.html')
body,js=Lg.split_tail_scripts(Lg.body(s))
body=Lg.PACIFICO.sub(Lg.EYEBROW,body)
CSS='.fq-pg{background:#f6f7f9;color:#1f2a37}\n'+Lg.scope_css('\n'.join(Lg.head_styles(s)),'.fq-pg')
out=C.prodpage('faq.html',Lg.title(s),Lg.desc(s),'<main class="fq-pg">\n'+body+'\n</main>',css=CSS,js=js,head=Lg.FONT_EXTRA)
Lg.check('faq.html',out,must_have=('fq-tab','sec-club'),must_not=('Pacifico',))
