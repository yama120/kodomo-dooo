import re,os,sys
sys.path.insert(0,'/private/tmp/claude-501/-Users-hyogoyamada-claudecode-project/5ae8baa4-4330-4bf8-b599-64aa8ac5ef83/scratchpad/')
import cards
P='/private/tmp/claude-501/-Users-hyogoyamada-claudecode-project/5ae8baa4-4330-4bf8-b599-64aa8ac5ef83/scratchpad/'
D=os.path.expanduser('~/kodomo-dooo-deploy/')
top=open(D+'video-hero-preview.html',encoding='utf-8').read()
BASE_CSS=top[top.index('<style>')+7:top.index('</style>')]
header=top[top.index('<header'):top.index('</header>')+9]
footer=top[top.index('<footer>'):top.index('</footer>')+9]
tail=top[top.index('<div id="skins">'):top.index('</body>')]
club_css=open(P+'page.css',encoding='utf-8').read()   # クラブ詳細の部品（.nc .art .rel .cta2 など）

FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&family=Zen+Old+Mincho:wght@600;900&family=Anton&display=swap" rel="stylesheet">'

COMMON='''
/* ---- 共通（サブページ） ---- */
.pgh{padding:22px 0 6px}
.pgh .bc{font-size:11.5px;font-weight:700;color:var(--sub);display:flex;gap:5px;flex-wrap:wrap;margin-bottom:12px}
.pgh h1{font-family:var(--fh);margin:0 0 6px;font-size:clamp(24px,6vw,40px);font-weight:900;line-height:1.3;letter-spacing:var(--ls)}
.pgh h1 em{font-style:normal;color:var(--accent)}
.pgh .ld{font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.btn{display:inline-block;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:14.5px;border-radius:calc(var(--r) - 4px);padding:14px 22px;text-align:center}
body[data-skin="stadium"] .btn{color:#0b0c0f}
.btn.ghost{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.btn.blockb{display:block}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:8px 13px;font-size:12.5px;font-weight:900;cursor:pointer;white-space:nowrap}
.chip.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
body[data-skin="magazine"] .chip,body[data-skin="editorial"] .chip{border-radius:0}
.chip svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.blk{margin-top:34px}
.blk h2{font-family:var(--fh);margin:0 0 4px;font-size:clamp(17px,4.2vw,22px);font-weight:900;letter-spacing:var(--ls);border-top:2px solid var(--ink);padding-top:13px}
.blk h2 em{font-style:normal;color:var(--accent)}
.blk .sub{margin:0 0 14px;font-size:12px;font-weight:700;color:var(--sub)}
@media(min-width:760px){.blk{margin-top:52px}.pgh{padding:34px 0 10px}}
'''

def page(fname,title,body,css='',bodyattr='data-skin="bright"',extra_js=''):
    html=('<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
          '<meta name="robots" content="noindex,nofollow">\n<title>'+title+'</title>\n'+FONTS+'\n<link rel="stylesheet" href="preview-quiz.css">\n<style>'+BASE_CSS+club_css+COMMON+css+'</style>\n</head>\n'
          '<body '+bodyattr+'>\n\n'+header+'\n'+body+'\n'+footer+'\n\n'+tail+extra_js+'\n<script src="preview-quiz.js"></script>\n</body>\n</html>')
    open(D+fname,'w',encoding='utf-8').write(html)
    o=len(re.findall(r'<div\b',html)); c=len(re.findall(r'</div>',html))
    miss=[m for m in set(re.findall(r'src="(assets/[^"]+)"',html)) if not os.path.exists(D+m)]
    print(f'{fname}: {len(html)//1024}KB  div差={o-c}  missing={miss}')

IMG=['jp-soccer-duel','wm-bball-jp','wm-karate','wm-kidsrun-1','px-3755440','wm-outdoor','px-3448250','px-399187','px-209977']
def nc(img,meta,hl,name,place,video=True,pr=False,new=False):
    return ('<div class="nc"><div class="nc-img"><img src="assets/preview-video/%s.jpg" alt="">%s%s'
            '<span class="nc-fav"><svg viewBox="0 0 24 24"><path d="M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9z"/></svg></span></div>'
            '<div class="nc-b"><div class="nc-meta">%s</div><div class="nc-hl">%s</div><div class="nc-name">%s</div><div class="nc-place">%s</div>%s</div></div>'
            %(img,('<span class="nc-new">新着</span>' if new else ''),('<span class="nc-new" style="left:auto;right:48px;background:rgba(0,0,0,.72);color:#fff">PR</span>' if pr else ''),
              meta,hl,name,place,('<span class="nc-tag"><span class="v">▶</span>動画あり</span>' if video else '')))

CLUBS=[('jp-soccer-duel','サッカー ・ 小学1〜6年','6年生が、1年生の靴をそろえる','わかばFC','世田谷区 桜丘 ・ 千歳船橋駅 徒歩8分<br>週2回（土日） ・ 月謝5,000円',True),
 ('px-3448250','サッカー ・ 小学1〜6年','試合前、監督はなにも言わない','青空サッカークラブ','練馬区 石神井台 ・ 大泉学園駅 徒歩12分<br>週2回（土日） ・ 月謝4,000円',True),
 ('wm-outdoor','サッカー ・ 年中〜小6','土曜だけ、全力で','多摩川ジュニアSC','世田谷区 玉川 ・ 二子玉川駅 徒歩10分<br>週1回（土） ・ 月謝4,000円',False),
 ('px-399187','サッカー ・ 小学3〜6年','日曜だけ。それでも県大会に行く','石神井フットボール','練馬区 石神井町 ・ 石神井公園駅 徒歩7分<br>週1回（日） ・ 月謝3,500円',False),
 ('px-3755440','サッカー ・ 小学1〜6年','半分は、入ってから始めた子','大森フットボールクラブ','大田区 大森北 ・ 大森駅 徒歩9分<br>週2回（水土） ・ 月謝4,500円',True),
 ('wm-kidsrun-1','サッカー ・ 未就学〜小2','はじめの30分は、ずっと鬼ごっこ','経堂キッズサッカー','世田谷区 経堂 ・ 経堂駅 徒歩5分<br>週1回（土） ・ 月謝3,000円',False),
 ('wm-bball-jp','サッカー ・ 小学1〜6年','コーチ4人が、全員もと保護者','桜丘SC','世田谷区 桜丘 ・ 千歳船橋駅 徒歩11分<br>週2回（土日） ・ 月謝4,000円',True),
 ('wm-karate','サッカー ・ 小学1〜4年','雨の日は体育館で、鬼ごっこ','用賀ジュニア','世田谷区 用賀 ・ 用賀駅 徒歩6分<br>週1回（日） ・ 月謝3,500円',False),
 ('px-209977','サッカー ・ 小学3〜6年','女の子が、8人います','FC三軒茶屋','世田谷区 三軒茶屋 ・ 三軒茶屋駅 徒歩8分<br>週2回（火土） ・ 月謝5,500円',False)]

