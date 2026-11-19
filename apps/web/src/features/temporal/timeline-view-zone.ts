import { Temporal, detectDeviceTimeZone, validateNamedTimeZone } from '@dante/time';

import type { TemporalTimelineWindow } from './timeline-read';

/** A presentation preference, NEVER a mutation of a Schedule or a Session. */
export const TIMELINE_VIEW_ZONE_STORAGE_KEY = 'dante.timeline.view-zone.v1';

/** View-only comparison scales; never part of Schedule or Session persistence. */
export const TIMELINE_SECONDARY_ZONES_STORAGE_KEY =
  'dante.timeline.secondary-zones.v1';
export const MAX_TIMELINE_VISIBLE_ZONES = 3;

/** Resolve aliases once; repeated rendering must not instantiate many formatters. */
const canonicalZoneCache = new Map<string, string>();

function canonicalTimelineZone(zone: string): string {
  const cached = canonicalZoneCache.get(zone);
  if (cached !== undefined) return cached;
  const normalized = new Intl.DateTimeFormat('en-US', {
    timeZone: zone,
  }).resolvedOptions().timeZone;
  canonicalZoneCache.set(zone, normalized);
  return normalized;
}

/** Treat IANA aliases (e.g. UTC and Etc/UTC) as the same display zone. */
export function sameTimelineTimeZone(left: string, right: string): boolean {
  if (left === right) return true;
  try {
    return canonicalTimelineZone(left) === canonicalTimelineZone(right);
  } catch {
    return false;
  }
}

export function normalizeTimelineSecondaryZones(
  primaryZone: string,
  candidates: readonly unknown[],
): readonly string[] {
  const valid: string[] = [];
  for (const candidate of candidates) {
    if (typeof candidate !== 'string') continue;
    try {
      const zone = validateNamedTimeZone(candidate);
      if (!sameTimelineTimeZone(zone, primaryZone) &&
          !valid.some((entry) => sameTimelineTimeZone(entry, zone))) {
        valid.push(zone);
      }
    } catch {
      // Ignore malformed or stale browser preferences only when reading them.
    }
    if (valid.length === MAX_TIMELINE_VISIBLE_ZONES - 1) break;
  }
  return valid;
}

export function readTimelineSecondaryZones(primaryZone: string): readonly string[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(TIMELINE_SECONDARY_ZONES_STORAGE_KEY);
    if (!raw) return [];
    const decoded: unknown = JSON.parse(raw);
    return Array.isArray(decoded)
      ? normalizeTimelineSecondaryZones(primaryZone, decoded) : [];
  } catch {
    return [];
  }
}

export function saveTimelineSecondaryZones(zones: readonly string[]): void {
  // Validate before the storage try/catch. Invalid zones must never be saved.
  const valid = zones.map(validateNamedTimeZone);
  if (valid.length > MAX_TIMELINE_VISIBLE_ZONES - 1 ||
      valid.some((zone, index) => valid.slice(0, index)
        .some((previous) => sameTimelineTimeZone(previous, zone)))) {
    throw new RangeError('Timeline supports up to two distinct secondary zones.');
  }
  if (typeof window === 'undefined') return;
  try {
    if (!valid.length) window.localStorage.removeItem(TIMELINE_SECONDARY_ZONES_STORAGE_KEY);
    else window.localStorage.setItem(
      TIMELINE_SECONDARY_ZONES_STORAGE_KEY, JSON.stringify(valid),
    );
  } catch {
    // In-memory selection works when browser storage is restricted.
  }
}

export function addTimelineSecondaryZone(
  primaryZone: string,
  current: readonly string[],
  newZone: string,
): readonly string[] {
  const candidate = validateNamedTimeZone(newZone);
  const normalized = normalizeTimelineSecondaryZones(primaryZone, current);
  if (sameTimelineTimeZone(candidate, primaryZone) ||
      normalized.some((entry) => sameTimelineTimeZone(entry, candidate)) ||
      normalized.length >= MAX_TIMELINE_VISIBLE_ZONES - 1) return normalized;
  return [...normalized, candidate];
}

/** Promote a secondary without changing the number of visible ruler columns. */
export function swapTimelinePrimaryZone(
  oldPrimary: string,
  nextPrimary: string,
  current: readonly string[],
): readonly string[] {
  const next = validateNamedTimeZone(nextPrimary);
  const normalized = normalizeTimelineSecondaryZones(oldPrimary, current);
  const existingIndex = normalized.findIndex((zone) => sameTimelineTimeZone(zone, next));
  if (existingIndex === -1) {
    return normalizeTimelineSecondaryZones(next, normalized);
  }
  const swapped = [...normalized];
  swapped[existingIndex] = validateNamedTimeZone(oldPrimary);
  return normalizeTimelineSecondaryZones(next, swapped);
}

