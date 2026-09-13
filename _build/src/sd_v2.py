# ---- 3問診断 v2（build_pages.py から exec。sd_css / cards / page を使う）
sd_css2=sd_css+open(P+'sd_v2.css',encoding='utf-8').read()
res_cards2="\n".join(cards.card(**c) for c in [cards.CLUBS[0],cards.CLUBS[2],cards.CLUBS[5],cards.CLUBS[8]])
def opt(t,sub='',on=False,ck=False):
    return '<div class="opt%s">%s%s%s</div>'%(' on' if on else '',('<span class="ck"></span>' if ck else ''),t,('<small>%s</small>'%sub if sub else ''))
sd_body2='''
<main><div class="wrap">
  <div class="note">【診断 v2・5問】★<b>質問を組み直した</b>：旧版は「地域」と「子どもの年齢」を聞いていなかった（結果に世田谷区と出るのに、どこで探すかを聞いていない）。年齢は登録項目（未就学／小学生／中学生）なのにQ3のチェック1つに混ざっていた。「土日両方」は絞り込みに無い条件なので外し、登録項目どおり「平日／土日／どちらでも」に。★ユーザー「3問以上でも良い」→ <b>1画面1問の5問</b>：①地域 ②年齢 ③種目（複数OK） ④曜日 ⑤こだわり（任意）。1問ずつなので迷わない。種目は興味が複数あってよいので複数選択。★結果は「クラブ4件」の前に<b>「おすすめの種目」</b>を年齢から出す（まだ決めていない人への約束）。保存はマイページ、はじめての人は記事へ。★TOPのボタンも「5つの質問でさがす」に変更。★デザイン：PCは左に手順（追従）、右に質問。選択肢は箱の羅列ではなく<b>黒罫のマス目</b>、選ぶと黒ベタ。質問の右上に大きな中抜き数字。★v1は <a href="shindan-preview-v1.html">shindan-preview-v1.html</a>。</div>
  <div class="sdlay">
  <aside class="steps">
    <div class="k">5 QUESTIONS</div>
    <div class="s on" data-n="01">どこで<small>お住まいの地域</small></div>
    <div class="s" data-n="02">だれが<small>お子さんの年齢</small></div>
    <div class="s" data-n="03">なにを<small>気になる種目（複数OK）</small></div>
    <div class="s" data-n="04">いつ<small>通える曜日</small></div>
    <div class="s" data-n="05">こだわり<small>あれば（任意）</small></div>
    <div class="why">答えは、クラブが登録している項目だけで絞ります。当番の有無など、載っていないことは聞きません。1分で終わります。</div>
  </aside>
  <div class="sd">
    <div class="prog"><i class="on cur">01</i><i>02</i><i>03</i><i>04</i><i>05</i></div>
    <div class="q on" data-q="1">
      <div class="big">01</div>
      <div class="n">STEP 01 / 05</div><h1>どこで、探しますか。</h1><div class="ld">お住まいの地域か、いまいる場所から。</div>
      <div class="sel"><select><option>東京都</option></select><select><option>世田谷区</option></select></div>
      <a class="geo" href="#"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>現在地から探す</a>
      <div class="nav"><span></span><a class="btn next" href="#">つぎへ ›</a></div>
    </div>
    <div class="q" data-q="2">
      <div class="big">02</div>
      <div class="n">STEP 02 / 05</div><h1>お子さんは、いまいくつですか。</h1><div class="ld">クラブの対象年齢で絞ります。</div>
      <div class="opts">%s%s%s%s</div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">つぎへ ›</a></div>
    </div>
    <div class="q" data-q="3">
      <div class="big">03</div>
      <div class="n">STEP 03 / 05</div><h1>どんな種目が、気になりますか。</h1><div class="ld">いくつ選んでも大丈夫です。決めていなければ、いちばん下を。</div>
      <div class="opts" data-multi="1">%s%s%s%s%s%s%s%s</div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">つぎへ ›</a></div>
    </div>
    <div class="q" data-q="4">
      <div class="big">04</div>
      <div class="n">STEP 04 / 05</div><h1>いつ、通えますか。</h1><div class="ld">活動曜日で絞ります。</div>
      <div class="opts three">%s%s%s</div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">つぎへ ›</a></div>
    </div>
    <div class="q" data-q="5">
      <div class="big">05</div>
      <div class="n">STEP 05 / 05</div><h1>あれば、こだわりを。</h1><div class="ld">複数えらべます。なくても、そのまま結果へ。</div>
      <div class="opts" data-multi="1">%s%s%s%s</div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">結果を見る ›</a></div>
    </div>
    <div class="res">
      <div class="hd"><div class="k">RESULT</div><h1>世田谷区で、合いそうなクラブが<em style="font-style:normal;color:var(--accent)">4件</em>。</h1><p>小学1〜3年のお子さんが、土日に通えるクラブです。体験OKのところだけに絞っています。</p>
        <div class="cond"><span class="chip on">世田谷区</span><span class="chip on">小学1〜3年</span><span class="chip on">サッカー</span><span class="chip on">土日</span><span class="chip on">体験OK</span><a class="chip" href="#">条件を変える</a></div></div>
      <div class="sug"><div class="k">FOR THIS AGE</div><h2>小学1〜3年なら、こんな種目も。</h2><p>「まだ決めていない」を選んだときに出します。この年齢はいろいろな動きを経験するほど、あとで伸びます。</p>
        <div class="row">
          <div class="s"><span>体操</span><small>走る・跳ぶ・回るの土台。どの種目にもつながる</small><a href="#">世田谷区の体操を見る ›</a></div>
          <div class="s"><span>水泳</span><small>全身を使い、けがが少ない。個人で進められる</small><a href="#">世田谷区の水泳を見る ›</a></div>
          <div class="s"><span>サッカー</span><small>友だちと一緒に始めやすい。週1から</small><a href="#">世田谷区のサッカーを見る ›</a></div>
        </div></div>
      <div class="sug" style="border-top-width:1px;border-top-color:var(--line)"><div class="k">CLUBS</div><h2>合いそうなクラブ</h2></div>
      <div class="news">%s</div>
      <div class="save"><div class="k">SAVE</div><div class="t">この結果を、保存しておきますか。</div><p>マイページに保存すると、あとから見比べられます。近くに新しいクラブが載ったときにもお知らせします。</p><div class="row"><a class="btn" href="#">保存する（無料）</a><a class="btn ghost" href="search-preview.html">一覧で見る</a></div></div>
      <div class="alt"><div class="t">FOR BEGINNERS</div>
        <div class="arts">
          <div class="art"><div class="b"><h3>「うちの子に合うクラブ」の見つけ方・5つの視点</h3><div class="m"><b>クラブ選び</b>2026/06/12</div></div><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""></div>
          <div class="art"><div class="b"><h3>見学のとき、コーチに聞いておきたい5つのこと</h3><div class="m"><b>はじめて</b>2026/08/28</div></div><img src="assets/preview-video/wm-bball-jp.jpg" alt=""></div>
        </div></div>
    </div>
  </div>
  </div>
</div></main>
'''%(opt('未就学','年少〜年長'),opt('小学1〜3年','',True),opt('小学4〜6年'),opt('中学生'),
     opt('サッカー',ck=True,on=True),opt('野球',ck=True),opt('バスケットボール',ck=True),opt('ダンス',ck=True),opt('水泳',ck=True),opt('空手・剣道',ck=True),opt('体操',ck=True),opt('まだ決めていない','おすすめの種目も出します',ck=True),
     opt('平日','放課後'),opt('土日','',True),opt('どちらでも'),
     opt('女の子です','女の子歓迎のクラブ',ck=True),opt('女性の指導者がいる',ck=True),opt('入会金がない',ck=True),opt('まず体験したい','体験OKのクラブ',True,True),
     res_cards2)
