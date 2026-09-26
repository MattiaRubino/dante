import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ConfirmationControls } from './confirmation-controls';

const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ab';
const ACTUAL = '01991f2a-1234-7abc-8def-1234567890ac';
const ACTUAL_STATE = '01991f2a-1234-7abc-8def-1234567890ad';
const OUTCOME = '01991f2a-1234-7abc-8def-1234567890ae';
const OUTCOME_STATE = '01991f2a-1234-7abc-8def-1234567890af';
const CONFIRMATION = '01991f2a-1234-7abc-8def-1234567890b0';
const CONFIRMATION_STATE_1 = '01991f2a-1234-7abc-8def-1234567890b1';
const CONFIRMATION_STATE_2 = '01991f2a-1234-7abc-8def-1234567890b2';
const OTHER_CONFIRMATION = '01991f2a-1234-7abc-8def-1234567890b3';
const OTHER_PERSON = '01991f2a-1234-7abc-8def-1234567890b4';
const SELF_PERSON = '01991f2a-1234-7abc-8def-1234567890b5';

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

function outcome() {
  return {
    outcome_ref: OUTCOME,
    actual_ref: ACTUAL,
    actual_realization_material_state_ref: ACTUAL_STATE,
    material_state_ref: OUTCOME_STATE,
    disposition_code: 'decision.deferred',
    replayed: false,
  };
}

function confirmation(
  materialStateRef: string,
  stanceCode: string,
  extras: Partial<{
    confirmation_ref: string;
    confirmer_person_ref: string;
    confirmer_is_self: boolean;
  }> = {},
) {
  return {
    confirmation_ref: extras.confirmation_ref ?? CONFIRMATION,
    outcome_ref: OUTCOME,
    outcome_disposition_material_state_ref: OUTCOME_STATE,
    confirmer_person_ref: extras.confirmer_person_ref ?? SELF_PERSON,
    purpose_code: 'review.personal',
    material_state_ref: materialStateRef,
    stance_code: stanceCode,
    confirmer_is_self: extras.confirmer_is_self ?? true,
    replayed: false,
  };
}

function notFound(code: string, title: string, detail: string) {
  return Response.json(
    { code, category: 'not_found', title, detail },
    { status: 404 },
  );
}

describe('Confirmation controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('does not manufacture a Confirmation when no Outcome exists', async () => {
    const fetchFn = vi.fn<Fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith(`/events/${SUBJECT}/actual`)) {
        return notFound(
          'temporal.actual.not_found',
          'Actual unavailable',
          'No Actual is established for this subject.',
        );
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ConfirmationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Confirmation'));

    await screen.findByText('Confirmation non disponibile: registra prima un Outcome.');
    expect(screen.queryByText('Registra Confirmation')).toBeNull();
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('keeps absence unknown then records and corrects an explicit Confirmation', async () => {
    const bodies: Array<Record<string, unknown>> = [];
    let current: ReturnType<typeof confirmation> | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${SUBJECT}/actual`)) {
        return Response.json(actual());
      }
      if (url.endsWith(`/actuals/${ACTUAL}/outcome`)) {
        return Response.json(outcome());
      }
      if (init?.method === 'POST' && url.endsWith(`/outcomes/${OUTCOME}/confirmations`)) {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        bodies.push(body);
        current = confirmation(
          bodies.length === 1 ? CONFIRMATION_STATE_1 : CONFIRMATION_STATE_2,
          String(body.stance_code),
        );
        return Response.json({ ...current, replayed: false }, { status: 201 });
      }
      if (url.endsWith(`/outcomes/${OUTCOME}/confirmations`)) {
        return Response.json(current === null ? [] : [current]);
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ConfirmationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Confirmation'));

    await screen.findByText('Confirmation: nessuna Confirmation esplicita');
    await screen.findByText(
      'Nessuna Confirmation registrata. Questo non significa che l’Outcome sia falso.',
    );
    expect(screen.queryByText(/non confermato = falso/i)).toBeNull();
    expect(screen.queryByText('confirmed')).toBeNull();

    fireEvent.change(screen.getByLabelText('Scopo Confirmation'), {
      target: { value: 'review.personal' },
    });
    fireEvent.change(screen.getByLabelText('Attestazione Confirmation'), {
      target: { value: 'attested' },
    });
    fireEvent.click(screen.getByText('Registra Confirmation'));
    await screen.findByText('Confirmation registrata.');
    expect(screen.getByText('Confirmation: review.personal / attested')).toBeTruthy();

    expect(bodies[0]).toMatchObject({
      outcome_disposition_material_state_ref: OUTCOME_STATE,
      expected_material_state_ref: null,
      purpose_code: 'review.personal',
      stance_code: 'attested',
    });
    expect(bodies[0]).not.toHaveProperty('confirmed');

    fireEvent.change(screen.getByLabelText('Attestazione Confirmation'), {
      target: { value: 'retracted' },
    });
    fireEvent.click(screen.getByText('Correggi Confirmation'));
    await waitFor(() => expect(bodies).toHaveLength(2));
    expect(bodies[1]).toMatchObject({
      outcome_disposition_material_state_ref: OUTCOME_STATE,
      expected_material_state_ref: CONFIRMATION_STATE_1,
      stance_code: 'retracted',
    });
    expect(screen.getByText('Confirmation: review.personal / retracted')).toBeTruthy();
  });

  it('shows other actors’ Confirmation without treating it as universal truth', async () => {
    const fetchFn = vi.fn<Fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith(`/events/${SUBJECT}/actual`)) {
        return Response.json(actual());
      }
      if (url.endsWith(`/actuals/${ACTUAL}/outcome`)) {
        return Response.json(outcome());
      }
      if (url.endsWith(`/outcomes/${OUTCOME}/confirmations`)) {
        return Response.json([
          confirmation(CONFIRMATION_STATE_1, 'disputed', {
            confirmation_ref: OTHER_CONFIRMATION,
            confirmer_person_ref: OTHER_PERSON,
            confirmer_is_self: false,
          }),
        ]);
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ConfirmationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Confirmation'));

    await screen.findByText('Confirmation: nessuna Confirmation esplicita');
    await screen.findByText('Altre Confirmation sullo stesso Outcome: 1');
    expect(screen.queryByText(/confirmed=true/i)).toBeNull();
  });
});
