# ヒーロー h1 の強調（「やってみたい」）の色。既定はイメージカラー。環境変数 HL で差し替え
import os,re
HL=os.environ.get('HL','#C8FF00')
D=os.path.expanduser('~/kodomo-dooo-deploy/'); f=D+'video-hero-preview.html'
s=open(f,encoding='utf-8').read()
# 1) トークン
if '--hl:#' in s:
    s=re.sub(r'--hl:#[0-9A-Fa-f]{6}','--hl:'+HL,s)
else:
    s=s.replace("--accent2:#E43B4D;","--accent2:#E43B4D; --hl:"+HL+";",1)
# 2) スキン別の上書きも --hl に揃える（余計な text-shadow は落とす）
s=re.sub(r'body\[data-skin="(magazine|stadium)"\] \.hero h1 em\{[^}]*\}',
         lambda m:'body[data-skin="%s"] .hero h1 em{font-style:normal;color:var(--hl)}'%m.group(1),s)
# 3) 既定（BRIGHT／EDITORIAL）のルール：.hero h1 の直後に1行
base='.hero h1 em{font-style:normal;color:var(--hl);text-shadow:0 2px 20px rgba(0,0,0,.45)}\n'
if re.search(r'(?m)^\.hero h1 em\{',s):
    s=re.sub(r'(?m)^\.hero h1 em\{[^}]*\}\n',base,s,count=1)
else:
    k=s.index('.hero h1{font-family:var(--fh)'); e=s.index('\n',k)+1; s=s[:e]+base+s[e:]
open(f,'w',encoding='utf-8').write(s); print('hero highlight =',HL)
