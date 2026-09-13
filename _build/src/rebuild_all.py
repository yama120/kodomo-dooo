import os,sys,subprocess
P=(os.path.dirname(os.path.abspath(__file__))+'/') if '__file__' in globals() else P   # 部品は _build/src/ から読む
os.chdir(P)
exec(open(P+'build_pages.py',encoding='utf-8').read())
for s in ['search_v2','mag_v2','art_v2','sd_v3','mp_v2','svc_listing','svc_ads','svc_sns','svc_hub','cmp_v2','reg_v2','lg_v2','adm_v2','ct_v2','about_v2']:
    print('==',s); exec(open(P+s+'.py',encoding='utf-8').read())
print('== build_club'); subprocess.run([sys.executable,P+'build_club.py'],check=True)
