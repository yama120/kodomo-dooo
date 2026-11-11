-- 2026-11-11 保護者からの連絡を受ける窓口を、クラブが選べるようにする（Webのクラブページ）
-- teams.contact_channels：'chibispo'（チビスポの申込みフォーム）/'form'（trial_form_url）/'website'/'instagram'/'line' の配列。
-- NULL・空は今までどおり 'chibispo' だけとして扱う。アプリは常にアプリ内の申込み。
-- ★teams は列単位の SELECT GRANT。GRANT しないと club.html の取得が旧列だけの表示に落ちる。
-- ★このSQLを本番に流してから club.html / club-mypage.html をデプロイする。1文ずつ流す。追加のみ。

alter table public.teams add column if not exists contact_channels text[];

alter table public.teams add constraint teams_contact_channels_allowed
  check (contact_channels is null or contact_channels <@ array['chibispo','form','website','instagram','line']::text[]);

grant select (contact_channels) on public.teams to anon, authenticated;
