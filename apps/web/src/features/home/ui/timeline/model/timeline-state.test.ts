import { describe, expect, it } from 'vitest';

import {
  buildCalendarMonthGrid,
  buildCalendarYearPage,
  calendarCursorFromDate,
} from './timeline-calendar';
import { TIMELINE_PROTOTYPE_TODAY } from './timeline-fixtures';
import {
  createInitialTimelineState,
  timelineEventsForDate,
  timelineReducer,
} from './timeline-state';
import { parseTimelineDate } from './timeline-temporal';

function eventById(
  state: ReturnType<typeof createInitialTimelineState>,
  dateKey: string,
  eventId: string,
) {
  return timelineEventsForDate(state, dateKey).find(
    (event) => event.id === eventId,
  );
}

describe('timeline state', () => {
  it('moves an event across days without changing its duration and can undo it', () => {
    const initial = createInitialTimelineState();
    const before = eventById(initial, '2026-08-04', '1');
    expect(before).toBeTruthy();

    const moved = timelineReducer(initial, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-05',
      eventId: '1',
      startMinute: 10 * 60 + 5,
    });

    expect(eventById(moved, '2026-08-04', '1')).toBeUndefined();
    expect(eventById(moved, '2026-08-05', '1')).toMatchObject({
      startMinute: 605,
      endMinute: 635,
    });

    const restored = timelineReducer(moved, {
      type: 'undo-last-event-change',
    });
    expect(eventById(restored, '2026-08-05', '1')).toBeUndefined();
    expect(eventById(restored, '2026-08-04', '1')).toEqual(before);
  });

  it('preserves duration when moving against the end-of-day boundary', () => {
    const initial = createInitialTimelineState();
    const moved = timelineReducer(initial, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-04',
      eventId: '2',
      startMinute: 1439,
    });

    expect(eventById(moved, '2026-08-04', '2')).toMatchObject({
      startMinute: 1320,
      endMinute: 1440,
    });
  });

  it('rejects invalid time-editor commits', () => {
    const initial = createInitialTimelineState();
    const invalid = timelineReducer(initial, {
      type: 'update-event-time',
      dateKey: '2026-08-04',
      eventId: '2',
      startMinute: 700,
      endMinute: 699,
    });

    expect(invalid).toBe(initial);
  });

  it('keeps filter, focus and zoom semantics independent', () => {
    const initial = createInitialTimelineState();
    const filtered = timelineReducer(initial, {
      type: 'toggle-filter',
      groupId: 'focus',
    });
    const focused = timelineReducer(filtered, {
      type: 'focus-event',
      eventId: '2',
    });
    const zoomed = timelineReducer(focused, {
      type: 'set-zoom',
      zoom: 99,
    });

    expect(zoomed.filters.has('focus')).toBe(true);
    expect(zoomed.focusedEventId).toBe('2');
    expect(zoomed.zoom).toBe(2.1);
  });

  it('moves a group exactly one adjacent slot in either direction', () => {
    const initial = createInitialTimelineState();
    const movedRight = timelineReducer(initial, {
      type: 'reorder-group',
      groupId: 'focus',
      targetIndex: 1,
    });

    expect(movedRight.groups.slice(0, 3).map((group) => group.id)).toEqual([
      'riunioni',
      'focus',
      'salute',
    ]);

    const movedLeft = timelineReducer(movedRight, {
      type: 'reorder-group',
      groupId: 'focus',
      targetIndex: 0,
    });

    expect(movedLeft.groups.slice(0, 3).map((group) => group.id)).toEqual([
      'focus',
      'riunioni',
      'salute',
    ]);
  });

  it('anchors the accepted rich fixture sequence to an arbitrary runtime day', () => {
    const state = createInitialTimelineState(parseTimelineDate('2034-02-17'));

    expect(eventById(state, '2034-02-17', '2')).toMatchObject({
      title: 'Redesign LifeOS — sessione focus',
      startMinute: 540,
      endMinute: 660,
    });
    expect(eventById(state, '2034-02-18', '101')).toMatchObject({
      title: 'Standup settimanale',
    });
    expect(state.eventsByDate['2026-08-04']).toBeUndefined();
  });

  it('materializes deterministic prototype events for distant calendar dates', () => {
    const state = createInitialTimelineState();
    const first = timelineEventsForDate(state, '2034-02-17');
    const second = timelineEventsForDate(state, '2034-02-17');

    expect(first.map((event) => event.id)).toEqual(second.map((event) => event.id));
    expect(first[0]?.id).toBe('gen-2034-02-17-1');
  });
});

describe('timeline calendar model', () => {
  it('builds the six-row Monday-first month grid used by the prototype', () => {
    const cursor = calendarCursorFromDate(TIMELINE_PROTOTYPE_TODAY);
    const grid = buildCalendarMonthGrid(cursor);

    expect(grid).toHaveLength(42);
    expect(grid[0]?.toString()).toBe('2026-07-27');
    expect(grid[41]?.toString()).toBe('2026-09-06');
  });

  it('uses stable twelve-year pages', () => {
    expect(buildCalendarYearPage(2026)).toEqual([
      2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026,
      2027,
    ]);
  });
});
