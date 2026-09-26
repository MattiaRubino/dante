import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ReconciliationControls } from './reconciliation-controls';

const SUBJECT = '01991f2a-1234-7abc-8def-1234567890ab';
const ACTUAL = '01991f2a-1234-7abc-8def-1234567890ac';
const ACTUAL_STATE = '01991f2a-1234-7abc-8def-1234567890ad';
const OUTCOME = '01991f2a-1234-7abc-8def-1234567890ae';
const OUTCOME_STATE = '01991f2a-1234-7abc-8def-1234567890af';
const CONFIRMATION_A = '01991f2a-1234-7abc-8def-1234567890b0';
const CONFIRMATION_A_STATE = '01991f2a-1234-7abc-8def-1234567890b1';
const CONFIRMATION_B = '01991f2a-1234-7abc-8def-1234567890b2';
const CONFIRMATION_B_STATE = '01991f2a-1234-7abc-8def-1234567890b3';
const PERSON_A = '01991f2a-1234-7abc-8def-1234567890b4';
const PERSON_B = '01991f2a-1234-7abc-8def-1234567890b5';
const RECONCILIATION = '01991f2a-1234-7abc-8def-1234567890b6';
const RECONCILIATION_STATE_1 = '01991f2a-1234-7abc-8def-1234567890b7';
const RECONCILIATION_STATE_2 = '01991f2a-1234-7abc-8def-1234567890b8';

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
  confirmationRef: string,
  materialStateRef: string,
  personRef: string,
  stanceCode: string,
) {
  return {
    confirmation_ref: confirmationRef,
    outcome_ref: OUTCOME,
    outcome_disposition_material_state_ref: OUTCOME_STATE,
    confirmer_person_ref: personRef,
    purpose_code: 'review.personal',
    material_state_ref: materialStateRef,
    stance_code: stanceCode,
    confirmer_is_self: personRef === PERSON_A,
    replayed: false,
  };
}

function reconciliation(
  materialStateRef: string,
  actionCode: string,
  evidence: readonly Record<string, string>[],
) {
  return {
    reconciliation_ref: RECONCILIATION,
    outcome_ref: OUTCOME,
    outcome_disposition_material_state_ref: OUTCOME_STATE,
    purpose_code: 'review.personal',
    material_state_ref: materialStateRef,
    action_code: actionCode,
    resolved_by_person_ref: PERSON_A,
    evidence,
    replayed: false,
  };
}

function evidence(confirmationRef: string, stateRef: string, roleCode: string) {
  return {
    confirmation_ref: confirmationRef,
    confirmation_attestation_material_state_ref: stateRef,
    role_code: roleCode,
  };
}

function notFound(code: string, title: string, detail: string) {
  return Response.json({ code, category: 'not_found', title, detail }, { status: 404 });
}

