import { Temporal, detectDeviceTimeZone, type PlainDate } from '@dante/time';
import {
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';

import './timeline.css';

import { TemporalScheduleRemoteError } from '../../../temporal/remote-schedule-data-source';
import type { TemporalSchedulePlacementInput } from '../../../temporal/schedule-data-source';
import { useTemporalTimelineRuntime } from '../../../temporal/timeline-runtime-boundary';
import { useAuthoritativeTimelineHydration } from './timeline-authoritative-hydration';
import { TimelineCanonicalActionsProvider } from './timeline-canonical-actions';
import { createTimelineLocalContext } from './model/timeline-context-catalog';
import {
  TIMELINE_PROTOTYPE_NOW_MINUTE,
  TIMELINE_PROTOTYPE_TODAY,
} from './model/timeline-fixtures';
import { timelineCanonicalRevisionForDisplayEdit } from './model/timeline-canonical-revision';
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
  findTimelineEvent,
  timelineReducer,
} from './model/timeline-state';
import {
  addTimelineDays,
  formatTimelineMinute,
  parseTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type {
  TimelineAllDayItem,
  TimelineCanonicalScheduleBasis,
  TimelineEvent,
  TimelineGroup,
  TimelineGroupId,
  TimelineSemanticTone,
} from './model/timeline-types';
import { applyTimelineAllDayGeometry } from './timeline-all-day-runtime';
import { TimelineDayStream } from './timeline-day-stream';
import { TimelineHeader } from './timeline-header';
import {
  canonicalOrganizationGroups,
  LEGACY_UNASSIGNED_GROUP,
  TimelineOrganizationPanel,
  useTimelineOrganization,
} from './timeline-organization';
import { TimelinePostponedEventsPanel } from './timeline-postponed-events';
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
  event: TimelineEvent;
  allowUnschedule: boolean;
  opener: HTMLElement;
}>;

type ScheduleNotice = Readonly<{
  kind: 'status' | 'error';
  message: string;
}>;

