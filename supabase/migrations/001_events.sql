begin;

create table public.events (
  id uuid primary key default gen_random_uuid(),
  title text not null check (length(trim(title)) > 0),
  description text not null default '',
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  timezone text not null default 'Europe/Moscow',
  location_name text not null,
  latitude double precision not null check (latitude between -90 and 90),
  longitude double precision not null check (longitude between -180 and 180),
  constraint event_interval check (ends_at > starts_at)
);

create index events_dates_idx on public.events (starts_at, ends_at);
alter table public.events enable row level security;
revoke all on table public.events from anon, authenticated;
grant select on table public.events to anon;
create policy "Public read for POC events" on public.events for select to anon using (true);

commit;
