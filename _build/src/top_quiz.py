# TOP に「3問診断」のセクションを足す（スポーツジャンルの直後）。ヘッダーからは外したぶん、ここで見せる
import os
D=os.path.expanduser('~/kodomo-dooo-deploy/'); f=D+'video-hero-preview.html'
top=open(f,encoding='utf-8').read()
CSS='''/* ===================== QUIZ BAND ===================== */
.qz-p{margin-top:14px;background:var(--ink);color:var(--bg);padding:22px 20px 24px;display:grid;gap:20px}
.qz-s{display:grid;grid-template-columns:auto 1fr;column-gap:11px;align-items:baseline}
.qz-s+.qz-s{margin-top:14px}
.qz-s i{grid-row:span 2;font-family:'Anton',sans-serif;font-style:normal;font-size:13px;letter-spacing:.06em;color:var(--accent)}
.qz-s b{font-family:var(--fh);font-weight:900;font-size:15.5px;line-height:1.5}
.qz-s p{margin:3px 0 0;font-size:12px;font-weight:700;line-height:1.75;opacity:.76}
.qz-c{display:flex;flex-direction:column;justify-content:center;gap:9px}
.qz-c .btn-fill{text-align:center}
.qz-c .n{font-size:11.5px;font-weight:700;line-height:1.6;opacity:.72;text-align:center}
body[data-skin="stadium"] .qz-p{background:var(--card);color:var(--ink)}
body[data-skin="bright"] .qz-p,body[data-skin="stadium"] .qz-p{border-radius:var(--r)}
@media(min-width:760px){.qz-p{padding:28px 28px 30px;grid-template-columns:1fr 300px;gap:34px;align-items:center}
.qz-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.qz-s+.qz-s{margin-top:0}}
'''
HTML='''<!-- ============ 3問診断 ============ -->
<section class="sec qz" id="shindan">
  <div class="wrap">
    <div class="eyebrow">QUIZ</div>
    <div class="sec-h"><h2>種目が決まっていなくても、<em>選ぶだけ</em>で。</h2></div>
    <div class="sec-sub">地域や年齢、好きな遊び方。当てはまるものをタップしていくだけで、合いそうな種目と、近くのクラブをお出しします。</div>
    <div class="qz-p">
      <div class="qz-steps">
        <div class="qz-s"><i>01</i><b>タップするだけ</b><p>用意した選択肢から選ぶだけ。文章を書く欄はありません。</p></div>
        <div class="qz-s"><i>02</i><b>合いそうな種目</b><p>遊び方や好きなことから、合いそうな種目を3つ。</p></div>
        <div class="qz-s"><i>03</i><b>近くのクラブ</b><p>その種目で、通える範囲のクラブをそのまま一覧に。</p></div>
      </div>
      <div class="qz-c">
        <a class="btn-fill" href="shindan-preview.html" data-quiz>質問に答えてさがす（無料・1分）</a>
        <div class="n">結果はマイページに保存できます。</div>
      </div>
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
