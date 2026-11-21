import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';
import type {
  TemporalAuthoredActivityResult,
  TemporalAuthoredEventResult,
} from '../../../../temporal/authoring-data-source';
import { timelineAllDayFromAuthoredDateSpan } from '../timeline-create-bridge';

import {
  createInitialTimelineState,
  timelineAllDayItemsForDate,
  timelineReducer,
} from './timeline-state';
import type { TimelineAllDayItem } from './timeline-types';

const anchor = Temporal.PlainDate.from('2026-08-04');

function item(): TimelineAllDayItem {
  return Object.freeze({
    id: 'create:all-day:1',
    startDateKey: '2026-08-04',
    endDateExclusiveKey: '2026-08-07',
    title: 'Fiera',
    groupId: 'creativita',
    origin: 'create' as const,
    meta: 'Evento',
  });
}

describe('Timeline native all-day state', () => {
  it('materializes one date span and projects it onto every covered date', () => {
    const initial = createInitialTimelineState(anchor);
    const created = timelineReducer(initial, {
      type: 'materialize-all-day',
      item: item(),
    });

    expect(created.allDayItems).toHaveLength(1);
    expect(timelineAllDayItemsForDate(created, '2026-08-03')).toEqual([]);
    expect(timelineAllDayItemsForDate(created, '2026-08-04')).toHaveLength(1);
    expect(timelineAllDayItemsForDate(created, '2026-08-05')).toHaveLength(1);
    expect(timelineAllDayItemsForDate(created, '2026-08-06')).toHaveLength(1);
    expect(timelineAllDayItemsForDate(created, '2026-08-07')).toEqual([]);
  });

  it('is idempotent by identity and removes the entire range as one item', () => {
    const initial = createInitialTimelineState(anchor);
    const once = timelineReducer(initial, {
      type: 'materialize-all-day',
      item: item(),
    });
    const twice = timelineReducer(once, {
      type: 'materialize-all-day',
      item: item(),
    });

    expect(twice).toBe(once);

    const removed = timelineReducer(twice, {
      type: 'remove-all-day',
      itemId: item().id,
    });
    expect(removed.allDayItems).toEqual([]);
  });

  it('rejects an empty or reversed half-open date span', () => {
    const initial = createInitialTimelineState(anchor);
    const invalid = Object.freeze({
      ...item(),
      startDateKey: '2026-08-07',
      endDateExclusiveKey: '2026-08-07',
    });

    expect(
      timelineReducer(initial, { type: 'materialize-all-day', item: invalid }),
    ).toBe(initial);
  });

  it.each(['activity', 'event'] as const)(
    'materializes the accepted %s date span without a page reload',
    (kind) => {
      const start = Temporal.PlainDate.from('2026-11-21');
      const endDateExclusive = start.add({ days: 2 });
      const common = {
        item: {
          subjectRef: 'subject-1',
          title: 'Due giorni',
          createdAt: Temporal.Instant.from('2026-11-21T09:00:00Z'),
          description: null,
          location: null,
          colorCode: '#aabbcc',
          lifeAreaRef: 'area-1',
          lifeAreaAssignmentRevision: 1,
          lifeAreaColorCode: '#aabbcc',
          lifeAreaRevision: 1,
        },
        schedule: {
          scheduleRef: 'schedule-1',
          placementMaterialStateRef: 'state-1',
          placement: {
            kind: 'date-span' as const,
            startDate: start,
            endDateExclusive,
          },
        },
        replayed: false,
      };
      const authored:
        TemporalAuthoredActivityResult | TemporalAuthoredEventResult =
        kind === 'activity'
          ? {
              ...common,
              sessionCaptureMode: 'record',
              childGuardMode: 'none',
              plannedSlices: [],
              activityIntervals: [],
              children: [],
            }
          : { ...common, agendaRevision: 0, agendaParts: [] };
      const createdItem = timelineAllDayFromAuthoredDateSpan(kind, authored);
      expect(createdItem).toMatchObject({
        id: 'schedule-1',
        groupId: 'area-1',
        appearanceColorCode: '#aabbcc',
        canonicalBasis: {
          kind: kind === 'activity' ? 'scheduled-activity' : 'scheduled-event',
          scheduleRef: 'schedule-1',
          placementMaterialStateRef: 'state-1',
          placement: { kind: 'date-span', startDate: start, endDateExclusive },
        },
      });
      if (!createdItem) throw new Error('Expected accepted date span');
      const created = timelineReducer(createInitialTimelineState(start), {
        type: 'materialize-all-day',
        item: createdItem,
      });
      expect(timelineAllDayItemsForDate(created, '2026-11-21')).toEqual([
        createdItem,
      ]);
      expect(timelineAllDayItemsForDate(created, '2026-11-22')).toEqual([
        createdItem,
      ]);
      expect(timelineAllDayItemsForDate(created, '2026-11-23')).toEqual([]);
      expect(
        timelineAllDayFromAuthoredDateSpan(kind, {
          ...authored,
          schedule: null,
        }),
      ).toBeNull();
    },
  );
});
