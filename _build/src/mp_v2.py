# ---- マイページ（プレビュー v3・2026-09-12）：上にアカウント、下はタブで分ける。スイッチは ON/OFF が読める形
mp_css='''
/* ===== 上：アカウントの帯 ===== */
.mp-head{display:grid;grid-template-columns:1fr;gap:14px;align-items:center;padding:26px 0 18px;border-bottom:2px solid var(--ink)}
.mp-who{display:flex;gap:14px;align-items:center;min-width:0}
.mp-av{width:56px;height:56px;border-radius:50%;background:var(--accent);color:#fff;font-family:var(--fh);font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none}
.mp-who .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:3px}
.mp-who h1{font-family:var(--fh);margin:0;font-size:clamp(20px,5vw,26px);font-weight:900;line-height:1.2;letter-spacing:-.01em}
.mp-who h1 small{font-size:12px;font-weight:700;color:var(--sub);margin-left:8px;letter-spacing:0}
.mp-who p{margin:4px 0 0;font-size:12px;font-weight:700;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mp-act{display:flex;gap:8px;flex-wrap:wrap}
.mp-act a{font-size:12.5px;font-weight:900;padding:10px 14px;border:1.5px solid var(--ink);color:var(--ink);white-space:nowrap}
.mp-act a.pri{background:var(--ink);color:var(--bg)}
/* ===== タブ ===== */
.mp-tabs{position:sticky;top:56px;z-index:20;background:var(--bg);display:flex;gap:0;border-bottom:1px solid var(--ink);margin:0 -20px;padding:0 20px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.mp-tabs::-webkit-scrollbar{display:none}
.mp-tabs button{flex:none;background:transparent;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:14px 14px 12px;font-family:var(--fh);font-size:13.5px;font-weight:900;color:var(--sub);cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.mp-tabs button i{font-style:normal;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.04em;background:var(--accent);color:#fff;padding:2px 6px;border-radius:999px;min-width:20px;text-align:center}
.mp-tabs button i.off{background:var(--line);color:var(--sub)}
.mp-tabs button.on{color:var(--ink);border-bottom-color:var(--ink)}
.mp-tabs button:hover{color:var(--ink)}
/* ===== パネル ===== */
.mp-panel{display:none;padding:26px 0 0;max-width:880px}
.mp-panel.on{display:block;animation:mpIn .3s}
@keyframes mpIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.mp-panel h2{font-family:var(--fh);margin:0 0 4px;font-size:clamp(19px,4.6vw,24px);font-weight:900;line-height:1.3;letter-spacing:-.01em;border:0;padding:0}
.mp-panel h2 em{font-style:normal;color:var(--accent)}
.mp-panel .lead{margin:0 0 18px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.mp-panel h3{font-family:var(--fh);margin:28px 0 10px;font-size:15px;font-weight:900;padding-bottom:8px;border-bottom:1px solid var(--line)}
/* ホーム：状況カード */
.mp-home{display:grid;grid-template-columns:1fr;gap:10px}
.mp-hc{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;border:1px solid var(--ink);background:var(--card);padding:16px 16px;color:var(--ink);transition:transform .15s,box-shadow .15s}
.mp-hc:hover{transform:translateY(-2px);box-shadow:6px 6px 0 var(--ink)}
.mp-hc .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.22em;color:var(--accent);margin-bottom:5px}
.mp-hc b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;line-height:1.35}
.mp-hc small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:3px;line-height:1.6}
.mp-hc .go{width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--bg);font-family:'Anton',sans-serif;font-size:16px;display:flex;align-items:center;justify-content:center}
.mp-hc.hot{border:2px solid var(--accent)}.mp-hc.hot .go{background:var(--accent);color:#fff}
/* 診断の結果 */
.saved{border:1px solid var(--ink);padding:18px 16px 16px;position:relative;background:var(--card)}
body[data-skin="bright"] .saved,body[data-skin="stadium"] .saved{border-radius:var(--r)}
.saved .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:6px}
.saved .tp{font-family:var(--fh);font-size:clamp(19px,5vw,24px);font-weight:900;line-height:1.3;margin:0 0 10px;padding-right:90px}
.saved .tp em{font-style:normal;color:var(--accent)}
.saved .cond{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.saved .cond span{border:1px solid var(--ink);padding:5px 10px;font-size:11.5px;font-weight:900}
.saved .sp{font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.saved .sp b{color:var(--ink)}
.saved .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
.saved .row a{font-size:12.5px;font-weight:900;padding:9px 12px;border:1.5px solid var(--ink)}
.saved .row a.pri{background:var(--accent);border-color:var(--accent);color:#fff}
.saved .date{position:absolute;right:16px;top:16px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.16em;color:var(--sub)}
.empty2{border:1.5px dashed var(--line);padding:24px 18px;text-align:center}
.empty2 .t{font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:6px}
.empty2 p{margin:0 0 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
/* お知らせ：ON/OFF が読めるスイッチ */
.ntf{display:grid;gap:10px}
.ntf label{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:center;padding:14px 16px;border:1px solid var(--ink);background:var(--card);cursor:pointer;transition:background .15s}
.ntf label:has(input:checked){background:color-mix(in srgb,var(--accent) 5%,var(--card))}
.ntf label .t{font-size:13.5px;font-weight:900}
.ntf label .s{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7;margin-top:3px}
.ntf input{position:absolute;opacity:0;width:0;height:0}
.mp-sw{position:relative;width:64px;height:32px;border-radius:999px;background:#c9c5bb;flex:none;transition:background .2s;box-shadow:inset 0 1px 3px rgba(0,0,0,.2)}
.mp-sw::before{content:"OFF";position:absolute;right:9px;top:50%;transform:translateY(-50%);font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.08em;color:#fff}
.mp-sw::after{content:"";position:absolute;left:3px;top:3px;width:26px;height:26px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.3);transition:left .2s}
.ntf input:checked+.mp-sw{background:#1f9d55}
.ntf input:checked+.mp-sw::before{content:"ON";right:auto;left:11px}
.ntf input:checked+.mp-sw::after{left:35px}
.ntf .how{margin-top:14px;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.8}
.ntf-ch{display:grid;grid-template-columns:1fr;gap:8px;margin-top:8px}
.ntf-ch label{padding:12px 14px}
/* お気に入り・保存した検索 */
.favs.news{grid-template-columns:repeat(2,1fr)}
.msg{border-top:2px solid var(--ink)}
.msg .m{display:grid;grid-template-columns:1fr auto;gap:12px;padding:14px 0;border-bottom:1px solid var(--line);align-items:center}
.msg .m .n{font-family:var(--fh);font-size:14px;font-weight:900}
.msg .m .s{font-size:12px;font-weight:700;color:var(--sub);margin-top:3px;line-height:1.7}
.msg .m .st{font-size:11px;font-weight:900;letter-spacing:.06em;color:var(--accent);white-space:nowrap;border:1px solid var(--accent);padding:4px 8px}
.msg .m .st.dim{color:var(--sub);border-color:var(--line)}
.msg .m .st.new{background:var(--accent);color:#fff}
/* アカウント */
.acc{display:grid;grid-template-columns:1fr;gap:0;border:1px solid var(--ink);background:var(--card)}
.acc .r{display:grid;grid-template-columns:96px 1fr auto;gap:10px;align-items:center;padding:13px 16px;border-bottom:1px solid var(--line);font-size:13px;font-weight:700}
.acc .r:last-child{border-bottom:0}
.acc .r b{font-size:11px;letter-spacing:.06em;color:var(--sub)}
.acc .r a{font-size:12px;font-weight:900;text-decoration:underline;text-underline-offset:3px;white-space:nowrap}
.acc-danger{margin-top:18px;display:flex;gap:14px;flex-wrap:wrap;font-size:12px;font-weight:700}
.acc-danger a{color:var(--sub);text-decoration:underline;text-underline-offset:3px}
@media(min-width:760px){
  .mp-head{grid-template-columns:1fr auto;padding:34px 0 22px}
  .mp-av{width:64px;height:64px;font-size:26px}
  .mp-tabs{margin:0;padding:0;top:60px}
  .mp-tabs button{padding:16px 18px 14px;font-size:14px}
  .mp-home{grid-template-columns:1fr 1fr;gap:14px}
  .ntf-ch{grid-template-columns:1fr 1fr}
  .favs.news{grid-template-columns:repeat(3,1fr)}
}
'''
fav_cards="\n".join(cards.card(**dict(c,liked=True)) for c in [cards.CLUBS[0],cards.CLUBS[2],cards.CLUBS[5]])
mp_body='''
<main><div class="wrap">
  <div class="note">【マイページ v3（2026-09-12）】ユーザー「ON/OFFが分かりにくい／アカウントは分かりやすい位置に／1枚に集約されすぎて見にくい」→ ①上にアカウントの帯（アイコン・ニックネーム・地域・お子さん・「アカウント設定」ボタン）②その下は<b>タブ</b>で1画面1テーマ（ホーム／診断の結果／お知らせ／お気に入り／申込・メッセージ／アカウント）。ホームは「いま何があるか」の状況カード4枚だけ ③スイッチは<b>緑＝ON・灰＝OFF の文字入り</b>（行の下の「受け取る／受け取らない」は重複なので出さない）。`?tab=notify` のように直接開ける。保存されるのは v2 と同じ（タイプ＋条件＋種目3つ、localStorage `chibispo_quiz`）。</div>

  <div class="mp-head">
    <div class="mp-who"><div class="mp-av">は</div><div><div class="k">MY PAGE</div><h1>はなまま<small>さん</small></h1><p>東京都 世田谷区 ・ お子さん 小2 ・ you@example.com</p></div></div>
    <div class="mp-act"><a href="#" data-tab="account" class="pri">アカウント設定</a><a href="#" data-quiz>もう一度診断する</a></div>
  </div>

  <div class="mp-tabs" id="mpTabs">
    <button data-tab="home" class="on">ホーム</button>
    <button data-tab="result">診断の結果</button>
    <button data-tab="notify">お知らせ <i>2</i></button>
    <button data-tab="fav">お気に入り <i class="off">3</i></button>
    <button data-tab="msg">申込・メッセージ <i>1</i></button>
    <button data-tab="account">アカウント</button>
  </div>

  <section class="mp-panel on" data-tab="home">
    <h2>いま、<em>見るもの</em>。</h2>
    <p class="lead">新しい動きがあるものから並べています。</p>
    <div class="mp-home">
      <a class="mp-hc hot" href="#" data-tab="msg"><div><div class="k">MESSAGE</div><b>わかばFCから返信が届いています</b><small>体験申込 9/14（土）10:00</small></div><span class="go">›</span></a>
      <a class="mp-hc" href="#" data-tab="result"><div><div class="k">YOUR TYPE</div><b>お子さんに合いそうなのは、王道スポーツ</b><small>サッカー・バスケットボール・野球 ・ 2026.09.08</small></div><span class="go">›</span></a>
      <a class="mp-hc" href="#" data-tab="fav"><div><div class="k">FAVORITES</div><b>お気に入り 3クラブ</b><small>「世田谷区 × サッカー」に新着 2件</small></div><span class="go">›</span></a>
      <a class="mp-hc" href="#" data-tab="notify"><div><div class="k">NOTIFICATIONS</div><b>お知らせ 2つを受け取る設定</b><small>新しいクラブ・体験の募集</small></div><span class="go">›</span></a>
    </div>
  </section>

  <section class="mp-panel" data-tab="result">
    <h2>診断の<em>結果</em></h2>
    <p class="lead">保存した結果です。条件を変えるか、もう一度診断できます。</p>
    <div class="saved" id="mpSaved">
      <div class="date">2026.09.08</div>
      <div class="k">TYPE</div>
      <div class="tp">お子さんに合いそうなのは、<em>王道スポーツ</em>。</div>
      <div class="cond"><span>世田谷区</span><span>小学1〜3年</span><span>土日</span><span>まず体験したい</span><span>楽しむこと</span></div>
      <div class="sp">まず見てほしい種目：<b>サッカー</b>・<b>バスケットボール</b>・<b>野球</b></div>
      <div class="row"><a class="pri" href="search-preview.html">この条件でクラブを見る ›</a><a href="#" data-quiz>もう一度診断する</a><a href="#">条件を編集</a></div>
    </div>
    <div class="empty2" id="mpEmpty" hidden><div class="t">まだ診断の結果がありません。</div><p>1分の質問に答えると、合いそうな種目のタイプと近くのクラブが出ます。保存すると、条件に合うクラブが載ったときにお知らせします。</p><a class="btn" href="#" data-quiz>診断をはじめる（無料）</a></div>
  </section>

  <section class="mp-panel" data-tab="notify">
    <h2>お知らせの<em>設定</em></h2>
    <p class="lead">受け取るものだけ ON にしてください。いつでも変えられます。</p>
    <div class="ntf">
      <label><div><div class="t">条件に合う新しいクラブが載ったとき</div><div class="s">世田谷区・小学1〜3年・土日・体験OK に合うクラブが登録されたら</div></div><input type="checkbox" checked><span class="mp-sw"></span></label>
      <label><div><div class="t">保存した種目で、体験の募集が始まったとき</div><div class="s">サッカー・バスケットボール・野球の体験会・入団募集</div></div><input type="checkbox" checked><span class="mp-sw"></span></label>
      <label><div><div class="t">王道スポーツタイプ向けの記事</div><div class="s">週1本まで。マガジンの新着から</div></div><input type="checkbox"><span class="mp-sw"></span></label>
    </div>
    <h3>届け方</h3>
    <div class="ntf ntf-ch">
      <label><div><div class="t">アプリのプッシュ通知</div></div><input type="checkbox" checked><span class="mp-sw"></span></label>
      <label><div><div class="t">メール</div></div><input type="checkbox" checked><span class="mp-sw"></span></label>
    </div>
    <div class="ntf"><div class="how">通知は1日1回までにまとめて届きます。</div></div>
  </section>

  <section class="mp-panel" data-tab="fav">
    <h2>お気に入り<em>クラブ</em></h2>
    <p class="lead">♡ を押したクラブです。比べて、体験を申し込めます。</p>
    <div class="news favs">%s</div>
    <h3>保存した検索条件</h3>
    <div class="msg">
      <div class="m"><div><div class="n">世田谷区 × サッカー</div><div class="s">小学生 ・ 土日 ・ 体験OK</div></div><div class="st new">新着 2</div></div>
    </div>
  </section>

  <section class="mp-panel" data-tab="msg">
    <h2>体験申込と<em>メッセージ</em></h2>
    <p class="lead">クラブからの返信はここに届きます。</p>
    <div class="msg">
      <div class="m"><div><div class="n">わかばFC</div><div class="s">体験申込 9/14（土）10:00 ・ クラブから返信あり</div></div><div class="st new">返信あり</div></div>
      <div class="m"><div><div class="n">世田谷ジュニアテニス</div><div class="s">見学の希望を送信 ・ 返信待ち</div></div><div class="st dim">送信済み</div></div>
    </div>
  </section>

  <section class="mp-panel" data-tab="account">
    <h2>アカウント</h2>
    <p class="lead">お子さんの情報は、診断とお知らせの条件に使います。</p>
    <div class="acc">
      <div class="r"><b>ニックネーム</b><span>はなまま</span><a href="#">変更</a></div>
      <div class="r"><b>メール</b><span>you@example.com</span><a href="#">変更</a></div>
      <div class="r"><b>地域</b><span>東京都 世田谷区</span><a href="#">変更</a></div>
      <div class="r"><b>お子さん</b><span>小2 ・ 男の子</span><a href="#">変更</a></div>
      <div class="r"><b>パスワード</b><span>••••••••</span><a href="#">変更</a></div>
    </div>
    <div class="acc-danger"><a href="#">ログアウト</a><a href="#">アカウントを削除</a></div>
  </section>

  <div style="height:40px"></div>
</div></main>
'''%fav_cards
mp_js='''<script>
(function(){
 var tabs=document.getElementById('mpTabs');
 function show(k){document.querySelectorAll('.mp-panel').forEach(function(p){p.classList.toggle('on',p.dataset.tab===k)});tabs.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.tab===k)});}
 tabs.addEventListener('click',function(e){var b=e.target.closest('button');if(b){show(b.dataset.tab);history.replaceState(null,'','?tab='+b.dataset.tab)}});
 document.addEventListener('click',function(e){var a=e.target.closest('a[data-tab]');if(a){e.preventDefault();show(a.dataset.tab);history.replaceState(null,'','?tab='+a.dataset.tab);window.scrollTo({top:tabs.getBoundingClientRect().top+scrollY-70,behavior:'smooth'})}});
 var m=location.search.match(/tab=(home|result|notify|fav|msg|account)/);if(m)show(m[1]);
 var s=null;try{s=JSON.parse(localStorage.getItem('chibispo_quiz')||'null')}catch(e){}
 var box=document.getElementById('mpSaved');if(!s||!box)return;
 box.querySelector('.tp').innerHTML='お子さんに合いそうなのは、<em>'+s.typeName+'</em>。';
 box.querySelector('.cond').innerHTML=s.cond.map(function(c){return '<span>'+c+'</span>'}).join('');
 box.querySelector('.sp').innerHTML='まず見てほしい種目：'+s.sports.map(function(x){return '<b>'+x+'</b>'}).join('・');
 var d=new Date(s.at);box.querySelector('.date').textContent=d.getFullYear()+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+('0'+d.getDate()).slice(-2);
 if(location.search.indexOf('saved=1')>=0){show('result');var n=document.createElement('div');n.style.cssText='margin:0 0 14px;padding:10px 14px;border:1px solid var(--accent);color:var(--accent);font-size:12.5px;font-weight:900';n.textContent='診断の結果を保存しました。条件に合うクラブが載ったらお知らせします。';box.parentNode.insertBefore(n,box)}
})();
</script>'''
page('mypage-preview.html','マイページ｜チビスポ（プレビュー）',mp_body,mp_css,extra_js=mp_js)
