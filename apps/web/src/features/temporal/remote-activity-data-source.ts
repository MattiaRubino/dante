import { Temporal } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalActivityCreateRequest,
  TemporalActivityCreateResult,
  TemporalActivityDataSource,
  TemporalActivityRecord,
  TemporalActivityScheduleEstablishRequest,
  TemporalScheduledActivityCreateRequest,
  TemporalScheduledActivityCreateResult,
} from './activity-data-source';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const ACTIVITY_ENDPOINT = '/api/v1/temporal/activities';
const SCHEDULED_ACTIVITY_ENDPOINT = '/api/v1/temporal/activities/scheduled';
const activityScheduleEndpoint = (activityRef: string) =>
  `${ACTIVITY_ENDPOINT}/${encodeURIComponent(activityRef)}/schedule`;
const UNPLACED_ACTIVITY_ENDPOINT = '/api/v1/temporal/activities/unplaced';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';

export type TemporalActivityRemoteFailureKind =
  'transport' | 'http' | 'protocol' | 'authentication';

export class TemporalActivityRemoteError extends Error {
  constructor(
    readonly kind: TemporalActivityRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalActivityRemoteError';
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
      throw new TemporalActivityRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
}

function parseUuidV7(value: unknown, field: string): string {
  if (
    typeof value !== 'string' ||
    !/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
      value,
    )
  ) {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseCreatedAt(
  value: unknown,
): ReturnType<typeof Temporal.Instant.from> {
  if (typeof value !== 'string') {
    throw new TemporalActivityRemoteError(
      'protocol',
      'created_at must be an absolute timestamp.',
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalActivityRemoteError(
      'protocol',
      'created_at must be an absolute timestamp.',
    );
  }
}

function parseFloatingLocalDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }
}

function parseActivity(
  payload: unknown,
  { allowReplay }: Readonly<{ allowReplay: boolean }>,
): Readonly<{ activity: TemporalActivityRecord; replayed: boolean }> {
  if (!isRecord(payload)) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Activity response must be an object.',
    );
  }
  requireExactKeys(
    payload,
    ['activity_ref', 'title', 'created_at', 'replayed'],
    'Activity response',
  );
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Activity title must be a non-empty string.',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Activity replayed must be boolean.',
    );
  }
  if (!allowReplay && payload.replayed) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Read-only Activity projection cannot report a replay.',
    );
  }

  return Object.freeze({
    activity: Object.freeze({
      activityRef: parseUuidV7(payload.activity_ref, 'activity_ref'),
      title: payload.title,
      createdAt: parseCreatedAt(payload.created_at),
    }),
    replayed: payload.replayed,
  });
}

function parseScheduledActivity(
  payload: unknown,
): TemporalScheduledActivityCreateResult {
  if (!isRecord(payload)) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Scheduled Activity response must be an object.',
    );
  }
  requireExactKeys(
    payload,
    [
      'activity_ref',
      'title',
      'created_at',
      'schedule_ref',
      'placement_material_state_ref',
      'temporal_form',
      'starts_local_at',
      'ends_local_at',
      'replayed',
    ],
    'Scheduled Activity response',
  );
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Scheduled Activity title must be a non-empty string.',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Scheduled Activity replayed must be boolean.',
    );
  }
  if (payload.temporal_form !== 'floating_local') {
    throw new TemporalActivityRemoteError(
      'protocol',
      'B02-A Scheduled Activity must preserve floating-local placement semantics.',
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
    throw new TemporalActivityRemoteError(
      'protocol',
      'B02-A Scheduled Activity must be a positive same-local-day interval.',
    );
  }

  return Object.freeze({
    activity: Object.freeze({
      activityRef: parseUuidV7(payload.activity_ref, 'activity_ref'),
      title: payload.title,
      createdAt: parseCreatedAt(payload.created_at),
    }),
    schedule: Object.freeze({
      scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
      placementMaterialStateRef: parseUuidV7(
        payload.placement_material_state_ref,
        'placement_material_state_ref',
      ),
      temporalForm: 'floating-local',
      startsLocalAt,
      endsLocalAt,
    }),
    replayed: payload.replayed,
  });
}

