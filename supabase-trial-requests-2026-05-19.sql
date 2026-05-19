-- 2026-05-19 体験申込みフォーム機能のテーブル作成
-- Supabase SQL Editorで実行してください
--
-- 注意：RLSは「ログイン済みなら全件読める」状態。
-- UIからは自分のチーム宛のみ表示。
-- 将来的にuser_idを trial_requests に持たせて user_id = auth.uid() で絞り込む方針に変更予定。

-- 1. trial_requests テーブル作成
create table if not exists public.trial_requests (
  id uuid primary key default gen_random_uuid(),
  team_id uuid not null references public.teams(id) on delete cascade,
  child_name text,
  child_name_kana text,
  child_age int,
  child_grade text,
  experience_level text,
  preferred_date_1 text,
  preferred_date_2 text,
  preferred_date_3 text,
  parent_name text not null,
  parent_email text not null,
  message text,
  status text not null default 'new',
  created_at timestamptz not null default now()
);

-- 既存テーブルに列追加（途中で列を追加した場合の冪等性）
alter table public.trial_requests add column if not exists child_name text;
alter table public.trial_requests add column if not exists child_name_kana text;

-- 2. インデックス
create index if not exists idx_trial_requests_team_id on public.trial_requests(team_id);
create index if not exists idx_trial_requests_status on public.trial_requests(status);
create index if not exists idx_trial_requests_created_at on public.trial_requests(created_at desc);

-- 3. 既存ポリシー・関数を全削除（再実行時の冪等性確保）
drop policy if exists "owners can read own team trial requests" on public.trial_requests;
drop policy if exists "owners can update own team trial requests" on public.trial_requests;
drop policy if exists "admins can read all trial requests" on public.trial_requests;
drop policy if exists "admins can update all trial requests" on public.trial_requests;
drop policy if exists "anyone can insert trial requests" on public.trial_requests;
drop policy if exists "anyone can read trial requests temp" on public.trial_requests;
drop policy if exists "authenticated can read trial requests" on public.trial_requests;
drop policy if exists "authenticated can update trial requests" on public.trial_requests;
drop function if exists public.owns_team(uuid);

-- 4. GRANT
grant select, insert, update on public.trial_requests to authenticated;
grant insert on public.trial_requests to anon;

-- 5. RLS有効化
alter table public.trial_requests enable row level security;

-- 6. ポリシー（INSERT：誰でも、SELECT/UPDATE：ログイン済みのみ）
create policy "trial_anon_insert"
  on public.trial_requests for insert
  to anon
  with check (true);

create policy "trial_authenticated_insert"
  on public.trial_requests for insert
  to authenticated
  with check (true);

create policy "trial_authenticated_select"
  on public.trial_requests for select
  to authenticated
  using (true);

create policy "trial_authenticated_update"
  on public.trial_requests for update
  to authenticated
  using (true);
