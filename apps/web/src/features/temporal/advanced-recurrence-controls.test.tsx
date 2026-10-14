import { domElement } from '../../test-support/dom-element';
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

import { AdvancedRecurrenceControls } from './advanced-recurrence-controls';

const EVENT = '01991f2a-1234-7abc-8def-1234567890ab';
const ROUTINE = '01991f2a-1234-7abc-8def-1234567890b1';
const STATE_1 = '01991f2a-1234-7abc-8def-1234567890ac';
const STATE_2 = '01991f2a-1234-7abc-8def-1234567890ad';
const ANCHOR = '01991f2a-1234-7abc-8def-1234567890ae';

type Fetch = typeof globalThis.fetch;

function recurrence(materialStateRef: string) {
  return {
    material_state_ref: materialStateRef,
    recurrence: {
      family_code: 'calendar_wall_clock',
    },
  };
}

function unavailable() {
  return Response.json(
    {
      code: 'temporal.advanced_recurrence.unavailable',
      category: 'not_found',
      title: 'Advanced Recurrence unavailable',
      detail: 'Current Recurrence is not a B11-A dynamic elapsed Recurrence.',
    },
    { status: 404 },
  );
}

function advanced(
  materialStateRef: string,
  mode: 'previous_completion' | 'anchor_stream',
  ownerKind: 'routine' | 'event' = 'event',
) {
  return {
    owner_kind: ownerKind,
    source_ref: ownerKind === 'routine' ? ROUTINE : EVENT,
    material_state_ref: materialStateRef,
    range_kind: 'open',
    expected_occurrence_count: null,
    effective_from: '2026-10-01T08:00:00Z',
    effective_until: null,
    elapsed_seconds: '90.000000',
    anchor_mode_code: mode,
    anchor_source_family: mode === 'anchor_stream' ? 'routine' : null,
    anchor_source_native_ref: mode === 'anchor_stream' ? ANCHOR : null,
    replayed: false,
  };
}

function resolvedJson(value: unknown, init?: ResponseInit): Promise<Response> {
  return Promise.resolve(Response.json(value, init));
}

