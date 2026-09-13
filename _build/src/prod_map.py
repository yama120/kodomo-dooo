# 地図 本番：map-preview.html（reskin_map.py の出力＝map.html の機械リスキン）から、プレビュー専用の部品を外して map.html に
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
s=open(D+'map-preview.html',encoding='utf-8').read()
# 設計メモ
s=re.sub(r'<div class="wrap" style="max-width:1460px;margin:0 auto;padding:0 20px"><div class="note">.*?</div></div>\n?','',s,flags=re.S)
assert 'class="note"' not in s
# スキン切替・設計メモボタン・プレビュー診断（tail）
a=s.index('<div id="skins">'); b=s.rindex('</body>')
s=s[:a]+s[b:]
s=s.replace('shared.js?v=20260731b','shared.js?v='+C.V)
s=s.replace('<meta name="robots" content="noindex,nofollow">\n','')
assert 'preview-quiz' not in s and 'noindex' not in s.split('<body')[0]
open(D+'map.html','w',encoding='utf-8').write(s); print('map.html',len(s)//1024,'KB')
