import { Temporal } from '@dante/time';

import type { SessionVisual } from '../../../temporal/use-session-panel';
import type { TimelineEvent, TimelineGroup } from './model/timeline-types';
import type { TimelineRenderedDay } from './timeline-day-stream';

export type TimelineSessionReality = Readonly<{
  state: 'running' | 'paused' | 'ended';
  startedAt: string;
  endedAt: string | null;
  fill: string;
  actualLabel: string;
  sessionRefs: readonly string[];
}>;

type Span = Readonly<{ from: number; until: number; paused: boolean }>;
type Projected = Readonly<{ reality: TimelineSessionReality }>;

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
  start: number,
  end: number,
  ranges: readonly Span[],
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
    const covering = ranges.filter(
      (r) => r.from <= midpoint && midpoint < r.until,
    );
    const tone =
      covering.length === 0
        ? UNTRACKED
        : covering.every((r) => r.paused)
          ? PAUSED
          : ACTIVE;
    const p1 = (((from - start) / length) * 100).toFixed(3);
    const p2 = (((to - start) / length) * 100).toFixed(3);
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
  const dayFrom = Temporal.PlainDate.from(dateKey)
    .toZonedDateTime({ timeZone: zone, plainTime: '00:00' })
    .toInstant().epochMilliseconds;
  const dayUntil = Temporal.PlainDate.from(dateKey)
    .add({ days: 1 })
    .toZonedDateTime({ timeZone: zone, plainTime: '00:00' })
    .toInstant().epochMilliseconds;
  // Never bridge two executions on unrelated calendar days with a fake
  // all-day interval merely because they share the same Activity identity.
  const relevant = slices.filter((slice) => {
    const start = Date.parse(slice.started_at);
    const end = slice.ended_at ? Date.parse(slice.ended_at) : clockAt;
    return (
      Number.isFinite(start) &&
      Number.isFinite(end) &&
      end > dayFrom &&
      start < dayUntil
    );
  });
  if (relevant.length === 0) return null;
  const mains = relevant.filter((slice) => slice.planned_schedule_ref === null);
  // When there is a main real Session it determines outer geometry, not the
  // sum of overlapping internal executions.
  const chosen = mains.length > 0 ? mains : relevant;
  const spans: Span[] = [];
  for (const slice of chosen) {
    const first = Date.parse(slice.started_at);
    const last = slice.ended_at ? Date.parse(slice.ended_at) : clockAt;
    if (!Number.isFinite(first) || !Number.isFinite(last) || last <= first)
      continue;
    const pauses = [...slice.pause_ranges]
      .map((p) => ({
        from: bounded(Date.parse(p.started_at), first, last),
        until: bounded(p.ended_at ? Date.parse(p.ended_at) : last, first, last),
      }))
      .filter((p) => p.until > p.from)
      .sort((a, b) => a.from - b.from);
    let cursor = first;
    for (const pause of pauses) {
      if (pause.from > cursor)
        spans.push({ from: cursor, until: pause.from, paused: false });
      spans.push({ from: pause.from, until: pause.until, paused: true });
      cursor = Math.max(cursor, pause.until);
    }
    if (cursor < last) spans.push({ from: cursor, until: last, paused: false });
  }
  if (spans.length === 0) return null;
  const startAt = Math.min(...spans.map((r) => r.from));
  const endAt = Math.max(...spans.map((r) => r.until));
  if (endAt <= dayFrom || startAt >= dayUntil) return null;
  const visibleStart = Math.max(dayFrom, startAt);
  const visibleEnd = Math.min(dayUntil, endAt);
  const fill = colorSegments(visibleStart, visibleEnd, spans);
  const running = chosen.some((r) => r.ended_at === null);
  const paused =
    running &&
    chosen.every(
      (r) =>
        r.ended_at !== null || r.pause_ranges.some((p) => p.ended_at === null),
    );
  const startedAt = new Date(startAt).toISOString();
  const endedAt = running ? null : new Date(endAt).toISOString();
  return {
    reality: {
      state: !running ? 'ended' : paused ? 'paused' : 'running',
      startedAt,
      endedAt,
      fill,
      sessionRefs: chosen.map((slice) => slice.session_ref),
      actualLabel: `${labelAt(startedAt, zone)}–${endedAt ? labelAt(endedAt, zone) : 'ora'}`,
    },
  };
}

/**
 * Adds actual Session state to the planned card without changing its Timeline
 * geometry. A short live Session must never magnify minute density, card
 * height, lanes, or following-day offsets.
 */
export function applyTimelineSessionReality(
  days: readonly TimelineRenderedDay[],
  visuals: readonly SessionVisual[],
  zone: string,
  evaluatedAt: string,
  clockAt: number,
  _groups: readonly TimelineGroup[],
  _zoom: number,
  _expandedEventIds: ReadonlySet<string>,
): readonly TimelineRenderedDay[] {
  if (visuals.length === 0) return days;
  const now = Number.isFinite(Date.parse(evaluatedAt)) ? clockAt : Date.now();
  const byActivity = new Map<string, SessionVisual[]>();
  for (const visual of visuals) {
    const list = byActivity.get(visual.activity_ref) ?? [];
    list.push(visual);
    byActivity.set(visual.activity_ref, list);
  }

  let offsetTop = 0;
  return days.map((day) => {
    const activityEvents = new Map<string, TimelineEvent[]>();
    for (const event of day.events) {
      if (event.canonicalBasis?.kind !== 'scheduled-activity') continue;
      const key = event.canonicalBasis.activityRef;
      activityEvents.set(key, [...(activityEvents.get(key) ?? []), event]);
    }

    const overlays = new Map<string, Projected>();
    for (const event of day.events) {
      const basis = event.canonicalBasis;
      if (basis?.kind !== 'scheduled-activity') continue;
      const activity = byActivity.get(basis.activityRef) ?? [];
      const intervals = activityEvents.get(basis.activityRef) ?? [];
      // A real Session is attached to one visible planned interval, including
      // when it starts early or ends before that interval begins.
      const relevant =
        intervals.length === 1
          ? activity
          : activity.filter((slice) => {
              if (slice.planned_schedule_ref === basis.scheduleRef) return true;
              const minute = onDay(slice.started_at, day.dateKey, zone);
              const nearest = [...intervals].sort(
                (a, b) =>
                  Math.abs(a.startMinute - minute) -
                    Math.abs(b.startMinute - minute) ||
                  a.id.localeCompare(b.id),
              )[0];
              return nearest?.id === event.id;
            });
      const projected = project(relevant, day.dateKey, zone, now);
      if (projected) overlays.set(event.id, projected);
    }

    const layouts = day.layouts.map((layout) => {
      const reality = overlays.get(layout.event.id);
      return reality
        ? { ...layout, sessionReality: reality.reality }
        : layout;
    });
    const rendered = { ...day, layouts, offsetTop };
    offsetTop += day.height;
    return rendered;
  });
}
