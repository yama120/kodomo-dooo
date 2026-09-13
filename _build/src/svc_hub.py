# ---- 07：クラブ・事業者向け 総合LP（ハブ）。マガジン・SNS・CTAからの着地点。01〜05の各LPへ送る
HUB_NUM_CLUBS='136'   # 掲載クラブ数＝DBの approved 実数（2026-09-11時点・teams 141件中）。本番はDBから
HUB_NUM_PREF='24'     # 都道府県（clubs/ 配下の実数）
A='assets/preview-video/'

hub_css=sl_css+r'''
/* ===== HERO（総合） ===== */
.hub-hero{position:relative;background:#101215;color:#fff;overflow:hidden}
.hub-hero .bg{position:absolute;inset:0;background:url(assets/preview-video/jp-soccer-duel.jpg) center 30%/cover;opacity:.55;transform:scale(1.06);animation:heroZoom 14s ease-out forwards}
.hub-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(16,18,21,.94) 0%,rgba(16,18,21,.78) 48%,rgba(16,18,21,.25) 100%)}
.hub-hero .ty5{position:absolute;right:-10px;bottom:-30px;font-family:'Anton',sans-serif;font-size:clamp(110px,22vw,300px);line-height:.84;letter-spacing:-.01em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.16);pointer-events:none;z-index:1}
.hub-hero .in{position:relative;z-index:2;max-width:1200px;margin:0 auto;padding:54px 20px 44px;display:grid;grid-template-columns:1fr;gap:34px;align-items:center}
.hub-hero .ey{color:#fff}.hub-hero .ey::before{background:var(--accent)}
.hub-hero h1{font-family:var(--fh);margin:0 0 14px;font-size:clamp(30px,7.4vw,56px);font-weight:900;line-height:1.15;letter-spacing:-.015em}
.hub-hero h1 em{font-style:normal;color:#111;background:#fff;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.hub-hero h1 span{display:inline-block;opacity:0;transform:translateY(18px);animation:up .7s cubic-bezier(.2,.7,.2,1) forwards}
.hub-hero h1 span:nth-child(2){animation-delay:.12s}.hub-hero h1 span:nth-child(3){animation-delay:.24s}
.hub-hero .ld{font-size:14px;font-weight:700;color:rgba(255,255,255,.82);line-height:1.9;max-width:540px;margin:0 0 20px}
.hub-hero .cta{display:flex;gap:10px;flex-wrap:wrap}
.hub-hero .b1{background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:16px 28px;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.hub-hero .b2{border:1.5px solid rgba(255,255,255,.8);color:#fff;font-family:var(--fh);font-weight:900;font-size:15px;padding:15px 24px}
.hub-hero .stats{display:flex;gap:18px 30px;flex-wrap:wrap;margin-top:24px;padding-top:16px;border-top:1px solid rgba(255,255,255,.28)}
.hub-hero .stats div{font-family:'Anton',sans-serif;letter-spacing:.06em}
.hub-hero .stats b{display:block;font-size:30px;font-weight:400;line-height:1;color:#fff}
.hub-hero .stats b small{font-family:var(--f);font-size:12px;font-weight:900;margin-left:2px}
.hub-hero .stats span{font-size:10.5px;letter-spacing:.22em;color:rgba(255,255,255,.65)}
/* 目次カード（INDEX） */
.idx{width:100%;max-width:400px;justify-self:center;background:#fff;color:#111;border:1px solid #111;box-shadow:14px 14px 0 var(--accent);position:relative}
.idx .ih{display:flex;justify-content:space-between;align-items:baseline;padding:14px 18px 10px;border-bottom:2px solid #111}
.idx .ih b{font-family:'Anton',sans-serif;font-size:13px;letter-spacing:.28em}
.idx .ih small{font-size:10.5px;font-weight:900;color:var(--sub)}
.idx a{display:grid;grid-template-columns:34px 1fr auto;gap:10px;align-items:center;padding:12px 18px;border-bottom:1px solid #e6e3dc;opacity:0;transform:translateX(-8px);animation:idxIn .5s forwards;transition:background .15s}
.idx a:nth-child(2){animation-delay:.25s}.idx a:nth-child(3){animation-delay:.35s}.idx a:nth-child(4){animation-delay:.45s}.idx a:nth-child(5){animation-delay:.55s}.idx a:nth-child(6){animation-delay:.65s}
@keyframes idxIn{to{opacity:1;transform:none}}
.idx a:last-of-type{border-bottom:0}
.idx a:hover{background:#f6f4ef}
.idx a .n{font-family:'Anton',sans-serif;font-size:14px;color:var(--accent);letter-spacing:.06em}
.idx a b{display:block;font-family:var(--fh);font-size:14px;font-weight:900;line-height:1.3}
.idx a b small{display:block;font-size:10.5px;font-weight:700;color:var(--sub)}
.idx a .p{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.06em;color:#111;white-space:nowrap}
.idx a .p.free{color:var(--accent)}
.idx a .p.tba{font-family:var(--f);font-size:10px;font-weight:900;color:#fff;background:#111;padding:3px 7px;letter-spacing:.1em}
.idx .stamp{position:absolute;right:-12px;top:-14px;background:var(--accent);color:#fff;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.2em;padding:7px 11px;transform:rotate(6deg)}
/* ===== ABOUT：チビスポとは（3画面の流れ） ===== */
.about{display:grid;grid-template-columns:1fr;gap:14px}
.ab{border:1px solid var(--ink);background:var(--card);position:relative}
.ab .im{position:relative;aspect-ratio:4/3;overflow:hidden;background:#f2f0eb;border-bottom:1px solid var(--ink)}
.ab .im img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .6s}
.ab:hover .im img{transform:scale(1.03)}
.ab .tx b i{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;margin-right:8px;background:var(--ink);color:var(--bg);font-style:normal;font-family:'Anton',sans-serif;font-size:12px;vertical-align:2px}
/* 3画面を同じスマホで（探す→見る→申し込む） */
.ab .im{background:#e9e6df;aspect-ratio:auto;height:280px}
.ab .im .m-ph{position:absolute;left:50%;top:18px;bottom:-30px;width:210px;margin-left:-105px;background:#fff;border:6px solid #1b1d21;border-bottom:0;border-radius:28px 28px 0 0;box-shadow:0 18px 40px rgba(0,0,0,.18);overflow:hidden;text-align:left;color:#111}
.ab .im .m-sc{position:absolute;inset:0;padding:12px 10px 0;overflow:hidden}
.ab .im .m-ph img{max-width:none}
.ab .im .m-bar{display:flex;justify-content:space-between;align-items:baseline;gap:6px;border-bottom:2px solid #111;padding-bottom:5px;margin-bottom:6px}
.ab .im .m-bar b{font-family:var(--fh);font-size:11px;font-weight:900;white-space:nowrap}
.ab .im .m-bar small{font-family:'Anton',sans-serif;font-size:10px;color:var(--sub)}
.ab .im .m-chips{display:flex;gap:3px;flex-wrap:nowrap;overflow:hidden;margin-bottom:7px}
.ab .im .m-chips span{flex:none;font-size:8.5px;font-weight:900;padding:3px 6px;border:1px solid #d9d5cc;white-space:nowrap}
.ab .im .m-chips span.on{background:#111;border-color:#111;color:#fff}
.ab .im .m-cc{display:grid;grid-template-columns:52px 1fr;gap:7px;align-items:center;padding:5px;border:1px solid #e3dfd6;margin-bottom:5px;background:#fff}
.ab .im .m-cc.hot{border:2px solid var(--accent);box-shadow:0 6px 14px rgba(0,0,0,.12)}
.ab .im .m-cc img{width:52px;height:44px;object-fit:cover;display:block}
.ab .im .m-ci{min-width:0}
.ab .im .m-ci b{display:block;font-family:var(--fh);font-size:10.5px;font-weight:900;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ab .im .m-ci small{display:block;font-size:8px;font-weight:700;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ab .im .m-tg{display:flex;gap:3px;margin-top:3px;overflow:hidden}
.ab .im .m-tg i{flex:none;font-style:normal;font-size:7.5px;font-weight:900;padding:1px 4px;border:1px solid #111;white-space:nowrap}
.ab .im .m-sc>.m-hero{margin:-12px -10px 6px;height:64px;position:relative}
.ab .im .m-hero img{width:100%;height:100%;object-fit:cover;display:block}
.ab .im .m-hero span{position:absolute;right:6px;bottom:6px;background:var(--accent);color:#fff;font-size:8px;font-weight:900;padding:2px 5px}
.ab .im .m-nm b{display:block;font-family:var(--fh);font-size:13px;font-weight:900;line-height:1.2}
.ab .im .m-nm small{display:block;font-size:8px;font-weight:700;color:var(--sub);margin-bottom:5px}
.ab .im .m-sec{font-family:var(--fh);font-size:9px;font-weight:900;border-top:1px solid #e3dfd6;padding-top:5px;margin-bottom:4px}
.ab .im .m-sl{display:grid;grid-template-columns:auto 1fr auto;gap:5px;align-items:center;font-size:7.5px;font-weight:700;color:var(--sub);margin-bottom:5px}
.ab .im .m-sl i{position:relative;height:2px;background:#e3dfd6;display:block}
.ab .im .m-sl em{position:absolute;top:50%;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;background:var(--accent)}
.ab .im .m-tags{display:flex;flex-wrap:wrap;gap:3px;margin-bottom:6px}
.ab .im .m-tags span{font-size:8px;font-weight:900;padding:2px 5px;border:1px solid #111;white-space:nowrap}
.ab .im .m-tags span.on{border-color:var(--accent);color:var(--accent);box-shadow:0 0 0 1.5px color-mix(in srgb,var(--accent) 25%,transparent)}
.ab .im .m-co{display:grid;grid-template-columns:22px 1fr;gap:6px;align-items:center;background:#f4f2ed;padding:5px 6px;margin-bottom:6px}
.ab .im .m-co img{width:22px;height:22px;border-radius:50%;object-fit:cover;object-position:top;display:block}
.ab .im .m-co span{font-size:8px;font-weight:700;line-height:1.4}
.ab .im .m-btn{background:var(--accent);color:#fff;text-align:center;font-family:var(--fh);font-size:10px;font-weight:900;padding:7px 0}
.ab .im .m-fh{border-bottom:2px solid #111;padding:4px 0 6px;margin-bottom:4px}
.ab .im .m-fh small{display:block;font-size:8.5px;font-weight:900;color:var(--accent)}
.ab .im .m-fh b{display:block;font-family:var(--fh);font-size:13px;font-weight:900}
.ab .im .m-fr{display:flex;justify-content:space-between;gap:6px;font-size:9px;padding:6px 0;border-bottom:1px solid #eee}
.ab .im .m-fr span{color:var(--sub);font-weight:700;flex:none}.ab .im .m-fr b{font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ab .im .m-fr+.m-btn{margin-top:10px}
.ab .im .m-toast{position:absolute;left:8px;right:8px;top:192px;background:#111;color:#fff;display:flex;gap:7px;align-items:center;padding:8px 9px;border-radius:10px;box-shadow:0 10px 24px rgba(0,0,0,.35)}
.ab .im .m-toast i{flex:none;width:18px;height:18px;border-radius:50%;background:#5BD6A0;color:#111;font-style:normal;font-size:10px;font-weight:900;display:flex;align-items:center;justify-content:center}
.ab .im .m-toast b{display:block;font-size:9.5px;font-weight:900}
.ab .im .m-toast span{font-size:8px;font-weight:700;color:rgba(255,255,255,.7);line-height:1.35}
.ab .im .m-tap{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:rgba(232,69,95,.28);border:2px solid var(--accent);z-index:3}
.ab .im .m-tap::after{content:"";position:absolute;inset:-7px;border-radius:50%;border:2px solid var(--accent);opacity:0;animation:ping 2s ease-out infinite}
.ab .tx{padding:14px 16px 16px}
.ab .tx b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:4px}
.ab .tx small{display:block;font-size:12px;font-weight:700;color:var(--sub);line-height:1.75}
.ab .arr{display:none}
.about-note{margin-top:18px;padding:14px 16px;border-left:3px solid var(--accent);font-size:13px;font-weight:700;line-height:1.85;color:var(--sub)}
.about-note b{color:var(--ink)}
/* ===== 保護者が見る3つ（黒帯） ===== */
.look{margin:48px -20px 0;background:#101215;color:#fff;padding:36px 20px}
.look .in{max-width:1180px;margin:0 auto}
.look .ey{color:#fff}
.look h2{font-family:var(--fh);margin:0 0 6px;font-size:clamp(21px,5vw,30px);font-weight:900;line-height:1.3}
.look h2 em{font-style:normal;color:var(--accent)}
.look p.sub{margin:0 0 22px;font-size:13px;font-weight:700;color:rgba(255,255,255,.7);line-height:1.9}
.look3{display:grid;grid-template-columns:1fr;gap:12px}
.look3 div{position:relative;padding:16px 16px 16px 52px;border:1px solid rgba(255,255,255,.22)}
.look3 div::before{content:attr(data-n);position:absolute;left:16px;top:16px;font-family:'Anton',sans-serif;font-size:20px;color:var(--accent);line-height:1}
.look3 b{display:block;font-family:var(--fh);font-size:15px;font-weight:900;margin-bottom:4px}
.look3 small{font-size:12px;font-weight:700;color:rgba(255,255,255,.7);line-height:1.7}
/* ===== START HERE：質問形（E案・2026-09-12確定） ===== */
/* E 質問（フローチャート） */
.flow{display:grid;gap:0;max-width:820px}
.flow .frow{display:grid;grid-template-columns:1fr;gap:10px;align-items:stretch}
.flow .fq{position:relative;border:2px solid var(--ink);background:var(--card);padding:16px 16px 16px 60px;font-family:var(--fh);font-size:clamp(14px,3.4vw,17px);font-weight:900;line-height:1.4;display:flex;align-items:center;min-height:64px}
.flow .fk{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-family:'Anton',sans-serif;font-size:14px;color:var(--accent);letter-spacing:.06em}
.flow .frow.bz .fq{padding-left:16px;flex-direction:column;align-items:flex-start;gap:4px}
.flow .frow.bz .fk{position:static;transform:none;font-family:var(--f);font-size:10px;letter-spacing:.14em}
.flow .fbr{display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:center}
.flow .fno{font-size:11px;font-weight:900;color:var(--sub);white-space:nowrap;padding-left:8px;position:relative}
.flow .fno::after{content:"›";font-family:'Anton',sans-serif;color:var(--accent);font-size:16px;margin-left:6px}
.flow .fans{display:grid;grid-template-columns:auto 1fr;gap:0 10px;align-items:center;background:var(--ink);color:var(--bg);padding:12px 14px;transition:transform .2s}
.flow .fans:hover{transform:translateX(4px)}
.flow .fans i{font-style:normal;font-family:'Anton',sans-serif;font-size:20px;color:var(--accent);grid-row:span 2;line-height:1}
.flow .fans{font-family:var(--fh);font-size:14px;font-weight:900}
.flow .fans small{font-size:11px;font-weight:700;color:color-mix(in srgb,var(--bg) 70%,transparent)}
.flow .frow.bz .fans{background:var(--accent);color:#fff}.flow .frow.bz .fans i{color:#fff}.flow .frow.bz .fans small{color:rgba(255,255,255,.75)}
.flow .fyes{position:relative;height:38px;margin-left:30px;padding-left:16px;font-size:11px;font-weight:900;color:var(--sub);display:flex;align-items:center}
.flow .fyes::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--ink)}
.flow .fyes::after{content:"";position:absolute;left:-4px;bottom:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:7px solid var(--ink)}
.flow .fend{margin:14px 0 26px 30px;padding-left:16px;border-left:2px dashed var(--line);font-size:12px;font-weight:700;color:var(--sub);line-height:1.7}
@media(min-width:760px){
  .flow .frow{grid-template-columns:1fr 1fr;gap:18px}
  .flow .fbr{grid-template-columns:auto 1fr}
}
/* ===== SERVICES：特集型（交互） ===== */
.svc-list{display:grid;gap:26px}
.fs{position:relative;border:1px solid var(--ink);background:var(--card);display:grid;grid-template-columns:1fr}
.fs .vis{position:relative;min-height:230px;background:#f2f0eb;border-bottom:1px solid var(--ink);overflow:hidden;display:flex;align-items:center;justify-content:center}
.fs .bd{padding:20px 18px 20px;position:relative}
.fs .num{position:absolute;right:14px;top:6px;font-family:'Anton',sans-serif;font-size:64px;line-height:1;color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--ink) 25%,transparent);pointer-events:none}
.fs .k{display:flex;align-items:center;gap:8px;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent);margin-bottom:8px}
.fs .k i{font-style:normal;font-family:var(--f);font-size:9.5px;letter-spacing:.12em;padding:2px 7px;background:var(--ink);color:var(--bg)}
.fs .k i.free{background:var(--accent)}
.fs h3{font-family:var(--fh);margin:0 0 6px;font-size:clamp(20px,4.6vw,26px);font-weight:900;line-height:1.3;letter-spacing:-.01em}
.fs h3 em{font-style:normal;color:var(--accent)}
.fs .ld{margin:0 0 12px;font-size:13px;font-weight:700;color:var(--sub);line-height:1.85}
.fs ul{list-style:none;margin:0 0 14px;padding:12px 0 0;border-top:1px solid var(--line);display:grid;gap:6px}
.fs li{position:relative;padding-left:18px;font-size:12.5px;font-weight:700;line-height:1.6}
.fs li::before{content:"";position:absolute;left:0;top:8px;width:9px;height:5px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
.fs .who{font-size:11.5px;font-weight:700;color:var(--sub);margin-bottom:12px;padding:8px 10px;background:color-mix(in srgb,var(--ink) 5%,var(--bg))}
.fs .who b{color:var(--ink);margin-right:4px}
.fs .row{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;border-top:2px solid var(--ink);padding-top:12px}
.fs .pr{font-family:'Anton',sans-serif;font-size:24px;letter-spacing:.02em;line-height:1}
.fs .pr small{font-family:var(--f);font-size:11px;font-weight:700;color:var(--sub);letter-spacing:0;margin-left:5px}
.fs .pr.free{color:var(--accent)}
.fs .pr.jp{font-family:var(--fh);font-size:18px;font-weight:900}
.fs .go{display:inline-block;background:var(--ink);color:var(--bg);font-family:var(--fh);font-weight:900;font-size:13.5px;padding:12px 18px;transition:background .15s}
.fs .go:hover{background:var(--accent);color:#fff}
.fs.hot .go{background:var(--accent);color:#fff}
.fs.hot{border:2px solid var(--accent);box-shadow:10px 10px 0 var(--accent)}
.fs .pin{position:absolute;left:14px;top:-12px;z-index:3;background:var(--accent);color:#fff;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.18em;padding:5px 10px}
/* 01：スマホで流れるクラブページ */
.fs .pm{width:200px;aspect-ratio:9/17;transform:rotate(-3deg);margin:22px auto}
.fs .pm-scr img{animation-duration:11s}
.fs .pm-ntf{top:26px}
/* 02：動画（準備中） */
.fs .vid{position:absolute;inset:0}
.fs .vid img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(1.05)}
.fs .vid .play{position:absolute;left:50%;top:50%;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center}
.fs .vid .play::after{content:"";margin-left:5px;border-left:20px solid #111;border-top:12px solid transparent;border-bottom:12px solid transparent}
.fs .vid .len{position:absolute;right:12px;bottom:12px;background:#111;color:#fff;font-family:'Anton',sans-serif;font-size:11px;letter-spacing:.1em;padding:4px 8px}
.fs .soon{padding:22px 18px}
#s02 .vis{min-height:340px}
.fs .soon .t{font-size:18px}
/* 03：投稿2枚 */
.fs .posts{position:relative;width:250px;height:230px;margin:0 auto}
.fs .posts img{position:absolute;width:150px;aspect-ratio:4/5;object-fit:cover;object-position:top;border:3px solid #fff;box-shadow:0 14px 30px rgba(0,0,0,.25)}
.fs .posts .a{left:0;top:18px;transform:rotate(-6deg)}
.fs .posts .b{right:0;top:0;transform:rotate(5deg);z-index:2}
.fs .posts .c{left:50%;bottom:6px;width:140px;aspect-ratio:1;margin-left:-70px;transform:rotate(2deg);z-index:3}
.fs .posts .lb{position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);background:var(--accent);color:#fff;font-size:10.5px;font-weight:900;padding:4px 9px;z-index:4;white-space:nowrap}
/* 04：サイト3種を扇に */
.fs .sites{position:relative;width:100%;max-width:360px;height:230px;margin:0 auto}
.fs .sites img{position:absolute;width:220px;aspect-ratio:16/10;object-fit:cover;object-position:top;border:1px solid var(--ink);background:#fff;box-shadow:0 14px 30px rgba(0,0,0,.22);transition:transform .4s}
.fs .sites .s1{left:0;top:24px;transform:rotate(-5deg)}
.fs .sites .s2{left:50%;top:8px;margin-left:-110px;z-index:2}
.fs .sites .s3{right:0;top:36px;transform:rotate(5deg);z-index:1}
.fs:hover .sites .s1{transform:rotate(-8deg) translateX(-10px)}
.fs:hover .sites .s3{transform:rotate(8deg) translateX(10px)}
.fs .sites .lb{position:absolute;left:50%;bottom:0;transform:translateX(-50%);background:#fff;border:1px solid var(--ink);font-size:10.5px;font-weight:900;padding:4px 9px;z-index:4;white-space:nowrap}
/* 05：広告タイル＋地図 */
.fs .adv{position:absolute;inset:0;background:url(assets/preview-video/ad-hero-map.jpg) center/cover}
.fs .adv::before{content:"";position:absolute;inset:0;background:rgba(255,255,255,.55)}
.fs .adv .tiles{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:grid;grid-template-columns:1fr 1fr;gap:8px;width:250px}
.fs .adv .tile{background:#fff;border:1px solid var(--ink);padding:6px;box-shadow:0 10px 24px rgba(0,0,0,.18)}
.fs .adv .tile img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.fs .adv .tile b{display:block;font-size:10.5px;font-weight:900;margin-top:5px}
.fs .adv .tile small{display:block;font-size:9px;font-weight:700;color:var(--sub)}
.fs .adv .tile .ad{font-size:8px;letter-spacing:.14em;color:var(--sub);font-weight:900}
/* ===== FLOW 3 ===== */
.hf{display:grid;grid-template-columns:1fr;gap:14px}
.hf>div{position:relative;border-top:2px solid var(--ink);padding:14px 0 0 0}
.hf div .n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.2em;color:var(--accent);margin-bottom:6px}
.hf div b{display:block;font-family:var(--fh);font-size:16px;font-weight:900;margin-bottom:4px}
.hf div small{font-size:12.5px;font-weight:700;color:var(--sub);line-height:1.8}
.hf div em{display:block;margin-top:8px;font-style:normal;font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.18em;color:var(--accent)}
/* ===== 事業者向け帯 ===== */
.biz{margin-top:26px;border:1px solid var(--ink);background:var(--ink);color:var(--bg);padding:20px 18px;display:grid;gap:10px}
.biz .k{font-family:'Anton',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--accent)}
.biz b{font-family:var(--fh);font-size:18px;font-weight:900;line-height:1.35}
.biz p{margin:0;font-size:12.5px;font-weight:700;color:color-mix(in srgb,var(--bg) 72%,transparent);line-height:1.8}
.biz a{justify-self:start;background:var(--accent);color:#fff;font-family:var(--fh);font-weight:900;font-size:13.5px;padding:12px 18px}
@media(min-width:760px){
  .hub-hero .in{grid-template-columns:1.15fr .85fr;padding:72px 20px 64px;gap:50px}
  .idx{justify-self:end}
  .about{grid-template-columns:repeat(3,1fr);gap:0}
  .ab{border-right:0}.ab:last-child{border-right:1px solid var(--ink)}
  .ab .arr{display:flex;position:absolute;right:-13px;top:88px;width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;align-items:center;justify-content:center;font-family:'Anton',sans-serif;font-size:14px;z-index:2}
  .ab:last-child .arr{display:none}
  .look{padding:48px 20px}
  .look3{grid-template-columns:repeat(3,1fr);gap:14px}
  .sit{grid-template-columns:repeat(4,1fr);gap:16px}
  .sit-q{padding:20px 20px 22px}
  .sit-a{padding:20px 56px 18px 20px}
  .sit-go{width:34px;height:34px;margin-top:-17px;right:16px}
  .fs{grid-template-columns:1fr 1fr;align-items:stretch}
  .fs .vis{border-bottom:0;border-right:1px solid var(--ink);min-height:320px}
  .fs.alt .vis{order:2;border-right:0;border-left:1px solid var(--ink)}
  .fs .bd{padding:28px 30px 26px}
  .fs .num{font-size:96px;right:22px;top:10px}
  .fs .pm{width:220px;margin:0}
  .fs .posts{width:300px;height:260px}
  .fs .posts img{width:170px}
  .fs .posts .c{width:150px;margin-left:-75px}
  .fs .sites{height:260px;max-width:420px}
  .fs .sites img{width:250px}
  .fs .sites .s2{margin-left:-125px}
  .hf{grid-template-columns:repeat(3,1fr);gap:24px}
  .biz{grid-template-columns:1fr auto;align-items:center;padding:24px 28px}
  .biz .tx{display:grid;gap:6px}
}
'''

