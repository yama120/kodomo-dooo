<script>
/* ============ 描画：いま ============ */
function isPro(){return !!(D&&D.club&&D.club.pro);}
function spark(arr,color){
  if(!arr||arr.length<2||!arr.some(function(v){return v>0;}))return '';
  var W=200,H=34,max=Math.max.apply(null,arr.concat([1]));
  var pts=arr.map(function(v,i){return [i*(W/(arr.length-1)), H-2-(H-6)*v/max];});
  var d=pts.map(function(p,i){return (i?'L':'M')+p[0].toFixed(1)+','+p[1].toFixed(1);}).join('');
  return '<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none"><path d="'+d+'L'+W+','+H+'L0,'+H+'Z" fill="'+color+'" opacity=".12"/><path d="'+d+'" fill="none" stroke="'+color+'" stroke-width="2"/></svg>';
}
function trialsByMonth(){return (D&&D.trials&&D.trials.by_month)||{};}
function renderMove(){
  var el=$('#secMove'), ar=(D&&D.ai_report)||{}, rep=ar.report||[], q=ar.quota||{used:0,limit:3}, left=Math.max(0,(q.limit||3)-(q.used||0));
  var when=ar.at?new Date(ar.at):null, dateStr=(when&&!isNaN(when))?((when.getMonth()+1)+'月'+when.getDate()+'日'):'';
  var pri={'高':0,'中':1,'低':2}; rep=rep.slice().sort(function(a,b){return (pri[a.p]||0)-(pri[b.p]||0);});
  var top=rep[0], alts=rep.slice(1);
  var genBtn='<button class="btn s o" id="aiGen" '+(left<=0?'disabled':'')+'>'+(top?'更新する':'AIに提案してもらう')+'</button><span class="hint">本日 '+(q.used||0)+'/'+(q.limit||3)+'回</span>';
  if(DEMO)genBtn='<span class="hint">実データでは、ボタン1つでAIが今週の一手を出します（1日3回まで）</span>';
  if(!top){
    el.innerHTML='<div class="move"><div class="k">THIS WEEK ・ 今週の一手</div><h3>実データから「今週やること」を1つに絞って提案します</h3><p>閲覧・申込・投稿・アンケートの数字をもとに、優先度をつけて3つ。データが少ないうちは「まず何を計測するか」から。</p><div class="more">'+genBtn+'</div></div>';
    return;
  }
  el.innerHTML='<div class="move" id="moveBox"><div class="k">THIS WEEK ・ 今週の一手'+(dateStr?'<span class="hint" style="letter-spacing:0;color:var(--mute)">'+dateStr+' 生成</span>':'')+'</div>'
    +'<h3>'+esc(top.title)+'</h3><p>'+esc(top.body)+'</p>'+(top.why?'<div class="why">'+esc(top.why)+'</div>':'')
    +'<div class="more">'+(alts.length?'<button class="btn s" id="moveMore">ほかの'+alts.length+'つも見る</button>':'')+genBtn+'</div>'
    +(alts.length?'<div class="alt">'+alts.map(function(a){return '<div class="it"><span class="tag '+(a.p==='中'?'p2':'p3')+'">'+(a.p==='中'?'次の候補':'伸びしろ')+'</span> <b>'+esc(a.title)+'</b><span>'+esc(a.body)+'</span></div>';}).join('')+'</div>':'')+'</div>';
  var mm=$('#moveMore'); if(mm)mm.onclick=function(){var b=$('#moveBox');b.classList.toggle('open');mm.textContent=b.classList.contains('open')?'閉じる':'ほかの'+alts.length+'つも見る';};
  var g=$('#aiGen'); if(g)g.onclick=function(){genReport(g);};
}
function renderKPI(){
  var a=(D&&D.analytics&&D.analytics.club)||null, days=(D&&D.analytics&&D.analytics.range&&D.analytics.range.lookback_days)||30;
  var views=a?(+a.views||0):null, daily=((a&&a.daily)||[]).map(function(x){return +x.views||0;});
  var ms=monthsBack(6), bm=trialsByMonth(), thisM=ms[5].key, lastM=ms[4].key;
  var tThis=(+bm[thisM]||0)+getNum('trial_manual',0)*0, tLast=+bm[lastM]||0; // 手動分は累計なので月には足さない
  var tTotal=(D&&D.trials?(+D.trials.total||0):0)+getNum('trial_manual',0);
  var jm=joinsData(), jThis=+(jm[thisM]||0), jLast=+(jm[lastM]||0);
  var members=getNum('members',0), goal=getNum('goal',40), pct=goal>0?Math.min(100,Math.round(members/goal*100)):0;
  var delta=function(cur,prev){if(prev==null)return '';var d=cur-prev;if(d===0)return '<span>先月と同じ</span>';return '<span class="'+(d>0?'up':'dn')+'">'+(d>0?'▲':'▼')+Math.abs(d)+' vs 先月</span>';};
  $('#kpiWin').textContent='閲覧は過去'+days+'日、申込・入会は今月';
  $('#kpi').innerHTML=
    '<div class="card kpi"><div class="lb">クラブページ閲覧<span class="win">'+days+' DAYS</span></div><div class="v">'+(views==null?'<span style="color:#c3c3c3">—</span>':fmtN(views))+'</div><div class="d">'+(views==null?'掲載ページが見られると出ます':'自動計測（'+fmtN(a.users||0)+'人が訪問）')+'</div>'+spark(daily,'#2a6fdb')+'</div>'
    +'<div class="card kpi"><div class="lb">体験申込<span class="win">MONTH</span></div><div class="v">'+fmtN(tThis)+'<small>件</small></div><div class="d">'+delta(tThis,tLast)+'　累計 <b>'+fmtN(tTotal)+'</b> <button class="ed" data-rec="体験・見学の申込">＋記録</button></div>'+spark(ms.map(function(m){return +bm[m.key]||0;}),'#1f8a5b')+'</div>'
    +'<div class="card kpi"><div class="lb">入会<span class="win">MONTH</span></div><div class="v">'+fmtN(jThis)+'<small>人</small></div><div class="d">'+delta(jThis,jLast)+(joinsAvg()!=null?'　月平均 <b>'+joinsAvg()+'人</b>':'')+' <button class="ed" data-rec="入会が決まった">＋記録</button></div>'+spark(ms.map(function(m){return +(jm[m.key]||0);}),'#E43B4D')+'</div>'
    +'<div class="card kpi"><div class="lb">会員数<span class="win">GOAL</span></div><div class="v">'+fmtN(members)+'<small>/ '+fmtN(goal)+'人</small></div><div class="pbar"><i style="width:'+pct+'%"></i></div><div class="d" style="margin-top:6px">あと<b>'+Math.max(0,goal-members)+'人</b>（'+pct+'%） <button class="ed" data-edit="members">会員数</button> <button class="ed" data-edit="goal">目標</button></div></div>';
  // 逆算：実績の転換率（無ければ目安）で「あと何件の申込・何回の閲覧」が要るか
  var remain=Math.max(0,goal-members);
  var trialsAll=(D&&D.trials?(+D.trials.total||0):0)+getNum('trial_manual',0), joinsAll=joinsTotal();
  var rTJ=(trialsAll>=5&&joinsAll>0)?Math.min(.9,joinsAll/trialsAll):.45;
  // 閲覧は過去30日なので、申込も同じ長さ（今月＋先月の残り日数ぶん）で見る
  var now=new Date(), dim=new Date(now.getFullYear(),now.getMonth(),0).getDate(), t30=(+bm[thisM]||0)+Math.round((+bm[lastM]||0)*Math.max(0,30-now.getDate())/dim);
  var rVT=(views&&t30>0)?Math.min(.2,t30/views):.02;
  var needT=Math.ceil(remain/rTJ), needV=Math.ceil(needT/rVT);
  var pace=(joinsAvg()||0)>0?Math.ceil(remain/joinsAvg()):null;
  $('#rev').innerHTML=remain>0
    ? 'あと<b>'+remain+'人</b>の入会に必要な量（'+(trialsAll>=5&&joinsAll>0?'実績から逆算':'一般的な目安で計算')+'）：体験申込 <b>約'+needT+'件</b> ＝ ページ閲覧 <b>約'+fmtN(needV)+'回</b><small>'+(pace?'今のペース（月'+joinsAvg()+'人）だと約'+pace+'ヶ月。':'入会を「＋記録」で残すと、今のペースが出ます。')+'上の「今週の一手」で加速します。</small>'
    : '目標の会員数に達しています。<small>次の目標は「目標」ボタンから変えられます。</small>';
}
function renderTrend(){
  var ms=monthsBack(6), bm=trialsByMonth(), jm=joinsData();
  var trials=ms.map(function(m){return +bm[m.key]||0;}), joins=ms.map(function(m){return +(jm[m.key]||0);});
  var postM={};((D&&D.post_stats)||[]).forEach(function(s){var m=String(s.period_start).slice(0,7);postM[m]=(postM[m]||0)+(+s.post_count||0);});
  var posts=ms.map(function(m){return postM[m.key]||0;});
  var recs=recList().filter(function(r){return isPolicy(r.k);});
  var W=640,H=214,L=30,R=16,T=18,B=44,pw=(W-L-R)/6;
  var max=Math.max.apply(null,trials.concat(joins,[1]));
  var y=function(v){return T+(H-T-B)*(1-v/max);};
  var s='';
  for(var g=0;g<=2;g++){var gy=T+(H-T-B)*g/2;s+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+gy+'" y2="'+gy+'" stroke="#e5e8ec" stroke-dasharray="2 4"/>';}
  ms.forEach(function(m,i){var cx=L+pw*(i+.5);
    var bw=pw*.34; s+='<rect x="'+(cx-bw)+'" y="'+y(trials[i])+'" width="'+bw+'" height="'+(H-B-y(trials[i]))+'" fill="#1f8a5b" opacity=".85"><title>'+m.label+' 体験申込 '+trials[i]+'件</title></rect>';
    s+='<rect x="'+cx+'" y="'+y(joins[i])+'" width="'+bw+'" height="'+(H-B-y(joins[i]))+'" fill="#E43B4D"><title>'+m.label+' 入会 '+joins[i]+'人</title></rect>';
    if(trials[i])s+='<text x="'+(cx-bw/2)+'" y="'+(y(trials[i])-4)+'" text-anchor="middle" font-size="10" font-weight="800" fill="#1f8a5b">'+trials[i]+'</text>';
    if(joins[i])s+='<text x="'+(cx+bw/2)+'" y="'+(y(joins[i])-4)+'" text-anchor="middle" font-size="10" font-weight="800" fill="#E43B4D">'+joins[i]+'</text>';
    s+='<text x="'+cx+'" y="'+(H-26)+'" text-anchor="middle" font-size="11" font-weight="800" fill="#1f2430">'+m.label+'</text>';
    if(posts[i])s+='<text x="'+cx+'" y="'+(H-10)+'" text-anchor="middle" font-size="9.5" fill="#8a93a0">投稿 '+posts[i]+'本</text>';
  });
  var marks=recs.map(function(r,i){var idx=ms.findIndex(function(m){return r.d.slice(0,7)===m.key;});if(idx<0)return '';var day=+r.d.slice(8,10)||15;var cx=L+pw*idx+pw*Math.min(1,day/31);
    return '<line x1="'+cx+'" x2="'+cx+'" y1="'+(T-6)+'" y2="'+(H-B)+'" stroke="#1f2430" stroke-width="1.2" stroke-dasharray="3 3"/><circle cx="'+cx+'" cy="'+(T-6)+'" r="7" fill="#1f2430"/><text x="'+cx+'" y="'+(T-3)+'" text-anchor="middle" font-size="9" font-weight="900" fill="#fff">'+(i+1)+'</text>';}).join('');
  var legend='<div class="lg"><span><i style="background:#1f8a5b"></i>体験申込</span><span><i style="background:#E43B4D"></i>入会</span>'+(recs.length?'<span><i style="background:#1f2430"></i>施策</span>':'')+'</div>'
    +(recs.length?'<div class="note">'+recs.map(function(r,i){return '<b>'+(i+1)+'</b> '+esc(r.d.slice(5).replace('-','/'))+' '+esc(r.m||r.k.replace(/^..\s?/,''));}).join('　')+'</div>':'<div class="note">ポスター掲示・チラシ配布などをすると、ここに番号の縦線が立ちます。「その後に数字が動いたか」で効いたかどうかが見えます。</div>');
  $('#trend').innerHTML='<svg viewBox="0 0 '+W+' '+H+'">'+s+marks+'</svg>'+legend;
}

