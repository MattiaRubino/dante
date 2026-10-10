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

export type ObjectiveInputPayload = Readonly<{
  observed_boolean?: boolean | null;
  observed_numeric?: number | null;
  qualitative_code?: string | null;
  assessment_code?: ObjectiveAssessment | null;
}>;

export type ObjectiveInputDraftView = Readonly<{
  objectiveRef: string;
  payload: ObjectiveInputPayload;
  revision: number;
  confirmedAt: string | null;
  updatedAt: string;
}>;

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

export type ObjectiveDefinitionState = Readonly<{
  objectiveRef: string;
  definitionRevision: number;
  label: string;
  resultKind: ObjectiveKind;
  comparatorCode: ObjectiveComparator | null;
  targetValue: number | null;
  targetMin: number | null;
  targetMax: number | null;
  unitCode: string | null;
  presentationOrder: number;
  evaluationStateRef: string | null;
}>;

export type ActivityObjectiveBatchCreate = Readonly<{
  operationId: string;
  label: string;
  resultKind: ObjectiveKind;
  comparatorCode: ObjectiveComparator | null;
  targetValue: number | null;
  targetMin: number | null;
  targetMax: number | null;
  unitCode: string | null;
  presentationOrder: number;
}>;

export type ActivityObjectiveBatchRevision = Readonly<{
  objectiveRef: string;
  change: ObjectiveDefinitionChange;
}>;

export type ActivityObjectiveBatchRetirement = Readonly<{
  objectiveRef: string;
  operationId: string;
  expectedRevision: number;
}>;

export type ObjectiveSeriesEditState = Readonly<{
  sourceNativeRef: string;
  occurrenceRef: string;
  templateSlot: number;
  sourceRevision: number;
  recurrenceStateRef: string | null;
}>;

