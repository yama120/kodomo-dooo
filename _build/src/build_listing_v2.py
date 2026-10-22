# クラブ向け掲載LP v2（プレビュー）を組む：listing.html の header/footer ＋ listing_v2_template.html ＋ assets/listing-v2/credits.json → listing-v2-preview.html（*-preview.html は .gitignore で本番に出ない）
# usage: python3 _build/src/build_listing_v2.py          → listing-v2-preview.html（noindex・PREVIEWバッジ付き）
#        python3 _build/src/build_listing_v2.py --prod   → listing.html（本番。2026-10-22 公開）
import re,json,os,html,sys
PROD='--prod' in sys.argv
repo=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/'
src=open(repo+'listing.html',encoding='utf-8').read()
header=re.search(r'<header class="site-hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="site-ft">.*?</footer>',src,re.S).group(0)
credits=json.load(open(repo+'assets/listing-v2/credits.json'))
short={'tresaja-gk':'トレサージャGKスクール','dazaifu-onigokko':'太宰府市スポーツ鬼ごっこクラブ','grow-doubledutch':'ダブルダッチスクール GROW UP！','fukui-karate':'和道会福井県本部 技道塾','star-sapporo':'STARアカデミー札幌白石','jasper-doubledutch':'JASPERダブルダッチスクール','coolrunnings':'COOLRUNNINGS 陸上スクール','fukuyama-redarrows':'福山レッドアローズ','bloom-dance':'Bloom Dance Circle','kairon-kendo':'KAIRON武導スクール','bjj-sapporo':'ブラジリアン柔術 手稲キッズクラブ','dream-baton':'Dream Baton Twirlers','kbbc-badminton':'スポーツクラブKBBC','orca-gym':'スポーツクラブ・オルカ','kidsball-nagakute':'キッズボールスポーツ教室','minoo-redstars':'箕面船場レッドスターズ'}
order=['tresaja-gk','kairon-kendo','grow-doubledutch','star-sapporo','minoo-redstars','fukui-karate','bloom-dance','coolrunnings','jasper-doubledutch','dream-baton','fukuyama-redarrows','kbbc-badminton','dazaifu-onigokko','bjj-sapporo','orca-gym','kidsball-nagakute']
cm={c['slug']:c for c in credits}
wall=''
for s in order:
    c=cm[s]; w,h=c['size']
    wall+=f'<a class="lx-wi lx-rv" href="club.html?id={c["id"]}"><img loading="lazy" decoding="async" src="assets/listing-v2/club-{s}.webp" width="{w}" height="{h}" alt="{html.escape(short[s])}（{html.escape(c["sport"])}・{html.escape(c["city"])}）"><span class="lx-wc"><b>{html.escape(short[s])}</b><i>{html.escape(c["sport"])} ・ {html.escape(c["city"])}</i></span></a>\n'
igs=[('ig-0','501st Basketball Club','埼玉県草加市 ・ バスケットボール'),('ig-6','SKY FORCE DANCE STUDIO','埼玉県入間市 ・ ダンス'),('ig-3','トレサージャGKスクール','千葉県松戸市・船橋市 ・ サッカー'),('ig-4','Dream Baton Twirlers','千葉県柏市 ・ バトントワーリング'),('ig-2','松伏サンズ','埼玉県松伏町 ・ バスケットボール'),('ig-1','キッズボールスポーツ教室','愛知県長久手市 ・ マルチスポーツ'),('ig-5','白井冨士FC','千葉県白井市 ・ サッカー')]
ig=''.join(f'<figure class="lx-igi lx-rv"><img loading="lazy" decoding="async" src="assets/listing-v2/{f}.webp" width="640" height="800" alt="Instagram投稿：{html.escape(n)}"><figcaption><b>{html.escape(n)}</b><i>{html.escape(m)}</i></figcaption></figure>' for f,n,m in igs)
tpl=open(os.path.join(os.path.dirname(__file__),'listing_v2_template.html'),encoding='utf-8').read()
if PROD:
    tpl=re.sub(r'<meta name="robots"[^>]*>\n?','',tpl)
    tpl=re.sub(r'<div class="lx-pv-badge">.*?</div>\n?','',tpl,flags=re.S)
    tpl=tpl.replace('（プレビュー）</title>','</title>')
    og=('<link rel="canonical" href="https://chibispo.com/listing.html">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="チビスポ">\n'
        '<meta property="og:title" content="クラブを載せる｜地域のクラブを、近くの子供たちへ｜チビスポ">\n'
        '<meta property="og:description" content="チビスポにクラブを載せると、地域と種目でクラブを探す保護者に、検索・地図・Instagram・アプリ通知で届きます。掲載は無料、登録は1〜2分、写真1枚から。">\n'
        '<meta property="og:url" content="https://chibispo.com/listing.html">\n<meta property="og:image" content="https://chibispo.com/assets/ogp.jpg?v=2">\n<meta name="twitter:card" content="summary_large_image">\n')
    tpl=tpl.replace('<link rel="stylesheet" href="site.css?v=20261004">',og+'<link rel="stylesheet" href="site.css?v=20261004">',1)
    for bad in ('noindex','PREVIEW ・ 本番未反映','（プレビュー）'):
        if bad in tpl: raise SystemExit('still contains: '+bad)
out=tpl.replace('{{HEADER}}',header).replace('{{FOOTER}}',footer).replace('{{WALL}}',wall).replace('{{IG}}',ig)
dst=repo+('listing.html' if PROD else 'listing-v2-preview.html')
open(dst,'w',encoding='utf-8').write(out)
print('written',dst,len(out))
