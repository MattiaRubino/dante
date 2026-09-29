import { createWebFetch } from '../../platform/api/web-fetch';
import type { PlanWork } from './remote-plan-work-data-source';

export type ProposedSlice = Readonly<{
  sliceRef: string;
  startsAt: string;
  endsAt: string;
}>;

export type TemporalRuleAssessment = Readonly<{
  constraintRef: string;
  strength: 'hard' | 'soft';
  evaluation: string;
  reasonCode: string;
  constrainedFacet: string;
}>;

export type ExecutionAssessment = Readonly<{
  basis: string;
  proposedCount: number;
  countStatus: string;
  countReason: string;
  sliceAssessments: readonly Readonly<{
    sliceRef: string;
    temporalStatus: string;
    temporalRules: readonly TemporalRuleAssessment[];
  }>[];
  mergeStatus: string;
  mergeReason: string;
  mergedTemporalStatus: string | null;
  mergedTemporalRules: readonly TemporalRuleAssessment[];
}>;

function rules(value: unknown): readonly TemporalRuleAssessment[] {
  if (!Array.isArray(value)) throw new Error('Regole temporali non valide.');
  return value.map((entry: unknown) => {
    if (entry === null || typeof entry !== 'object') {
      throw new Error('Regola temporale non valida.');
    }
    const item = entry as Record<string, unknown>;
    if (typeof item.constraint_ref !== 'string' ||
        (item.strength !== 'hard' && item.strength !== 'soft') ||
        typeof item.evaluation !== 'string' || typeof item.reason_code !== 'string' ||
        typeof item.constrained_facet !== 'string') {
      throw new Error('Regola temporale non valida.');
    }
    return {
      constraintRef: item.constraint_ref, strength: item.strength,
      evaluation: item.evaluation, reasonCode: item.reason_code,
      constrainedFacet: item.constrained_facet,
    };
  });
}

export function createRemotePlanExecutionDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  return Object.freeze({
    async assess(
      plan: PlanWork, stepRef: string, slices: readonly ProposedSlice[],
      mergePair: readonly [string, string] | null,
    ): Promise<ExecutionAssessment> {
      const response = await webFetch(
        `/api/v1/temporal/plans/${encodeURIComponent(plan.planRef)}/steps/` +
        `${encodeURIComponent(stepRef)}/execution/assess`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            expected_state_ref: plan.stateRef,
            slices: slices.map((item) => ({
              slice_ref: item.sliceRef, starts_at: item.startsAt, ends_at: item.endsAt,
            })),
            merge_pair: mergePair,
          }),
        },
      );
      if (!response.ok) {
        const payload: unknown = await response.json().catch(() => null);
        const detail = payload !== null && typeof payload === 'object' && 'detail' in payload
          ? payload.detail : null;
        throw new Error(typeof detail === 'string' ? detail : `Valutazione non riuscita (${response.status}).`);
      }
      const raw: unknown = await response.json();
      if (raw === null || typeof raw !== 'object' || !('slice_assessments' in raw) ||
          !Array.isArray(raw.slice_assessments) || !('count_status' in raw) ||
          typeof raw.count_status !== 'string' || !('merge_status' in raw) ||
          typeof raw.merge_status !== 'string') {
        throw new Error('Valutazione non valida.');
      }
      const row = raw as Record<string, unknown>;
      return {
        basis: String(row.basis), proposedCount: Number(row.proposed_count),
        countStatus: raw.count_status, countReason: String(row.count_reason),
        sliceAssessments: raw.slice_assessments.map((value: unknown) => {
          const item = value as Record<string, unknown>;
          return {
            sliceRef: String(item.slice_ref), temporalStatus: String(item.temporal_status),
            temporalRules: rules(item.temporal_rules),
          };
        }),
        mergeStatus: raw.merge_status, mergeReason: String(row.merge_reason),
        mergedTemporalStatus: typeof row.merged_temporal_status === 'string'
          ? row.merged_temporal_status : null,
        mergedTemporalRules: rules(row.merged_temporal_rules),
      };
    },
  });
}
