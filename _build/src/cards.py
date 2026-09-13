# 標準クラブカード（全ページ共通）：クラブ名が主役・丸バッジ・♡/💬
SPORT={
 'サッカー':('#6BAAEF','<circle cx="12" cy="12" r="9"/><polygon points="12,8 15,10.2 13.8,13.8 10.2,13.8 9,10.2"/>'),
 'バスケットボール':('#F5A24B','<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.6 5.6c3.2 3.2 9.6 9.6 12.8 12.8M18.4 5.6C15.2 8.8 8.8 15.2 5.6 18.4"/>'),
 'バスケ':('#F5A24B','<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.6 5.6c3.2 3.2 9.6 9.6 12.8 12.8M18.4 5.6C15.2 8.8 8.8 15.2 5.6 18.4"/>'),
 '野球':('#E8884A','<circle cx="12" cy="12" r="9"/><path d="M7 5.2c2.6 2.8 4.4 7.4 4.4 13.6M17 5.2c-2.6 2.8-4.4 7.4-4.4 13.6"/>'),
 'バレーボール':('#FFC83F','<circle cx="12" cy="12" r="9"/><path d="M12 3a18 18 0 010 18M3.4 9c5 1 11.6 4 16.2 9M3.4 15c5-1 11.6-4 16.2-9"/>'),
 'テニス':('#5BD6A0','<ellipse cx="10" cy="8.5" rx="5" ry="6"/><path d="M6.6 13.2 3.5 19.5M7 6l6 5"/>'),
 '水泳':('#3FB6D6','<circle cx="15" cy="6" r="2"/><path d="M3 16c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 6 0M4 12l5-3 3 2"/>'),
 'ダンス':('#FF7FB6','<circle cx="13" cy="5" r="2"/><path d="M13 7l-2 6M11 13l-3.5 5M11 13l4 2M13 9l4-1"/>'),
 '空手':('#7B8CE8','<circle cx="12" cy="5" r="2"/><path d="M12 7v5l4 2M12 12l-4 2M8 20l4-4 4 4"/>'),
 '剣道':('#7B8CE8','<circle cx="12" cy="5" r="2"/><path d="M12 7v5l4 2M12 12l-4 2M8 20l4-4 4 4"/>'),
 '体操':('#C98BFF','<circle cx="12" cy="5" r="2"/><path d="M12 7v6M8 9.5l8 1.5M9 19l3-6 3 6"/>'),
 '陸上':('#C98BFF','<circle cx="12" cy="5" r="2"/><path d="M12 7v6M8 9.5l8 1.5M9 19l3-6 3 6"/>'),
 'ラクロス':('#9aa3ad','<path d="M12 3.5l2.4 4.9 5.4.8-3.9 3.8.9 5.4L12 17.8l-4.8 2.6.9-5.4L4.2 9.2l5.4-.8z"/>'),
}
HEART='<svg viewBox="0 0 24 24"><path d="M12 20.3l-1.45-1.32C5.4 14.24 2 11.16 2 7.38 2 4.3 4.42 2 7.5 2c1.74 0 3.41.81 4.5 2.09C13.09 2.81 14.76 2 16.5 2 19.58 2 22 4.3 22 7.38c0 3.78-3.4 6.86-8.55 11.61L12 20.3z"/></svg>'
CMT='<svg viewBox="0 0 24 24"><path d="M21 11.5a8.5 8.5 0 0 1-12.2 7.7L3 21l1.8-5.8A8.5 8.5 0 1 1 21 11.5z"/></svg>'
def badge(sport):
    c,i=SPORT.get(sport,SPORT['ラクロス'])
    return '<span class="sb" style="background:%s"><svg viewBox="0 0 24 24">%s</svg></span>'%(c,i)
