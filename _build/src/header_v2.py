# ヘッダー v2：本番（shared.js）のヘッダーから必要な導線を新デザインに移植する
# 対象：video-hero-preview.html の <style> 内 HEADER ブロックと <header>…</header>
import os,re
D=os.path.expanduser('~/kodomo-dooo-deploy/')
f=D+'video-hero-preview.html'
top=open(f,encoding='utf-8').read()

CSS='''/* ===================== HEADER ===================== */
header{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.hd{display:flex;align-items:center;justify-content:space-between;gap:18px;height:68px}
.logo{display:flex;align-items:center;flex:0 0 auto;color:var(--ink)}
.logo img{width:auto;display:block}
.logo .lg-w{height:44px}
.logo .lg-s{height:28px;display:none}
.logo-tg{display:none}
body[data-skin="stadium"] .logo img{background:#fff;padding:3px 7px;border-radius:6px}
.hd-nav{display:flex;align-items:center;gap:22px;margin-left:6px;flex:1 1 auto;min-width:0}
.hd-nav a{font-size:13.5px;font-weight:800;color:var(--ink);white-space:nowrap;position:relative;padding:6px 0}
.hd-nav a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--accent);transform:scaleX(0);transition:transform .18s}
.hd-nav a:hover::after,.hd-nav a.on::after{transform:scaleX(1)}
.hd-r{display:flex;align-items:center;gap:4px;flex:0 0 auto}
.hd-ic{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:54px;padding:5px 4px;font-size:10px;font-weight:800;color:var(--sub);border-radius:8px;line-height:1;white-space:nowrap}
.hd-ic svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.hd-ic:hover{color:var(--ink);background:color-mix(in srgb,var(--ink) 6%,transparent)}
.hd-av{width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900}
body[data-skin="stadium"] .hd-av{color:#0b0c0f}
.hd-cta{font-size:12.5px;font-weight:900;border:1.5px solid var(--ink);border-radius:999px;padding:9px 16px;margin-left:8px;white-space:nowrap}
body[data-skin="stadium"] .hd-cta{background:var(--accent);border-color:var(--accent);color:#0b0c0f}
body[data-skin="editorial"] .hd-cta{border-radius:0;letter-spacing:.1em}
.hd-burger{display:none;flex-direction:column;justify-content:center;gap:5px;width:42px;height:42px;margin-left:4px;border:0;background:transparent;cursor:pointer;padding:0 10px;border-radius:8px}
.hd-burger span{display:block;height:2px;background:var(--ink);border-radius:2px}
.hd-in{display:none!important}
body.auth-in .hd-out{display:none!important}
body.auth-in .hd-ic.hd-in{display:flex!important}
body.auth-in .sh-btn.hd-in{display:block!important}
/* ボトムシート（本番 cc-menu の移植。JSで body 末尾に足す） */
.sh-bd{position:fixed;inset:0;background:rgba(15,21,30,.45);z-index:1290;opacity:0;pointer-events:none;transition:opacity .25s}
.sh-bd.on{opacity:1;pointer-events:auto}
.sheet{position:fixed;left:0;right:0;bottom:0;margin:0 auto;width:100%;max-width:560px;background:var(--card);color:var(--ink);border-radius:22px 22px 0 0;box-shadow:0 -10px 40px rgba(0,0,0,.18);padding:14px 18px calc(24px + env(safe-area-inset-bottom));z-index:1300;max-height:88vh;overflow-y:auto;transform:translateY(110%);transition:transform .38s cubic-bezier(.32,.72,0,1);font-family:var(--f)}
.sheet.on{transform:translateY(0)}
body[data-skin="magazine"] .sheet,body[data-skin="editorial"] .sheet{border-radius:0}
.sh-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.sh-hd img{height:34px;width:auto;display:block}
body[data-skin="stadium"] .sh-hd img{background:#fff;padding:3px 6px;border-radius:6px}
.sh-x{border:0;background:transparent;font-size:24px;line-height:1;color:var(--sub);cursor:pointer;padding:4px 6px;font-family:inherit}
.sh-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.sh-grid a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;padding:14px 2px;border:1px solid var(--line);border-radius:12px;font-size:10.5px;font-weight:800;color:var(--ink);text-align:center;line-height:1.25;overflow-wrap:anywhere}
body[data-skin="magazine"] .sh-grid a,body[data-skin="editorial"] .sh-grid a{border-radius:0}
.sh-grid svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.sh-btn{display:block;text-align:center;font-weight:900;font-size:14px;border-radius:999px;padding:14px 0;margin-top:10px;border:1.5px solid var(--ink);color:var(--ink)}
.sh-btn.pri{background:var(--accent);border-color:var(--accent);color:#fff;margin-top:16px}
body[data-skin="stadium"] .sh-btn.pri{color:#0b0c0f}
body[data-skin="magazine"] .sh-btn,body[data-skin="editorial"] .sh-btn{border-radius:0}
.sh-ft{display:flex;justify-content:center;gap:18px;margin-top:14px;font-size:11.5px;font-weight:700;color:var(--sub)}
@media(max-width:1279px){.hd-nav{gap:16px}}
@media(max-width:1139px){.hd-nav{display:none}.hd-burger{display:flex}}
@media(max-width:759px){.logo .lg-w{display:none}.logo .lg-s{display:block}}
@media(max-width:759px){.hd-ic{display:none}.hd{height:56px;gap:10px}.logo img{height:26px}.hd-cta{padding:7px 11px;font-size:12px;margin-left:0}.hd-burger{margin-left:0}}
@media(max-width:380px){.sh-grid{gap:6px}.sh-grid a{padding:12px 2px;font-size:10px}}
'''

