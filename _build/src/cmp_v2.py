# ---- クラブマイページ（プレビュー v2・2026-09-12）：上にクラブの帯、下はタブ。新デザインのクラブ詳細が出す項目を全部入力できる形に
cm_css='''
.cm-head{display:grid;grid-template-columns:1fr;gap:14px;align-items:center;padding:26px 0 18px;border-bottom:2px solid var(--ink)}
.cm-who{display:flex;gap:14px;align-items:center;min-width:0}
.cm-av{width:56px;height:56px;border-radius:50%;background:#fff;border:3px solid var(--accent);color:var(--accent);font-family:var(--fh);font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none}
.cm-who .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:3px}
.cm-who h1{font-family:var(--fh);margin:0;font-size:clamp(20px,5vw,26px);font-weight:900;line-height:1.2;letter-spacing:-.01em;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.cm-who h1 .pl{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em;padding:4px 8px;border:1px solid var(--ink);color:var(--ink)}
.cm-who h1 .pub{font-size:10.5px;font-weight:900;padding:4px 8px;background:#1f9d55;color:#fff;letter-spacing:.06em}
.cm-who p{margin:4px 0 0;font-size:12px;font-weight:700;color:var(--sub)}
.cm-act{display:flex;gap:8px;flex-wrap:wrap}
.cm-act a{font-size:12.5px;font-weight:900;padding:10px 14px;border:1.5px solid var(--ink);color:var(--ink);white-space:nowrap}
.cm-act a.pri{background:var(--ink);color:var(--bg)}
.cm-tabs{position:sticky;top:56px;z-index:20;background:var(--bg);display:flex;border-bottom:1px solid var(--ink);margin:0 -20px;padding:0 20px;overflow-x:auto;scrollbar-width:none}
.cm-tabs::-webkit-scrollbar{display:none}
.cm-tabs button{flex:none;background:transparent;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:14px 14px 12px;font-family:var(--fh);font-size:13.5px;font-weight:900;color:var(--sub);cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.cm-tabs button i{font-style:normal;font-family:'Anton',sans-serif;font-size:10.5px;background:var(--accent);color:#fff;padding:2px 6px;border-radius:999px;min-width:20px;text-align:center}
.cm-tabs button i.off{background:var(--line);color:var(--sub)}
.cm-tabs button.on{color:var(--ink);border-bottom-color:var(--ink)}
.cm-panel{display:none;padding:26px 0 0;max-width:900px}
.cm-panel.on{display:block;animation:mpIn .3s}
@keyframes mpIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.cm-panel h2{font-family:var(--fh);margin:0 0 4px;font-size:clamp(19px,4.6vw,24px);font-weight:900;line-height:1.3;letter-spacing:-.01em;border:0;padding:0}
.cm-panel h2 em{font-style:normal;color:var(--accent)}
.cm-panel .lead{margin:0 0 18px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
/* ホーム */
.cm-home{display:grid;grid-template-columns:1fr;gap:10px}
.cm-hc{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;border:1px solid var(--ink);background:var(--card);padding:16px;color:var(--ink);transition:transform .15s,box-shadow .15s}
.cm-hc:hover{transform:translateY(-2px);box-shadow:6px 6px 0 var(--ink)}
.cm-hc .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.22em;color:var(--accent);margin-bottom:5px}
.cm-hc b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;line-height:1.35}
.cm-hc small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:3px;line-height:1.6}
.cm-hc .go{width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--bg);font-family:'Anton',sans-serif;font-size:16px;display:flex;align-items:center;justify-content:center}
.cm-hc.hot{border:2px solid var(--accent)}.cm-hc.hot .go{background:var(--accent);color:#fff}
.cm-hc.lock{opacity:.85}.cm-hc.lock .go{background:var(--line);color:var(--sub)}
.cm-hc .lk{display:inline-block;margin-top:6px;font-size:10.5px;font-weight:900;color:var(--accent);border:1px solid var(--accent);padding:2px 7px}
.cm-done{margin-top:18px;border:1px solid var(--ink);background:var(--card);padding:16px}
.cm-done .t{display:flex;justify-content:space-between;align-items:baseline;font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:8px}
.cm-done .t b{font-family:'Anton',sans-serif;font-size:22px;color:var(--accent);letter-spacing:.02em}
.cm-done .bar{height:8px;background:var(--line);position:relative;margin-bottom:12px}
.cm-done .bar i{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
.cm-done ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.cm-done li{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;font-weight:700;padding:8px 0;border-top:1px solid var(--line)}
.cm-done li a{font-weight:900;color:var(--accent);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}
/* 申込・質問 */
.cm-tr{border-top:2px solid var(--ink)}
.cm-tr .r{display:grid;grid-template-columns:1fr auto;gap:12px;padding:14px 0;border-bottom:1px solid var(--line);align-items:center}
.cm-tr .n{font-family:var(--fh);font-size:14px;font-weight:900}
.cm-tr .s{font-size:12px;font-weight:700;color:var(--sub);margin-top:3px;line-height:1.7}
.cm-tr .st{font-size:11px;font-weight:900;letter-spacing:.06em;white-space:nowrap;border:1px solid var(--accent);color:var(--accent);padding:4px 8px}
.cm-tr .st.new{background:var(--accent);color:#fff}.cm-tr .st.dim{color:var(--sub);border-color:var(--line)}
.cm-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.cm-bar a,.cm-bar span{font-size:12px;font-weight:900;padding:8px 12px;border:1.5px solid var(--ink)}
.cm-bar span{border-color:var(--line);color:var(--sub);font-weight:700}
/* 申込・質問：受信箱（左一覧・右スレッド） */
.cm-panel.wide{max-width:none}
.cm-inbox{display:grid;grid-template-columns:1fr;gap:14px;border:1px solid var(--ink);background:var(--card)}
.cm-list{border-bottom:1px solid var(--ink)}
.cm-flt{display:flex;gap:6px;flex-wrap:wrap;padding:12px 12px 10px;border-bottom:1px solid var(--line)}
.cm-flt span{font-size:11px;font-weight:900;padding:5px 9px;border:1px solid var(--line);color:var(--sub);cursor:pointer}
.cm-flt span.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.cm-it{display:grid;grid-template-columns:38px 1fr auto;gap:10px;align-items:center;padding:12px 12px;border-bottom:1px solid var(--line);color:var(--ink);position:relative}
.cm-it.on{background:color-mix(in srgb,var(--accent) 6%,var(--card));box-shadow:inset 3px 0 0 var(--accent)}
.cm-it.dim{opacity:.6}
.cm-it .av{width:38px;height:38px;border-radius:50%;background:var(--ink);color:var(--bg);font-family:var(--fh);font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center}
.cm-it .tx{min-width:0}
.cm-it b{display:flex;justify-content:space-between;gap:8px;font-family:var(--fh);font-size:13.5px;font-weight:900}
.cm-it b small{font-size:10.5px;font-weight:700;color:var(--sub)}
.cm-it span{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:2px}
.cm-it em{display:block;font-style:normal;font-size:12px;font-weight:700;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cm-it .dot{width:10px;height:10px;border-radius:50%;background:var(--accent)}
.cm-more{display:flex;gap:12px;flex-wrap:wrap;padding:12px;font-size:11.5px;font-weight:900}
.cm-more a{text-decoration:underline;text-underline-offset:3px}
.cm-thread{display:flex;flex-direction:column;min-height:420px}
.cm-th{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap;padding:14px 16px;border-bottom:2px solid var(--ink)}
.cm-th b{font-family:var(--fh);font-size:15px;font-weight:900;display:block}
.cm-th small{font-size:11px;font-weight:700;color:var(--sub)}
.cm-stsel{display:flex;gap:4px;flex-wrap:wrap}
.cm-stsel span{font-size:10.5px;font-weight:900;padding:5px 9px;border:1px solid var(--line);color:var(--sub);cursor:pointer}
.cm-stsel span.on{background:var(--accent);border-color:var(--accent);color:#fff}
.cm-msgs{flex:1;padding:16px;display:grid;gap:12px;align-content:start;background:color-mix(in srgb,var(--ink) 3%,var(--card))}
.cm-m{max-width:80%;display:grid;gap:4px}
.cm-m.them{justify-self:start}.cm-m.me{justify-self:end}
.cm-m .b{padding:10px 12px;font-size:13px;font-weight:700;line-height:1.7;background:#fff;border:1px solid var(--line);border-radius:14px 14px 14px 4px}
.cm-m.me .b{background:var(--ink);color:var(--bg);border-color:var(--ink);border-radius:14px 14px 4px 14px}
.cm-m small{font-size:10.5px;font-weight:700;color:var(--sub)}
.cm-m.sys{max-width:none;justify-self:center}
.cm-m.sys span{font-size:10.5px;font-weight:900;color:var(--sub);border:1px dashed var(--line);padding:5px 10px}
.cm-reply{border-top:1px solid var(--ink);padding:12px 16px 14px;background:var(--card)}
.cm-tpl{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:11px;font-weight:700;color:var(--sub);margin-bottom:8px}
.cm-tpl a{font-weight:900;color:var(--ink);border:1px solid var(--ink);padding:4px 8px}
.cm-reply textarea{min-height:96px}
.cm-rrow{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:8px;flex-wrap:wrap}
.cm-rrow small{font-size:11px;font-weight:700;color:var(--sub)}
.cm-rrow .send{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:13.5px;padding:11px 18px}
@media(min-width:900px){
  .cm-inbox{grid-template-columns:340px 1fr;gap:0}
  .cm-list{border-bottom:0;border-right:1px solid var(--ink)}
}
/* フォーム */
.cm-sec{border:1px solid var(--ink);background:var(--card);margin-bottom:14px}
.cm-sec>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:14px 16px}
.cm-sec>summary::-webkit-details-marker{display:none}
.cm-sec>summary b{font-family:var(--fh);font-size:15px;font-weight:900}
.cm-sec>summary small{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:2px}
.cm-sec>summary .pm{font-family:'Anton',sans-serif;font-size:18px;color:var(--accent)}
.cm-sec[open]>summary .pm::before{content:"–"}.cm-sec:not([open])>summary .pm::before{content:"+"}
.cm-sec .bd{padding:4px 16px 18px;border-top:1px solid var(--line)}
.cm-f{display:grid;grid-template-columns:1fr;gap:6px;padding:12px 0;border-bottom:1px solid var(--line)}
.cm-f:last-child{border-bottom:0}
.cm-f>label{font-size:12px;font-weight:900;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.cm-f>label .req{font-size:9.5px;letter-spacing:.08em;background:var(--ink);color:var(--bg);padding:1px 5px}
.cm-f>label .new{font-family:'Anton',sans-serif;font-size:9.5px;letter-spacing:.14em;background:var(--accent);color:#fff;padding:2px 6px}
.cm-f>label .sh{font-size:10.5px;font-weight:700;color:var(--sub);margin-left:auto}
.cm-f .hint{font-size:11px;font-weight:700;color:var(--sub);line-height:1.6}
.cm-in{width:100%;border:1px solid var(--ink);background:#fff;font-family:var(--f);font-size:13.5px;font-weight:700;padding:10px 12px;color:var(--ink)}
.cm-in.sm{max-width:200px}
textarea.cm-in{min-height:88px;resize:vertical}
.cm-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.cm-row .cm-in{width:auto;flex:1;min-width:120px}
.cm-chk{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;border:1px solid var(--ink);padding:8px 11px;background:#fff;cursor:pointer}
.cm-chk.on{background:var(--ink);color:var(--bg)}
.cm-chk input{margin:0}
.cm-tags{display:flex;gap:6px;flex-wrap:wrap}
.cm-tags .grp{width:100%;font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.2em;color:var(--sub);margin-top:6px}
.cm-tag{font-size:12px;font-weight:900;padding:6px 10px;border:1px solid var(--ink);background:#fff;cursor:pointer}
.cm-tag.on{background:var(--accent);border-color:var(--accent);color:#fff}
.cm-tag i{font-style:normal;opacity:.7;margin-left:2px}
.cm-tagin{display:inline-flex;align-items:stretch;border:1px solid var(--ink);background:#fff}
.cm-tagin .cm-in{border:0;width:220px;padding:6px 10px;font-size:12px}
.cm-tagin span{display:flex;align-items:center;padding:0 10px;background:var(--ink);color:var(--bg);font-size:12px;font-weight:900}
.cm-sl{display:grid;grid-template-columns:78px 1fr 78px;gap:10px;align-items:center;font-size:11.5px;font-weight:700;color:var(--sub);padding:6px 0}
.cm-sl span:last-child{text-align:right}
.cm-sl input[type=range]{width:100%;accent-color:var(--accent)}
.cm-tbl{width:100%;border-collapse:collapse;font-size:12px}
.cm-tbl th{text-align:left;font-size:10px;letter-spacing:.14em;color:var(--sub);font-weight:900;padding:6px 6px;border-bottom:2px solid var(--ink)}
.cm-tbl td{padding:6px 6px;border-bottom:1px solid var(--line)}
.cm-tbl td .cm-in{padding:7px 8px;font-size:12px}
.cm-add{display:inline-block;margin-top:10px;font-size:12px;font-weight:900;border:1.5px solid var(--ink);padding:8px 12px;background:#fff}
.cm-staff{display:grid;grid-template-columns:56px 1fr;gap:12px;align-items:start;border:1px solid var(--line);padding:12px;margin-bottom:8px;background:#fff}
.cm-staff .ph{width:56px;height:56px;border-radius:50%;background:var(--line);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:900;color:var(--sub);text-align:center;line-height:1.2}
.cm-staff .cm-in{margin-bottom:6px}
.cm-photos{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.cm-photos div{aspect-ratio:4/3;position:relative;overflow:hidden;border:1px solid var(--ink);background:#f2f0eb}
.cm-photos img{width:100%;height:100%;object-fit:cover;display:block}
.cm-photos .cv{position:absolute;left:8px;top:8px;background:var(--accent);color:#fff;font-size:10px;font-weight:900;padding:3px 7px}
.cm-photos .lock{display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;font-size:11px;font-weight:900;color:var(--sub);border-style:dashed;text-align:center;padding:8px}
.cm-photos .lock b{font-family:'Anton',sans-serif;font-size:16px;color:var(--ink)}
.cm-save{position:sticky;bottom:0;z-index:15;margin:18px -20px 0;padding:12px 20px calc(12px + env(safe-area-inset-bottom));background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(10px);border-top:1px solid var(--line);display:flex;gap:10px;align-items:center;justify-content:space-between}
.cm-save small{font-size:11.5px;font-weight:700;color:var(--sub)}
.cm-save a{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:14px;padding:13px 22px}
/* プラン */
.cm-plans{display:grid;grid-template-columns:1fr;gap:10px}
.cm-pl{border:1px solid var(--ink);background:var(--card);padding:16px}
.cm-pl.cur{border:2px solid var(--ink)}.cm-pl.hot{border:2px solid var(--accent);box-shadow:8px 8px 0 var(--accent)}
.cm-pl .n{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--sub);margin-bottom:4px}
.cm-pl h3{font-family:var(--fh);margin:0 0 4px;font-size:18px;font-weight:900}
.cm-pl .pr{font-family:'Anton',sans-serif;font-size:28px;line-height:1;margin:6px 0 8px}
.cm-pl .pr small{font-family:var(--f);font-size:11px;font-weight:700;color:var(--sub);margin-left:4px}
.cm-pl ul{list-style:none;margin:0 0 12px;padding:10px 0 0;border-top:1px solid var(--line);display:grid;gap:5px}
.cm-pl li{position:relative;padding-left:16px;font-size:12px;font-weight:700}
.cm-pl li::before{content:"";position:absolute;left:0;top:7px;width:8px;height:5px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
.cm-pl a{display:block;text-align:center;font-family:var(--fh);font-weight:900;font-size:13px;padding:11px;border:1.5px solid var(--ink)}
.cm-pl.hot a{background:var(--accent);border-color:var(--accent);color:#fff}
.cm-pl .cur-lb{display:inline-block;font-size:10.5px;font-weight:900;background:var(--ink);color:var(--bg);padding:3px 8px;margin-bottom:8px}
/* 設定 */
.cm-set{border:1px solid var(--ink);background:var(--card)}
.cm-set .r{display:grid;grid-template-columns:110px 1fr auto;gap:10px;align-items:center;padding:13px 16px;border-bottom:1px solid var(--line);font-size:13px;font-weight:700}
.cm-set .r:last-child{border-bottom:0}
.cm-set .r b{font-size:11px;letter-spacing:.06em;color:var(--sub)}
.cm-set .r a{font-size:12px;font-weight:900;text-decoration:underline;text-underline-offset:3px;white-space:nowrap}
.cm-danger{margin-top:18px;display:flex;gap:14px;flex-wrap:wrap;font-size:12px;font-weight:700}
.cm-danger a{color:var(--sub);text-decoration:underline;text-underline-offset:3px}
@media(min-width:760px){
  .cm-head{grid-template-columns:1fr auto;padding:34px 0 22px}
  .cm-tabs{margin:0;padding:0;top:60px}
  .cm-home{grid-template-columns:1fr 1fr;gap:14px}
  .cm-f{grid-template-columns:200px 1fr;gap:6px 18px;align-items:start}
  .cm-f>label{padding-top:10px}
  .cm-f .hint{grid-column:2}
  .cm-plans{grid-template-columns:repeat(3,1fr);gap:16px}
  .cm-photos{grid-template-columns:repeat(4,1fr)}
  .cm-save{margin:18px 0 0;padding:12px 16px}
}
'''
A='assets/preview-video/'
def f(label,body,req=False,new=False,hint='',show=''):
    return '<div class="cm-f"><label>%s%s%s%s</label><div>%s</div>%s</div>'%(label,' <span class="req">必須</span>' if req else '',' <span class="new">NEW</span>' if new else '',('<span class="sh">表示：%s</span>'%show) if show else '',body,('<div class="hint">%s</div>'%hint) if hint else '')
