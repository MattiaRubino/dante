import { Temporal } from '@dante/time';

import type { SessionVisual } from '../../../temporal/use-session-panel';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type {
  TimelineEvent, TimelineEventLayout, TimelineGroup, TimelineTimeMapper,
} from './model/timeline-types';
import type { TimelineRenderedDay } from './timeline-day-stream';

export type TimelineSessionReality = Readonly<{
  state: 'running' | 'paused' | 'ended';
  startedAt: string;
  endedAt: string | null;
  fill: string;
  actualLabel: string;
}>;

type Span = Readonly<{ from: number; until: number; paused: boolean }>;
type Projected = Readonly<{
  startMinute: number;
  endMinute: number;
  reality: TimelineSessionReality;
}>;

const ACTIVE = 'rgba(234, 92, 18, .25)';
const PAUSED = 'rgba(147, 163, 184, .30)';
const UNTRACKED = 'rgba(147, 163, 184, .07)';

function bounded(n: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, n));
}

function minutesAt(instant: string, zone: string): number {
  const local = Temporal.Instant.from(instant).toZonedDateTimeISO(zone);
  return local.hour * 60 + local.minute + local.second / 60;
}

function labelAt(instant: string, zone: string): string {
  const local = Temporal.Instant.from(instant).toZonedDateTimeISO(zone);
  return `${String(local.hour).padStart(2, '0')}:${String(local.minute).padStart(2, '0')}`;
}

function onDay(instant: string, dateKey: string, zone: string): number {
  const local = Temporal.Instant.from(instant).toZonedDateTimeISO(zone);
  const date = local.toPlainDate().toString();
  if (date < dateKey) return 0;
  if (date > dateKey) return 1440;
  return bounded(minutesAt(instant, zone), 0, 1440);
}

function colorSegments(
  start: number, end: number, ranges: readonly Span[],
): string {
  const length = Math.max(1, end - start);
  const boundaries = new Set([start, end]);
  for (const span of ranges) {
    boundaries.add(bounded(span.from, start, end));
    boundaries.add(bounded(span.until, start, end));
  }
  const edges = [...boundaries].sort((a, b) => a - b);
  const stops: string[] = [];
  for (let i = 0; i < edges.length - 1; i += 1) {
    const from = edges[i] ?? start;
    const to = edges[i + 1] ?? end;
    if (to <= from) continue;
    const midpoint = (from + to) / 2;
    const covering = ranges.filter((r) => r.from <= midpoint && midpoint < r.until);
    const tone = covering.length === 0 ? UNTRACKED
      : covering.every((r) => r.paused) ? PAUSED : ACTIVE;
    const p1 = ((from - start) / length * 100).toFixed(3);
    const p2 = ((to - start) / length * 100).toFixed(3);
    stops.push(`${tone} ${p1}%`, `${tone} ${p2}%`);
  }
  return `linear-gradient(to bottom, ${stops.join(', ') || `${UNTRACKED} 0%, ${UNTRACKED} 100%`})`;
}

function project(
  slices: readonly SessionVisual[],
  dateKey: string,
  zone: string,
  clockAt: number,
): Projected | null {
  if (slices.length === 0) return null;
  const mains = slices.filter((slice) => slice.planned_schedule_ref === null);
  // When there is a main real Session it determines outer geometry, not the
  // sum of overlapping internal executions.
  const chosen = mains.length > 0 ? mains : slices;
  const spans: Span[] = [];
  for (const slice of chosen) {
    const first = Date.parse(slice.started_at);
    const last = slice.ended_at ? Date.parse(slice.ended_at) : clockAt;
    if (!Number.isFinite(first) || !Number.isFinite(last) || last <= first) continue;
    const pauses = [...slice.pause_ranges]
      .map((p) => ({
        from: bounded(Date.parse(p.started_at), first, last),
        until: bounded(p.ended_at ? Date.parse(p.ended_at) : last, first, last),
      }))
      .filter((p) => p.until > p.from)
      .sort((a, b) => a.from - b.from);
    let cursor = first;
    for (const pause of pauses) {
      if (pause.from > cursor) spans.push({ from: cursor, until: pause.from, paused: false });
      spans.push({ from: pause.from, until: pause.until, paused: true });
      cursor = Math.max(cursor, pause.until);
    }
    if (cursor < last) spans.push({ from: cursor, until: last, paused: false });
  }
  if (spans.length === 0) return null;
  const startAt = Math.min(...spans.map((r) => r.from));
  const endAt = Math.max(...spans.map((r) => r.until));
  const dayFrom = Temporal.PlainDate.from(dateKey)
    .toZonedDateTime({ timeZone: zone, plainTime: '00:00' }).toInstant().epochMilliseconds;
  const dayUntil = Temporal.PlainDate.from(dateKey).add({ days: 1 })
    .toZonedDateTime({ timeZone: zone, plainTime: '00:00' }).toInstant().epochMilliseconds;
  if (endAt <= dayFrom || startAt >= dayUntil) return null;
  const visibleStart = Math.max(dayFrom, startAt);
  const visibleEnd = Math.min(dayUntil, endAt);
  const fill = colorSegments(visibleStart, visibleEnd, spans);
  const running = chosen.some((r) => r.ended_at === null);
  const paused = running && chosen.every((r) =>
    r.ended_at !== null || r.pause_ranges.some((p) => p.ended_at === null));
  const startedAt = new Date(startAt).toISOString();
  const endedAt = running ? null : new Date(endAt).toISOString();
  const first = onDay(startedAt, dateKey, zone);
  const last = onDay(new Date(endAt).toISOString(), dateKey, zone);
  return {
    startMinute: first,
    endMinute: Math.max(first + 1 / 60, last),
    reality: {
      state: !running ? 'ended' : paused ? 'paused' : 'running',
      startedAt, endedAt, fill,
      actualLabel: `${labelAt(startedAt, zone)}–${endedAt ? labelAt(endedAt, zone) : 'ora'}`,
    },
  };
}

