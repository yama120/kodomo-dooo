# パスワード再設定 本番：旧 reset-password.html（_build/src/legacy/）。
# 旧ページは body を flex で中央寄せした単独カードだったので、サイト共通のヘッダー／フッターの間にカードを置く形に。
# .card / .btn は site.css と衝突するので .rp-card / .rp-btn に。Supabase の処理（インライン JS）は supabase-lite.js の後ろで走らせる
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('reset-password.html')
RENAME={'card':'rp-card','btn':'rp-btn'}
body,js=Lg.split_tail_scripts(Lg.body(s))
body=Lg.rename_html(body,RENAME); js=Lg.rename_html(js,RENAME)
css=Lg.scope_css('\n'.join(Lg.head_styles(s)),'.rp-pg',mode='all',rename=RENAME)
CSS='.rp-pg{background:#f5f7f9;color:#1f2430;padding:40px 16px 70px;display:flex;justify-content:center}\n'+css
out=C.prodpage('reset-password.html',Lg.title(s),'チビスポのパスワード再設定。登録しているメールアドレスに再設定用のリンクをお送りします。',
    '<main class="rp-pg">\n'+body+'\n</main>',css=CSS,js=js,supabase=True,noindex=True,head=Lg.FONT_EXTRA)
Lg.check('reset-password.html',out,must_have=('id="formArea"','id="requestArea"','class="rp-btn"','supabase-lite.js'),must_not=('class="card"','class="btn"'))
