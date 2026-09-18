# ---- 有料プラン（plans.html）：スタンダード／プロで何が変わるかを、実際の画面のスクショで見せる。
#      無料掲載との比較は listing.html に任せ、このページは有料の2プランを別ブロックで説明する。
#      svc_listing.py の後に exec（sl_css を継承：.rv .ey .sec2 .cmp .svcta .svnav .sbar .lp-go）
#      機能の記述はコードの実装に合わせる：順位＝shared.js ChibiPlan.rank（pr-plus 2 > pr 1 > free 0）／
#      おすすめ枠＝search.html showRec（検索ページは全国の有料クラブ・地域ページは地域に無ければ全国）／
#      写真上限＝club-mypage・club_prod.js（1／7／15）／分析＝Worker /api/dashboard とその周辺APIはすべてプロ限定（2026-09-18）／
#      SNS連携＝Worker /auth/*/start（pro 限定）／30日無料＝スタンダード月額のみ（Stripe 設定・ユーザー確認済）
#      実画面のスクショ（assets/plans/pc-*.webp）は、検証用クラブ（城東 18a23e5d…）をローカルのプロキシで
#      架空クラブ16件（名古屋9・東京7、名前・紹介文・写真＝サイト内ストック）に**一覧ごと差し替えて**描画し、PC1280／スマホ390で撮ったもの。本番DBは触っていない。
#      検索結果の先頭1カラム大カード＝prod_search.py の .nc-feat（有料クラブを1ページ目で拡大）
pl_css=sl_css+r'''
/* ===== 料金ページ固有 ===== */
.pl-hero{position:relative;background:#101215;color:#fff;overflow:hidden}
.pl-hero::before{content:"PLANS";position:absolute;right:-10px;top:-18px;font-family:'Anton',sans-serif;font-size:clamp(120px,26vw,340px);line-height:.84;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.10);pointer-events:none}
.pl-hero .in{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:50px 20px 0;display:grid;grid-template-columns:1fr;gap:30px;align-items:end}
.pl-hero .ey{color:var(--accent)}
.pl-hero h1{font-family:var(--fh);margin:0 0 14px;font-size:clamp(30px,7.6vw,54px);font-weight:900;line-height:1.18;letter-spacing:-.015em}
.pl-hero h1 em{font-style:normal;color:var(--accent)}
.pl-hero h1 span{display:inline-block;opacity:0;transform:translateY(18px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.pl-hero h1 span:nth-child(2){animation-delay:.12s}.pl-hero h1 span:nth-child(3){animation-delay:.24s}
.pl-hero .ld{font-size:14px;font-weight:700;color:rgba(255,255,255,.78);line-height:1.9;max-width:540px;margin:0 0 20px}
.pl-hero .cta{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:26px}
.pl-hero .b1{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 28px;box-shadow:0 8px 24px rgba(232,69,95,.35)}
.pl-hero .b2{border:1.5px solid rgba(255,255,255,.75);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 24px}
.pl-hero .prices{display:flex;gap:22px;padding:16px 0 30px;border-top:1px solid rgba(255,255,255,.22)}
.pl-hero .prices div{font-family:'Anton',sans-serif;letter-spacing:.06em}
.pl-hero .prices b{display:block;font-size:30px;font-weight:400;line-height:1;color:#fff}
.pl-hero .prices b small{font-family:var(--f);font-size:11px;font-weight:700;color:rgba(255,255,255,.6);letter-spacing:0;margin-left:3px}
.pl-hero .prices small{font-size:10.5px;letter-spacing:.22em;color:rgba(255,255,255,.6)}
.pl-hero .prices div.hot b{color:var(--accent)}
/* ヒーロー右：PC画面（ブラウザ枠）＋スマホ画面を重ねる */
.pl-hero .hshot{position:relative;width:100%;padding:0 0 40px 24px;opacity:0;transform:translateY(30px);animation:up .9s .35s cubic-bezier(.2,.7,.2,1) forwards}
.pl-hero .hshot .win{box-shadow:0 30px 60px rgba(0,0,0,.5)}
.pl-hero .hshot .ph{position:absolute;left:0;bottom:0;width:132px;border-width:5px;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,.55)}
.pl-hero .hshot .tag{position:absolute;right:-6px;top:-16px;z-index:2;background:var(--accent);color:#fff;font-size:12px;font-weight:900;line-height:1.5;padding:8px 12px;box-shadow:0 8px 20px rgba(0,0,0,.4);transform:rotate(2deg);max-width:250px}
.pl-hero .hshot .tag b{display:block;font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.2em;font-weight:400;opacity:.85}
/* 実画面の見せ方：ブラウザ枠とスマホ枠 */
.win{width:100%;background:#fff;border-radius:10px;overflow:hidden;border:1px solid var(--line);box-shadow:0 18px 40px rgba(0,0,0,.14)}
.win::before{content:"";display:block;height:22px;background:#e9ebef;border-bottom:1px solid #d9dde3;background-image:radial-gradient(circle at 12px 11px,#f06a6a 4px,transparent 4.5px),radial-gradient(circle at 28px 11px,#f5c04a 4px,transparent 4.5px),radial-gradient(circle at 44px 11px,#5fca70 4px,transparent 4.5px)}
.win img{width:100%;display:block}
.ph{width:250px;max-width:100%;border:7px solid #1b1d21;border-radius:30px;background:#fff;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.35);position:relative;margin:0 auto}
.ph img{width:100%;display:block}
.fb.dark .win{border-color:transparent;box-shadow:0 26px 50px rgba(0,0,0,.45)}
.vi .cap{position:absolute;left:12px;bottom:12px;background:#111;color:#fff;font-size:10.5px;font-weight:900;padding:6px 10px;box-shadow:0 8px 20px rgba(0,0,0,.25);max-width:calc(100% - 24px);line-height:1.5}
.fb.dark .vi .cap{background:#fff;color:#111}
.vi .lb{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.2em;color:var(--sub);margin:0 0 6px}
.fb.dark .vi .lb{color:rgba(255,255,255,.6)}
.only-pc{display:none}
.combo{position:relative;width:100%;padding:0 0 26px 0}
.combo .win{width:100%}
.combo .ph{position:absolute;right:-4px;bottom:0;width:120px;border-width:5px;border-radius:20px;margin:0}
/* PRの拡大吹き出し */
.zoom{position:absolute;left:14px;top:14px;z-index:3;background:#fff;border:2px solid var(--accent);border-radius:8px;padding:8px 10px;font-size:11px;font-weight:900;line-height:1.5;box-shadow:0 10px 24px rgba(0,0,0,.25);max-width:190px}
.zoom b{display:inline-block;background:var(--accent);color:#fff;font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.14em;padding:3px 7px;border-radius:3px;margin-right:6px;vertical-align:1px}
/* プランの頭（帯） */
.plan-head{position:relative;border:2px solid var(--ink);background:var(--card);padding:24px 20px 22px;display:grid;gap:14px;margin-bottom:22px;overflow:hidden}
.plan-head.hot{border-color:var(--accent);box-shadow:8px 8px 0 var(--accent)}
.plan-head.pro{background:#101215;color:#fff;border-color:#101215;box-shadow:8px 8px 0 var(--ink)}
.plan-head::after{content:attr(data-big);position:absolute;right:-6px;top:-14px;font-family:'Anton',sans-serif;font-size:clamp(80px,18vw,170px);line-height:.9;color:transparent;-webkit-text-stroke:1px rgba(31,36,48,.14);pointer-events:none}
.plan-head.pro::after{-webkit-text-stroke:1px rgba(255,255,255,.14)}
.plan-head .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent)}
.plan-head h2{margin:0;font-family:var(--fh);font-size:clamp(24px,6vw,36px);font-weight:900;line-height:1.25;letter-spacing:-.015em}
.plan-head h2 em{font-style:normal;color:var(--accent)}
.plan-head .for{font-size:13px;font-weight:700;color:var(--sub);line-height:1.9;margin:0}
.plan-head.pro .for{color:rgba(255,255,255,.72)}
.plan-head .pr-row{display:flex;gap:16px 26px;flex-wrap:wrap;align-items:flex-end;position:relative}
.plan-head .pr-row div{font-family:'Anton',sans-serif;letter-spacing:.02em}
.plan-head .pr-row b{display:block;font-size:40px;font-weight:400;line-height:1}
.plan-head .pr-row b small{font-family:var(--f);font-size:12px;font-weight:700;color:var(--sub);letter-spacing:0;margin-left:4px}
.plan-head.pro .pr-row b small{color:rgba(255,255,255,.6)}
.plan-head .pr-row small.u{display:block;font-family:var(--f);font-size:11.5px;font-weight:700;color:var(--sub);letter-spacing:0;margin-top:6px}
.plan-head.pro .pr-row small.u{color:rgba(255,255,255,.6)}
.plan-head .pr-row .y b{font-size:26px}
.plan-head .badge30{display:inline-block;background:var(--accent);color:#fff;font-size:11px;font-weight:900;padding:4px 9px;letter-spacing:.04em;margin-bottom:8px;font-family:var(--f)}
.plan-head .cta{display:flex;gap:10px;flex-wrap:wrap;position:relative}
.plan-head .cta .lp-go{display:inline-block;padding:13px 22px;font-size:14px}
.plan-head.hot .cta .b1{background:var(--accent);border-color:var(--accent);color:#fff}
.plan-head.pro .cta .lp-go{border-color:#fff;color:#fff}
.plan-head.pro .cta .b1{background:#fff;color:#111}
.plan-head .pts{list-style:none;margin:0;padding:12px 0 0;border-top:1px solid var(--line);display:grid;gap:6px 14px;grid-template-columns:1fr}
.plan-head.pro .pts{border-top-color:rgba(255,255,255,.2)}
.plan-head .pts li{position:relative;padding-left:18px;font-size:12.5px;font-weight:700;line-height:1.6}
.plan-head .pts li::before{content:"";position:absolute;left:0;top:8px;width:9px;height:5px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
/* 機能ブロック：文＋画面の2カラム。画面は必要な部分だけを大きく */
.fb-list{display:grid;gap:18px}
.fb{border:1px solid var(--ink);background:var(--card);display:grid;grid-template-columns:1fr;overflow:hidden}
.fb .tx{padding:22px 20px 18px;display:grid;gap:10px;align-content:start}
.fb .n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.2em;color:var(--accent)}
.fb h3{font-family:var(--fh);margin:0;font-size:19px;font-weight:900;line-height:1.35}
.fb p{margin:0;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.fb .pts{list-style:none;margin:2px 0 0;padding:0;display:grid;gap:5px}
.fb .pts li{position:relative;padding-left:18px;font-size:12.5px;font-weight:700;line-height:1.6}
.fb .pts li::before{content:"";position:absolute;left:0;top:8px;width:9px;height:5px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
.fb .vi{position:relative;background:#eef0f3;padding:22px 18px 46px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.fb.dark .vi{background:#101215}
.fb.dark .tx{background:#101215;color:#fff}
.fb.dark .tx p{color:rgba(255,255,255,.72)}
.fb.dark{border-color:#101215;background:#101215}
/* プロの箇条 */
.pro-extra{display:grid;grid-template-columns:1fr;gap:10px;margin-top:18px}
.pro-extra div{border:1px solid var(--ink);padding:14px 16px;font-size:13px;font-weight:900;line-height:1.6;display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:start}
.pro-extra div i{font-style:normal;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.16em;color:var(--accent);padding-top:3px}
.pro-extra div small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px}
/* 比較表（スタンダード／プロの2列） */
.cmp.two-col th:first-child{width:52%}
.cmp.two-col td.sm{font-size:11.5px;color:var(--sub)}
.cmp.two-col tr.sec td{background:#f2f3f5;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em;color:var(--sub);text-align:left;padding:8px}
.cmp.two-col td .lp-go{display:block;font-size:12px;padding:9px 6px;border:1.5px solid var(--ink);color:var(--ink);font-family:var(--fh);font-weight:900}
.cmp.two-col td.hot .lp-go{background:var(--accent);border-color:var(--accent);color:#fff}
.cmp.two-col td a.tr{display:block;font-size:10.5px;margin-top:6px}
@media(max-width:899px){.cmp.two-col{font-size:11.5px}.cmp.two-col th,.cmp.two-col td{padding:9px 4px}.cmp.two-col td:first-child{padding-left:0}.cmp.two-col tr.cmp-btn{display:none}}
/* 支払い・変更 */
.bl-grid{display:grid;grid-template-columns:1fr;gap:12px}
.bl{border:1px solid var(--ink);background:var(--card);padding:18px 18px 16px;display:grid;gap:6px;align-content:start}
.bl .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--accent)}
.bl h3{font-family:var(--fh);margin:0;font-size:15.5px;font-weight:900;line-height:1.45}
.bl p{margin:0;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
/* FAQ（サイト共通の .faq と衝突するので別名） */
.plfaq{display:grid;gap:10px}
.plfaq details{border:1px solid var(--ink);background:var(--card)}
.plfaq summary{list-style:none;cursor:pointer;padding:14px 16px;font-size:14px;font-weight:900;display:flex;justify-content:space-between;align-items:center;gap:12px;line-height:1.5;text-align:left}
.plfaq summary::-webkit-details-marker{display:none}
.plfaq summary::before{content:none}
.plfaq summary::after{content:"+";font-family:'Anton',sans-serif;font-size:18px;color:var(--accent);flex:0 0 auto}
.plfaq details[open] summary::after{content:"–"}
.plfaq .a{padding:0 16px 16px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.free-note{margin-top:18px;border:1px dashed var(--line);padding:12px 14px;font-size:12px;font-weight:700;color:var(--sub);line-height:1.8}
.free-note a{color:var(--accent);text-decoration:underline;font-weight:900}
@media(min-width:900px){
  .pl-hero .in{grid-template-columns:1fr 1.05fr;padding:70px 20px 0;gap:44px;align-items:center}
  .pl-hero .hshot{padding:0 0 50px 40px}
  .pl-hero .hshot .ph{width:170px;border-width:6px;border-radius:24px}
  .only-pc{display:block}.only-sp{display:none}
  .plan-head{grid-template-columns:1.1fr .9fr;gap:14px 30px;padding:30px 30px 26px}
  .plan-head .pts{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}
  .plan-head .cta{grid-column:1}
  .plan-head .pr-row{grid-column:2;grid-row:1/4;align-self:start;justify-self:end;flex-direction:column;align-items:flex-end;gap:12px;text-align:right}
  .fb{grid-template-columns:38fr 62fr}
  .fb.flip{grid-template-columns:62fr 38fr}
  .fb.flip .tx{order:2}
  .fb .tx{padding:30px 28px 28px;align-content:center}
  .fb h3{font-size:22px}
  .fb .vi{padding:28px 28px 50px;min-height:340px}
  .fb .vi>.win,.fb .vi>.combo{max-width:720px}
  .fb .vi>.ph{width:270px}
  .combo{padding:0 70px 30px 0}
  .combo .ph{width:170px;right:0;bottom:0;border-width:6px;border-radius:24px}
  .pro-extra{grid-template-columns:repeat(3,1fr)}
  .bl-grid{grid-template-columns:repeat(3,1fr)}
}
'''
pl_body='''
<main>
<section class="pl-hero">
  <div class="in">
    <div>
      <div class="ey">FOR CLUBS ・ PAID PLANS</div>
      <h1><span>地域で探した保護者に、</span><span><em>いちばん先に</em></span><span>見つかる。</span></h1>
      <p class="ld">有料プラン（スタンダード・プロ）にすると、クラブの見え方がどう変わるか。図ではなく、実際のチビスポの画面でお見せします。掲載・体験申込の受付・保護者とのやりとりは、これまでどおり無料です。</p>
      <div class="cta"><a class="b1" data-plan-go="pr" href="register.html?plan=pr">スタンダードを30日無料で試す</a><a class="b2" href="#pro">プロを見る</a></div>
      <div class="prices"><div class="hot"><b>¥3,000<small>/月</small></b><small>STANDARD ・ 30 DAYS FREE</small></div><div><b>¥10,000<small>/月</small></b><small>PRO</small></div></div>
    </div>
    <div class="hshot"><div class="tag"><b>REAL SCREEN</b>名古屋市で絞った検索結果。<br>有料クラブが1番目に、大きく</div><div class="win"><img src="assets/plans/pc-search-top.webp" alt="名古屋市で絞った検索結果。有料クラブが1番目に横いっぱいのカードで表示" loading="eager"></div><div class="ph"><img src="assets/plans/sp-search-top.webp" alt="同じ検索結果のスマホ表示" loading="eager"></div></div>
  </div>
</section>
<div class="wrap">

  <section class="sec2" id="standard">
    <div class="plan-head hot rv" data-big="STANDARD">
      <div><div class="k">STANDARD</div><h2>スタンダード<br>地域で探されたとき、<em>最初に出る</em>。</h2></div>
      <p class="for">募集の時期に「載っているのに見られない」を減らすプランです。お支払いが確認できた時点で、すべて自動で切り替わります。設定はいりません。</p>
      <div class="cta"><a class="lp-go b1" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="lp-go" data-plan-go="pr-y" href="register.html?plan=pr-y">年額で申し込む</a></div>
      <div class="pr-row"><div><span class="badge30">初回30日は¥0</span><b>¥3,000<small>/月</small></b><small class="u">31日目から。いつでも解約できます</small></div><div class="y"><b>¥30,000<small>/年</small></b><small class="u">2ヶ月分お得（月あたり¥2,500）</small></div></div>
      <ul class="pts"><li>地域で絞った検索で、1番目に大きく表示</li><li>ほかの地域の検索でも「おすすめクラブ」に</li><li>トップの「編集部おすすめ」・「近くのクラブ」でも先頭</li><li>写真を7枚まで（フリーは1枚）</li><li>カードに「PR」表示</li><li>初回30日は¥0・いつでも解約</li></ul>
    </div>
    <div class="fb-list">
      <div class="fb rv"><div class="tx"><div class="n">01</div><h3>地域で絞ると、最初に、1カラムで大きく出ます。</h3><p>保護者は「都道府県 → 市区町村」で絞ってクラブを探します。その一覧のいちばん上に、有料プランのクラブだけが横いっぱいの大きなカードで出ます。写真も紹介文も、ほかのクラブより大きく見えます。市区町村ごとのクラブ一覧ページも同じです。同じプラン同士は新着順です。</p></div>
        <div class="vi"><div class="win only-pc"><div class="zoom"><b>PR</b>有料プランのカードには、小さくPRが付きます</div><img src="assets/plans/pc-search-top.webp" alt="名古屋市で絞った検索結果。有料クラブが1番目に大きなカードで" loading="lazy"></div><div class="ph only-sp"><img src="assets/plans/sp-search-top.webp" alt="名古屋市で絞った検索結果。有料クラブが1番目に大きなカードで" loading="lazy"></div><div class="cap">実際の画面：愛知県 → 名古屋市で絞った検索結果（9クラブ中の1番目）</div></div></div>
      <div class="fb rv flip"><div class="tx"><div class="n">02</div><h3>近くの市や、ほかの県で探している保護者にも届きます。</h3><p>検索ページの「おすすめクラブ」枠は、有料プランのクラブだけが入る枠です。地域を絞る前の保護者にも、別の市や県で検索している保護者にも表示されます。隣の市から通ってくれる子は、ここから見つかります。</p><ul class="pts"><li>検索ページ：全国の有料クラブから表示</li><li>市区町村ページ：その地域に有料クラブがなければ、ほかの地域の有料クラブを表示</li></ul></div>
        <div class="vi"><div class="ph"><img src="assets/plans/sp-other-pickup.webp" alt="東京都で検索したときの「おすすめクラブ」枠に、名古屋市のクラブが表示されている" loading="lazy"></div><div class="cap">実際の画面：東京都で検索したときの「おすすめクラブ」枠。名古屋市のクラブが出ている</div></div></div>
      <div class="fb rv"><div class="tx"><div class="n">03</div><h3>トップページと、ほかのクラブのページでも先頭です。</h3><p>トップページの「編集部おすすめ」は有料プランのクラブを先に並べます。同じ地域のほかのクラブページの下にある「近くのクラブ」でも、先頭に出ます。保護者がどこから入ってきても、先に目に入る位置です。</p></div>
        <div class="vi"><div class="combo"><div class="lb">TOP ・ 編集部おすすめ ／ CLUB PAGE ・ 近くのクラブ</div><div class="win"><img src="assets/plans/pc-top-picks.webp" alt="トップページの編集部おすすめ枠で先頭に表示" loading="lazy"></div><div class="ph"><img src="assets/plans/sp-near.webp" alt="ほかのクラブページの「近くのクラブ」で先頭に表示" loading="lazy"></div></div></div></div>
      <div class="fb rv flip"><div class="tx"><div class="n">04</div><h3>写真が7枚まで。1枚目がカバーです。</h3><p>フリーは1枚のところ、練習の様子・コーチ・保護者が見守る場所・持ち物まで、雰囲気が伝わる順に7枚。表示位置の調整・並べ替え・削除は、クラブのマイページからいつでもできます。</p></div>
        <div class="vi"><div class="win"><img src="assets/plans/pc-club-photos.webp" alt="クラブページの写真欄。7枚まで並ぶ" loading="lazy"></div><div class="cap">実際の画面：クラブページの「写真」欄（横にスクロールで7枚）</div></div></div>
    </div>
    <div class="free-note">無料掲載でできること（クラブページ・検索と地図への掲載・体験申込の受付）は <a href="service-listing-preview.html">クラブを載せる</a> のページにまとめています。</div>
  </section>

  <section class="sec2" id="pro">
    <div class="plan-head pro rv" data-big="PRO">
      <div><div class="k">PRO</div><h2>プロ<br>見られた数から、<em>効いた広報</em>まで見える。</h2></div>
      <p class="for">スタンダードの見つかり方に加えて、クラブ分析が開きます。何回見られて何件申し込まれたか、どの広報から来たか、保護者がどう感じているかが1つの画面にまとまります。</p>
      <div class="cta"><a class="lp-go b1" data-plan-go="pr-plus" href="register.html?plan=pr-plus">プロで申し込む</a><a class="lp-go" data-plan-go="pr-plus-y" href="register.html?plan=pr-plus-y">年額で申し込む</a></div>
      <div class="pr-row"><div><b>¥10,000<small>/月</small></b><small class="u">初月から。無料期間はありません</small></div><div class="y"><b>¥100,000<small>/年</small></b><small class="u">2ヶ月分お得（月あたり¥8,333）</small></div></div>
      <ul class="pts"><li>スタンダードのすべて</li><li>クラブ分析：閲覧数・申込・入会が1画面</li><li>QR・計測リンクで「どこから来たか」</li><li>SNS連携（Instagram・Threads・YouTube）と投稿の分析</li><li>保護者アンケート（QR配布・自動集計）</li><li>写真を15枚まで・順位はスタンダードより上・公式SNSで月1回紹介</li></ul>
    </div>
    <div class="fb-list">
      <div class="fb rv dark"><div class="tx"><div class="n">01</div><h3>何回見られて、何件申し込まれたかが、1画面で。</h3><p>クラブページの閲覧数（直近30日）、体験申込、入会、会員数をひとつの画面で。電話や紙の申込も「＋記録」から10秒で足せます。目標までの逆算と6ヶ月の推移、AIの「今週の一手」も一緒に見えます。</p></div>
        <div class="vi"><div class="ph"><img src="assets/plans/dash-now-sp.webp" alt="クラブ分析「いま」タブ" loading="lazy"></div><div class="cap">クラブ分析の画面（サンプルの数字）</div></div></div>
      <div class="fb rv dark flip"><div class="tx"><div class="n">02</div><h3>保護者アンケートが、配るだけで集計されます。</h3><p>QRを印刷して配るだけ。どこでクラブを知ったか、満足度、友人にすすめたい度（NPS）が自動で集計され、ほかのクラブの平均と並びます。結果からAIが改善のアドバイスを出します。</p></div>
        <div class="vi"><div class="win only-pc"><img src="assets/plans/dash-survey-pc.webp" alt="保護者アンケートの集計画面" loading="lazy"></div><div class="ph only-sp"><img src="assets/plans/dash-survey-sp.webp" alt="保護者アンケートの集計画面" loading="lazy"></div><div class="cap">クラブ分析「保護者アンケート」（サンプルの数字）</div></div></div>
      <div class="fb rv dark"><div class="tx"><div class="n">03</div><h3>QR・計測リンクで、「どこから来たか」を数えます。</h3><p>駅前のポスター、体験会のチラシ、紹介カード。配る場所ごとにQRを発行すると、読み取られた数と、そこからの体験申込が並びます。効いている場所を増やし、効いていない場所をやめられます。</p><ul class="pts"><li>QRは分析画面から何枚でも発行</li><li>チビスポのページに来た経路（SNS・検索・直接）も自動で</li></ul></div>
        <div class="vi"><div class="win only-pc"><img src="assets/plans/dash-sources-pc.webp" alt="どこから来ているか" loading="lazy"></div><div class="ph only-sp"><img src="assets/plans/dash-sources-sp.webp" alt="どこから来ているか" loading="lazy"></div><div class="cap">集客タブ「どこから来ているか」（サンプルの数字）</div></div></div>
      <div class="fb rv dark flip"><div class="tx"><div class="n">04</div><h3>SNSをつなぐと、投稿の反応が毎朝たまります。</h3><p>Instagram・Threads・YouTubeを連携すると、投稿と反応（♥・コメント・表示回数）を毎朝6時に自動で取り込みます。どのタイプの投稿が反応されているか、当たり投稿の共通点、投稿が続いているかが見えます。</p><ul class="pts"><li>投稿のタイプ分け（試合・コーチ・練習・募集）はAIが自動</li><li>週ごとの本数で「続いているか」を確認</li></ul></div>
        <div class="vi"><div class="ph"><img src="assets/plans/dash-post-sp.webp" alt="投稿タブ" loading="lazy"></div><div class="cap">投稿タブ（サンプルの数字）</div></div></div>
      <div class="fb rv dark"><div class="tx"><div class="n">05</div><h3>認知から入会まで、どの段階で減っているか。</h3><p>SNSで表示された回数 → ページに来た人 → 体験申込 → 体験参加 → 入会。5段階の数字と、子ども向けスポーツクラブの目安の率を並べて、いちばん弱い段階と直し方を示します。</p></div>
        <div class="vi"><div class="win only-pc"><img src="assets/plans/dash-funnel-pc.webp" alt="ファネル" loading="lazy"></div><div class="ph only-sp"><img src="assets/plans/dash-funnel-sp.webp" alt="ファネル" loading="lazy"></div><div class="cap">集客タブ「ファネル」（サンプルの数字）</div></div></div>
    </div>
    <div class="pro-extra rv">
      <div><i>06</i><span>写真が15枚まで<small>スタンダードの7枚から、さらに8枚</small></span></div>
      <div><i>07</i><span>順位はスタンダードより上<small>検索結果・おすすめクラブ・編集部おすすめ・近くのクラブ、すべてで先頭のグループ</small></span></div>
      <div><i>08</i><span>公式SNSで月1回紹介<small>チビスポのInstagram・Threadsで、クラブを紹介します</small></span></div>
    </div>
  </section>

  <section class="sec2" id="cmp">
    <div class="ey rv">STANDARD vs PRO</div>
    <h2 class="rv d1">2つのプランを、<em>一覧</em>で。</h2>
    <table class="cmp two-col rv">
      <tr><th>&nbsp;</th><th class="hot">STANDARD</th><th>PRO</th></tr>
      <tr class="sec"><td colspan="3">見つかり方</td></tr>
      <tr><td>地域で絞った検索で、先頭に大きなカードで表示</td><td class="hot">✓（2番目）</td><td>✓（1番目）</td></tr>
      <tr><td>「おすすめクラブ」枠（検索ページ・市区町村ページ）</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>トップ「編集部おすすめ」・「近くのクラブ」で先頭</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>写真の枚数</td><td class="hot"><b>7</b></td><td><b>15</b></td></tr>
      <tr><td>公式SNSで月1回紹介</td><td class="hot no">—</td><td>✓</td></tr>
      <tr class="sec"><td colspan="3">クラブ分析（プロだけ）</td></tr>
      <tr><td>閲覧数（直近30日）・申込・入会・会員数</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>目標までの逆算・6ヶ月の推移・AIの「今週の一手」</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>保護者アンケート（QR配布・自動集計）</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>QR・計測リンク（ポスター・チラシ・紹介カード）</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>SNS連携と投稿の分析</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>ファネル（認知から入会まで）</td><td class="hot no">—</td><td>✓</td></tr>
      <tr class="sec"><td colspan="3">料金</td></tr>
      <tr><td>月額</td><td class="hot"><b>¥3,000</b></td><td><b>¥10,000</b></td></tr>
      <tr><td>年額（2ヶ月分お得）</td><td class="hot"><b>¥30,000</b></td><td><b>¥100,000</b></td></tr>
      <tr><td>初回30日無料</td><td class="hot">月額のみ</td><td class="no">—</td></tr>
      <tr class="cmp-btn"><td>&nbsp;</td><td class="hot"><a class="lp-go" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="tr" data-plan-go="pr-y" href="register.html?plan=pr-y">年額で申し込む ›</a></td><td><a class="lp-go" data-plan-go="pr-plus" href="register.html?plan=pr-plus">プロで申し込む</a><a class="tr" data-plan-go="pr-plus-y" href="register.html?plan=pr-plus-y" style="color:var(--sub)">年額で申し込む ›</a></td></tr>
    </table>
  </section>

  <section class="sec2" id="billing">
    <div class="ey rv">BILLING</div>
    <h2 class="rv d1">支払いと変更は、<em>いつでも</em>。</h2>
    <div class="bl-grid">
      <div class="bl rv"><div class="k">PAYMENT</div><h3>クレジットカードで、自動で続きます。</h3><p>お支払いはクレジットカード（Stripe）です。月額は毎月、年額は毎年、申し込んだ日と同じ日に自動で決済されます。表示の金額がそのままお支払い額で、追加の税や手数料はありません。カード明細には「CHIBISPO」と載ります。</p></div>
      <div class="bl rv d1"><div class="k">30 DAYS FREE</div><h3>スタンダード月額は、初回30日が¥0です。</h3><p>申込時にカードの登録は必要ですが、30日以内に解約すれば請求はありません。31日目から¥3,000です。年額とプロには無料期間はありません。</p></div>
      <div class="bl rv d2"><div class="k">CHANGE</div><h3>プランの変更は、日割りで切り替わります。</h3><p>スタンダードからプロへ、月額から年額へ。クラブのマイページの「プランの変更・解約」（カスタマーポータル）から、差額は日割りで自動計算されます。</p></div>
      <div class="bl rv"><div class="k">CANCEL</div><h3>解約は、いつでも。違約金はありません。</h3><p>同じカスタマーポータルから解約できます。解約後もその請求期間の終わりまで有料の機能が使え、期間が終わると自動でフリーに戻ります。掲載は消えません。</p></div>
      <div class="bl rv d1"><div class="k">AFTER</div><h3>フリーに戻ると、写真は1枚目だけになります。</h3><p>順位は標準に、写真は1枚目だけの表示に戻ります。プロをやめると分析画面は閉じますが、登録した写真・記録・アンケートの回答は残るので、また有料にすれば続きから見られます。</p></div>
      <div class="bl rv d2"><div class="k">RECEIPT</div><h3>領収書は、その場で発行できます。</h3><p>カスタマーポータルから、決済ごとの領収書をいつでもダウンロードできます。請求書払いや団体でのお申し込みは、<a href="contact.html?who=club" style="color:var(--accent);text-decoration:underline">お問い合わせ</a>から相談してください。</p></div>
    </div>
  </section>

  <section class="sec2" id="faq">
    <div class="ey rv">FAQ</div>
    <h2 class="rv d1">有料プランについて、<em>よく聞かれること</em>。</h2>
    <div class="plfaq rv">
      <details><summary>スタンダードとプロ、どちらから始めればいいですか。</summary><div class="a">募集の時期に見てもらいたいだけなら、スタンダードで足ります。ポスターやSNSに手をかけていて「どれが効いているか」を知りたいなら、プロです。数字を見ながら運営したいなら、最初からプロです。分析画面（閲覧数・申込・アンケート）はプロだけに付きます。</div></details>
      <details><summary>「最初に出る」は、どういう並び順ですか。</summary><div class="a">同じ検索条件の中で、プロ → スタンダード → フリーの順に並びます。有料プランのクラブは一覧の先頭に、横いっぱいの大きなカードで出ます。同じプランの中は、これまでどおり新着順です。検索結果・市区町村ページ・おすすめクラブ枠・編集部おすすめ・近くのクラブ、すべて同じルールです。</div></details>
      <details><summary>ほかの地域の保護者にも見えるのは、どの画面ですか。</summary><div class="a">検索ページの「おすすめクラブ」枠です。この枠は有料プランのクラブだけが入り、検索している地域に関係なく表示されます。市区町村ページの同じ枠は、その地域に有料クラブがないときに、ほかの地域の有料クラブを表示します。</div></details>
      <details><summary>有料にすると、保護者からの見え方は変わりますか。</summary><div class="a">順番が上がり、写真が増え、おすすめ枠に入ります。クラブのカードには小さく「PR」と表示されます。それ以外の見た目や、体験申込の流れは変わりません。</div></details>
      <details><summary>お支払いが終わったあと、何かする必要はありますか。</summary><div class="a">ありません。お支払いが確認できた時点で、順位・写真の枚数・分析画面が自動で切り替わります。写真を増やすときだけ、クラブのマイページから追加してください。</div></details>
      <details><summary>複数のクラブや教室を運営しています。</summary><div class="a">プランはクラブページ1つごとです。2つのクラブページを上位にしたい場合は、それぞれで申し込みます。まとめての申し込みは<a href="contact.html?who=club" style="color:var(--accent);text-decoration:underline">お問い合わせ</a>から相談してください。</div></details>
      <details><summary>プロのSNS連携には、何が必要ですか。</summary><div class="a">クラブのInstagram・Threads・YouTubeのアカウントでログインして「連携する」を押すだけです。パスワードをこちらに渡す必要はありません。連携をやめるのも、分析画面の設定からいつでもできます。</div></details>
      <details><summary>プロをやめたら、分析のデータは消えますか。</summary><div class="a">消えません。記録した申込・入会・施策、アンケートの回答は残ります。もう一度プロにすると、続きから見られます。</div></details>
    </div>
  </section>

  <div class="svcta"><div class="big">PLANS</div><div class="in"><div class="ey">30 DAYS FREE</div><h2>募集の時期に、<br>最初に見つかるクラブへ。</h2><p>スタンダードは初回30日が¥0。合わなければ、期間内の解約で請求はありません。</p><div class="row"><a class="b1" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="b2" href="#pro">プロを見る</a></div></div></div>
  <div class="svnav"><span class="cur">有料プラン</span><a href="service-listing-preview.html">01 クラブを載せる</a><a href="service-sns-preview.html">03 SNS運用サポート</a><a href="hp-samples/">04 ホームページ制作</a><a href="service-ads-preview.html">05 地域の広告掲載</a><a href="faq.html">よくある質問</a></div>
  <div style="height:40px"></div>
</div>
<div class="sbar" id="sbar"><div class="t">スタンダード ¥3,000/月<small>初回30日無料・いつでも解約OK</small></div><a class="lp-go" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a></div>
</main>
'''
pl_js='''<script>
(function(){
 if(/noanim=1/.test(location.search)){var st=document.createElement('style');st.textContent='*{transition:none!important;animation:none!important}.pl-hero h1 span,.pl-hero .hshot{opacity:1!important;transform:none!important}';document.head.appendChild(st);document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});return}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
 document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
 /* ログイン中のクラブ運営者が有料プランを押したら、新規登録ではなくマイページのプラン選択へ（二重登録を防ぐ） */
 if(window.ChibiAuth&&ChibiAuth.ready&&ChibiAuth.ready()){ ChibiAuth.getProfile().then(function(p){ if(!p||p.role!=='club') return;
   document.querySelectorAll('[data-plan-go]').forEach(function(a){ a.href='club-mypage.html#mp-upsell'; }); }).catch(function(){}); }
 var sb=document.getElementById('sbar'),hero=document.querySelector('.pl-hero');
 if(sb&&hero)new IntersectionObserver(function(e){sb.classList.toggle('on',!e[0].isIntersecting&&e[0].boundingClientRect.top<0)},{threshold:0}).observe(hero);
})();
</script>'''
page('service-plans-preview.html','有料プラン｜スタンダード・プロで、クラブの見え方はこう変わる｜チビスポ（プレビュー）',pl_body,pl_css,extra_js=pl_js)
