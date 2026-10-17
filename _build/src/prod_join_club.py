# クラブに参加する（スタッフ招待の受け口）本番：旧 join-club.html（_build/src/legacy/）。
# 旧ページは body を flex で中央寄せした単独カード。reset-password と同じく、共通ヘッダー／フッターの間にカードを置く。
# .card / .btn / .btn-ghost は site.css と衝突するので .jc- 接頭辞に。招待トークンの照合（インライン JS）は supabase-lite.js の後ろで
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('join-club.html')
RENAME={'card':'jc-card','btn':'jc-btn','btn-ghost':'jc-btn-ghost'}
body,js=Lg.split_tail_scripts(Lg.body(s))
body=Lg.rename_html(body,RENAME); js=Lg.rename_html(js,RENAME)
css=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.jc-pg',mode='all',rename=RENAME)
CSS='.jc-pg{background:#f5f7f9;color:#1f2430;padding:40px 16px 70px;display:flex;justify-content:center}\n'+css
out=C.prodpage('join-club.html',Lg.title(s),'クラブのスタッフ招待を受けて、チビスポのクラブ管理ページに参加します。',
    '<main class="jc-pg">\n'+body+'\n</main>',css=CSS,js=js,supabase=True,noindex=Lg.noindex(s),head=Lg.FONT_EXTRA)
Lg.check('join-club.html',out,must_have=('id="signupArea"','id="switchArea"','class="jc-btn jc-btn-ghost"','noindex'),must_not=('class="card"','class="btn"','class="btn btn-ghost"'))