type CanonicalScheduleUndo =
  | Readonly<{
      kind: 'revision';
      scheduleRef: string;
      expectedPlacementMaterialStateRef: string;
      placement: TemporalSchedulePlacementInput;
    }>
  | Readonly<{
      kind: 'unschedule';
      scheduleRef: string;
      unscheduleOperationId: string;
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
  const {
    state: temporalRuntimeState,
    reviseSchedule,
    undoScheduleUnschedule,
    unscheduleSchedule,
  } = useTemporalTimelineRuntime();
  const effectiveZoneId =
    temporalRuntimeState.status === 'ready'
      ? temporalRuntimeState.effectiveZoneId
      : null;
  const locale = i18n.resolvedLanguage ?? i18n.language;
  const prototypeMode = import.meta.env.MODE === 'test';
  const clockZone = effectiveZoneId ?? detectDeviceTimeZone();
  const timelineToday = prototypeMode
    ? TIMELINE_PROTOTYPE_TODAY
    : Temporal.Now.plainDateISO(clockZone);
  const now = Temporal.Now.zonedDateTimeISO(clockZone);
  const timelineNowMinute = prototypeMode
    ? TIMELINE_PROTOTYPE_NOW_MINUTE
    : now.hour * 60 + now.minute;
  const initialDate = parseTimelineViewedDate(viewedDateIso) ?? timelineToday;
  const initialDateRef = useRef(initialDate);
  const [state, dispatch] = useReducer(
    timelineReducer,
    timelineToday,
    (today) => createInitialTimelineState(today, prototypeMode),
  );
  const organization = useTimelineOrganization(!prototypeMode);
  const canonicalGroups = useMemo(
    () =>
      organization.snapshot === null
        ? null
        : canonicalOrganizationGroups(organization.snapshot),
    [organization.snapshot],
  );
  const creationEnabled =
    prototypeMode ||
    (organization.snapshot?.areas.some((area) => !area.archived) ?? false);
  useEffect(() => {
    if (canonicalGroups !== null) {
      dispatch({ type: 'reconcile-canonical-groups', groups: canonicalGroups });
    }
  }, [canonicalGroups]);
  const assignmentBySubject = useMemo(
    () =>
      new Map(
        organization.snapshot?.assignments.map((entry) => [
          `${entry.kind}:${entry.itemRef}`,
          entry.areaRef,
        ]) ?? [],
      ),
    [organization.snapshot],
  );
  const resolveGroupId = useCallback(
    (item: import('../../../temporal/timeline-read').TemporalTimelineItem) =>
      assignmentBySubject.get(
        item.kind === 'scheduled_activity'
          ? `activity:${item.activityRef}`
          : item.kind === 'scheduled_event'
            ? `event:${item.eventRef}`
            : `${item.sourceKind}:${item.sourceNativeRef}`,
      ) ?? LEGACY_UNASSIGNED_GROUP,
    [assignmentBySubject],
  );
  const visibleGroups = useMemo(
    () => state.groups.filter((group) => !group.hidden),
    [state.groups],
  );
  const presentationFilters = useMemo(() => {
    if (!state.groups.some((group) => group.hidden)) return state.filters;
    const visible = new Set(visibleGroups.map((group) => group.id));
    if (state.filters.size) {
      const focused = new Set(
        [...state.filters].filter((id) => visible.has(id)),
      );
      return focused.size ? focused : new Set(['__no_visible_area__']);
    }
    // A sentinel prevents an empty focus from accidentally showing every hidden item.
    return visible.size ? visible : new Set(['__no_visible_area__']);
  }, [state.filters, state.groups, visibleGroups]);
  const [anchor, setAnchor] = useState<PlainDate>(() => initialDate);
  const [viewDate, setViewDate] = useState<PlainDate>(() => initialDate);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [viewOptionsOpen, setViewOptionsOpen] = useState(false);
  const [timeEditor, setTimeEditor] = useState<TimeEditorState | null>(null);
  const [detailState, setDetailState] = useState<DetailState | null>(null);
  const [nowNeeded, setNowNeeded] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastVisible, setToastVisible] = useState(false);
  const [scheduleNotice, setScheduleNotice] = useState<ScheduleNotice | null>(
    null,
  );
  const [canonicalUndo, setCanonicalUndo] =
    useState<CanonicalScheduleUndo | null>(null);
  const [pendingScheduleRef, setPendingScheduleRef] = useState<string | null>(
    null,
  );

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
  const scheduleNoticeTimerRef = useRef<number | null>(null);
  const pendingScheduleRefsRef = useRef(new Set<string>());

  const reconcileAuthoritativeEvents = useCallback(
    (
      projections: readonly Readonly<{
        dateKey: string;
        event: TimelineEvent;
      }>[],
    ) => {
      dispatch({ type: 'reconcile-authoritative-events', projections });
    },
    [],
  );
  const reconcileAuthoritativeDateLane = useCallback(
    (items: readonly TimelineAllDayItem[]) => {
      const incomingIds = new Set(items.map((item) => item.id));
      for (const current of state.allDayItems) {
        if (
          current.canonicalBasis !== undefined ||
          incomingIds.has(current.id)
        ) {
          dispatch({ type: 'remove-all-day', itemId: current.id });
        }
      }
      for (const item of items) {
        dispatch({ type: 'materialize-all-day', item });
      }
    },
    [state.allDayItems],
  );
  useAuthoritativeTimelineHydration(
    reconcileAuthoritativeEvents,
    reconcileAuthoritativeDateLane,
    prototypeMode
      ? undefined
      : organization.snapshot === null
        ? null
        : resolveGroupId,
  );

  const renderedDayInputs = useMemo(
    () => ({
      eventsByDate: state.eventsByDate,
      groups: visibleGroups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    }),
    [state.eventsByDate, state.expandedEventIds, visibleGroups, state.zoom],
  );
  const baseRenderedDays = useMemo(
    () =>
      buildTimelineRenderedDays(
        anchor,
        TIMELINE_POLICY.window.pastBufferDays,
        TIMELINE_POLICY.window.futureBufferDays,
        renderedDayInputs,
      ),
    [anchor, renderedDayInputs],
  );
  const renderedDays = useMemo(
    () =>
      applyTimelineAllDayGeometry(
        baseRenderedDays,
        state.allDayItems,
        presentationFilters,
      ),
    [baseRenderedDays, state.allDayItems, presentationFilters],
  );

  useLayoutEffect(() => {
    renderedDaysRef.current = renderedDays;
  }, [renderedDays]);

  const showFeedback = useCallback((message: string) => {
    setCanonicalUndo(null);
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

  const showScheduleNotice = useCallback((notice: ScheduleNotice) => {
    setScheduleNotice(notice);
    if (scheduleNoticeTimerRef.current !== null) {
      window.clearTimeout(scheduleNoticeTimerRef.current);
    }
    scheduleNoticeTimerRef.current = window.setTimeout(() => {
      setScheduleNotice(null);
      scheduleNoticeTimerRef.current = null;
    }, TIMELINE_POLICY.feedback.toastDurationMs);
  }, []);

  const showCanonicalUndo = useCallback((message: string) => {
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

  const reviseCanonicalEvent = useCallback(
    (
      event: TimelineEvent,
      fromDateKey: string,
      toDateKey: string,
      startMinute: number,
      endMinute: number,
    ) => {
      const basis = event.canonicalBasis;
      if (
        basis === undefined ||
        effectiveZoneId === null ||
        pendingScheduleRefsRef.current.has(basis.scheduleRef)
      ) {
        return;
      }

      const revision = timelineCanonicalRevisionForDisplayEdit({
        basis,
        fromDateKey,
        previousStartMinute: event.startMinute,
        previousEndMinute: event.endMinute,
        toDateKey,
        startMinute,
        endMinute,
        effectiveZoneId,
      });
      if (revision === null) {
        showScheduleNotice({
          kind: 'error',
          message: t(
            ($) => $.common.home.timeline.feedback.scheduleRevisionUnavailable,
          ),
        });
        return;
      }

      pendingScheduleRefsRef.current.add(basis.scheduleRef);
      setPendingScheduleRef(basis.scheduleRef);
      void reviseSchedule({
        scheduleRef: basis.scheduleRef,
        expectedPlacementMaterialStateRef: basis.placementMaterialStateRef,
        placement: revision.next,
      })
        .then((result) => {
          setCanonicalUndo({
            kind: 'revision',
            scheduleRef: result.scheduleRef,
            expectedPlacementMaterialStateRef: result.placementMaterialStateRef,
            placement: revision.previous,
          });
          showCanonicalUndo(
            t(($) => $.common.home.timeline.feedback.scheduleUndoAvailable),
          );
          showScheduleNotice({
            kind: 'status',
            message: t(
              ($) => $.common.home.timeline.feedback.scheduleRevisionUpdated,
            ),
          });
        })
        .catch((error: unknown) => {
          const conflict =
            error instanceof TemporalScheduleRemoteError &&
            error.status === 409 &&
            error.code === 'temporal.schedule.revision_conflict';
          showScheduleNotice({
            kind: 'error',
            message: conflict
              ? t(
                  ($) =>
                    $.common.home.timeline.feedback.scheduleRevisionConflict,
                )
              : t(
                  ($) =>
                    $.common.home.timeline.feedback.scheduleRevisionUnavailable,
                ),
          });
        })
        .finally(() => {
          pendingScheduleRefsRef.current.delete(basis.scheduleRef);
          setPendingScheduleRef((current) =>
            current === basis.scheduleRef ? null : current,
          );
        });
    },
    [effectiveZoneId, reviseSchedule, showCanonicalUndo, showScheduleNotice, t],
  );

  const unscheduleCanonicalBasis = useCallback(
    (basis: TimelineCanonicalScheduleBasis) => {
      if (pendingScheduleRefsRef.current.has(basis.scheduleRef)) {
        return;
      }

      pendingScheduleRefsRef.current.add(basis.scheduleRef);
      setPendingScheduleRef(basis.scheduleRef);
      void unscheduleSchedule({
        scheduleRef: basis.scheduleRef,
        expectedPlacementMaterialStateRef: basis.placementMaterialStateRef,
      })
        .then((result) => {
          setDetailState(null);
          setCanonicalUndo({
            kind: 'unschedule',
            scheduleRef: result.scheduleRef,
            unscheduleOperationId: result.unscheduleOperationId,
          });
          showCanonicalUndo(
            t(($) => $.common.home.timeline.feedback.scheduleUndoAvailable),
          );
          showScheduleNotice({
            kind: 'status',
            message: t(
              ($) => $.common.home.timeline.feedback.scheduleUnscheduled,
            ),
          });
        })
        .catch((error: unknown) => {
          const conflict =
            error instanceof TemporalScheduleRemoteError &&
            error.status === 409 &&
            error.code === 'temporal.schedule.unschedule_conflict';
          showScheduleNotice({
            kind: 'error',
            message: conflict
              ? t(
                  ($) =>
                    $.common.home.timeline.feedback.scheduleUnscheduleConflict,
                )
              : t(
                  ($) =>
                    $.common.home.timeline.feedback
                      .scheduleUnscheduleUnavailable,
                ),
          });
        })
        .finally(() => {
          pendingScheduleRefsRef.current.delete(basis.scheduleRef);
          setPendingScheduleRef((current) =>
            current === basis.scheduleRef ? null : current,
          );
        });
    },
    [showCanonicalUndo, showScheduleNotice, t, unscheduleSchedule],
  );

  const undoCanonicalSchedule = useCallback(() => {
    const undo = canonicalUndo;
    if (undo === null || pendingScheduleRefsRef.current.has(undo.scheduleRef)) {
      return;
    }

    pendingScheduleRefsRef.current.add(undo.scheduleRef);
    setPendingScheduleRef(undo.scheduleRef);
    const command =
      undo.kind === 'revision'
        ? reviseSchedule({
            scheduleRef: undo.scheduleRef,
            expectedPlacementMaterialStateRef:
              undo.expectedPlacementMaterialStateRef,
            placement: undo.placement,
          })
        : undoScheduleUnschedule({
            scheduleRef: undo.scheduleRef,
            unscheduleOperationId: undo.unscheduleOperationId,
          });

    void command
      .then(() => {
        setCanonicalUndo(null);
        setToastVisible(false);
        showScheduleNotice({
          kind: 'status',
          message: t(
            ($) => $.common.home.timeline.feedback.scheduleUndoUpdated,
          ),
        });
      })
      .catch((error: unknown) => {
        const conflict =
          error instanceof TemporalScheduleRemoteError &&
          error.status === 409 &&
          (error.code === 'temporal.schedule.revision_conflict' ||
            error.code === 'temporal.schedule.undo_conflict');
        showScheduleNotice({
          kind: 'error',
          message: conflict
            ? t(($) => $.common.home.timeline.feedback.scheduleUndoConflict)
            : t(($) => $.common.home.timeline.feedback.scheduleUndoUnavailable),
        });
      })
      .finally(() => {
        pendingScheduleRefsRef.current.delete(undo.scheduleRef);
        setPendingScheduleRef((current) =>
          current === undo.scheduleRef ? null : current,
        );
      });
  }, [
    canonicalUndo,
    reviseSchedule,
    showScheduleNotice,
    t,
    undoScheduleUnschedule,
  ]);

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

  const createContext = useCallback(
    (label: string, tone: TimelineSemanticTone): TimelineGroup => {
      const result = createTimelineLocalContext(state.groups, label, tone);
      if (result.created) {
        dispatch({ type: 'create-group', group: result.group });
      }
      return result.group;
    },
    [state.groups],
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
      if (scheduleNoticeTimerRef.current !== null) {
        window.clearTimeout(scheduleNoticeTimerRef.current);
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
        groups={visibleGroups}
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
        onReorderGroup={(groupId, targetIndex) => {
          if (prototypeMode) {
            dispatch({ type: 'reorder-group', groupId, targetIndex });
            return;
          }
          const areas = organization.snapshot?.areas;
          const targetGroup = visibleGroups[targetIndex];
          if (!areas || !targetGroup) return;
          const ordered = [...areas].sort((a, b) => a.sortOrder - b.sortOrder);
          const sourceIndex = ordered.findIndex((area) => area.ref === groupId);
          const destinationIndex = ordered.findIndex(
            (area) => area.ref === targetGroup.id,
          );
          if (sourceIndex < 0 || destinationIndex < 0) return;
          const [moved] = ordered.splice(sourceIndex, 1);
          if (!moved) return;
          ordered.splice(destinationIndex, 0, moved);
          void organization.source
            .reorderAreas(ordered)
            .then(organization.refresh)
            .catch(() => {
              organization.refresh();
              showScheduleNotice({
                kind: 'error',
                message: 'Ordine Life Area cambiato: aggiorna e riprova.',
              });
            });
        }}
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
        onCreateContext={createContext}
        onMaterializeCreatedEvent={(dateKey, event) =>
          dispatch({ type: 'materialize-event', dateKey, event })
        }
        onMaterializeCreatedAllDay={(item) =>
          dispatch({ type: 'materialize-all-day', item })
        }
        onRemoveCreatedEvent={(eventId) =>
          dispatch({ type: 'remove-event', eventId })
        }
        onRemoveCreatedAllDay={(itemId) =>
          dispatch({ type: 'remove-all-day', itemId })
        }
        creationEnabled={creationEnabled}
      />

      {!prototypeMode && (
        <TimelineOrganizationPanel
          snapshot={organization.snapshot}
          error={organization.error}
          source={organization.source}
          onRefresh={organization.refresh}
          selectedItem={(() => {
            const focused =
              state.focusedEventId === null
                ? detailState?.event
                : findTimelineEvent(state, state.focusedEventId)?.event;
            const basis = focused?.canonicalBasis;
            return basis?.kind === 'scheduled-event'
              ? ({ kind: 'event', itemRef: basis.eventRef } as const)
              : basis?.kind === 'scheduled-activity'
                ? ({ kind: 'activity', itemRef: basis.activityRef } as const)
                : null;
          })()}
        />
      )}
      <TimelinePostponedEventsPanel
        enabled={!prototypeMode}
        areas={organization.snapshot?.areas ?? []}
      />

      <TimelineCanonicalActionsProvider
        actions={{
          pendingScheduleRef,
          unschedule: unscheduleCanonicalBasis,
        }}
      >
        <TimelineDayStream
          days={renderedDays}
          today={timelineToday}
          nowMinute={timelineNowMinute}
          state={
            presentationFilters === state.filters
              ? state
              : { ...state, filters: presentationFilters }
          }
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
              event,
              allowUnschedule: event.canonicalBasis !== undefined,
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
              event,
              allowUnschedule: false,
              opener,
            })
          }
          onOpenTimeEditor={(dateKey, event, editorAnchor) =>
            setTimeEditor({ dateKey, event, anchor: editorAnchor })
          }
          onMoveEvent={(move) => {
            const current = findTimelineEvent(state, move.eventId)?.event;
            if (current?.canonicalBasis !== undefined) {
              const duration = current.endMinute - current.startMinute;
              reviseCanonicalEvent(
                current,
                move.fromDateKey,
                move.toDateKey,
                move.startMinute,
                move.startMinute + duration,
              );
              return;
            }

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
      </TimelineCanonicalActionsProvider>

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
        onDateSelect={goToDate}
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
            if (timeEditor.event.canonicalBasis !== undefined) {
              reviseCanonicalEvent(
                timeEditor.event,
                timeEditor.dateKey,
                dateKey,
                startMinute,
                endMinute,
              );
              return;
            }

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
        canUnschedule={
          detailState?.allowUnschedule === true &&
          detailState.event.canonicalBasis !== undefined
        }
        pending={
          detailState?.allowUnschedule === true &&
          detailState.event.canonicalBasis !== undefined &&
          pendingScheduleRef === detailState.event.canonicalBasis.scheduleRef
        }
        onUnschedule={() => {
          const basis = detailState?.event.canonicalBasis;
          if (basis !== undefined) {
            unscheduleCanonicalBasis(basis);
          }
        }}
        onClose={() => setDetailState(null)}
      />

      {scheduleNotice ? (
        <div
          className={`temporal-timeline-runtime-status${scheduleNotice.kind === 'error' ? ' temporal-timeline-runtime-status--error' : ''}`}
          role={scheduleNotice.kind === 'error' ? 'alert' : 'status'}
          aria-live={scheduleNotice.kind === 'error' ? undefined : 'polite'}
        >
          {scheduleNotice.message}
        </div>
      ) : null}

      <UndoToast
        visible={
          toastVisible && (state.undo !== null || canonicalUndo !== null)
        }
        message={toastMessage}
        onUndo={() => {
          if (canonicalUndo !== null) {
            undoCanonicalSchedule();
            return;
          }
          preserveRawScroll();
          dispatch({ type: 'undo-last-event-change' });
          setToastVisible(false);
        }}
      />
    </section>
  );
}
