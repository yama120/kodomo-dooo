import re,os
D=os.path.expanduser('~/kodomo-dooo-deploy/')
s=open(D+'map.html',encoding='utf-8').read()
top=open(D+'video-hero-preview.html',encoding='utf-8').read()
BASE=top[top.index('<style>')+7:top.index('</style>')]
tokens=BASE[:BASE.index('*{box-sizing')]
switch=BASE[BASE.index('/* ===================== SKIN SWITCH'):BASE.index('/* ===================== HEADER')]
tail=top[top.index('<div id="skins">'):top.index('</body>')]

head_end=s.index('<body')
head,body=s[:head_end],s[head_end:]

# ---------- 1) インライン色 → トークン（HTML部分のみ。JSは限定置換） ----------
INK=['#1f2430','#2b3340','#3a4452','#2b2b2b']
SUB=['#54606e','#5b6675','#7b8492','#8a95a0','#8a93a1','#9aa1ad','#9aa4af','#9aa3ae','#777777','#999999']
LINE=['#dfe3e8','#e9ecef','#eef0f2','#e5e8ec','#e2e5ea','#e6e9ed','#cfd4da','#eeeeee']
ALT=['#f0f2f4','#f3f4f6','#f6f7f9','#f1f6fd','#f0faf4','#f5f1fd','#fff4f6','#fef0ea','#f4f4f2']
def split_js(t):
    parts=re.split(r'(<script[^>]*>.*?</script>)',t,flags=re.S)
    return parts
def map_html(t):
    # アクセント背景ボタン内の白文字 → onaccent
    t=re.sub(r'(style="[^"]*background:#1668d9[^"]*?)color:#fff',r'\1color:var(--onaccent)',t)
    t=re.sub(r'(style="[^"]*background:#2a6fdb[^"]*?)color:#fff',r'\1color:var(--onaccent)',t)
    t=t.replace('background:#fff','background:var(--card)').replace('background: #fff','background:var(--card)')
    t=t.replace('background:#eceef1','background:var(--bg)')
    for c in INK:  t=re.sub(r'(color|stroke|fill|background):\s*'+c+r'\b',r'\1:var(--ink)',t)
    for c in SUB:  t=re.sub(r'(color|background):\s*'+c+r'\b',r'\1:var(--sub)',t)
    for c in LINE: t=re.sub(r'(#?)'+c+r'\b',r'var(--line)',t)
    for c in ALT:  t=re.sub(c+r'\b','var(--alt)',t)
    t=re.sub(r'#1668d9\b|#2a6fdb\b','var(--accent)',t)
    t=re.sub(r'#e6197e\b|#e8455f\b','var(--accent2)',t)
    # 角丸
    t=re.sub(r'border-radius:\s*(8|9|10)px',r'border-radius:var(--r-s)',t)
    t=re.sub(r'border-radius:\s*(14|16|20)px',r'border-radius:var(--r)',t)
    t=re.sub(r'border-radius:\s*24px',r'border-radius:999px',t)
    t=re.sub(r'border-radius:\s*(5|6)px',r'border-radius:var(--r-xs)',t)
    # 書体
    t=re.sub(r"font-family:\s*\\?'M PLUS Rounded 1c\\?',\s*sans-serif","font-family:var(--fh)",t)
    t=re.sub(r"font-family:\s*'Noto Sans JP',\s*sans-serif","font-family:var(--f)",t)
    return t