# ================================================================ 1. 検索結果
search_css='''
.fbar{position:sticky;top:60px;z-index:40;background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);margin:0 -20px;padding:10px 20px}
.fbar .row{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.fbar .row::-webkit-scrollbar{display:none}
.fbar .kw{display:flex;gap:8px;margin-bottom:8px}
.fbar .kw input{flex:1;min-width:0;border:1px solid var(--line);background:var(--card);border-radius:calc(var(--r) - 4px);padding:11px 13px;font-family:var(--f);font-size:14px}
.fbar .kw button{border:0;background:var(--ink);color:var(--bg);font-family:var(--fh);font-weight:900;border-radius:calc(var(--r) - 4px);padding:0 16px}
.rhead{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;padding:18px 0 12px}
.rhead h1{font-family:var(--fh);margin:0;font-size:clamp(18px,4.8vw,26px);font-weight:900;letter-spacing:var(--ls);line-height:1.35}
.rhead h1 small{display:block;font-size:12px;font-weight:700;color:var(--sub);margin-top:4px}
.rhead select{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:8px 12px;font-family:var(--f);font-size:12px;font-weight:900;color:var(--ink)}
.vsw{display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;margin-left:8px}
.vsw a{padding:8px 12px;font-size:12px;font-weight:900;color:var(--sub)}
.vsw a.on{background:var(--ink);color:var(--bg)}
.news{margin-top:8px}
.rhead{flex-wrap:wrap}
.nc .nc-img .nc-new{z-index:3}
.pager{display:flex;justify-content:center;gap:6px;margin-top:34px}
.pager a{min-width:38px;height:38px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;font-size:13px;font-weight:900;color:var(--sub)}
.pager a.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.empty{margin-top:22px;border:1.5px dashed var(--line);padding:26px 18px;text-align:center}
.empty .t{font-family:var(--fh);font-size:17px;font-weight:900;margin-bottom:6px}
.empty p{margin:0 0 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
.empty .in{display:flex;gap:8px;max-width:460px;margin:0 auto}
.empty input{flex:1;min-width:0;border:1px solid var(--line);border-radius:calc(var(--r) - 4px);padding:12px;font-family:var(--f);font-size:13.5px}
.seo2 h3{font-family:var(--fh);margin:26px 0 8px;font-size:14px;font-weight:900}
.seo2 .row{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:12.5px;font-weight:700;color:var(--sub)}
.slay{display:grid;grid-template-columns:1fr;gap:18px;align-items:start}
.fside{display:none;background:var(--card);border:1px solid var(--line);padding:18px 16px 20px}
.fside.open{display:block}
body[data-skin="bright"] .fside,body[data-skin="stadium"] .fside{border-radius:var(--r)}
.fside .ttl{display:flex;align-items:center;gap:8px;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:16px}
.fside .ttl svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2}
.fside .lb{font-size:11px;font-weight:900;letter-spacing:.1em;color:var(--sub);margin:16px 0 8px}
.fside .lb:first-of-type{margin-top:0}
.fside select,.fside input[type=text]{width:100%;border:1px solid var(--line);background:var(--card);padding:11px 12px;font-family:var(--f);font-size:13.5px;color:var(--ink);margin-bottom:8px;appearance:none;-webkit-appearance:none}
body[data-skin="bright"] .fside select,body[data-skin="stadium"] .fside select{border-radius:var(--r-s,9px)}
.fside .ages{display:flex;gap:7px}
.fside .ages span{flex:1;text-align:center;border:1px solid var(--line);padding:9px 0;font-size:12.5px;font-weight:900;cursor:pointer}
.fside .ages span.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.fside label{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:700;padding:5px 0;cursor:pointer}
.fside label i{width:18px;height:18px;border:1px solid var(--line);flex:none;display:inline-block;background:var(--card)}
.fside label i.r{border-radius:50%}
.fside label i.on{background:var(--accent);border-color:var(--accent);box-shadow:inset 0 0 0 3px var(--card)}
.fside .apply{display:block;width:100%;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px;text-align:center;margin-top:18px}
body[data-skin="stadium"] .fside .apply{color:#0b0c0f}
.fside .clear{display:block;width:100%;border:1.5px solid var(--ink);color:var(--ink);font-weight:900;font-size:13.5px;padding:12px;text-align:center;margin-top:8px}
.ftog{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:var(--card);padding:10px 14px;font-size:12.5px;font-weight:900;cursor:pointer;font-family:var(--f);color:var(--ink)}
.ftog svg{width:15px;height:15px;fill:none;stroke:var(--accent);stroke-width:2}
@media(min-width:760px){.fbar{position:static;margin:0;padding:18px 0 6px;border:0;background:transparent;backdrop-filter:none}.fbar .kw{max-width:640px}.rhead{padding:26px 0 16px}}
.rec{display:grid;grid-template-columns:repeat(2,1fr);gap:16px 10px;margin-top:8px}
@media(min-width:760px){.rec{grid-template-columns:repeat(4,1fr);gap:24px 20px}}
.prband .ads{margin-top:8px}
@media(min-width:900px){.slay{grid-template-columns:280px 1fr;gap:36px}.fside{display:block;position:sticky;top:76px}.ftog{display:none}.fbar{display:none}.rhead{padding:6px 0 16px}}
'''
def chip(t,on=False,ic=''):
    return '<span class="chip%s">%s%s</span>'%(' on' if on else '',ic,t)
