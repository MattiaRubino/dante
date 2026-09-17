import { Temporal } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalEventAgendaDataSource,
  TemporalEventAgendaReplaceRequest,
  TemporalEventAgendaReplaceResult,
  TemporalEventDetailRecord,
} from './event-data-source';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const EVENT_ENDPOINT = '/api/v1/temporal/events';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type TemporalEventAgendaRemoteFailureKind =
  | 'transport'
  | 'http'
  | 'protocol'
  | 'authentication';

export class TemporalEventAgendaRemoteError extends Error {
  public constructor(
    readonly kind: TemporalEventAgendaRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalEventAgendaRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

function parseEventRef(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseAgendaParts(value: unknown): readonly string[] {
  if (!Array.isArray(value) || value.length > 100) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event Agenda must contain at most 100 ordered parts.',
    );
  }
  return Object.freeze(
    value.map((part, index) => {
      if (
        typeof part !== 'string' ||
        part.length === 0 ||
        part.length > 1000 ||
        part.trim() !== part
      ) {
        throw new TemporalEventAgendaRemoteError(
          'protocol',
          `Event Agenda part ${index + 1} is not canonical text.`,
        );
      }
      return part;
    }),
  );
}

function normalizeAgendaParts(value: readonly string[]): readonly string[] {
  if (value.length > 100) {
    throw new RangeError('Event Agenda may contain at most 100 parts.');
  }
  return Object.freeze(
    value.map((part) => {
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

function requireExactKeys(
  payload: Record<string, unknown>,
  keys: readonly string[],
  label: string,
): void {
  const expected = new Set(keys);
  for (const key of Object.keys(payload)) {
    if (!expected.has(key)) {
      throw new TemporalEventAgendaRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
  for (const key of keys) {
    if (!(key in payload)) {
      throw new TemporalEventAgendaRemoteError(
        'protocol',
        `${label} is missing required field ${key}.`,
      );
    }
  }
}

function parseRevision(value: unknown, minimum: number, field: string): number {
  if (!Number.isSafeInteger(value) || (value as number) < minimum) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      `${field} must be a safe integer >= ${minimum}.`,
    );
  }
  return value as number;
}

function parseInstant(value: unknown): Temporal.Instant {
  if (typeof value !== 'string') {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'created_at must be an absolute timestamp.',
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'created_at must be an absolute timestamp.',
    );
  }
}

function parseEvent(payload: unknown): TemporalEventDetailRecord {
  if (!isRecord(payload)) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event response must be an object.',
    );
  }
  requireExactKeys(
    payload,
    [
      'event_ref',
      'title',
      'agenda_revision',
      'agenda_parts',
      'created_at',
      'replayed',
    ],
    'Event response',
  );
  if (typeof payload.title !== 'string' || payload.title.trim() !== payload.title || !payload.title) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event title must be canonical non-empty text.',
    );
  }
  if (payload.replayed !== false) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event read response cannot claim mutation replay.',
    );
  }
  return Object.freeze({
    eventRef: parseEventRef(payload.event_ref, 'event_ref'),
    title: payload.title,
    agendaRevision: parseRevision(payload.agenda_revision, 0, 'agenda_revision'),
    agendaParts: parseAgendaParts(payload.agenda_parts),
    createdAt: parseInstant(payload.created_at),
  });
}

function parseMutation(payload: unknown): TemporalEventAgendaReplaceResult {
  if (!isRecord(payload)) {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event Agenda mutation response must be an object.',
    );
  }
  requireExactKeys(
    payload,
    ['event_ref', 'agenda_revision', 'agenda_parts', 'replayed'],
    'Event Agenda mutation response',
  );
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalEventAgendaRemoteError(
      'protocol',
      'Event Agenda replayed must be boolean.',
    );
  }
  return Object.freeze({
    eventRef: parseEventRef(payload.event_ref, 'event_ref'),
    agendaRevision: parseRevision(payload.agenda_revision, 1, 'agenda_revision'),
    agendaParts: parseAgendaParts(payload.agenda_parts),
    replayed: payload.replayed,
  });
}

async function fetchResponse(
  webFetch: typeof globalThis.fetch,
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<Response> {
  try {
    return await webFetch(input, init);
  } catch (error) {
    if (isAbortError(error)) {
      throw error;
    }
    throw new TemporalEventAgendaRemoteError(
      'transport',
      'Event Agenda request could not reach DANTE.',
    );
  }
}

async function readJson(response: Response, label: string): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalEventAgendaRemoteError(
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
    throw new TemporalEventAgendaRemoteError(
      'http',
      `${label} failed with HTTP ${response.status}.`,
      response.status,
      problemCode(payload),
    );
  }
  return payload;
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
    throw new TemporalEventAgendaRemoteError(
      'authentication',
      'Event Agenda mutation requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

export function createRemoteTemporalEventAgendaDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalEventAgendaDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  return Object.freeze({
    async loadEvent(
      eventRef: string,
      signal?: AbortSignal,
    ): Promise<TemporalEventDetailRecord> {
      const normalizedEventRef = parseEventRef(eventRef, 'eventRef');
      const response = await fetchResponse(
        webFetch,
        `${EVENT_ENDPOINT}/${normalizedEventRef}`,
        signal === undefined ? undefined : { signal },
      );
      return parseEvent(await requireOk(response, 'Event response'));
    },

    async replaceAgenda(
      request: TemporalEventAgendaReplaceRequest,
      signal?: AbortSignal,
    ): Promise<TemporalEventAgendaReplaceResult> {
      const eventRef = parseEventRef(request.eventRef, 'eventRef');
      const operationId = request.operationId.trim();
      if (!operationId || operationId.length > 200) {
        throw new RangeError(
          'Event Agenda operation id must contain 1 to 200 characters.',
        );
      }
      if (!Number.isSafeInteger(request.expectedRevision) || request.expectedRevision < 0) {
        throw new RangeError('Event Agenda expected revision must be non-negative.');
      }
      const agendaParts = normalizeAgendaParts(request.agendaParts);
      const csrf = await csrfToken(webFetch, signal);
      const response = await fetchResponse(
        webFetch,
        `${EVENT_ENDPOINT}/${eventRef}/agenda`,
        {
          method: 'PUT',
          headers: new Headers({
            'Content-Type': 'application/json',
            [CSRF_HEADER_NAME]: csrf,
          }),
          body: JSON.stringify({
            operation_id: operationId,
            expected_revision: request.expectedRevision,
            agenda_parts: agendaParts,
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      return parseMutation(
        await requireOk(response, 'Event Agenda mutation response'),
      );
    },
  });
}
