# ---- 企業紹介ページ（PR記事）の生成。1社＝ _build/pr/<slug>.json → pr/<slug>.html
#   python3 prod_pr.py            … _build/pr/*.json を全部
#   python3 prod_pr.py <slug>     … 1社だけ
#   python3 prod_pr.py --images <slug> <写真フォルダ>  … 写真を assets/pr/<slug>/ に webp 変換（hero/a/b/g1/g2/logo.* の名前で置く）
# 共通ヘッダー・フッター・OGP・GA は prod_common.prodpage が付ける。
import os,re,sys,json,glob,html as H
P=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,P)
import prod_common as C
D=C.D; J=os.path.abspath(P+'../pr/')+'/'
esc=lambda s:H.escape(str(s or ''),quote=True)

CSS=r'''
.pra{--acc:#E43B4D;--ink:#1f2a37;--sub:#3a4753;--mute:#8a95a0;--line:#e5e8ec;color:var(--ink);line-height:1.95}
.pra .pra-w{max-width:760px;margin:0 auto;padding:0 22px}
.pra-sample{background:#fff4d6;border-bottom:1px solid #f0dca0;color:#8a6a14;font-size:13px;font-weight:700;text-align:center;padding:11px 14px}
.pra-hero{position:relative;height:400px;overflow:hidden;background:#222}
.pra-hero img{width:100%;height:100%;object-fit:cover;display:block}
.pra-hero .pra-sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,24,30,.1) 0%,rgba(20,24,30,.74) 100%)}
.pra-hero .pra-tx{position:absolute;left:0;right:0;bottom:0;color:#fff;padding-bottom:26px}
.pra-hero .pra-pr{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.5);font-size:11px;font-weight:800;letter-spacing:.08em;padding:3px 10px;border-radius:999px;margin-bottom:12px}
.pra-hero h1{font-size:30px;font-weight:900;margin:0 0 12px;line-height:1.3;letter-spacing:.01em}
.pra-hero .pra-chips{display:flex;gap:8px;flex-wrap:wrap}
.pra-hero .pra-chip{font-size:12.5px;font-weight:700;padding:5px 12px;border-radius:999px;background:var(--acc);color:#fff}
.pra-hero .pra-chip.pra-g{background:rgba(255,255,255,.92);color:#333}
.pra-head{padding:34px 0 6px}
.pra-head .pra-hl{font-size:21px;font-weight:900;line-height:1.6;margin:0 0 6px}
.pra-head .pra-sb{font-size:16px;font-weight:700;color:var(--sub);margin:0 0 18px}
.pra p.pra-b{font-size:15px;color:var(--sub);line-height:2.1;margin:0 0 22px}
.pra h2{font-size:23px;font-weight:900;color:var(--ink);margin:46px 0 20px;line-height:1.55;position:relative;padding-left:15px}
.pra h2::before{content:"";position:absolute;left:0;top:5px;bottom:5px;width:5px;border-radius:3px;background:linear-gradient(#e8784a,#E43B4D)}
.pra .pra-fig{margin:28px 0 30px;border-radius:16px;overflow:hidden}
.pra .pra-fig img{width:100%;display:block;aspect-ratio:4/3;object-fit:cover}
.pra .pra-cap{font-size:12px;color:var(--mute);margin-top:8px;text-align:center}
.pra .pra-steps{display:grid;gap:12px;margin:0 0 8px}
.pra .pra-st{display:grid;grid-template-columns:38px 1fr;gap:12px;align-items:start;background:#fbf8f6;border:1px solid #f0e6df;border-radius:14px;padding:14px 16px}
.pra .pra-st .pra-n{width:34px;height:34px;border-radius:50%;background:var(--acc);color:#fff;font-weight:900;display:grid;place-items:center;font-size:15px}
.pra .pra-st b{display:block;font-size:15px;margin-bottom:2px}.pra .pra-st span{font-size:14px;color:var(--sub);line-height:1.8}
.pra .pra-qa{display:grid;gap:14px}
.pra .pra-qa div{background:#f7f8fa;border-radius:14px;padding:16px 18px}
.pra .pra-qa b{display:block;font-size:15px;margin-bottom:6px}.pra .pra-qa b::before{content:"Q. ";color:var(--acc)}
.pra .pra-qa p{margin:0;font-size:14.5px;color:var(--sub);line-height:1.9}
.pra ul.pra-fits{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.pra ul.pra-fits li{position:relative;padding-left:30px;font-size:15px;color:var(--sub)}
.pra ul.pra-fits li::before{content:"✓";position:absolute;left:0;top:0;width:22px;height:22px;border-radius:50%;background:#fde8ec;color:var(--acc);font-weight:900;font-size:13px;display:grid;place-items:center}
.pra .pra-gal{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:26px 0}
.pra .pra-gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:12px;display:block}
.pra .pra-voice{background:#fff;border:1px solid var(--line);border-left:5px solid var(--acc);border-radius:12px;padding:16px 18px;margin:0 0 12px}
.pra .pra-voice p{margin:0 0 6px;font-size:14.5px;color:var(--sub);line-height:1.9}.pra .pra-voice small{color:var(--mute);font-size:12.5px}
.pra .pra-info{border:1px solid var(--line);border-radius:14px;overflow:hidden;display:grid;grid-template-columns:110px 1fr;font-size:13.5px}
.pra .pra-info div{padding:13px 15px;border-bottom:1px solid #eef1f3}.pra .pra-info div:nth-last-child(-n+2){border-bottom:0}
.pra .pra-info .pra-k{background:#f5f7f9;font-weight:700;color:#54606e}.pra .pra-info .pra-v{color:#3a4550}
.pra .pra-ctas{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.pra .pra-ctas a{flex:1 1 150px;text-align:center;font-size:14.5px;font-weight:800;text-decoration:none;padding:14px 0;border-radius:999px;border:1.5px solid #54606e;color:#54606e;background:#fff}
.pra .pra-ctas a.pra-site{background:var(--acc);border-color:var(--acc);color:#fff;box-shadow:0 8px 18px rgba(232,69,95,.26)}
.pra .pra-ctas a.pra-line{border-color:#06c755;color:#06c755}
.pra .pra-ctas a.pra-ig{border-color:#d6336c;color:#d6336c}
.pra .pra-apply{display:block;text-decoration:none;background:linear-gradient(100deg,#fff4f6,#fef0ea);border:1px solid #f3c9da;border-radius:16px;padding:26px 24px;text-align:center;margin:40px 0 0;color:var(--ink)}
.pra .pra-apply b{display:block;font-size:18px;font-weight:900;margin-bottom:7px}
.pra .pra-apply p{font-size:13px;color:#7b8492;line-height:1.85;margin:0 0 18px}
.pra .pra-apply span{display:inline-block;background:var(--acc);color:#fff;font-size:14.5px;font-weight:800;padding:13px 30px;border-radius:999px}
.pra .pra-disc{background:#f6f7f9;border-radius:14px;padding:18px 20px;font-size:12px;color:var(--mute);line-height:1.85;margin:30px 0 0}
.pra .pra-back{text-align:center;margin:22px 0 56px}.pra .pra-back a{font-size:13.5px;font-weight:700;color:var(--acc);text-decoration:none}
@media(max-width:560px){.pra-hero{height:330px}.pra-hero h1{font-size:25px}.pra h2{font-size:20px}.pra p.pra-b{font-size:14.5px}.pra .pra-info{grid-template-columns:104px 1fr}}
'''

