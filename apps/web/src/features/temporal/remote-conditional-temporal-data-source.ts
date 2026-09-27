import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ConditionalTemporalSubjectKind = 'activity' | 'event' | 'occurrence';
export type ConditionalTemporalResult = 'satisfied' | 'not_satisfied' | 'indeterminate';
export type ConditionalTemporalDisposition = 'allow' | 'withhold';

export type ActualRealizationConditionView = Readonly<{
  conditionRef: string;
  subjectKind: ConditionalTemporalSubjectKind;
  subjectNativeRef: string;
  createdAt: string;
  replayed: boolean;
}>;

export type ConditionalEvaluationView = Readonly<{
  evaluationRef: string;
  conditionRef: string;
  resultCode: ConditionalTemporalResult;
  dispositionCode: ConditionalTemporalDisposition;
  actualRef: string | null;
  actualRealizationMaterialStateRef: string | null;
  evaluatedAt: string;
  replayed: boolean;
}>;

export class ConditionalTemporalRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'ConditionalTemporalRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new ConditionalTemporalRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function nullableUuid(value: unknown, field: string): string | null {
  return value === null ? null : uuid(value, field);
}

function subjectKind(value: unknown): ConditionalTemporalSubjectKind {
  if (value === 'activity' || value === 'event' || value === 'occurrence') return value;
  throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional subject kind.');
}

function condition(value: unknown): ActualRealizationConditionView {
  const payload = record(value);
  if (payload.family_code !== 'actual_realization' || typeof payload.created_at !== 'string') {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional intent.');
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional replay state.');
  }
  return Object.freeze({
    conditionRef: uuid(payload.condition_ref, 'condition_ref'),
    subjectKind: subjectKind(payload.subject_kind),
    subjectNativeRef: uuid(payload.subject_native_ref, 'subject_native_ref'),
    createdAt: payload.created_at,
    replayed: payload.replayed,
  });
}

function evaluation(value: unknown): ConditionalEvaluationView {
  const payload = record(value);
  if (
    payload.result_code !== 'satisfied' &&
    payload.result_code !== 'not_satisfied' &&
    payload.result_code !== 'indeterminate'
  ) {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional result.');
  }
  if (payload.disposition_code !== 'allow' && payload.disposition_code !== 'withhold') {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional disposition.');
  }
  if (typeof payload.evaluated_at !== 'string' || typeof payload.replayed !== 'boolean') {
    throw new ConditionalTemporalRemoteError('protocol', 'Invalid Conditional evaluation.');
  }
  return Object.freeze({
    evaluationRef: uuid(payload.evaluation_ref, 'evaluation_ref'),
    conditionRef: uuid(payload.condition_ref, 'condition_ref'),
    resultCode: payload.result_code,
    dispositionCode: payload.disposition_code,
    actualRef: nullableUuid(payload.actual_ref, 'actual_ref'),
    actualRealizationMaterialStateRef: nullableUuid(
      payload.actual_realization_material_state_ref,
      'actual_realization_material_state_ref',
    ),
    evaluatedAt: payload.evaluated_at,
    replayed: payload.replayed,
  });
}

export function createRemoteConditionalTemporalDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  const root = '/api/v1/temporal/conditions/actual-realization';

  async function problem(response: Response): Promise<ConditionalTemporalRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new ConditionalTemporalRemoteError(
        'http',
        'Conditional command rejected.',
        response.status,
      );
    }
    return new ConditionalTemporalRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Conditional command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const payload = record(await response.json());
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      payload.csrf_token.length === 0
    ) {
      throw new ConditionalTemporalRemoteError(
        'authentication',
        'Conditional commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  return Object.freeze({
    async find(
      kind: ConditionalTemporalSubjectKind,
      subjectRef: string,
    ): Promise<ActualRealizationConditionView | null> {
      const query = new URLSearchParams({
        subject_kind: kind,
        subject_native_ref: subjectRef,
      });
      const response = await webFetch(`${root}?${query.toString()}`);
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.conditional.not_found') {
          return null;
        }
        throw error;
      }
      return condition(await response.json());
    },

    async create(
      kind: ConditionalTemporalSubjectKind,
      subjectRef: string,
      operationId: string,
    ): Promise<ActualRealizationConditionView> {
      const response = await webFetch(root, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await csrf(),
        }),
        body: JSON.stringify({
          operation_id: operationId,
          subject_kind: kind,
          subject_native_ref: subjectRef,
        }),
      });
      if (!response.ok) throw await problem(response);
      return condition(await response.json());
    },

    async evaluate(
      conditionRef: string,
      operationId: string,
    ): Promise<ConditionalEvaluationView> {
      const response = await webFetch(`${root}/${encodeURIComponent(conditionRef)}/evaluations`, {
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await csrf(),
        }),
        body: JSON.stringify({ operation_id: operationId }),
      });
      if (!response.ok) throw await problem(response);
      return evaluation(await response.json());
    },
  });
}
