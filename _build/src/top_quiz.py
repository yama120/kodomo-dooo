# TOP に「3問診断」のセクションを足す（スポーツジャンルの直後）。ヘッダーからは外したぶん、ここで見せる
import os
D=os.path.expanduser('~/kodomo-dooo-deploy/'); f=D+'video-hero-preview.html'
top=open(f,encoding='utf-8').read()
CSS='''/* ===================== QUIZ BAND ===================== */
.qz-g{display:grid;gap:10px;margin-top:6px}
.qz-q{border:1.5px solid var(--ink);background:var(--card);padding:16px 18px 18px}
.qz-n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.18em;color:var(--accent)}
.qz-t{font-family:var(--fh);font-weight:900;font-size:16px;line-height:1.5;margin:4px 0 10px}
.qz-o{display:flex;flex-wrap:wrap;gap:6px}
.qz-o span{border:1px solid var(--line);padding:6px 10px;font-size:12px;font-weight:800;color:var(--sub);white-space:nowrap}
.qz-o span.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.qz-r{background:var(--ink);color:var(--bg);padding:18px 18px 20px;display:flex;flex-direction:column;gap:10px}
.qz-rt{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.2em;color:var(--accent)}
.qz-rb{font-family:var(--fh);font-weight:900;font-size:17px;line-height:1.55}
.qz-rb small{display:block;font-size:12px;font-weight:700;opacity:.8;margin-top:4px}
.qz-r .btn-fill{margin-top:auto;text-align:center}
.qz-r .hero-mini{color:var(--bg);opacity:.75;margin:0}
body[data-skin="stadium"] .qz-r{background:var(--card);color:var(--ink)}
body[data-skin="stadium"] .qz-r .hero-mini{color:var(--ink)}
body[data-skin="bright"] .qz-q,body[data-skin="stadium"] .qz-q{border-radius:var(--r)}
body[data-skin="bright"] .qz-r,body[data-skin="stadium"] .qz-r{border-radius:var(--r)}
@media(min-width:760px){.qz-g{grid-template-columns:1fr 1fr 1fr 1.25fr;gap:12px}}
'''
HTML='''<!-- ============ 3問診断 ============ -->
<section class="sec qz" id="shindan">
  <div class="wrap">
    <div class="eyebrow">QUIZ</div>
    <div class="sec-h"><h2>種目が決まっていなくても、<em>3つの質問</em>で。</h2></div>
    <div class="sec-sub">地域・年齢・好きな遊び方に答えると、合いそうな種目と近くのクラブを提案します。1分で終わります。</div>
    <div class="qz-g">
      <div class="qz-q"><div class="qz-n">Q1 ・ WHERE</div><div class="qz-t">どこで、探しますか。</div><div class="qz-o"><span class="on">世田谷区</span><span>現在地から</span></div></div>
      <div class="qz-q"><div class="qz-n">Q2 ・ WHO</div><div class="qz-t">お子さんは、いまいくつですか。</div><div class="qz-o"><span>未就学</span><span class="on">小学1〜3年</span><span>小学4〜6年</span></div></div>
      <div class="qz-q"><div class="qz-n">Q3 ・ STYLE</div><div class="qz-t">遊ぶときは、どちらが多いですか。</div><div class="qz-o"><span class="on">友だちと盛り上がる</span><span>ひとりで集中</span></div></div>
      <div class="qz-r"><div class="qz-rt">RESULT</div><div class="qz-rb">合いそうな種目 3つと、<br>近くのクラブ。<small>結果はマイページに保存できます。</small></div><a class="btn-fill" href="shindan-preview.html" data-quiz>質問に答えてさがす（無料・1分）</a></div>
    </div>
  </div>
</section>

'''
# CSS：QUIZ BAND ブロックを HERO の手前に（既にあれば置換）
if '/* ===================== QUIZ BAND' in top:
    a=top.index('/* ===================== QUIZ BAND'); b=top.index('/* ===================== HERO'); top=top[:a]+CSS+top[b:]
else:
    b=top.index('/* ===================== HERO'); top=top[:b]+CSS+top[b:]
# HTML：既存があれば置換、なければテーマ別まとめの手前に
mk='<!-- ============ テーマ別まとめ'
if '<!-- ============ 3問診断' in top:
    a=top.index('<!-- ============ 3問診断'); b=top.index(mk); top=top[:a]+HTML+top[b:]
else:
    b=top.index(mk); top=top[:b]+HTML+top[b:]
open(f,'w',encoding='utf-8').write(top); print('quiz band ok')
