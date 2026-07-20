/**
 * テスト用クラブの作成（アプリE2Eテスト＋Metaアプリ審査のテストアカウント兼用）
 * ------------------------------------------------------------------
 * 何度実行しても安全（冪等）：
 *   - ユーザーが既にいれば「パスワードを再設定」して表示します
 *   - クラブが既にあれば再利用します
 *   - 申込サンプルは無い場合だけ入れます
 *
 * 使い方：
 *   1. このコマンドをターミナルに貼る（まだEnterしない）
 *      cd ~/kodomo-dooo-deploy && SUPABASE_SERVICE_KEY=$(pbpaste) node create-test-club.mjs --yes
 *   2. Supabaseの Settings → API Keys で sb_secret_... をコピー
 *   3. ターミナルに戻って Enter
 */
import { randomBytes } from "node:crypto";

const URL_BASE = "https://emkpkomrgknzrmxqbrvx.supabase.co";
const KEY = process.env.SUPABASE_SERVICE_KEY || "";
const APPLY = process.argv.includes("--yes");

const TEST_EMAIL = "app-test@chibispo.com";
const TEST_CLUB_NAME = "テストFC（アプリ検証用）";

if (!KEY) { console.error("✗ SUPABASE_SERVICE_KEY が未設定です。"); process.exit(1); }
const KEY_TRIMMED = KEY.trim();
if (!/^(sb_secret_[A-Za-z0-9_-]+|eyJ[A-Za-z0-9_.-]+)$/.test(KEY_TRIMMED)) {
  console.error(`✗ クリップボードの中身がSupabaseのキーではありません（先頭: "${KEY_TRIMMED.slice(0, 30)}..."）。
  手順：
   1. まずこのコマンドをターミナルに貼る（まだEnterしない）
   2. Supabaseの Settings → API Keys で sb_secret_... をコピー
   3. ターミナルに戻って Enter`);
  process.exit(1);
}
const h = KEY_TRIMMED.startsWith("sb_")
  ? { apikey: KEY_TRIMMED, "Content-Type": "application/json" }
  : { apikey: KEY_TRIMMED, Authorization: `Bearer ${KEY_TRIMMED}`, "Content-Type": "application/json" };

async function api(path, init) {
  const r = await fetch(`${URL_BASE}${path}`, { ...init, headers: { ...h, ...(init?.headers || {}) } });
  const text = await r.text();
  let j; try { j = JSON.parse(text); } catch { j = text; }
  return { ok: r.ok, status: r.status, body: j };
}

if (!APPLY) {
  console.log(`作成予定（冪等・何度でも実行可）:
  ユーザー: ${TEST_EMAIL}（既存ならパスワード再設定）
  クラブ:   ${TEST_CLUB_NAME}（status=pending・公開ページに出ません）
  申込サンプル: 3件（無い場合のみ）
※ 確認のみ（--yes を付けると実行します）`);
  process.exit(0);
}

const password = "Test-" + randomBytes(6).toString("base64url");

// 1) ユーザー：既存クラブから user_id を引く → いなければ新規作成
let userId = null;
{
  const t = await api(`/rest/v1/teams?name=eq.${encodeURIComponent(TEST_CLUB_NAME)}&select=id,user_id`);
  if (t.ok && t.body.length) userId = t.body[0].user_id;
}
if (userId) {
  const r = await api(`/auth/v1/admin/users/${userId}`, {
    method: "PUT",
    body: JSON.stringify({ password, email_confirm: true }),
  });
  if (!r.ok) { console.error("✗ パスワード再設定失敗:", r.status, JSON.stringify(r.body).slice(0, 200)); process.exit(1); }
  console.log(`✓ 既存ユーザーのパスワードを再設定: ${userId}`);
} else {
  const r = await api(`/auth/v1/admin/users`, {
    method: "POST",
    body: JSON.stringify({ email: TEST_EMAIL, password, email_confirm: true }),
  });
  if (!r.ok) { console.error("✗ ユーザー作成失敗:", r.status, JSON.stringify(r.body).slice(0, 200)); process.exit(1); }
  userId = r.body.id;
  console.log(`✓ ユーザー作成: ${userId}`);
}

// ★ 以降で何が失敗してもログイン情報は失われないよう、先に表示する
console.log(`
============================================
✅ テスト用ログイン情報（チャットに貼ってOK）:
  メール:     ${TEST_EMAIL}
  パスワード: ${password}
============================================
`);

// 2) クラブ：既存なら再利用
let teamId = null;
{
  const t = await api(`/rest/v1/teams?name=eq.${encodeURIComponent(TEST_CLUB_NAME)}&select=id`);
  if (t.ok && t.body.length) { teamId = t.body[0].id; console.log(`✓ 既存クラブを再利用: ${teamId}`); }
}
if (!teamId) {
  const r = await api(`/rest/v1/teams`, {
    method: "POST",
    headers: { Prefer: "return=representation" },
    body: JSON.stringify([{
      name: TEST_CLUB_NAME, sport: "サッカー", pref: "岡山県", city: "岡山市北区",
      age_groups: ["小学生"], age_min: 6,
      female_instructor: false, girls_welcome: true,
      days: ["土"], fee_num: 3000, fee: "月3,000円", trial: true,
      description: "アプリ動作検証・審査用のテストクラブです（非公開）",
      status: "pending", user_id: userId,
    }]),
  });
  if (!r.ok) { console.error("✗ クラブ作成失敗:", r.status, JSON.stringify(r.body).slice(0, 300)); process.exit(1); }
  teamId = r.body[0].id;
  console.log(`✓ クラブ作成: ${teamId}`);
}
console.log(`  クラブID: ${teamId}`);

// 3) 体験申込サンプル（無い場合のみ。全行同じキー構成にする＝PostgRESTの一括insert要件）
{
  const ex = await api(`/rest/v1/trial_requests?team_id=eq.${teamId}&select=id&limit=1`);
  if (ex.ok && ex.body.length) {
    console.log("✓ 申込サンプルは既にあります（スキップ）");
  } else {
    const now = Date.now(), day = 86400000;
    const base = {
      team_id: teamId, parent_name: null, parent_email: null, parent_phone: null,
      child_name: null, child_grade: null, preferred_date_1: null, message: null,
      source: null, via: "form", status: "new", created_at: null,
    };
    const rows = [
      { ...base, parent_name: "山田", parent_email: "yamada-test@example.com", parent_phone: "090-0000-1111",
        child_name: "たろう", child_grade: "小2", preferred_date_1: "7/20(日)", message: "初心者ですが大丈夫ですか？",
        created_at: new Date(now - 1 * day).toISOString() },
      { ...base, parent_name: "佐々木", parent_email: "manual@chibispo.local", parent_phone: "080-0000-2222",
        child_grade: "年長", source: "電話", via: "manual",
        created_at: new Date(now - 2 * day).toISOString() },
      { ...base, parent_name: "伊藤", parent_email: "ito-test@example.com",
        child_name: "みお", child_grade: "小4", preferred_date_1: "7/13(日)", source: "知人の紹介", status: "attended",
        created_at: new Date(now - 6 * day).toISOString() },
    ];
    const r = await api(`/rest/v1/trial_requests`, { method: "POST", body: JSON.stringify(rows) });
    if (!r.ok) { console.error("✗ 申込サンプル作成失敗:", r.status, JSON.stringify(r.body).slice(0, 300)); process.exit(1); }
    console.log("✓ 体験申込サンプル 3件");
  }
}

console.log("\n完了。上のログイン情報をチャットに貼ってください。");
