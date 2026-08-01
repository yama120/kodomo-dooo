/* 地域ページを静的HTMLで生成する。
   実行： node build-area-pages.mjs

   なぜ作るのか：
     クラブ詳細は club.html?id=<UUID> の1ファイル使い回しで、中身もJS描画のため、
     「岡山市 サッカー 子ども」のような検索の受け皿がサイトに存在しなかった。

   URLの形（Airbnbの /okayama-japan/stays/pet-friendly と同じ考え方。パス階層・日本語なし）：
     /area/                                  全国の入口
     /area/okayama/                          都道府県
     /area/okayama/okayama/                  市区町村
     /area/okayama/sport/soccer/             都道府県 × 種目
     /area/okayama/okayama/sport/soccer/     市区町村 × 種目

   絞り込みUI（search.html）は Airbnb の /s/... と同じく noindex にして、
   検索エンジンにはこちらの地域ページを見せる。

   クラブが0件の組み合わせはページを作らない（存在しないURLは404のまま）。
   Airbnbも該当なしのカテゴリは410を返していて、空ページは作らない。 */
import { writeFileSync, mkdirSync, rmSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join, dirname } from "node:path";
import { slug, splitMulti } from "./seo-romaji.mjs";

const ORIGIN = "https://chibispo.com";
const ROOT = dirname(fileURLToPath(import.meta.url));
const OUT = join(ROOT, "area");
const SB = "https://emkpkomrgknzrmxqbrvx.supabase.co";
const KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ";

const COLS =
  "id,name,sport,pref,city,address,age_groups,age_min,days,fee,fee_num,trial," +
  "girls_welcome,female_instructor,description,photo_url,plan,plan_expires_at,created_at";

const esc = (s) =>
  String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
const jsonEsc = (s) => JSON.stringify(String(s ?? ""));
const stripPref = (p) => String(p || "").replace(/[都道府県]$/, "");

/* 掲載プラン順（プロ→スタンダード→フリー）。shared.js の ChibiPlan.rank と同じ基準 */
const planRank = (c) => {
  if (!c.plan || c.plan === "free") return 0;
  if (c.plan_expires_at && new Date(c.plan_expires_at) < new Date()) return 0;
  return c.plan === "pr-plus" ? 2 : 1;
};

const yen = (n) => "¥" + Number(n).toLocaleString("ja-JP");
const feeText = (c) =>
  c.fee_num != null
    ? (Number(c.fee_num) === 0 ? "無料" : `${yen(c.fee_num)}〜`)
    : (c.fee || "要問合せ");

/* ---------- 実データから紹介文を作る（同じ文が並ばないよう、数字で差をつける） ---------- */
function leadText(list, areaLabel, sportLabel) {
  const n = list.length;
  const what = sportLabel ? `${sportLabel}のクラブ・スクール` : "子ども向けスポーツクラブ・習い事";
  const fees = list.map((c) => c.fee_num).filter((v) => v != null).map(Number);
  const trial = list.filter((c) => c.trial).length;
  const ages = [...new Set(list.flatMap((c) => c.age_groups || []))];
  const weekend = list.filter((c) => (c.days || []).some((d) => d === "土" || d === "日")).length;
  const girls = list.filter((c) => c.girls_welcome).length;

  const parts = [`${areaLabel}で子どもが通える${what}を${n}件掲載しています。`];
  if (fees.length) {
    const lo = Math.min(...fees), hi = Math.max(...fees);
    parts.push(lo === hi
      ? `月謝は${lo === 0 ? "無料" : yen(lo)}。`
      : `月謝は${lo === 0 ? "無料" : yen(lo)}〜${yen(hi)}。`);
  }
  if (trial) parts.push(`${n}件中${trial}件が体験・見学を受け付けています。`);
  if (ages.length) parts.push(`対象は${ages.join("・")}。`);
  if (weekend) parts.push(`土日に活動するクラブが${weekend}件あります。`);
  if (girls) parts.push(`女の子歓迎のクラブは${girls}件です。`);
  return parts.join("");
}

