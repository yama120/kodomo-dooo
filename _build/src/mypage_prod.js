(function(){
  var A=window.ChibiAuth, SB='https://emkpkomrgknzrmxqbrvx.supabase.co', ANON='__ANON__';
  function $(id){ return document.getElementById(id); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  var tabs=$('mpTabs');
  function show(k){ document.querySelectorAll('.mp-panel').forEach(function(p){ p.classList.toggle('on',p.dataset.tab===k); }); tabs.querySelectorAll('button').forEach(function(b){ b.classList.toggle('on',b.dataset.tab===k); }); }
  tabs.addEventListener('click',function(e){ var b=e.target.closest('button'); if(b){ show(b.dataset.tab); history.replaceState(null,'','#'+b.dataset.tab); } });
  document.addEventListener('click',function(e){ var a=e.target.closest('a[data-tab]'); if(a){ e.preventDefault(); show(a.dataset.tab); history.replaceState(null,'','#'+a.dataset.tab); window.scrollTo({top:tabs.getBoundingClientRect().top+scrollY-70,behavior:'smooth'}); } });
  var h=(location.hash||'').replace('#',''); if(/^(home|result|notify|fav|msg|account)$/.test(h)) show(h);
  if(location.search.indexOf('saved=1')>=0) show('result');
  var GRADES={'未就学':'未就学','年長':'年長','小1〜2':'小1〜2','小3〜4':'小3〜4','小5〜6':'小5〜6','中学生':'中学生'};

  /* ---- 診断の結果（localStorage → プロフィールにも保存） ---- */
  var quiz=null; try{ quiz=JSON.parse(localStorage.getItem('chibispo_quiz')||'null'); }catch(e){}
  function renderQuiz(q){
    var box=$('mpSaved'), empty=$('mpEmpty'); if(!q){ box.hidden=true; empty.hidden=false; return; }
    box.hidden=false; empty.hidden=true;
    box.querySelector('.tp').innerHTML='お子さんに合いそうなのは、<em>'+esc(q.typeName||'')+'</em>。';
    box.querySelector('.cond').innerHTML=(q.cond||[]).map(function(c){ return '<span>'+esc(c)+'</span>'; }).join('');
    box.querySelector('.sp').innerHTML='まず見てほしい種目：'+(q.sports||[]).map(function(x){ return '<b>'+esc(x)+'</b>'; }).join('・');
    var d=new Date(q.at||Date.now()); box.querySelector('.date').textContent=d.getFullYear()+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+('0'+d.getDate()).slice(-2);
    var s=$('mpSavedSearch'); if(s&&q.sports&&q.sports[0]) s.href='search.html?sport='+encodeURIComponent(q.sports[0])+(q.areaPref?'&pref='+encodeURIComponent(q.areaPref):'');
    if(location.search.indexOf('saved=1')>=0&&!box.previousElementSibling.classList.contains('saved-note')){ var n=document.createElement('div'); n.className='saved-note'; n.style.cssText='margin:0 0 14px;padding:10px 14px;border:1px solid var(--accent);color:var(--accent);font-size:12.5px;font-weight:900;border-radius:var(--r)'; n.textContent='診断の結果を保存しました。条件に合うクラブが載ったらお知らせします。'; box.parentNode.insertBefore(n,box); }
  }
  /* ---- お気に入り（端末に保存。ログイン時は likes とも同期＝shared.js） ---- */
  function renderFavs(){
    var favs=(window.Chibi&&Chibi.getFavs())||[]; var wrap=$('mpFavs'), empty=$('mpFavEmpty'); $('mpFavN').textContent=favs.length;
    if(!favs.length){ wrap.innerHTML=''; empty.hidden=false; return; } empty.hidden=true;
    wrap.innerHTML=favs.map(function(f){ return '<a class="nc" href="'+esc(f.href||('/club.html?id='+f.id))+'"><div class="nc-img">'+(f.img?'<img src="'+esc(f.img)+'" alt="">':'<div class="nc-ph"></div>')+'<button class="rm" type="button" data-id="'+esc(f.id)+'" aria-label="外す">&times;</button></div><div class="nc-b"><h3 class="nc-name">'+esc(f.name)+'</h3>'+(f.area?'<div class="nc-area">'+esc(f.area)+'</div>':'')+'</div></a>'; }).join('');
    wrap.querySelectorAll('.rm').forEach(function(b){ b.addEventListener('click',function(e){ e.preventDefault(); e.stopPropagation(); if(window.Chibi) Chibi.removeFav(b.getAttribute('data-id')); }); });
  }
  document.addEventListener('chibi:favs',function(){ renderFavs(); renderHome(); });

  /* ---- 体験申込とメッセージ（アプリと同じ trial_requests / trial_messages / trial_reads） ---- */
  var TRIAL_LABEL={new:'受付済み・クラブ確認中',attended:'体験に参加しました',joined:'入会しました',lost:'見送り'};
  var chat={trialId:null,timer:null}, trialsCache=[], unreadTotal=0, me=null, prof=null;
  function authToken(){ var d=A.client(); if(!d) return Promise.resolve(null); return d.auth.getSession().then(function(r){ return (r&&r.data&&r.data.session&&r.data.session.access_token)||null; }).catch(function(){ return null; }); }
  function restGet(q){ return authToken().then(function(tok){ if(!tok) return []; return fetch(SB+'/rest/v1/'+q,{headers:{apikey:ANON,Authorization:'Bearer '+tok}}).then(function(r){ return r.ok?r.json():[]; }).catch(function(){ return []; }); }); }
  function loadTrials(){
    var d=A.client(); if(!d||!me) return Promise.resolve();
    return d.from('trial_requests').select('id,team_id,child_name,child_grade,status,type,created_at').order('created_at',{ascending:false}).then(function(res){
      var rows=(res&&res.data)||[]; trialsCache=rows; var host=$('mpTrials'), empty=$('mpTrialEmpty');
      if(!rows.length){ host.innerHTML=''; empty.hidden=false; $('mpMsgN').hidden=true; renderHome(); return; }
      empty.hidden=true;
      var teamIds=rows.map(function(r){ return r.team_id; }).filter(Boolean), trialIds=rows.map(function(r){ return r.id; });
      return Promise.all([restGet('teams?select=id,name&id=in.('+teamIds.join(',')+')'),restGet('trial_messages?select=trial_id,sender_role,created_at&trial_id=in.('+trialIds.join(',')+')'),restGet('trial_reads?select=trial_id,last_read_at&user_id=eq.'+me.id+'&trial_id=in.('+trialIds.join(',')+')')]).then(function(r3){
        var names={}; (r3[0]||[]).forEach(function(t){ names[t.id]=t.name; });
        var readAt={}; (r3[2]||[]).forEach(function(r){ readAt[r.trial_id]=Date.parse(r.last_read_at); });
        var unread={}, last={}; (r3[1]||[]).forEach(function(m){ var ts=Date.parse(m.created_at); if(!last[m.trial_id]||ts>last[m.trial_id]) last[m.trial_id]=ts; if(m.sender_role==='parent') return; var seen=readAt[m.trial_id]; if(!seen||ts>seen) unread[m.trial_id]=(unread[m.trial_id]||0)+1; });
        unreadTotal=0; rows.forEach(function(r){ r._name=names[r.team_id]||'クラブ'; r._unread=unread[r.id]||0; unreadTotal+=r._unread; r._last=last[r.id]||Date.parse(r.created_at); });
        host.innerHTML=rows.map(function(r){ var child=[r.child_name,r.child_grade].filter(Boolean).join('・'); var kind=r.type==='question'?'質問':'体験申込';
          return '<div class="m" data-chat="'+esc(r.id)+'" data-club="'+esc(r._name)+'" data-child="'+esc(child)+'"><div><div class="n">'+esc(r._name)+'</div><div class="s">'+kind+(child?' ・ '+esc(child):'')+' ・ '+String(r.created_at||'').slice(0,10)+(r.status&&TRIAL_LABEL[r.status]&&r.status!=='new'?' ・ '+TRIAL_LABEL[r.status]:'')+'</div></div><div class="st '+(r._unread?'new':'dim')+'">'+(r._unread?'返信 '+r._unread:'メッセージ')+'</div></div>'; }).join('');
        host.querySelectorAll('[data-chat]').forEach(function(b){ b.addEventListener('click',function(){ openChat(b.getAttribute('data-chat'),b.getAttribute('data-club'),b.getAttribute('data-child')); }); });
        var n=$('mpMsgN'); n.textContent=unreadTotal; n.hidden=!unreadTotal; renderHome();
      });
    });
  }
  function renderMessages(list){ var body=$('mp-chat-body'); if(!list.length){ body.innerHTML='<p class="empty">まだメッセージはありません。<br>日程の相談などにご利用ください。</p>'; return; }
    body.innerHTML=list.map(function(m){ var mine=m.sender_role==='parent'; var t=new Date(m.created_at); var hm=(t.getMonth()+1)+'/'+t.getDate()+' '+String(t.getHours()).padStart(2,'0')+':'+String(t.getMinutes()).padStart(2,'0');
      return '<div class="row'+(mine?' me':'')+'"><div class="bb"><div class="t">'+esc(m.body)+'</div><div class="d">'+hm+'</div></div></div>'; }).join(''); body.scrollTop=body.scrollHeight; }
  function fetchMessages(){ var d=A.client(); if(!d||!chat.trialId) return; d.from('trial_messages').select('id,sender_role,body,created_at').eq('trial_id',chat.trialId).order('created_at',{ascending:true}).then(function(res){ renderMessages((res&&res.data)||[]); }); }
  function markRead(trialId){ var d=A.client(); if(!d||!me) return; d.from('trial_reads').upsert({trial_id:trialId,user_id:me.id,last_read_at:new Date().toISOString()},{onConflict:'trial_id,user_id'}).then(function(){}); }
  function openChat(trialId,club,child){ chat.trialId=trialId; $('mp-chat-title').textContent=club; $('mp-chat-sub').textContent=(child?child+'の':'')+'申込について'; $('mp-chat-bg').style.display='flex'; $('mp-chat-body').innerHTML='<p class="empty">読み込み中…</p>'; fetchMessages(); markRead(trialId); clearInterval(chat.timer); chat.timer=setInterval(fetchMessages,15000); }
  function closeChat(){ $('mp-chat-bg').style.display='none'; clearInterval(chat.timer); chat.timer=null; chat.trialId=null; loadTrials(); }
  function sendMessage(){ var d=A.client(); if(!d||!chat.trialId||!me) return; var inp=$('mp-chat-input'), text=(inp.value||'').trim(); if(!text) return; var btn=$('mp-chat-send'); btn.disabled=true; inp.value='';
    d.from('trial_messages').insert({trial_id:chat.trialId,sender_role:'parent',sender_id:me.id,body:text}).then(function(res){ btn.disabled=false; if(res&&res.error){ inp.value=text; alert('送信に失敗しました。時間をおいてお試しください。'); return; } fetchMessages();
      authToken().then(function(tok){ if(!tok) return; fetch(SB+'/functions/v1/notify-message',{method:'POST',headers:{Authorization:'Bearer '+tok,'Content-Type':'application/json'},body:JSON.stringify({trial_id:chat.trialId,body:text})}).catch(function(){}); }); }); }
  $('mp-chat-close').addEventListener('click',closeChat); $('mp-chat-bg').addEventListener('click',function(e){ if(e.target===$('mp-chat-bg')) closeChat(); }); $('mp-chat-send').addEventListener('click',sendMessage);
  (function(){ var i=$('mp-chat-input'), composing=false; i.addEventListener('compositionstart',function(){ composing=true; }); i.addEventListener('compositionend',function(){ composing=false; }); i.addEventListener('keydown',function(e){ if(e.key!=='Enter') return; e.preventDefault(); if(composing||e.isComposing||e.keyCode===229) return; sendMessage(); }); })();

  /* ---- ホーム：動きがあるものから ---- */
  function renderHome(){
    var host=$('mpHome'); if(!host) return; var cards=[];
    var withUnread=trialsCache.filter(function(r){ return r._unread; }).sort(function(a,b){ return b._last-a._last; });
    if(withUnread.length){ var r=withUnread[0]; cards.push({k:'MESSAGE',b:esc(r._name)+'から返信が届いています',s:(r.type==='question'?'質問':'体験申込')+' ・ '+String(r.created_at||'').slice(0,10),tab:'msg',hot:true}); }
    else if(trialsCache.length){ var r0=trialsCache[0]; cards.push({k:'MESSAGE',b:esc(r0._name)+'への'+(r0.type==='question'?'質問':'体験申込'),s:'クラブからの返信を待っています',tab:'msg'}); }
    if(quiz) cards.push({k:'YOUR TYPE',b:'お子さんに合いそうなのは、'+esc(quiz.typeName||''),s:(quiz.sports||[]).join('・'),tab:'result'});
    else cards.push({k:'QUIZ',b:'3つの質問で、合いそうな種目を知る',s:'1分・無料。結果は保存できます',tab:'result'});
    var favs=(window.Chibi&&Chibi.getFavs())||[]; cards.push({k:'FAVORITES',b:'お気に入り '+favs.length+'クラブ',s:favs.length?'比べて、体験を申し込めます':'クラブの ♡ で残せます',tab:'fav'});
    var np=(prof&&prof.notify_prefs)||{}; var on=['new_clubs','trial_open','articles'].filter(function(k){ return np[k]; }).length;
    cards.push({k:'NOTIFICATIONS',b:'お知らせ '+on+'つを受け取る設定',s:on?'新しいクラブ・体験の募集':'受け取るものを選べます',tab:'notify'});
    host.innerHTML=cards.map(function(c){ return '<a class="mp-hc'+(c.hot?' hot':'')+'" href="#" data-tab="'+c.tab+'"><div><div class="k">'+c.k+'</div><b>'+c.b+'</b><small>'+esc(c.s)+'</small></div><span class="go">›</span></a>'; }).join('');
  }
  /* ---- お知らせ設定 ---- */
  function bindNotify(){ var np=(prof&&prof.notify_prefs)||{new_clubs:true,trial_open:true,articles:false,push:true,email:true};
    document.querySelectorAll('.ntf input[data-k]').forEach(function(i){ i.checked=!!np[i.dataset.k]; i.addEventListener('change',function(){ np[i.dataset.k]=i.checked; prof.notify_prefs=np; var d=A.client(); if(!d||!me) return; d.from('profiles').update({notify_prefs:np}).eq('id',me.id).then(function(res){ $('ntfMsg').textContent=(res&&res.error)?'保存に失敗しました。':'保存しました。通知は1日1回までにまとめて届きます。'; renderHome(); }); }); });
    var s=$('ntfNewS'); if(s){ var parts=[prof.pref,prof.city].filter(Boolean).join(' '); if(parts) s.textContent=parts+'で、条件に合うクラブが登録されたら'; } }
  /* ---- アカウント ---- */
  function fillAccount(){
    var name=prof.display_name||(prof.email?prof.email.split('@')[0]:'ゲスト');
    $('mpName').textContent=name; $('mpAv').textContent=name.charAt(0).toUpperCase();
    var ln=prof.last_name, fn=prof.first_name; if(!ln&&!fn&&prof.full_name){ var p=prof.full_name.trim().split(/\s+/); ln=p[0]||''; fn=p.slice(1).join(' '); }
    var region=[prof.pref,prof.city].filter(Boolean).join(' '); var child=[prof.child_grade,prof.child_gender].filter(Boolean).join(' ・ ');
    $('mpMeta').textContent=[region,child?'お子さん '+child:'',prof.email].filter(Boolean).join(' ・ ');
    $('vDisplay').textContent=prof.display_name||'未設定'; $('vName').textContent=[ln,fn].filter(Boolean).join(' ')||'未設定'; $('vEmail').textContent=prof.email||''; $('vRegion').textContent=region||'未設定'; $('vChild').textContent=child||'未設定';
    $('eDisplay').value=prof.display_name||''; $('eLast').value=ln||''; $('eFirst').value=fn||''; $('eGrade').value=prof.child_grade||''; $('eGender').value=prof.child_gender||'';
    if(typeof CITIES!=='undefined'){ var pf=$('ePref'), ct=$('eCity'); if(pf.options.length<=1){ pf.innerHTML='<option value="">都道府県</option>'+Object.keys(CITIES).map(function(p){ return '<option value="'+p+'">'+p+'</option>'; }).join(''); pf.addEventListener('change',function(){ ct.innerHTML='<option value="">市区町村</option>'+(CITIES[pf.value]||[]).map(function(c){ return '<option value="'+c+'">'+c+'</option>'; }).join(''); ct.disabled=!pf.value; }); }
      if(prof.pref){ pf.value=prof.pref; pf.dispatchEvent(new Event('change')); if(prof.city) ct.value=prof.city; } }
    if(region&&window.Chibi) Chibi.setRegionParts(prof.pref,prof.city);
    var g=null; try{ g=localStorage.getItem('chibispo_child_grade'); }catch(e){}
    if(g&&!prof.child_grade&&me){ A.client().from('profiles').update({child_grade:g}).eq('id',me.id).then(function(){ prof.child_grade=g; try{ localStorage.removeItem('chibispo_child_grade'); }catch(e){} fillAccount(); }); }
  }
  function saveMsg(ok,text){ var m=$('mpSaveMsg'); m.style.color=ok?'#1f8a5b':'#b3232e'; m.textContent=text; }
  document.querySelector('.acc').addEventListener('click',function(e){
    var ed=e.target.closest('a[data-edit]'); if(ed){ e.preventDefault(); $(ed.dataset.edit).classList.add('open'); return; }
    var cc=e.target.closest('button[data-cancel]'); if(cc){ $(cc.dataset.cancel).classList.remove('open'); return; }
    var sv=e.target.closest('button[data-save]'); if(!sv) return; var d=A.client(); if(!d||!me) return; var k=sv.dataset.save, patch={};
    if(k==='display'){ patch.display_name=$('eDisplay').value.trim(); if(!patch.display_name) return saveMsg(false,'ニックネームを入力してください。'); }
    if(k==='name'){ var l=$('eLast').value.trim(), f=$('eFirst').value.trim(); patch.last_name=l; patch.first_name=f; patch.full_name=[l,f].filter(Boolean).join(' '); }
    if(k==='region'){ patch.pref=$('ePref').value; patch.city=$('eCity').value; patch.region=[patch.pref,patch.city].filter(Boolean).join(' '); }
    if(k==='child'){ patch.child_grade=$('eGrade').value||null; patch.child_gender=$('eGender').value||null; }
    if(k==='pw'){ var p1=$('ePw1').value, p2=$('ePw2').value; if(!p1||p1.length<6) return saveMsg(false,'パスワードは6文字以上で入力してください。'); if(p1!==p2) return saveMsg(false,'パスワードが一致しません。');
      d.auth.updateUser({password:p1}).then(function(res){ if(res&&res.error) saveMsg(false,'更新に失敗しました。'); else { saveMsg(true,'パスワードを更新しました。'); $('ePw1').value=''; $('ePw2').value=''; $('rPw').classList.remove('open'); } }); return; }
    sv.disabled=true;
    d.from('profiles').update(patch).eq('id',me.id).then(function(res){ sv.disabled=false; if(res&&res.error){ saveMsg(false,'保存に失敗しました。'); return; } Object.keys(patch).forEach(function(x){ prof[x]=patch[x]; }); saveMsg(true,'保存しました。'); fillAccount(); document.querySelectorAll('.acc .r.open').forEach(function(r){ r.classList.remove('open'); }); });
  });
  $('mpLogout').addEventListener('click',function(e){ e.preventDefault(); A.signOut().then(function(){ location.href='index.html'; }); });

  /* ---- 起動 ---- */
  function out(){ $('mp-out').hidden=false; $('mp-in').hidden=true; }
  if(!A||!A.ready()){ out(); return; }
  A.getProfile().then(function(p){
    if(!p){ out(); return; }
    if(p.role==='club'){ location.href='club-mypage.html'; return; }
    A.hasTeam().then(function(isClub){ if(isClub) location.href='club-mypage.html'; });
    prof=p; me={id:p.id,email:p.email}; $('mp-in').hidden=false; $('mp-out').hidden=true;
    if(quiz&&!p.quiz_result){ A.client().from('profiles').update({quiz_result:quiz}).eq('id',p.id).then(function(){}); }
    if(!quiz&&p.quiz_result){ quiz=p.quiz_result; try{ localStorage.setItem('chibispo_quiz',JSON.stringify(quiz)); }catch(e){} }
    renderQuiz(quiz); renderFavs(); fillAccount(); bindNotify(); renderHome(); loadTrials();
  }).catch(out);
})();