def map_js(t):
    # JS内は「CSSプロパティの文脈」だけ置換（SVG属性の色は触らない）
    t=re.sub(r'(background|color):#1668d9\b',r'\1:var(--accent)',t)
    t=re.sub(r'(background|color):#e6197e\b',r'\1:var(--accent2)',t)
    t=re.sub(r'(background|border-color|color):#(dfe3e8|e9ecef|eef0f2)\b',r'\1:var(--line)',t)
    t=re.sub(r'(color):#(54606e|5b6675|7b8492|8a95a0|9aa1ad)\b',r'\1:var(--sub)',t)
    t=re.sub(r'(color):#(1f2430|2b3340|3a4452)\b',r'\1:var(--ink)',t)
    t=re.sub(r'background:#fff\b','background:var(--card)',t)
    # ---- pass2/3：文字列内に残る旧色・実行時に代入する色（SVG属性と種目パレットは触らない） ----
    t=re.sub(r'solid #1668d9\b','solid var(--accent)',t)
    t=re.sub(r'(box-shadow:0 0 0 [\d.]+px )#1668d9\b',r'\1var(--accent)',t)
    t=t.replace('#e9f1fd','color-mix(in srgb,var(--accent) 10%,var(--card))')
    t=re.sub(r'#(cdd3da|c5dcf7|f7c6dd)\b','var(--line)',t)
    t=t.replace("font-family:\\'M PLUS Rounded 1c\\',sans-serif","font-family:var(--fh)")
    t=re.sub(r'border-radius:(12|10|9)px','border-radius:var(--r-s)',t)
    t=t.replace("b.style.borderColor=on?'#1668d9':'#dfe3e8'","b.style.borderColor=on?'var(--accent)':'var(--line)'")
    t=t.replace("b.style.color=on?'#1668d9':'#54606e'","b.style.color=on?'var(--accent)':'var(--sub)'")
    t=t.replace("'border:1px solid #dfe3e8;background:","'border:1px solid var(--line);background:")
    t=t.replace("border:1px solid #dfe3e8'));","border:1px solid var(--line)'));")
    t=t.replace("background:'+(on?'#e6197e':'#d6dae0')","background:'+(on?'var(--accent2)':'var(--line)')")
    t=t.replace("'#fff'; b.style.color","'var(--card)'; b.style.color")
    return t
parts=split_js(body)
body="".join(map_js(p) if p.startswith('<script') else map_html(p) for p in parts)

# ---------- 2) <style> ブロック（クラス規則）をトークン化 ----------
def fix_style(m):
    c=m.group(1)
    c=c.replace("body{font-family:'Noto Sans JP',sans-serif;color:#1f2430;-webkit-font-smoothing:antialiased;background:#eceef1}",
                "body{font-family:var(--f);color:var(--ink);-webkit-font-smoothing:antialiased;background:var(--bg)}")
    c=c.replace(".leaflet-container{font-family:'Noto Sans JP',sans-serif;background:#eef1ea}",".leaflet-container{font-family:var(--f);background:var(--alt)}")
    c=c.replace("::-webkit-scrollbar-thumb{background:#cfd4da;border-radius:8px}","::-webkit-scrollbar-thumb{background:var(--line);border-radius:8px}")
    c=c.replace("background:#fff;border-radius:18px 18px 0 0","background:var(--card);border-radius:18px 18px 0 0")
    c=c.replace("background:#cfd4da}","background:var(--line)}")
    c=c.replace(".cc-sheet-label{font-size:13.5px;font-weight:700;color:#3a4452}",".cc-sheet-label{font-size:13.5px;font-weight:900;color:var(--ink);font-family:var(--fh)}")
    c=c.replace("border-right:1px solid #e9ecef !important","border-right:1px solid var(--line) !important")
    return '<style>'+c+'</style>'
head=re.sub(r'<style[^>]*>(.*?)</style>',fix_style,head,count=1,flags=re.S)

