-- チビスポ 新デザイン（2026-09 プレビュー13〜16ページ）で必要になる列・テーブル
-- 台帳：memory project_chibispo_db_gap_2026_09
-- ★Supabase の SQL Editor では「-- ==== 」で区切ったブロックを1つずつ実行する（まとめて流さない）
-- ★teams は列単位の SELECT GRANT で公開列を決めている（user_id / email / stripe_customer_id / billing_source / apple_original_transaction_id は非公開）。
--   新しい列は公開してよいものだけ GRANT する。

-- ==== 1. teams：クラブ詳細 v2・クラブマイページ v2 の項目 ====
alter table public.teams
  add column if not exists trial_fee text,                      -- 体験の費用（空＝要相談）
  add column if not exists member_count integer,                -- 在籍人数
  add column if not exists cost_items jsonb default '[]'::jsonb,-- 費用の内訳 [{name,amount,note}]
  add column if not exists style jsonb,                         -- 5段階 {strict,win,select,practice,gender}
  add column if not exists staff jsonb default '[]'::jsonb,     -- コーチ・スタッフ [{name,role,comment,photo_url}]
  add column if not exists video_url text,                      -- 動画URL
  add column if not exists postal_code text,                    -- 住所（郵便番号）
  add column if not exists address1 text,                       -- 町名・番地
  add column if not exists address2 text,                       -- 建物
  add column if not exists lat double precision,                -- 保存時に geocode
  add column if not exists lng double precision,
  add column if not exists editor_headline text,                -- 編集部の一言（有料）
  add column if not exists editor_note text;

-- ==== 2. teams：新しい列を公開（列単位GRANT） ====
grant select (trial_fee, member_count, cost_items, style, staff, video_url, postal_code, address1, address2, lat, lng, editor_headline, editor_note)
  on public.teams to anon, authenticated;

-- ==== 3. profiles：保護者マイページ v3・診断 ====
alter table public.profiles
  add column if not exists quiz_result jsonb,   -- 診断の結果 {type,cond[],sports[],at}
  add column if not exists notify_prefs jsonb,  -- {new_clubs,trial_open,articles,push,email}
  add column if not exists child_grade text,    -- お子さんの学年
  add column if not exists child_gender text;

-- ==== 4. articles：マガジン v2 ====
alter table public.articles
  add column if not exists category text,
  add column if not exists read_minutes integer,
  add column if not exists related_team_ids uuid[],
  add column if not exists hero_image_url text;

-- ==== 5. waitlist：準備中サービスの「お知らせを受け取る」 ====
create table if not exists public.waitlist (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  topic text not null,          -- 'video' など
  source text,                  -- どのページから
  created_at timestamptz not null default now(),
  unique (email, topic)
);
alter table public.waitlist enable row level security;

-- ==== 6. waitlist：ポリシーとGRANT（誰でも登録・読むのは管理者だけ） ====
create policy waitlist_anyone_insert on public.waitlist for insert to anon, authenticated with check (true);
create policy waitlist_admin_select on public.waitlist for select to authenticated using (is_admin());
create policy waitlist_admin_delete on public.waitlist for delete to authenticated using (is_admin());
grant insert on public.waitlist to anon, authenticated;
grant select, delete on public.waitlist to authenticated;

-- ==== 7. inquiries：広告・SNS・HP・相談のフォーム ====
create table if not exists public.inquiries (
  id uuid primary key default gen_random_uuid(),
  kind text not null,           -- 'ads' | 'sns' | 'hp' | 'consult'
  name text,
  org text,
  email text not null,
  phone text,
  plan text,
  message text,
  status text not null default 'new',  -- new | doing | done
  created_at timestamptz not null default now()
);
alter table public.inquiries enable row level security;

-- ==== 8. inquiries：ポリシーとGRANT ====
create policy inquiries_anyone_insert on public.inquiries for insert to anon, authenticated with check (true);
create policy inquiries_admin_select on public.inquiries for select to authenticated using (is_admin());
create policy inquiries_admin_update on public.inquiries for update to authenticated using (is_admin()) with check (is_admin());
grant insert on public.inquiries to anon, authenticated;
grant select, update on public.inquiries to authenticated;

-- ==== 9. 確認（匿名で叩く。RLS変更後は必ず） ====
-- curl -s -X POST "$SUPABASE_URL/rest/v1/waitlist" -H "apikey: $ANON" -H "Authorization: Bearer $ANON" -H "Content-Type: application/json" -H "Prefer: return=minimal" -d '{"email":"check@example.invalid","topic":"video","source":"check"}'   # → 201
-- curl -s "$SUPABASE_URL/rest/v1/waitlist?select=email&limit=1" -H "apikey: $ANON" -H "Authorization: Bearer $ANON"   # → 401 か []（匿名で読めない）
-- curl -s "$SUPABASE_URL/rest/v1/teams?select=id,trial_fee,style,video_url&status=eq.approved&limit=1" -H "apikey: $ANON" -H "Authorization: Bearer $ANON"   # → 200
-- その後：delete from public.waitlist where source='check';
