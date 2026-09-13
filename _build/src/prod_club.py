# クラブ詳細 v2 本番（club.html?id=…）：新デザインの骨組み＋旧 club.html のデータ処理（体験申込・質問・コメント・SEO）を移植
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
ANON=re.search(r"SB_KEY = '([^']+)'",open(D+'shared.js',encoding='utf-8').read()).group(1)
v2=C.strip_preview(open(P+'club_v2.css',encoding='utf-8').read())
CSS=v2+'''
/* ---- 本番の補い ---- */
.spec{background:transparent;border:0;gap:8px;padding:0}
.spec>div{background:var(--card);border:1px solid var(--line);border-radius:var(--r)}
#cd-veil{position:fixed;inset:0;background:var(--bg);z-index:50;display:flex;align-items:center;justify-content:center;transition:opacity .25s}
#cd-veil i{width:28px;height:28px;border:3px solid var(--line);border-top-color:var(--accent);border-radius:50%;animation:cdspin .8s linear infinite}
@keyframes cdspin{to{transform:rotate(360deg)}}
[hidden]{display:none!important}
.bc a{color:var(--sub)}
.chero .ph iframe{width:100%;height:100%;border:0;display:block}
.chero .ph .nc-ph{aspect-ratio:16/9}
.clogo img{width:100%;height:100%;object-fit:cover;display:block;border-radius:50%}
.cstats span{cursor:default}
.cstats .lk{cursor:pointer}
.spec dd .na{color:var(--sub);font-size:13px;font-weight:700}
.cta1 .fav.on svg{fill:var(--accent);stroke:var(--accent)}
.cta-ask{margin:10px 0 0;text-align:center;font-size:12.5px;font-weight:700;color:var(--sub)}
.cta-ask a{text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.photos .rail .card{cursor:pointer}
.photos .rail .card-v{aspect-ratio:4/3}
.links a{cursor:pointer}
.mapb .ph{aspect-ratio:16/9;background:var(--line)}
.mapb .ph iframe{width:100%;height:100%;border:0;display:block}
/* 口コミ（コメント） */
.cmt-form{display:grid;gap:10px;border:1px solid var(--line);border-radius:var(--r);padding:14px;background:var(--card);margin-bottom:14px}
.cmt-form .who{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;color:var(--sub)}
.cmt-form .av,.rev .av{width:30px;height:30px;border-radius:50%;background:var(--accent);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;flex:none}
.cmt-form textarea{width:100%;border:1px solid var(--line);border-radius:calc(var(--r) - 4px);padding:11px;font-family:var(--f);font-size:14px;line-height:1.7;resize:vertical}
.cmt-form .row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.cmt-form .msg{font-size:12px;font-weight:700}
.cmt-form button{background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:10px 18px;font-family:var(--fh);font-weight:900;font-size:13px;cursor:pointer}
.cmt-login{font-size:13px;font-weight:700;color:var(--sub);border:1px dashed var(--line);border-radius:var(--r);padding:14px;text-align:center;margin-bottom:14px}
.cmt-login a{color:var(--accent);text-decoration:underline;text-underline-offset:3px}
.rev .top{display:flex;align-items:center;gap:8px}
.rev .top .nm{font-weight:900;font-size:13.5px}
.rev .top .dt{margin-left:auto;font-size:11.5px;color:var(--sub);font-weight:700}
.rev .rep{text-align:right;margin-top:4px}
.rev .rep button{background:none;border:0;color:var(--sub);font-size:11px;cursor:pointer;font-family:inherit}
.cmt-empty{font-size:13px;font-weight:700;color:var(--sub);padding:8px 0}
/* モーダル（体験申込・質問） */
.cd-modal{position:fixed;inset:0;background:rgba(15,21,30,.55);z-index:200;display:none;align-items:center;justify-content:center;padding:14px}
.cd-modal .box{position:relative;background:var(--card);color:var(--ink);width:100%;max-width:540px;max-height:92vh;overflow-y:auto;border-radius:var(--r);padding:26px 22px 22px}
.cd-modal .x{position:absolute;right:10px;top:8px;border:0;background:transparent;font-size:26px;line-height:1;color:var(--sub);cursor:pointer;padding:4px 8px}
.cd-modal h2{font-family:var(--fh);font-size:20px;font-weight:900;margin:0 0 6px}
.cd-modal .ld{font-size:12.5px;font-weight:700;color:var(--sub);margin:0 0 14px;line-height:1.7}
.cd-modal label{display:block;font-size:12.5px;font-weight:900;margin:12px 0 5px}
.cd-modal label i{font-style:normal;background:var(--accent);color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;margin-left:6px;vertical-align:1px}
.cd-modal input,.cd-modal select,.cd-modal textarea{width:100%;border:1px solid var(--line);border-radius:calc(var(--r) - 4px);padding:11px 12px;font-family:var(--f);font-size:14px;background:var(--card);color:var(--ink);margin-bottom:6px}
.cd-modal .opts{display:flex;gap:8px;flex-wrap:wrap}
.cd-modal .opts span{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:12.5px;font-weight:900;cursor:pointer}
.cd-modal .opts span.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.cd-modal .err{display:none;background:#fff0f2;color:#b3232e;font-size:12.5px;font-weight:800;padding:10px 12px;border-radius:8px;margin:10px 0}
.cd-modal .send{display:block;width:100%;background:var(--accent);color:#fff;border:0;border-radius:calc(var(--r) - 4px);padding:15px;font-family:var(--fh);font-weight:900;font-size:15px;cursor:pointer;margin-top:14px}
.cd-modal .send:disabled{opacity:.6}
.cd-modal .note{margin:10px 0 0;font-size:11.5px;font-weight:700;color:var(--sub);text-align:center}
.cd-modal .done{display:none;text-align:center;padding:10px 0}
.cd-modal .done .em{font-size:40px}
.cd-modal .done .t{font-family:var(--fh);font-size:18px;font-weight:900;margin:8px 0 6px}
.cd-modal .done p{font-size:13px;font-weight:700;color:var(--sub);line-height:1.8;margin:0 0 14px}
.cd-modal .done a{display:none;background:var(--ink);color:var(--bg);border-radius:999px;padding:12px 20px;font-weight:900;font-size:13.5px;margin:4px}
.cd-modal .done button{display:block;margin:12px auto 0;background:transparent;border:1px solid var(--line);border-radius:999px;padding:10px 18px;font-family:inherit;font-weight:900;cursor:pointer;color:var(--ink)}
.cd-modal .quick{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.cd-modal .quick button{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:7px 11px;font-size:12px;font-weight:800;cursor:pointer;font-family:inherit;color:var(--ink)}
body.cd-lock{overflow:hidden}
.sticky .go{cursor:pointer}
'''
BODY='''<div id="cd-veil"><i></i></div>
<main>
<div class="wrap">
  <div class="bc"><a href="index.html">ホーム</a> › <a id="cd-bc-pref" href="search.html">地域</a> <span id="cd-bc-sep2">›</span> <a id="cd-bc-city" href="search.html">市区町村</a> › <span id="cd-bc-name">クラブ</span></div>
</div>
<section class="sec chead-sec nobg">
  <div class="wrap">
  <div class="chero"><div class="ph" id="cd-hero"></div></div>
  <div class="chead">
    <div class="clogo" id="cd-logo">ク</div>
    <div class="tx">
      <h1 id="cd-name">クラブ</h1>
      <div class="cmeta"><span id="cd-sport-wrap"><span id="cd-sport-icon"></span><b id="cd-sport"></b></span><span id="cd-area"></span><span id="cd-map-link-wrap" hidden><a id="cd-map-link" href="#" target="_blank" rel="noopener">地図で見る</a></span></div>
      <div class="cstats"><span class="lk" id="cd-like-top" title="お気に入り">%(HEART)s<span id="cd-like-n">0</span></span><span id="cd-cmt-top">%(CMT)s<span id="cd-cmt-n">0</span></span></div>
    </div>
  </div>
  <div class="epick" id="cd-epick" hidden>
    <div class="k">EDITORS PICK</div>
    <div class="h" id="cd-epick-h"></div>
    <p id="cd-epick-p"></p>
  </div>
  <dl class="spec" id="cd-spec"></dl>
  </div>
</section>
<div class="wrap">
  <div class="blk" id="cd-style" hidden style="margin-top:22px">
    <h2 data-en="STYLE">このクラブのスタイル</h2>
    <div class="sub">クラブが登録した5段階の目安です。</div>
    <div class="scale" id="cd-style-scale"></div>
  </div>
  <div class="ctags" id="cd-tags"></div>
  <div class="blk photos" id="cd-photos" hidden style="margin-top:22px">
    <h2 data-en="PHOTOS">写真</h2>
    <div class="rail" id="cd-photo-rail"></div>
  </div>
  <div class="cta1">
    <a class="go" id="cd-trial-open-top" href="#">体験申込をする（無料）</a>
    <a class="fav" id="cd-fav" href="#" aria-label="お気に入り">%(HEART)s</a>
  </div>
  <div class="cta-note">申込はチビスポからそのまま送れます。クラブから直接ご連絡が届きます。</div>
  <div class="cta-ask">申し込む前に聞きたいことがあれば、<a id="cd-ask-open">クラブに質問する</a></div>

  <div class="pair" id="cd-grid-rr">
    <div class="blk" id="cd-recommend" hidden>
      <h2 data-en="FOR KIDS WHO">こんなお子様におすすめ</h2>
      <div class="sub">クラブが登録した内容です。</div>
      <ul class="ul rec" id="cd-recommend-list"></ul>
    </div>
    <div class="blk" id="cd-points" hidden>
      <h2 data-en="HIGHLIGHTS">おすすめポイント</h2>
      <ul class="ul" id="cd-points-list"></ul>
    </div>
  </div>

  <div class="blk" id="cd-desc-blk" hidden>
    <h2 data-en="MESSAGE">クラブからの紹介文</h2>
    <p class="body" id="cd-desc"></p>
  </div>

  <div class="blk" id="cd-staff" hidden>
    <h2 data-en="COACHES">コーチ・スタッフ</h2>
    <div class="sub">お子さまが毎週会う人です。</div>
    <div class="staff" id="cd-staff-list"></div>
  </div>

  <div class="blk" id="cd-course" hidden>
    <h2 data-en="COURSES">コース</h2>
    <div class="tscroll"><table class="ctable"><tr><th>コース</th><th>対象</th><th>曜日・時間</th><th>月謝</th></tr><tbody id="cd-course-body"></tbody></table></div>
  </div>

  <div class="blk" id="cd-fees" hidden>
    <h2 data-en="FEES">費用の内訳</h2>
    <div class="sub">月謝のほかにかかるもの。</div>
    <table class="fee" id="cd-fee-table"></table>
  </div>

  <div class="blk" id="cd-map">
    <h2 data-en="ACCESS">地図・アクセス</h2>
    <div class="mapb">
      <div class="ph" id="cd-map-embed"></div>
      <div class="ad"><b>活動場所</b><span id="cd-map-addr-text">住所は登録され次第表示されます</span><span id="cd-venue-wrap" hidden><br><b>会場</b><span id="cd-venue"></span></span><br><a id="cd-map-gmap" href="#" target="_blank" rel="noopener" hidden>Googleマップで開く ›</a></div>
    </div>
  </div>

  <div class="blk" id="cd-comments">
    <h2 data-en="REVIEWS">口コミ・コメント<span class="pr-lb" style="margin-left:8px" id="cd-cmt-count-lb"><span id="cd-cmt-count">0</span>件</span></h2>
    <div class="sub">クラブの雰囲気や体験の感想など、ニックネームで投稿できます。誹謗中傷はご遠慮ください。</div>
    <div class="cmt-form" id="cd-cmt-form" hidden>
      <div class="who"><span class="av" id="cd-cmt-avatar">?</span><span><span id="cd-cmt-nick"></span> として投稿</span></div>
      <textarea id="cd-cmt-body" rows="3" maxlength="1000" placeholder="コメントを入力（1000文字まで）"></textarea>
      <div class="row"><span class="msg" id="cd-cmt-msg"></span><button id="cd-cmt-submit" type="button">投稿する</button></div>
    </div>
    <div class="cmt-login" id="cd-cmt-login" hidden>コメントするには <a href="login.html">ログイン / 会員登録</a></div>
    <div id="cd-cmt-list"></div>
    <div class="cmt-empty" id="cd-cmt-empty" hidden>まだコメントはありません。最初のコメントを書いてみませんか？</div>
  </div>

  <div class="blk" id="cd-links-blk" hidden>
    <h2 data-en="LINKS">公式リンク</h2>
    <div class="links" id="cd-links"></div>
  </div>

  <div class="cta2" id="cta2">
    <div class="t">ここまで読んで、気になったら。</div>
    <a class="go" id="cd-trial-open" href="#">体験申込をする（無料）</a>
    <div class="s">見学だけでも大丈夫です。日程はクラブと直接やりとりできます。</div>
  </div>
</div>

<section class="sec sec-alt pr" id="cd-near-sec" hidden>
  <div class="wrap">
    <div class="eyebrow">NEARBY</div>
    <div class="sec-h"><h2>近くの<em>クラブ</em></h2><a class="more" id="cd-near-more" href="search.html">この地域のクラブをすべて見る ›</a></div>
    <div class="rec" id="cd-club"></div>
  </div>
</section>
<section class="sec pr" id="cd-comp-sec" hidden>
  <div class="wrap">
    <div class="eyebrow">LOCAL PARTNERS</div>
    <div class="sec-h"><h2>地域の<em>おすすめ</em>企業<span class="pr-lb">PR</span></h2><span class="more">子育て世帯に向けて</span></div>
    <div class="ads" id="cd-companies"></div>
    <div class="ads-more">この枠に掲載する事業者の方は <a href="service-ads.html">掲載のご案内</a> へ。</div>
  </div>
</section>
<div class="wrap">
  <div class="blk">
    <h2 data-en="FOR BEGINNERS">はじめての方へ</h2>
    <div class="arts">
      <a class="art" href="magazine-4.html"><div class="b"><h3>「うちの子に合うクラブ」の見つけ方・5つの視点</h3><div class="m"><b>クラブ選び</b>2026/07/04</div></div><img src="assets/mag-4.jpg" alt="" loading="lazy"></a>
      <a class="art" href="magazine-3.html"><div class="b"><h3>運動が苦手な子でも、楽しく続く習い事の見つけ方</h3><div class="m"><b>はじめて</b>2026/07/03</div></div><img src="assets/mag-3.jpg" alt="" loading="lazy"></a>
    </div>
  </div>
  <div style="height:30px"></div>
</div>
</main>

<div class="sticky" id="sticky">
  <div class="nm" id="cd-sticky-name">クラブ<small id="cd-sticky-sub">体験・見学の申込</small></div>
  <a class="go" id="cd-trial-open-sticky">体験申込</a>
</div>

<div class="cd-modal" id="cd-trial-modal" role="dialog" aria-modal="true">
  <div class="box">
    <button class="x" id="cd-trial-close" type="button" aria-label="閉じる">&times;</button>
    <h2>体験申込み（無料）</h2>
    <p class="ld" id="cd-trial-team"></p>
    <div id="cd-trial-form">
      <label>お子さまのお名前<i>必須</i></label><input id="tr-child" type="text" placeholder="例：山田 太郎">
      <label>お名前の読み方（任意）</label><input id="tr-kana" type="text" placeholder="例：やまだ たろう">
      <label>お子さまの学年<i>必須</i></label>
      <select id="tr-grade"><option value="">選択してください</option><option>未就学（年少以下）</option><option>年中</option><option>年長</option><option>小学1年</option><option>小学2年</option><option>小学3年</option><option>小学4年</option><option>小学5年</option><option>小学6年</option><option>中学1年</option><option>中学2年</option><option>中学3年</option></select>
      <label>経験</label>
      <div class="opts" id="tr-exp"><span class="tr-exp-opt" data-v="はじめて">はじめて</span><span class="tr-exp-opt" data-v="少し経験あり">少し経験あり</span><span class="tr-exp-opt" data-v="経験者">経験者</span></div>
      <label>体験希望日（任意）</label><input id="tr-date1" type="text" placeholder="第1希望（例：7月12日（土）午前）"><input id="tr-date2" type="text" placeholder="第2希望（任意）">
      <label>保護者のお名前<i>必須</i></label><input id="tr-name" type="text" placeholder="例：山田 花子" autocomplete="name">
      <div id="tr-email-wrap"><label>連絡先メールアドレス<i>必須</i></label><input id="tr-email" type="email" placeholder="you@example.com" autocomplete="email"></div>
      <label>メッセージ（任意）</label><textarea id="tr-msg" rows="3" maxlength="500" placeholder="質問や気になることがあればどうぞ"></textarea>
      <div class="err" id="tr-err"></div>
      <button class="send" id="tr-submit" type="button">この内容で申し込む</button>
      <p class="note">申込後、そのままクラブとメッセージでやり取りできます。</p>
    </div>
    <div class="done" id="cd-trial-done">
      <div class="em">🎉</div><div class="t">申込みを送信しました</div>
      <p id="cd-trial-done-msg">クラブから連絡が届くまでお待ちください。</p>
      <a id="cd-trial-chat" href="mypage.html#msg">メッセージを開く</a><a id="cd-trial-signup" href="login.html">無料で会員登録する</a>
      <button id="cd-trial-done-close" type="button">閉じる</button>
    </div>
  </div>
</div>
<div class="cd-modal" id="cd-ask-modal" role="dialog" aria-modal="true">
  <div class="box">
    <button class="x" id="cd-ask-close" type="button" aria-label="閉じる">&times;</button>
    <h2>クラブに質問する</h2>
    <p class="ld">申し込む前の確認だけでも大丈夫です。メールアドレスは相手に表示されません。</p>
    <div id="cd-ask-form">
      <div class="quick" id="cd-ask-quick"></div>
      <textarea id="cd-ask-body" rows="4" maxlength="500" placeholder="聞きたいことを書いてください"></textarea>
      <div class="err" id="cd-ask-err"></div>
      <button class="send" id="cd-ask-send" type="button">質問を送る</button>
    </div>
    <div class="done" id="cd-ask-done">
      <div class="em">✉️</div><div class="t">質問を送りました</div>
      <p>クラブからの返信はマイページのメッセージに届きます。</p>
      <a href="mypage.html#msg" style="display:inline-block">メッセージを開く</a>
    </div>
  </div>
</div>'''%dict(HEART='<svg viewBox="0 0 24 24"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>',CMT='<svg viewBox="0 0 24 24"><path d="M21 11.5a8.5 8.5 0 0 1-12.2 7.7L3 21l1.8-5.8A8.5 8.5 0 1 1 21 11.5z"/></svg>')
JS=open(P+'club_prod.js',encoding='utf-8').read().replace('__ANON__',ANON)
C.prodpage('club.html','クラブ詳細｜チビスポ','子どものスポーツクラブの詳細。活動日・月謝・対象年齢・雰囲気・写真を見て、体験の申込みまでそのまま。',BODY,css=CSS,js='<script>\n'+JS+'\n</script>',supabase=True,noindex=False,scripts=('club-card.js?v='+C.V,'comment-guard.js?v=20260802','site.js?v='+C.V))