export type ObjectiveDefinitionChange = Readonly<{
  operationId: string;
  expectedRevision: number;
  label: string;
  resultKind: ObjectiveKind;
  comparatorCode: ObjectiveComparator | null;
  targetValue: number | null;
  targetMin: number | null;
  targetMax: number | null;
  unitCode: string | null;
  presentationOrder: number;
  scopeCode?: 'only_this' | 'this_and_following';
  seriesState?: ObjectiveSeriesEditState | null;
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

function parseObjectiveInputDraft(value: unknown): ObjectiveInputDraftView {
  const row = record(value);
  if (typeof row.objective_ref !== 'string' ||
      typeof row.revision !== 'number' ||
      !Number.isSafeInteger(row.revision) || row.revision < 1) {
    throw new Error('Bozza risultato Obiettivo non valida.');
  }
  const payload = record(row.payload);
  return Object.freeze({
    objectiveRef: row.objective_ref,
    payload: payload as ObjectiveInputPayload,
    revision: row.revision,
    confirmedAt: nullableString(row.confirmed_at),
    updatedAt: String(row.updated_at),
  });
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
    method: 'GET' | 'POST' | 'PUT',
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
    async getRealityMode(kind: RealitySubjectKind, subjectRef: string): Promise<RealityMode> {
      const row = record(await send(
        `/api/v1/temporal/${collection(kind)}/${encodeURIComponent(subjectRef)}/reality-policy`,
        'GET',
      ));
      if (row.subject_native_ref !== subjectRef ||
          !['manual', 'review_on_end', 'auto_confirm_outcome'].includes(String(row.mode_code))) {
        throw new Error('Invalid Reality policy response.');
      }
      return row.mode_code as RealityMode;
    },
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

    async applyActivityEdits(
      activityRef: string,
      edit: Readonly<{
        add: readonly ActivityObjectiveBatchCreate[];
        revise: readonly ActivityObjectiveBatchRevision[];
        retire: readonly ActivityObjectiveBatchRetirement[];
      }>,
    ): Promise<readonly ObjectiveView[]> {
      const controller = new AbortController();
      let timer: ReturnType<typeof setTimeout> | undefined;
      const timeout = new Promise<never>((_, reject) => {
        timer = setTimeout(() => {
          controller.abort();
          reject(new Error('Salvataggio obiettivi troppo lento. Riprova senza perdere le modifiche.'));
        }, 20_000);
      });
      try {
        return await Promise.race([(async () => {
          const response = await webFetch(
          `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/objective-edits`,
          {
            method: 'PUT',
            signal: controller.signal,
            headers: {
              'Content-Type': 'application/json',
              'X-Dante-CSRF': await csrf(),
            },
            body: JSON.stringify({
              add: edit.add.map((item) => ({
                operation_id: item.operationId,
                label: item.label, result_kind: item.resultKind,
                comparator_code: item.comparatorCode,
                target_value: item.targetValue, target_min: item.targetMin,
                target_max: item.targetMax, unit_code: item.unitCode,
                presentation_order: item.presentationOrder,
              })),
              revise: edit.revise.map((item) => ({
                objective_ref: item.objectiveRef,
                change: {
                  operation_id: item.change.operationId,
                  expected_revision: item.change.expectedRevision,
                  scope_code: item.change.scopeCode ?? 'only_this',
                  expected_source_revision: item.change.seriesState?.sourceRevision ?? null,
                  expected_recurrence_state_ref:
                    item.change.seriesState?.recurrenceStateRef ?? null,
                  label: item.change.label, result_kind: item.change.resultKind,
                  comparator_code: item.change.comparatorCode,
                  target_value: item.change.targetValue,
                  target_min: item.change.targetMin,
                  target_max: item.change.targetMax,
                  unit_code: item.change.unitCode,
                  presentation_order: item.change.presentationOrder,
                },
              })),
              retire: edit.retire.map((item) => ({
                objective_ref: item.objectiveRef,
                operation_id: item.operationId,
                expected_revision: item.expectedRevision,
              })),
            }),
          },
        );
        const payload: unknown = await response.json();
        if (!response.ok) {
          const problem = record(payload);
          throw new Error(typeof problem.detail === 'string'
            ? problem.detail : 'Impossibile salvare gli obiettivi.');
        }
        if (!Array.isArray(payload)) {
          throw new Error('Risposta Obiettivi non valida.');
        }
          return Object.freeze(payload.map(parseObjectiveView));
        })(), timeout]);
      } finally {
        if (timer) clearTimeout(timer);
      }
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

    async listObjectiveInputDrafts(): Promise<readonly ObjectiveInputDraftView[]> {
      const payload = await send('/api/v1/temporal/objective-inputs', 'GET');
      if (!Array.isArray(payload)) throw new Error('Bozze risultati Obiettivi non valide.');
      return Object.freeze(payload.map(parseObjectiveInputDraft));
    },

    async stageObjectiveInput(
      objectiveRef: string,
      payload: ObjectiveInputPayload,
      expectedRevision: number | null,
      operationId: string,
    ): Promise<ObjectiveInputDraftView> {
      return parseObjectiveInputDraft(await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/input-draft`,
        'PUT',
        {
          operation_id: operationId,
          expected_revision: expectedRevision,
          input: payload,
        },
      ));
    },

    async confirmObjectiveInput(
      objectiveRef: string, expectedRevision: number, operationId: string,
    ): Promise<void> {
      await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/confirm-input`,
        'POST',
        { operation_id: operationId, expected_revision: expectedRevision },
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

    async getSeriesState(
      objectiveRef: string,
    ): Promise<ObjectiveSeriesEditState | null> {
      const payload = await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/series-state`,
        'GET',
      );
      if (payload === null) return null;
      const state = record(payload);
      if (typeof state.source_native_ref !== 'string' ||
          typeof state.occurrence_ref !== 'string' ||
          !Number.isSafeInteger(state.template_slot) ||
          !Number.isSafeInteger(state.source_revision) ||
          typeof state.source_revision !== 'number' ||
          state.source_revision < 0) {
        throw new Error('Provenienza ricorrente dell’obiettivo non valida.');
      }
      return Object.freeze({
        sourceNativeRef: state.source_native_ref,
        occurrenceRef: state.occurrence_ref,
        templateSlot: state.template_slot as number,
        sourceRevision: state.source_revision as number,
        recurrenceStateRef: nullableString(state.recurrence_state_ref),
      });
    },

    async getDefinition(objectiveRef: string): Promise<ObjectiveDefinitionState> {
      const row = record(await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/definition`,
        'GET',
      ));
      if (row.objective_ref !== objectiveRef ||
          !Number.isSafeInteger(row.definition_revision) ||
          (row.definition_revision as number) < 0) {
        throw new Error('Versione della definizione non valida.');
      }
      return Object.freeze({
        objectiveRef,
        definitionRevision: row.definition_revision as number,
        label: String(row.label),
        resultKind: row.result_kind as ObjectiveKind,
        comparatorCode: nullableString(row.comparator_code) as ObjectiveComparator | null,
        targetValue: nullableNumber(row.target_value),
        targetMin: nullableNumber(row.target_min),
        targetMax: nullableNumber(row.target_max),
        unitCode: nullableString(row.unit_code),
        presentationOrder: Number(row.presentation_order),
        evaluationStateRef: nullableString(row.evaluation_state_ref),
      });
    },

    async reviseDefinition(
      objectiveRef: string,
      change: ObjectiveDefinitionChange,
    ): Promise<void> {
      const row = record(await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/definition`,
        'PUT',
        {
          operation_id: change.operationId,
          expected_revision: change.expectedRevision,
          scope_code: change.scopeCode ?? 'only_this',
          expected_source_revision: change.seriesState?.sourceRevision ?? null,
          expected_recurrence_state_ref: change.seriesState?.recurrenceStateRef ?? null,
          label: change.label,
          result_kind: change.resultKind,
          comparator_code: change.comparatorCode,
          target_value: change.targetValue,
          target_min: change.targetMin,
          target_max: change.targetMax,
          unit_code: change.unitCode,
          presentation_order: change.presentationOrder,
        },
      ));
      if (row.objective_ref !== objectiveRef) {
        throw new Error('Identità dell’obiettivo modificato non coerente.');
      }
    },

    async correctResult(
      objectiveRef: string,
      command: Readonly<{
        operationId: string;
        expectedEvaluationStateRef: string;
        observedBoolean: boolean | null;
        observedNumeric: number | null;
        qualitativeCode: string | null;
        assessmentCode: ObjectiveAssessment | null;
      }>,
    ): Promise<void> {
      const row = record(await send(
        `/api/v1/temporal/objectives/${encodeURIComponent(objectiveRef)}/correction`,
        'POST',
        {
          operation_id: command.operationId,
          expected_evaluation_state_ref: command.expectedEvaluationStateRef,
          observed_boolean: command.observedBoolean,
          observed_numeric: command.observedNumeric,
          qualitative_code: command.qualitativeCode,
          assessment_code: command.assessmentCode,
        },
      ));
      if (row.objective_ref !== objectiveRef) {
        throw new Error('La correzione non corrisponde all’obiettivo richiesto.');
      }
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
