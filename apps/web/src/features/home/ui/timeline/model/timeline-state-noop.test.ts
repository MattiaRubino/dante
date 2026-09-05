import { describe, expect, it } from 'vitest';

import {
  createInitialTimelineState,
  timelineEventsForDate,
  timelineReducer,
} from './timeline-state';

function eventById(
  state: ReturnType<typeof createInitialTimelineState>,
  dateKey: string,
  eventId: string,
) {
  return timelineEventsForDate(state, dateKey).find(
    (event) => event.id === eventId,
  );
}

describe('timeline no-op mutation semantics', () => {
  it('does not manufacture state or Undo for an unchanged time edit', () => {
    const initial = createInitialTimelineState();
    const event = eventById(initial, '2026-08-04', '2');
    expect(event).toBeDefined();
    if (!event) {
      return;
    }

    const unchanged = timelineReducer(initial, {
      type: 'update-event-time',
      dateKey: '2026-08-04',
      eventId: event.id,
      startMinute: event.startMinute,
      endMinute: event.endMinute,
    });

    expect(unchanged).toBe(initial);
    expect(unchanged.undo).toBeNull();
  });

  it('keeps the last real Undo when a repeated boundary move clamps to no change', () => {
    const initial = createInitialTimelineState();
    const original = eventById(initial, '2026-08-04', '2');
    expect(original).toBeDefined();

    const movedToBoundary = timelineReducer(initial, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-04',
      eventId: '2',
      startMinute: 1439,
    });

    expect(eventById(movedToBoundary, '2026-08-04', '2')).toMatchObject({
      startMinute: 1320,
      endMinute: 1440,
    });
    expect(movedToBoundary.undo).not.toBeNull();

    const repeatedBoundaryMove = timelineReducer(movedToBoundary, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-04',
      eventId: '2',
      startMinute: 1439,
    });

    expect(repeatedBoundaryMove).toBe(movedToBoundary);
    expect(repeatedBoundaryMove.undo).toBe(movedToBoundary.undo);

    const restored = timelineReducer(repeatedBoundaryMove, {
      type: 'undo-last-event-change',
    });
    expect(eventById(restored, '2026-08-04', '2')).toEqual(original);
  });

  it('still treats a cross-day move as real when the clock time is unchanged', () => {
    const initial = createInitialTimelineState();
    const event = eventById(initial, '2026-08-04', '2');
    expect(event).toBeDefined();
    if (!event) {
      return;
    }

    const moved = timelineReducer(initial, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-05',
      eventId: event.id,
      startMinute: event.startMinute,
    });

    expect(moved).not.toBe(initial);
    expect(eventById(moved, '2026-08-04', event.id)).toBeUndefined();
    expect(eventById(moved, '2026-08-05', event.id)).toMatchObject({
      startMinute: event.startMinute,
      endMinute: event.endMinute,
    });
    expect(moved.undo).not.toBeNull();
  });
});
