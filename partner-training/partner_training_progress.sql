-- =============================================
-- CEC 파트너 인증교육 진도 테이블 (멱등)
-- Supabase SQL Editor에 붙여넣고 Run
-- =============================================

create table if not exists public.partner_training_progress (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid references auth.users(id) on delete cascade,
  lesson_number int  not null,
  quiz_score    int,
  completed_at  timestamptz,
  created_at    timestamptz default now()
);

-- upsert 키 (한 사람당 강의별 1행)
do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'ptp_user_lesson_key') then
    alter table public.partner_training_progress
      add constraint ptp_user_lesson_key unique (user_id, lesson_number);
  end if;
end$$;

create index if not exists ptp_user_idx on public.partner_training_progress (user_id);

-- RLS: 본인 행만 읽기/쓰기 (publishable 키 = authenticated 사용자)
alter table public.partner_training_progress enable row level security;

drop policy if exists "ptp_select_own" on public.partner_training_progress;
create policy "ptp_select_own" on public.partner_training_progress
  for select to authenticated using (auth.uid() = user_id);

drop policy if exists "ptp_insert_own" on public.partner_training_progress;
create policy "ptp_insert_own" on public.partner_training_progress
  for insert to authenticated with check (auth.uid() = user_id);

drop policy if exists "ptp_update_own" on public.partner_training_progress;
create policy "ptp_update_own" on public.partner_training_progress
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 검증
select column_name, data_type
from information_schema.columns
where table_schema='public' and table_name='partner_training_progress'
order by ordinal_position;
