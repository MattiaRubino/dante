import { createWebFetch } from '../../platform/api/web-fetch';

import type { PlanWork } from './remote-plan-work-data-source';

export type DiagnosticCode =
  | 'unlinked_step'
  | 'unknown_basis'
  | 'multiple_current_placements'
  | 'unsupported_placement'
  | 'known_hard_violation'
  | 'dependency_cycle'
  | 'blocked_prerequisite'
  | 'no_known_conflict_in_supported_rules';

export type PlanDiagnosis = Readonly<{
  planRef: string;
  planStateRef: string;
  title: string;
  capacityEvaluated: boolean;
  steps: readonly Readonly<{
    stepRef: string;
    title: string;
    activityRef: string | null;
    diagnostics: readonly DiagnosticCode[];
    constraintStatus: string | null;
    hardSetStatus: string | null;
    placements: readonly Readonly<{
      scheduleRef: string;
      materialStateRef: string;
      temporalFormCode: string;
      startsAt: string | null;
      endsAt: string | null;
    }>[];
    constraints: readonly Readonly<{
      constraintRef: string;
      materialStateRef: string;
      strength: 'hard' | 'soft';
      evaluation: 'satisfied' | 'violated' | 'not_evaluable';
      reasonCode: string;
    }>[];
    dependencies: readonly Readonly<{
      dependencyRef: string;
      stateRef: string;
      prerequisiteStepRef: string;
      qualifierCode: 'actual_occurred' | 'outcome_code';
      evaluationCode: 'satisfied' | 'unsatisfied' | 'unknown' | null;
      actualMaterialStateRef: string | null;
      outcomeMaterialStateRef: string | null;
      cycle: boolean;
    }>[];
  }>[];
}>;

const UUID =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CODES: readonly string[] = [
  'unlinked_step',
  'unknown_basis',
  'multiple_current_placements',
  'unsupported_placement',
  'known_hard_violation',
  'dependency_cycle',
  'blocked_prerequisite',
  'no_known_conflict_in_supported_rules',
];

function object(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Diagnosi del Plan non valida.');
  }
  return value as Record<string, unknown>;
}

function ref(value: unknown): string {
  if (typeof value !== 'string' || !UUID.test(value)) {
    throw new Error('Riferimento della diagnosi non valido.');
  }
  return value.toLowerCase();
}

function optionalRef(value: unknown): string | null {
  return value === null ? null : ref(value);
}

function date(value: unknown): string | null {
  if (value === null) return null;
  if (typeof value !== 'string' || !Number.isFinite(Date.parse(value))) {
    throw new Error('Data della diagnosi non valida.');
  }
  return value;
}

function optionalCode(value: unknown): string | null {
  if (value === null) return null;
  if (typeof value !== 'string' || !/^[a-z_]+$/.test(value)) {
    throw new Error('Stato della diagnosi non valido.');
  }
  return value;
}

function list(value: unknown, maximum: number): unknown[] {
  if (!Array.isArray(value) || value.length > maximum) {
    throw new Error('Diagnosi del Plan fuori limite.');
  }
  return value;
}

