-- CEC English Camp — Visit Analytics v2 Migration
-- 2026-06-11
-- Run in Supabase SQL Editor

-- ─────────────────────────────────────────────
-- 1. visit_events
-- ─────────────────────────────────────────────
create table if not exists visit_events (
  id               uuid primary key default gen_random_uuid(),
  created_at       timestamptz not null default now(),
  event_date       date generated always as (created_at::date) stored,
  event_type       text not null,        -- page_view | cta_click | signup_click | payment_click | video_play | session_start | session_end
  url              text,
  normalized_url   text,
  page_title       text,
  referrer         text,
  utm_source       text,
  utm_medium       text,
  utm_campaign     text,
  visitor_id       text,
  session_id       text,
  user_agent       text,
  is_bot           boolean not null default false,
  is_admin         boolean not null default false,
  duration_seconds int,
  metadata         jsonb
);

-- Indexes for common query patterns
create index if not exists visit_events_date_idx        on visit_events (event_date);
create index if not exists visit_events_normalized_idx  on visit_events (normalized_url);
create index if not exists visit_events_visitor_idx     on visit_events (visitor_id);
create index if not exists visit_events_session_idx     on visit_events (session_id);
create index if not exists visit_events_type_idx        on visit_events (event_type);
create index if not exists visit_events_bot_idx         on visit_events (is_bot, is_admin);

-- Enable Row Level Security (allow anonymous insert, no public read)
alter table visit_events enable row level security;
create policy "allow_anon_insert" on visit_events for insert to anon with check (true);
create policy "allow_service_select" on visit_events for select to service_role using (true);

-- ─────────────────────────────────────────────
-- 2. visit_stats_daily_v2
-- ─────────────────────────────────────────────
create table if not exists visit_stats_daily_v2 (
  id                    uuid primary key default gen_random_uuid(),
  date                  date not null,
  normalized_url        text not null,
  page_views            int not null default 0,
  unique_visitors       int not null default 0,
  sessions              int not null default 0,
  avg_duration_seconds  numeric(10,2),
  cta_clicks            int not null default 0,
  signup_clicks         int not null default 0,
  payment_clicks        int not null default 0,
  bot_views             int not null default 0,
  admin_views           int not null default 0,
  top_referrer          text,
  created_at            timestamptz default now(),
  updated_at            timestamptz default now(),
  constraint visit_stats_daily_v2_pkey unique (date, normalized_url)
);

create index if not exists visit_stats_v2_date_idx on visit_stats_daily_v2 (date desc);

alter table visit_stats_daily_v2 enable row level security;
create policy "allow_service_all" on visit_stats_daily_v2 for all to service_role using (true);

-- ─────────────────────────────────────────────
-- 3. traffic_reports
-- ─────────────────────────────────────────────
create table if not exists traffic_reports (
  id               uuid primary key default gen_random_uuid(),
  created_at       timestamptz default now(),
  report_date      date not null,
  report_time      text not null,          -- '12:00 PM' | '6:00 PM'
  timezone         text default 'America/Los_Angeles',
  summary          jsonb,
  markdown         text,
  abnormal_flags   jsonb,
  recommendations  jsonb
);

create index if not exists traffic_reports_date_idx on traffic_reports (report_date desc);

alter table traffic_reports enable row level security;
create policy "allow_service_all" on traffic_reports for all to service_role using (true);
create policy "allow_anon_select" on traffic_reports for select to anon using (true);

