import { useMemo } from 'react';
import { useTranslation } from 'react-i18next';

import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
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
        <span>
          {t(($) => $.common.home.timeline.create.timeSemantics.allDay)}
        </span>
      </div>

      <div className="timeline-all-day-lane__items">
        {visibleItems.map((item) => {
          const group = groupMap.get(item.groupId);
          const tone = item.appearanceTone ?? group?.tone ?? 'personal';
          const position = timelineAllDayRangePosition(item, dateKey);
          const startsHere = position === 'single' || position === 'start';
          const endsHere = position === 'single' || position === 'end';

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
              data-range-position={position}
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
