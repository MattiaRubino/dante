import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalEventDataSource,
  TemporalScheduledEventCreateRequest,
  TemporalScheduledEventCreateResult,
} from './event-data-source';
import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const SCHEDULED_EVENT_ENDPOINT = '/api/v1/temporal/events/scheduled';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type TemporalEventRemoteFailureKind =
  | 'transport'
  | 'http'
  | 'protocol'
  | 'authentication';

export class TemporalEventRemoteError extends Error {
  public constructor(
    readonly kind: TemporalEventRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalEventRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

function requireExactKeys(
  payload: Record<string, unknown>,
  allowed: readonly string[],
  label: string,
): void {
  const allowedKeys = new Set(allowed);
  for (const key of Object.keys(payload)) {
    if (!allowedKeys.has(key)) {
      throw new TemporalEventRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
  for (const key of allowed) {
    if (!(key in payload)) {
      throw new TemporalEventRemoteError(
        'protocol',
        `${label} is missing required field ${key}.`,
      );
    }
  }
}

function parseUuidV7(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseInstant(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
}

function parsePlainDate(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalEventRemoteError(
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
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
}

function parseLocalDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
}

function parseZoneId(value: unknown, field: string): string {
  if (typeof value !== 'string') {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
    );
  }
  try {
    return validateNamedTimeZone(value);
  } catch {
    throw new TemporalEventRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
    );
  }
}

function parseAgendaParts(value: unknown): readonly string[] {
  if (!Array.isArray(value) || value.length > 100) {
    throw new TemporalEventRemoteError(
      'protocol',
      'Scheduled Event agenda_parts must be an array with at most 100 parts.',
    );
  }
  const parts = value.map((part, index) => {
    if (
      typeof part !== 'string' ||
      part.length === 0 ||
      part.length > 1000 ||
      part.trim() !== part
    ) {
      throw new TemporalEventRemoteError(
        'protocol',
        `Scheduled Event agenda_parts[${index}] must be canonical non-empty text.`,
      );
    }
    return part;
  });
  return Object.freeze(parts);
}

function parseAcceptedPlacement(
  payload: Record<string, unknown>,
): TemporalAcceptedSchedulePlacement {
  switch (payload.temporal_form) {
    case 'date_span': {
      const startDate = parsePlainDate(payload.start_date, 'start_date');
      const endDateExclusive = parsePlainDate(
        payload.end_date_exclusive,
        'end_date_exclusive',
      );
      if (Temporal.PlainDate.compare(startDate, endDateExclusive) >= 0) {
        throw new TemporalEventRemoteError(
          'protocol',
          'Scheduled Event date span must be positive.',
        );
      }
      return Object.freeze({
        kind: 'date-span' as const,
        startDate,
        endDateExclusive,
      });
    }
    case 'floating_local': {
      const startsLocalAt = parseLocalDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        payload.ends_local_at,
        'ends_local_at',
      );
      if (Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0) {
        throw new TemporalEventRemoteError(
          'protocol',
          'Scheduled Event floating-local interval must be positive.',
        );
      }
      return Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt,
        endsLocalAt,
      });
    }
    case 'named_zone_local': {
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
        throw new TemporalEventRemoteError(
          'protocol',
          'Scheduled Event named-zone interval must be positive.',
        );
      }
      return Object.freeze({
        kind: 'named-zone-local-interval' as const,
        startsLocalAt,
        endsLocalAt,
        zoneId: parseZoneId(payload.zone_id, 'zone_id'),
        resolvedStartAt,
        resolvedEndAt,
      });
    }
    case 'absolute': {
      const startsAt = parseInstant(payload.starts_at, 'starts_at');
      const endsAt = parseInstant(payload.ends_at, 'ends_at');
      if (Temporal.Instant.compare(startsAt, endsAt) >= 0) {
        throw new TemporalEventRemoteError(
          'protocol',
          'Scheduled Event absolute interval must be positive.',
        );
      }
      return Object.freeze({
        kind: 'absolute-interval' as const,
        startsAt,
        endsAt,
      });
    }
    case 'coarse_local_period': {
      if (
        payload.period !== 'morning' &&
        payload.period !== 'afternoon' &&
        payload.period !== 'evening'
      ) {
        throw new TemporalEventRemoteError(
          'protocol',
          'Scheduled Event coarse period is unsupported.',
        );
      }
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: parsePlainDate(payload.local_date, 'local_date'),
        period: payload.period,
      });
    }
    default:
      throw new TemporalEventRemoteError(
        'protocol',
        'Scheduled Event temporal form is unsupported.',
      );
  }
}

