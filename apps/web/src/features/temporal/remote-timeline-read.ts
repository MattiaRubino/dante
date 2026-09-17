import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineScheduledItem,
  TemporalTimelineWindow,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const TEMPORAL_TIMELINE_WINDOW_ENDPOINT = '/api/v1/temporal/timeline/window';
const MAX_TIMELINE_WINDOW_DAYS = 62;
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type TemporalTimelineRemoteFailureKind =
  | 'transport'
  | 'http'
  | 'protocol';

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
  for (const key of allowed) {
    if (!(key in payload)) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        `${label} is missing required field ${key}.`,
      );
    }
  }
}

function parsePlainDate(value: unknown, field: string) {
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
    return parsed;
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
}

function parsePlainDateKey(value: unknown, field: string): string {
  return parsePlainDate(value, field).toString();
}

function parseUuidV7(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseLocalDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
}

function parseInstant(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be an absolute instant.`,
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be an absolute instant.`,
    );
  }
}

function parseZoneId(value: unknown, field: string): string {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
    );
  }
  try {
    return validateNamedTimeZone(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
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

type ParsedOwnerIdentity =
  | Readonly<{
      kind: 'scheduled_activity';
      activityRef: string;
      scheduleRef: string;
      placementMaterialStateRef: string;
      title: string;
      wireRefKey: 'activity_ref';
    }>
  | Readonly<{
      kind: 'scheduled_event';
      eventRef: string;
      scheduleRef: string;
      placementMaterialStateRef: string;
      title: string;
      wireRefKey: 'event_ref';
    }>;

function parseOwnerIdentity(payload: Record<string, unknown>): ParsedOwnerIdentity {
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline owner title must be a non-empty string.',
    );
  }
  const shared = {
    scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: parseUuidV7(
      payload.placement_material_state_ref,
      'placement_material_state_ref',
    ),
    title: payload.title,
  };

  if (payload.kind === 'scheduled_activity') {
    return Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: parseUuidV7(payload.activity_ref, 'activity_ref'),
      ...shared,
      wireRefKey: 'activity_ref' as const,
    });
  }
  if (payload.kind === 'scheduled_event') {
    return Object.freeze({
      kind: 'scheduled_event' as const,
      eventRef: parseUuidV7(payload.event_ref, 'event_ref'),
      ...shared,
      wireRefKey: 'event_ref' as const,
    });
  }
  throw new TemporalTimelineRemoteError(
    'protocol',
    'Temporal Timeline item has an unsupported owner representation.',
  );
}

function publicIdentity(identity: ParsedOwnerIdentity) {
  if (identity.kind === 'scheduled_activity') {
    const { wireRefKey: _wireRefKey, ...result } = identity;
    return result;
  }
  const { wireRefKey: _wireRefKey, ...result } = identity;
  return result;
}

function parseScheduledItem(payload: unknown): TemporalTimelineScheduledItem {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline item has an unsupported representation.',
    );
  }

  const owner = parseOwnerIdentity(payload);
  const identity = publicIdentity(owner);
  const ownerLabel = owner.kind === 'scheduled_activity' ? 'Activity' : 'Event';
  const commonKeys = [
    'kind',
    owner.wireRefKey,
    'schedule_ref',
    'placement_material_state_ref',
    'title',
    'temporal_form',
  ] as const;

  switch (payload.temporal_form) {
    case 'date_span': {
      requireExactKeys(
        payload,
        [...commonKeys, 'start_date', 'end_date_exclusive'],
        `Temporal Timeline date-span ${ownerLabel}`,
      );
      const startDate = parsePlainDate(payload.start_date, 'start_date');
      const endDateExclusive = parsePlainDate(
        payload.end_date_exclusive,
        'end_date_exclusive',
      );
      if (Temporal.PlainDate.compare(startDate, endDateExclusive) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline date-span must be a positive half-open civil-date range.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'date-span' as const,
        startDate,
        endDateExclusive,
      });
    }

    case 'floating_local': {
      requireExactKeys(
        payload,
        [...commonKeys, 'starts_local_at', 'ends_local_at'],
        `Temporal Timeline floating-local ${ownerLabel}`,
      );
      const startsLocalAt = parseLocalDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        payload.ends_local_at,
        'ends_local_at',
      );
      if (Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline floating-local placement must be a positive interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'floating-local' as const,
        startsLocalAt,
        endsLocalAt,
      });
    }

    case 'named_zone_local': {
      requireExactKeys(
        payload,
        [
          ...commonKeys,
          'starts_local_at',
          'ends_local_at',
          'zone_id',
          'resolved_start_at',
          'resolved_end_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        `Temporal Timeline named-zone ${ownerLabel}`,
      );
      const startsLocalAt = parseLocalDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        payload.ends_local_at,
        'ends_local_at',
      );
      const resolvedStartAt = parseInstant(
        payload.resolved_start_at,
        'resolved_start_at',
      );
      const resolvedEndAt = parseInstant(
        payload.resolved_end_at,
        'resolved_end_at',
      );
      if (
        Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
        Temporal.Instant.compare(resolvedStartAt, resolvedEndAt) >= 0
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline named-zone placement must retain a positive local and resolved interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'named-zone-local' as const,
        startsLocalAt,
        endsLocalAt,
        zoneId: parseZoneId(payload.zone_id, 'zone_id'),
        resolvedStartAt,
        resolvedEndAt,
        displayStartsLocalAt: parseLocalDateTime(
          payload.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          payload.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }

    case 'absolute': {
      requireExactKeys(
        payload,
        [
          ...commonKeys,
          'starts_at',
          'ends_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        `Temporal Timeline absolute ${ownerLabel}`,
      );
      const startsAt = parseInstant(payload.starts_at, 'starts_at');
      const endsAt = parseInstant(payload.ends_at, 'ends_at');
      if (Temporal.Instant.compare(startsAt, endsAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline absolute placement must be a positive interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'absolute' as const,
        startsAt,
        endsAt,
        displayStartsLocalAt: parseLocalDateTime(
          payload.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          payload.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }

    case 'coarse_local_period': {
      requireExactKeys(
        payload,
        [...commonKeys, 'local_date', 'period'],
        `Temporal Timeline coarse-period ${ownerLabel}`,
      );
      if (
        payload.period !== 'morning' &&
        payload.period !== 'afternoon' &&
        payload.period !== 'evening'
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline coarse-period placement is outside the activated vocabulary.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'coarse-local-period' as const,
        localDate: parsePlainDate(payload.local_date, 'local_date'),
        period: payload.period,
      });
    }

    default:
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Temporal Timeline item has an unsupported temporal form.',
      );
  }
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
      kind: 'empty' as const,
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseZoneId(
        payload.effective_zone_id,
        'effective_zone_id',
      ),
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
      kind: 'window' as const,
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseZoneId(
        payload.effective_zone_id,
        'effective_zone_id',
      ),
      items: Object.freeze(payload.items.map(parseScheduledItem)),
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

  return Object.freeze({
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
  });
}