PIN='<svg viewBox="0 0 24 24"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>'
BALL='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17M3.5 12h17"/></svg>'
SL='<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/><circle cx="9" cy="7" r="2.1"/><circle cx="15" cy="12" r="2.1"/><circle cx="8" cy="17" r="2.1"/></svg>'
cards_html=[cards.card(**dict(c,pr=(i<2))) for i,c in enumerate(cards.CLUBS)]
rec_html=[cards.card(**dict(c,pr=True,new=False)) for c in cards.CLUBS[2:6]]
search_body='''
<main><div class="wrap">
  <div class="fbar">
    <div class="kw"><input value="世田谷区 サッカー"><button>検索</button></div>
    <button class="ftog" type="button" id="ftog"><svg viewBox="0 0 24 24"><path d="M3 5h18M6 12h12M10 19h4"/></svg>条件検索</button>
  </div>
  <div class="slay">
  <aside class="fside" id="fside">
    <div class="ttl"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.2-3.2"/></svg>条件検索</div>
    <div class="lb">フリーワード</div><input type="text" placeholder="例）サッカー、野球、バスケットボール">
    <div class="lb">地域</div><select><option>東京都</option></select><select><option>世田谷区</option></select>
    <div class="lb">種目（カテゴリ）</div><select><option>サッカー</option></select>
    <div class="lb">対象年齢</div><div class="ages"><span>未就学</span><span class="on">小学生</span><span>中学生</span></div>
    <div class="lb">こだわり条件</div>
    <label><i class="on"></i>体験OK</label><label><i></i>平日開催</label><label><i></i>土日開催</label><label><i></i>女の子歓迎</label><label><i></i>女性指導者あり</label><label><i></i>入会金なし</label>
    <div class="lb">月謝</div>
    <label><i class="r"></i>〜3,000円</label><label><i class="r"></i>〜5,000円</label><label><i class="r"></i>〜8,000円</label><label><i class="r"></i>〜10,000円</label><label><i class="r on"></i>指定しない</label>
    <a class="apply" href="#">この条件で表示</a><a class="clear" href="#">条件をクリア</a>
  </aside>
  <div class="sres">
  <div class="note">【検索結果】★PCは<b>左に条件検索パネル・右に結果</b>（現行と同じ配置。パネルは追従）。スマホは検索窓＋「条件検索」ボタンで開閉。★カードには<b>クラブの紹介文を2行</b>（現行カードにもある。クラブの声が一覧で読める）。結果の見出しは「条件×件数」で、いま何を見ているかを迷わせない。カードは新着カードと同じ型（見出し大・月謝は小さい行）。<b>PR枠は上位2件・PR表記</b>で、収益枠でもカードの型は同じにして違和感を出さない。並び替えに「月謝が安い順」は置くが既定は「おすすめ順」。★0件のときは<b>空白ではなく通知登録の入口</b>にする（12都道府県しか埋まっていない現状では、0件が最も多い画面になる）。</div>
  <div class="rhead">
    <h1>世田谷区 × サッカー<small>14クラブ ・ うち動画あり 4</small></h1>
    <div><select><option>おすすめ順</option><option>新着順</option><option>月謝が安い順</option><option>近い順</option></select><span class="vsw"><a class="on" href="#">一覧</a><a href="map-preview.html">地図</a></span></div>
  </div>
  <div class="news">
%s
  </div>
  <div class="pager"><a class="on" href="#">1</a><a href="#">2</a><a href="#">›</a></div>
  </div>
  </div>
</div>
<div class="prband">
  <div class="wrap">
  <div class="note">【収益枠】検索結果の下に<b>おすすめクラブ（PR）</b>と<b>地域のおすすめ企業（PR）</b>。ここが広報収益の枠。クラブは検索結果と同じカード型でPR表記だけ付ける（違和感を出さない）。企業枠はロゴ＋一言で、検索している地域に合わせて出す。</div>
  <div class="blk">
    <h2>おすすめクラブ<span class="pr-lb">PR</span></h2>
    <div class="sub">世田谷区・周辺で、いま募集しているクラブ。</div>
    <div class="rec">
%s
    </div>
  </div>
  <div class="blk">
    <h2>地域のおすすめ企業<span class="pr-lb">PR</span></h2>
    <div class="sub">世田谷区の子育て世帯に向けた、地域のお店・サービス。</div>
    <div class="ads">
      <div class="a"><div class="lg">D</div><div class="t">デザインボックス<small>チームのユニフォーム制作</small></div></div>
      <div class="a"><div class="lg">S</div><div class="t">桜丘整骨院<small>スポーツ外傷・子ども割引</small></div></div>
      <div class="a"><div class="lg">K</div><div class="t">経堂スポーツ用品<small>ジュニア用品・名入れ無料</small></div></div>
      <div class="a"><div class="lg">M</div><div class="t">みどり歯科<small>マウスガード作成</small></div></div>
    </div>
    <div class="ads-more">この枠に掲載する事業者の方は <a href="partner-preview.html">掲載のご案内</a> へ。</div>
  </div>
  </div>
</div>
<div class="wrap">
  <div class="blk">
    <h2>もし0件だったら（表示例）</h2>
    <div class="sub">条件に合うクラブが無いときの画面です。</div>
    <div class="empty">
      <div class="t">この条件のクラブは、まだ載っていません。</div>
      <p>近くに載ったらお知らせします。メールアドレスだけで登録できます。</p>
      <div class="in"><input placeholder="you@example.com"><a class="btn" href="#">お知らせを受け取る</a></div>
    </div>
  </div>

  <div class="seo2">
    <h3>世田谷区のほかの種目</h3>
    <div class="row"><a href="#">野球</a><a href="#">バスケットボール</a><a href="#">ダンス</a><a href="#">水泳</a><a href="#">空手</a><a href="#">体操</a><a href="#">テニス</a></div>
    <h3>近くのエリアのサッカー</h3>
    <div class="row"><a href="#">杉並区</a><a href="#">狛江市</a><a href="#">目黒区</a><a href="#">渋谷区</a><a href="#">調布市</a><a href="#">川崎市高津区</a></div>
  </div>
  <div style="height:40px"></div>
</div></main>
'''%("\n".join(cards_html),"\n".join(rec_html))
page('search-preview-v1.html','世田谷区のサッカークラブ 14件｜チビスポ（検索結果プレビュー v1・標準）',search_body,search_css,extra_js="<script>(function(){var t=document.getElementById('ftog'),a=document.getElementById('fside');if(t&&a)t.addEventListener('click',function(){a.classList.toggle('open')})})();</script>")

exec(open(P+'search_v2.py',encoding='utf-8').read())

# ================================================================ 2. 地図
map_css='''
.mapwrap{position:relative;margin:0 -20px;height:calc(100vh - 60px);min-height:520px;overflow:hidden;background:#0b0d10}
.mapwrap>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}
.mtop{position:absolute;left:0;right:0;top:0;z-index:5;padding:12px 14px;display:flex;gap:8px;align-items:center}
.mtop .kw{flex:1;display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.96);border-radius:999px;padding:11px 14px;font-size:13px;font-weight:900;color:#2b2b2b;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.mtop .kw svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2}
.mtop .loc{width:42px;height:42px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.mtop .loc svg{width:18px;height:18px;fill:none;stroke:#2b2b2b;stroke-width:2}
.mchips{position:absolute;left:0;right:0;top:64px;z-index:5;display:flex;gap:8px;padding:0 14px;overflow-x:auto;scrollbar-width:none}
.mchips::-webkit-scrollbar{display:none}
.mchips .chip{background:rgba(255,255,255,.96);border-color:transparent;box-shadow:0 4px 14px rgba(0,0,0,.2);color:#2b2b2b}
.mchips .chip.on{background:var(--accent);color:#fff}
body[data-skin="stadium"] .mchips .chip.on{color:#0b0c0f}
.pin{position:absolute;z-index:4;transform:translate(-50%,-100%);cursor:pointer;transition:transform .2s}
.pin .b{background:#fff;color:#2b2b2b;font-size:11.5px;font-weight:900;padding:6px 10px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.35);white-space:nowrap;border:2px solid transparent}
.pin::after{content:"";position:absolute;left:50%;bottom:-6px;width:10px;height:10px;background:#fff;transform:translateX(-50%) rotate(45deg)}
.pin.on{transform:translate(-50%,-100%) scale(1.08);z-index:6}
.pin.on .b{background:var(--accent);color:#fff;border-color:#fff}
body[data-skin="stadium"] .pin.on .b{color:#0b0c0f}
.pin.on::after{background:var(--accent)}
.mcards{position:absolute;left:0;right:0;bottom:0;z-index:6;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding:0 14px 14px;scrollbar-width:none}
.mcards::-webkit-scrollbar{display:none}
.mc{flex:0 0 82%;scroll-snap-align:center;background:var(--card);border-radius:var(--r);overflow:hidden;display:flex;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.mc img{width:104px;flex:none;object-fit:cover}
.mc .b{padding:11px 12px;min-width:0}
.mc .hl{font-family:var(--fh);font-size:13.5px;font-weight:900;line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.mc .nm{font-size:12px;font-weight:900;margin-top:4px}
.mc .m{font-size:11px;font-weight:700;color:var(--sub);margin-top:3px;line-height:1.6}
.mc.on{outline:2px solid var(--accent)}
.mlist{display:none}
@media(min-width:900px){
  .mapwrap{margin:0;height:calc(100vh - 60px);display:grid;grid-template-columns:1fr 420px;border-radius:var(--r)}
  .mapwrap>img{grid-column:1}
  .mcards{display:none}
  .mlist{display:block;grid-column:2;position:relative;z-index:6;background:var(--bg);overflow-y:auto;border-left:1px solid var(--line);padding:14px}
  .mlist .h{font-family:var(--fh);font-size:15px;font-weight:900;margin:4px 0 12px}
  .mlist .h small{font-weight:700;color:var(--sub);font-size:12px;margin-left:8px}
  .mlist .mc{flex:none;margin-bottom:10px;box-shadow:none;border:1px solid var(--line);cursor:pointer}
  .mtop,.mchips{right:420px}
}
'''
pins=[(38,46,'わかばFC'),(52,38,'桜丘SC'),(63,58,'経堂キッズ'),(30,62,'多摩川ジュニアSC'),(72,32,'FC三軒茶屋'),(46,72,'用賀ジュニア')]
pin_html="".join('<div class="pin%s" data-i="%d" style="left:%d%%;top:%d%%"><span class="b">%s</span></div>'%(' on' if i==0 else '',i,x,y,n) for i,(x,y,n) in enumerate(pins))
def mc(i,img,hl,nm,m,on=False):
    return '<div class="mc%s" data-i="%d"><img src="assets/preview-video/%s.jpg" alt=""><div class="b"><div class="hl">%s</div><div class="nm">%s</div><div class="m">%s</div></div></div>'%(' on' if on else '',i,img,hl,nm,m)
