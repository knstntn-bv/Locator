interface EventDates {
  start_date: string;
  end_date: string;
  start_time: string | null;
  end_time: string | null;
  timezone: string;
}

export function formatEventDates(event: EventDates): string {
  const formatDate = (value: string) => value.split('-').reverse().join('.');
  const start = formatDate(event.start_date);
  const end = formatDate(event.end_date);
  const dates = start === end ? start : `${start} — ${end}`;
  if (!event.start_time && !event.end_time) return `${dates} · Время не указано`;
  const from = event.start_time ? `с ${event.start_time.slice(0, 5)}` : 'начало без времени';
  const to = event.end_time ? `до ${event.end_time.slice(0, 5)}` : 'окончание без времени';
  return `${dates} · ${from}, ${to} (${event.timezone})`;
}
