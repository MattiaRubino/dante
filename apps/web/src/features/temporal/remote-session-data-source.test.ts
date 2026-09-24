import { describe, expect, it, vi } from 'vitest';

import {
  createRemoteTemporalSessionDataSource,
  TemporalSessionRemoteError,
} from './remote-session-data-source';

const SESSION = '01991f2a-1234-7abc-8def-1234567890ab';
const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ac';
const STATE = '01991f2a-1234-7abc-8def-1234567890ad';

const openSession = {
  session_ref: SESSION,
  subject_native_ref: SUBJECT,
  timing_material_state_ref: STATE,
  started_at: '2026-09-24T07:00:00Z',
  ended_at: null,
  open: true,
  replayed: false,
  paused: false,
  evaluated_at: '2026-09-24T07:30:00Z',
  elapsed_seconds: 1800,
  paused_seconds: 300,
  active_seconds: 1500,
  duration_evaluations: [],
} as const;

const minimumEvaluation = {
  constraint_ref: '01991f2a-1234-7abc-8def-1234567890ae',
  material_state_ref: '01991f2a-1234-7abc-8def-1234567890af',
  minimum_duration_microseconds: 2_700_000_000,
  strength: 'soft',
  evaluation: 'pending',
} as const;

describe('remote session data source', () => {
  it('starts an Activity Session through the canonical endpoint', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      expect(url).toBe(`/api/v1/temporal/activities/${SUBJECT}/sessions`);
      expect(init?.method).toBe('POST');
      expect((init?.headers as Headers).get('X-Dante-CSRF')).toBe('csrf');
      expect(JSON.parse(String(init?.body))).toEqual({ operation_id: 'op-1' });
      return Response.json(openSession);
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const started = await source.start('activity', SUBJECT, 'op-1');
    expect(started.open).toBe(true);
    expect(started.sessionRef).toBe(SESSION);
    expect(started.elapsedSeconds).toBe(1800);
    expect(started.pausedSeconds).toBe(300);
    expect(started.activeSeconds).toBe(1500);
  });

  it('starts an Occurrence Session through the occurrence endpoint', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      expect(url).toBe(`/api/v1/temporal/occurrences/${SUBJECT}/sessions`);
      expect(init?.method).toBe('POST');
      return Response.json(openSession);
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const started = await source.start('occurrence', SUBJECT, 'op-occurrence');
    expect(started.subjectNativeRef).toBe(SUBJECT);
    expect(started.open).toBe(true);
  });

  it('lists authoritative Sessions without acquiring a CSRF token', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      expect(String(input)).toBe(`/api/v1/temporal/activities/${SUBJECT}/sessions`);
      expect(init?.method).toBe('GET');
      return Response.json([openSession]);
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const listed = await source.list('activity', SUBJECT);
    expect(listed).toHaveLength(1);
    expect(listed[0]?.sessionRef).toBe(SESSION);
    expect(listed[0]?.evaluatedAt).toBe('2026-09-24T07:30:00Z');
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('parses canonical Session duration evaluations', async () => {
    const fetchFn = vi.fn<typeof fetch>(async () =>
      Response.json({ ...openSession, duration_evaluations: [minimumEvaluation] }),
    );
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const listed = await source.list('activity', SUBJECT);
    expect(listed[0]?.durationEvaluations).toEqual([
      {
        constraintRef: minimumEvaluation.constraint_ref,
        materialStateRef: minimumEvaluation.material_state_ref,
        minimumDurationMicroseconds: minimumEvaluation.minimum_duration_microseconds,
        strength: 'soft',
        evaluation: 'pending',
      },
    ]);
  });

  it('ends a Session with the expected timing MaterialStateRef', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      expect(url).toBe(`/api/v1/temporal/sessions/${SESSION}/end`);
      expect(init?.method).toBe('POST');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'op-end',
        expected_material_state_ref: STATE,
      });
      return Response.json({
        ...openSession,
        ended_at: '2026-09-24T08:00:00Z',
        evaluated_at: '2026-09-24T08:00:00Z',
        elapsed_seconds: 3600,
        paused_seconds: 300,
        active_seconds: 3300,
        open: false,
      });
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const ended = await source.end(SESSION, STATE, 'op-end');
    expect(ended.open).toBe(false);
    expect(ended.endedAt).toBe('2026-09-24T08:00:00Z');
    expect(ended.activeSeconds).toBe(3300);
  });

  it('pauses and resumes with the authoritative MaterialStateRef', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      expect(init?.method).toBe('POST');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'op-transition',
        expected_material_state_ref: STATE,
      });
      if (url.endsWith('/pause')) {
        return Response.json({ ...openSession, paused: true });
      }
      expect(url).toBe('/api/v1/temporal/sessions/' + SESSION + '/resume');
      return Response.json(openSession);
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    const paused = await source.pause(SESSION, STATE, 'op-transition');
    expect(paused.paused).toBe(true);
    expect(paused.elapsedSeconds).toBe(paused.activeSeconds + paused.pausedSeconds);
    expect((await source.resume(SESSION, STATE, 'op-transition')).paused).toBe(false);
  });

  it('rejects malformed duration totals at the transport boundary', async () => {
    const fetchFn = vi.fn<typeof fetch>(async () =>
      Response.json({ ...openSession, paused_seconds: 1900 }),
    );
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    await expect(source.list('activity', SUBJECT)).rejects.toMatchObject({
      kind: 'protocol',
    });
  });

  it('preserves the canonical HTTP problem code for conflicts', async () => {
    const fetchFn = vi.fn<typeof fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      return Response.json(
        {
          code: 'temporal.session.end_conflict',
          detail: 'Session end conflicts with current timing.',
        },
        { status: 409 },
      );
    });
    const source = createRemoteTemporalSessionDataSource(fetchFn);
    try {
      await source.end(SESSION, STATE, 'op-end');
      throw new Error('expected conflict');
    } catch (error) {
      expect(error).toBeInstanceOf(TemporalSessionRemoteError);
      const remote = error as TemporalSessionRemoteError;
      expect(remote.kind).toBe('http');
      expect(remote.status).toBe(409);
      expect(remote.code).toBe('temporal.session.end_conflict');
    }
  });
});