/* ---------- クラブカード（HTMLに中身を書く。JS描画では検索エンジンに届きにくい） ---------- */
function cardHtml(c) {
  const area = [c.pref, c.city].filter(Boolean).join("・");
  const img = c.photo_url
    ? `<img src="${esc(c.photo_url)}" alt="${esc(c.name)}の活動写真" loading="lazy" decoding="async" width="132" height="99" style="width:132px;height:99px;object-fit:cover;border-radius:10px;display:block;flex:0 0 auto;">`
    : `<div style="width:132px;height:99px;border-radius:10px;background:#eef1f4;flex:0 0 auto;"></div>`;
  const badges = [
    c.trial ? "体験あり" : null,
    c.girls_welcome ? "女の子歓迎" : null,
    c.female_instructor ? "女性指導者" : null,
  ].filter(Boolean).map((t) =>
    `<span style="font-size:11px;font-weight:700;color:#1f8a5b;background:#eaf6f0;border-radius:999px;padding:3px 9px;">${t}</span>`).join("");
  const desc = String(c.description || "").replace(/\s+/g, " ").trim().slice(0, 78);
  return `      <li style="list-style:none;">
        <a href="/club.html?id=${esc(c.id)}" style="display:flex;gap:13px;background:#fff;border:1px solid #e6e9ed;border-radius:14px;padding:13px;text-decoration:none;color:inherit;">
          ${img}
          <div style="min-width:0;flex:1;">
            <div style="font-size:11.5px;color:#8a93a0;font-weight:700;">${esc(c.sport || "スポーツ")}・${esc(area)}</div>
            <h3 style="margin:3px 0 5px;font-size:15px;font-weight:800;color:#28323f;line-height:1.4;">${esc(c.name)}</h3>
            <div style="font-size:12px;color:#54606e;line-height:1.7;">
              月謝 ${esc(feeText(c))}${(c.age_groups || []).length ? `／対象 ${esc((c.age_groups || []).join("・"))}` : ""}${(c.days || []).length ? `／${esc((c.days || []).join("・"))}曜` : ""}
            </div>
            ${desc ? `<p style="margin:5px 0 0;font-size:12px;color:#7b8492;line-height:1.7;">${esc(desc)}…</p>` : ""}
            ${badges ? `<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:7px;">${badges}</div>` : ""}
          </div>
        </a>
      </li>`;
}

/* ---------- 構造化データ。Airbnbの ItemList + ListItem + 施設 と同じ構成 ---------- */
function jsonLd({ url, crumbs, list, title }) {
  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((c, i) => ({
      "@type": "ListItem", position: i + 1, name: c.name, item: ORIGIN + c.href,
    })),
  };
  const items = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: title,
    url: ORIGIN + url,
    numberOfItems: list.length,
    itemListElement: list.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      item: {
        "@type": "SportsActivityLocation",
        name: c.name,
        url: `${ORIGIN}/club.html?id=${c.id}`,
        ...(c.photo_url ? { image: c.photo_url } : {}),
        ...(c.description ? { description: String(c.description).replace(/\s+/g, " ").trim().slice(0, 160) } : {}),
        address: {
          "@type": "PostalAddress",
          addressCountry: "JP",
          addressRegion: c.pref || undefined,
          addressLocality: c.city || undefined,
          streetAddress: c.address || undefined,
        },
      },
    })),
  };
  return `<script type="application/ld+json">${JSON.stringify(breadcrumb)}</script>
<script type="application/ld+json">${JSON.stringify(items)}</script>`;
}

function linkList(title, links) {
  if (!links.length) return "";
  return `    <section style="margin-top:26px;">
      <h2 style="margin:0 0 10px;font-size:15px;font-weight:800;color:#28323f;">${esc(title)}</h2>
      <div style="display:flex;flex-wrap:wrap;gap:8px;">
${links.map((l) => `        <a href="${esc(l.href)}" style="border:1px solid #dde2e7;border-radius:8px;padding:8px 14px;font-size:13px;color:#3b4654;text-decoration:none;background:#fff;">${esc(l.label)}${l.n ? `<span style="color:#9aa3ad;font-size:11.5px;">（${l.n}）</span>` : ""}</a>`).join("\n")}
      </div>
    </section>`;
}

function pageHtml({ url, title, description, h1, lead, list, crumbs, related, searchHref }) {
  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- shared.js のヘッダー・フッターは相対リンク（index.html など）で書かれている。
     このページは階層が深いので base で解決先をルートに固定する -->
<base href="/">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${ORIGIN}${url}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="チビスポ">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${ORIGIN}${url}">
<meta property="og:image" content="${ORIGIN}/assets/ogp.jpg?v=1">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
${jsonLd({ url, crumbs, list, title })}
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Noto Sans JP',system-ui,sans-serif;background:#f7f8fa;color:#28323f;line-height:1.75;-webkit-font-smoothing:antialiased;}
  .ar-wrap{max-width:1080px;margin:0 auto;padding:18px 20px 70px;}
  .ar-crumb{font-size:12px;color:#8a93a0;margin-bottom:12px;}
  .ar-crumb a{color:#8a93a0;text-decoration:none;}
  .ar-crumb a:hover{text-decoration:underline;}
  h1{font-family:'Zen Maru Gothic',sans-serif;font-size:24px;font-weight:900;line-height:1.4;margin-bottom:10px;}
  .ar-list{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:18px;padding:0;}
  @media (max-width:760px){ .ar-wrap{padding:14px 14px 70px;} h1{font-size:20px;} .ar-list{grid-template-columns:1fr;} }
</style>
</head>
<body>
<div class="ar-wrap">
  <nav class="ar-crumb" aria-label="パンくず">
${crumbs.map((c, i) =>
    i === crumbs.length - 1
      ? `    <span>${esc(c.name)}</span>`
      : `    <a href="${esc(c.href)}">${esc(c.name)}</a> ›`).join("\n")}
  </nav>
  <h1>${esc(h1)}</h1>
  <p style="font-size:14px;color:#54606e;">${esc(lead)}</p>

  <ul class="ar-list">
${list.map(cardHtml).join("\n")}
  </ul>

  <p style="margin-top:20px;">
    <a href="${esc(searchHref)}" style="display:inline-block;background:#2270e0;color:#fff;font-size:13.5px;font-weight:800;text-decoration:none;border-radius:999px;padding:11px 22px;">条件を追加して探す →</a>
  </p>

${related}
</div>
<script src="/shared.js?v=20260801"></script>
</body>
</html>
`;
}

