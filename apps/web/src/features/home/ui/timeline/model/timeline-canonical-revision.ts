import { Temporal, type Instant, type PlainDateTime } from '@dante/time';

import type {
  TemporalScheduleDisambiguation,
  TemporalSchedulePlacementInput,
} from '../../../../temporal/schedule-data-source';
import type {
  TimelineCanonicalScheduleBasis,
  TimelineCanonicalSchedulePlacement,
} from './timeline-types';

export type TimelineCanonicalDisplayEdit = Readonly<{
  basis: TimelineCanonicalScheduleBasis;
  fromDateKey: string;
  previousStartMinute: number;
  previousEndMinute: number;
  toDateKey: string;
  startMinute: number;
  endMinute: number;
  effectiveZoneId: string;
}>;

export type TimelineCanonicalRevision = Readonly<{
  previous: TemporalSchedulePlacementInput;
  next: TemporalSchedulePlacementInput;
}>;

function localDateTimeAtMinute(dateKey: string, minute: number): PlainDateTime {
  if (!Number.isFinite(minute) || minute < 0 || minute > 1440) {
    throw new RangeError('Timeline minute must remain inside one civil day.');
  }
  return Temporal.PlainDate.from(dateKey)
    .toPlainDateTime()
    .add({ minutes: minute });
}

function wallMinuteDelta(from: PlainDateTime, to: PlainDateTime): number {
  const difference = from.until(to, { largestUnit: 'days' });
  return (
    difference.days * 1440 +
    difference.hours * 60 +
    difference.minutes +
    difference.seconds / 60 +
    difference.milliseconds / 60_000 +
    difference.microseconds / 60_000_000 +
    difference.nanoseconds / 60_000_000_000
  );
}

function resolveLocal(
  local: PlainDateTime,
  zoneId: string,
  disambiguation: TemporalScheduleDisambiguation,
): Instant | null {
  try {
    return local.toZonedDateTime(zoneId, { disambiguation }).toInstant();
  } catch {
    return null;
  }
}

function commonDisambiguation(
  startsLocalAt: PlainDateTime,
  endsLocalAt: PlainDateTime,
  zoneId: string,
  resolvedStartAt: Instant,
  resolvedEndAt: Instant,
): TemporalScheduleDisambiguation | null {
  for (const disambiguation of ['reject', 'earlier', 'later'] as const) {
    const start = resolveLocal(startsLocalAt, zoneId, disambiguation);
    const end = resolveLocal(endsLocalAt, zoneId, disambiguation);
    if (
      start !== null &&
      end !== null &&
      start.equals(resolvedStartAt) &&
      end.equals(resolvedEndAt)
    ) {
      return disambiguation;
    }
  }
  return null;
}

function acceptedPlacementInput(
  placement: TimelineCanonicalSchedulePlacement,
): TemporalSchedulePlacementInput | null {
  switch (placement.kind) {
    case 'date-span':
      return Object.freeze({
        kind: 'date-span' as const,
        startDate: placement.startDate,
        endDateExclusive: placement.endDateExclusive,
      });
    case 'floating-local':
      return Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt: placement.startsLocalAt,
        endsLocalAt: placement.endsLocalAt,
      });
    case 'named-zone-local': {
      const disambiguation = commonDisambiguation(
        placement.startsLocalAt,
        placement.endsLocalAt,
        placement.zoneId,
        placement.resolvedStartAt,
        placement.resolvedEndAt,
      );
      return disambiguation === null
        ? null
        : Object.freeze({
            kind: 'named-zone-local-interval' as const,
            startsLocalAt: placement.startsLocalAt,
            endsLocalAt: placement.endsLocalAt,
            zoneId: placement.zoneId,
            disambiguation,
          });
    }
    case 'absolute':
      return Object.freeze({
        kind: 'absolute-interval' as const,
        startsAt: placement.startsAt,
        endsAt: placement.endsAt,
      });
    case 'coarse-local-period':
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: placement.localDate,
        period: placement.period,
      });
  }
}

function exactDisplayInterval(
  placement: TimelineCanonicalSchedulePlacement,
  effectiveZoneId: string,
): Readonly<{ start: PlainDateTime; end: PlainDateTime }> | null {
  switch (placement.kind) {
    case 'floating-local':
      return Object.freeze({
        start: placement.startsLocalAt,
        end: placement.endsLocalAt,
      });
    case 'named-zone-local':
      return Object.freeze({
        start: placement.resolvedStartAt
          .toZonedDateTimeISO(effectiveZoneId)
          .toPlainDateTime(),
        end: placement.resolvedEndAt
          .toZonedDateTimeISO(effectiveZoneId)
          .toPlainDateTime(),
      });
    case 'absolute':
      return Object.freeze({
        start: placement.startsAt
          .toZonedDateTimeISO(effectiveZoneId)
          .toPlainDateTime(),
        end: placement.endsAt
          .toZonedDateTimeISO(effectiveZoneId)
          .toPlainDateTime(),
      });
    case 'date-span':
    case 'coarse-local-period':
      return null;
  }
}

