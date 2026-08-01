/* 地域ページを静的HTMLで生成する。
   実行： node build-area-pages.mjs

   ■ 何をしているか
   検索ページ（search.html）をそのまま型として読み込み、
     ・タイトル / 説明文 / canonical / 構造化データ を地域ごとに差し替え
     ・検索結果のカードを HTML に焼き込む（Googleに中身を届けるため）
     ・window.__AREA_INIT で地域・種目の初期条件を渡す
   だけを行う。サイドバーも絞り込みも search.html のものがそのまま動く。

   ■ なぜこの形か
   ユーザーから見える画面は「検索ページ」1つだけにしたい。
   けれど「岡山市 サッカー」のような検索に応えるには、URLが分かれている必要がある
   （1つのURLは1つの話題でしか評価されないため）。
   そこで「画面は1つ・URLは230通り」にする。UIの定義は search.html だけにあり、
   ここではコピーしない。search.html を直せば230ページすべてに反映される。

   ■ URL
     /area/                                全国（条件なし）
     /area/okayama/                        都道府県
     /area/okayama/okayama/                市区町村
     /area/okayama/sport/soccer/           都道府県 × 種目
     /area/okayama/okayama/sport/soccer/   市区町村 × 種目
   クラブが0件の組み合わせはページを作らない（存在しないURLは404のまま）。 */
import { writeFileSync, mkdirSync, rmSync, existsSync, readFileSync } from "node:fs";
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
  "girls_welcome,female_instructor,description,photo_url,photo_positions,plan,plan_expires_at,created_at,owner_hash";

/* カードの描画は club-card.js に一本化してある（search.html と共用）。
   ブラウザ向けの素のスクリプトなので、window を渡して評価して使う */
const cardLib = {};
new Function("window", readFileSync(join(ROOT, "club-card.js"), "utf8"))(cardLib);
const { card, esc } = cardLib.ChibiCard;

const stripPref = (p) => String(p || "").replace(/[都道府県]$/, "");
const PER_PAGE = 12;   // search.html のページングと同じ。1ページ目だけ焼き込む

/* 掲載プラン順（プロ→スタンダード→フリー）。shared.js の ChibiPlan.rank と同じ基準 */
const planRank = (c) => {
  if (!c.plan || c.plan === "free") return 0;
  if (c.plan_expires_at && new Date(c.plan_expires_at) < new Date()) return 0;
  return c.plan === "pr-plus" ? 2 : 1;
};

const yen = (n) => "¥" + Number(n).toLocaleString("ja-JP");

/* 実データから紹介文を作る（同じ文が並ばないよう、数字で差をつける） */
function leadText(list, areaLabel, sportLabel) {
  const n = list.length;
  const what = sportLabel ? `${sportLabel}のクラブ・スクール` : "スポーツクラブ・習い事";
  const fees = list.map((c) => c.fee_num).filter((v) => v != null).map(Number);
  const trial = list.filter((c) => c.trial).length;
  const ages = [...new Set(list.flatMap((c) => c.age_groups || []))];
  const weekend = list.filter((c) => (c.days || []).some((d) => d === "土" || d === "日")).length;
  const girls = list.filter((c) => c.girls_welcome).length;
  const parts = [`${areaLabel}で子どもが通える${what}を${n}件掲載しています。`];
  if (fees.length) {
    const lo = Math.min(...fees), hi = Math.max(...fees);
    parts.push(lo === hi ? `月謝は${lo === 0 ? "無料" : yen(lo)}。`
      : `月謝は${lo === 0 ? "無料" : yen(lo)}〜${yen(hi)}。`);
  }
  if (trial) parts.push(`${n}件中${trial}件が体験・見学を受け付けています。`);
  if (ages.length) parts.push(`対象は${ages.join("・")}。`);
  if (weekend) parts.push(`土日に活動するクラブが${weekend}件あります。`);
  if (girls) parts.push(`女の子歓迎のクラブは${girls}件です。`);
  return parts.join("");
}

