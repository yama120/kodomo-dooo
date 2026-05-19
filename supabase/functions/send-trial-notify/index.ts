import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;
const ADMIN_EMAIL = 'moyori.info@gmail.com';

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, content-type',
      },
    });
  }

  const {
    type,
    team_name,
    team_email,
    team_instagram,
    sport,
    pref,
    city,
    parent_name,
    parent_email,
    child_name,
    child_name_kana,
    child_age,
    child_grade,
    message,
  } = await req.json();

  const isTrial = (type || 'trial') === 'trial';
  const typeLabel = isTrial ? '体験申込み' : 'お問い合わせ';
  const typeLabelEmoji = isTrial ? '🎉 体験申込み' : '💬 お問い合わせ';

  const results = [];

  // 1) クラブ運営者に通知（保護者の個人情報は載せない・マイページへ誘導）
  if (team_email) {
    try {
      const clubRes = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: 'チビスポ <info@chibispo.com>',
          to: team_email,
          subject: `【チビスポ】新しい${typeLabel}が届きました：${team_name}`,
          html: `
            <h2 style="color:#ff6b00;">新しい${typeLabel}が届きました</h2>
            <p>${team_name}様</p>
            <p>チビスポ経由で${typeLabel}が届きました。<br/>
            <strong>保護者の個人情報保護のため、内容はマイページでご確認ください。</strong></p>
            <table style="border-collapse:collapse;width:100%;max-width:500px;margin:16px 0;">
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>
            </table>
            <p style="margin-top:20px;">
              <a href="https://chibispo.com/mypage.html" style="background:#ff8c1a;color:#fff;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:bold;display:inline-block;">マイページで詳細を確認する</a>
            </p>
            <p style="font-size:13px;color:#64748b;margin-top:24px;">
              ※ご対応のほどよろしくお願いいたします。<br/>
              ※なるべく早めのご連絡をお願いします。
            </p>
            <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;" />
            <p style="font-size:12px;color:#94a3b8;">このメールはチビスポ（https://chibispo.com）から自動送信されています。</p>
          `,
        }),
      });
      results.push({ to: 'club', status: clubRes.status });
    } catch (e) {
      results.push({ to: 'club', error: String(e) });
    }
  }

  // 2) 保護者に受付完了通知（クラブのメアドは載せない）
  try {
    const trialRows = isTrial ? `
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">お子さまのお名前</td><td style="padding:8px;border:1px solid #ddd;">${child_name || '—'}${child_name_kana ? `（${child_name_kana}）` : ''}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">学年・年齢</td><td style="padding:8px;border:1px solid #ddd;">${child_age}歳・${child_grade}</td></tr>` : '';

    const parentRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'チビスポ <info@chibispo.com>',
        to: parent_email,
        subject: `【チビスポ】${typeLabel}を受け付けました：${team_name}`,
        html: `
          <h2 style="color:#ff6b00;">${typeLabel}を受け付けました</h2>
          <p>${parent_name}様</p>
          <p>このたびは「<strong>${team_name}</strong>」への${typeLabel}ありがとうございます。</p>
          <p>内容はクラブに通知されており、数日以内にクラブから直接ご${isTrial ? '連絡' : '返信'}が入ります。<br/>
          しばらくお待ちください。</p>
          <table style="border-collapse:collapse;width:100%;max-width:500px;margin:16px 0;">
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">クラブ名</td><td style="padding:8px;border:1px solid #ddd;">${team_name}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fff7ed;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>${trialRows}
          </table>
          <p style="font-size:13px;color:#64748b;margin-top:24px;">
            ※返信メールは${team_name}から直接届きます。<br/>
            ※迷惑メールフォルダもご確認ください。<br/>
            ※数日たっても連絡がない場合は <a href="mailto:info@chibispo.com">info@chibispo.com</a> までご連絡ください。
          </p>
          <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;" />
          <p style="font-size:12px;color:#94a3b8;">このメールはチビスポ（https://chibispo.com）から自動送信されています。</p>
        `,
      }),
    });
    results.push({ to: 'parent', status: parentRes.status });
  } catch (e) {
    results.push({ to: 'parent', error: String(e) });
  }

  // 3) 管理者（運営）に通知
  try {
    const childRow = isTrial
      ? `<tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">お子さま</td><td style="padding:8px;border:1px solid #ddd;">${child_name || '—'}${child_name_kana ? `（${child_name_kana}）` : ''}・${child_age}歳・${child_grade}</td></tr>`
      : '';
    const messageRow = message
      ? `<tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">メッセージ</td><td style="padding:8px;border:1px solid #ddd;">${message}</td></tr>`
      : '';

    const adminRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'チビスポ <info@chibispo.com>',
        to: ADMIN_EMAIL,
        subject: `【チビスポ管理】新規${typeLabel}：${team_name}`,
        html: `
          <h2>新規${typeLabel}</h2>
          <table style="border-collapse:collapse;width:100%;max-width:500px;">
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">クラブ</td><td style="padding:8px;border:1px solid #ddd;">${team_name}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">クラブ連絡先</td><td style="padding:8px;border:1px solid #ddd;">${team_email || (team_instagram ? `Instagram: @${team_instagram}` : '未登録')}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">保護者</td><td style="padding:8px;border:1px solid #ddd;">${parent_name}（${parent_email}）</td></tr>
            ${childRow}
            ${messageRow}
          </table>
          <p style="margin-top:20px;"><a href="https://chibispo.com/admin.html" style="background:#ff8c1a;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;">管理画面で確認する</a></p>
        `,
      }),
    });
    results.push({ to: 'admin', status: adminRes.status });
  } catch (e) {
    results.push({ to: 'admin', error: String(e) });
  }

  return new Response(JSON.stringify({ results }), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
});
