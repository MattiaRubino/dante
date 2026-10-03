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
  it('enables live controls from the accepted Activity execution policy', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockResolvedValue(
        response({
          activity_ref: ACTIVITY_REF,
          state_ref: '0199a222-2222-7222-8222-222222222222',
          mode_code: 'live',
        }),
      );
    const source = createRemoteTemporalSessionCapabilityDataSource(fetchFn);

    await expect(source.activityEnabled(ACTIVITY_REF)).resolves.toBe(true);
    expect(String(fetchFn.mock.calls[0]?.[0])).toBe(
      `/api/v1/temporal/activities/${ACTIVITY_REF}/execution-policy`,
    );
  });

  it('keeps live controls hidden for the explicit record-only policy', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockImplementation(async () =>
        response({
          activity_ref: ACTIVITY_REF,
          state_ref: null,
          mode_code: 'record',
        }),
      );
    const source = createRemoteTemporalSessionCapabilityDataSource(fetchFn);

    await expect(source.activityEnabled(ACTIVITY_REF)).resolves.toBe(false);
    await expect(source.activityMode?.(ACTIVITY_REF)).resolves.toBe('record');
  });
});
