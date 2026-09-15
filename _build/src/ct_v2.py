# ---- 相談する（お問い合わせ）ページ v2・2026-09-12：本番 contact.html（mailto だけ）を、相手別のフォームに
ct_css='''
.ct-head{padding:30px 0 18px;border-bottom:2px solid var(--ink)}
.ct-head .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:10px}
.ct-head .ey::before{content:"";width:22px;height:2px;background:var(--accent)}
.ct-head h1{font-family:var(--fh);margin:0 0 8px;font-size:clamp(24px,6vw,38px);font-weight:900;line-height:1.2;letter-spacing:-.01em}
.ct-head h1 em{font-style:normal;color:var(--accent)}
.ct-head p{margin:0;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.ct-lay{display:grid;grid-template-columns:1fr;gap:26px;margin-top:22px}
.ct-who{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}
.ct-who button{border:1.5px solid var(--ink);background:var(--card);color:var(--ink);font-family:var(--fh);font-weight:900;font-size:13px;padding:14px 10px;cursor:pointer;text-align:left;line-height:1.35;position:relative;transition:background .15s,color .15s}
.ct-who button small{display:block;font-family:var(--f);font-size:10.5px;font-weight:700;color:var(--sub);margin-top:2px}
.ct-who button.on{background:var(--ink);color:var(--bg)}
.ct-who button.on small{color:color-mix(in srgb,var(--bg) 70%,transparent)}
.ct-who button.on::after{content:"";position:absolute;left:50%;bottom:-8px;border-left:7px solid transparent;border-right:7px solid transparent;border-top:8px solid var(--ink);transform:translateX(-50%)}
.ct-box{border:1px solid var(--ink);background:var(--card);padding:18px 18px 20px}
.ct-p{display:none}.ct-p.on{display:block}
.ct-f{display:grid;gap:5px;margin-bottom:14px}
.ct-f>label{font-size:12px;font-weight:900;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.ct-f>label .req{font-size:9.5px;letter-spacing:.08em;background:var(--ink);color:var(--bg);padding:1px 5px}
.ct-f>label .opt{font-size:9.5px;letter-spacing:.08em;border:1px solid var(--line);color:var(--sub);padding:1px 5px}
.ct-f .hint{font-size:11px;font-weight:700;color:var(--sub);line-height:1.6}
.ct-in{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:14px;font-weight:700;padding:11px 12px;color:var(--ink);box-sizing:border-box}
textarea.ct-in{min-height:120px;resize:vertical}
.ct-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.ct-chips{display:flex;gap:6px;flex-wrap:wrap}
.ct-chips span{font-size:12px;font-weight:900;border:1px solid var(--ink);padding:8px 11px;background:#fff;cursor:pointer}
.ct-chips span.on{background:var(--accent);border-color:var(--accent);color:#fff}
.ct-chips span.dim{border-color:var(--line);color:var(--sub)}
.ct-note{border-left:3px solid var(--accent);padding:10px 12px;font-size:12px;font-weight:700;color:var(--sub);line-height:1.7;margin-bottom:14px;background:color-mix(in srgb,var(--accent) 5%,var(--card))}
.ct-note a{font-weight:900;color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.ct-btn{display:block;width:100%;text-align:center;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px;margin-top:6px;box-shadow:0 8px 24px rgba(232,69,95,.3)}
.ct-err{margin-top:10px;border:1px solid var(--accent);color:var(--accent);font-size:12.5px;font-weight:900;padding:9px 12px}
.ct-sum{margin:0 0 14px;border:1px solid var(--line);background:#fff}
.ct-sum div{display:grid;grid-template-columns:110px 1fr;gap:10px;padding:8px 12px;border-bottom:1px solid var(--line);font-size:12.5px;font-weight:700}
.ct-sum div:last-child{border-bottom:0}
.ct-sum b{color:var(--sub);font-size:11px;letter-spacing:.06em}
.ct-sum .st{font-size:11px;font-weight:900;color:var(--sub);padding:6px 12px;background:color-mix(in srgb,var(--ink) 4%,#fff)}
.ct-agree{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7;margin-top:10px}
.ct-agree a{font-weight:900;color:var(--ink);text-decoration:underline;text-underline-offset:3px}
/* 右 */
.ct-side{display:grid;gap:14px;align-content:start}
.ct-card{border:1px solid var(--ink);background:var(--card);padding:16px}
.ct-card .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.ct-card b{display:block;font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:6px}
.ct-card p{margin:0;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.ct-card .st{display:grid;gap:8px;margin-top:6px}
.ct-card .st div{position:relative;padding-left:28px;font-size:12.5px;font-weight:700;line-height:1.6}
.ct-card .st div::before{content:attr(data-n);position:absolute;left:0;top:0;font-family:'Anton',sans-serif;font-size:13px;color:var(--accent)}
.ct-card .st div small{display:block;font-size:11px;color:var(--sub)}
.ct-per{display:grid;grid-template-columns:48px 1fr;gap:12px;align-items:center}
.ct-per img{width:48px;height:48px;border-radius:50%;object-fit:cover;object-position:top}
.ct-per b{margin-bottom:2px}
.ct-per small{font-size:11px;font-weight:700;color:var(--sub);line-height:1.5}
.ct-links{display:grid;gap:0;border-top:2px solid var(--ink)}
.ct-links a{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:11px 0;border-bottom:1px solid var(--line);font-size:13px;font-weight:900;color:var(--ink)}
.ct-links a span{min-width:0}
.ct-links a small{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:2px}
.ct-links a i{font-style:normal;font-family:'Anton',sans-serif;color:var(--accent);font-size:16px}
.ct-faq details{border-bottom:1px solid var(--line)}
.ct-faq summary{list-style:none;cursor:pointer;padding:10px 0;font-size:12.5px;font-weight:900;display:flex;justify-content:space-between;gap:8px}
.ct-faq summary::-webkit-details-marker{display:none}
.ct-faq summary::after{content:"+";font-family:'Anton',sans-serif;color:var(--accent)}
.ct-faq details[open] summary::after{content:"–"}
.ct-faq .a{padding:0 0 10px;font-size:12px;font-weight:700;color:var(--sub);line-height:1.7}
/* 完了 */
.ct-done{display:none;border:2px solid var(--ink);background:var(--card);padding:26px 20px 22px;margin-top:22px;max-width:760px}
.ct-done .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.ct-done h2{font-family:var(--fh);margin:0 0 8px;font-size:22px;font-weight:900;border:0;padding:0}
.ct-done p{margin:0 0 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.ct-done .row{display:flex;gap:8px;flex-wrap:wrap}
.ct-done .row a{font-size:13px;font-weight:900;padding:11px 16px;border:1.5px solid var(--ink)}
.ct-done .row a.pri{background:var(--ink);color:var(--bg)}
body.done .ct-lay{display:none}body.done .ct-done{display:block}
@media(min-width:900px){
  .ct-lay{grid-template-columns:1fr 340px;gap:40px;margin-top:30px}
  .ct-side{position:sticky;top:80px}
  .ct-who{grid-template-columns:repeat(4,1fr)}
  .ct-box{padding:22px 24px 24px}
  .ct-head{padding:40px 0 22px}
}
'''
A='assets/preview-video/'
def f(label,body,req=False,opt=False,hint=''):
    return '<div class="ct-f"><label>%s%s%s</label><div>%s</div>%s</div>'%(label,' <span class="req">必須</span>' if req else '',' <span class="opt">任意</span>' if opt else '',body,('<div class="hint">%s</div>'%hint) if hint else '')
