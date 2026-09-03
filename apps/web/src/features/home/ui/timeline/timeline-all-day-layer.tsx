import { Temporal } from '@dante/time';
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineGroup,
  TimelineGroupId,
} from './model/timeline-types';

import './timeline-all-day-layer.css';

type TimelineAllDayLaneProps = Readonly<{
  dateKey: string;
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
}>;

type TimelineAllDayLayerProps = Readonly<{
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
}>;

type VisibleDayCandidate = Readonly<{
  dateKey: string;
  distance: number;
  containsProbe: boolean;
}>;

function isLastCoveredDate(item: TimelineAllDayItem, dateKey: string): boolean {
  return (
    Temporal.PlainDate.from(dateKey).add({ days: 1 }).toString() ===
    item.endDateExclusiveKey
  );
}

export function TimelineAllDayLane({
  dateKey,
  items,
  groups,
  filters,
}: TimelineAllDayLaneProps) {
  const { t } = useTranslation('common');
  const visibleItems = useMemo(
    () => timelineAllDayItemsForVisibleDate(items, filters, dateKey),
    [dateKey, filters, items],
  );
  const groupMap = useMemo(
    () => new Map(groups.map((group) => [group.id, group])),
    [groups],
  );

  if (visibleItems.length === 0) {
    return null;
  }

  return (
    <section
      className="timeline-all-day-lane"
      data-timeline-all-day-lane={dateKey}
      aria-label={t(($) => $.common.home.timeline.create.timeSemantics.allDay)}
      style={{ height: timelineAllDayLaneHeightPx(visibleItems.length) }}
    >
      <div className="timeline-all-day-lane__label">
        <span>{t(($) => $.common.home.timeline.create.timeSemantics.allDay)}</span>
      </div>
      <div className="timeline-all-day-lane__items">
        {visibleItems.map((item) => {
          const group = groupMap.get(item.groupId);
          const tone = item.appearanceTone ?? group?.tone ?? 'personal';
          const startsHere = dateKey === item.startDateKey;
          const endsHere = isLastCoveredDate(item, dateKey);
          return (
            <button
              className="timeline-all-day-item"
              type="button"
              key={item.id}
              data-timeline-all-day-item={item.id}
              data-temporal-create-projection={
                item.origin === 'create' ? item.id : undefined
              }
              data-timeline-tone={tone}
              data-range-start={startsHere || undefined}
              data-range-end={endsHere || undefined}
              aria-label={`${item.title} · ${t(
                ($) => $.common.home.timeline.create.timeSemantics.allDay,
              )} · ${group?.label ?? item.groupId}`}
              onClick={(event) => event.currentTarget.focus()}
            >
              <span
                className="timeline-all-day-item__continuation"
                aria-hidden="true"
              >
                {startsHere ? '' : '‹'}
              </span>
              <strong>{item.title}</strong>
              <span className="timeline-all-day-item__meta">
                {group?.label ?? item.groupId}
                {item.meta ? ` · ${item.meta}` : ''}
              </span>
              <span
                className="timeline-all-day-item__continuation"
                aria-hidden="true"
              >
                {endsHere ? '' : '›'}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

function activeTimelineDate(
  items: readonly TimelineAllDayItem[],
  filters: ReadonlySet<TimelineGroupId>,
): string | null {
  const grid = document.querySelector<HTMLElement>('.timeline-grid');
  if (!grid) {
    return null;
  }
  const gridRect = grid.getBoundingClientRect();
  if (gridRect.height <= 0) {
    return null;
  }

  const probeY = gridRect.top + gridRect.height * 0.34;
  const candidates = Array.from(
    grid.querySelectorAll<HTMLElement>(
      '.timeline-day-section[data-timeline-date]',
    ),
  ).flatMap<VisibleDayCandidate>((section) => {
    const dateKey = section.dataset.timelineDate;
    if (!dateKey) {
      return [];
    }
    const rect = section.getBoundingClientRect();
    const visibleTop = Math.max(rect.top, gridRect.top);
    const visibleBottom = Math.min(rect.bottom, gridRect.bottom);
    if (visibleBottom <= visibleTop) {
      return [];
    }
    return [
      {
        dateKey,
        distance: Math.abs((visibleTop + visibleBottom) / 2 - probeY),
        containsProbe: probeY >= rect.top && probeY < rect.bottom,
      },
    ];
  });

  const hasVisibleItem = (dateKey: string) =>
    timelineAllDayItemsForVisibleDate(items, filters, dateKey).length > 0;
  const direct = candidates.find((candidate) => candidate.containsProbe);
  if (direct && hasVisibleItem(direct.dateKey)) {
    return direct.dateKey;
  }
  const nearestWithItem = candidates
    .filter((candidate) => hasVisibleItem(candidate.dateKey))
    .sort((left, right) => left.distance - right.distance)[0];
  if (nearestWithItem) {
    return nearestWithItem.dateKey;
  }
  return direct?.dateKey ?? null;
}

/**
 * Transitional host used while Timeline viewport geometry moves the lane from
 * header space into each rendered day. It keeps the branch runnable between
 * atomic checkpoints; the final C1 candidate removes this compatibility host.
 */
export function TimelineAllDayLayer({
  items,
  groups,
  filters,
}: TimelineAllDayLayerProps) {
  const [activeDateKey, setActiveDateKey] = useState<string | null>(null);
  const frameRef = useRef<number | null>(null);

  const scheduleRefresh = useCallback(() => {
    if (frameRef.current !== null) {
      return;
    }
    frameRef.current = requestAnimationFrame(() => {
      frameRef.current = null;
      setActiveDateKey(activeTimelineDate(items, filters));
    });
  }, [filters, items]);

  useEffect(() => {
    const root = document.querySelector<HTMLElement>(
      '.home-timeline--production',
    );
    if (!root) {
      return;
    }
    const observer = new MutationObserver(scheduleRefresh);
    observer.observe(root, { childList: true, subtree: true });
    root.addEventListener('scroll', scheduleRefresh, true);
    window.addEventListener('resize', scheduleRefresh);
    scheduleRefresh();
    return () => {
      observer.disconnect();
      root.removeEventListener('scroll', scheduleRefresh, true);
      window.removeEventListener('resize', scheduleRefresh);
      if (frameRef.current !== null) {
        cancelAnimationFrame(frameRef.current);
        frameRef.current = null;
      }
    };
  }, [scheduleRefresh]);

  if (!activeDateKey) {
    return null;
  }
  if (
    timelineAllDayItemsForVisibleDate(items, filters, activeDateKey).length === 0
  ) {
    return null;
  }
  const host = document.querySelector<HTMLElement>(
    '.home-timeline--production > .dante-timeline-header',
  );
  if (!host) {
    return null;
  }

  return createPortal(
    <TimelineAllDayLane
      dateKey={activeDateKey}
      items={items}
      groups={groups}
      filters={filters}
    />,
    host,
  );
}
