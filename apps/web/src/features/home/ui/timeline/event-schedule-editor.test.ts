import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  eventScheduleDraftFromPlacement,
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
});
