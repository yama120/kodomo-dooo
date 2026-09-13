# ---- サービス03：SNS運用サポート（LP）。svc_ads.py の後に exec（ad_css を継承）
sns_css=ad_css+r'''
/* ===== SNS LP 固有 ===== */
.snshero{position:relative;background:var(--accent);color:#fff;overflow:hidden}
body[data-skin="stadium"] .snshero{background:#b8261a}
.snshero .in{position:relative;max-width:1200px;margin:0 auto;padding:44px 20px 40px;display:grid;grid-template-columns:1fr;gap:30px;align-items:center}
.snshero .ty4{position:absolute;right:-8px;top:-14px;font-family:'Anton',sans-serif;font-size:clamp(120px,24vw,320px);line-height:.84;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.28);pointer-events:none}
.snshero .cp{position:relative;z-index:1}
.snshero .ey{display:flex;align-items:center;gap:10px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:#fff;margin-bottom:12px}
.snshero .ey::before{content:"";width:22px;height:2px;background:#fff}
.snshero h1{font-family:var(--fh);margin:0 0 14px;font-size:clamp(30px,7.6vw,58px);font-weight:900;line-height:1.15;letter-spacing:-.015em;color:#fff}
.snshero h1 em{font-style:normal;color:#111;background:#fff;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.snshero h1 span{display:inline-block;opacity:0;transform:translateY(18px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.snshero h1 span:nth-child(2){animation-delay:.12s}.snshero h1 span:nth-child(3){animation-delay:.24s}
.snshero .ld{font-size:14px;font-weight:700;color:rgba(255,255,255,.88);line-height:1.9;max-width:540px;margin:0 0 18px}
.snshero .price-tag{display:inline-flex;align-items:baseline;flex-wrap:wrap;gap:8px;margin:0 0 18px;padding:10px 14px;border:1px solid rgba(255,255,255,.7);font-family:'Anton',sans-serif;letter-spacing:.06em;background:rgba(0,0,0,.14)}
.snshero .price-tag b{font-size:30px;font-weight:400;color:#fff}
.snshero .price-tag small{font-family:var(--f);font-size:11px;font-weight:700;color:rgba(255,255,255,.8);letter-spacing:0}
.snshero .price-tag em{font-style:normal;color:#fff;font-size:11px;letter-spacing:.2em;border-left:1px solid rgba(255,255,255,.5);padding-left:10px}
.snshero .cta{display:flex;gap:10px;flex-wrap:wrap}
.snshero .b1{background:#111;color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 28px;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.snshero .b2{border:1.5px solid #fff;color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 24px}
.snshero .stats{display:flex;gap:18px 30px;flex-wrap:wrap;margin-top:24px;padding-top:16px;border-top:1px solid rgba(255,255,255,.4)}
.snshero .stats div{font-family:'Anton',sans-serif;letter-spacing:.06em}
.snshero .stats b{display:block;font-size:30px;font-weight:400;line-height:1;color:#fff}
.snshero .stats small{font-size:10.5px;letter-spacing:.22em;color:rgba(255,255,255,.75)}
/* ヒーロー右：投稿（3ツリー）のモック＋1週間 */
.pv{position:relative;z-index:1;width:100%;max-width:520px;justify-self:center;display:grid;gap:14px}
.week{background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.35);padding:12px 14px;display:grid;gap:8px}
.week .wl{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.22em;color:rgba(255,255,255,.8)}
.week .wd{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.week .wd span{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.35);font-size:10px;font-weight:900;color:rgba(255,255,255,.8);gap:2px}
.week .wd span.on{background:#fff;color:#111}
.week .wd span.on em{font-style:normal;font-size:8px;color:var(--accent);letter-spacing:.06em;font-family:'Anton',sans-serif}
/* ---- 視覚版：ヒーロー右（理想のプロフィール画面） ---- */
.hp{position:relative;z-index:1;width:100%;max-width:520px;justify-self:center}
/* Instagram プロフィール画面（再現度優先） */
.ig{width:280px;margin:0 auto;background:#fff;color:#000;border:8px solid #1b1d21;border-radius:34px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.35);font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Hiragino Sans","Noto Sans JP",sans-serif;font-weight:400;letter-spacing:0;line-height:1.3;text-align:left}
.ig .ig-sb{display:flex;justify-content:space-between;align-items:center;padding:8px 18px 2px;font-size:11px;font-weight:700}
.ig .ig-sb svg{width:40px;height:12px;stroke:none}
.ig .ig-top{display:flex;align-items:center;justify-content:space-between;padding:6px 14px 8px}
.ig .ig-top b{font-size:15px;font-weight:700;display:flex;align-items:center;gap:4px}
.ig .ig-top b::after{content:"";width:6px;height:6px;border-right:1.6px solid #000;border-bottom:1.6px solid #000;transform:rotate(45deg);margin-top:-3px}
.ig .ig-top .ig-ic2{display:flex;gap:14px}
.ig svg{width:22px;height:22px;stroke:#000;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;display:block}
.ig .ig-head{display:flex;align-items:center;gap:16px;padding:2px 14px 8px}
.ig .ig-av{width:74px;height:74px;border-radius:50%;padding:2px;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7);flex:none}
.ig .ig-av span{display:block;width:100%;height:100%;border-radius:50%;border:2px solid #fff;overflow:hidden;background:#dbdbdb}
.ig .ig-av img{width:100%;height:100%;object-fit:cover;display:block}
.ig.gray .ig-av{background:#dbdbdb}
.ig .ig-cnt{display:flex;flex:1;justify-content:space-around;text-align:center}
.ig .ig-cnt b{display:block;font-size:15px;font-weight:700}
.ig .ig-cnt small{font-size:10.5px;color:#000}
.ig .ig-bio{padding:0 14px;font-size:11.5px;line-height:1.45}
.ig .ig-bio b{display:block;font-size:12px;font-weight:700}
.ig .ig-bio .ig-cat{color:#737373;display:block;margin-bottom:1px}
.ig .ig-bio .ig-lk{color:#00376b;font-weight:600;display:flex;align-items:center;gap:4px;margin-top:2px}
.ig .ig-bio .ig-lk svg{width:12px;height:12px;stroke:#00376b}
.ig .ig-btns{display:flex;gap:6px;padding:10px 14px 8px}
.ig .ig-btns span{flex:1;text-align:center;font-size:11.5px;font-weight:600;padding:7px 0;border-radius:8px;background:#efefef;color:#000}
.ig .ig-btns span.ig-pri{background:#0095f6;color:#fff}
.ig .ig-btns span.ig-sq{flex:0 0 32px;display:flex;align-items:center;justify-content:center}
.ig .ig-btns span.ig-sq svg{width:15px;height:15px}
.ig .ig-hl{display:flex;gap:12px;padding:4px 14px 10px;overflow:hidden}
.ig .ig-hl div{text-align:center;font-size:9.5px;flex:none;width:52px}
.ig .ig-hl i{display:block;width:52px;height:52px;border-radius:50%;border:1.5px solid #dbdbdb;padding:2px;margin:0 auto 3px;overflow:hidden;background:#fff}
.ig .ig-hl i img{width:100%;height:100%;object-fit:cover;border-radius:50%;display:block}
.ig .ig-hl i.ig-plus{display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:300;color:#000;font-style:normal;line-height:1}
.ig .ig-tabs{display:flex;border-top:1px solid #dbdbdb}
.ig .ig-tabs span{flex:1;display:flex;justify-content:center;padding:9px 0 8px;border-bottom:1.5px solid transparent}
.ig .ig-tabs span.ig-on{border-bottom-color:#000}
.ig .ig-tabs span:not(.ig-on) svg{stroke:#8e8e8e}
.ig .ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5px;background:#fff}
.ig .ig-grid img,.ig .ig-grid i{aspect-ratio:1;width:100%;object-fit:cover;object-position:top;display:block;background:#efefef}
.ig .ig-grid .ig-rl{position:relative}
.ig .ig-grid .ig-rl::after{content:"";position:absolute;right:5px;top:5px;width:0;height:0;border-left:9px solid #fff;border-top:5px solid transparent;border-bottom:5px solid transparent;filter:drop-shadow(0 1px 2px rgba(0,0,0,.5))}
.ig.gray .ig-grid img{filter:grayscale(1);opacity:.75}
.ig .ig-nav{display:flex;justify-content:space-around;align-items:center;padding:9px 6px 12px;border-top:1px solid #dbdbdb;background:#fff}
.ig .ig-nav .ig-me{width:22px;height:22px;border-radius:50%;overflow:hidden;border:1.5px solid #000}
.ig .ig-nav .ig-me img{width:100%;height:100%;object-fit:cover;display:block}
/* Instagram フィード投稿 */
.igpost{background:#fff;color:#000;width:250px;border-radius:12px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Hiragino Sans","Noto Sans JP",sans-serif;font-weight:400;letter-spacing:0;line-height:1.35;text-align:left}
.igpost .ph{display:flex;align-items:center;gap:8px;padding:9px 10px}
.igpost .ph .a{width:28px;height:28px;border-radius:50%;padding:1.5px;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7)}
.igpost .ph .a img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;border:1.5px solid #fff}
.igpost .ph b{font-size:12px;font-weight:600;flex:1}
.igpost .ph b small{display:block;font-size:10px;font-weight:400;color:#737373}
.igpost .ph .dots{font-size:14px;letter-spacing:1px}
.igpost .pic{aspect-ratio:1;background:#eee}
.igpost .pic img{width:100%;height:100%;object-fit:cover;display:block}
.igpost .act{display:flex;gap:12px;padding:8px 10px 4px}
.igpost .act svg{width:22px;height:22px;stroke:#000;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;display:block}
.igpost .act .bm{margin-left:auto}
.igpost .lk{padding:0 10px;font-size:12px;font-weight:600}
.igpost .cap{padding:3px 10px 0;font-size:11.5px;line-height:1.45}
.igpost .cap b{font-weight:600;margin-right:4px}
.igpost .cm{padding:3px 10px 10px;font-size:11px;color:#737373}
.igpost .cm span{display:block;font-size:10px;margin-top:2px}
.hp .igpost.float{position:absolute;right:-6px;bottom:40px;transform:rotate(3deg);box-shadow:0 26px 50px rgba(0,0,0,.4);animation:floaty 5s ease-in-out infinite}
/* フィードの帯 */
.feed{background:#111;color:#fff;padding:26px 0 30px;overflow:hidden}
.feed-h{max-width:1180px;margin:0 auto 14px;padding:0 20px;display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;font-size:12.5px;font-weight:700;color:rgba(255,255,255,.75)}
.feed-h .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.24em;color:var(--accent);padding-left:30px;background:linear-gradient(var(--accent),var(--accent)) 0 50%/20px 2px no-repeat}
.feed-row{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;padding:0 6px}
.fcell{position:relative;aspect-ratio:1;overflow:hidden}
.fcell img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s}.fcell img.tp{object-position:top}
.fcell:hover img{transform:scale(1.05)}
.fcell .lb{position:absolute;left:10px;bottom:10px;font-family:var(--fh);font-size:11.5px;font-weight:900;padding:5px 9px;color:#111}
.c1{background:#FFC83F}.c2{background:#5BD6A0}.c3{background:#6BAAEF;color:#fff!important}.c4{background:#FF7FB6}.c5{background:#fff}
/* 特徴カード（写真付き） */
.wcards{display:grid;grid-template-columns:1fr;gap:14px}
.wc{border:1px solid var(--ink);background:var(--card);overflow:hidden}
.wc .im{position:relative;aspect-ratio:16/9;overflow:hidden}
.wc .im img{width:100%;height:100%;object-fit:cover;display:block;object-position:top}
.wc .im .tag{position:absolute;left:12px;top:12px;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em;padding:5px 9px;color:#111}
.wc .im .ov-lb{position:absolute;right:12px;top:12px;font-family:var(--fh);font-size:10.5px;font-weight:900;padding:4px 8px;background:#FFC83F;color:#111}
.wc .im .ov-lb.b{top:38px;background:#5BD6A0}.wc .im .ov-lb.c{top:64px;background:#FF8FB1}
.wc .im .ov-crop{position:absolute;inset:14px 18px 20px 42%;border:1.5px dashed #fff;box-shadow:0 0 0 999px rgba(0,0,0,.35)}
.wc .im .ov-crop::before,.wc .im .ov-crop::after{content:"";position:absolute;width:10px;height:10px;border:2.5px solid #fff}
.wc .im .ov-crop::before{left:-2px;top:-2px;border-right:0;border-bottom:0}.wc .im .ov-crop::after{right:-2px;bottom:-2px;border-left:0;border-top:0}
.wc .im .ov-tool{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:center;gap:14px;padding:6px 0;background:rgba(0,0,0,.7)}
.wc .im .ov-tool i{width:14px;height:14px;border:1.5px solid #fff;border-radius:3px;opacity:.9}.wc .im .ov-tool i:nth-child(2){border-radius:50%}.wc .im .ov-tool i:nth-child(3){border-color:#FFC83F}
.wc .im .ov-ai{position:absolute;left:12px;right:12px;bottom:10px;background:#fff;color:#111;padding:8px 10px;border-radius:8px;box-shadow:0 6px 16px rgba(0,0,0,.3);display:block;text-align:left}
.wc .im .ov-ai .ah{display:flex;align-items:center;gap:6px;font-size:9.5px;font-weight:900;color:#666;margin-bottom:4px}
.wc .im .ov-ai .ah b{display:inline-flex;align-items:center;justify-content:center;width:22px;height:16px;border-radius:4px;background:#111;color:#fff;font-family:'Anton',sans-serif;font-size:9px;letter-spacing:.06em;padding:0;margin:0;line-height:1}
.wc .im .ov-ai .at{display:block;font-size:10.5px;font-weight:700;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wc .im .ov-ai em{display:block;font-style:normal;color:var(--accent);font-weight:900;font-size:10.5px;margin-top:3px}
.wc .im img.dim{filter:brightness(.72)}
.wc .im .ov-flow{position:absolute;left:12px;top:42px;white-space:nowrap;display:flex;align-items:center;gap:4px;font-size:9.5px;font-weight:900}
.wc .im .ov-flow i{font-style:normal;background:rgba(255,255,255,.92);color:#111;padding:3px 7px;border-radius:999px;position:relative}
.wc .im .ov-flow i+i{margin-left:10px}.wc .im .ov-flow i+i::before{content:"›";position:absolute;left:-11px;top:1px;color:#fff;font-size:12px}
.wc .im .ov-flow i.on{background:var(--accent);color:#fff}
.wc .im .ov-cp{position:absolute;left:12px;right:12px;bottom:10px;background:#fff;color:#111;padding:7px 96px 7px 40px;box-shadow:0 6px 16px rgba(0,0,0,.3);border:1px solid #111;min-height:40px;display:block;text-align:left}
.wc .im .ov-cp .cb{position:absolute;left:8px;top:50%;transform:translateY(-50%);width:24px;height:24px;border-radius:50%;background:#fff;border:2px solid var(--accent);color:var(--accent);font-family:var(--fh);font-weight:900;font-size:12px;display:flex;align-items:center;justify-content:center}
.wc .im .ov-cp b{display:block;font-family:var(--fh);font-size:11.5px;font-weight:900;padding:0;margin:0;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wc .im .ov-cp small{display:block;font-size:9px;color:#666;padding:0;margin:0;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wc .im .ov-cp em{position:absolute;right:7px;top:50%;transform:translateY(-50%);font-style:normal;background:var(--accent);color:#fff;font-size:9.5px;font-weight:900;padding:5px 8px;white-space:nowrap}
.wc b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;padding:14px 16px 4px;line-height:1.4}
.wc small{display:block;font-size:12px;font-weight:700;color:var(--sub);line-height:1.75;padding:0 16px 16px}
/* 渡すもの4つ（縮図付き） */
.sup2{display:grid;grid-template-columns:1fr;gap:14px}
.sup2 .s{border:1px solid var(--ink);background:var(--card);padding:0 0 16px;position:relative}
.sup2 .s .n{position:absolute;left:14px;top:14px;font-family:'Anton',sans-serif;font-size:14px;letter-spacing:.06em;color:#fff;background:var(--accent);padding:4px 8px;z-index:2}
.sup2 .s b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;padding:14px 16px 4px}
.sup2 .s small{display:block;font-size:12px;font-weight:700;color:var(--sub);line-height:1.75;padding:0 16px}
.vz{height:180px;background:var(--bg);border-bottom:1px solid var(--line);position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}
.mp2{width:200px;background:#fff;border:1px solid #ddd;padding:12px;position:relative}
.mp2 .row{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.mp2 .av{width:30px;height:30px;border-radius:50%;background:#e6e3dc;display:block}
.mp2 b{font-size:11px;display:block}.mp2 small{font-size:9px;color:#999}
.mp2 .ln{height:6px;background:#eee;margin:5px 0}.mp2 .ln.short{width:60%}
.mp2 .ck{position:absolute;font-size:9px;font-weight:900;color:#fff;background:var(--accent);padding:2px 6px;border-radius:999px}
.mp2 .k1{left:-8px;top:8px}.mp2 .k2{right:-10px;top:36px}.mp2 .k3{left:40%;bottom:-8px}
.tpl{width:210px;background:#fff;border:1px solid var(--ink);padding:12px;position:relative}
.tpl .tlab{font-family:'Anton',sans-serif;font-size:9px;letter-spacing:.2em;color:var(--accent);margin:4px 0 3px}
.tpl .tb{height:8px;background:#eee;margin-bottom:4px}.tpl .w70{width:70%}.tpl .w50{width:50%}
.tpl .stamp{position:absolute;right:-8px;top:-10px;background:#FFC83F;font-size:10px;font-weight:900;padding:4px 8px;transform:rotate(6deg)}
.fq{width:252px;background:#fff;border:1px solid #ddd;padding:10px 12px;font-size:9.5px}
.fq .fh{display:grid;grid-template-columns:82px 1fr 34px;gap:6px;color:#999;font-weight:700;font-size:8px;letter-spacing:.1em;padding-bottom:5px;border-bottom:1px solid #eee;margin-bottom:4px}
.fq .fr{display:grid;grid-template-columns:82px 1fr 34px;gap:6px;align-items:center;padding:5px 0;border-bottom:1px solid #f3f1ec}
.fq .fr:last-child{border-bottom:0}
.sup2 .s .fq b{font-family:var(--f);font-size:9.5px;font-weight:900;display:flex;align-items:center;gap:5px;color:#111;padding:0;white-space:nowrap}
.fq .fr i{width:10px;height:10px;border-radius:3px;display:inline-block}
.fq .k1{background:#FF8FB1}.fq .k2{background:#FFC83F}.fq .k3{background:#5BD6A0}.fq .k4{background:#6BAAEF}
.fq .fr span{color:#666;font-weight:700;line-height:1.3}
.sup2 .s .fq em{font-style:normal;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.04em;color:var(--accent);text-align:right;white-space:nowrap}
.cal{width:220px;background:#fff;border:1px solid #ddd;padding:10px}
.cal .ch{font-family:var(--fh);font-size:12px;font-weight:900;margin-bottom:6px}
.cal .cg{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
.cal .cg span{font-size:8px;text-align:center;color:#999;font-weight:700}
.cal .cg i{aspect-ratio:1;background:#f3f1ec;display:block;position:relative;font-style:normal}
.cal .cg i.d::after{content:"";position:absolute;left:50%;top:50%;width:7px;height:7px;border-radius:50%;background:var(--accent);transform:translate(-50%,-50%)}
.cal .cg i.ev{background:#FFC83F;font-size:7px;font-weight:900;display:flex;align-items:center;justify-content:center;color:#111}
.cal .cg i.ev::after{display:none}
.three{display:flex;gap:8px}
.three .p3{position:relative;width:64px;aspect-ratio:3/4;overflow:hidden;border:2px solid #fff;box-shadow:0 6px 16px rgba(0,0,0,.2)}
.three .p3:nth-child(2){transform:translateY(-8px)}
.three .p3 img{width:100%;height:100%;object-fit:cover;object-position:top}
.three .p3 span{position:absolute;left:4px;top:4px;background:var(--accent);color:#fff;font-family:'Anton',sans-serif;font-size:11px;padding:1px 6px}
/* Before / After */
.ba2{display:grid;grid-template-columns:1fr;gap:18px;align-items:start}
.ba2 .side{display:grid;gap:12px;justify-items:center}
.ba2 .cap{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.24em;color:var(--sub);border:1px solid var(--line);padding:5px 12px}
.ba2 .cap.on{color:#fff;background:var(--accent);border-color:var(--accent)}
.ba2 .ig{width:270px}
.ba2 .ig .ig-sb,.ba2 .ig .ig-nav,.ba2 .ig .ig-hl{display:none}
.ba2 ul{list-style:none;margin:0;padding:0;width:240px;border-top:1px solid var(--line)}
.ba2 li{padding:8px 0;border-bottom:1px solid var(--line);font-size:12.5px;font-weight:700;color:var(--sub);position:relative;padding-left:18px}
.ba2 li::before{content:"";position:absolute;left:2px;top:14px;width:6px;height:6px;background:var(--line);border-radius:50%}
.ba2 ul.on li{color:var(--ink);font-weight:900}
.ba2 ul.on li::before{background:var(--accent)}
.ba2 .arrow{display:flex;align-items:center;justify-content:center;font-family:'Anton',sans-serif;font-size:40px;color:var(--accent);transform:rotate(90deg)}
/* 役割3つ（色面） */
.roles2{display:grid;grid-template-columns:1fr;gap:12px}
.roles2 .r{padding:20px 18px;color:#111;position:relative;border:1px solid var(--ink)}
.roles2 .r .ic{width:52px;height:52px;background:#111;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.roles2 .r .ic svg{width:26px;height:26px;fill:none;stroke:#fff;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.roles2 .r .tm{position:absolute;right:14px;top:14px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.16em;color:#111;opacity:.7}
.roles2 .r b{display:block;font-family:var(--fh);font-size:18px;font-weight:900;margin-bottom:6px}
.roles2 .r em{display:block;font-style:normal;font-family:var(--fh);font-size:12.5px;font-weight:900;line-height:1.5;margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid rgba(0,0,0,.18)}
.roles2 .r small{font-size:12.5px;font-weight:700;line-height:1.75;color:#222}
.roles-note{margin-top:16px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.8}.roles-note b{color:var(--ink)}
@media(min-width:760px){.roles2 .r:not(:last-child)::after{content:"";position:absolute;right:-16px;top:50%;width:0;height:0;border-left:10px solid var(--ink);border-top:8px solid transparent;border-bottom:8px solid transparent;transform:translateY(-50%);z-index:2}}
.roles2 .r.c3{color:#fff}.roles2 .r.c3 small,.roles2 .r.c3 .tm,.roles2 .r.c3 em{color:#fff}.roles2 .r.c3 em{border-color:rgba(255,255,255,.4)}
.roles2 .r.c3 .ic{background:#fff}.roles2 .r.c3 .ic svg{stroke:#111}
@media(min-width:760px){
  .hp .ig{margin:0}.hp .igpost.float{right:0;bottom:30px;width:236px}
  .wcards{grid-template-columns:repeat(4,1fr)}
  .sup2{grid-template-columns:repeat(2,1fr);gap:20px}
  .ba2{grid-template-columns:1fr auto 1fr;gap:30px}
  .ba2 .arrow{transform:none;align-self:center}
  .one .l{display:flex;flex-direction:column;justify-content:center}
  .roles2{grid-template-columns:repeat(3,1fr);gap:20px}
}
@media(max-width:759px){.feed-row{grid-template-columns:repeat(3,1fr)}.hp .igpost.float{display:none}}
/* 理想の流れ（5ノード） */
.flow5{display:grid;grid-template-columns:1fr;gap:0}
.flow5 .nd{position:relative;border:1px solid var(--ink);padding:16px 16px 16px 60px;background:var(--card)}
.flow5 .nd+.nd{border-top:0}
.flow5 .nd .no{position:absolute;left:16px;top:16px;width:30px;height:30px;background:var(--ink);color:var(--bg);font-family:'Anton',sans-serif;font-size:12px;display:flex;align-items:center;justify-content:center}
.flow5 .nd.hot{background:var(--ink);color:var(--bg)}
.flow5 .nd.hot .no{background:var(--accent);color:#fff}
.flow5 .nd b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;margin-bottom:3px}
.flow5 .nd small{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7}
.flow5 .nd.hot small{color:color-mix(in srgb,var(--bg) 70%,transparent)}
.flow5 .nd .ic{display:none}
.flow5 .nd{opacity:0;transform:translateY(10px);transition:opacity .5s,transform .5s}
.flow5.in .nd{opacity:1;transform:none}
.flow5.in .nd:nth-child(2){transition-delay:.15s}.flow5.in .nd:nth-child(3){transition-delay:.3s}.flow5.in .nd:nth-child(4){transition-delay:.45s}.flow5.in .nd:nth-child(5){transition-delay:.6s}
/* 型：3ツリーの解説 */
.fmt{display:grid;grid-template-columns:1fr;gap:16px;align-items:start}
.fmt .post{box-shadow:8px 8px 0 var(--ink);border:1px solid var(--ink)}
.fmt ol{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
.fmt li{position:relative;padding:13px 0 13px 34px;border-bottom:1px solid var(--line);font-size:14px;font-weight:900}
.fmt li::before{content:attr(data-n);position:absolute;left:0;top:15px;font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.06em;color:var(--accent)}
.fmt li small{display:block;font-size:11.5px;font-weight:700;color:var(--sub);margin-top:2px;line-height:1.7}
/* 支援内容 4つ */
.sup{display:grid;grid-template-columns:1fr;border:1px solid var(--ink)}
.sup .s{display:grid;grid-template-columns:auto 1fr;gap:14px;padding:18px 18px;border-bottom:1px solid var(--ink);align-items:start}
.sup .s:last-child{border-bottom:0}
.sup .s .n{font-family:'Anton',sans-serif;font-size:24px;line-height:1;color:var(--accent);letter-spacing:.04em;padding-top:2px}
.sup .s b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:5px}
.sup .s small{font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
/* スポーツ特化 4つ */
.why4{display:grid;grid-template-columns:1fr;gap:0;border-top:2px solid var(--ink)}
.why4 .w{padding:18px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start}
.why4 .w svg{width:30px;height:30px;fill:none;stroke:var(--accent);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.why4 .w b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:5px;line-height:1.45}
.why4 .w small{font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
/* 変わること 3つ */
.res3{display:grid;grid-template-columns:1fr;gap:14px}
.res3 .r{border:1px solid var(--ink);padding:18px 18px 16px;background:var(--card)}
.res3 .r .k{font-family:'Anton',sans-serif;font-size:10px;letter-spacing:.22em;color:var(--sub);margin-bottom:10px}
.res3 .ba{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.res3 .bf{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.5;text-decoration:line-through;text-decoration-color:var(--line)}
.res3 .ar{font-family:'Anton',sans-serif;color:var(--accent);font-size:16px}
.res3 .af{font-size:12px;font-weight:900;color:var(--ink);line-height:1.5}
.res3 .r b{display:block;font-family:var(--fh);font-size:17px;font-weight:900;margin-bottom:5px}
.res3 .r small{font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.disc{margin-top:14px;font-size:11px;font-weight:700;color:var(--sub);line-height:1.8}
/* ネタの型5つ */
.types{display:grid;grid-template-columns:1fr;border:1px solid var(--ink)}
.types .t{padding:16px 16px;border-bottom:1px solid var(--ink);display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start}
.types .t:last-child{border-bottom:0}
.types .t .n{font-family:'Anton',sans-serif;font-size:22px;line-height:1;color:var(--accent);letter-spacing:.04em;padding-top:2px}
.types .t b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;margin-bottom:4px}
.types .t small{font-size:11.5px;font-weight:700;color:var(--sub);line-height:1.7}
.types .t q{display:block;margin-top:8px;font-size:12px;font-weight:700;color:var(--ink);border-left:2px solid var(--accent);padding-left:10px;quotes:none;line-height:1.7}
/* 役割分担 */
.roles{display:grid;grid-template-columns:1fr;gap:12px}
.roles .r{border:1px solid var(--ink);padding:16px;background:var(--card);position:relative}
.roles .r .k{font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.22em;color:var(--accent);margin-bottom:6px}
.roles .r b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:6px}
.roles .r small{font-size:12px;font-weight:700;color:var(--sub);line-height:1.75}
.roles .r .tm{position:absolute;right:14px;top:14px;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.16em;color:var(--sub)}
@media(min-width:760px){
  .snshero .in{grid-template-columns:1.05fr 1fr;gap:48px;padding:60px 20px 52px}
  .flow5{grid-template-columns:repeat(5,1fr)}
  .flow5 .nd+.nd{border-top:1px solid var(--ink);border-left:0}
  .flow5 .nd{padding:56px 16px 20px 16px}
  .flow5 .nd .no{left:16px;top:16px}
  .fmt{grid-template-columns:1fr 1.1fr;gap:40px}
  .sup{grid-template-columns:1fr 1fr}
  .sup .s:nth-child(1),.sup .s:nth-child(2){border-bottom:1px solid var(--ink)}
  .sup .s:nth-child(odd){border-right:1px solid var(--ink)}
  .sup .s:nth-child(3),.sup .s:nth-child(4){border-bottom:0}
  .why4{grid-template-columns:1fr 1fr;gap:0 40px}
  .res3{grid-template-columns:repeat(3,1fr);gap:20px}
  .types{grid-template-columns:repeat(5,1fr)}
  .types .t{border-bottom:0;border-right:1px solid var(--ink);grid-template-columns:1fr;gap:6px;padding:18px 16px}
  .types .t:last-child{border-right:0}
  .roles{grid-template-columns:repeat(3,1fr)}
}
'''
sns_body='''
<main><div class="wrap">
  <div class="note">【サービス03：SNS運用サポート（LP・視覚版）】ユーザー「文字ばかりで印象に残らない。SNSのページなので色と画像を」→ 写真と色を主役に再構成：①赤のヒーロー＝<b>理想のプロフィール画面のスマホ</b>（3×3のフィード・プロフィール文・クラブページへのリンク）に投稿カードを重ねる ②<b>フィードの帯</b>（全幅・写真6枚にラベル）③スポーツ特化4つ＝<b>写真付きカード</b> ④渡すもの4つ＝<b>縮図</b>（診断の赤丸／型のカード／カレンダー／3本）⑤変わること＝<b>Before/Afterの2台のスマホ</b> ⑥役割3つ＝色面＋アイコン。文章は各ブロック1〜2行に圧縮。ノウハウの中身は出さない（前回の方針を維持）。プラン以降は前回のまま。</div>
</div>
<section class="snshero">
  <div class="ty4" aria-hidden="true">SNS</div>
  <div class="in">
    <div class="cp">
      <div class="ey">FOR CLUBS ・ SERVICE 03 ・ SPORTS ONLY</div>
      <h1><span>SNSは、</span><span><em>見学</em>につながる</span><span>形で。</span></h1>
      <p class="ld">子どものスポーツクラブだけを見てきた立場で、そのクラブに合う発信の形を作ります。撮影の依頼も、特別な機材もいりません。コーチのスマホで足ります。</p>
      <div class="price-tag"><b>¥40,000</b><small>（税抜）・買い切り／月額なし</small><em>ONE-TIME</em></div>
      <div class="cta"><a class="b1" href="#apply">相談する</a><a class="b2" href="#changes">何が変わるか見る</a></div>
      <div class="stats"><div><b data-cnt="3">0</b><small>POSTS / WEEK</small></div><div><b data-cnt="2">0</b><small>WEEKS TO START</small></div><div><b data-cnt="0">0</b><small>MONTHLY FEE</small></div></div>
    </div>
    <div class="hp">
      <div class="ig"><div class="ig-sb"><span>9:41</span><svg viewBox="0 0 40 12"><rect x="0" y="7" width="3" height="5" rx=".6" fill="#000" stroke="none"/><rect x="4" y="5" width="3" height="7" rx=".6" fill="#000" stroke="none"/><rect x="8" y="3" width="3" height="9" rx=".6" fill="#000" stroke="none"/><rect x="12" y="1" width="3" height="11" rx=".6" fill="#000" stroke="none"/><rect x="21" y="1.5" width="16" height="9" rx="2.5" stroke="#000" stroke-width="1"/><rect x="22.5" y="3" width="11" height="6" rx="1.2" fill="#000" stroke="none"/><rect x="37.8" y="4" width="1.6" height="4" rx=".8" fill="#000" stroke="none"/></svg></div><div class="ig-top"><b>wakaba_fc</b><span class="ig-ic2"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span></div><div class="ig-head"><div class="ig-av"><span><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></span></div><div class="ig-cnt"><div><b>84</b><small>投稿</small></div><div><b>312</b><small>フォロワー</small></div><div><b>18</b><small>フォロー中</small></div></div></div><div class="ig-bio"><b>わかばFC</b><span class="ig-cat">スポーツクラブ</span>はじめてボールを触る子が半分🌱<br>学年ごとにコースを分けています<br>土曜の見学はいつでも👇<span class="ig-lk"><svg viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5"/></svg>chibispo.com/club/wakaba</span></div><div class="ig-btns"><span class="ig-pri">フォロー</span><span>メッセージ</span><span class="ig-sq"><svg viewBox="0 0 24 24"><circle cx="10" cy="8" r="4"/><path d="M3 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5M19 8v6M16 11h6"/></svg></span></div><div class="ig-hl"><div><i><img src="assets/preview-video/jp-soccer-dribble.jpg" alt=""></i>練習</div><div><i><img src="assets/preview-video/post-trial.jpg" alt=""></i>体験会</div><div><i><img src="assets/preview-video/post-coach.jpg" alt=""></i>コーチ</div><div><i><img src="assets/preview-video/post-parents.jpg" alt=""></i>保護者の声</div></div><div class="ig-tabs"><span class="ig-on"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="10" r="3"/><path d="M6.5 18c1.2-2.4 3.2-3.5 5.5-3.5s4.3 1.1 5.5 3.5"/></svg></span></div><div class="ig-grid"><img src="assets/preview-video/jp-soccer-shoot.jpg" alt=""><img src="assets/preview-video/post-coach.jpg" alt=""><img src="assets/preview-video/post-trial.jpg" alt=""><img src="assets/preview-video/jp-soccer-keep.jpg" alt=""><img src="assets/preview-video/post-parents.jpg" alt=""><img src="assets/preview-video/post-news.jpg" alt=""></div><div class="ig-nav"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8v10h-6v-6H9v6H3z"/></svg><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg><span class="ig-me"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></span></div></div>
      <div class="igpost float"><div class="ph"><span class="a"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></span><b>wakaba_fc<small>世田谷区・砧公園</small></b><span class="dots">•••</span></div><div class="pic"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></div><div class="act"><svg viewBox="0 0 24 24"><path d="M12 20.5s-8-4.9-8-11A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5c0 6.1-8 11-8 11z"/></svg><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 0 1-13.4 7.8L3 21l1.2-4.6A9 9 0 1 1 21 12z"/></svg><svg viewBox="0 0 24 24"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg><span class="bm"><svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg></span></div><div class="lk">いいね！24件</div><div class="cap"><b>wakaba_fc</b>今日は1年生だけの練習でした。はじめてボールを触る子、うちには半分います。土曜の午前は見学だけでも大丈夫です。日程はプロフィールから。</div><div class="cm">コメント6件をすべて見る<span>2時間前</span></div></div>
    </div>
  </div>
</section>

<section class="feed">
  <div class="feed-h"><span class="k">POST TYPES</span><span>投稿は、そのクラブに合った種別で組みます。写真はコーチのスマホで撮ったもので足ります。</span></div>
  <div class="feed-row">
    <div class="fcell"><img src="assets/preview-video/jp-soccer-dribble.jpg" alt=""><span class="lb c1">練習の日</span></div>
    <div class="fcell"><img src="assets/preview-video/post-trial.jpg" alt="" class="tp"><span class="lb c2">体験会</span></div>
    <div class="fcell"><img src="assets/preview-video/post-coach.jpg" alt="" class="tp"><span class="lb c3">コーチ紹介</span></div>
    <div class="fcell"><img src="assets/preview-video/post-parents.jpg" alt=""><span class="lb c4">保護者の声</span></div>
    <div class="fcell"><img src="assets/preview-video/jp-soccer-red.jpg" alt=""><span class="lb c1">試合の日</span></div>
    <div class="fcell"><img src="assets/preview-video/post-news.jpg" alt=""><span class="lb c5">お知らせ</span></div>
  </div>
</section>
<div class="wrap">

  <section class="sec2">
    <div class="ey rv">WHY SPORTS</div>
    <h2 class="rv d1">子どものスポーツクラブに<em>特化</em>した、SNSサポート。</h2>
    <p class="sub rv d2">一般のSNSコンサルと違うのは、この4つです。</p>
    <div class="wcards">
      <div class="wc rv"><div class="im"><img src="assets/preview-video/jp-soccer-keep.jpg" alt=""><span class="tag c1">POSTS</span><span class="ov-lb">練習の日</span><span class="ov-lb b">体験会</span><span class="ov-lb c">保護者の声</span></div><b>スポーツクラブならではの投稿</b><small>練習・体験会・試合・コーチ・保護者の声。入る前の保護者が知りたいことを、種別ごとの型にして渡します</small></div>
      <div class="wc rv d1"><div class="im"><img src="assets/preview-video/jp-soccer-red.jpg" alt=""><span class="tag c2">EDIT</span><span class="ov-crop"></span><span class="ov-tool"><i></i><i></i><i></i><i></i></span></div><b>写真・動画の編集を、スマホで教えます</b><small>コーチのスマホで撮った写真を、明るさ・切り抜き・文字入れ・15秒動画まで整える手順</small></div>
      <div class="wc rv d2"><div class="im"><img src="assets/preview-video/wm-kidsrun-1.jpg" alt=""><span class="tag c3">AI</span><span class="ov-ai"><span class="ah"><b>AI</b>クラブ専用プロンプト</span><span class="at">小1〜小3、はじめての子が半分、土曜に体験会…</span><em>投稿文を3案つくる ›</em></span></div><b>AIでできる、簡単な投稿編集</b><small>チビスポで実際に使っているプロンプトを、そのまま提供します。投稿文・返信・お知らせをAIに書かせる指示文です</small></div>
      <div class="wc rv d3"><div class="im"><img src="assets/preview-video/jp-soccer-run.jpg" alt="" class="dim"><span class="tag c4">CLUB PAGE</span><span class="ov-flow"><i>Instagram</i><i>クラブページ</i><i class="on">体験申込</i></span><span class="ov-cp"><span class="cb">わ</span><b>わかばFC</b><small>世田谷区・小1〜小6</small><em>体験を申し込む ›</em></span></div><b>申込の受け皿は、チビスポのクラブページ</b><small>投稿の行き先を、こちらで用意します。プロフィール → クラブページ → 体験申込まで1本でつながります</small></div>
    </div>
  </section>

  <section class="sec2 band">
    <div class="ey rv">SUPPORT</div>
    <h2 class="rv d1">渡すのは、この<em>4つ</em>。</h2>
    <p class="sub rv d2">何を書くか、いつ出すか、どこへつなぐか。クラブに合わせて決めたものを、そのまま使える形で。</p>
    <div class="sup2">
      <div class="s rv"><div class="vz v-diag"><div class="mp2"><div class="row"><i class="av"></i><div><b>club_name</b><small>プロフィール文が空欄</small></div></div><div class="ln"></div><div class="ln short"></div><span class="ck k1">写真</span><span class="ck k2">一言</span><span class="ck k3">リンク</span></div></div><div class="n">01</div><b>アカウント診断</b><small>いまのプロフィールと投稿を見て、直す順番をお伝えします</small></div>
      <div class="s rv d1"><div class="vz v-tpl"><div class="tpl"><div class="tlab">書き出し</div><div class="tb"></div><div class="tlab">本文</div><div class="tb"></div><div class="tb w70"></div><div class="tlab">締め</div><div class="tb w50"></div><span class="stamp">わかばFC用</span></div></div><div class="n">02</div><b>クラブ専用の投稿の型</b><small>そのクラブの強みに合わせた、書き出しから締めまでの型</small></div>
      <div class="s rv d2"><div class="vz v-cal"><div class="fq"><div class="fh"><span>形式</span><span>役割</span><span>頻度</span></div><div class="fr"><b><i class="k1"></i>リール</b><span>雰囲気を伝える</span><em>週1</em></div><div class="fr"><b><i class="k2"></i>ストーリーズ</b><span>練習の日の様子</span><em>週2〜3</em></div><div class="fr"><b><i class="k3"></i>カルーセル</b><span>体験会・募集の案内</span><em>月2</em></div><div class="fr"><b><i class="k4"></i>フィード</b><span>コーチ・保護者の声</span><em>週1</em></div></div></div><div class="n">03</div><b>リール・ストーリーズ・カルーセルの役割と頻度</b><small>どの形式で何を、どのくらい出すか。クラブに合わせて決めてお渡しします</small></div>
      <div class="s rv d3"><div class="vz v-three"><div class="three"><div class="p3"><img src="assets/preview-video/post-trial.jpg" alt=""><span>1</span></div><div class="p3"><img src="assets/preview-video/post-coach.jpg" alt=""><span>2</span></div><div class="p3"><img src="assets/preview-video/post-parents.jpg" alt=""><span>3</span></div></div></div><div class="n">04</div><b>最初の3本を、一緒に</b><small>オンラインで画面を見ながら書いて、出すところまで</small></div>
    </div>
    <div class="geo-note rv"><b>渡して終わりにしない</b><span>型・頻度表・テンプレートは<b>納品後クラブのもの</b>。担当が替わっても同じ型で続けられます。</span></div>
  </section>

  <section class="sec2" id="changes">
    <div class="ey rv">BEFORE / AFTER</div>
    <h2 class="rv d1">変わるのは、<em>画面</em>を見ればわかります。</h2>
    <p class="sub rv d2">フォロワー数は目標にしません。見るのは、見学と体験の申込です。</p>
    <div class="ba2">
      <div class="side rv"><div class="cap">BEFORE</div><div class="ig gray"><div class="ig-sb"><span>9:41</span><svg viewBox="0 0 40 12"><rect x="0" y="7" width="3" height="5" rx=".6" fill="#000" stroke="none"/><rect x="4" y="5" width="3" height="7" rx=".6" fill="#000" stroke="none"/><rect x="8" y="3" width="3" height="9" rx=".6" fill="#000" stroke="none"/><rect x="12" y="1" width="3" height="11" rx=".6" fill="#000" stroke="none"/><rect x="21" y="1.5" width="16" height="9" rx="2.5" stroke="#000" stroke-width="1"/><rect x="22.5" y="3" width="11" height="6" rx="1.2" fill="#000" stroke="none"/><rect x="37.8" y="4" width="1.6" height="4" rx=".8" fill="#000" stroke="none"/></svg></div><div class="ig-top"><b>club_name</b><span class="ig-ic2"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span></div><div class="ig-head"><div class="ig-av"><span></span></div><div class="ig-cnt"><div><b>7</b><small>投稿</small></div><div><b>41</b><small>フォロワー</small></div><div><b>3</b><small>フォロー中</small></div></div></div><div class="ig-bio"><span class="ig-cat">プロフィール文なし</span></div><div class="ig-btns"><span class="ig-pri">フォロー</span><span>メッセージ</span><span class="ig-sq"><svg viewBox="0 0 24 24"><circle cx="10" cy="8" r="4"/><path d="M3 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5M19 8v6M16 11h6"/></svg></span></div><div class="ig-tabs"><span class="ig-on"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="10" r="3"/><path d="M6.5 18c1.2-2.4 3.2-3.5 5.5-3.5s4.3 1.1 5.5 3.5"/></svg></span></div><div class="ig-grid"><img src="assets/preview-video/px-399187.jpg" alt=""><img src="assets/preview-video/px-3448250.jpg" alt=""><i></i><i></i><i></i><i></i></div><div class="ig-nav"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8v10h-6v-6H9v6H3z"/></svg><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg><span class="ig-me"></span></div></div>
        <ul><li>大会結果の報告だけ</li><li>思いついたときに投稿</li><li>リンク先がない</li></ul></div>
      <div class="arrow rv d1"><span>›</span></div>
      <div class="side rv d2"><div class="cap on">AFTER</div><div class="ig"><div class="ig-sb"><span>9:41</span><svg viewBox="0 0 40 12"><rect x="0" y="7" width="3" height="5" rx=".6" fill="#000" stroke="none"/><rect x="4" y="5" width="3" height="7" rx=".6" fill="#000" stroke="none"/><rect x="8" y="3" width="3" height="9" rx=".6" fill="#000" stroke="none"/><rect x="12" y="1" width="3" height="11" rx=".6" fill="#000" stroke="none"/><rect x="21" y="1.5" width="16" height="9" rx="2.5" stroke="#000" stroke-width="1"/><rect x="22.5" y="3" width="11" height="6" rx="1.2" fill="#000" stroke="none"/><rect x="37.8" y="4" width="1.6" height="4" rx=".8" fill="#000" stroke="none"/></svg></div><div class="ig-top"><b>wakaba_fc</b><span class="ig-ic2"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span></div><div class="ig-head"><div class="ig-av"><span><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></span></div><div class="ig-cnt"><div><b>84</b><small>投稿</small></div><div><b>312</b><small>フォロワー</small></div><div><b>18</b><small>フォロー中</small></div></div></div><div class="ig-bio"><b>わかばFC</b><span class="ig-cat">スポーツクラブ</span>はじめてボールを触る子が半分🌱 土曜の見学はいつでも👇<span class="ig-lk"><svg viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5"/></svg>chibispo.com/club/wakaba</span></div><div class="ig-btns"><span class="ig-pri">フォロー</span><span>メッセージ</span><span class="ig-sq"><svg viewBox="0 0 24 24"><circle cx="10" cy="8" r="4"/><path d="M3 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5M19 8v6M16 11h6"/></svg></span></div><div class="ig-tabs"><span class="ig-on"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg></span><span><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="10" r="3"/><path d="M6.5 18c1.2-2.4 3.2-3.5 5.5-3.5s4.3 1.1 5.5 3.5"/></svg></span></div><div class="ig-grid"><img src="assets/preview-video/jp-soccer-shoot.jpg" alt=""><img src="assets/preview-video/jp-soccer-dribble.jpg" alt=""><img src="assets/preview-video/post-trial.jpg" alt=""><img src="assets/preview-video/jp-soccer-keep.jpg" alt=""><img src="assets/preview-video/jp-soccer-duel.jpg" alt=""><img src="assets/preview-video/post-parents.jpg" alt=""></div><div class="ig-nav"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8v10h-6v-6H9v6H3z"/></svg><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M13 3l3 5.5"/><path d="M10.5 12.5v5l4-2.5z" fill="#8e8e8e" stroke="none"/></svg><span class="ig-me"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""></span></div></div>
        <ul class="on"><li>週3本・決まった曜日</li><li>入る前の保護者が知りたいこと</li><li>プロフィール → クラブページ → 体験申込</li></ul></div>
    </div>
    <div class="disc rv">効果には個人差があります。投稿の本数、地域、種目によって結果は変わります。数値の保証はしていません。</div>
  </section>

  <section class="sec2 band">
    <div class="ey rv">DECIDE FIRST</div>
    <h2 class="rv d1">何をやるかを、<em>先に</em>決める。</h2>
    <p class="sub rv d2">続かない理由は、投稿の形が決まっていないからです。撮る材料・書く内容・出す形を先に決めておくと、ネタ探しも文章も要らなくなります。</p>
    <div class="roles2">
      <div class="r rv c1"><div class="ic"><svg viewBox="0 0 24 24"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg></div><div class="tm">01 ・ SHOOT</div><b>撮る材料</b><em>何を撮るかが決まっているから、迷わない</em><small>練習の始めと終わり、体験会、試合。決めた場面をスマホで10枚。撮り方も一緒に決めます</small></div>
      <div class="r rv d1 c2"><div class="ic"><svg viewBox="0 0 24 24"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M13 7l3 3"/></svg></div><div class="tm">02 ・ WRITE</div><b>書く内容</b><em>撮る材料が決まっているから、書くことも決まる</em><small>写真を見て型に当てはめるだけ。文章が苦手でも、AIプロンプトで3案から選べます</small></div>
      <div class="r rv d2 c3"><div class="ic"><svg viewBox="0 0 24 24"><path d="M3 11l18-8-6 18-3-7z"/><path d="M12 14l9-11"/></svg></div><div class="tm">03 ・ POST</div><b>出す形</b><em>形式と曜日が決まっているから、続く</em><small>リール・ストーリーズ・カルーセルのどれで、いつ出すか。頻度表どおりに出すだけ。担当が替わっても同じ</small></div>
    </div>
    <div class="roles-note rv">材料が決まる → 内容が決まる → 形が決まる。<b>考える時間をゼロにするのが、このパックの中身です。</b></div>
  </section>

  <section class="sec2" id="plan">
    <div class="ey rv">PLAN</div>
    <h2 class="rv d1">型を渡したら、<em>あとは自分たち</em>で。</h2>
    <p class="sub rv d2">投稿を代わりにやるサービスではありません。買い切りの1回で、クラブが自分で回せる状態にして納品します。月額はかかりません。表示は税抜の目安。</p>
    <div class="one rv">
      <div class="l"><div class="n">SNS STARTER</div><h3>SNS立ち上げパック</h3><div class="pr">¥40,000<small>（税抜）</small></div><div class="per">買い切り・月額なし<small>納品まで2週間。最初の3本を一緒に出すところまでやります</small></div><a class="go" href="#apply">相談する</a><a class="go2" href="#apply">まず話だけ聞きたい</a></div>
      <div class="r"><div class="k">INCLUDED</div><ul>
        <li>アカウント診断と、クラブ専用の投稿の型<small>いまのプロフィール・投稿を見て、書き出しから締めまでの型と、話題の選び方をクラブに合わせて作ります</small></li>
        <li>形式ごとの役割と頻度<small>リール・ストーリーズ・カルーセル・フィードで何を、どのくらい出すか。体験会・大会に合わせて組み替え</small></li>
        <li>最初の3本を、一緒に書いて出す<small>写真の編集（明るさ・切り抜き・文字入れ・15秒動画）もここで。オンラインで画面を見ながら</small></li>
        <li>テンプレートと、チビスポで使っているAIプロンプト<small>投稿の下書き用シート、プロフィール文、返信の例、AIに投稿文を書かせる指示文。納品後はクラブのものです</small></li>
      </ul><div class="nt">写真はコーチのスマホで撮ったもので足ります。<b>撮影は含みません</b>。投稿そのものの代行やInstagramの画像制作は別途ご相談ください。<br>納品後も見てほしい方には、月1回30分の見守り（月¥5,000・いつでも終了）をご用意しています。</div></div>
    </div>
  </section>

  <section class="sec2">
    <div class="ey rv">FLOW</div>
    <h2 class="rv d1">納品まで、<em>2週間</em>。</h2>
    <p class="sub rv d2">最初の3本を出すところまでが、このパックの範囲です。</p>
    <div class="tl" data-tl><div class="lp-bar"><i></i></div>
      <div class="lp-st"><span class="dot">01</span><h3>相談</h3><p>下のフォームから。いまのSNSの状況と、困っていることを聞きます。</p><span class="t">ONLINE 30 MIN</span></div>
      <div class="lp-st"><span class="dot">02</span><h3>診断と型づくり</h3><p>プロフィールの直し方、クラブ専用の投稿の型、形式ごとの役割と頻度。</p><span class="t">1 WEEK</span></div>
      <div class="lp-st"><span class="dot">03</span><h3>最初の3本</h3><p>一緒に書いて、出します。ここで型が体に入ります。</p><span class="t">WEEK 2</span></div>
      <div class="lp-st"><span class="dot">04</span><h3>納品・自走へ</h3><p>型と頻度表とテンプレートをお渡しして完了。以降の費用はかかりません。</p><span class="t">DONE</span></div>
    </div>
  </section>

  <section class="sec2 band">
    <div class="ey rv">FAQ</div>
    <h2 class="rv d1">よくある質問</h2>
    <div class="faq rv d2">
      <details><summary>写真の撮影もしてもらえますか。</summary><div class="a">このパックに撮影は含みません。練習中にコーチのスマホで撮った写真で十分です。むしろ「その日の練習」が写っているほうが、保護者には届きます。撮影が必要な場合は別途ご相談ください。</div></details>
      <details><summary>Instagramだけ、Threadsだけでもいいですか。</summary><div class="a">どちらか1つで大丈夫です。保護者が多い地域ならInstagram、運営者や指導者とつながりたいならThreadsから始めます。</div></details>
      <details><summary>納品のあとはどうなりますか。</summary><div class="a">型・頻度表・テンプレートはクラブのものになります。以降の費用はかかりません。数字を見ながら一緒に直していきたい方には、月1回30分の見守り（月¥5,000・いつでも終了）もあります。</div></details>
      <details><summary>フォロワーがほとんどいません。</summary><div class="a">問題ありません。目的はフォロワー数ではなく、近所の保護者に届いて見学に来てもらうことです。最初は0でも、プロフィールとクラブページがつながっていれば申込は入ります。</div></details>
    </div>
  </section>

  <section class="sec2 apply-band" id="apply">
    <div class="ey rv">APPLY</div>
    <h2 class="rv d1">まず、<em>相談</em>から。</h2>
    <p class="sub rv d2">いまのアカウントを見て、何から直すかをお伝えします。2〜3営業日以内にご連絡します。</p>
    <form class="aform rv d2" onsubmit="return false">
      <div class="row">
        <div><label>クラブ名<i>必須</i></label><input placeholder="例）わかばFC"></div>
        <div><label>ご担当者名<i>必須</i></label><input placeholder="例）山田 太郎"></div>
        <div><label>メールアドレス<i>必須</i></label><input placeholder="you@example.com"></div>
        <div><label>SNSアカウント</label><input placeholder="@wakaba_fc（Instagram / Threads）"></div>
        <div><label>いまの状況</label><select><option>アカウントはあるが止まっている</option><option>週1本くらい出している</option><option>これから始める</option></select></div>
        <div><label>ご希望</label><select><option>まず相談したい</option><option>SNS立ち上げパック（¥40,000・買い切り）</option><option>投稿の代行も相談したい</option></select></div>
      </div>
      <label>困っていること</label><textarea placeholder="何を書けばいいか分からない、続かない、見学につながらない、など"></textarea>
      <button class="send" type="submit">この内容で送信する</button>
      <div class="pv2">送信によりプライバシーポリシーに同意したものとみなします。</div>
      <div class="re"><span><b>2–3</b>DAYS REPLY</span><span><b>2</b>WEEKS</span><span><b>0</b>MONTHLY FEE</span></div>
    </form>
    <div class="trust rv">
      <div data-n="01">代行ではなく、残る型<small>納品後はクラブのもの。月額もかかりません</small></div>
      <div data-n="02">クラブページとつながる<small>投稿→プロフィール→チビスポのクラブページ→体験申込。動線が1本になります</small></div>
      <div data-n="03">週30分で回る<small>撮る材料・書く内容・出す形を決めておけば、1週間の作業は30分で足ります</small></div>
    </div>
  </section>

  <div class="svcta"><div class="big">SNS</div><div class="in"><div class="ey">SNS SUPPORT</div><h2>投稿を、<br>見学につなげる形に。</h2><p>¥40,000（税抜）・買い切り。型と頻度表とテンプレートを渡して、クラブ自身が回せるように。</p><div class="row"><a class="b1" href="#apply">相談する</a><a class="b2" href="#flow">回し方を見る</a></div></div></div>
  <div class="svnav"><a href="service-listing-preview.html">01 クラブを載せる</a><a href="#">02 撮影・動画制作</a><span class="cur">03 SNS運用サポート</span><a href="#">04 ホームページ制作</a><a href="service-ads-preview.html">05 地域の広告掲載</a></div>
  <div style="height:40px"></div>
</div>
<div class="sbar" id="sbar"><div class="t">SNS立ち上げパック<small>¥40,000・買い切り・月額なし</small></div><a class="go" href="#apply">相談する</a></div>
</main>
'''
sns_js='''<script>
(function(){
 var hero=document.querySelector('.snshero');
 if(/noanim=1/.test(location.search)){
   var st=document.createElement('style');
   st.textContent='*{transition:none!important;animation:none!important}.snshero h1 span{opacity:1!important;transform:none!important}.flow5 .nd{opacity:1!important;transform:none!important}';
   document.head.appendChild(st);
   document.querySelectorAll('.rv,[data-tl],[data-app],.flow5').forEach(function(el){el.classList.add('in')});
   document.querySelectorAll('[data-cnt]').forEach(function(b){b.textContent=b.dataset.cnt});
   return;
 }
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
 document.querySelectorAll('.rv,[data-tl],[data-app],.flow5').forEach(function(el){io.observe(el)});
 document.querySelectorAll('[data-cnt]').forEach(function(b){var to=+b.dataset.cnt,t0=null;function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/900);b.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)}setTimeout(function(){requestAnimationFrame(f)},400)});
 var sb=document.getElementById('sbar');
 if(sb&&hero)new IntersectionObserver(function(e){sb.classList.toggle('on',!e[0].isIntersecting&&e[0].boundingClientRect.top<0)},{threshold:0}).observe(hero);
})();
</script>'''
# 申込フォームの注記クラスが .pv（ヒーロー右のモック）と衝突するので別名に
sns_css=sns_css.replace(".aform .pv{",".aform .pv2{")
page('service-sns-preview.html','SNS運用サポート｜チビスポ（サービス03・プレビュー）',sns_body,sns_css,extra_js=sns_js)
