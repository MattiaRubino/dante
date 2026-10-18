import {
  offsetTimelineTimeMapper,
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineGroupId,
} from './model/timeline-types';
import type { TimelineRenderedDay } from './timeline-viewport-runtime';

export function applyTimelineAllDayGeometry(
  days: readonly TimelineRenderedDay[],
  items: readonly TimelineAllDayItem[],
  filters: ReadonlySet<TimelineGroupId>,
  alignColumns = false,
): readonly TimelineRenderedDay[] {
  let offsetTop = 0;
  const sharedLaneHeight = alignColumns
    ? Math.max(
        0,
        ...days.map((day) =>
          timelineAllDayLaneHeightPx(
            timelineAllDayItemsForVisibleDate(items, filters, day.dateKey)
              .length,
          ),
        ),
      )
    : 0;

  return days.map((day) => {
    const visibleItems = timelineAllDayItemsForVisibleDate(
      items,
      filters,
      day.dateKey,
    );
    const laneHeight = alignColumns
      ? sharedLaneHeight
      : timelineAllDayLaneHeightPx(visibleItems.length);
    const mapper = offsetTimelineTimeMapper(day.mapper, laneHeight);
    const layouts =
      laneHeight === 0
        ? day.layouts
        : day.layouts.map((layout) =>
            Object.freeze({
              ...layout,
              top: layout.top + laneHeight,
            }),
          );
    const result = Object.freeze({
      ...day,
      mapper,
      layouts,
      offsetTop: alignColumns ? 0 : offsetTop,
      height: mapper.height,
    });
    offsetTop += result.height;
    return result;
  });
}
import { Temporal } from '@dante/time';

import type { TemporalSessionView } from '../../../temporal/remote-session-data-source';

/** Main execution decorates a date-lane plan without rewriting its Schedule.
 * A factual Stop retires only future presentation segments. */
export function projectTimelineDateLaneSessions(
  items: readonly TimelineAllDayItem[],
  sessionsByActivity: ReadonlyMap<string, readonly TemporalSessionView[]>,
  zone: string,
): readonly TimelineAllDayItem[] {
  return items
    .map((item) => {
      const basis = item.canonicalBasis;
      if (basis?.kind !== 'scheduled-activity') return item;
      const sessions = sessionsByActivity.get(basis.activityRef);
      if (!sessions) return item;
      const mains = sessions
        .filter((session) => session.plannedScheduleRef == null)
        .filter((session) => {
          const started = Temporal.Instant.from(session.startedAt)
            .toZonedDateTimeISO(zone)
            .toPlainDate()
            .toString();
          return started < item.endDateExclusiveKey;
        });
      const stopped = mains
        .filter((session) => session.endedAt !== null)
        .sort(
          (left, right) =>
            Date.parse(left.endedAt ?? '') - Date.parse(right.endedAt ?? ''),
        )[0];
      const open = mains.find((session) => session.open);
      const active = open ?? stopped;
      if (!active) return item;
      const stopDate = stopped?.endedAt
        ? Temporal.Instant.from(stopped.endedAt)
            .toZonedDateTimeISO(zone)
            .toPlainDate()
        : null;
      const stopEnd = stopDate?.add({ days: 1 }).toString();
      const endDateExclusiveKey =
        stopEnd && stopEnd < item.endDateExclusiveKey
          ? stopEnd
          : item.endDateExclusiveKey;
      return Object.freeze({
        ...item,
        endDateExclusiveKey,
        plannedEndDateExclusiveKey: item.endDateExclusiveKey,
        mainSession: Object.freeze({
          state: active.open ? (active.paused ? 'paused' : 'running') : 'ended',
          startedAt: active.startedAt,
          endedAt: active.endedAt,
          activeSeconds: active.activeSeconds,
          evaluatedAt: active.evaluatedAt,
        }),
      });
    })
    .filter((item) => item.startDateKey < item.endDateExclusiveKey);
}
