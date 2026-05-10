import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;
const ADMIN_EMAIL = 'moyori.info@gmail.com'; // 管理者メールアドレス

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, content-type',
      },
    });
  }

  const { team_name, sport, pref, city, applicant_email } = await req.json();

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'チビスポ <info@chibispo.com>',
      to: ADMIN_EMAIL,
      subject: `【チビスポ】新規チーム申請：${team_name}`,
      html: `
        <h2>新規チーム申請がありました</h2>
        <table style="border-collapse:collapse;width:100%;max-width:500px;">
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">チーム名</td><td style="padding:8px;border:1px solid #ddd;">${team_name}</td></tr>
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">連絡先</td><td style="padding:8px;border:1px solid #ddd;">${applicant_email}</td></tr>
        </table>
        <p style="margin-top:20px;"><a href="https://chibispo.com/admin.html" style="background:#FF8C1A;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;">管理画面で確認する</a></p>
      `,
    }),
  });

  const data = await res.json();
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
});