I={
 'search':'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>',
 'map':'<svg viewBox="0 0 24 24"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 'quiz':'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7"/><circle cx="12" cy="17" r=".6"/></svg>',
 'mag':'<svg viewBox="0 0 24 24"><path d="M4 5h7a2 2 0 0 1 2 2v13a1.5 1.5 0 0 0-1.5-1.5H4z"/><path d="M20 5h-7a2 2 0 0 0-2 2v13a1.5 1.5 0 0 1 1.5-1.5H20z"/></svg>',
 'about':'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="8" r=".6"/></svg>',
 'heart':'<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9z"/></svg>',
 'faq':'<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M12 8v3"/><circle cx="12" cy="13.5" r=".6"/></svg>',
 'biz':'<svg viewBox="0 0 24 24"><path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16"/><path d="M15 10h4a1 1 0 0 1 1 1v10"/><path d="M8 8h3M8 12h3M8 16h3M4 21h16"/></svg>',
 'user':'<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/></svg>',
 'mail':'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 'club':'<svg viewBox="0 0 24 24"><path d="M3 20h18"/><path d="M5 20V9l7-5 7 5v11"/><path d="M10 20v-5h4v5"/></svg>',
}

PREVIEW_LINKS=dict(home='video-hero-preview.html',search='search-preview.html',map='map-preview.html',about='about-preview.html',partner='partner-preview.html',fav='mypage-preview.html?tab=fav',clubmy='club-mypage-preview.html',login='login-preview.html',mypage='mypage-preview.html',listing='service-listing-preview.html',magazine='magazine-preview.html',faq='faq.html',contact='contact-preview.html',terms='legal.html#terms',privacy='legal.html#privacy',logo='assets/logo-sm.png',logow='assets/logo-wide.webp')
import json as _json
def sheet_html(L):
    return ('<div class="sh-bd" id="shBd"></div>'
    '<div class="sheet" id="sheet" role="dialog" aria-label="メニュー">'
    '<div class="sh-hd"><img src="%(logow)s" alt="チビスポ"><button class="sh-x" type="button" aria-label="閉じる">&times;</button></div>'
    '<div class="sh-grid">'
    '<a href="%(search)s">'+I['search']+'<span>クラブを探す</span></a>'
    '<a href="%(map)s">'+I['map']+'<span>地図から探す</span></a>'
    '<a href="%(magazine)s">'+I['mag']+'<span>マガジン</span></a>'
    '<a href="%(fav)s">'+I['heart']+'<span>お気に入り</span></a>'
    '<a href="%(about)s">'+I['about']+'<span>チビスポとは</span></a>'
    '<a href="%(faq)s">'+I['faq']+'<span>よくある質問</span></a>'
    '<a href="%(contact)s">'+I['mail']+'<span>お問い合わせ</span></a>'
    '<a href="%(partner)s">'+I['biz']+'<span>クラブ・<br>事業者の方へ</span></a>'
    '</div>'
    '<a class="sh-btn pri" href="%(listing)s">クラブを載せる（無料から）</a>'
    '<a class="sh-btn hd-out" href="%(login)s">一般（保護者）ログイン / 会員登録</a>'
    '<a class="sh-btn hd-out" href="%(clubmy)s">クラブ運営者ログイン（掲載・管理）</a>'
    '<a class="sh-btn hd-in" href="%(mypage)s">マイページ</a>'
    '<div class="sh-ft"><a href="%(terms)s">利用規約</a><a href="%(privacy)s">プライバシーポリシー</a></div>'
    '</div>')%L
