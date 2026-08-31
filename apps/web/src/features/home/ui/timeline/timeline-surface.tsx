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

import {
  TIMELINE_PROTOTYPE_NOW_MINUTE,
  TIMELINE_PROTOTYPE_TODAY,
} from './model/timeline-fixtures';
import {
  timelineEffectiveScrollBehavior,
  timelinePrefersReducedMotion,
} from './model/timeline-motion';
import {
  TIMELINE_POLICY,
  timelineSupportsExpandedLayout,
} from './model/timeline-policy';
import {
  createInitialTimelineState,
  timelineReducer,
} from './model/timeline-state';
import {
  addTimelineDays,
  formatTimelineMinute,
  parseTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type { TimelineEvent, TimelineGroupId } from './model/timeline-types';
import { TimelineDayStream } from './timeline-day-stream';
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
import {
  applyTimelineExpansion,
  buildTimelineRenderedDays,
  captureTimelineViewportAnchor,
  clampTimelineRuntime,
  findTimelineDayAtOffset,
  parseTimelineViewedDate,
  timelineNowViewportOffset,
  type TimelineRenderedDay,
} from './timeline-viewport-runtime';

type TimelineSurfaceProps = Readonly<{
  expanded: boolean;
  onExpandedChange: (expanded: boolean) => void;
  onExpansionProgress: (progress: number) => void;
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
  onDateNavigation?: ((isoDate: string | undefined) => void) | undefined;
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

export function TimelineSurface({
  expanded,
  onExpandedChange,
  onExpansionProgress,
  viewedDateIso,
  onViewedDateChange,
  onDateNavigation,
}: TimelineSurfaceProps) {
  const { t, i18n } = useTranslation('common');
  const locale = i18n.resolvedLanguage ?? i18n.language;
  // Phase 1 parity deliberately uses the accepted prototype clock. The mock
  // dataset is built around this instant; using wall-clock time makes the
  // initial viewport visually incomparable and moves the Now line away from
  // the reference scene. A real clock belongs to the later data-source layer.
  const timelineToday = TIMELINE_PROTOTYPE_TODAY;
  const timelineNowMinute = TIMELINE_PROTOTYPE_NOW_MINUTE;
  const initialDate = parseTimelineViewedDate(viewedDateIso) ?? timelineToday;
  const initialDateRef = useRef(initialDate);
  const [state, dispatch] = useReducer(
    timelineReducer,
    timelineToday,
    createInitialTimelineState,
  );
  const [anchor, setAnchor] = useState<PlainDate>(() => initialDate);
  const [viewDate, setViewDate] = useState<PlainDate>(() => initialDate);
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
  const expansionProgressRef = useRef(expanded ? 1 : 0);
  const expansionFrameRef = useRef<number | null>(null);
  const pendingExpansionRef = useRef(expanded ? 1 : 0);
  const expansionDragRef = useRef<{
    pointerId: number;
    startX: number;
    startProgress: number;
    dragDistance: number;
  } | null>(null);
  const suppressExpansionClickRef = useRef(false);
  const renderedDaysRef = useRef<readonly TimelineRenderedDay[]>([]);
  const pendingScrollTargetRef = useRef<ScrollTarget | null>(null);
  const initialScrollDoneRef = useRef(false);
  const initialViewPublishedRef = useRef(false);
  const rawScrollRestoreRef = useRef<number | null>(null);
  const windowTransitionRef = useRef(false);
  const lastScrollTopRef = useRef<number | null>(null);
  const scrollFrameRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);

  const renderedDayInputs = useMemo(
    () => ({
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    }),
    [state.eventsByDate, state.expandedEventIds, state.groups, state.zoom],
  );
  const renderedDays = useMemo(
    () =>
      buildTimelineRenderedDays(
        anchor,
        TIMELINE_POLICY.window.pastBufferDays,
        TIMELINE_POLICY.window.futureBufferDays,
        renderedDayInputs,
      ),
    [anchor, renderedDayInputs],
  );

  useLayoutEffect(() => {
    renderedDaysRef.current = renderedDays;
  }, [renderedDays]);

  const showFeedback = useCallback((message: string) => {
    setToastMessage(message);
    setToastVisible(true);
    if (toastTimerRef.current !== null) {
      window.clearTimeout(toastTimerRef.current);
    }
    toastTimerRef.current = window.setTimeout(() => {
      setToastVisible(false);
      toastTimerRef.current = null;
    }, TIMELINE_POLICY.feedback.toastDurationMs);
  }, []);

  const publishViewportDate = useCallback(
    (date: PlainDate) => {
      onViewedDateChange?.(
        date.equals(timelineToday) ? undefined : timelineDateKey(date),
      );
    },
    [onViewedDateChange, timelineToday],
  );

  const syncExpansion = useCallback(
    (progress: number) => {
      const normalizedProgress = timelineSupportsExpandedLayout(
        window.innerWidth,
      )
        ? clampTimelineRuntime(progress, 0, 1)
        : 0;
      expansionProgressRef.current = normalizedProgress;
      onExpansionProgress(normalizedProgress);
      applyTimelineExpansion(
        rootRef.current,
        gridRef.current,
        groupScrollerRef.current,
        state.groups.length,
        normalizedProgress,
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
      const day = days.find(
        (candidate) => candidate.dateKey === target.dateKey,
      );
      if (!day) {
        return false;
      }
      const minuteOffset =
        target.minute === null ? 0 : day.mapper.map(target.minute);
      const viewportOffset = target.viewportOffset ?? 0;
      const top = Math.max(0, day.offsetTop + minuteOffset - viewportOffset);
      const behavior = timelineEffectiveScrollBehavior(
        target.behavior,
        timelinePrefersReducedMotion(),
      );
      if (behavior === 'auto' || typeof grid.scrollTo !== 'function') {
        grid.scrollTop = top;
      } else {
        grid.scrollTo({ top, behavior });
      }
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
      notifyNavigation = true,
    ) => {
      const dateKey = timelineDateKey(date);
      const routeDate = date.equals(timelineToday) ? undefined : dateKey;
      const target: ScrollTarget = {
        dateKey,
        minute: options.minute ?? null,
        viewportOffset: options.viewportOffset ?? null,
        behavior: options.behavior ?? 'smooth',
      };
      setViewDate(date);
      publishViewportDate(date);
      if (notifyNavigation) {
        onDateNavigation?.(routeDate);
      }
      if (scrollToRenderedDay(target)) {
        return;
      }
      pendingScrollTargetRef.current = target;
      windowTransitionRef.current = true;
      setAnchor(date);
    },
    [onDateNavigation, publishViewportDate, scrollToRenderedDay, timelineToday],
  );

  const goNow = useCallback(() => {
    goToDate(timelineToday, {
      minute: timelineNowMinute,
      viewportOffset: timelineNowViewportOffset(
        gridRef.current?.clientHeight ??
          TIMELINE_POLICY.viewport.defaultGridHeightPx,
      ),
      behavior: 'smooth',
    });
  }, [goToDate, timelineNowMinute, timelineToday]);

  const synchronizeViewportContext = useCallback(
    (scrollTop: number) => {
      const grid = gridRef.current;
      const days = renderedDaysRef.current;
      if (!grid || days.length === 0) {
        return;
      }

      const probe =
        scrollTop +
        grid.clientHeight * TIMELINE_POLICY.viewport.contextProbeRatio;
      const viewed = findTimelineDayAtOffset(days, probe);
      if (viewed && !viewed.date.equals(viewDate)) {
        setViewDate(viewed.date);
        publishViewportDate(viewed.date);
      }

      const todayKey = timelineDateKey(timelineToday);
      const today = days.find((day) => day.dateKey === todayKey);
      const nowY = today
        ? today.offsetTop + today.mapper.map(timelineNowMinute)
        : null;
      const visible =
        nowY !== null &&
        nowY >= scrollTop &&
        nowY <= scrollTop + grid.clientHeight;
      setNowNeeded(!visible);
    },
    [publishViewportDate, timelineNowMinute, timelineToday, viewDate],
  );

  const handleScroll = useCallback(
    (scrollTop: number, scrollLeft: number) => {
      const grid = gridRef.current;
      if (!grid) {
        return;
      }
      const syncTolerance = TIMELINE_POLICY.viewport.horizontalSyncTolerancePx;
      if (expanded && groupScrollerRef.current) {
        const scroller = groupScrollerRef.current;
        if (Math.abs(scroller.scrollLeft - scrollLeft) > syncTolerance) {
          scroller.scrollLeft = scrollLeft;
        }
      }

      if (scrollFrameRef.current === null) {
        scrollFrameRef.current = requestAnimationFrame(() => {
          scrollFrameRef.current = null;
          synchronizeViewportContext(grid.scrollTop);
        });
      }

      const previousScrollTop = lastScrollTopRef.current ?? scrollTop;
      const verticalDelta = scrollTop - previousScrollTop;
      lastScrollTopRef.current = scrollTop;

      let shiftDays = 0;
      if (
        verticalDelta < 0 &&
        scrollTop < TIMELINE_POLICY.window.recyclePastTriggerPx
      ) {
        shiftDays = -TIMELINE_POLICY.window.shiftByDays;
      } else if (
        verticalDelta > 0 &&
        scrollTop + grid.clientHeight >
          grid.scrollHeight - TIMELINE_POLICY.window.recycleFutureTriggerPx
      ) {
        shiftDays = TIMELINE_POLICY.window.shiftByDays;
      }

      if (shiftDays !== 0 && !windowTransitionRef.current) {
        const viewportAnchor = captureTimelineViewportAnchor(
          renderedDaysRef.current,
          scrollTop,
          TIMELINE_POLICY.window.recycleAnchorViewportOffsetPx,
        );
        if (viewportAnchor) {
          pendingScrollTargetRef.current = {
            ...viewportAnchor,
            behavior: 'auto',
          };
          windowTransitionRef.current = true;
          setAnchor((current) => addTimelineDays(current, shiftDays));
        }
      }
    },
    [expanded, synchronizeViewportContext],
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
      const day = findTimelineDayAtOffset(renderedDaysRef.current, contentY);
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
    if (initialViewPublishedRef.current) {
      return;
    }
    initialViewPublishedRef.current = true;
    publishViewportDate(viewDate);
  }, [publishViewportDate, viewDate]);

  useLayoutEffect(() => {
    const externalDate =
      parseTimelineViewedDate(viewedDateIso) ?? timelineToday;
    if (externalDate.equals(viewDate)) {
      return;
    }
    const frame = requestAnimationFrame(() => {
      goToDate(externalDate, { behavior: 'auto' }, false);
    });
    return () => cancelAnimationFrame(frame);
  }, [goToDate, timelineToday, viewDate, viewedDateIso]);

  useLayoutEffect(() => {
    const grid = gridRef.current;
    if (!grid) {
      return;
    }

    if (!initialScrollDoneRef.current) {
      initialScrollDoneRef.current = true;
      const initialKey = timelineDateKey(initialDateRef.current);
      const day = renderedDays.find(
        (candidate) => candidate.dateKey === initialKey,
      );
      if (day) {
        if (initialDateRef.current.equals(timelineToday)) {
          grid.scrollTop = Math.max(
            0,
            day.offsetTop +
              day.mapper.map(timelineNowMinute) -
              timelineNowViewportOffset(grid.clientHeight),
          );
        } else {
          grid.scrollTop = Math.max(
            0,
            day.offsetTop +
              day.mapper.map(TIMELINE_POLICY.viewport.initialExternalMinute) -
              TIMELINE_POLICY.viewport.initialExternalOffsetPx,
          );
        }
      }
    }

    const rawScroll = rawScrollRestoreRef.current;
    if (rawScroll !== null) {
      grid.scrollTop = rawScroll;
      rawScrollRestoreRef.current = null;
    }

    const target = pendingScrollTargetRef.current;
    if (target && scrollToRenderedDay(target, renderedDays)) {
      pendingScrollTargetRef.current = null;
      windowTransitionRef.current = false;
    }
    lastScrollTopRef.current = grid.scrollTop;

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
    timelineNowMinute,
    timelineToday,
  ]);

  useLayoutEffect(() => {
    if (expansionDragRef.current) {
      return;
    }
    if (!timelineSupportsExpandedLayout(window.innerWidth) && expanded) {
      syncExpansion(0);
      onExpandedChange(false);
      return;
    }
    syncExpansion(expanded ? 1 : 0);
  }, [expanded, onExpandedChange, renderedDays, state.groups, syncExpansion]);

  useLayoutEffect(() => {
    const onResize = () => {
      if (!timelineSupportsExpandedLayout(window.innerWidth)) {
        syncExpansion(0);
        if (expanded) {
          onExpandedChange(false);
        }
      } else {
        syncExpansion(expanded ? 1 : expansionProgressRef.current);
      }
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [expanded, onExpandedChange, syncExpansion]);

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
    if (
      !timelineSupportsExpandedLayout(window.innerWidth) ||
      event.button !== 0
    ) {
      return;
    }
    const parent = rootRef.current?.parentElement;
    const rail = parent?.querySelector<HTMLElement>('.home-context-rail');
    const railWidth =
      rail?.getBoundingClientRect().width ??
      TIMELINE_POLICY.expansion.defaultContextRailWidthPx;
    expansionDragRef.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      startProgress: expansionProgressRef.current,
      dragDistance: Math.max(
        TIMELINE_POLICY.expansion.minDragDistancePx,
        railWidth,
      ),
    };
    rootRef.current?.setAttribute('data-timeline-expansion-dragging', 'true');
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const moveExpansionDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const drag = expansionDragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) {
      return;
    }
    const progress = clampTimelineRuntime(
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
    const deltaX = event.clientX - drag.startX;
    const progress = clampTimelineRuntime(
      drag.startProgress + deltaX / drag.dragDistance,
      0,
      1,
    );
    expansionDragRef.current = null;
    rootRef.current?.removeAttribute('data-timeline-expansion-dragging');

    if (Math.abs(deltaX) < TIMELINE_POLICY.expansion.dragActivationDistancePx) {
      return;
    }

    suppressExpansionClickRef.current = true;
    settleExpansion(
      progress >= TIMELINE_POLICY.expansion.settleThreshold ? 1 : 0,
    );
    requestAnimationFrame(() => {
      suppressExpansionClickRef.current = false;
    });
  };

  const cancelExpansionDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const drag = expansionDragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) {
      return;
    }
    expansionDragRef.current = null;
    rootRef.current?.removeAttribute('data-timeline-expansion-dragging');
    settleExpansion(
      drag.startProgress >= TIMELINE_POLICY.expansion.settleThreshold ? 1 : 0,
    );
  };

  const expansionKeyDown = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      settleExpansion(
        expansionProgressRef.current >=
          TIMELINE_POLICY.expansion.settleThreshold
          ? 0
          : 1,
      );
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
        today={timelineToday}
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
          settleExpansion(
            expansionProgressRef.current >=
              TIMELINE_POLICY.expansion.settleThreshold
              ? 0
              : 1,
          )
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
            Math.abs(grid.scrollLeft - scrollLeft) >
              TIMELINE_POLICY.viewport.horizontalSyncTolerancePx
          ) {
            grid.scrollLeft = scrollLeft;
          }
        }}
      />

      <TimelineDayStream
        days={renderedDays}
        today={timelineToday}
        nowMinute={timelineNowMinute}
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
          const targetIsRendered = renderedDaysRef.current.some(
            (day) => day.dateKey === move.toDateKey,
          );
          if (targetIsRendered) {
            preserveRawScroll();
          } else {
            rawScrollRestoreRef.current = null;
            pendingScrollTargetRef.current = {
              dateKey: move.toDateKey,
              minute: move.startMinute,
              viewportOffset: TIMELINE_POLICY.viewport.eventRevealInsetPx,
              behavior: 'auto',
            };
            windowTransitionRef.current = true;
            setAnchor(parseTimelineDate(move.toDateKey));
          }
          dispatch({ type: 'move-event', ...move });
        }}
        onMoveFeedback={showFeedback}
      />

      <button
        className="timeline-expansion-handle"
        type="button"
        onClick={() => {
          if (suppressExpansionClickRef.current) {
            suppressExpansionClickRef.current = false;
            return;
          }
          settleExpansion(
            expansionProgressRef.current >=
              TIMELINE_POLICY.expansion.settleThreshold
              ? 0
              : 1,
          );
        }}
        onPointerDown={beginExpansionDrag}
        onPointerMove={moveExpansionDrag}
        onPointerUp={finishExpansionDrag}
        onPointerCancel={cancelExpansionDrag}
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
        today={timelineToday}
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