/**
 * Only modifies view geometry. The original event/canonicalBasis is retained
 * in every resulting layout, including all scheduling and mutation handlers.
 */
export function applyTimelineSessionReality(
  days: readonly TimelineRenderedDay[],
  visuals: readonly SessionVisual[],
  zone: string,
  evaluatedAt: string,
  clockAt: number,
  groups: readonly TimelineGroup[],
): readonly TimelineRenderedDay[] {
  if (visuals.length === 0) return days;
  const now = Number.isFinite(Date.parse(evaluatedAt))
    ? Date.parse(evaluatedAt) + Math.max(0, clockAt - Date.parse(evaluatedAt))
    : clockAt;
  const byActivity = new Map<string, SessionVisual[]>();
  for (const visual of visuals) {
    const list = byActivity.get(visual.activity_ref) ?? [];
    list.push(visual);
    byActivity.set(visual.activity_ref, list);
  }
  return days.map((day) => {
    const activityCounts = new Map<string, number>();
    for (const event of day.events) {
      if (event.canonicalBasis?.kind !== 'scheduled-activity') continue;
      const key = event.canonicalBasis.activityRef;
      activityCounts.set(key, (activityCounts.get(key) ?? 0) + 1);
    }
    const overlays = new Map<string, Projected>();
    const displayEvents: TimelineEvent[] = day.events.map((event) => {
      const basis = event.canonicalBasis;
      if (basis?.kind !== 'scheduled-activity') return event;
      const activity = byActivity.get(basis.activityRef);
      if (!activity) return event;
      const projected = project(activity, day.dateKey, zone, now);
      if (!projected) return event;
      // Several independent accepted Activity intervals share one Activity
      // identity: never merge their technical-envelope gaps into one block.
      if ((activityCounts.get(basis.activityRef) ?? 0) > 1) {
        if (projected.endMinute <= event.startMinute ||
            projected.startMinute >= event.endMinute) return event;
        overlays.set(event.id, projected);
        return event;
      }
      overlays.set(event.id, projected);
      return {
        ...event,
        startMinute: projected.startMinute,
        endMinute: projected.endMinute,
      };
    });
    if (overlays.size === 0) return day;
    const mapped = computeTimelineEventLayouts(displayEvents, groups, day.mapper);
    const layouts: TimelineEventLayout[] = day.layouts.map((old, index) => {
      const target = mapped[index];
      if (!target) return old;
      const reality = overlays.get(old.event.id);
      if (!reality) return {
        ...old,
        compactLane: target.compactLane, compactLaneCount: target.compactLaneCount,
        compactLeftPercent: target.compactLeftPercent,
        compactWidthPercent: target.compactWidthPercent,
        groupLane: target.groupLane, groupLaneCount: target.groupLaneCount,
      };
      const canMove = (activityCounts.get(
        old.event.canonicalBasis?.kind === 'scheduled-activity'
          ? old.event.canonicalBasis.activityRef : '',
      ) ?? 0) === 1;
      const top = canMove
        ? old.top + day.mapper.map(reality.startMinute) - day.mapper.map(old.event.startMinute)
        : old.top;
      return {
        ...old, top: Math.max(0, top),
        height: canMove ? Math.max(24, day.mapper.map(reality.endMinute) -
          day.mapper.map(reality.startMinute)) : old.height,
        compactLane: target.compactLane, compactLaneCount: target.compactLaneCount,
        compactLeftPercent: target.compactLeftPercent,
        compactWidthPercent: target.compactWidthPercent,
        groupLane: target.groupLane, groupLaneCount: target.groupLaneCount,
        sessionReality: reality.reality,
      };
    });
    return { ...day, layouts };
  });
}
