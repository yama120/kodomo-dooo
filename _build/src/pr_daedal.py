# ---- DAEDAL.（ダイダル）企業紹介ページ（草案）。python3 pr_daedal.py → pr/daedal.html
# 事実の出典：公式ショップ daedal.stores.jp（2026-09-30 取得）・Instagram @daedal_sports
# 黄色の点線枠（.ask）＝DAEDAL さんに書いていただく箇所。【要確認】＝事実の確認待ち
import os,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
A='assets/pr/daedal/'
SHOP='https://daedal.stores.jp/'; IG='https://www.instagram.com/daedal_sports/'; LINE='https://lin.ee/WP86CaL'
TBC=lambda s:'<span class="tbc">【要確認：%s】</span>'%s
def ASK(title,items):
    return '<div class="ask"><b>DAEDALさんに書いていただきたいこと｜%s</b><ul>%s</ul></div>'%(title,''.join('<li>%s</li>'%i for i in items))
CSS=r'''
.dd{--k:#111;--pk:#ff2d87;--aq:#19c3c3;--line:#e7e7ea;--sub:#454a52;color:#111;line-height:1.9}
.dd .w{max-width:1040px;margin:0 auto;padding:0 22px}.dd .w2{max-width:760px;margin:0 auto;padding:0 22px}
.dd section{padding:64px 0}
.dd .ey{font-family:Anton,sans-serif;letter-spacing:.16em;font-size:12px;color:var(--pk);margin-bottom:12px}
.dd h2{font-size:clamp(24px,3.4vw,34px);font-weight:900;line-height:1.4;margin:0 0 16px}
.dd p.b{font-size:15px;color:var(--sub);margin:0 0 18px}
.tbc{color:#b7791f;background:#fff7e6;border-radius:6px;padding:0 6px;font-size:.92em;font-weight:700}
.ask{border:2px dashed #e8b64a;background:#fffaf0;border-radius:16px;padding:16px 20px;margin:20px 0 0}
.ask b{display:block;font-size:13.5px;color:#9a6a10;margin-bottom:6px}
.ask ul{margin:0;padding-left:1.2em;font-size:13.5px;color:#6b5320;line-height:1.8}
.dd-legend{background:#fffaf0;border-bottom:2px dashed #e8b64a;color:#9a6a10;font-size:13px;font-weight:700;text-align:center;padding:10px 14px}
/* hero */
.dd-hero{position:relative;min-height:min(84vh,700px);display:flex;align-items:flex-end;overflow:hidden;background:#222;color:#fff;padding:0!important}
.dd-hero .bg{position:absolute;inset:0}.dd-hero .bg img{width:100%;height:100%;object-fit:cover;object-position:center 55%;display:block}
.dd-hero .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 0%,rgba(0,0,0,.25) 40%,rgba(0,0,0,.82) 100%)}
.dd-hero .in{position:relative;width:100%;padding:110px 0 44px}
.dd-hero .pr{display:inline-block;border:1px solid rgba(255,255,255,.6);font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 11px;border-radius:999px;margin-bottom:16px}
.dd-hero .brand{font-family:'Zen Old Mincho',serif;font-weight:900;font-size:clamp(44px,8vw,88px);line-height:1;letter-spacing:.02em;margin:0}
.dd-hero .brand small{display:block;font-family:'Zen Kaku Gothic New',sans-serif;font-size:13px;letter-spacing:.24em;color:#ddd;font-weight:700;margin-top:12px}
.dd-hero h1{font-size:clamp(26px,4.4vw,46px);font-weight:900;line-height:1.35;margin:22px 0 12px}
.dd-hero .ld{font-size:15.5px;color:#e4e4e4;max-width:580px;margin:0 0 24px}
.dd-hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.dd-hero .cta a{display:inline-block;font-weight:800;font-size:15px;padding:14px 26px;border-radius:999px;text-decoration:none}
.dd-hero .cta .p{background:var(--pk);color:#fff;box-shadow:0 10px 24px rgba(255,45,135,.35)}.dd-hero .cta .s{border:1.5px solid rgba(255,255,255,.75);color:#fff}
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
/* qa */
.dd-qa .g{display:grid;grid-template-columns:1fr 1.3fr;gap:36px;align-items:start}
.dd-qa .ph{border-radius:20px;overflow:hidden;background:#eee;aspect-ratio:4/3}.dd-qa .ph img{width:100%;height:100%;object-fit:cover;display:block}
.dd-qa .qa{display:grid;gap:14px}.dd-qa .qa>div{background:#f6f6f8;border-radius:14px;padding:16px 18px}
.dd-qa .qa b{display:block;font-size:15px;margin-bottom:6px}.dd-qa .qa b::before{content:"Q. ";color:var(--pk)}.dd-qa .qa p{margin:0;font-size:14.5px;color:var(--sub)}
/* buy */
.dd-buy .g{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:10px}
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
@media(max-width:820px){.dd section{padding:48px 0}.dd-feat .g,.dd-line .g,.dd-ed .g,.dd-vo .g,.dd-buy .g{grid-template-columns:1fr}.dd-about .g,.dd-dc .g,.dd-qa .g{grid-template-columns:1fr;gap:26px}.dd-col .row{grid-template-columns:repeat(3,1fr);gap:8px}.dd-info .tb{grid-template-columns:104px 1fr}}
'''
body=f'''
<main class="dd">
<div class="dd-legend">草案です。黄色の点線の枠が、DAEDALさんに書いていただきたい箇所です。【要確認】は事実の確認待ちです。</div>

<section class="dd-hero">
  <div class="bg"><img src="{A}armor.webp" alt="DAEDAL Armor Collection エルボーガード"></div><div class="sh"></div>
  <div class="in"><div class="w">
    <span class="pr">PR ｜ 企業紹介</span>
    <p class="brand">DAEDAL.<small>ダイダル ｜ BASEBALL GEAR</small></p>
    <h1>選手の声から生まれた、<br>野球の道具。</h1>
    <p class="ld">現役選手のレビューをもとに、プレイヤー視点で作るバッティンググローブと打者用防具。色で選べる、自分だけの一式を。</p>
    <div class="cta"><a class="p" href="{SHOP}" target="_blank" rel="noopener sponsored">公式ショップを見る</a><a class="s" href="#lineup">アイテムを見る</a></div>
  </div></div>
  <div class="src">写真：DAEDAL公式ショップより（仮）</div>
</section>

<section class="dd-feat"><div class="w"><div class="g">
  <div class="c"><b><i>01</i>選手のレビューで作る</b><span>現役選手の声をもとに、プレイヤー視点で設計</span></div>
  <div class="c"><b><i>02</i>天然カブレッタレザー</b><span>バッティンググローブは ¥5,990（税込）から</span></div>
  <div class="c"><b><i>03</i>高校野球対応モデル</b><span>打者用防具 Armor Collection に白・黒の対応モデル</span></div>
</div></div></section>

<section class="dd-about"><div class="w"><div class="g">
  <div>
    <div class="ey">ABOUT</div>
    <h2>{TBC("ブランドを一言で表す見出し")}</h2>
    <p class="b">{TBC("ブランドの紹介文（3〜4行）")}</p>
    {ASK("ブランドについて",["DAEDAL.を始めたきっかけ・いつから・どこで","ブランド名「DAEDAL.」に込めた意味","どんな選手・チームに使ってほしいか","代表・つくり手の紹介（名前を出すかどうかも）"])}
  </div>
  <div class="logo"><img src="{A}logo.webp" alt="DAEDAL."></div>
</div></div></section>

<section class="dd-line" id="lineup"><div class="w">
  <div class="ey">LINEUP</div>
  <h2>バッティングから守りまで、打席に立つ道具。</h2>
  <p class="b">公式ショップで扱っているアイテムです。価格はすべて税込。</p>
  <div class="g">
    <div class="c"><div class="im"><img class="fit" src="{A}glove-aqua-1.webp" alt="バッティンググローブ"></div><div class="t"><em>¥5,990〜¥6,600</em><b>バッティンググローブ</b><span>天然カブレッタレザー。High-Grade と、独自柄の Designers create。野球・ソフトボール兼用。</span></div></div>
    <div class="c"><div class="im"><img src="{A}armor.webp" alt="打者用防具"></div><div class="t"><em>¥4,990〜¥8,800</em><b>打者用防具 Armor Collection</b><span>フットガード・エルボーガード・手甲ガード。スイングを妨げない軽量設計。高校野球対応モデルあり。</span></div></div>
    <div class="c"><div class="im"><img src="{A}belt.webp" alt="ベルト"></div><div class="t"><em>¥1,990</em><b>DAEDAL CORE BELT</b><span>シルバー・ゴールド・ホワイト・グリーン・パープル・オレンジなど、カラー展開の多いベルト。</span></div></div>
    <div class="c"><div class="im"><img src="{A}sunglass.webp" alt="感動サングラス"></div><div class="t"><em>¥2,480</em><b>感動サングラス</b><span>UV99%カット・UV400。軽量で長時間の試合にも。野球・ソフトボールのほかアウトドアにも。</span></div></div>
    <div class="c"><div class="im"><img src="{A}poncho.webp" alt="冷！感動ポンチョ"></div><div class="t"><em>¥1,290</em><b>冷！感動ポンチョ（夏季限定）</b><span>ひんやりサラサラ。夏の練習・観戦に。</span></div></div>
    <div class="c"><div class="im"><img src="assets/pr/placeholder/a.svg" alt="オーダーグラブの写真（提供待ち）"></div><div class="t"><em>硬式 ¥36,300〜／軟式 ¥27,500〜</em><b>オーダーグラブ</b><span>{TBC("オーダーの流れ・納期・選べる項目・写真")}</span></div></div>
  </div>
  {ASK("ラインナップ",["いちばん推したいアイテムと、その理由","オーダーグラブの写真と、注文の流れ・納期・選べる項目","子ども・ジュニア向けのサイズがあるアイテム"])}
</div></section>

<section class="dd-dc"><div class="w"><div class="g">
  <div class="ph"><img src="{A}glove-stars-1.webp" alt="Designers create United Stars"><img src="{A}glove-stars-2.webp" alt="Designers create United Stars"></div>
  <div>
    <div class="ey">DESIGNERS CREATE</div>
    <h2>他にない柄で、<br>打席に立つ。</h2>
    <p>より個性的な道具を求める野球人に向けたライン「Designers create」。第1弾の「United Stars」は、星を散らした独自の柄のバッティンググローブです。</p>
    <div class="q">「他社には無い独自の柄で、見る者を魅了する。」</div>
    <p style="font-size:13px">{TBC("今後の柄の展開予定・デザイナーについて")}</p>
  </div>
</div></div></section>

<section class="dd-col"><div class="w">
  <div class="ey">COLOR</div>
  <h2>チームカラーに合わせて選べる。</h2>
  <p class="b">同じ High-Grade でも、配色で印象が変わります。</p>
  <div class="row">
    <div><img src="{A}glove-aqua-2.webp" alt="Aqua Blue × White"><small>Aqua Blue × White</small></div>
    <div><img src="{A}glove-pink.webp" alt="Pink × White"><small>Pink × White</small></div>
    <div><img src="{A}glove-stars-1.webp" alt="United Stars"><small>United Stars</small></div>
  </div>
</div></section>

<section class="dd-ed"><div class="w">
  <div class="ey">EDITOR'S VIEW ／ 取材メモ</div>
  <h2>取材してわかった、DAEDAL.の3つのポイント</h2>
  <div class="note-draft">※ 取材前の下書きです。公式ショップの情報から書いています。取材後に書き直します。</div>
  <div class="g">
    <div class="c"><i>01</i><b>選手のレビューから作っている</b><p>商品説明に「現役選手からのレビューを基に制作」とある通り、作り手の側ではなく打席に立つ側から道具を考えているブランドです。</p></div>
    <div class="c"><i>02</i><b>「色で選べる」が、そのまま個性になる</b><p>グローブ・防具・ベルトまで配色の選択肢が多く、Designers create のような独自柄もある。チームカラーに合わせたい選手にも、人と被りたくない選手にも向いています。</p></div>
    <div class="c"><i>03</i><b>高校野球の規定まで見ている</b><p>防具には白・黒の「高校野球対応モデル」を用意。見た目の派手さだけでなく、公式戦で使えるかまで考えられている点は、チームで選ぶときの安心材料です。</p></div>
  </div>
</div></section>

<section class="dd-vo"><div class="w">
  <div class="ey">PLAYERS' VOICE</div>
  <h2>使っている選手・チームの声</h2>
  <p class="b">DAEDAL.を使っている選手・チームのレビューを、名前とあわせて載せます。掲載はご本人・チームの許可があるものだけです。</p>
  <div class="g">
    <div class="v"><b>{TBC("選手名またはチーム名")}</b><p>{TBC("レビュー本文")}</p></div>
    <div class="v"><b>{TBC("選手名またはチーム名")}</b><p>{TBC("レビュー本文")}</p></div>
    <div class="v"><b>{TBC("保護者・指導者の声")}</b><p>{TBC("レビュー本文")}</p></div>
  </div>
  {ASK("選手・チームの声",["ショップのレビュー（感動サングラスに4件あり）から、掲載してよいもの","使っている選手・チームの名前と写真（掲載許可のあるもの）","少年野球・中学・高校など、カテゴリがわかると伝わりやすい"])}
</div></section>

<section class="dd-qa"><div class="w"><div class="g">
  <div>
    <div class="ey">Q&amp;A</div>
    <h2>聞いておきたいこと</h2>
    <p class="b">スポーツクラブ・選手向けに聞いておきたいことをお尋ねしました。{TBC("回答")}</p>
    <div class="ph"><img src="assets/pr/placeholder/a.svg" alt="写真（提供待ち）"></div>
  </div>
  <div class="qa">
    <div><b>子ども・ジュニア向けのサイズはありますか？</b><p>{TBC("サイズ展開・選び方")}</p></div>
    <div><b>「高校野球対応モデル」とは、どこが違うのですか？</b><p>{TBC("規定への対応内容")}</p></div>
    <div><b>チームでまとめて注文できますか？</b><p>{TBC("まとめ買い・名入れ・チームカラーの対応")}</p></div>
  </div>
</div></div></section>

<section class="dd-buy"><div class="w">
  <div class="ey">SHOP</div>
  <h2>購入・相談</h2>
  <div class="g">
    <a class="card2 shop" href="{SHOP}" target="_blank" rel="noopener sponsored"><b>公式ショップ</b><span>STORES｜¥10,000以上で送料無料</span></a>
    <a class="card2 line" href="{LINE}" target="_blank" rel="noopener sponsored"><b>LINEで相談</b><span>オーダーグラブの相談など {TBC("窓口として載せてよいか")}</span></a>
    <a class="card2" href="{IG}" target="_blank" rel="noopener sponsored"><b>Instagram</b><span>@daedal_sports｜新作・着用写真</span></a>
  </div>
</div></section>

<section class="dd-cta"><div class="bg"><img src="{A}sunglass.webp" alt=""></div><div class="sh"></div><div class="w2">
  <h2>打席に立つ一式を、DAEDAL.で。</h2>
  <p>{TBC("チビスポ経由の特典（クーポンコードなど）")}</p>
  <a href="{SHOP}" target="_blank" rel="noopener sponsored">公式ショップを見る</a>
</div></section>

<section class="dd-info"><div class="w2">
  <h2 style="font-size:22px">ブランド情報</h2>
  <div class="tb">
    <div class="k">ブランド</div><div>DAEDAL.（ダイダル）</div>
    <div class="k">運営</div><div>{TBC("会社名・屋号・代表者名を載せるか")}</div>
    <div class="k">所在地</div><div>{TBC("市区町村まで")}</div>
    <div class="k">取り扱い</div><div>バッティンググローブ／打者用防具／ベルト／サングラス／オーダーグラブ ほか</div>
    <div class="k">支払い方法</div><div>クレジットカード・コンビニ決済・銀行振込・PayPay ほか</div>
    <div class="k">発送</div><div>注文から10日以内（防具など納期の記載がある商品を除く）</div>
    <div class="k">送料</div><div>¥10,000以上の購入で無料</div>
  </div>
  <a class="apply" href="service-ads.html"><b>あなたのお店も、こんなページで紹介しませんか？</b>地域の子育て世帯に届く、チビスポの企業紹介ページ。<br><span>掲載を申し込む ›</span></a>
  <div class="disc">この記事は、DAEDAL.の提供による<strong style="color:#555">チビスポのPR記事（広告）</strong>です。価格・商品情報は公式ショップの掲載内容（2026年9月30日時点）にもとづきます。最新情報は公式ショップをご確認ください。</div>
  <div class="back"><a href="search.html">‹ クラブを探すに戻る</a></div>
</div></section>
</main>
'''
C.prodpage('pr/daedal.html','DAEDAL.（ダイダル）｜チビスポ 企業紹介','現役選手のレビューをもとに作るバッティンググローブと打者用防具。野球用品ブランドDAEDAL.の紹介ページ。',body,css=CSS,noindex=True,base_root=True,og_image='https://chibispo.com/assets/pr/daedal/armor.webp')
