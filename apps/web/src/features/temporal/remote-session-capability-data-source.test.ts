import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalSessionCapabilityDataSource } from './remote-session-capability-data-source';

const ACTIVITY_REF = '0199a111-1111-7111-8111-111111111111';

function response(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('remote Session capability read', () => {
  it('enables card runtime only from an active session.active_duration constraint', async () => {
    const fetchFn = vi.fn<typeof fetch>().mockResolvedValue(
      response({
        items: [
          {
            constraint_ref: '0199a222-2222-7222-8222-222222222222',
            subject_ref: ACTIVITY_REF,
            subject_kind: 'activity',
            status: 'active',
            current_rule: {
              family: 'duration',
              duration_kind: 'minimum',
              constrained_facet: 'session.active_duration',
              strength: 'soft',
              duration_microseconds: 1_800_000_000,
              material_state_ref: '0199a333-3333-7333-8333-333333333333',
            },
          },
        ],
      }),
    );
    const source = createRemoteTemporalSessionCapabilityDataSource(fetchFn);

    await expect(source.activityEnabled(ACTIVITY_REF)).resolves.toBe(true);
    expect(String(fetchFn.mock.calls[0]?.[0])).toBe(
      `/api/v1/temporal/constraints?subject_ref=${ACTIVITY_REF}`,
    );
  });

  it('keeps cards disabled for unrelated or retired duration rules', async () => {
    const fetchFn = vi.fn<typeof fetch>().mockResolvedValue(
      response({
        items: [
          {
            subject_kind: 'activity',
            status: 'active',
            current_rule: {
              family: 'duration',
              constrained_facet: 'schedule.placement',
            },
          },
          {
            subject_kind: 'activity',
            status: 'retired',
            current_rule: {
              family: 'duration',
              constrained_facet: 'session.active_duration',
            },
          },
        ],
      }),
    );
    const source = createRemoteTemporalSessionCapabilityDataSource(fetchFn);

    await expect(source.activityEnabled(ACTIVITY_REF)).resolves.toBe(false);
  });
});