/* ============================ 生成 ============================ */
const res = await fetch(`${SB}/rest/v1/teams?select=${COLS}&status=eq.approved`, {
  headers: { apikey: KEY, Authorization: `Bearer ${KEY}` },
});
if (!res.ok) throw new Error(`teams取得に失敗: HTTP ${res.status}`);
const clubs = (await res.json()).sort((a, b) => planRank(b) - planRank(a));

/* 1つの欄に複数入っているクラブ（「南風原町、糸満市」など）は、それぞれのページに載せる。
   対応表に無い値があればここで落ちる（黙って変なURLを作らない） */
for (const c of clubs) {
  c.cityList = splitMulti(c.city);
  c.sportList = splitMulti(c.sport);
  slug("pref", c.pref);
  c.cityList.forEach((x) => slug("city", x));
  c.sportList.forEach((x) => slug("sport", x));
}

const byPref = new Map(), byCity = new Map(), byPrefSport = new Map(), byCitySport = new Map();
const push = (m, k, v) => { if (!m.has(k)) m.set(k, []); m.get(k).push(v); };
for (const c of clubs) {
  push(byPref, c.pref, c);
  for (const ci of c.cityList) push(byCity, `${c.pref} ${ci}`, c);
  for (const sp of c.sportList) push(byPrefSport, `${c.pref} ${sp}`, c);
  for (const ci of c.cityList) for (const sp of c.sportList) push(byCitySport, `${c.pref} ${ci} ${sp}`, c);
}

// 消えたクラブのページが残らないよう、毎回まるごと作り直す
if (existsSync(OUT)) rmSync(OUT, { recursive: true });
const written = [];
const write = (urlPath, html) => {          // urlPath は "/area/okayama/" の形
  const dir = join(ROOT, urlPath);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), html);
  written.push(urlPath);
};

