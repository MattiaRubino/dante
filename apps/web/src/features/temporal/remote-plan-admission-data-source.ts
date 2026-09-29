import { createWebFetch } from '../../platform/api/web-fetch';
import { invalidateTemporalPlanningRead, invalidateTemporalTimelineRead } from './timeline-invalidation';

import type { PlanWork } from './remote-plan-work-data-source';
import type { PlanCandidates } from './remote-plan-candidate-data-source';

export type ReviewedAlternative = Readonly<{
  startsAt: string;
  endsAt: string;
  operationId: string;
}>;
export type Admission = Readonly<{
  kind: 'committed' | 'pending_confirmation';
  proposalRef: string | null;
  replayed: boolean;
}>;

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta dello spostamento non valida.');
  }
  return value as Record<string, unknown>;
}

function parse(value: unknown): Admission {
  const row = record(value);
  if ((row.kind !== 'committed' && row.kind !== 'pending_confirmation') ||
      typeof row.replayed !== 'boolean' ||
      (row.proposal_ref !== null && typeof row.proposal_ref !== 'string') ||
      (row.kind === 'pending_confirmation' && row.proposal_ref === null)) {
    throw new Error('Esito dello spostamento non valido.');
  }
  if (row.kind === 'committed') {
    invalidateTemporalPlanningRead();
    invalidateTemporalTimelineRead();
  }
  return Object.freeze({
    kind: row.kind, proposalRef: row.proposal_ref as string | null,
    replayed: row.replayed,
  });
}

export function createRemotePlanAdmissionDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    if (!response.ok) throw new Error('Sessione non disponibile.');
    const row = record(await response.json());
    if (row.authenticated !== true || typeof row.csrf_token !== 'string') {
      throw new Error('Accedi prima di spostare un’Attività.');
    }
    return row.csrf_token;
  }
  async function submit(endpoint: string, body: object): Promise<Admission> {
    const response = await webFetch(endpoint, {
      method: 'POST', cache: 'no-store',
      headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const payload: unknown = await response.json().catch(() => null);
      const detail = payload !== null && typeof payload === 'object' &&
        'detail' in payload && typeof payload.detail === 'string'
        ? payload.detail : `Spostamento non disponibile (HTTP ${response.status}).`;
      throw new Error(detail);
    }
    return parse(await response.json());
  }
  return Object.freeze({
    request(plan: PlanWork, stepRef: string, result: PlanCandidates,
      selected: ReviewedAlternative): Promise<Admission> {
      const endpoint = `/api/v1/temporal/plans/${encodeURIComponent(plan.planRef)}` +
        `/steps/${encodeURIComponent(stepRef)}/candidate-moves`;
      return submit(endpoint, {
        operation_id: selected.operationId,
        expected_plan_state_ref: plan.stateRef,
        expected_schedule_ref: result.scheduleRef,
        expected_schedule_state_ref: result.scheduleStateRef,
        expected_policy_state_ref: result.policyStateRef,
        basis_fingerprint: result.basisFingerprint,
        starts_at: selected.startsAt, ends_at: selected.endsAt,
      });
    },
    confirm(plan: PlanWork, stepRef: string, result: PlanCandidates,
      selected: ReviewedAlternative, proposalRef: string): Promise<Admission> {
      const endpoint = `/api/v1/temporal/plans/${encodeURIComponent(plan.planRef)}` +
        `/steps/${encodeURIComponent(stepRef)}/candidate-moves/` +
        `${encodeURIComponent(proposalRef)}/confirm`;
      return submit(endpoint, {
        operation_id: selected.operationId,
        expected_plan_state_ref: plan.stateRef,
        expected_schedule_ref: result.scheduleRef,
        expected_schedule_state_ref: result.scheduleStateRef,
        expected_policy_state_ref: result.policyStateRef,
        basis_fingerprint: result.basisFingerprint,
        starts_at: selected.startsAt, ends_at: selected.endsAt,
      });
    },
  });
}
