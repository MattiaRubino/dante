import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { OutcomeControls } from './outcome-controls';

const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ab';
const ACTUAL = '01991f2a-1234-7abc-8def-1234567890ac';
const ACTUAL_STATE = '01991f2a-1234-7abc-8def-1234567890ad';
const OUTCOME = '01991f2a-1234-7abc-8def-1234567890ae';
const OUTCOME_STATE_1 = '01991f2a-1234-7abc-8def-1234567890af';
const OUTCOME_STATE_2 = '01991f2a-1234-7abc-8def-1234567890b0';

type Fetch = typeof globalThis.fetch;

function actual() {
  return {
    actual_ref: ACTUAL,
    subject_native_ref: SUBJECT,
    material_state_ref: ACTUAL_STATE,
    realization_occurred: true,
    timing: null,
    session_bases: [],
    replayed: false,
  };
}

function outcome(materialStateRef: string, resultCode: string) {
  return {
    outcome_ref: OUTCOME,
    actual_ref: ACTUAL,
    vocabulary_code: 'meeting.decision',
    material_state_ref: materialStateRef,
    result_code: resultCode,
    note: null,
    replayed: false,
  };
}

function actualNotFound() {
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

function outcomeNotFound() {
  return Response.json(
    {
      code: 'temporal.outcome.not_found',
      category: 'not_found',
      title: 'Outcome unavailable',
      detail: 'No Outcome is established for this Actual and vocabulary.',
    },
    { status: 404 },
  );
}

describe('Outcome controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('does not manufacture an Outcome when no Actual exists', async () => {
    const fetchFn = vi.fn<Fetch>(async () => actualNotFound());
    vi.stubGlobal('fetch', fetchFn);

    render(<OutcomeControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.change(screen.getByLabelText('Vocabolario Outcome'), {
      target: { value: 'meeting.decision' },
    });
    fireEvent.click(screen.getByText('Carica Outcome'));

    await screen.findByText('Esito non disponibile: registra prima lo stato reale.');
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('keeps absence unknown then records and corrects one contextual Outcome', async () => {
    const bodies: Array<Record<string, unknown>> = [];
    let current: ReturnType<typeof outcome> | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${SUBJECT}/actual`)) {
        return Response.json(actual());
      }
      if (init?.method === 'POST' && url.endsWith(`/actuals/${ACTUAL}/outcomes`)) {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        bodies.push(body);
        current = outcome(
          bodies.length === 1 ? OUTCOME_STATE_1 : OUTCOME_STATE_2,
          String(body.result_code),
        );
        return Response.json(current, { status: 201 });
      }
      if (url.includes(`/actuals/${ACTUAL}/outcomes/meeting.decision`)) {
        return current === null ? outcomeNotFound() : Response.json(current);
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<OutcomeControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.change(screen.getByLabelText('Vocabolario Outcome'), {
      target: { value: 'meeting.decision' },
    });
    fireEvent.click(screen.getByText('Carica Outcome'));

    await screen.findByText('Outcome: non registrato');
    expect(screen.queryByText('Outcome: decision.deferred')).toBeNull();

    fireEvent.change(screen.getByLabelText('Risultato Outcome'), {
      target: { value: 'decision.deferred' },
    });
    fireEvent.click(screen.getByText('Registra Outcome'));
    await screen.findByText('Outcome registrato.');
    expect(screen.getByText('Outcome: decision.deferred')).toBeTruthy();

    expect(bodies[0]).toMatchObject({
      vocabulary_code: 'meeting.decision',
      expected_material_state_ref: null,
      result_code: 'decision.deferred',
      note: null,
    });

    fireEvent.change(screen.getByLabelText('Risultato Outcome'), {
      target: { value: 'decision.reached' },
    });
    fireEvent.click(screen.getByText('Correggi Outcome'));
    await waitFor(() => expect(bodies).toHaveLength(2));

    expect(bodies[1]).toMatchObject({
      vocabulary_code: 'meeting.decision',
      expected_material_state_ref: OUTCOME_STATE_1,
      result_code: 'decision.reached',
      note: null,
    });
    expect(screen.getByText('Outcome: decision.reached')).toBeTruthy();
  });
});
