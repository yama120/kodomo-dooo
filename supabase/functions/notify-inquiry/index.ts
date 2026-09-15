/* お問い合わせ（inquiries）と、準備中サービスのお知らせ登録（waitlist）を管理者にメールで知らせる。
   - 宛先は固定（ADMIN_EMAIL）。リクエストで宛先は指定できない＝第三者への送信に使えない
   - 本文はすべてエスケープして埋める。長すぎる入力は切り詰める
   - 返信先に申込者のメールを入れるので、受信メールからそのまま返信できる */
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;
const ADMIN_EMAIL = 'moyori.info@gmail.com';
const FROM = 'チビスポ <info@chibispo.com>';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type, apikey, x-client-info',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

const esc = (v: unknown, max = 2000) =>
  String(v ?? '')
    .slice(0, max)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

const isEmail = (v: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

/* 相談したいことの内部値 → 表示名 */
const KIND_LABEL: Record<string, string> = {
  listing: '掲載について', sns: 'SNS運用サポート', hp: 'ホームページ制作',
  video: '撮影・動画制作', plan: '有料プランの変更', fix: '情報の修正', other: 'その他',
  ads: '広告掲載・取材', consult: '相談',
};
/* 準備中サービスの topic → 表示名 */
const TOPIC_LABEL: Record<string, string> = {
  video: '撮影・動画制作', sns: 'SNS運用サポート', hp: 'ホームページ制作', ads: '地域の広告掲載',
};

function row(k: string, v: string) {
  if (!v) return '';
  return `<tr><td style="padding:8px 10px;border:1px solid #e5e8ec;background:#f7f8fa;font-weight:700;white-space:nowrap">${k}</td>`
       + `<td style="padding:8px 10px;border:1px solid #e5e8ec">${v}</td></tr>`;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return new Response('method not allowed', { status: 405, headers: CORS });

  let body: Record<string, unknown> = {};
  try { body = await req.json(); } catch { /* 空でも落とさない */ }

  const type = String(body.type || 'inquiry');
  const email = String(body.email || '').slice(0, 200).trim();
  const replyTo = isEmail(email) ? email : undefined;

  let subject = '';
  let lead = '';
  let table = '';

  if (type === 'waitlist') {
    const topic = String(body.topic || '');
    const label = TOPIC_LABEL[topic] || topic || '準備中のサービス';
    subject = `【チビスポ】お知らせ登録：${label}`;
    lead = '準備中のサービスに「お知らせを受け取る」の登録がありました。';
    table = row('サービス', esc(label, 100)) + row('メール', esc(email, 200)) + row('登録元', esc(body.source, 300));
  } else {
    const kind = String(body.kind || '');
    /* topic はフォームに出ている日本語のまま（「掲載について」など）。無ければ kind から引く */
    const label = String(body.topic || '').slice(0, 60) || KIND_LABEL[kind] || kind || 'お問い合わせ';
    const who = String(body.who || '');
    subject = `【チビスポ】お問い合わせ：${label}`;
    lead = 'サイトのお問い合わせフォームから届きました。';
    table = row('相談したいこと', esc(label, 100))
          + row('立場', esc({ club: 'クラブ運営者', biz: '地域のお店・企業', parent: '保護者', other: 'その他・取材' }[who] || who, 60))
          + row('クラブ名・団体名', esc(body.org, 200))
          + row('お名前', esc(body.name, 100))
          + row('メール', esc(email, 200))
          + row('電話', esc(body.phone, 60))
          + row('プラン', esc(body.plan, 100))
          + row('内容', esc(body.message, 4000).replace(/\n/g, '<br>'));
  }

  const html = `
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans',sans-serif;color:#1f2430;line-height:1.7">
      <p style="margin:0 0 14px">${lead}</p>
      <table style="border-collapse:collapse;width:100%;max-width:620px;font-size:14px">${table}</table>
      <p style="margin:18px 0 0;font-size:12px;color:#7b8492">このメールに返信すると、申込者に直接届きます。</p>
    </div>`;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: ADMIN_EMAIL, subject, html, ...(replyTo ? { reply_to: replyTo } : {}) }),
  });

  const data = await res.json().catch(() => ({}));
  return new Response(JSON.stringify({ ok: res.ok, data }), {
    status: res.ok ? 200 : 502,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
});
