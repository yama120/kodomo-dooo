(function(){
  var SB='https://emkpkomrgknzrmxqbrvx.supabase.co', FN=SB+'/functions/v1';
  /* Payment Link（club-mypage の STRIPE_LINKS と同じ4本）。年額は -y。Webhook は定価で pr / pr-plus を判定する */
  var STRIPE_LINKS={ pr:'https://buy.stripe.com/cNi00j5SJ2dK6wG66V00000', 'pr-y':'https://buy.stripe.com/7sY8wP1Ct2dKbR0eDr00001', 'pr-plus':'https://buy.stripe.com/5kQ5kDftj2dK4oy8f300004', 'pr-plus-y':'https://buy.stripe.com/14AbJ1bd3aKg1cm1QF00005' };
  var PLAN_LABEL={ free:'フリー', pr:'スタンダード（月額 ¥3,000）', 'pr-y':'スタンダード（年額 ¥30,000）', 'pr-plus':'プロ（月額 ¥10,000）', 'pr-plus-y':'プロ（年額 ¥100,000）' };
  function $(id){ return document.getElementById(id); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  if(!window.supabase){ return; }
  var db=supabase.createClient(SB,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ');
  var q=new URLSearchParams(location.search), planKey=(q.get('plan')&&PLAN_LABEL[q.get('plan')])?q.get('plan'):'free';
  if(planKey!=='free'){ var hs=$('rg-hero-sub'); if(hs) hs.textContent=PLAN_LABEL[planKey]+' で申し込みます。登録内容を送ったあと、そのままお支払い手続きに進みます。初回30日は無料です。';
    $('rg-submit').textContent='申請してお支払いに進む ›'; $('rg-submit-note').innerHTML=PLAN_LABEL[planKey]+' で申請します。送信後、お支払い手続きに進みます。<br>スタイル・スタッフ・写真の追加は、承認後にマイページから。'; }
  /* ---- 種目 ---- */
  var SPORTS=['サッカー','野球','バスケットボール','バレーボール','テニス','卓球','水泳','体操','ダンス','チアダンス','空手','剣道','柔道','テコンドー','レスリング','陸上','バトントワーリング','ダブルダッチ','マルチスポーツ','ブラジリアン柔術','スキー','スノーボード','サーフィン','カヌー','和太鼓','運動教室'];
  var sportSel=$('sport'), sportOther=$('sportOther');
  sportSel.innerHTML='<option value="">選択してください</option>'+SPORTS.map(function(s){ return '<option>'+s+'</option>'; }).join('')+'<option value="その他">その他（入力する）</option>';
  sportSel.addEventListener('change',function(){ var o=(this.value==='その他'); sportOther.hidden=!o; if(!o) sportOther.value=''; preview(); });
  /* ---- 地域 ---- */
  var prefSel=$('pref'), citySel=$('city'), cityOther=$('cityOther');
  if(typeof CITIES!=='undefined') prefSel.innerHTML='<option value="">都道府県</option>'+Object.keys(CITIES).map(function(p){ return '<option>'+p+'</option>'; }).join('');
  function fillCities(keep){ cityOther.hidden=true; if(!keep) cityOther.value='';
    if(!prefSel.value){ citySel.innerHTML='<option value="">市区町村</option>'; citySel.disabled=true; return; }
    var cs=(typeof CITIES!=='undefined'&&CITIES[prefSel.value])?CITIES[prefSel.value]:[];
    citySel.innerHTML='<option value="">選択してください</option>'+cs.map(function(c){ return '<option>'+c+'</option>'; }).join('')+'<option value="その他">その他（入力する）</option>'; citySel.disabled=false; }
  prefSel.addEventListener('change',function(){ fillCities(); preview(); });
  citySel.addEventListener('change',function(){ var o=(this.value==='その他'); cityOther.hidden=!o; if(!o) cityOther.value=''; preview(); });
  fillCities();
  /* 郵便番号 → 住所（zipcloud） */
  $('zipBtn').addEventListener('click',function(){ var z=($('postal').value||'').replace(/[^0-9]/g,''); if(z.length!==7){ err('郵便番号は7桁の数字で入力してください。'); return; }
    fetch('https://zipcloud.ibsnet.co.jp/api/search?zipcode='+z).then(function(r){ return r.json(); }).then(function(j){ var r=j&&j.results&&j.results[0]; if(!r){ err('郵便番号に該当する住所が見つかりませんでした。'); return; }
      clearErr(); prefSel.value=r.address1; fillCities(); var opt=[].slice.call(citySel.options).some(function(o){ return o.value===r.address2; });
      if(opt) citySel.value=r.address2; else { citySel.value='その他'; cityOther.hidden=false; cityOther.value=r.address2; }
      if(!$('address1').value) $('address1').value=r.address3||''; preview(); }).catch(function(){ err('住所の取得に失敗しました。手で入力してください。'); }); });
  /* ---- チェック・ラジオの見た目 ---- */
  document.addEventListener('change',function(e){ var i=e.target; if(!(i.type==='checkbox'||i.type==='radio')) return; var name=i.name;
    if(i.type==='radio') document.querySelectorAll('input[name="'+name+'"]').forEach(function(x){ x.closest('.rg-chk').classList.toggle('on',x.checked); });
    else if(i.closest('.rg-chk')) i.closest('.rg-chk').classList.toggle('on',i.checked);
    if(name==='age'){ var pre=[].slice.call(document.querySelectorAll('input[name="age"]')).some(function(x){ return x.value==='未就学'&&x.checked; }); $('rg-amw').hidden=!pre; if(!pre) document.querySelectorAll('input[name="age_min"]').forEach(function(r){ r.checked=false; r.closest('.rg-chk').classList.remove('on'); }); }
    preview(); });
  var ta=$('description'), cnt=document.querySelector('.rg-cnt'); ta.addEventListener('input',function(){ cnt.textContent=ta.value.length+' / 400'; preview(); });
  ['name','address1','venue','feeNum','trialFee'].forEach(function(id){ $(id).addEventListener('input',preview); });
  /* ---- 写真（1枚・1200px・WebP） ---- */
  var photos=[]; var pInput=$('rg-photo-input');
  function resizeToDataURL(file,cb){ var img=new Image(), url=URL.createObjectURL(file);
    img.onload=function(){ var max=1200,w=img.width,h=img.height; if(w>max){ h=Math.round(h*max/w); w=max; } var c=document.createElement('canvas'); c.width=w; c.height=h; c.getContext('2d').drawImage(img,0,0,w,h); URL.revokeObjectURL(url);
      try{ var d=c.toDataURL('image/webp',0.82); if(d.indexOf('data:image/webp')!==0) d=c.toDataURL('image/jpeg',0.82); cb(d); }catch(e){ var r=new FileReader(); r.onload=function(ev){ cb(ev.target.result); }; r.readAsDataURL(file); } };
    img.onerror=function(){ URL.revokeObjectURL(url); var r=new FileReader(); r.onload=function(ev){ cb(ev.target.result); }; r.readAsDataURL(file); }; img.src=url; }
  function renderPhotos(){ $('rg-photos').innerHTML=photos.map(function(p,i){ return '<div class="p"><img src="'+p.src+'" alt=""><button type="button" data-rm="'+i+'" aria-label="削除">&times;</button></div>'; }).join('');
    $('rg-photos').querySelectorAll('[data-rm]').forEach(function(b){ b.addEventListener('click',function(){ photos.splice(+b.dataset.rm,1); renderPhotos(); preview(); }); }); }
  pInput.addEventListener('change',function(e){ var f=(e.target.files||[])[0]; if(!f) return; if(f.size>5*1024*1024){ err('5MB以下の画像を選んでください。'); return; } resizeToDataURL(f,function(src){ photos=[{src:src}]; renderPhotos(); preview(); }); pInput.value=''; });
  /* ---- プレビューのカード ---- */
  function formTeam(){ var sport=sportSel.value==='その他'?sportOther.value.trim():sportSel.value; var city=citySel.value==='その他'?cityOther.value.trim():citySel.value;
    var fee=parseInt($('feeNum').value,10); var tr=document.querySelector('input[name="trial"]:checked');
    return { id:'preview', name:$('name').value.trim()||'クラブ名', sport:sport||'種目', pref:prefSel.value, city:city, description:ta.value.trim(), photo_url:photos[0]?photos[0].src:'',
      age_groups:[].slice.call(document.querySelectorAll('input[name="age"]:checked')).map(function(x){ return x.value; }), days:[].slice.call(document.querySelectorAll('input[name="day"]:checked')).map(function(x){ return x.value; }),
      fee:isNaN(fee)?'':('月'+fee.toLocaleString()+'円'), trial:tr?tr.value==='true':false, girls_welcome:!!document.querySelector('input[name="feature"][value="女の子歓迎"]:checked'), female_instructor:!!document.querySelector('input[name="feature"][value="女性指導者あり"]:checked'), created_at:new Date().toISOString() }; }
  function preview(){ var c=$('rg-card'); if(!c||!window.ChibiCard) return; c.innerHTML=ChibiCard.card(formTeam()); c.querySelectorAll('a').forEach(function(a){ a.addEventListener('click',function(e){ e.preventDefault(); }); }); }
  preview();
  /* ---- 追加モード（ログイン中に別チームを追加） ---- */
  var isAddMode=false;
  (async function(){ if(q.get('add')!=='true') return; var s=await db.auth.getSession(); var ses=s&&s.data?s.data.session:null; if(!ses){ location.href='club-mypage.html'; return; }
    isAddMode=true; $('authCard').hidden=true; $('rg-hero-title').textContent='別のクラブを追加'; $('rg-hero-sub').textContent='ログイン中のアカウントに、別のクラブを追加できます。';
    try{ var t=await db.from('teams').select('id').eq('user_id',ses.user.id).order('created_at',{ascending:false}); if(t.data&&t.data[0]){ var em=await db.rpc('team_email',{team:t.data[0].id}); if(typeof em.data==='string'&&em.data&&!$('email').value) $('email').value=em.data; } }catch(_){}
  })();
  function dataURLtoBlob(d){ var parts=d.split(','), mime=(parts[0].match(/:(.*?);/)||[])[1]||'image/jpeg'; var bin=atob(parts[1]), n=bin.length, u8=new Uint8Array(n); while(n--) u8[n]=bin.charCodeAt(n); return new Blob([u8],{type:mime}); }
  var msg=$('rg-msg');
  function err(t){ msg.hidden=false; msg.className='rg-msg err'; msg.textContent=t; msg.scrollIntoView({behavior:'smooth',block:'center'}); }
  function clearErr(){ msg.hidden=true; }
  /* ---- 送信 ---- */
  $('rg-form').addEventListener('submit',async function(e){
    e.preventDefault(); clearErr();
    var ages=[].slice.call(document.querySelectorAll('input[name="age"]:checked')).map(function(x){ return x.value; });
    var ageMin=(document.querySelector('input[name="age_min"]:checked')||{}).value||null;
    var days=[].slice.call(document.querySelectorAll('input[name="day"]:checked')).map(function(x){ return x.value; });
    var trialEl=document.querySelector('input[name="trial"]:checked');
    var email=$('email').value.trim(), instagram=$('instagram').value.trim().replace(/^@/,''), twitter=$('twitter').value.trim().replace(/^@/,''), websiteUrl=$('website_url').value.trim(), lineUrl=$('line_url').value.trim();
    var feeNum=parseInt($('feeNum').value,10), name=$('name').value.trim();
    var sport=(sportSel.value==='その他')?sportOther.value.trim():sportSel.value; var city=(citySel.value==='その他')?cityOther.value.trim():citySel.value;
    var adm=$('admission').value.trim(); var admNum=adm===''?null:parseInt(adm,10);
    if(!name) return err('クラブ名を入力してください。'); if(!sport) return err('種目を選択してください。'); if(!prefSel.value) return err('都道府県を選択してください。'); if(!city) return err('市区町村を選択してください。');
    if(!ages.length) return err('対象年齢を1つ以上選択してください。'); if(ages.indexOf('未就学')>=0&&!ageMin) return err('未就学の受け入れ開始年齢を選んでください。'); if(!days.length) return err('活動曜日を1つ以上選択してください。');
    if(isNaN(feeNum)) return err('月謝を数字で入力してください（無料は 0）。'); if(!trialEl) return err('体験の受付を選択してください。'); if(!ta.value.trim()) return err('紹介文を入力してください。');
    if(!email) return err('申込の通知先メールアドレスを入力してください。');
    if(instagram&&!/^[a-zA-Z0-9._]+$/.test(instagram)) return err('InstagramのIDは半角英数字・ピリオド・アンダースコアのみです。'); if(twitter&&!/^[a-zA-Z0-9_]+$/.test(twitter)) return err('XのIDは半角英数字・アンダースコアのみです。');
    if(websiteUrl&&!/^https?:\/\//.test(websiteUrl)) return err('ホームページのURLは http/https から始めてください。'); if(lineUrl&&!/^https?:\/\//.test(lineUrl)) return err('LINE公式のURLは http/https から始めてください。');
    if(adm!==''&&isNaN(admNum)) return err('入会金は数字で入力してください。');
    if(!$('agreeCheck').checked) return err('利用規約・プライバシーポリシーへの同意が必要です。');
    if(!isAddMode){ var ae=$('authEmail').value.trim(), pw=$('authPassword').value, pw2=$('authPasswordConfirm').value; if(!ae) return err('アカウントのメールアドレスを入力してください。'); if(pw.length<8) return err('パスワードは8文字以上で入力してください。'); if(pw!==pw2) return err('パスワードが一致しません。'); }
    var btn=$('rg-submit'); btn.disabled=true; var label=btn.textContent; btn.textContent='送信中...';
    function back(t){ btn.disabled=false; btn.textContent=label; err(t); }
    var userId=null;
    if(isAddMode){ var s2=await db.auth.getSession(); userId=s2&&s2.data&&s2.data.session?s2.data.session.user.id:null; if(!userId) return back('ログインセッションが切れています。再度ログインしてください。'); }
    else { var au=await db.auth.signUp({email:$('authEmail').value.trim(),password:$('authPassword').value,options:{data:{role:'club'}}}); if(au.error) return back('アカウント作成に失敗しました：'+(au.error.message||'')); userId=au.data&&au.data.user?au.data.user.id:null; }
    var addr1=$('address1').value.trim()||null;
    var ins=await db.from('teams').insert({ name:name, sport:sport, pref:prefSel.value, city:city, age_groups:ages, age_min:ageMin, female_instructor:!!document.querySelector('input[name="feature"][value="女性指導者あり"]:checked'), girls_welcome:!!document.querySelector('input[name="feature"][value="女の子歓迎"]:checked'),
      days:days, fee_num:feeNum, fee:'月'+feeNum.toLocaleString()+'円', trial:trialEl.value==='true', trial_fee:$('trialFee').value.trim()||null, admission_fee_num:admNum,
      instagram:instagram||null, email:email||null, twitter:twitter||null, website_url:websiteUrl||null, line_url:lineUrl||null,
      address:addr1, address1:addr1, postal_code:($('postal').value||'').replace(/[^0-9]/g,'')||null, venue:$('venue').value.trim()||null,
      description:ta.value.trim()||null, status:'pending', user_id:userId||null });
    if(ins.error){ console.warn(ins.error); return back('送信に失敗しました。もう一度お試しください。'); }
    var teamId=null;
    try{ var tr=await db.from('teams').select('id').eq('user_id',userId).order('created_at',{ascending:false}); teamId=tr.data&&tr.data[0]?tr.data[0].id:null;
      if(teamId&&photos.length){ var blob=dataURLtoBlob(photos[0].src); var path=userId+'/'+teamId+'-'+Date.now()+'.'+(blob.type==='image/webp'?'webp':'jpg');
        var up=await db.storage.from('team-photos').upload(path,blob,{upsert:true,contentType:blob.type||'image/jpeg',cacheControl:'31536000'});
        if(!up.error){ var pub=db.storage.from('team-photos').getPublicUrl(path); await db.from('teams').update({photo_url:pub.data.publicUrl}).eq('id',teamId); } } }catch(_){}
    fetch(FN+'/send-admin-notify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({team_name:name,sport:sport,pref:prefSel.value,city:city,applicant_email:email||(instagram?('Instagram: @'+instagram):'未入力')})}).catch(function(){});
    if(typeof gtag==='function') gtag('event',isAddMode?'team_added':'team_registered',{team_name:name,sport:sport,plan:planKey});
    $('rg-form').hidden=true; document.body.classList.add('done'); window.scrollTo({top:0,behavior:'smooth'});
    var paid=STRIPE_LINKS[planKey];
    if(paid&&planKey!=='free'){ var payUrl=paid+(teamId?('?client_reference_id='+encodeURIComponent(teamId)):''); $('rg-success-title').textContent='登録を受け付けました'; $('rg-success-msg').innerHTML='続けてお支払い手続きに進みます…<br>自動で移動しない場合は下のボタンを押してください。'; $('rg-done-next').hidden=true; var sb=$('rg-success-btn'); sb.textContent='お支払いに進む ›'; sb.href=payUrl; setTimeout(function(){ location.href=payUrl; },1600); return; }
    if(isAddMode){ $('rg-success-title').textContent='クラブを追加しました'; $('rg-success-msg').innerHTML='運営の承認後に掲載されます。<br>マイページからクラブを切り替えて確認できます。'; }
  });
})();
