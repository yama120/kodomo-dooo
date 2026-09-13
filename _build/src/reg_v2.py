# ---- クラブ登録画面（プレビュー v2・2026-09-12）：3ステップ・右に「こう見えます」のカード
rg_css='''
.rg-head{padding:30px 0 18px;border-bottom:2px solid var(--ink)}
.rg-head .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:10px}
.rg-head .ey::before{content:"";width:22px;height:2px;background:var(--accent)}
.rg-head h1{font-family:var(--fh);margin:0 0 8px;font-size:clamp(24px,6vw,38px);font-weight:900;line-height:1.2;letter-spacing:-.01em}
.rg-head h1 em{font-style:normal;color:var(--accent)}
.rg-head p{margin:0;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.rg-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:18px 0 0;border:1px solid var(--ink)}
.rg-steps div{display:flex;align-items:center;gap:6px;padding:10px 8px;font-size:11px;font-weight:900;color:var(--sub);border-right:1px solid var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rg-steps div:last-child{border-right:0}
.rg-steps i{font-style:normal;font-family:'Anton',sans-serif;font-size:12px;width:22px;height:22px;border-radius:50%;border:1.5px solid var(--sub);display:flex;align-items:center;justify-content:center}
.rg-steps div.on{color:var(--ink);background:var(--card)}.rg-steps div.on i{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.rg-steps div.done i{background:var(--accent);border-color:var(--accent);color:#fff}
.rg-lay{display:grid;grid-template-columns:1fr;gap:26px;margin-top:22px}
.rg-sec{border:1px solid var(--ink);background:var(--card);margin-bottom:14px}
.rg-sec .hd{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:14px 16px;border-bottom:1px solid var(--line)}
.rg-sec .hd i{font-style:normal;font-family:'Anton',sans-serif;font-size:14px;width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--bg);display:flex;align-items:center;justify-content:center}
.rg-sec .hd b{display:block;font-family:var(--fh);font-size:16px;font-weight:900}
.rg-sec .hd small{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:2px}
.rg-sec .hd .tm{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.18em;color:var(--accent);white-space:nowrap}
.rg-sec .bd{padding:4px 16px 16px}
.rg-f{display:grid;grid-template-columns:1fr;gap:6px;padding:12px 0;border-bottom:1px solid var(--line)}
.rg-f:last-child{border-bottom:0}
.rg-f>label{font-size:12px;font-weight:900;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.rg-f>label .req{font-size:9.5px;letter-spacing:.08em;background:var(--ink);color:var(--bg);padding:1px 5px}
.rg-f>label .opt{font-size:9.5px;letter-spacing:.08em;border:1px solid var(--line);color:var(--sub);padding:1px 5px}
.rg-f .hint{font-size:11px;font-weight:700;color:var(--sub);line-height:1.6}
.rg-in{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:13.5px;font-weight:700;padding:10px 12px;color:var(--ink)}
.rg-in.sm{max-width:200px}
textarea.rg-in{min-height:96px;resize:vertical}
.rg-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.rg-row .rg-in{width:auto;flex:1;min-width:120px}
.rg-chk{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;border:1px solid var(--ink);padding:8px 11px;background:#fff;cursor:pointer}
.rg-chk.on{background:var(--ink);color:var(--bg)}
.rg-chk input{margin:0}
.rg-cnt{font-size:10.5px;font-weight:700;color:var(--sub);text-align:right}
.rg-drop{border:1.5px dashed var(--ink);padding:18px;text-align:center;background:#fff}
.rg-drop b{display:block;font-family:var(--fh);font-size:13px;font-weight:900;margin-bottom:4px}
.rg-drop small{font-size:11px;font-weight:700;color:var(--sub)}
.rg-more{border:1px solid var(--line);margin-top:6px}
.rg-more summary{list-style:none;cursor:pointer;padding:10px 12px;font-size:12px;font-weight:900;display:flex;justify-content:space-between}
.rg-more summary::-webkit-details-marker{display:none}
.rg-more summary::after{content:"+";font-family:'Anton',sans-serif;color:var(--accent)}
.rg-more[open] summary::after{content:"–"}
.rg-more .in2{padding:0 12px 6px}
.rg-agree{display:flex;gap:10px;align-items:flex-start;font-size:12.5px;font-weight:700;line-height:1.7;padding:12px 0}
.rg-agree a{text-decoration:underline;text-underline-offset:3px;font-weight:900}
.rg-submit{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-top:6px}
.rg-submit small{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.6}
.rg-submit a{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 26px;box-shadow:0 8px 24px rgba(232,69,95,.3)}
/* 右：こう見えます */
.rg-side{display:grid;gap:14px;align-content:start}
.rg-prev{border:1px solid var(--ink);background:var(--card);padding:14px}
.rg-prev .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.rg-prev .t{font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:10px}
.rg-prev .nc{max-width:320px}
.rg-prev p{margin:10px 0 0;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7}
.rg-after{border:1px solid var(--ink);background:var(--ink);color:var(--bg);padding:16px}
.rg-after .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.rg-after ol{margin:0;padding:0;list-style:none;display:grid;gap:8px}
.rg-after li{position:relative;padding-left:26px;font-size:12.5px;font-weight:700;line-height:1.6}
.rg-after li::before{content:attr(data-n);position:absolute;left:0;top:0;font-family:'Anton',sans-serif;color:var(--accent)}
.rg-after li b{color:#fff}
.rg-help{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.8}
.rg-help a{font-weight:900;text-decoration:underline;text-underline-offset:3px;color:var(--ink)}
/* 完了画面（?done=1） */
.rg-done{display:none;border:2px solid var(--ink);background:var(--card);padding:26px 20px 22px;margin-top:22px;max-width:900px}
.rg-done .top{text-align:center;padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:18px}
.rg-done .k2{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:4px}
.rg-done .t2{font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:12px}
.rg-next{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:18px}
.rg-nc{position:relative;display:block;border:1px solid var(--ink);background:#fff;padding:14px 14px 14px 46px;color:var(--ink);transition:transform .15s,box-shadow .15s}
.rg-nc:hover{transform:translateY(-2px);box-shadow:6px 6px 0 var(--ink)}
.rg-nc .n{position:absolute;left:14px;top:14px;font-family:'Anton',sans-serif;font-size:14px;color:var(--accent)}
.rg-nc b{display:block;font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:3px}
.rg-nc small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.6}
.rg-nc small em{font-style:normal;font-family:'Anton',sans-serif;font-size:13px;color:var(--ink);letter-spacing:.02em;margin-left:4px}
.rg-nc.hot{border:2px solid var(--accent);box-shadow:6px 6px 0 var(--accent)}
.rg-nc .go{display:inline-block;margin-top:8px;font-size:11.5px;font-weight:900;background:var(--accent);color:#fff;padding:6px 10px}
.rg-done .row{justify-content:center}
@media(min-width:760px){.rg-next{grid-template-columns:repeat(3,1fr);gap:14px}.rg-done{padding:30px 28px 26px}}
.rg-done .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.rg-done h2{font-family:var(--fh);margin:0 0 8px;font-size:22px;font-weight:900;border:0;padding:0}
.rg-done p{margin:0 0 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.rg-done .row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.rg-done .row a{font-size:13px;font-weight:900;padding:11px 16px;border:1.5px solid var(--ink)}
.rg-done .row a.pri{background:var(--ink);color:var(--bg)}
body.done .rg-lay,body.done .rg-steps{display:none}body.done .rg-done{display:block}
@media(min-width:900px){
  .rg-lay{grid-template-columns:1fr 340px;gap:40px}
  .rg-side{position:sticky;top:80px}
  .rg-f{grid-template-columns:170px 1fr;gap:6px 16px;align-items:start}
  .rg-f>label{padding-top:10px}
  .rg-f .hint{grid-column:2}
  .rg-head{padding:40px 0 22px}
  .rg-steps div{font-size:12px;padding:10px 12px;gap:8px}
}
'''
def f(label,body,req=False,opt=False,hint=''):
    return '<div class="rg-f"><label>%s%s%s</label><div>%s</div>%s</div>'%(label,' <span class="req">必須</span>' if req else '',' <span class="opt">任意</span>' if opt else '',body,('<div class="hint">%s</div>'%hint) if hint else '')
