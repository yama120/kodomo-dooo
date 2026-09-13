import os,sys,subprocess
P='/private/tmp/claude-501/-Users-hyogoyamada-claudecode-project/5ae8baa4-4330-4bf8-b599-64aa8ac5ef83/scratchpad/'
os.chdir(P)
exec(open(P+'build_pages.py',encoding='utf-8').read())
for s in ['search_v2','mag_v2','art_v2','sd_v3','mp_v2','svc_listing','svc_ads','svc_sns','svc_hub','cmp_v2','reg_v2','lg_v2','adm_v2','ct_v2','about_v2']:
    print('==',s); exec(open(P+s+'.py',encoding='utf-8').read())
print('== build_club'); subprocess.run([sys.executable,P+'build_club.py'],check=True)
