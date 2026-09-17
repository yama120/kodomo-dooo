<script>
/* ============ 操作：タブ・モーダル・記録・設定 ============ */
function showTab(t){document.querySelectorAll('.tabs[role=tablist] button').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.t===t));});document.querySelectorAll('.pane').forEach(function(p){p.classList.toggle('on',p.id==='pane-'+t);});history.replaceState(null,'','#'+t);window.scrollTo({top:0});}
document.querySelectorAll('.tabs[role=tablist] button').forEach(function(b){b.onclick=function(){showTab(b.dataset.t);};});
function openModal(html){$('#md').innerHTML='<button class="x" id="mdX" aria-label="閉じる">×</button>'+html;$('#ov').classList.add('on');$('#mdX').onclick=closeModal;}
function closeModal(){$('#ov').classList.remove('on');}
$('#ov').addEventListener('click',function(e){if(e.target===this)closeModal();});
function toast(msg){var b=$('#bar');b.className='bar ok';b.style.display='';b.textContent=msg;clearTimeout(toast._t);toast._t=setTimeout(function(){setBar();},2600);}
function setBar(msg,cls){var b=$('#bar');if(!msg){if(DEMO){b.className='bar demo';b.style.display='';b.textContent='サンプル表示：架空クラブ「サンプルFC」の数字です。契約後はあなたのクラブの実データが自動で入ります。';}else b.style.display='none';return;}b.className='bar '+(cls||'warn');b.style.display='';b.textContent=msg;}
function copyText(t){if(!t)return;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){toast('コピーしました');}).catch(function(){prompt('コピーしてください',t);});}
function qrSrc(url){return 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=8&data='+encodeURIComponent(url);}
function showQR(title,url){openModal('<h3>'+esc(title)+'</h3><p class="sub">QRを印刷物に載せる、URLをSNSのプロフィールに貼る、のどちらでも数えられます。</p><div class="qr"><img src="'+qrSrc(url)+'" alt="QR"><div style="flex:1;min-width:200px"><div class="url">'+esc(url)+'</div><div class="acts" style="margin-top:10px"><button class="btn s" id="qrCopy">URLをコピー</button><a class="btn s o" href="'+qrSrc(url)+'" download="qr.png" target="_blank" rel="noopener">QR画像を開く</a></div></div></div>');$('#qrCopy').onclick=function(){copyText(url);};}
function goUrl(slug){return API+'/go/'+encodeURIComponent(CLUB||'demo')+'/'+encodeURIComponent(slug);}

/* ---- ＋記録 ---- */
function openRecord(kind){
  var today=isoDate(new Date());
  openModal('<h3>記録する</h3><p class="sub">電話や紙で受けた申込、入会、やった施策。10秒で終わります。数字はすぐ反映されます。</p>'
    +'<label>いつ</label><input type="date" id="rDate" value="'+today+'">'
    +'<label>何があった</label><select id="rKind"><optgroup label="出来事"><option>体験・見学の申込</option><option>体験・見学に参加</option><option>入会が決まった</option><option>退会</option><option>電話の問い合わせ</option><option>LINEの問い合わせ</option></optgroup><optgroup label="施策（推移のグラフに縦線が立ちます）"><option>🪧 ポスターを掲示した</option><option>📄 チラシを配った</option><option>⚽ 体験会・イベントをやった</option><option>✏️ その他の施策</option></optgroup></select>'
    +'<div id="rRouteW"><label>きっかけ（わかれば）</label><select id="rRoute"><option>不明・聞いていない</option><option>電話（チラシを見て）</option><option>電話（ポスターを見て）</option><option>知人の紹介</option><option>Instagramを見て</option><option>チビスポを見て</option><option>その場で（見学中に）</option></select></div>'
    +'<div id="rNumW"><label>人数</label><input type="number" id="rNum" min="1" value="1" inputmode="numeric"></div>'
    +'<label>メモ（任意）</label><input id="rMemo" placeholder="例：小2の男の子。土曜の体験希望／駅前掲示板に掲示">'
    +'<div class="acts"><button class="btn a" id="rSave">記録する</button><button class="btn o" id="rCancel">閉じる</button></div>'
    +'<div class="hist" id="rHist"></div>');
  if(kind)$('#rKind').value=kind;
  var tog=function(){var k=$('#rKind').value,pol=isPolicy(k);$('#rRouteW').style.display=(pol||k==='退会')?'none':'';$('#rNumW').style.display=pol?'none':'';};
  $('#rKind').onchange=tog;tog();
  $('#rCancel').onclick=closeModal;$('#rSave').onclick=saveRecord;renderHist();
}
function renderHist(){var el=$('#rHist');if(!el)return;var recs=recList().slice().reverse().slice(0,8);el.innerHTML=recs.length?'<div class="hint" style="margin-bottom:4px">最近の記録</div>'+recs.map(function(r){return '<div class="h"><span>'+esc(r.d)+'</span><b style="flex:1">'+esc(r.k)+(r.n?' '+r.n+'人':'')+(r.m?'<span class="hint"> '+esc(r.m)+'</span>':'')+'</b></div>';}).join(''):'';}
function saveRecord(){
  var date=$('#rDate').value,kind=$('#rKind').value,pol=isPolicy(kind),num=pol?0:parseInt($('#rNum').value||'1',10),memo=$('#rMemo').value.trim();
  if(!date){alert('日付を入れてください');return;} if(!pol&&(isNaN(num)||num<1)){alert('人数は1以上で入力してください');return;}
  var recs=recList();recs.push({d:date,k:kind,r:(pol||kind==='退会')?'':$('#rRoute').value,n:num,m:memo});localStorage.setItem(hk('records'),JSON.stringify(recs));
  var mon=date.slice(0,7);
  if(kind==='体験・見学の申込')setNum('trial_manual',getNum('trial_manual',0)+num);
  else if(kind==='体験・見学に参加')setNum('attend',getNum('attend',0)+num);
  else if(kind==='入会が決まった'){var jm=joinsData();jm[mon]=(+jm[mon]||0)+num;localStorage.setItem(hk('joins_m'),JSON.stringify(jm));setNum('members',getNum('members',0)+num);}
  else if(kind==='退会')setNum('members',Math.max(0,getNum('members',0)-num));
  manualPush();renderAll();closeModal();toast('記録しました');
}
function editNum(k){
  var label=k==='goal'?'会員数の目標':'現在の会員数', cur=getNum(k,k==='goal'?40:0);
  openModal('<h3>'+label+'</h3><label>人数</label><input type="number" id="eNum" min="0" value="'+cur+'" inputmode="numeric"><div class="acts"><button class="btn a" id="eSave">保存</button><button class="btn o" id="eCancel">閉じる</button></div>');
  $('#eCancel').onclick=closeModal;$('#eSave').onclick=function(){var v=parseInt($('#eNum').value,10);if(isNaN(v)||v<0){alert('0以上の数字を入力してください');return;}setNum(k,v);manualPush();renderAll();closeModal();toast('保存しました');};
}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-rec]');if(b){openRecord(b.dataset.rec);return;}
  var ed=e.target.closest('[data-edit]');if(ed){editNum(ed.dataset.edit);return;}
  var q=e.target.closest('[data-qr]');if(q){showQR(q.dataset.nm,goUrl(q.dataset.qr));return;}
  var c=e.target.closest('[data-conn]');if(c){connectSns(c.dataset.conn);return;}
});
$('#fab').onclick=function(){openRecord();};

