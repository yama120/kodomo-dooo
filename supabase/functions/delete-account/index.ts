import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// アカウント削除：呼び出し元のJWTを検証し、そのユーザー自身のデータのみを削除・匿名化する。
// service_role は Supabase が Edge Function に自動注入する環境変数を使用（クライアントには出さない）。
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });

  try {
    const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
    if (!token) return json({ ok: false, error: 'no_token' }, 401);

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

    // JWTからユーザーを特定（本人以外のデータは触れない）
    const { data: ures, error: uerr } = await admin.auth.getUser(token);
    if (uerr || !ures.user) return json({ ok: false, error: 'invalid_token' }, 401);
    const uid = ures.user.id;
    const email = ures.user.email || null;

    const steps: Record<string, string> = {};

    // 1) コメント（口コミ）：削除ではなく匿名化してスレッドの整合性を保つ
    try {
      const { error } = await admin.from('comments')
        .update({ nickname: '退会したユーザー', user_id: null }).eq('user_id', uid);
      steps.comments = error ? error.message : 'anonymized';
    } catch (e) { steps.comments = String(e); }

    // 2) お気に入り：削除
    try {
      const { error } = await admin.from('favorites').delete().eq('user_id', uid);
      steps.favorites = error ? error.message : 'deleted';
    } catch (e) { steps.favorites = String(e); }

    // 3) プッシュ通知トークン：削除（テーブル未作成なら skip）
    try {
      const { error } = await admin.from('push_tokens').delete().eq('user_id', uid);
      steps.push_tokens = error ? ('skip:' + error.message) : 'deleted';
    } catch (e) { steps.push_tokens = 'skip:' + String(e); }

    // 4) 体験申込：法令・トラブル対応のため個人特定情報のみ匿名化して保持（emailで突合）
    if (email) {
      try {
        const { error } = await admin.from('trial_requests')
          .update({ parent_name: '（削除済み）', parent_email: null, parent_phone: null, child_name: null })
          .eq('parent_email', email);
        steps.trial_requests = error ? error.message : 'anonymized';
      } catch (e) { steps.trial_requests = String(e); }
    }

    // 5) クラブ運営者の場合：所有クラブを非公開化（データは残すが公開停止）
    try {
      const { data: teams } = await admin.from('teams').select('id').eq('user_id', uid);
      if (teams && teams.length) {
        const { error } = await admin.from('teams').update({ status: 'archived' }).eq('user_id', uid);
        steps.teams = error ? error.message : `archived:${teams.length}`;
      } else {
        steps.teams = 'none';
      }
    } catch (e) { steps.teams = String(e); }

    // 6) プロフィール削除
    try {
      const { error } = await admin.from('profiles').delete().eq('id', uid);
      steps.profile = error ? error.message : 'deleted';
    } catch (e) { steps.profile = String(e); }

    // 7) 認証ユーザー削除（最後）
    const { error: delErr } = await admin.auth.admin.deleteUser(uid);
    if (delErr) return json({ ok: false, error: 'auth_delete_failed', detail: delErr.message, steps }, 500);

    return json({ ok: true, steps });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
