import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineScheduledActivityItem,
  TemporalTimelineWindow,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const TEMPORAL_TIMELINE_WINDOW_ENDPOINT = '/api/v1/temporal/timeline/window';
const MAX_TIMELINE_WINDOW_DAYS = 62;

export type TemporalTimelineRemoteFailureKind =
  'transport' | 'http' | 'protocol';

export class TemporalTimelineRemoteError extends Error {
  constructor(
    readonly kind: TemporalTimelineRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
  ) {
    super(message);
    this.name = 'TemporalTimelineRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function requireExactKeys(
  payload: Record<string, unknown>,
  allowed: readonly string[],
  label: string,
): void {
  const allowedKeys = new Set(allowed);
  for (const key of Object.keys(payload)) {
    if (!allowedKeys.has(key)) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
}

function parsePlainDateKey(value: unknown, field: string): string {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }

  try {
    const parsed = Temporal.PlainDate.from(value);
    if (parsed.toString() !== value) {
      throw new RangeError('non-canonical PlainDate');
    }
    return value;
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
}

function parseUuidV7(value: unknown, field: string): string {
  if (
    typeof value !== 'string' ||
    !/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
      value,
    )
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseFloatingLocalDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }

  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }
}

function validateWindowRequest(request: TemporalTimelineWindowRequest): void {
  const start = Temporal.PlainDate.from(request.startDate);
  const end = Temporal.PlainDate.from(request.endDateExclusive);
  const days = start.until(end, { largestUnit: 'days' }).days;

  if (days <= 0) {
    throw new RangeError('Timeline endDateExclusive must be after startDate.');
  }
  if (days > MAX_TIMELINE_WINDOW_DAYS) {
    throw new RangeError(
      `Timeline window cannot exceed ${MAX_TIMELINE_WINDOW_DAYS} local days.`,
    );
  }
}

function parseEffectiveZoneId(value: unknown): string {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'effective_zone_id must be a named IANA timezone.',
    );
  }

  try {
    return validateNamedTimeZone(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'effective_zone_id must be a named IANA timezone.',
    );
  }
}

function parseScheduledActivity(
  payload: unknown,
): TemporalTimelineScheduledActivityItem {
  if (!isRecord(payload) || payload.kind !== 'scheduled_activity') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline item has an unsupported representation.',
    );
  }
  requireExactKeys(
    payload,
    [
      'kind',
      'activity_ref',
      'schedule_ref',
      'placement_material_state_ref',
      'title',
      'temporal_form',
      'starts_local_at',
      'ends_local_at',
    ],
    'Temporal Timeline scheduled Activity',
  );
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline Activity title must be a non-empty string.',
    );
  }
  if (payload.temporal_form !== 'floating_local') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'B02-A Timeline item must preserve floating-local placement semantics.',
    );
  }

  const startsLocalAt = parseFloatingLocalDateTime(
    payload.starts_local_at,
    'starts_local_at',
  );
  const endsLocalAt = parseFloatingLocalDateTime(
    payload.ends_local_at,
    'ends_local_at',
  );
  if (
    Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
    !startsLocalAt.toPlainDate().equals(endsLocalAt.toPlainDate())
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'B02-A Timeline placement must be a positive same-local-day interval.',
    );
  }

  return Object.freeze({
    kind: 'scheduled_activity',
    activityRef: parseUuidV7(payload.activity_ref, 'activity_ref'),
    scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: parseUuidV7(
      payload.placement_material_state_ref,
      'placement_material_state_ref',
    ),
    title: payload.title,
    temporalForm: 'floating-local',
    startsLocalAt,
    endsLocalAt,
  });
}

function parseWindow(payload: unknown): TemporalTimelineWindow {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline response has an unsupported representation.',
    );
  }

  if (payload.kind === 'empty') {
    requireExactKeys(
      payload,
      ['kind', 'start_date', 'end_date_exclusive', 'effective_zone_id'],
      'Temporal Timeline response',
    );
    return Object.freeze({
      kind: 'empty',
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseEffectiveZoneId(payload.effective_zone_id),
    });
  }

  if (payload.kind === 'window') {
    requireExactKeys(
      payload,
      [
        'kind',
        'start_date',
        'end_date_exclusive',
        'effective_zone_id',
        'items',
      ],
      'Temporal Timeline response',
    );
    if (!Array.isArray(payload.items) || payload.items.length === 0) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Populated Temporal Timeline window must contain at least one item.',
      );
    }
    return Object.freeze({
      kind: 'window',
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseEffectiveZoneId(payload.effective_zone_id),
      items: Object.freeze(payload.items.map(parseScheduledActivity)),
    });
  }

  throw new TemporalTimelineRemoteError(
    'protocol',
    'Temporal Timeline response has an unsupported representation.',
  );
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

export function createRemoteTemporalTimelineDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalTimelineDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  return {
    async loadWindow(
      request: TemporalTimelineWindowRequest,
      signal?: AbortSignal,
    ): Promise<TemporalTimelineWindow> {
      validateWindowRequest(request);
      const query = new URLSearchParams({
        start_date: request.startDate,
        end_date_exclusive: request.endDateExclusive,
      });

      let response: Response;
      try {
        response = await webFetch(
          `${TEMPORAL_TIMELINE_WINDOW_ENDPOINT}?${query.toString()}`,
          signal === undefined ? undefined : { signal },
        );
      } catch (error) {
        if (isAbortError(error)) {
          throw error;
        }
        throw new TemporalTimelineRemoteError(
          'transport',
          'Temporal Timeline request could not reach DANTE.',
        );
      }

      if (!response.ok) {
        throw new TemporalTimelineRemoteError(
          'http',
          `Temporal Timeline request failed with HTTP ${response.status}.`,
          response.status,
        );
      }

      let payload: unknown;
      try {
        payload = await response.json();
      } catch {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Temporal Timeline response is not valid JSON.',
          response.status,
        );
      }

      const window = parseWindow(payload);
      if (
        window.startDate !== request.startDate ||
        window.endDateExclusive !== request.endDateExclusive
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Temporal Timeline response does not match the requested window.',
          response.status,
        );
      }
      return window;
    },
  };
}