function scheduledResponseKeys(temporalForm: unknown): readonly string[] {
  const common = [
    'event_ref',
    'title',
    'agenda_parts',
    'created_at',
    'schedule_ref',
    'placement_material_state_ref',
    'temporal_form',
    'replayed',
  ] as const;
  switch (temporalForm) {
    case 'date_span':
      return [...common, 'start_date', 'end_date_exclusive'];
    case 'floating_local':
      return [...common, 'starts_local_at', 'ends_local_at'];
    case 'named_zone_local':
      return [
        ...common,
        'starts_local_at',
        'ends_local_at',
        'zone_id',
        'resolved_start_at',
        'resolved_end_at',
      ];
    case 'absolute':
      return [...common, 'starts_at', 'ends_at'];
    case 'coarse_local_period':
      return [...common, 'local_date', 'period'];
    default:
      return common;
  }
}

function parseScheduledEvent(
  payload: unknown,
): TemporalScheduledEventCreateResult {
  if (!isRecord(payload)) {
    throw new TemporalEventRemoteError(
      'protocol',
      'Scheduled Event response must be an object.',
    );
  }
  requireExactKeys(
    payload,
    scheduledResponseKeys(payload.temporal_form),
    'Scheduled Event response',
  );
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalEventRemoteError(
      'protocol',
      'Scheduled Event title must be a non-empty string.',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalEventRemoteError(
      'protocol',
      'Scheduled Event replayed must be boolean.',
    );
  }
  return Object.freeze({
    event: Object.freeze({
      eventRef: parseUuidV7(payload.event_ref, 'event_ref'),
      title: payload.title,
      agendaParts: parseAgendaParts(payload.agenda_parts),
      createdAt: parseInstant(payload.created_at, 'created_at'),
    }),
    schedule: Object.freeze({
      scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
      placementMaterialStateRef: parseUuidV7(
        payload.placement_material_state_ref,
        'placement_material_state_ref',
      ),
      placement: parseAcceptedPlacement(payload),
    }),
    replayed: payload.replayed,
  });
}

function validatePlacement(placement: TemporalSchedulePlacementInput): void {
  switch (placement.kind) {
    case 'date-span':
      if (
        Temporal.PlainDate.compare(
          placement.startDate,
          placement.endDateExclusive,
        ) >= 0
      ) {
        throw new RangeError('Event date span must be positive.');
      }
      return;
    case 'floating-local-interval':
      if (
        Temporal.PlainDateTime.compare(
          placement.startsLocalAt,
          placement.endsLocalAt,
        ) >= 0
      ) {
        throw new RangeError('Event floating-local interval must be positive.');
      }
      return;
    case 'named-zone-local-interval':
      if (
        Temporal.PlainDateTime.compare(
          placement.startsLocalAt,
          placement.endsLocalAt,
        ) >= 0
      ) {
        throw new RangeError('Event named-zone interval must be positive.');
      }
      validateNamedTimeZone(placement.zoneId);
      return;
    case 'absolute-interval':
      if (Temporal.Instant.compare(placement.startsAt, placement.endsAt) >= 0) {
        throw new RangeError('Event absolute interval must be positive.');
      }
      return;
    case 'coarse-local-period':
      return;
  }
}

