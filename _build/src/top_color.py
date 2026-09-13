# 色ツール：マスコットのコーラルピンク(#E85870)〜赤 の間でアクセント色を切り替えて比べる（プレビュー専用・全ページ共通）
import os
D=os.path.expanduser('~/kodomo-dooo-deploy/'); f=D+'video-hero-preview.html'
top=open(f,encoding='utf-8').read()
CSS='''/* ===================== COLOR TOOL ===================== */
#skins button.ct-btn{color:#ffd166}
#ctool{position:fixed;left:50%;bottom:58px;transform:translateX(-50%);z-index:121;width:min(92vw,560px);background:rgba(20,20,22,.94);color:#fff;border-radius:16px;padding:14px 16px 12px;box-shadow:0 10px 40px rgba(0,0,0,.35);backdrop-filter:blur(10px);font-family:'Zen Kaku Gothic New',system-ui,sans-serif;display:none}
#ctool.on{display:block}
#ctool .t{display:flex;justify-content:space-between;align-items:center;font-size:11px;letter-spacing:.14em;font-weight:900;margin-bottom:10px}
#ctool .t b{font-family:'Anton',sans-serif;font-weight:400;letter-spacing:.2em}
#ctool .t span{opacity:.7;font-weight:700;letter-spacing:.04em}
#ctool .sw{display:grid;grid-template-columns:repeat(9,1fr);gap:6px}
#ctool .sw button{aspect-ratio:1;border:2px solid transparent;border-radius:10px;cursor:pointer;padding:0;position:relative}
#ctool .sw button.on{border-color:#fff;box-shadow:0 0 0 2px rgba(0,0,0,.6)}
#ctool .sw button i{position:absolute;left:0;right:0;bottom:-16px;font-style:normal;font-size:8.5px;letter-spacing:.02em;opacity:.75;text-align:center;white-space:nowrap}
#ctool .lb{display:flex;justify-content:space-between;font-size:10px;opacity:.7;margin:22px 0 4px;font-weight:700}
#ctool input[type=range]{width:100%;accent-color:#fff}
#ctool .row{display:flex;gap:8px;align-items:center;margin-top:10px}
#ctool .cur{width:30px;height:30px;border-radius:8px;border:1px solid rgba(255,255,255,.4);flex:0 0 auto}
#ctool input[type=text]{flex:1;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:#fff;border-radius:8px;padding:7px 10px;font-size:13px;font-family:ui-monospace,Menlo,monospace;letter-spacing:.06em}
#ctool .row button{background:rgba(255,255,255,.12);border:0;color:#fff;border-radius:8px;padding:8px 12px;font-size:11.5px;font-weight:900;cursor:pointer;font-family:inherit}
#ctool .row button.ok{background:#fff;color:#111}
#ctool .nt{font-size:10.5px;opacity:.6;margin-top:8px;line-height:1.6}
@media(max-width:520px){#ctool{bottom:54px;padding:12px}#ctool .sw button i{display:none}}
'''
HTML=r'''<div id="ctool" role="dialog" aria-label="アクセント色">
  <div class="t"><b>ACCENT COLOR</b><span>マスコットのコーラルピンク → 赤</span></div>
  <div class="sw" id="ctSw"></div>
  <div class="lb"><span>ピンク寄り（マスコット）</span><span>赤寄り</span></div>
  <input type="range" id="ctRange" min="0" max="100" value="0">
  <div class="row"><span class="cur" id="ctCur"></span><input type="text" id="ctHex" value="#E85870" maxlength="7"><button id="ctApply" class="ok">この色にする</button><button id="ctReset">既定に戻す</button></div>
  <div class="nt">選んだ色は全ページに引き継がれます（この端末だけ）。URL に <code>?accent=%23D62828</code> を付けても同じ色で開けます。</div>
</div>
<script>
(function(){
  var A=[232,88,112], B=[204,28,28];            /* マスコット #E85870 → 赤 #CC1C1C */
  function hex(c){return '#'+c.map(function(v){v=Math.max(0,Math.min(255,Math.round(v)));return ('0'+v.toString(16)).slice(-2)}).join('').toUpperCase()}
  function rgb2hsl(r,g,b){r/=255;g/=255;b/=255;var M=Math.max(r,g,b),m=Math.min(r,g,b),h=0,s=0,l=(M+m)/2,d=M-m;if(d){s=l>.5?d/(2-M-m):d/(M+m);switch(M){case r:h=((g-b)/d+(g<b?6:0));break;case g:h=(b-r)/d+2;break;default:h=(r-g)/d+4}h*=60}return [h,s,l]}
  function hsl2rgb(h,s,l){h=((h%360)+360)%360;var c=(1-Math.abs(2*l-1))*s,x=c*(1-Math.abs((h/60)%2-1)),m=l-c/2,r,g,b;if(h<60){r=c;g=x;b=0}else if(h<120){r=x;g=c;b=0}else if(h<180){r=0;g=c;b=x}else if(h<240){r=0;g=x;b=c}else if(h<300){r=x;g=0;b=c}else{r=c;g=0;b=x}return [(r+m)*255,(g+m)*255,(b+m)*255]}
  function mix(t){var a=rgb2hsl.apply(null,A),b=rgb2hsl.apply(null,B);var ha=a[0],hb=b[0];if(ha>180)ha-=360;if(hb>180)hb-=360;var h=ha+(hb-ha)*t,s=a[1]+(b[1]-a[1])*t,l=a[2]+(b[2]-a[2])*t;return hex(hsl2rgb(h,s,l))}
  var KEY='chibispo_accent';
  function apply(c,save){
    if(!/^#[0-9a-f]{6}$/i.test(c))return; c=c.toUpperCase();
    document.body.style.setProperty('--accent',c);
    var r=parseInt(c.slice(1,3),16),g=parseInt(c.slice(3,5),16),b=parseInt(c.slice(5,7),16);
    document.body.style.setProperty('--accent-ink',(r*299+g*587+b*114)/1000>170?'#111':'#fff');
    var cur=document.getElementById('ctCur'),hx=document.getElementById('ctHex');if(cur)cur.style.background=c;if(hx&&hx.value.toUpperCase()!==c)hx.value=c;
    document.querySelectorAll('#ctSw button').forEach(function(b){b.classList.toggle('on',b.dataset.c===c)});
    var rg0=document.getElementById('ctRange');if(rg0){var best=0,bd=1e9;for(var k=0;k<=100;k++){var m=mix(k/100),dd=Math.abs(parseInt(m.slice(1,3),16)-r)+Math.abs(parseInt(m.slice(3,5),16)-g)+Math.abs(parseInt(m.slice(5,7),16)-b);if(dd<bd){bd=dd;best=k}}if(bd<40)rg0.value=best}
    if(save){try{localStorage.setItem(KEY,c)}catch(e){}}
  }
  function reset(){document.body.style.removeProperty('--accent');document.body.style.removeProperty('--accent-ink');try{localStorage.removeItem(KEY)}catch(e){}document.querySelectorAll('#ctSw button').forEach(function(b){b.classList.remove('on')});var cur=document.getElementById('ctCur');if(cur)cur.style.background='';}
  /* スウォッチ 9 段 */
  var sw=document.getElementById('ctSw'),NAMES=['マスコット','','','','中間','','','','赤'];
  for(var i=0;i<9;i++){var c=mix(i/8),b=document.createElement('button');b.style.background=c;b.dataset.c=c;b.title=c;b.innerHTML='<i>'+(NAMES[i]||c)+'</i>';b.addEventListener('click',function(){apply(this.dataset.c,true);document.getElementById('ctRange').value=Math.round([].indexOf.call(sw.children,this)/8*100)});sw.appendChild(b)}
  var rg=document.getElementById('ctRange');rg.addEventListener('input',function(){apply(mix(rg.value/100),true)});
  document.getElementById('ctApply').addEventListener('click',function(){apply(document.getElementById('ctHex').value.trim(),true)});
  document.getElementById('ctHex').addEventListener('keydown',function(e){if(e.key==='Enter')apply(this.value.trim(),true)});
  document.getElementById('ctReset').addEventListener('click',reset);
  /* 開閉ボタンをスキンバーに */
  var bar=document.getElementById('skins');if(bar){var tb=document.createElement('button');tb.className='ct-btn';tb.textContent='COLOR';tb.addEventListener('click',function(){document.getElementById('ctool').classList.toggle('on')});bar.appendChild(tb)}
  /* 初期化：URL ?accent= → localStorage */
  var q=new URLSearchParams(location.search),qa=q.get('accent');
  if(qa){apply(qa.charAt(0)==='#'?qa:'#'+qa,false)}else{try{var s=localStorage.getItem(KEY);if(s)apply(s,false)}catch(e){}}
  if(q.get('ctool')==='1')document.getElementById('ctool').classList.add('on');
})();
</script>
'''
if '/* ===================== COLOR TOOL' in top:
    a=top.index('/* ===================== COLOR TOOL'); b=top.index('/* ===================== HERO'); top=top[:a]+CSS+top[b:]
else:
    b=top.index('/* ===================== HERO'); top=top[:b]+CSS+top[b:]
mk='<button id="noteBtn">設計メモ</button>\n'
if '<div id="ctool"' in top:
    a=top.index('<div id="ctool"'); b=top.index('</script>',top.index('var A=[232,88,112]'))+9; top=top[:a]+HTML.rstrip('\n')+top[b:]
else:
    i=top.index(mk)+len(mk); top=top[:i]+HTML+top[i:]
open(f,'w',encoding='utf-8').write(top); print('color tool ok')
