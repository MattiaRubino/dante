import {
  TIMELINE_GROUPS,
  createTimelinePrototypeEventsForDate,
  createTimelinePrototypeStore,
} from './timeline-fixtures';
import { clampTimelineZoom } from './timeline-policy';
import type {
  TimelineEvent,
  TimelineEventId,
  TimelineGroup,
  TimelineGroupId,
} from './timeline-types';

export type TimelineViewOptions = Readonly<{
  showMargins: boolean;
  showNow: boolean;
  showMilestones: boolean;
}>;

type TimelineUndoSnapshot = Readonly<{
  eventId: TimelineEventId;
  beforeDateKey: string;
  beforeEvent: TimelineEvent;
  afterDateKey: string;
}>;

export type TimelineState = Readonly<{
  eventsByDate: Readonly<Record<string, readonly TimelineEvent[]>>;
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
  focusedEventId: TimelineEventId | null;
  expandedEventIds: ReadonlySet<TimelineEventId>;
  zoom: number;
  viewOptions: TimelineViewOptions;
  undo: TimelineUndoSnapshot | null;
}>;

export type TimelineAction =
  | Readonly<{ type: 'toggle-filter'; groupId: TimelineGroupId }>
  | Readonly<{ type: 'reset-groups-focus' }>
  | Readonly<{
      type: 'reorder-group';
      groupId: TimelineGroupId;
      targetIndex: number;
    }>
  | Readonly<{
      type: 'focus-event';
      eventId: TimelineEventId | null;
    }>
  | Readonly<{
      type: 'toggle-event-subitems';
      eventId: TimelineEventId;
    }>
  | Readonly<{ type: 'set-zoom'; zoom: number }>
  | Readonly<{
      type: 'set-view-option';
      option: keyof TimelineViewOptions;
      value: boolean;
    }>
  | Readonly<{ type: 'reset-view-options' }>
  | Readonly<{
      type: 'update-event-time';
      dateKey: string;
      eventId: TimelineEventId;
      startMinute: number;
      endMinute: number;
    }>
  | Readonly<{
      type: 'move-event';
      fromDateKey: string;
      toDateKey: string;
      eventId: TimelineEventId;
      startMinute: number;
    }>
  | Readonly<{ type: 'undo-last-event-change' }>;

const DEFAULT_VIEW_OPTIONS: TimelineViewOptions = {
  showMargins: true,
  showNow: true,
  showMilestones: true,
};

function sortEvents(events: readonly TimelineEvent[]): readonly TimelineEvent[] {
  return [...events].sort(
    (left, right) =>
      left.startMinute - right.startMinute ||
      left.endMinute - right.endMinute ||
      left.id.localeCompare(right.id),
  );
}

export function createInitialTimelineState(): TimelineState {
  return {
    eventsByDate: createTimelinePrototypeStore(),
    groups: [...TIMELINE_GROUPS],
    filters: new Set<TimelineGroupId>(),
    focusedEventId: null,
    expandedEventIds: new Set<TimelineEventId>(),
    zoom: 1,
    viewOptions: DEFAULT_VIEW_OPTIONS,
    undo: null,
  };
}

export function timelineEventsForDate(
  state: TimelineState,
  dateKey: string,
): readonly TimelineEvent[] {
  return state.eventsByDate[dateKey] ?? createTimelinePrototypeEventsForDate(dateKey);
}

export function findTimelineEvent(
  state: TimelineState,
  eventId: TimelineEventId,
): Readonly<{ dateKey: string; event: TimelineEvent }> | null {
  for (const [dateKey, events] of Object.entries(state.eventsByDate)) {
    const event = events.find((candidate) => candidate.id === eventId);
    if (event) {
      return { dateKey, event };
    }
  }

  return null;
}

function replaceDateEvents(
  state: TimelineState,
  dateKey: string,
  events: readonly TimelineEvent[],
): TimelineState['eventsByDate'] {
  return {
    ...state.eventsByDate,
    [dateKey]: sortEvents(events),
  };
}

function updateEventTime(
  state: TimelineState,
  action: Extract<TimelineAction, { type: 'update-event-time' }>,
): TimelineState {
  if (
    !Number.isFinite(action.startMinute) ||
    !Number.isFinite(action.endMinute) ||
    action.startMinute < 0 ||
    action.startMinute > 1439 ||
    action.endMinute < 1 ||
    action.endMinute > 1440 ||
    action.endMinute <= action.startMinute
  ) {
    return state;
  }

  const events = timelineEventsForDate(state, action.dateKey);
  const current = events.find((event) => event.id === action.eventId);
  if (!current) {
    return state;
  }

  const nextEvent: TimelineEvent = {
    ...current,
    startMinute: action.startMinute,
    endMinute: action.endMinute,
  };
  const nextEvents = events.map((event) =>
    event.id === action.eventId ? nextEvent : event,
  );

  return {
    ...state,
    eventsByDate: replaceDateEvents(state, action.dateKey, nextEvents),
    undo: {
      eventId: current.id,
      beforeDateKey: action.dateKey,
      beforeEvent: current,
      afterDateKey: action.dateKey,
    },
  };
}

