import { Temporal, type Instant } from '@dante/time';

import { createWebFetch } from '../../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type RecurringAuthoringOwner = 'routine' | 'event';

export type RecurringAuthoringCalendarRecurrence = Readonly<{
  family_code: 'calendar_wall_clock';
  range_kind: 'open' | 'until_boundary' | 'expected_count';
  expected_occurrence_count: number | null;
  effective_from: string;
  effective_until: string | null;
  pattern_code:
    | 'daily'
    | 'weekly_weekdays'
    | 'monthly_month_days'
    | 'monthly_ordinal_weekdays'
    | 'yearly_month_days'
    | 'anchor_step';
  interval_count: number;
  clock_basis_code: 'floating_local' | 'named_zone' | 'absolute_utc';
  zone_id: string | null;
  pattern_anchor_date: string | null;
  wall_times: readonly string[];
  weekdays: readonly number[];
  month_days: readonly number[];
  ordinal_weekdays: readonly Readonly<{
    weekday_number: number;
    ordinal: number;
  }>[];
  year_month_days: readonly Readonly<{
    month_number: number;
    month_day: number;
  }>[];
  nonexistent_local_time_policy: 'skip_civil_candidate' | null;
  ambiguous_local_time_policy: 'earlier' | 'later' | null;
  step_unit_code: 'day' | 'week' | 'month' | 'year' | null;
}>;

export type RecurringAuthoringElapsedRecurrence = Readonly<{
  family_code: 'elapsed_interval';
  range_kind: 'open' | 'until_boundary' | 'expected_count';
  expected_occurrence_count: number | null;
  effective_from: string;
  effective_until: string | null;
  elapsed_seconds: string;
  anchor_mode_code: 'fixed_anchor' | 'previous_expected';
  anchor_at: string;
}>;

export type RecurringAuthoringQuotaRecurrence = Readonly<{
  family_code: 'quota_per_period';
  range_kind: 'open' | 'until_boundary';
  expected_occurrence_count: null;
  effective_from: string;
  effective_until: string | null;
  quota_count: number;
  period_unit_code: 'day' | 'week' | 'month' | 'year';
  period_span: number;
  frame_code: 'floating_local' | 'named_zone' | 'absolute_utc';
  zone_id: string | null;
  week_start: number | null;
  pattern_anchor_date: string | null;
}>;

export type RecurringAuthoringCyclicRecurrence = Readonly<{
  family_code: 'cyclic_positional';
  range_kind: 'open' | 'until_boundary' | 'expected_count';
  expected_occurrence_count: number | null;
  effective_from: string;
  effective_until: string | null;
  cycle_length: number;
  position_unit_code: 'day' | 'week';
  pattern_anchor_date: string;
  generates_expected: readonly boolean[];
}>;

export type RecurringAuthoringRecurrence =
  | RecurringAuthoringCalendarRecurrence
  | RecurringAuthoringElapsedRecurrence
  | RecurringAuthoringQuotaRecurrence
  | RecurringAuthoringCyclicRecurrence;

export type CreateRecurringRoutineRequest = Readonly<{
  operationId: string;
  title: string;
  lifeAreaRef: string;
  tagRefs?: readonly string[];
  recurrence: RecurringAuthoringRecurrence;
}>;

export type CreateRecurringEventRequest = Readonly<{
  operationId: string;
  title: string;
  lifeAreaRef: string;
  agendaParts?: readonly string[];
  recurrence: RecurringAuthoringRecurrence;
}>;

export type RecurringAuthoringResult = Readonly<{
  ownerKind: RecurringAuthoringOwner;
  sourceRef: string;
  title: string;
  createdAt: Instant;
  recurrenceMaterialStateRef: string;
  replayed: boolean;
}>;

export type RecurringAuthoringRemoteFailureKind =
  | 'transport'
  | 'http'
  | 'protocol'
  | 'authentication';

export class RecurringAuthoringRemoteError extends Error {
  constructor(
    readonly kind: RecurringAuthoringRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'RecurringAuthoringRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring response.',
    );
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7.`,
    );
  }
  return value.toLowerCase();
}

function parseResult(value: unknown): RecurringAuthoringResult {
  const payload = record(value);
  const ownerKind = payload.owner_kind;
  if (ownerKind !== 'routine' && ownerKind !== 'event') {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring owner.',
    );
  }
  if (typeof payload.title !== 'string' || !payload.title.trim()) {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring title.',
    );
  }
  if (typeof payload.created_at !== 'string') {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring timestamp.',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring replay state.',
    );
  }
  let createdAt: Instant;
  try {
    createdAt = Temporal.Instant.from(payload.created_at);
  } catch {
    throw new RecurringAuthoringRemoteError(
      'protocol',
      'Invalid recurring authoring timestamp.',
    );
  }
  return Object.freeze({
    ownerKind,
    sourceRef: uuid(payload.source_ref, 'source_ref'),
    title: payload.title,
    createdAt,
    recurrenceMaterialStateRef: uuid(
      payload.recurrence_material_state_ref,
      'recurrence_material_state_ref',
    ),
    replayed: payload.replayed,
  });
}

export function createRemoteRecurringAuthoringDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function sessionCsrf(): Promise<string> {
    let response: Response;
    try {
      response = await webFetch('/api/v1/auth/session');
    } catch (error) {
      throw new RecurringAuthoringRemoteError(
        'transport',
        error instanceof Error ? error.message : 'Session unavailable.',
      );
    }
    let value: unknown;
    try {
      value = await response.json();
    } catch {
      throw new RecurringAuthoringRemoteError(
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
      throw new RecurringAuthoringRemoteError(
        'authentication',
        'Recurring authoring requires an authenticated session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function post(path: string, body: unknown): Promise<RecurringAuthoringResult> {
    const csrf = await sessionCsrf();
    let response: Response;
    try {
      response = await webFetch(path, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
          'X-Dante-CSRF': csrf,
        }),
        body: JSON.stringify(body),
      });
    } catch (error) {
      throw new RecurringAuthoringRemoteError(
        'transport',
        error instanceof Error ? error.message : 'Recurring authoring unavailable.',
      );
    }
    let value: unknown;
    try {
      value = await response.json();
    } catch {
      throw new RecurringAuthoringRemoteError(
        'protocol',
        'Invalid recurring authoring JSON.',
        response.status,
      );
    }
    if (!response.ok) {
      const problem = record(value);
      throw new RecurringAuthoringRemoteError(
        'http',
        typeof problem.detail === 'string'
          ? problem.detail
          : 'Recurring authoring rejected.',
        response.status,
        typeof problem.code === 'string' ? problem.code : null,
      );
    }
    return parseResult(value);
  }

  return Object.freeze({
    createRoutine(request: CreateRecurringRoutineRequest) {
      return post('/api/v1/temporal/recurring/routines', {
        operation_id: request.operationId,
        title: request.title,
        life_area_ref: request.lifeAreaRef,
        tag_refs: [...(request.tagRefs ?? [])],
        recurrence: request.recurrence,
      });
    },
    createEvent(request: CreateRecurringEventRequest) {
      return post('/api/v1/temporal/recurring/events', {
        operation_id: request.operationId,
        title: request.title,
        life_area_ref: request.lifeAreaRef,
        agenda_parts: [...(request.agendaParts ?? [])],
        recurrence: request.recurrence,
      });
    },
  });
}

export type RecurringAuthoringDataSource = ReturnType<
  typeof createRemoteRecurringAuthoringDataSource
>;
