-- =============================================================
-- 2026-10-11 クラブ登録フォームに「チビスポを何で知りましたか」（流入経路）を追加
-- Supabase の SQL Editor で実行する（何度実行しても同じ結果になる）
-- 目的：どの投稿・媒体がクラブ登録を生んだかを週次分析（マーケPDCAループ）で数えるため
-- ★referral_source（選択肢）は匿名で読める列にする（週次データ取得 fetch-teams-cloud.mjs が anon で読む）
-- ★referral_detail（自由記述）は公開しない（authenticated＝本人・管理者だけ）
-- =============================================================

alter table public.teams add column if not exists referral_source text;   -- threads / instagram / search / referral / outreach / other
alter table public.teams add column if not exists referral_detail text;   -- 「その他」や「知人・他のクラブ」の補足（任意）

grant select (referral_source) on public.teams to anon, authenticated;
grant select (referral_detail) on public.teams to authenticated;
grant insert (referral_source, referral_detail), update (referral_source, referral_detail) on public.teams to authenticated;

comment on column public.teams.referral_source is '登録時の流入経路（threads/instagram/search/referral/outreach/other）2026-10-11〜';
comment on column public.teams.referral_detail is '流入経路の補足（任意・非公開）';