mcs=[mc(0,'jp-soccer-duel','6年生が、1年生の靴をそろえる','わかばFC','サッカー ・ 千歳船橋 徒歩8分 ・ 月謝5,000円',True),
     mc(1,'wm-bball-jp','コーチ4人が、全員もと保護者','桜丘SC','サッカー ・ 千歳船橋 徒歩11分 ・ 月謝4,000円'),
     mc(2,'wm-kidsrun-1','はじめの30分は、ずっと鬼ごっこ','経堂キッズサッカー','サッカー ・ 経堂 徒歩5分 ・ 月謝3,000円'),
     mc(3,'wm-outdoor','土曜だけ、全力で','多摩川ジュニアSC','サッカー ・ 二子玉川 徒歩10分 ・ 月謝4,000円'),
     mc(4,'px-209977','女の子が、8人います','FC三軒茶屋','サッカー ・ 三軒茶屋 徒歩8分 ・ 月謝5,500円'),
     mc(5,'wm-karate','雨の日は体育館で、鬼ごっこ','用賀ジュニア','サッカー ・ 用賀 徒歩6分 ・ 月謝3,500円')]
map_body='''
<main><div class="wrap">
  <div class="note">【地図で探す】Googleマップ型。<b>スマホ＝地図が全画面、下にカードが横スワイプ</b>／<b>PC＝左に地図・右にリスト</b>。ピンは「◯」ではなく<b>クラブ名の吹き出し</b>にして、ズームしなくても何があるか分かる。上に検索窓と現在地ボタン、種目チップが浮く。ピンとカードは連動（どちらをタップしても相手が光る）。地図タイルは本番では CARTO（APIキー必須・帰属表示必須）。ここは背景画像で代用。</div>
  <div class="mapwrap">
    <img src="assets/app-hero/2026-09-05_map-bg-dark.png" alt="">
    <div class="mtop"><div class="kw"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>世田谷区 サッカー</div><div class="loc"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><circle cx="12" cy="12" r="8"/></svg></div></div>
    <div class="mchips">%s%s%s%s%s</div>
    %s
    <div class="mcards">%s</div>
    <div class="mlist"><div class="h">この範囲のクラブ<small>6件</small></div>%s</div>
  </div>
</div></main>
'''%(chip('すべて',True),chip('サッカー'),chip('野球'),chip('バスケ'),chip('ダンス'),pin_html,"".join(mcs),"".join(mcs))
map_js='''<script>
(function(){function sel(i){document.querySelectorAll('.pin,.mc').forEach(function(e){e.classList.toggle('on',e.dataset.i===String(i))});
 var c=document.querySelector('.mcards .mc[data-i="'+i+'"]');if(c&&c.scrollIntoView)c.scrollIntoView({behavior:'smooth',inline:'center',block:'nearest'})}
 document.querySelectorAll('.pin,.mc').forEach(function(e){e.addEventListener('click',function(){sel(e.dataset.i)})});})();
</script>'''
# map-preview.html は reskin_map.py（現行 map.html のリスキン）が正。ここでは生成しない
# page('map-preview.html', ...)

# ================================================================ 3. マガジン一覧
mag_css='''
.mhero{padding:28px 0 8px}
.mhero .big{font-family:'Anton',sans-serif;font-size:clamp(54px,16vw,150px);line-height:.9;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px var(--ink)}
body[data-skin="stadium"] .mhero .big{-webkit-text-stroke-color:var(--accent)}
.mhero .ld{margin-top:8px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.9}
.cats{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:16px 0 4px}
.cats::-webkit-scrollbar{display:none}
.feat{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:4/5;margin-top:14px;cursor:pointer}
.feat img{width:100%;height:100%;object-fit:cover}
.feat::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(0,0,0,.85))}
.feat .t{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:18px 16px;color:#fff}
.feat .t .c{font-size:11px;font-weight:900;letter-spacing:.1em;color:var(--accent);margin-bottom:8px}
body[data-skin="magazine"] .feat .t .c{color:#ffd98a}
.feat .t h2{font-family:var(--fh);margin:0 0 8px;font-size:clamp(20px,5.4vw,34px);font-weight:900;line-height:1.35}
.feat .t p{margin:0;font-size:12.5px;font-weight:700;color:rgba(255,255,255,.85);line-height:1.8}
.mgrid{display:grid;grid-template-columns:1fr;gap:18px;margin-top:22px}
.mi{cursor:pointer}
.mi img{aspect-ratio:16/10;width:100%;object-fit:cover;border-radius:var(--r)}
.mi .c{font-size:10.5px;font-weight:900;letter-spacing:.1em;color:var(--accent);margin:10px 0 5px}
.mi h3{font-family:var(--fh);margin:0 0 6px;font-size:15px;font-weight:900;line-height:1.55}
.mi .d{font-size:11px;font-weight:700;color:var(--sub)}
@media(min-width:760px){.feat{aspect-ratio:21/9}.feat .t{padding:34px 36px;max-width:640px}.mgrid{grid-template-columns:repeat(3,1fr);gap:26px 22px}}
'''
ARTS=[('クラブ選び','「うちの子に合うクラブ」の見つけ方・5つの視点','2026.06.12','jp-soccer-duel'),
      ('子どもの一歩','6歳までの運動が、脳を育てる。幼児期に大切にしたい「多様な動き」','2026.06.20','wm-kidsrun-1'),
      ('子どもの一歩','年齢別・おすすめの運動と「やりすぎ注意」な運動','2026.06.18','wm-outdoor'),
      ('クラブ選び','運動が苦手な子でも、楽しく続く習い事の見つけ方','2026.06.15','wm-karate'),
      ('コーチの想い','コーチに聞く「チームで伸びる子」の共通点','2026.06.01','wm-bball-jp'),
      ('はじめて','子どものやる気を引き出す、声かけのコツ','2026.06.09','px-3755440'),
      ('はじめて','けがを防ぐ！練習前後のストレッチ習慣','2026.06.08','px-399187')]
