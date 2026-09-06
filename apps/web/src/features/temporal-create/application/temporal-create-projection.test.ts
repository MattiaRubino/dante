import { describe, expect, it } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import { temporalCreateTimelinePreviewFromFields } from './temporal-create-projection';

describe('Temporal Create Timeline projection', () => {
  it('preserves the exclusive end of an all-day Event date span', () => {
    const baseline = createTemporalCreateFields({
      title: 'Fiera',
      kind: 'event',
      date: '2026-08-04',
      timeSemantics: 'all-day',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: {
        ...baseline.event,
        allDayEndDate: '2026-08-06',
      },
    });

    const projection = temporalCreateTimelinePreviewFromFields(fields);

    expect(projection).not.toBeNull();
    expect(projection?.allDay).toBe(true);
    expect(projection?.dateKey).toBe('2026-08-04');
    expect(projection?.endDateExclusiveKey).toBe('2026-08-07');
    expect(projection?.startMinute).toBeNull();
    expect(projection?.endMinute).toBeNull();
  });

  it('does not invent a date-span end for timed placement', () => {
    const fields = createTemporalCreateFields({
      title: 'Call',
      kind: 'event',
      date: '2026-08-04',
      startTime: '16:00',
      durationMinutes: 60,
    });
    const projection = temporalCreateTimelinePreviewFromFields(fields);

    expect(projection?.allDay).toBe(false);
    expect(projection?.endDateExclusiveKey).toBeNull();
  });

  it('carries ordered Event agenda parts without creating child Event identities', () => {
    const baseline = createTemporalCreateFields({
      title: 'Lezione inglese',
      kind: 'event',
      date: '2026-08-04',
      startTime: '18:00',
      durationMinutes: 90,
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: {
        ...baseline.event,
        agendaParts: Object.freeze(['Listening', 'Orale', 'Scritto']),
      },
    });

    const projection = temporalCreateTimelinePreviewFromFields(fields);

    expect(projection?.kind).toBe('event');
    expect(projection?.id).toBe('temporal-create-preview');
    expect(projection?.agendaParts).toEqual(['Listening', 'Orale', 'Scritto']);
    expect(Object.isFrozen(projection?.agendaParts)).toBe(true);
  });

  it('marks a Routine-backed repeated Activity projection recurring without inventing child identities', () => {
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-08-04',
      startTime: '18:00',
      durationMinutes: 60,
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        owner: 'routine',
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaPeriodInterval: 1,
      },
    });

    const projection = temporalCreateTimelinePreviewFromFields(fields);

    expect(projection?.kind).toBe('activity');
    expect(projection?.recurring).toBe(true);
    expect(projection?.id).toBe('temporal-create-preview');
    expect(projection?.agendaParts).toEqual([]);
  });
});
