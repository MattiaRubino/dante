import type { PlainDate } from '@dante/time';
import {
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  type RefObject,
  useEffect,
  useLayoutEffect,
  useRef,
} from 'react';
import { useTranslation } from 'react-i18next';

import { computeTimelineGaps } from './model/timeline-layout';
import {
  TIMELINE_MINUTES_PER_DAY,
  TIMELINE_POLICY,
  timelineDragSnapMinutes,
} from './model/timeline-policy';
import { findTimelineEvent, type TimelineState } from './model/timeline-state';
import {
  addTimelineDays,
  formatTimelineMinute,
  parseTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type {
  TimelineEvent,
  TimelineEventLayout,
  TimelineGroup,
  TimelineTimeMapper,
} from './model/timeline-types';

export type TimelineRenderedDay = Readonly<{
  date: PlainDate;
  dateKey: string;
  events: readonly TimelineEvent[];
  mapper: TimelineTimeMapper;
  layouts: readonly TimelineEventLayout[];
  offsetTop: number;
  height: number;
}>;

type TimelineEventMove = Readonly<{
  fromDateKey: string;
  toDateKey: string;
  eventId: string;
  startMinute: number;
}>;

type TimelineDayStreamProps = Readonly<{
  days: readonly TimelineRenderedDay[];
  today: PlainDate;
  nowMinute: number;
  state: TimelineState;
  expanded: boolean;
  gridRef: RefObject<HTMLDivElement | null>;
  onScroll: (scrollTop: number, scrollLeft: number) => void;
  onZoomAt: (clientY: number, factor: number) => void;
  onFocusEvent: (eventId: string) => void;
  onToggleSubitems: (eventId: string) => void;
  onOpenEventDetail: (event: TimelineEvent, opener: HTMLElement) => void;
  onOpenSubitemDetail: (
    event: TimelineEvent,
    subitem: string,
    opener: HTMLElement,
  ) => void;
  onOpenTimeEditor: (
    dateKey: string,
    event: TimelineEvent,
    anchor: HTMLButtonElement,
  ) => void;
  onMoveEvent: (move: TimelineEventMove) => void;
  onMoveFeedback: (message: string) => void;
}>;

type DragRuntime = {
  card: HTMLElement;
  event: TimelineEvent;
  fromDateKey: string;
  pointerId: number;
  startX: number;
  startY: number;
  clientX: number;
  clientY: number;
  anchorX: number;
  anchorY: number;
  overlay: HTMLElement | null;
  dragging: boolean;
  lastAutoFrame: number;
};

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function groupForEvent(
  event: TimelineEvent,
  groups: readonly TimelineGroup[],
): TimelineGroup | undefined {
  return groups.find((group) => group.id === event.groupId);
}

function TimelineEventCard({
  dateKey,
  layout,
  groups,
  focusedEvent,
  expandedSubitems,
  filtered,
  onFocusEvent,
  onToggleSubitems,
  onOpenEventDetail,
  onOpenSubitemDetail,
  onOpenTimeEditor,
  onPointerPress,
  onKeyboardMove,
  suppressClickRef,
}: Readonly<{
  dateKey: string;
  layout: TimelineEventLayout;
  groups: readonly TimelineGroup[];
  focusedEvent: TimelineEvent | null;
  expandedSubitems: boolean;
  filtered: boolean;
  onFocusEvent: (eventId: string) => void;
  onToggleSubitems: (eventId: string) => void;
  onOpenEventDetail: (event: TimelineEvent, opener: HTMLElement) => void;
  onOpenSubitemDetail: (
    event: TimelineEvent,
    subitem: string,
    opener: HTMLElement,
  ) => void;
  onOpenTimeEditor: (
    dateKey: string,
    event: TimelineEvent,
    anchor: HTMLButtonElement,
  ) => void;
  onPointerPress: (
    pointerEvent: ReactPointerEvent<HTMLElement>,
    dateKey: string,
    event: TimelineEvent,
  ) => void;
  onKeyboardMove: (
    event: TimelineEvent,
    dateKey: string,
    direction: 'earlier' | 'later' | 'previous-day' | 'next-day',
  ) => void;
  suppressClickRef: RefObject<string | null>;
}>) {
  const { t } = useTranslation('common');
  const event = layout.event;
  const group = groupForEvent(event, groups);
  const isFocused = focusedEvent?.id === event.id;
  const isGroupmate =
    focusedEvent !== null &&
    !isFocused &&
    focusedEvent.groupId === event.groupId;
  const isDim = focusedEvent !== null && !isFocused && !isGroupmate;
  const inlineActionsEnabled = focusedEvent === null || isFocused;

  if (filtered) {
    return null;
  }

  const style = {
    top: layout.top,
    height: layout.height,
    left: `${layout.compactLeftPercent}%`,
    width: `${layout.compactWidthPercent}%`,
  } satisfies CSSProperties;

  const keyboardMove = (keyboardEvent: KeyboardEvent<HTMLElement>) => {
    if (!keyboardEvent.altKey) {
      if (
        keyboardEvent.currentTarget === keyboardEvent.target &&
        (keyboardEvent.key === 'Enter' || keyboardEvent.key === ' ')
      ) {
        keyboardEvent.preventDefault();
        onFocusEvent(event.id);
      }
      return;
    }

    const directions: Partial<
      Record<string, 'earlier' | 'later' | 'previous-day' | 'next-day'>
    > = {
      ArrowUp: 'earlier',
      ArrowDown: 'later',
      ArrowLeft: 'previous-day',
      ArrowRight: 'next-day',
    };
    const direction = directions[keyboardEvent.key];
    if (!direction) {
      return;
    }
    keyboardEvent.preventDefault();
    onKeyboardMove(event, dateKey, direction);
  };

  return (
    <article
      className={`timeline-event-card${expandedSubitems ? ' is-expanded' : ''}${isFocused ? ' is-focused' : ''}${isGroupmate ? ' is-groupmate' : ''}${isDim ? ' is-dim' : ''}`}
      data-timeline-event={event.id}
      data-timeline-tone={group?.tone ?? 'personal'}
      data-compact-left={layout.compactLeftPercent}
      data-compact-width={layout.compactWidthPercent}
      data-group-index={layout.groupIndex}
      data-group-lane={layout.groupLane}
      data-group-lanes={layout.groupLaneCount}
      style={style}
      draggable={false}
      tabIndex={0}
      aria-label={`${event.title}, ${formatTimelineMinute(event.startMinute)}–${formatTimelineMinute(event.endMinute)}`}
      aria-keyshortcuts="Alt+ArrowUp Alt+ArrowDown Alt+ArrowLeft Alt+ArrowRight"
      onDragStart={(dragEvent) => dragEvent.preventDefault()}
      onKeyDown={keyboardMove}
      onPointerDown={(pointerEvent) =>
        onPointerPress(pointerEvent, dateKey, event)
      }
      onClick={(clickEvent) => {
        if ((clickEvent.target as Element).closest('button')) {
          return;
        }
        if (suppressClickRef.current === event.id) {
          suppressClickRef.current = null;
          return;
        }
        onFocusEvent(event.id);
      }}
    >
      <div className="timeline-event-card__top">
        <button
          className="timeline-event-card__title"
          type="button"
          tabIndex={inlineActionsEnabled ? 0 : -1}
          onClick={(clickEvent) => {
            clickEvent.stopPropagation();
            if (!inlineActionsEnabled) {
              onFocusEvent(event.id);
              return;
            }
            onOpenEventDetail(event, clickEvent.currentTarget);
          }}
        >
          {event.title}
        </button>
        <button
          className="timeline-event-card__time"
          type="button"
          tabIndex={inlineActionsEnabled ? 0 : -1}
          onClick={(clickEvent) => {
            clickEvent.stopPropagation();
            if (!inlineActionsEnabled) {
              onFocusEvent(event.id);
              return;
            }
            onOpenTimeEditor(dateKey, event, clickEvent.currentTarget);
          }}
          aria-label={t(($) => $.common.home.timeline.timeEditor.open, {
            title: event.title,
          })}
        >
          {formatTimelineMinute(event.startMinute)}–
          {formatTimelineMinute(event.endMinute)}
        </button>
        <div className="timeline-event-card__meta">
          {group?.label ?? event.groupId}
          {event.meta ? ` · ${event.meta}` : ''}
        </div>
      </div>

      {event.subitems?.length && expandedSubitems ? (
        <div className="timeline-event-card__subitems">
          {event.subitems.map((subitem, index) => (
            <button
              className="timeline-event-card__subitem"
              key={`${event.id}-${index}`}
              type="button"
              tabIndex={inlineActionsEnabled ? 0 : -1}
              onClick={(clickEvent) => {
                clickEvent.stopPropagation();
                if (!inlineActionsEnabled) {
                  onFocusEvent(event.id);
                  return;
                }
                onOpenSubitemDetail(event, subitem, clickEvent.currentTarget);
              }}
            >
              <span>• {subitem}</span>
            </button>
          ))}
        </div>
      ) : null}

      <div className="timeline-event-card__drag-zone" aria-hidden="true" />

      {event.subitems?.length ? (
        <button
          className="timeline-event-card__expander"
          type="button"
          tabIndex={inlineActionsEnabled ? 0 : -1}
          onClick={(clickEvent) => {
            clickEvent.stopPropagation();
            if (!inlineActionsEnabled) {
              onFocusEvent(event.id);
              return;
            }
            onToggleSubitems(event.id);
          }}
          aria-expanded={expandedSubitems}
        >
          <span>
            {expandedSubitems
              ? t(($) => $.common.home.timeline.event.hideSubitems)
              : t(($) => $.common.home.timeline.event.showSubitems, {
                  count: event.subitems?.length ?? 0,
                })}
          </span>
          <span className="timeline-event-card__chevron" aria-hidden="true">
            ⌄
          </span>
        </button>
      ) : null}
    </article>
  );
}

function TimelineDay({
  day,
  today,
  nowMinute,
  state,
  focusedEvent,
  onFocusEvent,
  onToggleSubitems,
  onOpenEventDetail,
  onOpenSubitemDetail,
  onOpenTimeEditor,
  onPointerPress,
  onKeyboardMove,
  suppressClickRef,
}: Readonly<{
  day: TimelineRenderedDay;
  today: PlainDate;
  nowMinute: number;
  state: TimelineState;
  focusedEvent: TimelineEvent | null;
  onFocusEvent: (eventId: string) => void;
  onToggleSubitems: (eventId: string) => void;
  onOpenEventDetail: (event: TimelineEvent, opener: HTMLElement) => void;
  onOpenSubitemDetail: (
    event: TimelineEvent,
    subitem: string,
    opener: HTMLElement,
  ) => void;
  onOpenTimeEditor: (
    dateKey: string,
    event: TimelineEvent,
    anchor: HTMLButtonElement,
  ) => void;
  onPointerPress: (
    pointerEvent: ReactPointerEvent<HTMLElement>,
    dateKey: string,
    event: TimelineEvent,
  ) => void;
  onKeyboardMove: (
    event: TimelineEvent,
    dateKey: string,
    direction: 'earlier' | 'later' | 'previous-day' | 'next-day',
  ) => void;
  suppressClickRef: RefObject<string | null>;
}>) {
  const { t, i18n } = useTranslation('common');
  const isToday = day.date.equals(today);
  const label = day.date.toLocaleString(i18n.language, {
    weekday: 'short',
    day: 'numeric',
    month: 'long',
  });
  const fullLabel = isToday
    ? `${t(($) => $.common.home.timeline.todayPrefix)} · ${label}`
    : label;
  const gaps = state.viewOptions.showMargins
    ? computeTimelineGaps(day.events)
    : [];
  const gridPolicy = TIMELINE_POLICY.grid;

  return (
    <section
      className="timeline-day-section"
      data-timeline-date={day.dateKey}
      style={{ height: day.height }}
      aria-label={fullLabel}
    >
      <div className="timeline-day-section__label">{fullLabel}</div>

      {Array.from(
        {
          length:
            TIMELINE_MINUTES_PER_DAY / gridPolicy.minorLineIntervalMinutes + 1,
        },
        (_, index) => index * gridPolicy.minorLineIntervalMinutes,
      ).map((minute) => (
        <span
          className={`timeline-hour-line${minute % gridPolicy.majorLineIntervalMinutes ? ' is-minor' : ''}`}
          key={minute}
          style={{ top: day.mapper.map(minute) }}
          aria-hidden="true"
        />
      ))}

      {isToday && state.viewOptions.showNow ? (
        <div
          className="timeline-now-line"
          style={{ top: day.mapper.map(nowMinute) }}
          aria-hidden="true"
        >
          <span>{formatTimelineMinute(nowMinute)}</span>
        </div>
      ) : null}

      {isToday && state.viewOptions.showMilestones
        ? gridPolicy.milestoneMinutes.map((minute) => (
            <span
              className="timeline-milestone"
              key={minute}
              style={{ top: day.mapper.map(minute) }}
              aria-hidden="true"
            >
              ⚑
            </span>
          ))
        : null}

      <div className="timeline-split-columns" aria-hidden="true">
        {state.groups.map((group) => (
          <span data-timeline-tone={group.tone} key={group.id} />
        ))}
      </div>

      {gaps
        .filter((gap) => gap.fromMinute <= gridPolicy.marginLabelCutoffMinute)
        .map((gap) => (
          <span
            className="timeline-margin-label"
            key={`${gap.fromMinute}-${gap.toMinute}`}
            style={{
              top:
                day.mapper.map(gap.fromMinute) + gridPolicy.marginLabelOffsetPx,
            }}
            aria-hidden="true"
          >
            {gap.durationMinutes} min
          </span>
        ))}

      <div className="timeline-events-layer">
        {day.layouts.map((layout) => (
          <TimelineEventCard
            dateKey={day.dateKey}
            layout={layout}
            groups={state.groups}
            focusedEvent={focusedEvent}
            expandedSubitems={state.expandedEventIds.has(layout.event.id)}
            filtered={
              state.filters.size > 0 && !state.filters.has(layout.event.groupId)
            }
            key={layout.event.id}
            onFocusEvent={onFocusEvent}
            onToggleSubitems={onToggleSubitems}
            onOpenEventDetail={onOpenEventDetail}
            onOpenSubitemDetail={onOpenSubitemDetail}
            onOpenTimeEditor={onOpenTimeEditor}
            onPointerPress={onPointerPress}
            onKeyboardMove={onKeyboardMove}
            suppressClickRef={suppressClickRef}
          />
        ))}
      </div>
    </section>
  );
}

export function TimelineDayStream({
  days,
  today,
  nowMinute,
  state,
  expanded,
  gridRef,
  onScroll,
  onZoomAt,
  onFocusEvent,
  onToggleSubitems,
  onOpenEventDetail,
  onOpenSubitemDetail,
  onOpenTimeEditor,
  onMoveEvent,
  onMoveFeedback,
}: TimelineDayStreamProps) {
  const { t } = useTranslation('common');
  const rulerStreamRef = useRef<HTMLDivElement | null>(null);
  const runtimeRef = useRef<DragRuntime | null>(null);
  const daysRef = useRef(days);
  const stateRef = useRef(state);
  const autoScrollFrameRef = useRef<number | null>(null);
  const dragCleanupRef = useRef<(() => void) | null>(null);
  const suppressClickRef = useRef<string | null>(null);

  useLayoutEffect(() => {
    daysRef.current = days;
    stateRef.current = state;
  }, [days, state]);

  const focusedEvent = state.focusedEventId
    ? (findTimelineEvent(state, state.focusedEventId)?.event ?? null)
    : null;

  const stopAutoScroll = () => {
    if (autoScrollFrameRef.current !== null) {
      cancelAnimationFrame(autoScrollFrameRef.current);
      autoScrollFrameRef.current = null;
    }
    if (runtimeRef.current) {
      runtimeRef.current.lastAutoFrame = 0;
    }
  };

  const updateOverlay = () => {
    const runtime = runtimeRef.current;
    if (!runtime?.dragging || !runtime.overlay) {
      return;
    }
    runtime.overlay.style.left = `${runtime.clientX - runtime.anchorX}px`;
    runtime.overlay.style.top = `${runtime.clientY - runtime.anchorY}px`;
  };

  const autoScrollTick = (time: number) => {
    const runtime = runtimeRef.current;
    const grid = gridRef.current;
    if (!runtime?.dragging || !grid) {
      stopAutoScroll();
      return;
    }

    const rect = grid.getBoundingClientRect();
    const edge = TIMELINE_POLICY.drag.autoScrollEdgePx;
    let direction = 0;
    let ratio = 0;
    if (runtime.clientY < rect.top + edge) {
      direction = -1;
      ratio = clamp((rect.top + edge - runtime.clientY) / edge, 0, 1);
    } else if (runtime.clientY > rect.bottom - edge) {
      direction = 1;
      ratio = clamp((runtime.clientY - (rect.bottom - edge)) / edge, 0, 1);
    }

    const previousTime = runtime.lastAutoFrame || time;
    const elapsedSeconds = Math.min(
      TIMELINE_POLICY.drag.autoScrollMaxFrameSeconds,
      Math.max(0, time - previousTime) / 1000,
    );
    runtime.lastAutoFrame = time;

    if (direction !== 0) {
      const minSpeed = TIMELINE_POLICY.drag.autoScrollMinPxPerSecond;
      const maxSpeed = TIMELINE_POLICY.drag.autoScrollMaxPxPerSecond;
      const speed = minSpeed + ratio * (maxSpeed - minSpeed);
      grid.scrollTop = clamp(
        grid.scrollTop + direction * speed * elapsedSeconds,
        0,
        Math.max(0, grid.scrollHeight - grid.clientHeight),
      );
      updateOverlay();
    }

    autoScrollFrameRef.current = requestAnimationFrame(autoScrollTick);
  };

  const beginDragVisual = () => {
    const runtime = runtimeRef.current;
    if (!runtime || runtime.dragging) {
      return;
    }
    const rect = runtime.card.getBoundingClientRect();
    const overlay = runtime.card.cloneNode(true) as HTMLElement;
    overlay.classList.remove('is-focused', 'is-groupmate', 'is-dim');
    overlay.classList.add('timeline-event-drag-overlay');
    overlay.removeAttribute('data-timeline-event');
    overlay.querySelectorAll<HTMLElement>('button').forEach((button) => {
      button.tabIndex = -1;
    });
    overlay.style.width = `${rect.width}px`;
    overlay.style.height = `${rect.height}px`;
    overlay.style.position = 'fixed';
    document.body.appendChild(overlay);

    runtime.overlay = overlay;
    runtime.dragging = true;
    runtime.lastAutoFrame = performance.now();
    runtime.card.classList.add('is-drag-source');
    updateOverlay();
    autoScrollFrameRef.current = requestAnimationFrame(autoScrollTick);
  };

  const finishDragVisual = () => {
    const runtime = runtimeRef.current;
    runtime?.overlay?.remove();
    runtime?.card.classList.remove('is-drag-source');
    if (runtime) {
      runtime.overlay = null;
    }
    stopAutoScroll();
  };

  const cancelDrag = () => {
    if (!runtimeRef.current) {
      return;
    }
    finishDragVisual();
    dragCleanupRef.current?.();
    dragCleanupRef.current = null;
    runtimeRef.current = null;
  };

  const commitDrag = (clientY: number) => {
    const runtime = runtimeRef.current;
    const grid = gridRef.current;
    if (!runtime || !grid || !runtime.dragging) {
      finishDragVisual();
      return;
    }

    const gridRect = grid.getBoundingClientRect();
    const contentTop =
      grid.scrollTop + (clientY - runtime.anchorY - gridRect.top);
    const overlayHeight = runtime.overlay?.getBoundingClientRect().height ?? 0;
    const targetDay =
      daysRef.current.find(
        (day) =>
          contentTop >= day.offsetTop &&
          contentTop < day.offsetTop + day.height,
      ) ?? null;

    if (!targetDay) {
      finishDragVisual();
      return;
    }

    const localY = clamp(
      contentTop - targetDay.offsetTop,
      0,
      Math.max(0, targetDay.height - overlayHeight),
    );
    const minute = targetDay.mapper.inv(localY);
    const snap = timelineDragSnapMinutes(stateRef.current.zoom);
    const snappedMinute = Math.round(minute / snap) * snap;

    onMoveEvent({
      fromDateKey: runtime.fromDateKey,
      toDateKey: targetDay.dateKey,
      eventId: runtime.event.id,
      startMinute: snappedMinute,
    });
    suppressClickRef.current = runtime.event.id;
    const duration = runtime.event.endMinute - runtime.event.startMinute;
    const bounded = clamp(
      snappedMinute,
      0,
      TIMELINE_MINUTES_PER_DAY - duration,
    );
    onMoveFeedback(
      `${t(($) => $.common.home.timeline.feedback.moved)} ${formatTimelineMinute(bounded)}–${formatTimelineMinute(bounded + duration)}`,
    );
    finishDragVisual();
  };

  const startPointerPress = (
    pointerEvent: ReactPointerEvent<HTMLElement>,
    dateKey: string,
    event: TimelineEvent,
  ) => {
    if (!pointerEvent.isPrimary || pointerEvent.button !== 0) {
      return;
    }
    const target = pointerEvent.target;
    if (
      target instanceof Element &&
      target.closest('button,input,textarea,select,a')
    ) {
      return;
    }

    cancelDrag();
    const card = pointerEvent.currentTarget;
    const rect = card.getBoundingClientRect();
    const pointerId = pointerEvent.pointerId;
    runtimeRef.current = {
      card,
      event,
      fromDateKey: dateKey,
      pointerId,
      startX: pointerEvent.clientX,
      startY: pointerEvent.clientY,
      clientX: pointerEvent.clientX,
      clientY: pointerEvent.clientY,
      anchorX: pointerEvent.clientX - rect.left,
      anchorY: pointerEvent.clientY - rect.top,
      overlay: null,
      dragging: false,
      lastAutoFrame: 0,
    };

    try {
      card.setPointerCapture(pointerId);
    } catch {
      cancelDrag();
      return;
    }

    const move = (eventMove: PointerEvent) => {
      const runtime = runtimeRef.current;
      if (!runtime || eventMove.pointerId !== runtime.pointerId) {
        return;
      }
      runtime.clientX = eventMove.clientX;
      runtime.clientY = eventMove.clientY;
      if (
        !runtime.dragging &&
        Math.hypot(
          eventMove.clientX - runtime.startX,
          eventMove.clientY - runtime.startY,
        ) >= TIMELINE_POLICY.drag.activationDistancePx
      ) {
        beginDragVisual();
      }
      if (runtime.dragging) {
        eventMove.preventDefault();
      }
      updateOverlay();
    };
    const finish = (eventUp: PointerEvent) => {
      const runtime = runtimeRef.current;
      if (!runtime || eventUp.pointerId !== runtime.pointerId) {
        return;
      }
      if (runtime.dragging) {
        commitDrag(eventUp.clientY);
      }
      dragCleanupRef.current?.();
      dragCleanupRef.current = null;
      runtimeRef.current = null;
    };
    const cancel = (eventCancel: PointerEvent) => {
      if (runtimeRef.current?.pointerId === eventCancel.pointerId) {
        cancelDrag();
      }
    };
    const lostCapture = (lostEvent: PointerEvent) => {
      if (runtimeRef.current?.pointerId === lostEvent.pointerId) {
        cancelDrag();
      }
    };
    const keyCancel = (keyEvent: globalThis.KeyboardEvent) => {
      if (keyEvent.key === 'Escape' && runtimeRef.current) {
        keyEvent.preventDefault();
        cancelDrag();
      }
    };
    const windowCancel = () => cancelDrag();
    const visibilityCancel = () => {
      if (document.visibilityState === 'hidden') {
        cancelDrag();
      }
    };
    const cleanup = () => {
      document.removeEventListener('pointermove', move, true);
      document.removeEventListener('pointerup', finish, true);
      document.removeEventListener('pointercancel', cancel, true);
      document.removeEventListener('keydown', keyCancel, true);
      document.removeEventListener('visibilitychange', visibilityCancel, true);
      window.removeEventListener('blur', windowCancel, true);
      card.removeEventListener('lostpointercapture', lostCapture, true);
      if (card.hasPointerCapture(pointerId)) {
        card.releasePointerCapture(pointerId);
      }
    };
    dragCleanupRef.current = cleanup;
    document.addEventListener('pointermove', move, true);
    document.addEventListener('pointerup', finish, true);
    document.addEventListener('pointercancel', cancel, true);
    document.addEventListener('keydown', keyCancel, true);
    document.addEventListener('visibilitychange', visibilityCancel, true);
    window.addEventListener('blur', windowCancel, true);
    card.addEventListener('lostpointercapture', lostCapture, true);
  };

  const keyboardMove = (
    event: TimelineEvent,
    dateKey: string,
    direction: 'earlier' | 'later' | 'previous-day' | 'next-day',
  ) => {
    const snap = timelineDragSnapMinutes(state.zoom);
    if (direction === 'previous-day' || direction === 'next-day') {
      const delta = direction === 'next-day' ? 1 : -1;
      const toDateKey = timelineDateKey(
        addTimelineDays(parseTimelineDate(dateKey), delta),
      );
      onMoveEvent({
        fromDateKey: dateKey,
        toDateKey,
        eventId: event.id,
        startMinute: event.startMinute,
      });
      onMoveFeedback(t(($) => $.common.home.timeline.feedback.movedDay));
      return;
    }

    const delta = direction === 'later' ? snap : -snap;
    onMoveEvent({
      fromDateKey: dateKey,
      toDateKey: dateKey,
      eventId: event.id,
      startMinute: event.startMinute + delta,
    });
    onMoveFeedback(t(($) => $.common.home.timeline.feedback.movedTime));
  };

  useEffect(() => {
    return () => {
      dragCleanupRef.current?.();
      if (autoScrollFrameRef.current !== null) {
        cancelAnimationFrame(autoScrollFrameRef.current);
      }
      runtimeRef.current?.overlay?.remove();
      runtimeRef.current?.card.classList.remove('is-drag-source');
    };
  }, []);

  const handleGridScroll = () => {
    const grid = gridRef.current;
    if (!grid) {
      return;
    }
    if (rulerStreamRef.current) {
      rulerStreamRef.current.style.transform = `translateY(${-grid.scrollTop}px)`;
    }
    onScroll(grid.scrollTop, grid.scrollLeft);
  };

  const pointerIsInsideFocusedCard = (target: EventTarget | null) =>
    target instanceof Element &&
    target.closest('.timeline-event-card.is-focused') !== null;

  return (
    <div className="timeline-frame timeline-frame--production">
      <div className="timeline-ruler" aria-hidden="true">
        <div ref={rulerStreamRef} className="timeline-ruler-stream">
          {days.map((day) => (
            <div
              className="timeline-ruler-day"
              key={day.dateKey}
              style={{ height: day.height }}
            >
              {Array.from(
                {
                  length:
                    TIMELINE_MINUTES_PER_DAY /
                      TIMELINE_POLICY.grid.majorLineIntervalMinutes +
                    1,
                },
                (_, index) =>
                  index * TIMELINE_POLICY.grid.majorLineIntervalMinutes,
              ).map((minute) => (
                <span
                  className="timeline-ruler-label"
                  key={minute}
                  style={{ top: day.mapper.map(minute) }}
                >
                  {formatTimelineMinute(minute)}
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>

      <div
        ref={gridRef}
        className={`timeline-grid${expanded ? ' is-expanded' : ''}`}
        onPointerDownCapture={(pointerEvent) => {
          if (focusedEvent && !pointerIsInsideFocusedCard(pointerEvent.target)) {
            pointerEvent.stopPropagation();
          }
        }}
        onClickCapture={(clickEvent) => {
          if (!focusedEvent || pointerIsInsideFocusedCard(clickEvent.target)) {
            return;
          }
          clickEvent.stopPropagation();
          onFocusEvent(focusedEvent.id);
        }}
        onScroll={handleGridScroll}
        onWheel={(wheelEvent) => {
          if (wheelEvent.ctrlKey) {
            wheelEvent.preventDefault();
            const factor = TIMELINE_POLICY.zoom.wheelStepFactor;
            onZoomAt(
              wheelEvent.clientY,
              wheelEvent.deltaY < 0 ? factor : 1 / factor,
            );
            return;
          }
          if (
            expanded &&
            wheelEvent.shiftKey &&
            Math.abs(wheelEvent.deltaY) > Math.abs(wheelEvent.deltaX)
          ) {
            wheelEvent.preventDefault();
            wheelEvent.currentTarget.scrollLeft += wheelEvent.deltaY;
          }
        }}
      >
        <div className="timeline-day-stream">
          {days.map((day) => (
            <TimelineDay
              day={day}
              today={today}
              nowMinute={nowMinute}
              state={state}
              focusedEvent={focusedEvent}
              key={day.dateKey}
              onFocusEvent={onFocusEvent}
              onToggleSubitems={onToggleSubitems}
              onOpenEventDetail={onOpenEventDetail}
              onOpenSubitemDetail={onOpenSubitemDetail}
              onOpenTimeEditor={onOpenTimeEditor}
              onPointerPress={startPointerPress}
              onKeyboardMove={keyboardMove}
              suppressClickRef={suppressClickRef}
            />
          ))}
          <div className="timeline-stream-loading">
            {t(($) => $.common.home.timeline.streamHint)}
          </div>
        </div>
      </div>

      <div
        className="timeline-zoom-float"
        aria-label={t(($) => $.common.home.timeline.zoom.label)}
      >
        <button
          type="button"
          onClick={() => {
            const grid = gridRef.current;
            if (grid) {
              const rect = grid.getBoundingClientRect();
              onZoomAt(
                rect.top + grid.clientHeight / 2,
                1 / TIMELINE_POLICY.zoom.controlStepFactor,
              );
            }
          }}
          aria-label={t(($) => $.common.home.timeline.zoom.out)}
        >
          −
        </button>
        <button
          type="button"
          onClick={() => {
            const grid = gridRef.current;
            if (grid) {
              const rect = grid.getBoundingClientRect();
              onZoomAt(
                rect.top + grid.clientHeight / 2,
                TIMELINE_POLICY.zoom.controlStepFactor,
              );
            }
          }}
          aria-label={t(($) => $.common.home.timeline.zoom.in)}
        >
          +
        </button>
      </div>
    </div>
  );
}
