import { describe, expect, it } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import { applyTemporalCreateFieldSeed } from './temporal-create-seed';

describe('Temporal Create semantic seed', () => {
  it('deep-merges structured intent without replacing unrelated defaults', () => {
    const base = createTemporalCreateFields({
      date: '2026-09-02',
      timeZoneId: 'Europe/Rome',
      contextId: 'focus',
    });
    const seeded = applyTemporalCreateFieldSeed(base, {
      title: 'Review trimestrale',
      kind: 'event',
      durationMinutes: 90,
      eventRecurrence: {
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaFrame: 'named-zone',
        quotaWeekStart: 'MO',
        quotaTimeZoneId: 'Europe/Rome',
      },
      event: {
        purpose: 'Chiudere le decisioni aperte',
      },
    });

    expect(seeded.title).toBe('Review trimestrale');
    expect(seeded.kind).toBe('event');
    expect(seeded.durationMinutes).toBe(90);
    expect(seeded.contextId).toBe('focus');
    expect(seeded.timeZoneId).toBe('Europe/Rome');
    expect(seeded.eventRecurrence.patternKind).toBe('quota-per-period');
    expect(seeded.eventRecurrence.quotaCount).toBe(3);
    expect(seeded.eventRecurrence.quotaPeriodInterval).toBe(1);
    expect(seeded.event.purpose).toBe('Chiudere le decisioni aperte');
    expect(seeded.event.visibility).toBe('default');
  });

  it('preserves owner normalization instead of letting a seed invent Activity recurrence', () => {
    const base = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-09-02',
    });
    const seeded = applyTemporalCreateFieldSeed(base, {
      eventRecurrence: {
        patternKind: 'elapsed-interval',
        elapsedIntervalMinutes: 1440,
      },
    });

    expect(seeded.kind).toBe('activity');
    expect(seeded.eventRecurrence.patternKind).toBe('none');
  });

  it('keeps unresolved or invalid interpreted values subject to normal Create validation', () => {
    const base = createTemporalCreateFields({
      date: '2026-09-02',
      timeZoneId: 'Europe/Rome',
    });
    const seeded = applyTemporalCreateFieldSeed(base, {
      title: 'Call',
      kind: 'event',
      timeMode: 'zoned',
      timeZoneId: 'Europe/Not-A-Zone',
    });

    expect(seeded.timeZoneId).toBe('Europe/Not-A-Zone');
    expect(seeded.title).toBe('Call');
  });
});
