import { describe, expect, it, vi } from 'vitest';

import { createRemotePlanDependencyDataSource } from './remote-plan-dependency-data-source';

const PLAN = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const RULE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const BEFORE = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';
const AFTER = '0199a8c0-5e74-7bc0-8ad0-a2f403f56181';
const ACTIVITY = '0199a8c0-5e74-7bc0-8ad0-a2f403f56182';

const row = {
  dependency_ref: RULE, plan_ref: PLAN,
  prerequisite_step_ref: BEFORE, prerequisite_activity_ref: ACTIVITY,
  dependent_step_ref: AFTER, dependent_activity_ref: ACTIVITY,
  state_ref: STATE, purpose_code: 'dependent_activity_admissibility',
  qualifier_code: 'outcome_code', disposition_code: 'work.completed',
  active: true, recorded_at: '2026-09-28T17:00:00Z',
  evaluation_code: 'unknown', cycle: false, replayed: false,
};

function urlText(value: RequestInfo | URL): string {
  return typeof value === 'string' ? value : value instanceof URL ? value.href : value.url;
}

function bodyText(value: BodyInit | null | undefined): string {
  if (typeof value !== 'string') throw new Error('Expected a JSON request body.');
  return value;
}

describe('remote Plan Dependency', () => {
  it('reads typed truth and sends authenticated create, revision and retirement', async () => {
    const calls: Array<{ url: string; init?: RequestInit }> = [];
    const fetchFn = vi.fn((url: RequestInfo | URL, init?: RequestInit) => {
      calls.push({ url: urlText(url), ...(init === undefined ? {} : { init }) });
      if (urlText(url) === '/api/v1/auth/session') {
        return Promise.resolve(new Response(JSON.stringify({ authenticated: true, csrf_token: 'csrf' })));
      }
      const payload: unknown = init?.body === undefined ? null : JSON.parse(bodyText(init.body));
      const active = typeof payload === 'object' && payload !== null && 'active' in payload
        && typeof payload.active === 'boolean' ? payload.active : true;
      return Promise.resolve(new Response(JSON.stringify(init?.method === undefined ? [row] :
        { ...row, active })));
    }) as typeof globalThis.fetch;
    const source = createRemotePlanDependencyDataSource(fetchFn);
    const [item] = await source.list(PLAN);
    expect(item?.evaluationCode).toBe('unknown');
    expect(item?.dispositionCode).toBe('work.completed');
    const intent = {
      prerequisiteStepRef: BEFORE, dependentStepRef: AFTER,
      qualifierCode: 'outcome_code' as const, dispositionCode: 'work.completed',
    };
    await source.create(PLAN, intent, 'create-op');
    await source.revise(item!, intent, true, 'revise-op');
    await source.revise(item!, intent, false, 'retire-op');
    expect(calls.map((call) => call.url)).toEqual([
      `/api/v1/temporal/plans/${PLAN}/dependencies`,
      '/api/v1/auth/session', `/api/v1/temporal/plans/${PLAN}/dependencies`,
      '/api/v1/auth/session', `/api/v1/temporal/plans/${PLAN}/dependencies/${RULE}`,
      '/api/v1/auth/session', `/api/v1/temporal/plans/${PLAN}/dependencies/${RULE}`,
    ]);
    expect(JSON.parse(bodyText(calls.at(-1)?.init?.body)) as unknown).toMatchObject({
      operation_id: 'retire-op', expected_state_ref: STATE, active: false,
      qualifier_code: 'outcome_code', disposition_code: 'work.completed',
    });
    expect(new Headers(calls.at(-1)?.init?.headers).get('X-Dante-CSRF')).toBe('csrf');
  });

  it('rejects an invented global blocked status in place of evaluation', async () => {
    const fetchFn = vi.fn(() => Promise.resolve(new Response(JSON.stringify([
      { ...row, evaluation_code: null, blocked: true },
    ])))) as typeof globalThis.fetch;
    const [retired] = await createRemotePlanDependencyDataSource(fetchFn).list(PLAN);
    expect(retired?.evaluationCode).toBeNull();
    expect('blocked' in retired!).toBe(false);
  });

  it('rejects a relation from another Plan or with an unknown qualifier', async () => {
    const foreign = vi.fn(() => Promise.resolve(new Response(JSON.stringify([
      { ...row, plan_ref: RULE },
    ])))) as typeof globalThis.fetch;
    await expect(createRemotePlanDependencyDataSource(foreign).list(PLAN)).rejects.toThrow(
      'Dependency esterna al Plan.',
    );
    const invented = vi.fn(() => Promise.resolve(new Response(JSON.stringify([
      { ...row, qualifier_code: 'generic' },
    ])))) as typeof globalThis.fetch;
    await expect(createRemotePlanDependencyDataSource(invented).list(PLAN)).rejects.toThrow(
      'Stato Dependency non valido.',
    );
  });
});
