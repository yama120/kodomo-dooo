# ---- 記事 v2（build_pages.py から exec。art_css / page を使う）
art_css2=art_css+open(P+'art_v2.css',encoding='utf-8').read()
art_body2='''
<div id="rprog"></div>
<main><div class="wrap">
  <div class="pgh"><div class="bc"><a href="#">ホーム</a> › <a href="magazine-preview.html">マガジン</a> › 子どもの一歩</div></div>
  <div class="note">【記事 v2】マガジン一覧・検索結果と同じ道具立て：カテゴリは<b>赤線＋英字ラベル（FIRST STEP）</b>、見出しは大きく、署名行は上罫で区切る。本文の小見出しは<b>Anton番号01〜05</b>（右の目次と同じ番号）。引用は箱をやめて<b>引き出し型</b>（大きな引用符＋短い赤線）。検索へのCTAは上下罫の帯。右カラムの目次は<b>番号付き・読んでいる節を赤で追従</b>。関連記事は右カラムでは1列。本文の下に<b>「次に読む」</b>を全幅で1本。画面上端に<b>読了の進み具合</b>（3pxの赤線）。★v1は <a href="article-preview-v1.html">article-preview-v1.html</a>。本文は720px・15px・行間2.1のまま。</div>
  <div class="ahead">
    <div class="ey">FIRST STEP<small>子どもの一歩</small></div>
    <h1>6歳までの運動が、脳を育てる。幼児期に大切にしたい「多様な動き」</h1>
    <div class="by"><img src="assets/app-hero/app-icon-512.webp" alt=""><span><b>チビスポ編集部</b> ・ 2026.06.20</span><span class="rt">6 MIN READ</span></div>
  </div>
  <div class="akv"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><div class="cap">写真：Wikimedia Commons</div></div>
  <div class="alay">
    <article class="art-body">
      <p class="lead">「何歳から始めればいいですか」は、いちばん多い質問です。答えは種目によって違いますが、6歳までに大事なのは種目ではなく「動きの種類」でした。</p>
      <h2 id="s1">神経系は6歳までに約9割が発達する</h2>
      <p>スキャモンの発育曲線では、神経系の発達は5〜6歳でおおよそ8〜9割に達するとされています。走る・跳ぶ・投げる・つかまる・バランスをとる。この時期にいろいろな動きを経験した子は、あとから新しいスポーツを始めたときの覚えが早い、というのが多くの指導者の実感です。</p>
      <blockquote>「早くから1つに絞る」は、逆効果になることがあります。</blockquote>
      <h2 id="s2">「早くから1つに絞る」は逆効果になりうる</h2>
      <p>同じ動きだけを繰り返すと、使う筋肉と神経が偏ります。幼児期は「上手になる」より「いろいろやる」ほうが、結果として伸びしろが残ります。</p>
      <figure><img src="assets/preview-video/wm-outdoor.jpg" alt=""><figcaption>公園で走り回るのも、立派な「多様な動き」です。</figcaption></figure>
      <h2 id="s3">家庭でできる「多様な動き」遊び</h2>
      <p>鬼ごっこ、けんけんぱ、ボール投げ、木登り、雲梯。特別な道具は要りません。週に何回、どれくらい、より「飽きないうちにやめる」ほうが続きます。</p>
      <div class="acta"><div class="ey">FIND A CLUB</div><div class="t">「いろいろやる」ができるクラブを探す</div><p>未就学から通えて、体験OKのクラブに絞れます。</p><a class="btn" href="search-preview.html">未就学からのクラブを見る</a></div>
      <h2 id="s4">習い事として始めるなら</h2>
      <p>まずは体験に行って、練習の最初の30分を見てください。準備運動が「走る・跳ぶ・転がる」で構成されているクラブは、この時期の子に向いています。</p>
      <h2 id="s5">クラブの体験に行くなら、ここを見る</h2>
      <p>コーチが子どもの目線までしゃがんで話しているか。できなかった子にどう声をかけているか。この2つだけ見れば、雰囲気はだいたい分かります。</p>
      <div class="share"><span class="lb">SHARE</span><a href="#">X</a><a href="#">LINE</a><a href="#">リンクをコピー</a></div>
      <div class="anext"><div class="ey">NEXT</div><div class="c"><div><div class="k">子どもの一歩 ・ 2026.06.18</div><h3>年齢別・おすすめの運動と「やりすぎ注意」な運動</h3></div><img src="assets/preview-video/wm-outdoor.jpg" alt=""></div></div>
    </article>
    <aside class="aside">
      <div class="toc"><div class="t">CONTENTS</div><ol><li><a href="#s1">神経系は6歳までに約9割が発達する</a></li><li><a href="#s2">「早くから1つに絞る」は逆効果になりうる</a></li><li><a href="#s3">家庭でできる「多様な動き」遊び</a></li><li><a href="#s4">習い事として始めるなら</a></li><li><a href="#s5">体験に行くなら、ここを見る</a></li></ol></div>
      <div class="blk" style="margin-top:28px"><h2 data-en="IN THIS STORY">この記事に出てくるクラブ</h2>
        <div class="rel" style="grid-template-columns:1fr">
          <div class="c"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><div class="n">はじめの30分は、ずっと鬼ごっこ</div><div class="m">経堂キッズサッカー／未就学〜小2</div></div>
        </div></div>
      <div class="blk"><h2 data-en="RELATED">関連する記事</h2>
        <div class="arts">
          <div class="art"><div class="b"><h3>年齢別・おすすめの運動と「やりすぎ注意」な運動</h3><div class="m"><b>子どもの一歩</b>2026/06/18</div></div><img src="assets/preview-video/wm-outdoor.jpg" alt=""></div>
          <div class="art"><div class="b"><h3>運動が苦手な子でも、楽しく続く習い事の見つけ方</h3><div class="m"><b>クラブ選び</b>2026/06/15</div></div><img src="assets/preview-video/wm-karate.jpg" alt=""></div>
        </div></div>
    </aside>
  </div>
  <div style="height:40px"></div>
</div></main>
'''
art_js2='''<script>
(function(){var bar=document.getElementById('rprog'),art=document.querySelector('.art-body'),hs=[].slice.call(document.querySelectorAll('.art-body h2[id]')),lis=[].slice.call(document.querySelectorAll('.toc li'));
function upd(){if(art&&bar){var r=art.getBoundingClientRect(),h=r.height-innerHeight,p=h>0?Math.min(1,Math.max(0,-r.top/h)):1;bar.style.width=(p*100).toFixed(1)+'%'}
 var cur=-1;hs.forEach(function(x,i){if(x.getBoundingClientRect().top<120)cur=i});lis.forEach(function(l,i){l.classList.toggle('on',i===cur)})}
addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd,{passive:true});upd()})();
</script>'''
page('article-preview.html','6歳までの運動が、脳を育てる｜チビスポ マガジン（プレビュー）',art_body2,art_css2,extra_js=art_js2)
