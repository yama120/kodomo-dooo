# 旧世代ページ（site.css を <link> せず shared.js が chrome.css を後から注入していたページ）を prodpage に載せ替えるための共通部品。
# 2026-10-17：「地図から探す」で読み込み直後にメニューが素のまま出て滑り落ちる現象の根本対応。
#  - 元の本文は _build/src/legacy/<name>.html に退避してある（これが唯一の原稿。生成物の *.html を編集しない）
#  - prodpage が site.css・ヘッダー・フッター・シートを同期で書くので、本文からは
#    「shared.js が注入するヘッダー／フッターの上書き」CSS と、html/body/* の全体リセットを外す
#  - 短いクラス名（.card .btn …）は site.css と衝突するので、ページ側に接頭辞を付ける（rename）
import os,re,sys,html as H
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D; L=P+'legacy/'
# 旧ページの本文は 400/500 を使う（site.css は見出し用の 700/900 だけ読む）
FONT_EXTRA='<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500&display=swap" rel="stylesheet">\n'
# 旧デザインの英字あしらい（Pacifico）→ 新デザインの eyebrow（Anton・字間広め）
PACIFICO=re.compile(r"font-family:'Pacifico',cursive;font-size:\d+px;")
EYEBROW="font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.22em;text-transform:uppercase;"
# 役目を終えたページへのリンクは行き先に直結させる（redirect を経由しない）
HREF={'recruit-pr.html':'service-ads.html','join.html':'listing.html','team-lp.html':'listing.html'}

def load(name): return open(L+name,encoding='utf-8').read()
def title(s): return H.unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1).strip())
def desc(s,default=''):
    m=re.search(r'<meta name="description" content="([^"]*)"',s); return H.unescape(m.group(1)) if m else default
def noindex(s): return bool(re.search(r'<meta name="robots" content="noindex',s))
def head_styles(s):
    """<head> 内の <style> 中身を順に返す。prod_reskin.py が足した「reskin v2」の body 上書きは外す"""
    h=s[:s.index('<body')]; out=[]
    for m in re.finditer(r'<style[^>]*>(.*?)</style>',h,re.S):
        if 'reskin v2' in h[max(0,m.start()-40):m.start()]: continue
        out.append(m.group(1))
    return out
def body(s):
    """<body> の中身。shared.js / supabase-lite.js の読み込みタグは prodpage が付けるので外す"""
    a=s.index('<body'); a=s.index('>',a)+1; b=s.rindex('</body>')
    t=s[a:b]
    t=re.sub(r'[ \t]*<script src="(shared|supabase-lite)\.js[^"]*"></script>\n?','',t)
    for k,v in HREF.items(): t=t.replace('href="'+k,'href="'+v)
    return t.strip('\n')
def split_tail_scripts(t):
    """本文末尾に連なるインライン <script> を切り出す（supabase-lite / shared.js の後ろで走らせたいもの）"""
    blocks=[(m.start(),m.end(),m.group(0)) for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>.*?</script>',t,re.S)]
    tail=[]; end=len(t.rstrip())
    for a,b,g in reversed(blocks):
        if t[b:end].strip()=='' : tail.insert(0,g); end=a
        else: break
    return t[:end].rstrip('\n'), '\n'.join(tail)

def _blocks(css):
    out=[];i=0;n=len(css)
    while i<n:
        j=css.find('{',i)
        if j<0: break
        pre=css[i:j].strip(); depth=1; k=j+1
        while k<n and depth:
            c=css[k]
            if c=='{': depth+=1
            elif c=='}': depth-=1
            k+=1
        out.append((pre,css[j+1:k-1])); i=k
    return out
def scope_css(css,scope,mode='globals',rename=None,drop=()):
    """ページ CSS を本文ラッパー（scope）の中だけに効かせる。
    mode='globals' … html/body/* の全体リセットと、要素名で始まるセレクタだけを scope の下に移す（クラス指定はそのまま）
    mode='all'     … 全セレクタに scope を付ける（label{} と .radio-item{} のように要素ルールとクラスルールが競うページ用。
                      一律に +1 クラス分なので、ページ内の優先順位は元のまま）
    :root{} は scope{} に（トークンをページ内に閉じる）。body{}・html{} は site.css が持つので落とす。
    body[...] / body.x で始まるものはそのまま（JS が body に属性を付けて切り替えるページ用）"""
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S); res=[]
    for pre,inner in _blocks(css):
        if pre.startswith('@media') or pre.startswith('@supports'):
            res.append(pre+'{\n'+scope_css(inner,scope,mode,rename,drop)+'\n}'); continue
        if pre.startswith('@'): res.append(pre+'{'+inner+'}'); continue
        sels=[]
        for s in pre.split(','):
            s=' '.join(s.split())
            if not s or s in drop: continue
            if rename:
                for a,b in rename.items(): s=re.sub(r'\.'+re.escape(a)+r'(?![\w-])','.'+b,s)
            first=re.split(r'[\s>+~]',s,1)[0]
            if first in ('html','body'): continue
            if first.startswith('body'): sels.append(s); continue
            if first.startswith(':root'): sels.append(re.sub(r'^:root',scope,s)); continue
            if first.startswith('*') or mode=='all' or re.match(r'^[a-z]',first): sels.append(scope+' '+s)
            else: sels.append(s)
        if sels: res.append(','.join(sels)+'{'+inner.strip()+'}')
    return '\n'.join(res)
def rename_html(t,rename):
    """class="…" の値・classList.x('…')・querySelector('.…') の中だけクラス名を置き換える（JS の変数名には触れない）"""
    def val(v): return ' '.join(rename.get(x,x) for x in v.split(' '))
    t=re.sub(r'(class=)(["\'])(.*?)\2',lambda m:m.group(1)+m.group(2)+val(m.group(3))+m.group(2),t)
    t=re.sub(r'(className\s*=\s*)(["\'])([^"\']*)\2',lambda m:m.group(1)+m.group(2)+val(m.group(3))+m.group(2),t)
    for a,b in rename.items():
        t=re.sub(r"(classList\.(?:add|remove|toggle|contains)\(\s*['\"])"+re.escape(a)+r"(['\"])",r'\g<1>'+b+r'\2',t)
        for _ in range(5): t=re.sub(r"(querySelector(?:All)?\(\s*['\"][^'\"]*?)\."+re.escape(a)+r"(?![\w-])",r'\g<1>.'+b,t)
        left=[l.strip()[:100] for l in t.split('\n') if re.search(r"['\"\.](?<![\w-])"+re.escape(a)+r"(?![\w-])",l) and 'class=' not in l]
        if left: print('  !! 要確認（置換していない '+a+'）:',left[:3])
    return t
def check(name,html_,must_have=(),must_not=()):
    """生成物の確認。must_not は本文側だけを見る（共通フッターの class="btn" などを拾わないよう、ヘッダー／フッターは外す）"""
    inner=html_.replace(C.HEADER_HTML,'').replace(C.FOOTER_HTML,'').replace(C.SHEET_HTML,'')
    for x in must_have:
        if x not in html_: print('  !! 無い:',name,x)
    for x in must_not:
        if x in inner: print('  !! 残り:',name,x)
