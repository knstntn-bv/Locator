import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dateBounds } from '../src/dates.ts';

test('both calendar date bounds are inclusive and unchanged', () => {
  const bounds = dateBounds('2026-11-23', '2026-11-23');
  assert.equal(bounds.from, '2026-11-23');
  assert.equal(bounds.until, '2026-11-23');
});
test('range crosses month and year boundaries', () => {
  assert.deepEqual(dateBounds('2026-12-31', '2027-01-02'), { from: '2026-12-31', until: '2027-01-02' });
});
test('invalid and reversed dates are rejected', () => {
  for (const [from, to] of [['', '2026-11-23'], ['2026-11-24', '2026-11-23'], ['2026-02-30', '2026-03-01']]) {
    assert.throws(() => dateBounds(from, to));
  }
});
