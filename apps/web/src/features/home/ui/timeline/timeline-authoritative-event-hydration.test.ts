import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalTimelineScheduledEventItem } from '../../../temporal/timeline-read';
import {
  canonicalScheduledDateLaneItem,
  canonicalScheduledTimelineEvents,
} from './timeline-authoritative-hydration';

const EVENT_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
const MATERIAL_STATE_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';

function floatingEvent(): TemporalTimelineScheduledEventItem {
  return Object.freeze({
    kind: 'scheduled_event',
    eventRef: EVENT_REF,
    scheduleRef: SCHEDULE_REF,
    placementMaterialStateRef: MATERIAL_STATE_REF,
    title: 'Evento B03-B',
    temporalForm: 'floating-local',
    startsLocalAt: Temporal.PlainDateTime.from('2026-09-17T18:30'),
    endsLocalAt: Temporal.PlainDateTime.from('2026-09-17T20:00'),
  });
}

describe('authoritative Event Timeline hydration', () => {
  it('renders a timed Event through Schedule identity while retaining Event identity', () => {
    const [projection] = canonicalScheduledTimelineEvents(floatingEvent());

    expect(projection).toMatchObject({
      dateKey: '2026-09-17',
      event: {
        id: SCHEDULE_REF,
        startMinute: 1110,
        endMinute: 1200,
        title: 'Evento B03-B',
        canonicalBasis: {
          kind: 'scheduled-event',
          eventRef: EVENT_REF,
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: MATERIAL_STATE_REF,
        },
      },
    });
    expect(projection?.event.canonicalBasis?.activityRef).toBeUndefined();
  });

  it('renders a multi-day date-span Event in the date lane without clock geometry', () => {
    const event = Object.freeze({
      kind: 'scheduled_event' as const,
      eventRef: EVENT_REF,
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: MATERIAL_STATE_REF,
      title: 'Conferenza',
      temporalForm: 'date-span' as const,
      startDate: Temporal.PlainDate.from('2026-09-18'),
      endDateExclusive: Temporal.PlainDate.from('2026-09-21'),
    }) satisfies TemporalTimelineScheduledEventItem;

    expect(canonicalScheduledTimelineEvents(event)).toEqual([]);
    expect(canonicalScheduledDateLaneItem(event)).toMatchObject({
      id: SCHEDULE_REF,
      startDateKey: '2026-09-18',
      endDateExclusiveKey: '2026-09-21',
      title: 'Conferenza',
      laneKind: 'all-day',
      canonicalBasis: {
        kind: 'scheduled-event',
        eventRef: EVENT_REF,
        scheduleRef: SCHEDULE_REF,
      },
    });
  });
});
