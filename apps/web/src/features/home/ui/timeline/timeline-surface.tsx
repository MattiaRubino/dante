import type { PlainDate } from '@dante/time';
import {
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  useCallback,
  useLayoutEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';

import './timeline.css';

import { createTimelineTimeMapper } from './model/timeline-density';
import {
  TIMELINE_PROTOTYPE_NOW_MINUTE,
  TIMELINE_PROTOTYPE_TODAY,
} from './model/timeline-fixtures';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import { TIMELINE_POLICY } from './model/timeline-policy';
import {
  createInitialTimelineState,
  timelineEventsForDate,
  timelineReducer,
} from './model/timeline-state';
import {
  addTimelineDays,
  formatTimelineMinute,
  timelineDateKey,
} from './model/timeline-temporal';
import type { TimelineEvent, TimelineGroupId } from './model/timeline-types';
import {
  TimelineDayStream,
  type TimelineRenderedDay,
} from './timeline-day-stream';
import { TimelineHeader } from './timeline-header';
import {
  CalendarPopover,
  EventDetailDialog,
  TimeEditorPopover,
  UndoToast,
  ViewOptionsPopover,
  detailFromEvent,
  detailFromSubitem,
  type TimelineDetail,
} from './timeline-overlays';

type TimelineSurfaceProps = Readonly<{
  expanded: boolean;
  onExpandedChange: (expanded: boolean) => void;
  onExpansionProgress: (progress: number) => void;
}>;

type ScrollTarget = Readonly<{
  dateKey: string;
  minute: number | null;
  viewportOffset: number | null;
  behavior: ScrollBehavior;
}>;

type TimeEditorState = Readonly<{
  dateKey: string;
  event: TimelineEvent;
  anchor: HTMLButtonElement;
}>;

type DetailState = Readonly<{
  detail: TimelineDetail;
  opener: HTMLElement;
}>;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function buildRenderedDays(
  anchor: PlainDate,
  pastDays: number,
  futureDays: number,
  state: ReturnType<typeof createInitialTimelineState>,
): readonly TimelineRenderedDay[] {
  const days: TimelineRenderedDay[] = [];
  let offsetTop = 0;

  for (let offset = -pastDays; offset <= futureDays; offset += 1) {
    const date = addTimelineDays(anchor, offset);
    const dateKey = timelineDateKey(date);
    const events = timelineEventsForDate(state, dateKey);
    const mapper = createTimelineTimeMapper(events, state.zoom, {
      expandedEventIds: state.expandedEventIds,
    });
    const layouts = computeTimelineEventLayouts(events, state.groups, mapper);
    days.push({
      date,
      dateKey,
      events,
      mapper,
      layouts,
      offsetTop,
      height: mapper.height,
    });
    offsetTop += mapper.height;
  }

  return days;
}

function findDayAtOffset(
  days: readonly TimelineRenderedDay[],
  offset: number,
): TimelineRenderedDay | null {
  return (
    days.find(
      (day) => offset >= day.offsetTop && offset < day.offsetTop + day.height,
    ) ??
    (offset < (days[0]?.offsetTop ?? 0)
      ? days[0] ?? null
      : days.at(-1) ?? null)
  );
}

function applyTimelineExpansion(
  root: HTMLElement | null,
  grid: HTMLDivElement | null,
  groupScroller: HTMLDivElement | null,
  groupCount: number,
  progress: number,
) {
  if (!root || !grid) {
    return;
  }

  const p = window.innerWidth <= 1120 ? 0 : clamp(progress, 0, 1);
  const viewportWidth = Math.max(1, grid.clientWidth);
  const expandedTrack = Math.max(
    viewportWidth,
    44 + groupCount * TIMELINE_POLICY.layout.groupMinWidthPx + 16,
  );
  const trackWidth = viewportWidth + (expandedTrack - viewportWidth) * p;
  const compactInner = Math.max(1, trackWidth - 60);
  const expandedInner = Math.max(1, expandedTrack - 60);
  const safeGroupCount = Math.max(1, groupCount);
  const groupWidth = expandedInner / safeGroupCount;

  root.style.setProperty('--timeline-group-opacity', String(clamp((p - 0.16) / 0.52, 0, 1)));
  root.style.setProperty('--timeline-expansion-progress', String(p));

  const stream = root.querySelector<HTMLElement>('.timeline-day-stream');
  if (stream) {
    stream.style.minWidth = `${trackWidth}px`;
  }
  root.querySelectorAll<HTMLElement>('.timeline-day-section').forEach((section) => {
    section.style.minWidth = `${trackWidth}px`;
  });

  root.querySelectorAll<HTMLElement>('.timeline-event-card').forEach((card) => {
    const compactLeft = Number(card.dataset.compactLeft ?? 1.4);
    const compactWidth = Number(card.dataset.compactWidth ?? 56);
    const groupIndex = Math.max(0, Number(card.dataset.groupIndex ?? 0));
    const groupLane = Math.max(0, Number(card.dataset.groupLane ?? 0));
    const groupLanes = Math.max(1, Number(card.dataset.groupLanes ?? 1));

    const leftA = (compactLeft / 100) * compactInner;
    const widthA = (compactWidth / 100) * compactInner;
    const leftB =
      groupIndex * groupWidth + (groupLane / groupLanes) * groupWidth;
    const widthB = Math.max(24, groupWidth / groupLanes - 8);
    const left = leftA + (leftB - leftA) * p;
    const width = widthA + (widthB - widthA) * p;

    card.style.left = `${left + 4}px`;
    card.style.width = `${Math.max(24, width)}px`;
  });

  if (p < 0.98) {
    if (Math.abs(grid.scrollLeft) > 0.5) {
      grid.scrollLeft = 0;
    }
    if (groupScroller && Math.abs(groupScroller.scrollLeft) > 0.5) {
      groupScroller.scrollLeft = 0;
    }
  } else if (
    groupScroller &&
    Math.abs(groupScroller.scrollLeft - grid.scrollLeft) > 0.5
  ) {
    groupScroller.scrollLeft = grid.scrollLeft;
  }
}

export function TimelineSurface({
  expanded,
  onExpandedChange,
  onExpansionProgress,
}: TimelineSurfaceProps) {
  const { t, i18n } = useTranslation('common');
  const locale = i18n.resolvedLanguage ?? i18n.language;
  const [state, dispatch] = useReducer(
    timelineReducer,
    undefined,
    createInitialTimelineState,
  );
  const [anchor, setAnchor] = useState(TIMELINE_PROTOTYPE_TODAY);
  const [viewDate, setViewDate] = useState(TIMELINE_PROTOTYPE_TODAY);
  const [pastDays, setPastDays] = useState(
    TIMELINE_POLICY.window.initialPastDays,
  );
  const [futureDays, setFutureDays] = useState(
    TIMELINE_POLICY.window.initialFutureDays,
  );
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [viewOptionsOpen, setViewOptionsOpen] = useState(false);
  const [timeEditor, setTimeEditor] = useState<TimeEditorState | null>(null);
  const [detailState, setDetailState] = useState<DetailState | null>(null);
  const [nowNeeded, setNowNeeded] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastVisible, setToastVisible] = useState(false);

  const rootRef = useRef<HTMLElement | null>(null);
  const gridRef = useRef<HTMLDivElement | null>(null);
  const groupScrollerRef = useRef<HTMLDivElement | null>(null);
  const calendarTriggerRef = useRef<HTMLButtonElement | null>(null);
  const viewOptionsTriggerRef = useRef<HTMLButtonElement | null>(null);
  const expansionHandleRef = useRef<HTMLButtonElement | null>(null);
  const expansionProgressRef = useRef(expanded ? 1 : 0);
  const expansionFrameRef = useRef<number | null>(null);
  const pendingExpansionRef = useRef(expansionProgressRef.current);
  const expansionDragRef = useRef<{
    pointerId: number;
    startX: number;
    startProgress: number;
    dragDistance: number;
  } | null>(null);
  const renderedDaysRef = useRef<readonly TimelineRenderedDay[]>([]);
  const pendingScrollTargetRef = useRef<ScrollTarget | null>(null);
  const initialScrollDoneRef = useRef(false);
  const rawScrollRestoreRef = useRef<number | null>(null);
  const pastExtensionRestoreRef = useRef<{
    scrollTop: number;
    scrollHeight: number;
  } | null>(null);
  const extendingPastRef = useRef(false);
  const extendingFutureRef = useRef(false);
  const scrollFrameRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);

  const renderedDays = useMemo(
    () => buildRenderedDays(anchor, pastDays, futureDays, state),
    [anchor, futureDays, pastDays, state],
  );
  renderedDaysRef.current = renderedDays;

  const showFeedback = useCallback((message: string) => {
    setToastMessage(message);
    setToastVisible(true);
    if (toastTimerRef.current !== null) {
      window.clearTimeout(toastTimerRef.current);
    }
    toastTimerRef.current = window.setTimeout(() => {
      setToastVisible(false);
      toastTimerRef.current = null;
    }, 5000);
  }, []);

  const syncExpansion = useCallback(
    (progress: number) => {
      const p = window.innerWidth <= 1120 ? 0 : clamp(progress, 0, 1);
      expansionProgressRef.current = p;
      onExpansionProgress(p);
      applyTimelineExpansion(
        rootRef.current,
        gridRef.current,
        groupScrollerRef.current,
        state.groups.length,
        p,
      );
    },
    [onExpansionProgress, state.groups.length],
  );

  const requestExpansion = useCallback(
    (progress: number) => {
      pendingExpansionRef.current = progress;
      if (expansionFrameRef.current !== null) {
        return;
      }
      expansionFrameRef.current = requestAnimationFrame(() => {
        expansionFrameRef.current = null;
        syncExpansion(pendingExpansionRef.current);
      });
    },
    [syncExpansion],
  );

  const settleExpansion = useCallback(
    (target: 0 | 1) => {
      expansionDragRef.current = null;
      rootRef.current?.removeAttribute('data-timeline-expansion-dragging');
      syncExpansion(target);
      onExpandedChange(target === 1);
    },
    [onExpandedChange, syncExpansion],
  );

  const scrollToRenderedDay = useCallback(
    (target: ScrollTarget, days = renderedDaysRef.current) => {
      const grid = gridRef.current;
      if (!grid) {
        return false;
      }
      const day = days.find((candidate) => candidate.dateKey === target.dateKey);
      if (!day) {
        return false;
      }
      const minuteOffset =
        target.minute === null ? 0 : day.mapper.map(target.minute);
      const viewportOffset = target.viewportOffset ?? 0;
      const top = Math.max(0, day.offsetTop + minuteOffset - viewportOffset);
      grid.scrollTo({ top, behavior: target.behavior });
      return true;
    },
    [],
  );

  const goToDate = useCallback(
    (
      date: PlainDate,
      options: Readonly<{
        minute?: number;
        viewportOffset?: number;
        behavior?: ScrollBehavior;
      }> = {},
    ) => {
      const dateKey = timelineDateKey(date);
      const target: ScrollTarget = {
        dateKey,
        minute: options.minute ?? null,
        viewportOffset: options.viewportOffset ?? null,
        behavior: options.behavior ?? 'smooth',
      };
      setViewDate(date);
      if (scrollToRenderedDay(target)) {
        return;
      }
      pendingScrollTargetRef.current = target;
      setAnchor(date);
      setPastDays(TIMELINE_POLICY.window.initialPastDays);
      setFutureDays(TIMELINE_POLICY.window.initialFutureDays);
    },
    [scrollToRenderedDay],
  );

  const goNow = useCallback(() => {
    goToDate(TIMELINE_PROTOTYPE_TODAY, {
      minute: TIMELINE_PROTOTYPE_NOW_MINUTE,
      viewportOffset: Math.max(80, (gridRef.current?.clientHeight ?? 570) * 0.34),
      behavior: 'smooth',
    });
  }, [goToDate]);

  const synchronizeViewportContext = useCallback(
    (scrollTop: number) => {
      const grid = gridRef.current;
      const days = renderedDaysRef.current;
      if (!grid || days.length === 0) {
        return;
      }

      const probe = scrollTop + grid.clientHeight * 0.34;
      const viewed = findDayAtOffset(days, probe);
      if (viewed && !viewed.date.equals(viewDate)) {
        setViewDate(viewed.date);
      }

      const todayKey = timelineDateKey(TIMELINE_PROTOTYPE_TODAY);
      const today = days.find((day) => day.dateKey === todayKey);
      const nowY = today
        ? today.offsetTop + today.mapper.map(TIMELINE_PROTOTYPE_NOW_MINUTE)
        : null;
      const visible =
        nowY !== null &&
        nowY >= scrollTop &&
        nowY <= scrollTop + grid.clientHeight;
      setNowNeeded(!visible);
    },
    [viewDate],
  );

  const handleScroll = useCallback(
    (scrollTop: number, scrollLeft: number) => {
      const grid = gridRef.current;
      if (!grid) {
        return;
      }
      if (expanded && groupScrollerRef.current) {
        const scroller = groupScrollerRef.current;
        if (Math.abs(scroller.scrollLeft - scrollLeft) > 0.5) {
          scroller.scrollLeft = scrollLeft;
        }
      }

      if (scrollFrameRef.current === null) {
        scrollFrameRef.current = requestAnimationFrame(() => {
          scrollFrameRef.current = null;
          synchronizeViewportContext(grid.scrollTop);
        });
      }

      if (
        scrollTop < 420 &&
        pastDays < TIMELINE_POLICY.window.maxPastDays &&
        !extendingPastRef.current
      ) {
        extendingPastRef.current = true;
        pastExtensionRestoreRef.current = {
          scrollTop,
          scrollHeight: grid.scrollHeight,
        };
        setPastDays((value) =>
          Math.min(
            TIMELINE_POLICY.window.maxPastDays,
            value + TIMELINE_POLICY.window.extendByDays,
          ),
        );
      }

      if (
        scrollTop + grid.clientHeight > grid.scrollHeight - 500 &&
        futureDays < TIMELINE_POLICY.window.maxFutureDays &&
        !extendingFutureRef.current
      ) {
        extendingFutureRef.current = true;
        setFutureDays((value) =>
          Math.min(
            TIMELINE_POLICY.window.maxFutureDays,
            value + TIMELINE_POLICY.window.extendByDays,
          ),
        );
      }
    },
    [expanded, futureDays, pastDays, synchronizeViewportContext],
  );

  const zoomAt = useCallback(
    (clientY: number, factor: number) => {
      const grid = gridRef.current;
      if (!grid) {
        return;
      }
      const rect = grid.getBoundingClientRect();
      const viewportOffset = clientY - rect.top;
      const contentY = grid.scrollTop + viewportOffset;
      const day = findDayAtOffset(renderedDaysRef.current, contentY);
      if (!day) {
        return;
      }
      pendingScrollTargetRef.current = {
        dateKey: day.dateKey,
        minute: day.mapper.inv(contentY - day.offsetTop),
        viewportOffset,
        behavior: 'auto',
      };
      dispatch({ type: 'set-zoom', zoom: state.zoom * factor });
    },
    [state.zoom],
  );

  const preserveRawScroll = useCallback(() => {
    rawScrollRestoreRef.current = gridRef.current?.scrollTop ?? null;
  }, []);

  const closeCalendar = useCallback((restoreFocus = true) => {
    setCalendarOpen(false);
    if (restoreFocus) {
      requestAnimationFrame(() => calendarTriggerRef.current?.focus());
    }
  }, []);

  const closeViewOptions = useCallback((restoreFocus = true) => {
    setViewOptionsOpen(false);
    if (restoreFocus) {
      requestAnimationFrame(() => viewOptionsTriggerRef.current?.focus());
    }
  }, []);

  useLayoutEffect(() => {
    const grid = gridRef.current;
    if (!grid) {
      return;
    }

    if (!initialScrollDoneRef.current) {
      initialScrollDoneRef.current = true;
      const todayKey = timelineDateKey(TIMELINE_PROTOTYPE_TODAY);
      const day = renderedDays.find((candidate) => candidate.dateKey === todayKey);
      if (day) {
        grid.scrollTop = Math.max(
          0,
          day.offsetTop +
            day.mapper.map(TIMELINE_PROTOTYPE_NOW_MINUTE - 120) -
            70,
        );
      }
    }

    const pastRestore = pastExtensionRestoreRef.current;
    if (pastRestore) {
      const delta = grid.scrollHeight - pastRestore.scrollHeight;
      grid.scrollTop = pastRestore.scrollTop + Math.max(0, delta);
      pastExtensionRestoreRef.current = null;
    }
    extendingPastRef.current = false;
    extendingFutureRef.current = false;

    const rawScroll = rawScrollRestoreRef.current;
    if (rawScroll !== null) {
      grid.scrollTop = rawScroll;
      rawScrollRestoreRef.current = null;
    }

    const target = pendingScrollTargetRef.current;
    if (target && scrollToRenderedDay(target, renderedDays)) {
      pendingScrollTargetRef.current = null;
    }

    synchronizeViewportContext(grid.scrollTop);
    applyTimelineExpansion(
      rootRef.current,
      grid,
      groupScrollerRef.current,
      state.groups.length,
      expansionProgressRef.current,
    );
  }, [
    renderedDays,
    scrollToRenderedDay,
    state.groups.length,
    synchronizeViewportContext,
  ]);

  useLayoutEffect(() => {
    if (expansionDragRef.current) {
      return;
    }
    syncExpansion(expanded ? 1 : 0);
  }, [expanded, renderedDays, state.groups, syncExpansion]);

  useLayoutEffect(() => {
    const onResize = () => {
      if (window.innerWidth <= 1120) {
        syncExpansion(0);
      } else {
        syncExpansion(expanded ? 1 : expansionProgressRef.current);
      }
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [expanded, syncExpansion]);

  useLayoutEffect(() => {
    return () => {
      if (expansionFrameRef.current !== null) {
        cancelAnimationFrame(expansionFrameRef.current);
      }
      if (scrollFrameRef.current !== null) {
        cancelAnimationFrame(scrollFrameRef.current);
      }
      if (toastTimerRef.current !== null) {
        window.clearTimeout(toastTimerRef.current);
      }
    };
  }, []);

  const beginExpansionDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    if (window.innerWidth <= 1120 || event.button !== 0) {
      return;
    }
    const parent = rootRef.current?.parentElement;
    const rail = parent?.querySelector<HTMLElement>('.home-context-rail');
    const railWidth = rail?.getBoundingClientRect().width ?? 190;
    expansionDragRef.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      startProgress: expansionProgressRef.current,
      dragDistance: Math.max(110, railWidth),
    };
    rootRef.current?.setAttribute('data-timeline-expansion-dragging', 'true');
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const moveExpansionDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const drag = expansionDragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) {
      return;
    }
    const progress = clamp(
      drag.startProgress + (event.clientX - drag.startX) / drag.dragDistance,
      0,
      1,
    );
    requestExpansion(progress);
  };

  const finishExpansionDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const drag = expansionDragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) {
      return;
    }
    const progress = clamp(
      drag.startProgress + (event.clientX - drag.startX) / drag.dragDistance,
      0,
      1,
    );
    settleExpansion(progress >= 0.5 ? 1 : 0);
  };

  const expansionKeyDown = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      settleExpansion(expansionProgressRef.current >= 0.5 ? 0 : 1);
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      settleExpansion(1);
    } else if (event.key === 'ArrowLeft') {
      event.preventDefault();
      settleExpansion(0);
    }
  };

  return (
    <section
      ref={rootRef}
      className="home-timeline home-timeline--production"
      data-home-region="timeline"
      data-home-timeline-state={expanded ? 'expanded' : 'normal'}
      aria-label={t(($) => $.common.home.timeline.label)}
    >
      <TimelineHeader
        locale={locale}
        today={TIMELINE_PROTOTYPE_TODAY}
        viewDate={viewDate}
        groups={state.groups}
        filters={state.filters}
        nowNeeded={nowNeeded}
        split={expanded}
        calendarOpen={calendarOpen}
        viewOptionsOpen={viewOptionsOpen}
        calendarTriggerRef={calendarTriggerRef}
        viewOptionsTriggerRef={viewOptionsTriggerRef}
        groupScrollerRef={groupScrollerRef}
        onCalendarToggle={() => {
          setViewOptionsOpen(false);
          setCalendarOpen((value) => !value);
        }}
        onDateSelect={(date) => goToDate(date)}
        onGoNow={goNow}
        onViewOptionsToggle={() => {
          setCalendarOpen(false);
          setViewOptionsOpen((value) => !value);
        }}
        onSplitToggle={() =>
          settleExpansion(expansionProgressRef.current >= 0.5 ? 0 : 1)
        }
        onResetGroupsFocus={() => dispatch({ type: 'reset-groups-focus' })}
        onToggleFilter={(groupId: TimelineGroupId) =>
          dispatch({ type: 'toggle-filter', groupId })
        }
        onReorderGroup={(groupId, targetIndex) =>
          dispatch({ type: 'reorder-group', groupId, targetIndex })
        }
        onGroupScroll={(scrollLeft) => {
          const grid = gridRef.current;
          if (
            expanded &&
            grid &&
            Math.abs(grid.scrollLeft - scrollLeft) > 0.5
          ) {
            grid.scrollLeft = scrollLeft;
          }
        }}
      />

      <TimelineDayStream
        days={renderedDays}
        today={TIMELINE_PROTOTYPE_TODAY}
        nowMinute={TIMELINE_PROTOTYPE_NOW_MINUTE}
        state={state}
        expanded={expanded}
        gridRef={gridRef}
        onScroll={handleScroll}
        onZoomAt={zoomAt}
        onFocusEvent={(eventId) => dispatch({ type: 'focus-event', eventId })}
        onToggleSubitems={(eventId) => {
          preserveRawScroll();
          dispatch({ type: 'toggle-event-subitems', eventId });
        }}
        onOpenEventDetail={(event, opener) =>
          setDetailState({
            detail: detailFromEvent(event, state.groups),
            opener,
          })
        }
        onOpenSubitemDetail={(event, subitem, opener) =>
          setDetailState({
            detail: detailFromSubitem(
              event,
              subitem,
              state.groups,
              t(($) => $.common.home.timeline.detail.subitemParent),
            ),
            opener,
          })
        }
        onOpenTimeEditor={(dateKey, event, editorAnchor) =>
          setTimeEditor({ dateKey, event, anchor: editorAnchor })
        }
        onMoveEvent={(move) => {
          preserveRawScroll();
          dispatch({ type: 'move-event', ...move });
        }}
        onMoveFeedback={showFeedback}
      />

      <button
        ref={expansionHandleRef}
        className="timeline-expansion-handle"
        type="button"
        onPointerDown={beginExpansionDrag}
        onPointerMove={moveExpansionDrag}
        onPointerUp={finishExpansionDrag}
        onPointerCancel={finishExpansionDrag}
        onKeyDown={expansionKeyDown}
        aria-label={t(($) =>
          expanded
            ? $.common.home.timeline.collapse
            : $.common.home.timeline.expand,
        )}
        aria-pressed={expanded}
      >
        <span aria-hidden="true" />
      </button>

      <CalendarPopover
        open={calendarOpen}
        locale={locale}
        today={TIMELINE_PROTOTYPE_TODAY}
        viewDate={viewDate}
        triggerRef={calendarTriggerRef}
        onClose={closeCalendar}
        onDateSelect={(date) => goToDate(date)}
        onGoToday={goNow}
      />

      <ViewOptionsPopover
        open={viewOptionsOpen}
        triggerRef={viewOptionsTriggerRef}
        options={state.viewOptions}
        onChange={(option, value) =>
          dispatch({ type: 'set-view-option', option, value })
        }
        onReset={() => dispatch({ type: 'reset-view-options' })}
        onClose={closeViewOptions}
      />

      {timeEditor ? (
        <TimeEditorPopover
          event={timeEditor.event}
          dateKey={timeEditor.dateKey}
          anchor={timeEditor.anchor}
          gridRef={gridRef}
          onSave={(dateKey, eventId, startMinute, endMinute) => {
            preserveRawScroll();
            dispatch({
              type: 'update-event-time',
              dateKey,
              eventId,
              startMinute,
              endMinute,
            });
            showFeedback(
              `${t(($) => $.common.home.timeline.feedback.timeUpdated)} ${formatTimelineMinute(startMinute)}–${formatTimelineMinute(endMinute)}`,
            );
          }}
          onClose={(restoreFocus = true) => {
            const anchorButton = timeEditor.anchor;
            setTimeEditor(null);
            if (restoreFocus) {
              requestAnimationFrame(() => anchorButton.focus());
            }
          }}
        />
      ) : null}

      <EventDetailDialog
        detail={detailState?.detail ?? null}
        opener={detailState?.opener ?? null}
        onClose={() => setDetailState(null)}
      />

      <UndoToast
        visible={toastVisible && state.undo !== null}
        message={toastMessage}
        onUndo={() => {
          preserveRawScroll();
          dispatch({ type: 'undo-last-event-change' });
          setToastVisible(false);
        }}
      />
    </section>
  );
}