export type TimelineSecondaryRulerTick = Readonly<{
  date: string;
  time: string;
  dayDelta: number;
  missingPrimaryHour: boolean;
}>;

/**
 * Project a primary ruler tick's physical instant into a comparison zone.
 * The primary 24-hour wall-clock axis is unchanged; nonexistent DST ticks
 * are explicitly marked rather than given an invented instant.
 */
export function timelineSecondaryRulerTick(
  primaryDay: string,
  minute: number,
  primaryZone: string,
  secondaryZone: string,
): TimelineSecondaryRulerTick {
  if (!Number.isFinite(minute) || minute < 0 || minute > 1440) {
    throw new RangeError('Ruler minute outside the 0..1440 visible day.');
  }
  const civilDay = Temporal.PlainDate.from(primaryDay);
  const hourMinute = minute % 1440;
  const source = civilDay.add({ days: Math.floor(minute / 1440) })
    .toPlainDateTime({
      hour: Math.floor(hourMinute / 60),
      minute: Math.floor(hourMinute % 60),
    });
  const zoned = source.toZonedDateTime(primaryZone, { disambiguation: 'compatible' });
  const missingPrimaryHour = !zoned.toPlainDateTime().equals(source);
  const target = zoned.withTimeZone(secondaryZone);
  const localDate = target.toPlainDate();
  return {
    date: localDate.toString(),
    time: missingPrimaryHour ? '—' :
      String(target.hour).padStart(2, '0') + ':' +
      String(target.minute).padStart(2, '0'),
    dayDelta: localDate.since(civilDay).days,
    missingPrimaryHour,
  };
}

export function readTimelineViewZonePreference(): string | null {
  if (typeof window === 'undefined') return null;
  try {
    const stored = window.localStorage.getItem(TIMELINE_VIEW_ZONE_STORAGE_KEY);
    return stored === null ? null : validateNamedTimeZone(stored);
  } catch {
    return null;
  }
}

export function saveTimelineViewZonePreference(zoneId: string | null): void {
  // Invalid named zones are a contract error, not a browser storage failure.
  const validatedZoneId = zoneId === null ? null : validateNamedTimeZone(zoneId);
  if (typeof window === 'undefined') return;
  try {
    if (validatedZoneId === null) {
      window.localStorage.removeItem(TIMELINE_VIEW_ZONE_STORAGE_KEY);
    } else {
      window.localStorage.setItem(
        TIMELINE_VIEW_ZONE_STORAGE_KEY, validatedZoneId,
      );
    }
  } catch {
    // Browser storage may be unavailable; the in-memory selection still works.
  }
}

/** Project only DISPLAY fields; canonical instants and original IANA zones survive. */
export function projectTimelineWindowInZone(
  source: TemporalTimelineWindow,
  zoneId: string,
): TemporalTimelineWindow {
  if (source.effectiveZoneId === zoneId) return source;
  const normalized = validateNamedTimeZone(zoneId);
  if (source.kind === 'empty') {
    return { ...source, effectiveZoneId: normalized };
  }
  return {
    ...source,
    effectiveZoneId: normalized,
    items: source.items.map((item) => {
      if (item.kind === 'expected_occurrence') return item;
      switch (item.temporalForm) {
        case 'named-zone-local':
          return {
            ...item,
            displayStartsLocalAt: item.resolvedStartAt
              .toZonedDateTimeISO(normalized).toPlainDateTime(),
            displayEndsLocalAt: item.resolvedEndAt
              .toZonedDateTimeISO(normalized).toPlainDateTime(),
          };
        case 'absolute':
          return {
            ...item,
            displayStartsLocalAt: item.startsAt
              .toZonedDateTimeISO(normalized).toPlainDateTime(),
            displayEndsLocalAt: item.endsAt
              .toZonedDateTimeISO(normalized).toPlainDateTime(),
          };
        case 'floating-local':
        case 'date-span':
        case 'coarse-local-period':
          return item;
      }
    }),
  };
}

export function currentTimelineDisplayZone(preference: string | null): string {
  return preference ?? detectDeviceTimeZone();
}

export function timelineViewZoneForInstant(
  instant: string,
  zoneId: string,
): Readonly<{ date: string; minute: number }> {
  const local = Temporal.Instant.from(instant).toZonedDateTimeISO(zoneId);
  return {
    date: local.toPlainDate().toString(),
    minute: local.hour * 60 + local.minute + local.second / 60,
  };
}