/* ============ 描画：集客 ============ */
function renderFunnel(){
  var snsViews=0;((D&&D.post_stats)||[]).forEach(function(s){snsViews+=(+s.total_views||0);});
  var a=(D&&D.analytics&&D.analytics.club)||null, views=a?(+a.views||0):0, days=(D&&D.analytics&&D.analytics.range&&D.analytics.range.lookback_days)||30;
  var trials=(D&&D.trials?(+D.trials.total||0):0)+getNum('trial_manual',0);
  var attend=(D&&D.trials?(+D.trials.attended||0):0)+getNum('attend',0);
  var joins=joinsTotal()||(D&&D.trials?(+D.trials.joined||0):0);
  var st=[
    {n:'認知',s:'SNSで表示された回数',src:'AUTO',v:snsViews,pro:true},
    {n:'流入',s:'クラブページに来た人',src:'AUTO',v:views,bench:[2,5],fix:{t:'表示はされているのに、来てもらえていない',b:'投稿の最後に「プロフィールのリンクから体験へ」の一言と、プロフィール文の整理で改善できます。'}},
    {n:'体験申込',s:'フォームは自動・電話は記録',src:'AUTO+手動',v:trials,bench:[1,3],rec:'体験・見学の申込',fix:{t:'ページを見た人が、申込まで進んでいない',b:'写真・体験の流れ・料金の明記が申込率を左右します。まずクラブページの写真と紹介文を見直しましょう。'}},
    {n:'体験参加',s:'受信箱で「体験に来た」にすると自動',src:'AUTO+手動',v:attend,bench:[60,90],rec:'体験・見学に参加',fix:{t:'申し込んだのに、来ていない人がいる',b:'前日のリマインド（LINE・SMS）だけで大きく改善します。日程変更の受け皿も効きます。'}},
    {n:'入会',s:'「＋記録」から月ごとに',src:'手動',v:joins,bench:[40,70],rec:'入会が決まった',fix:{t:'体験には来るが、入会に至っていない',b:'体験当日の「入会案内のひと押し」と初月の特典で変わります。'}}
  ];
  if(!isPro())st=st.filter(function(x){return !x.pro;});
  $('#fnWin').textContent='閲覧は過去'+days+'日、申込以降は累計';
  var max=Math.max.apply(null,st.map(function(x){return x.v;}).concat([1])), weakest=null, html='';
  st.forEach(function(x,i){
    var rate='';
    if(i>0&&x.bench){var prev=st[i-1].v; if(prev>0){var r=x.v/prev*100, bad=r<x.bench[0]; if(bad&&!weakest&&x.fix)weakest=x; rate='<span class="rt '+(bad?'ng':'ok')+'">'+(r<10?r.toFixed(1):Math.round(r))+'%・'+(bad?'目安未満':'良好')+'</span>';} else rate='<span class="rt na">—</span>';}
    var w=x.v>0?Math.max(2,100*Math.sqrt(x.v/max)):0;
    html+='<div class="st"><div class="nm">'+x.n+'<span class="src">'+x.src+'</span><span class="hint">'+x.s+'</span>'+(x.rec?' <button class="ed" data-rec="'+x.rec+'">＋記録</button>':'')+'</div><div class="val num">'+fmtN(x.v)+rate+'</div><div class="bar2"><i style="width:'+w+'%;opacity:'+(1-i*.13)+'"></i></div></div>';
  });
  if(weakest)html+='<div class="bn"><div class="k">BOTTLENECK ・ いちばん弱い段階</div><h3>'+weakest.fix.t+'</h3><p>'+weakest.fix.b+'<span class="hint">（目安：'+weakest.bench[0]+'〜'+weakest.bench[1]+'%）</span></p></div>';
  html+='<div class="note">％の目安は子ども向けスポーツクラブの一般的なレンジ。<b>数字が0の段階が「次にやること」</b>です。</div>';
  $('#funnel').innerHTML=html;
}
function chName(c){return RESERVED[c.slug]||c.name||c.slug;}
function renderSources(){
  var el=$('#sources'), a=(D&&D.analytics&&D.analytics.club)||null, ch=(a&&a.channels)||{};
  var map={'Organic Social':'SNSから','Direct':'直接・アプリ','Organic Search':'検索から','Referral':'他サイトから','Unassigned':'不明','(other)':'その他','Paid Social':'SNS広告'};
  var rows=Object.keys(ch).map(function(k){return [map[k]||k,+ch[k]||0];}).sort(function(x,y){return y[1]-x[1];}), tot=rows.reduce(function(s,r){return s+r[1];},0)||1;
  var ga='<div class="card"><div class="sh" style="margin-bottom:6px"><div class="l"><b style="font-size:13.5px">チビスポのページに、どこから来たか</b><span class="hint">アクセス解析（過去30日・自動）</span></div></div>'
    +(rows.length?'<div class="tb">'+rows.map(function(r){var p=Math.round(r[1]/tot*100);return '<div class="r"><span>'+esc(r[0])+'</span><div class="b"><i style="width:'+p+'%;background:#1f2430"></i></div><span class="v num">'+fmtN(r[1])+' <span class="hint">'+p+'%</span></span></div>';}).join('')+'</div>':'<div class="empty">掲載ページが見られると、ここに内訳が出ます</div>')+'</div>';
  if(!isPro()){
    el.innerHTML=ga+'<div class="lock" style="margin-top:10px"><div class="k">PRO ・ プロプランで見えるもの</div><h3>ポスター・チラシ・SNSごとの流入</h3><p>媒体ごとにQR・計測リンクを発行すると、どの発信が何人をクラブページまで運んだかが横並びで分かります。広報の当たり外れが数字で見えます。</p><a class="btn s a" href="/listing.html#plans">プロプランを見る</a></div>';
    $('#addMediaBtn').style.display='none'; return;
  }
  var chans=(D&&D.clicks&&D.clicks.channels)||[], max=Math.max.apply(null,chans.map(function(c){return c.clicks;}).concat([1]));
  var table='<div class="card"><div class="sh" style="margin-bottom:6px"><div class="l"><b style="font-size:13.5px">あなたが配ったQR・リンクごとの流入</b><span class="hint">計測リンク経由（過去30日・自動）</span></div></div>'
    +(chans.length?'<div class="tw"><table class="t"><thead><tr><th>媒体</th><th>種類</th><th class="n">流入</th><th style="width:90px"></th><th></th></tr></thead><tbody>'
      +chans.map(function(c){return '<tr><td><b>'+esc(chName(c))+'</b></td><td><span class="kind">'+esc(KIND_LABEL[c.kind]||c.kind||'—')+'</span></td><td class="n num">'+fmtN(c.clicks)+'</td><td><div class="mb"><i style="width:'+Math.round(c.clicks/max*100)+'%"></i></div></td><td><button class="link" data-qr="'+esc(c.slug)+'" data-nm="'+esc(chName(c))+'">リンク／QR</button></td></tr>';}).join('')+'</tbody></table></div>'
      :'<div class="empty">まだ計測リンクからのアクセスがありません。<br>「＋ QR・計測リンクを作る」で、ポスターやチラシ用のQRを発行できます。</div>')+'</div>';
  el.innerHTML=table+ga;
}
function renderSurvey(){
  var sv=(D&&D.survey)||null, counts=(sv&&sv.result&&sv.result.counts)||{}, numeric=(sv&&sv.result&&sv.result.numeric)||{}, bench=(sv&&sv.benchmark)||{}, total=(sv&&sv.total)||0, prov=!!(sv&&sv.form_url);
  var q=(sv&&sv.quota)||{}, rLeft=Math.max(0,(q.refresh_limit||10)-(q.refresh_used||0)), aLeft=Math.max(0,(q.advice_limit||5)-(q.advice_used||0));
  $('#svCount').textContent=total?('回答 '+total+'件'):'';
  var items=Object.keys(counts).map(function(k){return [k,counts[k]];}).sort(function(x,y){return y[1]-x[1];}), max=Math.max.apply(null,[1].concat(items.map(function(x){return x[1];})));
  var html='';
  if(total&&items.length){html+='<b style="font-size:13.5px">どこでクラブを知ったか</b>'+items.map(function(it){var p=Math.round(it[1]/total*100);return '<div class="r"><span>'+esc(it[0])+'</span><div class="b"><i style="width:'+Math.round(it[1]/max*100)+'%"></i></div><span class="num">'+it[1]+'人 <span class="hint">'+p+'%</span></span></div>';}).join('');}
  else html+='<div class="empty">'+(prov?'まだ回答がありません。QRやURLを保護者に配ると、ここに集まります。':'ボタン1つでアンケート（Googleフォーム）を作れます。回答は毎朝自動で集計されます。')+'</div>';
  var keys=Object.keys(numeric);
  if(keys.length){html+='<div class="tiles">'+keys.map(function(k){var m=numeric[k],b=bench[k],nps=typeof m.nps==='number';var mv=nps?m.nps:m.avg,bv=b?(nps?b.nps:b.avg):null;var cmp=(b&&b.clubs>1&&bv!=null)?('<div class="c '+(mv>=bv?'up':'dn')+'">'+(mv>=bv?'▲':'▼')+' 他クラブ平均 '+bv+'</div>'):'<div class="c">他クラブとの比較は参加クラブが増えると出ます</div>';
    return '<div class="tile"><div class="l">'+esc(String(k).slice(0,18))+'</div><div class="v">'+(nps?('NPS '+(m.nps>0?'+':'')+m.nps):(m.avg+'<small>/'+(m.max<=5?5:m.max)+'</small>'))+'</div>'+cmp+'</div>';}).join('')+'</div>';}
  var adv=(sv&&sv.advice)||'';
  if(total)html+='<div class="adv"><div class="sh" style="margin-bottom:4px"><b style="font-size:13.5px">AIの改善アドバイス</b><span><span class="hint">本日 '+(q.advice_used||0)+'/'+(q.advice_limit||5)+'回</span> <button class="btn s o" id="svAdv" '+(aLeft<=0||DEMO?'disabled':'')+'>'+(adv?'更新':'生成する')+'</button></span></div><div id="svAdvBody">'+(adv?advHtml(adv):'<span class="hint">「生成する」を押すと、集計と全クラブ平均をもとに次の一手を提案します。</span>')+'</div></div>';
  html+='<div class="foot">'+(prov
    ? '<button class="btn s o" id="svQR">QRコード</button><button class="btn s o" id="svURL">URLをコピー</button><button class="btn s o" id="svRefresh" '+(rLeft<=0||DEMO?'disabled':'')+'>最新の回答を取り込む</button>'+(sv.edit_url&&sv.edit_url!=='#'?'<a class="btn s o" href="'+esc(sv.edit_url)+'" target="_blank" rel="noopener">質問を編集 ↗</a>':'')
    : '<button class="btn s" id="svMake" '+(DEMO?'disabled':'')+'>＋ アンケートを作成</button><span class="hint">フォーム・QR・URLをその場で発行します</span>')+'</div>';
  if(prov)html+='<div class="note">毎朝6時に自動更新'+(sv.updated_at?'　最終更新 '+esc(String(sv.updated_at).slice(0,16).replace('T',' ')):'')+'</div>';
  $('#survey').innerHTML=html;
  var b;(b=$('#svAdv'))&&(b.onclick=function(){surveyAdvice();});(b=$('#svMake'))&&(b.onclick=function(){surveyProvision();});(b=$('#svRefresh'))&&(b.onclick=function(){surveyRefresh(b);});
  (b=$('#svQR'))&&(b.onclick=function(){showQR('保護者アンケート',sv.form_url);});(b=$('#svURL'))&&(b.onclick=function(){copyText(sv.form_url);});
}
function advHtml(t){return esc(t).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/^■\s*(.+)$/gm,'<h4>$1</h4>').replace(/\n/g,'<br>');}