const home = { name: "チビスポ", href: "/" };
const areaTop = { name: "地域から探す", href: "/area/" };
const sportsOf = (arr) => [...new Set(arr.flatMap((c) => c.sportList))];
const citiesOf = (arr) => [...new Set(arr.flatMap((c) => c.cityList))];

/* --- 都道府県 --- */
for (const [pref, list] of byPref) {
  const p = slug("pref", pref), url = `/area/${p}/`;
  const cities = citiesOf(list), sports = sportsOf(list);
  write(url, pageHtml({
    url,
    title: `${pref}の子ども向けスポーツクラブ・習い事${list.length}件｜チビスポ`,
    description: leadText(list, pref, null).slice(0, 120),
    h1: `${pref}の子ども向けスポーツクラブ・習い事（${list.length}件）`,
    lead: leadText(list, pref, null),
    list, crumbs: [home, areaTop, { name: pref, href: url }],
    searchHref: `/search.html?pref=${encodeURIComponent(stripPref(pref))}`,
    related:
      linkList(`${pref}の種目から探す`, sports.map((s) => ({
        label: s, n: byPrefSport.get(`${pref} ${s}`).length,
        href: `/area/${p}/sport/${slug("sport", s)}/`,
      }))) +
      linkList(`${pref}の市区町村から探す`, cities.map((ci) => ({
        label: ci, n: byCity.get(`${pref} ${ci}`).length,
        href: `/area/${p}/${slug("city", ci)}/`,
      }))) +
      linkList("他の都道府県から探す", [...byPref.keys()].filter((x) => x !== pref).slice(0, 20)
        .map((x) => ({ label: x, n: byPref.get(x).length, href: `/area/${slug("pref", x)}/` }))),
  }));
}

/* --- 都道府県 × 種目 --- */
for (const [key, list] of byPrefSport) {
  const [pref, sport] = key.split(" ");
  const p = slug("pref", pref), s = slug("sport", sport), url = `/area/${p}/sport/${s}/`;
  const cities = citiesOf(list);
  write(url, pageHtml({
    url,
    title: `${pref}の子ども向け${sport}クラブ・スクール${list.length}件｜チビスポ`,
    description: leadText(list, pref, sport).slice(0, 120),
    h1: `${pref}の子ども向け${sport}クラブ・スクール（${list.length}件）`,
    lead: leadText(list, pref, sport),
    list,
    crumbs: [home, areaTop, { name: pref, href: `/area/${p}/` }, { name: sport, href: url }],
    searchHref: `/search.html?pref=${encodeURIComponent(stripPref(pref))}&sport=${encodeURIComponent(sport)}`,
    related:
      linkList(`${pref}で${sport}を市区町村から探す`, cities.map((ci) => ({
        label: ci, n: (byCitySport.get(`${pref} ${ci} ${sport}`) || []).length,
        href: `/area/${p}/${slug("city", ci)}/sport/${s}/`,
      }))) +
      linkList(`${pref}の他の種目`, sportsOf(byPref.get(pref)).filter((x) => x !== sport).map((x) => ({
        label: x, n: byPrefSport.get(`${pref} ${x}`).length,
        href: `/area/${p}/sport/${slug("sport", x)}/`,
      }))) +
      linkList(`他の地域の${sport}`, [...byPrefSport.keys()]
        .filter((k) => k.endsWith(` ${sport}`) && k !== key).slice(0, 20)
        .map((k) => {
          const op = k.split(" ")[0];
          return { label: op, n: byPrefSport.get(k).length, href: `/area/${slug("pref", op)}/sport/${s}/` };
        })),
  }));
}

