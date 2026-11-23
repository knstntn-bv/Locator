import { test } from 'node:test';
import assert from 'node:assert/strict';
import { formatEventDates } from '../src/event-dates.ts';

const event = { start_date: '2026-11-23', end_date: '2026-11-24', start_time: null, end_time: null, timezone: 'Europe/Moscow' };
test('missing times are not replaced by midnight', () => {
  assert.equal(formatEventDates(event), '23.11.2026 — 24.11.2026 · Время не указано');
});
test('each time can be independently absent', () => {
  assert.match(formatEventDates({ ...event, start_time: '12:00:00' }), /с 12:00, окончание без времени/);
  assert.match(formatEventDates({ ...event, end_time: '18:00:00' }), /начало без времени, до 18:00/);
});
test('single day and explicit midnight are displayed correctly', () => {
  assert.equal(formatEventDates({ ...event, end_date: event.start_date, start_time: '00:00:00', end_time: '18:00:00' }), '23.11.2026 · с 00:00, до 18:00 (Europe/Moscow)');
});
