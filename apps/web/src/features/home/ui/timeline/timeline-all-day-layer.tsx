import { useMemo } from 'react';
import { useTranslation } from 'react-i18next';

import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineCoarsePeriod,
  TimelineGroup,
  TimelineGroupId,
} from './model/timeline-types';
import { useTimelineCanonicalActions } from './timeline-canonical-actions';

import './timeline-all-day-layer.css';

type TimelineAllDayLaneProps = Readonly<{
  dateKey: string;
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
}>;

function coarsePeriodLabel(
  period: TimelineCoarsePeriod,
  language: string,
): string {
  const english = language.toLowerCase().startsWith('en');
  if (english) {
    return {
      morning: 'Morning',
      afternoon: 'Afternoon',
      evening: 'Evening',
    }[period];
  }
  return {
    morning: 'Mattina',
    afternoon: 'Pomeriggio',
    evening: 'Sera',
  }[period];
}

export function TimelineAllDayLane({
  dateKey,
  items,
  groups,
  filters,
}: TimelineAllDayLaneProps) {
  const { t, i18n } = useTranslation('common');
  const canonicalActions = useTimelineCanonicalActions();
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

  const language = i18n.resolvedLanguage ?? i18n.language;
  const hasAllDay = visibleItems.some(
    (item) => (item.laneKind ?? 'all-day') === 'all-day',
  );
  const hasCoarse = visibleItems.some((item) => item.laneKind === 'coarse');
  const laneLabel =
    hasAllDay && hasCoarse
      ? language.toLowerCase().startsWith('en')
        ? 'All day · Period'
        : 'Tutto il giorno · Fascia'
      : hasCoarse
        ? language.toLowerCase().startsWith('en')
          ? 'Period'
          : 'Fascia'
        : t(($) => $.common.home.timeline.create.timeSemantics.allDay);

  return (
    <section
      className="timeline-all-day-lane"
      data-timeline-all-day-lane={dateKey}
      aria-label={laneLabel}
      style={{ height: timelineAllDayLaneHeightPx(visibleItems.length) }}
    >
      <div className="timeline-all-day-lane__label">
        <span>{laneLabel}</span>
      </div>

      <div className="timeline-all-day-lane__items">
        {visibleItems.map((item) => {
          const group = groupMap.get(item.groupId);
          const tone = item.appearanceTone ?? group?.tone ?? 'personal';
          const position = timelineAllDayRangePosition(item, dateKey);
          const startsHere = position === 'single' || position === 'start';
          const endsHere = position === 'single' || position === 'end';
          const laneKind = item.laneKind ?? 'all-day';
          const precisionLabel =
            laneKind === 'coarse' && item.coarsePeriod !== undefined
              ? coarsePeriodLabel(item.coarsePeriod, language)
              : t(($) => $.common.home.timeline.create.timeSemantics.allDay);
          const basis = item.canonicalBasis;
          const canUnschedule = basis !== undefined && canonicalActions !== null;
          const pending =
            basis !== undefined &&
            canonicalActions?.pendingScheduleRef === basis.scheduleRef;
          const eventPostpone = basis?.kind === 'scheduled-event';
          const withdrawalLabel = pending
            ? eventPostpone
              ? t(($) => $.common.home.timeline.detail.eventPostponing)
              : t(($) => $.common.home.timeline.detail.unscheduling)
            : eventPostpone
              ? t(($) => $.common.home.timeline.detail.eventPostpone)
              : t(($) => $.common.home.timeline.detail.unschedule);

          return (
            <div className="timeline-all-day-item-row" key={item.id}>
              <button
                className="timeline-all-day-item"
                type="button"
                data-timeline-all-day-item={item.id}
                data-timeline-date-lane-kind={laneKind}
                data-temporal-create-projection={
                  item.origin === 'create' ? item.id : undefined
                }
                data-timeline-tone={tone}
                data-range-position={position}
                data-range-start={startsHere || undefined}
                data-range-end={endsHere || undefined}
                aria-label={`${item.title} · ${precisionLabel} · ${group?.label ?? item.groupId}`}
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
                  {precisionLabel} · {group?.label ?? item.groupId}
                  {item.meta ? ` · ${item.meta}` : ''}
                </span>
                <span
                  className="timeline-all-day-item__continuation"
                  aria-hidden="true"
                >
                  {endsHere ? '' : '›'}
                </span>
              </button>
              {canUnschedule ? (
                <button
                  className="timeline-all-day-item__unschedule"
                  type="button"
                  disabled={pending}
                  data-timeline-unschedule-schedule={basis.scheduleRef}
                  aria-label={`${withdrawalLabel} · ${item.title}`}
                  onClick={() => canonicalActions.unschedule(basis)}
                >
                  {withdrawalLabel}
                </button>
              ) : null}
            </div>
          );
        })}
      </div>
    </section>
  );
}
