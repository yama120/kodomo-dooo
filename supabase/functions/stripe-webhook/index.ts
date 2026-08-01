// Stripe Webhook → teams.plan / plan_expires_at を自動反映
//
// 対応イベント：
//   checkout.session.completed        … Payment Link決済/申込完了（client_reference_id=teams.id）
//   customer.subscription.updated     … 更新・トライアル→本課金・プラン変更（期限と価格を同期）
//   customer.subscription.deleted     … 解約（期限まではプラン維持→自動でfree化）
//
// ★トライアル対応：初月無料でも「申し込んだ瞬間」にプランを立てる。
//   請求額ではなく、サブスクの price.unit_amount（トライアル中でも定価が入る）で判定。
//   3,000/30,000 → pr、10,000/100,000 → pr-plus。単発(特集/企業)は管理者メール通知のみ。
//
// 使うシークレット：
//   SUPABASE_SERVICE_ROLE_KEY / SUPABASE_URL … Supabaseが自動注入（手動設定不要）
//   STRIPE_SECRET_KEY     … sk_live_...（サブスク取得用）
//   STRIPE_WEBHOOK_SECRET … whsec_...（署名検証）
//   RESEND_API_KEY        … 管理者通知（任意）
//
// カラム： alter table teams add column if not exists stripe_customer_id text;

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const SB_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!; // Supabase自動注入のservice_role
const STRIPE_SECRET_KEY = Deno.env.get('STRIPE_SECRET_KEY')!;
const WEBHOOK_SECRET = Deno.env.get('STRIPE_WEBHOOK_SECRET')!;
const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY') || '';
const ADMIN_EMAIL = 'moyori.info@gmail.com';

