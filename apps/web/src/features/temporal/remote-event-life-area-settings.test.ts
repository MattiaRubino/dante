import { describe, expect, it, vi } from 'vitest';

import { createRemoteEventLifeAreaSettings } from './remote-event-life-area-settings';

const EVENT = '0199a111-1111-7111-8111-111111111111';
const AREA = '0199a222-2222-7222-8222-222222222222';

function json(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}

describe('Event Life Area owner-scoped edits', () => {
  it('permits explicit null unassignment and preserves revision CAS', async () => {
    const calls: unknown[] = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      const url = String(input);
      if (url === '/api/v1/temporal/life-areas')
        return Promise.resolve(json([{ life_area_ref: AREA, name: 'Lavoro', archived: false }]));
      if (url === '/api/v1/temporal/life-area-assignments')
        return Promise.resolve(json([{
          subject_kind: 'event', subject_native_ref: EVENT,
          life_area_ref: AREA, assignment_revision: 2,
        }]));
      if (url === '/api/v1/auth/session')
        return Promise.resolve(json({ authenticated: true, csrf_token: 'csrf' }));
      if (url === '/api/v1/temporal/life-area-assignments/events/' + EVENT) {
        expect(init?.method).toBe('PUT');
        expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf');
        calls.push(JSON.parse(String(init?.body)) as unknown);
        return Promise.resolve(json({
          subject_kind: 'event', subject_native_ref: EVENT,
          life_area_ref: null, assignment_revision: 3, replayed: false,
        }));
      }
      throw new Error('Unexpected Event request ' + url);
    });
    const source = createRemoteEventLifeAreaSettings(fetchFn);
    const loaded = await source.load(EVENT);
    expect(loaded).toMatchObject({ currentRef: AREA, currentRevision: 2 });
    const saved = await source.assign(EVENT, loaded, null, 'm4:unassign');
    expect(saved).toMatchObject({ currentRef: null, currentRevision: 3 });
    expect(calls).toEqual([{
      operation_id: 'm4:unassign', life_area_ref: null,
      expected_assignment_revision: 2,
    }]);
  });

  it('fails closed on a stale confirmation without claiming saved state', async () => {
    const source = createRemoteEventLifeAreaSettings(
      vi.fn<typeof globalThis.fetch>((input) => {
        const url = String(input);
        if (url === '/api/v1/auth/session')
          return Promise.resolve(json({ authenticated: true, csrf_token: 'csrf' }));
        return Promise.resolve(json({ code: 'life_area_assignment_revision_conflict' }, 409));
      }),
    );
    const current = {
      options: [{ ref: AREA, name: 'Lavoro' }],
      currentRef: null, currentRevision: 2,
    };
    await expect(source.assign(EVENT, current, AREA, 'm4:stale'))
      .rejects.toThrow('cambiata');
  });

  it('rejects incoherent actor assignments during Event Inspector load', async () => {
    const source = createRemoteEventLifeAreaSettings(
      vi.fn<typeof globalThis.fetch>((input) => Promise.resolve(
        String(input).endsWith('/life-areas')
          ? json([])
          : json([
              { subject_kind: 'event', subject_native_ref: EVENT,
                life_area_ref: AREA, assignment_revision: 1 },
              { subject_kind: 'event', subject_native_ref: EVENT,
                life_area_ref: null, assignment_revision: 2 },
            ]),
      )),
    );
    await expect(source.load(EVENT)).rejects.toThrow('incoerenti');
  });
});
