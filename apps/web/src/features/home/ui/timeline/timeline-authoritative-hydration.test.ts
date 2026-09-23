import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type {
  TemporalTimelineExpectedOccurrenceItem,
  TemporalTimelineScheduledActivityItem,
  TemporalTimelineScheduledOccurrenceItem,
} from '../../../temporal/timeline-read';
import {
  canonicalScheduledTimelineEvent,
  canonicalScheduledActivityTimelineEvent,
  canonicalScheduledActivityTimelineEvents,
  expectedOccurrenceDateLaneItem,
} from './timeline-authoritative-hydration';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const MATERIAL_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';

function scheduledActivity(): TemporalTimelineScheduledActivityItem {
  return Object.freeze({
    kind: 'scheduled_activity',
    activityRef: ACTIVITY_REF,
    scheduleRef: SCHEDULE_REF,
    placementMaterialStateRef: MATERIAL_STATE_REF,
    title: 'Scrivere specifica B02-A',
    temporalForm: 'floating-local',
    startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T13:15:30.500'),
    endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:45:30.500'),
  });
}

describe('authoritative Timeline hydration', () => {
  it('keys the visible projection on Schedule identity and retains its exact canonical basis', () => {
    const projection =
      canonicalScheduledActivityTimelineEvent(scheduledActivity());

    expect(projection.dateKey).toBe('2026-09-09');
    expect(projection.event).toMatchObject({
      id: SCHEDULE_REF,
      title: 'Scrivere specifica B02-A',
      groupId: 'personale',
      appearanceTone: 'personal',
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: ACTIVITY_REF,
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef: MATERIAL_STATE_REF,
      },
    });
    expect(projection.event.startMinute).toBeCloseTo(795.508333, 5);
    expect(projection.event.endMinute).toBeCloseTo(885.508333, 5);
  });

  it('carries a new exact MaterialState basis for revision or restored Undo', () => {
    const revised = Object.freeze({
      ...scheduledActivity(),
      placementMaterialStateRef: '0199a8c0-5e76-7bc0-8ad0-a2f403f5617d',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-10T09:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T10:00'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const projection = canonicalScheduledActivityTimelineEvent(revised);

    expect(projection.dateKey).toBe('2026-09-10');
    expect(projection.event.id).toBe(SCHEDULE_REF);
    expect(projection.event.canonicalBasis?.placementMaterialStateRef).toBe(
      '0199a8c0-5e76-7bc0-8ad0-a2f403f5617d',
    );
    expect(projection.event.canonicalBasis?.placementMaterialStateRef).not.toBe(
      MATERIAL_STATE_REF,
    );
  });

  it('does not collapse two Schedule identities for the same Activity', () => {
    const first = scheduledActivity();
    const second = Object.freeze({
      ...first,
      scheduleRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
      placementMaterialStateRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T17:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T18:00'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const firstProjection = canonicalScheduledActivityTimelineEvent(first);
    const secondProjection = canonicalScheduledActivityTimelineEvent(second);

    expect(firstProjection.event.id).not.toBe(secondProjection.event.id);
    expect(firstProjection.event.canonicalBasis?.activityRef).toBe(
      secondProjection.event.canonicalBasis?.activityRef,
    );
  });

  it('splits a cross-midnight exact placement only in the view while retaining one Schedule identity', () => {
    const item = Object.freeze({
      ...scheduledActivity(),
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T23:30'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T01:15'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const projections = canonicalScheduledActivityTimelineEvents(item);

    expect(projections).toHaveLength(2);
    expect(projections[0]).toMatchObject({
      dateKey: '2026-09-09',
      event: {
        id: `${SCHEDULE_REF}@2026-09-09`,
        startMinute: 1410,
        endMinute: 1440,
        canonicalBasis: { scheduleRef: SCHEDULE_REF },
      },
    });
    expect(projections[1]).toMatchObject({
      dateKey: '2026-09-10',
      event: {
        id: `${SCHEDULE_REF}@2026-09-10`,
        startMinute: 0,
        endMinute: 75,
        canonicalBasis: { scheduleRef: SCHEDULE_REF },
      },
    });
  });

  it('uses the effective-zone display coordinates for named-zone and absolute placements', () => {
    const named = Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: ACTIVITY_REF,
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: MATERIAL_STATE_REF,
      title: 'Named zone',
      temporalForm: 'named-zone-local' as const,
      startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:40'),
      zoneId: 'Europe/Rome',
      resolvedStartAt: Temporal.Instant.from('2026-10-25T01:10:00Z'),
      resolvedEndAt: Temporal.Instant.from('2026-10-25T01:40:00Z'),
      displayStartsLocalAt: Temporal.PlainDateTime.from('2026-10-25T09:10'),
      displayEndsLocalAt: Temporal.PlainDateTime.from('2026-10-25T09:40'),
    }) satisfies TemporalTimelineScheduledActivityItem;
    const absolute = Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: ACTIVITY_REF,
      scheduleRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
      placementMaterialStateRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
      title: 'Absolute',
      temporalForm: 'absolute' as const,
      startsAt: Temporal.Instant.from('2026-09-09T07:00:00Z'),
      endsAt: Temporal.Instant.from('2026-09-09T08:00:00Z'),
      displayStartsLocalAt: Temporal.PlainDateTime.from('2026-09-09T09:00'),
      displayEndsLocalAt: Temporal.PlainDateTime.from('2026-09-09T10:00'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const namedProjection = canonicalScheduledActivityTimelineEvent(named);
    const absoluteProjection =
      canonicalScheduledActivityTimelineEvent(absolute);

    expect(namedProjection.event.startMinute).toBe(550);
    expect(namedProjection.event.endMinute).toBe(580);
    expect(namedProjection.event.meta).toBe('Europe/Rome');
    expect(absoluteProjection.event.startMinute).toBe(540);
    expect(absoluteProjection.event.endMinute).toBe(600);
    expect(absoluteProjection.event.meta).toBe('absolute');
  });

  it('does not manufacture time-grid geometry for date-span or coarse placements', () => {
    const dateSpan = Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: ACTIVITY_REF,
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: MATERIAL_STATE_REF,
      title: 'All day',
      temporalForm: 'date-span' as const,
      startDate: Temporal.PlainDate.from('2026-09-09'),
      endDateExclusive: Temporal.PlainDate.from('2026-09-10'),
    }) satisfies TemporalTimelineScheduledActivityItem;
    const coarse = Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: ACTIVITY_REF,
      scheduleRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
      placementMaterialStateRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
      title: 'Pomeriggio',
      temporalForm: 'coarse-local-period' as const,
      localDate: Temporal.PlainDate.from('2026-09-09'),
      period: 'afternoon' as const,
    }) satisfies TemporalTimelineScheduledActivityItem;

    expect(canonicalScheduledActivityTimelineEvents(dateSpan)).toEqual([]);
    expect(canonicalScheduledActivityTimelineEvents(coarse)).toEqual([]);
  });

  it('retains Occurrence identity and source ownership on an accepted Schedule', () => {
    const item = Object.freeze({
      kind: 'scheduled_occurrence' as const,
      occurrenceRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
      sourceKind: 'routine' as const,
      sourceNativeRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: MATERIAL_STATE_REF,
      title: 'Farmaco',
      coordinate: null,
      temporalForm: 'floating-local' as const,
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T08:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T08:15'),
    }) satisfies TemporalTimelineScheduledOccurrenceItem;

    const projection = canonicalScheduledTimelineEvent(item);

    expect(projection.event.canonicalBasis).toMatchObject({
      kind: 'scheduled-occurrence',
      occurrenceRef: item.occurrenceRef,
      sourceKind: 'routine',
      sourceNativeRef: item.sourceNativeRef,
      scheduleRef: SCHEDULE_REF,
    });
  });

  it('renders quota expectations as flexible date-lane periods without clock geometry', () => {
    const item = Object.freeze({
      kind: 'expected_occurrence' as const,
      occurrenceRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
      sourceKind: 'event' as const,
      sourceNativeRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
      title: 'Allenamenti',
      coordinate: Object.freeze({
        familyCode: 'quota-per-period' as const,
        periodStartDate: Temporal.PlainDate.from('2026-09-07'),
        periodEndDateExclusive: Temporal.PlainDate.from('2026-09-14'),
        frame: 'floating-local' as const,
        zoneId: null,
      }),
    }) satisfies TemporalTimelineExpectedOccurrenceItem;

    expect(expectedOccurrenceDateLaneItem(item, 'Europe/Rome')).toMatchObject({
      id: item.occurrenceRef,
      startDateKey: '2026-09-07',
      endDateExclusiveKey: '2026-09-14',
      laneKind: 'flexible',
    });
  });
});
