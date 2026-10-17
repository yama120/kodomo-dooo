# クラブ マイページ 本番：旧 club-mypage.html（_build/src/legacy/）の本文・CSS・JS をそのまま prodpage に載せ替える。
# ★ v3（2026-09-25）で手当てした見た目・JS が大量にある。原稿は legacy/ の 1 枚だけ。生成物の club-mypage.html を直接編集しない。
# スクリプトの順番：本文中の小さな <script>（起動ベール・ログイン見出しの連動）はそのまま →
#   supabase-lite.js（prodpage）→ shared.js（prodpage）→ 本体 IIFE ＋ v3 の IIFE（js=）。
#   旧ページは本体 IIFE を shared.js の前に走らせていたが、shared.js はこの IIFE に依存せず、v3 側は mp:team イベントで動くので順番を変えても良い。
# :root のトークン（--bg:#f7f7f8 など）は .cmp-pg（本文ラッパー）に閉じる。ヘッダー・フッターは site.css のトークンのまま
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('club-mypage.html')
body=Lg.body(s)
# 末尾の 2 本（本体 IIFE・v3 IIFE）を切り出す。間にあった shared.js のタグは Lg.body が外している
body,js=Lg.split_tail_scripts(body)
# ログイン見出しの連動（MutationObserver）は #mp-login の直後で動かすものなので本文に戻す
m=re.match(r'(<script>new MutationObserver.*?</script>)\s*',js,re.S); assert m
body=body+'\n'+m.group(1); js=js[m.end():]
assert js.count('<script>')==2, js.count('<script>')
assert 'mp-veil' in body and 'MutationObserver' in body
CSS=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.cmp-pg')
assert ':root' not in CSS and '.cmp-pg a{' in CSS
CSS='.cmp-pg{background:var(--bg);color:var(--ink)}\n'+CSS
# 旧ページには description が無かった
DESC='クラブ運営者のマイページ。掲載情報・写真・体験申込・プランの管理はこちらから。'
out=C.prodpage('club-mypage.html',Lg.title(s),DESC,'<div class="cmp-pg">\n'+body+'\n</div>',css=CSS,js=js,supabase=True,head=Lg.FONT_EXTRA)
Lg.check('club-mypage.html',out,must_have=('id="mp-login"','id="mp-veil"','manage-subscription','mp:team','api.chibispo.com'),must_not=('shared.js?v=20261005',))
