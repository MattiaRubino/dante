import { describe, expect, it } from 'vitest';

import {
  createInitialTimelineState,
  findTimelineEvent,
  timelineReducer,
} from './timeline-state';
import type { TimelineEvent } from './timeline-types';

describe('Timeline Create presentation materialization', () => {
  it('materializes a created event into the normal Timeline state and removes it by identity after moves', () => {
    const created: TimelineEvent = {
      id: 'created-projection-1',
      startMinute: 13 * 60 + 30,
      endMinute: 14 * 60 + 30,
      title: 'Nuova attività',
      groupId: 'focus',
      origin: 'create',
      meta: 'Attività',
    };

    let state = timelineReducer(createInitialTimelineState(), {
      type: 'materialize-event',
      dateKey: '2026-08-04',
      event: created,
    });

    expect(findTimelineEvent(state, created.id)).toEqual({
      dateKey: '2026-08-04',
      event: created,
    });

    state = timelineReducer(state, {
      type: 'move-event',
      fromDateKey: '2026-08-04',
      toDateKey: '2026-08-05',
      eventId: created.id,
      startMinute: 15 * 60,
    });
    expect(findTimelineEvent(state, created.id)?.dateKey).toBe('2026-08-05');

    state = timelineReducer(state, {
      type: 'remove-event',
      eventId: created.id,
    });
    expect(findTimelineEvent(state, created.id)).toBeNull();
    expect(state.undo).toBeNull();
  });

  it('does not duplicate a materialized projection on a repeated presentation callback', () => {
    const event: TimelineEvent = {
      id: 'created-projection-2',
      startMinute: 9 * 60,
      endMinute: 10 * 60,
      title: 'Una sola volta',
      groupId: 'personale',
      origin: 'create',
    };
    const initial = createInitialTimelineState();
    const first = timelineReducer(initial, {
      type: 'materialize-event',
      dateKey: '2026-08-04',
      event,
    });
    const second = timelineReducer(first, {
      type: 'materialize-event',
      dateKey: '2026-08-04',
      event,
    });

    expect(second).toBe(first);
    expect(
      second.eventsByDate['2026-08-04']?.filter(
        (candidate) => candidate.id === event.id,
      ),
    ).toHaveLength(1);
  });
});