function namedZoneInputFromDisplay(
  start: PlainDateTime,
  end: PlainDateTime,
  effectiveZoneId: string,
  sourceZoneId: string,
): TemporalSchedulePlacementInput | null {
  const resolvedStartAt = resolveLocal(start, effectiveZoneId, 'reject');
  const resolvedEndAt = resolveLocal(end, effectiveZoneId, 'reject');
  if (
    resolvedStartAt === null ||
    resolvedEndAt === null ||
    Temporal.Instant.compare(resolvedStartAt, resolvedEndAt) >= 0
  ) {
    return null;
  }

  const startsLocalAt = resolvedStartAt
    .toZonedDateTimeISO(sourceZoneId)
    .toPlainDateTime();
  const endsLocalAt = resolvedEndAt
    .toZonedDateTimeISO(sourceZoneId)
    .toPlainDateTime();
  const disambiguation = commonDisambiguation(
    startsLocalAt,
    endsLocalAt,
    sourceZoneId,
    resolvedStartAt,
    resolvedEndAt,
  );
  if (disambiguation === null) {
    return null;
  }

  return Object.freeze({
    kind: 'named-zone-local-interval' as const,
    startsLocalAt,
    endsLocalAt,
    zoneId: sourceZoneId,
    disambiguation,
  });
}

function absoluteInputFromDisplay(
  start: PlainDateTime,
  end: PlainDateTime,
  effectiveZoneId: string,
): TemporalSchedulePlacementInput | null {
  const startsAt = resolveLocal(start, effectiveZoneId, 'reject');
  const endsAt = resolveLocal(end, effectiveZoneId, 'reject');
  if (
    startsAt === null ||
    endsAt === null ||
    Temporal.Instant.compare(startsAt, endsAt) >= 0
  ) {
    return null;
  }
  return Object.freeze({
    kind: 'absolute-interval' as const,
    startsAt,
    endsAt,
  });
}

export function timelineCanonicalRevisionForDisplayEdit(
  edit: TimelineCanonicalDisplayEdit,
): TimelineCanonicalRevision | null {
  const display = exactDisplayInterval(
    edit.basis.placement,
    edit.effectiveZoneId,
  );
  const previous = acceptedPlacementInput(edit.basis.placement);
  if (display === null || previous === null) {
    return null;
  }

  let previousSegmentStart: PlainDateTime;
  let previousSegmentEnd: PlainDateTime;
  let requestedSegmentStart: PlainDateTime;
  let requestedSegmentEnd: PlainDateTime;
  try {
    previousSegmentStart = localDateTimeAtMinute(
      edit.fromDateKey,
      edit.previousStartMinute,
    );
    previousSegmentEnd = localDateTimeAtMinute(
      edit.fromDateKey,
      edit.previousEndMinute,
    );
    requestedSegmentStart = localDateTimeAtMinute(
      edit.toDateKey,
      edit.startMinute,
    );
    requestedSegmentEnd = localDateTimeAtMinute(
      edit.toDateKey,
      edit.endMinute,
    );
  } catch {
    return null;
  }

  const startDelta = wallMinuteDelta(
    previousSegmentStart,
    requestedSegmentStart,
  );
  const endDelta = wallMinuteDelta(previousSegmentEnd, requestedSegmentEnd);
  const requestedStart = display.start.add({ minutes: startDelta });
  const requestedEnd = display.end.add({ minutes: endDelta });

  let next: TemporalSchedulePlacementInput | null;
  switch (edit.basis.placement.kind) {
    case 'floating-local':
      next =
        Temporal.PlainDateTime.compare(requestedStart, requestedEnd) < 0
          ? Object.freeze({
              kind: 'floating-local-interval' as const,
              startsLocalAt: requestedStart,
              endsLocalAt: requestedEnd,
            })
          : null;
      break;
    case 'named-zone-local':
      next = namedZoneInputFromDisplay(
        requestedStart,
        requestedEnd,
        edit.effectiveZoneId,
        edit.basis.placement.zoneId,
      );
      break;
    case 'absolute':
      next = absoluteInputFromDisplay(
        requestedStart,
        requestedEnd,
        edit.effectiveZoneId,
      );
      break;
    case 'date-span':
    case 'coarse-local-period':
      next = null;
      break;
  }

  return next === null ? null : Object.freeze({ previous, next });
}
