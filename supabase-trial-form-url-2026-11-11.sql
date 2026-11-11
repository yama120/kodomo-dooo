-- 2026-11-11 体験申込みを「クラブ自前の申込みフォーム」へつなぐ設定（Webのみ）
-- teams.trial_form_url が入っているクラブは、club.html の「体験申込」ボタンがそのURLを開く。
-- 空（NULL）のクラブは今までどおりチビスポ内の申込みフォーム。アプリは常にアプリ内の申込み。
--
-- ★teams は列単位の GRANT で公開列を決めている。新しい列は GRANT しないと匿名から読めず、
--   club.html の取得が丸ごと失敗して旧列だけの表示に落ちる。
-- ★このSQLを本番に流してから club.html / club-mypage.html をデプロイする（順番を逆にしない）。
-- 追加のみ。既存の列・権限・ポリシーには触らない。

alter table public.teams add column if not exists trial_form_url text;

alter table public.teams drop constraint if exists teams_trial_form_url_http;
alter table public.teams add constraint teams_trial_form_url_http
  check (trial_form_url is null or trial_form_url ~* '^https?://[^[:space:]]+$');

grant select (trial_form_url) on public.teams to anon, authenticated;
grant update (trial_form_url) on public.teams to authenticated;

-- 確認（匿名で読めること）：
--   curl "$SUPABASE_URL/rest/v1/teams?select=id,trial_form_url&limit=1" -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
