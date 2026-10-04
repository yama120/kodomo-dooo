# ---- makkiedrops design（マッキードロップスデザイン）企業紹介ページ（草案）。python3 pr_makkiedrops.py → pr/makkiedrops.html
# 事実の出典：公式サイト makkiedrops.com（2026-10-01 取得）。黄色の点線枠（.ask）＝先方に書いていただく箇所。【要確認】＝確認待ち
import os,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
A='assets/pr/makkiedrops/'
SITE='https://makkiedrops.com/'; CONTACT='https://makkiedrops.com/contact'; SHOP='https://makkiedrops.stores.jp/'; WORKS='https://makkiedrops.com/design/'; IG='https://www.instagram.com/makkiedropsdesign/'; COUPON='XEWTN5VVSH'
TBC=lambda s:'<span class="tbc">【要確認：%s】</span>'%s
def ASK(title,items):
    return '<div class="ask"><b>マッキードロップスさんに書いていただきたいこと｜%s</b><ul>%s</ul></div>'%(title,''.join('<li>%s</li>'%i for i in items))
CSS=r'''
.mk{--k:#15171c;--bl:#0d9be0;--ye:#ffe94d;--gr:#3aa845;--line:#e7e7ea;--sub:#454a52;color:#15171c;line-height:1.9}
.mk .w{max-width:1040px;margin:0 auto;padding:0 22px}.mk .w2{max-width:760px;margin:0 auto;padding:0 22px}
.mk section{padding:64px 0}
.mk .ey{font-family:Anton,sans-serif;letter-spacing:.16em;font-size:12px;color:var(--bl);margin-bottom:12px}
.mk h2{font-size:clamp(24px,3.4vw,34px);font-weight:900;line-height:1.4;margin:0 0 16px}
.mk p.b{font-size:15px;color:var(--sub);margin:0 0 18px}
.tbc{color:#b7791f;background:#fff7e6;border-radius:6px;padding:0 6px;font-size:.92em;font-weight:700}
.ask{border:2px dashed #e8b64a;background:#fffaf0;border-radius:16px;padding:16px 20px;margin:20px 0 0}
.ask b{display:block;font-size:13.5px;color:#9a6a10;margin-bottom:6px}.ask ul{margin:0;padding-left:1.2em;font-size:13.5px;color:#6b5320;line-height:1.8}
.mk-legend{background:#fffaf0;border-bottom:2px dashed #e8b64a;color:#9a6a10;font-size:13px;font-weight:700;text-align:center;padding:10px 14px}
.note-draft{background:#fff7e6;color:#b7791f;border:1px dashed #e8c98a;border-radius:10px;padding:10px 14px;font-size:12.5px;font-weight:700;margin:0 0 22px}
/* hero */
.mk-hero{position:relative;min-height:min(84vh,700px);display:flex;align-items:flex-end;overflow:hidden;background:#1c1d22;color:#fff;padding:0!important}
.mk-hero{background:#000}
.mk-hero .bg{position:absolute;inset:0}.mk-hero .bg img{width:100%;height:100%;object-fit:contain;object-position:center 18%;display:block}
.mk-hero .chr{position:absolute;z-index:1;width:clamp(96px,15vw,200px);height:auto}
.mk-hero .c1{left:3%;top:6%}.mk-hero .c4{right:5%;top:8%}.mk-hero .c2{right:4%;bottom:6%}.mk-hero .c3{right:22%;bottom:4%;width:clamp(70px,10vw,130px)}
@media(max-width:820px){.mk-hero .c3,.mk-hero .c2{display:none}.mk-hero .c1{top:3%}.mk-hero .c4{top:4%}}
.mk-hero .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,.35) 45%,rgba(0,0,0,.9) 100%)}
.mk-hero .in{z-index:2}
.mk-hero .in{position:relative;width:100%;padding:120px 0 44px}
.mk-hero .pr{display:inline-block;border:1px solid rgba(255,255,255,.6);font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 11px;border-radius:999px;margin-bottom:16px}
.mk-hero .brand{font-family:Anton,sans-serif;font-size:clamp(30px,5.4vw,58px);line-height:1.05;letter-spacing:.04em;margin:0}
.mk-hero .brand em{font-style:normal;color:var(--ye)}
.mk-hero .brand small{display:block;font-family:'Zen Kaku Gothic New',sans-serif;font-size:13px;letter-spacing:.2em;color:#d5d5d5;font-weight:700;margin-top:10px}
.mk-hero h1{font-size:clamp(25px,4.2vw,44px);font-weight:900;line-height:1.38;margin:22px 0 12px}
.mk-hero .ld{font-size:15.5px;color:#e4e4e4;max-width:600px;margin:0 0 24px}
.mk-hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.mk-hero .cta a{display:inline-block;font-weight:800;font-size:15px;padding:14px 26px;border-radius:999px;text-decoration:none}
.mk-hero .cta .p{background:var(--ye);color:#15171c}.mk-hero .cta .s{border:1.5px solid rgba(255,255,255,.75);color:#fff}
.mk-hero .src{position:absolute;right:14px;bottom:10px;font-size:10.5px;color:#aaa}
/* strip */
.mk-feat{background:var(--ye);padding:26px 0!important}
.mk-feat .g{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.mk-feat .c{background:#fff;border-radius:16px;padding:18px}.mk-feat b{display:block;font-family:Anton,sans-serif;font-size:clamp(26px,4vw,38px);line-height:1.1;letter-spacing:.02em}
.mk-feat b i{font-style:normal;font-family:'Zen Kaku Gothic New',sans-serif;font-size:.42em;font-weight:900;margin-left:4px}
.mk-feat span{display:block;font-size:13px;color:var(--sub);margin-top:6px;line-height:1.6}
/* about */
.mk-about .g{display:grid;grid-template-columns:.8fr 1.2fr;gap:44px;align-items:center}
.mk-about .ph{border-radius:24px;overflow:hidden;background:#f3f5f7;aspect-ratio:414/486}.mk-about .ph img{width:100%;height:100%;object-fit:cover;display:block}
.mk-about .q{font-size:clamp(20px,2.6vw,26px);font-weight:900;line-height:1.6;margin:0 0 14px}
.mk-about .nm{font-size:13.5px;color:var(--sub);font-weight:700}
.mk-about .q2{border-left:3px solid var(--bl);padding:4px 0 4px 16px;font-size:15.5px;font-weight:700;margin:6px 0 16px}
/* service */
.mk-sv{background:#f6f7f9}
.mk-sv .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}
.mk-sv .c{background:#fff;border-radius:18px;border:1px solid var(--line);padding:22px 20px}
.mk-sv .c em{display:block;font-style:normal;font-family:Anton,sans-serif;font-size:12px;letter-spacing:.14em;color:var(--bl);margin-bottom:6px}
.mk-sv .c b{display:block;font-size:18px;margin-bottom:6px}.mk-sv .c p{font-size:13.5px;color:var(--sub);margin:0 0 12px}
.mk-sv .c .pr2{font-weight:900;font-size:17px;border-top:1px dashed var(--line);padding-top:10px}.mk-sv .c .pr2 small{display:block;font-size:12px;font-weight:500;color:var(--sub)}
.mk-sv .c.hot{border:2px solid var(--bl)}
/* goods */
.mk-gd .bn{border-radius:22px;overflow:hidden;margin:0 0 18px}.mk-gd .bn img{width:100%;display:block}
.mk-gd .g{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.mk-gd .g figure{margin:0}.mk-gd .g img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;display:block;background:#eee}
.mk-gd .g figcaption{font-size:12.5px;color:var(--sub);margin-top:6px;text-align:center;font-weight:700}
.mk-gd .facts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.mk-gd .facts div{background:#f6f7f9;border-radius:16px;padding:18px}.mk-gd .facts b{display:block;font-size:15px;color:var(--bl);margin-bottom:4px}.mk-gd .facts span{font-size:14px;color:var(--sub)}
.cp{display:flex;gap:18px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:var(--ye);border-radius:18px;padding:20px 24px;margin-top:18px}
.cp small{display:block;font-size:12px;font-weight:800;letter-spacing:.08em}.cp b{display:block;font-size:19px;margin:2px 0 4px}.cp span{font-size:13.5px;color:#3a3a2a}
.cp code{font-family:Anton,ui-monospace,monospace;font-size:clamp(24px,4vw,34px);letter-spacing:.08em;background:#fff;border:2px dashed #15171c;border-radius:12px;padding:8px 18px;color:#15171c}
/* works */
.mk-wk{background:var(--k);color:#fff}
.mk-wk p.b{color:#c9ccd2}
.mk-wk .amrow{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 22px 18px;margin:0 -22px;scrollbar-width:none}
.mk-wk .amrow::-webkit-scrollbar{display:none}
.mk-wk .amrow figure{flex:0 0 min(62vw,280px);margin:0;scroll-snap-align:start}
.mk-wk .amrow img{width:100%;aspect-ratio:3/4;object-fit:contain;background:#fff;border-radius:14px;display:block}
.mk-wk .amrow figcaption{font-size:12.5px;color:#c9ccd2;margin-top:8px}
.mk-wk a.lk{color:var(--ye);font-weight:800;font-size:14px}
/* editor */
.mk-ed .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mk-ed .c{border:1px solid var(--line);border-radius:18px;padding:22px 20px}
.mk-ed .c i{font-style:normal;font-family:Anton,sans-serif;font-size:34px;line-height:1;color:var(--bl);display:block;margin-bottom:10px}
.mk-ed .c b{display:block;font-size:17px;line-height:1.5;margin-bottom:8px}.mk-ed .c p{font-size:14px;color:var(--sub);margin:0}
/* voices */
.mk-vo{background:#f6f7f9}
.mk-vo .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mk-vo .v{background:#fff;border-radius:18px;padding:22px 20px;border:1px solid var(--line)}
.mk-vo .v p{margin:0 0 10px;font-size:14.5px;line-height:1.85}.mk-vo .v p::before{content:"“";color:var(--bl);font-size:1.5em;margin-right:2px}
.mk-vo .v small{font-size:12.5px;color:var(--sub);font-weight:700}
.mk-vo .srcn{font-size:12px;color:#8a95a0;margin-top:14px}
/* flow */
.mk-fl .st{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.mk-fl .st>div{background:#f6f7f9;border-radius:16px;padding:18px}
.mk-fl .st i{font-style:normal;font-family:Anton,sans-serif;font-size:26px;color:var(--bl);display:block;line-height:1;margin-bottom:8px}
.mk-fl .st b{display:block;font-size:15px;margin-bottom:4px}.mk-fl .st span{font-size:13.5px;color:var(--sub)}
.mk-lc .g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mk-lc .c{border:1px solid var(--line);border-radius:18px;padding:22px 20px}.mk-lc .c b{display:block;font-size:16px;margin-bottom:6px}.mk-lc .c p{font-size:14px;color:var(--sub);margin:0 0 8px}
.mk-lc .ex{display:grid;gap:6px;margin:10px 0}.mk-lc .ex span{background:var(--ye);border-radius:10px;padding:8px 12px;font-size:13.5px;font-weight:800}.mk-lc .c small{font-size:12px;color:#8a95a0}
@media(max-width:820px){.mk-lc .g{grid-template-columns:1fr}}
/* qa */
.mk-qa .qa{display:grid;gap:14px}.mk-qa .qa>div{background:#f6f7f9;border-radius:14px;padding:16px 18px}
.mk-qa .qa b{display:block;font-size:15px;margin-bottom:6px}.mk-qa .qa b::before{content:"Q. ";color:var(--bl)}.mk-qa .qa p{margin:0;font-size:14.5px;color:var(--sub)}
/* cta */
.mk-cta{position:relative;color:#fff;text-align:center;overflow:hidden;padding:96px 0!important;background:var(--k)}
.mk-cta .bg{position:absolute;inset:0}.mk-cta .bg img{width:100%;height:100%;object-fit:cover;display:block}
.mk-cta .sh{position:absolute;inset:0;background:rgba(21,23,28,.72)}.mk-cta .w2{position:relative}
.mk-cta p{color:#e2e2e2;margin:0 0 22px}.mk-cta .bt{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.mk-cta a{display:inline-block;font-weight:900;font-size:16px;padding:15px 30px;border-radius:999px;text-decoration:none;background:var(--ye);color:#15171c}
.mk-cta a.s{background:transparent;border:1.5px solid #fff;color:#fff}
/* info */
.mk-info .tb{border:1px solid var(--line);border-radius:14px;overflow:hidden;display:grid;grid-template-columns:120px 1fr;font-size:13.5px}
.mk-info .tb div{padding:13px 15px;border-bottom:1px solid #eef0f3}.mk-info .tb div:nth-last-child(-n+2){border-bottom:0}.mk-info .tb .k{background:#f6f7f9;font-weight:700;color:#555}
.mk-info .apply{display:block;text-decoration:none;background:linear-gradient(100deg,#fff4f6,#fef0ea);border:1px solid #f3c9da;border-radius:16px;padding:24px;text-align:center;margin:36px 0 0;color:#111}
.mk-info .apply b{display:block;font-size:17px;margin-bottom:6px}.mk-info .apply span{display:inline-block;background:#E43B4D;color:#fff;font-weight:800;padding:12px 28px;border-radius:999px;margin-top:10px}
.mk-info .disc{background:#f6f7f9;border-radius:14px;padding:18px 20px;font-size:12px;color:#8a95a0;margin-top:28px}
.mk-info .back{text-align:center;margin:22px 0 0}.mk-info .back a{font-size:13.5px;font-weight:700;color:#E43B4D;text-decoration:none}
@media(max-width:820px){.mk-gd .facts{grid-template-columns:1fr}.mk section{padding:48px 0}.mk-feat .g,.mk-sv .g,.mk-ed .g,.mk-vo .g{grid-template-columns:1fr}.mk-about .g{grid-template-columns:1fr;gap:24px}.mk-about .ph{max-width:260px}.mk-fl .st{grid-template-columns:1fr 1fr}.mk-gd .g{grid-template-columns:1fr 1fr}.mk-info .tb{grid-template-columns:104px 1fr}}
'''
works=[('w-narax','NARA-X様｜ポスター'),('w-lasolbona-kh','LA SOL BONA（フットサルチーム）様｜ユニフォームキーホルダー'),('w-trail','大江山トレイルラン教室様｜ロゴ'),('w-oeyama-flyer','大江山トレイルラン教室様｜チラシ'),('w-oeyama-medal','大江山トレイルラン教室様｜メダル'),('w-tsunagu','京都北山わくわくランニングフェスタ様｜ロゴ')]
body=f'''
<main class="mk">
<div class="mk-legend">確認用の草案です。内容はご確認のうえ修正できます。</div>

<section class="mk-hero">
  <div class="bg"><img src="{A}hero-bg.webp" alt=""></div><div class="sh"></div>
  <img class="chr c1" src="{A}ch1.webp" alt=""><img class="chr c4" src="{A}ch4.webp" alt=""><img class="chr c2" src="{A}ch2.webp" alt=""><img class="chr c3" src="{A}ch3.webp" alt="">
  <div class="in"><div class="w">
    <span class="pr">PR ｜ 企業紹介</span>
    <p class="brand">DESIGN <em>×</em> SPORTS<small>makkiedrops design ｜ マッキードロップスデザイン</small></p>
    <h1>スポーツの現場を知るデザイナーが、<br>チームの「ほしい」を形にする。</h1>
    <p class="ld">ロゴ、部員募集のポスターやチラシ、卒団記念のグッズまで。奈良・生駒のスポーツ専門デザイン事務所が、スポーツクラブのデザインをまとめて引き受けます。全国から依頼できます。</p>
    <div class="cta"><a class="p" href="{CONTACT}" target="_blank" rel="noopener sponsored">無料で見積もりを相談</a><a class="s" href="#works">制作実績を見る</a></div>
  </div></div>
</section>

<section class="mk-feat"><div class="w"><div class="g">
  <div class="c"><b>2016<i>年〜</i></b><span>スポーツを専門にしたデザイン事務所として設立</span></div>
  <div class="c"><b>1<i>個から</i></b><span>卒団記念・チームのおそろいグッズをオーダーできる</span></div>
  <div class="c"><b>6<i>メニュー</i></b><span>ロゴ・チラシ・ポスター・名刺・グッズ・年間サブスク</span></div>
</div></div></section>

<section class="mk-gd"><div class="w">
  <div class="ey">FOR CLUBS</div>
  <h2>卒団記念も、チームのおそろいも。<br>1個からオーダーできる。</h2>
  <p class="b">ユニフォームをそのまま小さくしたキーホルダー、チームロゴの3D立体キーホルダー、大会のメダル、応援タオル。人数の少ないクラブでも頼める数から作れます。</p>
  <div class="bn"><img src="{A}g-uniform-keyholder.webp" alt="ユニフォーム型キーホルダー"></div>
  <div class="g">
    <figure><img loading="lazy" src="{A}g-koriyama-towel.webp" alt="高校野球部のタオル"><figcaption>高校野球部のタオル</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-koriyama-kh.webp" alt="高校野球部のユニフォームキーホルダー"><figcaption>高校野球部のユニフォームキーホルダー</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-handball.webp" alt="中学ハンドボール部のユニフォームキーホルダー"><figcaption>中学ハンドボール部のユニフォームキーホルダー</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-angelics.webp" alt="チアダンスチームの記念キーホルダー"><figcaption>チアダンスチームの20周年記念キーホルダー</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-ekiden.webp" alt="小学生駅伝大会のメダル"><figcaption>小学生駅伝大会のメダル</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-wadaiko.webp" alt="和太鼓部のキーホルダー"><figcaption>和太鼓部のキーホルダー</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-orc.webp" alt="ランニングクラブの3Dキーホルダー"><figcaption>ランニングクラブの3Dキーホルダー</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-badge.webp" alt="缶バッジ"><figcaption>リフティング達成の缶バッジ</figcaption></figure>
    <figure><img loading="lazy" src="{A}g-keyholder.webp" alt="オリジナルキーホルダー"><figcaption>イラスト描き下ろしのキーホルダー</figcaption></figure>
  </div>
  <div class="facts">
    <div><b>卒団記念で人気</b><span>ユニフォームキーホルダー。1人あたりおよそ1,000円（税込）。</span></div>
    <div><b>お届けまで</b><span>注文から通常2週間〜1か月。注文が集中する時期は1か月半ほど。</span></div>
    <div><b>卒団式に間に合わせるなら</b><span>3月中旬の卒団式なら、1月中旬までに相談。12月中の注文だと余裕があります。</span></div>
  </div>
  <div class="cp"><div><small>チビスポ読者の特典</small><b>チビスポはじめましてクーポン｜10% OFF</b><span>オンラインショップで10%引きになります。デザイン制作の依頼も「チビスポを見た」と伝えると対応してもらえます。</span></div><code>{COUPON}</code></div>
</div></section>

<section class="mk-wk" id="works"><div class="w">
  <div class="ey" style="color:var(--ye)">WORKS</div>
  <h2>スポーツチームと作ってきたもの</h2>
  <p class="b">実業団・社会人チームからランニングイベント、地域のクラブまで。横にスクロールして見てください。</p>
  <div class="amrow">
    {''.join('<figure><img loading="lazy" decoding="async" src="%s%s.webp" alt="%s"><figcaption>%s</figcaption></figure>'%(A,n,c,c) for n,c in works)}
  </div>
  <a class="lk" href="{WORKS}" target="_blank" rel="noopener">制作実績をもっと見る（公式サイト）›</a>
</div></section>

<section class="mk-about"><div class="w"><div class="g">
  <div class="ph"><img src="{A}rep.webp" alt="makkiedrops design 代表 松田真樹さん"></div>
  <div>
    <div class="ey">ABOUT</div>
    <p class="q">「とにかくスポーツが好きなデザイナー」</p>
    <p class="b">代表の松田真樹さんは、大学4年生まで体操競技の選手でした。いまは地域で開かれるJリーグやBリーグの運営ボランティアに関わり、友人たちとリレーマラソンにも出ています。観ることも応援することも含めて、いろいろな形でスポーツの中にいる人です。</p>
    <p class="b">makkiedrops design は、そんな松田さんが2016年に始めた、スポーツを得意とするデザイン事務所。合言葉は「ともにパンパカパーン！」。スポーツ事業者と一緒に走りながら、熱量の高いデザインを作っています。</p>
    <p class="q2">「自分が作った制作物が町に貼られていたり、グッズを手にして実際に身に着けている方を見たりすると、嬉しいです」</p>
    <p class="nm">代表　松田真樹さん（makkiedrops）</p>
  </div>
</div></div></section>

<section class="mk-ed"><div class="w">
  <div class="ey">EDITOR'S VIEW ／ 取材メモ</div>
  <h2>取材してわかった、makkiedrops design の3つのポイント</h2>
  <div class="note-draft">※ 下書きです。サンプルが届いたら、実物を見たうえで書き直します。</div>
  <div class="g">
    <div class="c"><i>01</i><b>選手だった人が作っている</b><p>代表は大学まで体操競技の選手で、いまもJリーグやBリーグの運営ボランティアに立っています。ユニフォームや競技の雰囲気を一から説明しなくても伝わる相手に頼めるのは、クラブ運営者にとって時間の節約になります。</p></div>
    <div class="c"><i>02</i><b>プロチームと同じ作り手に、地域のクラブが頼める</b><p>Vリーグのチームのホームゲームポスターや、実業団の陸上チームのポスターを手がけてきた事務所です。その同じ手で、地域のクラブの部員募集ポスターや卒団記念のグッズも作ってもらえます。</p></div>
    <div class="c"><i>03</i><b>デザインからグッズの現物まで1か所で</b><p>ロゴを作って、ポスターにして、キーホルダーやタオルにするところまで一続き。1個から作れるので、卒団生の人数分だけ、という頼み方ができます。</p></div>
  </div>
</div></section>

<section class="mk-vo"><div class="w">
  <div class="ey">VOICE</div>
  <h2>届いたお客様の声</h2>
  <div class="g">
    <div class="v"><p>記念品のキーホルダー、大絶賛で、特に子どもたちは大喜びでした。</p><small>グッズ制作のお客様</small></div>
    <div class="v"><p>メダルですが子供達は、色が可愛いとかすごくオシャレとか色々言ってくれて、聞いてる限り好評でした。</p><small>大会の参加賞を依頼されたお客様</small></div>
    <div class="v"><p>迅速で親切なご対応感謝です！ユニフォームも細かいところまで、再現していただけてうれしいです！</p><small>ユニフォーム型グッズのお客様</small></div>
  </div>
  <div class="srcn">makkiedrops design に直接届いた声を、許可を得て掲載しています。</div>
</div></section>

<section class="mk-fl"><div class="w">
  <div class="ey">FLOW</div>
  <h2>依頼から納品まで</h2>
  <p class="b">遠方のクラブは、電話やZoomでの打ち合わせに対応しています。</p>
  <div class="st">
    <div><i>01</i><b>問い合わせ</b><span>公式サイトのフォームから。見積もりは無料。</span></div>
    <div><i>02</i><b>ヒアリング・打ち合わせ</b><span>ヒアリングシートに記入し、対面またはオンラインで方向を決める。</span></div>
    <div><i>03</i><b>見積・制作・修正</b><span>見積もりに納得してから制作開始。ラフ案を確認しながら仕上げる。</span></div>
    <div><i>04</i><b>校了・納品</b><span>OKを出してから請求書。入金確認後に納品。</span></div>
  </div>
</div></section>

<section class="mk-sv" id="service"><div class="w">
  <div class="ey">SERVICE ／ PRICE</div>
  <h2>メニューと料金</h2>
  <p class="b">料金はすべて税込です。</p>
  <div class="g">
    <div class="c hot"><em>ORIGINAL GOODS</em><b>オリジナルグッズ制作</b><p>参加賞・卒団記念・チームのおそろいに。ユニフォーム型キーホルダーは1個からオーダー可能。</p><div class="pr2">要相談<small>数量や素材で変わります。ユニフォームキーホルダーは1人あたりおよそ1,000円</small></div></div>
    <div class="c hot"><em>POSTER ／ FLIER</em><b>ポスター・チラシ制作</b><p>部員・会員募集、イベント告知に。遠くからでも目を引くデザイン。チラシはB4まで。</p><div class="pr2">チラシ 44,000円〜／ポスター 66,000円〜<small>修正3回まで</small></div></div>
    <div class="c hot"><em>LOGO</em><b>ロゴ制作</b><p>チームのイメージをヒアリングして、実用性とイメージアップを兼ねたロゴに。</p><div class="pr2">55,000円〜77,000円<small>3提案まで・修正回数は無制限</small></div></div>
    <div class="c"><em>SUBSCRIPTION</em><b>年間サブスクリプション</b><p>1年間で使うポスターやSNSバナーを、予算に応じてまとめて制作。</p><div class="pr2">月額 16,500円〜<small>年間契約・要相談</small></div></div>
    <div class="c"><em>BUSINESS CARD</em><b>名刺制作</b><p>ロゴとあわせて依頼されることが多いメニュー。</p><div class="pr2">22,000円〜<small>表のみ。表・裏は 33,000円〜</small></div></div>
    <div class="c"><em>LICENSE</em><b>ライセンス契約でのグッズ化</b><p>注文の受付から発送まで任せられる受注生産。チームは在庫を持たず、売れた分だけ受け取れます。</p><div class="pr2">在庫の負担なし<small>くわしくは下の「ライセンス契約」へ</small></div></div>
  </div>
</div></section>

<section class="mk-lc" id="license"><div class="w">
  <div class="ey">LICENSE</div>
  <h2>在庫を持たずに、チームのグッズを売る</h2>
  <p class="b">チームに代わって、注文の受付からお客様への発送まで makkiedrops design が行うライセンス契約。完全受注生産なので、チームで在庫を抱える必要がありません。</p>
  <div class="g">
    <div class="c"><b>仕組み</b><p>オンラインショップにチームの商品を掲載し、注文を受けてから製作・発送。商品が1点売れるごとに、あらかじめ決めた金額がチームに支払われます。</p><div class="ex"><span>例｜販売価格 1,000円 → チームへ 200円</span><span>例｜販売価格 1,500円 → チームへ 400円</span></div><small>支払い額は商品によって異なります。相談時に案内されます。</small></div>
    <div class="c"><b>対応している商品</b><p>ユニフォームキーホルダー／3Dキーホルダー／ピンバッジ／タオル</p><b style="margin-top:14px">支払いの時期</b><p>チームへの支払い額の累計が10,000円以上になると、翌月末に指定口座へ振込。満たない場合は繰り越し、半年を目安に精算されます。</p></div>
    <div class="c"><b>知っておきたいこと</b><p>チームのイベントなどで直接販売する分は、チームでの買い取りになります。</p><p>3年間、商品の売上がない場合は契約終了となります。</p></div>
  </div>
</div></section>

<section class="mk-qa"><div class="w2">
  <div class="ey">Q&amp;A</div>
  <h2>聞いておきたいこと</h2>
  <p class="b">スポーツクラブ向けに聞いておきたいことをお尋ねしました。</p>
  <div class="qa">
    <div><b>奈良県外のクラブからも依頼できますか？</b><p>全国対応です。打ち合わせは電話やZoomで行えます。</p></div>
    <div><b>予算が少ない小さなクラブでも頼めますか？</b><p>グッズ販売のライセンス契約なら、在庫を持たずに始められます。キーホルダー類は1つからでも制作可能です。デザイン制作のサブスクリプションも、予算に合わせて制作物を相談できます。</p></div>
    <div><b>卒団式や大会に間に合わせるには、いつまでに相談すればいいですか？</b><p>キーホルダーは注文から通常2週間〜1か月。3月中旬の卒団式なら1月中旬までに相談を。大会は、Tシャツやタオルなど制作に時間がかかるものがあるので、2か月前くらいを目安に。</p></div>
  </div>
</div></section>

<section class="mk-cta"><div class="bg"><img src="{A}w-narax-set.webp" alt=""></div><div class="sh"></div><div class="w2">
  <h2>チームのデザイン、まとめて相談。</h2>
  <p>見積もりは無料。作りたいものが決まっていなくても大丈夫です。<br>オンラインショップでは「チビスポはじめましてクーポン」<b style="color:var(--ye);letter-spacing:.06em"> {COUPON} </b>で10% OFFになります。</p>
  <div class="bt"><a href="{CONTACT}" target="_blank" rel="noopener sponsored">無料で見積もりを相談</a><a class="s" href="{SHOP}" target="_blank" rel="noopener sponsored">オンラインショップ</a></div>
</div></section>

<section class="mk-info"><div class="w2">
  <h2 style="font-size:22px">事業所情報</h2>
  <div class="tb">
    <div class="k">事業所名</div><div>makkiedrops design（マッキードロップスデザイン）</div>
    <div class="k">代表</div><div>松田真樹</div>
    <div class="k">設立</div><div>2016年1月1日</div>
    <div class="k">事業内容</div><div>企画、イラスト、ポスター、チラシ、グッズ等各種デザイン制作</div>
    <div class="k">所在地</div><div>奈良県生駒市谷田町1615 アコール もやい館3階 IKOMA-DO内</div>
    <div class="k">対応</div><div>全国対応（対面の打ち合わせは近隣のみ。遠方は電話・Zoom）</div>
    <div class="k">Instagram</div><div><a href="{IG}" target="_blank" rel="noopener sponsored" style="color:var(--bl);font-weight:700">@makkiedropsdesign</a></div>
  </div>
  <a class="apply" href="service-ads.html"><b>あなたのお店も、こんなページで紹介しませんか？</b>地域の子育て世帯に届く、チビスポの企業紹介ページ。<br><span>掲載を申し込む ›</span></a>
  <div class="disc">この記事は、makkiedrops design の提供による<strong style="color:#555">チビスポのPR記事（広告）</strong>です。料金・内容は makkiedrops design からの回答と公式サイトの掲載内容（2026年10月時点）にもとづきます。最新情報は公式サイトをご確認ください。</div>
  <div class="back"><a href="search.html">‹ クラブを探すに戻る</a></div>
</div></section>
</main>
'''
C.prodpage('pr/makkiedrops.html','makkiedrops design（マッキードロップスデザイン）｜チビスポ 企業紹介','スポーツ専門のデザイン事務所。ロゴ・部員募集ポスター・卒団記念グッズまで、スポーツクラブのデザインをまとめて相談できます。',body,css=CSS,noindex=True,base_root=True,og_image='https://chibispo.com/assets/pr/makkiedrops/g-uniform-keyholder.webp')
