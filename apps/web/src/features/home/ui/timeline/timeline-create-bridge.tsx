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
import type { TimelineGroup } from './model/timeline-types';

import './timeline-create-bridge.css';

type TimelineCreateBridgeProps = Readonly<{
  defaultDate: PlainDate;
  groups: readonly TimelineGroup[];
  onRevealDate: (date: PlainDate) => void;
  onBeforeOpen?: () => void;
}>;

type PortalTarget = Readonly<{
  projection: TemporalCreateTimelineProjection;
  host: Element;
  style: CSSProperties;
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

function pixelAtMinute(section: HTMLElement, minute: number): number {
  const lines = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
  );
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;
  if (lines.length < 2) {
    return (
      (Math.max(0, Math.min(1440, minute)) / 1440) * section.clientHeight
    );
  }
  const normalized = Math.max(0, Math.min(1440, minute)) / interval;
  const lowerIndex = Math.min(lines.length - 1, Math.floor(normalized));
  const upperIndex = Math.min(lines.length - 1, lowerIndex + 1);
  const lower = parsePixel(lines[lowerIndex]?.style.top ?? '0');
  const upper = parsePixel(
    lines[upperIndex]?.style.top ?? String(lower),
  );
  return lower + (upper - lower) * (normalized - lowerIndex);
}

function toneForContext(
  groups: readonly TimelineGroup[],
  contextId: string,
): string {
  return groups.find((group) => group.id === contextId)?.tone ?? 'personal';
}

function formatMinute(minute: number): string {
  return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
    minute % 60,
  ).padStart(2, '0')}`;
}

export function TimelineCreateBridge({
  defaultDate,
  groups,
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
      const target = event.target;
      if (!(target instanceof Element)) {
        return;
      }
      if (
        target.closest(
          'button, input, select, textarea, .timeline-event-card, .temporal-create-projection-card',
        )
      ) {
        return;
      }
      const section = target.closest<HTMLElement>(
        '.timeline-day-section[data-timeline-date]',
      );
      if (!section?.dataset.timelineDate) {
        return;
      }
      const minute =
        Math.round(minuteAtClientY(section, event.clientY) / 15) * 15;
      setRequest({
        id: ++requestIdRef.current,
        date: Temporal.PlainDate.from(section.dataset.timelineDate),
        startMinute: Math.max(0, Math.min(1425, minute)),
        anchor: {
          left: event.clientX,
          top: event.clientY,
          bottom: event.clientY,
        },
      });
    };
    document.addEventListener('dblclick', onDoubleClick, true);
    return () => document.removeEventListener('dblclick', onDoubleClick, true);
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
        return;
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
    },
    [onRevealDate],
  );

  const applied = useCallback(
    (effect: TemporalCreateAppliedEffect) => {
      const projection = temporalCreateTimelineProjectionFromEffect(effect);
      setEffects((current) => [...current, effect]);
      setPreview(null);
      showCreateFeedback(effect);
      reveal(projection);
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

    return all.flatMap<PortalTarget>((projection) => {
      if (!projection.dateKey) {
        return [];
      }
      const section = document.querySelector<HTMLElement>(
        `.timeline-day-section[data-timeline-date="${CSS.escape(
          projection.dateKey,
        )}"]`,
      );
      if (!section) {
        return [];
      }
      const host = projection.allDay
        ? section
        : section.querySelector<HTMLElement>('.timeline-events-layer');
      if (!host) {
        return [];
      }
      if (projection.allDay) {
        return [
          {
            projection,
            host,
            tone: toneForContext(groups, projection.contextId),
            style: { top: 30, right: 18 },
          },
        ];
      }
      if (
        projection.startMinute === null ||
        projection.endMinute === null
      ) {
        return [];
      }
      const top = pixelAtMinute(section, projection.startMinute);
      const bottom = pixelAtMinute(section, projection.endMinute);
      const compactLeft = 14;
      const compactWidth = Math.min(
        300,
        Math.max(180, host.clientWidth * 0.34),
      );
      const foundGroupIndex = groups.findIndex(
        (group) => group.id === projection.contextId,
      );
      const groupIndex = foundGroupIndex < 0 ? 0 : foundGroupIndex;
      const expandedLeft = groupIndex * groupWidth + 6;
      const expandedWidth = Math.max(150, groupWidth - 12);
      return [
        {
          projection,
          host,
          tone: toneForContext(groups, projection.contextId),
          style: {
            top,
            left:
              compactLeft +
              (expandedLeft - compactLeft) * expansionProgress,
            width:
              compactWidth +
              (expandedWidth - compactWidth) * expansionProgress,
            height: Math.max(38, bottom - top),
          },
        },
      ];
    });
  }, [groups, layoutRevision, preview, projections]);

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

  return (
    <>
      <TemporalCreateEntry
        defaultDate={defaultDate}
        contexts={groups.map((group) => ({
          id: group.id,
          label: group.label,
        }))}
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
                    }`
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
