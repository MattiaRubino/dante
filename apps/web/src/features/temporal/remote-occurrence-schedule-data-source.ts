import { Temporal, validateNamedTimeZone } from '@dante/time';

import { createWebFetch } from '../../platform/api/web-fetch';
import type { TemporalSchedulePlacementInput } from './schedule-data-source';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type TemporalOccurrenceScheduleEstablishRequest = Readonly<{
  operationId: string;
  occurrenceRef: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalOccurrenceScheduleEstablishResult = Readonly<{
  occurrenceRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  replayed: boolean;
}>;

export type TemporalOccurrenceScheduleRemoteFailureKind =
  | 'transport'
  | 'http'
  | 'protocol'
  | 'authentication';

export class TemporalOccurrenceScheduleRemoteError extends Error {
  constructor(
    readonly kind: TemporalOccurrenceScheduleRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalOccurrenceScheduleRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalOccurrenceScheduleRemoteError(
      'protocol',
      'Invalid Occurrence Schedule response.',
    );
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalOccurrenceScheduleRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7.`,
    );
  }
  return value.toLowerCase();
}

function serializePlacement(placement: TemporalSchedulePlacementInput) {
  switch (placement.kind) {
    case 'date-span':
      if (
        Temporal.PlainDate.compare(
          placement.startDate,
          placement.endDateExclusive,
        ) >= 0
      ) {
        throw new RangeError('Schedule date span must be positive.');
      }
      return {
        kind: 'date_span',
        start_date: placement.startDate.toString(),
        end_date_exclusive: placement.endDateExclusive.toString(),
      } as const;
    case 'floating-local-interval':
      if (
        Temporal.PlainDateTime.compare(
          placement.startsLocalAt,
          placement.endsLocalAt,
        ) >= 0
      ) {
        throw new RangeError('Floating Schedule interval must be positive.');
      }
      return {
        kind: 'floating_local_interval',
        starts_local_at: placement.startsLocalAt.toString(),
        ends_local_at: placement.endsLocalAt.toString(),
      } as const;
    case 'named-zone-local-interval':
      if (
        Temporal.PlainDateTime.compare(
          placement.startsLocalAt,
          placement.endsLocalAt,
        ) >= 0
      ) {
        throw new RangeError('Named-zone Schedule interval must be positive.');
      }
      validateNamedTimeZone(placement.zoneId);
      return {
        kind: 'named_zone_local_interval',
        starts_local_at: placement.startsLocalAt.toString(),
        ends_local_at: placement.endsLocalAt.toString(),
        zone_id: placement.zoneId,
        disambiguation: placement.disambiguation,
      } as const;
    case 'absolute-interval':
      if (Temporal.Instant.compare(placement.startsAt, placement.endsAt) >= 0) {
        throw new RangeError('Absolute Schedule interval must be positive.');
      }
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

export function createRemoteTemporalOccurrenceScheduleDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    let response: Response;
    try {
      response = await webFetch('/api/v1/auth/session');
    } catch (error) {
      throw new TemporalOccurrenceScheduleRemoteError(
        'transport',
        error instanceof Error ? error.message : 'Session unavailable.',
      );
    }
    let value: unknown;
    try {
      value = await response.json();
    } catch {
      throw new TemporalOccurrenceScheduleRemoteError(
        'protocol',
        'Invalid session response.',
        response.status,
      );
    }
    const payload = record(value);
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      !payload.csrf_token
    ) {
      throw new TemporalOccurrenceScheduleRemoteError(
        'authentication',
        'Occurrence Schedule requires an authenticated session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  return Object.freeze({
    async establish(
      request: TemporalOccurrenceScheduleEstablishRequest,
    ): Promise<TemporalOccurrenceScheduleEstablishResult> {
      const csrfToken = await csrf();
      let response: Response;
      try {
        response = await webFetch(
          `/api/v1/temporal/occurrences/${encodeURIComponent(
            request.occurrenceRef,
          )}/schedule`,
          {
            method: 'POST',
            headers: new Headers({
              'Content-Type': 'application/json',
              'X-Dante-CSRF': csrfToken,
            }),
            body: JSON.stringify({
              operation_id: request.operationId,
              placement: serializePlacement(request.placement),
            }),
          },
        );
      } catch (error) {
        throw new TemporalOccurrenceScheduleRemoteError(
          'transport',
          error instanceof Error ? error.message : 'Occurrence Schedule unavailable.',
        );
      }

      let value: unknown;
      try {
        value = await response.json();
      } catch {
        throw new TemporalOccurrenceScheduleRemoteError(
          'protocol',
          'Invalid Occurrence Schedule JSON.',
          response.status,
        );
      }
      if (!response.ok) {
        const problem = record(value);
        throw new TemporalOccurrenceScheduleRemoteError(
          'http',
          typeof problem.detail === 'string'
            ? problem.detail
            : 'Occurrence Schedule rejected.',
          response.status,
          typeof problem.code === 'string' ? problem.code : null,
        );
      }
      const payload = record(value);
      if (typeof payload.replayed !== 'boolean') {
        throw new TemporalOccurrenceScheduleRemoteError(
          'protocol',
          'Invalid Occurrence Schedule replay state.',
        );
      }
      return Object.freeze({
        occurrenceRef: uuid(payload.occurrence_ref, 'occurrence_ref'),
        scheduleRef: uuid(payload.schedule_ref, 'schedule_ref'),
        placementMaterialStateRef: uuid(
          payload.placement_material_state_ref,
          'placement_material_state_ref',
        ),
        replayed: payload.replayed,
      });
    },
  });
}
