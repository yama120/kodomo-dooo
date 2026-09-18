# プレビューの生成スクリプト（about_v2 / svc_hub / svc_listing / svc_ads / svc_sns / ct_v2 …）をそのまま流し、
# page() を本番用に差し替えて本番ページを吐く。リンクはプレビュー名→本番名に写像。
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
HREF={'video-hero-preview.html':'index.html','search-preview.html':'search.html','map-preview.html':'map.html','club-preview.html':'search.html',
 'magazine-preview.html':'magazine.html','article-preview.html':'magazine-4.html','partner-preview.html':'partner.html','shindan-preview.html':'index.html#shindan',
 'mypage-preview.html':'mypage.html','service-listing-preview.html':'listing.html','service-ads-preview.html':'service-ads.html','service-sns-preview.html':'service-sns.html',
 'club-mypage-preview.html':'club-mypage.html','register-preview.html':'register.html','login-preview.html':'login.html','admin-preview.html':'admin.html',
 'contact-preview.html':'contact.html','service-plans-preview.html':'plans.html','about-preview.html':'about.html','partner-preview-v1.html':'partner.html','preview-index.html':'index.html'}
PAGES={  # プレビューの出力名 → (本番名, description, options)
 'about-preview.html':('about.html','チビスポは「地域スポーツを、もっと身近に。」を掲げる、子どものスポーツクラブと保護者をつなぐメディアです。なぜ始めたのか、決めていること、運営者の想い。',{}),
 'partner-preview.html':('partner.html','クラブ・地域のお店・企業の方へ。チビスポへの掲載は無料。SNS運用サポート・ホームページ制作・地域の広告掲載など、必要なところだけ手伝います。',{}),
 'service-listing-preview.html':('listing.html','チビスポにクラブを載せる。掲載は無料。地域・種目・こだわりの検索に載り、体験の申込みがそのまま届きます。',{}),
 'service-ads-preview.html':('service-ads.html','地域の広告掲載。整骨院・スポーツ用品店・歯科など、地域のお店を「クラブを探している最中」の保護者に届けます。年額1本。',{}),
 'service-sns-preview.html':('service-sns.html','子どものスポーツクラブに特化したSNS運用サポート。投稿の型と頻度を決めて、最初の3本を一緒に出します。買い切り・月額なし。',{}),
 'service-plans-preview.html':('plans.html','チビスポの有料プラン。スタンダード¥3,000/月・プロ¥10,000/月で、地域で絞った検索の最初に出る・ほかの地域でもおすすめに出る・写真7〜15枚・閲覧数と申込の分析。実際の画面で説明します。',{}),
 'contact-preview.html':('contact.html','チビスポへの相談・お問い合わせ。クラブ運営者・地域のお店・保護者・取材など、相手に合わせた窓口です。',{'supabase':False}),
}
def maphref(html):
    for a,b in HREF.items(): html=html.replace('href="'+a,'href="'+b).replace("href='"+a,"href='"+b).replace("location.href='"+a,"location.href='"+b)
    html=html.replace('preview-quiz.js','quiz.js').replace('preview-quiz.css','quiz.css')
    return html
made=[]
def page(fname,title,body,css='',bodyattr='data-skin="bright"',extra_js=''):
    if fname not in PAGES: return
    out,desc,opt=PAGES[fname]
    body=re.sub(r'<div class="note"[^>]*>.*?</div>\n?','',body,flags=re.S)
    body=maphref(body); extra_js=maphref(extra_js)
    # プレビュー専用の切替パネル（HERO案 / BG案）は本番に出さない。JSは要素が無ければ何もしない前提で残す
    body=re.sub(r'<div class="(hsw|bgsw)" id="\1">.*?</div>\n?','',body,flags=re.S)
    assert 'id="hsw"' not in body and 'id="bgsw"' not in body
    title=re.sub(r'（[^）]*プレビュー[^）]*）','',title).replace('（v2）','').strip()
    left=sorted(set(re.findall(r'[a-z0-9-]+-preview[a-z0-9-]*\.html',body+extra_js)))
    if left: print('  !! 未写像のリンク',out,left)
    C.prodpage(out,title,desc,body,css=css,js=extra_js,scripts=('club-card.js?v='+C.V,'site.js?v='+C.V,'quiz.js?v='+C.V),head='<link rel="stylesheet" href="quiz.css?v='+C.V+'">\n',**opt)
    made.append(out)
src=open(P+'build_pages.py',encoding='utf-8').read(); src=src[:src.index("page('")]
g={'__name__':'prod_static','P':P}
exec(src,g); g['page']=page
for name in ['about_v2','svc_listing','svc_ads','svc_sns','svc_hub','ct_v2','svc_plans']:
    exec(open(P+name+'.py',encoding='utf-8').read(),g)
print('made:',made)
