-- ─────────────────────────────────────────────────────────
-- 2026-06-11 / 2667 views 원인 분석 쿼리
-- Run in Supabase SQL Editor → compare each section
-- ─────────────────────────────────────────────────────────

-- 1. 해당 날짜 전체 집계 (URL 정규화 전 상태)
select
  url,
  count(*)                         as total_rows,
  count(distinct user_agent)       as distinct_uas,
  min(created_at)                  as first_seen,
  max(created_at)                  as last_seen
from visit_logs
where created_at::date = '2026-06-11'
  and (url like '%cecenglishcamp%/' or url = '/' or url like '%/index.html')
group by url
order by total_rows desc;

-- 2. / vs /index.html 분리 여부
select
  url,
  count(*) as cnt
from visit_logs
where created_at::date = '2026-06-11'
  and (url = '/'
    or url like '%/index.html'
    or url like '%cecenglishcamp.com/'
    or url like '%cecenglishcamp.github.io/')
group by url
order by cnt desc;

-- 3. 같은 user_agent가 얼마나 반복되는지 (봇 여부)
select
  user_agent,
  count(*) as hits,
  count(distinct created_at::date) as days_active
from visit_logs
where created_at::date = '2026-06-11'
  and (url = '/' or url like '%cecenglishcamp%/')
group by user_agent
order by hits desc
limit 30;

-- 4. 1분 단위 분포 — 특정 시간에 몰린 요청이 있는지
select
  date_trunc('minute', created_at) as minute,
  count(*)                         as hits
from visit_logs
where created_at::date = '2026-06-11'
  and (url = '/' or url like '%cecenglishcamp%/')
group by 1
order by hits desc
limit 30;

-- 5. 10초 이내 같은 조합 반복 (tracking script 중복 실행 여부)
--    created_at이 매우 근접한 row 쌍
select
  l1.url,
  l1.user_agent,
  l1.created_at as t1,
  l2.created_at as t2,
  extract(epoch from (l2.created_at - l1.created_at)) as gap_seconds
from visit_logs l1
join visit_logs l2
  on l1.user_agent = l2.user_agent
 and l2.created_at > l1.created_at
 and l2.created_at < l1.created_at + interval '10 seconds'
where l1.created_at::date = '2026-06-11'
  and l1.url like '%cecenglishcamp%/'
limit 50;

-- 6. 전날(2026-06-10) 비교 — 정상 트래픽 수준
select
  created_at::date as dt,
  count(*)         as total_rows
from visit_logs
where created_at::date between '2026-06-08' and '2026-06-11'
  and (url = '/' or url like '%cecenglishcamp%/')
group by 1
order by 1;
