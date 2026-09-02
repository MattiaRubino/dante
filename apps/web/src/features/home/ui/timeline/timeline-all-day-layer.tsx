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

import type {
  TimelineAllDayItem,
  TimelineGroup,
  TimelineGroupId,
} from './model/timeline-types';

import './timeline-all-day-layer.css';

type TimelineAllDayLayerProps = Readonly<{
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
}>;

type VisibleAllDayItem = Readonly<{
  item: TimelineAllDayItem;
  tone: TimelineGroup['tone'];
  groupLabel: string;
  startsHere: boolean;
  endsHere: boolean;
}>;

function coversDate(item: TimelineAllDayItem, dateKey: string): boolean {
  return item.startDateKey <= dateKey && dateKey < item.endDateExclusiveKey;
}

function isLastCoveredDate(item: TimelineAllDayItem, dateKey: string): boolean {
  return (
    Temporal.PlainDate.from(dateKey).add({ days: 1 }).toString() ===
    item.endDateExclusiveKey
  );
}

function activeTimelineDate(): string | null {
  const grid = document.querySelector<HTMLElement>('.timeline-grid');
  if (!grid) {
    return null;
  }
  const gridRect = grid.getBoundingClientRect();
  if (gridRect.height <= 0) {
    return null;
  }

  const probeY = gridRect.top + gridRect.height * 0.34;
  const sections = Array.from(
    grid.querySelectorAll<HTMLElement>(
      '.timeline-day-section[data-timeline-date]',
    ),
  );
  const direct = sections.find((section) => {
    const rect = section.getBoundingClientRect();
    return probeY >= rect.top && probeY < rect.bottom;
  });
  if (direct?.dataset.timelineDate) {
    return direct.dataset.timelineDate;
  }

  let nearest: Readonly<{ dateKey: string; distance: number }> | null = null;
  for (const section of sections) {
    const dateKey = section.dataset.timelineDate;
    if (!dateKey) {
      continue;
    }
    const rect = section.getBoundingClientRect();
    const visibleTop = Math.max(rect.top, gridRect.top);
    const visibleBottom = Math.min(rect.bottom, gridRect.bottom);
    if (visibleBottom <= visibleTop) {
      continue;
    }
    const distance = Math.abs((visibleTop + visibleBottom) / 2 - probeY);
    if (!nearest || distance < nearest.distance) {
      nearest = { dateKey, distance };
    }
  }
  return nearest?.dateKey ?? null;
}

export function TimelineAllDayLayer({
  items,
  groups,
  filters,
}: TimelineAllDayLayerProps) {
  const { t } = useTranslation('common');
  const [activeDateKey, setActiveDateKey] = useState<string | null>(null);
  const frameRef = useRef<number | null>(null);

  const scheduleRefresh = useCallback(() => {
    if (frameRef.current !== null) {
      return;
    }
    frameRef.current = requestAnimationFrame(() => {
      frameRef.current = null;
      setActiveDateKey(activeTimelineDate());
    });
  }, []);

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

  const visibleItems = useMemo(() => {
    if (!activeDateKey) {
      return [] as VisibleAllDayItem[];
    }
    const groupMap = new Map(groups.map((group) => [group.id, group]));
    return items.flatMap((item) => {
      if (
        !coversDate(item, activeDateKey) ||
        (filters.size > 0 && !filters.has(item.groupId))
      ) {
        return [];
      }
      const group = groupMap.get(item.groupId);
      return [
        {
          item,
          tone: item.appearanceTone ?? group?.tone ?? 'personal',
          groupLabel: group?.label ?? item.groupId,
          startsHere: activeDateKey === item.startDateKey,
          endsHere: isLastCoveredDate(item, activeDateKey),
        },
      ];
    });
  }, [activeDateKey, filters, groups, items]);

  if (!activeDateKey || visibleItems.length === 0) {
    return null;
  }

  const host = document.querySelector<HTMLElement>(
    '.home-timeline-head--production',
  );
  if (!host) {
    return null;
  }

  return createPortal(
    <section
      className="timeline-all-day-strip"
      data-timeline-all-day-strip={activeDateKey}
      aria-label={t(($) => $.common.home.timeline.create.timeSemantics.allDay)}
    >
      <div className="timeline-all-day-strip__label">
        <span>{t(($) => $.common.home.timeline.create.timeSemantics.allDay)}</span>
        <time dateTime={activeDateKey}>{activeDateKey}</time>
      </div>
      <div className="timeline-all-day-strip__items">
        {visibleItems.map(
          ({ item, tone, groupLabel, startsHere, endsHere }) => (
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
              )} · ${groupLabel}`}
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
                {groupLabel}
                {item.meta ? ` · ${item.meta}` : ''}
              </span>
              <span
                className="timeline-all-day-item__continuation"
                aria-hidden="true"
              >
                {endsHere ? '' : '›'}
              </span>
            </button>
          ),
        )}
      </div>
    </section>,
    host,
  );
}
