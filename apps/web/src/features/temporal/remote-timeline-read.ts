import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const TEMPORAL_TIMELINE_WINDOW_ENDPOINT = '/api/v1/temporal/timeline/window';
const MAX_TIMELINE_WINDOW_DAYS = 62;

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

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function parseEmptyWindow(payload: unknown): TemporalTimelineWindow {
  if (!isRecord(payload) || payload.kind !== 'empty') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline response has an unsupported representation.',
    );
  }

  const allowedKeys = new Set([
    'kind',
    'start_date',
    'end_date_exclusive',
    'effective_zone_id',
  ]);
  for (const key of Object.keys(payload)) {
    if (!allowedKeys.has(key)) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        `Temporal Timeline response contains unexpected field ${key}.`,
      );
    }
  }

  const startDate = parsePlainDateKey(payload.start_date, 'start_date');
  const endDateExclusive = parsePlainDateKey(
    payload.end_date_exclusive,
    'end_date_exclusive',
  );
  if (typeof payload.effective_zone_id !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'effective_zone_id must be a named IANA timezone.',
    );
  }

  let effectiveZoneId: string;
  try {
    effectiveZoneId = validateNamedTimeZone(payload.effective_zone_id);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'effective_zone_id must be a named IANA timezone.',
    );
  }

  return Object.freeze({
    kind: 'empty',
    startDate,
    endDateExclusive,
    effectiveZoneId,
  });
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

      const window = parseEmptyWindow(payload);
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
