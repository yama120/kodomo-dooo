# 管理画面 本番：旧 admin.html（_build/src/legacy/）。運営者だけが開く。
# 旧ページはヘッダー／フッター無し（shared.js も無し）。共通ヘッダー／フッターを付け、ダッシュボード自身の <header>（赤帯）は .adm-pg の中だけに効かせる。
# .card / .btn は site.css と衝突するので .adm- 接頭辞に（JS のテンプレート文字列の class="…" も同じ置換）。
# :root のトークン（--bg --shadow --radius …）は site.css と名前が重なるので .adm-pg に閉じる。検索エンジンには出さない（noindex）
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('admin.html')
RENAME={'card':'adm-card','btn':'adm-btn'}
body,js=Lg.split_tail_scripts(Lg.body(s))
body=Lg.rename_html(body,RENAME); js=Lg.rename_html(js,RENAME)
css=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.adm-pg',mode='all',rename=RENAME)
css=css.replace('.adm-pg .login-wrap{min-height: 100vh;','.adm-pg .login-wrap{min-height: 60vh;')
assert '.adm-pg header{' in css and '.adm-pg{--primary' in css
CSS='.adm-pg{background:#f8fafc;color:#1e293b}\n'+css
HEAD=Lg.FONT_EXTRA+'<script src="cities.js?v=20260731b"></script>\n'
out=C.prodpage('admin.html',Lg.title(s),'チビスポの管理画面（運営者用）。','<main class="adm-pg">\n'+body+'\n</main>',css=CSS,js=js,supabase=True,noindex=True,head=HEAD)
Lg.check('admin.html',out,must_have=('id="loginWrap"','id="dashboard"','class="adm-btn btn-approve"','cities.js','supabase-lite.js'),must_not=('class="card"','class="btn"','class="btn btn-'))
