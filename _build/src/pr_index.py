# ---- 企業紹介ページの一覧（pr/index.html → https://chibispo.com/pr/）2026-10-17 新設
#   python3 pr_index.py
#   会社を足す／外す：下の COMPANIES に1件足す（listed=False で非表示）。本文は各社の pr/<slug>.html から転記する
#   ★クラス名はすべて prl- 接頭辞（site.css の .pri .pr .sec .chip 等と衝突させない）
#   ★雑誌一覧（magazine.html）と同じ道具立て：Anton の輪郭文字＋墨＋赤1色。写真は各社ページの実物だけ使う
import os,sys,html as H
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
esc=lambda s:H.escape(str(s or ''),quote=True)

COMPANIES=[
  dict(slug='armoury', listed=False,   # ★2026-10-17 ユーザー決定：本番の一覧にはまだ載せない
       name='ARMOURY', kana='アーマリー', ey='TEAM UNIFORM', cat='ユニフォーム',
       img='assets/pr/armoury/soccer-134-f.webp', img2='assets/pr/armoury/soccer-134-b.webp', pos='50% 12%',
       h='1着で、2チーム分。<br>表と裏で、2つのユニフォーム。',
       lead='表と裏で色もデザインも違う「両面ユニフォーム」を、チーム単位でオーダー制作。韓国発のチームウェアブランドの日本法人が、スポーツクラブの注文を受け付けています。',
       pts=['「両面」は見た目の仕掛けではなく、運営の仕掛け','「決めきれない」を減らすデザイン番号方式','4年かけて特許まで行った本気度'],
       place='東京都渋谷区 ／ 全国（オンライン）', note='表と裏'),
  dict(slug='daedal', listed=True,
       name='DAEDAL.', kana='ディーデル', ey='BASEBALL GEAR', cat='野球用品',
       img='assets/pr/daedal/p-uniform-team.webp', pos='50% 50%',
       h='道具の値段で、<br>野球を諦めさせない。',
       lead='デザインを自由に決められるユニフォームから、オーダーグラブ、バッティンググローブ、打者用防具まで。高校2年生が立ち上げた野球ブランド。',
       pts=['「値段で諦める選手を減らしたい」から始まっている','「色で選べる」が、そのまま個性になる','ユニフォームからグラブまで、チームで揃えられる'],
       place='千葉県柏市 ／ 全国（オンライン）'),
  dict(slug='makkiedrops', listed=True,
       name='makkiedrops design', kana='マッキードロップスデザイン', ey='DESIGN & GOODS', cat='デザイン・グッズ',
       img='assets/pr/makkiedrops/g-handball.webp', pos='50% 55%',
       h='スポーツの現場を知るデザイナーが、<br>チームの「ほしい」を形にする。',
       lead='ロゴ、部員募集のポスターやチラシ、卒団記念のグッズまで。奈良・生駒のスポーツ専門デザイン事務所。全国から依頼できます。',
       pts=['選手だった人が作っている','プロチームと同じ作り手に、地域のクラブが頼める','デザインからグッズの現物まで1か所で'],
       place='奈良県生駒市 ／ 全国対応'),
]