function parse(value: unknown): PlanDiagnosis {
  const row = object(value);
  if (
    typeof row.title !== 'string' ||
    !row.title.trim() ||
    row.capacity_evaluated !== false
  ) {
    throw new Error('Diagnosi del Plan non valida.');
  }
  const steps = list(row.steps, 20).map((candidate) => {
    const step = object(candidate);
    if (typeof step.title !== 'string' || !step.title.trim()) {
      throw new Error('Step della diagnosi non valido.');
    }
    const diagnostics = list(step.diagnostics, 8).map((code) => {
      if (typeof code !== 'string' || !CODES.includes(code)) {
        throw new Error('Motivo della diagnosi non valido.');
      }
      return code as DiagnosticCode;
    });
    const placements = list(step.placements, 20).map((candidatePlacement) => {
      const placement = object(candidatePlacement);
      if (typeof placement.temporal_form_code !== 'string') {
        throw new Error('Schedule della diagnosi non valido.');
      }
      return Object.freeze({
        scheduleRef: ref(placement.schedule_ref),
        materialStateRef: ref(placement.material_state_ref),
        temporalFormCode: placement.temporal_form_code,
        startsAt: date(placement.starts_at),
        endsAt: date(placement.ends_at),
      });
    });
    const constraints = list(step.constraints, 100).map((candidateRule) => {
      const rule = object(candidateRule);
      if (
        (rule.strength !== 'hard' && rule.strength !== 'soft') ||
        (rule.evaluation !== 'satisfied' &&
          rule.evaluation !== 'violated' &&
          rule.evaluation !== 'not_evaluable') ||
        typeof rule.reason_code !== 'string'
      ) {
        throw new Error('Vincolo della diagnosi non valido.');
      }
      return Object.freeze({
        constraintRef: ref(rule.constraint_ref),
        materialStateRef: ref(rule.material_state_ref),
        strength: rule.strength,
        evaluation: rule.evaluation,
        reasonCode: rule.reason_code,
      });
    });
    const dependencies = list(step.dependencies, 40).map(
      (candidateDependency) => {
        const dependency = object(candidateDependency);
        if (
          (dependency.qualifier_code !== 'actual_occurred' &&
            dependency.qualifier_code !== 'outcome_code') ||
          (dependency.evaluation_code !== null &&
            dependency.evaluation_code !== 'satisfied' &&
            dependency.evaluation_code !== 'unsatisfied' &&
            dependency.evaluation_code !== 'unknown') ||
          typeof dependency.cycle !== 'boolean'
        ) {
          throw new Error('Dependency della diagnosi non valida.');
        }
        return Object.freeze({
          dependencyRef: ref(dependency.dependency_ref),
          stateRef: ref(dependency.state_ref),
          prerequisiteStepRef: ref(dependency.prerequisite_step_ref),
          qualifierCode: dependency.qualifier_code,
          evaluationCode: dependency.evaluation_code,
          actualMaterialStateRef: optionalRef(
            dependency.actual_material_state_ref,
          ),
          outcomeMaterialStateRef: optionalRef(
            dependency.outcome_material_state_ref,
          ),
          cycle: dependency.cycle,
        });
      },
    );
    return Object.freeze({
      stepRef: ref(step.step_ref),
      title: step.title,
      activityRef: optionalRef(step.activity_ref),
      constraintStatus: optionalCode(step.constraint_status),
      hardSetStatus: optionalCode(step.hard_set_status),
      diagnostics: Object.freeze(diagnostics),
      placements: Object.freeze(placements),
      constraints: Object.freeze(constraints),
      dependencies: Object.freeze(dependencies),
    });
  });
  return Object.freeze({
    planRef: ref(row.plan_ref),
    planStateRef: ref(row.plan_state_ref),
    title: row.title,
    capacityEvaluated: false,
    steps: Object.freeze(steps),
  });
}

export function createRemotePlanConflictDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  return Object.freeze({
    async diagnose(plan: PlanWork): Promise<PlanDiagnosis> {
      const endpoint =
        `/api/v1/temporal/plans/${encodeURIComponent(plan.planRef)}` +
        `/conflicts?expected_state_ref=${encodeURIComponent(plan.stateRef)}`;
      const response = await webFetch(endpoint, { cache: 'no-store' });
      if (!response.ok) {
        const body: unknown = await response.json().catch(() => null);
        const detail =
          body !== null &&
          typeof body === 'object' &&
          'detail' in body &&
          typeof body.detail === 'string'
            ? body.detail
            : `Diagnosi non disponibile (HTTP ${response.status}).`;
        throw new Error(detail);
      }
      const result = parse(await response.json());
      if (
        result.planRef !== plan.planRef ||
        result.planStateRef !== plan.stateRef
      ) {
        throw new Error('Il Plan è cambiato. Ricaricalo e riprova.');
      }
      return result;
    },
  });
}
