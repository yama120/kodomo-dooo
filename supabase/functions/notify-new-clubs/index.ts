import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// 保存された検索条件に合う「新着クラブ」を保護者へプッシュ通知するバッチ。
// 定期実行（cron）または管理者が手動で叩く想定。secret 必須。
// 入力: { secret, hours?（既定24）, dry?（true なら送信せず件数だけ返す） }
const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const ANON = Deno.env.get('SUPABASE_ANON_KEY')!;
const PUSH_SECRET = Deno.env.get('PUSH_TRIGGER_SECRET') || '';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json', ...cors } });

// アプリ側 MOOD_GROUPS と同じ定義（キー → 実際のmoods）
const MOOD_MAP: Record<string, string[]> = {
  fun: ['楽しむこと', 'アットホーム', 'アミューズメント', '親子で参加'],
  praise: ['ほめて伸ばす'],
  serious: ['本格志向', '真剣に取り組む', '礼儀・しつけ'],
  small: ['少人数で丁寧', 'パーソナルレッスン'],
};

type Club = {
  id: string; name: string; sport: string | null; pref: string | null; city: string | null;
  age_groups: string[] | null; moods: string[] | null; fee_num: number | null; created_at: string;
};
type Saved = {
  id: string; user_id: string; label: string | null; pref: string | null; city: string | null;
  sport: string | null; ages: string[]; moods: string[]; fee_max: number | null;
  notify: boolean; last_notified_at: string | null;
};

function matches(c: Club, s: Saved): boolean {
  if (s.pref && c.pref !== s.pref) return false;
  if (s.sport && c.sport !== s.sport) return false;
  if (s.ages?.length && !s.ages.some((a) => (c.age_groups || []).some((x) => String(x).includes(a)))) return false;
  if (s.moods?.length) {
    const want = s.moods.flatMap((k) => MOOD_MAP[k] || []);
    if (!want.some((m) => (c.moods || []).includes(m))) return false;
  }
  if (s.fee_max != null && !(typeof c.fee_num === 'number' && c.fee_num > 0 && c.fee_num <= s.fee_max)) return false;
  return true;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const { secret, hours = 24, dry = false } = await req.json().catch(() => ({}));
    if (PUSH_SECRET && secret !== PUSH_SECRET) return json({ ok: false, error: 'forbidden' }, 403);

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });
    const since = new Date(Date.now() - hours * 3600 * 1000).toISOString();

    const { data: clubs } = await admin.from('teams')
      .select('id,name,sport,pref,city,age_groups,moods,fee_num,created_at')
      .eq('status', 'approved').gte('created_at', since);
    if (!clubs?.length) return json({ ok: true, new_clubs: 0, sent: 0 });

    const { data: saves } = await admin.from('saved_searches')
      .select('id,user_id,label,pref,city,sport,ages,moods,fee_max,notify,last_notified_at')
      .eq('notify', true);
    if (!saves?.length) return json({ ok: true, new_clubs: clubs.length, sent: 0, note: 'no_saved_searches' });

    let sent = 0;
    const results: unknown[] = [];
    for (const s of saves as Saved[]) {
      // 前回通知より後に増えたクラブだけを対象にする（二重通知の防止）
      const cutoff = s.last_notified_at ? new Date(s.last_notified_at).getTime() : 0;
      const hits = (clubs as Club[]).filter((c) => new Date(c.created_at).getTime() > cutoff && matches(c, s));
      if (!hits.length) continue;

      const title = '条件に合う新しいクラブ';
      const body = hits.length === 1
        ? `${hits[0].city || hits[0].pref || ''}に「${hits[0].name}」が掲載されました`
        : `保存した条件に合うクラブが${hits.length}件掲載されました`;

      if (!dry) {
        const r = await fetch(`${SUPABASE_URL}/functions/v1/send-push`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', apikey: ANON, Authorization: `Bearer ${ANON}` },
          body: JSON.stringify({
            user_id: s.user_id, title, body,
            data: { kind: 'saved_search', saved_id: s.id, club_id: hits[0].id },
            secret: PUSH_SECRET,
          }),
        });
        const pj = await r.json().catch(() => ({}));
        results.push({ saved: s.id, hits: hits.length, push: pj });
        await admin.from('saved_searches').update({ last_notified_at: new Date().toISOString() }).eq('id', s.id);
      } else {
        results.push({ saved: s.id, hits: hits.length, dry: true });
      }
      sent++;
    }
    return json({ ok: true, new_clubs: clubs.length, saved_searches: saves.length, sent, results });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
