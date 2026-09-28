import { describe, expect, it, vi } from 'vitest';

import { createRemotePlanWorkDataSource, newPlanStepRef } from './remote-plan-work-data-source';

const PLAN = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const STEP = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';

const item = {
  plan_ref: PLAN,
  state_ref: STATE,
  title: 'Album',
  created_at: '2026-09-28T12:00:00Z',
  steps: [{ step_ref: STEP, position: 0, title: 'Record', activity_ref: null }],
  replayed: false,
};

describe('remote Plan work structure', () => {
  it('reads accepted order and uses the authenticated mutation boundary', async () => {
    const calls: Array<{ url: string; init?: RequestInit }> = [];
    const fetchFn = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      calls.push({ url: String(url), ...(init === undefined ? {} : { init }) });
      if (String(url) === '/api/v1/auth/session') {
        return new Response(JSON.stringify({ authenticated: true, csrf_token: 'csrf' }));
      }
      if (init?.method === 'PUT') return new Response(JSON.stringify(item));
      if (init?.method === 'POST') return new Response(JSON.stringify({ ...item, steps: [] }));
      return new Response(JSON.stringify([item]));
    }) as typeof globalThis.fetch;
    const source = createRemotePlanWorkDataSource(fetchFn);
    const [loaded] = await source.list();
    expect(loaded?.steps[0]?.stepRef).toBe(STEP);
    await source.create(' Album ', 'create-op');
    await source.replace(loaded!, 'Album', loaded!.steps, 'replace-op');
    expect(calls.map((call) => call.url)).toEqual([
      '/api/v1/temporal/plans',
      '/api/v1/auth/session', '/api/v1/temporal/plans',
      '/api/v1/auth/session', `/api/v1/temporal/plans/${PLAN}`,
    ]);
    const last = calls.at(-1)!;
    expect(last.init?.method).toBe('PUT');
    expect(new Headers(last.init?.headers).get('X-Dante-CSRF')).toBe('csrf');
    expect(JSON.parse(String(last.init?.body))).toMatchObject({
      operation_id: 'replace-op',
      expected_state_ref: STATE,
      steps: [{ step_ref: STEP, title: 'Record', activity_ref: null }],
    });
  });

  it('issues UUIDv7 references for internal Steps', () => {
    expect(newPlanStepRef()).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/,
    );
  });

  it('rejects a response whose order is not contiguous', async () => {
    const fetchFn = vi.fn(async () => new Response(JSON.stringify([
      { ...item, steps: [{ ...item.steps[0], position: 2 }] },
    ]))) as typeof globalThis.fetch;
    await expect(createRemotePlanWorkDataSource(fetchFn).list()).rejects.toThrow(
      'Ordine del Plan non valido.',
    );
  });
});
