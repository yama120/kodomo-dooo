# ---- 管理画面（プレビュー v2・2026-09-12）：本番 admin.html（クラブ承認・編集・削除／体験申込／コメント通報）に、新デザインで増える管理（広告・記事・問い合わせ・お知らせ登録・編集部の一言）を足す
ad2_css='''
.am-head{display:grid;grid-template-columns:1fr;gap:12px;align-items:center;padding:22px 0 14px;border-bottom:2px solid var(--ink)}
.am-head .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:3px}
.am-head h1{font-family:var(--fh);margin:0;font-size:clamp(20px,5vw,26px);font-weight:900;line-height:1.2;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.am-head h1 .adm{font-size:10.5px;font-weight:900;padding:4px 8px;background:var(--ink);color:var(--bg);letter-spacing:.06em}
.am-head p{margin:4px 0 0;font-size:12px;font-weight:700;color:var(--sub)}
.am-act{display:flex;gap:8px;flex-wrap:wrap}
.am-act a{font-size:12px;font-weight:900;padding:9px 12px;border:1.5px solid var(--ink);color:var(--ink);white-space:nowrap}
.am-kpi{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:14px 0 0}
.am-kpi a{border:1px solid var(--ink);background:var(--card);padding:12px 14px;color:var(--ink);position:relative}
.am-kpi a:hover{box-shadow:6px 6px 0 var(--ink);transform:translateY(-2px)}
.am-kpi .k{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.22em;color:var(--sub)}
.am-kpi b{display:block;font-family:'Anton',sans-serif;font-size:28px;line-height:1.1;margin:4px 0 2px}
.am-kpi b.hot{color:var(--accent)}
.am-kpi small{font-size:11px;font-weight:700;color:var(--sub)}
.am-tabs{position:sticky;top:56px;z-index:20;background:var(--bg);display:flex;border-bottom:1px solid var(--ink);margin:16px -20px 0;padding:0 20px;overflow-x:auto;scrollbar-width:none}
.am-tabs::-webkit-scrollbar{display:none}
.am-tabs button{flex:none;background:transparent;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:13px 12px 11px;font-family:var(--fh);font-size:13px;font-weight:900;color:var(--sub);cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.am-tabs button i{font-style:normal;font-family:'Anton',sans-serif;font-size:10.5px;background:var(--accent);color:#fff;padding:2px 6px;border-radius:999px;min-width:20px;text-align:center}
.am-tabs button i.off{background:var(--line);color:var(--sub)}
.am-tabs button.on{color:var(--ink);border-bottom-color:var(--ink)}
.am-panel{display:none;padding:22px 0 0}
.am-panel.on{display:block}
.am-panel h2{font-family:var(--fh);margin:0 0 4px;font-size:clamp(18px,4.4vw,22px);font-weight:900;border:0;padding:0}
.am-panel h2 em{font-style:normal;color:var(--accent)}
.am-panel .lead{margin:0 0 14px;font-size:12px;font-weight:700;color:var(--sub);line-height:1.8}
.am-sub{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.am-sub span{font-size:11px;font-weight:900;padding:6px 10px;border:1px solid var(--line);color:var(--sub);cursor:pointer}
.am-sub span.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.am-srch{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.am-srch input{flex:1;min-width:200px;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:13px;font-weight:700;padding:9px 12px}
.am-srch select{border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:12.5px;font-weight:700;padding:9px 10px}
/* 一覧（表） */
.am-tbl{width:100%;min-width:680px;border-collapse:collapse;font-size:12.5px;background:var(--card);border:1px solid var(--ink)}
.am-tbl th{text-align:left;font-size:10px;letter-spacing:.14em;color:var(--sub);font-weight:900;padding:10px 12px;border-bottom:2px solid var(--ink);white-space:nowrap}
.am-tbl td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
.am-tbl tr:last-child td{border-bottom:0}
.am-tbl .nm{font-family:var(--fh);font-weight:900;font-size:13.5px;white-space:nowrap}
.am-tbl .nm small{display:block;font-size:11px;font-weight:700;color:var(--sub)}
.am-tbl .th{width:44px;height:34px;object-fit:cover;display:block;border:1px solid var(--line)}
.am-st{display:inline-block;font-size:10.5px;font-weight:900;letter-spacing:.04em;padding:3px 8px;border:1px solid var(--line);color:var(--sub);white-space:nowrap}
.am-st.pend{background:var(--accent);border-color:var(--accent);color:#fff}
.am-st.ok{background:#1f9d55;border-color:#1f9d55;color:#fff}
.am-st.pause{background:#c9c5bb;border-color:#c9c5bb;color:#111}
.am-st.paid{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.am-btns{display:flex;gap:4px;flex-wrap:wrap}
.am-btns a{font-size:11px;font-weight:900;padding:6px 9px;border:1.5px solid var(--ink);color:var(--ink);white-space:nowrap}
.am-btns a.pri{background:var(--ink);color:var(--bg)}
.am-btns a.acc{background:var(--accent);border-color:var(--accent);color:#fff}
.am-btns a.dim{border-color:var(--line);color:var(--sub)}
.am-wrapx{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -20px;padding:0 20px}
@media(min-width:760px){.am-wrapx{margin:0;padding:0}}
/* 承認の詳細（右） */
.am-split{display:grid;grid-template-columns:1fr;gap:14px}
.am-detail{border:1px solid var(--ink);background:var(--card);padding:16px;align-self:start}
.am-detail .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.22em;color:var(--accent);margin-bottom:6px}
.am-detail h3{font-family:var(--fh);margin:0 0 8px;font-size:16px;font-weight:900}
.am-detail dl{margin:0 0 12px;display:grid;grid-template-columns:90px 1fr;gap:6px 10px;font-size:12px;font-weight:700}
.am-detail dt{color:var(--sub)}.am-detail dd{margin:0}
.am-detail .chk{display:grid;gap:6px;margin-bottom:12px}
.am-detail .chk label{display:flex;gap:8px;align-items:flex-start;font-size:12px;font-weight:700;line-height:1.5}
.am-detail .chk input{margin-top:3px}
.am-detail textarea{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:12.5px;font-weight:700;padding:9px 10px;min-height:64px;box-sizing:border-box}
.am-detail .row{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.am-detail .row a{font-size:12px;font-weight:900;padding:9px 12px;border:1.5px solid var(--ink);color:var(--ink)}
.am-detail .row a.acc{background:#1f9d55;border-color:#1f9d55;color:#fff}
.am-detail .row a.rej{border-color:var(--accent);color:var(--accent)}
.am-note{margin-top:10px;font-size:11px;font-weight:700;color:var(--sub);line-height:1.7}
/* 編集部の一言 */
.am-ed{display:grid;gap:10px}
.am-ed .c{display:grid;grid-template-columns:44px 1fr auto;gap:10px;align-items:center;border:1px solid var(--ink);background:var(--card);padding:10px 12px}
.am-ed .c img{width:44px;height:34px;object-fit:cover;border:1px solid var(--line)}
.am-ed .c b{display:block;font-family:var(--fh);font-size:13px;font-weight:900}
.am-ed .c input{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:12.5px;font-weight:700;padding:7px 9px;margin-top:4px;box-sizing:border-box}
.am-ed .c small{display:block;font-size:10.5px;font-weight:700;color:var(--sub);margin-top:3px}
/* 問い合わせ */
.am-inq .r{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}
.am-inq .kind{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.14em;padding:5px 8px;border:1px solid var(--ink);white-space:nowrap}
.am-inq .kind.ads{background:var(--accent);border-color:var(--accent);color:#fff}
.am-inq b{display:block;font-family:var(--fh);font-size:13.5px;font-weight:900}
.am-inq small{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:2px;line-height:1.6}
.am-inq .inq-list{border-top:2px solid var(--ink)}
@media(min-width:760px){
  .am-head{grid-template-columns:1fr auto;padding:30px 0 18px}
  .am-kpi{grid-template-columns:repeat(6,1fr);gap:10px}
  .am-tabs{margin:18px 0 0;padding:0;top:60px}
  .am-split{grid-template-columns:1fr 360px;gap:20px}
}
'''
A='assets/preview-video/'
def st(t,c=''): return '<span class="am-st %s">%s</span>'%(c,t)
def btns(*bs): return '<div class="am-btns">'+''.join('<a class="%s" href="#">%s</a>'%(c,t) for t,c in bs)+'</div>'
teams=[('post-trial.jpg','さくらキッズダンス','ダンス ・ 世田谷区 ・ 9/12 申請',st('承認待ち','pend'),'フリー',btns(('見る',''),('承認','acc'),('修正依頼',''),('却下','dim'))),
 ('jp-soccer-run.jpg','わかばFC','サッカー ・ 世田谷区 ・ 8/30 承認',st('公開中','ok'),st('スタンダード','paid'),btns(('見る',''),('編集','pri'),('停止','dim'))),
 ('wm-bball-jp.jpg','港北ジュニアバスケ','バスケットボール ・ 横浜市港北区 ・ 8/12 承認',st('公開中','ok'),'フリー',btns(('見る',''),('編集','pri'),('停止','dim'))),
 ('wm-karate.jpg','狛江キッズ空手','空手 ・ 狛江市 ・ 7/2 承認',st('募集停止中','pause'),'フリー',btns(('見る',''),('編集','pri'),('再開',''))),
 ('jp-soccer-keep.jpg','青空サッカークラブ','サッカー ・ 練馬区 ・ 9/10 申請',st('承認待ち','pend'),'フリー',btns(('見る',''),('承認','acc'),('修正依頼',''),('却下','dim')))]
