export function dateInputValue(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

// The end is exclusive: advance a calendar day, rather than adding 24 hours (DST).
export function dateBounds(start: string, end: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end) || start > end) {
    throw new Error('Укажите корректный интервал: начало не позже окончания.');
  }
  const from = new Date(`${start}T00:00:00`);
  const until = new Date(`${end}T00:00:00`);
  if (Number.isNaN(+from) || Number.isNaN(+until) || dateInputValue(from) !== start || dateInputValue(until) !== end) {
    throw new Error('Укажите существующие даты.');
  }
  until.setDate(until.getDate() + 1);
  return { from: from.toISOString(), until: until.toISOString() };
}
