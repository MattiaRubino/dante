import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { timelineCanonicalRevisionForDisplayEdit } from './timeline-canonical-revision';
import type {
  TimelineCanonicalScheduleBasis,
  TimelineCanonicalScheduledActivityBasis,
  TimelineCanonicalScheduledEventBasis,
} from './timeline-types';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const EVENT_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const MATERIAL_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';

function basis(
  placement: TimelineCanonicalScheduledActivityBasis['placement'],
): TimelineCanonicalScheduledActivityBasis {
  return Object.freeze({
    kind: 'scheduled-activity',
    activityRef: ACTIVITY_REF,
    scheduleRef: SCHEDULE_REF,
    placementMaterialStateRef: MATERIAL_STATE_REF,
    placement,
  });
}

function eventBasis(
  placement: TimelineCanonicalScheduledEventBasis['placement'],
): TimelineCanonicalScheduledEventBasis {
  return Object.freeze({
    kind: 'scheduled-event',
    eventRef: EVENT_REF,
    scheduleRef: SCHEDULE_REF,
    placementMaterialStateRef: MATERIAL_STATE_REF,
    placement,
  });
}

function reviseFloating(basisValue: TimelineCanonicalScheduleBasis) {
  return timelineCanonicalRevisionForDisplayEdit({
    basis: basisValue,
    fromDateKey: '2026-09-16',
    previousStartMinute: 600,
    previousEndMinute: 690,
    toDateKey: '2026-09-17',
    startMinute: 780,
    endMinute: 870,
    effectiveZoneId: 'Europe/Rome',
  });
}

describe('B02-E3 / B03-C canonical Timeline revision', () => {
  it('moves floating-local wall-clock intent without changing form', () => {
    const revision = reviseFloating(
      basis({
        kind: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-16T10:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-16T11:30'),
      }),
    );

    expect(revision?.previous).toMatchObject({
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-16T10:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-16T11:30'),
    });
    expect(revision?.next).toMatchObject({
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-17T13:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-17T14:30'),
    });
  });

  it('uses the same Schedule revision semantics for Event without collapsing Event identity', () => {
    const canonicalBasis = eventBasis({
      kind: 'floating-local',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-16T10:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-16T11:30'),
    });
    const revision = reviseFloating(canonicalBasis);

    expect(canonicalBasis.kind).toBe('scheduled-event');
    expect(canonicalBasis.eventRef).toBe(EVENT_REF);
    expect(canonicalBasis.scheduleRef).toBe(SCHEDULE_REF);
    expect(revision?.previous).toMatchObject({
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-16T10:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-16T11:30'),
    });
    expect(revision?.next).toMatchObject({
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-17T13:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-17T14:30'),
    });
  });

  it('moves an absolute interval through the effective viewing zone while retaining absolute instants', () => {
    const revision = timelineCanonicalRevisionForDisplayEdit({
      basis: basis({
        kind: 'absolute',
        startsAt: Temporal.Instant.from('2026-09-16T08:00:00Z'),
        endsAt: Temporal.Instant.from('2026-09-16T09:00:00Z'),
      }),
      fromDateKey: '2026-09-16',
      previousStartMinute: 600,
      previousEndMinute: 660,
      toDateKey: '2026-09-16',
      startMinute: 720,
      endMinute: 780,
      effectiveZoneId: 'Europe/Rome',
    });

    expect(revision?.next.kind).toBe('absolute-interval');
    if (revision?.next.kind !== 'absolute-interval') {
      throw new Error('Expected an absolute revision.');
    }
    expect(revision.next.startsAt.toString()).toBe('2026-09-16T10:00:00Z');
    expect(revision.next.endsAt.toString()).toBe('2026-09-16T11:00:00Z');
  });

  it('reconstructs a retained later-overlap named-zone placement for revision Undo', () => {
    const revision = timelineCanonicalRevisionForDisplayEdit({
      basis: basis({
        kind: 'named-zone-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:40'),
        zoneId: 'Europe/Rome',
        resolvedStartAt: Temporal.Instant.from('2026-10-25T01:10:00Z'),
        resolvedEndAt: Temporal.Instant.from('2026-10-25T01:40:00Z'),
      }),
      fromDateKey: '2026-10-25',
      previousStartMinute: 130,
      previousEndMinute: 160,
      toDateKey: '2026-10-25',
      startMinute: 250,
      endMinute: 280,
      effectiveZoneId: 'Europe/Rome',
    });

    expect(revision?.previous).toMatchObject({
      kind: 'named-zone-local-interval',
      zoneId: 'Europe/Rome',
      disambiguation: 'later',
    });
    expect(revision?.next).toMatchObject({
      kind: 'named-zone-local-interval',
      zoneId: 'Europe/Rome',
      disambiguation: 'reject',
      startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T04:10'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T04:40'),
    });
  });

  it('fails closed when an exact drag would land in a DST gap', () => {
    const revision = timelineCanonicalRevisionForDisplayEdit({
      basis: basis({
        kind: 'named-zone-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-03-29T01:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-03-29T01:30'),
        zoneId: 'Europe/Rome',
        resolvedStartAt: Temporal.Instant.from('2026-03-29T00:00:00Z'),
        resolvedEndAt: Temporal.Instant.from('2026-03-29T00:30:00Z'),
      }),
      fromDateKey: '2026-03-29',
      previousStartMinute: 60,
      previousEndMinute: 90,
      toDateKey: '2026-03-29',
      startMinute: 150,
      endMinute: 180,
      effectiveZoneId: 'Europe/Rome',
    });

    expect(revision).toBeNull();
  });

  it('fails closed when an absolute drag targets an ambiguous viewing-zone wall clock', () => {
    const revision = timelineCanonicalRevisionForDisplayEdit({
      basis: basis({
        kind: 'absolute',
        startsAt: Temporal.Instant.from('2026-10-24T23:00:00Z'),
        endsAt: Temporal.Instant.from('2026-10-24T23:30:00Z'),
      }),
      fromDateKey: '2026-10-25',
      previousStartMinute: 60,
      previousEndMinute: 90,
      toDateKey: '2026-10-25',
      startMinute: 150,
      endMinute: 180,
      effectiveZoneId: 'Europe/Rome',
    });

    expect(revision).toBeNull();
  });
});