mi="".join('<div class="mi"><img src="assets/preview-video/%s.jpg" alt=""><div class="c">%s</div><h3>%s</h3><div class="d">%s</div></div>'%(im,c,t,d) for c,t,d,im in ARTS[1:])
mag_body='''
<main><div class="wrap">
  <div class="note">【マガジン一覧】雑誌の目次。巨大な「MAGAZINE」は中抜きで、記事の写真を邪魔しない。<b>特集1本を大きく</b>＋グリッド（cowcamo MAGAZINEと同じ配分）。カテゴリは既存フッターの4分類（クラブのらしさ／コーチの想い／子どもの一歩／はじめてのスポーツ選び）。記事タイトルは実在の7本。</div>
  <div class="mhero"><div class="big">MAGAZINE</div><div class="ld">クラブ選びの前に、読んでおくと少し楽になる話。</div></div>
  <div class="cats">%s%s%s%s%s</div>
  <div class="feat"><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""><div class="t"><div class="c">クラブ選び ・ 特集</div><h2>「うちの子に合うクラブ」の見つけ方・5つの視点</h2><p>強いか弱いかより先に見るところがあります。見学の前に、5つだけ。</p></div></div>
  <div class="mgrid">%s</div>
  <div style="height:40px"></div>
</div></main>
'''%(chip('すべて',True),chip('クラブ選び'),chip('コーチの想い'),chip('子どもの一歩'),chip('はじめて'),mi)
page('magazine-preview-v1.html','マガジン｜チビスポ（プレビュー v1）',mag_body,mag_css)
exec(open(P+'mag_v2.py',encoding='utf-8').read())

# ================================================================ 4. 記事
art_css='''
.ahead{padding:26px 0 0;max-width:760px}
.ahead .c{font-size:11px;font-weight:900;letter-spacing:.12em;color:var(--accent);margin-bottom:10px}
.ahead h1{font-family:var(--fh);margin:0 0 12px;font-size:clamp(23px,5.8vw,38px);font-weight:900;line-height:1.4;letter-spacing:var(--ls)}
.ahead .by{display:flex;align-items:center;gap:10px;font-size:12px;font-weight:700;color:var(--sub)}
.ahead .by img{width:32px;height:32px;border-radius:50%}
.akv{margin:18px 0 0;border-radius:var(--r);overflow:hidden;aspect-ratio:16/9}
.akv img{width:100%;height:100%;object-fit:cover}
.alay{display:grid;grid-template-columns:1fr;gap:30px;margin-top:22px}
.toc{border:1px solid var(--line);padding:14px 16px;background:var(--card)}
.toc .t{font-size:11px;font-weight:900;letter-spacing:.12em;color:var(--sub);margin-bottom:8px}
.toc ol{margin:0;padding-left:1.3em;font-size:12.5px;font-weight:700;line-height:2}
.art-body{max-width:720px;font-size:15px;font-weight:500;line-height:2.1}
body[data-skin="stadium"] .art-body{font-weight:700}
.art-body h2{font-family:var(--fh);font-size:clamp(18px,4.6vw,24px);font-weight:900;line-height:1.5;margin:40px 0 14px;padding-left:14px;border-left:4px solid var(--accent)}
.art-body p{margin:0 0 20px}
.art-body .lead{font-weight:700;font-size:15.5px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:16px 0;margin-bottom:26px}
.art-body blockquote{margin:22px 0;padding:16px 18px;background:color-mix(in srgb,var(--accent) 7%,var(--bg));font-family:var(--fh);font-size:16px;font-weight:900;line-height:1.7}
.art-body figure{margin:24px 0}
.art-body figure img{border-radius:var(--r);width:100%}
.art-body figcaption{font-size:11.5px;font-weight:700;color:var(--sub);margin-top:6px}
.acta{margin:34px 0;border:1.5px solid var(--accent);padding:20px 18px;text-align:center}
.acta .t{font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:10px}
.acta p{margin:0 0 12px;font-size:12.5px;font-weight:700;color:var(--sub)}
.aside .blk{margin-top:0}
.aside .blk+.blk{margin-top:28px}
.share{display:flex;gap:8px;margin-top:26px}
.share a{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:12px;font-weight:900;color:var(--sub)}
@media(min-width:900px){.alay{grid-template-columns:1fr 300px;gap:56px}.toc{position:sticky;top:76px}}
'''
art_body='''
<main><div class="wrap">
  <div class="pgh"><div class="bc"><a href="#">ホーム</a> › <a href="magazine-preview.html">マガジン</a> › 子どもの一歩</div></div>
  <div class="note">【記事】本文は<b>720px幅・15px・行間2.1</b>で読み物として成立させる。見出しは左に朱の縦線（雑誌の小見出し）。PCは右に目次（追従）＋関連クラブ。★記事内のクラブへのリンクは feature-track.js の計測対象（/go/&lt;clubId&gt;/chibispo-feature）。記事中盤と末尾に検索へのCTA。本文は magazine-1.html の実タイトル・実見出しを使用（本文は要約サンプル）。</div>
  <div class="ahead">
    <div class="c">子どもの一歩</div>
    <h1>6歳までの運動が、脳を育てる。幼児期に大切にしたい「多様な動き」</h1>
    <div class="by"><img src="assets/app-hero/app-icon-512.webp" alt=""><span>チビスポ編集部 ・ 2026.06.20 ・ 読了 6分</span></div>
  </div>
  <div class="akv"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""></div>
  <div class="alay">
    <article class="art-body">
      <p class="lead">「何歳から始めればいいですか」は、いちばん多い質問です。答えは種目によって違いますが、6歳までに大事なのは種目ではなく「動きの種類」でした。</p>
      <h2 id="s1">神経系は6歳までに約9割が発達する</h2>
      <p>スキャモンの発育曲線では、神経系の発達は5〜6歳でおおよそ8〜9割に達するとされています。走る・跳ぶ・投げる・つかまる・バランスをとる。この時期にいろいろな動きを経験した子は、あとから新しいスポーツを始めたときの覚えが早い、というのが多くの指導者の実感です。</p>
      <blockquote>「早くから1つに絞る」は、逆効果になることがあります。</blockquote>
      <h2 id="s2">「早くから1つに絞る」は逆効果になりうる</h2>
      <p>同じ動きだけを繰り返すと、使う筋肉と神経が偏ります。幼児期は「上手になる」より「いろいろやる」ほうが、結果として伸びしろが残ります。</p>
      <figure><img src="assets/preview-video/wm-outdoor.jpg" alt=""><figcaption>公園で走り回るのも、立派な「多様な動き」です。</figcaption></figure>
      <h2 id="s3">家庭でできる「多様な動き」遊び</h2>
      <p>鬼ごっこ、けんけんぱ、ボール投げ、木登り、雲梯。特別な道具は要りません。週に何回、どれくらい、より「飽きないうちにやめる」ほうが続きます。</p>
      <div class="acta"><div class="t">「いろいろやる」ができるクラブを探す</div><p>未就学から通えて、体験OKのクラブに絞れます。</p><a class="btn" href="search-preview.html">未就学からのクラブを見る</a></div>
      <h2 id="s4">習い事として始めるなら</h2>
      <p>まずは体験に行って、練習の最初の30分を見てください。準備運動が「走る・跳ぶ・転がる」で構成されているクラブは、この時期の子に向いています。</p>
      <h2 id="s5">クラブの体験に行くなら、ここを見る</h2>
      <p>コーチが子どもの目線までしゃがんで話しているか。できなかった子にどう声をかけているか。この2つだけ見れば、雰囲気はだいたい分かります。</p>
      <div class="share"><a href="#">X</a><a href="#">LINE</a><a href="#">リンクをコピー</a></div>
    </article>
    <aside class="aside">
      <div class="toc"><div class="t">目次</div><ol><li><a href="#s1">神経系は6歳までに約9割が発達する</a></li><li><a href="#s2">「早くから1つに絞る」は逆効果になりうる</a></li><li><a href="#s3">家庭でできる「多様な動き」遊び</a></li><li><a href="#s4">習い事として始めるなら</a></li><li><a href="#s5">体験に行くなら、ここを見る</a></li></ol></div>
      <div class="blk" style="margin-top:28px"><h2>この記事に出てくるクラブ</h2>
        <div class="rel" style="grid-template-columns:1fr">
          <div class="c"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><div class="n">はじめの30分は、ずっと鬼ごっこ</div><div class="m">経堂キッズサッカー／未就学〜小2</div></div>
        </div></div>
      <div class="blk"><h2>関連する記事</h2>
        <div class="arts">
          <div class="art"><div class="b"><h3>年齢別・おすすめの運動と「やりすぎ注意」な運動</h3><div class="m"><b>子どもの一歩</b>2026/06/18</div></div><img src="assets/preview-video/wm-outdoor.jpg" alt=""></div>
          <div class="art"><div class="b"><h3>運動が苦手な子でも、楽しく続く習い事の見つけ方</h3><div class="m"><b>クラブ選び</b>2026/06/15</div></div><img src="assets/preview-video/wm-karate.jpg" alt=""></div>
        </div></div>
    </aside>
  </div>
  <div style="height:40px"></div>
</div></main>
'''
page('article-preview-v1.html','6歳までの運動が、脳を育てる｜チビスポ マガジン（プレビュー v1）',art_body,art_css)
exec(open(P+'art_v2.py',encoding='utf-8').read())

