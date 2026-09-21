import type { PlainDate } from '@dante/time';

import {
  TIMELINE_GROUPS,
  TIMELINE_PROTOTYPE_TODAY,
  createTimelinePrototypeEventsForDate,
  createTimelinePrototypeStore,
} from './timeline-fixtures';
import { clampTimelineZoom } from './timeline-policy';
import type {
  TimelineAllDayItem,
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

type TimelineUndoGroup = 'single' | 'keyboard-nudge';

type TimelineUndoSnapshot = Readonly<{
  eventId: TimelineEventId;
  beforeDateKey: string;
  beforeEvent: TimelineEvent;
  afterDateKey: string;
  group: TimelineUndoGroup;
}>;

export type TimelineState = Readonly<{
  eventsByDate: Readonly<Record<string, readonly TimelineEvent[]>>;
  allDayItems: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  prototypeEnabled: boolean;
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
  | Readonly<{ type: 'reconcile-canonical-groups'; groups: readonly TimelineGroup[] }>
  | Readonly<{ type: 'create-group'; group: TimelineGroup }>
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
      type: 'materialize-event';
      dateKey: string;
      event: TimelineEvent;
    }>
  | Readonly<{
      type: 'reconcile-authoritative-events';
      projections: readonly Readonly<{
        dateKey: string;
        event: TimelineEvent;
      }>[];
    }>
  | Readonly<{
      type: 'materialize-all-day';
      item: TimelineAllDayItem;
    }>
  | Readonly<{ type: 'remove-event'; eventId: TimelineEventId }>
  | Readonly<{ type: 'remove-all-day'; itemId: string }>
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
      undoGroup?: 'keyboard-nudge';
    }>
  | Readonly<{ type: 'undo-last-event-change' }>;

const DEFAULT_VIEW_OPTIONS: TimelineViewOptions = {
  showMargins: true,
  showNow: true,
  showMilestones: true,
};

function sortEvents(
  events: readonly TimelineEvent[],
): readonly TimelineEvent[] {
  return [...events].sort(
    (left, right) =>
      left.startMinute - right.startMinute ||
      left.endMinute - right.endMinute ||
      left.id.localeCompare(right.id),
  );
}

function sortAllDayItems(
  items: readonly TimelineAllDayItem[],
): readonly TimelineAllDayItem[] {
  return [...items].sort(
    (left, right) =>
      left.startDateKey.localeCompare(right.startDateKey) ||
      left.endDateExclusiveKey.localeCompare(right.endDateExclusiveKey) ||
      left.id.localeCompare(right.id),
  );
}

