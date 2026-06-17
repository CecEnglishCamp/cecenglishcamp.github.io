-- CEC English Camp - Add Snapshot Support to traffic_reports
-- 2026-06-15
-- Run in Supabase SQL Editor
--
-- ⚠️ BEFORE RUNNING: Check for existing duplicates!
--
--   SELECT report_date, report_time, count(*)
--   FROM traffic_reports
--   GROUP BY report_date, report_time
--   HAVING count(*) > 1;
--
--   If any rows returned, resolve duplicates first (delete extras)
--   or the CREATE UNIQUE INDEX below will fail.
--   Expected: no rows returned.
--
--   Note: Daily reports use report_time = '12:00 PM' / '6:00 PM'.
--   Snapshot reports use report_time = '12:00-14:00 PT' format.
--   The format difference means no cross-type conflict.

-- 1. Add columns for snapshot tracking
alter table traffic_reports
  add column if not exists snapshot     boolean not null default false,
  add column if not exists window_start timestamptz,
  add column if not exists window_end   timestamptz;

-- 2. Unique constraint for snapshot dedup (upsert key)
--    Same report_date + report_time + snapshot flag = single row
--    Daily reports: snapshot=false (distinct from snapshot rows)
create unique index if not exists traffic_reports_snapshot_unique
  on traffic_reports (report_date, report_time, snapshot);

-- 3. Allow snapshot rows to be upserted by service_role
--    Existing policy "allow_service_all" covers this.
