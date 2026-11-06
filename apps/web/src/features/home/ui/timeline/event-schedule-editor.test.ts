// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { describe, expect, it, vi } from 'vitest';

import {
  EventScheduleEditor,
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

  it('automatically chooses one fold and never exposes a DST selector', () => {
    const repeatedHour = {
      kind: 'timed' as const,
      startDate: '2026-10-25',
      endDate: '2026-10-25',
      startTime: '02:15',
      endTime: '02:45',
      zoneId: 'Europe/Rome',
      disambiguation: 'earlier' as const,
    };
    render(
      createElement(EventScheduleEditor, {
        draft: repeatedHour,
        onChange: vi.fn(),
        disabled: false,
        error: '',
      }),
    );
    expect(screen.queryByText('Cambio dell’ora')).toBeNull();
    expect(screen.queryByText('Rifiuta orari ambigui')).toBeNull();
    expect(eventSchedulePlacementFromDraft(repeatedHour)).toMatchObject({
      disambiguation: 'earlier',
    });
  });

  it('keeps the original later instant when editing a saved Event in the repeated hour', () => {
    const start = Temporal.PlainDateTime.from('2026-10-25T02:15');
    const end = Temporal.PlainDateTime.from('2026-10-25T02:45');
    const placement = {
      kind: 'named-zone-local' as const,
      startsLocalAt: start,
      endsLocalAt: end,
      zoneId: 'Europe/Rome',
      resolvedStartAt: start
        .toZonedDateTime('Europe/Rome', { disambiguation: 'later' })
        .toInstant(),
      resolvedEndAt: end
        .toZonedDateTime('Europe/Rome', { disambiguation: 'later' })
        .toInstant(),
    };
    const draft = eventScheduleDraftFromPlacement(placement);
    expect(draft?.disambiguation).toBe('later');
    expect(eventSchedulePlacementFromDraft(draft!)).toMatchObject({
      disambiguation: 'later',
    });
  });

  it('rejects a new spring gap and retains an untouched saved placement', () => {
    const base = {
      kind: 'timed' as const,
      startDate: '2026-03-29',
      endDate: '2026-03-29',
      startTime: '01:30',
      endTime: '03:30',
      zoneId: 'Europe/Rome',
      disambiguation: 'earlier' as const,
    };
    expect(() =>
      eventSchedulePlacementFromDraft({ ...base, endTime: '02:30' }),
    ).toThrow('non esiste');
    expect(() =>
      eventSchedulePlacementFromDraft({ ...base, startTime: '02:30' }),
    ).toThrow('non esiste');
    const existingGap = {
      ...base,
      endTime: '02:30',
      original: {
        start: '2026-03-29T01:30:00',
        end: '2026-03-29T02:30:00',
        zoneId: 'Europe/Rome',
      },
    };
    expect(eventSchedulePlacementFromDraft(existingGap)).toMatchObject({
      kind: 'named_zone_local_interval',
      ends_local_at: '2026-03-29T02:30:00',
    });
    expect(() =>
      eventSchedulePlacementFromDraft({
        ...existingGap,
        zoneId: 'Europe/Paris',
      }),
    ).toThrow('non esiste');
  });
});