RESKIN2 = r'''
<style id="reskin2">
/* ================= 地図ページ：カード・文字・ボタンを新デザインに（インラインより優先） ================= */
/* --- サイドバー --- */
.cc-side{background:var(--bg)!important;border-right:1px solid var(--line)!important;padding:24px 22px 32px!important}
.cc-side span[style*="font-size:18px"]{font-family:var(--fh)!important;font-size:17px!important;font-weight:900!important;letter-spacing:var(--ls)}
.cc-side div[style*="font-size:13px;font-weight:700"]{font-size:11px!important;font-weight:900!important;letter-spacing:.1em!important;color:var(--sub)!important;margin-bottom:9px!important}
.cc-side input,.cc-side select{background:var(--card)!important;border:1px solid var(--line)!important;border-radius:var(--r-s)!important;color:var(--ink)!important;font-family:var(--f)!important;font-size:13.5px!important;padding:12px 13px!important}
.cc-side select{padding-right:34px!important}
.cc-side input::placeholder{color:var(--sub)}
.cc-side div[style*="font-size:11px;color"]{color:var(--sub)!important}
.cc-age{border:1px solid var(--line)!important;background:var(--card)!important;border-radius:999px!important;font-weight:900!important;font-size:12.5px!important;color:var(--ink)!important;padding:9px 0!important}
body[data-skin="magazine"] .cc-age,body[data-skin="editorial"] .cc-age{border-radius:0!important}
.cc-age[style*="border-color: var(--accent)"],.cc-age[style*="border-color:var(--accent)"]{background:var(--ink)!important;color:var(--bg)!important;border-color:var(--ink)!important}
.cc-check span[style*="font-size:14px"],.cc-fee span[style*="font-size:14px"]{font-size:13.5px!important;font-weight:700!important;color:var(--ink)!important}
.cc-cond-box{border-radius:var(--r-xs)!important;border-color:var(--line)!important}
#cc-apply{background:var(--accent)!important;color:var(--onaccent)!important;font-family:var(--fh)!important;font-weight:900!important;font-size:15px!important;border-radius:var(--r-s)!important;padding:15px!important;letter-spacing:.03em}
#cc-clear{background:transparent!important;color:var(--ink)!important;border:1.5px solid var(--ink)!important;border-radius:var(--r-s)!important;font-weight:900!important}
#cc-clear svg{stroke:var(--ink)}
#cc-side-close{background:var(--alt)!important}
/* --- 地図の上のコントロール --- */
#cc-map{border:1px solid var(--line)!important;border-radius:var(--r)!important}
#cc-back,#cc-filter-open,.cc-recenter,#cc-research,#cc-cards-next{background:var(--card)!important;border:1px solid var(--line)!important;color:var(--ink)!important;box-shadow:0 4px 14px rgba(0,0,0,.14)!important;font-family:var(--fh)!important;font-weight:900!important}
#cc-filter-open,.cc-recenter,#cc-research{border-radius:999px!important;font-size:12.5px!important}
#cc-filter-open svg,.cc-recenter svg,#cc-research svg{stroke:var(--accent)!important}
.cc-maphint,div[style*="地図を動かして"]{font-weight:900!important}
/* --- カード（JS生成） --- */
.cc-cards-wrap{gap:14px!important;padding:6px 4px 10px!important}
.cc-card{width:196px!important;background:var(--card)!important;border:1px solid var(--line)!important;border-radius:var(--r)!important;box-shadow:none!important;transition:border-color .15s,transform .15s!important}
.cc-card:hover{transform:translateY(-2px)}
.cc-card[style*="0 0 0 2.5px"]{border-color:var(--accent)!important;box-shadow:0 0 0 2px var(--accent)!important}
.cc-card > div:first-child img,.cc-card > div:first-child > div{height:118px!important}
.cc-card > div:first-child span[style*="PR"]{background:rgba(0,0,0,.72)!important;color:#fff!important;font-family:'Anton',sans-serif!important;font-weight:400!important;letter-spacing:.12em!important;font-size:9.5px!important;border-radius:3px!important}
.cc-card > div:last-child{padding:10px 12px 12px!important}
.cc-card > div:last-child > div:nth-child(1){font-size:10.5px!important;font-weight:900!important;letter-spacing:.04em!important;color:var(--sub)!important;margin-bottom:4px!important}
.cc-card > div:last-child > div:nth-child(2){font-family:var(--fh)!important;font-size:14px!important;font-weight:900!important;color:var(--ink)!important;line-height:1.4!important;white-space:normal!important;display:-webkit-box!important;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden!important;margin-bottom:6px!important;letter-spacing:var(--ls)}
.cc-card > div:last-child > div:nth-child(3){font-size:11px!important;font-weight:700!important;color:var(--sub)!important;margin-bottom:8px!important}
.cc-card > div:last-child > div:nth-child(n+4){font-size:11px!important;font-weight:700!important;color:var(--sub)!important}
.cc-card > div:last-child > div:nth-child(n+4) svg{stroke:var(--sub)}
/* --- 下部シート --- */
#cc-sheet{background:var(--card)!important}
.cc-sheet-label{font-family:var(--fh)!important;font-weight:900!important;font-size:13.5px!important;color:var(--ink)!important}
/* --- 詳細パネル --- */
#cc-panel{background:var(--card)!important;border:1px solid var(--line)!important;border-radius:var(--r)!important;box-shadow:0 18px 40px rgba(0,0,0,.22)!important}
#cc-close{background:var(--card)!important;border:1px solid var(--line)!important;box-shadow:none!important}
#cc-detail-name{font-family:var(--fh)!important;font-size:16px!important;font-weight:900!important;line-height:1.4!important;letter-spacing:var(--ls);color:var(--ink)!important}
#cc-detail-sport,#cc-detail-area,#cc-detail-age,#cc-panel div[style*="font-size:11px;color"]{color:var(--sub)!important;font-weight:700!important}
#cc-detail-desc{color:var(--ink)!important;line-height:1.85!important}
#cc-detail-tags span{border:1px solid var(--line)!important;background:var(--card)!important;color:var(--ink)!important;border-radius:999px!important;font-size:10.5px!important;font-weight:900!important;padding:4px 9px!important}
body[data-skin="magazine"] #cc-detail-tags span,body[data-skin="editorial"] #cc-detail-tags span{border-radius:0!important}
#cc-detail-link{background:var(--accent)!important;color:var(--onaccent)!important;font-family:var(--fh)!important;font-weight:900!important;border-radius:var(--r-s)!important;padding:13px!important;font-size:13.5px!important;text-align:center!important}
#cc-detail-pr{background:rgba(0,0,0,.72)!important;font-family:'Anton',sans-serif!important;font-weight:400!important;letter-spacing:.12em!important;border-radius:3px!important}
/* --- 下部セクション（マガジン／他のクラブ／地域企業） --- */
.mx-extra div[style*="border:1px solid"]{border:0!important;border-radius:0!important;background:transparent!important;padding:0!important}
.mx-extra h3{font-family:var(--fh)!important;font-size:clamp(17px,4.2vw,22px)!important;font-weight:900!important;letter-spacing:var(--ls);border-top:2px solid var(--ink)!important;padding-top:13px!important;margin:34px 0 14px!important;color:var(--ink)!important}
.mx-extra a{color:var(--ink)}
.mx-extra div[style*="border-radius"]{border-radius:var(--r)!important}
.mx-extra img{border-radius:var(--r)!important}
.mx-extra div[style*="font-size:12.5px;font-weight:700"]{font-family:var(--fh)!important;font-size:13.5px!important;font-weight:900!important;line-height:1.5!important}
.mx-extra div[style*="font-size:12px;font-weight:700"]{color:var(--sub)!important;font-weight:700!important}
.mx-extra span[style*="border-radius:999px"]{background:var(--accent)!important;color:var(--onaccent)!important;font-family:var(--fh)!important;font-weight:900!important}
body[data-skin="magazine"] .mx-extra span[style*="border-radius:999px"],body[data-skin="editorial"] .mx-extra span[style*="border-radius:999px"]{border-radius:0!important}

/* --- カルーセルの矢印（下部セクション・地図下） --- */
.cd-mag-prev,.cd-mag-next,.cd-club-prev,.cd-club-next,#cc-cards-next{background:var(--card)!important;border:1px solid var(--line)!important;box-shadow:0 6px 18px rgba(0,0,0,.18)!important;width:40px!important;height:40px!important;transition:border-color .15s,transform .15s}
.cd-mag-prev:hover,.cd-mag-next:hover,.cd-club-prev:hover,.cd-club-next:hover,#cc-cards-next:hover{border-color:var(--accent)!important;transform:translateY(-50%) scale(1.06)}
.cd-mag-prev:hover,.cd-mag-next:hover,.cd-club-prev:hover,.cd-club-next:hover{transform:scale(1.06)}
.cd-mag-prev svg,.cd-mag-next svg,.cd-club-prev svg,.cd-club-next svg,#cc-cards-next svg{stroke:var(--ink)!important;width:20px;height:20px}
/* --- 広告バンド：スキンに追従する落ち着いた帯 --- */
.mx-extra a[href="recruit-pr.html"]{background:var(--alt)!important;border:1px solid var(--line)!important;border-radius:var(--r)!important;padding:14px 18px!important}
.mx-extra a[href="recruit-pr.html"] > div{color:var(--ink)!important;font-size:12.5px!important;font-weight:900!important}
.mx-extra a[href="recruit-pr.html"] > div > span{color:var(--sub)!important;font-weight:700!important}
.mx-extra a[href="recruit-pr.html"] > span{background:var(--accent)!important;color:var(--onaccent)!important;font-family:var(--fh)!important;font-weight:900!important}
body[data-skin="magazine"] .mx-extra a[href="recruit-pr.html"] > span,body[data-skin="editorial"] .mx-extra a[href="recruit-pr.html"] > span{border-radius:0!important}
/* --- 暗いスキンではロゴ画像に白い下地（ロゴ自体は変えない） --- */
body[data-skin="stadium"] .cc-logo-img,body[data-skin="stadium"] footer[data-screen-label="フッター"] img[alt="チビスポ"]{background:#fff;padding:4px 8px;border-radius:8px;box-sizing:content-box}
/* --- 種目アイコン：色は残し、丸バッジ（種目色の下地＋白い線画）に統一 --- */
.cc-card > div:last-child > div:nth-child(1) > svg,#cc-detail-sport svg,#cc-panel div[style*="font-size:11px"] > svg,.mx-extra div[style*="font-weight:700"] > svg:first-child{display:inline-block!important;width:12px!important;height:12px!important;padding:3px!important;box-sizing:content-box!important;border-radius:50%!important;vertical-align:-5px!important;margin-right:2px;stroke:#fff!important;stroke-width:2.2!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#2a6fdb"],#cc-detail-sport svg[stroke="#2a6fdb"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#2a6fdb"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#2a6fdb"]{background:#2a6fdb!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#3FB6D6"],#cc-detail-sport svg[stroke="#3FB6D6"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#3FB6D6"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#3FB6D6"]{background:#3FB6D6!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#58b7d8"],#cc-detail-sport svg[stroke="#58b7d8"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#58b7d8"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#58b7d8"]{background:#58b7d8!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#5BD6A0"],#cc-detail-sport svg[stroke="#5BD6A0"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#5BD6A0"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#5BD6A0"]{background:#5BD6A0!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#6BAAEF"],#cc-detail-sport svg[stroke="#6BAAEF"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#6BAAEF"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#6BAAEF"]{background:#6BAAEF!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#7B8CE8"],#cc-detail-sport svg[stroke="#7B8CE8"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#7B8CE8"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#7B8CE8"]{background:#7B8CE8!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#9aa3ad"],#cc-detail-sport svg[stroke="#9aa3ad"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#9aa3ad"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#9aa3ad"]{background:#9aa3ad!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#b04ae8"],#cc-detail-sport svg[stroke="#b04ae8"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#b04ae8"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#b04ae8"]{background:#b04ae8!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#C98BFF"],#cc-detail-sport svg[stroke="#C98BFF"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#C98BFF"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#C98BFF"]{background:#C98BFF!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#E8884A"],#cc-detail-sport svg[stroke="#E8884A"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#E8884A"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#E8884A"]{background:#E8884A!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#e8884a"],#cc-detail-sport svg[stroke="#e8884a"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#e8884a"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#e8884a"]{background:#e8884a!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#F5A24B"],#cc-detail-sport svg[stroke="#F5A24B"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#F5A24B"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#F5A24B"]{background:#F5A24B!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#FF7FB6"],#cc-detail-sport svg[stroke="#FF7FB6"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#FF7FB6"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#FF7FB6"]{background:#FF7FB6!important}
.cc-card > div:last-child > div:nth-child(1) > svg[stroke="#FFC83F"],#cc-detail-sport svg[stroke="#FFC83F"],#cc-panel div[style*="font-size:11px"] > svg[stroke="#FFC83F"],.mx-extra div[style*="font-weight:700"] > svg:first-child[stroke="#FFC83F"]{background:#FFC83F!important}
/* 写真なしのプレースホルダ：元の薄い種目色の下地を活かし、アイコンは種目色のまま控えめに */
.cc-card div[style*="linear-gradient(135deg"] svg,.mx-extra div[style*="linear-gradient(135deg"] svg,#cc-detail-photoph svg{opacity:.5!important;width:44px!important;height:44px!important}
/* --- スクロールバー・細部 --- */
::-webkit-scrollbar-thumb{background:var(--line)!important}
</style>
'''
# ---------- 3) トークン・スキン・上書きCSSを注入 ----------
extra='''
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&family=Zen+Old+Mincho:wght@600;900&family=Anton&display=swap" rel="stylesheet">
<style id="reskin">
'''+tokens+'''
:root{--onaccent:#fff;--r-s:9px;--r-xs:6px}
body{--alt:color-mix(in srgb,var(--ink) 4%,var(--bg))} /* body で宣言：スキンの --ink/--bg を使って解決させる */
body[data-skin="stadium"]{--onaccent:#0b0c0f;--r-s:5px;--r-xs:4px}
body[data-skin="magazine"],body[data-skin="editorial"]{--r-s:0px;--r-xs:0px}
'''+switch+'''
/* ---- shared.js が注入するヘッダー／フッターの上書き ---- */
header[data-screen-label="ヘッダー"]{background:color-mix(in srgb,var(--bg) 92%,transparent)!important;border-bottom:1px solid var(--line)!important}
header[data-screen-label="ヘッダー"] .cc-nav a{color:var(--ink)!important;font-family:var(--fh)!important;font-weight:900!important;letter-spacing:var(--ls)}
header[data-screen-label="ヘッダー"] .cc-nav svg{stroke:var(--ink)}
header[data-screen-label="ヘッダー"] .cc-nav svg [fill]:not([fill="none"]){fill:var(--accent)}
header[data-screen-label="ヘッダー"] .cc-divider{background:var(--line)!important}
header[data-screen-label="ヘッダー"] .cc-actions a,header[data-screen-label="ヘッダー"] .cc-actions button{color:var(--ink)!important}
header[data-screen-label="ヘッダー"] .cc-actions svg{stroke:var(--ink)}
header[data-screen-label="ヘッダー"] .cc-publish{background:var(--accent)!important;color:var(--onaccent)!important;border-radius:999px!important;font-family:var(--fh)!important;font-weight:900!important}
body[data-skin="magazine"] header[data-screen-label="ヘッダー"] .cc-publish,body[data-skin="editorial"] header[data-screen-label="ヘッダー"] .cc-publish{border-radius:0!important}
header[data-screen-label="ヘッダー"] span[style*="地域スポーツ"],header[data-screen-label="ヘッダー"] a>span{color:var(--sub)!important}
.cc-menu{background:var(--card)!important;color:var(--ink)!important}
.cc-menu a{color:var(--ink)!important}
.cc-bottombar{background:color-mix(in srgb,var(--bg) 94%,transparent)!important;border-top:1px solid var(--line)!important}
.cc-bottombar a,.cc-bottombar span{color:var(--ink)!important}
footer[data-screen-label="フッター"]{background:var(--alt)!important;border-top:1px solid var(--line)}
footer[data-screen-label="フッター"] div{color:var(--ink)}
footer[data-screen-label="フッター"] a{color:var(--sub)!important}
footer[data-screen-label="フッター"] div[style*="font-weight: 900"]{color:var(--ink)!important;font-family:var(--fh)}
footer[data-screen-label="フッター"] div[style*="text-align: center"]{color:var(--sub)!important}
/* ---- Leaflet のコントロール ---- */
.leaflet-bar a{background:var(--card)!important;color:var(--ink)!important;border-bottom-color:var(--line)!important}
.leaflet-control-attribution{background:color-mix(in srgb,var(--card) 80%,transparent)!important;color:var(--sub)!important}
.leaflet-control-attribution a{color:var(--sub)!important}
/* ---- 見出し類を新書体に ---- */
#cc-detail-name,.cc-sheet-label,span[style*="font-size:18px;font-weight:700"]{font-family:var(--fh)!important;font-weight:900!important;letter-spacing:var(--ls)}
#cc-map{box-shadow:none!important}
input,select,button{font-family:var(--f)}
.note{position:relative;z-index:2}
</style>
'''
RESKIN3=open(P+'reskin3.css',encoding='utf-8').read() if 'P' in globals() else open('/private/tmp/claude-501/-Users-hyogoyamada-claudecode-project/5ae8baa4-4330-4bf8-b599-64aa8ac5ef83/scratchpad/reskin3.css',encoding='utf-8').read()
head=head.replace('</title>','</title>'+extra+RESKIN2+RESKIN3,1)