CSS=r'''
.prl{--ink:#2b2b2b;--sub:#6a7385;--line:#ececec;--acc:#E43B4D;--k:#101216;--f:'Zen Kaku Gothic New',system-ui,sans-serif;color:var(--ink);line-height:1.85}
.prl *{box-sizing:border-box}
.prl .prl-w{max-width:1180px;margin:0 auto;padding:0 20px}
/* 見出し帯（マガジン一覧と同じ輪郭文字） */
.prl-head{padding:28px 0 0}
.prl-head .prl-big{font-family:'Anton',sans-serif;font-size:clamp(54px,16vw,150px);line-height:.9;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px var(--ink);margin-bottom:14px}
.prl-head .prl-k{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--acc);margin-bottom:8px}
.prl-head .prl-k::before{content:"";width:22px;height:2px;background:var(--acc)}
.prl-head .prl-k i{font-style:normal;display:inline-block;font-size:9.5px;letter-spacing:.12em;color:var(--sub);border:1px solid var(--line);padding:2px 6px;border-radius:3px;line-height:1.4}
.prl-head h1{font-family:var(--f);margin:0;font-size:clamp(22px,5.4vw,38px);font-weight:900;letter-spacing:-.01em;line-height:1.3}
.prl-head h1 em{font-style:normal;color:var(--acc)}
.prl-head .prl-ld{margin-top:10px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9;max-width:720px}
.prl-cats{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin-top:18px;padding:14px 0 4px;border-top:2px solid var(--ink)}
.prl-cats::-webkit-scrollbar{display:none}
.prl-cats button{flex:none;font-family:var(--f);display:inline-flex;align-items:center;gap:6px;border:1px solid var(--ink);background:#fff;color:var(--ink);border-radius:999px;padding:8px 13px;font-size:12.5px;font-weight:900;cursor:pointer;white-space:nowrap}
.prl-cats button.on{background:var(--ink);color:#fff}
.prl-cats button small{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.08em;font-weight:400;opacity:.7}
/* 一覧：1社＝1見開き */
.prl-list{display:grid;gap:34px;margin-top:22px;counter-reset:c}
.prl-c{counter-increment:c;display:block;color:inherit;text-decoration:none;border-top:1px solid var(--line);padding-top:18px}
.prl-c[hidden]{display:none}
.prl-c .prl-ph{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:4/3;background:var(--k)}
.prl-c .prl-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;transition:opacity .6s ease,transform .8s ease}
.prl-c .prl-ph img.b{opacity:0}
.prl-c .prl-no{position:absolute;right:14px;top:10px;z-index:2;font-family:'Anton',sans-serif;font-size:44px;line-height:1;color:transparent;-webkit-text-stroke:1.2px rgba(255,255,255,.8)}
.prl-c .prl-no::before{content:counter(c,decimal-leading-zero)}
.prl-c .prl-pr{position:absolute;left:12px;top:12px;z-index:2;background:rgba(0,0,0,.72);color:#fff;font-family:'Anton',sans-serif;font-size:9.5px;letter-spacing:.12em;padding:4px 8px;border-radius:3px}
.prl-c .prl-flip{position:absolute;left:12px;bottom:12px;z-index:2;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.92);color:var(--k);font-size:10.5px;font-weight:900;letter-spacing:.06em;padding:5px 9px;border-radius:999px}
.prl-c .prl-flip i{font-style:normal;width:7px;height:7px;border-radius:50%;background:var(--acc)}
.prl-c .prl-t{padding:14px 2px 0}
.prl-c .prl-ey{display:flex;justify-content:space-between;align-items:baseline;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--acc)}
.prl-c .prl-ey small{font-family:var(--f);font-size:11px;font-weight:700;letter-spacing:0;color:var(--sub)}
.prl-c .prl-brand{margin:8px 0 2px;font-family:'Anton',sans-serif;font-size:clamp(26px,6.6vw,40px);letter-spacing:.03em;line-height:1;color:var(--ink)}
.prl-c .prl-brand small{display:block;font-family:var(--f);font-size:11.5px;font-weight:700;letter-spacing:.16em;color:var(--sub);margin-top:6px}
.prl-c h2{font-family:var(--f);margin:12px 0 8px;font-size:clamp(17px,4.6vw,24px);font-weight:900;line-height:1.5;letter-spacing:-.01em}
.prl-c .prl-lead{margin:0;font-size:13.5px;font-weight:700;color:var(--sub);line-height:1.85}
.prl-c .prl-pts{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:7px}
.prl-c .prl-pts li{position:relative;padding-left:30px;font-size:13.5px;font-weight:700;line-height:1.6}
.prl-c .prl-pts li::before{content:counter(p,decimal-leading-zero);counter-increment:p;position:absolute;left:0;top:3px;font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.06em;color:var(--acc)}
.prl-c .prl-pts{counter-reset:p}
.prl-c .prl-pts .prl-ptk{display:block;font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.24em;color:var(--sub);padding-left:0;margin-bottom:2px}
.prl-c .prl-pts .prl-ptk::before{content:none}
.prl-c .prl-go{display:inline-flex;align-items:center;gap:8px;margin-top:16px;font-size:13.5px;font-weight:900;color:var(--ink);border-bottom:2px solid var(--acc);padding-bottom:3px}
.prl-c .prl-go::after{content:"›";color:var(--acc);font-size:18px;line-height:1}
/* 下：募集 */
.prl-cta{margin:56px 0 0;border:1px solid var(--ink);padding:24px 20px 22px;position:relative;overflow:hidden;background:#fff}
.prl-cta .prl-bigk{position:absolute;right:-6px;top:-18px;font-family:'Anton',sans-serif;font-size:clamp(64px,18vw,140px);line-height:1;color:transparent;-webkit-text-stroke:1px var(--line);pointer-events:none;user-select:none}
.prl-cta .prl-k{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--acc);margin-bottom:8px}
.prl-cta .prl-k::before{content:"";width:22px;height:2px;background:var(--acc)}
.prl-cta h2{font-family:var(--f);margin:0 0 8px;font-size:clamp(19px,4.8vw,26px);font-weight:900;line-height:1.4;position:relative}
.prl-cta h2 em{font-style:normal;color:var(--acc)}
.prl-cta p{margin:0 0 16px;font-size:13.5px;font-weight:700;color:var(--sub);line-height:1.85;position:relative;max-width:560px}
.prl-cta .prl-btn{display:inline-block;background:var(--acc);color:#fff;font-weight:900;font-size:14.5px;padding:13px 26px;border-radius:999px;text-decoration:none;box-shadow:0 10px 24px rgba(228,59,77,.3);position:relative}
.prl-disc{margin:22px 0 0;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.8}
.prl-back{text-align:center;margin:26px 0 60px;font-size:13px;font-weight:700}
.prl-back a{color:var(--sub);text-decoration:none;margin:0 10px}
.prl-back a:hover{color:var(--acc)}
/* 動き：ARMOURY の表⇄裏（hover できる端末は hover、できない端末はゆっくり自動） */
@media(hover:hover){
  .prl-c:hover .prl-ph img.f{transform:scale(1.03)}
  .prl-c.has2:hover .prl-ph img.f{opacity:0}
  .prl-c.has2:hover .prl-ph img.b{opacity:1}
}
@media(hover:none){
  .prl-c.has2 .prl-ph img.b{animation:prlflip 7s ease-in-out infinite}
}
@keyframes prlflip{0%,42%{opacity:0}50%,92%{opacity:1}100%{opacity:0}}
@media(prefers-reduced-motion:reduce){.prl-c.has2 .prl-ph img.b{animation:none}}
/* デスクトップ：写真と文章を左右に。番号で左右を入れ替える */
@media(min-width:760px){
  .prl-head{padding-top:38px}
  .prl-head h1 br{display:none}
  .prl-list{gap:0;margin-top:28px}
  .prl-c{display:grid;grid-template-columns:1.05fr 1fr;gap:0 44px;align-items:center;padding:34px 0;border-top:1px solid var(--line)}
  .prl-c:nth-child(even) .prl-ph{order:2}
  .prl-c .prl-ph{aspect-ratio:4/3;border-radius:18px}
  .prl-c .prl-no{font-size:64px;right:22px;top:16px}
  .prl-c .prl-t{padding:0}
  .prl-c .prl-pts li{font-size:14px}
  .prl-cta{padding:34px 36px 32px}
}
'''

