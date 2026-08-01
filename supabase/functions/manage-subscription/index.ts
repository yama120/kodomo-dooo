// チビスポ内で完結するプラン変更・解約。club-mypageの「プラン管理」から呼ぶ。
//   action='status' … 現在のプラン/状態を返す
//   action='switch' plan=std_m|std_y|pro_m|pro_y … サブスクを別プランに切替（日割り）
//   action='cancel' … 請求期間の終了時に解約（それまでは利用可）
// 実行後、クラブの連絡先メールに確認メールを送る（Resend）。
//
// 認証：ログインユーザーのaccess_tokenを検証 → 本人のteam → そのstripe_customer_idのサブスクのみ操作。
// デプロイ： supabase functions deploy manage-subscription --no-verify-jwt

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const SB_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const ANON_KEY = Deno.env.get('SUPABASE_ANON_KEY')!;
const STRIPE_SECRET_KEY = Deno.env.get('STRIPE_SECRET_KEY')!;
const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY') || '';

const PRICES: Record<string, { id: string; label: string }> = {
  std_m: { id: 'price_1Tnpl0FUkIpaH1EAcaa3lQv8', label: 'スタンダード（月額 ¥3,000）' },
  std_y: { id: 'price_1TnqXbFUkIpaH1EAY1hsSqRp', label: 'スタンダード（年額 ¥30,000）' },
  pro_m: { id: 'price_1TpNfSFUkIpaH1EAu8JH2yzn', label: 'プロ（月額 ¥10,000）' },
  pro_y: { id: 'price_1TpNlLFUkIpaH1EAo8Ib6b4H', label: 'プロ（年額 ¥100,000）' },
};

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
function json(obj: unknown, status: number) {
  return new Response(JSON.stringify(obj), { status, headers: { ...CORS, 'Content-Type': 'application/json' } });
}

async function stripe(method: string, path: string, params?: Record<string, string>) {
  const res = await fetch(`https://api.stripe.com/v1/${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${STRIPE_SECRET_KEY}`,
      ...(params ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}),
    },
    body: params ? new URLSearchParams(params).toString() : undefined,
  });
  return { ok: res.ok, data: await res.json() };
}

async function sendClubEmail(to: string, subject: string, html: string) {
  if (!RESEND_API_KEY || !to) return;
  try {
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: 'Chibispo <info@chibispo.com>', to: [to], subject, html }),
    });
  } catch (_) { /* 送信失敗は握りつぶす（本処理は成立済み） */ }
}

