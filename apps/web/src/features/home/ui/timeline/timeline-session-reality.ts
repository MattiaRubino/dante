import { Temporal } from '@dante/time';

import type { SessionVisual } from '../../../temporal/use-session-panel';
import type { TemporalSessionView } from '../../../temporal/remote-session-data-source';
import { createTimelineTimeMapper } from './model/timeline-density';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type { TimelineGroup } from './model/timeline-types';
import type { TimelineRenderedDay } from './timeline-day-stream';
import { createTimelineSharedWeekMapper } from './timeline-viewport-runtime';

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
const PAUSED = 'rgba(234, 92, 18, .12)';
const UNTRACKED = 'rgba(234, 92, 18, .04)';

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
  // Only the Activity's own Session belongs on the Activity card. Named
  // planned Sessions keep their separate controls in the Session panel.
  const chosen = relevant
    .filter((slice) => slice.planned_schedule_ref === null)
    .sort((a, b) => Date.parse(b.started_at) - Date.parse(a.started_at))
    .slice(0, 1);
  if (chosen.length === 0) return null;
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

/** Project execution over the unchanged plan-derived time scale. Starting
 * moves the card; only an ended attempt changes its visible duration. */
export function applyTimelineSessionReality(
  days: readonly TimelineRenderedDay[],
  visuals: readonly SessionVisual[],
  zone: string,
  evaluatedAt: string,
  clockAt: number,
  groups: readonly TimelineGroup[],
  zoom: number,
  expandedEventIds: ReadonlySet<string>,
  sessionsByActivity: ReadonlyMap<
    string,
    readonly TemporalSessionView[]
  > = new Map(),
): readonly TimelineRenderedDay[] {
  if (visuals.length === 0 && sessionsByActivity.size === 0) return days;
  const now = Number.isFinite(Date.parse(evaluatedAt)) ? clockAt : Date.now();
  const visualRefs = new Set(visuals.map((visual) => visual.session_ref));
  const executionVisuals: readonly SessionVisual[] = [
    ...visuals,
    ...[...sessionsByActivity].flatMap(([activityRef, sessions]) =>
      sessions
        .filter(
          (session) =>
            session.plannedScheduleRef == null &&
            !visualRefs.has(session.sessionRef),
        )
        .map((session) => ({
          activity_ref: activityRef,
          session_ref: session.sessionRef,
          planned_schedule_ref: null,
          started_at: session.startedAt,
          ended_at: session.endedAt,
          pause_ranges: [],
        })),
    ),
  ];
  const allEvents = days.flatMap((day) =>
    day.events.map((event) => ({ event, plannedDay: day })),
  );
  const plannedAt = (entry: (typeof allEvents)[number]) =>
    Temporal.PlainDate.from(entry.plannedDay.dateKey)
      .toZonedDateTime({ timeZone: zone, plainTime: '00:00' })
      .toInstant().epochMilliseconds +
    entry.event.startMinute * 60_000;
  const openActivities = new Set<string>();
  const stoppedAt = new Map<string, number>();
  const record = (activityRef: string, endedAt: string | null) => {
    if (endedAt === null) {
      openActivities.add(activityRef);
      return;
    }
    const value = Date.parse(endedAt);
    if (Number.isFinite(value))
      stoppedAt.set(
        activityRef,
        Math.max(stoppedAt.get(activityRef) ?? -Infinity, value),
      );
  };
  for (const visual of executionVisuals)
    if (visual.planned_schedule_ref === null)
      record(visual.activity_ref, visual.ended_at);
  for (const [activityRef, sessions] of sessionsByActivity)
    for (const session of sessions)
      if (session.plannedScheduleRef == null)
        record(activityRef, session.endedAt);
  for (const activityRef of openActivities) stoppedAt.delete(activityRef);
  const mainByEvent = new Map<string, SessionVisual>();
  for (const visual of executionVisuals) {
    if (visual.planned_schedule_ref !== null) continue;
    const started = Date.parse(visual.started_at);
    if (!Number.isFinite(started)) continue;
    const candidates = allEvents.filter(
      ({ event }) =>
        event.canonicalBasis?.kind === 'scheduled-activity' &&
        event.canonicalBasis.activityRef === visual.activity_ref,
    );
    const nearest = candidates.sort((a, b) => {
      return (
        Math.abs(plannedAt(a) - started) - Math.abs(plannedAt(b) - started) ||
        a.event.id.localeCompare(b.event.id)
      );
    })[0];
    if (!nearest) continue;
    const previous = mainByEvent.get(nearest.event.id);
    if (!previous || Date.parse(previous.started_at) < started)
      mainByEvent.set(nearest.event.id, visual);
  }

  const retiredIds = new Set(
    allEvents
      .filter((entry) => {
        const basis = entry.event.canonicalBasis;
        if (
          basis?.kind !== 'scheduled-activity' ||
          mainByEvent.has(entry.event.id)
        )
          return false;
        const stop = stoppedAt.get(basis.activityRef);
        return stop !== undefined && plannedAt(entry) > stop;
      })
      .map(({ event }) => event.id),
  );

  const placements = allEvents
    .filter(({ event }) => !retiredIds.has(event.id))
    .map(({ event, plannedDay }) => {
      const visual = mainByEvent.get(event.id);
      const realDate = visual
        ? Temporal.Instant.from(visual.started_at)
            .toZonedDateTimeISO(zone)
            .toPlainDate()
            .toString()
        : plannedDay.dateKey;
      const displayDay = days.find((day) => day.dateKey === realDate);
      const target = displayDay ?? plannedDay;
      const overlay = visual
        ? project([visual], target.dateKey, zone, now)
        : null;
      return { event, plannedDay, target, reality: overlay?.reality };
    });

  const prepared = days.map((day) => {
    const visible = placements.filter((placement) => placement.target === day);
    const displayEvents = visible.map(({ event, reality }) => {
      if (!reality) return event;
      const startMinute = onDay(reality.startedAt, day.dateKey, zone);
      const duration = event.endMinute - event.startMinute;
      const endMinute =
        reality.endedAt === null
          ? startMinute + duration
          : onDay(reality.endedAt, day.dateKey, zone);
      return {
        ...event,
        startMinute,
        endMinute: Math.max(startMinute + 1 / 60, Math.min(1440, endMinute)),
        // Stop can turn a 30-minute Activity into a five-second factual
        // interval. The card still contains planned/actual labels and
        // optional Session/Objective badges. Reserve a readable presentation
        // floor within the precise second-level local time stretch rather
        // than clipping these rows or altering the canonical Schedule.
        ...(reality.endedAt !== null && endMinute - startMinute < 5
          ? {
              visualMinimumHeightPx: Math.max(
                event.visualMinimumHeightPx ?? 0,
                168,
              ),
            }
          : {}),
      };
    });
    return { day, visible, displayEvents };
  });
  // The clock never changes the scale while an attempt is running/paused.
  // Once stopped, the real interval owns its readable height: recomputing at
  // that transition prevents a short card from painting beyond its end time.
  const hasEnded =
    retiredIds.size > 0 ||
    prepared.some(({ visible }) =>
      visible.some(({ reality }) => reality?.endedAt != null),
    );
  const endedIds = new Set(
    placements
      .filter(({ reality }) => reality?.endedAt != null)
      .map(({ event }) => event.id),
  );
  const densityEvents = prepared.map(({ day, visible, displayEvents }) => [
    ...day.events.filter(
      (event) => !endedIds.has(event.id) && !retiredIds.has(event.id),
    ),
    ...displayEvents.filter(
      (event, index) => visible[index]?.reality?.endedAt != null,
    ),
  ]);
  const isWeek =
    days.length === 7 && days.every((candidate) => candidate.offsetTop === 0);
  const weekMapper =
    hasEnded && isWeek
      ? createTimelineSharedWeekMapper(densityEvents, zoom, expandedEventIds)
      : null;
  let offsetTop = 0;
  return prepared.map(({ day, visible, displayEvents }, index) => {
    const dayChanged =
      densityEvents[index]?.some((event) => endedIds.has(event.id)) ||
      day.events.some(
        (event) => endedIds.has(event.id) || retiredIds.has(event.id),
      );
    const mapper =
      weekMapper ??
      (hasEnded && dayChanged
        ? createTimelineTimeMapper(densityEvents[index] ?? [], zoom, {
            expandedEventIds,
          })
        : day.mapper);
    // Reassign collision lanes using the rectangles that are actually painted,
    // while preserving canonical event identity and the planned Schedule.
    // Collision detection must use the *painted* height, not just the
    // shifted clock duration. During Play/Pause the card intentionally keeps
    // its original planned height, which may extend past the short actual
    // interval and would otherwise overlap a neighbor assigned to its lane.
    // This visual floor is fed only to packing, NEVER the time mapper: the
    // clock's elastic scale must remain stable during live execution.
    const paintSizedEvents = displayEvents.map((event, eventIndex) => {
      const placement = visible[eventIndex];
      if (!placement?.reality || placement.reality.endedAt !== null)
        return event;
      const plannedHeight = placement.plannedDay.layouts.find(
        (candidate) => candidate.event.id === event.id,
      )?.height;
      if (plannedHeight === undefined) return event;
      return {
        ...event,
        visualMinimumHeightPx: Math.max(
          event.visualMinimumHeightPx ?? 0,
          plannedHeight,
        ),
      };
    });
    const displayed = computeTimelineEventLayouts(
      paintSizedEvents,
      groups,
      mapper,
    );
    const layouts = displayed.map((layout, index) => {
      const placement = visible[index];
      const planned = placement?.event ?? layout.event;
      const reality = placement?.reality;
      if (!reality) return { ...layout, event: planned };
      const plannedLayout = placement.plannedDay.layouts.find(
        (candidate) => candidate.event.id === planned.id,
      );
      return {
        ...layout,
        event: planned,
        plannedDateKey: placement.plannedDay.dateKey,
        // Play/Pause never resize; Stop maps the factual interval. The minimum
        // readable card height remains a purely visual floor for tiny attempts.
        height:
          reality.endedAt === null
            ? (plannedLayout?.height ?? layout.height)
            : layout.height,
        sessionReality: reality,
      };
    });
    const rendered = {
      ...day,
      events: visible.map((entry) => entry.event),
      mapper,
      layouts,
      offsetTop: isWeek ? 0 : offsetTop,
      height: mapper.height,
    };
    offsetTop += mapper.height;
    return rendered;
  });
}