/* ============ 描画：投稿 ============ */
function renderConn(connected){
  var el=$('#conn');
  if(!isPro()){el.innerHTML='<div class="lock"><div class="k">PRO ・ プロプランで見えるもの</div><h3>投稿の反応が、毎日自動でたまります</h3><p>Instagram・Threadsを連携すると、どのタイプの投稿が見られているか、当たり投稿、投稿の続き具合が分かります。ポスターやチビスポのページと横並びで広報の効果を比べられます。</p><a class="btn s a" href="/listing.html#plans">プロプランを見る</a></div>';
    ['#postWeekly','#postTypes','#topPosts','#recent'].forEach(function(s){$(s).innerHTML='';$(s).style.display='none';});$('#chSeg').innerHTML='';return;}
  connected=connected||{};
  var ps=[{k:'instagram',n:'Instagram'},{k:'threads',n:'Threads'},{k:'youtube',n:'YouTube'}];
  el.innerHTML='<div class="conn">'+ps.map(function(p){var on=!!connected[p.k];return '<div class="c"><b>'+p.n+'</b>'+(on?'<span class="st on">連携済み ✓</span>':(DEMO?'<span class="st">連携する →</span>':'<button class="link" data-conn="'+p.k+'">連携する →</button>'))+'</div>';}).join('')+'</div>';
}
function weekKey(d){var day=(d.getDay()+6)%7;var m=new Date(d);m.setDate(d.getDate()-day);m.setHours(0,0,0,0);return isoDate(m);}
function renderPostWeekly(){
  var stats=(D&&D.post_stats)||[], weeks=[], mon=thisMonday();
  for(var i=11;i>=0;i--)weeks.push(isoDate(new Date(mon.getTime()-i*7*86400000)));
  var plats=Array.from(new Set(stats.map(function(s){return s.platform;}))).filter(function(p){return CH==='all'||p===CH;});
  var by={};stats.forEach(function(s){var k=weekKey(new Date(s.period_start));(by[k]=by[k]||{})[s.platform]=(by[k][s.platform]||0)+(+s.post_count||0);});
  var totals=weeks.map(function(w){var t=0;plats.forEach(function(p){t+=(by[w]&&by[w][p])||0;});return t;}), max=Math.max.apply(null,totals.concat([1]));
  var thisW=totals[11], streak=0;for(var j=11;j>=0;j--){if(totals[j]>=3)streak++;else break;}
  var W=640,H=170,L=8,R=8,T=14,B=26,bw=(W-L-R)/12;
  var s='';weeks.forEach(function(w,i){var y0=H-B;plats.forEach(function(p){var v=(by[w]&&by[w][p])||0;if(!v)return;var h=(H-T-B)*v/max;s+='<rect x="'+(L+bw*i+3)+'" y="'+(y0-h)+'" width="'+(bw-6)+'" height="'+h+'" rx="2" fill="'+(PLAT_COLOR[p]||'#999')+'"><title>'+w.slice(5).replace('-','/')+'の週 '+(PLAT[p]||p)+' '+v+'本</title></rect>';y0-=h;});
    if(i%3===0||i===11)s+='<text x="'+(L+bw*i+bw/2)+'" y="'+(H-8)+'" text-anchor="middle" font-size="10" font-weight="800" fill="#8a93a0">'+w.slice(5).replace('-','/')+'</text>';});
  $('#postWeekly').innerHTML='<div class="sh" style="margin-bottom:4px"><div class="l"><b style="font-size:13.5px">投稿は続けられている？</b><span class="hint">週ごとの本数（直近12週）</span></div><span class="sub">今週 <b style="color:var(--accent);font-size:15px">'+thisW+'本</b>'+(streak>=2?'　週3本以上が'+streak+'週連続':'')+'</span></div>'
    +(stats.length?'<svg viewBox="0 0 '+W+' '+H+'">'+s+'</svg><div class="lg">'+plats.map(function(p){return '<span><i style="background:'+(PLAT_COLOR[p]||'#999')+'"></i>'+(PLAT[p]||p)+'</span>';}).join('')+'</div>':'<div class="empty">SNSを連携すると、週ごとの本数がここに出ます</div>');
}
function filteredPosts(){var posts=(D&&D.posts)||[];return CH==='all'?posts:posts.filter(function(p){return p.platform===CH;});}
function renderPostTypes(){
  var posts=filteredPosts(), by={};
  posts.forEach(function(p){var t=p.post_type||'その他';(by[t]=by[t]||{n:0,s:0}).n++;by[t].s+=(+p.like_count||0)+(+p.comments_count||0);});
  var rows=Object.keys(by).map(function(t){return {t:t,n:by[t].n,avg:by[t].n?by[t].s/by[t].n:0};}).sort(function(a,b){return b.avg-a.avg;}), max=Math.max.apply(null,rows.map(function(r){return r.avg;}).concat([1]));
  $('#postTypes').innerHTML='<div class="sh" style="margin-bottom:8px"><div class="l"><b style="font-size:13.5px">どのタイプが反応されている？</b><span class="hint">棒＝反応（♥＋💬）の平均。タイプ分けはAIが自動</span></div></div>'
    +(rows.length?'<div class="tb">'+rows.map(function(r){return '<div class="r"><span>'+esc(r.t)+' <span class="hint">('+r.n+')</span></span><div class="b"><i style="width:'+Math.round(r.avg/max*100)+'%;background:'+(TYPE_COLOR[r.t]||'#b8bec6')+'"></i></div><span class="v num">'+Math.round(r.avg)+'</span></div>';}).join('')+'</div>':'<div class="empty">投稿が取り込まれると、タイプ別の反応が出ます</div>');
}
function fmtDate(iso){var d=new Date(iso);return isNaN(d)?'':(d.getMonth()+1)+'/'+d.getDate();}
function renderTop(){
  var posts=filteredPosts().filter(function(p){return p.like_count!=null||p.comments_count!=null;}).map(function(p){return {p:p,sc:(+p.like_count||0)+(+p.comments_count||0)};}).sort(function(a,b){return b.sc-a.sc;}).slice(0,8);
  if(posts.length<3){$('#topPosts').innerHTML='<div class="empty">反応データがたまると、当たり投稿がここに出ます</div>';return;}
  var tc={},pc={};posts.forEach(function(x){if(x.p.post_type)tc[x.p.post_type]=(tc[x.p.post_type]||0)+1;pc[x.p.platform]=(pc[x.p.platform]||0)+1;});
  var tt=Object.entries(tc).sort(function(a,b){return b[1]-a[1];})[0], tp=Object.entries(pc).sort(function(a,b){return b[1]-a[1];})[0], ins='';
  if(tt&&tt[1]>=2)ins='上位'+posts.length+'件のうち<b>'+tt[1]+'件が「'+esc(tt[0])+'」</b>'+(tp&&Object.keys(pc).length>1?'、媒体は<b>'+(PLAT[tp[0]]||tp[0])+'が'+tp[1]+'件</b>':'')+'。この型の投稿を増やすのが近道です。';
  else if(tp&&Object.keys(pc).length>1)ins='上位'+posts.length+'件のうち<b>'+tp[1]+'件が'+(PLAT[tp[0]]||tp[0])+'</b>。この媒体が反応を取れています。';
  $('#topPosts').innerHTML='<div class="tw"><table class="t"><thead><tr><th></th><th>日付</th><th>媒体</th><th>タイプ</th><th>投稿</th><th class="n">♥</th><th class="n">💬</th><th></th></tr></thead><tbody>'
    +posts.map(function(x,i){var p=x.p;return '<tr><td style="color:var(--accent);font-weight:900">'+(i+1)+'</td><td>'+fmtDate(p.posted_at)+'</td><td><span class="chip" style="background:'+(PLAT_COLOR[p.platform]||'#999')+'"></span>'+(PLAT[p.platform]||esc(p.platform))+'</td><td>'+(p.post_type?'<span class="kind" style="background:'+(TYPE_COLOR[p.post_type]||'#b8bec6')+';color:#fff">'+esc(p.post_type)+'</span>':'—')+'</td><td class="w">'+esc(String(p.text||'').replace(/\s+/g,' ').slice(0,42))+'</td><td class="n num">'+(p.like_count==null?'—':p.like_count)+'</td><td class="n num">'+(p.comments_count==null?'—':p.comments_count)+'</td><td>'+(p.permalink&&p.permalink!=='#'?'<a class="link" href="'+esc(p.permalink)+'" target="_blank" rel="noopener">見る↗</a>':'')+'</td></tr>';}).join('')+'</tbody></table></div>'+(ins?'<div class="ins">'+ins+'</div>':'');
}
var __recentOpen=false;
function renderRecent(){
  var posts=filteredPosts();
  if(!posts.length){$('#recent').innerHTML='<div class="empty">'+(CH==='all'?'SNSを連携すると、投稿が毎日ここに入ります':'この媒体の投稿はまだ取り込まれていません')+'</div>';return;}
  var shown=__recentOpen?posts.slice(0,30):posts.slice(0,6);
  $('#recent').innerHTML=shown.map(function(p){return '<div class="post"><div class="m"><span class="pl" style="background:'+(PLAT_COLOR[p.platform]||'#999')+'">'+(PLAT[p.platform]||esc(p.platform))+'</span>'+(p.post_type?'<span class="ty">'+esc(p.post_type)+'</span>':'')+'<span>'+fmtDate(p.posted_at)+'</span>'+((p.like_count!=null||p.comments_count!=null)?'<span>♥ '+(p.like_count||0)+'　💬 '+(p.comments_count||0)+'</span>':'')+(p.permalink&&p.permalink!=='#'?'<a class="link" href="'+esc(p.permalink)+'" target="_blank" rel="noopener">見る↗</a>':'')+'</div><div class="tx">'+esc(String(p.text||'').replace(/\s+/g,' ').slice(0,100))+'</div></div>';}).join('')
    +(posts.length>6?'<div style="margin-top:10px"><button class="btn s o" id="recMore">'+(__recentOpen?'閉じる':'もっと見る（全'+posts.length+'件）')+'</button></div>':'');
  var b=$('#recMore');if(b)b.onclick=function(){__recentOpen=!__recentOpen;renderRecent();};
}
function renderSeg(){
  var plats=Array.from(new Set(((D&&D.posts)||[]).map(function(p){return p.platform;}).concat(((D&&D.post_stats)||[]).map(function(s){return s.platform;}))));
  if(!isPro()||plats.length<2){$('#chSeg').innerHTML='';return;}
  $('#chSeg').innerHTML=['all'].concat(plats).map(function(p){return '<button data-ch="'+p+'" aria-selected="'+(CH===p)+'" style="min-width:70px;padding:6px 8px 5px;font-size:12px">'+(p==='all'?'全体':(PLAT[p]||p))+'</button>';}).join('');
  $('#chSeg').querySelectorAll('button').forEach(function(b){b.onclick=function(){CH=b.dataset.ch;renderSeg();renderPostWeekly();renderPostTypes();renderTop();renderRecent();};});
}
function renderAll(){renderMove();renderKPI();renderTrend();renderFunnel();renderSources();renderSurvey();renderSeg();renderPostWeekly();renderPostTypes();renderTop();renderRecent();}
</script>
