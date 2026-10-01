import { Temporal } from '@dante/time';

import { createWebFetch } from '../../platform/api/web-fetch';
import type {
  TemporalPlanningTrayDataSource,
  TemporalPlanningTrayItem,
  TemporalPlanningTrayPlaceRequest,
  TemporalPlanningTrayPlaceResult,
} from './planning-tray-data-source';
import type { TemporalSchedulePlacementInput } from './schedule-data-source';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

const ENDPOINT = '/api/v1/temporal/planning-tray';
const SESSION_ENDPOINT = '/api/v1/auth/session';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export class TemporalPlanningTrayRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalPlanningTrayRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function parseUuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalPlanningTrayRemoteError('protocol', `${field} must be UUIDv7.`);
  }
  return value.toLowerCase();
}

function parseNullableUuid(value: unknown, field: string): string | null {
  return value === null || value === undefined ? null : parseUuid(value, field);
}

function parseRevision(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  if (typeof value !== 'number' || !Number.isInteger(value) || value < 1) {
    throw new TemporalPlanningTrayRemoteError(
      'protocol',
      'Life Area assignment revision must be a positive integer.',
    );
  }
  return value;
}

function parseItem(value: unknown): TemporalPlanningTrayItem {
  if (!isRecord(value)) {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item must be an object.');
  }
  if (value.kind !== 'activity' && value.kind !== 'event') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item kind is invalid.');
  }
  if (value.state !== 'unplaced' && value.state !== 'postponed') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item state is invalid.');
  }
  if (value.kind === 'activity' && value.state === 'postponed') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Only Events can be postponed.');
  }
  if (typeof value.title !== 'string' || !value.title.trim()) {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item title is invalid.');
  }
  if (typeof value.created_at !== 'string') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item created_at is invalid.');
  }
  let createdAt: Temporal.Instant;
  try {
    createdAt = Temporal.Instant.from(value.created_at);
  } catch {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Planning item created_at is invalid.');
  }
  const scheduleRef = parseNullableUuid(value.schedule_ref, 'schedule_ref');
  if (value.state === 'postponed' && scheduleRef === null) {
    throw new TemporalPlanningTrayRemoteError(
      'protocol',
      'Postponed Event must retain its Schedule reference.',
    );
  }
  return Object.freeze({
    kind: value.kind,
    state: value.state,
    subjectRef: parseUuid(value.subject_ref, 'subject_ref'),
    title: value.title,
    createdAt,
    lifeAreaRef: parseNullableUuid(value.life_area_ref, 'life_area_ref'),
    lifeAreaAssignmentRevision: parseRevision(value.life_area_assignment_revision),
    scheduleRef,
  });
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

async function fetchResponse(
  webFetch: typeof globalThis.fetch,
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<Response> {
  try {
    return await webFetch(input, init);
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error;
    throw new TemporalPlanningTrayRemoteError(
      'transport',
      'Da collocare could not reach DANTE.',
    );
  }
}

async function json(response: Response, label: string): Promise<unknown> {
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new TemporalPlanningTrayRemoteError('protocol', `${label} is not valid JSON.`);
  }
  if (!response.ok) {
    throw new TemporalPlanningTrayRemoteError(
      'http',
      `${label} failed with HTTP ${response.status}.`,
      response.status,
      isRecord(payload) && typeof payload.code === 'string' ? payload.code : null,
    );
  }
  return payload;
}

async function csrfToken(webFetch: typeof globalThis.fetch, signal?: AbortSignal) {
  const response = await fetchResponse(
    webFetch,
    SESSION_ENDPOINT,
    signal === undefined ? undefined : { signal },
  );
  const payload = await json(response, 'Auth session response');
  if (
    !isRecord(payload) ||
    payload.authenticated !== true ||
    typeof payload.csrf_token !== 'string' ||
    !payload.csrf_token
  ) {
    throw new TemporalPlanningTrayRemoteError(
      'authentication',
      'Da collocare requires an authenticated browser session.',
    );
  }
  return payload.csrf_token;
}

function parsePlacementResult(value: unknown): TemporalPlanningTrayPlaceResult {
  if (!isRecord(value)) {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Placement response must be an object.');
  }
  if (value.kind !== 'activity' && value.kind !== 'event') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Placement response kind is invalid.');
  }
  if (typeof value.replayed !== 'boolean') {
    throw new TemporalPlanningTrayRemoteError('protocol', 'Placement replayed flag is invalid.');
  }
  return Object.freeze({
    kind: value.kind,
    subjectRef: parseUuid(value.subject_ref, 'subject_ref'),
    scheduleRef: parseUuid(value.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: parseUuid(
      value.placement_material_state_ref,
      'placement_material_state_ref',
    ),
    replayed: value.replayed,
  });
}

export function createRemoteTemporalPlanningTrayDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
): TemporalPlanningTrayDataSource {
  const webFetch = createWebFetch(fetchFn);
  return Object.freeze({
    async listItems(signal?: AbortSignal) {
      const response = await fetchResponse(
        webFetch,
        ENDPOINT,
        signal === undefined ? undefined : { signal },
      );
      const payload = await json(response, 'Planning tray response');
      if (!Array.isArray(payload)) {
        throw new TemporalPlanningTrayRemoteError(
          'protocol',
          'Planning tray response must be an array.',
        );
      }
      return Object.freeze(payload.map(parseItem));
    },
    async placeItem(request: TemporalPlanningTrayPlaceRequest, signal?: AbortSignal) {
      if (!request.operationId.trim() || request.operationId.trim().length > 200) {
        throw new RangeError('Planning operation id must contain 1 to 200 characters.');
      }
      parseUuid(request.subjectRef, 'subjectRef');
      const csrf = await csrfToken(webFetch, signal);
      const response = await fetchResponse(
        webFetch,
        `${ENDPOINT}/${request.kind}/${request.subjectRef}/place`,
        {
          method: 'POST',
          headers: new Headers({
            'Content-Type': 'application/json',
            [CSRF_HEADER_NAME]: csrf,
          }),
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            placement: serializePlacement(request.placement),
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      const result = parsePlacementResult(await json(response, 'Planning placement response'));
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return result;
    },
  });
}
