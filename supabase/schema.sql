-- Cumulative application schema for a NEW Supabase project only.
-- Structure current through: 003_split_event_dates.sql.
-- Requires Supabase-provided roles anon and authenticated and gen_random_uuid().
-- Alternative to applying structural migrations, not an additional migration.
-- Seed data is intentionally excluded; apply the compatible seed separately.
begin;

create table public.events (
  id uuid primary key default gen_random_uuid(),
  title text not null check (length(trim(title)) > 0),
  description text not null default '',
  start_date date not null,
  end_date date not null,
  start_time time without time zone,
  end_time time without time zone,
  timezone text not null default 'Europe/Moscow',
  location_name text not null,
  latitude double precision not null check (latitude between -90 and 90),
  longitude double precision not null check (longitude between -180 and 180),
  constraint event_dates check (end_date >= start_date),
  constraint event_times check (
    end_date > start_date or start_time is null or end_time is null or end_time > start_time
  )
);

create index events_dates_idx on public.events (start_date, end_date);
alter table public.events enable row level security;
revoke all on table public.events from anon, authenticated;
grant select on table public.events to anon;
create policy "Public read for POC events" on public.events for select to anon using (true);

commit;