def card(c):
    has2=bool(c.get('img2'))
    o=[]
    o.append('<a class="prl-c%s" href="pr/%s.html" data-cat="%s">'%(' has2' if has2 else '',c['slug'],esc(c['cat'])))
    o.append('<div class="prl-ph"><span class="prl-pr">PR</span><span class="prl-no"></span>')
    o.append('<img class="f" loading="lazy" decoding="async" src="%s" alt="%s" style="object-position:%s">'%(esc(c['img']),esc(c['name']),esc(c.get('pos','50% 50%'))))
    if has2:
        o.append('<img class="b" loading="lazy" decoding="async" src="%s" alt="" style="object-position:%s">'%(esc(c['img2']),esc(c.get('pos','50% 50%'))))
        o.append('<span class="prl-flip"><i></i>%s</span>'%esc(c.get('note','表と裏')))
    o.append('</div>')
    o.append('<div class="prl-t">')
    o.append('<div class="prl-ey">%s<small>%s</small></div>'%(esc(c['ey']),esc(c['place'])))
    o.append('<div class="prl-brand">%s<small>%s ｜ %s</small></div>'%(esc(c['name']),esc(c['kana']),esc(c['cat'])))
    o.append('<h2>%s</h2>'%c['h'])
    o.append('<p class="prl-lead">%s</p>'%esc(c['lead']))
    o.append('<ul class="prl-pts"><li class="prl-ptk">取材してわかった3つのポイント</li>'+''.join('<li>%s</li>'%esc(p) for p in c['pts'])+'</ul>')
    o.append('<span class="prl-go">紹介ページを読む</span>')
    o.append('</div></a>')
    return '\n'.join(o)