export function createInitialTimelineState(
  fixtureAnchor: PlainDate = TIMELINE_PROTOTYPE_TODAY,
  prototypeEnabled = true,
): TimelineState {
  return {
    eventsByDate: prototypeEnabled ? createTimelinePrototypeStore(fixtureAnchor) : {},
    allDayItems: [],
    groups: prototypeEnabled ? [...TIMELINE_GROUPS] : [],
    prototypeEnabled,
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
  return (
    state.eventsByDate[dateKey] ??
    (state.prototypeEnabled ? createTimelinePrototypeEventsForDate(dateKey) : [])
  );
}

export function timelineAllDayItemsForDate(
  state: TimelineState,
  dateKey: string,
): readonly TimelineAllDayItem[] {
  return state.allDayItems.filter(
    (item) =>
      item.startDateKey <= dateKey && dateKey < item.endDateExclusiveKey,
  );
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

export function findTimelineAllDayItem(
  state: TimelineState,
  itemId: string,
): TimelineAllDayItem | null {
  return state.allDayItems.find((item) => item.id === itemId) ?? null;
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

function sameEvent(left: TimelineEvent, right: TimelineEvent): boolean {
  return (
    left.id === right.id &&
    left.startMinute === right.startMinute &&
    left.endMinute === right.endMinute &&
    left.title === right.title &&
    left.groupId === right.groupId &&
    left.appearanceTone === right.appearanceTone &&
    left.origin === right.origin &&
    left.meta === right.meta &&
    left.canonicalBasis?.kind === right.canonicalBasis?.kind &&
    left.canonicalBasis?.activityRef === right.canonicalBasis?.activityRef &&
    left.canonicalBasis?.scheduleRef === right.canonicalBasis?.scheduleRef &&
    left.canonicalBasis?.placementMaterialStateRef ===
      right.canonicalBasis?.placementMaterialStateRef &&
    (left.subitems ?? []).length === (right.subitems ?? []).length &&
    (left.subitems ?? []).every(
      (subitem, index) => subitem === right.subitems?.[index],
    )
  );
}

function materializeEvent(
  state: TimelineState,
  action: Extract<TimelineAction, { type: 'materialize-event' }>,
): TimelineState {
  const current = findTimelineEvent(state, action.event.id);
  if (
    current?.dateKey === action.dateKey &&
    sameEvent(current.event, action.event)
  ) {
    return state;
  }

  const eventsByDate: Record<string, readonly TimelineEvent[]> =
    Object.fromEntries(
      Object.entries(state.eventsByDate).map(([dateKey, events]) => [
        dateKey,
        events.filter((event) => event.id !== action.event.id),
      ]),
    );
  const targetEvents =
    eventsByDate[action.dateKey] ??
    (state.prototypeEnabled ? createTimelinePrototypeEventsForDate(action.dateKey) : []);
  eventsByDate[action.dateKey] = sortEvents([
    ...targetEvents.filter((event) => event.id !== action.event.id),
    action.event,
  ]);

  return {
    ...state,
    eventsByDate,
    undo: state.undo?.eventId === action.event.id ? null : state.undo,
  };
}

function reconcileAuthoritativeEvents(
  state: TimelineState,
  projections: readonly Readonly<{
    dateKey: string;
    event: TimelineEvent;
  }>[],
): TimelineState {
  const canonicalIds = new Set(
    projections.map((projection) => projection.event.id),
  );
  let changed = false;
  const eventsByDate: Record<string, readonly TimelineEvent[]> =
    Object.fromEntries(
      Object.entries(state.eventsByDate).map(([dateKey, events]) => {
        const retained = events.filter(
          (event) => event.canonicalBasis === undefined,
        );
        if (retained.length !== events.length) {
          changed = true;
        }
        return [dateKey, retained];
      }),
    );

  for (const projection of projections) {
    const currentEvents =
      eventsByDate[projection.dateKey] ??
      (state.prototypeEnabled ? createTimelinePrototypeEventsForDate(projection.dateKey) : []);
    eventsByDate[projection.dateKey] = sortEvents([
      ...currentEvents.filter((event) => event.id !== projection.event.id),
      projection.event,
    ]);
    const current = findTimelineEvent(state, projection.event.id);
    if (
      current?.dateKey !== projection.dateKey ||
      !sameEvent(current.event, projection.event)
    ) {
      changed = true;
    }
  }

  if (!changed) {
    return state;
  }

  const focusedCanonicalRemoved =
    state.focusedEventId !== null &&
    !canonicalIds.has(state.focusedEventId) &&
    findTimelineEvent(state, state.focusedEventId)?.event.canonicalBasis !==
      undefined;
  const expandedEventIds = new Set(
    [...state.expandedEventIds].filter(
      (eventId) =>
        canonicalIds.has(eventId) ||
        findTimelineEvent(state, eventId)?.event.canonicalBasis === undefined,
    ),
  );

  return {
    ...state,
    eventsByDate,
    focusedEventId: focusedCanonicalRemoved ? null : state.focusedEventId,
    expandedEventIds,
    undo:
      state.undo !== null &&
      findTimelineEvent(state, state.undo.eventId)?.event.canonicalBasis !==
        undefined
        ? null
        : state.undo,
  };
}

function materializeAllDay(
  state: TimelineState,
  action: Extract<TimelineAction, { type: 'materialize-all-day' }>,
): TimelineState {
  const item = action.item;
  if (
    findTimelineAllDayItem(state, item.id) ||
    item.id.trim().length === 0 ||
    item.title.trim().length === 0 ||
    item.groupId.trim().length === 0 ||
    item.startDateKey >= item.endDateExclusiveKey
  ) {
    return state;
  }

  return {
    ...state,
    allDayItems: sortAllDayItems([...state.allDayItems, item]),
  };
}

function removeEvent(
  state: TimelineState,
  eventId: TimelineEventId,
): TimelineState {
  let removed = false;
  const eventsByDate = Object.fromEntries(
    Object.entries(state.eventsByDate).map(([dateKey, events]) => {
      const next = events.filter((event) => event.id !== eventId);
      if (next.length !== events.length) {
        removed = true;
      }
      return [dateKey, next];
    }),
  );

  if (!removed) {
    return state;
  }

  const expandedEventIds = new Set(state.expandedEventIds);
  expandedEventIds.delete(eventId);

  return {
    ...state,
    eventsByDate,
    focusedEventId:
      state.focusedEventId === eventId ? null : state.focusedEventId,
    expandedEventIds,
    undo: state.undo?.eventId === eventId ? null : state.undo,
  };
}

function removeAllDay(state: TimelineState, itemId: string): TimelineState {
  const allDayItems = state.allDayItems.filter((item) => item.id !== itemId);
  return allDayItems.length === state.allDayItems.length
    ? state
    : { ...state, allDayItems };
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

  if (
    current.startMinute === action.startMinute &&
    current.endMinute === action.endMinute
  ) {
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
      group: 'single',
    },
  };
}

function moveUndoSnapshot(
  state: TimelineState,
  current: TimelineEvent,
  action: Extract<TimelineAction, { type: 'move-event' }>,
): TimelineUndoSnapshot {
  if (
    action.undoGroup === 'keyboard-nudge' &&
    state.undo?.group === 'keyboard-nudge' &&
    state.undo.eventId === current.id &&
    state.undo.afterDateKey === action.fromDateKey
  ) {
    return {
      ...state.undo,
      afterDateKey: action.toDateKey,
    };
  }

  return {
    eventId: current.id,
    beforeDateKey: action.fromDateKey,
    beforeEvent: current,
    afterDateKey: action.toDateKey,
    group: action.undoGroup ?? 'single',
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

  if (
    action.fromDateKey === action.toDateKey &&
    movedEvent.startMinute === current.startMinute &&
    movedEvent.endMinute === current.endMinute
  ) {
    return state;
  }

  const undo = moveUndoSnapshot(state, current, action);

  if (action.fromDateKey === action.toDateKey) {
    const nextEvents = sourceEvents.map((event) =>
      event.id === action.eventId ? movedEvent : event,
    );
    return {
      ...state,
      eventsByDate: replaceDateEvents(state, action.fromDateKey, nextEvents),
      undo,
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
    undo,
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

    case 'reconcile-canonical-groups': {
      const ids = new Set(action.groups.map((group) => group.id));
      return {
        ...state,
        groups: action.groups,
        filters: new Set([...state.filters].filter((id) => ids.has(id))),
      };
    }

    case 'create-group': {
      const duplicate = state.groups.some(
        (group) =>
          group.id === action.group.id ||
          group.label.localeCompare(action.group.label, undefined, {
            sensitivity: 'accent',
          }) === 0,
      );
      return duplicate
        ? state
        : { ...state, groups: [...state.groups, action.group] };
    }

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

    case 'materialize-event':
      return materializeEvent(state, action);

    case 'reconcile-authoritative-events':
      return reconcileAuthoritativeEvents(state, action.projections);

    case 'materialize-all-day':
      return materializeAllDay(state, action);

    case 'remove-event':
      return removeEvent(state, action.eventId);

    case 'remove-all-day':
      return removeAllDay(state, action.itemId);

    case 'update-event-time':
      return updateEventTime(state, action);

    case 'move-event':
      return moveEvent(state, action);

    case 'undo-last-event-change':
      return undoLastEventChange(state);
  }
}
