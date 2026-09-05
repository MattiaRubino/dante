import { Temporal, type PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import type { TemporalPlacement } from '../../../temporal';
import {
  TemporalCreateContextCatalogProvider,
  TemporalCreateEntry,
  temporalCreateTimelineProjectionFromEffect,
  type TemporalCreateAppliedEffect,
  type TemporalCreateContextInput,
  type TemporalCreateContextOption,
  type TemporalCreateInvocation,
  type TemporalCreateMutationEffect,
  type TemporalCreateTimelineProjection,
} from '../../../temporal-create';
import { TIMELINE_POLICY } from './model/timeline-policy';
import type {
  TimelineAllDayItem,
  TimelineEvent,
  TimelineGroup,
  TimelineGroupId,
  TimelineSemanticTone,
} from './model/timeline-types';
import {
  TimelinePlanningTray,
  type TimelinePlanningTrayItem,
} from './timeline-planning-tray';

import './timeline-create-bridge.css';

type TimelineCreateBridgeProps = Readonly<{
  defaultDate: PlainDate;
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
  onRevealDate: (date: PlainDate) => void;
  onCreateContext: (label: string, tone: TimelineSemanticTone) => TimelineGroup;
  onMaterializeCreatedEvent: (dateKey: string, event: TimelineEvent) => void;
  onMaterializeCreatedAllDay: (item: TimelineAllDayItem) => void;
  onRemoveCreatedEvent: (eventId: TimelineEvent['id']) => void;
  onRemoveCreatedAllDay: (itemId: string) => void;
  onBeforeOpen?: () => void;
}>;

type PortalTarget = Readonly<{
  projection: TemporalCreateTimelineProjection;
  host: Element;
  style: CSSProperties;
  tone: string;
}>;

type RangeGesture = Readonly<{
  pointerId: number;
  section: HTMLElement;
  date: PlainDate;
  startMinute: number;
  startX: number;
  startY: number;
}>;

type DayLayout = Readonly<{
  section: HTMLElement;
  eventsHost: HTMLElement | null;
  pixelAtMinute: (minute: number) => number;
}>;

type GroupLayout = Readonly<{
  index: number;
  tone: string;
}>;

type PlanningUndo = Readonly<{
  kind: 'placement' | 'delete';
  originalEffect: TemporalCreateAppliedEffect;
  mutation: TemporalCreateMutationEffect;
}>;

function parsePixel(value: string): number {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function minuteAtClientY(section: HTMLElement, clientY: number): number {
  const rect = section.getBoundingClientRect();
  const localY = clientY - rect.top;
  const lines = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
  );
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;
  if (lines.length < 2) {
    return Math.max(
      0,
      Math.min(1439, (localY / Math.max(1, rect.height)) * 1440),
    );
  }

  for (let index = 0; index < lines.length - 1; index += 1) {
    const current = parsePixel(lines[index]?.style.top ?? '0');
    const next = parsePixel(lines[index + 1]?.style.top ?? String(current));
    if (localY <= next) {
      const progress =
        next <= current ? 0 : (localY - current) / (next - current);
      return Math.max(
        0,
        Math.min(1439, (index + Math.max(0, Math.min(1, progress))) * interval),
      );
    }
  }

  return 1439;
}

function snapMinute(minute: number): number {
  return Math.max(0, Math.min(1425, Math.round(minute / 15) * 15));
}

function createMinutePixelMapper(
  section: HTMLElement,
): (minute: number) => number {
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;
  const lineTops = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
    (line) => parsePixel(line.style.top),
  );

  if (lineTops.length < 2) {
    const sectionHeight = section.clientHeight;
    return (minute) =>
      (Math.max(0, Math.min(1440, minute)) / 1440) * sectionHeight;
  }

  return (minute) => {
    const normalized = Math.max(0, Math.min(1440, minute)) / interval;
    const lowerIndex = Math.min(lineTops.length - 1, Math.floor(normalized));
    const upperIndex = Math.min(lineTops.length - 1, lowerIndex + 1);
    const lower = lineTops[lowerIndex] ?? 0;
    const upper = lineTops[upperIndex] ?? lower;
    return lower + (upper - lower) * (normalized - lowerIndex);
  };
}