def inp(v='',ph='',cls='',typ='text'): return '<input class="cm-in %s" type="%s" value="%s" placeholder="%s">'%(cls,typ,v,ph)
def chks(opts,on=()): return '<div class="cm-row">'+''.join('<label class="cm-chk%s"><input type="checkbox"%s>%s</label>'%(' on' if o in on else '',' checked' if o in on else '',o) for o in opts)+'</div>'
def tags(groups,on=()):
    h='<div class="cm-tags">'
    for g,items in groups: h+='<div class="grp">%s</div>'%g+''.join('<span class="cm-tag%s">%s</span>'%(' on' if i in on else '',i) for i in items)
    h+='<div class="grp">自分の言葉で</div><span class="cm-tag on">週末は親子で試合観戦 <i>×</i></span><span class="cm-tagin"><input class="cm-in" maxlength="12" placeholder="例：礼儀を大事にする（12字まで）"><span>追加</span></span>'
    return h+'</div>'
def sl(l,r,v): return '<div class="cm-sl"><span>%s</span><input type="range" min="1" max="5" value="%d"><span>%s</span></div>'%(l,v,r)
def sec(title,sub,body,open_=True): return '<details class="cm-sec"%s><summary><div><b>%s</b><small>%s</small></div><span class="pm"></span></summary><div class="bd">%s</div></details>'%(' open' if open_ else '',title,sub,body)

