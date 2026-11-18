import { Temporal } from 'temporal-polyfill';

export { Temporal };

export type Instant = Temporal.Instant;
export type PlainDate = Temporal.PlainDate;
export type PlainTime = Temporal.PlainTime;
export type PlainDateTime = Temporal.PlainDateTime;
export type ZonedDateTime = Temporal.ZonedDateTime;
export type Duration = Temporal.Duration;

export type TimeZonePolicy =
  | { readonly mode: 'follow_device' }
  | { readonly mode: 'fixed'; readonly timeZone: string };

export function parseInstant(value: string): Instant {
  return Temporal.Instant.from(value);
}

export function parsePlainDate(value: string): PlainDate {
  return Temporal.PlainDate.from(value);
}

export function parsePlainTime(value: string): PlainTime {
  return Temporal.PlainTime.from(value);
}

export function parsePlainDateTime(value: string): PlainDateTime {
  return Temporal.PlainDateTime.from(value);
}

export function parseZonedDateTime(value: string): ZonedDateTime {
  return Temporal.ZonedDateTime.from(value);
}

export function parseDuration(value: string): Duration {
  return Temporal.Duration.from(value);
}

export function instantToZonedDateTime(
  instant: Instant,
  timeZone: string,
): ZonedDateTime {
  return instant.toZonedDateTimeISO(validateNamedTimeZone(timeZone));
}

export function zonedDateTimeToInstant(zonedDateTime: ZonedDateTime): Instant {
  return zonedDateTime.toInstant();
}

export function validateNamedTimeZone(timeZone: string): string {
  if (timeZone.length === 0 || timeZone.trim() !== timeZone) {
    throw new RangeError(
      'Timezone must be a non-empty unpadded IANA identifier.',
    );
  }

  // ECMA-402 also admits numeric offset identifiers in some runtimes. DANTE deliberately
  // requires a named timezone so future DST/rule changes remain representable.
  if (/^[+-]\d{2}(?::?\d{2})?$/.test(timeZone)) {
    throw new RangeError(
      'DANTE requires a named IANA timezone, not a fixed UTC offset.',
    );
  }

  try {
    new Intl.DateTimeFormat('en-US', { timeZone }).format(0);
  } catch (error) {
    if (error instanceof RangeError) {
      throw new RangeError(`Unknown IANA timezone: ${timeZone}`, {
        cause: error,
      });
    }
    throw error;
  }

  return timeZone;
}

export function detectDeviceTimeZone(
  resolver: () => string = () =>
    Intl.DateTimeFormat().resolvedOptions().timeZone,
): string {
  return validateNamedTimeZone(resolver());
}

export function resolveEffectiveTimeZone(
  policy: TimeZonePolicy,
  deviceTimeZone: string | undefined,
): string {
  if (policy.mode === 'fixed') {
    return validateNamedTimeZone(policy.timeZone);
  }

  if (deviceTimeZone === undefined) {
    throw new RangeError(
      'follow_device timezone policy requires a detected device timezone.',
    );
  }
  return validateNamedTimeZone(deviceTimeZone);
}

/** Local wall-clock start movement. The accepted duration is kept unchanged. */
export function moveCivilStartPreservingDuration(
  originalStart: string,
  originalEnd: string,
  newStart: string,
): string {
  const start = Temporal.PlainDateTime.from(originalStart);
  const end = Temporal.PlainDateTime.from(originalEnd);
  if (Temporal.PlainDateTime.compare(end, start) <= 0) {
    throw new RangeError('An interval must have a positive duration.');
  }
  const duration = start.until(end, { largestUnit: 'minutes' });
  return Temporal.PlainDateTime.from(newStart)
    .add(duration)
    .toString({ smallestUnit: 'minute' });
}

/** Inclusive civil-date range movement; never treat all-day as a UTC duration. */
export function moveAllDayRangePreservingDays(
  originalStart: string,
  originalEndInclusive: string,
  newStart: string,
): string {
  const start = Temporal.PlainDate.from(originalStart);
  const end = Temporal.PlainDate.from(originalEndInclusive);
  if (Temporal.PlainDate.compare(end, start) < 0) {
    throw new RangeError('All-day end must not precede start.');
  }
  const days = start.until(end).days;
  return Temporal.PlainDate.from(newStart).add({ days }).toString();
}

/** Strict local end ordering; an overnight end must name the next calendar date. */
export function isValidCivilInterval(start: string, end: string): boolean {
  try {
    return Temporal.PlainDateTime.compare(
      Temporal.PlainDateTime.from(end),
      Temporal.PlainDateTime.from(start),
    ) > 0;
  } catch {
    return false;
  }
}

/** Resolve a named-zone wall time without ever accepting a spring DST gap. */
export function resolveCivilNamedInstant(
  local: string,
  zoneId: string,
  disambiguation: 'earlier' | 'later' | 'reject' = 'earlier',
): Temporal.Instant {
  const wall = Temporal.PlainDateTime.from(local);
  const zoned = wall.toZonedDateTime(zoneId, { disambiguation });
  if (!zoned.toPlainDateTime().equals(wall)) {
    throw new RangeError('This local time does not exist in the selected timezone.');
  }
  return zoned.toInstant();
}

/** Calculate an end displayed in its own zone from one elapsed duration. */
export function projectElapsedEndToZone(
  startLocal: string,
  startZone: string,
  elapsedMinutes: number,
  endZone: string,
  disambiguation: 'earlier' | 'later' | 'reject' = 'earlier',
): string {
  if (!Number.isInteger(elapsedMinutes) || elapsedMinutes <= 0) {
    throw new RangeError('An elapsed duration must be positive whole minutes.');
  }
  const end = resolveCivilNamedInstant(startLocal, startZone, disambiguation)
    .add({ minutes: elapsedMinutes })
    .toZonedDateTimeISO(endZone)
    .toPlainDateTime();
  return end.toString({ smallestUnit: 'minute' });
}

/** Real elapsed minutes, never a subtraction of unrelated wall-clock numbers. */
export function elapsedMinutesBetweenZonedBounds(
  startLocal: string,
  startZone: string,
  endLocal: string,
  endZone: string,
  disambiguation: 'earlier' | 'later' | 'reject' = 'earlier',
): number {
  const start = resolveCivilNamedInstant(startLocal, startZone, disambiguation);
  const end = resolveCivilNamedInstant(endLocal, endZone, disambiguation);
  const minutes = start.until(end).total({ unit: 'minutes' });
  if (!Number.isInteger(minutes) || minutes <= 0) {
    throw new RangeError('The resolved end must follow the resolved start.');
  }
  return minutes;
}
