# ---- 料金プラン（plans.html）：フリー／スタンダード／プロで何が変わるかを画面つきで説明する。
#      svc_listing.py の後に exec（sl_css を継承：.rv .ey .sec2 .plans .pl .cmp .svcta .svnav .sbar）
#      機能の記述はコードの実装に合わせる：順位＝shared.js ChibiPlan.rank（pr-plus 2 > pr 1 > free 0）／
#      写真上限＝club-mypage・club_prod.js（1／7／15）／分析＝Worker /api/dashboard（std は clicks・posts を返さない）／
#      SNS連携＝Worker /auth/*/start（pro 限定）／30日無料＝スタンダード月額のみ（Stripe 設定・ユーザー確認済）
pl_css=sl_css+r'''
/* ===== 料金ページ固有 ===== */
.pl-hero{position:relative;background:#101215;color:#fff;overflow:hidden}
.pl-hero::before{content:"PLANS";position:absolute;right:-10px;top:-18px;font-family:'Anton',sans-serif;font-size:clamp(120px,26vw,340px);line-height:.84;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.10);pointer-events:none}
.pl-hero .in{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:50px 20px 44px;display:grid;grid-template-columns:1fr;gap:34px;align-items:center}
.pl-hero .ey{color:var(--accent)}
.pl-hero h1{font-family:var(--fh);margin:0 0 14px;font-size:clamp(30px,7.6vw,56px);font-weight:900;line-height:1.15;letter-spacing:-.015em}
.pl-hero h1 em{font-style:normal;color:var(--accent)}
.pl-hero h1 span{display:inline-block;opacity:0;transform:translateY(18px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.pl-hero h1 span:nth-child(2){animation-delay:.12s}.pl-hero h1 span:nth-child(3){animation-delay:.24s}
.pl-hero .ld{font-size:14px;font-weight:700;color:rgba(255,255,255,.78);line-height:1.9;max-width:540px;margin:0 0 20px}
.pl-hero .cta{display:flex;gap:10px;flex-wrap:wrap}
.pl-hero .b1{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 28px;box-shadow:0 8px 24px rgba(232,69,95,.35)}
.pl-hero .b2{border:1.5px solid rgba(255,255,255,.75);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 24px}
.pl-hero .stats{display:flex;gap:26px;margin-top:26px;padding-top:18px;border-top:1px solid rgba(255,255,255,.22)}
.pl-hero .stats div{font-family:'Anton',sans-serif;letter-spacing:.06em}
.pl-hero .stats b{display:block;font-size:34px;font-weight:400;line-height:1;color:#fff}
.pl-hero .stats small{font-size:10.5px;letter-spacing:.22em;color:rgba(255,255,255,.6)}
/* ヒーロー右：3段のはしご */
.ladder{position:relative;display:grid;gap:10px;max-width:420px;margin:0 auto;width:100%}
.ladder .st{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.04);padding:14px 16px;opacity:0;transform:translateX(24px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.ladder .st:nth-child(1){animation-delay:.3s;margin-right:56px}.ladder .st:nth-child(2){animation-delay:.5s;margin-right:28px}.ladder .st:nth-child(3){animation-delay:.7s}
.ladder .st.hot{border-color:var(--accent);background:rgba(232,69,95,.12);box-shadow:0 12px 30px rgba(0,0,0,.35)}
.ladder .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.22em;color:rgba(255,255,255,.7);width:74px}
.ladder .st.hot .k{color:var(--accent)}
.ladder .t{font-size:12.5px;font-weight:900;line-height:1.5}
.ladder .t small{display:block;font-size:11px;font-weight:700;color:rgba(255,255,255,.62)}
.ladder .p{font-family:'Anton',sans-serif;font-size:22px;letter-spacing:.02em;white-space:nowrap}
.ladder .p small{font-family:var(--f);font-size:10px;font-weight:700;color:rgba(255,255,255,.6);letter-spacing:0}
.ladder .arrow{position:absolute;left:-2px;top:0;bottom:0;width:2px;background:linear-gradient(180deg,rgba(255,255,255,.1),var(--accent));transform:scaleY(0);transform-origin:top;animation:grow 1.2s .5s ease-out forwards}
@keyframes grow{to{transform:none}}
/* どれが合うか */
.picks3{display:grid;grid-template-columns:1fr;gap:12px}
.pk{border:1px solid var(--ink);background:var(--card);padding:18px 18px 16px;display:grid;gap:8px;position:relative;transition:transform .2s,box-shadow .2s}
.pk:hover{transform:translateY(-4px);box-shadow:8px 8px 0 var(--ink)}
.pk .q{font-size:15px;font-weight:900;line-height:1.5}
.pk .q::before{content:"“";color:var(--accent);font-family:'Anton',sans-serif;font-size:22px;margin-right:4px;vertical-align:-4px}
.pk .a{display:flex;align-items:center;gap:10px;padding-top:10px;border-top:1px solid var(--line);font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.7}
.pk .a b{flex:0 0 auto;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.18em;color:#fff;background:var(--ink);padding:6px 10px}
.pk.hot .a b{background:var(--accent)}
/* 月額／年額の切替 */
.tg{display:inline-flex;border:1.5px solid var(--ink);margin:0 0 22px;font-size:12.5px;font-weight:900}
.tg button{appearance:none;border:0;background:transparent;color:var(--ink);font:inherit;padding:10px 18px;cursor:pointer}
.tg button.on{background:var(--ink);color:#fff}
.tg button small{display:block;font-size:9.5px;font-weight:700;letter-spacing:.06em;opacity:.7}
.plans[data-iv="y"] .iv-m,.plans[data-iv="m"] .iv-y{display:none!important}
.pl .pr .per{display:block;font-family:var(--f);font-size:11px;font-weight:700;color:var(--sub);letter-spacing:0;margin-top:6px}
.pl .badge30{display:inline-block;background:var(--accent);color:#fff;font-size:10.5px;font-weight:900;padding:3px 8px;margin-top:8px;letter-spacing:.04em}
/* 機能ブロック */
.ft-list{display:grid;gap:18px}
.ft{border:1px solid var(--ink);background:var(--card);display:grid;grid-template-columns:1fr;overflow:hidden}
.ft .tx{padding:22px 20px 20px;display:grid;gap:10px;align-content:start}
.ft .n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.2em;color:var(--accent)}
.ft h3{font-family:var(--fh);margin:0;font-size:19px;font-weight:900;line-height:1.35}
.ft p{margin:0;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.ft .pts{list-style:none;margin:2px 0 0;padding:0;display:grid;gap:5px}
.ft .pts li{position:relative;padding-left:18px;font-size:12.5px;font-weight:700;line-height:1.6}
.ft .pts li::before{content:"";position:absolute;left:0;top:8px;width:9px;height:5px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
.ft .vi{background:#f2f3f5;padding:22px 20px;display:flex;align-items:center;justify-content:center;min-height:220px}
.ft.dark .vi{background:#101215}
/* スマホ枠（分析画面の実スクショ） */
.ph{width:236px;border:7px solid #1b1d21;border-radius:30px;background:#fff;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.35);position:relative}
.ph img{width:100%;display:block}
.ph.tall{max-height:440px}
.vi .cap{position:absolute;left:12px;bottom:12px;background:#fff;color:#111;font-size:10.5px;font-weight:900;padding:6px 10px;box-shadow:0 8px 20px rgba(0,0,0,.25)}
.ft .vi{position:relative}
/* 図解：検索順位 */
.mk-list{width:100%;max-width:300px;display:grid;gap:8px}
.mk-list .r{display:grid;grid-template-columns:44px 1fr auto;gap:10px;align-items:center;background:#fff;border:1px solid var(--line);padding:9px 10px;font-size:11.5px;font-weight:900;opacity:.6}
.mk-list .r .im{height:34px;background:#d9dde3}
.mk-list .r small{display:block;font-size:10px;font-weight:700;color:var(--sub)}
.mk-list .r .pr{font-family:'Anton',sans-serif;font-size:9.5px;letter-spacing:.14em;color:#fff;background:var(--ink);padding:3px 6px}
.mk-list .r.on{opacity:1;border-color:var(--accent);box-shadow:4px 4px 0 var(--accent)}
.mk-list .r.on .im{background:linear-gradient(135deg,#f0a1ab,#E43B4D)}
.mk-list .r.on .pr{background:var(--accent)}
.mk-list .lb{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.2em;color:var(--sub);margin-bottom:-2px}
/* 図解：写真 */
.mk-ph{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;width:100%;max-width:300px}
.mk-ph span{aspect-ratio:1;background:#d9dde3;display:flex;align-items:flex-end;justify-content:flex-end;padding:4px 6px;font-family:'Anton',sans-serif;font-size:11px;color:#fff;letter-spacing:.06em}
.mk-ph span:first-child{grid-column:1/3;grid-row:1/3;background:linear-gradient(135deg,#f0a1ab,#E43B4D)}
.mk-ph span.x{background:#fff;border:1px dashed #c8cdd4;color:#c8cdd4}
/* 図解：アンケート */
.mk-sv{width:100%;max-width:300px;background:#fff;border:1px solid var(--line);padding:14px 14px 12px;display:grid;gap:8px;font-size:11px;font-weight:900}
.mk-sv .h{display:flex;justify-content:space-between;align-items:center;font-size:12px}
.mk-sv .h small{font-weight:700;color:var(--sub);font-size:10px}
.mk-sv .b{display:grid;grid-template-columns:78px 1fr 28px;gap:8px;align-items:center}
.mk-sv .b i{display:block;height:8px;background:#e5e8ec;position:relative}
.mk-sv .b i::after{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--w);background:var(--ink)}
.mk-sv .b:nth-child(2) i::after{background:var(--accent)}
.mk-sv .b em{font-style:normal;text-align:right;color:var(--sub);font-weight:700}
.mk-sv .qr{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;margin-top:4px;padding-top:10px;border-top:1px solid var(--line);font-size:10.5px;font-weight:700;color:var(--sub);line-height:1.5}
.mk-sv .qr i{width:36px;height:36px;background:repeating-conic-gradient(var(--ink) 0 25%,#fff 0 50%) 0 0/8px 8px;border:2px solid var(--ink)}
/* プロの箇条 */
.pro-extra{display:grid;grid-template-columns:1fr;gap:10px;margin-top:18px}
.pro-extra div{border:1px solid var(--ink);padding:14px 16px;font-size:13px;font-weight:900;line-height:1.6;display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:start}
.pro-extra div i{font-style:normal;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.16em;color:var(--accent);padding-top:3px}
.pro-extra div small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px}
/* 比較表（フル） */
.cmp.full td.sm{font-size:11.5px;color:var(--sub)}
.cmp.full tr.sec td{background:#f2f3f5;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em;color:var(--sub);text-align:left;padding:8px}
.cmp.full td .lp-go{display:block;font-size:12px;padding:9px 6px;border:1.5px solid var(--ink);color:var(--ink);font-family:var(--fh);font-weight:900}
.cmp.full td.hot .lp-go{background:var(--accent);border-color:var(--accent);color:#fff}
.cmp.full td a.tr{display:block;font-size:10.5px;margin-top:6px}
/* 比較表：スマホは1列目を広く、ボタン行はカード側に任せる */
@media(max-width:899px){.cmp.full{font-size:11.5px}.cmp.full td:first-child{width:40%;padding-left:0}.cmp.full th,.cmp.full td{padding:9px 4px}.cmp.full tr.cmp-btn{display:none}}
/* 支払い・変更 */
.bl-grid{display:grid;grid-template-columns:1fr;gap:12px}
.bl{border:1px solid var(--ink);background:var(--card);padding:18px 18px 16px;display:grid;gap:6px;align-content:start}
.bl .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--accent)}
.bl h3{font-family:var(--fh);margin:0;font-size:15.5px;font-weight:900;line-height:1.45}
.bl p{margin:0;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
/* FAQ */
.plfaq{display:grid;gap:10px}
.plfaq details{border:1px solid var(--ink);background:var(--card)}
.plfaq summary{list-style:none;cursor:pointer;padding:14px 16px;font-size:14px;font-weight:900;display:flex;justify-content:space-between;align-items:center;gap:12px;line-height:1.5;text-align:left}
.plfaq summary::-webkit-details-marker{display:none}
.plfaq summary::before{content:none}
.plfaq summary::after{content:"+";font-family:'Anton',sans-serif;font-size:18px;color:var(--accent);flex:0 0 auto}
.plfaq details[open] summary::after{content:"–"}
.plfaq .a{padding:0 16px 16px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
@media(min-width:900px){
  .pl-hero .in{grid-template-columns:1.1fr .9fr;padding:70px 20px 64px}
  .picks3{grid-template-columns:repeat(3,1fr)}
  .plans{grid-template-columns:repeat(3,1fr);gap:20px;padding-top:12px}
  .ft{grid-template-columns:1.1fr .9fr}
  .ft:nth-child(even){grid-template-columns:.9fr 1.1fr}
  .ft:nth-child(even) .tx{order:2}
  .ft .tx{padding:28px 28px 26px}
  .ft .vi{min-height:300px}
  .ft h3{font-size:22px}
  .pro-extra{grid-template-columns:repeat(3,1fr)}
  .bl-grid{grid-template-columns:repeat(3,1fr)}
}
'''
pl_body='''
<main>
<section class="pl-hero">
  <div class="in">
    <div>
      <div class="ey">FOR CLUBS ・ PLANS</div>
      <h1><span>無料で載せて、</span><span>見てほしい<em>ぶんだけ</em></span><span>足す。</span></h1>
      <p class="ld">フリー・スタンダード・プロ。3つのプランで何が変わるのかを、実際の画面つきで説明します。掲載・体験申込の受付・保護者とのやりとりは、どのプランでも無料のままです。</p>
      <div class="cta"><a class="b1" data-plan-go="pr" href="register.html?plan=pr">スタンダードを30日無料で試す</a><a class="b2" href="#cmp">比較表を見る</a></div>
      <div class="stats"><div><b data-cnt="0">0</b><small>YEN / START</small></div><div><b data-cnt="30">0</b><small>DAYS FREE</small></div><div><b data-cnt="0">0</b><small>YEN / CANCEL</small></div></div>
    </div>
    <div class="ladder"><span class="arrow"></span>
      <div class="st"><span class="k">FREE</span><span class="t">まず載せる<small>検索・地図・新着に掲載。体験申込も届く</small></span><span class="p">¥0</span></div>
      <div class="st hot"><span class="k">STANDARD</span><span class="t">見つけてもらいやすく<small>検索で上位・写真7枚・閲覧数がわかる</small></span><span class="p">¥3,000<small>/月</small></span></div>
      <div class="st"><span class="k">PRO</span><span class="t">広報の効果まで見る<small>QR・SNS連携で「どこから来たか」がわかる</small></span><span class="p">¥10,000<small>/月</small></span></div>
    </div>
  </div>
</section>
<div class="wrap">

  <section class="sec2" id="which">
    <div class="ey rv">WHICH ONE</div>
    <h2 class="rv d1">いまの状況から、<em>選ぶ</em>。</h2>
    <p class="sub rv d2">迷ったらスタンダードから。月額は初回30日が無料で、合わなければ期間内の解約で請求はありません。</p>
    <div class="picks3">
      <div class="pk rv"><div class="q">まず載せてみたい。</div><div class="a"><b>FREE</b>写真1枚と紹介文で、検索・地図・新着に載ります。体験申込もそのまま届きます。</div></div>
      <div class="pk hot rv d1"><div class="q">募集の時期に、もっと見てもらいたい。</div><div class="a"><b>STANDARD</b>検索で上に出て、写真が7枚に。何回見られたか・申込が何件かが1つの画面で分かります。</div></div>
      <div class="pk rv d2"><div class="q">チラシ・SNS・チビスポ、どれが効いているか知りたい。</div><div class="a"><b>PRO</b>QRとSNS連携で、申込がどこから来たかまで分かります。次に力を入れる場所が決まります。</div></div>
    </div>
  </section>

  <section class="sec2" id="plans">
    <div class="ey rv">PLANS</div>
    <h2 class="rv d1">3つのプランと、<em>料金</em>。</h2>
    <p class="sub rv d2">有料プランは無料掲載への追加です。表示の金額がそのままお支払い額で、追加の税や手数料はかかりません。</p>
    <div class="tg rv" id="pl-tg"><button class="on" data-iv="m">月額<small>MONTHLY</small></button><button data-iv="y">年額<small>2ヶ月分お得</small></button></div>
    <div class="plans" id="pl-plans" data-iv="m">
      <div class="pl rv"><div class="n">FREE</div><h3>フリー</h3><div class="pr">¥0<small>/月</small><span class="per">ずっと無料</span></div><div class="for">まずは載せてみたいクラブに。</div>
        <ul><li>クラブページ・検索・地図に掲載</li><li>写真1枚・コース・体験申込</li><li>保護者とメッセージ</li><li>クラブ運営アプリ（通知・返信）</li><li>スタッフ登録・情報更新は無制限</li></ul>
        <a class="lp-go" data-plan-go href="register.html">無料で申し込む</a></div>
      <div class="pl hot rv d1"><span class="lp-pin">人気 NO.1</span><div class="n">STANDARD</div><h3>スタンダード</h3>
        <div class="pr iv-m">¥3,000<small>/月</small><span class="per">初回30日は¥0。31日目から</span></div>
        <div class="pr iv-y">¥30,000<small>/年</small><span class="per">月あたり¥2,500。月額より¥6,000お得</span></div>
        <div class="for">募集シーズンに、見つけてもらいやすく。</div>
        <ul><li>フリーのすべて</li><li>写真を7枚まで</li><li>検索結果で上位に表示</li><li>「おすすめ」枠に掲載</li><li>閲覧数・申込・入会が1画面でわかる</li><li>保護者アンケート（QR配布・自動集計）</li><li>AIの「今週の一手」</li></ul>
        <a class="lp-go iv-m" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="lp-go iv-y" data-plan-go="pr-y" href="register.html?plan=pr-y">年額で申し込む</a>
        <div class="tr iv-m"><a data-plan-go="pr-y" href="register.html?plan=pr-y">年額 ¥30,000 で申し込む ›</a></div><div class="tr iv-y"><a data-plan-go="pr" href="register.html?plan=pr">月額（初回30日無料）で申し込む ›</a></div></div>
      <div class="pl rv d2"><div class="n">PRO</div><h3>プロ</h3>
        <div class="pr iv-m">¥10,000<small>/月</small><span class="per">初月から。無料期間はありません</span></div>
        <div class="pr iv-y">¥100,000<small>/年</small><span class="per">月あたり¥8,333。月額より¥20,000お得</span></div>
        <div class="for">広報の効果まで見たいクラブに。</div>
        <ul><li>スタンダードのすべて</li><li>写真を15枚まで</li><li>検索結果でスタンダードよりさらに上</li><li>QR・計測リンクで「どこから来たか」</li><li>SNS連携（Instagram・Threads・YouTube）と投稿の分析</li><li>認知から入会までのファネル</li><li>公式SNSで月1回紹介</li></ul>
        <a class="lp-go iv-m" data-plan-go="pr-plus" href="register.html?plan=pr-plus">プロで申し込む</a><a class="lp-go iv-y" data-plan-go="pr-plus-y" href="register.html?plan=pr-plus-y">年額で申し込む</a>
        <div class="tr iv-m" style="color:var(--sub)"><a data-plan-go="pr-plus-y" href="register.html?plan=pr-plus-y" style="color:inherit">年額 ¥100,000 で申し込む ›</a></div><div class="tr iv-y" style="color:var(--sub)"><a data-plan-go="pr-plus" href="register.html?plan=pr-plus" style="color:inherit">月額 ¥10,000 で申し込む ›</a></div></div>
    </div>
    <div class="pl-note">プランを使わなくても、検索・地図・新着・診断・アプリ通知への掲載は変わりません。有料プランのカードには小さく「PR」と表示されます。</div>
  </section>

  <section class="sec2" id="standard">
    <div class="ey rv">STANDARD ・ ¥3,000 / MONTH</div>
    <h2 class="rv d1">見つけてもらいやすくする、<em>5つ</em>。</h2>
    <p class="sub rv d2">募集の時期に「載っているのに見られない」を減らすためのプランです。設定はいりません。お支払いが確認できた時点で、すべて自動で切り替わります。</p>
    <div class="ft-list">
      <div class="ft rv"><div class="tx"><div class="n">01</div><h3>検索で、上に出ます。</h3><p>保護者が地域や種目で検索したとき、同じ条件のフリーのクラブより先に表示されます。市区町村ごとのクラブ一覧ページも同じ順番です。同じプラン同士は、いつもどおり新着順・距離順です。</p></div>
        <div class="vi"><div class="mk-list"><div class="lb">SEARCH ・ 世田谷区 × サッカー</div>
          <div class="r on"><span class="im"></span><span>あなたのクラブ<small>スタンダード</small></span><span class="pr">PR</span></div>
          <div class="r"><span class="im"></span><span>◯◯FC<small>フリー・新着</small></span><span></span></div>
          <div class="r"><span class="im"></span><span>△△スポーツ少年団<small>フリー</small></span><span></span></div>
          <div class="r"><span class="im"></span><span>□□サッカースクール<small>フリー</small></span><span></span></div></div></div></div>
      <div class="ft rv"><div class="tx"><div class="n">02</div><h3>「おすすめ」枠に載ります。</h3><p>検索ページの上部にある「おすすめ」枠と、トップページの「編集部おすすめ」に優先して入ります。条件で絞る前の、いちばん目に入る場所です。</p><ul class="pts"><li>検索ページ「おすすめ」（PICK UP）</li><li>トップページ「編集部おすすめ」</li><li>掲載後、編集部が見出しとひとことを書き足すことがあります</li></ul></div>
        <div class="vi"><div class="mk-list"><div class="lb">PICK UP ・ おすすめ</div>
          <div class="r on"><span class="im"></span><span>あなたのクラブ<small>世田谷区・サッカー</small></span><span class="pr">PR</span></div>
          <div class="r on" style="opacity:.85"><span class="im"></span><span>◯◯バスケ教室<small>杉並区・バスケ</small></span><span class="pr">PR</span></div></div></div></div>
      <div class="ft rv"><div class="tx"><div class="n">03</div><h3>写真が7枚まで。1枚目がカバーです。</h3><p>練習の様子・コーチ・保護者が見守る場所・持ち物。雰囲気が伝わる順に並べられます。表示位置の調整・並べ替え・削除は、クラブのマイページからいつでも。</p></div>
        <div class="vi"><div class="mk-ph"><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span class="x">8</span></div></div></div>
      <div class="ft rv dark"><div class="tx"><div class="n">04</div><h3>何回見られて、何件申し込まれたかが、1画面で。</h3><p>クラブページの閲覧数（直近30日）、体験申込、入会、会員数をひとつの画面で。電話や紙の申込も「＋記録」から10秒で足せます。目標までの逆算と、6ヶ月の推移も一緒に見えます。</p><ul class="pts"><li>AIが「今週の一手」を1つ提案（1日3回まで）</li><li>やった施策（チラシ・ポスター）を推移の上に記録</li><li>スマホで開けます</li></ul></div>
        <div class="vi"><div class="ph tall"><img src="assets/plans/dash-now.webp" alt="クラブ分析「いま」タブ" loading="lazy"></div><div class="cap">クラブ分析（サンプル表示）</div></div></div>
      <div class="ft rv"><div class="tx"><div class="n">05</div><h3>保護者アンケートが、配るだけで集計されます。</h3><p>QRを印刷して配るだけ。どこでクラブを知ったか、満足度、友人にすすめたい度（NPS）が自動で集計されます。他のクラブの平均と比べられて、結果からAIがアドバイスを出します。</p></div>
        <div class="vi"><div class="mk-sv"><div class="h">どこでクラブを知ったか<small>回答 15件</small></div>
          <div class="b"><span>知人の紹介</span><i style="--w:72%"></i><em>5</em></div><div class="b"><span>チビスポ</span><i style="--w:56%"></i><em>4</em></div><div class="b"><span>ポスター</span><i style="--w:42%"></i><em>3</em></div><div class="b"><span>Instagram</span><i style="--w:28%"></i><em>2</em></div>
          <div class="qr"><i></i><span>配布用QR。読み取った保護者のスマホで、その場で回答できます</span></div></div></div></div>
    </div>
  </section>

  <section class="sec2" id="pro">
    <div class="ey rv">PRO ・ ¥10,000 / MONTH</div>
    <h2 class="rv d1">広報の<em>効果</em>まで、見る。</h2>
    <p class="sub rv d2">スタンダードの全部に加えて、ポスター・チラシ・SNSからの流入を横並びにします。「どこから申込が来たか」が分かると、次にどこへ力を入れるかが決まります。</p>
    <div class="ft-list">
      <div class="ft rv dark"><div class="tx"><div class="n">01</div><h3>QR・計測リンクで、「どこから来たか」を数えます。</h3><p>駅前のポスター、体験会のチラシ、紹介カード。配る場所ごとにQRを発行すると、読み取られた数と、そこからの体験申込が並びます。効いている場所を増やし、効いていない場所をやめられます。</p><ul class="pts"><li>QRは分析画面から何枚でも発行</li><li>チビスポのページに来た経路（SNS・検索・直接）も自動で</li></ul></div>
        <div class="vi"><div class="ph tall"><img src="assets/plans/dash-sources.webp" alt="どこから来ているか" loading="lazy"></div><div class="cap">集客タブ「どこから来ているか」</div></div></div>
      <div class="ft rv dark"><div class="tx"><div class="n">02</div><h3>SNSをつなぐと、投稿の反応が毎朝たまります。</h3><p>Instagram・Threads・YouTubeを連携すると、投稿と反応（♥・コメント・表示回数）を毎朝6時に自動で取り込みます。どのタイプの投稿が反応されているか、当たり投稿の共通点、投稿が続いているかが見えます。</p><ul class="pts"><li>投稿のタイプ分け（試合・コーチ・練習・募集）はAIが自動</li><li>週ごとの本数で「続いているか」を確認</li></ul></div>
        <div class="vi"><div class="ph tall"><img src="assets/plans/dash-post.webp" alt="投稿タブ" loading="lazy"></div><div class="cap">投稿タブ（サンプル表示）</div></div></div>
      <div class="ft rv dark"><div class="tx"><div class="n">03</div><h3>認知から入会まで、どの段階で減っているか。</h3><p>SNSで表示された回数 → ページに来た人 → 体験申込 → 体験参加 → 入会。5段階の数字と、子ども向けスポーツクラブの目安の率を並べて、いちばん弱い段階と直し方を示します。</p></div>
        <div class="vi"><div class="ph tall"><img src="assets/plans/dash-funnel.webp" alt="ファネル" loading="lazy"></div><div class="cap">集客タブ「ファネル」</div></div></div>
    </div>
    <div class="pro-extra rv">
      <div><i>04</i><span>写真が15枚まで<small>スタンダードの7枚から、さらに8枚</small></span></div>
      <div><i>05</i><span>順位はスタンダードより上<small>検索結果・おすすめ枠、すべてで最上位のグループ</small></span></div>
      <div><i>06</i><span>公式SNSで月1回紹介<small>チビスポのInstagram・Threadsで、クラブを紹介します</small></span></div>
    </div>
  </section>

  <section class="sec2" id="cmp">
    <div class="ey rv">COMPARE</div>
    <h2 class="rv d1">全部を、<em>一覧</em>で。</h2>
    <table class="cmp full rv">
      <tr><th>&nbsp;</th><th>FREE</th><th class="hot">STANDARD</th><th>PRO</th></tr>
      <tr class="sec"><td colspan="4">クラブページ</td></tr>
      <tr><td>掲載（検索・地図・新着・診断・アプリ通知）</td><td>✓</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>体験申込の受付・保護者とメッセージ</td><td>✓</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>写真の枚数</td><td><b>1</b></td><td class="hot"><b>7</b></td><td><b>15</b></td></tr>
      <tr><td>検索結果での順位</td><td class="sm">標準</td><td class="hot">上位</td><td>最上位</td></tr>
      <tr><td>「おすすめ」枠（検索ページ・トップ）</td><td class="no">—</td><td class="hot">✓</td><td>✓</td></tr>
      <tr class="sec"><td colspan="4">クラブ分析</td></tr>
      <tr><td>閲覧数（直近30日）・申込・入会・会員数</td><td class="no">—</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>目標までの逆算・6ヶ月の推移</td><td class="no">—</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>AIの「今週の一手」（1日3回）</td><td class="no">—</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>保護者アンケート（QR配布・自動集計）</td><td class="no">—</td><td class="hot">✓</td><td>✓</td></tr>
      <tr><td>QR・計測リンク（ポスター・チラシ・紹介カード）</td><td class="no">—</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>SNS連携と投稿の分析</td><td class="no">—</td><td class="hot no">—</td><td>✓</td></tr>
      <tr><td>ファネル（認知から入会まで）</td><td class="no">—</td><td class="hot sm">流入から</td><td>認知から</td></tr>
      <tr><td>公式SNSで月1回紹介</td><td class="no">—</td><td class="hot no">—</td><td>✓</td></tr>
      <tr class="sec"><td colspan="4">料金</td></tr>
      <tr><td>月額</td><td><b>¥0</b></td><td class="hot"><b>¥3,000</b></td><td><b>¥10,000</b></td></tr>
      <tr><td>年額（2ヶ月分お得）</td><td class="no">—</td><td class="hot"><b>¥30,000</b></td><td><b>¥100,000</b></td></tr>
      <tr><td>初回30日無料</td><td class="no">—</td><td class="hot">月額のみ</td><td class="no">—</td></tr>
      <tr class="cmp-btn"><td>&nbsp;</td><td><a class="lp-go" data-plan-go href="register.html">無料で申し込む</a></td><td class="hot"><a class="lp-go" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="tr" data-plan-go="pr-y" href="register.html?plan=pr-y">年額で申し込む ›</a></td><td><a class="lp-go" data-plan-go="pr-plus" href="register.html?plan=pr-plus">プロで申し込む</a><a class="tr" data-plan-go="pr-plus-y" href="register.html?plan=pr-plus-y" style="color:var(--sub)">年額で申し込む ›</a></td></tr>
    </table>
  </section>

  <section class="sec2" id="billing">
    <div class="ey rv">BILLING</div>
    <h2 class="rv d1">支払いと変更は、<em>いつでも</em>。</h2>
    <div class="bl-grid">
      <div class="bl rv"><div class="k">PAYMENT</div><h3>クレジットカードで、自動で続きます。</h3><p>お支払いはクレジットカード（Stripe）です。月額は毎月、年額は毎年、申し込んだ日と同じ日に自動で決済されます。カード明細には「CHIBISPO」と載ります。</p></div>
      <div class="bl rv d1"><div class="k">30 DAYS FREE</div><h3>スタンダード月額は、初回30日が¥0です。</h3><p>申込時にカードの登録は必要ですが、30日以内に解約すれば請求はありません。31日目から¥3,000です。年額とプロには無料期間はありません。</p></div>
      <div class="bl rv d2"><div class="k">CHANGE</div><h3>プランの変更は、日割りで切り替わります。</h3><p>スタンダードからプロへ、月額から年額へ。クラブのマイページの「プランの変更・解約」（カスタマーポータル）から、差額は日割りで自動計算されます。</p></div>
      <div class="bl rv"><div class="k">CANCEL</div><h3>解約は、いつでも。違約金はありません。</h3><p>同じカスタマーポータルから解約できます。解約後もその請求期間の終わりまで有料の機能が使え、期間が終わると自動でフリーに戻ります。掲載は消えません。</p></div>
      <div class="bl rv d1"><div class="k">AFTER</div><h3>フリーに戻ると、写真は1枚目だけになります。</h3><p>順位は標準に、写真は1枚目だけの表示に戻ります。登録した写真・記録・アンケートの回答は残るので、また有料にすれば続きから見られます。</p></div>
      <div class="bl rv d2"><div class="k">RECEIPT</div><h3>領収書は、その場で発行できます。</h3><p>カスタマーポータルから、決済ごとの領収書をいつでもダウンロードできます。請求書払いや団体でのお申し込みは、<a href="contact.html?who=club" style="color:var(--accent);text-decoration:underline">お問い合わせ</a>から相談してください。</p></div>
    </div>
  </section>

  <section class="sec2" id="faq">
    <div class="ey rv">FAQ</div>
    <h2 class="rv d1">プランについて、<em>よく聞かれること</em>。</h2>
    <div class="plfaq rv">
      <details><summary>スタンダードとプロ、どちらから始めればいいですか。</summary><div class="a">募集の時期に見てもらいたいだけなら、スタンダードで足ります。ポスターやSNSに手をかけていて「どれが効いているか」を知りたいなら、プロです。プロには無料期間がないので、まずスタンダードの30日で分析画面に慣れてから、カスタマーポータルでプロに切り替えるのもおすすめです。</div></details>
      <details><summary>「上位表示」は、どういう並び順ですか。</summary><div class="a">同じ検索条件の中で、プロ → スタンダード → フリーの順に並びます。同じプランの中は、これまでどおり新着順・距離順です。検索結果・市区町村ページ・おすすめ枠、すべて同じルールです。</div></details>
      <details><summary>有料にすると、保護者からの見え方は変わりますか。</summary><div class="a">順番が上がり、写真が増え、おすすめ枠に入ります。クラブのカードには小さく「PR」と表示されます。それ以外の見た目や、体験申込の流れは変わりません。</div></details>
      <details><summary>お支払いが終わったあと、何かする必要はありますか。</summary><div class="a">ありません。お支払いが確認できた時点で、順位・写真の枚数・分析画面が自動で切り替わります。写真を増やすときだけ、クラブのマイページから追加してください。</div></details>
      <details><summary>複数のクラブや教室を運営しています。</summary><div class="a">プランはクラブページ1つごとです。2つのクラブページを上位にしたい場合は、それぞれで申し込みます。まとめての申し込みは<a href="contact.html?who=club" style="color:var(--accent);text-decoration:underline">お問い合わせ</a>から相談してください。</div></details>
      <details><summary>プロのSNS連携には、何が必要ですか。</summary><div class="a">クラブのInstagram・Threads・YouTubeのアカウントでログインして「連携する」を押すだけです。パスワードをこちらに渡す必要はありません。連携をやめるのも、分析画面の設定からいつでもできます。</div></details>
      <details><summary>解約したら、分析のデータは消えますか。</summary><div class="a">消えません。記録した申込・入会・施策、アンケートの回答は残ります。もう一度有料にすると、続きから見られます。</div></details>
    </div>
  </section>

  <div class="svcta"><div class="big">PLANS</div><div class="in"><div class="ey">START FREE</div><h2>まず無料で載せて、<br>必要になったら足してください。</h2><p>スタンダードは初回30日が¥0。合わなければ、期間内の解約で請求はありません。</p><div class="row"><a class="b1" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a><a class="b2" href="register.html">無料で掲載する</a></div></div></div>
  <div class="svnav"><span class="cur">料金プラン</span><a href="service-listing-preview.html">01 クラブを載せる</a><a href="service-sns-preview.html">03 SNS運用サポート</a><a href="hp-samples/">04 ホームページ制作</a><a href="service-ads-preview.html">05 地域の広告掲載</a><a href="faq.html">よくある質問</a></div>
  <div style="height:40px"></div>
</div>
<div class="sbar" id="sbar"><div class="t">スタンダード ¥3,000/月<small>初回30日無料・いつでも解約OK</small></div><a class="lp-go" data-plan-go="pr" href="register.html?plan=pr">30日無料で試す</a></div>
</main>
'''
pl_js='''<script>
(function(){
 if(/noanim=1/.test(location.search)){var st=document.createElement('style');st.textContent='*{transition:none!important;animation:none!important}.pl-hero h1 span,.ladder .st,.ladder .arrow{opacity:1!important;transform:none!important}';document.head.appendChild(st);document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});document.querySelectorAll('[data-cnt]').forEach(function(b){b.textContent=b.dataset.cnt});return}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
 document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
 document.querySelectorAll('[data-cnt]').forEach(function(b){var to=+b.dataset.cnt,t0=null;function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/900);b.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)}setTimeout(function(){requestAnimationFrame(f)},400)});
 /* 月額／年額 */
 var tg=document.getElementById('pl-tg'),pl=document.getElementById('pl-plans');
 if(tg&&pl)tg.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;pl.dataset.iv=b.dataset.iv;tg.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)})});
 /* ログイン中のクラブ運営者が有料プランを押したら、新規登録ではなくマイページのプラン選択へ（二重登録を防ぐ） */
 if(window.ChibiAuth&&ChibiAuth.ready&&ChibiAuth.ready()){ ChibiAuth.getProfile().then(function(p){ if(!p||p.role!=='club') return;
   document.querySelectorAll('[data-plan-go]').forEach(function(a){ a.href='club-mypage.html#mp-upsell'; }); }).catch(function(){}); }
 var sb=document.getElementById('sbar'),hero=document.querySelector('.pl-hero');
 if(sb&&hero)new IntersectionObserver(function(e){sb.classList.toggle('on',!e[0].isIntersecting&&e[0].boundingClientRect.top<0)},{threshold:0}).observe(hero);
})();
</script>'''
page('service-plans-preview.html','料金プラン｜フリー・スタンダード・プロで何が変わるか｜チビスポ（プレビュー）',pl_body,pl_css,extra_js=pl_js)