# ---------- 4) body 属性・設計メモ・スキン切替 ----------
body=body.replace('<body>','<body data-skin="bright">',1)
note='''<div class="wrap" style="max-width:1460px;margin:0 auto;padding:0 20px"><div class="note">【v2で揃えたこと・2026-09-08】検索結果（マガジン調）と道具立てを統一：条件検索を<b>罫線＋番号の紙面型</b>（FILTER／01〜06・下線だけの入力欄・黒いボタン）／地図の枠とボタンを<b>角型・黒罫</b>（MAGAZINE・EDITORIALのみ。BRIGHT・STADIUMは丸のまま）／詳細パネルとホバーを角型／カード幅を検索結果に合わせ、上に「CLUBS IN THIS AREA」の小見出し／下部セクションの見出しを収益枠と同じ控えめ型／ヘッダーのナビアイコンを単色に。<b>構造・JSは無改変</b>（差分は文字列内の色・書体・角丸だけ）。【地図（現行ページのリスキン）】★<b>機能・構造・JSは map.html のまま</b>。変えたのは見た目だけ＝インラインの色（#1668d9→アクセント、#3a4452→ink、#dfe3e8→line…）・角丸・書体をトークンに機械置換し、shared.js が注入するヘッダー／フッターはCSSで上書き。Leaflet／CARTO／ピン／下部シート／条件ドロワーはそのまま動く。★SVG属性の色（stroke="#…"）は var() が効かないので触っていない＝一部のアイコンが旧配色のまま。スキンを切り替えると地図以外が追従する。</div></div>
'''
body=body.replace('<!-- ヘッダーは shared.js で共通注入 -->','<!-- ヘッダーは shared.js で共通注入 -->\n'+note,1)
body=body.replace('</body>',tail+'\n</body>',1)

open(D+'map-preview.html','w',encoding='utf-8').write(head+body)
out=head+body
import collections
left=collections.Counter(re.findall(r'#[0-9a-fA-F]{6}\b',re.sub(r'<script[^>]*>.*?</script>','',out,flags=re.S)))
print('size:',len(out)//1024,'KB | JS無改変確認:', re.findall(r'<script[^>]*>.*?</script>',s,re.S)[-1][-400:]==re.findall(r'<script[^>]*>.*?</script>',out,re.S)[-1][-400:])
print('HTML側に残った直書き色:',left.most_common(10))
