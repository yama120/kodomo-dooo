# ---- DAEDAL.（ディーデル）企業紹介ページ（草案）。python3 pr_daedal.py → pr/daedal.html
# 事実の出典：公式ショップ daedal.stores.jp（2026-09-30 取得）・Instagram @daedal_sports
# 黄色の点線枠（.ask）＝DAEDAL さんに書いていただく箇所。【要確認】＝事実の確認待ち
import os,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
A='assets/pr/daedal/'
SHOP='https://daedal.stores.jp/'; SHOP2='https://daedalonline.base.shop/'; IG='https://www.instagram.com/daedal_sports/'; TIKTOK='https://www.tiktok.com/@daedal035'; LINE='https://lin.ee/WP86CaL'
TBC=lambda s:'<span class="tbc">【要確認：%s】</span>'%s
def ASK(title,items):
    return '<div class="ask"><b>DAEDALさんに書いていただきたいこと｜%s</b><ul>%s</ul></div>'%(title,''.join('<li>%s</li>'%i for i in items))
CSS=r'''
.dd{--k:#111;--pk:#ff2d87;--aq:#19c3c3;--line:#e7e7ea;--sub:#454a52;color:#111;line-height:1.9}
.dd .w{max-width:1040px;margin:0 auto;padding:0 22px}.dd .w2{max-width:760px;margin:0 auto;padding:0 22px}
.dd section{padding:64px 0}
.dd .ey{font-family:Anton,sans-serif;letter-spacing:.16em;font-size:12px;color:var(--pk);margin-bottom:12px}
.dd h2{font-size:clamp(24px,3.4vw,34px);font-weight:900;line-height:1.4;margin:0 0 16px}
.dd h2,.dd-hero h1{text-wrap:balance;word-break:auto-phrase}
.dd-about h2{font-size:clamp(21px,2.9vw,30px)}
.dd p.b{font-size:15px;color:var(--sub);margin:0 0 18px}
.tbc{color:#b7791f;background:#fff7e6;border-radius:6px;padding:0 6px;font-size:.92em;font-weight:700}
.ask{border:2px dashed #e8b64a;background:#fffaf0;border-radius:16px;padding:16px 20px;margin:20px 0 0}
.ask b{display:block;font-size:13.5px;color:#9a6a10;margin-bottom:6px}
.ask ul{margin:0;padding-left:1.2em;font-size:13.5px;color:#6b5320;line-height:1.8}
.dd-legend{background:#fffaf0;border-bottom:2px dashed #e8b64a;color:#9a6a10;font-size:13px;font-weight:700;text-align:center;padding:10px 14px}
/* hero */
.dd-hero{position:relative;min-height:min(84vh,700px);display:flex;align-items:flex-end;overflow:hidden;background:#222;color:#fff;padding:0!important}
.dd-hero .bg{position:absolute;inset:0}.dd-hero .bg img{width:100%;height:100%;object-fit:cover;object-position:center 45%;display:block}
.dd-hero .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.22) 0%,rgba(0,0,0,.4) 40%,rgba(0,0,0,.85) 100%)}
.dd-hero .in{position:relative;width:100%;padding:110px 0 44px}
.dd-hero .pr{display:inline-block;border:1px solid rgba(255,255,255,.6);font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 11px;border-radius:999px;margin-bottom:16px}
.dd-hero .brand{font-family:'Zen Old Mincho',serif;font-weight:900;font-size:clamp(44px,8vw,88px);line-height:1;letter-spacing:.02em;margin:0}
.dd-hero .brand small{display:block;font-family:'Zen Kaku Gothic New',sans-serif;font-size:13px;letter-spacing:.24em;color:#ddd;font-weight:700;margin-top:12px}
.dd-hero h1{font-size:clamp(26px,4.4vw,46px);font-weight:900;line-height:1.35;margin:22px 0 12px}
.dd-hero .ld{font-size:15.5px;color:#e4e4e4;max-width:580px;margin:0 0 24px}
.dd-hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.dd-hero .cta a{display:inline-block;font-weight:800;font-size:15px;padding:14px 26px;border-radius:999px;text-decoration:none}
.dd-hero .cta .p{background:#06c755;color:#fff;box-shadow:0 10px 24px rgba(6,199,85,.35)}.dd-hero .cta .s{border:1.5px solid rgba(255,255,255,.75);color:#fff}
.dd-hero .src{position:absolute;right:14px;bottom:10px;font-size:10.5px;color:#bbb}
/* features */
.dd-feat{background:#111;color:#fff;padding:28px 0!important}
.dd-feat .g{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#2a2a2a;border:1px solid #2a2a2a}
.dd-feat .c{background:#111;padding:20px 18px}.dd-feat b{display:block;font-size:17px;margin-bottom:4px}.dd-feat b i{font-style:normal;color:var(--pk);font-family:Anton,sans-serif;margin-right:8px}
.dd-feat span{font-size:13px;color:#b9b9b9}
/* about */
.dd-about .g{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center}
.dd-about .logo{background:#fff;border:1px solid var(--line);border-radius:20px;padding:44px 34px;display:grid;place-items:center}
.dd-about .logo img{width:100%;max-width:420px;display:block}
.dd-about .ph2{border-radius:22px;overflow:hidden;aspect-ratio:4/5;background:#eee}.dd-about .ph2 img{width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block}
.dd-about .q{border-left:3px solid var(--pk);padding:4px 0 4px 16px;font-size:18px;font-weight:800;margin:6px 0 0}
/* uniform */
.dd-uni{background:#111;color:#fff}.dd-uni p.b{color:#cfcfcf}
.dd-uni .g{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center}
.dd-uni ul{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:12px}
.dd-uni li{display:grid;grid-template-columns:44px 1fr;gap:12px;background:#1c1c1c;border-radius:14px;padding:14px 16px}
.dd-uni li i{font-style:normal;width:40px;height:40px;border-radius:12px;background:var(--pk);color:#fff;display:grid;place-items:center;font-family:Anton,sans-serif}
.dd-uni li b{display:block;font-size:15px}.dd-uni li span{font-size:14px;color:#cfcfcf}.dd-uni li .pl b{display:inline;color:#fff;font-size:15px}.dd-uni li .pl small{font-size:12px;color:#aaa}
.dd-uni .phs{display:grid;grid-template-columns:1fr 1fr;gap:12px}.dd-uni .phs img{width:100%;border-radius:16px;display:block;object-fit:cover;aspect-ratio:3/4}.dd-uni .phs img.wd{grid-column:1/3;aspect-ratio:4/3}
/* glove */
.dd-gl .g{display:grid;grid-template-columns:1fr 1.1fr;gap:40px;align-items:center}
.dd-gl .phs{display:grid;grid-template-columns:1fr 1fr;gap:12px}.dd-gl .phs img{width:100%;border-radius:16px;display:block;object-fit:cover;aspect-ratio:3/4}
.dd-gl .st{display:grid;gap:12px;margin-top:16px}.dd-gl .st>div{display:grid;grid-template-columns:38px 1fr;gap:12px;background:#f6f6f8;border-radius:14px;padding:14px 16px}
.dd-gl .st i{font-style:normal;width:34px;height:34px;border-radius:50%;background:#111;color:#fff;font-family:Anton,sans-serif;display:grid;place-items:center}.dd-gl .st b{display:block;font-size:15px}.dd-gl .st span{font-size:14px;color:var(--sub)}
/* lineup */
.dd-line{background:#f6f6f8}
.dd-line .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}
.dd-line .c{background:#fff;border-radius:18px;overflow:hidden;border:1px solid var(--line);display:flex;flex-direction:column}
.dd-line .c .im{aspect-ratio:4/3;background:#eef0f3;display:grid;place-items:center;overflow:hidden}
.dd-line .c .im img{width:100%;height:100%;object-fit:cover;display:block}.dd-line .c .im img.fit{object-fit:contain;padding:14px}
.dd-line .c .t{padding:16px 18px 18px}.dd-line .c b{display:block;font-size:16.5px;margin-bottom:4px}
.dd-line .c em{display:inline-block;font-style:normal;font-size:12px;font-weight:800;color:var(--pk);margin-bottom:6px}
.dd-line .c span{font-size:13.5px;color:var(--sub)}
/* designers */
.dd-dc{background:#0f1830;color:#fff}
.dd-dc .g{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.dd-dc .ph{background:radial-gradient(circle at 50% 45%,#23376b,#0f1830 70%);border-radius:24px;padding:26px;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.dd-dc .ph img{width:100%;display:block;filter:drop-shadow(0 16px 26px rgba(0,0,0,.45))}
.dd-dc p{color:#cfd6e6;font-size:15px}.dd-dc .q{border-left:3px solid var(--pk);padding:4px 0 4px 16px;font-size:18px;font-weight:800;margin:18px 0}
/* colors */
.dd-col .row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
.dd-col .row div{border-radius:18px;background:#f6f6f8;padding:18px;display:grid;place-items:center}
.dd-col .row img{width:100%;max-width:260px;display:block}
.dd-col .row small{display:block;text-align:center;font-size:12.5px;font-weight:700;color:var(--sub);margin-top:8px}
/* editor */
.dd-ed .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.dd-ed .c{border:1px solid var(--line);border-radius:18px;padding:22px 20px}
.dd-ed .c i{font-style:normal;font-family:Anton,sans-serif;font-size:34px;line-height:1;color:var(--pk);display:block;margin-bottom:10px}
.dd-ed .c b{display:block;font-size:17px;line-height:1.5;margin-bottom:8px}.dd-ed .c p{font-size:14px;color:var(--sub);margin:0}
.note-draft{background:#fff7e6;color:#b7791f;border:1px dashed #e8c98a;border-radius:10px;padding:10px 14px;font-size:12.5px;font-weight:700;margin:0 0 22px}
/* voices */
.dd-vo{background:#f6f6f8}
.dd-vo .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.dd-vo .v{background:#fff;border-radius:18px;padding:22px 20px;border:1px solid var(--line)}
.dd-vo .v b{display:block;font-size:14px;margin-bottom:8px}.dd-vo .v p{margin:0;font-size:14.5px;color:#111}
.dd-vo .g2{display:grid;grid-template-columns:1fr 1.4fr;gap:28px;align-items:center}
.dd-vo .g2+.g2{margin-top:22px}.dd-vo .g2.rev{grid-template-columns:1.4fr 1fr}.dd-vo .g2.rev .ph{order:2}
.dd-vo .ph{border-radius:20px;overflow:hidden;aspect-ratio:3/2;background:#eee}.dd-vo .ph.tall{aspect-ratio:1/1}.dd-vo .ph.tall img{object-position:center 0%}.dd-vo .ph img{width:100%;height:100%;object-fit:cover;display:block}
.dd-vo .v2{background:#fff;border-radius:18px;padding:26px 28px;border:1px solid var(--line)}
.dd-vo .v2 .q{font-size:17px;line-height:1.9;margin:0 0 16px;color:#111}.dd-vo .v2 .q::before{content:"“";color:var(--pk);font-size:1.6em;line-height:0;margin-right:4px}
.dd-vo .who b{display:block;font-size:15px}.dd-vo .who span{display:block;font-size:12.5px;color:var(--sub);margin-top:4px;line-height:1.7}
.dd-vo .nt{font-size:12px;color:#8a95a0;margin:16px 0 0}
@media(max-width:820px){.dd-vo .g2,.dd-vo .g2.rev{grid-template-columns:1fr}.dd-vo .g2.rev .ph{order:0}}
/* qa */
.dd-qa .g{display:grid;grid-template-columns:1fr 1.3fr;gap:36px;align-items:start}
.dd-qa .ph{border-radius:20px;overflow:hidden;background:#eee;aspect-ratio:4/3}.dd-qa .ph img{width:100%;height:100%;object-fit:cover;display:block}
.dd-qa .qa{display:grid;gap:14px}.dd-qa .qa>div{background:#f6f6f8;border-radius:14px;padding:16px 18px}
.dd-qa .qa b{display:block;font-size:15px;margin-bottom:6px}.dd-qa .qa b::before{content:"Q. ";color:var(--pk)}.dd-qa .qa p{margin:0;font-size:14.5px;color:var(--sub)}
/* buy */
.dd-buy .g{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:10px}
.dd-buy a.card2{display:block;text-decoration:none;color:#111;border:1px solid var(--line);border-radius:18px;padding:20px}
.dd-buy a.card2 b{display:block;font-size:16px;margin-bottom:4px}.dd-buy a.card2 span{font-size:13px;color:var(--sub)}
.dd-buy a.card2.shop{background:#111;color:#fff;border-color:#111}.dd-buy a.card2.shop span{color:#ccc}
.dd-buy a.card2.line b{color:#06c755}
/* cta */
.dd-cta{position:relative;color:#fff;text-align:center;overflow:hidden;padding:96px 0!important}
.dd-cta .bg{position:absolute;inset:0}.dd-cta .bg img{width:100%;height:100%;object-fit:cover;display:block}
.dd-cta .sh{position:absolute;inset:0;background:rgba(0,0,0,.62)}.dd-cta .w2{position:relative}
.dd-cta p{color:#e2e2e2;margin:0 0 22px}.dd-cta a{display:inline-block;background:var(--pk);color:#fff;font-weight:900;font-size:16px;padding:15px 34px;border-radius:999px;text-decoration:none}
/* info */
.dd-info .tb{border:1px solid var(--line);border-radius:14px;overflow:hidden;display:grid;grid-template-columns:120px 1fr;font-size:13.5px}
.dd-info .tb div{padding:13px 15px;border-bottom:1px solid #eef0f3}.dd-info .tb div:nth-last-child(-n+2){border-bottom:0}.dd-info .tb .k{background:#f6f7f9;font-weight:700;color:#555}
.dd-info .apply{display:block;text-decoration:none;background:linear-gradient(100deg,#fff4f6,#fef0ea);border:1px solid #f3c9da;border-radius:16px;padding:24px;text-align:center;margin:36px 0 0;color:#111}
.dd-info .apply b{display:block;font-size:17px;margin-bottom:6px}.dd-info .apply span{display:inline-block;background:#E43B4D;color:#fff;font-weight:800;padding:12px 28px;border-radius:999px;margin-top:10px}
.dd-info .disc{background:#f6f7f9;border-radius:14px;padding:18px 20px;font-size:12px;color:#8a95a0;margin-top:28px}
.dd-info .back{text-align:center;margin:22px 0 0}.dd-info .back a{font-size:13.5px;font-weight:700;color:#E43B4D;text-decoration:none}
@media(max-width:820px){.dd-uni .g,.dd-gl .g{grid-template-columns:1fr;gap:26px}.dd section{padding:48px 0}.dd-feat .g,.dd-line .g,.dd-ed .g,.dd-vo .g,.dd-buy .g{grid-template-columns:1fr}.dd-about .g,.dd-dc .g,.dd-qa .g{grid-template-columns:1fr;gap:26px}.dd-col .row{grid-template-columns:repeat(3,1fr);gap:8px}.dd-info .tb{grid-template-columns:104px 1fr}}
'''
body=f'''
<main class="dd">
<div class="dd-legend">確認用の草案です。【要確認】は確認待ちの箇所です。</div>

<section class="dd-hero">
  <div class="bg"><img src="{A}p-uniform-team.webp" alt="DAEDAL.のユニフォームを着た選手たち"></div><div class="sh"></div>
  <div class="in"><div class="w">
    <span class="pr">PR ｜ 企業紹介</span>
    <p class="brand">DAEDAL.<small>ディーデル ｜ BASEBALL GEAR</small></p>
    <h1>道具の値段で、<br>野球を諦めさせない。</h1>
    <p class="ld">デザインを自由に決められるユニフォームから、オーダーグラブ、バッティンググローブ、打者用防具まで。</p>
    <div class="cta"><a class="p" href="{LINE}" target="_blank" rel="noopener sponsored">公式LINEで相談</a><a class="s" href="#uniform">ユニフォームを見る</a></div>
  </div></div>
</section>

<section class="dd-feat"><div class="w"><div class="g">
  <div class="c"><b><i>01</i>2024年10月、高校2年で設立</b><span>野球用品の値上がりに気づいたのがきっかけ</span></div>
  <div class="c"><b><i>02</i>ユニフォームは最短20日</b><span>デザイン自由。チームでのまとめ注文も歓迎</span></div>
  <div class="c"><b><i>03</i>オーダーグラブは約30日</b><span>公式LINEからシミュレーションして注文</span></div>
</div></div></section>

<section class="dd-about"><div class="w"><div class="g">
  <div>
    <div class="ey">STORY</div>
    <h2>ユニフォーム代を理由に、<br>入団を諦める選手を減らしたい。</h2>
    <p class="b">DAEDAL.が始まったのは2024年10月。代表が高校2年生のときです。野球用品を買い替えようとして、値段が大きく上がっていることに気づきました。自分のチーム「DBC柏」でも、入団費（ユニフォーム代）を理由に入団を諦める選手がいる。それを減らしたい、というのが出発点でした。</p>
    <p class="b">代表は野球未経験から、高校野球のクラブチームを立ち上げた人です。野球部に入っていない球児のための、第二の居場所。「居場所のない球児に野球の場を」をモットーに、全国展開を目指しています。</p>
    <p class="b">ブランド名は、ギリシャ神話のものづくりの名工「ダイダロス」から。デザイン性に富んだブランドを作りたい、という想いを込めています。</p>
    <div class="q">「形から入りたい、すべての野球人に使ってほしい」</div>
  </div>
  <div class="ph2"><img loading="lazy" src="{A}p-pitcher-kashiwa.webp" alt="DAEDAL.のグラブで投げる選手"></div>
</div></div></section>

<section class="dd-uni" id="uniform"><div class="w"><div class="g">
  <div>
    <div class="ey">UNIFORM ／ いちばんの推し</div>
    <h2>チームのユニフォームを、<br>自由なデザインで。</h2>
    <p class="b">DAEDAL.がいちばん推しているのがユニフォームです。入団のときの負担を軽くしたい、というブランドの出発点がそのまま形になっています。</p>
    <ul>
      <li><i>01</i><div><b>デザインは自由</b><span>色も柄もロゴも、チームの希望から作れる。</span></div></li>
      <li><i>02</i><div><b>価格を抑える</b><span class="pl">キャップ＋昇華ユニフォームシャツ <b>¥6,990</b><br>キャップ <b>¥2,990</b>／昇華ユニフォームシャツ <b>¥4,990</b><br><small>※刺繍対応やパンツは要相談</small></span></div></li>
      <li><i>03</i><div><b>納期は最短20日</b><span>新チームの立ち上げや、追加の入団にも間に合わせやすい。</span></div></li>
    </ul>
    <p class="b" style="margin-top:16px;font-size:13.5px">子ども・ジュニア向けのサイズも取り扱いがあります。チームでのまとめ注文は大歓迎とのことです。</p>
  </div>
  <div class="phs"><img class="wd" loading="lazy" src="{A}p-dugout.webp" alt="DAEDAL.のユニフォームを着た選手たち" style="object-position:center 25%"></div>
</div></div></section>

<section class="dd-gl"><div class="w"><div class="g">
  <div class="phs"><img loading="lazy" src="{A}p-glove-mint.webp" alt="DAEDAL.のオーダーグラブ"><img loading="lazy" src="{A}p-order-sim.webp" alt="オーダーシミュレーションの画面とグラブ"></div>
  <div>
    <div class="ey">ORDER GLOVE</div>
    <h2>画面で色を決めて、<br>自分だけのグラブを。</h2>
    <p class="b">硬式用 ¥36,300（税込）〜、軟式用 ¥27,500（税込）〜。革の色、紐、刺繍まで、オーダーシミュレーションで仕上がりを見ながら決められます。</p>
    <div class="st">
      <div><i>1</i><div><b>公式LINEで相談</b><span>まずはLINEから。希望を伝える。</span></div></div>
      <div><i>2</i><div><b>オーダーシミュレーション</b><span>画面上で型・色・オプション・刺繍を選ぶ。</span></div></div>
      <div><i>3</i><div><b>制作・お届け</b><span>通常の納期は30日ほど。</span></div></div>
    </div>
  </div>
</div></div></section>

<section class="dd-line" id="lineup"><div class="w">
  <div class="ey">LINEUP</div>
  <h2>バッティングから守りまで、打席に立つ道具。</h2>
  <p class="b">公式ショップで扱っているアイテムです。価格はすべて税込。バッティンググローブはリストガード付きで、Sサイズは小学校高学年から使えます。</p>
  <div class="g">
    <div class="c"><div class="im"><img class="fit" src="{A}glove-aqua-1.webp" alt="バッティンググローブ"></div><div class="t"><em>¥5,990〜¥6,600</em><b>バッティンググローブ</b><span>天然カブレッタレザー。High-Grade と、独自柄の Designers create。野球・ソフトボール兼用。</span></div></div>
    <div class="c"><div class="im"><img src="{A}armor.webp" alt="打者用防具"></div><div class="t"><em>¥4,990〜¥8,800</em><b>打者用防具 Armor Collection</b><span>フットガード・エルボーガード・手甲ガード。スイングを妨げない軽量設計。高校野球対応モデルあり。</span></div></div>
    <div class="c"><div class="im"><img src="{A}belt.webp" alt="ベルト"></div><div class="t"><em>¥1,990</em><b>DAEDAL CORE BELT</b><span>シルバー・ゴールド・ホワイト・グリーン・パープル・オレンジなど、カラー展開の多いベルト。</span></div></div>
    <div class="c"><div class="im"><img src="{A}sunglass.webp" alt="感動サングラス"></div><div class="t"><em>¥2,480</em><b>感動サングラス</b><span>UV99%カット・UV400。軽量で長時間の試合にも。野球・ソフトボールのほかアウトドアにも。</span></div></div>
    <div class="c"><div class="im"><img src="{A}p-glove-mint-card.webp" alt="オーダーグラブ"></div><div class="t"><em>硬式 ¥36,300〜／軟式 ¥27,500〜</em><b>オーダーグラブ</b><span>公式LINEからシミュレーションして注文。通常の納期は30日ほど。</span></div></div>
  </div>
</div></section>

<section class="dd-dc"><div class="w"><div class="g">
  <div class="ph"><img src="{A}glove-stars-1.webp" alt="Designers create United Stars"><img src="{A}glove-stars-2.webp" alt="Designers create United Stars"></div>
  <div>
    <div class="ey">DESIGNERS CREATE</div>
    <h2>他にない柄で、<br>打席に立つ。</h2>
    <p>より個性的な道具を求める野球人に向けたライン「Designers create」。第1弾の「United Stars」は、星を散らした独自の柄のバッティンググローブです。</p>
    <div class="q">「他社には無い独自の柄で、見る者を魅了する。」</div>
  </div>
</div></div></section>

<section class="dd-col"><div class="w">
  <div class="ey">COLOR</div>
  <h2>チームカラーに合わせて選べる。</h2>
  <p class="b">同じ High-Grade でも、配色で印象が変わります。</p>
  <div class="row">
    <div><img src="{A}glove-aqua-1.webp" alt="Aqua Blue × White"><small>Aqua Blue × White</small></div>
    <div><img src="{A}glove-pink.webp" alt="Pink × White"><small>Pink × White</small></div>
    <div><img src="{A}glove-stars-1.webp" alt="United Stars"><small>United Stars</small></div>
  </div>
</div></section>

<section class="dd-ed"><div class="w">
  <div class="ey">EDITOR'S VIEW ／ 取材メモ</div>
  <h2>取材してわかった、DAEDAL.の3つのポイント</h2>
  <div class="note-draft">※ 下書きです。サンプルが届いたら、実物を見たうえで書き直します。</div>
  <div class="g">
    <div class="c"><i>01</i><b>「値段で諦める選手を減らしたい」から始まっている</b><p>高校2年生が、自分のチームで入団を諦める仲間を見て立ち上げたブランドです。売りたい商品が先にあったのではなく、困りごとが先にあった。ユニフォームをいちばんに推している理由が、成り立ちと一致しています。</p></div>
    <div class="c"><i>02</i><b>「色で選べる」が、そのまま個性になる</b><p>グローブ・防具・ベルトまで配色の選択肢が多く、Designers create のような独自柄もある。チームカラーに合わせたい選手にも、人と被りたくない選手にも向いています。</p></div>
    <div class="c"><i>03</i><b>ユニフォームからグラブまで、チームで揃えられる</b><p>ユニフォームは最短20日、オーダーグラブは30日ほど。防具には白・黒の高校野球対応モデルもあります。チームの立ち上げや新入団のタイミングで、一式を同じブランドで相談できます。</p></div>
  </div>
</div></section>

<section class="dd-vo"><div class="w">
  <div class="ey">PLAYERS' VOICE</div>
  <h2>使っている選手の声</h2>
  <div class="g2">
    <div class="ph"><img loading="lazy" src="{A}p-pitcher-blueglove.webp" alt="DAEDAL.のグラブで投げる青田将志投手"></div>
    <div class="v2">
      <p class="q">「DAEDALのグローブを提供して頂いて使わせてもらっています。少し小さめに作られてて扱いやすく、軽量で投げやすくて、他のブランドにも負けない使いやすいグローブです。」</p>
      <div class="who"><b>青田 将志 投手</b><span>成立学園 → 東洋学園大 → 福井ネクサスエレファンツ → 千葉スカイセイラーズ → 大分Bリングス → ショウワコーポレーション</span></div>
    </div>
  </div>
  <div class="g2 rev">
    <div class="ph tall"><img loading="lazy" src="{A}p-batter-stars.webp" alt="DAEDAL.のバッティンググローブと防具で打つ佐藤仁選手"></div>
    <div class="v2">
      <p class="q">「DAEDALのバッティングアーマー、バッティンググローブを提供して頂いて使用しています。唯一無二のフィット感とデザイン性を両立したアイテムたち。他のブランドには無い、野球が楽しくなる道具です。」</p>
      <div class="who"><b>佐藤 仁 選手</b><span>西日本短大附属 → 北九州下関フェニックス</span></div>
    </div>
  </div>
  <p class="nt">DAEDAL.を通じて届いたレビューを、ご本人の了承のもと掲載しています。</p>
</div></section>

<section class="dd-qa"><div class="w"><div class="g">
  <div>
    <div class="ey">Q&amp;A</div>
    <h2>聞いておきたいこと</h2>
    <p class="b">スポーツクラブ・選手向けに聞いておきたいことをお尋ねしました。</p>
    <div class="ph"><img loading="lazy" src="{A}p-order-sim.webp" alt="オーダーグラブとオーダーシミュレーションの画面" style="object-position:center 60%"></div>
  </div>
  <div class="qa">
    <div><b>子ども・ジュニア向けのサイズはありますか？</b><p>ユニフォーム類は取り扱いがあります。バッティンググローブはリストガード付きのため、Sサイズは小学校高学年以上であれば使えます。</p></div>
    <div><b>「高校野球対応モデル」があるのは、どの商品ですか？</b><p>現在は打者用防具のみです。ほかの商品については検討中とのことです。</p></div>
    <div><b>チームでまとめて注文できますか？</b><p>大歓迎です。公式LINEから相談できます。</p></div>
  </div>
</div></div></section>

<section class="dd-buy"><div class="w">
  <div class="ey">SHOP</div>
  <h2>購入・相談</h2>
  <div class="g">
    <a class="card2 shop" href="{SHOP}" target="_blank" rel="noopener sponsored"><b>公式ショップ（STORES）</b><span>グローブ・防具・ベルトなど｜¥10,000以上で送料無料</span></a>
    <a class="card2 shop" href="{SHOP2}" target="_blank" rel="noopener sponsored"><b>公式ショップ（BASE）</b><span>daedalonline.base.shop</span></a>
    <a class="card2 line" href="{LINE}" target="_blank" rel="noopener sponsored"><b>LINEで相談</b><span>ユニフォーム・オーダーグラブの相談はこちら</span></a>
    <a class="card2" href="{IG}" target="_blank" rel="noopener sponsored"><b>Instagram</b><span>@daedal_sports｜新作・着用写真</span></a>
    <a class="card2" href="{TIKTOK}" target="_blank" rel="noopener sponsored"><b>TikTok</b><span>@daedal035｜動画で見る</span></a>
  </div>
</div></section>

<section class="dd-cta"><div class="bg"><img src="{A}p-uniform-team.webp" alt=""></div><div class="sh"></div><div class="w2">
  <h2>チームの一式を、DAEDAL.で。</h2>
  <p>ユニフォームもグラブも、まずは公式LINEから。</p>
  <a href="{LINE}" target="_blank" rel="noopener sponsored" style="background:#06c755">公式LINEで相談</a>
</div></section>

<section class="dd-info"><div class="w2">
  <h2 style="font-size:22px">ブランド情報</h2>
  <div class="tb">
    <div class="k">ブランド</div><div>DAEDAL.（ディーデル）</div>
    <div class="k">設立</div><div>2024年10月</div>
    <div class="k">所在地</div><div>千葉県柏市大井</div>
    <div class="k">取り扱い</div><div>ユニフォーム／オーダーグラブ／バッティンググローブ／打者用防具／ベルト／サングラス ほか</div>
    <div class="k">相談窓口</div><div>公式LINE</div>
    <div class="k">支払い方法</div><div>クレジットカード・コンビニ決済・銀行振込・PayPay ほか</div>
    <div class="k">発送</div><div>注文から10日以内（防具など納期の記載がある商品を除く）</div>
    <div class="k">送料</div><div>¥10,000以上の購入で無料</div>
  </div>
  <a class="apply" href="service-ads.html"><b>あなたのお店も、こんなページで紹介しませんか？</b>地域の子育て世帯に届く、チビスポの企業紹介ページ。<br><span>掲載を申し込む ›</span></a>
  <div class="disc">この記事は、DAEDAL.の提供による<strong style="color:#555">チビスポのPR記事（広告）</strong>です。内容は DAEDAL. からの回答と公式ショップの掲載内容（2026年10月時点）にもとづきます。最新情報は公式ショップをご確認ください。</div>
  <div class="back"><a href="search.html">‹ クラブを探すに戻る</a></div>
</div></section>
</main>
'''
C.prodpage('pr/daedal.html','DAEDAL.（ディーデル）｜チビスポ 企業紹介','高校2年生が立ち上げた野球ブランドDAEDAL.。デザイン自由のユニフォーム、オーダーグラブ、バッティンググローブ、打者用防具。',body,css=CSS,noindex=True,base_root=True,og_image='https://chibispo.com/assets/pr/daedal/p-uniform-team.webp')
