import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type { TemporalTimelineScheduledActivityItem } from '../../../temporal/timeline-read';
import {
  canonicalScheduledActivityDateLaneItem,
  canonicalScheduledActivityTimelineEvent,
} from './timeline-authoritative-hydration';
import { TimelineAllDayLane } from './timeline-all-day-layer';
import { TimelineCanonicalActionsProvider } from './timeline-canonical-actions';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const MATERIAL_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function common() {
  return Object.freeze({
    kind: 'scheduled_activity' as const,
    activityRef: ACTIVITY_REF,
    scheduleRef: SCHEDULE_REF,
    placementMaterialStateRef: MATERIAL_STATE_REF,
  });
}

describe('B02-E3 Schedule form rendering', () => {
  it('projects date-span into the date lane with exact half-open canonical basis', () => {
    const item = Object.freeze({
      ...common(),
      title: 'Conferenza',
      temporalForm: 'date-span' as const,
      startDate: Temporal.PlainDate.from('2026-09-16'),
      endDateExclusive: Temporal.PlainDate.from('2026-09-18'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const laneItem = canonicalScheduledActivityDateLaneItem(item);

    expect(laneItem).toMatchObject({
      id: SCHEDULE_REF,
      startDateKey: '2026-09-16',
      endDateExclusiveKey: '2026-09-18',
      laneKind: 'all-day',
      canonicalBasis: {
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef: MATERIAL_STATE_REF,
        placement: {
          kind: 'date-span',
        },
      },
    });
    expect(laneItem?.canonicalBasis?.placement.kind).toBe('date-span');
  });

  it('renders coarse precision without fake clock geometry and routes unschedule through the canonical basis', () => {
    const item = Object.freeze({
      ...common(),
      title: 'Scrivere relazione',
      temporalForm: 'coarse-local-period' as const,
      localDate: Temporal.PlainDate.from('2026-09-16'),
      period: 'afternoon' as const,
    }) satisfies TemporalTimelineScheduledActivityItem;
    const laneItem = canonicalScheduledActivityDateLaneItem(item);
    if (laneItem === null || laneItem.canonicalBasis === undefined) {
      throw new Error('Expected a canonical coarse date-lane projection.');
    }
    const unschedule = vi.fn();

    const { container } = render(
      <TimelineCanonicalActionsProvider
        actions={{ pendingScheduleRef: null, unschedule }}
      >
        <TimelineAllDayLane
          dateKey="2026-09-16"
          items={[laneItem]}
          groups={[
            Object.freeze({ id: 'personale', label: 'Personale', tone: 'personal' }),
          ]}
          filters={new Set()}
        />
      </TimelineCanonicalActionsProvider>,
    );

    expect(screen.getByText('Fascia')).toBeTruthy();
    expect(screen.getByText('Scrivere relazione')).toBeTruthy();
    expect(screen.getByText(/Pomeriggio · Personale/)).toBeTruthy();
    const coarseButton = screen.getByRole('button', {
      name: 'Scrivere relazione · Pomeriggio · Personale',
    });
    expect(coarseButton.getAttribute('data-timeline-date-lane-kind')).toBe(
      'coarse',
    );
    expect(laneItem.canonicalBasis.placement).toMatchObject({
      kind: 'coarse-local-period',
      period: 'afternoon',
    });

    const unscheduleButton = container.querySelector<HTMLButtonElement>(
      `[data-timeline-unschedule-schedule="${SCHEDULE_REF}"]`,
    );
    expect(unscheduleButton).not.toBeNull();
    if (unscheduleButton === null) {
      throw new Error('Expected the governed unschedule action.');
    }
    fireEvent.click(unscheduleButton);
    expect(unschedule).toHaveBeenCalledTimes(1);
    expect(unschedule).toHaveBeenCalledWith(laneItem.canonicalBasis);
  });

  it('retains named-zone source intent while rendering effective-zone coordinates', () => {
    const item = Object.freeze({
      ...common(),
      title: 'Call Tokyo',
      temporalForm: 'named-zone-local' as const,
      startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:40'),
      zoneId: 'Europe/Rome',
      resolvedStartAt: Temporal.Instant.from('2026-10-25T01:10:00Z'),
      resolvedEndAt: Temporal.Instant.from('2026-10-25T01:40:00Z'),
      displayStartsLocalAt: Temporal.PlainDateTime.from('2026-10-25T09:10'),
      displayEndsLocalAt: Temporal.PlainDateTime.from('2026-10-25T09:40'),
    }) satisfies TemporalTimelineScheduledActivityItem;

    const projection = canonicalScheduledActivityTimelineEvent(item);

    expect(projection.event.startMinute).toBe(550);
    expect(projection.event.endMinute).toBe(580);
    expect(projection.event.meta).toBe('Europe/Rome');
    expect(projection.event.canonicalBasis?.placement).toMatchObject({
      kind: 'named-zone-local',
      zoneId: 'Europe/Rome',
      startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10'),
      resolvedStartAt: Temporal.Instant.from('2026-10-25T01:10:00Z'),
    });
  });
});
