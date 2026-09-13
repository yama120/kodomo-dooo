# 404：入口を用意しつつ、/clubs/…/club.html?id=… のような「ルート直下のページを下の階層で開いた」URLは自動で直す
import os,sys
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
BODY='''<main><div class="wrap">
  <div class="pgh" style="text-align:center;padding:60px 0 10px">
    <div class="eyebrow" style="justify-content:center">404 NOT FOUND</div>
    <h1>このページは<em>見つかりません</em>でした。</h1>
    <p class="ld" id="nf-msg">アドレスが変わったか、削除された可能性があります。</p>
  </div>
  <div class="abt-cta" style="max-width:960px;margin:24px auto 60px">
    <a class="pri" href="/search.html"><div class="k">FOR PARENTS</div><b>クラブを探す</b><span>地域・種目・雰囲気から、お子さんに合うクラブを。</span><i>さがしてみる ›</i></a>
    <a href="/"><div class="k">HOME</div><b>トップに戻る</b><span>チビスポの入口です。</span><i>トップへ ›</i></a>
    <a href="/contact.html"><div class="k">CONTACT</div><b>お問い合わせ</b><span>見つからないときは、こちらから。</span><i>相談する ›</i></a>
  </div>
</div></main>'''
CSS='''
.abt-cta{display:grid;gap:12px}
.abt-cta a{display:block;border:1.5px solid var(--ink);padding:20px;background:var(--card);color:var(--ink);border-radius:var(--r)}
.abt-cta a.pri{background:var(--ink);color:var(--bg)}
.abt-cta .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--accent)}
.abt-cta b{display:block;font-family:var(--fh);font-size:19px;font-weight:900;margin:4px 0}
.abt-cta span{font-size:12.5px;font-weight:700;opacity:.8}
.abt-cta i{display:block;font-style:normal;font-weight:900;margin-top:10px}
.pgh .eyebrow{display:flex;gap:10px;align-items:center}
@media(min-width:760px){.abt-cta{grid-template-columns:1fr 1fr 1fr}}
'''
JS=r'''<script>
/* 古いリンク対策：ルート直下のページを下の階層で開いてしまったURL（例 /clubs/tokyo/club.html?id=…）は、
   ルートの同じページへ送り直す。検索ページは条件で履歴を書き換えるため、この形のURLが残ることがある。 */
(function(){
  var m=location.pathname.match(/\/([a-z0-9-]+\.html)$/i);
  var ROOT=['club.html','search.html','map.html','index.html','magazine.html','about.html','partner.html','listing.html','contact.html','login.html','mypage.html','register.html','club-mypage.html','faq.html','legal.html','service-ads.html','service-sns.html'];
  if(m && location.pathname!=='/'+m[1] && ROOT.indexOf(m[1].toLowerCase())>=0){
    location.replace('/'+m[1]+location.search+location.hash); return;
  }
  var e=document.getElementById('nf-msg');
  if(e) e.textContent='アドレスが変わったか、削除された可能性があります。（'+location.pathname+'）';
})();
</script>'''
C.prodpage('404.html','ページが見つかりません｜チビスポ','お探しのページは見つかりませんでした。クラブを探す・トップ・お問い合わせからお進みください。',BODY,css=CSS,js=JS,noindex=True,base_root=True,scripts=('site.js?v='+C.V,))