def inp(ph='',typ='text',v='',k=''): return '<input class="ct-in" type="%s" placeholder="%s" value="%s" data-k="%s">'%(typ,ph,v,k)
def chips(opts,on=None,dim=(),k='topic'): return '<div class="ct-chips" data-k="%s">'%k+''.join('<span class="%s">%s</span>'%(('on' if o==on else '')+(' dim' if o in dim else ''),o) for o in opts)+'</div>'
common_tail=f('お名前',inp('例：山田 花子',k='name'),req=True)+f('メールアドレス',inp('you@example.com','email',k='email'),req=True,hint='返信はこのメールに届きます')+f('電話番号',inp('090-…','tel',k='phone'),opt=True,hint='オンラインや電話での相談を希望する方だけ')
club=(
 '<div class="ct-note">体験申込への返信やクラブ情報の編集は、<a href="club-mypage-preview.html">クラブのマイページ</a>からできます。ここは運営への相談用です。</div>'+
 f('相談したいこと',chips(['掲載について','SNS運用サポート','ホームページ制作','撮影・動画制作（準備中）','有料プランの変更','情報の修正','その他'],on='SNS運用サポート',dim=('撮影・動画制作（準備中）',)),req=True,hint='当てはまるものを1つ。複数あれば内容に書いてください')+
 f('クラブ名',inp('例：わかばFC',k='org'),req=True)+common_tail+
 f('内容','<textarea class="ct-in" data-k="message" placeholder="例：Instagramを始めたいが、何から手をつければいいか分からない。体験会が10月にある。"></textarea>',req=True,hint='困っていること・時期・いまの状況を、そのまま書いてください')+
 f('相談の形',chips(['メールで返信','オンラインで30分（無料）','電話'],on='オンラインで30分（無料）',k='how'),hint='オンラインは平日夜・土日も相談できます')+
 f('都合のいい時間帯',inp('例：平日 20時以降、土曜午前',k='time'),opt=True))
