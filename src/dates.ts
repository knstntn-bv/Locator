export function dateInputValue(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

// Compare calendar dates as stored, without converting them between timezones.
export function dateBounds(start: string, end: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end) || start > end) {
    throw new Error('Укажите корректный интервал: начало не позже окончания.');
  }
  const from = new Date(`${start}T00:00:00Z`);
  const until = new Date(`${end}T00:00:00Z`);
  if (Number.isNaN(+from) || Number.isNaN(+until) || from.toISOString().slice(0, 10) !== start || until.toISOString().slice(0, 10) !== end) {
    throw new Error('Укажите существующие даты.');
  }
  return { from: start, until: end };
}
