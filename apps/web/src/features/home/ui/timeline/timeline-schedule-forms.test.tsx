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
  it('shows two sticky date bars, expands overflow and opens the selected Inspector', () => {
    const onOpen = vi.fn();
    const items = ['Primo', 'Secondo', 'Terzo'].map((title, index) => ({
      id: `local-${index}`,
      title,
      groupId: 'personale',
      startDateKey: '2026-09-16',
      endDateExclusiveKey: '2026-09-20',
      laneKind: 'all-day' as const,
    }));
    const { container } = render(
      <TimelineAllDayLane
        dateKey="2026-09-17"
        items={items}
        groups={[{ id: 'personale', label: 'Personale', tone: 'personal' }]}
        filters={new Set()}
        onOpenItemDetail={onOpen}
      />,
    );

    expect(
      container
        .querySelector('[data-timeline-all-day-lane]')
        ?.getAttribute('style'),
    ).toContain('94px');
    expect(screen.queryByText('Terzo')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: '+ 1' }));
    fireEvent.click(
      screen.getByRole('button', { name: /Terzo · Tutto il giorno/ }),
    );
    expect(onOpen).toHaveBeenCalledWith(items[2], expect.any(HTMLElement));
  });

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

  it('renders coarse precision without fake clock geometry or a remove-placement command', () => {
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
    const { container } = render(
      <TimelineAllDayLane
        dateKey="2026-09-16"
        items={[laneItem]}
        groups={[
          Object.freeze({
            id: 'personale',
            label: 'Personale',
            tone: 'personal',
          }),
        ]}
        filters={new Set()}
      />,
    );

    expect(screen.getByText('16 set · Fascia')).toBeTruthy();
    expect(screen.getByText('Scrivere relazione')).toBeTruthy();
    expect(screen.getByText(/Pomeriggio · 16 set · Personale/)).toBeTruthy();
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

    expect(
      container.querySelector('[data-timeline-unschedule-schedule]'),
    ).toBeNull();
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
