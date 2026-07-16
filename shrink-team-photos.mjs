/**
 * 既存のクラブ写真を縮小して差し替える（Supabaseの配信量[Cached Egress]対策）
 * ------------------------------------------------------------------
 * スマホ写真が原寸(4〜5MB)のままアップされている画像を、長辺1280px・JPEG品質85%に縮小して
 * 同じURLのまま上書きする。URLが変わらないので teams テーブルの更新は不要。
 *
 * 使い方（キーはターミナルの環境変数で渡す。チャットには貼らない）：
 *   確認のみ（何も変更しない）:
 *     SUPABASE_SERVICE_KEY='sb_secret_...' node shrink-team-photos.mjs
 *   実行:
 *     SUPABASE_SERVICE_KEY='sb_secret_...' node shrink-team-photos.mjs --yes
 *
 * オプション:
 *   --min=500     何KB超の画像を対象にするか（既定: 500KB）
 *   --max=1280    長辺の最大px（既定: 1280。マイページのリサイズと同条件）
 *
 * 必要: macOSの sips（標準搭載）を使うので追加インストール不要。
 */
import { execFileSync } from "node:child_process";
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const URL_BASE = "https://emkpkomrgknzrmxqbrvx.supabase.co";
const BUCKET = "team-photos";
const KEY = process.env.SUPABASE_SERVICE_KEY;
const args = process.argv.slice(2);
const APPLY = args.includes("--yes");
const MIN_KB = Number((args.find((a) => a.startsWith("--min=")) || "--min=500").split("=")[1]);
const MAX_PX = Number((args.find((a) => a.startsWith("--max=")) || "--max=1280").split("=")[1]);

if (!KEY) {
  console.error("✗ 環境変数 SUPABASE_SERVICE_KEY が未設定です。");
  process.exit(1);
}
const h = KEY.startsWith("sb_") ? { apikey: KEY } : { apikey: KEY, Authorization: `Bearer ${KEY}` };

// 1) 画像URLを集める
const res = await fetch(`${URL_BASE}/rest/v1/teams?select=id,name,photo_url,logo_url,photos`, { headers: h });
if (!res.ok) { console.error("✗ teams取得失敗:", res.status, (await res.text()).slice(0, 200)); process.exit(1); }
const teams = await res.json();

const urls = [];
for (const t of teams) {
  for (const k of ["photo_url", "logo_url"]) if (t[k]) urls.push({ name: t.name, url: t[k] });
  if (Array.isArray(t.photos)) for (const u of t.photos) if (typeof u === "string" && u.startsWith("http")) urls.push({ name: t.name, url: u });
}
console.log(`画像URL: ${urls.length}件 / 対象条件: ${MIN_KB}KB超 → 長辺${MAX_PX}px・JPEG85%\n`);

// 2) サイズを測って対象を絞る
const targets = [];
for (const it of urls) {
  try {
    const r = await fetch(it.url, { method: "HEAD" });
    const sz = Number(r.headers.get("content-length") || 0);
    if (sz > MIN_KB * 1024) targets.push({ ...it, size: sz });
  } catch { /* 取れないものはスキップ */ }
}
targets.sort((a, b) => b.size - a.size);
const totalBefore = targets.reduce((s, t) => s + t.size, 0);
console.log(`■ 対象: ${targets.length}件 / 合計 ${(totalBefore / 1024 / 1024).toFixed(1)}MB`);
for (const t of targets) console.log(`   ${(t.size / 1024 / 1024).toFixed(2)}MB  ${t.name}`);

if (!targets.length) { console.log("\n対象なし。何もしません。"); process.exit(0); }
if (!APPLY) { console.log("\n※ 確認のみ（--yes を付けると実行します）"); process.exit(0); }

// 3) ダウンロード → sipsで縮小 → 同じパスへ上書き
const tmp = mkdtempSync(join(tmpdir(), "shrink-"));
let done = 0, totalAfter = 0;
for (const t of targets) {
  try {
    const path = decodeURIComponent(new globalThis.URL(t.url).pathname.split(`/object/public/${BUCKET}/`)[1] || "");
    if (!path) { console.log(`  skip(パス不明): ${t.name}`); continue; }

    const buf = Buffer.from(await (await fetch(t.url)).arrayBuffer());
    const f = join(tmp, "x.jpg");
    writeFileSync(f, buf);
    execFileSync("sips", ["-Z", String(MAX_PX), "-s", "format", "jpeg", "-s", "formatOptions", "85", f], { stdio: "ignore" });
    const out = readFileSync(f);

    const up = await fetch(`${URL_BASE}/storage/v1/object/${BUCKET}/${path.split("/").map(encodeURIComponent).join("/")}`, {
      method: "POST",
      headers: { ...h, "Content-Type": "image/jpeg", "x-upsert": "true", "cache-control": "public, max-age=31536000" },
      body: out,
    });
    if (!up.ok) { console.log(`  ✗ ${t.name}: 上書き失敗 ${up.status} ${(await up.text()).slice(0, 120)}`); continue; }

    totalAfter += out.length;
    done++;
    console.log(`  ✓ ${t.name}: ${(t.size / 1024 / 1024).toFixed(2)}MB → ${(out.length / 1024).toFixed(0)}KB`);
  } catch (e) {
    console.log(`  ✗ ${t.name}: ${String(e.message).slice(0, 120)}`);
  }
}
rmSync(tmp, { recursive: true, force: true });

console.log(`\n完了: ${done}/${targets.length}件`);
console.log(`合計 ${(totalBefore / 1024 / 1024).toFixed(1)}MB → ${(totalAfter / 1024 / 1024).toFixed(1)}MB（${Math.round((1 - totalAfter / totalBefore) * 100)}%削減）`);
console.log("※ URLは変わらないため teams の更新は不要。CDNキャッシュが切れ次第、新しい画像が配信されます。");
