import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalAuthorActivityRequest,
  TemporalAuthorEventRequest,
  TemporalAuthoringDataSource,
  TemporalAuthoringItem,
  TemporalAuthoringLifeAreaInput,
  TemporalAuthoringSchedule,
  TemporalAuthoredActivityResult,
  TemporalAuthoredEventResult,
  TemporalSessionCaptureMode,
} from './authoring-data-source';
import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const ACTIVITY_ENDPOINT = '/api/v1/temporal/authoring/activities';
const EVENT_ENDPOINT = '/api/v1/temporal/authoring/events';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const COLOR = /^#[0-9A-F]{6}$/;

export type TemporalAuthoringRemoteFailureKind =
  'transport' | 'http' | 'protocol' | 'authentication';

export class TemporalAuthoringRemoteError extends Error {
  public constructor(
    readonly kind: TemporalAuthoringRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalAuthoringRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

function exactKeys(
  payload: Record<string, unknown>,
  required: readonly string[],
  optional: readonly string[] = [],
): void {
  const allowed = new Set([...required, ...optional]);
  for (const key of Object.keys(payload)) {
    if (!allowed.has(key)) {
      throw new TemporalAuthoringRemoteError(
        'protocol',
        `Authoring response contains unexpected field ${key}.`,
      );
    }
  }
  for (const key of required) {
    if (!(key in payload)) {
      throw new TemporalAuthoringRemoteError(
        'protocol',
        `Authoring response is missing ${key}.`,
      );
    }
  }
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function nullableUuid(value: unknown, field: string): string | null {
  return value === null ? null : uuid(value, field);
}

function positiveRevision(value: unknown, field: string): number | null {
  if (value === null) return null;
  if (typeof value !== 'number' || !Number.isInteger(value) || value < 1) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a positive integer or null.`,
    );
  }
  return value;
}

function nullableText(value: unknown, field: string): string | null {
  if (value === null) return null;
  if (typeof value !== 'string' || !value.trim() || value.trim() !== value) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be canonical non-empty text or null.`,
    );
  }
  return value;
}

function nullableColor(value: unknown, field: string): string | null {
  if (value === null) return null;
  if (typeof value !== 'string' || !COLOR.test(value)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be #RRGGBB or null.`,
    );
  }
  return value;
}

function instant(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
}