function serializePlacement(placement: TemporalSchedulePlacementInput) {
  switch (placement.kind) {
    case 'date-span':
      return {
        kind: 'date_span',
        start_date: placement.startDate.toString(),
        end_date_exclusive: placement.endDateExclusive.toString(),
      } as const;
    case 'floating-local-interval':
      return {
        kind: 'floating_local_interval',
        starts_local_at: placement.startsLocalAt.toString(),
        ends_local_at: placement.endsLocalAt.toString(),
      } as const;
    case 'named-zone-local-interval':
      return {
        kind: 'named_zone_local_interval',
        starts_local_at: placement.startsLocalAt.toString(),
        ends_local_at: placement.endsLocalAt.toString(),
        zone_id: placement.zoneId,
        disambiguation: placement.disambiguation,
      } as const;
    case 'absolute-interval':
      return {
        kind: 'absolute_interval',
        starts_at: placement.startsAt.toString(),
        ends_at: placement.endsAt.toString(),
      } as const;
    case 'coarse-local-period':
      return {
        kind: 'coarse_local_period',
        local_date: placement.localDate.toString(),
        period: placement.period,
      } as const;
  }
}

async function readJson(response: Response, label: string): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalEventRemoteError(
      'protocol',
      `${label} is not valid JSON.`,
      response.status,
    );
  }
}

function problemCode(payload: unknown): string | null {
  return isRecord(payload) && typeof payload.code === 'string'
    ? payload.code
    : null;
}

async function requireOk(response: Response, label: string): Promise<unknown> {
  const payload = await readJson(response, label);
  if (!response.ok) {
    throw new TemporalEventRemoteError(
      'http',
      `${label} failed with HTTP ${response.status}.`,
      response.status,
      problemCode(payload),
    );
  }
  return payload;
}

async function fetchResponse(
  webFetch: typeof globalThis.fetch,
  input: RequestInfo | URL,
  init: RequestInit | undefined,
): Promise<Response> {
  try {
    return await webFetch(input, init);
  } catch (error) {
    if (isAbortError(error)) {
      throw error;
    }
    throw new TemporalEventRemoteError(
      'transport',
      'Event request could not reach DANTE.',
    );
  }
}

async function csrfToken(
  webFetch: typeof globalThis.fetch,
  signal?: AbortSignal,
): Promise<string> {
  const response = await fetchResponse(
    webFetch,
    SESSION_ENDPOINT,
    signal === undefined ? undefined : { signal },
  );
  const payload = await requireOk(response, 'Auth session response');
  if (
    !isRecord(payload) ||
    payload.authenticated !== true ||
    typeof payload.csrf_token !== 'string' ||
    payload.csrf_token.length === 0
  ) {
    throw new TemporalEventRemoteError(
      'authentication',
      'Event mutation requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

function normalizedAgendaParts(parts: readonly string[]): readonly string[] {
  if (parts.length > 100) {
    throw new RangeError('Event Agenda may contain at most 100 parts.');
  }
  return Object.freeze(
    parts.map((part) => {
      const normalized = part.trim();
      if (!normalized || normalized.length > 1000) {
        throw new RangeError(
          'Event Agenda parts must contain 1 to 1000 non-padding characters.',
        );
      }
      return normalized;
    }),
  );
}

function validateRequest(request: TemporalScheduledEventCreateRequest): void {
  const operationId = request.operationId.trim();
  const title = request.title.trim();
  if (!operationId || operationId.length > 200) {
    throw new RangeError('Event operation id must contain 1 to 200 characters.');
  }
  if (!title || title.length > 300) {
    throw new RangeError('Event title must contain 1 to 300 characters.');
  }
  normalizedAgendaParts(request.agendaParts);
  validatePlacement(request.placement);
}

export function createRemoteTemporalEventDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalEventDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  return Object.freeze({
    async createScheduledEvent(
      request: TemporalScheduledEventCreateRequest,
      signal?: AbortSignal,
    ): Promise<TemporalScheduledEventCreateResult> {
      validateRequest(request);
      const agendaParts = normalizedAgendaParts(request.agendaParts);
      const csrf = await csrfToken(webFetch, signal);
      const response = await fetchResponse(webFetch, SCHEDULED_EVENT_ENDPOINT, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
          [CSRF_HEADER_NAME]: csrf,
        }),
        body: JSON.stringify({
          operation_id: request.operationId.trim(),
          title: request.title.trim(),
          agenda_parts: agendaParts,
          placement: serializePlacement(request.placement),
        }),
        ...(signal === undefined ? {} : { signal }),
      });
      const payload = await requireOk(response, 'Create Scheduled Event response');
      const result = parseScheduledEvent(payload);
      invalidateTemporalTimelineRead();
      return result;
    },
  });
}
