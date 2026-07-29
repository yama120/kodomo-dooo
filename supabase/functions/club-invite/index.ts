import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

/* クラブスタッフの招待。
   3つの action を持つ：
     invite … オーナーがスタッフを招待する（要オーナーのJWT）
     peek   … 招待リンクの中身を見る（未ログインでも可・トークンのみ）
     accept … 招待を承諾して team_members.user_id を埋める（要本人のJWT）

   team_members への書き込みはすべてここ（service_role）で行う。
   ブラウザから直接書けるようにすると、他人が任意のクラブに
   自分を追加できてしまうため。 */

const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY') || '';
const SITE = 'https://chibispo.com';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (b: unknown, s = 200) =>
  new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', ...cors } });

/* 検証用アカウントから実在のクラブ関係者へメールを出さない。
   2026-07-28の誤送信を受けたサーバ側のガード（運用ルールだけに頼らない） */
const TEST_ADDRS = ['app-parent-test@chibispo.com', 'app-test@chibispo.com'];
const isTestAddr = (e: string) => TEST_ADDRS.includes(String(e || '').toLowerCase());

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ ok: false, error: 'method' }, 405);

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });
  const { action, token, team_id, email, name, role } = await req.json().catch(() => ({}));
  const bearer = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');

  /* ---------- 招待リンクの中身を見る（未ログインでも可） ---------- */
  if (action === 'peek') {
    if (!token) return json({ ok: false, error: 'no_token' }, 400);
    const { data } = await admin.from('team_members')
      .select('email, role, user_id, invite_expires_at, team_id, teams(name)')
      .eq('invite_token', token).limit(1);
    const row = data?.[0] as
      | { email: string; role: string; user_id: string | null; invite_expires_at: string | null; team_id: string; teams?: { name?: string } }
      | undefined;
    if (!row) return json({ ok: false, error: 'invalid' }, 404);
    if (row.user_id) return json({ ok: false, error: 'used' }, 409);
    if (row.invite_expires_at && Date.parse(row.invite_expires_at) < Date.now()) {
      return json({ ok: false, error: 'expired' }, 410);
    }
    return json({ ok: true, email: row.email, role: row.role, team_name: row.teams?.name || null });
  }

  /* ---------- 招待を承諾する（要ログイン） ---------- */
  if (action === 'accept') {
    if (!token) return json({ ok: false, error: 'no_token' }, 400);
    if (!bearer) return json({ ok: false, error: 'no_auth' }, 401);
    const { data: ures } = await admin.auth.getUser(bearer);
    const user = ures?.user;
    if (!user) return json({ ok: false, error: 'invalid_token' }, 401);

    const { data } = await admin.from('team_members')
      .select('id, email, user_id, invite_expires_at').eq('invite_token', token).limit(1);
    const row = data?.[0] as { id: string; email: string; user_id: string | null; invite_expires_at: string | null } | undefined;
    if (!row) return json({ ok: false, error: 'invalid' }, 404);
    if (row.user_id) return json({ ok: false, error: 'used' }, 409);
    if (row.invite_expires_at && Date.parse(row.invite_expires_at) < Date.now()) {
      return json({ ok: false, error: 'expired' }, 410);
    }
    // 招待されたアドレス以外のアカウントで承諾させない。
    // これを許すと、リンクを拾った第三者が自分のアカウントを紐づけられる
    if (String(row.email || '').toLowerCase() !== String(user.email || '').toLowerCase()) {
      return json({ ok: false, error: 'email_mismatch' }, 403);
    }

    const { error } = await admin.from('team_members')
      .update({ user_id: user.id, joined_at: new Date().toISOString(), invite_token: null, invite_expires_at: null })
      .eq('id', row.id);
    if (error) return json({ ok: false, error: 'update_failed' }, 500);
    return json({ ok: true });
  }

  /* ---------- スタッフを招待する（要オーナーのJWT） ---------- */
  if (action === 'invite') {
    if (!bearer) return json({ ok: false, error: 'no_auth' }, 401);
    const { data: ures } = await admin.auth.getUser(bearer);
    const user = ures?.user;
    if (!user) return json({ ok: false, error: 'invalid_token' }, 401);

    const addr = String(email || '').trim().toLowerCase();
    if (!addr || !addr.includes('@')) return json({ ok: false, error: 'bad_email' }, 400);

    // 招待できるのはクラブの代表者だけ
    const { data: teams } = await admin.from('teams').select('id, name, user_id').eq('id', team_id).limit(1);
    const team = teams?.[0] as { id: string; name: string; user_id: string } | undefined;
    if (!team) return json({ ok: false, error: 'team_not_found' }, 404);
    if (team.user_id !== user.id) return json({ ok: false, error: 'not_owner' }, 403);

    const inviteToken = crypto.randomUUID();
    const expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString();

    // 既に通知先として登録済みなら、その行に招待を発行する
    const { data: exist } = await admin.from('team_members')
      .select('id, user_id').eq('team_id', team.id).ilike('email', addr).limit(1);
    const existing = exist?.[0] as { id: string; user_id: string | null } | undefined;
    if (existing?.user_id) return json({ ok: false, error: 'already_joined' }, 409);

    if (existing) {
      const { error } = await admin.from('team_members')
        .update({ invite_token: inviteToken, invite_expires_at: expires, role: role === 'owner' ? 'owner' : 'staff', name: name || null })
        .eq('id', existing.id);
      if (error) return json({ ok: false, error: 'update_failed', detail: error.message }, 500);
    } else {
      const { error } = await admin.from('team_members').insert({
        team_id: team.id, email: addr, name: name || null,
        role: role === 'owner' ? 'owner' : 'staff', notify: true,
        invite_token: inviteToken, invite_expires_at: expires,
      });
      if (error) return json({ ok: false, error: 'insert_failed', detail: error.message }, 500);
    }

    const link = `${SITE}/join-club.html?token=${inviteToken}`;

    // 検証用アカウントから実在の相手には送らない
    const inviterIsTest = isTestAddr(user.email || '');
    if (inviterIsTest && !isTestAddr(addr)) {
      return json({ ok: true, mail: 'skipped_test_account_to_real_recipient', link });
    }
    if (!RESEND_API_KEY) return json({ ok: true, mail: 'skipped_no_key', link });

    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${RESEND_API_KEY}` },
      body: JSON.stringify({
        from: 'チビスポ <info@chibispo.com>',
        to: addr,
        subject: `【チビスポ】${team.name} のスタッフに招待されました`,
        html: `
          <div style="font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Noto Sans JP',sans-serif;background:#fafbfc;padding:28px 16px;">
            <div style="max-width:520px;margin:0 auto;background:#ffffff;border:1px solid #edf0f4;border-radius:16px;padding:28px 24px;">
              <div style="font-size:19px;font-weight:800;color:#f0435c;letter-spacing:.04em;">チビスポ</div>
              <h1 style="font-size:17px;font-weight:700;color:#21315b;margin:18px 0 0;">${team.name} のスタッフに招待されました</h1>
              <p style="font-size:13.5px;line-height:1.9;color:#4a5468;margin:14px 0 0;">
                下のボタンから参加すると、体験申込みの確認と保護者への返信ができるようになります。<br>
                はじめての方は、その場でパスワードを決めるだけで参加できます。
              </p>
              <p style="margin:24px 0 0;">
                <a href="${link}" style="display:inline-block;background:#f0435c;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:13px 28px;border-radius:12px;">
                  クラブに参加する
                </a>
              </p>
              <hr style="border:none;border-top:1px solid #edf0f4;margin:22px 0 0;">
              <p style="font-size:11.5px;line-height:1.8;color:#7a8299;margin:16px 0 0;">
                このリンクは7日間有効です。<br>
                心当たりがない場合は、このメールを破棄してください。リンクを開かない限り何も起こりません。
              </p>
              <p style="font-size:11px;color:#9aa1b2;margin:16px 0 0;">
                チビスポ ／ <a href="${SITE}" style="color:#9aa1b2;">chibispo.com</a>
              </p>
            </div>
          </div>`,
      }),
    });
    return json({ ok: true, mail: r.status });
  }

  return json({ ok: false, error: 'unknown_action' }, 400);
});