def build(d):
    slug=d['slug']; im=d.get('images',{}); name=d['name']
    area=d.get('area_label') or ('オンラインショップ（全国対応）' if d.get('online') else ' '.join(x for x in [d.get('pref',''),d.get('city','')] if x))
    o=[]; a=o.append
    a('<main class="pra">')
    if d.get('sample'): a('<div class="pra-sample">🔖 これは掲載イメージのサンプル記事です（実在の会社・内容ではありません）。点線の枠が、写真を入れる場所です。</div>')
    a('<section class="pra-hero"><img src="%s" alt="%s"><div class="pra-sh"></div><div class="pra-tx"><div class="pra-w">'%(esc(im.get('hero','')),esc(name)))
    a('<span class="pra-pr">PR ｜ %s</span><h1>%s</h1><div class="pra-chips"><span class="pra-chip">%s</span>%s</div>'%('サンプル記事' if d.get('sample') else '企業紹介',esc(name),esc(d.get('category','')),'<span class="pra-chip pra-g">%s</span>'%esc(area) if area else ''))
    a('</div></div></section>')
    a('<section class="pra-head"><div class="pra-w">')
    if d.get('headline'): a('<p class="pra-hl">%s</p>'%esc(d['headline']))
    if d.get('sub'): a('<p class="pra-sb">%s</p>'%esc(d['sub']))
    if d.get('lead'): a('<p class="pra-b">%s</p>'%d['lead'])
    a('</div></section>')
    a('<section><div class="pra-w">')
    for s in d.get('sections',[]):
        a('<h2>%s</h2>'%esc(s['h2']))
        if s.get('body'): a('<p class="pra-b">%s</p>'%s['body'])
        if s.get('steps'):
            a('<div class="pra-steps">'+''.join('<div class="pra-st"><div class="pra-n">%d</div><div><b>%s</b><span>%s</span></div></div>'%(i+1,esc(x['t']),esc(x['d'])) for i,x in enumerate(s['steps']))+'</div>')
        if s.get('image') and im.get(s['image']):
            a('<div class="pra-fig"><img loading="lazy" decoding="async" src="%s" alt="%s">%s</div>'%(esc(im[s['image']]),esc(s.get('alt','')),'<div class="pra-cap">%s</div>'%esc(s['caption']) if s.get('caption') else ''))
    if d.get('qa'):
        a('<h2>%s</h2><div class="pra-qa">'%esc(d.get('qa_title','担当者に聞きました'))+''.join('<div><b>%s</b><p>%s</p></div>'%(esc(x['q']),esc(x['a'])) for x in d['qa'])+'</div>')
    if d.get('fits'):
        a('<h2>%s</h2><ul class="pra-fits">'%esc(d.get('fits_title','こんなときに'))+''.join('<li>%s</li>'%esc(x) for x in d['fits'])+'</ul>')
    if im.get('g1') or im.get('g2') or d.get('voices'):
        a('<h2>%s</h2>'%esc(d.get('voices_title','納品事例・利用したチームの声')))
        if im.get('g1') or im.get('g2'):
            a('<div class="pra-gal">'+''.join('<img loading="lazy" decoding="async" src="%s" alt="">'%esc(im[k]) for k in ('g1','g2') if im.get(k))+'</div>')
        for v in d.get('voices',[]): a('<div class="pra-voice"><p>「%s」</p><small>— %s</small></div>'%(esc(v['text']),esc(v.get('who',''))))
    a('</div></section>')
    a('<section><div class="pra-w"><h2>%s</h2>'%esc(d.get('info_title','店舗・会社情報')))
    a('<div class="pra-info">'+''.join('<div class="pra-k">%s</div><div class="pra-v">%s</div>'%(esc(x['label']),esc(x['value'])) for x in d.get('info',[]))+'</div>')
    ctas=list(d.get('ctas',[]))
    if d.get('sns',{}).get('instagram'): ctas.append({'kind':'ig','label':'Instagram','url':d['sns']['instagram']})
    a('<div class="pra-ctas">'+''.join('<a class="pra-%s" href="%s" target="_blank" rel="noopener sponsored">%s</a>'%(esc(x.get('kind','')),esc(x['url']),esc(x['label'])) for x in ctas)+'</div>')
    a('<a class="pra-apply" href="service-ads.html"><b>あなたのお店も、こんな記事で紹介しませんか？</b><p>地域の子育て世帯に届く、チビスポの企業紹介ページ。<br>取材・制作はおまかせください。</p><span>掲載を申し込む ›</span></a>')
    a('<div class="pra-disc">この記事は、%sの提供による<strong style="color:#54606e">チビスポのPR記事（広告）</strong>です。掲載内容は取材時点のものです。最新情報は各社の公式サイト等をご確認ください。</div>'%esc(name))
    a('<div class="pra-back"><a href="search.html">‹ クラブを探すに戻る</a></div>')
    a('</div></section></main>')
    body='\n'.join(o)
    fname=d.get('out') or 'pr/%s.html'%slug
    os.makedirs(os.path.dirname(D+fname),exist_ok=True)
    title='%s｜チビスポ 企業紹介%s'%(name,'（サンプル）' if d.get('sample') else '')
    desc=d.get('description') or re.sub(r'<[^>]+>','',d.get('lead',''))[:110]
    og=d.get('og_image') or ('https://chibispo.com/'+im['hero'] if im.get('hero') and not im['hero'].endswith('.svg') else 'https://chibispo.com/assets/ogp.jpg?v=2')
    C.prodpage(fname,title,desc,body,css=CSS,noindex=bool(d.get('noindex')),base_root=True,og_image=og)
    # 広告枠（companies）に入れる行を横に出す
    print('  companies:',json.dumps({'name':name,'category':d.get('category'),'tagline':d.get('tagline'),'pref':d.get('pref') or None,'city':d.get('city') or None,'online':bool(d.get('online')),'banner_url':im.get('logo') or im.get('hero'),'page_url':fname,'status':'active'},ensure_ascii=False))