hub_body='''
<section class="hub-hero" id="top">
  <div class="bg"></div>
  <div class="ty5" aria-hidden="true">FOR<br>CLUBS</div>
  <div class="in">
    <div class="cp">
      <div class="ey">FOR CLUBS &amp; LOCAL BUSINESS ・ CHIBISPO</div>
      <h1><span>クラブの<em>いいところ</em>、</span><br><span>探している保護者に</span><br><span>届けます。</span></h1>
      <p class="ld">チビスポは、地域と種目から子どものスポーツクラブを探せるサイトです。載せるのは無料。そこから先の「伝わる形」を、必要なところだけ手伝います。</p>
      <div class="cta"><a class="b1" href="service-listing-preview.html">無料で載せる</a><a class="b2" href="#svc">サービスを見る</a></div>
      <div class="stats"><div><b data-cnt="%(clubs)s">0</b><span>CLUBS</span></div><div><b data-cnt="%(pref)s">0</b><span>PREFECTURES</span></div><div><b>0<small>円</small></b><span>LISTING FEE</span></div></div>
    </div>
    <nav class="idx" aria-label="サービス一覧">
      <div class="stamp">INDEX</div>
      <div class="ih"><b>SERVICES</b><small>必要なところだけ</small></div>
      <a href="service-listing-preview.html"><span class="n">01</span><b>クラブを載せる<small>検索・地図・種目ページに掲載</small></b><span class="p free">FREE</span></a>
      <a href="#s02"><span class="n">02</span><b>撮影・動画制作<small>30秒のクラブ紹介動画</small></b><span class="p tba">準備中</span></a>
      <a href="service-sns-preview.html"><span class="n">03</span><b>SNS運用サポート<small>見学につながる投稿の型</small></b><span class="p">¥40,000</span></a>
      <a href="hp-samples/"><span class="n">04</span><b>ホームページ制作<small>スマホ前提の公式サイト</small></b><span class="p">¥40,000</span></a>
      <a href="service-ads-preview.html"><span class="n">05</span><b>地域の広告掲載<small>お店・企業の方へ</small></b><span class="p">¥50,000<small style="font-family:var(--f);font-size:9px">/年</small></span></a>
    </nav>
  </div>
</section>
<main><div class="wrap">
  <div class="note">【07 クラブ・事業者向け 総合LP（v2）】旧 partner-preview（partner＋recruit-pr の統合）を作り直し。役割＝<b>マガジン・SNS投稿・各ページのCTAからの着地点</b>。TOPは各LPへ直接つなぐので、ここは「チビスポとは」→「保護者が見ている3つ」→「あなたはどれ？（状況→おすすめの順路）」→「01〜05を特集型で」→「流れ」→「FAQ」→「CTA」。ヒーロー右の INDEX カードが目次兼ナビ。02は準備中マスク＋お知らせ登録（localStorage）。04のLPは未作成（見本サイトの縮図で見せる）。数字：掲載クラブは<b>サンプル</b>（本番はDBから）・都道府県は clubs/ 配下の実数。</div>

  <section class="sec2" id="about">
    <div class="ey rv">WHAT IS CHIBISPO</div>
    <h2 class="rv d1">探して、見て、<em>そのまま申し込める</em>。</h2>
    <p class="sub rv d2">保護者は「地域」と「種目」で探し、雰囲気を見て、体験を申し込みます。チビスポはその3つを1本の流れにしたサイトです。</p>
    <div class="about">
      <div class="ab rv"><div class="im"><div class="m-ph"><div class="m-sc">
        <div class="m-bar"><b>世田谷区のサッカークラブ</b><small>12件</small></div>
        <div class="m-chips"><span class="on">世田谷区</span><span class="on">サッカー</span><span class="on">初心者OK</span><span>土日</span></div>
        <div class="m-cc hot"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""><div class="m-ci"><b>わかばFC</b><small>世田谷区 ・ 小1〜小6</small><div class="m-tg"><i>体験OK</i><i>初心者OK</i></div></div></div>
        <div class="m-cc"><img src="assets/preview-video/jp-soccer-dribble.jpg" alt=""><div class="m-ci"><b>青空サッカークラブ</b><small>世田谷区 ・ 年長〜小6 ・ 月4,000円</small><div class="m-tg"><i>土日開催</i></div></div></div>
        <div class="m-cc"><img src="assets/preview-video/jp-soccer-keep.jpg" alt=""><div class="m-ci"><b>多摩川ジュニアSC</b><small>世田谷区 ・ 小1〜小4</small></div></div>
      </div><span class="m-tap" style="left:47px;top:104px"></span></div></div><div class="tx"><b><i>1</i>地域と種目で探す</b><small>市区町村・種目・こだわり（初心者OK・親の当番なし）で絞り込み。地図からも探せます</small></div><span class="arr">›</span></div>
      <div class="ab rv d1"><div class="im"><div class="m-ph"><div class="m-sc">
        <div class="m-hero"><img src="assets/preview-video/jp-soccer-run.jpg" alt=""><span>▶ 0:30</span></div>
        <div class="m-nm"><b>わかばFC</b><small>サッカー ・ 世田谷区 ・ 小1〜小6</small></div>
        <div class="m-sec">このクラブのスタイル</div>
                <div class="m-tags"><span class="on">はじめての子が多い</span><span class="on">親子で参加OK</span><span class="on">試合より練習が好き</span><span>女の子歓迎</span></div>
        <div class="m-co"><img src="assets/preview-video/post-coach.jpg" alt=""><span>まずは「楽しい」から。上手さは後からついてきます</span></div>
        <div class="m-btn">体験を申し込む（無料）</div>
      </div><span class="m-tap" style="left:105px;top:224px"></span></div></div><div class="tx"><b><i>2</i>雰囲気を見て決める</b><small>写真・動画・雰囲気のタグ・コーチの一言。「うちの子に合うか」をここで判断します</small></div><span class="arr">›</span></div>
      <div class="ab rv d2"><div class="im"><div class="m-ph"><div class="m-sc">
        <div class="m-fh"><small>わかばFC</small><b>体験を申し込む</b></div>
        <div class="m-fr"><span>お子さま</span><b>小2 ・ 男の子</b></div>
        <div class="m-fr"><span>希望日</span><b>土曜 10:00〜</b></div>
        <div class="m-fr"><span>経験</span><b>はじめて</b></div>
                <div class="m-btn">この内容で申し込む</div>
      </div><div class="m-toast"><i>✓</i><span><b>わかばFCに届きました</b>返信はマイページに届きます</span></div></div></div><div class="tx"><b><i>3</i>体験をそのまま申し込む</b><small>クラブページから見学・体験を申込。クラブにはメールで届き、マイページで返信できます</small></div><span class="arr">›</span></div>
    </div>
    <div class="about-note rv"><b>載せるのは無料です。</b>掲載料も成果報酬もありません。有料なのは、撮影・SNS・ホームページのように「手元に成果物が残るもの」だけです。</div>
  </section>

  <div class="look rv"><div class="in">
    <div class="ey">WHAT PARENTS LOOK AT</div>
    <h2>入る前の保護者が見ているのは、<em>この3つ</em>。</h2>
    <p class="sub">実績や戦績より先に見られています。ここが伝わっているクラブに、体験申込が集まります。</p>
    <div class="look3">
      <div data-n="1"><b>雰囲気</b><small>練習の様子、コーチの声かけ、子どもの表情。写真と動画で「合いそうか」を見ています</small></div>
      <div data-n="2"><b>はじめてでも大丈夫か</b><small>初心者の割合、学年ごとのコース、見学の受け入れ。最初の一歩の不安を消す情報です</small></div>
      <div data-n="3"><b>費用と親の負担</b><small>月謝・道具・当番・送迎。書いてあるだけで、問い合わせの手前で決めてもらえます</small></div>
    </div>
  </div></div>

  <section class="sec2" id="start" data-sit="e">
    <div class="ey rv">START HERE</div>
    <h2 class="rv d1">いまの状況から、<em>始める</em>。</h2>
    <p class="sub rv d2">上から順に答えると、行き先が出ます。</p>
    <div class="sv sv-e rv"><div class="flow">
  <div class="frow"><div class="fq"><span class="fk">Q1</span>チビスポに載せていますか？</div><div class="fbr"><span class="fno">いいえ</span><a class="fans" href="service-listing-preview.html"><i>01</i>クラブを載せる<small>写真1枚から・無料</small></a></div></div>
  <div class="fyes">はい</div>
  <div class="frow"><div class="fq"><span class="fk">Q2</span>SNSで、クラブの良さが伝わっていますか？</div><div class="fbr"><span class="fno">いいえ</span><a class="fans" href="service-sns-preview.html"><i>03</i>SNS運用サポート<small>投稿の型と頻度を決める</small></a></div></div>
  <div class="fyes">はい</div>
  <div class="frow"><div class="fq"><span class="fk">Q3</span>クラブの公式サイトはありますか？</div><div class="fbr"><span class="fno">ない</span><a class="fans" href="hp-samples/"><i>04</i>ホームページ制作<small>検索されたときの受け皿</small></a></div></div>
  <div class="fend">はい → いまの形で続けて大丈夫です。困ったら相談から。</div>
  <div class="frow bz"><div class="fq"><span class="fk">お店・企業の方</span>地域の子育て世帯に届けたい</div><div class="fbr"><span class="fno">こちら</span><a class="fans" href="service-ads-preview.html"><i>05</i>地域の広告掲載<small>探している保護者に届く</small></a></div></div>
</div></div>
  </section>

  <section class="sec2" id="svc">
    <div class="ey rv">SERVICES</div>
    <h2 class="rv d1">載せるところから、<em>伝わるところ</em>まで。</h2>
    <p class="sub rv d2">01は無料。02〜04はクラブ向け、05は地域のお店・企業向けです。それぞれ詳しいページがあります。</p>
    <div class="svc-list">

      <article class="fs rv" id="s01">
        <div class="vis"><div class="pm"><div class="pm-scr"><img src="%(A)ssvc-clubpage.png" alt=""></div><div class="pm-ntf"><b>体験申込が届きました</b>わかばFC ・ 小2 ・ 土曜の見学希望</div></div></div>
        <div class="bd"><div class="num">01</div>
          <div class="k">LISTING <i class="free">FREE</i></div>
          <h3>クラブを<em>載せる</em></h3>
          <p class="ld">情報とタグを登録すると、地域・種目・こだわりの検索、地図、種目ページに載ります。体験申込はメールとマイページに届きます。</p>
          <ul><li>登録は1分。写真1枚と紹介文から（スタンダードで7枚、プロで15枚まで）</li><li>雰囲気タグ（初心者OK・親の当番なし など）で見つかる</li><li>有料プラン（¥3,000／¥10,000）で上位表示と編集部の一言</li></ul>
          <div class="who"><b>こんなクラブに</b>まだ載せていない／少年団・スポ少／写真が少ない</div>
          <div class="row"><div class="pr free">FREE<small>掲載料・成果報酬なし</small></div><a class="go" href="service-listing-preview.html">詳しく見る ›</a></div>
        </div>
      </article>

      <article class="fs alt rv" id="s02">
        <div class="vis"><div class="vid"><img src="%(A)sjp-soccer-run.jpg" alt=""><span class="play"></span><span class="len">0:30</span></div>
          <div class="soon"><div class="soon-in"><div class="k">COMING SOON</div><div class="t">撮影・動画制作は<br>準備中です。</div><p>受付を始めたら、メールでお知らせします。</p><form class="soon-f" data-topic="video"><input type="email" placeholder="you@example.com" required><button type="submit">お知らせを受け取る</button></form><div class="soon-ok" hidden>登録しました。受付開始時にメールでお知らせします。</div><div class="soon-nt">お知らせ以外には使いません。</div></div></div>
        </div>
        <div class="bd"><div class="num">02</div>
          <div class="k">VIDEO <i>準備中</i></div>
          <h3>撮影・<em>動画制作</em></h3>
          <p class="ld">新入団の募集シーズンに向けて、練習の様子を30秒にまとめます。クラブページのヒーローとSNSでそのまま使えます。</p>
          <ul><li>練習1回に伺って撮影</li><li>30秒の紹介動画＋写真20枚</li><li>クラブページ・SNS・ホームページで共通利用</li></ul>
          <div class="who"><b>こんなクラブに</b>写真では雰囲気が伝わらない／募集シーズン前／SNSにも使いたい</div>
          <div class="row"><div class="pr jp">準備中<small>受付開始をお知らせします</small></div><a class="go" href="#s02">お知らせを受け取る</a></div>
        </div>
      </article>

      <article class="fs hot rv" id="s03">
        <span class="pin">おすすめ</span>
        <div class="vis"><div class="posts"><img class="a" src="%(A)spost-trial.jpg" alt=""><img class="b" src="%(A)spost-coach.jpg" alt=""><img class="c" src="%(A)spost-parents.jpg" alt=""><span class="lb">見学につながる投稿の型</span></div></div>
        <div class="bd"><div class="num">03</div>
          <div class="k">SNS <i>買い切り</i></div>
          <h3>SNS運用<em>サポート</em></h3>
          <p class="ld">投稿を代わりにやるサービスではありません。そのクラブに合った投稿の型と頻度を決めて、最初の3本を一緒に出すところまで。あとは自分たちで回せます。</p>
          <ul><li>アカウント診断と、クラブ専用の投稿の型</li><li>リール・ストーリーズ・カルーセルの役割と頻度</li><li>写真の編集と、チビスポで使っているAIプロンプト</li></ul>
          <div class="who"><b>こんなクラブに</b>投稿が続かない／何を出せばいいか分からない／担当が替わる</div>
          <div class="row"><div class="pr">¥40,000<small>税抜・月額なし</small></div><a class="go" href="service-sns-preview.html">詳しく見る ›</a></div>
        </div>
      </article>

      <article class="fs alt rv" id="s04">
        <div class="vis"><div class="sites"><img class="s1" src="%(A)st1-dance.webp" alt=""><img class="s2" src="%(A)st2-soccer.webp" alt=""><img class="s3" src="%(A)st4-warm.webp" alt=""><span class="lb">デザインは5タイプから選ぶ</span></div></div>
        <div class="bd"><div class="num">04</div>
          <div class="k">WEBSITE</div>
          <h3>ホームページ<em>制作</em></h3>
          <p class="ld">クラブ名で検索されたときに出る、スマホ前提の公式サイトを1ページで。チビスポの掲載情報と写真をそのまま流用するので、原稿づくりの負担がありません。</p>
          <ul><li>スポーツ・あたたかい・凛と など5タイプから選ぶ</li><li>活動日・月謝・体験申込フォームまで1ページに</li><li>更新はこちらで。年1回の見直し込み</li></ul>
          <div class="who"><b>こんなクラブに</b>SNSだけで運営している／古いサイトを作り直したい</div>
          <div class="row"><div class="pr">¥40,000<small>税抜＋運用 年¥20,000</small></div><a class="go" href="hp-samples/">見本を見る ›</a></div>
        </div>
      </article>

      <article class="fs rv" id="s05">
        <div class="vis"><div class="adv"><div class="tiles">
          <div class="tile"><img src="%(A)sad-seikotsu.jpg" alt=""><span class="ad">AD</span><b>みどり整骨院</b><small>世田谷区 ・ 徒歩5分</small></div>
          <div class="tile"><img src="%(A)sad-sports.jpg" alt=""><span class="ad">AD</span><b>スポーツ用品店</b><small>スパイク・ユニフォーム</small></div>
        </div></div></div>
        <div class="bd"><div class="num">05</div>
          <div class="k">FOR LOCAL BUSINESS</div>
          <h3>地域の<em>広告掲載</em></h3>
          <p class="ld">クラブを探している最中の保護者に、地域のお店として出ます。検索結果とクラブページの「地域のおすすめ企業」枠。取材はオンライン、写真はお店からのご提供で。</p>
          <ul><li>市区町村ごとの枠。同業は少数に限定</li><li>オンライン取材30分で紹介文を作成</li><li>年額1本。月額・成果報酬なし</li></ul>
          <div class="who"><b>こんなお店に</b>整骨院・接骨院／スポーツ用品店／歯科・小児科／学習塾</div>
          <div class="row"><div class="pr">¥50,000<small>税抜・年額</small></div><a class="go" href="service-ads-preview.html">詳しく見る ›</a></div>
        </div>
      </article>
    </div>
  </section>

  <section class="sec2" id="flow">
    <div class="ey rv">HOW TO START</div>
    <h2 class="rv d1">決めるのは、<em>話してから</em>で大丈夫です。</h2>
    <p class="sub rv d2">何が必要か分からない状態でも構いません。いまの状況をうかがってから、必要なものだけ提案します。</p>
    <div class="hf rv">
      <div><div class="n">STEP 01</div><b>相談する</b><small>下のフォームか、各ページのフォームから。オンラインで30分、いまの状況を聞きます。</small><em>FREE ・ ONLINE 30 MIN</em></div>
      <div><div class="n">STEP 02</div><b>順路を決める</b><small>載せるだけで足りるのか、動画やSNSが要るのか。必要のないものは提案しません。</small><em>NO PRESSURE</em></div>
      <div><div class="n">STEP 03</div><b>始める</b><small>掲載はその日から。制作は納品まで2週間が目安です。</small><em>SAME DAY LISTING</em></div>
    </div>
    <div class="biz rv"><div class="tx"><div class="k">FOR LOCAL BUSINESS</div><b>地域のお店・企業の方は、広告掲載のページへ。</b><p>整骨院・スポーツ用品店・歯科・塾など、子育て世帯が使うお店の枠です。市区町村ごとに少数枠。</p></div><a href="service-ads-preview.html">広告掲載を見る ›</a></div>
  </section>

  <section class="sec2" id="faq">
    <div class="ey rv">FAQ</div>
    <h2 class="rv d1">よくある質問</h2>
    <div class="faq rv">
      <details><summary>本当に無料ですか。</summary><div class="a">掲載・体験申込の受信・マイページでの編集は無料です。有料なのは撮影・SNS・ホームページのように、手元に成果物が残るものだけです。無料のまま使い続けられます。</div></details>
      <details><summary>少年団（ボランティア運営）でも載せられますか。</summary><div class="a">載せられます。掲載クラブの多くが少年団・スポ少です。年度予算がなくても、掲載だけなら費用はかかりません。</div></details>
      <details><summary>写真や動画がありません。</summary><div class="a">写真1枚と紹介文があれば載せられます。写真のあるクラブのほうが体験申込は明らかに多いので、スマホの写真1枚で構わないので載せることをおすすめしています。枚数を増やしたい場合はスタンダード（7枚）・プロ（15枚）があります。</div></details>
      <details><summary>どれを頼めばいいか分かりません。</summary><div class="a">「いまの状況から、始める。」で当てはまるものを選ぶか、相談フォームから送ってください。必要のないものは提案しません。</div></details>
      <details><summary>広告はどんな業種が載っていますか。</summary><div class="a">整骨院・接骨院、スポーツ用品店、歯科・小児科、学習塾など、子育て世帯が使うお店が中心です。市区町村ごとに同業は少数に限定しています。</div></details>
    </div>
  </section>

  <div class="svcta" id="apply"><div class="big">CHIBISPO</div><div class="in"><div class="ey">FOR CLUBS</div><h2>まず、無料で載せてみてください。</h2><p>登録は1分。載せてから、必要なものを決めれば大丈夫です。相談だけでも構いません。</p><div class="row"><a class="b1" href="service-listing-preview.html">無料で載せる</a><a class="b2" href="contact-preview.html?who=club">相談する</a></div></div></div>
  <div class="svnav"><span class="cur">クラブ・事業者の方へ</span><a href="service-listing-preview.html">01 クラブを載せる</a><a href="#s02">02 撮影・動画制作</a><a href="service-sns-preview.html">03 SNS運用サポート</a><a href="hp-samples/">04 ホームページ制作</a><a href="service-ads-preview.html">05 地域の広告掲載</a></div>
  <div style="height:40px"></div>
</div></main>
<div class="sbar" id="sbar"><div class="t">掲載は無料です<small>登録1分・写真1枚と紹介文から</small></div><a class="lp-go" href="service-listing-preview.html">無料で載せる</a></div>
'''%dict(A=A,clubs=HUB_NUM_CLUBS,pref=HUB_NUM_PREF)

