import { Temporal } from '@dante/time';
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

type AllDayTarget = Readonly<{
  item: TimelineAllDayItem;
  dateKey: string;
  host: HTMLElement;
  lane: number;
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

export function TimelineAllDayLayer({
  items,
  groups,
  filters,
}: TimelineAllDayLayerProps) {
  const { t } = useTranslation('common');
  const [layoutRevision, setLayoutRevision] = useState(0);
  const frameRef = useRef<number | null>(null);

  const scheduleRefresh = useCallback(() => {
    if (frameRef.current !== null) {
      return;
    }
    frameRef.current = requestAnimationFrame(() => {
      frameRef.current = null;
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
    const observer = new MutationObserver(scheduleRefresh);
    observer.observe(root, { childList: true, subtree: true });
    root.addEventListener('scroll', scheduleRefresh, true);
    window.addEventListener('resize', scheduleRefresh);
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

  const targets = useMemo(() => {
    void layoutRevision;
    if (typeof document === 'undefined' || items.length === 0) {
      return [] as AllDayTarget[];
    }

    const groupMap = new Map(groups.map((group) => [group.id, group]));
    const sections = Array.from(
      document.querySelectorAll<HTMLElement>(
        '.timeline-day-section[data-timeline-date]',
      ),
    );
    const result: AllDayTarget[] = [];

    for (const section of sections) {
      const dateKey = section.dataset.timelineDate;
      if (!dateKey) {
        continue;
      }
      let lane = 0;
      for (const item of items) {
        if (
          !coversDate(item, dateKey) ||
          (filters.size > 0 && !filters.has(item.groupId))
        ) {
          continue;
        }
        const group = groupMap.get(item.groupId);
        result.push({
          item,
          dateKey,
          host: section,
          lane,
          tone: item.appearanceTone ?? group?.tone ?? 'personal',
          groupLabel: group?.label ?? item.groupId,
          startsHere: dateKey === item.startDateKey,
          endsHere: isLastCoveredDate(item, dateKey),
        });
        lane += 1;
      }
    }

    return result;
  }, [filters, groups, items, layoutRevision]);

  return (
    <>
      {targets.map(
        ({
          item,
          dateKey,
          host,
          lane,
          tone,
          groupLabel,
          startsHere,
          endsHere,
        }) =>
          createPortal(
            <button
              className="timeline-all-day-item"
              type="button"
              data-timeline-all-day-item={item.id}
              data-temporal-create-projection={
                item.origin === 'create' ? item.id : undefined
              }
              data-timeline-tone={tone}
              data-range-start={startsHere || undefined}
              data-range-end={endsHere || undefined}
              style={{ '--timeline-all-day-lane': lane } as CSSProperties}
              aria-label={`${item.title} · ${t(
                ($) => $.common.home.timeline.create.timeSemantics.allDay,
              )} · ${groupLabel}`}
              onClick={(event) => event.currentTarget.focus()}
            >
              <span className="timeline-all-day-item__continuation" aria-hidden="true">
                {startsHere ? '' : '‹'}
              </span>
              <strong>{item.title}</strong>
              <span className="timeline-all-day-item__meta">
                {groupLabel}
                {item.meta ? ` · ${item.meta}` : ''}
              </span>
              <span className="timeline-all-day-item__continuation" aria-hidden="true">
                {endsHere ? '' : '›'}
              </span>
            </button>,
            host,
            `${item.id}:${dateKey}`,
          ),
      )}
    </>
  );
}