# ================================================================ 5. クラブ・事業者向け
pt_css='''
.phero{position:relative;margin:0;padding:54px 20px 40px;overflow:hidden;background:#0d0d10;color:#fff}
.phero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;filter:grayscale(.3)}
.phero::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(0,0,0,.92),rgba(0,0,0,.45))}
.phero .in{position:relative;z-index:2;max-width:1180px;margin:0 auto}
.phero .k{font-family:'Anton',sans-serif;font-size:11.5px;letter-spacing:.2em;color:var(--accent);margin-bottom:10px}
.phero h1{font-family:var(--fh);margin:0 0 12px;font-size:clamp(26px,6.8vw,50px);font-weight:900;line-height:1.3;letter-spacing:var(--ls)}
.phero h1 em{font-style:normal;color:var(--accent)}
.phero p{margin:0 0 20px;font-size:13.5px;font-weight:700;color:rgba(255,255,255,.86);line-height:1.95;max-width:40em}
.phero .btns{display:flex;flex-wrap:wrap;gap:9px}
.phero .btn.ghost{color:#fff;border-color:rgba(255,255,255,.6)}
.two{display:grid;grid-template-columns:1fr;gap:12px;margin-top:22px}
.two .c{border:1px solid var(--line);background:var(--card);padding:18px 16px}
.two .c .k{font-size:10.5px;font-weight:900;letter-spacing:.14em;color:var(--accent);margin-bottom:6px}
.two .c h3{font-family:var(--fh);margin:0 0 8px;font-size:18px;font-weight:900}
.two .c p{margin:0 0 12px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
.steps{display:grid;grid-template-columns:1fr;gap:10px}
.steps .s{display:flex;gap:14px;align-items:flex-start;border-top:1px solid var(--line);padding:14px 0}
.steps .n{font-family:'Anton',sans-serif;font-size:26px;line-height:1;color:var(--accent);flex:none;width:44px}
.steps h3{font-family:var(--fh);margin:0 0 4px;font-size:15px;font-weight:900}
.steps p{margin:0;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.plans{display:grid;grid-template-columns:1fr;gap:12px}
.pl{border:1px solid var(--line);background:var(--card);padding:18px 16px;position:relative}
.pl.main{border:2px solid var(--accent)}
.pl .pin{position:absolute;right:12px;top:12px;background:var(--accent2);color:#fff;font-size:10px;font-weight:900;padding:3px 8px;border-radius:999px}
.pl .k{font-size:10.5px;font-weight:900;letter-spacing:.14em;color:var(--sub);margin-bottom:6px}
.pl h3{font-family:var(--fh);margin:0 0 6px;font-size:17px;font-weight:900}
.pl .who{font-size:11.5px;font-weight:900;color:var(--accent);margin-bottom:8px}
.pl ul{margin:0 0 12px;padding-left:1.2em;font-size:12.5px;font-weight:700;line-height:1.9}
.pl .pr{font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:10px}
.pl .pr small{font-size:11px;font-weight:700;color:var(--sub);margin-left:6px}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.nums div{background:var(--card);padding:16px 10px;text-align:center}
.nums b{display:block;font-family:'Anton',sans-serif;font-size:30px;color:var(--accent);line-height:1}
.nums span{font-size:11px;font-weight:900;color:var(--sub);display:block;margin-top:6px}
.faq{border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line);padding:13px 0}
.faq summary{font-size:13.5px;font-weight:900;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:10px}
.faq summary::after{content:"＋";color:var(--accent);flex:none}
.faq details[open] summary::after{content:"－"}
.faq p{margin:10px 0 0;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
.pcta{margin-top:40px;background:var(--ink);color:var(--bg);padding:30px 20px;text-align:center}
.pcta h2{font-family:var(--fh);margin:0 0 8px;font-size:clamp(19px,5vw,28px);font-weight:900;border:0;padding:0;color:var(--bg)}
.pcta p{margin:0 0 16px;font-size:12.5px;font-weight:700;opacity:.8}
@media(min-width:760px){.phero{padding:84px 20px 64px}.two{grid-template-columns:1fr 1fr;gap:18px}.steps{grid-template-columns:repeat(3,1fr);gap:18px}.steps .s{flex-direction:column;border-top:2px solid var(--ink)}.plans{grid-template-columns:repeat(3,1fr);gap:16px}.pcta{padding:48px 20px}}
'''
pt_body='''
<div class="phero"><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""><div class="in">
  <div class="k">FOR CLUBS &amp; PARTNERS</div>
  <h1>クラブの<em>「かっこよさ」</em>、<br>撮って載せませんか。</h1>
  <p>チビスポへの掲載は無料です。そのうえで、新入団の募集シーズンに向けた撮影・動画制作や、SNS・ホームページ・チラシまで、必要なところだけ手伝います。</p>
  <div class="btns"><a class="btn" href="#">無料で掲載する</a><a class="btn ghost" href="#">まず相談する</a></div>
</div></div>
<main><div class="wrap">
  <div class="note">【クラブ・事業者向け】partner.html（掲載・広告のご案内）と recruit-pr.html（地域企業PR）を1ページに統合。★<b>金額はサイトに書かない</b>（Phase 1ルール＝値付けを実測してから公開）。主力は「新入団募集シーズンパック」＝単発・年1回（スポ少の年度予算主義に合わせる。月額サブスクは不採用）。制作系（撮影・SNS・HP・チラシ）はトラフィックに依存しないので今すぐ売れる。地域広告はトラフィック証明後。数字は実データ（掲載299）。</div>

  <div class="two">
    <div class="c"><div class="k">CLUBS</div><h3>クラブを載せたい</h3><p>掲載は無料。写真・活動日・月謝・雰囲気タグを登録すると、地域・種目の検索と地図に載ります。体験申込はチビスポから直接届きます。</p><a class="btn" href="#">無料で掲載する</a></div>
    <div class="c"><div class="k">PARTNERS</div><h3>企業として広告したい</h3><p>整骨院・スポーツ用品店・塾・クリニックなど。地域の子育て世帯が見るクラブページに、お店を載せられます。</p><a class="btn ghost" href="service-ads-preview.html">広告のご案内を見る</a></div>
  </div>

  <div class="blk"><h2>掲載までの<em>3ステップ</em></h2><div class="sub">最短で当日に載ります。</div>
    <div class="steps">
      <div class="s"><div class="n">01</div><div><h3>クラブ登録</h3><p>メールアドレスとパスワードだけ。1分です。</p></div></div>
      <div class="s"><div class="n">02</div><div><h3>クラブ情報を入力</h3><p>写真・活動曜日・月謝・雰囲気タグ・おすすめポイント。スマホからでもできます。</p></div></div>
      <div class="s"><div class="n">03</div><div><h3>公開・体験申込が届く</h3><p>検索と地図に載り、保護者からの体験申込がメールで届きます。</p></div></div>
    </div>
  </div>

  <div class="blk"><h2>プラン</h2><div class="sub">掲載は無料。そのうえで、必要なところだけ。</div>
    <div class="plans">
      <div class="pl"><div class="k">FREE</div><h3>無料掲載</h3><div class="who">すべてのクラブ</div><ul><li>検索・地図・種目ページに掲載</li><li>写真・動画（お持ちのもの）の掲載</li><li>体験申込・お問い合わせの受信</li><li>クラブマイページで編集</li></ul><div class="pr">0円</div><a class="btn ghost blockb" href="#">登録する</a></div>
      <div class="pl main"><span class="pin">主力</span><div class="k">SEASON PACK</div><h3>新入団募集シーズンパック</h3><div class="who">民間スクール・クラブチーム／募集に本気の少年団</div><ul><li>30秒のクラブ紹介動画（縦・横）</li><li>切り出し写真・SNS用素材一式</li><li>募集チラシ・ポスターのデータ</li><li>チビスポの「編集部おすすめ」枠に掲載</li><li>クラブのSNS・説明会でそのまま使えます</li></ul><div class="pr">個別にご案内<small>年1回・単発</small></div><a class="btn blockb" href="#">相談する</a></div>
      <div class="pl"><div class="k">SUPPORT</div><h3>SNS運用・HP・チラシ</h3><div class="who">手が回らないクラブ</div><ul><li>InstagramやThreadsの運用代行・伴走</li><li>クラブ公式サイトの制作（スマホ前提）</li><li>募集チラシ・ポスターの制作</li></ul><div class="pr">個別にご案内<small>必要なものだけ</small></div><a class="btn ghost blockb" href="#">相談する</a></div>
    </div>
  </div>

  <div class="blk"><h2>いま、チビスポには</h2>
    <div class="nums"><div><b>299</b><span>掲載クラブ</span></div><div><b>12</b><span>都道府県</span></div><div><b>0円</b><span>掲載料</span></div></div>
  </div>

  <div class="blk"><h2>よくある質問</h2>
    <div class="faq">
      <details><summary>本当に無料ですか</summary><p>掲載・体験申込の受信・マイページでの編集は無料です。有料なのは撮影や制作など、成果物が手元に残るものだけです。</p></details>
      <details><summary>少年団（ボランティア運営）でも載せられますか</summary><p>載せられます。掲載クラブの多くが少年団・スポ少です。</p></details>
      <details><summary>写真や動画がありません</summary><p>写真なしでも掲載できます。ただし写真があるクラブのほうが体験申込は明らかに多いので、スマホの写真で構わないので1枚は入れてください。</p></details>
      <details><summary>シーズンパックの時期は</summary><p>新入団募集に合わせて、撮影は11〜12月、納品は1月を目安にしています。年度予算での申込みが多いので、早めのご相談をおすすめします。</p></details>
      <details><summary>広告はどんな業種が載っていますか</summary><p>整骨院・スポーツ用品店・学習塾・歯科・カフェなど、子育て世帯が使うお店が中心です。</p></details>
    </div>
  </div>

  <div class="pcta"><h2>まず、無料で載せてみてください。</h2><p>登録は1分。載せてから、必要なものを決めれば大丈夫です。</p><a class="btn" href="#">無料で掲載する</a></div>
  <div style="height:40px"></div>
</div></main>
'''
page('partner-preview-v1.html','クラブ・事業者の方へ｜チビスポ（プレビュー v1・統合型）',pt_body,pt_css)

