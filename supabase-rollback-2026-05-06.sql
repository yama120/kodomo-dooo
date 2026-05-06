-- 2026-05-06 rollback for チビスポ security changes
-- Supabase SQL Editorで実行してください。
-- teams のデータは削除しません。今日追加したRLS/ポリシー/関数/トリガーを外します。

drop trigger if exists prevent_owner_status_or_owner_change on public.teams;
drop function if exists public.prevent_owner_status_or_owner_change();

drop function if exists public.is_admin();

drop policy if exists "admins can read admins" on public.admins;
drop policy if exists "public can read approved teams" on public.teams;
drop policy if exists "owners can read own teams" on public.teams;
drop policy if exists "admins can read all teams" on public.teams;
drop policy if exists "owners can insert own pending teams" on public.teams;
drop policy if exists "owners can update own non-status fields" on public.teams;
drop policy if exists "admins can update all teams" on public.teams;
drop policy if exists "admins can delete teams" on public.teams;

drop policy if exists "public can read team photos" on storage.objects;
drop policy if exists "owners can upload own team photos" on storage.objects;
drop policy if exists "owners can update own team photos" on storage.objects;
drop policy if exists "owners can delete own team photos" on storage.objects;

alter table if exists public.teams disable row level security;
alter table if exists public.admins disable row level security;

drop table if exists public.admins;
