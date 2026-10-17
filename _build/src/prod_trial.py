# 体験申し込み・お問い合わせ 本番：旧 trial.html（_build/src/legacy/）。
# 旧ページは自前のオレンジのヘッダー／フッターを持っていたので外し、サイト共通のヘッダー／フッターに載せる。
# フォーム本体は JS が #root に描く（Supabase REST を fetch で直接叩く・ライブラリ不要）。.card は site.css と衝突するので .tr-card に
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('trial.html')
RENAME={'card':'tr-card'}
body,js=Lg.split_tail_scripts(Lg.body(s))
body=re.sub(r'<header>.*?</header>\s*','',body,flags=re.S)
body=re.sub(r'<footer>.*?</footer>\s*','',body,flags=re.S)
body=Lg.rename_html(body,RENAME); js=Lg.rename_html(js,RENAME)
# 旧ヘッダーにあった見出しと戻り先は本文の先頭に
body=body.replace('<div class="container">','<div class="container">\n  <div class="tr-top"><a href="index.html">‹ トップへ戻る</a><h1>体験申し込み・お問い合わせ</h1></div>',1)
css=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.tr-pg',mode='all',rename=RENAME,drop=('.tr-pg header','header','header a','header a:hover','header h1','footer','footer a'))
CSS='''.tr-pg{background:var(--bg);color:var(--text);line-height:1.6}
.tr-pg .tr-top{margin:0 0 18px}
.tr-pg .tr-top a{font-size:12.5px;font-weight:700;color:var(--muted)}
.tr-pg .tr-top h1{font-family:var(--fh);font-size:clamp(22px,5.4vw,30px);font-weight:900;line-height:1.3;margin:6px 0 0}
'''+css
out=C.prodpage('trial.html',Lg.title(s),'クラブへの体験申し込みと質問はこちらから。希望日・お子さまの情報・保護者の連絡先を送ると、クラブから直接連絡が届きます。','<main class="tr-pg">\n'+body+'\n</main>',css=CSS,js=js,head=Lg.FONT_EXTRA)
Lg.check('trial.html',out,must_have=('id="root"','class="tr-card success-card"','trialForm'),must_not=('class="card"','<header>\n  <a href="/">'))
