import { createWebFetch } from '../../platform/api/web-fetch';

export type RealitySubjectKind = 'activity' | 'event' | 'occurrence';
export type RealityMode = 'manual' | 'review_on_end' | 'auto_confirm_outcome';
export type ObjectiveKind = 'boolean' | 'quantity' | 'qualitative' | 'range';
export type ObjectiveComparator = 'eq' | 'gte' | 'lte' | 'between';
export type ObjectiveAssessment =
  | 'satisfied'
  | 'partial'
  | 'not_satisfied'
  | 'unknown'
  | 'indeterminate';

export type ObjectiveView = Readonly<{
  objectiveRef: string;
  label: string;
  resultKind: ObjectiveKind;
  comparatorCode: ObjectiveComparator | null;
  targetValue: number | null;
  targetMin: number | null;
  targetMax: number | null;
  unitCode: string | null;
  presentationOrder: number;
  observationRef: string | null;
  observedBoolean: boolean | null;
  observedNumeric: number | null;
  qualitativeCode: string | null;
  evaluationStateRef: string | null;
  assessmentCode: ObjectiveAssessment | null;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Invalid Reality/Objectives response.');
  }
  return value as Record<string, unknown>;
}

function nullableNumber(value: unknown): number | null {
  if (value === null) return null;
  const parsed = typeof value === 'number' ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function nullableString(value: unknown): string | null {
  if (value === null) return null;
  if (typeof value !== 'string') throw new Error('Invalid Objective response.');
  return value;
}

export function parseObjectiveView(value: unknown): ObjectiveView {
  const row = record(value);
  return Object.freeze({
    objectiveRef: String(row.objective_ref),
    label: String(row.label),
    resultKind: row.result_kind as ObjectiveKind,
    comparatorCode:
      row.comparator_code === null
        ? null
        : (row.comparator_code as ObjectiveComparator),
    targetValue: nullableNumber(row.target_value),
    targetMin: nullableNumber(row.target_min),
    targetMax: nullableNumber(row.target_max),
    unitCode: nullableString(row.unit_code),
    presentationOrder: Number(row.presentation_order),
    observationRef: nullableString(row.observation_ref),
    observedBoolean:
      row.observed_boolean === null ? null : Boolean(row.observed_boolean),
    observedNumeric: nullableNumber(row.observed_numeric),
    qualitativeCode: nullableString(row.qualitative_code),
    evaluationStateRef: nullableString(row.evaluation_state_ref),
    assessmentCode:
      row.assessment_code === null
        ? null
        : (row.assessment_code as ObjectiveAssessment),
  });
}

export function createRemoteRealityObjectiveDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const row = record(await response.json());
    if (
      !response.ok ||
      row.authenticated !== true ||
      typeof row.csrf_token !== 'string' ||
      !row.csrf_token
    ) {
      throw new Error('Reality/Objectives require an authenticated session.');
    }
    return row.csrf_token;
  }

  async function send(
    path: string,
    method: 'GET' | 'POST',
    body?: unknown,
  ): Promise<unknown> {
    const headers = new Headers();
    if (method !== 'GET') {
      headers.set('Content-Type', 'application/json');
      headers.set('X-Dante-CSRF', await csrf());
    }
    const response = await webFetch(path, {
      method,
      headers,
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const payload: unknown = await response.json();
    if (!response.ok) {
      const problem = record(payload);
      throw new Error(
        typeof problem.detail === 'string'
          ? problem.detail
          : 'Reality/Objectives request rejected.',
      );
    }
    return payload;
  }

  const collection = (kind: RealitySubjectKind) =>
    kind === 'activity'
      ? 'activities'
      : kind === 'event'
        ? 'events'
        : 'occurrences';

  return Object.freeze({
    async configureReality(
      kind: RealitySubjectKind,
      subjectRef: string,
      command: Readonly<{
        operationId: string;
        mode: RealityMode;
        expectedStateRef?: string | null;
      }>,
    ): Promise<void> {
      await send(
        `/api/v1/temporal/${collection(kind)}/${encodeURIComponent(subjectRef)}/reality-policy`,
        'POST',
        {
          operation_id: command.operationId,
          mode_code: command.mode,
          expected_state_ref: command.expectedStateRef ?? null,
        },
      );
    },

    async createObjective(
      kind: 'activity' | 'event',
      subjectRef: string,
      command: Readonly<{
        operationId: string;
        label: string;
        resultKind: ObjectiveKind;
        comparatorCode: ObjectiveComparator | null;
        targetValue: number | null;
        targetMin: number | null;
        targetMax: number | null;
        unitCode: string | null;
        presentationOrder: number;
      }>,
    ): Promise<ObjectiveView> {
      return parseObjectiveView(
        await send(
          `/api/v1/temporal/${collection(kind)}/${encodeURIComponent(subjectRef)}/objectives`,
          'POST',
          {
            operation_id: command.operationId,
            label: command.label,
            result_kind: command.resultKind,
            comparator_code: command.comparatorCode,
            target_value: command.targetValue,
            target_min: command.targetMin,
            target_max: command.targetMax,
            unit_code: command.unitCode,
            presentation_order: command.presentationOrder,
          },
        ),
      );
    },

    async listObjectives(
      kind: RealitySubjectKind,
      subjectRef: string,
    ): Promise<readonly ObjectiveView[]> {
      const payload = await send(
        `/api/v1/temporal/${collection(kind)}/${encodeURIComponent(subjectRef)}/objectives`,
        'GET',
      );
      if (!Array.isArray(payload)) throw new Error('Objectives must be a list.');
      return Object.freeze(payload.map(parseObjectiveView));
    },

    async recordResult(
      objectiveRef: string,
      command: Readonly<{
        operationId: string;
        observedBoolean?: boolean | null;
        observedNumeric?: number | null;
        qualitativeCode?: string | null;
        assessmentCode?: ObjectiveAssessment | null;
      }>,
    ): Promise<void> {
      await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/result`,
        'POST',
        {
          operation_id: command.operationId,
          observed_boolean: command.observedBoolean ?? null,
          observed_numeric: command.observedNumeric ?? null,
          qualitative_code: command.qualitativeCode ?? null,
          assessment_code: command.assessmentCode ?? null,
        },
      );
    },
  });
}
