import { describe, expect, it, vi } from 'vitest';

import { createRemoteEventRecurrenceGuard } from './remote-event-recurrence-guard';

const EVENT = '0199a111-1111-7111-8111-111111111111';

function response(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('Event duplicate recurrence ownership guard', () => {
  it('allows a one-off Event only after owner API confirms no recurrence', async () => {
    const fetchFn = vi.fn<typeof fetch>(() => Promise.resolve(response(null)));
    await expect(createRemoteEventRecurrenceGuard(fetchFn)
      .isRecurring(EVENT)).resolves.toBe(false);
    expect(fetchFn).toHaveBeenCalledWith(
      `/api/v1/temporal/events/${EVENT}/recurrence`,
      expect.anything(),
    );
  });

  it('recognizes an existing recurring Event source', async () => {
    const fetchFn = vi.fn<typeof fetch>(() =>
      Promise.resolve(response({ owner_kind: 'event', material_state_ref: EVENT })));
    await expect(createRemoteEventRecurrenceGuard(fetchFn)
      .isRecurring(EVENT)).resolves.toBe(true);
  });

  it('fails closed if the recurrence authority cannot be read', async () => {
    const fetchFn = vi.fn<typeof fetch>(() =>
      Promise.resolve(response({ code: 'unavailable' }, 503)));
    await expect(createRemoteEventRecurrenceGuard(fetchFn)
      .isRecurring(EVENT)).rejects.toThrow('duplicazione bloccata');
  });
});
