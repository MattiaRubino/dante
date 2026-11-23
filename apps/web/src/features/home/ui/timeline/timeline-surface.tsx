import {
  Temporal,
  detectDeviceTimeZone,
  type PlainDate,
  type PlainDateTime,
} from '@dante/time';
import {
  type CSSProperties,
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

import { formatDateWithCapitalizedMonth } from '../../../../platform/format-localized-date';
import { createPortal } from 'react-dom';

import './timeline.css';

import { TemporalScheduleRemoteError } from '../../../temporal/remote-schedule-data-source';
import type { TemporalSchedulePlacementInput } from '../../../temporal/schedule-data-source';
import {
  createRemoteActivityEditSettings,
  type ActivityEditSettings,
  type ActivityReplanDraft,
} from '../../../temporal/remote-activity-edit-settings';
import { createRemoteActivityInspector } from '../../../temporal/remote-activity-inspector';
import {
  createRemoteTemporalSessionDataSource,
  type TemporalSessionView,
} from '../../../temporal/remote-session-data-source';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import { useTemporalTimelineRuntime } from '../../../temporal/timeline-runtime-boundary';
import {
  addTimelineSecondaryZone,
  normalizeTimelineSecondaryZones,
  readTimelineSecondaryZones,
  saveTimelineSecondaryZones,
  swapTimelinePrimaryZone,
} from '../../../temporal/timeline-view-zone';
import { REVIEW_QUEUE_INVALIDATED } from '../context-rail/review-events';
import { useSessionPanel } from '../../../temporal/use-session-panel';
import { useSessionPanelPresentation } from './timeline-session-panel';
import { TimelineRecurrenceRenewals } from './timeline-recurrence-renewals';
import {
  movedVaultSubjectKey,
  wasMovedToVault,
} from './timeline-vault-move-visibility';
import { applyTimelineSessionReality } from './timeline-session-reality';
import {
  authoritativeDateLaneIdsToReplace,
  useAuthoritativeTimelineHydration,
} from './timeline-authoritative-hydration';
import { createTimelineLocalContext } from './model/timeline-context-catalog';
import {
  TIMELINE_PROTOTYPE_NOW_MINUTE,
  TIMELINE_PROTOTYPE_TODAY,
} from './model/timeline-fixtures';
import { timelineCanonicalRevisionForDisplayEdit } from './model/timeline-canonical-revision';
import { activityReplanForTimelineRevision } from './model/timeline-activity-replan';
import {
  timelineEffectiveScrollBehavior,
  timelinePrefersReducedMotion,
} from './model/timeline-motion';
import {
  TIMELINE_POLICY,
  stepTimelineZoom,
  timelineSupportsExpandedLayout,
} from './model/timeline-policy';
import {
  createInitialTimelineState,
  findTimelineEvent,
  timelineReducer,
} from './model/timeline-state';
import {
  addTimelineDays,
  parseTimelineDate,
  timelineDateKey,
  formatTimelineMinute,
  timelineMinuteOfClock,
} from './model/timeline-temporal';
import type {
  TimelineAllDayItem,
  TimelineEvent,
  TimelineGroup,
  TimelineGroupId,
  TimelineSemanticTone,
} from './model/timeline-types';
import {
  applyTimelineAllDayGeometry,
  projectTimelineDateLaneSessions,
} from './timeline-all-day-runtime';
import { TimelineDayStream } from './timeline-day-stream';
import { TimelineHeader } from './timeline-header';
import { RecurringEditScopeDialog } from './recurring-edit-scope-dialog';
import {
  canonicalOrganizationGroups,
  canonicalItemLifeAreaGroup,
  LEGACY_UNASSIGNED_GROUP,
  TimelineOrganizationPanel,
  useTimelineOrganization,
} from './timeline-organization';
import type { TimelineInspectorClickPoint } from './timeline-inspector-position';
import {
  CalendarPopover,
  EventDetailDialog,
  UndoToast,
  detailFromEvent,
  detailFromSubitem,
  inspectorAppearanceForEvent,
  type TimelineDetail,
} from './timeline-overlays';
import {
  applyTimelineExpansion,
  buildTimelineDayProjectionDays,
  buildTimelineRenderedDays,
  buildTimelineRenderedWeek,
  buildTimelineSessionSourceDays,
  captureTimelineViewportAnchor,
  clampTimelineRuntime,
  findTimelineDayAtOffset,
  parseTimelineViewedDate,
  timelineNowViewportOffset,
  type TimelineRenderedDay,
} from './timeline-viewport-runtime';

type TimelineSurfaceProps = Readonly<{
  sessionPanelEnabled?: boolean;
  expanded: boolean;
  onExpandedChange: (expanded: boolean) => void;
  onExpansionProgress: (progress: number) => void;
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
  onDateNavigation?: ((isoDate: string | undefined) => void) | undefined;
}>;

type TimelineView = 'timeline' | 'day' | 'week';

type ScrollTarget = Readonly<{
  dateKey: string;
  minute: number | null;
  viewportOffset: number | null;
  behavior: ScrollBehavior;
}>;

type DetailState = Readonly<{
  detail: TimelineDetail;
  event: TimelineEvent;
  opener: HTMLElement;
  anchorPoint?: TimelineInspectorClickPoint;
  savedAppearanceColorCode?: string | null;
  openActivityEdit?: boolean;
  activityEditScope?: 'this_and_following';
}>;

type ScheduleNotice = Readonly<{
  kind: 'status' | 'error';
  message: string;
  undo?: boolean;
}>;

type PendingActivityReplan = Readonly<{
  activityRef: string;
  scheduleRef: string;
  title: string;
  settings: ActivityEditSettings;
  draft: ActivityReplanDraft;
  destination?: string;
  restoreDraft?: ActivityReplanDraft;
}> &
  (
    | Readonly<{
        kind: 'drag';
        event: TimelineEvent;
        fromDateKey: string;
        recurring: boolean;
        isUndo?: false;
      }>
    | Readonly<{
        kind: 'undo';
        recurring: boolean;
        isUndo: true;
      }>
  );

type CanonicalScheduleUndo =
  | Readonly<{
      kind: 'activity-replan';
      activityRef: string;
      scheduleRef: string;
      title: string;
      settings: ActivityEditSettings;
      draft: ActivityReplanDraft;
    }>
  | Readonly<{
      kind: 'revision';
      scheduleRef: string;
      expectedPlacementMaterialStateRef: string;
      placement: TemporalSchedulePlacementInput;
    }>;

function formatReplannedPeriod(
  placement: TemporalSchedulePlacementInput,
  zoneId: string,
  locale: string,
): string {
  let start: PlainDateTime;
  let end: PlainDateTime;
  switch (placement.kind) {
    case 'floating-local-interval':
      start = placement.startsLocalAt;
      end = placement.endsLocalAt;
      break;
    case 'named-zone-local-interval':
      start = placement.startsLocalAt
        .toZonedDateTime(placement.zoneId, {
          disambiguation: placement.disambiguation,
        })
        .withTimeZone(zoneId)
        .toPlainDateTime();
      end = placement.endsLocalAt
        .toZonedDateTime(placement.endZoneId ?? placement.zoneId, {
          disambiguation: placement.disambiguation,
        })
        .withTimeZone(zoneId)
        .toPlainDateTime();
      break;
    case 'absolute-interval':
      start = placement.startsAt.toZonedDateTimeISO(zoneId).toPlainDateTime();
      end = placement.endsAt.toZonedDateTimeISO(zoneId).toPlainDateTime();
      break;
    default:
      return '';
  }
  const date = (value: PlainDateTime) =>
    formatDateWithCapitalizedMonth(
      new Intl.DateTimeFormat(locale, {
        day: 'numeric',
        month: 'short',
        timeZone: 'UTC',
      }),
      new Date(Date.UTC(value.year, value.month - 1, value.day, 12)),
    );
  const startTime = formatTimelineMinute(start.hour * 60 + start.minute);
  const endTime = formatTimelineMinute(end.hour * 60 + end.minute);
  return start.toPlainDate().equals(end.toPlainDate())
    ? `${date(start)}, ${startTime}–${endTime}`
    : `${date(start)} ${startTime} – ${date(end)} ${endTime}`;
}

export function TimelineSurface({
  sessionPanelEnabled = import.meta.env.MODE !== 'test',
  expanded,
  onExpandedChange,
  onExpansionProgress,
  viewedDateIso,
  onViewedDateChange,
  onDateNavigation,
}: TimelineSurfaceProps) {
  const { t, i18n } = useTranslation('common');
  const [activityEditSource] = useState(createRemoteActivityEditSettings);
  const [activityImpactSource] = useState(createRemoteActivityInspector);
  const [recurringEditSource] = useState(createRemoteRecurringProfileEdit);
  const [pendingActivityReplan, setPendingActivityReplan] =
    useState<PendingActivityReplan | null>(null);
  const {
    state: temporalRuntimeState,
    reviseSchedule,
    viewZoneId,
    setViewZoneId,
  } = useTemporalTimelineRuntime();
  const effectiveZoneId =
    temporalRuntimeState.status === 'ready'
      ? temporalRuntimeState.effectiveZoneId
      : null;
  const locale = i18n.resolvedLanguage ?? i18n.language;
  const prototypeMode = import.meta.env.MODE === 'test';
  const clockZone = viewZoneId ?? effectiveZoneId ?? detectDeviceTimeZone();
  const [secondaryZones, setSecondaryZones] = useState<readonly string[]>(
    () => readTimelineSecondaryZones(clockZone),
  );
  const visibleSecondaryZones = useMemo(
    () => normalizeTimelineSecondaryZones(clockZone, secondaryZones),
    [clockZone, secondaryZones],
  );
  const commitSecondaryZones = (next: readonly string[]) => {
    saveTimelineSecondaryZones(next);
    setSecondaryZones(next);
  };
  const now = Temporal.Now.zonedDateTimeISO(clockZone);
  const timelineToday = prototypeMode
    ? TIMELINE_PROTOTYPE_TODAY
    : now.toPlainDate();
  const timelineNowMinute = prototypeMode
    ? TIMELINE_PROTOTYPE_NOW_MINUTE
    : timelineMinuteOfClock(now);
  const initialDate = parseTimelineViewedDate(viewedDateIso) ?? timelineToday;
  const initialDateRef = useRef(initialDate);
  const externalViewedDateRef = useRef(viewedDateIso);
  const [state, dispatch] = useReducer(
    timelineReducer,
    timelineToday,
    (today) => createInitialTimelineState(today, prototypeMode),
  );
  const organization = useTimelineOrganization(!prototypeMode);
  const refreshOrganization = organization.refresh;
  const readyRuntimeWindow =
    temporalRuntimeState.status === 'ready'
      ? temporalRuntimeState.window
      : null;
  useEffect(() => {
    if (prototypeMode || readyRuntimeWindow === null) {
      return;
    }
    // Timeline checkpointing may materialize recurring Activity instances and
    // their Life Area assignments. Refresh organization only after that read
    // completed so group/color projection cannot race ahead of canonical truth.
    refreshOrganization();
  }, [refreshOrganization, prototypeMode, readyRuntimeWindow]);
  const canonicalGroups = useMemo(() => {
    if (organization.snapshot === null) return null;
    const groups = canonicalOrganizationGroups(organization.snapshot);
    // An individual Event instance may remove the inherited Life Area even
    // while every source object remains assigned. Keep an unassigned group
    // available for that explicitly detached occurrence.
    const localUnassigned =
      readyRuntimeWindow?.kind === 'window' &&
      readyRuntimeWindow.items.some(
        (item) =>
          (((item.kind === 'scheduled_occurrence' ||
            item.kind === 'expected_occurrence') &&
            item.sourceKind === 'event') ||
            item.kind === 'scheduled_event') &&
          ((item.lifeAreaOverridePresent === true &&
            item.lifeAreaOverrideRef === null) ||
            (item.lifeAreaOverridePresent !== true &&
              item.seriesLifeAreaPresent === true &&
              item.seriesLifeAreaRef === null)),
      );
    return localUnassigned &&
      !groups.some((group) => group.id === LEGACY_UNASSIGNED_GROUP)
      ? [
          ...groups,
          {
            id: LEGACY_UNASSIGNED_GROUP,
            label: 'Senza Area',
            tone: 'personal' as const,
          },
        ]
      : groups;
  }, [organization.snapshot, readyRuntimeWindow]);
  const creationEnabled = prototypeMode || organization.snapshot !== null;
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
  const organizationKeyForItem = useCallback(
    (item: import('../../../temporal/timeline-read').TemporalTimelineItem) =>
      item.kind === 'scheduled_activity'
        ? `activity:${item.activityRef}`
        : item.kind === 'scheduled_event'
          ? `event:${item.eventRef}`
          : `${item.sourceKind}:${item.sourceNativeRef}`,
    [],
  );
  const resolveGroupId = useCallback(
    (item: import('../../../temporal/timeline-read').TemporalTimelineItem) =>
      canonicalItemLifeAreaGroup(item, assignmentBySubject),
    [assignmentBySubject],
  );
  const resolveAppearanceColorCode = useCallback(
    (item: import('../../../temporal/timeline-read').TemporalTimelineItem) => {
      const groupId = resolveGroupId(item);
      const group = canonicalGroups?.find(
        (candidate) => candidate.id === groupId,
      );
      if (!group) return null;
      if (groupId === LEGACY_UNASSIGNED_GROUP) {
        if (
          (((item.kind === 'scheduled_occurrence' ||
            item.kind === 'expected_occurrence') &&
            item.sourceKind === 'event') ||
            item.kind === 'scheduled_event') &&
          item.lifeAreaOverridePresent &&
          item.lifeAreaOverrideRef === null
        ) {
          return null; // never reuse the removed source area's color
        }
        return group.itemColorCodes?.[organizationKeyForItem(item)] ?? null;
      }
      return group.colorCode ?? null;
    },
    [canonicalGroups, organizationKeyForItem, resolveGroupId],
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
  const [timelineView, setTimelineView] = useState<TimelineView>('timeline');
  // Date-lane expansion is view state, never a Schedule mutation. Both the
  // painted rows and the calendar's time mapper read exactly this Set.
  const [expandedDateLaneKeys, setExpandedDateLaneKeys] = useState<
    ReadonlySet<string>
  >(() => new Set());
  const [realityClock, setRealityClock] = useState(() => Date.now());
  const sessionPanel = useSessionPanel(
    sessionPanelEnabled,
    timelineDateKey(viewDate),
    clockZone,
    timelineView === 'week',
  );
  const sessionPresentation = useSessionPanelPresentation(sessionPanel);
  const openRealityCount =
    sessionPanel.snapshot?.visuals?.filter((visual) => visual.ended_at === null)
      .length ?? 0;
  useEffect(() => {
    // Keep the now ruler at the actual instant, including seconds. A stopped
    // Session can otherwise appear below a minute-rounded 19:31 marker.
    const interval = window.setInterval(
      () => setRealityClock(Date.now()),
      openRealityCount > 0 ? 15_000 : 60_000,
    );
    return () => window.clearInterval(interval);
  }, [openRealityCount]);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [detailState, setDetailState] = useState<DetailState | null>(null);
  // Confirmed hard moves must not briefly resurrect from an older Timeline
  // window or lose their Life Area colour before being removed.
  const movedVaultSubjectsRef = useRef<Set<string>>(new Set());
  const inspectorAppearance = useMemo(() => {
    if (!detailState) return undefined;
    const liveEvent = findTimelineEvent(state, detailState.event.id)?.event;
    const allDayItem = liveEvent
      ? null
      : state.allDayItems.find((item) => item.id === detailState.event.id);
    const currentEvent = allDayItem
      ? (() => {
          const { appearanceColorCode: _previous, ...original } =
            detailState.event;
          void _previous;
          return {
            ...original,
            groupId: allDayItem.groupId,
            ...(allDayItem.appearanceColorCode
              ? { appearanceColorCode: allDayItem.appearanceColorCode }
              : {}),
          };
        })()
      : (liveEvent ?? detailState.event);
    const appearance = inspectorAppearanceForEvent(currentEvent, state.groups);
    // An Activity profile save can precede the refreshed all-day projection.
    if (
      appearance.groupLabel === 'Senza Area' &&
      detailState.savedAppearanceColorCode !== undefined
    ) {
      return {
        ...appearance,
        accentColorCode: detailState.savedAppearanceColorCode,
      };
    }
    return appearance;
  }, [detailState, state.allDayItems, state.eventsByDate, state.groups]);
  useEffect(() => {
    if (!detailState || detailState.savedAppearanceColorCode === undefined) {
      return;
    }
    const liveEvent = findTimelineEvent(state, detailState.event.id)?.event;
    const allDayItem = state.allDayItems.find(
      (item) => item.id === detailState.event.id,
    );
    const projectedColor =
      liveEvent?.appearanceColorCode ?? allDayItem?.appearanceColorCode ?? null;
    if (
      inspectorAppearance?.groupLabel === 'Senza Area' &&
      projectedColor !== detailState.savedAppearanceColorCode
    ) {
      return;
    }
    setDetailState((current) => {
      if (
        !current ||
        current.event.id !== detailState.event.id ||
        current.savedAppearanceColorCode !==
          detailState.savedAppearanceColorCode
      ) {
        return current;
      }
      const { savedAppearanceColorCode: _matched, ...fresh } = current;
      void _matched;
      return fresh;
    });
  }, [detailState, inspectorAppearance, state.allDayItems, state.eventsByDate]);
  const [nowNeeded, setNowNeeded] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastVisible, setToastVisible] = useState(false);
  const [scheduleNotice, setScheduleNotice] = useState<ScheduleNotice | null>(
    null,
  );
  const [canonicalUndo, setCanonicalUndo] =
    useState<CanonicalScheduleUndo | null>(null);

  const rootRef = useRef<HTMLElement | null>(null);
  const gridRef = useRef<HTMLDivElement | null>(null);
  const groupScrollerRef = useRef<HTMLDivElement | null>(null);
  const calendarTriggerRef = useRef<HTMLButtonElement | null>(null);
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
  const cardContentHeightsRef = useRef<ReadonlyMap<string, number>>(new Map());
  const [cardContentHeights, setCardContentHeights] =
    useState<ReadonlyMap<string, number>>(cardContentHeightsRef.current);
  const dragActiveRef = useRef(false);
  const [dragSnapshot, setDragSnapshot] = useState<{
    days: readonly TimelineRenderedDay[];
    nowMinute: number;
  } | null>(null);
  const pendingScrollTargetRef = useRef<ScrollTarget | null>(null);
  const initialScrollDoneRef = useRef(false);
  const initialViewPublishedRef = useRef(false);
  const windowTransitionRef = useRef(false);
  const lastScrollTopRef = useRef<number | null>(null);
  const scrollFrameRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);
  const scheduleNoticeTimerRef = useRef<number | null>(null);
  const pendingScheduleRefsRef = useRef(new Set<string>());

  const preserveViewportTime = useCallback(() => {
    const grid = gridRef.current;
    if (
      !grid ||
      dragActiveRef.current ||
      !initialScrollDoneRef.current ||
      pendingScrollTargetRef.current !== null ||
      windowTransitionRef.current
    ) {
      return;
    }
    const anchor = captureTimelineViewportAnchor(
      renderedDaysRef.current,
      grid.scrollTop,
      grid.clientHeight * TIMELINE_POLICY.viewport.contextProbeRatio,
    );
    if (anchor) {
      pendingScrollTargetRef.current = { ...anchor, behavior: 'auto' };
    }
  }, []);

  const onCardContentHeight = useCallback(
    (eventId: string, height: number) => {
      const measured = Math.ceil(height);
      if (!Number.isFinite(measured)) return;
      const floor = TIMELINE_POLICY.event.activityMinimumHeightPx;
      const current = cardContentHeightsRef.current.get(eventId);
      if (
        current === measured ||
        (measured <= floor && current === undefined)
      ) {
        return;
      }
      preserveViewportTime();
      const next = new Map(cardContentHeightsRef.current);
      if (measured > floor) next.set(eventId, measured);
      else next.delete(eventId);
      cardContentHeightsRef.current = next;
      setCardContentHeights(next);
    },
    [preserveViewportTime],
  );

  const reconcileAuthoritativeEvents = useCallback(
    (
      projections: readonly Readonly<{
        dateKey: string;
        event: TimelineEvent;
      }>[],
    ) => {
      preserveViewportTime();
      dispatch({
        type: 'reconcile-authoritative-events',
        projections: projections.filter(
          ({ event }) =>
            !wasMovedToVault(event.canonicalBasis, movedVaultSubjectsRef.current),
        ),
      });
    },
    [preserveViewportTime],
  );
  const reconcileAuthoritativeDateLane = useCallback(
    (items: readonly TimelineAllDayItem[]) => {
      const visibleItems = items.filter(
        (item) =>
          !wasMovedToVault(item.canonicalBasis, movedVaultSubjectsRef.current),
      );
      for (const itemId of authoritativeDateLaneIdsToReplace(
        state.allDayItems,
        visibleItems,
      )) {
        dispatch({ type: 'remove-all-day', itemId });
      }
      for (const item of visibleItems) {
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
    prototypeMode
      ? undefined
      : organization.snapshot === null
        ? null
        : resolveAppearanceColorCode,
  );

  const dateLaneActivityRefs = useMemo(() => {
    const timedActivities = new Set<string>();
    for (const events of Object.values(state.eventsByDate)) {
      for (const event of events) {
        const basis = event.canonicalBasis;
        if (basis?.kind !== 'scheduled-activity') continue;
        timedActivities.add(basis.activityRef);
      }
    }
    return [
      ...new Set([
        ...state.allDayItems.flatMap((item) =>
          item.canonicalBasis?.kind === 'scheduled-activity'
            ? [item.canonicalBasis.activityRef]
            : [],
        ),
        ...timedActivities,
      ]),
    ].sort();
  }, [state.allDayItems, state.eventsByDate]);
  const dateLaneActivityKey = dateLaneActivityRefs.join('|');
  const dateLaneSessionSource = useMemo(
    () => createRemoteTemporalSessionDataSource(),
    [],
  );
  const [dateLaneSessions, setDateLaneSessions] = useState<
    ReadonlyMap<string, readonly TemporalSessionView[]>
  >(new Map());
  const [dateLaneSessionRevision, setDateLaneSessionRevision] = useState(0);
  useEffect(() => {
    if (prototypeMode) return;
    const refresh = () =>
      setDateLaneSessionRevision((revision) => revision + 1);
    window.addEventListener('dante:session-changed', refresh);
    return () => window.removeEventListener('dante:session-changed', refresh);
  }, [prototypeMode]);
  useEffect(() => {
    if (prototypeMode || !dateLaneActivityKey) return;
    let cancelled = false;
    void Promise.all(
      dateLaneActivityRefs.map(async (activityRef) => {
        try {
          return [
            activityRef,
            await dateLaneSessionSource.list('activity', activityRef),
          ] as const;
        } catch {
          return null;
        }
      }),
    ).then((entries) => {
      if (!cancelled)
        setDateLaneSessions(new Map(entries.filter((entry) => entry !== null)));
    });
    return () => {
      cancelled = true;
    };
  }, [
    dateLaneActivityKey,
    dateLaneActivityRefs,
    dateLaneSessionRevision,
    dateLaneSessionSource,
    prototypeMode,
  ]);
  const projectedDateLaneItems = useMemo(
    () =>
      projectTimelineDateLaneSessions(
        state.allDayItems,
        dateLaneSessions,
        clockZone,
      ),
    [state.allDayItems, dateLaneSessions, clockZone],
  );

  const renderedDayInputs = useMemo(
    () => ({
      eventsByDate: state.eventsByDate,
      groups: visibleGroups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
      cardContentHeights,
    }),
    [
      cardContentHeights,
      state.eventsByDate,
      state.expandedEventIds,
      visibleGroups,
      state.zoom,
    ],
  );
  const baseRenderedDays = useMemo(
    () =>
      timelineView === 'week'
        ? buildTimelineRenderedWeek(viewDate, renderedDayInputs)
        : timelineView === 'day'
          ? buildTimelineDayProjectionDays(
              viewDate,
              renderedDayInputs,
              sessionPanel.snapshot?.visuals ?? [],
              clockZone,
            )
          : buildTimelineRenderedDays(
              anchor,
              TIMELINE_POLICY.window.pastBufferDays,
              TIMELINE_POLICY.window.futureBufferDays,
              renderedDayInputs,
            ),
    [
      anchor,
      clockZone,
      renderedDayInputs,
      sessionPanel.snapshot?.visuals,
      timelineView,
      viewDate,
    ],
  );
  const renderedDays = useMemo(() => {
    const sourceDays = buildTimelineSessionSourceDays(
      baseRenderedDays,
      renderedDayInputs,
      [
        ...(sessionPanel.snapshot?.visuals ?? []),
        ...[...dateLaneSessions].flatMap(([activityRef, sessions]) =>
          sessions.map((session) => ({
            activity_ref: activityRef,
            planned_schedule_ref: session.plannedScheduleRef ?? null,
            started_at: session.startedAt,
          })),
        ),
      ],
      clockZone,
    );
    const projected = applyTimelineSessionReality(
      applyTimelineAllDayGeometry(
        baseRenderedDays,
        projectedDateLaneItems,
        presentationFilters,
        timelineView === 'week',
        expandedDateLaneKeys,
      ),
      sessionPanel.snapshot?.visuals ?? [],
      clockZone,
      sessionPanel.snapshot?.evaluated_at ??
        new Date(realityClock).toISOString(),
      sessionPanel.snapshot
        ? Date.parse(sessionPanel.snapshot.evaluated_at) +
            Math.max(
              0,
              realityClock -
                (sessionPanel.snapshot.clientReceivedAt ?? realityClock),
            )
        : realityClock,
      visibleGroups,
      state.zoom,
      state.expandedEventIds,
      dateLaneSessions,
      sourceDays,
    );
    return timelineView === 'day'
      ? projected
          .filter((day) => day.dateKey === timelineDateKey(viewDate))
          .map((day) => ({ ...day, offsetTop: 0 }))
      : projected;
  }, [
    baseRenderedDays,
    renderedDayInputs,
    projectedDateLaneItems,
    presentationFilters,
    timelineView,
    expandedDateLaneKeys,
    viewDate,
    sessionPanel.snapshot,
    dateLaneSessions,
    clockZone,
    realityClock,
    visibleGroups,
    state.zoom,
    state.expandedEventIds,
  ]);

  const visibleRenderedDays = dragSnapshot?.days ?? renderedDays;
  const visibleNowMinute = dragSnapshot?.nowMinute ?? timelineNowMinute;

  useLayoutEffect(() => {
    // Also refresh after the snapshot is released: renderedDays may have
    // updated while dragging without changing again on pointerup.
    if (!dragActiveRef.current) renderedDaysRef.current = renderedDays;
  }, [renderedDays, dragSnapshot]);

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

  const applyActivityTimelineReplan = useCallback(
    (proposal: PendingActivityReplan) => {
      void activityEditSource
        .applyReplan(
          proposal.activityRef,
          proposal.settings,
          proposal.draft,
          crypto.randomUUID(),
        )
        .then((saved) => {
          window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
          setToastVisible(false);
          if (!proposal.isUndo && proposal.restoreDraft) {
            setCanonicalUndo({
              kind: 'activity-replan',
              activityRef: proposal.activityRef,
              scheduleRef: proposal.scheduleRef,
              title: proposal.title,
              settings: saved,
              draft: proposal.restoreDraft,
            });
          } else {
            setCanonicalUndo(null);
          }
          showScheduleNotice({
            kind: 'status',
            message: proposal.isUndo
              ? t(($) => $.common.home.timeline.feedback.scheduleUndoUpdated)
              : `${t(($) => $.common.home.timeline.feedback.activityRescheduled)} ${proposal.destination ?? ''}`.trim(),
            undo: !proposal.isUndo && proposal.restoreDraft !== undefined,
          });
        })
        .catch((reason: unknown) => {
          showScheduleNotice({
            kind: 'error',
            message:
              reason instanceof Error
                ? reason.message
                : 'Impossibile spostare l’attività. Ricarica e riprova.',
            undo: proposal.isUndo === true,
          });
        })
        .finally(() => {
          pendingScheduleRefsRef.current.delete(proposal.scheduleRef);
        });
    },
    [activityEditSource, showScheduleNotice, t],
  );

  const confirmActivityTimelineReplan = () => {
    const proposal = pendingActivityReplan;
    if (proposal === null) return;
    setPendingActivityReplan(null);
    applyActivityTimelineReplan(proposal);
  };

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

      if (basis.kind === 'scheduled-activity') {
        pendingScheduleRefsRef.current.add(basis.scheduleRef);

        void Promise.all([
          activityEditSource.load(basis.activityRef),
          activityImpactSource.sessionImpact(basis.activityRef),
          recurringEditSource.loadActivityContext(basis.activityRef),
        ])
          .then(([settings, impact, recurringContext]) => {
            if (impact.attempts.length > 0) {
              const opener =
                rootRef.current?.querySelector<HTMLElement>(
                  `[data-timeline-event="${event.id}"]`,
                ) ?? rootRef.current;
              if (opener) {
                setDetailState({
                  event,
                  detail: detailFromEvent(event, state.groups, fromDateKey),
                  opener,
                  openActivityEdit: true,
                });
              }
              // The gesture is complete: keeping this ref pending would make
              // every later drag of the same card a silent no-op until reload.
              pendingScheduleRefsRef.current.delete(basis.scheduleRef);
              return;
            }
            // Crossing the pointer-drag threshold within the same snapped
            // slot is still an attempt when recordings exist, but it must
            // never submit a no-op replan for an unrecorded Activity.
            if (
              fromDateKey === toDateKey &&
              event.startMinute === startMinute &&
              event.endMinute === endMinute
            ) {
              pendingScheduleRefsRef.current.delete(basis.scheduleRef);
              return;
            }
            if (basis.placementLocked) {
              throw new Error(
                'Sblocca gli spostamenti prima di modificare l’orario.',
              );
            }
            const draft = activityReplanForTimelineRevision(
              settings,
              basis,
              revision,
            );
            if (draft === null) {
              throw new Error(
                'Questo orario richiede Modifica dell’attività o intervalli non sovrapposti.',
              );
            }
            const proposal: PendingActivityReplan = {
              kind: 'drag',
              event,
              fromDateKey,
              activityRef: basis.activityRef,
              scheduleRef: basis.scheduleRef,
              title: event.title,
              settings,
              draft,
              recurring: recurringContext !== null,
              destination: formatReplannedPeriod(
                revision.next,
                effectiveZoneId,
                locale,
              ),
              restoreDraft: {
                times: Object.fromEntries(
                  settings.schedules
                    .filter((row) =>
                      settings.schedules.some(
                        (item) => item.role === 'interval',
                      )
                        ? row.role === 'interval'
                        : row.role === 'envelope',
                    )
                    .map((row) => [
                      row.scheduleRef,
                      { start: row.start!, end: row.end! },
                    ]),
                ),
                removedIntervals: [],
                newIntervals: [],
                removedPlanned: [],
                deletedPlanned: [],
                newPlanned: [],
              },
            };
            if (recurringContext !== null) {
              setPendingActivityReplan(proposal);
            } else {
              applyActivityTimelineReplan(proposal);
            }
          })
          .catch((reason: unknown) => {
            showScheduleNotice({
              kind: 'error',
              message:
                reason instanceof Error
                  ? reason.message
                  : 'Impossibile leggere l’attività. Riprova.',
            });
            pendingScheduleRefsRef.current.delete(basis.scheduleRef);
          });
        return;
      }

      pendingScheduleRefsRef.current.add(basis.scheduleRef);

      void reviseSchedule({
        scheduleRef: basis.scheduleRef,
        expectedPlacementMaterialStateRef: basis.placementMaterialStateRef,
        placement: revision.next,
      })
        .then((result) => {
          window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
          setToastVisible(false);
          setCanonicalUndo({
            kind: 'revision',
            scheduleRef: result.scheduleRef,
            expectedPlacementMaterialStateRef: result.placementMaterialStateRef,
            placement: revision.previous,
          });
          showScheduleNotice({
            kind: 'status',
            message: `${t(($) => $.common.home.timeline.feedback.eventRescheduled)} ${formatReplannedPeriod(revision.next, effectiveZoneId, locale)}`,
            undo: true,
          });
        })
        .catch((error: unknown) => {
          const intervalConflict =
            error instanceof TemporalScheduleRemoteError &&
            error.code ===
              'temporal.schedule.activity_interval_requires_replan';
          const locked =
            error instanceof TemporalScheduleRemoteError &&
            error.code === 'temporal.schedule.placement_locked';
          const conflict =
            error instanceof TemporalScheduleRemoteError &&
            error.status === 409 &&
            error.code === 'temporal.schedule.revision_conflict';
          showScheduleNotice({
            kind: 'error',
            message: locked
              ? i18n.language.startsWith('it')
                ? 'Sblocca gli spostamenti prima di modificare l’orario.'
                : 'Unlock placement before changing the time.'
              : intervalConflict
                ? i18n.language.startsWith('it')
                  ? 'Apri Modifica per gestire le registrazioni prima di cambiare il periodo.'
                  : 'Open Edit to manage recordings before changing the period.'
                : conflict
                  ? t(
                      ($) =>
                        $.common.home.timeline.feedback
                          .scheduleRevisionConflict,
                    )
                  : t(
                      ($) =>
                        $.common.home.timeline.feedback
                          .scheduleRevisionUnavailable,
                    ),
          });
        })
        .finally(() => {
          pendingScheduleRefsRef.current.delete(basis.scheduleRef);
        });
    },
    [
      activityEditSource,
      activityImpactSource,
      applyActivityTimelineReplan,
      recurringEditSource,
      effectiveZoneId,
      i18n,
      reviseSchedule,
      showScheduleNotice,
      locale,
      state.groups,
      t,
    ],
  );

  const undoCanonicalSchedule = useCallback(() => {
    const undo = canonicalUndo;
    if (undo === null || pendingScheduleRefsRef.current.has(undo.scheduleRef)) {
      return;
    }

    if (undo.kind === 'activity-replan') {
      pendingScheduleRefsRef.current.add(undo.scheduleRef);

      void Promise.all([
        activityImpactSource.sessionImpact(undo.activityRef),
        recurringEditSource.loadActivityContext(undo.activityRef),
      ])
        .then(([impact, recurringContext]) => {
          const proposal: PendingActivityReplan = {
            kind: 'undo',
            activityRef: undo.activityRef,
            scheduleRef: undo.scheduleRef,
            title: undo.title,
            settings: undo.settings,
            draft: undo.draft,
            recurring: recurringContext !== null,
            isUndo: true,
          };
          if (impact.attempts.length > 0) {
            showScheduleNotice({
              kind: 'error',
              message:
                'Questa attività contiene registrazioni: apri Modifica per gestirle prima di annullare lo spostamento.',
            });
            pendingScheduleRefsRef.current.delete(undo.scheduleRef);
          } else if (recurringContext !== null) {
            setPendingActivityReplan(proposal);
          } else {
            applyActivityTimelineReplan(proposal);
          }
        })
        .catch((reason: unknown) => {
          showScheduleNotice({
            kind: 'error',
            message:
              reason instanceof Error
                ? reason.message
                : 'Impossibile verificare le Sessioni. Riprova.',
          });
          pendingScheduleRefsRef.current.delete(undo.scheduleRef);
        });
      return;
    }

    pendingScheduleRefsRef.current.add(undo.scheduleRef);

    const command = reviseSchedule({
      scheduleRef: undo.scheduleRef,
      expectedPlacementMaterialStateRef: undo.expectedPlacementMaterialStateRef,
      placement: undo.placement,
    });

    void command
      .then(() => {
        window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
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
          undo: true,
        });
      })
      .finally(() => {
        pendingScheduleRefsRef.current.delete(undo.scheduleRef);
      });
  }, [
    activityImpactSource,
    applyActivityTimelineReplan,
    recurringEditSource,
    canonicalUndo,
    reviseSchedule,
    showScheduleNotice,
    t,
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
        visibleGroups.length,
        normalizedProgress,
      );
    },
    [onExpansionProgress, visibleGroups.length],
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

  useEffect(() => {
    const onFirstPlay = () => goNow();
    window.addEventListener('dante:session-started', onFirstPlay);
    return () =>
      window.removeEventListener('dante:session-started', onFirstPlay);
  }, [goNow]);

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
      if (
        timelineView === 'timeline' &&
        viewed &&
        !viewed.date.equals(viewDate)
      ) {
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
    [
      publishViewportDate,
      timelineNowMinute,
      timelineToday,
      viewDate,
      timelineView,
    ],
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

      // Keep native auto-scroll working but don't recycle timeline days
      // under the dragged card when it crosses the live now marker.
      if (dragActiveRef.current || timelineView !== 'timeline') return;

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
    [expanded, synchronizeViewportContext, timelineView],
  );

  const zoomAt = useCallback(
    (clientY: number, factor: number) => {
      const nextZoom = stepTimelineZoom(state.zoom, factor);
      if (nextZoom === state.zoom) return;
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
      dispatch({ type: 'set-zoom', zoom: nextZoom });
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

  const closeCalendar = useCallback((restoreFocus = true) => {
    setCalendarOpen(false);
    if (restoreFocus) {
      requestAnimationFrame(() => calendarTriggerRef.current?.focus());
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
    // Scrolling changes viewDate locally. Only a changed route prop is an
    // external navigation request; otherwise this effect pulls the viewport
    // back to the previous date on every upward/downward scroll.
    if (externalViewedDateRef.current === viewedDateIso) return;
    externalViewedDateRef.current = viewedDateIso;
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
    if (!grid || dragActiveRef.current) {
      // The clock and Session projections may refresh every 15 seconds.
      // Do not re-anchor the viewport or recalculate expansion mid-drag.
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
      visibleGroups.length,
      expansionProgressRef.current,
    );
  }, [
    renderedDays,
    scrollToRenderedDay,
    visibleGroups.length,
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
      data-timeline-view={timelineView}
      data-home-region="timeline"
      data-home-timeline-state={expanded ? 'expanded' : 'normal'}
      data-timeline-card-dragging={dragSnapshot === null ? 'false' : 'true'}
      style={{
        '--dante-timeline-extra-ruler-width':
          String(visibleSecondaryZones.length * 84) + 'px',
      } as CSSProperties}
      aria-label={t(($) => $.common.home.timeline.label)}
    >
      <TimelineHeader
        sessionPanelToggle={sessionPresentation.control}
        locale={locale}
        today={timelineToday}
        viewDate={viewDate}
        effectiveZoneId={clockZone}
        selectedViewZoneId={viewZoneId}
        secondaryZoneIds={visibleSecondaryZones}
        onAddSecondaryZone={(zoneId) => {
          commitSecondaryZones(addTimelineSecondaryZone(
            clockZone, visibleSecondaryZones, zoneId,
          ));
        }}
        onRemoveSecondaryZone={(zoneId) => {
          commitSecondaryZones(visibleSecondaryZones.filter(
            (secondary) => secondary !== zoneId,
          ));
        }}
        onReorderSecondaryZones={() => {
          if (visibleSecondaryZones.length === 2) {
            commitSecondaryZones([...visibleSecondaryZones].reverse());
          }
        }}
        onViewZoneChange={(nextZone) => {
          if (nextZone === viewZoneId) return;
          // Preserve the observed INSTANT, not the old local hour,
          // when the currently viewed Timeline crosses a timezone boundary.
          const grid = gridRef.current;
          const anchor = grid && captureTimelineViewportAnchor(
            renderedDaysRef.current,
            grid.scrollTop,
            grid.clientHeight * TIMELINE_POLICY.viewport.contextProbeRatio,
          );
          const zone = nextZone ?? detectDeviceTimeZone();
          if (anchor) {
            const boundedMinute = Math.min(
              1439, Math.max(0, Math.floor(anchor.minute)),
            );
            const originalLocal = Temporal.PlainDateTime.from(
              `${anchor.dateKey}T${String(Math.floor(boundedMinute / 60)).padStart(2, '0')}:${String(boundedMinute % 60).padStart(2, '0')}`,
            );
            const shifted = originalLocal.toZonedDateTime(
              clockZone, { disambiguation: 'compatible' },
            ).withTimeZone(zone);
            const newDate = shifted.toPlainDate();
            pendingScrollTargetRef.current = {
              dateKey: newDate.toString(),
              minute: shifted.hour * 60 + shifted.minute,
              viewportOffset: anchor.viewportOffset,
              behavior: 'auto',
            };
            setAnchor(newDate);
            setViewDate(newDate);
            publishViewportDate(newDate);
          }
          commitSecondaryZones(swapTimelinePrimaryZone(
            clockZone, zone, visibleSecondaryZones,
          ));
          setViewZoneId(nextZone);
        }}
        timelineView={timelineView}
        onTimelineViewChange={(nextView) => {
          if (nextView === timelineView) return;
          setTimelineView(nextView);
          setViewDate(timelineToday);
          setAnchor(timelineToday);
          publishViewportDate(timelineToday);
          onDateNavigation?.(undefined);
          pendingScrollTargetRef.current = {
            dateKey: timelineDateKey(timelineToday),
            minute: timelineNowMinute,
            viewportOffset: timelineNowViewportOffset(
              gridRef.current?.clientHeight ??
                TIMELINE_POLICY.viewport.defaultGridHeightPx,
            ),
            behavior: 'auto',
          };
        }}
        groups={visibleGroups}
        filters={state.filters}
        nowNeeded={nowNeeded}
        split={expanded}
        calendarOpen={calendarOpen}
        calendarTriggerRef={calendarTriggerRef}
        groupScrollerRef={groupScrollerRef}
        onCalendarToggle={() => {
          setCalendarOpen((value) => !value);
        }}
        onDateSelect={(date) => goToDate(date)}
        onGoNow={goNow}
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
                message: 'Ordine delle aree cambiato: aggiorna e riprova.',
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
      {!prototypeMode ? <TimelineRecurrenceRenewals /> : null}
      <div className="timeline-session-panel__edge-host">
        {sessionPresentation.panel}
      </div>

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

      <TimelineDayStream
        days={visibleRenderedDays}
        view={timelineView}
        primaryZoneId={clockZone}
        secondaryZoneIds={visibleSecondaryZones}
        today={timelineToday}
        nowMinute={visibleNowMinute}
        onDragActiveChange={(active) => {
          if (active === dragActiveRef.current) return;
          dragActiveRef.current = active;
          if (active) {
            setDragSnapshot({
              days: renderedDaysRef.current,
              nowMinute: timelineNowMinute,
            });
          } else {
            setDragSnapshot(null);
          }
        }}
        onCardContentHeight={onCardContentHeight}
        state={{
          ...state,
          allDayItems: projectedDateLaneItems,
          filters: presentationFilters,
        }}
        expanded={expanded}
        gridRef={gridRef}
        onScroll={handleScroll}
        onZoomAt={zoomAt}
        onFocusEvent={(eventId) => dispatch({ type: 'focus-event', eventId })}
        onToggleSubitems={(eventId) => {
          preserveViewportTime();
          dispatch({ type: 'toggle-event-subitems', eventId });
        }}
        onOpenEventDetail={(event, opener) =>
          setDetailState({
            detail: detailFromEvent(
              event,
              state.groups,
              opener.closest<HTMLElement>('[data-timeline-date]')?.dataset
                .timelineDate ?? findTimelineEvent(state, event.id)?.dateKey,
            ),
            event,
            opener,
          })
        }
        expandedDateLaneKeys={expandedDateLaneKeys}
        onExpandedDateLaneChange={(dateKey, isExpanded) => {
          if (dragActiveRef.current) return;
          // This is an explicit user expansion: keep the clicked date strip
          // visible and let timed rows move down. Restoring the previous
          // time anchor here would scroll the newly revealed cards offscreen.
          setExpandedDateLaneKeys((previous) => {
            if (previous.has(dateKey) === isExpanded) return previous;
            const next = new Set(previous);
            if (isExpanded) next.add(dateKey);
            else next.delete(dateKey);
            return next;
          });
        }}
        onOpenDateLaneDetail={(item, opener, anchorPoint) => {
          const event: TimelineEvent = {
            id: item.id,
            title: item.title,
            groupId: item.groupId,
            startMinute: 0,
            endMinute: 1440,
            ...(item.canonicalBasis
              ? { canonicalBasis: item.canonicalBasis }
              : {}),
            ...(item.appearanceColorCode
              ? { appearanceColorCode: item.appearanceColorCode }
              : {}),
          };
          setDetailState({
            detail: detailFromEvent(event, state.groups, item.startDateKey),
            event,
            opener,
            ...(anchorPoint ? { anchorPoint } : {}),
          });
        }}
        onOpenSubitemDetail={(event, subitem, opener) =>
          setDetailState({
            detail: detailFromSubitem(
              event,
              subitem,
              state.groups,
              t(($) => $.common.home.timeline.detail.subitemParent),
              opener.closest<HTMLElement>('[data-timeline-date]')?.dataset
                .timelineDate ?? findTimelineEvent(state, event.id)?.dateKey,
            ),
            event,
            opener,
          })
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
            preserveViewportTime();
          } else {
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
        onDateSelect={goToDate}
        onGoToday={goNow}
      />

      {pendingActivityReplan?.recurring &&
      pendingActivityReplan.kind === 'drag' ? (
        <RecurringEditScopeDialog
          subjectLabel="attività"
          selectedProtection={null}
          dragNotice="Solo questa applica lo spostamento. Per questa e le successive si apre Modifica: gli orari della serie non sono ancora modificabili e il trascinamento non verrà salvato."
          onOnlyThis={confirmActivityTimelineReplan}
          onFollowing={() => {
            const proposal = pendingActivityReplan;
            setPendingActivityReplan(null);
            pendingScheduleRefsRef.current.delete(proposal.scheduleRef);
            const opener =
              rootRef.current?.querySelector<HTMLElement>(
                `[data-timeline-event="${proposal.event.id}"]`,
              ) ?? rootRef.current;
            if (opener) {
              setDetailState({
                event: proposal.event,
                detail: detailFromEvent(
                  proposal.event,
                  state.groups,
                  proposal.fromDateKey,
                ),
                opener,
                openActivityEdit: true,
                activityEditScope: 'this_and_following',
              });
            }
          }}
          onCancel={() => {
            pendingScheduleRefsRef.current.delete(
              pendingActivityReplan.scheduleRef,
            );
            setPendingActivityReplan(null);
          }}
        />
      ) : pendingActivityReplan ? (
        createPortal(
          <div className="timeline-activity-replan-backdrop">
            <div
              className="timeline-activity-replan-dialog"
              role="alertdialog"
              aria-modal="true"
              aria-label="Conferma spostamento attività"
              onKeyDown={(event) => {
                if (event.key === 'Escape') {
                  event.preventDefault();
                  pendingScheduleRefsRef.current.delete(
                    pendingActivityReplan.scheduleRef,
                  );

                  setPendingActivityReplan(null);
                }
              }}
            >
              <h2>{pendingActivityReplan.title}</h2>
              <div className="timeline-activity-replan-dialog__actions">
                <button
                  type="button"
                  autoFocus
                  onClick={confirmActivityTimelineReplan}
                >
                  Solo questa
                </button>
                <button
                  type="button"
                  onClick={() => {
                    pendingScheduleRefsRef.current.delete(
                      pendingActivityReplan.scheduleRef,
                    );

                    setPendingActivityReplan(null);
                  }}
                >
                  Annulla
                </button>
              </div>
            </div>
          </div>,
          document.body,
        )
      ) : null}

      <EventDetailDialog
        detail={detailState?.detail ?? null}
        {...(inspectorAppearance ? { appearance: inspectorAppearance } : {})}
        opener={detailState?.opener ?? null}
        {...(detailState?.anchorPoint
          ? { anchorPoint: detailState.anchorPoint }
          : {})}
        locale={locale}
        timeZone={clockZone}
        sessionSubject={(() => {
          const basis = detailState?.event.canonicalBasis;
          if (basis?.kind === 'scheduled-activity') {
            return { kind: 'activity' as const, ref: basis.activityRef };
          }
          if (basis?.kind === 'scheduled-occurrence') {
            return { kind: 'occurrence' as const, ref: basis.occurrenceRef };
          }
          return null;
        })()}
        responsibilitySubject={(() => {
          const basis = detailState?.event.canonicalBasis;
          if (basis?.kind === 'scheduled-activity') {
            return { kind: 'activity' as const, ref: basis.activityRef };
          }
          if (basis?.kind === 'scheduled-event') {
            return { kind: 'event' as const, ref: basis.eventRef };
          }
          return null;
        })()}
        reminderScheduleRef={(() => {
          const basis = detailState?.event.canonicalBasis;
          if (
            basis?.placement.kind === 'absolute' ||
            basis?.placement.kind === 'named-zone-local'
          ) {
            return basis.scheduleRef;
          }
          return null;
        })()}
        placementLockScheduleRef={(() => {
          const basis = detailState?.event.canonicalBasis;
          return basis?.kind === 'scheduled-activity' ||
            basis?.kind === 'scheduled-event' ||
            (basis?.kind === 'scheduled-occurrence' &&
              basis.sourceKind === 'event')
            ? basis.scheduleRef
            : null;
        })()}
        openActivityEdit={detailState?.openActivityEdit === true}
        initialActivityEditScope={detailState?.activityEditScope}
        onActivitySaved={(profile) => {
          window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
          if (!detailState) return;
          const existing = findTimelineEvent(state, detailState.event.id);
          if (existing) {
            preserveViewportTime();
            const {
              appearanceColorCode: _previousColor,
              ...eventWithoutColor
            } = existing.event;
            void _previousColor;
            dispatch({
              type: 'materialize-event',
              dateKey: existing.dateKey,
              event: {
                ...eventWithoutColor,
                title: profile.title,
                ...(profile.colorCode
                  ? { appearanceColorCode: profile.colorCode }
                  : {}),
              },
            });
          }
          setDetailState(
            (current) => {
              if (!current) return null;
              const { appearanceColorCode: _oldColor, ...event } = current.event;
              void _oldColor;
              return {
                ...current,
                savedAppearanceColorCode: profile.colorCode,
                event: {
                  ...event,
                  title: profile.title,
                  ...(profile.colorCode
                    ? { appearanceColorCode: profile.colorCode }
                    : {}),
                },
                detail: { ...current.detail, title: profile.title },
              };
            },
          );
        }}
        onVaultMoved={(kind, nativeRef) => {
          // Already committed by the backend. Locally remove the card before
          // the datasource invalidation starts reloading organization colours.
          movedVaultSubjectsRef.current.add(
            movedVaultSubjectKey(kind, nativeRef),
          );
          if (detailState) {
            preserveViewportTime();
            dispatch({ type: 'remove-event', eventId: detailState.event.id });
            dispatch({ type: 'remove-all-day', itemId: detailState.event.id });
          }
          setDetailState(null);
          window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
          showScheduleNotice({
            kind: 'status',
            message: 'Spostato nelle Bozze.',
          });
        }}
        onActivityDeleted={() => {
          window.dispatchEvent(new Event(REVIEW_QUEUE_INVALIDATED));
          if (detailState) {
            preserveViewportTime();
            dispatch({ type: 'remove-event', eventId: detailState.event.id });
          }
          setDetailState(null);
          showScheduleNotice({
            kind: 'status',
            message: 'Attività eliminata.',
          });
        }}
        onClose={() => setDetailState(null)}
      />

      {scheduleNotice ? (
        <div
          className={`temporal-timeline-runtime-status${scheduleNotice.kind === 'error' ? ' temporal-timeline-runtime-status--error' : ''}${scheduleNotice.undo ? ' temporal-timeline-runtime-status--with-undo' : ''}`}
          role={scheduleNotice.kind === 'error' ? 'alert' : 'status'}
          aria-live={scheduleNotice.kind === 'error' ? undefined : 'polite'}
        >
          <span>{scheduleNotice.message}</span>
          {scheduleNotice.undo && canonicalUndo !== null ? (
            <button type="button" onClick={undoCanonicalSchedule}>
              {t(($) => $.common.home.timeline.undo)}
            </button>
          ) : null}
        </div>
      ) : null}

      <UndoToast
        visible={toastVisible && state.undo !== null}
        message={toastMessage}
        onUndo={() => {
          preserveViewportTime();
          dispatch({ type: 'undo-last-event-change' });
          setToastVisible(false);
        }}
      />
    </section>
  );
}