biz=(
 '<div class="ct-note">地域の広告掲載の内容と料金は <a href="service-ads-preview.html">広告掲載のページ</a> にまとめています。申込もそのページからできます。</div>'+
 f('相談したいこと',chips(['広告掲載について','掲載枠の空き（地域）','取材・記事について','請求書・支払い','その他'],on='広告掲載について'),req=True)+
 f('お店・会社名',inp('例：みどり整骨院',k='org'),req=True)+f('業種と地域','<div class="ct-row">'+inp('例：整骨院',k='industry')+inp('例：世田谷区',k='area')+'</div>',req=True,hint='同業は市区町村ごとに少数に限定しているので、先に空きを確認します')+
 common_tail+f('内容','<textarea class="ct-in" data-k="message" placeholder="例：クラブに通う子の保護者に、けがの相談先として知ってもらいたい。"></textarea>',req=True)+
 f('相談の形',chips(['メールで返信','オンラインで30分（無料）','電話'],on='メールで返信',k='how')))
parent=(
 '<div class="ct-note">クラブへの体験申込や質問は、<a href="club-preview.html">クラブのページ</a>から直接送れます。返信は <a href="mypage-preview.html">マイページ</a> とアプリに届きます。ここは運営への相談用です。</div>'+
 f('相談したいこと',chips(['使い方がわからない','クラブの情報が違う','クラブから返信がない','アカウント・退会','アプリの不具合','その他'],on='使い方がわからない'),req=True)+
 f('関係するクラブ',inp('例：わかばFC',k='org'),opt=True)+common_tail+
 f('内容','<textarea class="ct-in" data-k="message" placeholder="例：9/10に体験を申し込んだが、まだ返信がない。"></textarea>',req=True,hint='日付やクラブ名があると早く対応できます'))
other=(
 f('相談したいこと',chips(['取材・メディア','提携・協業','自治体・学校','採用','その他'],on='提携・協業'),req=True)+
 f('会社・団体名',inp('例：○○株式会社',k='org'),opt=True)+common_tail+
 f('内容','<textarea class="ct-in" data-k="message" placeholder="内容をお書きください"></textarea>',req=True))
