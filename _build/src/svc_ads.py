# ---- サービス05：地域の広告掲載（LP・売上直結）。svc_listing.py の後に exec（sl_css を継承）
ad_css=sl_css+r'''
/* ===== 広告LP 固有 ===== */
/* ヒーロー：明るい地色・実寸の広告枠 */
.adhero{position:relative;background:var(--card);color:var(--ink);overflow:hidden;border-bottom:2px solid var(--ink)}
.adhero .bgl{position:absolute;inset:0;display:none;pointer-events:none}
.adhero[data-bg="map"] .bg-map,.adhero[data-bg="grid"] .bg-grid,.adhero[data-bg="dots"] .bg-dots{display:block}
/* E 地図 */
.bg-map{background:url(assets/preview-video/ad-hero-map.jpg) center right/cover no-repeat;opacity:.5;filter:saturate(.85)}
.bg-map::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--card) 0%,var(--card) 30%,color-mix(in srgb,var(--card) 55%,transparent) 62%,color-mix(in srgb,var(--card) 25%,transparent) 100%)}
.bg-map::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,var(--card) 0%,transparent 22%,transparent 80%,var(--card) 100%)}
/* B 方眼＋同心円＋ピン（地図の抽象） */
.bg-grid{background-image:
  repeating-linear-gradient(0deg,color-mix(in srgb,var(--ink) 7%,transparent) 0 1px,transparent 1px 56px),
  repeating-linear-gradient(90deg,color-mix(in srgb,var(--ink) 7%,transparent) 0 1px,transparent 1px 56px);
  -webkit-mask-image:radial-gradient(120% 100% at 78% 45%,#000 0%,#000 42%,transparent 78%);
  mask-image:radial-gradient(120% 100% at 78% 45%,#000 0%,#000 42%,transparent 78%)}
.bg-grid::before{content:"";position:absolute;left:78%;top:45%;width:min(900px,62vw);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;
  background:repeating-radial-gradient(circle,transparent 0 68px,color-mix(in srgb,var(--accent) 16%,transparent) 68px 69px);
  -webkit-mask-image:radial-gradient(circle,#000 30%,transparent 72%);mask-image:radial-gradient(circle,#000 30%,transparent 72%)}
.bg-grid .pin{position:absolute;width:18px;height:18px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:color-mix(in srgb,var(--accent) 26%,transparent);animation:pinUp .7s ease-out backwards}
.bg-grid .pin::after{content:"";position:absolute;left:5px;top:5px;width:8px;height:8px;border-radius:50%;background:color-mix(in srgb,var(--card) 85%,transparent)}
.bg-grid .p1{left:60%;top:24%;animation-delay:.2s}.bg-grid .p2{left:86%;top:34%;animation-delay:.35s}
.bg-grid .p3{left:70%;top:70%;animation-delay:.5s}.bg-grid .p4{left:92%;top:66%;animation-delay:.65s}
.bg-grid .p5{left:54%;top:52%;width:24px;height:24px;background:color-mix(in srgb,var(--accent) 42%,transparent);animation-delay:.8s}
.bg-grid .p5::after{left:7px;top:7px;width:10px;height:10px}
@keyframes pinUp{from{opacity:0;transform:rotate(-45deg) translate(6px,-10px)}to{opacity:1;transform:rotate(-45deg)}}
/* C ドット */
.bg-dots{background-image:radial-gradient(color-mix(in srgb,var(--ink) 13%,transparent) 1.4px,transparent 1.4px);background-size:20px 20px;
  -webkit-mask-image:linear-gradient(100deg,transparent 26%,#000 58%,#000 100%);mask-image:linear-gradient(100deg,transparent 26%,#000 58%,#000 100%)}
/* D 巨大タイポ */
.adhero[data-bg="type"] .ty3{right:-4vw;top:-4vw}
.adhero[data-bg="type"] .ty3 span{font-size:clamp(120px,24vw,340px);-webkit-text-stroke-width:2px;-webkit-text-stroke-color:color-mix(in srgb,var(--ink) 13%,transparent)}
.adhero[data-bg="none"] .ty3{display:none}
body[data-skin="stadium"] .bg-map{opacity:.22;filter:grayscale(1) invert(1)}
@media(max-width:759px){.bg-map{opacity:.3}.bg-grid{-webkit-mask-image:radial-gradient(140% 60% at 70% 30%,#000 0%,#000 40%,transparent 80%);mask-image:radial-gradient(140% 60% at 70% 30%,#000 0%,#000 40%,transparent 80%)}.bg-grid::before{left:70%;top:28%;width:80vw}}
/* 切替バー（プレビュー専用） */
.bgsw{position:fixed;left:14px;bottom:14px;z-index:70;display:flex;gap:4px;align-items:center;background:var(--card);border:1px solid var(--ink);padding:6px 8px;font-size:11px;font-weight:900;flex-wrap:wrap;max-width:calc(100vw - 28px)}
.bgsw span{font-family:'Anton',sans-serif;letter-spacing:.2em;color:var(--accent);margin-right:4px}
.bgsw button{border:1px solid var(--line);background:transparent;color:var(--ink);font-family:var(--f);font-size:11px;font-weight:900;padding:5px 8px;cursor:pointer}
.bgsw button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.adhero .in{position:relative;max-width:1200px;margin:0 auto;padding:40px 20px 34px;display:grid;grid-template-columns:1fr;gap:28px}
.adhero .ty3{position:absolute;right:-6px;top:-10px;z-index:1;display:grid;justify-items:end;line-height:.84;font-family:'Anton',sans-serif;letter-spacing:-.01em;pointer-events:none;z-index:0}
.adhero .ty3 span{font-size:clamp(90px,17vw,240px);color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--ink) 16%,transparent)}
.adhero .cp{position:relative;z-index:1}
.adhero .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:12px}
.adhero .ey::before{content:"";width:22px;height:2px;background:var(--accent)}
.adhero h1{font-family:var(--fh);margin:0 0 14px;font-size:clamp(30px,7.6vw,58px);font-weight:900;line-height:1.15;letter-spacing:-.015em}
.adhero h1 em{font-style:normal;color:var(--accent)}
.adhero h1 span{display:inline-block;opacity:0;transform:translateY(18px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.adhero h1 span:nth-child(2){animation-delay:.12s}.adhero h1 span:nth-child(3){animation-delay:.24s}
.adhero .ld{font-size:14px;font-weight:700;color:var(--sub);line-height:1.9;max-width:520px;margin:0 0 18px}
.adhero .price-tag{display:inline-flex;align-items:baseline;flex-wrap:wrap;gap:8px;margin:0 0 18px;padding:10px 14px;border:1px solid var(--ink);font-family:'Anton',sans-serif;letter-spacing:.06em;background:var(--card)}
.adhero .price-tag b{font-size:30px;font-weight:400}
.adhero .price-tag small{font-family:var(--f);font-size:11px;font-weight:700;color:var(--sub);letter-spacing:0}
.adhero .price-tag em{font-style:normal;color:var(--accent);font-size:11px;letter-spacing:.2em}
.adhero .cta{display:flex;gap:10px;flex-wrap:wrap}
.adhero .b1{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 28px;box-shadow:0 8px 24px rgba(232,69,95,.35)}
.adhero .b1.pulse{animation:pulseBtn 2.4s ease-in-out infinite}
.adhero .b2{border:1.5px solid var(--ink);color:var(--ink);font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 24px}
.adhero .unitw{position:relative;z-index:1}
.unit-lb{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:11.5px;font-weight:700;color:var(--sub);margin-bottom:10px}
.unit-lb .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.22em;color:var(--accent);padding-left:30px;background:linear-gradient(var(--accent),var(--accent)) 0 50%/20px 2px no-repeat}
.adunit{background:var(--bg);border:1px solid var(--line);padding:18px 16px 14px;position:relative}
.adunit .uh{margin-bottom:12px}
.adunit .ut{font-family:var(--fh);font-size:18px;font-weight:900;letter-spacing:-.01em}
.adunit .ut em{font-style:normal;color:var(--accent)}
.adunit .ut i{font-style:normal;display:inline-block;font-size:9.5px;font-weight:900;letter-spacing:.12em;color:var(--sub);border:1px solid var(--line);padding:2px 6px;border-radius:3px;vertical-align:middle;margin-left:8px}
.adunit .us{font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px}
.adunit .ug{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.adunit .tile{position:relative;border:1px solid var(--line);background:var(--card);padding:12px;display:flex;gap:11px;align-items:center}
.adunit .tile .lg{width:64px;height:64px;background:color-mix(in srgb,var(--ink) 6%,var(--bg));overflow:hidden;flex:none}
.adunit .tile .lg img{width:100%;height:100%;object-fit:cover;display:block}
.adunit .tile .t{font-size:12.5px;font-weight:900;line-height:1.4;min-width:0}
.adunit .tile .t small{display:block;font-size:10.5px;font-weight:700;color:var(--sub);margin-top:2px}
.adunit .tile.you{border:2px solid var(--accent);background:color-mix(in srgb,var(--accent) 6%,var(--card))}
.adunit .tile.you .lg{outline:2px solid var(--accent);outline-offset:-2px}
.adunit .tile.you .tag{position:absolute;left:-2px;top:-12px;background:var(--accent);color:#fff;font-size:10px;font-weight:900;padding:3px 8px;letter-spacing:.06em}
.adunit .tile.you .ring{position:absolute;inset:-6px;border:2px solid var(--accent);opacity:0;animation:ping 2.2s ease-out infinite;pointer-events:none}
.adunit .uf{margin-top:10px;font-size:11px;font-weight:700;color:var(--sub)}
.adhero .stats{display:flex;gap:18px 30px;flex-wrap:wrap;margin-top:18px;padding-top:14px;border-top:1px solid var(--line)}
.adhero .stats div{font-family:'Anton',sans-serif;letter-spacing:.06em}
.adhero .stats b{display:block;font-size:30px;font-weight:400;line-height:1;color:var(--ink)}
.adhero .stats small{font-size:10.5px;letter-spacing:.22em;color:var(--sub)}
/* 流れの縮図 */
.vis{height:190px;background:var(--bg);border:1px solid var(--line);margin-bottom:12px;overflow:hidden;position:relative;font-family:var(--f);color:var(--ink)}
.flow4 .nd.hot .vis{border-color:color-mix(in srgb,var(--bg) 30%,transparent)}
.vis .mp{padding:12px;display:grid;gap:8px;align-content:center;height:100%}
.vis .mh{font-family:'Anton',sans-serif;font-size:9.5px;letter-spacing:.22em;color:var(--accent)}
.vis .mr{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center;background:var(--card);border:1px solid var(--line);padding:9px 10px}
.vis .mr i{width:26px;height:26px;background:color-mix(in srgb,var(--accent) 12%,var(--card));border-radius:50%;position:relative}
.vis .mr i::after{content:"";position:absolute;left:9px;top:6px;width:8px;height:8px;border:2px solid var(--accent);border-radius:50% 50% 50% 0;transform:rotate(-45deg)}
.vis .mr small{display:block;font-size:8.5px;font-weight:700;color:var(--sub)}
.vis .mr b{font-size:12px;font-weight:900}
.vis .mr span{font-size:9px;font-weight:900;border:1px solid var(--ink);padding:3px 7px}
.vis .mqq{font-size:9.5px;font-weight:700;color:var(--sub)}
.vis .ub{padding:12px;background:var(--bg);height:100%;display:grid;align-content:center}
.vis .ubt{font-family:var(--fh);font-size:11.5px;font-weight:900;margin-bottom:8px;color:var(--ink)}
.vis .ubt i{font-style:normal;font-size:7.5px;letter-spacing:.1em;color:var(--sub);border:1px solid var(--line);padding:1px 4px;margin-left:4px;vertical-align:1px}
.vis .ubg{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.vis .ubg div{display:flex;align-items:center;gap:6px;background:var(--card);border:1px solid var(--line);padding:7px 8px;font-size:9px;font-weight:900;white-space:nowrap;overflow:hidden;color:var(--ink)}
.vis .ubg span{width:26px;height:26px;flex:none;overflow:hidden;background:color-mix(in srgb,var(--ink) 6%,var(--bg))}
.vis .ubg span img{width:100%;height:100%;object-fit:cover;display:block}
.vis .ubg .you span{outline:0}
.vis .ubg .you{border:2px solid var(--accent);background:color-mix(in srgb,var(--accent) 6%,var(--card))}

.vis.v3 img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.vis .bt{padding:12px;display:grid;gap:10px;align-content:center;height:100%;background:linear-gradient(180deg,var(--bg),color-mix(in srgb,var(--ink) 4%,var(--bg)))}
.vis .bh{font-family:var(--fh);font-size:12px;font-weight:900}
.vis .bh small{display:block;font-size:8.5px;font-weight:700;color:var(--sub);margin-top:2px}
.vis .bb{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px}
.vis .bb span{font-size:8.5px;font-weight:900;text-align:center;padding:8px 2px;border:1px solid var(--ink)}
.vis .bb .c2{background:#06c755;color:#fff;border-color:#06c755}
.vis .bb .c3{background:var(--accent);color:#fff;border-color:var(--accent)}
@media(max-width:519px){.adunit .ug{grid-template-columns:1fr}.adunit .tile .t{font-size:13px}}
.band{margin:56px -20px 0;padding:46px 20px 44px;background:color-mix(in srgb,var(--ink) 4%,var(--bg));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
body[data-skin="stadium"] .band{background:#0f1115}
.band+.sec2{padding-top:56px}
@media(min-width:760px){.band{padding:56px 40px 52px}}
/* 申込の帯 */
.apply-band{margin:60px -20px 0;padding:44px 20px 40px;background:color-mix(in srgb,var(--accent) 7%,var(--bg));border-top:3px solid var(--accent)}
.apply-band .aform{background:var(--card);border:1px solid var(--ink);padding:8px 20px 22px;box-shadow:8px 8px 0 var(--ink)}
.apply-band .trust{border-top:0;margin-top:26px}
.apply-band .trust div{border-bottom-color:color-mix(in srgb,var(--ink) 15%,transparent)}

.lp-hero.lpads .bg{background-image:url(assets/preview-video/wm-bball-jp.jpg)}
.lp-hero .b1.pulse{animation:pulseBtn 2.4s ease-in-out infinite}
@keyframes pulseBtn{0%,100%{box-shadow:0 8px 24px rgba(232,69,95,.35)}50%{box-shadow:0 8px 34px rgba(232,69,95,.7)}}
.lp-hero .price-tag{display:inline-flex;align-items:baseline;gap:8px;margin:0 0 16px;padding:8px 14px;border:1px solid rgba(255,255,255,.35);font-family:'Anton',sans-serif;letter-spacing:.06em}
.lp-hero .price-tag b{font-size:28px;font-weight:400;color:#fff}
.lp-hero .price-tag small{font-family:var(--f);font-size:11px;font-weight:700;color:rgba(255,255,255,.7);letter-spacing:0}
.lp-hero .price-tag em{font-style:normal;color:var(--accent);font-size:11px;letter-spacing:.2em;margin-left:6px}
/* ヒーロー右：掲載イメージ（HTMLで組む・実画面の縮図） */
.adv{position:relative;height:470px;width:100%;max-width:520px;justify-self:center}
.adv .ty2{right:0;top:-6px}
.adv .fan2{width:186px;height:362px;margin-left:-93px;bottom:48px}
.adv .fan2>*{position:absolute;inset:0;width:100%;height:100%;max-width:none;border-radius:16px;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.14);transform-origin:50% 115%;transition:transform .5s cubic-bezier(.2,.7,.2,1);opacity:0;animation:fanIn .7s forwards;background:#f2f0eb}
.adv .fan2 .a1{transform:rotate(-10deg) translateX(-118px) translateY(10px);z-index:1;animation-delay:.5s}
.adv .fan2 .a2{transform:rotate(8deg) translateX(118px) translateY(4px);z-index:2;animation-delay:.8s}
.adv .fan2:hover .a1{transform:rotate(-16deg) translateX(-158px) translateY(10px)}
.adv .fan2:hover .a2{transform:rotate(14deg) translateX(158px) translateY(4px)}
.adv .fan2 img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.mini{background:#f4f2ee;color:#111;padding:14px 12px;font-family:var(--f);display:flex;flex-direction:column;gap:8px;height:100%}
.mini .mh{font-size:9.5px;font-weight:900;color:#777;letter-spacing:.04em}
.mini .mcta{background:var(--accent);color:#fff;font-size:10.5px;font-weight:900;text-align:center;padding:9px;font-family:var(--fh)}
.mini .mtl{margin-top:8px;padding-top:10px;border-top:2px solid #111;font-size:11.5px;font-weight:900;font-family:var(--fh)}
.mini .mtl i{font-style:normal;font-size:8px;letter-spacing:.1em;color:#777;border:1px solid #ccc;padding:1px 4px;margin-left:6px;vertical-align:1px}
.mini .mg{display:grid;grid-template-columns:1fr;gap:6px}
.mini .mg div{border:1px solid #ddd;background:#fff;padding:7px 8px;display:flex;gap:8px;align-items:center;font-size:10px;font-weight:900;line-height:1.3;white-space:nowrap;overflow:hidden}
.mini .mg div span{width:22px;height:22px;background:#eee;flex:none;display:flex;align-items:center;justify-content:center;font-family:'Anton',sans-serif;font-size:10px;color:#888}
.mini .mg div small{display:block;font-size:8px;font-weight:700;color:#777}
.mini .mg div.you{border:2px solid var(--accent);position:relative;background:color-mix(in srgb,var(--accent) 6%,#fff)}
.mini .mg div.you::after{content:"あなたのお店";position:absolute;left:-2px;top:-14px;background:var(--accent);color:#fff;font-size:8px;font-weight:900;padding:2px 6px;letter-spacing:.04em}
.mini .mg div.you span{background:var(--accent);color:#fff}
.adv .hv-cap{position:absolute;left:0;right:0;bottom:0;margin:0}
/* こんなお店に */
.who{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--ink)}
.who .w{padding:16px 14px;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.who .w:nth-child(2n){border-right:0}
.who .w:nth-last-child(-n+2){border-bottom:0}
.who .w svg{width:28px;height:28px;fill:none;stroke:var(--accent);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;margin-bottom:8px}
.who .w b{display:block;font-family:var(--fh);font-size:14px;font-weight:900;margin-bottom:4px}
.who .w small{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7}
/* 流れ図（4ノード） */
.flow4{display:grid;grid-template-columns:1fr;gap:0}
.flow4 .nd{position:relative;border:1px solid var(--ink);padding:16px 16px 16px 60px;background:var(--card)}
.flow4 .nd+.nd{border-top:0}
.flow4 .nd .no{position:absolute;left:16px;top:16px;width:30px;height:30px;background:var(--ink);color:var(--bg);font-family:'Anton',sans-serif;font-size:12px;display:flex;align-items:center;justify-content:center}
.flow4 .nd.hot{background:var(--ink);color:var(--bg)}
.flow4 .nd.hot .no{background:var(--accent);color:#fff}
.flow4 .nd b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;margin-bottom:3px}
.flow4 .nd small{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7}
.flow4 .nd.hot small{color:color-mix(in srgb,var(--bg) 70%,transparent)}
.flow4 .nd{opacity:0;transform:translateY(10px);transition:opacity .5s,transform .5s}
.flow4.in .nd{opacity:1;transform:none}
.flow4.in .nd:nth-child(2){transition-delay:.2s}.flow4.in .nd:nth-child(3){transition-delay:.4s}.flow4.in .nd:nth-child(4){transition-delay:.6s}
.geo-note{margin-top:14px;display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start;border-left:3px solid var(--accent);padding:4px 0 4px 14px;font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.geo-note b{color:var(--ink)}
/* 単一プラン */
.one{display:grid;grid-template-columns:1fr;gap:0;border:2px solid var(--accent);box-shadow:10px 10px 0 var(--accent);background:var(--card)}
body[data-skin="bright"] .one,body[data-skin="stadium"] .one{border-radius:var(--r)}
.one .l{padding:26px 22px 22px;border-bottom:1px solid var(--line)}
.one .n{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.one h3{font-family:var(--fh);margin:0 0 10px;font-size:24px;font-weight:900;line-height:1.3}
.one .pr{font-family:'Anton',sans-serif;font-size:52px;line-height:1;letter-spacing:.02em}
.one .pr small{font-family:var(--f);font-size:13px;font-weight:700;color:var(--sub);letter-spacing:0;margin-left:6px}
.one .per{margin-top:8px;font-size:12.5px;font-weight:900;color:var(--accent)}
.one .per small{display:block;font-weight:700;color:var(--sub);font-size:11px;margin-top:2px}
.one .go{display:block;margin-top:18px;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:16px;padding:16px;text-align:center;letter-spacing:.04em;box-shadow:0 8px 24px rgba(232,69,95,.3)}
.one .go2{display:block;margin-top:8px;text-align:center;font-size:12.5px;font-weight:900;text-decoration:underline;text-underline-offset:4px}
.one .r{padding:22px 22px 24px}
.one .r .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--sub);margin-bottom:8px}
.one ul{list-style:none;margin:0;padding:0}
.one li{position:relative;padding:10px 0 10px 26px;border-bottom:1px solid var(--line);font-size:13.5px;font-weight:900;line-height:1.5}
.one li::before{content:"";position:absolute;left:2px;top:15px;width:11px;height:6px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
.one li small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px}
.one .r .nt{margin-top:12px;font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.8}
/* 取材記事の中身 */
.sample{display:grid;grid-template-columns:1fr;gap:22px;align-items:center}
.sample .ph2{width:230px;margin:0 auto;border:8px solid #1b1d21;border-radius:34px;background:#000;box-shadow:12px 12px 0 var(--ink);overflow:hidden;aspect-ratio:9/18.4;position:relative}
.sample .ph2 img{width:100%;display:block;animation:pmScroll 10s ease-in-out infinite alternate}
.sample ul{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
.sample li{position:relative;padding:12px 0 12px 34px;border-bottom:1px solid var(--line);font-size:14px;font-weight:900}
.sample li::before{content:attr(data-n);position:absolute;left:0;top:14px;font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.06em;color:var(--accent)}
.sample li small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px}
.sample .lk{margin-top:14px;display:inline-block;font-size:13px;font-weight:900;text-decoration:underline;text-underline-offset:4px}
/* 申込フォーム */
.aform{border-top:2px solid var(--ink);padding-top:6px}
.aform .row{display:grid;grid-template-columns:1fr;gap:0 24px}
.aform label{display:block;padding:14px 0 6px;font-size:11.5px;font-weight:900;letter-spacing:.08em}
.aform label i{font-style:normal;font-size:9px;letter-spacing:.08em;color:var(--bg);background:var(--ink);padding:1px 6px;margin-left:8px;vertical-align:1px}
.aform input,.aform select,.aform textarea{width:100%;border:0;border-bottom:1px solid var(--ink);background:transparent;padding:10px 0;font-family:var(--f);font-size:14px;font-weight:700;color:var(--ink);border-radius:0}
.aform textarea{min-height:90px;border:1px solid var(--line);padding:10px}
.aform .send{display:block;width:100%;margin-top:22px;background:var(--accent);color:#fff;border:0;font-family:var(--fh);font-weight:900;font-size:16px;padding:17px;cursor:pointer;letter-spacing:.04em;box-shadow:0 8px 24px rgba(232,69,95,.3)}
.aform .pv{margin-top:10px;font-size:11px;font-weight:700;color:var(--sub);text-align:center}
.aform .re{margin-top:18px;display:flex;gap:18px;justify-content:center;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--sub)}
.aform .re b{font-size:16px;font-weight:400;color:var(--ink);margin-right:5px}
.trust{display:grid;grid-template-columns:1fr;gap:0;border-top:2px solid var(--ink);margin-top:26px}
.trust div{position:relative;padding:14px 0 14px 30px;border-bottom:1px solid var(--line);font-size:13px;font-weight:900;line-height:1.5}
.trust div::before{content:attr(data-n);position:absolute;left:0;top:16px;font-family:'Anton',sans-serif;font-size:12px;color:var(--accent)}
.trust div small{display:block;font-weight:700;color:var(--sub);font-size:11.5px;margin-top:2px;line-height:1.7}
@media(max-width:759px){.adv{height:400px}.adv .fan2{width:150px;height:292px;margin-left:-75px;bottom:40px}.adv .fan2 .a1{transform:rotate(-8deg) translateX(-78px) translateY(8px)}.adv .fan2 .a2{transform:rotate(7deg) translateX(78px) translateY(2px)}.adv .ty2 span{font-size:64px}}
@media(min-width:760px){
  .adhero .in{grid-template-columns:1fr 1.05fr;gap:48px;align-items:center;padding:56px 20px 44px}
  .adunit{padding:22px 22px 16px}
  .adunit .ug{grid-template-columns:1fr 1fr}
  .apply-band{padding:56px 40px 50px}
  .apply-band .aform{padding:10px 34px 28px}
  .who{grid-template-columns:repeat(3,1fr)}
  .who .w:nth-child(2n){border-right:1px solid var(--ink)}
  .who .w:nth-child(3n){border-right:0}
  .who .w:nth-last-child(-n+2){border-bottom:1px solid var(--ink)}
  .who .w:nth-last-child(-n+3){border-bottom:0}
  .flow4{grid-template-columns:repeat(4,1fr)}
  .flow4 .nd+.nd{border-top:1px solid var(--ink);border-left:0}
  .flow4 .nd{padding:56px 18px 20px 18px}
  .flow4 .nd .no{left:18px;top:16px}
  .one{grid-template-columns:1fr 1.15fr}
  .one .l{border-bottom:0;border-right:1px solid var(--line);padding:34px 30px 30px}
  .one .r{padding:30px}
  .sample{grid-template-columns:300px 1fr;gap:56px}
  .aform .row{grid-template-columns:1fr 1fr}
  .trust{grid-template-columns:repeat(3,1fr);gap:0 28px}
}
'''
ad_body='''
<main><div class="wrap">
  <div class="note">【サービス05：地域の広告掲載（LP）】ユーザー「広告事業として大切。デザインとCTAから売上につながるように」。★事実は本番 recruit-pr.html／partner.html／pr-sample.html のとおり：<b>企業紹介プラン ¥50,000/年（税抜目安・制作＋1年掲載込み・初期費用0・2年目以降も同額・年1回の内容リフレッシュ・スポット記事も相談）</b>、対象業種6つ、仕組み＝<b>保護者の登録地域に合わせて表示→取材記事ページへ</b>、掲載先は新サイトの「地域のおすすめ企業」枠（検索結果・クラブ詳細・地図の下）。★売るための設計：①ヒーローに価格と「月あたり約4,200円」の言い換え、赤ボタンは脈打つ ②右に「あなたのお店」が入った掲載イメージ＋取材記事の実画面 ③流れ図で「保護者→枠→記事→予約」を1本に ④プランは1枚で迷わせない・申込ボタンを大きく ⑤取材記事の中身を5点で ⑥最後に<b>申込フォームをページ内に</b>（本番 recruit-pr のフォーム項目と同じ・2〜3営業日で連絡）⑦スマホは追従ボタン。フォームは送信しないダミー。</div>
</div>
<section class="adhero" data-bg="grid">
  <div class="bgl bg-map" aria-hidden="true"></div>
  <div class="bgl bg-grid" aria-hidden="true"><span class="pin p1"></span><span class="pin p2"></span><span class="pin p3"></span><span class="pin p4"></span><span class="pin p5"></span></div>
  <div class="bgl bg-dots" aria-hidden="true"></div>
  <div class="in">
    <div class="ty3" aria-hidden="true"><span>LOCAL</span><span>AD</span></div>
    <div class="cp">
      <div class="ey">FOR LOCAL BUSINESS ・ SERVICE 05</div>
      <h1><span>子育て世帯に、</span><span><em>いちばん近い</em></span><span>広告枠。</span></h1>
      <p class="ld">子どものクラブを探している保護者が見るページに、あなたのお店。取材記事つきで、その地域の家庭にだけ出ます。取材はオンライン30分、写真をお送りいただくだけです。</p>
      <div class="price-tag"><b>¥50,000</b><small>/年（税抜）・オンライン取材と記事制作込み</small><em>≈ ¥4,200 / MONTH</em></div>
      <div class="cta"><a class="b1 pulse" href="#apply">掲載を申し込む</a><a class="b2" href="#sample">取材記事の見本を見る</a></div>
    </div>
    <div class="unitw">
      <div class="unit-lb"><span class="k">ACTUAL AD UNIT</span><span>実際の掲載枠（検索結果・クラブ詳細・地図の下に、この形で出ます）</span></div>
      <div class="adunit">
        <div class="uh"><div class="ut">地域の<em>おすすめ</em>企業<i>PR</i></div><div class="us">世田谷区の子育て世帯に向けて</div></div>
        <div class="ug">
          <div class="tile you"><div class="lg"><img src="assets/preview-video/ad-seikotsu.jpg" alt=""></div><div class="t">さくら整骨院<small>スポーツ外傷・子ども割引</small></div><span class="ring"></span><span class="tag">あなたのお店</span></div>
          <div class="tile"><div class="lg"><img src="assets/preview-video/ad-sports.jpg" alt=""></div><div class="t">経堂スポーツ用品<small>ジュニア用品・名入れ無料</small></div></div>
          <div class="tile"><div class="lg"><img src="assets/preview-video/ad-shika.jpg" alt=""></div><div class="t">みどり歯科<small>マウスガード作成</small></div></div>
          <div class="tile"><div class="lg"><img src="assets/preview-video/ad-uniform.jpg" alt=""></div><div class="t">デザインボックス<small>チームのユニフォーム制作</small></div></div>
        </div>
        <div class="uf">この枠に掲載する事業者の方は <u>掲載のご案内</u> へ。</div>
      </div>
      <div class="stats"><div><b data-cnt="3">0</b><small>PLACES SHOWN</small></div><div><b data-cnt="1">0</b><small>PR ARTICLE</small></div><div><b data-cnt="0">0</b><small>SETUP FEE</small></div><div><b data-cnt="30">0</b><small>MIN ONLINE</small></div></div>
    </div>
  </div>
</section>
<div class="bgsw" id="bgsw"><span>BG</span><button data-b="none">A なし</button><button data-b="grid" class="on">B 方眼＋ピン</button><button data-b="dots">C ドット</button><button data-b="type">D 巨大タイポ</button><button data-b="map">E 地図</button></div>
<div class="wrap">

  <section class="sec2">
    <div class="ey rv">WHO IT IS FOR</div>
    <h2 class="rv d1">子どもの<em>スポーツまわり</em>で、頼られるお店に。</h2>
    <p class="sub rv d2">保護者は「クラブを探す」ついでに、送迎の途中で寄れるお店を探しています。</p>
    <div class="who rv d2">
      <div class="w"><svg viewBox="0 0 24 24"><path d="M12 3v18M5 8h14M7 21h10"/><path d="M8 8v6a4 4 0 0 0 8 0V8"/></svg><b>整骨院・整体・接骨院</b><small>成長期のケガとケア。「練習のあと膝が痛い」の相談先に</small></div>
      <div class="w"><svg viewBox="0 0 24 24"><path d="M3 15l4-6 5 3 4-7 5 5v5H3z"/><path d="M3 15v3h18v-3"/></svg><b>スポーツ用品店</b><small>シューズ・ウェアの買い替えは年2回。名入れ・ジュニアサイズで</small></div>
      <div class="w"><svg viewBox="0 0 24 24"><path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg><b>学習塾・習い事</b><small>同じ子育て世帯に、文武両道の提案を</small></div>
      <div class="w"><svg viewBox="0 0 24 24"><path d="M5 12a7 7 0 0 1 14 0v7H5z"/><path d="M9 19v2M15 19v2M12 5V3"/></svg><b>飲食・栄養・カフェ</b><small>「食事で体をつくる」と、練習帰りの一杯</small></div>
      <div class="w"><svg viewBox="0 0 24 24"><path d="M12 3l8 4v6c0 5-3.5 7.5-8 8-4.5-.5-8-3-8-8V7z"/><path d="M12 8v8M8 12h8"/></svg><b>クリニック・薬局・歯科</b><small>マウスガード、健診、スポーツ歯科。安心の担当医として</small></div>
      <div class="w"><svg viewBox="0 0 24 24"><path d="M4 10l8-6 8 6v10H4z"/><path d="M10 20v-6h4v6"/></svg><b>地域の店舗・サービス</b><small>写真館・ユニフォーム制作・送迎・保険など、近隣のファミリーに</small></div>
    </div>
  </section>

  <section class="sec2 band">
    <div class="ey rv">HOW IT WORKS</div>
    <h2 class="rv d1">保護者の画面から、<em>予約</em>までが1本。</h2>
    <p class="sub rv d2">クラブを探す動線の途中に、お店が置かれます。</p>
    <div class="flow4" data-tl>
      <div class="nd"><span class="no">01</span><div class="vis v1"><div class="mp"><div class="mh">MY PAGE</div><div class="mr"><i></i><div><small>あなたの地域</small><b>東京都 世田谷区</b></div><span>変更</span></div><div class="mqq">診断・検索でも地域を選びます</div></div></div><b>保護者が地域を登録</b><small>マイページで「世田谷区」。診断や検索でも地域を選ぶ</small></div>
      <div class="nd hot"><span class="no">02</span><div class="vis v2"><div class="ub"><div class="ubt">地域のおすすめ企業 <i>PR</i></div><div class="ubg"><div class="you"><span><img src="assets/preview-video/ad-seikotsu.jpg" alt=""></span>さくら整骨院</div><div><span><img src="assets/preview-video/ad-sports.jpg" alt=""></span>経堂スポーツ用品</div><div><span><img src="assets/preview-video/ad-shika.jpg" alt=""></span>みどり歯科</div><div><span><img src="assets/preview-video/ad-uniform.jpg" alt=""></span>デザインボックス</div></div></div></div><b>同じ地域のお店だけ表示</b><small>検索結果・クラブ詳細・地図の下の枠に、ロゴ＋一言</small></div>
      <div class="nd"><span class="no">03</span><div class="vis v3"><img src="assets/preview-video/svc-shot-pr.png" alt=""></div><b>取材記事ページへ</b><small>想い・こだわり・Q&amp;A・お悩み・店舗情報。検索にも載る</small></div>
      <div class="nd"><span class="no">04</span><div class="vis v4"><div class="bt"><div class="bh">さくら整骨院<small>名古屋市中区 ・ 平日 9:00〜20:00</small></div><div class="bb"><span class="c1">公式サイト</span><span class="c2">LINEで予約</span><span class="c3">電話する</span></div></div></div><b>電話・LINE・公式サイトへ</b><small>記事の下に予約導線。保護者はそのまま連絡できる</small></div>
    </div>
    <div class="geo-note rv"><b>地域でしぼる</b><span>表示は<b>保護者が登録した地域</b>をもとに切り替わります。商圏の外の家庭にはムダに出ないので、小さなお店でも成立します。</span></div>
  </section>

  <section class="sec2" id="plan">
    <div class="ey rv">PLAN</div>
    <h2 class="rv d1">プランは<em>1つ</em>。制作も掲載も、まとめて。</h2>
    <p class="sub rv d2">取材・記事制作・1年間の掲載をセットにした年間プランです。表示は税抜の目安。</p>
    <div class="one rv">
      <div class="l"><div class="n">LOCAL PARTNER</div><h3>企業紹介プラン</h3><div class="pr">¥50,000<small>/年</small></div><div class="per">月あたり約4,200円<small>初期費用0円。2年目以降も同額（年1回の内容リフレッシュ込み）</small></div><a class="go" href="#apply">このプランで申し込む</a><a class="go2" href="#apply">まず相談だけしたい</a></div>
      <div class="r"><div class="k">INCLUDED</div><ul>
        <li>オンライン取材と、専用の紹介ページ（取材記事）の制作<small>取材は30分・オンラインで。文章はこちらで書きます。写真はお店からご提供ください（スマホで撮ったもので大丈夫です）</small></li>
        <li>「地域のおすすめ企業」枠に1年間掲載<small>検索結果・クラブ詳細・地図の下。ロゴ＋一言で記事へ誘導</small></li>
        <li>検索にも載る、長く残る集客資産<small>記事ページはチビスポの中に残り、検索エンジンからも見つかります</small></li>
        <li>掲載内容の差し替え<small>キャンペーンや営業時間の変更は相談OK</small></li>
      </ul><div class="nt">現地での取材・撮影をご希望の場合は別途ご相談ください。スポット（単発）の記事掲載も承ります。掲載エリアやご予算はお気軽にご相談ください。</div></div>
    </div>
  </section>

  <section class="sec2 band" id="sample">
    <div class="ey rv">THE ARTICLE</div>
    <h2 class="rv d1">取材記事は、<em>広告に見えない</em>広告。</h2>
    <p class="sub rv d2">「チビスポが取材した」記事として載るので、保護者は最後まで読みます。</p>
    <div class="sample" data-app>
      <div class="ph2 rv"><img src="assets/preview-video/svc-shot-pr.png" alt=""></div>
      <div>
        <ul class="rv d2">
          <li data-n="01">お店の想い<small>「頑張る子の体を、ケガから守りたい」。見出しはここから</small></li>
          <li data-n="02">こだわり・取り組み<small>成長期への向き合い方、予防、家でできるケア</small></li>
          <li data-n="03">Q&amp;A<small>どんな子が来ている？ 保護者へのサポートは？</small></li>
          <li data-n="04">こんなお悩みに<small>保護者が自分ごとにできる4つの症状・場面</small></li>
          <li data-n="05">店舗情報と予約導線<small>住所・受付時間・最寄り。電話／LINE／公式サイトのボタン</small></li>
        </ul>
        <a class="lk rv d3" href="pr-sample.html" target="_blank">見本の記事をそのまま読む ›</a>
      </div>
    </div>
  </section>

  <section class="sec2">
    <div class="ey rv">FLOW</div>
    <h2 class="rv d1">申込から掲載まで、<em>2週間</em>。</h2>
    <p class="sub rv d2">お店側の作業は、オンライン30分の取材と、写真の送付、原稿の確認だけです。</p>
    <div class="tl" data-tl><div class="lp-bar"><i></i></div>
      <div class="lp-st"><span class="dot">01</span><h3>申込・相談</h3><p>下のフォームから。2〜3営業日以内にご連絡します。</p><span class="t">2–3 DAYS</span></div>
      <div class="lp-st"><span class="dot">02</span><h3>オンライン取材</h3><p>30分程度。あわせて、お店の写真をお送りください。</p><span class="t">ONLINE 30 MIN</span></div>
      <div class="lp-st"><span class="dot">03</span><h3>制作・確認</h3><p>記事とバナーを作成。内容をご確認いただきます。</p><span class="t">1 WEEK</span></div>
      <div class="lp-st"><span class="dot">04</span><h3>掲載開始</h3><p>その地域の保護者の画面に表示。1年間。</p><span class="t">1 YEAR</span></div>
    </div>
  </section>

  <section class="sec2 band">
    <div class="ey rv">FAQ</div>
    <h2 class="rv d1">よくある質問</h2>
    <div class="faq rv d2">
      <details><summary>文章を書くのが苦手です。写真はどうすればいいですか。</summary><div class="a">文章はこちらで書きます。写真はお店からお送りください。スマホで撮ったもので大丈夫です。店内・スタッフ・施術やサービスの様子が3〜5枚あると記事になります。手元に写真がない場合や、現地での取材・撮影をご希望の場合は別途ご相談ください。</div></details>
      <details><summary>どの地域に表示されますか。</summary><div class="a">保護者がマイページや検索で登録・選択した地域をもとに表示します。お店の商圏に合わせて掲載エリアを相談できます。</div></details>
      <details><summary>途中で内容を変えられますか。</summary><div class="a">キャンペーンや営業時間の変更など、掲載内容の差し替えは相談OKです。2年目以降は年1回の内容リフレッシュが含まれます。</div></details>
      <details><summary>どんなお店でも載せられますか。</summary><div class="a">子育て世帯に向くお店・サービスが対象です。内容によってはお断りする場合があります。迷ったら、まず相談ください。</div></details>
    </div>
  </section>

  <section class="sec2 apply-band" id="apply">
    <div class="ey rv">APPLY</div>
    <h2 class="rv d1">掲載のお申し込み・<em>相談</em></h2>
    <p class="sub rv d2">「まず相談したい」で大丈夫です。担当より2〜3営業日以内にご連絡します。</p>
    <form class="aform rv d2" onsubmit="return false">
      <div class="row">
        <div><label>店舗・会社名<i>必須</i></label><input placeholder="例）さくら整骨院"></div>
        <div><label>ご担当者名<i>必須</i></label><input placeholder="例）山田 太郎"></div>
        <div><label>メールアドレス<i>必須</i></label><input placeholder="you@example.com"></div>
        <div><label>電話番号</label><input placeholder="任意"></div>
        <div><label>業種</label><select><option>整骨院・整体</option><option>スポーツ用品店</option><option>学習塾・習い事</option><option>飲食・栄養</option><option>クリニック・薬局</option><option>その他</option></select></div>
        <div><label>ご希望</label><select><option>未定・相談したい</option><option>企業紹介プラン（¥50,000/年・制作＋掲載込み）</option><option>記事掲載（スポット・要相談）</option><option>現地取材・撮影も相談したい</option></select></div>
      </div>
      <label>ご質問・ご要望</label><textarea placeholder="掲載したい地域、お店の特徴、気になることなど"></textarea>
      <button class="send" type="submit">この内容で送信する</button>
      <div class="pv">送信によりプライバシーポリシーに同意したものとみなします。</div>
      <div class="re"><span><b>2–3</b>DAYS REPLY</span><span><b>0</b>SETUP FEE</span><span><b>30</b>MIN ONLINE</span></div>
    </form>
    <div class="trust rv">
      <div data-n="01">いま探している人に出る<small>クラブを選んでいる最中の画面に出ます。見学や体験を決める前のタイミングです</small></div>
      <div data-n="02">広告に見えない記事<small>「取材」の形なので、最後まで読まれます</small></div>
      <div data-n="03">地域の外には出ない<small>登録地域に合わせて表示。ムダ打ちがありません</small></div>
    </div>
  </section>

  <div class="svcta"><div class="big">LOCAL AD</div><div class="in"><div class="ey">LOCAL PARTNERS</div><h2>その地域の子育て世帯に、<br>お店をまるごと届ける。</h2><p>年¥50,000（税抜）。取材・記事制作・1年間の掲載込み。まず相談だけでも。</p><div class="row"><a class="b1" href="#apply">掲載を申し込む</a><a class="b2" href="pr-sample.html" target="_blank">見本の記事を見る</a></div></div></div>
  <div class="svnav"><a href="service-listing-preview.html">01 クラブを載せる</a><a href="#">02 撮影・動画制作</a><a href="service-sns-preview.html">03 SNS運用サポート</a><a href="#">04 ホームページ制作</a><span class="cur">05 地域の広告掲載</span></div>
  <div style="height:40px"></div>
</div>
<div class="sbar" id="sbar"><div class="t">地域の広告掲載<small>年¥50,000・制作費込み・2〜3営業日で連絡</small></div><a class="go" href="#apply">申し込む</a></div>
</main>
'''
ad_js='''<script>
(function(){
 var ah=document.querySelector('.adhero'),bsw=document.getElementById('bgsw');
 var bm=location.search.match(/bg=(none|grid|dots|type|map)/);
 if(bm&&ah)ah.dataset.bg=bm[1];
 if(bsw&&ah){
   function setBg(k){ah.dataset.bg=k;bsw.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.b===k)})}
   setBg(ah.dataset.bg);
   bsw.addEventListener('click',function(e){var b=e.target.closest('button');if(b)setBg(b.dataset.b)});
 }
 if(/noanim=1/.test(location.search)){
   var st=document.createElement('style');
   st.textContent='*{transition:none!important;animation:none!important}.adhero h1 span,.ty3 span,.bg-grid .pin{opacity:1!important;transform:none!important}.bg-grid .pin{transform:rotate(-45deg)!important}';
   document.head.appendChild(st);
   document.querySelectorAll('.rv,[data-tl],[data-app],.flow4').forEach(function(el){el.classList.add('in')});
   document.querySelectorAll('[data-cnt]').forEach(function(b){b.textContent=b.dataset.cnt});
   return;
 }
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
 document.querySelectorAll('.rv,[data-tl],[data-app],.flow4').forEach(function(el){io.observe(el)});
 document.querySelectorAll('[data-cnt]').forEach(function(b){var to=+b.dataset.cnt,t0=null;function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/900);b.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)}setTimeout(function(){requestAnimationFrame(f)},400)});
 var sb=document.getElementById('sbar');
 if(sb&&ah)new IntersectionObserver(function(e){sb.classList.toggle('on',!e[0].isIntersecting&&e[0].boundingClientRect.top<0)},{threshold:0}).observe(ah);
})();
</script>'''
page('service-ads-preview.html','地域の広告掲載｜チビスポ（サービス05・プレビュー）',ad_body,ad_css,extra_js=ad_js)
