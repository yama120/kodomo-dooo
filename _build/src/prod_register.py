# クラブ登録 本番（register.html）：reg_v2 の見た目＋旧 register.html の処理（signUp → teams insert → 写真 → 管理者通知 → 有料なら Stripe）
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
cap={}
def page(fname,title,body,css='',bodyattr='',extra_js=''): cap[fname]=dict(body=body,css=css)
import prod_exec; g=prod_exec.load(page,('reg_v2',))
CSS=C.strip_preview(cap['register-preview.html']['css'])+'''
/* ---- 本番の補い ---- */
[hidden]{display:none!important}
.rg-msg{margin:0 0 14px;padding:11px 14px;border-radius:calc(var(--r) - 4px);font-size:13px;font-weight:800;line-height:1.7}
.rg-msg.err{background:#fff0f2;color:#b3232e}.rg-msg.ok{background:#eafaf0;color:#1f8a5b}
select.rg-in{appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23111' stroke-width='2.4'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;background-size:12px;padding-right:30px}
.rg-chk{cursor:pointer}
.rg-chk input{position:absolute;opacity:0;width:0;height:0}
.rg-drop{cursor:pointer;position:relative}
.rg-drop input{position:absolute;inset:0;opacity:0;cursor:pointer}
.rg-ph{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.rg-ph .p{position:relative;width:110px;height:82px;border-radius:calc(var(--r) - 6px);overflow:hidden;border:1px solid var(--line)}
.rg-ph .p img{width:100%;height:100%;object-fit:cover;display:block}
.rg-ph .p button{position:absolute;right:4px;top:4px;width:22px;height:22px;border-radius:50%;border:0;background:rgba(20,24,30,.7);color:#fff;font-size:13px;line-height:1;cursor:pointer}
.rg-submit button{display:block;width:100%;background:var(--accent);color:#fff;border:0;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px;border-radius:calc(var(--r) - 4px);cursor:pointer}
.rg-submit button:disabled{opacity:.6}
.rg-zip{background:var(--ink);color:var(--bg);border:0;cursor:pointer;font-family:inherit;font-weight:900;font-size:12px;padding:8px 12px;border-radius:999px}
#rg-amw{margin-top:8px}
'''
def f(label,body,req=False,opt=False,hint=''):
    return '<div class="rg-f"><label>%s%s%s</label><div>%s</div>%s</div>'%(label,' <span class="req">必須</span>' if req else '',' <span class="opt">任意</span>' if opt else '',body,('<div class="hint">%s</div>'%hint) if hint else '')
def inp(idn,ph='',cls='',typ='text',extra=''): return '<input class="rg-in %s" id="%s" type="%s" placeholder="%s" %s>'%(cls,idn,typ,ph,extra)
def chks(name,opts,on=()): return '<div class="rg-row">'+''.join('<label class="rg-chk%s"><input type="checkbox" name="%s" value="%s"%s>%s</label>'%(' on' if o in on else '',name,o,' checked' if o in on else '',o) for o in opts)+'</div>'
def radios(name,opts,on=None): return '<div class="rg-row">'+''.join('<label class="rg-chk%s"><input type="radio" name="%s" value="%s"%s>%s</label>'%(' on' if v==on else '',name,v,' checked' if v==on else '',o) for o,v in opts)+'</div>'
def sec(n,title,sub,tm,body,idn=''): return '<div class="rg-sec" id="%s"><div class="hd"><i>%s</i><div><b>%s</b><small>%s</small></div><span class="tm">%s</span></div><div class="bd">%s</div></div>'%(idn,n,title,sub,tm,body)
s1=sec('1','アカウント','承認後にマイページで編集するためのものです','30 SEC',
   f('メールアドレス',inp('authEmail','coach@example.com',typ='email',extra='autocomplete="email"'),req=True,hint='ログインと、運営からの連絡に使います')+
   f('パスワード','<div class="rg-row">'+inp('authPassword','8文字以上',typ='password',extra='autocomplete="new-password"')+inp('authPasswordConfirm','もう一度',typ='password',extra='autocomplete="new-password"')+'</div>',req=True),idn='authCard')
