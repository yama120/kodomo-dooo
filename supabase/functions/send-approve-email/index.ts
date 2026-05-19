import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, content-type',
      },
    });
  }

  const { to_email, team_name, mypage_url } = await req.json();

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'チビスポ <info@chibispo.com>',
      reply_to: 'info@chibispo.com',
      to: to_email,
      subject: `【チビスポ】${team_name} の掲載が承認されました`,
      html: `
        <h2>掲載承認のお知らせ</h2>
        <p>${team_name} のチビスポへの掲載が承認されました。</p>
        <p>マイページから情報の編集・確認ができます。</p>
        <p style="margin-top:20px;">
          <a href="${mypage_url}" style="background:#FF8C1A;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;">マイページへ</a>
        </p>

        <div style="margin-top:30px;padding:18px 20px;background:#fff7ed;border-left:4px solid #ff8c1a;border-radius:6px;">
          <p style="margin:0 0 10px;font-weight:bold;color:#c2410c;">【重要】今後の通知メールについて</p>
          <p style="margin:0 0 10px;font-size:14px;color:#475569;line-height:1.7;">
            保護者から体験申込み・お問い合わせがあると、チビスポから <strong>info@chibispo.com</strong> で通知メールが届きます。
          </p>
          <p style="margin:0;font-size:14px;color:#475569;line-height:1.7;">
            迷惑メールフォルダに振り分けられないよう、お手数ですが以下のアドレスを連絡先に追加してください。
          </p>
          <p style="margin:12px 0 0;font-size:15px;font-weight:bold;text-align:center;">📧 info@chibispo.com</p>
        </div>

        <hr style="margin-top:30px;border:none;border-top:1px solid #eee;" />
        <p style="color:#999;font-size:12px;">チビスポ｜子どもスポーツクラブ情報プラットフォーム<br>https://chibispo.com</p>
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
