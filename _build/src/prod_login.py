# 保護者のログイン／新規登録 本番（login.html）：lg_v2 の見た目＋旧 login.html の ChibiAuth 処理
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
cap={}
def page(fname,title,body,css='',bodyattr='',extra_js=''): cap.update(body=body,css=css)
src=open(P+'build_pages.py',encoding='utf-8').read(); src=src[:src.index("page('")]
g={'__name__':'prod_login','P':P}; exec(src,g); g['page']=page; exec(open(P+'lg_v2.py',encoding='utf-8').read(),g)
body=re.sub(r'<div class="note"[^>]*>.*?</div>\n?','',cap['body'],flags=re.S)
GICON=re.search(r'<a class="lg-g" href="#">(<svg.*?</svg>)',body,re.S).group(1)
head=body[:body.index('<div class="lg-box">')]
head=head.replace('href="video-hero-preview.html"','href="index.html"')
BOX='''<div class="lg-box" id="lg-auth">
      <div class="lg-tabs" id="lgTabs"><button type="button" data-m="login" class="on">ログイン</button><button type="button" data-m="signup">新規登録（無料）</button></div>
      <div class="lg-msg" id="lg-msg" hidden></div>
      <div class="lg-p on" data-m="login">
        <button type="button" class="lg-g" id="lg-google">%(g)s Googleでログイン</button>
        <div class="lg-or">または メールで</div>
        <div class="lg-f"><label>メールアドレス</label><input class="lg-in" id="lg-email" type="email" placeholder="you@example.com" autocomplete="email"></div>
        <div class="lg-f"><label>パスワード</label><div class="lg-pw"><input class="lg-in" id="lg-pw" type="password" placeholder="••••••••" autocomplete="current-password"><span class="eye">表示</span></div></div>
        <button type="button" class="lg-btn" id="lg-submit">ログイン ›</button>
        <div class="lg-links"><a href="#" id="lg-forgot">パスワードを忘れた方</a><span>はじめての方は <a href="#" data-m="signup">新規登録</a></span></div>
        <div class="lg-app"><img src="assets/icon-192.png" alt="" onerror="this.style.display='none'"><div><b>アプリなら通知がすぐ届きます</b><small>体験の返信・新着クラブ・お知らせ</small></div><a href="https://apps.apple.com/jp/app/id6797169414" target="_blank" rel="noopener">アプリを開く</a></div>
      </div>
      <div class="lg-p" data-m="signup">
        <button type="button" class="lg-g" id="sg-google">%(g)s Googleで登録</button>
        <div class="lg-or">または メールで</div>
        <div class="lg-f"><label>ニックネーム <span class="req">必須</span><span class="pv">サイトに表示されます</span></label><input class="lg-in" id="sg-display" placeholder="例：はなまま"><div class="hint">口コミやコメントに出る名前です</div></div>
        <div class="lg-f"><label>お名前 <span class="req">必須</span><span class="pv">サイトには表示されません</span></label><div class="lg-row"><input class="lg-in" id="sg-last" placeholder="姓（例：山田）" autocomplete="family-name"><input class="lg-in" id="sg-first" placeholder="名（例：花子）" autocomplete="given-name"></div><div class="hint">体験を申し込むときに、クラブにだけ伝わります</div></div>
        <div class="lg-f"><label>お住まいの地域 <span class="opt">任意</span></label><div class="lg-row"><select class="lg-in" id="sg-pref"><option value="">都道府県</option></select><select class="lg-in" id="sg-city" disabled><option value="">市区町村</option></select></div><div class="hint">近くのクラブと、地域の新着のお知らせに使います</div></div>
        <div class="lg-f"><label>お子さんの学年 <span class="opt">任意</span></label><div class="lg-chip" id="sg-grade"><span data-v="未就学">未就学</span><span data-v="年長">年長</span><span data-v="小1〜2">小1〜2</span><span data-v="小3〜4">小3〜4</span><span data-v="小5〜6">小5〜6</span><span data-v="中学生">中学生</span></div><div class="hint">診断と体験申込のフォームに、自動で入ります。あとから変えられます</div></div>
        <div class="lg-f"><label>メールアドレス <span class="req">必須</span></label><input class="lg-in" id="sg-email" type="email" placeholder="you@example.com" autocomplete="email"></div>
        <div class="lg-f"><label>パスワード <span class="req">必須</span></label><div class="lg-row"><input class="lg-in" id="sg-pw" type="password" placeholder="8文字以上" autocomplete="new-password"><input class="lg-in" id="sg-pw2" type="password" placeholder="もう一度" autocomplete="new-password"></div></div>
        <button type="button" class="lg-btn" id="sg-submit">無料で登録する ›</button>
        <div class="lg-agree">登録すると <a href="legal.html#terms">利用規約</a> と <a href="legal.html#privacy">プライバシーポリシー</a> に同意したことになります。お知らせはいつでも止められます。</div>
        <div class="lg-links"><span>すでに登録している方は <a href="#" data-m="login">ログイン</a></span></div>
      </div>
    </div>
    <div class="lg-box lg-done" id="lg-done" hidden>
      <div class="lg-done-av" id="lg-done-initial">M</div>
      <div class="lg-done-name" id="lg-done-name">さん</div>
      <div class="lg-done-mail" id="lg-done-email"></div>
      <p>ログイン済みです。</p>
      <a class="lg-btn" id="lg-done-mypage" href="mypage.html">マイページへ ›</a>
      <div class="lg-links"><a href="#" id="lg-logout">ログアウト</a></div>
    </div>
  </div>
  <div style="height:40px"></div>
</div></main>'''%dict(g=GICON)
BODY=head+BOX
CSS=C.strip_preview(cap['css'])+'''
.lg-g{cursor:pointer;font-family:var(--f);width:100%%;background:var(--card)}
.lg-btn{cursor:pointer;border:0;width:100%%;font-family:var(--fh)}
.lg-msg{margin:0 0 12px;padding:10px 12px;border-radius:calc(var(--r) - 4px);font-size:12.5px;font-weight:800;line-height:1.6}
.lg-msg.err{background:#fff0f2;color:#b3232e}.lg-msg.ok{background:#eafaf0;color:#1f8a5b}
.lg-chip span{cursor:pointer}
.lg-done{text-align:center;padding:34px 24px}
.lg-done-av{width:56px;height:56px;border-radius:50%%;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:24px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px}
.lg-done-name{font-family:var(--fh);font-size:20px;font-weight:900}
.lg-done-mail{font-size:12.5px;font-weight:700;color:var(--sub);margin:2px 0 10px}
.lg-done p{font-size:13px;font-weight:700;margin:0 0 14px}
select.lg-in{appearance:none;-webkit-appearance:none}
'''.replace('%%','%')
JS=r'''<script>
(function(){
  var A=window.ChibiAuth; function $(id){ return document.getElementById(id); }
  var tabs=$('lgTabs'), mode='login';
  function show(m){ mode=m; document.querySelectorAll('.lg-p').forEach(function(p){ p.classList.toggle('on',p.dataset.m===m); }); tabs.querySelectorAll('button').forEach(function(b){ b.classList.toggle('on',b.dataset.m===m); }); clearMsg(); }
  tabs.addEventListener('click',function(e){ var b=e.target.closest('button'); if(b){ show(b.dataset.m); history.replaceState(null,'','?mode='+b.dataset.m+(next?'&next='+encodeURIComponent(next):'')); } });
  document.addEventListener('click',function(e){ var a=e.target.closest('a[data-m]'); if(a){ e.preventDefault(); show(a.dataset.m); }
    var c=e.target.closest('.lg-chip span'); if(c){ c.parentNode.querySelectorAll('span').forEach(function(x){ x.classList.toggle('on',x===c); }); }
    var ey=e.target.closest('.eye'); if(ey){ var i=ey.parentNode.querySelector('input'); i.type=i.type==='password'?'text':'password'; ey.textContent=i.type==='password'?'表示':'隠す'; } });
  var q=new URLSearchParams(location.search), next=q.get('next')||'';
  if(q.get('mode')==='signup') show('signup');
  function safeNext(){ return (next && /^[a-z0-9\-_.\/]+(\?.*)?$/i.test(next) && next.indexOf('//')<0) ? next : ''; }
  function msg(type,text){ var m=$('lg-msg'); m.hidden=false; m.className='lg-msg '+type; m.textContent=text; m.scrollIntoView({block:'nearest'}); }
  function clearMsg(){ var m=$('lg-msg'); m.hidden=true; m.textContent=''; }
  (function(){ if(typeof CITIES==='undefined') return; var pf=$('sg-pref'), ct=$('sg-city');
    pf.innerHTML='<option value="">都道府県</option>'+Object.keys(CITIES).map(function(p){ return '<option value="'+p+'">'+p+'</option>'; }).join('');
    pf.addEventListener('change',function(){ if(!pf.value){ ct.innerHTML='<option value="">市区町村</option>'; ct.disabled=true; return; } ct.innerHTML='<option value="">市区町村</option>'+(CITIES[pf.value]||[]).map(function(c){ return '<option value="'+c+'">'+c+'</option>'; }).join(''); ct.disabled=false; });
    var rp=window.Chibi&&Chibi.getRegionPref&&Chibi.getRegionPref(); if(rp&&CITIES[rp]){ pf.value=rp; pf.dispatchEvent(new Event('change')); var rc=Chibi.getRegionCity&&Chibi.getRegionCity(); if(rc) ct.value=rc; }
  })();
  function afterLogin(){ var n=safeNext(); if(n){ location.href=n; return; } A.getProfile().then(function(prof){ location.href=(prof&&prof.role==='club')?'club-mypage.html':'mypage.html'; }).catch(function(){ location.href='mypage.html'; }); }
  function errText(e){ var t=(e&&(e.message||e.error_description||e.msg))||'エラーが発生しました。'; if(/Invalid login/i.test(t)) t='メールアドレスまたはパスワードが正しくありません。'; if(/already registered|already been registered|User already/i.test(t)) t='このメールアドレスは既に登録されています。「ログイン」からログインしてください。（クラブとして登録済みの場合もこのままログインできます）'; if(/Email not confirmed/i.test(t)) t='メールアドレスの確認が済んでいません。届いているメールのリンクを開いてください。'; return t; }
  if(!A){ msg('err','読み込みに失敗しました。ページを再読み込みしてください。'); return; }
  $('lg-submit').addEventListener('click',function(){ clearMsg();
    var email=$('lg-email').value.trim(), pw=$('lg-pw').value;
    if(!email) return msg('err','メールアドレスを入力してください。'); if(!pw||pw.length<6) return msg('err','パスワードは6文字以上で入力してください。');
    var b=$('lg-submit'); b.disabled=true;
    A.signIn(email,pw).then(function(res){ if(res.error) throw res.error; afterLogin(); }).catch(function(e){ b.disabled=false; msg('err',errText(e)); });
  });
  $('sg-submit').addEventListener('click',function(){ clearMsg();
    var email=$('sg-email').value.trim(), pw=$('sg-pw').value, pw2=$('sg-pw2').value;
    var display=$('sg-display').value.trim(), ln=$('sg-last').value.trim(), fn=$('sg-first').value.trim();
    var pref=$('sg-pref').value, city=$('sg-city').value; var gc=document.querySelector('#sg-grade span.on'); var grade=gc?gc.dataset.v:'';
    if(!display) return msg('err','ニックネームを入力してください。'); if(!ln||!fn) return msg('err','お名前（姓・名）を入力してください。');
    if(!email) return msg('err','メールアドレスを入力してください。'); if(!pw||pw.length<8) return msg('err','パスワードは8文字以上で入力してください。'); if(pw!==pw2) return msg('err','パスワードが一致しません。もう一度ご確認ください。');
    var b=$('sg-submit'); b.disabled=true;
    if(window.Chibi&&(pref||city)) Chibi.setRegionParts(pref,city);
    try{ if(grade) localStorage.setItem('chibispo_child_grade',grade); }catch(e){}
    A.signUp(email,pw,{role:'parent',last_name:ln,first_name:fn,display_name:display,pref:pref,city:city}).then(function(res){
      if(res.error) throw res.error;
      if(res.data&&res.data.session){
        var d=A.client(); var u=res.data.session.user;
        var done=function(){ location.href=safeNext()||'mypage.html'; };
        if(grade&&d&&u){ d.from('profiles').update({child_grade:grade}).eq('id',u.id).then(done).catch(done); } else done();
        return;
      }
      msg('ok','確認メールを送信しました。メール内のリンクをクリックすると登録完了です。'); b.disabled=false;
    }).catch(function(e){ b.disabled=false; msg('err',errText(e)); });
  });
  function google(){ clearMsg(); var to=location.origin+'/'+(safeNext()||'mypage.html'); A.signInWithGoogle(to).catch(function(){ msg('err','Googleログインは現在準備中です。メールでのログインをご利用ください。'); }); }
  $('lg-google').addEventListener('click',google); $('sg-google').addEventListener('click',google);
  $('lg-forgot').addEventListener('click',function(e){ e.preventDefault(); var email=$('lg-email').value.trim(); if(!email){ msg('err','メールアドレスを入力してから押してください。'); return; }
    A.resetPassword(email,location.origin+'/reset-password.html').then(function(){ msg('ok','パスワード再設定メールを送信しました。'); }).catch(function(){ msg('err','送信に失敗しました。'); }); });
  $('lg-logout').addEventListener('click',function(e){ e.preventDefault(); A.signOut().then(function(){ location.reload(); }); });
  function showLoggedIn(prof){ $('lg-auth').hidden=true; $('lg-done').hidden=false; var name=(prof&&prof.display_name)||(prof&&prof.email&&prof.email.split('@')[0])||'ゲスト';
    $('lg-done-name').textContent=name+' さん'; $('lg-done-email').textContent=(prof&&prof.email)||''; $('lg-done-initial').textContent=name.charAt(0).toUpperCase();
    if(prof&&prof.role==='club'){ $('lg-done-mypage').href='club-mypage.html'; $('lg-done-mypage').textContent='クラブのマイページへ ›'; } }
  if(A.ready()){ A.getProfile().then(function(prof){ if(prof){ if(safeNext()){ location.href=safeNext(); return; } showLoggedIn(prof); } }).catch(function(){}); }
})();
</script>'''
C.prodpage('login.html','ログイン / 新規登録｜チビスポ','チビスポの保護者アカウント。登録すると、体験の申込みとクラブとのやり取り、お気に入り、診断の保存、新着のお知らせが使えます。無料・1分。',BODY,css=CSS,js=JS,supabase=True,scripts=('cities.js?v=20260731b','site.js?v='+C.V))