s2=sec('2','クラブの基本','検索とクラブページに出る内容です','1 MIN',
   f('クラブ名',inp('name','例：わかばFC'),req=True)+
   f('種目','<div class="rg-row"><select class="rg-in" id="sport"></select></div><div class="rg-row" style="margin-top:6px">'+inp('sportOther','種目を入力（例：フラッグフットボール）',extra='hidden')+'</div>',req=True,hint='一覧にない種目は「その他」を選んで入力してください')+
   f('住所','<div class="rg-row">'+inp('postal','郵便番号（例：1570073）',cls='sm',extra='inputmode="numeric" style="max-width:170px"')+'<button type="button" class="rg-zip" id="zipBtn">郵便番号から入力</button></div><div class="rg-row" style="margin-top:6px"><select class="rg-in sm" id="pref"><option value="">都道府県</option></select><select class="rg-in sm" id="city" disabled><option value="">市区町村</option></select></div><div class="rg-row" style="margin-top:6px">'+inp('cityOther','市区町村を入力',extra='hidden')+'</div><div class="rg-row" style="margin-top:6px">'+inp('address1','町名・番地（例：砧公園1-1）')+inp('venue','会場名（例：砧公園グラウンド）')+'</div>',req=True,hint='検索の「地域」と地図のピンは、この住所から決まります。会場が複数あるときは主な場所を')+
   f('対象年齢',chks('age',['未就学','小学生','中学生'])+'<div class="rg-row" id="rg-amw" hidden>'+radios('age_min',[('3歳〜','3歳〜'),('4歳〜','4歳〜'),('5歳〜','5歳〜'),('年中〜','年中〜'),('年長〜','年長〜')])+'</div>',req=True,hint='未就学を選んだら、受け入れ開始の年齢も')+
   f('活動曜日',chks('day',['月','火','水','木','金','土','日']),req=True)+
   f('月謝','<div class="rg-row">'+inp('feeNum','3000',cls='sm',extra='inputmode="numeric" style="max-width:140px"')+'<span class="hint" style="display:inline">円／月 ・ 無料は 0 ・ コースで違うときは一番安い額を</span></div>',req=True)+
   f('体験',radios('trial',[('受付中','true'),('要相談','false')],on='true')+'<div class="rg-row" style="margin-top:8px">'+inp('trialFee','体験の費用（例：無料、1回500円）',cls='sm')+'</div>',req=True)+
   f('紹介文','<textarea class="rg-in" id="description" maxlength="400" placeholder="例：はじめてボールを触る子が半分。学年ごとにコースを分けているので、経験がなくても大丈夫です。土曜の見学はいつでも。"></textarea><div class="rg-cnt">0 / 400</div>',req=True,hint='最初の2行がカードに出ます。「はじめての子の割合」「見学できるか」「コーチは誰か」が保護者に効きます')+
   f('写真','<div class="rg-drop"><b>写真を1枚選ぶ</b><small>JPG・PNG・5MBまで。スマホの写真で構いません。承認後にマイページで増やせます</small><input type="file" id="rg-photo-input" accept="image/*"></div><div class="rg-ph" id="rg-photos"></div>',opt=True)+
   f('申込の通知先',inp('email','team@example.com',typ='email'),req=True,hint='体験申込が届くメールです。保護者には公開されません')+
   f('女の子・女性指導者',chks('feature',['女の子歓迎','女性指導者あり']),opt=True)+
   '<details class="rg-more"><summary>SNS・ホームページ・初期費用（あとからでも）</summary><div class="in2">'+f('Instagram',inp('instagram','ユーザー名（@なし）'),opt=True)+f('X',inp('twitter','ユーザー名（@なし）'),opt=True)+f('ホームページ',inp('website_url','https://…',typ='url'),opt=True)+f('LINE公式',inp('line_url','https://lin.ee/…',typ='url'),opt=True)+f('入会金','<div class="rg-row">'+inp('admission','0',cls='sm',extra='inputmode="numeric" style="max-width:140px"')+'<span class="hint" style="display:inline">円 ・ 0なら「入会金なし」で検索に出ます</span></div>',opt=True)+'</div></details>')