rows=''.join('<tr><td><img class="th" src="%s%s" alt=""></td><td class="nm">%s<small>%s</small></td><td>%s</td><td>%s</td><td>%s</td></tr>'%(A,im,n,m,s1,s2,b) for im,n,m,s1,s2,b in teams)
adm_body='''
<main><div class="wrap">
  <div class="note">【管理画面 v2（2026-09-12）】本番 admin.html（管理者ログイン／クラブ：承認待ち・公開中・募集停止中・却下＋編集モーダル・削除／体験申込：新規・対応中・対応済み＋クラブ別ランキング／コメント通報：未対応・対応済み・問題なし）を新デザインに。★新デザインで増える管理を足した：<b>編集部おすすめ（有料クラブの一言）</b>／<b>広告（companies：掲載企業・期限）</b>／<b>マガジン（articles：公開・カテゴリ・関連クラブ）</b>／<b>問い合わせ（inquiries：広告・SNS・HP・相談のフォーム）とお知らせ登録（waitlist）</b>。承認は「一覧＋右に確認カード（チェック4つ・修正依頼の文面・承認／却下）」。上のKPI 6つは「今日やること」の順。DB：inquiries／waitlist／editor_headline は差分台帳（project_chibispo_db_gap_2026_09）。<code>?tab=teams</code> などで直接開ける。</div>

  <div class="am-head">
    <div><div class="k">ADMIN</div><h1>チビスポ 管理画面 <span class="adm">管理者</span></h1><p>hyogo ・ 最終ログイン 9/12 07:40</p></div>
    <div class="am-act"><a href="video-hero-preview.html">サイトを見る ›</a><a href="#">ログアウト</a></div>
  </div>
  <div class="am-kpi">
    <a href="#" data-tab="teams"><div class="k">承認待ち</div><b class="hot">2</b><small>クラブの申請</small></a>
    <a href="#" data-tab="trial"><div class="k">未対応の申込</div><b class="hot">3</b><small>クラブが未返信 48h超</small></a>
    <a href="#" data-tab="inq"><div class="k">問い合わせ</div><b class="hot">1</b><small>広告の申込</small></a>
    <a href="#" data-tab="report"><div class="k">通報</div><b>0</b><small>コメント</small></a>
    <a href="#" data-tab="teams"><div class="k">公開中</div><b>136</b><small>／ 141 クラブ</small></a>
    <a href="#" data-tab="ads"><div class="k">広告</div><b>4</b><small>期限30日以内 1</small></a>
  </div>

  <div class="am-tabs" id="amTabs">
    <button data-tab="teams" class="on">クラブ <i>2</i></button>
    <button data-tab="editor">編集部おすすめ</button>
    <button data-tab="trial">体験申込 <i>3</i></button>
    <button data-tab="inq">問い合わせ <i>1</i></button>
    <button data-tab="ads">広告 <i class="off">4</i></button>
    <button data-tab="mag">マガジン</button>
    <button data-tab="report">通報 <i class="off">0</i></button>
  </div>

  <section class="am-panel on" data-tab="teams">
    <h2>クラブの<em>承認と管理</em></h2>
    <p class="lead">承認待ちを先頭に。承認すると検索・地図・種目ページに載り、クラブにメールが届きます。</p>
    <div class="am-sub"><span class="on">承認待ち 2</span><span>公開中 136</span><span>募集停止中 3</span><span>却下 0</span><span>すべて 141</span></div>
    <div class="am-srch"><input placeholder="クラブ名・地域・種目・メールで検索"><select><option>プラン：すべて</option><option>フリー</option><option>スタンダード</option><option>プロ</option></select><select><option>並び：新しい順</option><option>申込が多い順</option><option>充実度が低い順</option></select></div>
    <div class="am-split">
      <div class="am-wrapx"><table class="am-tbl"><tr><th></th><th>クラブ</th><th>状態</th><th>プラン</th><th>操作</th></tr>%(rows)s</table></div>
      <div class="am-detail">
        <div class="k">REVIEW</div><h3>さくらキッズダンス</h3>
        <dl><dt>種目</dt><dd>ダンス</dd><dt>住所</dt><dd>東京都世田谷区桜丘2-1（桜丘区民センター）</dd><dt>対象</dt><dd>未就学・小学生</dd><dt>月謝</dt><dd>4,500円 ・ 初期費用 5,000円</dd><dt>連絡先</dt><dd>sakura@example.com</dd><dt>写真</dt><dd>1枚</dd></dl>
        <div class="chk"><label><input type="checkbox" checked>実在するクラブ（サイト・SNS・電話のいずれかで確認）</label><label><input type="checkbox" checked>住所が地図に落ちる</label><label><input type="checkbox" checked>紹介文に連絡先・URL・勧誘文がない</label><label><input type="checkbox">写真に他人の顔・ロゴの無断使用がない</label></div>
        <textarea placeholder="修正依頼の文面（クラブにメールで届きます）">写真に写っているお子さまの掲載許可が取れているか、ご確認をお願いします。</textarea>
        <div class="row"><a class="acc" href="#">承認して公開</a><a href="#">修正を依頼</a><a class="rej" href="#">却下</a></div>
        <div class="am-note">承認するとクラブに「掲載が始まりました」のメール。修正依頼は理由つきで届き、直したら再申請されます。</div>
      </div>
    </div>
  </section>

  <section class="am-panel" data-tab="editor">
    <h2>編集部<em>おすすめ</em></h2>
    <p class="lead">有料（スタンダード以上）のクラブに、編集部の一言を付けます。TOPの「編集部おすすめ」枠と検索結果の TOP PICK に出ます。</p>
    <div class="am-sub"><span class="on">一言なし 3</span><span>掲載中 5</span><span>すべて 8</span></div>
    <div class="am-ed">
      <div class="c"><img src="%(A)sjp-soccer-run.jpg" alt=""><div><b>わかばFC <span class="am-st paid">スタンダード</span></b><input value="はじめての子が半分。コーチの声かけが、とにかくやさしい。"><small>26字 ・ 40字まで ・ 検索結果の1枚目に出ます</small></div>%(b1)s</div>
      <div class="c"><img src="%(A)swm-bball-jp.jpg" alt=""><div><b>さくらミニバスケットボールクラブ <span class="am-st paid">プロ</span></b><input placeholder="一言を書く（40字まで）"><small>未入力 ・ 有料なのに一言がないクラブ</small></div>%(b2)s</div>
      <div class="c"><img src="%(A)swm-kidsrun-1.jpg" alt=""><div><b>杉並アスレチッククラブ <span class="am-st paid">スタンダード</span></b><input placeholder="一言を書く（40字まで）"><small>未入力</small></div>%(b2)s</div>
    </div>
    <div class="am-note">一言は「編集部が見に行った」とは書かない。写真と情報がそろっていて雰囲気が伝わるクラブに付ける（言い方の線）。</div>
  </section>

  <section class="am-panel" data-tab="trial">
    <h2>体験申込の<em>見守り</em></h2>
    <p class="lead">クラブが返信していない申込を先に。48時間を超えたらクラブに催促のメールを送れます。</p>
    <div class="am-sub"><span class="on">クラブ未返信 3</span><span>やり取り中 9</span><span>体験済み 21</span><span>すべて 33</span></div>
    <div class="am-wrapx"><table class="am-tbl"><tr><th>クラブ</th><th>保護者 ・ お子さま</th><th>受信</th><th>状態</th><th>操作</th></tr>
      <tr><td class="nm">狛江キッズ空手</td><td>たなか さん ・ 小3</td><td>9/9 ・ 3日前</td><td>%(pend)s</td><td>%(tb)s</td></tr>
      <tr><td class="nm">青空サッカークラブ</td><td>すずき さん ・ 年長</td><td>9/10 ・ 2日前</td><td>%(pend)s</td><td>%(tb)s</td></tr>
      <tr><td class="nm">港北ジュニアバスケ</td><td>いとう さん ・ 小5</td><td>9/10 ・ 2日前</td><td>%(pend)s</td><td>%(tb)s</td></tr>
    </table></div>
    <h2 style="margin-top:22px;font-size:16px">今月の申込が多いクラブ</h2>
    <div class="am-wrapx"><table class="am-tbl"><tr><th>#</th><th>クラブ</th><th>申込</th><th>返信率</th><th>プラン</th></tr>
      <tr><td>1</td><td class="nm">わかばFC</td><td>7</td><td>100%%</td><td>%(paid)s</td></tr><tr><td>2</td><td class="nm">さくらミニバスケットボールクラブ</td><td>5</td><td>80%%</td><td>%(paid2)s</td></tr><tr><td>3</td><td class="nm">港北ジュニアバスケ</td><td>4</td><td>50%%</td><td>フリー</td></tr>
    </table></div>
  </section>

  <section class="am-panel" data-tab="inq">
    <h2>問い合わせと<em>お知らせ登録</em></h2>
    <p class="lead">サービスLPのフォーム（広告・SNS・HP・相談）と、準備中サービスの「お知らせを受け取る」の登録です。</p>
    <div class="am-sub"><span class="on">未対応 1</span><span>対応中 2</span><span>完了 6</span><span>お知らせ登録 14</span></div>
    <div class="am-inq"><div class="inq-list">
      <div class="r"><span class="kind ads">ADS</span><div><b>みどり整骨院 ・ 山本 さん</b><small>世田谷区 ・ 企業紹介プラン ¥50,000/年 ・ 「体験クラブの保護者に届けたい」 ・ 9/12 09:10</small></div>%(ib1)s</div>
      <div class="r"><span class="kind">SNS</span><div><b>杉並アスレチッククラブ ・ 佐藤 さん</b><small>SNS立ち上げパック ・ 「Instagramを始めたい」 ・ 9/11</small></div>%(ib2)s</div>
      <div class="r"><span class="kind">HP</span><div><b>狛江キッズ空手 ・ 木村 さん</b><small>ホームページ制作 ・ 見本「スポーツ」タイプ希望 ・ 9/9</small></div>%(ib2)s</div>
      <div class="r"><span class="kind">WAIT</span><div><b>お知らせ登録（撮影・動画制作）14件</b><small>受付を始めるとき、一斉メールで案内（Resend）。最新 9/12</small></div>%(ib3)s</div>
    </div></div>
  </section>

  <section class="am-panel" data-tab="ads">
    <h2>地域の<em>広告</em></h2>
    <p class="lead">掲載企業と期限。検索結果・クラブ詳細の「地域のおすすめ企業」枠に出ます。同業は市区町村ごとに少数に限定。</p>
    <div class="am-wrapx"><table class="am-tbl"><tr><th></th><th>企業</th><th>地域 ・ 業種</th><th>期限</th><th>状態</th><th>操作</th></tr>
      <tr><td><img class="th" src="%(A)sad-seikotsu.jpg" alt=""></td><td class="nm">さくら整骨院<small>pr-sample.html</small></td><td>世田谷区 ・ 整骨院</td><td>2027/03/31</td><td>%(ok)s</td><td>%(ab)s</td></tr>
      <tr><td><img class="th" src="%(A)sad-sports.jpg" alt=""></td><td class="nm">スポーツ用品 タケダ<small>pr-sample-sports.html</small></td><td>世田谷区 ・ スポーツ用品</td><td>2026/10/05 <span class="am-st pend">30日以内</span></td><td>%(ok)s</td><td>%(ab)s</td></tr>
      <tr><td><img class="th" src="%(A)sad-shika.jpg" alt=""></td><td class="nm">みなと歯科<small>pr-sample-design.html</small></td><td>港区 ・ 歯科</td><td>2027/01/20</td><td>%(ok)s</td><td>%(ab)s</td></tr>
      <tr><td><img class="th" src="%(A)sad-uniform.jpg" alt=""></td><td class="nm">ユニフォーム工房<small>—</small></td><td>練馬区 ・ ユニフォーム</td><td>—</td><td>%(pend2)s</td><td>%(ab2)s</td></tr>
    </table></div>
  </section>

  <section class="am-panel" data-tab="mag">
    <h2>マガジン</h2>
    <p class="lead">記事の公開・カテゴリ・記事に出てくるクラブ。運動をすすめる読み物として。</p>
    <div class="am-sub"><span class="on">公開 7</span><span>下書き 2</span></div>
    <div class="am-wrapx"><table class="am-tbl"><tr><th>記事</th><th>カテゴリ</th><th>関連クラブ</th><th>公開日</th><th>操作</th></tr>
      <tr><td class="nm">6歳までの運動が、脳を育てる<small>art-01 ・ 読了4分</small></td><td>からだと発達</td><td>わかばFC ほか2</td><td>9/1</td><td>%(mb)s</td></tr>
      <tr><td class="nm">はじめての習い事、何を見て決める？<small>art-02 ・ 読了5分</small></td><td>クラブの選び方</td><td>—</td><td>8/20</td><td>%(mb)s</td></tr>
      <tr><td class="nm">週1回でも、運動は効く<small>art-08 ・ 下書き</small></td><td>からだと発達</td><td>—</td><td>—</td><td>%(mb2)s</td></tr>
    </table></div>
  </section>

  <section class="am-panel" data-tab="report">
    <h2>コメントの<em>通報</em></h2>
    <p class="lead">通報されたコメントを確認して、非表示にするか問題なしにします。</p>
    <div class="am-sub"><span class="on">未対応 0</span><span>対応済み 3</span><span>問題なし 5</span></div>
    <div class="am-wrapx"><table class="am-tbl"><tr><th>コメント</th><th>クラブ</th><th>理由</th><th>日時</th><th>操作</th></tr>
      <tr><td>「コーチが厳しすぎる。二度と行かない」<br><small>投稿者：匿名さん ・ 通報 1</small></td><td class="nm">—</td><td>誹謗中傷</td><td>8/30 ・ 対応済み</td><td>%(rb)s</td></tr>
    </table></div>
  </section>
  <div style="height:40px"></div>
</div></main>
'''%dict(A=A,rows=rows,
  b1=btns(('保存','pri'),('外す','dim')),b2=btns(('保存','pri')),
  pend=st('クラブ未返信','pend'),tb=btns(('やり取りを見る',''),('クラブに催促','acc')),paid=st('スタンダード','paid'),paid2=st('プロ','paid'),
  ib1=btns(('返信する','acc'),('対応中に','')),ib2=btns(('見る',''),('完了','')),ib3=btns(('一覧','') ,('一斉メール','pri')),
  ok=st('掲載中','ok'),pend2=st('申込中','pend'),ab=btns(('編集','pri'),('更新の案内','')),ab2=btns(('掲載を開始','acc'),('編集','pri')),
  mb=btns(('編集','pri'),('非公開','dim')),mb2=btns(('編集','pri'),('公開','acc')),rb=btns(('コメントを見る',''),('表示に戻す','dim')))
adm_js='''<script>
(function(){
 var tabs=document.getElementById('amTabs');
 function show(k){document.querySelectorAll('.am-panel').forEach(function(p){p.classList.toggle('on',p.dataset.tab===k)});tabs.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.tab===k)})}
 tabs.addEventListener('click',function(e){var b=e.target.closest('button');if(b){show(b.dataset.tab);history.replaceState(null,'','?tab='+b.dataset.tab)}});
 document.addEventListener('click',function(e){var a=e.target.closest('a[data-tab]');if(a){e.preventDefault();show(a.dataset.tab);history.replaceState(null,'','?tab='+a.dataset.tab);window.scrollTo({top:tabs.getBoundingClientRect().top+scrollY-70,behavior:'smooth'})}var s=e.target.closest('.am-sub span');if(s){s.parentNode.querySelectorAll('span').forEach(function(x){x.classList.toggle('on',x===s)})}});
 var m=location.search.match(/tab=(teams|editor|trial|inq|ads|mag|report)/);if(m)show(m[1]);
})();
</script>'''
page('admin-preview.html','管理画面｜チビスポ（プレビュー）',adm_body,ad2_css,extra_js=adm_js)