/* ---- 媒体（QR・計測リンク）を追加 ---- */
var KINDS=[['poster','ポスター','掲示場所ごとに分けると効果を比べられます'],['flyer','チラシ','配布のタイミングごとに分けるのがおすすめ'],['sns','SNS','プロフィールのリンクに貼り替えるだけ'],['referral','紹介カード','保護者に渡す口コミ計測用'],['web','自クラブHP','リンクを貼り替えるだけ'],['other','その他','看板・地域誌・イベントなど']];
function openAddMedia(){
  openModal('<h3>QR・計測リンクを作る</h3><p class="sub">媒体ごとに専用のリンクとQRを発行します。そこから来た人数が自動で数えられ、「どこから来ているか」に並びます。</p>'
    +'<label>媒体の名前（あとで見て分かる名前に）</label><input id="mName" placeholder="例：小学校前ポスター、体験会チラシ6月">'
    +'<label>種類</label><div class="grid g2" id="mKinds">'+KINDS.map(function(k,i){return '<label class="card" style="padding:10px 12px;display:flex;gap:8px;align-items:flex-start;margin:0;cursor:pointer"><input type="radio" name="mk" value="'+k[0]+'" '+(i===0?'checked':'')+' style="width:auto;margin-top:4px"><span><b style="font-size:13.5px">'+k[1]+'</b><br><span class="hint">'+k[2]+'</span></span></label>';}).join('')+'</div>'
    +'<div class="acts"><button class="btn a" id="mMake" '+(DEMO?'disabled':'')+'>発行する</button><button class="btn o" id="mCancel">閉じる</button>'+(DEMO?'<span class="hint">サンプルでは発行できません</span>':'')+'</div>');
  $('#mCancel').onclick=closeModal;
  $('#mMake').onclick=function(){var name=$('#mName').value.trim();if(!name){alert('媒体の名前を入れてください');return;}var kind=(document.querySelector('input[name=mk]:checked')||{}).value||'other';
    this.disabled=true;this.textContent='発行中…';
    api('/api/add-media',{name:name,kind:kind}).then(function(j){if(!j||!j.ok){alert('追加に失敗しました。ログイン状態を確認してもう一度お試しください。');closeModal();return;}showQR(name,j.url);toast('発行しました。次回の読み込みから一覧に出ます');}).catch(function(){alert('追加に失敗しました（通信エラー）');closeModal();});};
}
$('#addMediaBtn').onclick=openAddMedia;