form=''.join([
 sec('基本情報','クラブ名・種目・地域',
   f('クラブ名',inp('わかばFC'),req=True,show='見出し')+
   f('種目',inp('サッカー'),req=True,show='丸バッジ・検索')+
   f('住所','<div class="cm-row"><input class="cm-in sm" value="157-0075" placeholder="郵便番号" style="max-width:130px"><span class="cm-chk" style="padding:8px 10px">郵便番号から入力</span></div><div class="cm-row" style="margin-top:6px">'+inp('東京都','都道府県',cls='sm')+inp('世田谷区','市区町村',cls='sm')+'</div><div class="cm-row" style="margin-top:6px">'+inp('砧公園1-1','町名・番地')+inp('','建物名・部屋番号（任意）')+'</div>',req=True,show='📍地域・検索・地図のピン',hint='郵便番号を入れると都道府県・市区町村が入ります。検索の「地域」と地図のピンは、この住所から自動で決まります')+
   f('活動場所の名前',inp('砧公園グラウンド','例：砧公園グラウンド・○○小学校 体育館'),show='地図・アクセスの見出し',hint='複数あるときは主な場所を。詳しくは紹介文に')+
   f('ロゴ','<div class="cm-row"><span class="cm-chk">画像を選ぶ</span><span class="hint">正方形推奨。無いときは頭文字の丸になります</span></div>',show='クラブ名の左')),
 sec('対象と活動','対象年齢・曜日・体験',
   f('対象年齢',chks(['未就学（〜6歳）','小学生','中学生'],on=('小学生',)),req=True,show='対象・検索')+
   f('活動曜日',chks(['月','火','水','木','金','土','日'],on=('土','日')),show='活動曜日・検索（平日／土日）')+
   f('体験',chks(['受付中','要相談'],on=('受付中',))+'<div class="cm-row" style="margin-top:8px">'+inp('無料','体験の費用（例：無料・1回500円）',cls='sm')+'</div>',new=True,show='体験の欄',hint='「体験の費用」は新しい項目です。空なら「要相談」と出ます')+
   f('在籍人数','<div class="cm-row">'+inp('38','',cls='sm')+'<span class="hint">人 ・ 学年の幅は対象年齢から出します</span></div>',new=True,show='在籍')),
 sec('費用','月謝・初期費用・内訳',
   f('月謝',inp('5000','',cls='sm')+' <span class="hint" style="display:inline">円／月 ・ 検索の「月謝◯円以下」に使います</span>',req=True,show='月謝・検索')+
   f('初期費用の目安',inp('12000','',cls='sm')+' <span class="hint" style="display:inline">円 ・ 0なら「入会金なし」で検索に出ます</span>',show='初期費用・検索')+
   f('費用の内訳','<table class="cm-tbl"><tr><th>項目</th><th>金額</th><th>備考</th></tr>'+''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(inp(a),inp(b,'',cls='sm'),inp(c,'任意')) for a,b,c in [('年会費','3,000円',''),('ユニフォーム・道具','8,000円','初回のみ'),('スポーツ保険','800円','年1回'),('遠征・大会','','都度')])+'</table><span class="cm-add">＋ 行を追加</span>',new=True,show='費用の内訳',hint='月謝のほかにかかるもの。書いてあるだけで問い合わせの手前で決めてもらえます')),
 sec('雰囲気とスタイル','タグ・5段階の目安',
   f('雰囲気タグ',tags([('方針',['楽しむこと','本格志向']),('指導',['ほめて伸ばす','礼儀・しつけ']),('空気',['アットホーム','少人数で丁寧','真剣に取り組む']),('こんなクラブ',['親子で参加OK','はじめての子が多い','試合より練習が好き','女の子歓迎','女性指導者あり','未就学から'])],on=('楽しむこと','ほめて伸ばす','親子で参加OK','はじめての子が多い','試合より練習が好き')),show='雰囲気タグ・診断',hint='候補を押すか、自分の言葉で追加できます（12字まで・合計6個まで）。カードには3つまで出ます。クラブが大切にしていることが集まったら、候補にまとめていきます')+
   f('このクラブのスタイル',sl('きびしい','のびのび',4)+sl('勝ち重視','楽しさ重視',4)+sl('実力で選ぶ','全員が出る',5)+sl('練習が多い','少ない',3)+sl('男の子が多い','女の子が多い',2),new=True,show='このクラブのスタイル',hint='5段階の目安。保護者が「うちの子に合うか」を見る欄です')),
 sec('紹介文とおすすめ','紹介文・おすすめポイント・こんなお子様に',
   f('クラブからの紹介文','<textarea class="cm-in">世田谷区の桜丘を中心に活動している少年サッカークラブです。土日のどちらか、または両方の参加を選べます。はじめてボールを触る子が半分くらいなので、経験がなくても大丈夫です。</textarea>',req=True,show='クラブからの紹介文・カードの2行',hint='最初の2行がカードに出ます。「はじめての子が半分」のように保護者が知りたいことを先に')+
   f('おすすめポイント','<div class="cm-row" style="flex-direction:column;align-items:stretch">'+''.join(inp(x) for x in ['コーチ4人のうち3人が、もと保護者です','学年ごとにコースが分かれています','入会金はいただいていません','体験は何回でも無料です','雨の日は近くの体育館に振り替えます'])+'</div>',show='おすすめポイント',hint='5つまで')+
   f('こんなお子様におすすめ','<div class="cm-row">'+''.join(inp(x,cls='sm') for x in ['はじめてサッカーをする子','体を動かすのが好きな子','友だちと一緒に続けたい子','週末だけ通いたい子'])+'</div>',show='こんなお子様におすすめ',hint='4つまで')),
 sec('コース','学年・曜日・時間・月謝の一覧',
   '<table class="cm-tbl"><tr><th>コース名</th><th>対象</th><th>曜日</th><th>時間</th><th>月謝</th></tr>'+''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%tuple(inp(v) for v in r) for r in [('キッズ','小1〜2','土','9:00〜10:00','4,000円'),('ジュニア','小3〜4','土・日','10:00〜11:30','5,000円'),('ジュニアユース','小5〜6','日','13:00〜15:00','5,000円')])+'</table><span class="cm-add">＋ コースを追加（12件まで）</span>',open_=False),
 sec('コーチ・スタッフ','お子さまが毎週会う人',
   ''.join('<div class="cm-staff"><div class="ph">写真</div><div>'+inp(n,'名前')+'<div class="cm-row">'+inp(r,'役割',cls='sm')+'</div>'+inp(c,'一言（40字まで）')+'</div></div>' for n,r,c in [('佐々木 あゆみ','コーチ／キッズ担当','年中〜小2を担当。まずは「楽しい」から。'),('田中 健','代表・コーチ','元少年団の保護者。土曜は全学年を見ています')])+'<span class="cm-add">＋ スタッフを追加（4人まで）</span><div class="hint" style="margin-top:8px"><span class="new" style="font-family:Anton,sans-serif;font-size:9.5px;letter-spacing:.14em;background:var(--accent);color:#fff;padding:2px 6px">NEW</span> 新しい項目です。顔写真は任意。名前は姓だけでも構いません</div>',open_=False),
 sec('公式リンク','SNS・ホームページ',
   f('Instagram',inp('https://instagram.com/wakaba_fc'),show='公式リンク・SNS連携（プロ）')+f('X',inp('','https://x.com/…'))+f('ホームページ',inp('https://wakaba-fc.example'))+f('LINE',inp('','公式LINEのURL')),open_=False),
])