async function readJson(response: Response, label: string): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalActivityRemoteError(
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
    throw new TemporalActivityRemoteError(
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
    throw new TemporalActivityRemoteError(
      'transport',
      'Activity request could not reach DANTE.',
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
    throw new TemporalActivityRemoteError(
      'authentication',
      'Activity mutation requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

function validateCreateRequest(request: TemporalActivityCreateRequest): void {
  const operationId = request.operationId.trim();
  const title = request.title.trim();
  if (!operationId || operationId.length > 200) {
    throw new RangeError(
      'Activity operation id must contain 1 to 200 characters.',
    );
  }
  if (!title || title.length > 300) {
    throw new RangeError('Activity title must contain 1 to 300 characters.');
  }
}

function validateFloatingLocalPlacement(
  placement: TemporalScheduledActivityCreateRequest['placement'],
  slice: 'B02-A' | 'B02-B',
): void {
  if (placement.kind !== 'floating-local-interval') {
    throw new RangeError(
      `${slice} supports only floating-local interval placement.`,
    );
  }
  if (
    Temporal.PlainDateTime.compare(
      placement.startsLocalAt,
      placement.endsLocalAt,
    ) >= 0 ||
    !placement.startsLocalAt
      .toPlainDate()
      .equals(placement.endsLocalAt.toPlainDate())
  ) {
    throw new RangeError(
      `${slice} placement must be a positive same-local-day interval.`,
    );
  }
}

function validateScheduledCreateRequest(
  request: TemporalScheduledActivityCreateRequest,
): void {
  validateCreateRequest(request);
  validateFloatingLocalPlacement(request.placement, 'B02-A');
}

function validateActivityScheduleEstablishRequest(
  request: TemporalActivityScheduleEstablishRequest,
): void {
  const activityRef = request.activityRef.trim();
  const operationId = request.operationId.trim();
  if (
    !/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
      activityRef,
    )
  ) {
    throw new RangeError('Activity reference must be a canonical UUIDv7 string.');
  }
  if (!operationId || operationId.length > 200) {
    throw new RangeError(
      'Schedule operation id must contain 1 to 200 characters.',
    );
  }
  validateFloatingLocalPlacement(request.placement, 'B02-B');
}

export function createRemoteTemporalActivityDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalActivityDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  return Object.freeze({
    async createActivity(
      request: TemporalActivityCreateRequest,
      signal?: AbortSignal,
    ): Promise<TemporalActivityCreateResult> {
      validateCreateRequest(request);
      const csrf = await csrfToken(webFetch, signal);
      const headers = new Headers({
        'Content-Type': 'application/json',
        [CSRF_HEADER_NAME]: csrf,
      });
      const response = await fetchResponse(webFetch, ACTIVITY_ENDPOINT, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          operation_id: request.operationId.trim(),
          title: request.title.trim(),
        }),
        ...(signal === undefined ? {} : { signal }),
      });
      const payload = await requireOk(response, 'Create Activity response');
      return parseActivity(payload, { allowReplay: true });
    },

    async createScheduledActivity(
      request: TemporalScheduledActivityCreateRequest,
      signal?: AbortSignal,
    ): Promise<TemporalScheduledActivityCreateResult> {
      validateScheduledCreateRequest(request);
      const csrf = await csrfToken(webFetch, signal);
      const headers = new Headers({
        'Content-Type': 'application/json',
        [CSRF_HEADER_NAME]: csrf,
      });
      const response = await fetchResponse(
        webFetch,
        SCHEDULED_ACTIVITY_ENDPOINT,
        {
          method: 'POST',
          headers,
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            title: request.title.trim(),
            placement: {
              kind: 'floating_local_interval',
              starts_local_at: request.placement.startsLocalAt.toString(),
              ends_local_at: request.placement.endsLocalAt.toString(),
            },
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      const payload = await requireOk(
        response,
        'Create Scheduled Activity response',
      );
      const result = parseScheduledActivity(payload);
      invalidateTemporalTimelineRead();
      return result;
    },

    async establishActivitySchedule(
      request: TemporalActivityScheduleEstablishRequest,
      signal?: AbortSignal,
    ): Promise<TemporalScheduledActivityCreateResult> {
      validateActivityScheduleEstablishRequest(request);
      const csrf = await csrfToken(webFetch, signal);
      const headers = new Headers({
        'Content-Type': 'application/json',
        [CSRF_HEADER_NAME]: csrf,
      });
      const response = await fetchResponse(
        webFetch,
        activityScheduleEndpoint(request.activityRef.trim().toLowerCase()),
        {
          method: 'POST',
          headers,
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            placement: {
              kind: 'floating_local_interval',
              starts_local_at: request.placement.startsLocalAt.toString(),
              ends_local_at: request.placement.endsLocalAt.toString(),
            },
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      const payload = await requireOk(
        response,
        'Establish Activity Schedule response',
      );
      const result = parseScheduledActivity(payload);
      if (
        result.activity.activityRef !==
        request.activityRef.trim().toLowerCase()
      ) {
        throw new TemporalActivityRemoteError(
          'protocol',
          'Established Schedule response changed the Activity identity.',
          response.status,
        );
      }
      invalidateTemporalTimelineRead();
      return result;
    },

    async loadUnplaced(
      signal?: AbortSignal,
    ): Promise<readonly TemporalActivityRecord[]> {
      const response = await fetchResponse(
        webFetch,
        UNPLACED_ACTIVITY_ENDPOINT,
        signal === undefined ? undefined : { signal },
      );
      const payload = await requireOk(response, 'Unplaced Activities response');
      if (
        !isRecord(payload) ||
        payload.kind !== 'unplaced' ||
        !Array.isArray(payload.items)
      ) {
        throw new TemporalActivityRemoteError(
          'protocol',
          'Unplaced Activities response has an unsupported representation.',
          response.status,
        );
      }
      requireExactKeys(
        payload,
        ['kind', 'items'],
        'Unplaced Activities response',
      );
      return Object.freeze(
        payload.items.map(
          (item) => parseActivity(item, { allowReplay: false }).activity,
        ),
      );
    },
  });
}