/* ---- AI・SNS・アンケート ---- */
function genReport(btn){if(DEMO)return;if(!token()){alert('ログインが必要です');return;}btn.disabled=true;btn.textContent='生成中…';
  var manual=manualCollect(),tc={};((D&&D.posts)||[]).forEach(function(p){var t=p.post_type||'未分類';tc[t]=(tc[t]||0)+1;});
  var days=(D.analytics&&D.analytics.range&&D.analytics.range.lookback_days)||30, jm=manual.joins_m||{}, jt=Object.keys(jm).reduce(function(s,k){return s+(+jm[k]||0);},0);
  var tf=(D.trials&&+D.trials.total)||0;
  var summary={'集計期間':days+'日間','クラブページの閲覧数':(D.analytics&&D.analytics.club&&+D.analytics.club.views)||0,'SNSで表示された回数':(D.post_stats||[]).reduce(function(s,r){return s+(+r.total_views||0);},0),'SNS投稿数_タイプ別':tc,
    '計測リンク経由のクリック数_媒体別':((D.clicks&&D.clicks.channels)||[]).map(function(c){return chName(c)+'：'+(+c.clicks||0)+'クリック';}),
    '体験申込の件数':{'合計':tf+(manual.trial_manual||0),'クラブページのフォーム経由（自動計測）':tf,'電話・紙など（手動で記録した分）':manual.trial_manual||0},'体験に実際に参加した人数':manual.attend||0,'入会した人数':{'合計':jt,'月別':jm},'現在の会員数':manual.members||0,'会員数の目標':manual.goal||40,
    '保護者アンケート':(D.survey&&D.survey.result)?{'回答数':D.survey.total,'どこでクラブを知ったか（回答者の内訳）':D.survey.result.counts||{},'満足度':Object.keys(D.survey.result.numeric||{}).map(function(k){var m=D.survey.result.numeric[k];return typeof m.nps==='number'?k+'：おすすめ度(NPS)＝'+m.nps+'（0〜10点で平均'+m.avg+'点・回答'+m.n+'件）':k+'：平均'+m.avg+'点（'+(m.max<=5?5:m.max)+'点満点・回答'+m.n+'件）';})}:'まだアンケートを配布していない（または回答0件）',
    '実施済みの施策（すでに記録・設定タブに登録済み）':recList().filter(function(r){return isPolicy(r.k);}).map(function(r){return r.d+' '+(r.m||r.k);}).slice(-10)};
  api('/api/home/report',{summary:summary}).then(function(j){if(j&&j.ok&&j.report){var pq=(D.ai_report&&D.ai_report.quota)||{used:0,limit:3};D.ai_report={report:j.report,at:j.at||new Date().toISOString(),quota:{used:(j.used!=null?j.used:pq.used),limit:j.limit||pq.limit||3}};renderMove();
      if(j.unchanged)toast('前回からデータに変化がないため、保存済みの提案を表示しています');else if(j.limit_reached)toast('本日の生成上限に達しました。保存済みの提案を表示しています');else if(j.cached)toast('さきほど生成した提案です（更新は約'+Math.ceil((j.wait||600)/60)+'分後から）');}
    else{btn.disabled=false;btn.textContent='AIに提案してもらう';alert('生成に失敗しました：'+((j&&(j.detail||j.error))||'不明'));}}).catch(function(){btn.disabled=false;alert('生成に失敗しました（通信エラー）');});
}
function connectSns(p){if(DEMO)return;if(!token()){alert('ログインが必要です');return;}
  if(p==='youtube'){var ch=prompt('YouTubeチャンネルのURL（または @ハンドル）を入力してください。\n例：https://www.youtube.com/@yourchannel');if(!ch)return;api('/auth/youtube/connect',{channel:ch}).then(function(j){if(j&&j.ok){alert('YouTube「'+j.name+'」を連携しました。動画データは毎日自動で取り込まれます。');location.reload();}else if(j&&j.error==='channel_not_found')alert('チャンネルが見つかりませんでした。URLか@ハンドルをご確認ください。');else alert('連携に失敗しました。もう一度お試しください。');}).catch(function(){alert('連携に失敗しました（通信エラー）');});return;}
  api('/auth/'+p+'/start',{}).then(function(j){if(!j||!j.auth_url){alert('連携を開始できませんでした。ログイン状態を確認して、もう一度お試しください。');return;}location.assign(j.auth_url);}).catch(function(){alert('連携を開始できませんでした（通信エラー）');});
}
function surveyProvision(){if(!token()){alert('ログインが必要です');return;}if(!confirm('このクラブ専用の保護者アンケート（Googleフォーム）を作成します。よろしいですか？'))return;openModal('<div style="text-align:center;padding:24px 8px"><b>アンケートを作成しています…</b><br><span class="hint">10秒ほどかかります</span></div>');
  api('/api/survey/provision',{}).then(function(j){closeModal();if(j&&j.ok){alert('アンケートを作成しました。QR・URLが使えるようになりました。');location.reload();}else if(j&&j.error==='not_configured')alert('サーバー側のアンケート設定が未完了です。');else alert('作成に失敗しました：'+((j&&(j.detail||j.error))||'不明'));}).catch(function(){closeModal();alert('作成に失敗しました（通信エラー）');});}
