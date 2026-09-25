import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CONTEXT_CODE = /^[a-z][a-z0-9._-]{0,99}$/;

export type TemporalOutcomeView = Readonly<{
  outcomeRef: string;
  actualRef: string;
  vocabularyCode: string;
  materialStateRef: string;
  resultCode: string;
  note: string | null;
  replayed: boolean;
}>;

export type RecordOutcomeCommand = Readonly<{
  operationId: string;
  expectedMaterialStateRef: string | null;
  resultCode: string;
  note: string | null;
}>;

export class TemporalOutcomeRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalOutcomeRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalOutcomeRemoteError('protocol', 'Invalid Outcome response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalOutcomeRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function contextualCode(value: unknown, field: string): string {
  if (typeof value !== 'string' || !CONTEXT_CODE.test(value)) {
    throw new TemporalOutcomeRemoteError('protocol', `${field} must be a contextual code.`);
  }
  return value;
}

function view(value: unknown): TemporalOutcomeView {
  const payload = record(value);
  if (
    typeof payload.replayed !== 'boolean' ||
    (payload.note !== null && typeof payload.note !== 'string')
  ) {
    throw new TemporalOutcomeRemoteError('protocol', 'Invalid Outcome result state.');
  }
  return Object.freeze({
    outcomeRef: uuid(payload.outcome_ref, 'outcome_ref'),
    actualRef: uuid(payload.actual_ref, 'actual_ref'),
    vocabularyCode: contextualCode(payload.vocabulary_code, 'vocabulary_code'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    resultCode: contextualCode(payload.result_code, 'result_code'),
    note: payload.note as string | null,
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalOutcomeDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const payload = record(await response.json());
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      !payload.csrf_token
    ) {
      throw new TemporalOutcomeRemoteError(
        'authentication',
        'Outcome commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function problem(response: Response): Promise<TemporalOutcomeRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new TemporalOutcomeRemoteError('http', 'Outcome command rejected.', response.status);
    }
    return new TemporalOutcomeRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Outcome command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  function assertVocabularyCode(vocabularyCode: string): string {
    const normalized = vocabularyCode.trim();
    if (normalized !== vocabularyCode || !CONTEXT_CODE.test(normalized)) {
      throw new TemporalOutcomeRemoteError(
        'protocol',
        'Outcome vocabulary_code must be a contextual code.',
      );
    }
    return normalized;
  }

  return Object.freeze({
    async get(actualRef: string, vocabularyCode: string): Promise<TemporalOutcomeView | null> {
      const vocabulary = assertVocabularyCode(vocabularyCode);
      const response = await webFetch(
        `/api/v1/temporal/actuals/${encodeURIComponent(actualRef)}/outcomes/${encodeURIComponent(vocabulary)}`,
      );
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.outcome.not_found') {
          return null;
        }
        throw error;
      }
      return view(await response.json());
    },

    async record(
      actualRef: string,
      vocabularyCode: string,
      command: RecordOutcomeCommand,
    ): Promise<TemporalOutcomeView> {
      const vocabulary = assertVocabularyCode(vocabularyCode);
      const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      });
      const response = await webFetch(
        `/api/v1/temporal/actuals/${encodeURIComponent(actualRef)}/outcomes/${encodeURIComponent(vocabulary)}`,
        {
          method: 'POST',
          headers,
          body: JSON.stringify({
            operation_id: command.operationId,
            expected_material_state_ref: command.expectedMaterialStateRef,
            result_code: command.resultCode,
            note: command.note,
          }),
        },
      );
      if (!response.ok) throw await problem(response);
      return view(await response.json());
    },
  });
}