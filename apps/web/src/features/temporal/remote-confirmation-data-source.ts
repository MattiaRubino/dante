import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CONTEXT_CODE = /^[a-z0-9][a-z0-9._:-]{0,119}$/;

export type TemporalConfirmationView = Readonly<{
  confirmationRef: string;
  outcomeRef: string;
  outcomeDispositionMaterialStateRef: string;
  confirmerPersonRef: string;
  purposeCode: string;
  materialStateRef: string;
  stanceCode: string;
  confirmerIsSelf: boolean;
  replayed: boolean;
}>;

export type RecordConfirmationCommand = Readonly<{
  operationId: string;
  outcomeDispositionMaterialStateRef: string;
  expectedMaterialStateRef: string | null;
  purposeCode: string;
  stanceCode: string;
}>;

export class TemporalConfirmationRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalConfirmationRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalConfirmationRemoteError('protocol', 'Invalid Confirmation response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalConfirmationRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function contextCode(value: unknown, field: string): string {
  if (typeof value !== 'string' || !CONTEXT_CODE.test(value)) {
    throw new TemporalConfirmationRemoteError('protocol', `Invalid Confirmation ${field}.`);
  }
  return value;
}

function view(value: unknown): TemporalConfirmationView {
  const payload = record(value);
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalConfirmationRemoteError('protocol', 'Invalid Confirmation replay state.');
  }
  if (typeof payload.confirmer_is_self !== 'boolean') {
    throw new TemporalConfirmationRemoteError('protocol', 'Invalid Confirmation actor flag.');
  }
  return Object.freeze({
    confirmationRef: uuid(payload.confirmation_ref, 'confirmation_ref'),
    outcomeRef: uuid(payload.outcome_ref, 'outcome_ref'),
    outcomeDispositionMaterialStateRef: uuid(
      payload.outcome_disposition_material_state_ref,
      'outcome_disposition_material_state_ref',
    ),
    confirmerPersonRef: uuid(payload.confirmer_person_ref, 'confirmer_person_ref'),
    purposeCode: contextCode(payload.purpose_code, 'purpose_code'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    stanceCode: contextCode(payload.stance_code, 'stance_code'),
    confirmerIsSelf: payload.confirmer_is_self,
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalConfirmationDataSource(
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
      throw new TemporalConfirmationRemoteError(
        'authentication',
        'Confirmation commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function problem(response: Response): Promise<TemporalConfirmationRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new TemporalConfirmationRemoteError(
        'http',
        'Confirmation command rejected.',
        response.status,
      );
    }
    return new TemporalConfirmationRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Confirmation command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  return Object.freeze({
    async list(outcomeRef: string): Promise<readonly TemporalConfirmationView[]> {
      const response = await webFetch(
        `/api/v1/temporal/outcomes/${encodeURIComponent(outcomeRef)}/confirmations`,
      );
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.confirmation.not_found') {
          return [];
        }
        throw error;
      }
      const payload: unknown = await response.json();
      if (!Array.isArray(payload)) {
        throw new TemporalConfirmationRemoteError('protocol', 'Invalid Confirmation list.');
      }
      return Object.freeze(payload.map((item) => view({ ...record(item), replayed: false })));
    },

    async record(
      outcomeRef: string,
      command: RecordConfirmationCommand,
    ): Promise<TemporalConfirmationView> {
      if (!CONTEXT_CODE.test(command.purposeCode) || !CONTEXT_CODE.test(command.stanceCode)) {
        throw new TemporalConfirmationRemoteError(
          'protocol',
          'Confirmation purpose_code and stance_code must be contextual codes.',
        );
      }
      const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      });
      const response = await webFetch(
        `/api/v1/temporal/outcomes/${encodeURIComponent(outcomeRef)}/confirmations`,
        {
          method: 'POST',
          headers,
          body: JSON.stringify({
            operation_id: command.operationId,
            outcome_disposition_material_state_ref: command.outcomeDispositionMaterialStateRef,
            expected_material_state_ref: command.expectedMaterialStateRef,
            purpose_code: command.purposeCode,
            stance_code: command.stanceCode,
          }),
        },
      );
      if (!response.ok) throw await problem(response);
      return view(await response.json());
    },
  });
}