function surveyRefresh(btn){if(!token()){alert('ログインが必要です');return;}btn.disabled=true;btn.textContent='取り込み中…';api('/api/survey/refresh',{}).then(function(j){if(j&&j.ok){alert(j.no_column?'読み込めましたが「どこで知ったか」の項目が見つかりませんでした。':'回答 '+j.total+'件を取り込みました。');location.reload();}else{btn.disabled=false;btn.textContent='最新の回答を取り込む';alert(j&&j.error==='daily_limit'?'本日の取り込み上限に達しました。明朝6時の自動更新をお待ちください。':j&&j.error==='too_soon'?'さきほど取り込んだばかりです。少し待ってからお試しください。':'取り込みに失敗しました：'+((j&&(j.detail||j.error))||'不明'));}}).catch(function(){btn.disabled=false;alert('取り込みに失敗しました（通信エラー）');});}
function surveyAdvice(){if(!token()){alert('ログインが必要です');return;}var body=$('#svAdvBody');body.innerHTML='<span class="hint">AIが分析しています…（10秒ほど）</span>';
  api('/api/survey/advice',{}).then(function(j){if(j&&j.ok){body.innerHTML=advHtml(j.advice||'');if(j.unchanged)toast('前回から回答に変化がないため、保存済みの結果です');else if(j.limit_reached)toast('本日の生成上限に達しました');}else if(j&&j.error==='no_data')body.innerHTML='<span class="hint">まだ回答がありません。集まってから生成できます。</span>';else body.innerHTML='<span style="color:var(--accent)">生成に失敗しました：'+esc((j&&(j.detail||j.error))||'不明')+'</span>';}).catch(function(){body.innerHTML='<span style="color:var(--accent)">生成に失敗しました（通信エラー）</span>';});}

