# ---- マガジン一覧 v2（build_pages.py から exec。mag_css / ARTS / chip / page を使う）
mag_css2=mag_css+open(P+'mag_v2.css',encoding='utf-8').read()
CAT_EN={'クラブ選び':'CHOOSING','子どもの一歩':'FIRST STEP','コーチの想い':'COACH','はじめて':'BEGINNERS'}
mi2="".join('<div class="mi"><img src="assets/preview-video/%s.jpg" alt=""><div class="c">%s</div><h3>%s</h3><div class="d"><b>%s</b>%s</div></div>'%(im,CAT_EN.get(c,c),t,c,d) for c,t,d,im in ARTS[1:])
mag_body2='''
<main>
<section class="sec mhead">
  <div class="wrap">
    <div class="note">【マガジン一覧 v2】<b>中抜きの巨大「MAGAZINE」は残す</b>（ユーザー判断・2026-09-08）。その下に見出し＋Anton数字（検索結果と同じ型）。★見出しは「クラブ選び」ではなく<b>運動をすすめる内容</b>（運動の効果の記事も含むため）。背景の英字は入れない（クラブ詳細で「見にくい」と判断されたため）。特集1本は全幅のまま、右上に番号01。以下の記事に<b>通し番号02〜</b>と罫線、カテゴリは英字ラベルで、日本語のカテゴリ名は日付の横に。★v1は <a href="magazine-preview-v1.html">magazine-preview-v1.html</a>。</div>
    <div class="big">MAGAZINE</div>
    <div class="s-h1">
      <h1>体を動かすと、<em>いいこと</em>がある。</h1>
      <div class="s-cnt"><span><b>7</b><small>ARTICLES</small></span><span class="sep"></span><span><b>4</b><small>TOPICS</small></span></div>
    </div>
    <div class="ld">運動が子どもに何をもたらすか、から、クラブの選び方まで。読むと動きたくなる話を集めました。</div>
    <div class="cats">%s%s%s%s%s</div>
  </div>
</section>
<div class="wrap">
  <div class="feat"><div class="no">01</div><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""><div class="t"><div class="c">FEATURE ・ CHOOSING</div><h2>「うちの子に合うクラブ」の見つけ方・5つの視点</h2><p>強いか弱いかより先に見るところがあります。見学の前に、5つだけ。</p></div></div>
  <div class="mh2"><div><div class="ey">LATEST</div><h2>新しい<em>記事</em></h2></div><span class="more">週1本、金曜に更新</span></div>
  <div class="mgrid mag">%s</div>
  <div class="pager"><a class="on" href="#">01</a><a href="#">02</a><a href="#">NEXT ›</a></div>
  <div style="height:40px"></div>
</div>
</main>
'''%(chip('すべて',True),chip('クラブ選び'),chip('コーチの想い'),chip('子どもの一歩'),chip('はじめて'),mi2)
page('magazine-preview.html','マガジン｜チビスポ（プレビュー）',mag_body2,mag_css2)
