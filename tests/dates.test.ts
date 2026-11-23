import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dateBounds } from '../src/dates.ts';

test('end date is inclusive, using next local midnight as exclusive bound', () => {
  const bounds = dateBounds('2026-11-23', '2026-11-23');
  assert.equal(bounds.from, new Date(2026, 10, 23).toISOString());
  assert.equal(bounds.until, new Date(2026, 10, 24).toISOString());
});
test('range crosses month and year boundaries', () => {
  assert.equal(dateBounds('2026-12-31', '2026-12-31').until, new Date(2027, 0, 1).toISOString());
});
test('invalid and reversed dates are rejected', () => {
  for (const [from, to] of [['', '2026-11-23'], ['2026-11-24', '2026-11-23'], ['2026-02-30', '2026-03-01']]) {
    assert.throws(() => dateBounds(from, to));
  }
});