def inp(v='',ph='',cls='',typ='text'): return '<input class="rg-in %s" type="%s" value="%s" placeholder="%s">'%(cls,typ,v,ph)
def chks(opts,on=()): return '<div class="rg-row">'+''.join('<label class="rg-chk%s"><input type="checkbox"%s>%s</label>'%(' on' if o in on else '',' checked' if o in on else '',o) for o in opts)+'</div>'
def sec(n,title,sub,tm,body): return '<div class="rg-sec"><div class="hd"><i>%s</i><div><b>%s</b><small>%s</small></div><span class="tm">%s</span></div><div class="bd">%s</div></div>'%(n,title,sub,tm,body)
preview_card=cards.card(**dict(cards.CLUBS[0],new=True,likes=0,comments=0,video=False))
rg_body='''
<main><div class="wrap">
  <div class="note">【クラブ登録画面 v2（2026-09-12）】本番 register.html（1枚のフォーム→teams に status=pending で登録→運営の承認→掲載。アカウントは承認後のマイページ編集用）を新デザインに。★3ステップを1ページに：①アカウント（メール・パスワード）②クラブの基本（クラブ名・種目・住所＝郵便番号から・対象年齢・曜日・月謝・体験・紹介文・写真1枚・申込の通知先）③確認して送信（利用規約・審査の説明）。右に<b>「こう見えます」＝入力がそのままカードに反映</b>（本番化ではJSで同期）と「送信のあと」の3ステップ。SNS・ホームページ・初期費用は「あとから」に畳んで、必須を減らした（必須＝クラブ名・種目・住所・対象年齢・月謝・紹介文・アカウント）。スタイル・スタッフ・費用の内訳など詳しい項目は登録後にマイページで。<code>?done=1</code> で完了画面。</div>

  <div class="rg-head"><div class="ey">FOR CLUBS ・ FREE LISTING</div><h1>クラブを<em>載せる</em>。</h1><p>登録は1分。写真1枚と紹介文があれば、今日から載せられます。有料プランは登録後にマイページから。</p>
    <div class="rg-steps"><div class="on"><i>1</i>アカウント</div><div><i>2</i>クラブの基本</div><div><i>3</i>確認して送信</div></div>
  </div>

  <div class="rg-lay">
  <div>
    %(s1)s
    %(s2)s
    %(s3)s
  </div>
  <aside class="rg-side">
    <div class="rg-prev"><div class="k">PREVIEW</div><div class="t">検索結果では、こう見えます</div>%(card)s<p>入力するとその場で変わります。紹介文の最初の2行がカードに出ます。</p></div>
    <div class="rg-after"><div class="k">AFTER YOU SEND</div><ol><li data-n="1"><b>運営が内容を確認</b>（最短で当日）</li><li data-n="2"><b>掲載開始</b>。検索・地図・種目ページに載ります</li><li data-n="3"><b>マイページで育てる</b>。スタイル・スタッフ・写真を足すほど申込が集まります</li></ol></div>
    <div class="rg-help">すでに登録している方は <a href="#">ログイン</a>。うまく登録できないときは <a href="#">お問い合わせ</a> から。</div>
  </aside>
  </div>

  <div class="rg-done">
    <div class="top"><div class="k">RECEIVED</div><h2>申請を受け付けました。</h2><p>運営の確認後に掲載されます（最短で当日）。確認が終わったらメールでお知らせします。</p></div>
    <div class="k2">WHILE YOU WAIT</div>
    <div class="t2">待っている間に、できること。</div>
    <div class="rg-next">
      <a class="rg-nc" href="club-mypage-preview.html?tab=media"><div class="n">01</div><b>写真を足す</b><small>フリーは1枚。写真が多いクラブほど体験申込が集まります</small></a>
      <a class="rg-nc" href="club-mypage-preview.html?tab=info"><div class="n">02</div><b>スタイルとスタッフを入力</b><small>「うちの子に合うか」を保護者が見る欄です</small></a>
      <a class="rg-nc hot" href="club-mypage-preview.html?tab=plan"><div class="n">03</div><b>スタンダードで上位に</b><small>写真7枚・検索で上位表示・編集部おすすめ枠・閲覧数。<em>¥3,000/月</em></small><span class="go">プランを見る ›</span></a>
    </div>
    <div class="row"><a class="pri" href="club-mypage-preview.html">マイページへ ›</a><a href="video-hero-preview.html">フリーのまま、トップに戻る</a></div>
  </div>
  <div style="height:40px"></div>
</div></main>
'''%dict(
 card=preview_card,
 s1=sec('1','アカウント','承認後にマイページで編集するためのものです','30 SEC',
   f('メールアドレス',inp('','coach@example.com',typ='email'),req=True,hint='ログインと、運営からの連絡に使います')+
   f('パスワード','<div class="rg-row">'+inp('','8文字以上',typ='password')+inp('','もう一度',typ='password')+'</div>',req=True)),
 s2=sec('2','クラブの基本','検索とクラブページに出る内容です','1 MIN',
   f('クラブ名',inp('','例：わかばFC'),req=True)+
   f('種目','<div class="rg-row">'+inp('','例：サッカー・ダンス・体操（選ぶか入力）')+'</div>',req=True,hint='一覧にない種目は、そのまま入力して構いません')+
   f('住所','<div class="rg-row"><input class="rg-in sm" placeholder="郵便番号" style="max-width:130px"><span class="rg-chk" style="padding:8px 10px">郵便番号から入力</span></div><div class="rg-row" style="margin-top:6px">'+inp('','都道府県',cls='sm')+inp('','市区町村',cls='sm')+'</div><div class="rg-row" style="margin-top:6px">'+inp('','町名・番地（例：砧公園1-1）')+inp('','会場名（例：砧公園グラウンド）')+'</div>',req=True,hint='検索の「地域」と地図のピンは、この住所から自動で決まります。会場が複数あるときは主な場所を')+
   f('対象年齢',chks(['未就学（〜6歳）','小学生','中学生']),req=True)+
   f('活動曜日',chks(['月','火','水','木','金','土','日']))+
   f('月謝','<div class="rg-row">'+inp('','3000',cls='sm')+'<span class="hint" style="display:inline">円／月 ・ コースで違うときは一番安い額を</span></div>',req=True)+
   f('体験',chks(['受付中','要相談'],on=('受付中',))+'<div class="rg-row" style="margin-top:8px">'+inp('','体験の費用（例：無料）',cls='sm')+'</div>')+
   f('紹介文','<textarea class="rg-in" placeholder="例：はじめてボールを触る子が半分。学年ごとにコースを分けているので、経験がなくても大丈夫です。土曜の見学はいつでも。"></textarea><div class="rg-cnt">0 / 400</div>',req=True,hint='最初の2行がカードに出ます。「はじめての子の割合」「見学できるか」「コーチは誰か」が保護者に効きます')+
   f('写真','<div class="rg-drop"><b>写真を1枚選ぶ</b><small>JPG・PNG・5MBまで。スマホの写真で構いません。あとで増やせます</small></div>',opt=True)+
   f('申込の通知先',inp('','team@example.com',typ='email'),hint='体験申込が届くメール。空ならアカウントのメールに届きます')+
   '<details class="rg-more"><summary>SNS・ホームページ・初期費用（あとからでも）</summary><div class="in2">'+f('Instagram',inp('','ユーザー名（@なし）'),opt=True)+f('X',inp('','ユーザー名（@なし）'),opt=True)+f('ホームページ',inp('','https://…'),opt=True)+f('LINE公式',inp('','https://lin.ee/…'),opt=True)+f('初期費用の目安','<div class="rg-row">'+inp('','0',cls='sm')+'<span class="hint" style="display:inline">円 ・ 0なら「入会金なし」で検索に出ます</span></div>',opt=True)+'</div></details>'),
 s3=sec('3','確認して送信','送信後、運営の確認を経て掲載されます','10 SEC',
   '<div class="rg-agree"><input type="checkbox" checked><span><a href="#">利用規約</a>と<a href="#">プライバシーポリシー</a>に同意します。掲載内容は運営が確認し、内容によっては修正をお願いすることがあります。</span></div>'+
   '<div class="rg-submit"><small>掲載は無料です。送信後、最短で当日に載ります。<br>スタイル・スタッフ・写真の追加は、承認後にマイページから。</small><a href="?done=1">この内容で申請する ›</a></div>'))
rg_js='''<script>
(function(){
 if(/done=1/.test(location.search)){document.body.classList.add('done');window.scrollTo(0,0)}
 document.addEventListener('click',function(e){var c=e.target.closest('.rg-chk');if(c){setTimeout(function(){var i=c.querySelector('input');if(i)c.classList.toggle('on',i.checked)},0)}});
 var ta=document.querySelector('textarea.rg-in'),cnt=document.querySelector('.rg-cnt');if(ta&&cnt)ta.addEventListener('input',function(){cnt.textContent=ta.value.length+' / 400'});
})();
</script>'''
page('register-preview.html','クラブを載せる（登録）｜チビスポ（プレビュー）',rg_body,rg_css,extra_js=rg_js)
