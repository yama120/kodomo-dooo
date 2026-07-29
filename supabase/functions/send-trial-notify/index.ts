import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;
const ADMIN_EMAIL = 'moyori.info@gmail.com';

/* クラブの通知先を team_members から引く。
   担当者が1人しか登録できないと、その人が交代した時点で申込通知が
   誰にも届かなくなり、しかもクラブ側は気づけない。
   team_members が空・未作成のときは、呼び出し元が渡した team_email に落とす。 */
async function resolveClubEmails(teamId: string, fallback: string): Promise<string[]> {
  const url = Deno.env.get('SUPABASE_URL');
  const key = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
  const fb = String(fallback || '').trim();
  const fbList = fb ? [fb.toLowerCase()] : [];
  if (!url || !key || !teamId) return fbList;
  try {
    const r = await fetch(
      `${url}/rest/v1/team_members?team_id=eq.${encodeURIComponent(teamId)}&notify=is.true&select=email`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } },
    );
    if (!r.ok) return fbList;
    const rows = await r.json();
    const list = (Array.isArray(rows) ? rows : [])
      .map((m: { email?: string }) => String(m.email || '').trim().toLowerCase())
      .filter(Boolean);
    return list.length ? [...new Set(list)] : fbList;
  } catch {
    return fbList;
  }
}

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
    team_id,
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

  /* 検証用アカウントからの申込では、実在クラブにメールを飛ばさない。
     2026-07-28、動作確認のつもりで実在クラブ（誠空会）に架空の申込通知を
     送ってしまった。運用ルールだけでは同じ事故が起きるのでサーバ側で止める。
     テスト用クラブ（テストFC）宛は従来どおり送るので検証は続けられる。 */
  const TEST_SENDERS = ['app-parent-test@chibispo.com', 'app-test@chibispo.com'];
  const TEST_TEAM_IDS = ['129e5f93-1f0e-4606-8edc-a770e765e644'];   // テストFC
  const fromTestAccount = TEST_SENDERS.includes(String(parent_email || '').toLowerCase());
  const toTestTeam = TEST_TEAM_IDS.includes(String(team_id || ''));
  const blockRealClubMail = fromTestAccount && !toTestTeam;

  const results = [];

  // クラブの通知先（複数可）。登録がなければ呼び出し元の team_email に落とす
  const clubEmails = await resolveClubEmails(String(team_id || ''), String(team_email || ''));

  // 1) クラブ運営者に通知（保護者の個人情報は載せない・マイページへ誘導）
  if (blockRealClubMail) {
    results.push({ to: 'club', skipped: 'test_account_to_real_club' });
  } else if (clubEmails.length) {
    try {
      const clubRes = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: 'チビスポ <info@chibispo.com>',
          to: clubEmails,
          subject: `【チビスポ】新しい${typeLabel}が届きました：${team_name}`,
          html: `
            <h2 style="color:#ff6b00;">新しい${typeLabel}が届きました</h2>
            <p>${team_name}様</p>
            <p>チビスポ経由で${typeLabel}が届きました。<br/>
            <strong>保護者の個人情報保護のため、内容はマイページでご確認ください。</strong></p>
            <table style="border-collapse:collapse;width:100%;max-width:500px;margin:16px 0;">
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
              <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>
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
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">お子さまのお名前</td><td style="padding:8px;border:1px solid #ddd;">${child_name || '—'}${child_name_kana ? `（${child_name_kana}）` : ''}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">学年・年齢</td><td style="padding:8px;border:1px solid #ddd;">${child_age}歳・${child_grade}</td></tr>` : '';

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
          <h2 style="color:#f0435c;">${typeLabel}を受け付けました</h2>
          <p>${parent_name}様</p>
          <p>このたびは「<strong>${team_name}</strong>」への${typeLabel}ありがとうございます。</p>
          <p>内容はクラブに通知されており、数日以内にクラブからご${isTrial ? '連絡' : '返信'}が入ります。<br/>
          しばらくお待ちください。</p>

          <div style="background:#fdedef;border-radius:12px;padding:16px 18px;margin:18px 0;max-width:500px;">
            <p style="margin:0 0 6px;font-size:14px;font-weight:bold;color:#21315b;">マイページでクラブとやり取りできます</p>
            <p style="margin:0 0 12px;font-size:13px;line-height:1.8;color:#4a5468;">
              日程の相談や質問は、メールではなくマイページのメッセージでやり取りできます。
              メールアドレスを相手に知らせずに済み、やり取りが1か所にまとまります。
            </p>
            <a href="https://chibispo.com/mypage.html"
               style="display:inline-block;background:#f0435c;color:#ffffff;text-decoration:none;font-size:14px;font-weight:bold;padding:11px 24px;border-radius:10px;">
              マイページを開く
            </a>
            <p style="margin:10px 0 0;font-size:11.5px;color:#7a8299;">
              ※このメールアドレス（${parent_email}）でログインすると、この申込が表示されます。
            </p>
          </div>
          <table style="border-collapse:collapse;width:100%;max-width:500px;margin:16px 0;">
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">クラブ名</td><td style="padding:8px;border:1px solid #ddd;">${team_name}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;background:#fdedef;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>${trialRows}
          </table>
          <p style="font-size:13px;color:#64748b;margin-top:24px;">
            ※クラブからの返信は、マイページのメッセージまたはメールで届きます。<br/>
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
        subject: `${fromTestAccount ? '【テスト】' : ''}【チビスポ管理】新規${typeLabel}：${team_name}`,
        html: `
          <h2>新規${typeLabel}</h2>
          <table style="border-collapse:collapse;width:100%;max-width:500px;">
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">種別</td><td style="padding:8px;border:1px solid #ddd;">${typeLabelEmoji}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">クラブ</td><td style="padding:8px;border:1px solid #ddd;">${team_name}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">種目</td><td style="padding:8px;border:1px solid #ddd;">${sport}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">エリア</td><td style="padding:8px;border:1px solid #ddd;">${pref} ${city}</td></tr>
            <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold;">クラブ通知先</td><td style="padding:8px;border:1px solid #ddd;">${clubEmails.length ? clubEmails.join('<br>') : (team_instagram ? `Instagram: @${team_instagram}` : '<strong style="color:#c0314b;">未登録（通知が届いていません）</strong>')}</td></tr>
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

  // 4) クラブ運営者にプッシュ通知（アプリ版・トークンがあれば）
  if (isTrial && team_id) {
    try {
      const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
      const ANON = Deno.env.get('SUPABASE_ANON_KEY')!;
      const secret = Deno.env.get('PUSH_TRIGGER_SECRET') || '';
      const pr = await fetch(`${SUPABASE_URL}/functions/v1/send-push`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: ANON, Authorization: `Bearer ${ANON}` },
        body: JSON.stringify({
          team_id,
          title: '新しい体験申込が届きました',
          body: `${team_name}に体験の申込がありました。受信箱で確認しましょう。`,
          data: { kind: 'trial', team_id },
          secret,
        }),
      });
      results.push({ to: 'push', status: pr.status });
    } catch (e) {
      results.push({ to: 'push', error: String(e) });
    }
  }

  return new Response(JSON.stringify({ results }), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
});
