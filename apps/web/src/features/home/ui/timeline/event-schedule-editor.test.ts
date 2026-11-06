import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  eventScheduleDraftFromPlacement,
  eventScheduleHasAmbiguousHour,
  eventSchedulePlacementFromDraft,
} from './event-schedule-editor';

describe('Event Schedule edit conversion', () => {
  it('preserves a full-day exclusive end without shifting the displayed last date', () => {
    const draft = eventScheduleDraftFromPlacement({
      kind: 'date-span',
      startDate: Temporal.PlainDate.from('2026-11-05'),
      endDateExclusive: Temporal.PlainDate.from('2026-11-07'),
    });
    expect(draft?.endDate).toBe('2026-11-06');
    expect(eventSchedulePlacementFromDraft(draft!)).toEqual({
      kind: 'date_span',
      start_date: '2026-11-05',
      end_date_exclusive: '2026-11-07',
    });
  });

  it('refuses a reversed timed window before submitting any mutation', () => {
    const draft = eventScheduleDraftFromPlacement({
      kind: 'floating-local',
      startsLocalAt: Temporal.PlainDateTime.from('2026-11-05T19:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-11-05T19:30'),
    });
    expect(() =>
      eventSchedulePlacementFromDraft({ ...draft!, endTime: '18:30' }),
    ).toThrow('successiva');
  });

  it('offers the clock-change choice only when a named-zone endpoint repeats', () => {
    const ordinary = {
      kind: 'timed' as const,
      startDate: '2026-11-06',
      endDate: '2026-11-06',
      startTime: '13:30',
      endTime: '14:00',
      zoneId: 'Europe/Rome',
      disambiguation: 'reject' as const,
    };
    expect(eventScheduleHasAmbiguousHour(ordinary)).toBe(false);
    expect(
      eventScheduleHasAmbiguousHour({
        ...ordinary,
        startDate: '2026-10-25',
        endDate: '2026-10-25',
        startTime: '02:15',
        endTime: '02:45',
      }),
    ).toBe(true);
    expect(
      eventScheduleHasAmbiguousHour({
        ...ordinary,
        startDate: '2026-03-29',
        endDate: '2026-03-29',
        startTime: '02:15',
        endTime: '02:45',
      }),
    ).toBe(false);
  });
});
