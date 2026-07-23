import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// FCM HTTP v1 でプッシュ通知を送る。サーバー間呼び出し前提（クライアントからは呼ばせない）。
// 入力: { team_id?, user_id?, title, body, data?, secret }
//  - team_id → teams.user_id を引いてそのクラブ運営者へ
//  - user_id → そのユーザーへ
//  - secret  → PUSH_TRIGGER_SECRET と一致必須（無断トリガー防止）
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const SERVICE_ACCOUNT = Deno.env.get('FIREBASE_SERVICE_ACCOUNT')!;
const TRIGGER_SECRET = Deno.env.get('PUSH_TRIGGER_SECRET') || '';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', ...cors } });

function b64url(buf: ArrayBuffer | Uint8Array): string {
  const bytes = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
  let str = '';
  for (const b of bytes) str += String.fromCharCode(b);
  return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// サービスアカウントのRS256署名JWTでアクセストークンを取得（キャッシュなし・都度）
async function getAccessToken(sa: { client_email: string; private_key: string }): Promise<string> {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(new TextEncoder().encode(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const claims = b64url(new TextEncoder().encode(JSON.stringify({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/firebase.messaging',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now, exp: now + 3600,
  })));
  const signingInput = `${header}.${claims}`;

  const pem = sa.private_key.replace(/-----BEGIN PRIVATE KEY-----/, '').replace(/-----END PRIVATE KEY-----/, '').replace(/\s/g, '');
  const der = Uint8Array.from(atob(pem), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey('pkcs8', der, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(signingInput));
  const jwt = `${signingInput}.${b64url(sig)}`;

  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${jwt}`,
  });
  const j = await r.json();
  if (!j.access_token) throw new Error('token_exchange_failed: ' + JSON.stringify(j));
  return j.access_token;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const { team_id, user_id, title, body, data, secret } = await req.json();
    if (TRIGGER_SECRET && secret !== TRIGGER_SECRET) return json({ ok: false, error: 'forbidden' }, 403);
    if (!title || !body) return json({ ok: false, error: 'missing_title_body' }, 400);

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

    // 対象ユーザーを決定
    let uid = user_id as string | undefined;
    if (!uid && team_id) {
      const { data: t } = await admin.from('teams').select('user_id').eq('id', team_id).limit(1);
      uid = t?.[0]?.user_id;
    }
    if (!uid) return json({ ok: false, error: 'no_target' }, 400);

    // 有効なトークンを取得
    const { data: toks } = await admin.from('push_tokens').select('token').eq('user_id', uid).eq('enabled', true);
    if (!toks || !toks.length) return json({ ok: true, sent: 0, note: 'no_tokens' });

    const sa = JSON.parse(SERVICE_ACCOUNT);
    const accessToken = await getAccessToken(sa);
    const projectId = sa.project_id;

    let sent = 0;
    const dead: string[] = [];
    for (const { token } of toks) {
      const msg = {
        message: {
          token,
          notification: { title, body },
          data: data ? Object.fromEntries(Object.entries(data).map(([k, v]) => [k, String(v)])) : undefined,
          android: { priority: 'high' },
          apns: { headers: { 'apns-priority': '10' } },
        },
      };
      const r = await fetch(`https://fcm.googleapis.com/v1/projects/${projectId}/messages:send`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(msg),
      });
      if (r.status === 200) sent++;
      else {
        const err = await r.json().catch(() => ({}));
        const code = err?.error?.details?.[0]?.errorCode || err?.error?.status;
        if (r.status === 404 || code === 'UNREGISTERED' || code === 'INVALID_ARGUMENT') dead.push(token);
      }
    }
    // 無効トークンを掃除
    if (dead.length) await admin.from('push_tokens').delete().in('token', dead);

    return json({ ok: true, sent, cleaned: dead.length });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
