import { describe, expect, it, vi } from 'vitest';

import { createRemoteActivityInspector } from './remote-activity-inspector';
import { subscribeTemporalTimelineInvalidation } from './timeline-invalidation';

const ref = '0199a111-1111-7111-8111-111111111111';
const profile = {
  activity_ref: ref, title: 'Prima', description: null,
  location: null, color_code: '#EA5C12', revision: 0,
};

function json(value: unknown, status = 200) {
  return new Response(JSON.stringify(value), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}

describe('remote Activity Inspector', () => {
  it('uses the authenticated session, CAS and Timeline invalidation for an edit', async () => {
    const invalidated = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidated);
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      expect(init?.credentials).toBe('same-origin');
      const headers = new Headers(init?.headers);
      expect(headers.get('X-Dante-Client')).toBe('web');
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(json({ authenticated: true, csrf_token: 'token' }));
      }
      expect(input).toBe(`/api/v1/temporal/activities/${ref}/profile`);
      if (init?.method === 'PUT') {
        expect(headers.get('X-Dante-CSRF')).toBe('token');
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        expect(body).toMatchObject({ expected_revision: 0, title: 'Dopo' });
        expect(typeof body.operation_id).toBe('string');
        return Promise.resolve(json({ ...profile, title: 'Dopo', revision: 1 }));
      }
      return Promise.resolve(json(profile));
    });
    try {
      const source = createRemoteActivityInspector(fetchFn);
      const current = await source.get(ref);
      const saved = await source.revise(current, {
        title: 'Dopo', description: null, location: null, colorCode: current.colorCode,
      });
      expect(saved.revision).toBe(1);
      expect(invalidated).toHaveBeenCalledOnce();
    } finally {
      unsubscribe();
    }
  });

  it('keeps recorded history intact and explains the retirement veto', async () => {
    const invalidated = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidated);
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => Promise.resolve(
      input === '/api/v1/auth/session'
        ? json({ authenticated: true, csrf_token: 'token' })
        : json({ code: 'temporal.activity_profile.recorded_truth' }, 409),
    ));
    try {
      await expect(createRemoteActivityInspector(fetchFn).retire(ref))
        .rejects.toThrow('sessioni o risultati registrati');
      expect(invalidated).not.toHaveBeenCalled();
    } finally {
      unsubscribe();
    }
  });

  it('does not invalidate the Timeline when deletion is rejected', async () => {
    const invalidated = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidated);
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => Promise.resolve(
      input === '/api/v1/auth/session'
        ? json({ authenticated: true, csrf_token: 'token' })
        : json({ code: 'temporal.activity_profile.active_session' }, 409),
    ));
    try {
      await expect(createRemoteActivityInspector(fetchFn).retire(ref))
        .rejects.toThrow('Termina prima la sessione attiva');
      expect(invalidated).not.toHaveBeenCalled();
    } finally {
      unsubscribe();
    }
  });
});
