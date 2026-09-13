import re,os,sys
P='/private/tmp/claude-501/-Users-hyogoyamada-claudecode-project/5ae8baa4-4330-4bf8-b599-64aa8ac5ef83/scratchpad/'
sys.path.insert(0,P); import cards
D=os.path.expanduser('~/kodomo-dooo-deploy/')
top=open(D+'video-hero-preview.html',encoding='utf-8').read()
BASE_CSS=top[top.index('<style>')+7:top.index('</style>')]
header=top[top.index('<header>'):top.index('</header>')+9]
footer=top[top.index('<footer>'):top.index('</footer>')+9]
tail=top[top.index('<div id="skins">'):top.index('</body>')]
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&family=Zen+Old+Mincho:wght@600;900&family=Anton&display=swap" rel="stylesheet">'
page_css=open(P+'page.css',encoding='utf-8').read()
v2_css=open(P+'club_v2.css',encoding='utf-8').read()
body=open(P+'page.html',encoding='utf-8').read()

# 1) クラブ名の帯を .sec.s-head に（背後に地域×種目の英字）。基本情報までを帯に含める
i=body.index('  <div class="chead">'); j=body.index('  <div class="blk" style="margin-top:22px">')
mid=body[i:j]
body=body[:i]+'</div>\n<section class="sec chead-sec">\n  <div class="wrap">\n'+mid+'  </div>\n</section>\n<div class="wrap">\n'+body[j:]
# 2) 見出しに英字ラベル
EN={'このクラブのスタイル':'STYLE','写真':'PHOTOS','こんなお子様におすすめ':'FOR KIDS WHO','おすすめポイント':'HIGHLIGHTS','クラブからの紹介文':'MESSAGE','コーチ・スタッフ':'STAFF','コース':'COURSES','費用の内訳':'FEES','地図・アクセス':'ACCESS','口コミ':'REVIEWS','公式リンク':'LINKS','はじめての方へ':'FOR BEGINNERS'}
for jp,en in EN.items():
    body,n=re.subn(r'<h2>(%s)(<|\n|</h2>)'%re.escape(jp),r'<h2 data-en="%s">\1\2'%en,body,count=1)
    assert n==1,jp
# 3) 収益枠を検索結果 v2 と同じ節に
a=body.index('<div class="prband">'); b=body.index('<div class="wrap">\n  <div class="blk">\n    <h2 data-en="FOR BEGINNERS">')
rec=[cards.card(**dict(c,pr=(k<2))) for k,c in enumerate(cards.CLUBS[1:])]
pr='''<section class="sec sec-alt pr">
  <div class="wrap">
    <div class="eyebrow">NEARBY</div>
    <div class="sec-h"><h2>近くの<em>クラブ</em><span class="pr-lb">PRを含む</span></h2><span class="more">世田谷区・周辺で、いま募集しているクラブ</span></div>
    <div class="rec">
%s
    </div>
  </div>
</section>
<section class="sec pr" style="margin-top:0">
  <div class="wrap">
    <div class="eyebrow">LOCAL PARTNERS</div>
    <div class="sec-h"><h2>地域の<em>おすすめ</em>企業<span class="pr-lb">PR</span></h2><span class="more">世田谷区の子育て世帯に向けて</span></div>
    <div class="ads">
      <div class="a"><div class="lg">D</div><div class="t">デザインボックス<small>チームのユニフォーム制作</small></div></div>
      <div class="a"><div class="lg">S</div><div class="t">桜丘整骨院<small>スポーツ外傷・子ども割引</small></div></div>
      <div class="a"><div class="lg">K</div><div class="t">経堂スポーツ用品<small>ジュニア用品・名入れ無料</small></div></div>
      <div class="a"><div class="lg">M</div><div class="t">みどり歯科<small>マウスガード作成</small></div></div>
    </div>
    <div class="ads-more">この枠に掲載する事業者の方は <a href="partner-preview.html">掲載のご案内</a> へ。</div>
  </div>
</section>
'''%("\n".join(rec))
body=body[:a]+pr+body[b:]
# 4) 設計メモに v2 の要点を足す
body=body.replace('<div class="note">【クラブ詳細ページ】','<div class="note">【v2・2026-09-08】検索結果v2と同じ道具立て：クラブ名の背後の英字は<b>見にくいので無し</b>（ユーザー判断・検索結果は残す）／各見出しに<b>英字ラベル＋短い赤線＋細い下罫</b>／基本情報・口コミ・スタッフ・コース表を<b>箱から罫線へ</b>／収益枠は検索結果と同じ節（NEARBY／LOCAL PARTNERS・背景タイポなし）。★v1は <a href="club-preview-v1.html">club-preview-v1.html</a>。</div>\n  <div class="note">【クラブ詳細ページ】',1)

JS='''<script>
(function(){var st=document.getElementById('sticky'),c1=document.querySelector('.cta1'),c2=document.getElementById('cta2');
 if(st&&c1){var past1=false,see2=false;function upd(){st.classList.toggle('on',past1&&!see2)}
 new IntersectionObserver(function(e){past1=!e[0].isIntersecting&&e[0].boundingClientRect.top<0;upd()},{threshold:0}).observe(c1);
 if(c2)new IntersectionObserver(function(e){see2=e[0].isIntersecting;upd()},{threshold:.2}).observe(c2);}
 var pt=document.getElementById('paidToggle');if(pt)pt.addEventListener('click',function(){var on=document.body.classList.toggle('paid');pt.textContent=on?'プレビュー：有料（編集部おすすめ）表示 ▸ 無料に戻す':'プレビュー：無料プラン表示 ▸ 有料（編集部おすすめ）に切替'});
})();
</script>
'''
html=('<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<meta name="robots" content="noindex,nofollow">\n'
      '<title>わかばFC｜チビスポ（クラブ詳細プレビュー）</title>\n'+FONTS+'\n<link rel="stylesheet" href="preview-quiz.css">\n<style>'+BASE_CSS+page_css+v2_css+'</style>\n</head>\n<body data-skin="bright">\n\n'+header+'\n'+body+'\n'+footer+'\n\n'+tail+JS+'\n<script src="preview-quiz.js"></script>\n</body>\n</html>')
open(D+'club-preview.html','w',encoding='utf-8').write(html)
o=len(re.findall(r'<div\b',html)); c=len(re.findall(r'</div>',html))
print('club-preview.html',len(html)//1024,'KB div差',o-c)
