import { describe, expect, it } from 'vitest';

import type { RecurringSeriesSource } from '../../../temporal/remote-recurring-series-edit';
import { initialRecurrenceForScope } from './recurring-series-bounds';

const base: RecurringSeriesSource = {
  sourceRef: '0199a111-1111-7111-8111-111111111111',
  owner: 'event',
  selectedDate: '2026-11-29',
  editRevision: 2,
  recurrenceStateRef: '0199a222-2222-7222-8222-222222222222',
  title: 'Serie bisettimanale',
  description: null,
  location: null,
  colorCode: null,
  recurrence: {
    family_code: 'calendar_wall_clock',
    pattern_code: 'weekly_weekdays',
    interval_count: 2,
    effective_from: '2026-11-15',
    range_kind: 'expected_count',
    expected_occurrence_count: 5,
  },
  structure: {},
  remainingIncludingSelected: 4,
  remainingAfterSelected: 3,
};

describe('Finite recurring-series editor boundaries', () => {
  it.each(['event', 'routine'] as const)(
    '%s keeps four remaining including the selected day',
    (owner) => {
      expect(initialRecurrenceForScope({ ...base, owner }, 'this_and_following'))
        .toMatchObject({
          effective_from: '2026-11-29',
          expected_occurrence_count: 4,
        });
    },
  );

  it.each(['event', 'routine'] as const)(
    '%s keeps three after the selected day for from-next',
    (owner) => {
      expect(initialRecurrenceForScope({ ...base, owner }, 'from_next'))
        .toMatchObject({
          effective_from: '2026-11-30',
          expected_occurrence_count: 3,
        });
    },
  );

  it('retains an explicit edited count rather than forcing the original count', () => {
    const draft = initialRecurrenceForScope(base, 'this_and_following');
    expect({ ...draft, expected_occurrence_count: 7 })
      .toMatchObject({ expected_occurrence_count: 7 });
  });

  it('allows an unchanged open recurrence without finite metadata', () => {
    expect(initialRecurrenceForScope({
      ...base,
      recurrence: { ...base.recurrence, range_kind: 'open', expected_occurrence_count: null },
      remainingIncludingSelected: null,
      remainingAfterSelected: null,
    }, 'from_next')).toMatchObject({
      effective_from: '2026-11-30',
      range_kind: 'open',
      expected_occurrence_count: null,
    });
  });

  it('rejects missing bounded metadata instead of extending silently', () => {
    const incomplete = { ...base };
    delete incomplete.remainingIncludingSelected;
    expect(() =>
      initialRecurrenceForScope(incomplete, 'this_and_following'),
    ).toThrow('Limite della serie finita non disponibile.');
  });

  it('allows zero remaining after the final instance to be refused on Save', () => {
    expect(initialRecurrenceForScope({
      ...base, remainingAfterSelected: 0,
    }, 'from_next')).toMatchObject({ expected_occurrence_count: 0 });
  });
});
