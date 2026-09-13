# ---- 保護者の登録・ログイン画面（プレビュー v2・2026-09-12）：左に理由、右にフォーム。ログイン／新規登録はタブ
lg_css='''
.lg-lay{display:grid;grid-template-columns:1fr;gap:26px;padding:26px 0 0}
.lg-why{position:relative;background:#101215;color:#fff;padding:26px 22px;overflow:hidden}
.lg-why .bg{position:absolute;inset:0;background:url(assets/preview-video/jp-soccer-keep.jpg) center 30%/cover;opacity:.35}
.lg-why::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(16,18,21,.55),rgba(16,18,21,.95))}
.lg-why>*{position:relative;z-index:1}
.lg-why .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:10px}
.lg-why .ey::before{content:"";width:22px;height:2px;background:var(--accent)}
.lg-why h1{font-family:var(--fh);margin:0 0 10px;font-size:clamp(24px,6vw,36px);font-weight:900;line-height:1.25;letter-spacing:-.01em}
.lg-why h1 em{font-style:normal;color:#111;background:#fff;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.lg-why p{margin:0 0 18px;font-size:13px;font-weight:700;color:rgba(255,255,255,.78);line-height:1.9}
.lg-why ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.lg-why li{position:relative;padding-left:34px;font-size:13px;font-weight:900;line-height:1.5}
.lg-why li small{display:block;font-size:11px;font-weight:700;color:rgba(255,255,255,.65);margin-top:2px}
.lg-why li i{position:absolute;left:0;top:0;width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;font-style:normal;font-family:'Anton',sans-serif;font-size:11px;display:flex;align-items:center;justify-content:center}
.lg-why .free{margin-top:20px;display:inline-block;border:1px solid rgba(255,255,255,.5);padding:6px 10px;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em}
.lg-box{border:1px solid var(--ink);background:var(--card)}
.lg-tabs{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--ink)}
.lg-tabs button{background:transparent;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:16px 10px 13px;font-family:var(--fh);font-size:14.5px;font-weight:900;color:var(--sub);cursor:pointer}
.lg-tabs button.on{color:var(--ink);border-bottom-color:var(--ink)}
.lg-p{display:none;padding:18px 18px 20px}
.lg-p.on{display:block}
.lg-g{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;border:1.5px solid var(--ink);background:#fff;color:var(--ink);font-family:var(--fh);font-size:14px;font-weight:900;padding:13px;box-sizing:border-box}
.lg-g svg{width:18px;height:18px}
.lg-or{display:flex;align-items:center;gap:10px;margin:14px 0;font-size:11px;font-weight:900;color:var(--sub);letter-spacing:.1em}
.lg-or::before,.lg-or::after{content:"";flex:1;height:1px;background:var(--line)}
.lg-f{display:grid;gap:5px;margin-bottom:12px}
.lg-f label{font-size:12px;font-weight:900;display:flex;align-items:center;gap:6px}
.lg-f label .req{font-size:9.5px;letter-spacing:.08em;background:var(--ink);color:var(--bg);padding:1px 5px}
.lg-f label .opt{font-size:9.5px;letter-spacing:.08em;border:1px solid var(--line);color:var(--sub);padding:1px 5px}
.lg-f label .pv{margin-left:auto;font-size:10px;font-weight:700;color:var(--sub)}
.lg-f .hint{font-size:11px;font-weight:700;color:var(--sub);line-height:1.6}
.lg-in{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:14px;font-weight:700;padding:11px 12px;color:var(--ink);box-sizing:border-box}
.lg-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.lg-pw{position:relative}
.lg-pw .eye{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:11px;font-weight:900;color:var(--sub);cursor:pointer}
.lg-btn{display:block;width:100%;text-align:center;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:14px;margin-top:6px;box-shadow:0 8px 24px rgba(232,69,95,.3)}
.lg-links{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:12px;font-size:12px;font-weight:700;color:var(--sub)}
.lg-links a{font-weight:900;color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.lg-agree{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7;margin-top:10px}
.lg-agree a{font-weight:900;color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.lg-child{display:grid;grid-template-columns:1fr;gap:8px}
.lg-chip{display:flex;gap:6px;flex-wrap:wrap}
.lg-chip span{font-size:12px;font-weight:900;border:1px solid var(--ink);padding:7px 10px;background:#fff;cursor:pointer}
.lg-chip span.on{background:var(--ink);color:var(--bg)}
.lg-app{margin-top:14px;display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;border:1px solid var(--line);padding:12px 14px;background:var(--card)}
.lg-app img{width:40px;height:40px}
.lg-app b{display:block;font-family:var(--fh);font-size:13px;font-weight:900}
.lg-app small{font-size:11px;font-weight:700;color:var(--sub)}
.lg-app a{font-size:12px;font-weight:900;border:1.5px solid var(--ink);padding:8px 12px;white-space:nowrap}
@media(min-width:900px){
  .lg-lay{grid-template-columns:1fr 440px;gap:40px;padding:36px 0 0;align-items:start}
  .lg-why{padding:40px 36px;min-height:520px;display:flex;flex-direction:column;justify-content:center}
  .lg-box{position:sticky;top:80px}
  .lg-p{padding:22px 24px 24px}
}
'''
GICON='<svg viewBox="0 0 24 24"><path fill="#4285F4" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.9h5.4c-.2 1.2-.9 2.3-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.4z"/><path fill="#34A853" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6C4.7 19.8 8.1 22 12 22z"/><path fill="#FBBC05" d="M6.4 14c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2V7.4H3.1C2.4 8.8 2 10.4 2 12s.4 3.2 1.1 4.6L6.4 14z"/><path fill="#EA4335" d="M12 5.9c1.5 0 2.8.5 3.8 1.5l2.8-2.8C17 3 14.7 2 12 2 8.1 2 4.7 4.2 3.1 7.4L6.4 10c.8-2.3 3-4.1 5.6-4.1z"/></svg>'
lg_body='''
<main><div class="wrap">
  <div class="note">【保護者の登録・ログイン v2（2026-09-12）】本番 login.html（Googleログイン＋メール。登録＝ニックネーム・本名（非表示）・地域（任意）・メール・パスワード、パスワードを忘れた方）を新デザインに。★左に「登録すると何ができるか」4つ（お気に入り／体験申込とメッセージ／診断の保存とお知らせ／保存した検索）、右にフォーム。ログイン／新規登録は**タブ**（`?mode=signup` で登録側）。新規登録に<b>お子さんの学年（任意・NEW）</b>を追加＝診断と体験申込フォームの自動入力に使う（DB：profiles.child_grade）。本名は「クラブに伝わる名前」として体験申込のときに使う説明を添えた。アプリ（App Store）への導線を下に。Apple ログインはアプリのみ（Webは Google＋メール）。</div>
  <div class="lg-lay">
    <div class="lg-why"><div class="bg"></div>
      <div class="ey">FOR PARENTS ・ FREE</div>
      <h1>うちの子に合うクラブを、<br><em>逃さない</em>。</h1>
      <p>登録しておくと、条件に合う新しいクラブや体験の募集がすぐ届きます。申込はお子さんの情報が自動で入るので、1分で済みます。</p>
      <ul>
        <li><i>1</i>新しいクラブをいち早くキャッチ<small>条件に合うクラブが載ったら、アプリとメールでお知らせ</small></li>
        <li><i>2</i>体験の申込が1分で済む<small>お子さんの情報は入力ずみ。クラブの返信もここに届きます</small></li>
        <li><i>3</i>気になるクラブを並べて比べる<small>♡ で残したクラブを、あとからまとめて見られます</small></li>
        <li><i>4</i>診断の結果から、次の可能性を見つける<small>合いそうな種目と近くのクラブを、いつでも見返せます</small></li>
      </ul>
      <span class="free">FREE ・ 1 MIN</span>
    </div>
    <div class="lg-box">
      <div class="lg-tabs" id="lgTabs"><button data-m="login" class="on">ログイン</button><button data-m="signup">新規登録（無料）</button></div>
      <div class="lg-p on" data-m="login">
        <a class="lg-g" href="#">%(g)s Googleでログイン</a>
        <div class="lg-or">または メールで</div>
        <div class="lg-f"><label>メールアドレス</label><input class="lg-in" type="email" placeholder="you@example.com"></div>
        <div class="lg-f"><label>パスワード</label><div class="lg-pw"><input class="lg-in" type="password" placeholder="••••••••"><span class="eye">表示</span></div></div>
        <a class="lg-btn" href="mypage-preview.html">ログイン ›</a>
        <div class="lg-links"><a href="#">パスワードを忘れた方</a><span>はじめての方は <a href="#" data-m="signup">新規登録</a></span></div>
        <div class="lg-app"><img src="assets/icon-192.png" alt="" onerror="this.style.display='none'"><div><b>アプリなら通知がすぐ届きます</b><small>体験の返信・新着クラブ・お知らせ</small></div><a href="#">アプリを開く</a></div>
      </div>
      <div class="lg-p" data-m="signup">
        <a class="lg-g" href="#">%(g)s Googleで登録</a>
        <div class="lg-or">または メールで</div>
        <div class="lg-f"><label>ニックネーム <span class="req">必須</span><span class="pv">サイトに表示されます</span></label><input class="lg-in" placeholder="例：はなまま"><div class="hint">口コミやコメントに出る名前です</div></div>
        <div class="lg-f"><label>お名前 <span class="req">必須</span><span class="pv">サイトには表示されません</span></label><div class="lg-row"><input class="lg-in" placeholder="姓（例：山田）"><input class="lg-in" placeholder="名（例：花子）"></div><div class="hint">体験を申し込むときに、クラブにだけ伝わります</div></div>
        <div class="lg-f"><label>お住まいの地域 <span class="opt">任意</span></label><div class="lg-row"><input class="lg-in" placeholder="都道府県"><input class="lg-in" placeholder="市区町村"></div><div class="hint">近くのクラブと、地域の新着のお知らせに使います</div></div>
        <div class="lg-f"><label>お子さんの学年 <span class="opt">任意</span></label><div class="lg-chip"><span>未就学</span><span>年長</span><span class="on">小1〜2</span><span>小3〜4</span><span>小5〜6</span><span>中学生</span></div><div class="hint">診断と体験申込のフォームに、自動で入ります。あとから変えられます</div></div>
        <div class="lg-f"><label>メールアドレス <span class="req">必須</span></label><input class="lg-in" type="email" placeholder="you@example.com"></div>
        <div class="lg-f"><label>パスワード <span class="req">必須</span></label><div class="lg-row"><input class="lg-in" type="password" placeholder="8文字以上"><input class="lg-in" type="password" placeholder="もう一度"></div></div>
        <a class="lg-btn" href="mypage-preview.html">無料で登録する ›</a>
        <div class="lg-agree">登録すると <a href="#">利用規約</a> と <a href="#">プライバシーポリシー</a> に同意したことになります。お知らせはいつでも止められます。</div>
        <div class="lg-links"><span>すでに登録している方は <a href="#" data-m="login">ログイン</a></span></div>
      </div>
    </div>
  </div>
  <div style="height:40px"></div>
</div></main>
'''%dict(g=GICON)
lg_js='''<script>
(function(){
 var tabs=document.getElementById('lgTabs');
 function show(m){document.querySelectorAll('.lg-p').forEach(function(p){p.classList.toggle('on',p.dataset.m===m)});tabs.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.m===m)})}
 tabs.addEventListener('click',function(e){var b=e.target.closest('button');if(b){show(b.dataset.m);history.replaceState(null,'','?mode='+b.dataset.m)}});
 document.addEventListener('click',function(e){var a=e.target.closest('a[data-m]');if(a){e.preventDefault();show(a.dataset.m)}var c=e.target.closest('.lg-chip span');if(c){c.parentNode.querySelectorAll('span').forEach(function(x){x.classList.toggle('on',x===c)})}var ey=e.target.closest('.eye');if(ey){var i=ey.parentNode.querySelector('input');i.type=i.type==='password'?'text':'password';ey.textContent=i.type==='password'?'表示':'隠す'}});
 var m=location.search.match(/mode=(login|signup)/);if(m)show(m[1]);
})();
</script>'''
page('login-preview.html','ログイン／新規登録｜チビスポ（プレビュー）',lg_body,lg_css,extra_js=lg_js)
