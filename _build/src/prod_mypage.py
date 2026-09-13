# 保護者マイページ v3 本番（mypage.html）：mp_v2 の見た目＋旧 mypage.html の処理（体験申込・チャット・プロフィール）＋新項目（診断・お知らせ設定・お子さん）
import os,re,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D
ANON=re.search(r"SB_KEY = '([^']+)'",open(D+'shared.js',encoding='utf-8').read()).group(1)
cap={}
def page(fname,title,body,css='',bodyattr='',extra_js=''): cap.update(css=css)
import prod_exec; g=prod_exec.load(page,('mp_v2',))
CSS=C.strip_preview(cap['css'])+'''
/* ---- 本番の補い ---- */
[hidden]{display:none!important}
.mp-out{max-width:520px;margin:40px auto;text-align:center;border:1px solid var(--line);border-radius:var(--r);padding:34px 22px;background:var(--card)}
.mp-out h1{font-family:var(--fh);font-size:22px;font-weight:900;margin:0 0 8px}
.mp-out p{font-size:13.5px;font-weight:700;color:var(--sub);line-height:1.8;margin:0 0 18px}
.mp-out .btn{display:inline-block;margin:4px}
.mp-panel .empty2 .btn{display:inline-block;margin-top:8px}
.msg .m{cursor:pointer}
.msg .m .st.new{background:var(--accent);color:#fff}
.favs .nc .rm{position:absolute;left:9px;top:9px;z-index:2;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.92);border:0;cursor:pointer;font-size:16px;line-height:1;color:var(--ink)}
.acc .r input,.acc .r select{border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-family:var(--f);font-size:13.5px;background:var(--card);color:var(--ink);min-width:0}
.acc .r .ed{display:none;flex-wrap:wrap;gap:6px;align-items:center;flex:1 1 100%}
.acc .r.open .ed{display:flex}
.acc .r.open>span{display:none}
.acc .r .ed button{background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:8px 14px;font-weight:900;font-size:12.5px;cursor:pointer;font-family:inherit}
.acc .r .ed .cancel{background:transparent;color:var(--sub);border:1px solid var(--line)}
.acc .r a{cursor:pointer}
.mp-save-msg{font-size:12.5px;font-weight:800;margin:6px 0 0}
.ntf label{cursor:pointer}
/* チャット */
.mp-chat-bg{position:fixed;inset:0;background:rgba(15,21,30,.55);z-index:200;display:none;align-items:flex-end;justify-content:center}
.mp-chat{background:var(--card);width:100%;max-width:640px;height:min(88vh,720px);border-radius:var(--r) var(--r) 0 0;display:flex;flex-direction:column;overflow:hidden}
@media(min-width:760px){.mp-chat-bg{align-items:center}.mp-chat{border-radius:var(--r)}}
.mp-chat .hd2{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--line)}
.mp-chat .hd2 b{font-family:var(--fh);font-size:15px;font-weight:900;display:block}
.mp-chat .hd2 small{font-size:11.5px;color:var(--sub);font-weight:700}
.mp-chat .hd2 button{margin-left:auto;border:0;background:transparent;font-size:24px;line-height:1;cursor:pointer;color:var(--sub)}
.mp-chat .body{flex:1;overflow-y:auto;padding:16px;background:color-mix(in srgb,var(--ink) 3%,var(--bg))}
.mp-chat .row{display:flex;margin-bottom:12px}.mp-chat .row.me{justify-content:flex-end}
.mp-chat .bb{max-width:78%}
.mp-chat .bb .t{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px 14px;font-size:14px;line-height:1.7;white-space:pre-wrap;word-break:break-word}
.mp-chat .row.me .bb .t{background:var(--accent);color:#fff;border-color:var(--accent)}
.mp-chat .bb .d{font-size:10.5px;color:var(--sub);margin-top:4px;font-weight:700}
.mp-chat .row.me .bb .d{text-align:right}
.mp-chat .ft2{display:flex;gap:8px;padding:12px 14px;border-top:1px solid var(--line)}
.mp-chat .ft2 input{flex:1;border:1px solid var(--line);border-radius:999px;padding:11px 14px;font-family:var(--f);font-size:14px}
.mp-chat .ft2 button{background:var(--accent);color:#fff;border:0;border-radius:999px;padding:0 18px;font-weight:900;cursor:pointer;font-family:inherit}
.mp-chat .empty{text-align:center;color:var(--sub);font-size:13px;font-weight:700;padding:30px 0}
'''
BODY='''<main><div class="wrap">
  <div class="mp-out" id="mp-out" hidden>
    <h1>マイページ</h1>
    <p>ログインすると、体験申込のやり取り・お気に入り・診断の結果・お知らせの設定が使えます。</p>
    <a class="btn" href="login.html?next=mypage.html">ログイン / 新規登録（無料）</a>
  </div>
  <div id="mp-in" hidden>
  <div class="mp-head">
    <div class="mp-who"><div class="mp-av" id="mpAv">M</div><div><div class="k">MY PAGE</div><h1><span id="mpName"></span><small>さん</small></h1><p id="mpMeta"></p></div></div>
    <div class="mp-act"><a href="#" data-tab="account" class="pri">アカウント設定</a><a href="#" data-quiz>診断する</a></div>
  </div>
  <div class="mp-tabs" id="mpTabs">
    <button data-tab="home" class="on">ホーム</button>
    <button data-tab="result">診断の結果</button>
    <button data-tab="notify">お知らせ</button>
    <button data-tab="fav">お気に入り <i class="off" id="mpFavN">0</i></button>
    <button data-tab="msg">申込・メッセージ <i id="mpMsgN" hidden>0</i></button>
    <button data-tab="account">アカウント</button>
  </div>
  <section class="mp-panel on" data-tab="home">
    <h2>いま、<em>見るもの</em>。</h2>
    <p class="lead">新しい動きがあるものから並べています。</p>
    <div class="mp-home" id="mpHome"></div>
  </section>
  <section class="mp-panel" data-tab="result">
    <h2>診断の<em>結果</em></h2>
    <p class="lead">保存した結果です。条件を変えるか、もう一度診断できます。</p>
    <div class="saved" id="mpSaved" hidden>
      <div class="date"></div><div class="k">TYPE</div><div class="tp"></div><div class="cond"></div><div class="sp"></div>
      <div class="row"><a class="pri" id="mpSavedSearch" href="search.html">この条件でクラブを見る ›</a><a href="#" data-quiz>もう一度診断する</a></div>
    </div>
    <div class="empty2" id="mpEmpty"><div class="t">まだ診断の結果がありません。</div><p>1分の質問に答えると、合いそうな種目のタイプと近くのクラブが出ます。保存すると、条件に合うクラブが載ったときにお知らせします。</p><a class="btn" href="#" data-quiz>診断をはじめる（無料）</a></div>
  </section>
  <section class="mp-panel" data-tab="notify">
    <h2>お知らせの<em>設定</em></h2>
    <p class="lead">受け取るものだけ ON にしてください。いつでも変えられます。</p>
    <div class="ntf">
      <label><div><div class="t">条件に合う新しいクラブが載ったとき</div><div class="s" id="ntfNewS">お住まいの地域と診断の条件に合うクラブが登録されたら</div></div><input type="checkbox" data-k="new_clubs"><span class="mp-sw"></span></label>
      <label><div><div class="t">お気に入り・診断の種目で、体験の募集が始まったとき</div><div class="s">体験会・入団募集のお知らせ</div></div><input type="checkbox" data-k="trial_open"><span class="mp-sw"></span></label>
      <label><div><div class="t">マガジンの新着記事</div><div class="s">週1本まで</div></div><input type="checkbox" data-k="articles"><span class="mp-sw"></span></label>
    </div>
    <h3>届け方</h3>
    <div class="ntf ntf-ch">
      <label><div><div class="t">アプリのプッシュ通知</div><div class="s">チビスポアプリを入れている場合</div></div><input type="checkbox" data-k="push"><span class="mp-sw"></span></label>
      <label><div><div class="t">メール</div></div><input type="checkbox" data-k="email"><span class="mp-sw"></span></label>
    </div>
    <div class="ntf"><div class="how" id="ntfMsg">通知は1日1回までにまとめて届きます。</div></div>
  </section>
  <section class="mp-panel" data-tab="fav">
    <h2>お気に入り<em>クラブ</em></h2>
    <p class="lead">♡ を押したクラブです。比べて、体験を申し込めます。</p>
    <div class="news favs" id="mpFavs"></div>
    <div class="empty2" id="mpFavEmpty" hidden><div class="t">まだお気に入りはありません。</div><p>クラブの ♡ を押すと、ここに残ります。</p><a class="btn" href="search.html">クラブを探す</a></div>
  </section>
  <section class="mp-panel" data-tab="msg">
    <h2>体験申込と<em>メッセージ</em></h2>
    <p class="lead">クラブからの返信はここに届きます。</p>
    <div class="msg" id="mpTrials"></div>
    <div class="empty2" id="mpTrialEmpty" hidden><div class="t">まだ申込はありません。</div><p>クラブのページから体験を申し込むと、やり取りがここに残ります。</p><a class="btn" href="search.html">クラブを探す</a></div>
  </section>
  <section class="mp-panel" data-tab="account">
    <h2>アカウント</h2>
    <p class="lead">お子さんの情報は、診断とお知らせの条件に使います。</p>
    <div class="acc">
      <div class="r" id="rDisplay"><b>ニックネーム</b><span id="vDisplay"></span><a href="#" data-edit="rDisplay">変更</a><div class="ed"><input id="eDisplay" placeholder="例：はなまま"><button data-save="display">保存</button><button class="cancel" data-cancel="rDisplay">やめる</button></div></div>
      <div class="r" id="rName"><b>お名前</b><span id="vName"></span><a href="#" data-edit="rName">変更</a><div class="ed"><input id="eLast" placeholder="姓"><input id="eFirst" placeholder="名"><button data-save="name">保存</button><button class="cancel" data-cancel="rName">やめる</button></div></div>
      <div class="r"><b>メール</b><span id="vEmail"></span><span></span></div>
      <div class="r" id="rRegion"><b>地域</b><span id="vRegion"></span><a href="#" data-edit="rRegion">変更</a><div class="ed"><select id="ePref"><option value="">都道府県</option></select><select id="eCity" disabled><option value="">市区町村</option></select><button data-save="region">保存</button><button class="cancel" data-cancel="rRegion">やめる</button></div></div>
      <div class="r" id="rChild"><b>お子さん</b><span id="vChild"></span><a href="#" data-edit="rChild">変更</a><div class="ed"><select id="eGrade"><option value="">学年</option><option>未就学</option><option>年長</option><option>小1〜2</option><option>小3〜4</option><option>小5〜6</option><option>中学生</option></select><select id="eGender"><option value="">性別（任意）</option><option>男の子</option><option>女の子</option></select><button data-save="child">保存</button><button class="cancel" data-cancel="rChild">やめる</button></div></div>
      <div class="r" id="rPw"><b>パスワード</b><span>••••••••</span><a href="#" data-edit="rPw">変更</a><div class="ed"><input id="ePw1" type="password" placeholder="新しいパスワード（6文字以上）"><input id="ePw2" type="password" placeholder="もう一度"><button data-save="pw">保存</button><button class="cancel" data-cancel="rPw">やめる</button></div></div>
    </div>
    <div class="mp-save-msg" id="mpSaveMsg"></div>
    <div class="acc-danger"><a href="#" id="mpLogout">ログアウト</a><a href="account-delete.html">アカウントを削除</a></div>
  </section>
  </div>
  <div style="height:40px"></div>
</div></main>
<div class="mp-chat-bg" id="mp-chat-bg">
  <div class="mp-chat" role="dialog" aria-modal="true">
    <div class="hd2"><div><b id="mp-chat-title"></b><small id="mp-chat-sub"></small></div><button type="button" id="mp-chat-close" aria-label="閉じる">&times;</button></div>
    <div class="body" id="mp-chat-body"></div>
    <div class="ft2"><input id="mp-chat-input" placeholder="メッセージを入力" autocomplete="off"><button type="button" id="mp-chat-send">送信</button></div>
  </div>
</div>'''
JS=open(P+'mypage_prod.js',encoding='utf-8').read().replace('__ANON__',ANON)
C.prodpage('mypage.html','マイページ｜チビスポ','体験申込のやり取り・お気に入り・診断の結果・お知らせの設定。',BODY,css=CSS,js='<script>\n'+JS+'\n</script>',supabase=True,noindex=True,scripts=('club-card.js?v='+C.V,'cities.js?v=20260731b','site.js?v='+C.V,'quiz.js?v='+C.V),head='<link rel="stylesheet" href="quiz.css?v='+C.V+'">\n')