// ---- Stripe署名検証（v1, HMAC-SHA256）----
async function verifyStripeSignature(payload: string, sigHeader: string): Promise<boolean> {
  try {
    const parts = Object.fromEntries(sigHeader.split(',').map(kv => kv.split('=') as [string, string]));
    const t = parts['t']; const v1 = parts['v1'];
    if (!t || !v1) return false;
    if (Math.abs(Date.now() / 1000 - Number(t)) > 300) return false; // リプレイ対策
    const enc = new TextEncoder();
    const key = await crypto.subtle.importKey('raw', enc.encode(WEBHOOK_SECRET), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const mac = await crypto.subtle.sign('HMAC', key, enc.encode(`${t}.${payload}`));
    const hex = [...new Uint8Array(mac)].map(b => b.toString(16).padStart(2, '0')).join('');
    return hex === v1;
  } catch (_) { return false; }
}

// ---- Supabase REST（service role・ヘッダーは平易なオブジェクトで組む）----
async function sbPatch(pathWithQuery: string, bodyObj: Record<string, unknown>) {
  try {
    const res = await fetch(`${SB_URL}/rest/v1/${pathWithQuery}`, {
      method: 'PATCH',
      headers: {
        apikey: SERVICE_KEY,
        Authorization: `Bearer ${SERVICE_KEY}`,
        'Content-Type': 'application/json',
        Prefer: 'return=representation',
      },
      body: JSON.stringify(bodyObj),
    });
    const text = await res.text();
    return { ok: res.ok, status: res.status, body: text.slice(0, 300) };
  } catch (e) {
    return { ok: false, status: 0, body: String(e).slice(0, 200) };
  }
}

// ---- Stripe API GET（サブスク情報の取得）----
async function stripeGet(path: string): Promise<any | null> {
  try {
    const res = await fetch(`https://api.stripe.com/v1/${path}`, {
      headers: { Authorization: `Bearer ${STRIPE_SECRET_KEY}` },
    });
    return res.ok ? await res.json() : null;
  } catch (_) { return null; }
}

function planFromUnitAmount(amount: number): string | null {
  if (amount === 3000 || amount === 30000) return 'pr';
  if (amount === 10000 || amount === 100000) return 'pr-plus';
  return null;
}

function graceExpiry(periodEndUnix: number | null): string {
  const d = periodEndUnix ? new Date(periodEndUnix * 1000) : new Date();
  d.setDate(d.getDate() + 3);
  return d.toISOString();
}

function fmtDate(unix: number | null): string {
  const d = unix ? new Date(unix * 1000) : new Date();
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

// plan(pr/pr-plus) → 表示名
function planLabel(plan: string): string {
  return plan === 'pr-plus' ? 'プロ' : 'スタンダード';
}

// 定価から月額/年額を判定
function intervalLabel(unit: number): string {
  return (unit === 30000 || unit === 100000) ? '年額' : '月額';
}

// teams から連絡先・名前を取得
async function sbGet(pathWithQuery: string): Promise<any[]> {
  try {
    const res = await fetch(`${SB_URL}/rest/v1/${pathWithQuery}`, {
      headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}` },
    });
    return res.ok ? await res.json() : [];
  } catch (_) { return []; }
}

// クラブ本人への確認メール（Resend）
async function sendClubEmail(to: string, subject: string, html: string) {
  if (!RESEND_API_KEY || !to) return;
  try {
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: 'Chibispo <info@chibispo.com>', to: [to], subject, html }),
    });
  } catch (_) { /* 送信失敗は無視（本処理は成立済み） */ }
}

async function notifyAdmin(subject: string, body: string) {
  if (!RESEND_API_KEY) return;
  try {
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: 'Chibispo <info@chibispo.com>', to: [ADMIN_EMAIL], subject, html: `<pre style="font-family:sans-serif">${body}</pre>` }),
    });
  } catch (_) { /* 通知失敗は無視 */ }
}

serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 });
  const payload = await req.text();
  const sig = req.headers.get('stripe-signature') || '';
  if (!(await verifyStripeSignature(payload, sig))) {
    return new Response('Invalid signature', { status: 400 });
  }

  const event = JSON.parse(payload);
  const type = event.type as string;
  const obj = event.data?.object ?? {};

  try {
    // ===== 1) 申込/決済 完了 =====
    if (type === 'checkout.session.completed') {
      const teamId = obj.client_reference_id || null;
      const customer = obj.customer || null;
      const subId = obj.subscription || null;
      const email = obj.customer_details?.email || '';

      if (subId && teamId) {
        const sub = await stripeGet(`subscriptions/${subId}`);
        const item = sub?.items?.data?.[0];
        const unit = item?.price?.unit_amount ?? 0;
        const plan = planFromUnitAmount(unit);
        // 新API(2026+)では current_period_end は items 側。両対応で取得。
        const periodEnd = item?.current_period_end ?? sub?.current_period_end ?? null;
        const trialing = sub?.status === 'trialing';

        if (plan) {
          const upd = await sbPatch(`teams?id=eq.${teamId}`, {
            plan,
            plan_expires_at: graceExpiry(periodEnd),
            stripe_customer_id: customer,
          });
          await notifyAdmin(
            `[Chibispo] plan申込: ${plan}${trialing ? '(初月無料トライアル中)' : ''} / 定価${unit}`,
            `team_id: ${teamId}\nplan: ${plan}\nstatus: ${sub?.status}\nemail: ${email}\nteams更新: ${upd.ok ? 'OK(申込時点で即反映)' : 'FAILED(' + upd.status + ') ' + upd.body}`
          );

          // ▼ クラブ本人へ「〇〇プランに登録しました」の確認メール
          const rows = await sbGet(`teams?id=eq.${teamId}&select=name,email`);
          const team = rows[0] || {};
          const to = team.email || email;
          const label = planLabel(plan);       // スタンダード / プロ
          const iv = intervalLabel(unit);       // 月額 / 年額
          const priceStr = `¥${unit.toLocaleString()}`;
          const trialNote = trialing
            ? `<p>初回<strong>30日間は無料</strong>でご利用いただけます。無料期間の終了後（${fmtDate(periodEnd)}）に、自動で ${iv}${priceStr} の課金が始まります。</p>`
            : `<p>ご利用は ${fmtDate(periodEnd)} まで有効です（以降は自動更新されます）。</p>`;
          await sendClubEmail(to, `【チビスポ】${label}プランに登録しました`,
            `<p>${team.name || ''} 様</p>`
            + `<p>この度は<strong>${label}プラン（${iv} ${priceStr}）</strong>にお申し込みいただき、ありがとうございます。</p>`
            + trialNote
            + `<p>掲載内容の編集やプランの変更・解約は、いつでもマイページ（<a href="https://chibispo.com/club-mypage.html">club-mypage</a>）から行えます。</p>`
            + `<p>これからどうぞよろしくお願いいたします。<br>チビスポ</p>`);
        } else {
          await notifyAdmin(
            `[Chibispo] サブスク申込: 定価が対象外(手動対応)`,
            `team_id: ${teamId}\nunit_amount: ${unit}\nsubscription: ${subId}\nemail: ${email}`
          );
        }
      } else {
        await notifyAdmin(
          `[Chibispo] 単発決済(手動対応): ${Number(obj.amount_total ?? 0)}`,
          `client_reference_id: ${teamId || 'なし'}\nemail: ${email}\nmode: ${obj.mode}`
        );
      }
    }

    // ===== 2) サブスク更新（トライアル→本課金・更新・プラン変更）=====
    if (type === 'customer.subscription.updated') {
      const customer = obj.customer;
      const item = obj.items?.data?.[0];
      const unit = item?.price?.unit_amount ?? 0;
      const plan = planFromUnitAmount(unit);
      const periodEnd = item?.current_period_end ?? obj.current_period_end ?? null;
      if (customer) {
        const body: Record<string, unknown> = { plan_expires_at: graceExpiry(periodEnd) };
        if (plan) body.plan = plan;
        await sbPatch(`teams?stripe_customer_id=eq.${customer}`, body);
      }
    }

    // ===== 3) 解約完了（サブスク削除）→ freeに戻す =====
    // 「期間終了時に解約」は期間終了時、「即時解約」は即時にこのイベントが来る。
    // どちらのタイミングでも、削除された時点でフリープランに戻すのが正しい。
    if (type === 'customer.subscription.deleted') {
      const customer = obj.customer;
      if (customer) {
        const upd = await sbPatch(`teams?stripe_customer_id=eq.${customer}`, { plan: 'free', plan_expires_at: null });
        await notifyAdmin('[Chibispo] サブスク解約→フリーに戻しました', `stripe_customer: ${customer}\nteams更新: ${upd.ok ? 'OK(plan=free)' : 'FAILED(' + upd.status + ') ' + upd.body}`);
      }
    }

    return new Response(JSON.stringify({ received: true }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(`Webhook handler error: ${e}`, { status: 500 }); // 500ならStripeが自動リトライ
  }
});
