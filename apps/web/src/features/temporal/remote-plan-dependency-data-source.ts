import { createWebFetch } from '../../platform/api/web-fetch';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EVALUATION = new Set(['satisfied', 'unsatisfied', 'unknown']);

export type PlanDependency = Readonly<{
  dependencyRef: string;
  planRef: string;
  prerequisiteStepRef: string;
  prerequisiteActivityRef: string;
  dependentStepRef: string;
  dependentActivityRef: string;
  stateRef: string;
  purposeCode: 'dependent_activity_admissibility';
  qualifierCode: 'actual_occurred' | 'outcome_code';
  dispositionCode: string | null;
  active: boolean;
  recordedAt: string;
  evaluationCode: 'satisfied' | 'unsatisfied' | 'unknown' | null;
  cycle: boolean;
  replayed: boolean;
}>;

export type PlanDependencyIntent = Readonly<{
  prerequisiteStepRef: string;
  dependentStepRef: string;
  qualifierCode: PlanDependency['qualifierCode'];
  dispositionCode: string | null;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Risposta Dependency non valida.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown): string {
  if (typeof value !== 'string' || !UUID.test(value)) {
    throw new Error('Riferimento Dependency non valido.');
  }
  return value.toLowerCase();
}

function dependency(value: unknown): PlanDependency {
  const row = record(value);
  const qualifier = row.qualifier_code;
  const code = row.disposition_code;
  const evaluation = row.evaluation_code;
  if ((qualifier !== 'actual_occurred' && qualifier !== 'outcome_code') ||
      (qualifier === 'actual_occurred' && code !== null) ||
      (qualifier === 'outcome_code' && (typeof code !== 'string' || !code)) ||
      row.purpose_code !== 'dependent_activity_admissibility' ||
      (evaluation !== null &&
        (typeof evaluation !== 'string' || !EVALUATION.has(evaluation))) ||
      typeof row.active !== 'boolean' || typeof row.cycle !== 'boolean' ||
      typeof row.replayed !== 'boolean' || typeof row.recorded_at !== 'string' ||
      !Number.isFinite(Date.parse(row.recorded_at))) {
    throw new Error('Stato Dependency non valido.');
  }
  return Object.freeze({
    dependencyRef: uuid(row.dependency_ref),
    planRef: uuid(row.plan_ref),
    prerequisiteStepRef: uuid(row.prerequisite_step_ref),
    prerequisiteActivityRef: uuid(row.prerequisite_activity_ref),
    dependentStepRef: uuid(row.dependent_step_ref),
    dependentActivityRef: uuid(row.dependent_activity_ref),
    stateRef: uuid(row.state_ref),
    purposeCode: 'dependent_activity_admissibility',
    qualifierCode: qualifier,
    dispositionCode: code as string | null,
    active: row.active,
    recordedAt: row.recorded_at,
    evaluationCode: evaluation as PlanDependency['evaluationCode'],
    cycle: row.cycle,
    replayed: row.replayed,
  });
}

async function failure(response: Response): Promise<Error> {
  try {
    const payload = record(await response.json());
    if (typeof payload.detail === 'string' && payload.detail.trim()) {
      return new Error(payload.detail);
    }
  } catch {
    // Keep the HTTP status if ProblemDetails is unreadable.
  }
  return new Error(`Dependency non disponibile (HTTP ${response.status}).`);
}

export function createRemotePlanDependencyDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  const path = (planRef: string) =>
    `/api/v1/temporal/plans/${encodeURIComponent(planRef)}/dependencies`;

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    if (!response.ok) throw new Error('Sessione non disponibile.');
    const payload = record(await response.json());
    if (payload.authenticated !== true || typeof payload.csrf_token !== 'string' ||
        !payload.csrf_token) {
      throw new Error('Accedi prima di modificare una Dependency.');
    }
    return payload.csrf_token;
  }

  async function mutate(
    endpoint: string, method: 'POST' | 'PUT', body: Record<string, unknown>,
  ): Promise<PlanDependency> {
    const response = await webFetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw await failure(response);
    return dependency(await response.json());
  }

  function body(intent: PlanDependencyIntent, operationId: string) {
    return {
      operation_id: operationId,
      prerequisite_step_ref: intent.prerequisiteStepRef,
      dependent_step_ref: intent.dependentStepRef,
      qualifier_code: intent.qualifierCode,
      disposition_code: intent.dispositionCode,
    };
  }

  return Object.freeze({
    async list(planRef: string): Promise<readonly PlanDependency[]> {
      const response = await webFetch(path(planRef));
      if (!response.ok) throw await failure(response);
      const raw: unknown = await response.json();
      if (!Array.isArray(raw)) throw new Error('Elenco Dependency non valido.');
      const items = raw.map(dependency);
      if (items.some((item) => item.planRef !== planRef)) {
        throw new Error('Dependency esterna al Plan.');
      }
      return Object.freeze(items);
    },
    create(planRef: string, intent: PlanDependencyIntent, operationId: string) {
      return mutate(path(planRef), 'POST', body(intent, operationId));
    },
    revise(
      item: PlanDependency, intent: PlanDependencyIntent,
      active: boolean, operationId: string,
    ) {
      return mutate(
        `${path(item.planRef)}/${encodeURIComponent(item.dependencyRef)}`, 'PUT',
        { ...body(intent, operationId), expected_state_ref: item.stateRef, active },
      );
    },
  });
}
