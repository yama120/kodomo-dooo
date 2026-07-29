import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// チャット新着メッセージの相手へプッシュ通知。
// 呼び出し元のJWTで送信者を特定し、申込のもう一方（保護者 or クラブ）へ send-push する。
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const ANON = Deno.env.get('SUPABASE_ANON_KEY')!;
const PUSH_SECRET = Deno.env.get('PUSH_TRIGGER_SECRET') || '';
const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY') || '';

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
    const { data: trs } = await admin.from('trial_requests')
      .select('user_id, team_id, parent_name, parent_email').eq('id', trial_id).limit(1);
    const tr = trs?.[0];
    if (!tr) return json({ ok: false, error: 'trial_not_found' }, 404);
    const { data: teams } = await admin.from('teams')
      .select('user_id, name, email').eq('id', tr.team_id).limit(1);
    const team = teams?.[0];

    const preview = (body || '').slice(0, 60);
    const isClubSender = !!team && senderUid === team.user_id;
    // ダミーアドレス（手動追加した申込）にはメールを送らない
    const rawParentEmail = (tr.parent_email as string | null) || '';
    const parentEmail = rawParentEmail && !rawParentEmail.endsWith('@chibispo.local') ? rawParentEmail : '';
    /* クラブ側の宛先。担当者が交代しても届くよう team_members から引く。
       teams.email 1件だけだと、その担当者が辞めた時点で通知が誰にも
       届かなくなり、しかもクラブは気づけない。
       team_members が未作成・空のときは従来どおり teams.email に落とす */
    const clubEmails: string[] = await (async () => {
      const { data } = await admin.from('team_members')
        .select('email, notify').eq('team_id', tr.team_id).eq('notify', true);
      const list = (data || []).map((m) => String(m.email || '').trim()).filter(Boolean);
      if (list.length) return [...new Set(list.map((e) => e.toLowerCase()))];
      const fallback = String(team?.email || '').trim();
      return fallback ? [fallback.toLowerCase()] : [];
    })();
    const clubEmail = clubEmails[0] || '';

    const target: { team_id?: string; user_id?: string; title: string } = isClubSender
      ? { user_id: (tr.user_id as string) || '', title: `${team?.name || 'クラブ'}からメッセージ` }
      : { team_id: tr.team_id as string, title: `${tr.parent_name || '保護者'}さんからメッセージ` };

    // プッシュは相手にアカウントがある場合だけ。無くてもメールは送るので中断しない
    let pj: unknown = { skipped: 'parent_no_account' };
    if (!isClubSender || tr.user_id) {
      const pr = await fetch(`${SUPABASE_URL}/functions/v1/send-push`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: ANON, Authorization: `Bearer ${ANON}` },
        body: JSON.stringify({ ...target, body: preview, kind: 'trial_reply', data: { kind: 'message', trial_id }, secret: PUSH_SECRET }),
      });
      pj = await pr.json().catch(() => ({}));
    }

    /* 新着メール。プッシュはネイティブアプリ限定なので、
       Webしか使っていない相手にはこれが唯一の気づく手段になる。
       本文は載せずリンクで開かせる（内容をメールに残さない）。 */
    let mail: unknown = { skipped: 'no_key' };
    if (RESEND_API_KEY) {
      /* 「前回この相手にメール通知したのがいつか」で判定する。
         直前メッセージの送信者で判定すると、スレッド1通目まで抑制されたり
         クライアントの挿入タイミングで判定がずれたりするため。
         テーブルが未作成でも通知自体は止めない（抑制が効かないだけ） */
      const toRole = isClubSender ? 'parent' : 'club';
      const { data: logRow } = await admin.from('message_notify_log')
        .select('last_sent_at').eq('trial_id', trial_id).eq('to_role', toRole).limit(1);
      const lastSent = logRow?.[0]?.last_sent_at as string | undefined;
      const notifiedRecently = !!lastSent
        && Date.now() - Date.parse(lastSent) < 30 * 60 * 1000;

      if (notifiedRecently) {
        mail = { skipped: 'recently_notified' };
      } else {
        // クラブ宛は登録された通知先すべてに送る（保護者宛は本人1件）
        const to = isClubSender ? (parentEmail ? [parentEmail] : []) : clubEmails;
        /* 検証用アカウントが絡むやり取りでは、実在の相手にメールを出さない。
           2026-07-28の誤送信を受けたサーバ側のガード（運用ルールだけに頼らない） */
        const TEST_ADDRS = ['app-parent-test@chibispo.com', 'app-test@chibispo.com'];
        const isTestAddr = (e: string) => TEST_ADDRS.includes(String(e || '').toLowerCase());
        const testInvolved = isTestAddr(parentEmail) || clubEmails.some(isTestAddr);
        // 宛先が1件でも実在アドレスを含むなら送らない（一部だけ送るほうが危険）
        const toIsTest = to.length > 0 && to.every(isTestAddr);
        if (testInvolved && !toIsTest) {
          mail = { skipped: 'test_account_to_real_recipient' };
        } else if (!to.length) {
          mail = { skipped: 'no_address' };
        } else {
          const who = isClubSender ? (team?.name || 'クラブ') : `${tr.parent_name || '保護者'}さん`;
          const link = isClubSender ? 'https://chibispo.com/mypage.html' : 'https://chibispo.com/club-mypage.html';
          const r = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${RESEND_API_KEY}` },
            body: JSON.stringify({
              from: 'チビスポ <info@chibispo.com>',
              to,
              subject: `【チビスポ】${who}から新しいメッセージが届いています`,
              html: `
                <div style="font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Noto Sans JP',sans-serif;background:#fafbfc;padding:28px 16px;">
                  <div style="max-width:520px;margin:0 auto;background:#ffffff;border:1px solid #edf0f4;border-radius:16px;padding:28px 24px;">
                    <div style="font-size:19px;font-weight:800;color:#f0435c;letter-spacing:.04em;">チビスポ</div>
                    <h1 style="font-size:17px;font-weight:700;color:#21315b;margin:18px 0 0;">新しいメッセージが届いています</h1>
                    <p style="font-size:13.5px;line-height:1.9;color:#4a5468;margin:14px 0 0;">
                      <strong style="color:#21315b;">${who}</strong> からメッセージが届きました。<br>
                      下のボタンから開いて、そのまま返信できます。
                    </p>
                    <p style="margin:24px 0 0;">
                      <a href="${link}" style="display:inline-block;background:#f0435c;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:13px 28px;border-radius:12px;">
                        メッセージを見る
                      </a>
                    </p>
                    <hr style="border:none;border-top:1px solid #edf0f4;margin:22px 0 0;">
                    <p style="font-size:11.5px;line-height:1.8;color:#7a8299;margin:16px 0 0;">
                      やり取りはチビスポ内で完結します。メールアドレスが相手に伝わることはありません。<br>
                      内容の確認・返信はログインが必要です。
                    </p>
                    <p style="font-size:11px;color:#9aa1b2;margin:16px 0 0;">
                      チビスポ ／ <a href="https://chibispo.com" style="color:#9aa1b2;">chibispo.com</a>
                    </p>
                  </div>
                </div>`,
            }),
          });
          mail = { status: r.status };
          if (r.ok) {
            await admin.from('message_notify_log')
              .upsert({ trial_id, to_role: toRole, last_sent_at: new Date().toISOString() },
                { onConflict: 'trial_id,to_role' });
          }
        }
      }
    }
    return json({ ok: true, push: pj, mail });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
