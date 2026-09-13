# ---- 検索結果 v2（マガジン調）。build_pages.py から exec される（cards, page, search_css, rec_html を使う）
search_css2=search_css+open(P+'search_v2_css.css',encoding='utf-8').read()
lead_c=cards.CLUBS[0]
lead_html=('<div class="lead"><div class="im"><img src="assets/preview-video/%s.jpg" alt=""><span class="nc-pr">PR</span><span class="nc-fav">%s</span>%s</div>'
  '<div class="bd"><div class="no">01</div><div class="ey">TOP PICK</div><div class="nc-top">%s<span class="sp">%s</span></div>'
  '<h2 class="nm">%s</h2><div class="nc-area"><svg class="pin" viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 1 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.3"/></svg>%s</div>'
  '<p class="ds">%s 練習は2面のグラウンドを学年で分けて使います。土曜は保護者の見学も自由です。</p><div class="nc-meta">%s</div><div class="nc-tags">%s</div>'
  '<div class="nc-foot"><span class="lk on">%s%d</span><span class="cm">%s%d</span><a class="go" href="club-preview.html">クラブを見る ›</a></div></div></div>')%(
  lead_c['img'],cards.HEART,('<span class="nc-vid">▶ 動画</span>' if lead_c.get('video') else ''),cards.badge(lead_c['sport']),lead_c['sport'],lead_c['name'],lead_c['area'],
  lead_c['desc'],lead_c['meta'],''.join('<span>%s</span>'%t for t in lead_c['tags']),cards.HEART,lead_c['likes'],cards.CMT,lead_c['comments'])
grid2=[cards.card(**dict(c,pr=(i==0))) for i,c in enumerate(cards.CLUBS[1:])]
strip='<div class="strip"><div><div class="ey">FOR BEGINNERS</div><div class="t">見学のとき、コーチに聞いておきたい5つのこと</div><div class="l">はじめてのクラブ選びで迷ったら。<b>記事を読む ›</b></div></div><img src="assets/preview-video/wm-bball-jp.jpg" alt=""></div>'
grid2.insert(5,strip)
fside2=open(P+'search_v2_fside.html',encoding='utf-8').read()
tpl=open(P+'search_v2_body.html',encoding='utf-8').read()
search_body2=tpl.replace('{{FSIDE}}',fside2).replace('{{LEAD}}',lead_html).replace('{{GRID}}',"\n".join(grid2)).replace('{{REC}}',"\n".join(rec_html))
page('search-preview.html','世田谷区のサッカークラブ 14件｜チビスポ（検索結果プレビュー）',search_body2,search_css2,extra_js="<script>(function(){var t=document.getElementById('ftog'),a=document.getElementById('fside');if(t&&a)t.addEventListener('click',function(){a.classList.toggle('open')})})();</script>"+open(P+'search_v2_bgfit.js',encoding='utf-8').read())