def build():
    cs=[c for c in COMPANIES if c.get('listed',True)]
    cats=[]
    for c in cs:
        if c['cat'] not in cats: cats.append(c['cat'])
    chips='<button type="button" class="on" data-cat="">すべて</button>'+''.join('<button type="button" data-cat="%s">%s</button>'%(esc(k),esc(k)) for k in cats)
    body='''<main class="prl">
<section class="prl-head"><div class="prl-w">
  <div class="prl-big">PARTNERS</div>
  <div class="prl-k">CHIBISPO ・ COMPANIES <i>PR</i></div>
  <h1>チームの「ほしい」に、<br><em>応えてくれる</em>会社。</h1>
  <p class="prl-ld">ユニフォーム、野球用品、ロゴやグッズのデザイン。チビスポ編集部が取材して書いた企業紹介ページを、1か所に集めました。クラブの運営者にも、道具を揃える保護者にも。</p>
  <div class="prl-cats" id="prlCats">%s</div>
</div></section>
<div class="prl-w">
  <div class="prl-list" id="prlList">
%s
  </div>
  <section class="prl-cta">
    <div class="prl-bigk">LOCAL AD</div>
    <div class="prl-k">FOR LOCAL BUSINESS</div>
    <h2>あなたの会社も、<em>こんなページ</em>で紹介しませんか。</h2>
    <p>地域の子育て世帯と、クラブの運営者に届く企業紹介ページ。取材はオンライン、写真は会社からのご提供で。制作から1年間の掲載まで込みです。</p>
    <a class="prl-btn" href="service-ads.html">掲載について見る ›</a>
  </section>
  <p class="prl-disc">このページで紹介している企業のページは、各社の提供によるチビスポのPR記事（広告）です。掲載内容は取材時点のものです。最新情報は各社の公式サイト等をご確認ください。</p>
  <div class="prl-back"><a href="search.html">‹ クラブを探す</a><a href="partner.html">クラブ・事業者の方へ ›</a></div>
</div>
</main>'''%(chips,'\n'.join(card(c) for c in cs))
    js='''<script>
(function(){
  var cats=document.getElementById('prlCats'), list=document.getElementById('prlList'); if(!cats||!list) return;
  cats.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    cats.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on',x===b); });
    var k=b.getAttribute('data-cat')||'';
    list.querySelectorAll('.prl-c').forEach(function(c){ c.hidden=!!(k && c.getAttribute('data-cat')!==k); });
  });
})();
</script>'''
    title='企業紹介｜チビスポ ― 子どものスポーツを支える会社'
    desc='ユニフォーム、野球用品、ロゴやグッズのデザイン。チビスポ編集部が取材して書いた企業紹介ページの一覧です。クラブの運営者にも、道具を揃える保護者にも。'
    og='https://chibispo.com/'+cs[0]['img'] if cs else 'https://chibispo.com/assets/ogp.jpg?v=2'
    C.prodpage('pr/index.html',title,desc,body,css=CSS,js=js,base_root=True,og_image=og,canonical='https://chibispo.com/pr/')

if __name__=='__main__':
    build()
