import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CONTEXT_CODE = /^[a-z0-9][a-z0-9._:-]{0,119}$/;

export type TemporalReconciliationAction =
  | 'unresolved'
  | 'select'
  | 'accept_multiple'
  | 'defer'
  | 'escalate';
export type TemporalReconciliationEvidenceRole = 'considered' | 'selected';

export type TemporalReconciliationEvidenceView = Readonly<{
  confirmationRef: string;
  confirmationAttestationMaterialStateRef: string;
  roleCode: TemporalReconciliationEvidenceRole;
}>;

export type TemporalReconciliationView = Readonly<{
  reconciliationRef: string;
  outcomeRef: string;
  outcomeDispositionMaterialStateRef: string;
  purposeCode: string;
  materialStateRef: string;
  actionCode: TemporalReconciliationAction;
  resolvedByPersonRef: string;
  evidence: readonly TemporalReconciliationEvidenceView[];
  replayed: boolean;
}>;

export type RecordReconciliationCommand = Readonly<{
  operationId: string;
  outcomeDispositionMaterialStateRef: string;
  expectedMaterialStateRef: string | null;
  purposeCode: string;
  actionCode: TemporalReconciliationAction;
  evidence: readonly TemporalReconciliationEvidenceView[];
}>;

export class TemporalReconciliationRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalReconciliationRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalReconciliationRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function contextCode(value: unknown, field: string): string {
  if (typeof value !== 'string' || !CONTEXT_CODE.test(value)) {
    throw new TemporalReconciliationRemoteError('protocol', `Invalid Reconciliation ${field}.`);
  }
  return value;
}

function action(value: unknown): TemporalReconciliationAction {
  if (
    value !== 'unresolved' &&
    value !== 'select' &&
    value !== 'accept_multiple' &&
    value !== 'defer' &&
    value !== 'escalate'
  ) {
    throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation action_code.');
  }
  return value;
}

function evidenceRole(value: unknown): TemporalReconciliationEvidenceRole {
  if (value !== 'considered' && value !== 'selected') {
    throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation evidence role_code.');
  }
  return value;
}

function evidenceView(value: unknown): TemporalReconciliationEvidenceView {
  const payload = record(value);
  return Object.freeze({
    confirmationRef: uuid(payload.confirmation_ref, 'confirmation_ref'),
    confirmationAttestationMaterialStateRef: uuid(
      payload.confirmation_attestation_material_state_ref,
      'confirmation_attestation_material_state_ref',
    ),
    roleCode: evidenceRole(payload.role_code),
  });
}

function view(value: unknown): TemporalReconciliationView {
  const payload = record(value);
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation replay state.');
  }
  if (!Array.isArray(payload.evidence)) {
    throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation evidence list.');
  }
  return Object.freeze({
    reconciliationRef: uuid(payload.reconciliation_ref, 'reconciliation_ref'),
    outcomeRef: uuid(payload.outcome_ref, 'outcome_ref'),
    outcomeDispositionMaterialStateRef: uuid(
      payload.outcome_disposition_material_state_ref,
      'outcome_disposition_material_state_ref',
    ),
    purposeCode: contextCode(payload.purpose_code, 'purpose_code'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    actionCode: action(payload.action_code),
    resolvedByPersonRef: uuid(payload.resolved_by_person_ref, 'resolved_by_person_ref'),
    evidence: Object.freeze(payload.evidence.map(evidenceView)),
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalReconciliationDataSource(
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
      throw new TemporalReconciliationRemoteError(
        'authentication',
        'Reconciliation commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function problem(response: Response): Promise<TemporalReconciliationRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new TemporalReconciliationRemoteError(
        'http',
        'Reconciliation command rejected.',
        response.status,
      );
    }
    return new TemporalReconciliationRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Reconciliation command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  return Object.freeze({
    async list(outcomeRef: string): Promise<readonly TemporalReconciliationView[]> {
      const response = await webFetch(
        `/api/v1/temporal/outcomes/${encodeURIComponent(outcomeRef)}/reconciliations`,
      );
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.reconciliation.not_found') {
          return [];
        }
        throw error;
      }
      const payload: unknown = await response.json();
      if (!Array.isArray(payload)) {
        throw new TemporalReconciliationRemoteError('protocol', 'Invalid Reconciliation list.');
      }
      return Object.freeze(payload.map((item) => view({ ...record(item), replayed: false })));
    },

    async record(
      outcomeRef: string,
      command: RecordReconciliationCommand,
    ): Promise<TemporalReconciliationView> {
      if (!CONTEXT_CODE.test(command.purposeCode)) {
        throw new TemporalReconciliationRemoteError(
          'protocol',
          'Reconciliation purpose_code must be a contextual code.',
        );
      }
      const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      });
      const response = await webFetch(
        `/api/v1/temporal/outcomes/${encodeURIComponent(outcomeRef)}/reconciliations`,
        {
          method: 'POST',
          headers,
          body: JSON.stringify({
            operation_id: command.operationId,
            outcome_disposition_material_state_ref: command.outcomeDispositionMaterialStateRef,
            expected_material_state_ref: command.expectedMaterialStateRef,
            purpose_code: command.purposeCode,
            action_code: command.actionCode,
            evidence: command.evidence.map((item) => ({
              confirmation_ref: item.confirmationRef,
              confirmation_attestation_material_state_ref:
                item.confirmationAttestationMaterialStateRef,
              role_code: item.roleCode,
            })),
          }),
        },
      );
      if (!response.ok) throw await problem(response);
      return view(await response.json());
    },
  });
}
