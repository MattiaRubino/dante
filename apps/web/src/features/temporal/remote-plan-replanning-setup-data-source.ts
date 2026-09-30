import { createWebFetch } from '../../platform/api/web-fetch';
import { invalidateTemporalPlanningRead } from './timeline-invalidation';

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta di configurazione non valida.');
  }
  return value as Record<string, unknown>;
}

export function createRemotePlanReplanningSetupDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    if (!response.ok) throw new Error('Sessione non disponibile.');
    const row = record(await response.json());
    if (row.authenticated !== true || typeof row.csrf_token !== 'string') {
      throw new Error('Accedi per configurare lo spostamento.');
    }
    return row.csrf_token;
  }
  async function write(endpoint: string, method: 'PUT' | 'POST', body: object) {
    const response = await webFetch(endpoint, {
      method, cache: 'no-store',
      headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const payload: unknown = await response.json().catch(() => null);
      const detail = payload !== null && typeof payload === 'object' &&
        'detail' in payload && typeof payload.detail === 'string'
        ? payload.detail : `Configurazione non disponibile (HTTP ${response.status}).`;
      throw new Error(detail);
    }
    invalidateTemporalPlanningRead();
    return record(await response.json());
  }
  return Object.freeze({
    async requireConfirmation(scheduleRef: string, expectedPolicyStateRef: string | null) {
      const row = await write(
        `/api/v1/temporal/schedules/${encodeURIComponent(scheduleRef)}/movement-policy`,
        'PUT', {
          operation_id: crypto.randomUUID(),
          expected_material_state_ref: expectedPolicyStateRef,
          automatic_movement: 'automatic',
          acceptance_path: 'confirmation_required',
        },
      );
      if (row.schedule_ref !== scheduleRef || typeof row.material_state_ref !== 'string') {
        throw new Error('Movement Policy salvata con una base inattesa.');
      }
    },
    async setEarliestStart(activityRef: string, startsAt: string) {
      const row = await write('/api/v1/temporal/constraints', 'POST', {
        operation_id: crypto.randomUUID(), subject_ref: activityRef,
        rule: {
          family: 'boundary', boundary_kind: 'earliest_start',
          constrained_facet: 'schedule.start', strength: 'hard',
          temporal_form: 'absolute', boundary_at: startsAt,
        },
      });
      if (row.subject_ref !== activityRef || typeof row.constraint_ref !== 'string') {
        throw new Error('Vincolo salvato con un’Attività inattesa.');
      }
    },
  });
}
