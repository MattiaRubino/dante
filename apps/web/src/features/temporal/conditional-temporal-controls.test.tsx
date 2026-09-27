import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ConditionalTemporalControls } from './conditional-temporal-controls';

const EVENT = '01991f2a-1234-7abc-8def-1234567890ab';
const CONDITION = '01991f2a-1234-7abc-8def-1234567890ac';
const EVALUATION = '01991f2a-1234-7abc-8def-1234567890ad';
const ACTUAL = '01991f2a-1234-7abc-8def-1234567890ae';
const ACTUAL_STATE = '01991f2a-1234-7abc-8def-1234567890af';

type Fetch = typeof globalThis.fetch;

function unavailable() {
  return Response.json(
    {
      code: 'temporal.conditional.not_found',
      category: 'not_found',
      title: 'Conditional temporal intent unavailable',
      detail: 'Conditional temporal intent unavailable.',
    },
    { status: 404 },
  );
}

function condition(replayed = false) {
  return {
    condition_ref: CONDITION,
    subject_kind: 'event',
    subject_native_ref: EVENT,
    family_code: 'actual_realization',
    created_at: '2026-10-05T08:00:00Z',
    replayed,
  };
}

describe('Conditional temporal controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('recovers the canonical Condition by subject and evaluates PostgreSQL-derived truth', async () => {
    const writes: Array<Record<string, unknown>> = [];
    let created = false;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.includes('/conditions/actual-realization?')) {
        return created ? Response.json(condition()) : unavailable();
      }
      if (init?.method === 'POST' && url.endsWith('/conditions/actual-realization')) {
        writes.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        created = true;
        return Response.json(condition(), { status: 201 });
      }
      if (init?.method === 'POST' && url.endsWith(`/conditions/actual-realization/${CONDITION}/evaluations`)) {
        writes.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        return Response.json(
          {
            evaluation_ref: EVALUATION,
            condition_ref: CONDITION,
            result_code: 'satisfied',
            disposition_code: 'allow',
            actual_ref: ACTUAL,
            actual_realization_material_state_ref: ACTUAL_STATE,
            evaluated_at: '2026-10-05T09:00:00Z',
            replayed: false,
          },
          { status: 201 },
        );
      }
      return unavailable();
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ConditionalTemporalControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Condizione Actual: non configurata');

    fireEvent.click(screen.getByText('Crea condizione Actual'));
    await screen.findByText('Condizione Actual creata.');
    expect(writes[0]).toMatchObject({
      operation_id: expect.any(String),
      subject_kind: 'event',
      subject_native_ref: EVENT,
    });

    fireEvent.click(screen.getByText('Valuta condizione Actual'));
    await screen.findByText('Valutazione: soddisfatta → consenti');
    await waitFor(() => expect(writes).toHaveLength(2));
    expect(writes[1]).toMatchObject({ operation_id: expect.any(String) });
    expect(writes[1]).not.toHaveProperty('result_code');
    expect(writes[1]).not.toHaveProperty('disposition_code');
  });
});
