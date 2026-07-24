import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// チャット新着メッセージの相手へプッシュ通知。
// 呼び出し元のJWTで送信者を特定し、申込のもう一方（保護者 or クラブ）へ send-push する。
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const ANON = Deno.env.get('SUPABASE_ANON_KEY')!;
const PUSH_SECRET = Deno.env.get('PUSH_TRIGGER_SECRET') || '';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', ...cors } });

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
    if (!token) return json({ ok: false, error: 'no_token' }, 401);
    const { trial_id, body } = await req.json();
    if (!trial_id) return json({ ok: false, error: 'no_trial' }, 400);

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });
    const { data: ures } = await admin.auth.getUser(token);
    if (!ures.user) return json({ ok: false, error: 'invalid_token' }, 401);
    const senderUid = ures.user.id;

    // 申込とクラブ所有者を取得
    const { data: trs } = await admin.from('trial_requests').select('user_id, team_id, parent_name').eq('id', trial_id).limit(1);
    const tr = trs?.[0];
    if (!tr) return json({ ok: false, error: 'trial_not_found' }, 404);
    const { data: teams } = await admin.from('teams').select('user_id, name').eq('id', tr.team_id).limit(1);
    const team = teams?.[0];

    const preview = (body || '').slice(0, 60);
    let target: { team_id?: string; user_id?: string; title: string } | null = null;

    if (team && senderUid === team.user_id) {
      // クラブ→保護者
      if (!tr.user_id) return json({ ok: true, sent: 0, note: 'parent_no_account' });
      target = { user_id: tr.user_id, title: `${team.name}からメッセージ` };
    } else {
      // 保護者→クラブ
      target = { team_id: tr.team_id, title: `${tr.parent_name || '保護者'}さんからメッセージ` };
    }

    const pr = await fetch(`${SUPABASE_URL}/functions/v1/send-push`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', apikey: ANON, Authorization: `Bearer ${ANON}` },
      body: JSON.stringify({ ...target, body: preview, data: { kind: 'message', trial_id }, secret: PUSH_SECRET }),
    });
    const pj = await pr.json().catch(() => ({}));
    return json({ ok: true, push: pj });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
