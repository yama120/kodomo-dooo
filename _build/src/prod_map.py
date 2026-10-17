# 地図から探す 本番：旧 map.html（_build/src/legacy/）の本文・Leaflet・地図ロジックをそのまま prodpage に載せ替える。
# 旧ページは head に「トークン＋スキン切替＋標準クラブカード＋旧ヘッダー／フッターの上書き」（reskin）、
# 「地図ページの新デザイン化」（reskin2 / reskin3）、「地図本体のレスポンシブ」の 4 つの <style> を持っていた。
#  - トークン・標準クラブカード（.nc）は site.css が持つので落とす。足りないトークン（--alt --r-s --r-xs --onaccent）だけ足す
#  - 旧ヘッダー（header[data-screen-label]）・下部タブバー（.cc-bottombar）・旧フッターへの上書きは、もう対象が無いので落とす
#  - スキン（data-skin）分岐は本番では bright 固定なので落とす
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C, prod_legacy as Lg
s=Lg.load('map.html')
styles=Lg.head_styles(s); assert len(styles)==4, len(styles)
reskin,reskin2,reskin3,page=styles
def lines(css,keep):
    return '\n'.join(l for l in css.split('\n') if keep(l))
def no_skin(l): return 'data-skin' not in l and 'data-screen-label' not in l and 'cc-bottombar' not in l and 'recruit-pr.html' not in l
# reskin：Leaflet のコントロール色・見出し書体・#cc-map だけ拾う
a=reskin.index('/* ---- Leaflet のコントロール ---- */'); r1=lines(reskin[a:],lambda l:no_skin(l) and not l.startswith('.note'))
r2=lines(reskin2,no_skin); r3=lines(reskin3,no_skin)
pg=lines(page,lambda l:no_skin(l) and 'body{padding-bottom:0' not in l)
CSS=(':root{--onaccent:#fff;--r-s:9px;--r-xs:6px;--alt:color-mix(in srgb,var(--ink) 4%,var(--bg))}\n'
     +Lg.scope_css(r1,'.mp-pg')+'\n'+Lg.scope_css(r2,'.mp-pg')+'\n'+Lg.scope_css(r3,'.mp-pg')+'\n'+Lg.scope_css(pg,'.mp-pg'))
# 旧の reskin が body で --alt を宣言していたのは「スキンごとに解決させる」ため。本番は bright 固定なので :root で良い
for bad in ('data-skin','data-screen-label','#skins','.note{','cc-bottombar'):
    assert bad not in CSS, bad
body=Lg.body(s)
body=body.replace('<!-- ヘッダーは shared.js で共通注入 -->\n','')
# 本文の inline <script> は 3 つ：地域企業の読み込み（本文中）・カルーセル矢印・地図本体。すべて Leaflet（head）だけに依存するので本文に残す
HEAD=('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
      '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n'
      '<script src="cities.js?v=20260731b"></script>\n')
out=C.prodpage('map.html',Lg.title(s),Lg.desc(s),'<div class="mp-pg">\n'+body+'\n</div>',css=CSS,head=HEAD)
Lg.check('map.html',out,must_have=('id="cc-leaflet"','id="cc-sheet"','mp-comp-sec','leaflet.js','cities.js'),must_not=('data-skin','M+PLUS+Rounded','shared.js?v=20261005','<!-- ヘッダーは shared.js'))