cm_body='''
<main><div class="wrap">
  <div class="note">【クラブマイページ v2（2026-09-12）】本番 club-mypage.html（募集の状態／スタッフと通知先／プランの管理／申込み・質問／コメント／クラブ情報の編集／もっと見てもらうには／パスワード／削除）を新デザインに。★役割＝<b>新デザインのクラブ詳細・検索・カードが出す項目を、クラブが全部入力できる</b>こと。突き合わせで足りなかった6項目を <b>NEW</b> で追加：体験の費用／在籍人数／費用の内訳／スタイル5段階／コーチ・スタッフ／動画URL。雰囲気タグは既存3群（方針・指導・空気）に「こんなクラブ」6つを追加。各項目に「表示：どこに出るか」を付けた。★本番化に必要なDB列：teams.trial_fee, member_count, cost_items(jsonb), style(jsonb 5値), staff(jsonb), video_url。写真の上限はプラン連動（フリー1／スタンダード7／プロ15）で本番と同じ。閲覧数はスタンダード以上（本番の仕様どおり）。</div>

  <div class="cm-head">
    <div class="cm-who"><div class="cm-av">わ</div><div><div class="k">CLUB MY PAGE</div><h1>わかばFC <span class="pl">FREE</span><span class="pub">公開中</span></h1><p>サッカー ・ 東京都 世田谷区 ・ 体験 受付中</p></div></div>
    <div class="cm-act"><a class="pri" href="club-preview.html">クラブページを見る ›</a><a href="#" data-tab="plan">プランを変更</a></div>
  </div>

  <div class="cm-tabs" id="cmTabs">
    <button data-tab="home" class="on">ホーム</button>
    <button data-tab="tr">申込・質問 <i>2</i></button>
    <button data-tab="info">クラブ情報 <i class="off">70%%</i></button>
    <button data-tab="media">写真・動画</button>
    <button data-tab="plan">プラン</button>
    <button data-tab="set">スタッフ・設定</button>
  </div>

  <section class="cm-panel on" data-tab="home">
    <h2>いま、<em>やること</em>。</h2>
    <p class="lead">返信が必要なものと、足りない情報から並べています。</p>
    <div class="cm-home">
      <a class="cm-hc hot" href="#" data-tab="tr"><div><div class="k">TRIAL REQUESTS</div><b>体験申込が2件、返信待ちです</b><small>はなまま さん（小2）9/14 土 ・ さとう さん（年長）</small></div><span class="go">›</span></a>
      <a class="cm-hc" href="#" data-tab="info"><div><div class="k">PROFILE</div><b>クラブ情報の充実度 70%%</b><small>スタイル・スタッフ・費用の内訳が未入力</small></div><span class="go">›</span></a>
      <a class="cm-hc lock" href="#" data-tab="plan"><div><div class="k">VIEWS</div><b>今週の閲覧数</b><small>スタンダード以上で見られます</small><span class="lk">プランを見る</span></div><span class="go">›</span></a>
      <a class="cm-hc" href="#" data-tab="media"><div><div class="k">PHOTOS</div><b>写真を増やして、クラブの魅力をもっと</b><small>いま1枚。写真が多いクラブほど体験申込が集まります</small></div><span class="go">›</span></a>
    </div>
    <div class="cm-done"><div class="t"><span>クラブ情報の充実度</span><b>70%%</b></div><div class="bar"><i style="width:70%%"></i></div>
      <ul><li>このクラブのスタイル（5段階）<a href="#" data-tab="info">入力する ›</a></li><li>コーチ・スタッフ<a href="#" data-tab="info">入力する ›</a></li><li>費用の内訳<a href="#" data-tab="info">入力する ›</a></li></ul></div>
  </section>

  <section class="cm-panel wide" data-tab="tr">
    <h2>申込・<em>質問</em></h2>
    <p class="lead">左で選んで、右で返信。保護者はアプリでもWebでも同じやり取りを見ています。</p>
    <div class="cm-inbox">
      <div class="cm-list">
        <div class="cm-flt"><span class="on">未返信 2</span><span>返信済み</span><span>体験予定</span><span>入団</span><span>すべて 5</span></div>
        <a class="cm-it on" href="#"><div class="av">は</div><div class="tx"><b>はなまま さん<small>9/11</small></b><span>小2 ・ 体験希望 9/14（土）10:00</span><em>見学だけでも大丈夫ですか</em></div><i class="dot"></i></a>
        <a class="cm-it" href="#"><div class="av">さ</div><div class="tx"><b>さとう さん<small>9/10</small></b><span>年長 ・ 体験希望 9/21（日）</span><em>はじめてです。ボールは必要ですか</em></div><i class="dot"></i></a>
        <a class="cm-it" href="#"><div class="av">や</div><div class="tx"><b>やまだ さん<small>9/8</small></b><span>小4 ・ 質問</span><em>ありがとうございます。日曜に伺います</em></div></a>
        <a class="cm-it dim" href="#"><div class="av">か</div><div class="tx"><b>かとう さん<small>9/7</small></b><span>小1 ・ 電話で受付 ・ 入団</span><em>体験 9/7 実施</em></div></a>
        <div class="cm-more"><a href="#">＋ 電話・紙の申込を追加</a><a href="#">CSVで書き出す</a></div>
      </div>
      <div class="cm-thread">
        <div class="cm-th"><div><b>はなまま さん</b><small>お子さま 小2（男の子）・ はじめて ・ 体験希望 9/14（土）10:00</small></div><div class="cm-stsel"><span class="on">未返信</span><span>体験予定</span><span>入団</span><span>見送り</span></div></div>
        <div class="cm-msgs">
          <div class="cm-m them"><div class="b">はじめまして。小2の息子がサッカーに興味を持ち始めました。9/14の10時に体験をお願いしたいのですが、まずは見学だけでも大丈夫ですか。</div><small>9/11 21:04 ・ アプリから</small></div>
          <div class="cm-m sys"><span>体験申込を受け付けました ・ 保護者にはアプリとメールで通知</span></div>
        </div>
        <div class="cm-reply">
          <div class="cm-tpl"><span>テンプレート：</span><a href="#">体験のご案内</a><a href="#">持ち物</a><a href="#">日程の相談</a></div>
          <textarea class="cm-in" placeholder="返信を書く（保護者のアプリとメールに届きます）">はなまま さん、お申し込みありがとうございます。9/14（土）10:00、砧公園グラウンドでお待ちしています。見学だけでも大丈夫です。動きやすい服と飲み物だけお持ちください。</textarea>
          <div class="cm-rrow"><small>送信すると「返信済み」になります</small><a class="send" href="#">返信を送る ›</a></div>
        </div>
      </div>
    </div>
  </section>

  <section class="cm-panel" data-tab="info">
    <h2>クラブ<em>情報</em></h2>
    <p class="lead">クラブページ・検索・カードに出る内容です。「表示：」はどこに出るかです。</p>
    %(FORM)s
    <div class="cm-save"><small>変更は保存するまで公開されません</small><a href="#">保存して公開</a></div>
  </section>

  <section class="cm-panel" data-tab="media">
    <h2>写真・<em>動画</em></h2>
    <p class="lead">1枚目がカバー写真です。スマホの写真で構いません。</p>
    <div class="cm-photos">
      <div><img src="%(A)sjp-soccer-run.jpg" alt=""><span class="cv">カバー</span></div>
      <div class="lock"><b>+6</b>スタンダードで<br>7枚まで</div>
      <div class="lock"><b>+14</b>プロで<br>15枚まで</div>
    </div>
    <div class="hint" style="margin-top:10px;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7">練習の様子・コーチ・子どもの表情・グラウンド。枚数を増やすほど、雰囲気が伝わります。<a href="#" data-tab="plan" style="font-weight:900;color:var(--accent);text-decoration:underline;text-underline-offset:3px">写真を増やす（プランを見る）›</a></div>
    <div class="cm-f" style="margin-top:14px"><label>動画 <span class="new">NEW</span><span class="sh">表示：クラブページの最上部・カードの「動画」印</span></label><div>%(VID)s<div class="hint">YouTube か Instagram のリールのURL。30秒の紹介動画は「撮影・動画制作」（準備中）でも作れます</div></div></div>
    <div class="cm-save"><small>写真の並べ替えは、写真をクリック</small><a href="#">保存して公開</a></div>
  </section>

  <section class="cm-panel" data-tab="plan">
    <h2>プラン</h2>
    <p class="lead">いまはフリーです。載せるのは無料のまま、見てもらう量を増やすならスタンダードから。</p>
    <div class="cm-plans">
      <div class="cm-pl cur"><span class="cur-lb">いまのプラン</span><div class="n">FREE</div><h3>フリー</h3><div class="pr">¥0</div><ul><li>クラブページ・検索・地図に掲載</li><li>写真1枚・コース・体験申込</li><li>保護者とメッセージ</li></ul><a href="#">このまま</a></div>
      <div class="cm-pl hot"><div class="n">STANDARD</div><h3>スタンダード</h3><div class="pr">¥3,000<small>/月（税抜）</small></div><ul><li>写真を7枚まで</li><li>検索結果で上位に表示</li><li>「編集部おすすめ」枠に掲載</li><li>ページの閲覧数がわかる</li></ul><a href="#">スタンダードにする</a></div>
      <div class="cm-pl"><div class="n">PRO</div><h3>プロ</h3><div class="pr">¥10,000<small>/月（税抜）</small></div><ul><li>写真を15枚まで</li><li>SNS連携（Instagram・Threads）</li><li>どの発信から申込につながったかわかる</li><li>公式SNSで月1回紹介</li></ul><a href="#">プロにする</a></div>
    </div>
    <p class="lead" style="margin-top:14px">支払いはカード（Stripe）。年払いは2か月分お得です。プランの変更・解約はいつでも。</p>
  </section>

  <section class="cm-panel" data-tab="set">
    <h2>スタッフ・<em>設定</em></h2>
    <p class="lead">申込の通知先と、ログインできるスタッフです。</p>
    <div class="cm-set">
      <div class="r"><b>募集の状態</b><span>公開中 ・ 体験 受付中</span><a href="#">変更</a></div>
      <div class="r"><b>通知先メール</b><span>coach@wakaba-fc.example（田中）</span><a href="#">変更</a></div>
      <div class="r"><b>スタッフ</b><span>田中 健（代表）・佐々木 あゆみ（コーチ）</span><a href="#">招待</a></div>
      <div class="r"><b>ログインメール</b><span>you@example.com</span><a href="#">変更</a></div>
      <div class="r"><b>パスワード</b><span>••••••••</span><a href="#">変更</a></div>
    </div>
    <div class="cm-danger"><a href="#">ログアウト</a><a href="#">掲載を一時停止</a><a href="#">掲載を削除</a></div>
  </section>
  <div style="height:40px"></div>
</div></main>
'''%dict(A=A,FORM=form,VID=inp('','https://youtu.be/…'))
cm_js='''<script>
(function(){
 var tabs=document.getElementById('cmTabs');
 function show(k){document.querySelectorAll('.cm-panel').forEach(function(p){p.classList.toggle('on',p.dataset.tab===k)});tabs.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.tab===k)});}
 tabs.addEventListener('click',function(e){var b=e.target.closest('button');if(b){show(b.dataset.tab);history.replaceState(null,'','?tab='+b.dataset.tab)}});
 document.addEventListener('click',function(e){var a=e.target.closest('a[data-tab]');if(a){e.preventDefault();show(a.dataset.tab);history.replaceState(null,'','?tab='+a.dataset.tab);window.scrollTo({top:tabs.getBoundingClientRect().top+scrollY-70,behavior:'smooth'})}
   var t=e.target.closest('.cm-tag');if(t){t.classList.toggle('on')}
   var c=e.target.closest('.cm-chk');if(c){setTimeout(function(){var i=c.querySelector('input');if(i)c.classList.toggle('on',i.checked)},0)}});
 var m=location.search.match(/tab=(home|tr|info|media|plan|set)/);if(m)show(m[1]);
})();
</script>'''
page('club-mypage-preview.html','クラブ マイページ｜チビスポ（プレビュー）',cm_body,cm_css,extra_js=cm_js)
