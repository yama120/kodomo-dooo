# ---- 診断 v3：ポップアップ版の入口ページ（直リンク用。開くと自動でポップアップ）
sd3_css='''
.qin{max-width:720px;margin:0 auto;padding:40px 0 60px}
.qin .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:12px}
.qin .ey::before{content:"";width:22px;height:2px;background:var(--accent)}
.qin h1{font-family:var(--fh);margin:0 0 10px;font-size:clamp(26px,6.4vw,42px);font-weight:900;line-height:1.25;letter-spacing:-.01em}
.qin h1 em{font-style:normal;color:var(--accent)}
.qin p{margin:0 0 20px;font-size:13.5px;font-weight:700;color:var(--sub);line-height:1.9}
.qin .meta{display:flex;gap:18px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--sub);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 0;margin-bottom:22px}
.qin .meta b{font-size:18px;font-weight:400;color:var(--ink);margin-right:6px;letter-spacing:.04em}
.qin .go{display:inline-block;background:var(--ink);color:var(--bg);font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 34px;letter-spacing:.06em}
body[data-skin="stadium"] .qin .go{color:#0b0c0f}
.qin .qs{margin-top:34px;border-top:2px solid var(--ink);padding-top:6px}
.qin .qs div{display:flex;gap:12px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--line);font-size:13px;font-weight:900}
.qin .qs div::before{content:attr(data-n);font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.06em;color:var(--accent)}
.qin .qs div small{margin-left:auto;font-weight:700;color:var(--sub);font-size:11.5px}
'''
sd3_body='''
<main><div class="wrap">
  <div class="note">【診断 v3＝ポップアップ】ユーザー「別ページより、MOYORIのキャリア診断のようにポップアップで。その方が自然に答えてくれる」→ 診断は<b>どのページからでも開けるポップアップ</b>（`preview-quiz.js`）。TOPのヒーロー「質問に答えてさがす」で開く。このページは直リンク用の入口で、開くと自動で始まる。★<b>質問を「種目」から「好み」に変えた</b>：種目が決まっている人は診断しない。①どこで ②年齢 ③友だちと／ひとりで ④外／室内／水 ⑤好きなこと（ボール・走る跳ぶ・音楽・礼儀・珍しいこと） ⑥雰囲気（楽しむ／本格＝登録の雰囲気タグ） ⑦曜日 ⑧こだわり。<b>4タイプ</b>（王道／個人／アウトドア／マイナー＝本番のカテゴリページと同じ分類）に落とし、種目3つ＋近くのクラブ2件。<b>保存→マイページ</b>で、条件に合う新着・体験募集のお知らせを受け取る。★v1（3問ページ）・v2（5問ページ）も残してある。</div>
  <div class="qin">
    <div class="ey">FIND YOUR SPORT</div>
    <h1>どんなスポーツが<em>合いそう</em>か、<br>1分でわかります。</h1>
    <p>種目が決まっていなくても大丈夫。好きな遊び方や雰囲気から、合いそうな種目のタイプと、近くのクラブをお出しします。答えは、クラブが登録している項目だけで絞ります。</p>
    <div class="meta"><span><b>8</b>QUESTIONS</span><span><b>1</b>MIN</span><span><b>4</b>TYPES</span></div>
    <a class="go" href="#" data-quiz>診断をはじめる ›</a>
    <div class="qs">
      <div data-n="01">どこで<small>地域・現在地</small></div><div data-n="02">お子さんの年齢<small>対象年齢</small></div><div data-n="03">友だちと？ ひとりで？<small>チーム／個人</small></div><div data-n="04">外？ 室内？ 水の中？<small>種目の分類</small></div>
      <div data-n="05">好きなこと<small>ボール・走る跳ぶ・音楽・礼儀・珍しいこと</small></div><div data-n="06">合いそうな空気<small>雰囲気タグ</small></div><div data-n="07">通える曜日<small>活動曜日</small></div><div data-n="08">あれば、こだわり<small>任意</small></div>
    </div>
  </div>
</div></main>
'''
page('shindan-preview.html','どんなスポーツが合いそうか、1分でわかる｜チビスポ（プレビュー）',sd3_body,sd3_css,bodyattr='data-skin="bright" data-quiz-auto="1"')
