import { Temporal, detectDeviceTimeZone, validateNamedTimeZone } from '@dante/time';

import type { TemporalTimelineWindow } from './timeline-read';

/** A presentation preference, NEVER a mutation of a Schedule or a Session. */
export const TIMELINE_VIEW_ZONE_STORAGE_KEY = 'dante.timeline.view-zone.v1';

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