ct_body='''
<main><div class="wrap">
  <div class="note">【相談する（お問い合わせ）v2（2026-09-12）】本番 contact.html は info@chibispo.com への mailto だけ。新デザインでは<b>相手別のフォーム</b>に：上で「クラブ運営者／地域のお店・企業／保護者／その他・取材」を選ぶと項目が変わる（`?who=club|biz|parent|other`）。クラブ＝相談したいこと（掲載・SNS・HP・撮影（準備中）・プラン・修正）＋相談の形（メール／オンライン30分無料／電話）＋都合のいい時間帯。お店＝業種と地域（枠の空き確認）。保護者＝クラブへの申込はクラブページから、と最初に案内してから運営向けの相談内容。右＝返信の目安・担当・よくある質問・ほかの窓口。送信先＝<b>inquiries</b>（kind=consult／plan=「相手 / 相談したいこと」／org=クラブ名・店名／message=内容＋相談の形＋時間帯＋業種・地域）＋ info@chibispo.com への通知メール。★プレビューでも本当に送る：Supabase REST に POST → 表が無い・失敗のときは端末（localStorage `chibispo_inquiries`）に保存して、完了画面に<b>送った内容</b>を表示（選んだチップが入っているかここで確認できる）。`?done=1` で完了画面。各LPの「相談する」「まず相談する」はここへ。</div>

  <div class="ct-head"><div class="ey">CONTACT ・ FREE</div><h1>決めるのは、<em>話してから</em>で大丈夫です。</h1><p>何が必要か分からない状態でも構いません。いまの状況をうかがってから、必要なものだけ提案します。相談は無料です。</p></div>

  <div class="ct-lay">
  <div>
    <div class="ct-who" id="ctWho">
      <button data-who="club" class="on">クラブ運営者<small>掲載・SNS・HP・プラン</small></button>
      <button data-who="biz">地域のお店・企業<small>広告掲載・取材</small></button>
      <button data-who="parent">保護者<small>使い方・情報の間違い</small></button>
      <button data-who="other">その他・取材<small>提携・自治体・採用</small></button>
    </div>
    <div class="ct-box">
      <div class="ct-p on" data-who="club">%(club)s</div>
      <div class="ct-p" data-who="biz">%(biz)s</div>
      <div class="ct-p" data-who="parent">%(parent)s</div>
      <div class="ct-p" data-who="other">%(other)s</div>
      <a class="ct-btn" href="#" id="ctSend">この内容で送る ›</a><div class="ct-err" id="ctErr" hidden></div>
      <div class="ct-agree">送信すると <a href="#">プライバシーポリシー</a> に同意したことになります。内容は相談の返信にだけ使います。</div>
    </div>
  </div>
  <aside class="ct-side">
    <div class="ct-card"><div class="k">REPLY</div><b>返信の目安</b><div class="st"><div data-n="1">2営業日以内にメールで返信<small>平日 9:00〜18:00 に確認しています</small></div><div data-n="2">オンライン相談は日程を3つ提案<small>30分・無料・Google Meet</small></div><div data-n="3">必要なものだけ提案<small>要らないものは勧めません</small></div></div></div>
    <div class="ct-card"><div class="k">FAQ</div><div class="ct-faq">
      <details><summary>相談だけでも大丈夫ですか</summary><div class="a">大丈夫です。話したうえで「いまは載せるだけでいい」となることも多いです。</div></details>
      <details><summary>オンライン相談は何を話しますか</summary><div class="a">いまの状況（掲載の有無・SNS・体験申込の数）を聞いて、順路を一緒に決めます。資料は不要です。</div></details>
      <details><summary>体験申込の返信はここからできますか</summary><div class="a">クラブのマイページからお願いします。ここは運営への相談用です。</div></details>
    </div></div>
    <div class="ct-card"><div class="k">OTHER WAYS</div><div class="ct-links">
      <a href="club-mypage-preview.html"><span>クラブのマイページ<small>体験申込の返信・情報の編集</small></span><i>›</i></a>
      <a href="mypage-preview.html"><span>保護者のマイページ<small>申込の状況・クラブからの返信</small></span><i>›</i></a>
      <a href="mailto:info@chibispo.com"><span>メールで送る<small>info@chibispo.com</small></span><i>›</i></a>
    </div></div>
  </aside>
  </div>

  <div class="ct-done"><div class="k">RECEIVED</div><h2>相談を受け付けました。</h2><div class="ct-sum" id="ctSum"></div><p>2営業日以内に、入力いただいたメールへ返信します。オンライン相談を希望された方には、日程を3つ提案します。<br>確認メールが届かないときは、迷惑メールフォルダをご確認ください。</p><div class="row"><a class="pri" href="video-hero-preview.html">トップに戻る</a><a href="partner-preview.html">クラブ・事業者向けのページ</a></div></div>
  <div style="height:40px"></div>
</div></main>
'''%dict(A=A,club=club,biz=biz,parent=parent,other=other)
ct_js=r'''<script>
(function(){
 var SB='https://emkpkomrgknzrmxqbrvx.supabase.co',ANON='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ';
 var who=document.getElementById('ctWho');
 var WHO={club:'クラブ運営者',biz:'地域のお店・企業',parent:'保護者',other:'その他・取材'};
 function cur(){var b=who.querySelector('button.on');return b?b.dataset.who:'club'}
 function show(k){document.querySelectorAll('.ct-p').forEach(function(p){p.classList.toggle('on',p.dataset.who===k)});who.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.who===k)})}
 who.addEventListener('click',function(e){var b=e.target.closest('button');if(b){show(b.dataset.who);history.replaceState(null,'','?who='+b.dataset.who)}});
 document.addEventListener('click',function(e){var c=e.target.closest('.ct-chips span');if(c&&!c.classList.contains('dim')){c.parentNode.querySelectorAll('span').forEach(function(x){x.classList.toggle('on',x===c)})}});
 var m=location.search.match(/who=(club|biz|parent|other)/);if(m)show(m[1]);
 function collect(){
   var p=document.querySelector('.ct-p.on'),d={who:cur(),whoLabel:WHO[cur()]};
   p.querySelectorAll('[data-k]').forEach(function(el){var k=el.dataset.k;if(el.classList.contains('ct-chips')){var on=el.querySelector('span.on');d[k]=on?on.textContent.trim():''}else{d[k]=el.value.trim()}});
   return d;
 }
 function validate(d){
   if(!d.topic)return '「相談したいこと」を選んでください';
   var p=document.querySelector('.ct-p.on');
   var missing=[];p.querySelectorAll('.ct-f').forEach(function(f){if(!f.querySelector('.req'))return;var el=f.querySelector('[data-k]');if(!el||el.classList.contains('ct-chips'))return;if(!el.value.trim())missing.push(f.querySelector('label').firstChild.textContent.trim())});
   if(missing.length)return '未入力：'+missing.join('・');
   if(d.email&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email))return 'メールアドレスの形式を確認してください';
   return '';
 }
 function payload(d){
   var msg=[d.message];
   if(d.how)msg.push('相談の形：'+d.how);
   if(d.time)msg.push('都合のいい時間帯：'+d.time);
   if(d.industry||d.area)msg.push('業種・地域：'+[d.industry,d.area].filter(Boolean).join(' / '));
   return {kind:'consult',name:d.name||null,org:d.org||null,email:d.email,phone:d.phone||null,plan:d.whoLabel+' / '+d.topic,message:msg.join('\n')};
 }
 function done(d,pl,saved){
   var sum=document.getElementById('ctSum');
   var rows=[['相手',d.whoLabel],['相談したいこと',d.topic],['クラブ・会社名',d.org||'—'],['お名前',d.name],['メール',d.email],['電話',d.phone||'—'],['内容',pl.message.replace(/\n/g,' ／ ')]];
   sum.innerHTML='<div class="st">送った内容</div>'+rows.map(function(r){return '<div><b>'+r[0]+'</b><span>'+r[1]+'</span></div>'}).join('');
   document.body.classList.add('done');window.scrollTo(0,0);history.replaceState(null,'','?done=1');
 }
 document.getElementById('ctSend').addEventListener('click',function(e){
   e.preventDefault();var d=collect(),err=validate(d),eb=document.getElementById('ctErr');
   if(err){eb.textContent=err;eb.hidden=false;return}eb.hidden=true;
   var pl=payload(d);
   fetch(SB+'/rest/v1/inquiries',{method:'POST',headers:{'apikey':ANON,'Authorization':'Bearer '+ANON,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify(pl)})
     .then(function(r){if(r.status!==201)throw new Error(r.status);
       /* 運営に知らせる。失敗しても申込は保存済みなので画面は進める */
       fetch(SB+'/functions/v1/notify-inquiry',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+ANON},
         body:JSON.stringify({type:'inquiry',kind:pl.kind,who:d.who,topic:d.topic,name:pl.name,org:pl.org,email:pl.email,phone:pl.phone,message:pl.message})}).catch(function(){});
       done(d,pl,'db')})
     .catch(function(){try{var a=JSON.parse(localStorage.getItem('chibispo_inquiries')||'[]');a.push(Object.assign({at:new Date().toISOString()},pl));localStorage.setItem('chibispo_inquiries',JSON.stringify(a))}catch(e){}done(d,pl,'local')});
 });
 if(/done=1/.test(location.search)&&!document.getElementById('ctSum').innerHTML){document.body.classList.add('done')}
})();
</script>'''
page('contact-preview.html','相談する｜チビスポ（プレビュー）',ct_body,ct_css,extra_js=ct_js)