-- ─────────────────────────────────────────────
-- 4. aggregate_daily_stats() — upsert for a given date
-- ─────────────────────────────────────────────
create or replace function aggregate_daily_stats(target_date date default current_date)
returns void
language plpgsql
security definer
as $$
begin
  -- Delete existing rows for the date (full re-aggregate)
  delete from visit_stats_daily_v2 where date = target_date;

  insert into visit_stats_daily_v2 (
    date, normalized_url,
    page_views, unique_visitors, sessions,
    avg_duration_seconds,
    cta_clicks, signup_clicks, payment_clicks,
    bot_views, admin_views,
    top_referrer
  )
  select
    target_date                                                   as date,
    normalized_url,
    count(*) filter (where event_type = 'page_view'
                       and not is_bot and not is_admin)           as page_views,
    count(distinct visitor_id) filter (where event_type = 'page_view'
                                         and not is_bot
                                         and not is_admin)        as unique_visitors,
    count(distinct session_id) filter (where event_type = 'page_view'
                                         and not is_bot
                                         and not is_admin)        as sessions,
    round(avg(duration_seconds) filter (
      where event_type = 'session_end'
        and duration_seconds between 3 and 1800
        and not is_bot and not is_admin
    )::numeric, 2)                                                as avg_duration_seconds,
    count(*) filter (where event_type = 'cta_click'
                       and not is_bot and not is_admin)           as cta_clicks,
    count(*) filter (where event_type = 'signup_click'
                       and not is_bot and not is_admin)           as signup_clicks,
    count(*) filter (where event_type = 'payment_click'
                       and not is_bot and not is_admin)           as payment_clicks,
    count(*) filter (where event_type = 'page_view' and is_bot)   as bot_views,
    count(*) filter (where event_type = 'page_view' and is_admin) as admin_views,
    (
      select referrer
      from visit_events sub
      where sub.event_date = target_date
        and sub.normalized_url = ve.normalized_url
        and sub.referrer is not null
        and sub.referrer <> ''
        and not sub.is_bot
      group by referrer
      order by count(*) desc
      limit 1
    )                                                              as top_referrer
  from visit_events ve
  where event_date = target_date
    and normalized_url is not null
  group by normalized_url;
end;
$$;

-- ─────────────────────────────────────────────
-- 5. detect_abnormal_spikes() — returns rows with anomaly flags
-- ─────────────────────────────────────────────
create or replace function detect_abnormal_spikes(target_date date default current_date)
returns table (
  normalized_url     text,
  page_views         bigint,
  unique_visitors    bigint,
  bot_views          bigint,
  bot_ratio          numeric,
  anomaly_reason     text
)
language sql
security definer
as $$
  with daily as (
    select
      normalized_url,
      count(*) filter (where event_type='page_view' and not is_bot and not is_admin) as pv,
      count(*) filter (where event_type='page_view' and is_bot)                      as bv,
      count(distinct visitor_id) filter (where not is_bot and not is_admin)          as uv
    from visit_events
    where event_date = target_date
    group by normalized_url
  ),
  avg_7d as (
    select
      normalized_url,
      avg(page_views) as avg_pv_7d
    from visit_stats_daily_v2
    where date between target_date - 7 and target_date - 1
    group by normalized_url
  )
  select
    d.normalized_url,
    d.pv,
    d.uv,
    d.bv,
    case when (d.pv + d.bv) > 0
         then round(d.bv::numeric / (d.pv + d.bv), 3)
         else 0 end                              as bot_ratio,
    case
      when d.bv > 100              then 'High bot volume'
      when d.pv > 500              then 'Very high page views'
      when a.avg_pv_7d > 0
       and d.pv > a.avg_pv_7d * 5  then '5x spike vs 7-day avg'
      when d.uv > 0
       and d.pv::numeric / d.uv > 20 then 'High views-per-visitor ratio'
      else null
    end                                          as anomaly_reason
  from daily d
  left join avg_7d a using (normalized_url)
  where
    d.bv > 100
    or d.pv > 500
    or (a.avg_pv_7d > 0 and d.pv > a.avg_pv_7d * 5)
    or (d.uv > 0 and d.pv::numeric / d.uv > 20)
  order by d.pv desc;
$$;

-- ─────────────────────────────────────────────
-- 6. Top pages view helper
-- ─────────────────────────────────────────────
create or replace view visit_top_pages_today as
  select
    normalized_url,
    count(*) filter (where event_type = 'page_view'
                       and not is_bot and not is_admin)          as page_views,
    count(distinct visitor_id) filter (where not is_bot
                                         and not is_admin)       as unique_visitors,
    count(*) filter (where event_type = 'cta_click'
                       and not is_bot and not is_admin)          as cta_clicks
  from visit_events
  where event_date = current_date
    and normalized_url is not null
  group by normalized_url
  order by page_views desc;
