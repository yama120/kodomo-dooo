/* sitemap.xml を生成する。
   静的ページ＋承認済みクラブの詳細ページを列挙し、Googleに発見させる。
   実行： node build-sitemap.mjs
   クラブを増やしたら、掲載承認のあとに流し直すこと（GitHub Actionsで自動化してもよい）。 */
import { writeFileSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join, dirname, relative, sep } from "node:path";

const ORIGIN = "https://chibispo.com";
const SB = "https://emkpkomrgknzrmxqbrvx.supabase.co";
const KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVta3Brb21yZ2tuenJteHFicnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5Nzg0MTYsImV4cCI6MjA5MjU1NDQxNn0.YmtVc_0le-EDjGzv1PJHet0ShnhfFZLIYT587FzcJHQ";

/* 検索結果に出したい静的ページ。robots.txt で弾いているものは入れない。
   priority は相対的な重み付けで、Googleは参考程度にしか見ない */
const STATIC = [
  ["/", 1.0, "daily"],
  ["/area/", 0.9, "daily"],
  // search.html は noindex（絞り込み結果は地域ページと重複するため）なので載せない
  ["/map.html", 0.8, "weekly"],
  ["/magazine.html", 0.8, "weekly"],
  ["/about.html", 0.6, "monthly"],
  ["/listing.html", 0.7, "monthly"],
  ["/faq.html", 0.5, "monthly"],
  ["/contact.html", 0.4, "yearly"],
  ["/partner.html", 0.4, "monthly"],
  ["/recruit-pr.html", 0.4, "monthly"],
  ["/legal.html", 0.2, "yearly"],
  ["/trial.html", 0.5, "monthly"],
];

const SPORTS = [
  "baseball", "basketball", "baton", "bjj", "canoe", "dance", "double-dutch",
  "gymnastics", "karate", "multi", "ski", "snowboard", "soccer", "surfing",
  "swimming", "volleyball", "wrestling",
];
const CATEGORIES = ["minor", "outdoor", "personal", "royal"];
const MAGAZINES = [1, 2, 3, 4, 5, 6, 7];

const esc = (s) =>
  String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&apos;");

const url = (loc, priority, changefreq, lastmod) =>
  `  <url>\n    <loc>${esc(ORIGIN + loc)}</loc>\n` +
  (lastmod ? `    <lastmod>${lastmod.slice(0, 10)}</lastmod>\n` : "") +
  `    <changefreq>${changefreq}</changefreq>\n    <priority>${priority}</priority>\n  </url>`;

const res = await fetch(
  `${SB}/rest/v1/teams?select=id,created_at&status=eq.approved&order=created_at.desc`,
  { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } },
);
if (!res.ok) throw new Error(`teams取得に失敗: HTTP ${res.status}`);
const clubs = await res.json();

/* build-area-pages.mjs が書き出した地域ページを拾う。
   ここで走査するので、地域ページを作り直したら sitemap も流し直すこと */
const ROOT = dirname(fileURLToPath(import.meta.url));
const areaDirs = [];
(function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) walk(join(dir, e.name));
    else if (e.name === "index.html") {
      const rel = relative(ROOT, dir).split(sep).join("/");
      if (rel !== "area") areaDirs.push(`/${rel}/`);   // /area/ 自体は STATIC 側で入れている
    }
  }
})(existsSync(join(ROOT, "area")) ? join(ROOT, "area") : ROOT);

const rows = [
  ...STATIC.map(([p, pr, cf]) => url(p, pr, cf)),
  // 階層が深いほど競合が少なく刺さりやすいので、市区町村×種目を少しだけ強めに置く
  ...areaDirs.map((p) => url(p, p.split("/").length >= 6 ? 0.8 : 0.7, "weekly")),
  ...SPORTS.map((s) => url(`/sport-${s}.html`, 0.7, "weekly")),
  ...CATEGORIES.map((c) => url(`/category-${c}.html`, 0.6, "weekly")),
  ...MAGAZINES.map((n) => url(`/magazine-${n}.html`, 0.6, "monthly")),
  ...clubs.map((c) =>
    url(`/club.html?id=${c.id}`, 0.8, "weekly", c.created_at)),
];

writeFileSync(
  new URL("./sitemap.xml", import.meta.url),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${rows.join("\n")}\n</urlset>\n`,
);
console.log(`sitemap.xml を書き出しました：${rows.length}件（うちクラブ ${clubs.length}件）`);
