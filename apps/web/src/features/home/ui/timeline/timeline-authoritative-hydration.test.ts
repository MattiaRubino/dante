import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalTimelineScheduledActivityItem } from '../../../temporal/timeline-read';
import { canonicalScheduledActivityTimelineEvent } from './timeline-authoritative-hydration';

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

  it('carries the new exact MaterialState basis for the same revised Schedule identity', () => {
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
});
