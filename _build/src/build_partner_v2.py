# クラブ・事業者向け総合ページ v2（振り分け＋概要）を組む：listing.html の header/footer ＋ partner_v2_template.html → partner-v2-preview.html
# usage: python3 _build/src/build_partner_v2.py          → partner-v2-preview.html（noindex・PREVIEWバッジ・ヒーロー切替付き。*-preview.html は .gitignore）
#        python3 _build/src/build_partner_v2.py --prod   → partner.html（本番。2026-10-27 公開）
import re,os,sys
PROD='--prod' in sys.argv
repo=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/'
src=open(repo+'listing.html',encoding='utf-8').read()
header=re.search(r'<header class="site-hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="site-ft">.*?</footer>',src,re.S).group(0)
tpl=open(os.path.join(os.path.dirname(__file__),'partner_v2_template.html'),encoding='utf-8').read()
if PROD:
    if 'id="lx-hsw"' in tpl: raise SystemExit('切替UIが残っている。ヒーローを1案に固定してから --prod')
    tpl=re.sub(r'<meta name="robots"[^>]*>\n?','',tpl); tpl=re.sub(r'<div class="lx-pv-badge">.*?</div>\n?','',tpl,flags=re.S); tpl=tpl.replace('（プレビュー）</title>','</title>')
    og=('<link rel="canonical" href="https://chibispo.com/partner.html">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="チビスポ">\n'
        '<meta property="og:title" content="クラブ・事業者の方へ｜地域のクラブと、地域のお店を、近くの家族へ｜チビスポ">\n'
        '<meta property="og:description" content="チビスポは、保護者が地域と種目でスポーツクラブを探すサイトです。クラブは無料で載せられます。お店・企業は、探している最中の家族に地域の広告として届きます。">\n'
        '<meta property="og:url" content="https://chibispo.com/partner.html">\n<meta property="og:image" content="https://chibispo.com/assets/ogp.jpg?v=2">\n<meta name="twitter:card" content="summary_large_image">\n')
    tpl=tpl.replace('<link rel="stylesheet" href="site.css?v=20261004">',og+'<link rel="stylesheet" href="site.css?v=20261004">',1)
    for bad in ('noindex','PREVIEW ・ 本番未反映','（プレビュー）'):
        if bad in tpl: raise SystemExit('still contains: '+bad)
out=tpl.replace('{{HEADER}}',header).replace('{{FOOTER}}',footer)
dst=repo+('partner.html' if PROD else 'partner-v2-preview.html')
open(dst,'w',encoding='utf-8').write(out); print('written',dst,len(out))