function moveEvent(
  state: TimelineState,
  action: Extract<TimelineAction, { type: 'move-event' }>,
): TimelineState {
  const sourceEvents = timelineEventsForDate(state, action.fromDateKey);
  const current = sourceEvents.find((event) => event.id === action.eventId);
  if (!current || !Number.isFinite(action.startMinute)) {
    return state;
  }

  const duration = Math.max(1, current.endMinute - current.startMinute);
  const startMinute = Math.max(
    0,
    Math.min(1440 - duration, Math.round(action.startMinute)),
  );
  const movedEvent: TimelineEvent = {
    ...current,
    startMinute,
    endMinute: startMinute + duration,
  };

  if (action.fromDateKey === action.toDateKey) {
    const nextEvents = sourceEvents.map((event) =>
      event.id === action.eventId ? movedEvent : event,
    );
    return {
      ...state,
      eventsByDate: replaceDateEvents(state, action.fromDateKey, nextEvents),
      undo: {
        eventId: current.id,
        beforeDateKey: action.fromDateKey,
        beforeEvent: current,
        afterDateKey: action.toDateKey,
      },
    };
  }

  const targetEvents = timelineEventsForDate(state, action.toDateKey).filter(
    (event) => event.id !== action.eventId,
  );
  const withoutSource = sourceEvents.filter(
    (event) => event.id !== action.eventId,
  );
  const withSourceUpdated = replaceDateEvents(
    state,
    action.fromDateKey,
    withoutSource,
  );

  return {
    ...state,
    eventsByDate: {
      ...withSourceUpdated,
      [action.toDateKey]: sortEvents([...targetEvents, movedEvent]),
    },
    undo: {
      eventId: current.id,
      beforeDateKey: action.fromDateKey,
      beforeEvent: current,
      afterDateKey: action.toDateKey,
    },
  };
}

function undoLastEventChange(state: TimelineState): TimelineState {
  const undo = state.undo;
  if (!undo) {
    return state;
  }

  if (undo.beforeDateKey === undo.afterDateKey) {
    const events = timelineEventsForDate(state, undo.beforeDateKey);
    const restored = events.map((event) =>
      event.id === undo.eventId ? undo.beforeEvent : event,
    );
    return {
      ...state,
      eventsByDate: replaceDateEvents(state, undo.beforeDateKey, restored),
      undo: null,
    };
  }

  const afterEvents = timelineEventsForDate(state, undo.afterDateKey).filter(
    (event) => event.id !== undo.eventId,
  );
  const beforeEvents = timelineEventsForDate(state, undo.beforeDateKey).filter(
    (event) => event.id !== undo.eventId,
  );

  return {
    ...state,
    eventsByDate: {
      ...state.eventsByDate,
      [undo.afterDateKey]: sortEvents(afterEvents),
      [undo.beforeDateKey]: sortEvents([...beforeEvents, undo.beforeEvent]),
    },
    undo: null,
  };
}

export function timelineReducer(
  state: TimelineState,
  action: TimelineAction,
): TimelineState {
  switch (action.type) {
    case 'toggle-filter': {
      const filters = new Set(state.filters);
      if (filters.has(action.groupId)) {
        filters.delete(action.groupId);
      } else {
        filters.add(action.groupId);
      }
      return { ...state, filters };
    }

    case 'reset-groups-focus':
      return {
        ...state,
        filters: new Set<TimelineGroupId>(),
        focusedEventId: null,
      };

    case 'reorder-group': {
      const fromIndex = state.groups.findIndex(
        (group) => group.id === action.groupId,
      );
      if (fromIndex < 0) {
        return state;
      }
      const targetIndex = Math.max(
        0,
        Math.min(state.groups.length - 1, action.targetIndex),
      );
      if (fromIndex === targetIndex) {
        return state;
      }
      const groups = [...state.groups];
      const [moved] = groups.splice(fromIndex, 1);
      if (!moved) {
        return state;
      }
      groups.splice(targetIndex, 0, moved);
      return { ...state, groups };
    }

    case 'focus-event':
      return {
        ...state,
        focusedEventId:
          state.focusedEventId === action.eventId ? null : action.eventId,
      };

    case 'toggle-event-subitems': {
      const expandedEventIds = new Set(state.expandedEventIds);
      if (expandedEventIds.has(action.eventId)) {
        expandedEventIds.delete(action.eventId);
      } else {
        expandedEventIds.add(action.eventId);
      }
      return { ...state, expandedEventIds };
    }

    case 'set-zoom':
      return { ...state, zoom: clampTimelineZoom(action.zoom) };

    case 'set-view-option':
      return {
        ...state,
        viewOptions: {
          ...state.viewOptions,
          [action.option]: action.value,
        },
      };

    case 'reset-view-options':
      return { ...state, viewOptions: DEFAULT_VIEW_OPTIONS };

    case 'update-event-time':
      return updateEventTime(state, action);

    case 'move-event':
      return moveEvent(state, action);

    case 'undo-last-event-change':
      return undoLastEventChange(state);
  }
}
