// AI下書きが「クラブ確認待ち」になったことをクラブに知らせる（Resend）
//   呼び出し：手元の runner（draft-requested-runner.mjs）が pending 登録の直後に POST { team_id }
//   守り：宛先は本文で受け取らず、teams.email を service_role で引く。24時間以内の pending 下書きが無ければ送らない
//        → 外から叩かれても「登録済みクラブに、実在する下書きの案内」以外は送れない
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!;
const SB_URL = Deno.env.get('SUPABASE_URL')!;
const SB_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'authorization, content-type' };
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', ...CORS } });
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] as string));

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  let body: { team_id?: string } = {};
  try { body = await req.json(); } catch { /* noop */ }
  const id = String(body.team_id || '');
  if (!/^[0-9a-f-]{36}$/i.test(id)) return json({ error: 'bad_request' }, 400);

  const H = { apikey: SB_KEY, Authorization: `Bearer ${SB_KEY}` };
  const since = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
  const [draft] = await (await fetch(`${SB_URL}/rest/v1/club_drafts?team_id=eq.${id}&status=eq.pending&created_at=gte.${since}&select=id,applied_fields&limit=1`, { headers: H })).json();
  if (!draft) return json({ error: 'no_pending_draft' }, 404);
  // 同じ下書きには1通だけ（送った印を applied_fields に置く。承認時に上書きされるので邪魔にならない）
  if (draft.applied_fields && draft.applied_fields.notified_at) return json({ ok: true, id: null, error: null, already: true });
  const [team] = await (await fetch(`${SB_URL}/rest/v1/teams?id=eq.${id}&select=name,email`, { headers: H })).json();
  if (!team?.email) return json({ error: 'no_email' }, 404);

  const name = esc(team.name);
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'チビスポ <info@chibispo.com>',
      reply_to: 'info@chibispo.com',
      to: team.email,
      subject: `【チビスポ】${team.name} のクラブページの下書きができました`,
      html: `
        <h2>クラブページの下書きができました</h2>
        <p>${name} の公式サイト・Instagram をもとに、チビスポがクラブページの下書きを作りました。</p>
        <p style="font-size:14px;color:#475569;line-height:1.8;">
          <strong>ご登録時に書いていただいた内容はそのまま残し、それにプラスする形</strong>で、大事にしていること・コーチ紹介・成績など、まだ空いている項目の案を用意しました。<br>
          マイページで<strong>載せてよい項目にチェックを入れるだけ</strong>で、クラブページに反映されます。<br>
          <strong>ご確認いただくまで公開されません。</strong>合わない項目は外して大丈夫です。<br>
          公式サイトなどから確かめられなかった項目は、推測で埋めずに<strong>空のまま</strong>にしています。必要なものはマイページから追加できます。
        </p>
        <p style="margin-top:20px;">
          <a href="https://chibispo.com/club-mypage.html" style="background:#E43B4D;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;">マイページで確認する</a>
        </p>
        <p style="font-size:13px;color:#64748b;line-height:1.7;margin-top:18px;">
          下書きには、公式サイトと登録内容で食い違っていた点や、確認したい質問も添えています。<br>
          ページの見え方が変わるのは、チェックを入れて「反映する」を押したあとだけです。
        </p>
        <hr style="margin-top:30px;border:none;border-top:1px solid #eee;" />
        <p style="color:#999;font-size:12px;">チビスポ｜子どもスポーツクラブ情報プラットフォーム<br>https://chibispo.com</p>
      `,
    }),
  });
  const data = await res.json();
  if (res.ok) await fetch(`${SB_URL}/rest/v1/club_drafts?id=eq.${draft.id}`, { method: 'PATCH', headers: { ...H, 'Content-Type': 'application/json', Prefer: 'return=minimal' }, body: JSON.stringify({ applied_fields: { notified_at: new Date().toISOString(), mail_id: data?.id || null } }) }).catch(() => {});
  return json({ ok: res.ok, id: data?.id || null, error: res.ok ? null : (data?.message || 'resend_failed') }, res.ok ? 200 : 502);
});
