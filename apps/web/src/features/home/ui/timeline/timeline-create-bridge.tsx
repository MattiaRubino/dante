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

import {
  TemporalCreateEntry,
  temporalCreateTimelineProjectionFromEffect,
  type TemporalCreateAppliedEffect,
  type TemporalCreateInvocation,
  type TemporalCreateTimelineProjection,
} from '../../../temporal-create';
import { TIMELINE_POLICY } from './model/timeline-policy';
import type { TimelineGroup, TimelineGroupId } from './model/timeline-types';

import './timeline-create-bridge.css';

type TimelineCreateBridgeProps = Readonly<{
  defaultDate: PlainDate;
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
  onRevealDate: (date: PlainDate) => void;
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
    const next = parsePixel(
      lines[index + 1]?.style.top ?? String(current),
    );
    if (localY <= next) {
      const progress =
        next <= current ? 0 : (localY - current) / (next - current);
      return Math.max(
        0,
        Math.min(
          1439,
          (index + Math.max(0, Math.min(1, progress))) * interval,
        ),
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
      'button, input, select, textarea, .timeline-event-card, .temporal-create-projection-card, .temporal-create-all-day',
    )
  ) {
    return null;
  }
  return target.closest<HTMLElement>(
    '.timeline-day-section[data-timeline-date]',
  );
}

function slotKey(projection: TemporalCreateTimelineProjection): string {
  return `${projection.dateKey ?? ''}|${projection.allDay ? 'all-day' : 'timed'}|${
    projection.startMinute ?? 'none'
  }`;
}

export function TimelineCreateBridge({
  defaultDate,
  groups,
  filters,
  onRevealDate,
  onBeforeOpen,
}: TimelineCreateBridgeProps) {
  const { t } = useTranslation('common');
  const [effects, setEffects] = useState<readonly TemporalCreateAppliedEffect[]>(
    [],
  );
  const [preview, setPreview] =
    useState<TemporalCreateTimelineProjection | null>(null);
  const [request, setRequest] = useState<TemporalCreateInvocation | null>(null);
  const [layoutRevision, setLayoutRevision] = useState(0);
  const [undoEffect, setUndoEffect] =
    useState<TemporalCreateAppliedEffect | null>(null);
  const [toastVisible, setToastVisible] = useState(false);
  const requestIdRef = useRef(0);
  const layoutFrameRef = useRef<number | null>(null);
  const toastTimerRef = useRef<number | null>(null);
  const rangeGestureRef = useRef<RangeGesture | null>(null);

  const contextOptions = useMemo(
    () => groups.map((group) => ({ id: group.id, label: group.label })),
    [groups],
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
      document.documentElement.setAttribute('data-temporal-create-ranging', 'true');
      event.preventDefault();
    };

    const finishRange = (event: PointerEvent) => {
      const gesture = rangeGestureRef.current;
      if (!gesture || gesture.pointerId !== event.pointerId) {
        return;
      }
      rangeGestureRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-ranging');
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

  const showCreateFeedback = useCallback(
    (effect: TemporalCreateAppliedEffect) => {
      setUndoEffect(effect);
      setToastVisible(true);
      if (toastTimerRef.current !== null) {
        window.clearTimeout(toastTimerRef.current);
      }
      toastTimerRef.current = window.setTimeout(() => {
        setToastVisible(false);
        toastTimerRef.current = null;
      }, TIMELINE_POLICY.feedback.toastDurationMs);
    },
    [],
  );

  const reveal = useCallback(
    (projection: TemporalCreateTimelineProjection) => {
      if (!projection.dateKey) {
        return false;
      }
      onRevealDate(Temporal.PlainDate.from(projection.dateKey));
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          const selector = `[data-temporal-create-projection="${CSS.escape(
            projection.id,
          )}"]`;
          const card = document.querySelector<HTMLElement>(selector);
          const grid = document.querySelector<HTMLElement>('.timeline-grid');
          const day = card?.closest<HTMLElement>('.timeline-day-section');
          if (card && grid && day) {
            grid.scrollTo({
              top: Math.max(
                0,
                day.offsetTop + card.offsetTop - grid.clientHeight * 0.28,
              ),
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
      setEffects((current) => [...current, effect]);
      setPreview(null);
      showCreateFeedback(effect);
      return reveal(projection);
    },
    [reveal, showCreateFeedback],
  );

  const projections = useMemo(
    () => effects.map(temporalCreateTimelineProjectionFromEffect),
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
      const tone = groupLayout?.tone ?? 'personal';

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
      const expandedLeft =
        groupIndex * groupWidth + 6 + precedingSameSlot * 8;
      const expandedWidth = Math.max(150, groupWidth - 12);

      targets.push({
        projection,
        host: dayLayout.eventsHost,
        tone,
        style: {
          top: top + precedingSameSlot * 4,
          left:
            compactLeft + (expandedLeft - compactLeft) * expansionProgress,
          width:
            compactWidth + (expandedWidth - compactWidth) * expansionProgress,
          height: Math.max(38, bottom - top),
        },
      });
    }

    return targets;
  }, [filters, groups, layoutRevision, preview, projections]);

  const undo = async () => {
    const effect = undoEffect;
    if (!effect) {
      return;
    }
    const result = await effect.undo();
    if (result.status === 'applied') {
      setEffects((current) =>
        current.filter(
          (candidate) => candidate.projection.id !== effect.projection.id,
        ),
      );
      setUndoEffect(null);
      setToastVisible(false);
    }
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
      <TemporalCreateEntry
        defaultDate={defaultDate}
        contexts={contextOptions}
        request={request}
        onPreview={setPreview}
        onApplied={applied}
        onBeforeOpen={onBeforeOpen}
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
              className={`temporal-create-toast${
                toastVisible ? ' is-on' : ''
              }`}
              role="status"
              aria-live="polite"
            >
              <span>
                {undoEffect
                  ? `${t(($) => $.common.home.timeline.feedback.created)} ${
                      undoEffect.projection.title
                    }${feedbackSuffix}`
                  : ''}
              </span>
              {undoEffect ? (
                <button type="button" onClick={() => void undo()}>
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
