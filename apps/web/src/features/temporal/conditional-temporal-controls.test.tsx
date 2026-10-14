import {
  fetchRequestUrl,
  fetchRequestBody,
} from '../../test-support/fetch-request';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
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

function resolvedJson(value: unknown, init?: ResponseInit): Promise<Response> {
  return Promise.resolve(Response.json(value, init));
}

describe('Conditional temporal controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('recovers the canonical Condition by subject and evaluates PostgreSQL-derived truth', async () => {
    const writes: Array<Record<string, unknown>> = [];
    let created = false;
    const fetchFn = vi.fn<Fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return resolvedJson({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.includes('/conditions/actual-realization?')) {
        return created ? resolvedJson(condition()) : Promise.resolve(unavailable());
      }
      if (
        init?.method === 'POST' &&
        url.endsWith('/conditions/actual-realization')
      ) {
        writes.push(
          JSON.parse(fetchRequestBody(init.body)) as Record<string, unknown>,
        );
        created = true;
        return resolvedJson(condition(), { status: 201 });
      }
      if (
        init?.method === 'POST' &&
        url.endsWith(`/conditions/actual-realization/${CONDITION}/evaluations`)
      ) {
        writes.push(
          JSON.parse(fetchRequestBody(init.body)) as Record<string, unknown>,
        );
        return resolvedJson(
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
      return Promise.resolve(unavailable());
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ConditionalTemporalControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Condizione Actual: non configurata');

    fireEvent.click(screen.getByText('Crea condizione Actual'));
    await screen.findByText('Condizione Actual creata.');
    expect(typeof writes[0]?.operation_id).toBe('string');
    expect(writes[0]).toMatchObject({
      subject_kind: 'event',
      subject_native_ref: EVENT,
    });

    fireEvent.click(screen.getByText('Valuta condizione Actual'));
    await screen.findByText('Valutazione: soddisfatta → consenti');
    await waitFor(() => expect(writes).toHaveLength(2));
    expect(typeof writes[1]?.operation_id).toBe('string');
    expect(writes[1]).not.toHaveProperty('result_code');
    expect(writes[1]).not.toHaveProperty('disposition_code');
  });
});