/* 構造化データ。パンくずと一覧をGoogleに渡す */
function jsonLd({ url, crumbs, list, title }) {
  const breadcrumb = {
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    itemListElement: crumbs.map((c, i) => ({
      "@type": "ListItem", position: i + 1, name: c.name, item: ORIGIN + c.href,
    })),
  };
  const items = {
    "@context": "https://schema.org", "@type": "ItemList",
    name: title, url: ORIGIN + url, numberOfItems: list.length,
    itemListElement: list.slice(0, PER_PAGE).map((c, i) => ({
      "@type": "ListItem", position: i + 1,
      item: {
        "@type": "SportsActivityLocation",
        name: c.name, url: `${ORIGIN}/club.html?id=${c.id}`,
        ...(c.photo_url ? { image: c.photo_url } : {}),
        ...(c.description ? { description: String(c.description).replace(/\s+/g, " ").trim().slice(0, 160) } : {}),
        address: {
          "@type": "PostalAddress", addressCountry: "JP",
          addressRegion: c.pref || undefined, addressLocality: c.city || undefined,
          streetAddress: c.address || undefined,
        },
      },
    })),
  };
  return `<script type="application/ld+json">${JSON.stringify(breadcrumb)}</script>\n` +
         `<script type="application/ld+json">${JSON.stringify(items)}</script>`;
}

function linkList(title, links) {
  if (!links.length) return "";
  return `<section style="margin:26px 0 0;">
  <h2 style="margin:0 0 10px;font-size:15px;font-weight:800;color:#28323f;">${esc(title)}</h2>
  <div style="display:flex;flex-wrap:wrap;gap:8px;">
${links.map((l) => `    <a href="${esc(l.href)}" style="border:1px solid #dde2e7;border-radius:8px;padding:8px 14px;font-size:13px;color:#3b4654;text-decoration:none;background:#fff;">${esc(l.label)}${l.n ? `<span style="color:#9aa3ad;font-size:11.5px;">（${l.n}）</span>` : ""}</a>`).join("\n")}
  </div>
</section>`;
}

/* ============ search.html を型にして1ページ組み立てる ============ */
const TEMPLATE = readFileSync(join(ROOT, "search.html"), "utf8");