describe('Reconciliation controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('does not manufacture reconciliation without an Outcome', async () => {
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

    render(<ReconciliationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Reconciliation'));

    await screen.findByText('Reconciliation non disponibile: registra prima un Outcome.');
    expect(screen.queryByText('Registra Reconciliation')).toBeNull();
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('can explicitly keep the current Outcome unresolved without inventing evidence or truth', async () => {
    const bodies: Array<Record<string, unknown>> = [];
    let current: ReturnType<typeof reconciliation> | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${SUBJECT}/actual`)) return Response.json(actual());
      if (url.endsWith(`/actuals/${ACTUAL}/outcome`)) return Response.json(outcome());
      if (url.endsWith(`/outcomes/${OUTCOME}/confirmations`)) return Response.json([]);
      if (init?.method === 'POST' && url.endsWith(`/outcomes/${OUTCOME}/reconciliations`)) {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        bodies.push(body);
        current = reconciliation(RECONCILIATION_STATE_1, 'unresolved', []);
        return Response.json(current, { status: 201 });
      }
      if (url.endsWith(`/outcomes/${OUTCOME}/reconciliations`)) {
        return Response.json(current === null ? [] : [current]);
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ReconciliationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Reconciliation'));

    await screen.findByText('Reconciliation: nessuna decisione contestuale registrata');
    await screen.findByText(
      'Nessuna Reconciliation registrata. Il conflitto può restare esplicitamente irrisolto.',
    );
    fireEvent.click(screen.getByText('Registra Reconciliation'));
    await screen.findByText('Reconciliation registrata.');

    expect(bodies).toHaveLength(1);
    expect(bodies[0]).toMatchObject({
      outcome_disposition_material_state_ref: OUTCOME_STATE,
      expected_material_state_ref: null,
      purpose_code: 'review.personal',
      action_code: 'unresolved',
      evidence: [],
    });
    expect(bodies[0]).not.toHaveProperty('truth');
    expect(bodies[0]).not.toHaveProperty('resolved');
  });

  it('pins exact Confirmation states and uses expected-current when correcting selection', async () => {
    const confirmations = [
      confirmation(CONFIRMATION_A, CONFIRMATION_A_STATE, PERSON_A, 'attested'),
      confirmation(CONFIRMATION_B, CONFIRMATION_B_STATE, PERSON_B, 'disputed'),
    ];
    const bodies: Array<Record<string, unknown>> = [];
    let current: ReturnType<typeof reconciliation> | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${SUBJECT}/actual`)) return Response.json(actual());
      if (url.endsWith(`/actuals/${ACTUAL}/outcome`)) return Response.json(outcome());
      if (url.endsWith(`/outcomes/${OUTCOME}/confirmations`)) return Response.json(confirmations);
      if (init?.method === 'POST' && url.endsWith(`/outcomes/${OUTCOME}/reconciliations`)) {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        bodies.push(body);
        const state = bodies.length === 1 ? RECONCILIATION_STATE_1 : RECONCILIATION_STATE_2;
        current = reconciliation(
          state,
          String(body.action_code),
          body.evidence as readonly Record<string, string>[],
        );
        return Response.json(current, { status: 201 });
      }
      if (url.endsWith(`/outcomes/${OUTCOME}/reconciliations`)) {
        return Response.json(current === null ? [] : [current]);
      }
      throw new Error(`Unexpected fetch ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ReconciliationControls kind="event" subjectRef={SUBJECT} />);
    fireEvent.click(screen.getByText('Carica Reconciliation'));
    await screen.findByText('Reconciliation: nessuna decisione contestuale registrata');

    fireEvent.change(screen.getByLabelText('Azione Reconciliation'), {
      target: { value: 'select' },
    });
    expect(screen.getByText('select richiede esattamente una Confirmation selezionata.')).toBeTruthy();
    expect((screen.getByText('Registra Reconciliation') as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByLabelText(`Seleziona Confirmation ${CONFIRMATION_A}`));
    expect((screen.getByText('Registra Reconciliation') as HTMLButtonElement).disabled).toBe(false);
    fireEvent.click(screen.getByText('Registra Reconciliation'));
    await screen.findByText('Reconciliation registrata.');

    const firstEvidence = bodies[0]?.evidence as Array<Record<string, unknown>>;
    expect(bodies[0]).toMatchObject({
      outcome_disposition_material_state_ref: OUTCOME_STATE,
      expected_material_state_ref: null,
      action_code: 'select',
    });
    expect(firstEvidence).toEqual(
      expect.arrayContaining([
        evidence(CONFIRMATION_A, CONFIRMATION_A_STATE, 'selected'),
        evidence(CONFIRMATION_B, CONFIRMATION_B_STATE, 'considered'),
      ]),
    );

    fireEvent.click(screen.getByLabelText(`Seleziona Confirmation ${CONFIRMATION_A}`));
    fireEvent.click(screen.getByLabelText(`Seleziona Confirmation ${CONFIRMATION_B}`));
    fireEvent.click(screen.getByText('Correggi Reconciliation'));
    await waitFor(() => expect(bodies).toHaveLength(2));

    expect(bodies[1]).toMatchObject({
      outcome_disposition_material_state_ref: OUTCOME_STATE,
      expected_material_state_ref: RECONCILIATION_STATE_1,
      action_code: 'select',
    });
    const secondEvidence = bodies[1]?.evidence as Array<Record<string, unknown>>;
    expect(secondEvidence).toEqual(
      expect.arrayContaining([
        evidence(CONFIRMATION_A, CONFIRMATION_A_STATE, 'considered'),
        evidence(CONFIRMATION_B, CONFIRMATION_B_STATE, 'selected'),
      ]),
    );
    expect(screen.getByText('Reconciliation: review.personal / select')).toBeTruthy();
  });
});