def header_html(L,wrap='wrap'):
    return ('<header class="site-hd">\n  <div class="'+wrap+' hd">\n'
    '    <a class="logo" href="%(home)s"><img class="lg-w" src="%(logow)s" alt="チビスポ｜地域スポーツを、もっと身近に。" width="700" height="220"><img class="lg-s" src="%(logo)s" alt="チビスポ" width="300" height="72"></a>\n'
    '    <nav class="hd-nav">\n'
    '      <a href="%(search)s">クラブを探す</a>\n'
    '      <a href="%(map)s">地図から探す</a>\n'
    '      <a href="%(about)s">チビスポとは</a>\n'
    '      <a href="%(partner)s">クラブ・事業者の方へ</a>\n'
    '    </nav>\n'
    '    <div class="hd-r">\n'
    '      <a class="hd-ic" href="%(fav)s">'+I['heart']+'<span>お気に入り</span></a>\n'
    '      <a class="hd-ic hd-out" href="%(clubmy)s">'+I['club']+'<span>クラブログイン</span></a>\n'
    '      <a class="hd-ic hd-out" href="%(login)s">'+I['user']+'<span>ログイン</span></a>\n'
    '      <a class="hd-ic hd-in" href="%(mypage)s"><span class="hd-av">M</span><span>マイページ</span></a>\n'
    '      <a class="hd-cta" href="%(listing)s">クラブを載せる</a>\n'
    '      <button class="hd-burger" type="button" aria-label="メニューを開く"><span></span><span></span><span></span></button>\n'
    '    </div>\n  </div>\n')%L