function pageHtml({ url, title, description, h1, lead, list, crumbs, related, init }) {
  let s = TEMPLATE;

  // 検索ページは noindex。生成した地域ページは検索対象なので必ず外す
  s = s.replace(/<!--[\s\S]{0,300}?絞り込み結果はURL[\s\S]*?-->\s*/, "");
  s = s.replace(/<meta name="robots"[^>]*>\s*/, "");
  if (/noindex/.test(s)) throw new Error(`noindexが残っています: ${url}`);

  // 階層が深いので、相対で書かれた読み込み（cities.js など）の起点をルートに固定する
  s = s.replace(/(<meta charset="[^"]*">)/i, '$1\n<base href="/">');
  if (!s.includes('<base href="/">')) throw new Error(`baseを差し込めませんでした: ${url}`);

  // タイトル・説明・canonical・構造化データ
  s = s.replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(title)}</title>\n` +
    `<meta name="description" content="${esc(description)}">\n` +
    `<link rel="canonical" href="${ORIGIN}${url}">\n` +
    jsonLd({ url, crumbs, list, title }));
  s = s.replace(/(<meta property="og:title" content=")[^"]*(">)/, `$1${esc(title)}$2`);
  s = s.replace(/(<meta property="og:url" content=")[^"]*(">)/, `$1${ORIGIN}${url}$2`);
  s = s.replace(/(<meta name="twitter:title" content=")[^"]*(">)/, `$1${esc(title)}$2`);

  // 見出しを地域ごとの内容にする（「検索結果」のままではSEOにならない）
  s = s.replace(/(<h1 style="margin:0;font-size:22px;font-weight:800;">)検索結果(<\/h1>)/,
    `$1${esc(h1)}$2`);

  // パンくずと紹介文を見出しの直後に置く
  const intro = `<nav style="font-size:12px;color:#8a93a0;margin:0 0 10px;" aria-label="パンくず">` +
    crumbs.map((c, i) => i === crumbs.length - 1
      ? `<span>${esc(c.name)}</span>`
      : `<a href="${esc(c.href)}" style="color:#8a93a0;text-decoration:none;">${esc(c.name)}</a> › `).join("") +
    `</nav>\n    <p style="font-size:14px;color:#54606e;line-height:1.9;margin:0 0 16px;">${esc(lead)}</p>`;
  s = s.replace("<!-- 条件検索ボタン（タブレット以下） -->", `${intro}\n\n    <!-- 条件検索ボタン（タブレット以下） -->`);

  // 検索結果のカードを焼き込む（JSが動く前に中身が読める状態にする）
  const baked = list.slice(0, PER_PAGE).map(card).join("\n");
  s = s.replace(/(<div class="sr-cards"[^>]*>)/, `$1\n${baked}\n`);
  s = s.replace(/(<div class="sr-count"[^>]*>検索結果：<span[^>]*>)\d+(<\/span>)/, `$1${list.length}$2`);

  // 関連リンクを一覧の下に置く（クローラーの回遊路 兼 ユーザーの探し直し）
  s = s.replace('<div id="sr-pagination"', `${related}\n        <div id="sr-pagination"`);

  // 地域・種目の初期条件を渡す（search.html 側が window.__AREA_INIT を読む）
  s = s.replace("</head>", `<script>window.__AREA_INIT=${JSON.stringify(init)};</script>\n</head>`);
  return s;
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
const write = (urlPath, html) => {
  const dir = join(ROOT, urlPath);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), html);
  written.push(urlPath);
};

const home = { name: "チビスポ", href: "/" };
const areaTop = { name: "クラブを探す", href: "/area/" };
const sportsOf = (arr) => [...new Set(arr.flatMap((c) => c.sportList))];
const citiesOf = (arr) => [...new Set(arr.flatMap((c) => c.cityList))];

/* --- 都道府県 --- */
for (const [pref, list] of byPref) {
  const p = slug("pref", pref), url = `/area/${p}/`;
  write(url, pageHtml({
    url,
    title: `${pref}の子ども向けスポーツクラブ・習い事${list.length}件｜チビスポ`,
    description: leadText(list, pref, null).slice(0, 120),
    h1: `${pref}の子ども向けスポーツクラブ・習い事（${list.length}件）`,
    lead: leadText(list, pref, null),
    list, crumbs: [home, areaTop, { name: pref, href: url }],
    init: { pref: stripPref(pref) },
    related:
      linkList(`${pref}の種目から探す`, sportsOf(list).map((s) => ({
        label: s, n: byPrefSport.get(`${pref} ${s}`).length,
        href: `/area/${p}/sport/${slug("sport", s)}/`,
      }))) +
      linkList(`${pref}の市区町村から探す`, citiesOf(list).map((ci) => ({
        label: ci, n: byCity.get(`${pref} ${ci}`).length,
        href: `/area/${p}/${slug("city", ci)}/`,
      }))) +
      linkList("他の都道府県から探す", [...byPref.keys()].filter((x) => x !== pref)
        .map((x) => ({ label: x, n: byPref.get(x).length, href: `/area/${slug("pref", x)}/` }))),
  }));
}

/* --- 都道府県 × 種目 --- */
for (const [key, list] of byPrefSport) {
  const [pref, sport] = key.split(" ");
  const p = slug("pref", pref), s = slug("sport", sport), url = `/area/${p}/sport/${s}/`;
  write(url, pageHtml({
    url,
    title: `${pref}の子ども向け${sport}クラブ・スクール${list.length}件｜チビスポ`,
    description: leadText(list, pref, sport).slice(0, 120),
    h1: `${pref}の子ども向け${sport}クラブ・スクール（${list.length}件）`,
    lead: leadText(list, pref, sport),
    list,
    crumbs: [home, areaTop, { name: pref, href: `/area/${p}/` }, { name: sport, href: url }],
    init: { pref: stripPref(pref), sport },
    related:
      linkList(`${pref}で${sport}を市区町村から探す`, citiesOf(list).map((ci) => ({
        label: ci, n: (byCitySport.get(`${pref} ${ci} ${sport}`) || []).length,
        href: `/area/${p}/${slug("city", ci)}/sport/${s}/`,
      }))) +
      linkList(`${pref}の他の種目`, sportsOf(byPref.get(pref)).filter((x) => x !== sport).map((x) => ({
        label: x, n: byPrefSport.get(`${pref} ${x}`).length,
        href: `/area/${p}/sport/${slug("sport", x)}/`,
      }))) +
      linkList(`他の地域の${sport}`, [...byPrefSport.keys()]
        .filter((k) => k.endsWith(` ${sport}`) && k !== key)
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
  write(url, pageHtml({
    url,
    title: `${city}（${pref}）の子ども向けスポーツクラブ・習い事${list.length}件｜チビスポ`,
    description: leadText(list, city, null).slice(0, 120),
    h1: `${city}の子ども向けスポーツクラブ・習い事（${list.length}件）`,
    lead: leadText(list, city, null),
    list,
    crumbs: [home, areaTop, { name: pref, href: `/area/${p}/` }, { name: city, href: url }],
    init: { pref: stripPref(pref), city },
    related:
      linkList(`${city}の種目から探す`, sportsOf(list).map((s) => ({
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
    init: { pref: stripPref(pref), city, sport },
    related:
      linkList(`${city}の他の種目`, sportsOf(byCity.get(`${pref} ${city}`)).filter((x) => x !== sport)
        .map((x) => ({
          label: x, n: byCitySport.get(`${pref} ${city} ${x}`).length,
          href: `/area/${p}/${ci}/sport/${slug("sport", x)}/`,
        }))) +
      linkList(`${pref}全体で${sport}を探す`, [{
        label: `${pref}全体`, n: byPrefSport.get(`${pref} ${sport}`).length,
        href: `/area/${p}/sport/${s}/`,
      }]) +
      linkList(`${pref}の他の市区町村で${sport}`, [...byCitySport.keys()]
        .filter((k) => k.startsWith(`${pref} `) && k.endsWith(` ${sport}`) && k !== key)
        .map((k) => {
          const oc = k.split(" ")[1];
          return { label: oc, n: byCitySport.get(k).length, href: `/area/${p}/${slug("city", oc)}/sport/${s}/` };
        })),
  }));
}

/* --- /area/ 全国の入口。条件なしの検索画面そのもの --- */
{
  const url = "/area/";
  const rows = [...byPref.entries()].sort((a, b) => b[1].length - a[1].length);
  const sports = [...new Set(clubs.flatMap((c) => c.sportList))];
  // 入口は「どんなクラブが載っているか」を見せる場所。系列校が並ぶと同じ名前ばかりに
  // なるので、トップページと同じく運営者ごとに1校だけ焼き込む
  const seen = new Set(), showcase = [];
  for (const c of clubs) {
    const k = c.owner_hash || c.id;
    if (seen.has(k)) continue;
    seen.add(k); showcase.push(c);
    if (showcase.length === PER_PAGE) break;
  }
  write(url, pageHtml({
    url,
    title: `子ども向けスポーツクラブ・習い事を探す｜チビスポ`,
    description: `全国${byPref.size}都道府県・${byCity.size}市区町村の子ども向けスポーツクラブ${clubs.length}件を掲載。地域・種目・条件から探せます。`,
    h1: `子ども向けスポーツクラブ・習い事を探す（${clubs.length}件）`,
    lead: `チビスポに掲載中の${clubs.length}件を、${byPref.size}都道府県・${byCity.size}市区町村・${sports.length}種目から探せます。`,
    list: showcase, crumbs: [home, { name: "クラブを探す", href: url }],
    init: {},
    related:
      linkList("都道府県から探す", rows.map(([pref, l]) => ({
        label: pref, n: l.length, href: `/area/${slug("pref", pref)}/`,
      }))) +
      linkList("種目から探す", sports.map((s) => ({
        label: s, n: clubs.filter((c) => c.sportList.includes(s)).length,
        href: `/area/${slug("pref", clubs.find((c) => c.sportList.includes(s)).pref)}/sport/${slug("sport", s)}/`,
      }))),
  }));
  // 件数は全87件を出したいので、焼き込んだ枚数ではなく総数で上書きしている
}

console.log(`地域ページを ${written.length}枚 生成しました`);
console.log(`  都道府県 ${byPref.size} ／ 市区町村 ${byCity.size} ／ 都道府県×種目 ${byPrefSport.size} ／ 市区町村×種目 ${byCitySport.size} ／ 入口 1`);