function fmtDate(unix: number) {
  const d = new Date((unix || 0) * 1000);
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

// 新API(2026+)では current_period_end は items 側にある。両対応で取得。
function periodEnd(sub: any): number | null {
  return sub?.items?.data?.[0]?.current_period_end ?? sub?.current_period_end ?? null;
}

// 期間終了 + 3日の猶予（支払いリトライ用）。webhookと同じ基準。
function graceExpiry(periodEndUnix: number | null): string {
  const d = periodEndUnix ? new Date(periodEndUnix * 1000) : new Date();
  d.setDate(d.getDate() + 3);
  return d.toISOString();
}

// teams を service_role で更新（有効期限の自己修復用）
async function patchTeam(teamId: string, body: Record<string, unknown>) {
  try {
    await fetch(`${SB_URL}/rest/v1/teams?id=eq.${teamId}`, {
      method: 'PATCH',
      headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (_) { /* 同期失敗は無視（本処理には影響なし） */ }
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405, headers: CORS });

  try {
    // 認証
    const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
    if (!token) return json({ error: 'no_token' }, 401);
    const uRes = await fetch(`${SB_URL}/auth/v1/user`, { headers: { apikey: ANON_KEY, Authorization: `Bearer ${token}` } });
    const user = uRes.ok ? await uRes.json() : null;
    if (!user?.id) return json({ error: 'unauthorized' }, 401);

    const payload = await req.json().catch(() => ({}));
    const action = payload.action as string;
    const planKey = payload.plan as string;
    const teamId = payload.team_id as string | undefined; // 複数チーム対応：操作対象を指定

    // 本人のteam → stripe_customer_id
    const tRes = await fetch(
      `${SB_URL}/rest/v1/teams?user_id=eq.${user.id}&select=id,email,name,stripe_customer_id&order=created_at.desc`,
      { headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}` } }
    );
    const teams = tRes.ok ? await tRes.json() : [];
    // team_id 指定があればそのチーム（本人所有＋支払い情報あり）を対象に。無ければ支払い情報を持つ先頭。
    const team = Array.isArray(teams)
      ? (teamId
          ? teams.find((t: any) => t.id === teamId && t.stripe_customer_id)
          : teams.find((t: any) => t.stripe_customer_id))
      : null;
    if (!team?.stripe_customer_id) return json({ error: 'no_customer', message: 'お支払い情報が見つかりません。' }, 404);

    // 有効なサブスクを取得
    const subList = await stripe('GET', `subscriptions?customer=${team.stripe_customer_id}&status=all&limit=10`);
    const subs = subList.data?.data || [];
    const sub = subs.find((s: any) => ['active', 'trialing', 'past_due'].includes(s.status));
    if (!sub) return json({ error: 'no_subscription', message: '有効なサブスクリプションが見つかりません。' }, 404);

    const curPriceId = sub.items?.data?.[0]?.price?.id;
    const curKey = Object.keys(PRICES).find((k) => PRICES[k].id === curPriceId) || null;

    // ---- 状態取得 ----
    if (action === 'status') {
      const pe = periodEnd(sub);
      // DBの有効期限をStripeの実データに同期（旧バグ値の自己修復＋Webhook取りこぼしの保険）
      const dbPlan = curKey ? (curKey.startsWith('pro') ? 'pr-plus' : 'pr') : null;
      if (pe) await patchTeam(team.id, { plan_expires_at: graceExpiry(pe), ...(dbPlan ? { plan: dbPlan } : {}) });
      return json({ ok: true, status: sub.status, cancel_at_period_end: !!sub.cancel_at_period_end, current: curKey, period_end: pe });
    }

    // ---- 解約の取り消し（再開）----
    if (action === 'reactivate') {
      const r = await stripe('POST', `subscriptions/${sub.id}`, { cancel_at_period_end: 'false' });
      if (!r.ok) return json({ error: 'stripe_error', detail: r.data }, 500);
      await sendClubEmail(team.email, '【チビスポ】解約を取り消しました',
        `<p>${team.name} 様</p><p>解約の予約を取り消しました。これまで通り継続してご利用いただけます。</p><p>チビスポ</p>`);
      return json({ ok: true, message: '解約を取り消しました。これまで通りご利用いただけます。', cancel_at_period_end: false });
    }

    // ---- プラン変更 ----
    if (action === 'switch') {
      const p = PRICES[planKey];
      if (!p) return json({ error: 'bad_plan' }, 400);
      if (curKey === planKey) return json({ ok: true, message: 'すでにこのプランをご利用中です。', current: curKey });
      const itemId = sub.items?.data?.[0]?.id;
      const r = await stripe('POST', `subscriptions/${sub.id}`, {
        'items[0][id]': itemId,
        'items[0][price]': p.id,
        cancel_at_period_end: 'false',
        proration_behavior: 'create_prorations',
      });
      if (!r.ok) return json({ error: 'stripe_error', detail: r.data }, 500);
      await sendClubEmail(team.email, '【チビスポ】プランを変更しました',
        `<p>${team.name} 様</p><p>掲載プランを「<strong>${p.label}</strong>」に変更しました。差額は日割りで調整されます。</p><p>チビスポ</p>`);
      return json({ ok: true, message: `「${p.label}」に変更しました。`, current: planKey });
    }

    // ---- 解約（期間終了時）----
    if (action === 'cancel') {
      const r = await stripe('POST', `subscriptions/${sub.id}`, { cancel_at_period_end: 'true' });
      if (!r.ok) return json({ error: 'stripe_error', detail: r.data }, 500);
      const endStr = fmtDate(periodEnd(sub));
      await sendClubEmail(team.email, '【チビスポ】解約を受け付けました',
        `<p>${team.name} 様</p><p>掲載プランの解約を受け付けました。<br><strong>${endStr}</strong>まではこれまで通りご利用いただけ、その後は自動でフリープランに切り替わります（掲載自体は無料で継続されます）。</p><p>またのご利用をお待ちしております。<br>チビスポ</p>`);
      return json({ ok: true, message: `解約を受け付けました。${endStr}までご利用いただけます。`, cancel_at_period_end: true });
    }

    return json({ error: 'bad_action' }, 400);
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
