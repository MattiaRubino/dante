import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalSessionDataSource } from './remote-session-data-source';

const SESSION = '01991f2a-1234-7abc-8def-1234567890ab';
const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ac';
const STATE = '01991f2a-1234-7abc-8def-1234567890ad';

describe('remote session data source', () => {
  it('starts an Activity Session through the canonical endpoint', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      expect(url).toBe(`/api/v1/temporal/activities/${SUBJECT}/sessions`);
      expect(init?.method).toBe('POST');
      return Response.json({
        session_ref: SESSION,
        subject_native_ref: SUBJECT,
        timing_material_state_ref: STATE,
        started_at: '2026-09-24T07:00:00Z',
        ended_at: null,
        open: true,
        replayed: false,
      });
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const started = await source.start('activity', SUBJECT, 'op-1');
    expect(started.open).toBe(true);
    expect(started.sessionRef).toBe(SESSION);
  });
});
