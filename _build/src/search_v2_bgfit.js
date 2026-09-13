<script>
/* 背景の英字（地域×種目）を自動生成し、1行に収める。本番では AREA/SPORT の英語名をマスタから渡す */
(function(){
  var AREA={'世田谷区':'SETAGAYA','練馬区':'NERIMA','杉並区':'SUGINAMI','狛江市':'KOMAE','目黒区':'MEGURO','調布市':'CHOFU','川崎市高津区':'KAWASAKI TAKATSU','横浜市港北区':'YOKOHAMA KOHOKU','さいたま市':'SAITAMA','国立市':'KUNITACHI','武蔵野市':'MUSASHINO','東京都':'TOKYO'};
  var SPORT={'サッカー':'FOOTBALL','野球':'BASEBALL','バスケットボール':'BASKETBALL','バレーボール':'VOLLEYBALL','テニス':'TENNIS','水泳':'SWIMMING','ダンス':'DANCE','空手':'KARATE','剣道':'KENDO','体操':'GYMNASTICS','陸上':'ATHLETICS','新体操':'RHYTHMIC GYMNASTICS','ラグビー':'RUGBY','チアダンス':'CHEER DANCE','ラクロス':'LACROSSE'};
  var sec=document.querySelector('.s-head');if(!sec)return;
  var q=new URLSearchParams(location.search);
  if(q.get('area'))sec.dataset.area=q.get('area');
  if(q.get('sport'))sec.dataset.sport=q.get('sport');
  var h1=sec.querySelector('.s-h1 h1'),eb=sec.querySelector('.eyebrow'),cnt=sec.querySelector('.s-cnt'),dbg=document.getElementById('bgdbg');
  function hash(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;return h}
  function fit(){
    var bg=sec.querySelector('.bgw');if(!bg)return;
    if(/nobg=1/.test(location.search)){bg.style.display='none'}
    var area=sec.dataset.area||'世田谷区',sport=sec.dataset.sport||'サッカー';
    var a=(AREA[area]||area).toUpperCase(),s=(SPORT[sport]||sport).toUpperCase();
    if(eb)eb.textContent=a+' '+s;
    if(h1){h1.innerHTML=area+'の<em>'+sport+'</em>クラブ';
      var n=8+hash(area+sport)%18,v=Math.max(1,Math.round(n/4));
      if(cnt)cnt.innerHTML='<span><b>'+n+'</b><small>CLUBS</small></span><span class="sep"></span><span><b>'+v+'</b><small>WITH VIDEO</small></span>';
      document.title=area+'の'+sport+'クラブ '+n+'件｜チビスポ';}
    var mobile=innerWidth<760,pad=mobile?20:0;
    var W=sec.clientWidth-pad-(mobile?0:8);
    var MIN=mobile?44:104,MAX=Math.floor(Math.min(196,innerWidth*0.165));
    if(sec.dataset.bgmax){MAX=Math.min(MAX,+sec.dataset.bgmax);MIN=Math.min(MIN,MAX)}
    var cands=[a+' '+s,s,a],pick=null,size=MIN,why='';
    for(var i=0;i<cands.length;i++){
      bg.textContent=cands[i];bg.style.fontSize='100px';bg.style.width='max-content';
      var tw=bg.offsetWidth-pad;bg.style.width='';
      var f=Math.floor(100*W/tw*0.985);
      if(f>=MIN){pick=cands[i];size=Math.min(f,MAX);why=i===0?'両方':(i===1?'種目のみ（両方だと最小より小さくなる）':'地域のみ');break}
    }
    if(!pick){pick=cands[1];size=MIN;why='最小サイズで右を切る'}
    bg.textContent=pick;bg.style.fontSize=size+'px';
    if(dbg)dbg.textContent='背景: '+pick+' / '+size+'px / '+why;
  }
  function run(){fit();var d=document.getElementById('demo');if(d){d.hidden=false}}
  if(document.fonts&&document.fonts.load){document.fonts.load('100px Anton').then(run,run)}else run();
  addEventListener('resize',fit,{passive:true});
  /* プレビュー用：地域・種目の切替 */
  var da=document.getElementById('d-area'),ds=document.getElementById('d-sport');
  if(da&&ds){
    Object.keys(AREA).forEach(function(k){var o=document.createElement('option');o.textContent=k;da.appendChild(o)});
    Object.keys(SPORT).forEach(function(k){var o=document.createElement('option');o.textContent=k;ds.appendChild(o)});
    da.value=sec.dataset.area||'世田谷区';ds.value=sec.dataset.sport||'サッカー';
    da.addEventListener('change',function(){sec.dataset.area=da.value;fit()});
    ds.addEventListener('change',function(){sec.dataset.sport=ds.value;fit()});
  }
})();
</script>
