import { Temporal } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalScheduleDataSource,
  TemporalScheduleRevisionRequest,
  TemporalScheduleRevisionResult,
} from './schedule-data-source';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const schedulePlacementEndpoint = (scheduleRef: string) =>
  `/api/v1/temporal/schedules/${encodeURIComponent(scheduleRef)}/placement`;

export type TemporalScheduleRemoteFailureKind =
  'transport' | 'http' | 'protocol' | 'authentication';

export class TemporalScheduleRemoteError extends Error {
  constructor(
    readonly kind: TemporalScheduleRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalScheduleRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function exactKeys(
  payload: Record<string, unknown>,
  allowed: readonly string[],
  label: string,
): void {
  const accepted = new Set(allowed);
  for (const key of Object.keys(payload)) {
    if (!accepted.has(key)) {
      throw new TemporalScheduleRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
}

function uuidV7(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function localDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalScheduleRemoteError(
      'protocol',
      `${field} must be a floating local date-time without zone or offset.`,
    );
  }
}

function validateRequest(request: TemporalScheduleRevisionRequest): void {
  if (!UUID_V7.test(request.scheduleRef.trim())) {
    throw new RangeError(
      'Schedule reference must be a canonical UUIDv7 string.',
    );
  }
  if (!UUID_V7.test(request.expectedPlacementMaterialStateRef.trim())) {
    throw new RangeError(
      'Expected placement MaterialState reference must be a canonical UUIDv7 string.',
    );
  }
  const operationId = request.operationId.trim();
  if (!operationId || operationId.length > 200) {
    throw new RangeError(
      'Schedule operation id must contain 1 to 200 characters.',
    );
  }
  if (
    request.placement.kind !== 'floating-local-interval' ||
    Temporal.PlainDateTime.compare(
      request.placement.startsLocalAt,
      request.placement.endsLocalAt,
    ) >= 0 ||
    !request.placement.startsLocalAt
      .toPlainDate()
      .equals(request.placement.endsLocalAt.toPlainDate())
  ) {
    throw new RangeError(
      'B02-C supports only positive same-local-day floating-local intervals.',
    );
  }
}

async function responseJson(
  response: Response,
  label: string,
): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalScheduleRemoteError(
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

async function okJson(response: Response, label: string): Promise<unknown> {
  const payload = await responseJson(response, label);
  if (!response.ok) {
    throw new TemporalScheduleRemoteError(
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
  init?: RequestInit,
): Promise<Response> {
  try {
    return await webFetch(input, init);
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw error;
    }
    throw new TemporalScheduleRemoteError(
      'transport',
      'Schedule revision could not reach DANTE.',
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
  const payload = await okJson(response, 'Auth session response');
  if (
    !isRecord(payload) ||
    payload.authenticated !== true ||
    typeof payload.csrf_token !== 'string' ||
    payload.csrf_token.length === 0
  ) {
    throw new TemporalScheduleRemoteError(
      'authentication',
      'Schedule revision requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

function parseRevision(
  payload: unknown,
  request: TemporalScheduleRevisionRequest,
  status: number,
): TemporalScheduleRevisionResult {
  if (!isRecord(payload)) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      'Schedule revision response must be an object.',
      status,
    );
  }
  exactKeys(
    payload,
    [
      'schedule_ref',
      'previous_placement_material_state_ref',
      'placement_material_state_ref',
      'temporal_form',
      'starts_local_at',
      'ends_local_at',
      'replayed',
    ],
    'Schedule revision response',
  );
  if (
    payload.temporal_form !== 'floating_local' ||
    typeof payload.replayed !== 'boolean'
  ) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      'Schedule revision response changed the accepted temporal form.',
      status,
    );
  }

  const scheduleRef = uuidV7(payload.schedule_ref, 'schedule_ref');
  const previousPlacementMaterialStateRef = uuidV7(
    payload.previous_placement_material_state_ref,
    'previous_placement_material_state_ref',
  );
  const startsLocalAt = localDateTime(
    payload.starts_local_at,
    'starts_local_at',
  );
  const endsLocalAt = localDateTime(payload.ends_local_at, 'ends_local_at');
  if (
    Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
    !startsLocalAt.toPlainDate().equals(endsLocalAt.toPlainDate())
  ) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      'Schedule revision response must be a positive same-local-day interval.',
      status,
    );
  }
  const placementMaterialStateRef = uuidV7(
    payload.placement_material_state_ref,
    'placement_material_state_ref',
  );
  if (
    scheduleRef !== request.scheduleRef.trim().toLowerCase() ||
    previousPlacementMaterialStateRef !==
      request.expectedPlacementMaterialStateRef.trim().toLowerCase() ||
    placementMaterialStateRef === previousPlacementMaterialStateRef ||
    !startsLocalAt.equals(request.placement.startsLocalAt) ||
    !endsLocalAt.equals(request.placement.endsLocalAt)
  ) {
    throw new TemporalScheduleRemoteError(
      'protocol',
      'Schedule revision response changed its identity, basis, or accepted placement.',
      status,
    );
  }

  return Object.freeze({
    scheduleRef,
    previousPlacementMaterialStateRef,
    placementMaterialStateRef,
    placement: Object.freeze({
      kind: 'floating-local-interval' as const,
      startsLocalAt,
      endsLocalAt,
    }),
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalScheduleDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalScheduleDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);
  return Object.freeze({
    async reviseSchedule(
      request: TemporalScheduleRevisionRequest,
      signal?: AbortSignal,
    ): Promise<TemporalScheduleRevisionResult> {
      validateRequest(request);
      const csrf = await csrfToken(webFetch, signal);
      const response = await fetchResponse(
        webFetch,
        schedulePlacementEndpoint(request.scheduleRef.trim().toLowerCase()),
        {
          method: 'PATCH',
          headers: new Headers({
            'Content-Type': 'application/json',
            [CSRF_HEADER_NAME]: csrf,
          }),
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            expected_placement_material_state_ref:
              request.expectedPlacementMaterialStateRef.trim().toLowerCase(),
            placement: {
              kind: 'floating_local_interval',
              starts_local_at: request.placement.startsLocalAt.toString(),
              ends_local_at: request.placement.endsLocalAt.toString(),
            },
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      const payload = await okJson(response, 'Revise Schedule response');
      return parseRevision(payload, request, response.status);
    },
  });
}