function plainDate(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a PlainDate string.`,
    );
  }
  try {
    const parsed = Temporal.PlainDate.from(value);
    if (parsed.toString() !== value) throw new RangeError('non-canonical');
    return parsed;
  } catch {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
}

function localDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
}

function acceptedPlacement(
  payload: unknown,
): TemporalAcceptedSchedulePlacement {
  if (!isRecord(payload) || typeof payload.kind !== 'string') {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Authoring schedule placement is invalid.',
    );
  }
  switch (payload.kind) {
    case 'date_span': {
      exactKeys(payload, ['kind', 'start_date', 'end_date_exclusive']);
      const startDate = plainDate(payload.start_date, 'start_date');
      const endDateExclusive = plainDate(
        payload.end_date_exclusive,
        'end_date_exclusive',
      );
      if (Temporal.PlainDate.compare(startDate, endDateExclusive) >= 0) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring date span must be positive.',
        );
      }
      return Object.freeze({
        kind: 'date-span' as const,
        startDate,
        endDateExclusive,
      });
    }
    case 'floating_local_interval': {
      exactKeys(payload, ['kind', 'starts_local_at', 'ends_local_at']);
      const startsLocalAt = localDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = localDateTime(payload.ends_local_at, 'ends_local_at');
      if (Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring floating-local interval must be positive.',
        );
      }
      return Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt,
        endsLocalAt,
      });
    }
    case 'named_zone_local_interval': {
      exactKeys(payload, [
        'kind',
        'starts_local_at',
        'ends_local_at',
        'zone_id',
        'disambiguation',
        'resolved_start_at',
        'resolved_end_at',
      ]);
      const startsLocalAt = localDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = localDateTime(payload.ends_local_at, 'ends_local_at');
      const resolvedStartAt = instant(
        payload.resolved_start_at,
        'resolved_start_at',
      );
      const resolvedEndAt = instant(payload.resolved_end_at, 'resolved_end_at');
      if (
        Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
        Temporal.Instant.compare(resolvedStartAt, resolvedEndAt) >= 0
      ) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring named-zone interval must be positive.',
        );
      }
      if (
        payload.disambiguation !== 'reject' &&
        payload.disambiguation !== 'earlier' &&
        payload.disambiguation !== 'later'
      ) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring disambiguation is unsupported.',
        );
      }
      if (typeof payload.zone_id !== 'string') {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring zone_id must be text.',
        );
      }
      const zoneId = validateNamedTimeZone(payload.zone_id);
      return Object.freeze({
        kind: 'named-zone-local-interval' as const,
        startsLocalAt,
        endsLocalAt,
        zoneId,
        disambiguation: payload.disambiguation,
        resolvedStartAt,
        resolvedEndAt,
      });
    }
    case 'absolute_interval': {
      exactKeys(payload, ['kind', 'starts_at', 'ends_at']);
      const startsAt = instant(payload.starts_at, 'starts_at');
      const endsAt = instant(payload.ends_at, 'ends_at');
      if (Temporal.Instant.compare(startsAt, endsAt) >= 0) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring absolute interval must be positive.',
        );
      }
      return Object.freeze({
        kind: 'absolute-interval' as const,
        startsAt,
        endsAt,
      });
    }
    case 'coarse_local_period': {
      exactKeys(payload, ['kind', 'local_date', 'period']);
      if (
        payload.period !== 'morning' &&
        payload.period !== 'afternoon' &&
        payload.period !== 'evening'
      ) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Authoring coarse period is unsupported.',
        );
      }
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: plainDate(payload.local_date, 'local_date'),
        period: payload.period,
      });
    }
    default:
      throw new TemporalAuthoringRemoteError(
        'protocol',
        'Authoring placement kind is unsupported.',
      );
  }
}

function schedule(value: unknown): TemporalAuthoringSchedule | null {
  if (value === null) return null;
  if (!isRecord(value)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Authoring schedule must be an object or null.',
    );
  }
  exactKeys(value, [
    'schedule_ref',
    'placement_material_state_ref',
    'placement',
  ]);
  return Object.freeze({
    scheduleRef: uuid(value.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: uuid(
      value.placement_material_state_ref,
      'placement_material_state_ref',
    ),
    placement: acceptedPlacement(value.placement),
  });
}

function schedules(
  value: unknown,
  field: string,
): readonly TemporalAuthoringSchedule[] {
  if (!Array.isArray(value)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      `${field} must be an array.`,
    );
  }
  return Object.freeze(
    value.map((entry) => {
      const parsed = schedule(entry);
      if (parsed === null) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          `${field} must contain schedules.`,
        );
      }
      return parsed;
    }),
  );
}

function captureMode(value: unknown): TemporalSessionCaptureMode {
  if (
    value === 'disabled' ||
    value === 'record' ||
    value === 'live' ||
    value === 'record_and_live'
  ) {
    return value;
  }
  throw new TemporalAuthoringRemoteError(
    'protocol',
    'Activity session_capture_mode is unsupported.',
  );
}

function authoredChild(value: unknown) {
  if (!isRecord(value)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Activity child must be an object.',
    );
  }
  exactKeys(value, [
    'activity_ref',
    'title',
    'decomposition_ref',
    'decomposition_state_ref',
    'requirement_code',
    'presentation_order',
    'schedule',
    'planned_slices',
    'session_capture_mode',
  ]);
  if (
    typeof value.title !== 'string' ||
    !value.title.trim() ||
    (value.requirement_code !== 'required' &&
      value.requirement_code !== 'optional') ||
    typeof value.presentation_order !== 'number' ||
    !Number.isInteger(value.presentation_order) ||
    value.presentation_order < 1
  ) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Activity child metadata is invalid.',
    );
  }
  return Object.freeze({
    activityRef: uuid(value.activity_ref, 'activity_ref'),
    title: value.title,
    decompositionRef: uuid(value.decomposition_ref, 'decomposition_ref'),
    decompositionStateRef: uuid(
      value.decomposition_state_ref,
      'decomposition_state_ref',
    ),
    requirementCode: value.requirement_code,
    presentationOrder: value.presentation_order,
    schedule: schedule(value.schedule),
    plannedSlices: schedules(value.planned_slices, 'planned_slices'),
    sessionCaptureMode: captureMode(value.session_capture_mode),
  });
}

const COMMON_RESPONSE_KEYS = [
  'title',
  'created_at',
  'description',
  'location',
  'color_code',
  'life_area_ref',
  'life_area_assignment_revision',
  'life_area_color_code',
  'life_area_revision',
  'schedule',
  'replayed',
] as const;

function item(
  payload: Record<string, unknown>,
  refField: 'activity_ref' | 'event_ref',
): TemporalAuthoringItem {
  if (typeof payload.title !== 'string' || !payload.title.trim()) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Authoring title must be non-empty text.',
    );
  }
  return Object.freeze({
    subjectRef: uuid(payload[refField], refField),
    title: payload.title,
    createdAt: instant(payload.created_at, 'created_at'),
    description: nullableText(payload.description, 'description'),
    location: nullableText(payload.location, 'location'),
    colorCode: nullableColor(payload.color_code, 'color_code'),
    lifeAreaRef: nullableUuid(payload.life_area_ref, 'life_area_ref'),
    lifeAreaAssignmentRevision: positiveRevision(
      payload.life_area_assignment_revision,
      'life_area_assignment_revision',
    ),
    lifeAreaColorCode: nullableColor(
      payload.life_area_color_code,
      'life_area_color_code',
    ),
    lifeAreaRevision: positiveRevision(
      payload.life_area_revision,
      'life_area_revision',
    ),
  });
}

function activityResult(payload: unknown): TemporalAuthoredActivityResult {
  if (!isRecord(payload)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Activity authoring response must be an object.',
    );
  }
  exactKeys(payload, [
    'activity_ref',
    ...COMMON_RESPONSE_KEYS,
    'session_capture_mode',
    'child_guard_mode',
    'planned_slices',
    'activity_intervals',
    'children',
  ]);
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Activity authoring replayed must be boolean.',
    );
  }
  return Object.freeze({
    item: item(payload, 'activity_ref'),
    schedule: schedule(payload.schedule),
    sessionCaptureMode: captureMode(payload.session_capture_mode),
    childGuardMode: (() => {
      if (
        payload.child_guard_mode === 'none' ||
        payload.child_guard_mode === 'confirm' ||
        payload.child_guard_mode === 'block'
      ) {
        return payload.child_guard_mode;
      }
      throw new TemporalAuthoringRemoteError(
        'protocol',
        'Activity child_guard_mode is unsupported.',
      );
    })(),
    plannedSlices: schedules(payload.planned_slices, 'planned_slices'),
    activityIntervals: schedules(
      payload.activity_intervals,
      'activity_intervals',
    ),
    children: (() => {
      if (!Array.isArray(payload.children)) {
        throw new TemporalAuthoringRemoteError(
          'protocol',
          'Activity children must be an array.',
        );
      }
      return Object.freeze(payload.children.map(authoredChild));
    })(),
    replayed: payload.replayed,
  });
}

function eventResult(payload: unknown): TemporalAuthoredEventResult {
  if (!isRecord(payload)) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Event authoring response must be an object.',
    );
  }
  exactKeys(payload, [
    'event_ref',
    ...COMMON_RESPONSE_KEYS,
    'agenda_revision',
    'agenda_parts',
  ]);
  if (
    typeof payload.agenda_revision !== 'number' ||
    !Number.isInteger(payload.agenda_revision) ||
    payload.agenda_revision < 0
  ) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Event agenda_revision must be a non-negative integer.',
    );
  }
  if (
    !Array.isArray(payload.agenda_parts) ||
    payload.agenda_parts.some((part) => typeof part !== 'string')
  ) {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Event agenda_parts must be text[].',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalAuthoringRemoteError(
      'protocol',
      'Event authoring replayed must be boolean.',
    );
  }
  return Object.freeze({
    item: item(payload, 'event_ref'),
    schedule: schedule(payload.schedule),
    replayed: payload.replayed,
    agendaRevision: payload.agenda_revision,
    agendaParts: Object.freeze([...payload.agenda_parts] as string[]),
  });
}

function lifeAreaPayload(
  value: TemporalAuthoringLifeAreaInput | undefined,
): Record<string, unknown> | undefined {
  if (value === undefined) return undefined;
  const result: Record<string, unknown> = {};
  if (value.lifeAreaRef !== undefined) result.life_area_ref = value.lifeAreaRef;
  if (value.newName !== undefined) result.new_name = value.newName.trim();
  if (value.expectedRevision !== undefined) {
    result.expected_revision = value.expectedRevision;
  }
  if (value.colorCode !== undefined) {
    result.color_code = value.colorCode.toUpperCase();
  }
  return result;
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

function requestBody(
  request: TemporalAuthorActivityRequest | TemporalAuthorEventRequest,
): Record<string, unknown> {
  const result: Record<string, unknown> = {
    operation_id: request.operationId.trim(),
    title: request.title.trim(),
    description: request.description?.trim() || null,
    location: request.location?.trim() || null,
    item_color_code: request.itemColorCode?.toUpperCase() ?? null,
    life_area: lifeAreaPayload(request.lifeArea) ?? null,
    placement:
      request.placement === undefined
        ? null
        : serializePlacement(request.placement),
  };
  if ('agendaParts' in request) result.agenda_parts = [...request.agendaParts];
  else {
    if (request.sessionCaptureMode !== undefined) {
      result.session_capture_mode = request.sessionCaptureMode;
    }
    if (request.minimumSessionDurationMicroseconds !== undefined) {
      result.minimum_session_duration_microseconds =
        request.minimumSessionDurationMicroseconds;
    }
    if (request.childGuardMode !== undefined) {
      result.child_guard_mode = request.childGuardMode;
    }
    if (request.plannedSlices !== undefined) {
      result.planned_slices = request.plannedSlices.map(serializePlacement);
    }
    if (request.activityIntervals !== undefined) {
      result.activity_intervals =
        request.activityIntervals.map(serializePlacement);
    }
    if (request.plannedSliceNames !== undefined) {
      result.planned_slice_names = [...request.plannedSliceNames];
    }
    if (request.children !== undefined) {
      result.children = request.children.map((child) => ({
        title: child.title.trim(),
        description: child.description?.trim() || null,
        requirement_code: child.requirementCode ?? 'required',
        presentation_order: child.presentationOrder ?? 1,
        placement:
          child.placement === undefined
            ? null
            : serializePlacement(child.placement),
        planned_slices: child.plannedSlices?.map(serializePlacement) ?? [],
        ...(child.plannedSliceNames === undefined
          ? {}
          : { planned_slice_names: [...child.plannedSliceNames] }),
        session_capture_mode: child.sessionCaptureMode ?? null,
      }));
    }
  }
  return result;
}

async function readJson(response: Response, label: string): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalAuthoringRemoteError(
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
    throw new TemporalAuthoringRemoteError(
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
    if (isAbortError(error)) throw error;
    throw new TemporalAuthoringRemoteError(
      'transport',
      'Authoring request could not reach DANTE.',
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
    throw new TemporalAuthoringRemoteError(
      'authentication',
      'Authoring requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

function validateCommon(request: TemporalAuthorActivityRequest): void {
  if (!request.operationId.trim() || request.operationId.trim().length > 200) {
    throw new RangeError(
      'Authoring operation id must contain 1 to 200 characters.',
    );
  }
  if (!request.title.trim() || request.title.trim().length > 300) {
    throw new RangeError('Authoring title must contain 1 to 300 characters.');
  }
}

export function createRemoteTemporalAuthoringDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalAuthoringDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  const mutate = async (
    endpoint: string,
    request: TemporalAuthorActivityRequest | TemporalAuthorEventRequest,
    signal: AbortSignal | undefined,
  ): Promise<unknown> => {
    validateCommon(request);
    const csrf = await csrfToken(webFetch, signal);
    const response = await fetchResponse(webFetch, endpoint, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
        [CSRF_HEADER_NAME]: csrf,
      }),
      body: JSON.stringify(requestBody(request)),
      ...(signal === undefined ? {} : { signal }),
    });
    return await requireOk(response, 'Authoring response');
  };

  return Object.freeze({
    async authorActivity(
      request: TemporalAuthorActivityRequest,
      signal?: AbortSignal,
    ) {
      const result = activityResult(
        await mutate(ACTIVITY_ENDPOINT, request, signal),
      );
      invalidateTemporalTimelineRead();
      return result;
    },
    async authorEvent(
      request: TemporalAuthorEventRequest,
      signal?: AbortSignal,
    ) {
      const result = eventResult(await mutate(EVENT_ENDPOINT, request, signal));
      invalidateTemporalTimelineRead();
      return result;
    },
  });
}