/* ---- 設定（歯車） ---- */
function openSettings(){
  var sv=(D&&D.survey)||{}, pro=isPro();
  openModal('<h3>設定</h3><div class="set">'
    +'<div class="it"><b>会員数と目標</b><p>現在 '+getNum('members',0)+'人 ／ 目標 '+getNum('goal',40)+'人</p><button class="btn s o" data-edit="members">会員数を変更</button> <button class="btn s o" data-edit="goal">目標を変更</button></div>'
    +'<div class="it"><b>SNS連携</b><p>'+(pro?'Instagram・Threads・YouTubeをつなぐと、投稿と反応が毎朝自動で取り込まれます。':'プロプランの機能です。')+'</p>'+(pro?'<button class="btn s o" data-conn="instagram">Instagram</button> <button class="btn s o" data-conn="threads">Threads</button> <button class="btn s o" data-conn="youtube">YouTube</button>':'')+'</div>'
    +'<div class="it"><b>QR・計測リンク</b><p>'+(pro?'ポスター・チラシ・SNSごとに発行して、どこから来たかを数えます。':'プロプランの機能です。')+'</p>'+(pro?'<button class="btn s o" id="sAdd">＋ 発行する</button>':'')+'</div>'
    +'<div class="it"><b>保護者アンケート</b><p>'+(sv.form_url?'稼働中。QR・URLで配ると毎朝自動で集計されます。':'ボタン1つでGoogleフォームを自動作成します。')+'</p>'+(sv.form_url?'<button class="btn s o" id="sQR">QRコード</button> <button class="btn s o" id="sURL">URLをコピー</button>':'<button class="btn s o" id="sMake" '+(DEMO?'disabled':'')+'>作成する</button>')+'</div>'
    +'<div class="it"><b>使い方</b><p>ポスターにQRを付ける手順、アンケートの配り方、用語の説明。</p><a class="btn s o" href="guide.html" target="_blank" rel="noopener">ガイドを開く ↗</a> <a class="btn s o" href="/club-mypage.html">マイページへ</a></div>'
    +'</div>');
  var b;(b=$('#sAdd'))&&(b.onclick=function(){openAddMedia();});(b=$('#sMake'))&&(b.onclick=function(){surveyProvision();});(b=$('#sQR'))&&(b.onclick=function(){showQR('保護者アンケート',sv.form_url);});(b=$('#sURL'))&&(b.onclick=function(){copyText(sv.form_url);});
}
$('#gearBtn').onclick=openSettings;