describe('Advanced Recurrence controls', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('authors completion-relative recurrence against the current canonical MaterialState', async () => {
    const writes: Array<Record<string, unknown>> = [];
    let saved = false;
    const fetchFn = vi.fn<Fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return resolvedJson({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${EVENT}/recurrence`)) {
        return resolvedJson(recurrence(saved ? STATE_2 : STATE_1));
      }
      if (init?.method === 'PUT') {
        writes.push(
          JSON.parse(fetchRequestBody(init.body)) as Record<string, unknown>,
        );
        saved = true;
        return resolvedJson(advanced(STATE_2, 'previous_completion'), {
          status: 201,
        });
      }
      return Promise.resolve(unavailable());
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<AdvancedRecurrenceControls ownerKind="event" sourceRef={EVENT} />);
    await screen.findByText('Recurrence avanzata: non configurata');

    fireEvent.change(
      screen.getByLabelText('Ritardo Recurrence avanzata in secondi'),
      {
        target: { value: '90.000000' },
      },
    );
    fireEvent.change(screen.getByLabelText('Inizio Recurrence avanzata'), {
      target: { value: '2026-10-01T10:00' },
    });
    fireEvent.click(screen.getByText('Salva Recurrence avanzata'));

    await screen.findByText('Recurrence avanzata salvata.');
    expect(writes).toHaveLength(1);
    expect(typeof writes[0]?.operation_id).toBe('string');
    expect(writes[0]).toMatchObject({
      expected_material_state_ref: STATE_1,
      range_kind: 'open',
      expected_occurrence_count: null,
      elapsed_seconds: '90.000000',
      anchor_mode_code: 'previous_completion',
      anchor_source_family: null,
      anchor_source_native_ref: null,
    });
  });

  it('authors a typed anchor-stream recurrence without inventing a generic anchor', async () => {
    const writes: Array<Record<string, unknown>> = [];
    const fetchFn = vi.fn<Fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return resolvedJson({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/events/${EVENT}/recurrence`)) {
        return resolvedJson(recurrence(STATE_1));
      }
      if (init?.method === 'PUT') {
        writes.push(
          JSON.parse(fetchRequestBody(init.body)) as Record<string, unknown>,
        );
        return resolvedJson(advanced(STATE_2, 'anchor_stream'), {
          status: 201,
        });
      }
      return Promise.resolve(unavailable());
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<AdvancedRecurrenceControls ownerKind="event" sourceRef={EVENT} />);
    await screen.findByText('Recurrence avanzata: non configurata');

    fireEvent.change(screen.getByLabelText('Regola Recurrence avanzata'), {
      target: { value: 'anchor_stream' },
    });
    fireEvent.change(screen.getByLabelText('Tipo sorgente anchor'), {
      target: { value: 'routine' },
    });
    fireEvent.change(screen.getByLabelText('Riferimento sorgente anchor'), {
      target: { value: ANCHOR },
    });
    fireEvent.change(
      screen.getByLabelText('Ritardo Recurrence avanzata in secondi'),
      {
        target: { value: '45' },
      },
    );
    fireEvent.change(screen.getByLabelText('Inizio Recurrence avanzata'), {
      target: { value: '2026-10-01T10:00' },
    });
    fireEvent.click(screen.getByText('Salva Recurrence avanzata'));

    await waitFor(() => expect(writes).toHaveLength(1));
    expect(writes[0]).toMatchObject({
      expected_material_state_ref: STATE_1,
      elapsed_seconds: '45',
      anchor_mode_code: 'anchor_stream',
      anchor_source_family: 'routine',
      anchor_source_native_ref: ANCHOR,
    });
  });

  it('authors a Routine recurrence through the Routine owner endpoint', async () => {
    const writes: Array<{ url: string; body: Record<string, unknown> }> = [];
    const fetchFn = vi.fn<Fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return resolvedJson({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/routines/${ROUTINE}/recurrence`)) {
        return resolvedJson(recurrence(STATE_1));
      }
      if (
        init?.method === 'PUT' &&
        url.endsWith(`/routines/${ROUTINE}/advanced-recurrence`)
      ) {
        writes.push({
          url,
          body: JSON.parse(fetchRequestBody(init.body)) as Record<
            string,
            unknown
          >,
        });
        return resolvedJson(
          advanced(STATE_2, 'previous_completion', 'routine'),
          {
            status: 201,
          },
        );
      }
      return Promise.resolve(unavailable());
    });
    vi.stubGlobal('fetch', fetchFn);

    render(
      <AdvancedRecurrenceControls ownerKind="routine" sourceRef={ROUTINE} />,
    );
    await screen.findByText('Recurrence avanzata: non configurata');
    fireEvent.change(
      screen.getByLabelText('Ritardo Recurrence avanzata in secondi'),
      {
        target: { value: '3600' },
      },
    );
    fireEvent.click(screen.getByText('Salva Recurrence avanzata'));

    await screen.findByText('Recurrence avanzata salvata.');
    expect(writes).toHaveLength(1);
    expect(writes[0]?.body).toMatchObject({
      expected_material_state_ref: STATE_1,
      anchor_mode_code: 'previous_completion',
    });
    expect(writes[0]?.url).toContain(
      `/routines/${ROUTINE}/advanced-recurrence`,
    );
  });

  it('does not report a source as non-recurring when reading its Recurrence failed', async () => {
    const fetchFn = vi.fn<Fetch>((input) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith(`/routines/${ROUTINE}/recurrence`)) {
        return resolvedJson(
          {
            code: 'temporal.recurrence.persistence_unavailable',
            detail: 'Canonical Recurrence state could not be read.',
          },
          { status: 503 },
        );
      }
      return Promise.resolve(unavailable());
    });
    vi.stubGlobal('fetch', fetchFn);

    render(
      <AdvancedRecurrenceControls ownerKind="routine" sourceRef={ROUTINE} />,
    );

    await screen.findByRole('alert');
    expect(
      screen.getByText('Recurrence avanzata: lettura non disponibile'),
    ).toBeTruthy();
    expect(
      screen.queryByText('Recurrence avanzata: sorgente non ricorrente'),
    ).toBeNull();
    expect(
      domElement(
        screen.getByLabelText('Regola Recurrence avanzata'),
        HTMLSelectElement,
      ).disabled,
    ).toBe(true);
  });
});