sd_js2='''<script>
(function(){var qs=[].slice.call(document.querySelectorAll('.q')),res=document.querySelector('.res'),prog=[].slice.call(document.querySelectorAll('.prog i')),steps=[].slice.call(document.querySelectorAll('.steps .s')),i=0;
 function show(n){i=n;qs.forEach(function(q,k){q.classList.toggle('on',k===n)});prog.forEach(function(p,k){p.classList.toggle('on',k<=n);p.classList.toggle('cur',k===n)});steps.forEach(function(s,k){s.classList.toggle('on',k===n||(n>=qs.length))});res.classList.toggle('on',n>=qs.length);window.scrollTo({top:0,behavior:'smooth'})}
 document.querySelectorAll('.opt').forEach(function(o){o.addEventListener('click',function(){var g=o.parentElement,multi=g.dataset.multi==='1';if(!multi)g.querySelectorAll('.opt').forEach(function(x){x.classList.remove('on')});o.classList.toggle('on')})});
 document.querySelectorAll('.next').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();show(i+1)})});
 document.querySelectorAll('.back').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();show(Math.max(0,i-1))})});
})();
</script>'''
page('shindan-preview-v2.html','5つの質問でさがす｜チビスポ（プレビュー v2・ページ版）',sd_body2,sd_css2,extra_js=sd_js2)
