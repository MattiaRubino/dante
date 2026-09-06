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
    throw new RangeError('Timezone must be a non-empty unpadded IANA identifier.');
  }

  // ECMA-402 also admits numeric offset identifiers in some runtimes. DANTE deliberately
  // requires a named timezone so future DST/rule changes remain representable.
  if (/^[+-]\d{2}(?::?\d{2})?$/.test(timeZone)) {
    throw new RangeError('DANTE requires a named IANA timezone, not a fixed UTC offset.');
  }

  try {
    new Intl.DateTimeFormat('en-US', { timeZone }).format(0);
  } catch (error) {
    if (error instanceof RangeError) {
      throw new RangeError(`Unknown IANA timezone: ${timeZone}`, { cause: error });
    }
    throw error;
  }

  return timeZone;
}

export function detectDeviceTimeZone(
  resolver: () => string = () => Intl.DateTimeFormat().resolvedOptions().timeZone,
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
    throw new RangeError('follow_device timezone policy requires a detected device timezone.');
  }
  return validateNamedTimeZone(deviceTimeZone);
}