hub_js='''<script>
(function(){
 var hero=document.querySelector('.hub-hero');
 var tabs=document.getElementById('sttabs');
 if(tabs){tabs.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;tabs.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});document.querySelectorAll('.st-p').forEach(function(p){p.classList.toggle('on',p.dataset.st===b.dataset.st)})});}
 var sm=location.search.match(/st=([abcd])/);if(sm&&tabs){var tb=tabs.querySelector('[data-st="'+sm[1]+'"]');if(tb)tb.click()}
 /* 「お知らせを受け取る」の保存は shared.js に集約（waitlist テーブルへ） */
 if(/noanim=1/.test(location.search)){
   var st=document.createElement('style');
   st.textContent='*{transition:none!important;animation:none!important}.hub-hero h1 span,.idx a{opacity:1!important;transform:none!important}.hub-hero .bg{transform:none!important}';
   document.head.appendChild(st);
   document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});
   document.querySelectorAll('[data-cnt]').forEach(function(b){b.textContent=b.dataset.cnt});
   return;
 }
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
 document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
 document.querySelectorAll('[data-cnt]').forEach(function(b){var to=+b.dataset.cnt,t0=null;function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/900);b.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)}setTimeout(function(){requestAnimationFrame(f)},400)});
 var sb=document.getElementById('sbar');
 if(sb&&hero)new IntersectionObserver(function(e){sb.classList.toggle('on',!e[0].isIntersecting&&e[0].boundingClientRect.top<0)},{threshold:0}).observe(hero);
})();
</script>'''
page('partner-preview.html','クラブ・事業者の方へ｜チビスポ（総合案内・プレビュー）',hub_body,hub_css,extra_js=hub_js)
