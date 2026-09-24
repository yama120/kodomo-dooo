-- =============================================================
-- 2026-09-25 チビスポアシスト：口座の登録前から受け付け、口座が有効になったら送金する（Separate charges and transfers）
-- Supabase の SQL Editor で実行する（何度実行しても同じ結果になる）
-- ★実行するまで、Worker はアシストを「準備中」として受け付けない（クラブページにカードが出ない）
-- =============================================================

-- ==== 1. assists：送金の記録 ====
alter table public.assists add column if not exists charge_id       text;         -- Stripe の Charge（送金の元）
alter table public.assists add column if not exists stripe_fee      integer;      -- 決済手数料の実額（円）
alter table public.assists add column if not exists transfer_id     text;         -- Stripe の Transfer
alter table public.assists add column if not exists transfer_status text not null default 'pending'; -- pending（送金待ち）/ transferred / refunded / reversed
alter table public.assists add column if not exists transferred_at  timestamptz;
create index if not exists assists_transfer_idx on public.assists (transfer_status, team_id);

-- ==== 2. 確認 ====
-- curl "https://api.chibispo.com/api/assist/list?club=<team_id>" → "open":true になる（Stripe 設定済みのため）
