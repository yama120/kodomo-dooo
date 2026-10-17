# 本番ページを全部作り直す（順番が大事：プレビューのCSS → 共通 → 各ページ → 地域ページ → サイトマップ）
import os,subprocess,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; D=os.path.expanduser('~/kodomo-dooo-deploy/')
HL='#E43B4D'   # ヒーローの強調色（イメージカラー）
def run(f,env=None):
    e=dict(os.environ); e.update(env or {})
    r=subprocess.run([sys.executable,P+f],capture_output=True,text=True,env=e,cwd=P)
    tag='OK ' if r.returncode==0 else 'NG '
    print(tag+f, (r.stdout.strip().splitlines() or [''])[-1][:90])
    if r.returncode: print(r.stderr.strip()[-500:]); sys.exit(1)
# 1) プレビューのTOP（＝共通CSSの元）
for f in ['header_v2.py','top_quiz.py']: run(f)
run('top_hero.py',{'HL':HL})
# 2) 共通部品
for f in ['prod_common.py','prod_shared.py']: run(f)
# 3) 各ページ
for f in ['prod_index.py','prod_search.py','prod_club.py','prod_static.py','prod_login.py','prod_mypage.py','prod_register.py','prod_magazine.py','prod_quiz.py','prod_404.py']: run(f)
# 3b) 旧世代ページ（2026-10-17 に prodpage へ載せ替え。原稿は _build/src/legacy/、共通部品は prod_legacy.py）
for f in ['prod_map.py','prod_sports.py','prod_faq.py','prod_legal.py','prod_trial.py','prod_account_delete.py','prod_reset_password.py','prod_join_club.py','prod_club_mypage.py','prod_admin.py','prod_pr_sample.py']: run(f)
# 3c) まだ載せ替えていない旧ページ（dashboard/）の書体・色当てとリダイレクト
run('prod_reskin.py')
# 4) 地域ページとサイトマップ
for cmd in [['node','build-area-pages.mjs'],['node','build-sitemap.mjs']]:
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=D); print(('OK ' if r.returncode==0 else 'NG ')+cmd[1], r.stdout.strip().splitlines()[-1][:80] if r.stdout.strip() else '')
    if r.returncode: print(r.stderr[-400:]); sys.exit(1)
# 5) 目視できない取りこぼしの確認
import re
idx=open(D+'index.html',encoding='utf-8').read(); css=open(D+'site.css',encoding='utf-8').read()
print('確認 →','--hl:',re.search(r'--hl:#[0-9A-Fa-f]{6}',css).group(0),'| --accent:',re.search(r'--accent:#[0-9A-Fa-f]{6}',css).group(0),'| logo-wide:',idx.count('logo-wide.webp'),'| v:',re.search(r'site\.css\?v=(\d+)',idx).group(1),'| skin残:',css.count('data-skin="stadium"'))