# シートの開閉・アクティブ表示・ログイン判定（プレビュー用。本番は shared.js が同じことをする）
def header_js(L):
    return ('<script>\n(function(){\n  var SHEET='+_json.dumps(sheet_html(L),ensure_ascii=False)+';\n'
    r'''  function init(){
      document.body.insertAdjacentHTML('beforeend',SHEET);
      var bd=document.getElementById('shBd'),sh=document.getElementById('sheet'),open=false;
      function set(v){open=v;bd.classList.toggle('on',v);sh.classList.toggle('on',v);document.documentElement.style.overflow=v?'hidden':'';}
      document.querySelectorAll('.hd-burger').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();set(!open);});});
      bd.addEventListener('click',function(){set(false);});
      sh.querySelector('.sh-x').addEventListener('click',function(){set(false);});
      sh.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){set(false);});});
      document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false);});
      var here=(location.pathname.split('/').pop()||'index.html');
      document.querySelectorAll('.hd-nav a').forEach(function(a){if(a.getAttribute('href').split('?')[0]===here)a.classList.add('on');});
      var inn=/[?&]login=1/.test(location.search);
      try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i),v=localStorage.getItem(k);if(/^sb-.*-auth/.test(k)&&v&&v!=='null')inn=true;}}catch(e){}
      if(inn)document.body.classList.add('auth-in');
    }
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  })();
  </script>
''')
HEADER=header_html(PREVIEW_LINKS)+header_js(PREVIEW_LINKS)+'</header>'
_OLD_HEADER='''<header>
  <div class="wrap hd">
    <a class="logo" href="video-hero-preview.html"><img src="assets/logo-sm.png" alt="チビスポ"><span class="logo-tg">地域スポーツを、もっと身近に。</span></a>
    <nav class="hd-nav">
      <a href="search-preview.html">クラブを探す</a>
      <a href="map-preview.html">地図から探す</a>
      <a href="about-preview.html">チビスポとは</a>
      <a href="partner-preview.html">クラブ・事業者の方へ</a>
    </nav>
    <div class="hd-r">
      <a class="hd-ic" href="mypage-preview.html?tab=fav">%(heart)s<span>お気に入り</span></a>
      <a class="hd-ic hd-out" href="club-mypage-preview.html">%(club)s<span>クラブログイン</span></a>
      <a class="hd-ic hd-out" href="login-preview.html">%(user)s<span>ログイン</span></a>
      <a class="hd-ic hd-in" href="mypage-preview.html"><span class="hd-av">M</span><span>マイページ</span></a>
      <a class="hd-cta" href="service-listing-preview.html">クラブを載せる</a>
      <button class="hd-burger" type="button" aria-label="メニューを開く"><span></span><span></span><span></span></button>
    </div>
  </div>
  <script>
  (function(){
    var SHEET='<div class="sh-bd" id="shBd"></div>'
    +'<div class="sheet" id="sheet" role="dialog" aria-label="メニュー">'
    +'<div class="sh-hd"><img src="assets/logo-sm.png" alt="チビスポ"><button class="sh-x" type="button" aria-label="閉じる">&times;</button></div>'
    +'<div class="sh-grid">'
    +'<a href="search-preview.html">%(search)s<span>クラブを探す</span></a>'
    +'<a href="map-preview.html">%(map)s<span>地図から探す</span></a>'
    +'<a href="magazine-preview.html">%(mag)s<span>マガジン</span></a>'
    +'<a href="mypage-preview.html?tab=fav">%(heart)s<span>お気に入り</span></a>'
    +'<a href="about-preview.html">%(about)s<span>チビスポとは</span></a>'
    +'<a href="faq.html">%(faq)s<span>よくある質問</span></a>'
    +'<a href="contact-preview.html">%(mail)s<span>お問い合わせ</span></a>'
    +'<a href="partner-preview.html">%(biz)s<span>クラブ・<br>事業者の方へ</span></a>'
    +'</div>'
    +'<a class="sh-btn pri" href="service-listing-preview.html">クラブを載せる（無料から）</a>'
    +'<a class="sh-btn hd-out" href="login-preview.html">一般（保護者）ログイン / 会員登録</a>'
    +'<a class="sh-btn hd-out" href="club-mypage-preview.html">クラブ運営者ログイン（掲載・管理）</a>'
    +'<a class="sh-btn hd-in" href="mypage-preview.html">マイページ</a>'
    +'<div class="sh-ft"><a href="legal.html#terms">利用規約</a><a href="legal.html#privacy">プライバシーポリシー</a></div>'
    +'</div>';
    function init(){
      document.body.insertAdjacentHTML('beforeend',SHEET);
      var bd=document.getElementById('shBd'),sh=document.getElementById('sheet'),open=false;
      function set(v){open=v;bd.classList.toggle('on',v);sh.classList.toggle('on',v);document.documentElement.style.overflow=v?'hidden':'';}
      document.querySelectorAll('.hd-burger').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();set(!open);});});
      bd.addEventListener('click',function(){set(false);});
      sh.querySelector('.sh-x').addEventListener('click',function(){set(false);});
      sh.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){set(false);});});
      document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false);});
      var here=(location.pathname.split('/').pop()||'index.html');
      document.querySelectorAll('.hd-nav a').forEach(function(a){if(a.getAttribute('href').split('?')[0]===here)a.classList.add('on');});
      var inn=/[?&]login=1/.test(location.search);
      try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i),v=localStorage.getItem(k);if(/^sb-.*-auth/.test(k)&&v&&v!=='null')inn=true;}}catch(e){}
      if(inn)document.body.classList.add('auth-in');
    }
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  })();
  </script>
</header>'''

def patch_preview():
    global top
    top=open(f,encoding='utf-8').read()
    # --- CSS 差し替え：HEADER ブロック（/* === HEADER === */ から /* === HERO === */ の手前まで）
    a=top.index('/* ===================== HEADER ===================== */')
    # HEADER の次に来るブロックまで（QUIZ BAND が入っていることがある）
    b=min(i for i in [top.find('/* ===================== QUIZ BAND'),top.find('/* ===================== HERO')] if i>a)
    old_block=top[a:b]
    # 520px の共通メディア行（.sec-h の分）はヘッダー分だけ削って残す
    m=re.search(r'@media\(max-width:520px\)\{[^\n]*\}\n',old_block)
    keep=''
    if m:
        line=m.group(0)
        line=line.replace('.hd-link{display:none}','').replace('.hd-cta{padding:7px 11px;font-size:12px}','').replace('.hd{height:56px}','').replace('.logo{font-size:19px}','')
        keep='\n'+line
    top=top[:a]+CSS+keep+top[b:]

    # --- 旧 .logo span 由来の他所参照は無し（確認済み）。markup 差し替え
    h1=top.index('<header'); h2=top.index('</header>')+9
    top=top[:h1]+HEADER+top[h2:]
    open(f,'w',encoding='utf-8').write(top)
    print('patched: css',len(CSS),'bytes; header',len(HEADER),'bytes')

if __name__=='__main__':
    patch_preview()