# ================================================================ 6. 3問診断
sd_css='''
.sd{max-width:640px;margin:0 auto;padding:22px 0 40px}
.sd .prog{display:flex;gap:6px;margin-bottom:22px}
.sd .prog i{flex:1;height:4px;background:var(--line);border-radius:999px}
.sd .prog i.on{background:var(--accent)}
.q{display:none}
.q.on{display:block}
.q .n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.2em;color:var(--accent);margin-bottom:8px}
.q h1{font-family:var(--fh);margin:0 0 6px;font-size:clamp(22px,5.8vw,32px);font-weight:900;line-height:1.4;letter-spacing:var(--ls)}
.q .ld{font-size:12.5px;font-weight:700;color:var(--sub);margin-bottom:18px;line-height:1.8}
.opts{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.opt{border:1.5px solid var(--line);background:var(--card);padding:16px 10px;text-align:center;font-family:var(--fh);font-size:14px;font-weight:900;cursor:pointer;transition:.15s;min-width:0;overflow-wrap:anywhere}
.opt:hover{border-color:var(--accent)}
.opt.on{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 8%,var(--bg))}
.opt small{display:block;font-size:11px;font-weight:700;color:var(--sub);margin-top:4px;font-family:var(--f)}
.opts.one{grid-template-columns:1fr}
.sd .nav{display:flex;justify-content:space-between;gap:10px;margin-top:22px}
.sd .nav .back{font-size:12.5px;font-weight:900;color:var(--sub);padding:14px 0}
.res{display:none}
.res.on{display:block}
.res .hd{border-top:3px solid var(--ink);padding-top:16px;margin-bottom:6px}
.res .hd .k{font-family:'Anton',sans-serif;font-size:11.5px;letter-spacing:.2em;color:var(--accent);margin-bottom:8px}
.res .hd h1{font-family:var(--fh);margin:0 0 6px;font-size:clamp(22px,5.8vw,32px);font-weight:900;line-height:1.4}
.res .hd p{margin:0 0 16px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.85}
.res .cond{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.res .news{grid-template-columns:1fr}
.save{margin-top:26px;border:1.5px solid var(--accent);padding:18px 16px;text-align:center}
.save .t{font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:6px}
.save p{margin:0 0 12px;font-size:12px;font-weight:700;color:var(--sub);line-height:1.8}
.save .row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.alt{margin-top:22px;border-top:1px solid var(--line);padding-top:16px}
.alt .t{font-size:12px;font-weight:900;color:var(--sub);letter-spacing:.06em;margin-bottom:10px}
@media(min-width:760px){.sd{max-width:720px;padding:40px 0 60px}.res .news{grid-template-columns:repeat(2,1fr)}}
'''
res_cards="\n".join(cards.card(**c) for c in [cards.CLUBS[0],cards.CLUBS[2],cards.CLUBS[5],cards.CLUBS[8]])
sd_body='''
<main><div class="wrap">
  <div class="note">【3問診断】ヒーロー第2導線の着地。★<b>質問はすべて登録項目で絞れるもの</b>（種目／活動曜日／こだわり＝未就学から・女の子歓迎・入会金なし・体験OK）。当番や試合出場は項目に無いので聞かない。★順番：<b>先に結果（クラブ4件）を渡してから</b>、保存したい人にマイページ、はじめての人に読みもの。診断ロジックは検索の絞り込みをそのまま使うので新しいデータは不要。</div>
  <div class="sd">
    <div class="prog"><i class="on"></i><i></i><i></i></div>

    <div class="q on" data-q="1">
      <div class="n">Q1 / 3</div><h1>どんな種目が気になりますか。</h1><div class="ld">まだ決めていなくても大丈夫です。</div>
      <div class="opts">
        <div class="opt">サッカー</div><div class="opt">野球</div><div class="opt">バスケットボール</div><div class="opt">ダンス</div><div class="opt">水泳</div><div class="opt">空手・剣道</div><div class="opt">体操</div><div class="opt">まだ決めていない<small>おすすめの種目も出します</small></div>
      </div>
      <div class="nav"><span></span><a class="btn next" href="#">つぎへ</a></div>
    </div>

    <div class="q" data-q="2">
      <div class="n">Q2 / 3</div><h1>通えるのは、いつですか。</h1><div class="ld">活動曜日で絞ります。</div>
      <div class="opts">
        <div class="opt">土日どちらか<small>週1回が目安</small></div><div class="opt">土日両方<small>週2回</small></div><div class="opt">平日の放課後</div><div class="opt">こだわらない</div>
      </div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">つぎへ</a></div>
    </div>

    <div class="q" data-q="3">
      <div class="n">Q3 / 3</div><h1>あてはまるものがあれば。</h1><div class="ld">複数えらべます。なくても大丈夫です。</div>
      <div class="opts">
        <div class="opt">未就学から通いたい</div><div class="opt">女の子です</div><div class="opt">入会金がないところ</div><div class="opt">まず体験してみたい</div>
      </div>
      <div class="nav"><a class="back" href="#">もどる</a><a class="btn next" href="#">結果を見る</a></div>
    </div>

    <div class="res">
      <div class="hd"><div class="k">RESULT</div><h1>合いそうなクラブが、<em style="font-style:normal;color:var(--accent)">4件</em>ありました。</h1><p>世田谷区のまわりで、土日どちらかに通えて、体験OKのサッカークラブです。</p>
        <div class="cond"><span class="chip on">サッカー</span><span class="chip on">土日どちらか</span><span class="chip on">体験OK</span><a class="chip" href="#">条件を変える</a></div></div>
      <div class="news">%s</div>
      <div class="save"><div class="t">この結果を、保存しておきますか。</div><p>マイページに保存すると、あとから見比べられます。近くに新しいクラブが載ったときにもお知らせします。</p><div class="row"><a class="btn" href="#">保存する（無料）</a><a class="btn ghost" href="search-preview.html">一覧で見る</a></div></div>
      <div class="alt"><div class="t">はじめての方は、こちらも</div>
        <div class="arts">
          <div class="art"><div class="b"><h3>「うちの子に合うクラブ」の見つけ方・5つの視点</h3><div class="m"><b>クラブ選び</b>2026/06/12</div></div><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""></div>
          <div class="art"><div class="b"><h3>見学のとき、コーチに聞いておきたい5つのこと</h3><div class="m"><b>はじめて</b>2026/08/28</div></div><img src="assets/preview-video/wm-bball-jp.jpg" alt=""></div>
        </div></div>
    </div>
  </div>
</div></main>
'''%res_cards
sd_js='''<script>
(function(){var qs=[].slice.call(document.querySelectorAll('.q')),res=document.querySelector('.res'),prog=[].slice.call(document.querySelectorAll('.prog i')),i=0;
 function show(n){i=n;qs.forEach(function(q,k){q.classList.toggle('on',k===n)});prog.forEach(function(p,k){p.classList.toggle('on',k<=n)});res.classList.toggle('on',n>=qs.length);window.scrollTo({top:0,behavior:'smooth'})}
 document.querySelectorAll('.opt').forEach(function(o){o.addEventListener('click',function(){var multi=o.closest('.q').dataset.q==='3';if(!multi)o.parentElement.querySelectorAll('.opt').forEach(function(x){x.classList.remove('on')});o.classList.toggle('on')})});
 document.querySelectorAll('.next').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();show(i+1)})});
 document.querySelectorAll('.back').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();show(Math.max(0,i-1))})});
})();
</script>'''
page('shindan-preview-v1.html','3つの質問でさがす｜チビスポ（プレビュー v1）',sd_body,sd_css,extra_js=sd_js)
exec(open(P+'sd_v2.py',encoding='utf-8').read())
exec(open(P+'sd_v3.py',encoding='utf-8').read())
exec(open(P+'mp_v2.py',encoding='utf-8').read())
exec(open(P+'svc_listing.py',encoding='utf-8').read())
exec(open(P+'svc_ads.py',encoding='utf-8').read())
exec(open(P+'svc_sns.py',encoding='utf-8').read())
exec(open(P+'svc_hub.py',encoding='utf-8').read())
exec(open(P+'cmp_v2.py',encoding='utf-8').read())
exec(open(P+'reg_v2.py',encoding='utf-8').read())
exec(open(P+'lg_v2.py',encoding='utf-8').read())
exec(open(P+'adm_v2.py',encoding='utf-8').read())
exec(open(P+'ct_v2.py',encoding='utf-8').read())
print('done')
