import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { buildEventDuplicateSeed } from './event-duplicate-seed';

const event = {
  eventRef: '0199a111-1111-7111-8111-111111111111',
  title: 'Conferenza',
  agendaRevision: 3,
  agendaParts: ['Introduzione', 'Domande'],
  createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
  lifeAreaRef: '0199a222-2222-7222-8222-222222222222',
} as const;

const participants = [{
  personRef: '0199a333-3333-7333-8333-333333333333',
  displayLabel: 'Collaboratore',
  requirementCode: 'required' as const,
}];

describe('canonical Event duplicate seed', () => {
  it('copies an exact named-zone Schedule, agenda, Life Area and expected participants', () => {
    const placement = {
      kind: 'named-zone-local' as const,
      startsLocalAt: Temporal.PlainDateTime.from('2026-10-09T09:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-10-09T10:30'),
      zoneId: 'Europe/Rome',
      resolvedStartAt: Temporal.Instant.from('2026-10-09T07:00:00Z'),
      resolvedEndAt: Temporal.Instant.from('2026-10-09T08:30:00Z'),
    };
    const result = buildEventDuplicateSeed(event, placement, participants);
    expect(result.fields).toMatchObject({
      kind: 'event', title: 'Conferenza', contextId: event.lifeAreaRef,
      date: '2026-10-09', timeSemantics: 'timed', timeMode: 'zoned',
      timeZoneId: 'Europe/Rome', startTime: '09:00', durationMinutes: 90,
      event: { agendaParts: ['Introduzione', 'Domande'] },
    });
    expect(result.advanced.eventParticipants).toEqual(participants);
    expect(result.fields).not.toHaveProperty('eventRef');
    expect(result.advanced).not.toHaveProperty('actual');
    expect(event.agendaParts).toEqual(['Introduzione', 'Domande']);
  });

  it('preserves a date span without changing its exclusive end convention', () => {
    const result = buildEventDuplicateSeed(event, {
      kind: 'date-span',
      startDate: Temporal.PlainDate.from('2026-10-09'),
      endDateExclusive: Temporal.PlainDate.from('2026-10-12'),
    });
    expect(result.fields).toMatchObject({
      date: '2026-10-09', timeSemantics: 'all-day',
      event: { allDayEndDate: '2026-10-11' },
    });
    expect(result.advanced.endDate).toBe('2026-10-11');
  });

  it('rejects unsupported absolute time rather than silently moving it', () => {
    expect(() => buildEventDuplicateSeed(event, {
      kind: 'absolute',
      startsAt: Temporal.Instant.from('2026-10-09T07:00:00Z'),
      endsAt: Temporal.Instant.from('2026-10-09T08:00:00Z'),
    })).toThrow('non è duplicabile fedelmente');
  });

  it('preserves coarse local period without inventing a clock time', () => {
    expect(buildEventDuplicateSeed(event, {
      kind: 'coarse-local-period',
      localDate: Temporal.PlainDate.from('2026-10-09'),
      period: 'morning',
    }).fields).toMatchObject({
      timeSemantics: 'coarse', date: '2026-10-09', coarsePeriod: 'morning',
    });
  });
});
