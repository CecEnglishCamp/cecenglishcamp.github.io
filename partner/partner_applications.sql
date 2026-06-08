-- =============================================
-- CEC 파트너 신청 테이블 (멱등) · Supabase SQL Editor에서 Run
-- =============================================
create table if not exists public.partner_applications (
  id                 uuid primary key default gen_random_uuid(),
  track              text,            -- A / B / C
  name               text not null,
  phone              text not null,
  email              text not null,
  region             text,
  english_level      text,            -- 상 / 중 / 하
  has_child          boolean,
  currently_employed boolean,
  employer           text,
  noncompete_aware   text,            -- Y / N / 모름
  agree_no_solicit   boolean,
  agree_new_only     boolean,
  agree_no_data      boolean,
  message            text,
  status             text default 'new',
  created_at         timestamptz default now()
);

create index if not exists pa_created_idx on public.partner_applications (created_at);

-- RLS: 누구나(anon) 신청서 제출(insert) 가능. 읽기/수정은 service_role(관리자)만.
alter table public.partner_applications enable row level security;

drop policy if exists "pa_insert_public" on public.partner_applications;
create policy "pa_insert_public" on public.partner_applications
  for insert to anon, authenticated with check (true);

-- 검증
select column_name, data_type
from information_schema.columns
where table_schema='public' and table_name='partner_applications'
order by ordinal_position;
