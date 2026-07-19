/**
 * テスト用クラブの作成（アプリE2Eテスト＋Metaアプリ審査のテストアカウント兼用）
 * ------------------------------------------------------------------
 * 作るもの：
 *   1. テスト用ログインユーザー（メール確認済みとして作成）
 *   2. teams 1件（status='pending' なので公開ページには出ない）
 *   3. サンプルの体験申込 3件（受信箱のテスト用）
 *
 * 使い方（サービスキーはターミナルの環境変数で。チャットに貼らない）：
 *   確認のみ:  SUPABASE_SERVICE_KEY=$(pbpaste) node create-test-club.mjs
 *   実行:      SUPABASE_SERVICE_KEY=$(pbpaste) node create-test-club.mjs --yes
 *
 * 実行するとテスト用の「メール・パスワード」がターミナルに表示されます。
 * （実在の個人情報を含まない捨てアカウントなので、チャットに貼ってOK）
 */
import { randomBytes } from "node:crypto";

const URL_BASE = "https://emkpkomrgknzrmxqbrvx.supabase.co";
const KEY = process.env.SUPABASE_SERVICE_KEY;
const APPLY = process.argv.includes("--yes");

const TEST_EMAIL = "app-test@chibispo.com";
const TEST_CLUB_NAME = "テストFC（アプリ検証用）";

if (!KEY) { console.error("✗ SUPABASE_SERVICE_KEY が未設定です。"); process.exit(1); }
const h = KEY.startsWith("sb_")
  ? { apikey: KEY, "Content-Type": "application/json" }
  : { apikey: KEY, Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" };

async function api(path, init) {
  const r = await fetch(`${URL_BASE}${path}`, { ...init, headers: { ...h, ...(init?.headers || {}) } });
  const text = await r.text();
  let j; try { j = JSON.parse(text); } catch { j = text; }
  return { ok: r.ok, status: r.status, body: j };
}

// 既存チェック
const existing = await api(`/rest/v1/teams?name=eq.${encodeURIComponent(TEST_CLUB_NAME)}&select=id,user_id`);
if (existing.ok && existing.body.length) {
  console.log(`✓ テストクラブは既に存在します: ${existing.body[0].id}`);
  console.log("  ログイン情報を忘れた場合は、一度このチームとユーザーを消してから再実行してください。");
  process.exit(0);
}

console.log(`作成予定:
  ユーザー: ${TEST_EMAIL}
  クラブ:   ${TEST_CLUB_NAME}（status=pending・公開ページに出ません）
  申込サンプル: 3件`);
if (!APPLY) { console.log("\n※ 確認のみ（--yes を付けると実行します）"); process.exit(0); }

// 1) ユーザー作成（メール確認済み扱い）
const password = "Test-" + randomBytes(6).toString("base64url");
let userId;
{
  const r = await api(`/auth/v1/admin/users`, {
    method: "POST",
    body: JSON.stringify({ email: TEST_EMAIL, password, email_confirm: true }),
  });
  if (!r.ok) {
    if (String(JSON.stringify(r.body)).includes("already")) {
      console.error("✗ ユーザーが既に存在します。パスワード不明なら管理画面から削除して再実行を。");
    } else {
      console.error("✗ ユーザー作成失敗:", r.status, JSON.stringify(r.body).slice(0, 200));
    }
    process.exit(1);
  }
  userId = r.body.id;
  console.log(`✓ ユーザー作成: ${userId}`);
}

// 2) チーム作成
let teamId;
{
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
  if (!r.ok) { console.error("✗ チーム作成失敗:", r.status, JSON.stringify(r.body).slice(0, 300)); process.exit(1); }
  teamId = r.body[0].id;
  console.log(`✓ クラブ作成: ${teamId}`);
}

// 3) 体験申込サンプル
{
  const now = Date.now(), day = 86400000;
  const rows = [
    { team_id: teamId, parent_name: "山田", parent_email: "yamada-test@example.com", parent_phone: "090-0000-1111",
      child_name: "たろう", child_grade: "小2", preferred_date_1: "7/20(日)", message: "初心者ですが大丈夫ですか？",
      source: null, via: "form", status: "new", created_at: new Date(now - 1 * day).toISOString() },
    { team_id: teamId, parent_name: "佐々木", parent_email: "manual@chibispo.local", parent_phone: "080-0000-2222",
      child_grade: "年長", source: "電話", via: "manual", status: "new", created_at: new Date(now - 2 * day).toISOString() },
    { team_id: teamId, parent_name: "伊藤", parent_email: "ito-test@example.com",
      child_name: "みお", child_grade: "小4", preferred_date_1: "7/13(日)",
      source: "知人の紹介", via: "form", status: "attended", created_at: new Date(now - 6 * day).toISOString() },
  ];
  const r = await api(`/rest/v1/trial_requests`, { method: "POST", body: JSON.stringify(rows) });
  if (!r.ok) { console.error("✗ 申込サンプル作成失敗:", r.status, JSON.stringify(r.body).slice(0, 300)); process.exit(1); }
  console.log("✓ 体験申込サンプル 3件");
}

console.log(`
============================================
✅ 完了。テスト用ログイン情報（チャットに貼ってOK）:
  メール:     ${TEST_EMAIL}
  パスワード: ${password}
  クラブID:   ${teamId}
============================================`);
