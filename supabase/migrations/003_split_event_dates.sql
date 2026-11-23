begin;

alter table public.events
  add column start_date date,
  add column end_date date,
  add column start_time time without time zone,
  add column end_time time without time zone;

-- Preserve the event's local date and time, not the SQL session timezone.
update public.events set
  start_date = (starts_at at time zone timezone)::date,
  end_date = (ends_at at time zone timezone)::date,
  start_time = (starts_at at time zone timezone)::time,
  end_time = (ends_at at time zone timezone)::time;

alter table public.events
  alter column start_date set not null,
  alter column end_date set not null,
  drop constraint event_interval,
  drop column starts_at,
  drop column ends_at,
  add constraint event_dates check (end_date >= start_date),
  add constraint event_times check (
    end_date > start_date or start_time is null or end_time is null or end_time > start_time
  );

create index events_dates_idx on public.events (start_date, end_date);
commit;
