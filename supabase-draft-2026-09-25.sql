-- =============================================================
-- 2026-09-25 AI下書きの「依頼」を、管理画面と登録画面から入れられるようにする
-- Supabase の SQL Editor で実行する（何度実行しても同じ結果になる）
-- 流れ：登録（HP/IGあり）→ club_drafts に requested → 手元の runner が claude -p で生成して pending
--       → クラブがマイページで確認して反映（確認するまで公開されない）
-- =============================================================

-- 管理者：依頼（requested）だけ入れられる。下書きの中身は Worker（service_role）しか書かない
drop policy if exists club_drafts_admin_insert on public.club_drafts;
create policy club_drafts_admin_insert on public.club_drafts
  for insert to authenticated
  with check (is_admin() and status = 'requested');

-- クラブ本人：自分のクラブの依頼（requested）だけ入れられる（登録直後の自動依頼に使う）
drop policy if exists club_drafts_owner_insert on public.club_drafts;
create policy club_drafts_owner_insert on public.club_drafts
  for insert to authenticated
  with check (
    status = 'requested'
    and exists (select 1 from public.teams t where t.id = team_id and t.user_id = auth.uid())
  );

grant insert on public.club_drafts to authenticated;

-- 確認：管理画面の承認待ちに「AI下書きを作る」ボタンが出て、押すと「下書き：作成待ち」になる