function formatMinute(minute: number): string {
  return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
    minute % 60,
  ).padStart(2, '0')}`;
}

function emptyTimelineTarget(target: EventTarget | null): HTMLElement | null {
  if (!(target instanceof Element)) {
    return null;
  }
  if (
    target.closest(
      'button, input, select, textarea, .timeline-event-card, .timeline-all-day-lane, .timeline-all-day-item, .temporal-create-projection-card, .temporal-create-all-day',
    )
  ) {
    return null;
  }
  return target.closest<HTMLElement>(
    '.timeline-day-section[data-timeline-date]',
  );
}

function clientYInsideAllDayLane(
  section: HTMLElement,
  clientY: number,
): boolean {
  const lane = section.querySelector<HTMLElement>('.timeline-all-day-lane');
  if (!lane) {
    return false;
  }
  const rect = lane.getBoundingClientRect();
  return clientY >= rect.top && clientY < rect.bottom;
}

function slotKey(projection: TemporalCreateTimelineProjection): string {
  return `${projection.dateKey ?? ''}|${projection.allDay ? 'all-day' : 'timed'}|${
    projection.startMinute ?? 'none'
  }`;
}

function timelineEventFromProjection(
  projection: TemporalCreateTimelineProjection,
  meta: string,
): Readonly<{ dateKey: string; event: TimelineEvent }> | null {
  if (
    projection.preview ||
    projection.allDay ||
    projection.dateKey === null ||
    projection.startMinute === null ||
    projection.endMinute === null
  ) {
    return null;
  }

  return Object.freeze({
    dateKey: projection.dateKey,
    event: Object.freeze({
      id: projection.id,
      startMinute: projection.startMinute,
      endMinute: projection.endMinute,
      title: projection.title,
      groupId: projection.contextId,
      ...(projection.appearanceTone
        ? { appearanceTone: projection.appearanceTone }
        : {}),
      ...(projection.kind === 'event' && projection.agendaParts.length > 0
        ? { subitems: projection.agendaParts }
        : {}),
      origin: 'create' as const,
      meta,
    }),
  });
}

function timelineAllDayFromProjection(
  projection: TemporalCreateTimelineProjection,
  meta: string,
): TimelineAllDayItem | null {
  if (
    projection.preview ||
    !projection.allDay ||
    projection.dateKey === null ||
    projection.endDateExclusiveKey === null
  ) {
    return null;
  }

  return Object.freeze({
    id: projection.id,
    startDateKey: projection.dateKey,
    endDateExclusiveKey: projection.endDateExclusiveKey,
    title: projection.title,
    groupId: projection.contextId,
    ...(projection.appearanceTone
      ? { appearanceTone: projection.appearanceTone }
      : {}),
    origin: 'create' as const,
    meta,
  });
}

function isNativeMaterializedProjection(
  projection: TemporalCreateTimelineProjection,
): boolean {
  return (
    timelineEventFromProjection(projection, '') !== null ||
    timelineAllDayFromProjection(projection, '') !== null
  );
}

function withProjection(
  effect: TemporalCreateAppliedEffect,
  projection: TemporalCreateAppliedEffect['projection'],
): TemporalCreateAppliedEffect {
  return Object.freeze({ ...effect, projection });
}

function planningPlacement(
  effect: TemporalCreateAppliedEffect,
  dateKey: string,
  requestedStartMinute: number,
): TemporalPlacement {
  const specification = effect.metadata.specification;
  const date = Temporal.PlainDate.from(dateKey);
  const duration = Math.max(5, specification.durationMinutes);
  const startMinute = Math.max(
    0,
    Math.min(1439, Math.round(requestedStartMinute)),
  );
  const localStart = Temporal.PlainDateTime.from({
    year: date.year,
    month: date.month,
    day: date.day,
    hour: Math.floor(startMinute / 60),
    minute: startMinute % 60,
  });

  if (specification.timeMode === 'zoned') {
    const start = localStart.toZonedDateTime(effect.metadata.timeZoneId);
    return Object.freeze({
      kind: 'zoned' as const,
      start,
      end: start.add({ minutes: duration }),
    });
  }

  return Object.freeze({
    kind: 'floating-local' as const,
    start: localStart,
    end: localStart.add({ minutes: duration }),
  });
}

export function TimelineCreateBridge({
  defaultDate,
  groups,
  filters,
  onRevealDate,
  onCreateContext,
  onMaterializeCreatedEvent,
  onMaterializeCreatedAllDay,
  onRemoveCreatedEvent,
  onRemoveCreatedAllDay,
  onBeforeOpen,
}: TimelineCreateBridgeProps) {
  const { t } = useTranslation('common');
  const [effects, setEffects] = useState<
    readonly TemporalCreateAppliedEffect[]
  >([]);
  const [preview, setPreview] =
    useState<TemporalCreateTimelineProjection | null>(null);
  const [request, setRequest] = useState<TemporalCreateInvocation | null>(null);
  const [layoutRevision, setLayoutRevision] = useState(0);
  const [undoEffect, setUndoEffect] =
    useState<TemporalCreateAppliedEffect | null>(null);
  const [planningUndo, setPlanningUndo] = useState<PlanningUndo | null>(null);
  const [planningFeedback, setPlanningFeedback] = useState('');
  const [toastVisible, setToastVisible] = useState(false);
  const requestIdRef = useRef(0);
  const layoutFrameRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);
  const rangeGestureRef = useRef<RangeGesture | null>(null);

  const contextOptions = useMemo<readonly TemporalCreateContextOption[]>(
    () =>
      groups.map((group) => ({
        id: group.id,
        label: group.label,
        tone: group.tone,
        local: group.id.startsWith('local-context:'),
      })),
    [groups],
  );

  const planningItems = useMemo<readonly TimelinePlanningTrayItem[]>(() => {
    const groupMap = new Map(
      groups.map((group, index) => [group.id, { group, index }]),
    );
    return effects.flatMap((effect) => {
      if (
        effect.metadata.kind !== 'activity' ||
        effect.projection.placement !== null
      ) {
        return [];
      }
      const specification = effect.metadata.specification;
      const groupEntry = groupMap.get(effect.metadata.contextId);
      return [
        Object.freeze({
          id: effect.projection.id,
          title: effect.projection.title,
          contextLabel: groupEntry?.group.label ?? effect.metadata.contextId,
          tone:
            specification.appearanceTone ??
            groupEntry?.group.tone ??
            ('personal' as const),
          groupIndex: groupEntry?.index ?? 0,
          durationMinutes: specification.durationMinutes,
          constraintKind: specification.scheduling.constraintKind,
          splittable: specification.execution.sessionMode === 'splittable',
          notes: effect.metadata.notes,
        }),
      ];
    });
  }, [effects, groups]);

  const createContext = useCallback(
    (input: TemporalCreateContextInput): TemporalCreateContextOption => {
      const group = onCreateContext(input.label, input.tone);
      return Object.freeze({
        id: group.id,
        label: group.label,
        tone: group.tone,
        local: group.id.startsWith('local-context:'),
      });
    },
    [onCreateContext],
  );

  const scheduleLayoutRefresh = useCallback(() => {
    if (layoutFrameRef.current !== null) {
      return;
    }
    layoutFrameRef.current = requestAnimationFrame(() => {
      layoutFrameRef.current = null;
      setLayoutRevision((current) => current + 1);
    });
  }, []);

  useEffect(() => {
    const root = document.querySelector<HTMLElement>(
      '.home-timeline--production',
    );
    if (!root) {
      return;
    }
    const childObserver = new MutationObserver(scheduleLayoutRefresh);
    childObserver.observe(root, { childList: true, subtree: true });
    const rootStyleObserver = new MutationObserver(scheduleLayoutRefresh);
    rootStyleObserver.observe(root, {
      attributes: true,
      attributeFilter: ['style'],
    });
    window.addEventListener('resize', scheduleLayoutRefresh);
    root.addEventListener('scroll', scheduleLayoutRefresh, true);
    return () => {
      childObserver.disconnect();
      rootStyleObserver.disconnect();
      window.removeEventListener('resize', scheduleLayoutRefresh);
      root.removeEventListener('scroll', scheduleLayoutRefresh, true);
      if (layoutFrameRef.current !== null) {
        cancelAnimationFrame(layoutFrameRef.current);
        layoutFrameRef.current = null;
      }
    };
  }, [scheduleLayoutRefresh]);

  useEffect(() => {
    const onDoubleClick = (event: MouseEvent) => {
      const section = emptyTimelineTarget(event.target);
      if (!section?.dataset.timelineDate) {
        return;
      }
      const minute = snapMinute(minuteAtClientY(section, event.clientY));
      setRequest({
        id: ++requestIdRef.current,
        date: Temporal.PlainDate.from(section.dataset.timelineDate),
        startMinute: minute,
        anchor: {
          left: event.clientX,
          top: event.clientY,
          bottom: event.clientY,
        },
      });
    };

    const onPointerDown = (event: PointerEvent) => {
      if (!event.shiftKey || event.button !== 0) {
        return;
      }
      const section = emptyTimelineTarget(event.target);
      if (!section?.dataset.timelineDate) {
        return;
      }
      rangeGestureRef.current = {
        pointerId: event.pointerId,
        section,
        date: Temporal.PlainDate.from(section.dataset.timelineDate),
        startMinute: snapMinute(minuteAtClientY(section, event.clientY)),
        startX: event.clientX,
        startY: event.clientY,
      };
      document.documentElement.setAttribute(
        'data-temporal-create-ranging',
        'true',
      );
      event.preventDefault();
    };

    const finishRange = (event: PointerEvent) => {
      const gesture = rangeGestureRef.current;
      if (!gesture || gesture.pointerId !== event.pointerId) {
        return;
      }
      rangeGestureRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-ranging');
      if (clientYInsideAllDayLane(gesture.section, event.clientY)) {
        return;
      }
      const endMinute = snapMinute(
        minuteAtClientY(gesture.section, event.clientY),
      );
      const startMinute = Math.min(gesture.startMinute, endMinute);
      const rawDuration = Math.abs(endMinute - gesture.startMinute);
      const durationMinutes = Math.max(15, rawDuration || 30);
      const moved =
        Math.abs(event.clientY - gesture.startY) >= 8 ||
        Math.abs(event.clientX - gesture.startX) >= 8;
      if (!moved) {
        return;
      }
      setRequest({
        id: ++requestIdRef.current,
        date: gesture.date,
        startMinute,
        durationMinutes,
        anchor: {
          left: event.clientX,
          top: event.clientY,
          bottom: event.clientY,
        },
      });
      event.preventDefault();
    };

    const cancelRange = (event: PointerEvent) => {
      if (rangeGestureRef.current?.pointerId !== event.pointerId) {
        return;
      }
      rangeGestureRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-ranging');
    };

    document.addEventListener('dblclick', onDoubleClick, true);
    document.addEventListener('pointerdown', onPointerDown, true);
    document.addEventListener('pointerup', finishRange, true);
    document.addEventListener('pointercancel', cancelRange, true);
    return () => {
      document.removeEventListener('dblclick', onDoubleClick, true);
      document.removeEventListener('pointerdown', onPointerDown, true);
      document.removeEventListener('pointerup', finishRange, true);
      document.removeEventListener('pointercancel', cancelRange, true);
      document.documentElement.removeAttribute('data-temporal-create-ranging');
    };
  }, []);

  useEffect(() => {
    return () => {
      if (toastTimerRef.current !== null) {
        window.clearTimeout(toastTimerRef.current);
      }
    };
  }, []);

  const showToast = useCallback(() => {
    setToastVisible(true);
    if (toastTimerRef.current !== null) {
      window.clearTimeout(toastTimerRef.current);
    }
    toastTimerRef.current = window.setTimeout(() => {
      setToastVisible(false);
      toastTimerRef.current = null;
    }, TIMELINE_POLICY.feedback.toastDurationMs);
  }, []);

  const showCreateFeedback = useCallback(
    (effect: TemporalCreateAppliedEffect) => {
      setPlanningUndo(null);
      setPlanningFeedback('');
      setUndoEffect(effect);
      showToast();
    },
    [showToast],
  );

  const showPlanningFeedback = useCallback(
    (feedback: string, undo: PlanningUndo) => {
      setUndoEffect(null);
      setPlanningUndo(undo);
      setPlanningFeedback(feedback);
      showToast();
    },
    [showToast],
  );

  const reveal = useCallback(
    (projection: TemporalCreateTimelineProjection) => {
      if (!projection.dateKey) {
        return false;
      }
      onRevealDate(Temporal.PlainDate.from(projection.dateKey));
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          const id = CSS.escape(projection.id);
          const card = document.querySelector<HTMLElement>(
            `[data-timeline-event="${id}"], [data-timeline-all-day-item="${id}"], [data-temporal-create-projection="${id}"]`,
          );
          const grid = document.querySelector<HTMLElement>('.timeline-grid');
          if (card?.matches('[data-timeline-event]')) {
            card.dataset.temporalCreateProjection = projection.id;
          }
          if (card && grid) {
            const gridRect = grid.getBoundingClientRect();
            const cardRect = card.getBoundingClientRect();
            const cardContentTop =
              grid.scrollTop + (cardRect.top - gridRect.top);
            grid.scrollTo({
              top: Math.max(0, cardContentTop - grid.clientHeight * 0.28),
              behavior: window.matchMedia('(prefers-reduced-motion: reduce)')
                .matches
                ? 'auto'
                : 'smooth',
            });
            card.focus({ preventScroll: true });
          }
        });
      });
      return true;
    },
    [onRevealDate],
  );

  const applied = useCallback(
    (effect: TemporalCreateAppliedEffect) => {
      const projection = temporalCreateTimelineProjectionFromEffect(effect);
      const meta = projection.recurring
        ? t(($) => $.common.home.timeline.create.recurrence.recurringBadge)
        : projection.kind === 'activity'
          ? t(($) => $.common.home.timeline.create.kind.activity)
          : t(($) => $.common.home.timeline.create.kind.event);
      const timed = timelineEventFromProjection(projection, meta);
      const allDay = timelineAllDayFromProjection(projection, meta);
      if (timed) {
        onMaterializeCreatedEvent(timed.dateKey, timed.event);
      } else if (allDay) {
        onMaterializeCreatedAllDay(allDay);
      }
      setEffects((current) => [...current, effect]);
      setPreview(null);
      showCreateFeedback(effect);
      return reveal(projection);
    },
    [
      onMaterializeCreatedAllDay,
      onMaterializeCreatedEvent,
      reveal,
      showCreateFeedback,
      t,
    ],
  );

  const placePlanningItem = useCallback(
    async (itemId: string, dateKey: string, startMinute: number) => {
      const effect = effects.find(
        (candidate) => candidate.projection.id === itemId,
      );
      if (!effect || effect.projection.placement !== null) {
        return false;
      }
      const execution = await effect.replacePlacement(
        planningPlacement(effect, dateKey, startMinute),
      );
      const mutation = execution.effect;
      if (execution.result.status !== 'applied' || !mutation?.projection) {
        return false;
      }

      const updated = withProjection(effect, mutation.projection);
      setEffects((current) =>
        current.map((candidate) =>
          candidate.projection.id === itemId ? updated : candidate,
        ),
      );
      const projection = temporalCreateTimelineProjectionFromEffect(updated);
      const native = timelineEventFromProjection(
        projection,
        t(($) => $.common.home.timeline.create.kind.activity),
      );
      if (!native) {
        await mutation.undo();
        return false;
      }
      onMaterializeCreatedEvent(native.dateKey, native.event);
      reveal(projection);
      showPlanningFeedback(
        `${t(($) => $.common.home.timeline.create.kind.activity)} · ${formatMinute(native.event.startMinute)}`,
        Object.freeze({
          kind: 'placement',
          originalEffect: effect,
          mutation,
        }),
      );
      return true;
    },
    [effects, onMaterializeCreatedEvent, reveal, showPlanningFeedback, t],
  );

  const deletePlanningItem = useCallback(
    async (itemId: string) => {
      const effect = effects.find(
        (candidate) => candidate.projection.id === itemId,
      );
      if (!effect || effect.projection.placement !== null) {
        return false;
      }
      const execution = await effect.remove();
      const mutation = execution.effect;
      if (execution.result.status !== 'applied' || !mutation) {
        return false;
      }
      setEffects((current) =>
        current.filter((candidate) => candidate.projection.id !== itemId),
      );
      showPlanningFeedback(
        `${t(($) => $.common.home.timeline.create.kind.activity)} · ${effect.projection.title}`,
        Object.freeze({
          kind: 'delete',
          originalEffect: effect,
          mutation,
        }),
      );
      return true;
    },
    [effects, showPlanningFeedback, t],
  );

  const projections = useMemo(
    () =>
      effects
        .map(temporalCreateTimelineProjectionFromEffect)
        .filter((projection) => !isNativeMaterializedProjection(projection)),
    [effects],
  );

  const portalTargets = useMemo(() => {
    void layoutRevision;
    if (typeof document === 'undefined') {
      return [] as PortalTarget[];
    }

    const all = preview ? [...projections, preview] : projections;
    const root = document.querySelector<HTMLElement>(
      '.home-timeline--production',
    );
    const rootStyle = root ? getComputedStyle(root) : null;
    const expansionProgress =
      Number.parseFloat(
        rootStyle?.getPropertyValue('--timeline-expansion-progress') ?? '0',
      ) || 0;
    const groupWidth =
      Number.parseFloat(
        rootStyle?.getPropertyValue('--timeline-expanded-group-width') ?? '260',
      ) || 260;
    const groupLayouts = new Map<string, GroupLayout>();
    groups.forEach((group, index) => {
      groupLayouts.set(group.id, { index, tone: group.tone });
    });
    const dayLayouts = new Map<string, DayLayout | null>();
    const slotCounts = new Map<string, number>();
    const targets: PortalTarget[] = [];

    const dayLayoutFor = (dateKey: string): DayLayout | null => {
      if (dayLayouts.has(dateKey)) {
        return dayLayouts.get(dateKey) ?? null;
      }
      const section = document.querySelector<HTMLElement>(
        `.timeline-day-section[data-timeline-date="${CSS.escape(dateKey)}"]`,
      );
      if (!section) {
        dayLayouts.set(dateKey, null);
        return null;
      }
      const dayLayout = Object.freeze({
        section,
        eventsHost: section.querySelector<HTMLElement>(
          '.timeline-events-layer',
        ),
        pixelAtMinute: createMinutePixelMapper(section),
      });
      dayLayouts.set(dateKey, dayLayout);
      return dayLayout;
    };

    for (const projection of all) {
      if (
        !projection.dateKey ||
        (filters.size > 0 && !filters.has(projection.contextId))
      ) {
        continue;
      }

      const key = slotKey(projection);
      const precedingSameSlot = slotCounts.get(key) ?? 0;
      slotCounts.set(key, precedingSameSlot + 1);

      const dayLayout = dayLayoutFor(projection.dateKey);
      if (!dayLayout) {
        continue;
      }
      const groupLayout = groupLayouts.get(projection.contextId);
      const tone = projection.appearanceTone ?? groupLayout?.tone ?? 'personal';

      if (projection.allDay) {
        targets.push({
          projection,
          host: dayLayout.section,
          tone,
          style: { top: 30 + precedingSameSlot * 30, right: 18 },
        });
        continue;
      }

      if (
        projection.startMinute === null ||
        projection.endMinute === null ||
        !dayLayout.eventsHost
      ) {
        continue;
      }

      const top = dayLayout.pixelAtMinute(projection.startMinute);
      const bottom = dayLayout.pixelAtMinute(projection.endMinute);
      const compactLeft = 14 + precedingSameSlot * 8;
      const compactWidth = Math.min(
        300,
        Math.max(180, dayLayout.eventsHost.clientWidth * 0.34),
      );
      const groupIndex = groupLayout?.index ?? 0;
      const expandedLeft = groupIndex * groupWidth + 6 + precedingSameSlot * 8;
      const expandedWidth = Math.max(150, groupWidth - 12);

      targets.push({
        projection,
        host: dayLayout.eventsHost,
        tone,
        style: {
          top: top + precedingSameSlot * 4,
          left: compactLeft + (expandedLeft - compactLeft) * expansionProgress,
          width:
            compactWidth + (expandedWidth - compactWidth) * expansionProgress,
          height: Math.max(38, bottom - top),
        },
      });
    }

    return targets;
  }, [filters, groups, layoutRevision, preview, projections]);

  const undoCreate = async () => {
    const effect = undoEffect;
    if (!effect) {
      return;
    }
    const projection = temporalCreateTimelineProjectionFromEffect(effect);
    const result = await effect.undo();
    if (result.status === 'applied') {
      if (projection.allDay) {
        onRemoveCreatedAllDay(projection.id);
      } else {
        onRemoveCreatedEvent(projection.id);
      }
      setEffects((current) =>
        current.filter(
          (candidate) => candidate.projection.id !== effect.projection.id,
        ),
      );
      setUndoEffect(null);
      setToastVisible(false);
    }
  };

  const undoPlanningMutation = async () => {
    const undo = planningUndo;
    if (!undo) {
      return;
    }
    const result = await undo.mutation.undo();
    if (result.status !== 'applied' || !result.item) {
      return;
    }

    if (undo.kind === 'placement') {
      onRemoveCreatedEvent(undo.originalEffect.projection.id);
      const restored = withProjection(undo.originalEffect, result.item);
      setEffects((current) =>
        current.map((candidate) =>
          candidate.projection.id === restored.projection.id
            ? restored
            : candidate,
        ),
      );
    } else {
      const restored = withProjection(undo.originalEffect, result.item);
      setEffects((current) =>
        current.some(
          (candidate) => candidate.projection.id === restored.projection.id,
        )
          ? current
          : [...current, restored],
      );
    }

    setPlanningUndo(null);
    setPlanningFeedback('');
    setToastVisible(false);
  };

  const feedbackSuffix = undoEffect
    ? undoEffect.metadata.specification.scheduling.constraintKind !== 'none'
      ? ` · ${t(($) => $.common.home.timeline.create.timeSemantics.unscheduled)}`
      : undoEffect.metadata.timeSemantics === 'unscheduled'
        ? ` · ${t(($) => $.common.home.timeline.create.timeSemantics.unscheduled)}`
        : ''
    : '';

  return (
    <>
      <TemporalCreateContextCatalogProvider onCreateContext={createContext}>
        <TemporalCreateEntry
          defaultDate={defaultDate}
          contexts={contextOptions}
          request={request}
          onPreview={setPreview}
          onApplied={applied}
          onBeforeOpen={onBeforeOpen}
        />
      </TemporalCreateContextCatalogProvider>

      <TimelinePlanningTray
        items={planningItems}
        defaultDate={defaultDate}
        onBeforeOpen={onBeforeOpen}
        onPlace={placePlanningItem}
        onDelete={deletePlanningItem}
      />

      {portalTargets.map(({ projection, host, style, tone }) =>
        createPortal(
          projection.allDay ? (
            <div
              className={`temporal-create-all-day${
                projection.preview ? ' is-preview' : ''
              }`}
              data-timeline-tone={tone}
              data-temporal-create-projection={projection.id}
              style={style}
              tabIndex={projection.preview ? -1 : 0}
            >
              <span>
                {projection.kind === 'activity'
                  ? t(($) => $.common.home.timeline.create.kind.activity)
                  : t(($) => $.common.home.timeline.create.kind.event)}
                {projection.recurring
                  ? ` · ${t(($) => $.common.home.timeline.create.recurrence.recurringBadge)}`
                  : ''}
              </span>
              <strong>{projection.title}</strong>
            </div>
          ) : (
            <article
              className={`temporal-create-projection-card${
                projection.preview ? ' is-preview' : ''
              }`}
              data-timeline-tone={tone}
              data-temporal-create-projection={projection.id}
              style={style}
              tabIndex={projection.preview ? -1 : 0}
              aria-label={`${projection.title}, ${
                projection.startMinute === null
                  ? ''
                  : formatMinute(projection.startMinute)
              }`}
            >
              <strong>{projection.title}</strong>
              <span>
                {projection.startMinute === null
                  ? ''
                  : formatMinute(projection.startMinute)}{' '}
                ·{' '}
                {projection.kind === 'activity'
                  ? t(($) => $.common.home.timeline.create.kind.activity)
                  : t(($) => $.common.home.timeline.create.kind.event)}
                {projection.recurring
                  ? ` · ${t(($) => $.common.home.timeline.create.recurrence.recurringBadge)}`
                  : ''}
              </span>
            </article>
          ),
          host,
          projection.id,
        ),
      )}

      {typeof document !== 'undefined'
        ? createPortal(
            <div
              className={`temporal-create-toast${toastVisible ? ' is-on' : ''}`}
              role="status"
              aria-live="polite"
            >
              <span>
                {planningUndo
                  ? planningFeedback
                  : undoEffect
                    ? `${t(($) => $.common.home.timeline.feedback.created)} ${
                        undoEffect.projection.title
                      }${feedbackSuffix}`
                    : ''}
              </span>
              {planningUndo || undoEffect ? (
                <button
                  type="button"
                  onClick={() =>
                    void (planningUndo ? undoPlanningMutation() : undoCreate())
                  }
                >
                  {t(($) => $.common.home.timeline.undo)}
                </button>
              ) : null}
            </div>,
            document.body,
          )
        : null}
    </>
  );
}
