# アカウント削除の申請 本番：旧 account-delete.html（_build/src/legacy/）。ストアの審査で参照される説明ページ。
# 旧ページはヘッダー／フッター無しの単独ページ（shared.js も読んでいなかった）。共通ヘッダー／フッターを付け、.card / .btn は .ad- 接頭辞に
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('account-delete.html')
RENAME={'card':'ad-card','btn':'ad-btn'}
body=Lg.rename_html(Lg.PACIFICO.sub(Lg.EYEBROW,Lg.body(s)),RENAME)
CSS='.ad-pg{background:#f6f7f9;color:#1f2a37}\n'+Lg.scope_css('\n'.join(Lg.head_styles(s)),'.ad-pg',rename=RENAME)
out=C.prodpage('account-delete.html',Lg.title(s),Lg.desc(s),'<main class="ad-pg">\n'+body+'\n</main>',css=CSS,head=Lg.FONT_EXTRA)
Lg.check('account-delete.html',out,must_have=('class="ad-card"','class="ad-btn"','mailto:info@chibispo.com'),must_not=('class="card"','class="btn"','Pacifico'))