/* ============ 起動 ============ */
function gate(title,sub,acts){document.querySelectorAll('header.hd, main, .fab').forEach(function(el){el.style.display='none';});var g=$('#gate');g.style.display='block';$('#gTitle').textContent=title;$('#gSub').textContent=sub;$('#gActs').innerHTML=acts;}
function btnA(label,href,primary){return '<a class="btn '+(primary?'a':'o')+'" href="'+href+'">'+label+'</a>';}
function boot(){
  var h=location.hash.replace('#','');if(['now','acq','post'].indexOf(h)>=0)showTab(h);
  if(DEMO){D=demoData();manualApply(D.manual);$('#clubName').textContent=D.club.name;$('#planBadge').textContent='PRO';$('#planBadge').className='plan pro';setBar();renderAll();renderConn({instagram:true,threads:true});return;}
  if(!CLUB){
    var uid=null;try{var tk=token();if(tk)uid=JSON.parse(atob(tk.split('.')[1].replace(/-/g,'+').replace(/_/g,'/'))).sub||null;}catch(e){}
    if(!uid){gate('ログインすると、あなたのクラブの数字が表示されます','クラブアカウントでログインしてから、もう一度開いてください。中身だけ先に見たい場合はサンプルをどうぞ。',btnA('クラブログイン','/club-mypage.html',true)+btnA('サンプルを見る','?demo=1'));return;}
    fetch(SB_URL+'/rest/v1/teams?select=id,name&user_id=eq.'+encodeURIComponent(uid)+'&order=created_at.asc',{headers:{apikey:SB_KEY,Authorization:'Bearer '+SB_KEY}}).then(function(r){return r.json();}).then(function(rows){
      if(Array.isArray(rows)&&rows.length===1){location.replace('?club='+encodeURIComponent(rows[0].id));return;}
      if(Array.isArray(rows)&&rows.length>1){gate('どのクラブの数字を見ますか？','',rows.map(function(x){return btnA(x.name,'?club='+encodeURIComponent(x.id),true);}).join(''));return;}
      gate('このアカウントには、まだクラブが登録されていません','クラブを登録すると、掲載ページの閲覧数や申込の推移がここに出ます。',btnA('クラブを登録する','/register.html',true)+btnA('サンプルを見る','?demo=1'));
    }).catch(function(){gate('クラブを読み込めませんでした','通信環境をご確認のうえ、もう一度お試しください。',btnA('マイページへ','/club-mypage.html',true));});
    return;
  }
  setBar('読み込んでいます…','ok');
  authFetch(API+'/api/dashboard?club='+encodeURIComponent(CLUB)).then(function(r){
    if(!r){gate('ログインが切れています','クラブアカウントでログインし直してから、もう一度開いてください。',btnA('クラブログイン','/club-mypage.html',true));return;}
    if(r.status===402){gate('分析ダッシュボードは、有料プランの機能です','スタンダードはクラブページの閲覧数、プロは広報ぜんぶの分析が見られます。',btnA('プランを見る','/listing.html#plans',true)+btnA('マイページへ','/club-mypage.html'));return;}
    if(r.status===401||r.status===403){gate('このクラブの数字は表示できません','ログイン中のアカウントがこのクラブの担当者ではないか、ログインが切れています。',btnA('マイページへ','/club-mypage.html',true));return;}
    return r.json().then(function(d){
      if(!d||!d.ok){gate('読み込みに失敗しました','時間をおいて、もう一度お試しください。',btnA('マイページへ','/club-mypage.html',true));return;}
      D=d; if(d.manual)manualApply(d.manual); else if(recList().length||getNum('members',0))manualPush();
      document.title=d.club.name+'のクラブ分析｜チビスポ';$('#clubName').textContent=d.club.name;
      var pm={free:'FREE',pr:'STANDARD','pr-plus':'PRO'};$('#planBadge').textContent=pm[d.club.plan]||'PLAN';$('#planBadge').className='plan'+(d.club.pro?' pro':'');
      setBar(); renderAll();
      if(isPro()){var conn={};(d.post_stats||[]).concat(d.posts||[]).forEach(function(x){conn[String(x.platform).toLowerCase()]=true;});renderConn(conn);
        authFetch(API+'/api/sns-status?club='+encodeURIComponent(CLUB)).then(function(r2){return r2&&r2.ok?r2.json():null;}).then(function(s){if(!s||!s.ok)return;['instagram','threads','youtube'].forEach(function(k){if(s[k])conn[k]=true;});renderConn(conn);}).catch(function(){});
      } else renderConn({});
      var qs=new URLSearchParams(location.search);if(qs.get('ig')==='connected'||qs.get('threads')==='connected')toast('SNSを連携しました。投稿は明朝6時から自動で取り込まれます');
    });
  }).catch(function(){gate('読み込みに失敗しました','通信環境をご確認のうえ、もう一度お試しください。',btnA('マイページへ','/club-mypage.html',true));});
}
boot();
</script>
<footer class="wrap" style="padding:30px 16px 20px;color:var(--mute);font-size:11.5px;font-weight:700;text-align:center">チビスポ クラブ分析 ｜ <a href="guide.html" style="color:var(--accent)">使い方ガイド</a> ｜ <a href="/club-mypage.html">マイページ</a></footer>
</body>
</html>