s3=sec('3','確認して送信','送信後、運営の確認を経て掲載されます','10 SEC',
   '<div class="rg-agree"><input type="checkbox" id="agreeCheck" checked><span><a href="legal.html#terms" target="_blank">利用規約</a>と<a href="legal.html#privacy" target="_blank">プライバシーポリシー</a>に同意します。掲載内容は運営が確認し、内容によっては修正をお願いすることがあります。</span></div>'+
   '<div class="rg-msg err" id="rg-msg" hidden></div>'+
   '<div class="rg-submit"><small id="rg-submit-note">掲載は無料です。送信後、最短で当日に載ります。<br>スタイル・スタッフ・写真の追加は、承認後にマイページから。</small><button type="submit" id="rg-submit">この内容で申請する ›</button></div>')
BODY='''<main><div class="wrap">
  <div class="rg-head"><div class="ey">FOR CLUBS ・ FREE LISTING</div><h1 id="rg-hero-title">クラブを<em>載せる</em>。</h1><p id="rg-hero-sub">登録は1分。写真1枚と紹介文があれば、今日から載せられます。有料プランは登録後にマイページから。</p>
    <div class="rg-steps"><div class="on"><i>1</i>アカウント</div><div><i>2</i>クラブの基本</div><div><i>3</i>確認して送信</div></div>
  </div>
  <form class="rg-lay" id="rg-form" novalidate>
  <div>
    %(s1)s
    %(s2)s
    %(s3)s
  </div>
  <aside class="rg-side">
    <div class="rg-prev"><div class="k">PREVIEW</div><div class="t">検索結果では、こう見えます</div><div id="rg-card"></div><p>入力するとその場で変わります。紹介文の最初の2行がカードに出ます。</p></div>
    <div class="rg-after"><div class="k">AFTER YOU SEND</div><ol><li data-n="1"><b>運営が内容を確認</b>（最短で当日）</li><li data-n="2"><b>掲載開始</b>。検索・地図・種目ページに載ります</li><li data-n="3"><b>マイページで育てる</b>。スタイル・スタッフ・写真を足すほど申込が集まります</li></ol></div>
    <div class="rg-help">すでに登録している方は <a href="club-mypage.html">ログイン</a>。うまく登録できないときは <a href="contact.html?who=club">お問い合わせ</a> から。</div>
  </aside>
  </form>
  <div class="rg-done" id="rg-done">
    <div class="top"><div class="k">RECEIVED</div><h2 id="rg-success-title">申請を受け付けました。</h2><p id="rg-success-msg">運営の確認後に掲載されます（最短で当日）。確認が終わったらメールでお知らせします。</p></div>
    <div id="rg-done-next">
    <div class="k2">WHILE YOU WAIT</div>
    <div class="t2">待っている間に、できること。</div>
    <div class="rg-next">
      <a class="rg-nc" href="club-mypage.html"><div class="n">01</div><b>写真を足す</b><small>フリーは1枚。写真が多いクラブほど体験申込が集まります</small></a>
      <a class="rg-nc" href="club-mypage.html"><div class="n">02</div><b>紹介文とコースを整える</b><small>「うちの子に合うか」を保護者が見る欄です</small></a>
      <a class="rg-nc hot" href="club-mypage.html"><div class="n">03</div><b>スタンダードで上位に</b><small>写真7枚・検索で上位表示・閲覧数。<em>¥3,000/月</em></small><span class="go">プランを見る ›</span></a>
    </div>
    </div>
    <div class="row"><a class="pri" id="rg-success-btn" href="club-mypage.html">マイページへ ›</a><a href="index.html">フリーのまま、トップに戻る</a></div>
  </div>
  <div style="height:40px"></div>
</div></main>'''%dict(s1=s1,s2=s2,s3=s3)
JS=open(P+'register_prod.js',encoding='utf-8').read()
C.prodpage('register.html','クラブを載せる（登録）｜チビスポ','チビスポにクラブを載せる。掲載は無料。写真1枚と紹介文があれば1分で登録できます。運営の確認後、検索・地図・種目ページに載ります。',BODY,css=CSS,js='<script>\n'+JS+'\n</script>',supabase=True,scripts=('club-card.js?v='+C.V,'cities.js?v=20260731b','site.js?v='+C.V))
