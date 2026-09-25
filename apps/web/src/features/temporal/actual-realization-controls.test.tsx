import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActualRealizationControls } from './actual-realization-controls';

const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ab';
const ACTUAL = '01991f2a-1234-7abc-8def-1234567890ac';
const STATE_1 = '01991f2a-1234-7abc-8def-1234567890ad';
const STATE_2 = '01991f2a-1234-7abc-8def-1234567890ae';

type Fetch = typeof globalThis.fetch;

function actual(materialStateRef: string, occurred: boolean) {
  return {
    actual_ref: ACTUAL,
    subject_native_ref: SUBJECT,
    material_state_ref: materialStateRef,
    realization_occurred: occurred,
    timing: null,
    session_bases: [],
    replayed: false,
  };
}

function notFound() {
  return Response.json(
    {
      code: 'temporal.actual.not_found',
      category: 'not_found',
      title: 'Actual unavailable',
      detail: 'No Actual is established for this subject.',
    },
    { status: 404 },
  );
}

describe('Actual realization controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('keeps absence as unknown and records the first realization with no expected state', async () => {
    const bodies: unknown[] = [];
    let current: ReturnType<typeof actual> | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (init?.method === 'POST') {
        const body = JSON.parse(String(init.body));
        bodies.push(body);
        current = actual(STATE_1, true);
        return Response.json(current, { status: 201 });
      }
      return current === null ? notFound() : Response.json(current);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ActualRealizationControls kind="event" subjectRef={SUBJECT} />);
    await screen.findByText('Stato reale: sconosciuto');
    expect(screen.queryByText('Stato reale: non avvenuto')).toBeNull();

    fireEvent.click(screen.getByText('Segna avvenuto'));
    await screen.findByText('Stato reale: avvenuto');

    expect(bodies).toEqual([
      {
        operation_id: expect.any(String),
        expected_material_state_ref: null,
        realization_occurred: true,
        timing: null,
        session_bases: [],
      },
    ]);
  });

  it('uses the current MaterialState as compare-and-set input for a later realization', async () => {
    const bodies: Array<Record<string, unknown>> = [];
    let current = actual(STATE_1, true);
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (init?.method === 'POST') {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        bodies.push(body);
        current = actual(STATE_2, false);
        return Response.json(current, { status: 201 });
      }
      return Response.json(current);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ActualRealizationControls kind="activity" subjectRef={SUBJECT} />);
    await screen.findByText('Stato reale: avvenuto');

    fireEvent.click(screen.getByText('Segna non avvenuto'));
    await screen.findByText('Stato reale: non avvenuto');

    expect(bodies).toHaveLength(1);
    expect(bodies[0]).toMatchObject({
      expected_material_state_ref: STATE_1,
      realization_occurred: false,
    });
  });

  it('reloads authoritative state after a stale-current rejection', async () => {
    let reads = 0;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (init?.method === 'POST') {
        return Response.json(
          {
            code: 'temporal.actual.current_conflict',
            detail: 'Actual realization changed.',
          },
          { status: 409 },
        );
      }
      reads += 1;
      return Response.json(actual(reads === 1 ? STATE_1 : STATE_2, reads === 1));
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ActualRealizationControls kind="occurrence" subjectRef={SUBJECT} />);
    await screen.findByText('Stato reale: avvenuto');

    fireEvent.click(screen.getByText('Segna non avvenuto'));
    await waitFor(() => {
      expect(screen.getByRole('alert').textContent).toContain(
        'Actual realization changed.',
      );
    });
    expect(screen.getByText('Stato reale: non avvenuto')).toBeTruthy();
    expect(reads).toBe(2);
  });
});
