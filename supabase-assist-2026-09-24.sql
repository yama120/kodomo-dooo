-- =============================================================
-- 2026-09-24 クラブ詳細の充実化（AI下書き・Instagram写真）＋ チビスポアシスト（少額応援・Stripe Connect）
-- Supabase の SQL Editor で、上から順に実行する（何度実行しても同じ結果になるよう if not exists で書いてある）
-- ★teams は列単位の SELECT GRANT で公開列を決めている。stripe_account_id と assist_agreed_at は公開しない
-- =============================================================

-- ==== 1. teams：新しい列 ====
alter table public.teams add column if not exists tagline            text;      -- ヒーロー下の一文（AI下書き・承認後）
alter table public.teams add column if not exists story              jsonb;     -- [{heading, body}]（最初はリード）
alter table public.teams add column if not exists story_policies     jsonb;     -- [{title, body}] 大事にしていること3つ
alter table public.teams add column if not exists features           jsonb;     -- [{title, body}] ほかのクラブとの違い
alter table public.teams add column if not exists greeting           jsonb;     -- {title, name, role, body, photo_url}
alter table public.teams add column if not exists achievements       jsonb;     -- [text]
alter table public.teams add column if not exists achievement_photos jsonb;     -- [{photo_url, caption}]
alter table public.teams add column if not exists practice_log       jsonb;     -- [{date, title, body, url, image}]
alter table public.teams add column if not exists ig_photos          jsonb;     -- [{code, kind, url, thumb, added_at}] Instagram の投稿（Worker が写真を保存）
alter table public.teams add column if not exists stripe_account_id  text;      -- Stripe Connect Express のアカウント（非公開）
alter table public.teams add column if not exists assist_enabled     boolean not null default false; -- 口座の審査が通り受け取れる状態
alter table public.teams add column if not exists assist_agreed_at   timestamptz; -- アシスト利用規約への同意日時（非公開）

-- ==== 2. teams：公開してよい列だけ GRANT ====
grant select (tagline, story, story_policies, features, greeting, achievements, achievement_photos, practice_log, ig_photos, assist_enabled)
  on public.teams to anon, authenticated;

-- ==== 3. club_drafts：AI下書き（クラブが承認するまで本番に出ない） ====
create table if not exists public.club_drafts (
  id             uuid primary key default gen_random_uuid(),
  team_id        uuid not null references public.teams(id) on delete cascade,
  draft          jsonb not null,
  sources        jsonb,
  status         text not null default 'pending',   -- pending / approved / rejected
  applied_fields jsonb,
  reviewed_at    timestamptz,
  created_at     timestamptz not null default now()
);
create index if not exists club_drafts_team_idx on public.club_drafts (team_id, status, created_at desc);
alter table public.club_drafts enable row level security;
-- 読み書きは Worker（service_role）だけ。管理者は画面から読める
drop policy if exists club_drafts_admin_select on public.club_drafts;
create policy club_drafts_admin_select on public.club_drafts for select to authenticated using (is_admin());
grant select on public.club_drafts to authenticated;

-- ==== 4. assists：アシスト（決済の記録） ====
create table if not exists public.assists (
  id              uuid primary key default gen_random_uuid(),
  team_id         uuid not null references public.teams(id) on delete cascade,
  session_id      text not null unique,        -- Stripe Checkout Session（Webhook と確認のどちらが先でも1件）
  payment_intent  text,
  amount          integer not null,            -- 支払い額（円）
  fee             integer not null,            -- チビスポの運営費（10%）
  stripe_fee_est  integer not null,            -- 決済手数料の目安（3.6%）
  net_to_club     integer not null,            -- クラブに届く額の目安
  kind            text not null default 'assist', -- assist / sponsor
  anon            boolean not null default true,
  name            text,
  message         text,
  status          text not null default 'paid',   -- paid / refunded
  created_at      timestamptz not null default now()
);
create index if not exists assists_team_idx on public.assists (team_id, status, created_at desc);
alter table public.assists enable row level security;
drop policy if exists assists_admin_select on public.assists;
create policy assists_admin_select on public.assists for select to authenticated using (is_admin());
grant select on public.assists to authenticated;

-- ==== 5. sponsor_inquiries：お店・企業のスポンサー相談（A型：チビスポが契約と請求書） ====
create table if not exists public.sponsor_inquiries (
  id         uuid primary key default gen_random_uuid(),
  team_id    uuid not null references public.teams(id) on delete cascade,
  club_name  text,
  org        text not null,
  person     text not null,
  email      text not null,
  tel        text,
  site       text,
  term       text,            -- year / once / talk
  budget     text,            -- 10000 / 30000 / 100000 / more / undecided
  show       jsonb,           -- ["name","logo","link","message","other"]
  message    text,
  status     text not null default 'new',  -- new / contacted / contracted / closed
  created_at timestamptz not null default now()
);
alter table public.sponsor_inquiries enable row level security;
drop policy if exists sponsor_admin_select on public.sponsor_inquiries;
drop policy if exists sponsor_admin_update on public.sponsor_inquiries;
create policy sponsor_admin_select on public.sponsor_inquiries for select to authenticated using (is_admin());
create policy sponsor_admin_update on public.sponsor_inquiries for update to authenticated using (is_admin()) with check (is_admin());
grant select, update on public.sponsor_inquiries to authenticated;

-- ==== 6. Worker（service_role）の権限 ====
-- ★このプロジェクトはテーブルの既定権限を絞ってあるので、create table だけでは Worker から読み書きできない（sb 403）。
--   新しいテーブルを作ったら必ず service_role に GRANT する（2026-09-24 に実際に踏んだ）
grant all on public.assists           to service_role;
grant all on public.club_drafts       to service_role;
grant all on public.sponsor_inquiries to service_role;

-- ==== 7. 確認（実行後に匿名キーで） ====
-- curl "$SUPABASE_URL/rest/v1/teams?select=id,tagline,ig_photos,assist_enabled&limit=1" -H "apikey: <anon>"   → 200
-- curl "$SUPABASE_URL/rest/v1/teams?select=stripe_account_id&limit=1" -H "apikey: <anon>"                     → 401/42501（非公開のまま）
-- curl "$SUPABASE_URL/rest/v1/assists?select=id&limit=1" -H "apikey: <anon>"                                   → 401/42501