def card(img,sport,area,name,meta,tags=(),likes=0,comments=0,video=False,pr=False,new=False,liked=False,desc=''):
    return ('<div class="nc"><div class="nc-img"><img src="assets/preview-video/%s.jpg" alt="">%s%s'
            '<span class="nc-fav">%s</span>%s</div>'
            '<div class="nc-b"><div class="nc-top">%s<span class="sp">%s</span></div>'
            '<div class="nc-name">%s</div><div class="nc-area"><svg class="pin" viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 1 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.3"/></svg>%s</div>%s<div class="nc-meta">%s</div>%s'
            '<div class="nc-foot"><span class="lk%s">%s%d</span><span class="cm">%s%d</span></div></div></div>')%(
        img,('<span class="nc-new">新着</span>' if new else ''),('<span class="nc-pr">PR</span>' if pr else ''),HEART,
        ('<span class="nc-vid">▶ 動画</span>' if video else ''),badge(sport),sport,name,area,('<div class="nc-desc">%s</div>'%desc if desc else ''),meta,
        ('<div class="nc-tags">'+''.join('<span>%s</span>'%t for t in list(tags)[:3])+'</div>' if tags else ''),
        (' on' if liked else ''),HEART,likes,CMT,comments)

CLUBS=[
 dict(img='jp-soccer-run',sport='サッカー',area='世田谷区',name='わかばFC',desc='はじめてボールを触る子が半分。学年ごとにコースを分けて、体格差で怖い思いをさせません。',meta='小学1〜6年 ・ 週2（土日） ・ 月謝5,000円',tags=('体験OK','女の子歓迎'),likes=24,comments=6,video=True),
 dict(img='px-3448250',sport='サッカー',area='練馬区',name='青空サッカークラブ',desc='試合前に監督は何も言いません。子どもたちが自分で考えて動く時間を、いちばん大事にしています。',meta='小学1〜6年 ・ 週2（土日） ・ 月謝4,000円',tags=('体験OK',),likes=18,comments=3,video=True),
 dict(img='wm-outdoor',sport='サッカー',area='世田谷区',name='多摩川ジュニアSC',desc='土曜だけの少人数クラブです。河川敷のグラウンドで、年中さんから一緒に走っています。',meta='年中〜小6 ・ 週1（土） ・ 月謝4,000円',tags=('未就学から','入会金なし'),likes=9,comments=1),
 dict(img='px-399187',sport='野球',area='練馬区',name='石神井フットボール',desc='日曜だけの活動で県大会を目指しています。練習は少なめ、そのぶん1回に集中します。',meta='小学3〜6年 ・ 週1（日） ・ 月謝3,500円',tags=('体験OK',),likes=12,comments=2),
 dict(img='px-3755440',sport='バスケットボール',area='横浜市港北区',name='港北ジュニアバスケ',desc='コーチ4人のうち3人がもと保護者。負けた日ほど円が小さくなる、そんなチームです。',meta='小学3〜6年 ・ 週2（火木） ・ 月謝6,500円',tags=('女性指導者あり','体験OK'),likes=31,comments=8,video=True,liked=True),
 dict(img='wm-kidsrun-1',sport='陸上',area='杉並区',name='杉並アスレチッククラブ',desc='走るのが遅い子から走らせます。速さより、走るのが好きになることを先に。',meta='小学4〜6年 ・ 週1（日） ・ 月謝5,500円',tags=('体験OK',),likes=7,comments=0),
 dict(img='wm-bball-jp',sport='バスケットボール',area='さいたま市',name='さくらミニバスケットボールクラブ',desc='未就学から入れるミニバス。ボールを使わない鬼ごっこから始めます。',meta='小学1〜6年 ・ 週2（土日） ・ 月謝2,500円',tags=('未就学から',),likes=15,comments=4,video=True),
 dict(img='wm-karate',sport='空手',area='狛江市',name='狛江キッズ空手',desc='はじめの30分はずっと鬼ごっこ。礼儀と体づくりを、遊びの延長でやっています。',meta='未就学〜中学生 ・ 週1（土） ・ 月謝3,000円',tags=('未就学から','入会金なし'),likes=11,comments=2),
 dict(img='px-209977',sport='テニス',area='世田谷区',name='世田谷ジュニアテニス',desc='コース制で年齢と経験に合わせて練習します。セレクションはありますが、見学は自由です。',meta='小学3〜6年 ・ 週2（火土） ・ 月謝7,000円',tags=('コース制',),likes=5,comments=1),
]
NC_CSS='''
/* ===================== 標準クラブカード（全ページ共通） ===================== */
.news{display:grid;grid-template-columns:repeat(2,1fr);gap:16px 10px}
.nc{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;cursor:pointer;transition:border-color .15s,transform .15s}
.nc:hover{border-color:var(--accent);transform:translateY(-2px)}
.nc-img{position:relative;aspect-ratio:4/3;background:#000;overflow:hidden}
.nc-img img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.nc:hover .nc-img img{transform:scale(1.04)}
.nc-new{position:absolute;left:10px;top:10px;z-index:2;background:var(--accent);color:#fff;font-size:10.5px;font-weight:900;padding:4px 9px;border-radius:4px;letter-spacing:.05em}
body[data-skin="stadium"] .nc-new{color:#0b0c0f}
.nc-pr{position:absolute;left:10px;top:10px;z-index:2;background:rgba(0,0,0,.72);color:#fff;font-family:'Anton',sans-serif;font-size:9.5px;letter-spacing:.12em;padding:4px 8px;border-radius:3px}
.nc-new+.nc-pr{left:auto;right:48px}
.nc-fav{position:absolute;right:9px;top:9px;z-index:2;width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center}
.nc-fav svg{width:16px;height:16px;fill:none;stroke:#2b2b2b;stroke-width:2}
.nc-vid{position:absolute;right:9px;bottom:9px;z-index:2;background:var(--accent);color:#fff;font-size:10.5px;font-weight:900;padding:4px 8px;border-radius:4px}
body[data-skin="stadium"] .nc-vid{color:#0b0c0f}
.nc-b{padding:11px 12px 12px;display:flex;flex-direction:column;flex:1}
.nc-top{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:900;color:var(--sub);letter-spacing:.04em;margin-bottom:6px;min-width:0}
.sb{display:inline-flex;width:18px;height:18px;border-radius:50%;flex:none;align-items:center;justify-content:center}
.sb svg{width:12px;height:12px;fill:none;stroke:#fff;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.nc-top .sp{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.nc-area{display:flex;align-items:center;gap:4px;font-size:11px;font-weight:700;color:var(--sub);margin:-1px 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nc-area .pin{width:11px;height:11px;flex:none;fill:none;stroke:currentColor;stroke-width:1.9}
.nc-name{font-family:var(--fh);font-size:14px;font-weight:900;line-height:1.4;letter-spacing:var(--ls);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:5px;color:var(--ink)}
.nc-desc{font-size:11.5px;font-weight:700;color:var(--ink);line-height:1.65;margin:2px 0 6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.nc-meta{font-size:11px;font-weight:700;color:var(--sub);line-height:1.6}
.nc-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
.nc-tags span{font-size:10.5px;font-weight:900;border:1px solid var(--line);border-radius:999px;padding:3px 8px;color:var(--ink);max-width:11em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
body[data-skin="magazine"] .nc-tags span,body[data-skin="editorial"] .nc-tags span{border-radius:0}
.nc-foot{display:flex;align-items:center;gap:14px;margin-top:auto;padding-top:10px;font-size:12px;font-weight:900;color:var(--sub)}
.nc-foot span{display:inline-flex;align-items:center;gap:4px}
.nc-foot svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.9}
.nc-foot .lk.on{color:var(--accent2)}.nc-foot .lk.on svg{fill:var(--accent2);stroke:var(--accent2)}
@media(min-width:760px){.news{grid-template-columns:repeat(3,1fr);gap:24px 20px}.nc-name{font-size:15px}}
'''