/* --- 市区町村 --- */
for (const [key, list] of byCity) {
  const [pref, city] = key.split(" ");
  const p = slug("pref", pref), ci = slug("city", city), url = `/area/${p}/${ci}/`;
  const sports = sportsOf(list);
  write(url, pageHtml({
    url,
    title: `${city}（${pref}）の子ども向けスポーツクラブ・習い事${list.length}件｜チビスポ`,
    description: leadText(list, city, null).slice(0, 120),
    h1: `${city}の子ども向けスポーツクラブ・習い事（${list.length}件）`,
    lead: leadText(list, city, null),
    list,
    crumbs: [home, areaTop, { name: pref, href: `/area/${p}/` }, { name: city, href: url }],
    searchHref: `/search.html?pref=${encodeURIComponent(stripPref(pref))}&city=${encodeURIComponent(city)}`,
    related:
      linkList(`${city}の種目から探す`, sports.map((s) => ({
        label: s, n: byCitySport.get(`${pref} ${city} ${s}`).length,
        href: `/area/${p}/${ci}/sport/${slug("sport", s)}/`,
      }))) +
      linkList(`${pref}の他の市区町村`, citiesOf(byPref.get(pref)).filter((x) => x !== city).map((x) => ({
        label: x, n: byCity.get(`${pref} ${x}`).length,
        href: `/area/${p}/${slug("city", x)}/`,
      }))),
  }));
}

/* --- 市区町村 × 種目 --- */
for (const [key, list] of byCitySport) {
  const [pref, city, sport] = key.split(" ");
  const p = slug("pref", pref), ci = slug("city", city), s = slug("sport", sport);
  const url = `/area/${p}/${ci}/sport/${s}/`;
  write(url, pageHtml({
    url,
    title: `${city}の子ども向け${sport}クラブ・スクール${list.length}件｜チビスポ`,
    description: leadText(list, city, sport).slice(0, 120),
    h1: `${city}の子ども向け${sport}クラブ・スクール（${list.length}件）`,
    lead: leadText(list, city, sport),
    list,
    crumbs: [home, areaTop, { name: pref, href: `/area/${p}/` },
      { name: city, href: `/area/${p}/${ci}/` }, { name: sport, href: url }],
    searchHref: `/search.html?pref=${encodeURIComponent(stripPref(pref))}&city=${encodeURIComponent(city)}&sport=${encodeURIComponent(sport)}`,
    related:
      linkList(`${city}の他の種目`, sportsOf(byCity.get(`${pref} ${city}`)).filter((x) => x !== sport)
        .map((x) => ({
          label: x, n: byCitySport.get(`${pref} ${city} ${x}`).length,
          href: `/area/${p}/${ci}/sport/${slug("sport", x)}/`,
        }))) +
      linkList(`${pref}で${sport}を探す`, [`${pref}全体`].map(() => ({
        label: `${pref}全体（${byPrefSport.get(`${pref} ${sport}`).length}件）`,
        href: `/area/${p}/sport/${s}/`,
      }))) +
      linkList(`${pref}の他の市区町村で${sport}`, [...byCitySport.keys()]
        .filter((k) => k.startsWith(`${pref} `) && k.endsWith(` ${sport}`) && k !== key)
        .map((k) => {
          const oc = k.split(" ")[1];
          return { label: oc, n: byCitySport.get(k).length, href: `/area/${p}/${slug("city", oc)}/sport/${s}/` };
        })),
  }));
}

/* --- /area/ 全国の入口。ここから全ページへ辿れるようにする（クロールの起点） --- */
{
  const url = "/area/";
  const rows = [...byPref.entries()].sort((a, b) => b[1].length - a[1].length);
  write(url, pageHtml({
    url,
    title: `地域から子ども向けスポーツクラブを探す｜チビスポ`,
    description: `全国${byPref.size}都道府県・${byCity.size}市区町村の子ども向けスポーツクラブ${clubs.length}件を掲載。地域と種目から探せます。`,
    h1: `地域から子ども向けスポーツクラブを探す`,
    lead: `チビスポに掲載中の${clubs.length}件を、${byPref.size}都道府県・${byCity.size}市区町村・${new Set(clubs.map((c) => c.sport)).size}種目から探せます。`,
    list: clubs.slice(0, 12),
    crumbs: [home, { name: "地域から探す", href: url }],
    searchHref: "/search.html",
    related: linkList("都道府県から探す", rows.map(([pref, l]) => ({
      label: pref, n: l.length, href: `/area/${slug("pref", pref)}/`,
    }))),
  }));
}

console.log(`地域ページを ${written.length}枚 生成しました`);
console.log(`  都道府県 ${byPref.size} ／ 市区町村 ${byCity.size} ／ 都道府県×種目 ${byPrefSport.size} ／ 市区町村×種目 ${byCitySport.size} ／ 入口 1`);
