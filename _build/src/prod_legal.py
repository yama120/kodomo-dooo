# プライバシーポリシー・利用規約 本番：旧 legal.html（_build/src/legacy/）の本文を prodpage に載せ替える。#terms / #privacy のタブ切替 JS はそのまま
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('legal.html')
body,js=Lg.split_tail_scripts(Lg.body(s))
body=Lg.PACIFICO.sub(Lg.EYEBROW,body)
CSS='.lg-pg{background:#f6f7f9;color:#1f2a37}\n'+Lg.scope_css('\n'.join(Lg.head_styles(s)),'.lg-pg')
DESC='チビスポのプライバシーポリシー・利用規約・アカウント削除の手順・運営者情報。取得する情報と利用目的、口コミのルール、お問い合わせ先をまとめています。'
out=C.prodpage('legal.html',Lg.title(s),Lg.desc(s,DESC),'<main class="lg-pg">\n'+body+'\n</main>',css=CSS,js=js,head=Lg.FONT_EXTRA)
Lg.check('legal.html',out,must_have=('pane-privacy','pane-operator','tokushoho.html'),must_not=('Pacifico',))
