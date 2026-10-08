import { describe, expect, it, vi } from 'vitest';

import { createRemoteRealityObjectiveDataSource } from './remote-reality-objective-data-source';

const ref = '0199a567-8888-7888-8888-012345678901';

function response(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}

describe('M2 Objective corrections', () => {
  it('loads current version, revises the same Objective and corrects one Observation', async () => {
    const posts: unknown[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const uri = typeof input === 'string' ? input
          : input instanceof URL ? input.href : input.url;
        if (uri.endsWith('/auth/session')) return Promise.resolve(response({
          authenticated: true, csrf_token: 'csrf',
        }));
        if (uri.endsWith('/definition') && init?.method === 'GET') {
          return Promise.resolve(response({
            objective_ref: ref, definition_revision: 2, label: '7 km',
            result_kind: 'quantity', comparator_code: 'gte',
            target_value: 7, target_min: null, target_max: null,
            unit_code: 'km', presentation_order: 0,
            evaluation_state_ref: 'state1',
          }));
        }
        if (uri.endsWith('/definition') && init?.method === 'PUT') {
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('csrf');
          posts.push(JSON.parse(String(init.body)) as unknown);
          return Promise.resolve(response({
            objective_ref: ref, definition_revision: 3,
            evaluation_state_ref: 'state2', assessment_code: 'satisfied',
            replayed: false,
          }));
        }
        if (uri.endsWith('/correction') && init?.method === 'POST') {
          posts.push(JSON.parse(String(init.body)) as unknown);
          return Promise.resolve(response({
            objective_ref: ref, observation_ref: 'observation2',
            evaluation_state_ref: 'state3', assessment_code: 'not_satisfied',
            replayed: false,
          }));
        }
        throw new Error(`Unexpected request ${uri} ${init?.method}`);
      },
    );
    const source = createRemoteRealityObjectiveDataSource(fetchFn);
    const state = await source.getDefinition(ref);
    expect(state.definitionRevision).toBe(2);
    expect(state.targetValue).toBe(7);
    await source.reviseDefinition(ref, {
      operationId: 'definition:3', expectedRevision: state.definitionRevision,
      label: '6 km', resultKind: 'quantity', comparatorCode: 'gte',
      targetValue: 6, targetMin: null, targetMax: null,
      unitCode: 'km', presentationOrder: 0,
    });
    await source.correctResult(ref, {
      operationId: 'result:correct', expectedEvaluationStateRef: 'state2',
      observedBoolean: null, observedNumeric: 5, qualitativeCode: null,
      assessmentCode: null,
    });
    expect(posts).toEqual([
      {
        operation_id: 'definition:3', expected_revision: 2,
        label: '6 km', result_kind: 'quantity', comparator_code: 'gte',
        target_value: 6, target_min: null, target_max: null,
        unit_code: 'km', presentation_order: 0,
      },
      {
        operation_id: 'result:correct', expected_evaluation_state_ref: 'state2',
        observed_boolean: null, observed_numeric: 5,
        qualitative_code: null, assessment_code: null,
      },
    ]);
  });

  it('does not convert a correction conflict into a false success', async () => {
    const fetchFn = vi.fn(
      (input: RequestInfo | URL): Promise<Response> => {
        const uri = typeof input === 'string' ? input
          : input instanceof URL ? input.href : input.url;
        if (uri.endsWith('/auth/session')) return Promise.resolve(response({
          authenticated: true, csrf_token: 'csrf',
        }));
        return Promise.resolve(response({ detail: 'Current state changed' }, 409));
      },
    );
    const source = createRemoteRealityObjectiveDataSource(fetchFn);
    await expect(source.correctResult(ref, {
      operationId: 'result:conflict', expectedEvaluationStateRef: 'old',
      observedBoolean: true, observedNumeric: null,
      qualitativeCode: null, assessmentCode: null,
    })).rejects.toThrow('Current state changed');
  });
});
