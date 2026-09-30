import { createWebFetch } from '../../platform/api/web-fetch';

import type { PlanWork } from './remote-plan-work-data-source';

export type PlanCandidates = Readonly<{
  basisFingerprint: string;
  scheduleRef: string | null;
  scheduleStateRef: string | null;
  placementForm: string | null;
  policyStateRef: string | null;
  currentStartsAt: string | null;
  currentEndsAt: string | null;
  basisStatus: 'supported' | 'unknown' | 'blocked' | 'unsupported';
  reasonCode: string;
  solverStatus: 'OPTIMAL' | 'FEASIBLE' | 'INFEASIBLE' | 'MODEL_INVALID' | 'UNKNOWN' | null;
  movementPolicyStatus: 'automatic' | 'blocked' | 'missing';
  capacityEvaluated: false;
  candidates: readonly Readonly<{
    startsAt: string;
    endsAt: string;
    softViolations: number;
  }>[];
}>;

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta delle alternative non valida.');
  }
  return value as Record<string, unknown>;
}

function date(value: unknown): string {
  if (typeof value !== 'string' || !Number.isFinite(Date.parse(value))) {
    throw new Error('Intervallo candidato non valido.');
  }
  return value;
}

function parse(value: unknown, plan: PlanWork, stepRef: string): PlanCandidates {
  const row = record(value);
  const statuses = ['OPTIMAL', 'FEASIBLE', 'INFEASIBLE', 'MODEL_INVALID', 'UNKNOWN'];
  if (
    row.plan_ref !== plan.planRef || row.plan_state_ref !== plan.stateRef ||
    row.step_ref !== stepRef || row.capacity_evaluated !== false ||
    typeof row.basis_fingerprint !== 'string' ||
    !/^[0-9a-f]{64}$/.test(row.basis_fingerprint) ||
    !['supported', 'unknown', 'blocked', 'unsupported'].includes(String(row.basis_status)) ||
    !['automatic', 'blocked', 'missing'].includes(String(row.movement_policy_status)) ||
    (row.solver_status !== null && !statuses.includes(String(row.solver_status))) ||
    typeof row.reason_code !== 'string' || !Array.isArray(row.candidates) ||
    row.candidates.length > 3
  ) {
    throw new Error('Il Plan è cambiato o la risposta delle alternative non è valida.');
  }
  const candidates = row.candidates.map((entry: unknown) => {
    const item = record(entry);
    if (!Array.isArray(item.soft_findings) || item.soft_findings.length > 100) {
      throw new Error('Vincoli del candidato non validi.');
    }
    const startsAt = date(item.starts_at);
    const endsAt = date(item.ends_at);
    if (Date.parse(startsAt) >= Date.parse(endsAt)) {
      throw new Error('Intervallo candidato non valido.');
    }
    return Object.freeze({
      startsAt, endsAt,
      softViolations: item.soft_findings.filter((finding: unknown) =>
        record(finding).evaluation === 'violated',
      ).length,
    });
  });
  const placement = row.placement === null ? null : record(row.placement);
  if (placement !== null && (
    typeof placement.schedule_ref !== 'string' ||
    typeof placement.material_state_ref !== 'string' ||
    typeof placement.temporal_form_code !== 'string'
  )) throw new Error('Base Schedule non valida.');
  return Object.freeze({
    basisFingerprint: row.basis_fingerprint,
    scheduleRef: placement === null ? null : placement.schedule_ref as string,
    scheduleStateRef: placement === null ? null : placement.material_state_ref as string,
    placementForm: placement === null ? null : placement.temporal_form_code as string,
    currentStartsAt: placement === null || placement.starts_at === null
      ? null : date(placement.starts_at),
    currentEndsAt: placement === null || placement.ends_at === null
      ? null : date(placement.ends_at),
    policyStateRef: row.movement_policy_material_state_ref === null
      ? null : String(row.movement_policy_material_state_ref),
    basisStatus: row.basis_status as PlanCandidates['basisStatus'],
    reasonCode: row.reason_code,
    solverStatus: row.solver_status as PlanCandidates['solverStatus'],
    movementPolicyStatus: row.movement_policy_status as PlanCandidates['movementPolicyStatus'],
    capacityEvaluated: false,
    candidates: Object.freeze(candidates),
  });
}

export function createRemotePlanCandidateDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  return Object.freeze({
    async search(plan: PlanWork, stepRef: string): Promise<PlanCandidates> {
      const endpoint =
        `/api/v1/temporal/plans/${encodeURIComponent(plan.planRef)}` +
        `/steps/${encodeURIComponent(stepRef)}/candidates` +
        `?expected_state_ref=${encodeURIComponent(plan.stateRef)}`;
      const response = await webFetch(endpoint, { cache: 'no-store' });
      if (!response.ok) {
        const body: unknown = await response.json().catch(() => null);
        const detail = body !== null && typeof body === 'object' &&
          'detail' in body && typeof body.detail === 'string'
          ? body.detail : `Alternative non disponibili (HTTP ${response.status}).`;
        throw new Error(detail);
      }
      return parse(await response.json(), plan, stepRef);
    },
  });
}
