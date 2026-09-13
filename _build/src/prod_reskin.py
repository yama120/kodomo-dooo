# まだ作り直していない旧ページに、新デザインの書体と色だけ当てる（構造・JSは無改変）。
# ヘッダー・フッターは shared.js v2 が付ける。役目を終えたページはリダイレクトに。
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
ACC='#E43B4D'
BRAND=['#1f8a5b','#2270e0','#2563eb','#2a6fdb','#e8455f','#f0435c','#ea3b7e','#ff5fa2','#1a8fff','#ff4d8a','#ef4444']   # 旧のブランド色（緑・青・ピンク）→ 新の赤
SEMANTIC_GREEN=['#1f8a5b']   # club-mypage / admin では「成功」の意味で使うので残す
FONT_SUB={"'Zen Maru Gothic'":"'Zen Kaku Gothic New'","'Noto Sans JP'":"'Zen Kaku Gothic New'","'M PLUS Rounded 1c'":"'Zen Kaku Gothic New'",'Zen+Maru+Gothic':'Zen+Kaku+Gothic+New','Noto+Sans+JP':'Zen+Kaku+Gothic+New','M+PLUS+Rounded+1c':'Zen+Kaku+Gothic+New'}
def reskin(fname,keep_green=False,extra_css=''):
    s=open(D+fname,encoding='utf-8').read()
    if '<!-- reskin v2 -->' in s:   # 済みでも版番号だけ追従させる（共通CSS/JSの更新を確実に届ける）
        s2=re.sub(r'shared\.js\?v=\d+','shared.js?v='+C.V,s)
        if s2!=s: open(D+fname,'w',encoding='utf-8').write(s2); print('bump',fname)
        return
    head_end=s.index('</head>')
    for k,v in FONT_SUB.items(): s=s.replace(k,v)
    for c in BRAND: s=re.sub(re.escape(c),ACC,s,flags=re.I)
    if keep_green:   # 「成功」の意味で使っている緑だけ戻す（ボタンや枠の緑はブランド色なので赤に）
        for a,b in [("ok?'#E43B4D':'#c0314b'","ok?'#1f8a5b':'#c0314b'"),("'#E43B4D':'#c0314b'","'#1f8a5b':'#c0314b'"),("st.style.color='#E43B4D'","st.style.color='#1f8a5b'"),("solid #bfe6cf;color:#E43B4D","solid #bfe6cf;color:#1f8a5b"),("#16a34a","#16a34a")]:
            s=s.replace(a,b)
    s=s.replace('shared.js?v=20260731b','shared.js?v='+C.V)
    css='<!-- reskin v2 -->\n<style>body{font-family:\'Zen Kaku Gothic New\',system-ui,sans-serif!important;color:#2b2b2b}'+extra_css+'</style>\n'
    i=s.index('</head>'); s=s[:i]+css+s[i:]
    open(D+fname,'w',encoding='utf-8').write(s); print('reskin',fname)
def redirect(fname,to,title):
    html=('<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>%s</title>'
          '<link rel="canonical" href="https://chibispo.com/%s"><meta http-equiv="refresh" content="0;url=%s"><script>location.replace("%s")</script></head>'
          '<body><p style="font-family:sans-serif;padding:24px">移動しました： <a href="%s">%s</a></p></body></html>')%(title,to,to,to,to,title)
    open(D+fname,'w',encoding='utf-8').write(html); print('redirect',fname,'→',to)
for f in ['faq.html','legal.html','account-delete.html','reset-password.html','category-royal.html','category-personal.html','category-outdoor.html','category-minor.html','pr-sample.html','pr-sample-cafe.html','pr-sample-design.html','pr-sample-sports.html','trial.html','join-club.html']:
    if os.path.exists(D+f): reskin(f)
import glob
for f in sorted(glob.glob(D+'sport-*.html')): reskin(os.path.basename(f))
reskin('club-mypage.html',keep_green=True); reskin('admin.html',keep_green=True); reskin('dashboard/index.html',keep_green=True); reskin('dashboard/guide.html',keep_green=True)
redirect('recruit-pr.html','service-ads.html','地域の広告掲載｜チビスポ')
redirect('join.html','listing.html','クラブを載せる｜チビスポ')
redirect('team-lp.html','listing.html','クラブを載せる｜チビスポ')