def images(slug,src):
    from PIL import Image
    out=D+'assets/pr/%s/'%slug; os.makedirs(out,exist_ok=True)
    spec={'hero':(1400,None),'a':(1200,None),'b':(1200,None),'g1':(1200,None),'g2':(1200,None),'logo':(400,400)}
    for f in sorted(os.listdir(src)):
        k=os.path.splitext(f)[0].lower()
        if k not in spec or f.startswith('.'): continue
        w,sq=spec[k]; im=Image.open(os.path.join(src,f)).convert('RGB')
        if sq:   # 正方形に中央トリミング
            s=min(im.size); im=im.crop(((im.width-s)//2,(im.height-s)//2,(im.width-s)//2+s,(im.height-s)//2+s))
        if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
        im.save(out+k+'.webp','WEBP',quality=82,method=6); print(' ',k,im.size,os.path.getsize(out+k+'.webp')//1024,'KB')
    print('→ json の images に assets/pr/%s/<key>.webp を書く'%slug)

if __name__=='__main__':
    args=sys.argv[1:]
    if args and args[0]=='--images': images(args[1],args[2]); sys.exit()
    files=[J+a+'.json' for a in args] if args else sorted(glob.glob(J+'*.json'))
    for f in files:
        d=json.load(open(f,encoding='utf-8')); print(f.split('/')[-1]); build(d)
