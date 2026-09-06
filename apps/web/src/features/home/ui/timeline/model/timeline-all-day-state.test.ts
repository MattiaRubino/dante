import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

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
});
