import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { ResponsibilityControls } from './responsibility-controls';

const EVENT = '01991f2a-1234-7abc-8def-1234567890ab';
const PERSON = '01991f2a-1234-7abc-8def-1234567890ac';

type Fetch = typeof globalThis.fetch;

function responsibility(holder: string | null) {
  return {
    subject_kind: 'event',
    subject_native_ref: EVENT,
    responsible_person_ref: holder,
    responsible_is_self: holder !== null,
    established_at: holder === null ? null : '2026-09-25T08:00:00Z',
    replayed: false,
  };
}

function participation(requirement: 'required' | 'optional' | null) {
  return {
    event_ref: EVENT,
    participant_person_ref: PERSON,
    participant_is_self: true,
    requirement_code: requirement,
    established_at: '2026-09-25T08:00:00Z',
    replayed: false,
  };
}

describe('responsibility controls', () => {
  it('assigns Responsibility to the actor without sending a Person reference', async () => {
    let holder: string | null = null;
    const bodies: unknown[] = [];
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith('/expected-participation')) {
        return Response.json([]);
      }
      if (init?.method === 'PUT') {
        bodies.push(JSON.parse(String(init.body)));
        holder = PERSON;
        return Response.json(responsibility(holder));
      }
      return Response.json(responsibility(holder));
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ResponsibilityControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Nessun responsabile');

    fireEvent.click(screen.getByText('Assegna a me'));
    await screen.findByText('Responsabile: tu');

    expect(bodies).toEqual([
      {
        operation_id: expect.any(String),
        holder: 'self',
        expected_holder: null,
      },
    ]);
    vi.unstubAllGlobals();
  });

  it('sends the previously read requirement as the expected value', async () => {
    let current: 'required' | 'optional' | null = 'required';
    const bodies: unknown[] = [];
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith('/expected-participation') && init?.method === 'PUT') {
        const body = JSON.parse(String(init.body));
        bodies.push(body);
        current = body.requirement_code;
        return Response.json(participation(current));
      }
      if (url.endsWith('/expected-participation')) {
        return Response.json(current === null ? [] : [participation(current)]);
      }
      return Response.json(responsibility(null));
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ResponsibilityControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Partecipazione attesa: obbligatoria');

    fireEvent.click(screen.getByText('Facoltativa'));
    await screen.findByText('Partecipazione attesa: facoltativa');

    expect(bodies).toEqual([
      {
        operation_id: expect.any(String),
        participant: 'self',
        requirement_code: 'optional',
        expected_requirement_code: 'required',
      },
    ]);
    vi.unstubAllGlobals();
  });

  it('reports a rejected command instead of showing an optimistic state', async () => {
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith('/expected-participation')) {
        return Response.json([]);
      }
      if (init?.method === 'PUT') {
        return Response.json(
          { detail: 'Responsibility holder changed since it was read.' },
          { status: 409 },
        );
      }
      return Response.json(responsibility(null));
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ResponsibilityControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Nessun responsabile');

    fireEvent.click(screen.getByText('Assegna a me'));
    await waitFor(() => {
      expect(screen.getByRole('status').textContent).toContain(
        'Responsibility holder changed since it was read.',
      );
    });
    expect(screen.getByText('Nessun responsabile')).toBeTruthy();
    vi.unstubAllGlobals();
  });

  it('does not offer Event Participation controls on an Activity', async () => {
    const fetchFn = vi.fn<Fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      return Response.json({
        subject_kind: 'activity',
        subject_native_ref: EVENT,
        responsible_person_ref: null,
        responsible_is_self: false,
        established_at: null,
        replayed: false,
      });
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ResponsibilityControls kind="activity" subjectRef={EVENT} />);
    await screen.findByText('Nessun responsabile');
    expect(screen.queryByText('Partecipazione attesa: non indicata')).toBeNull();
    expect(screen.queryByText('Obbligatoria')).toBeNull();
    vi.unstubAllGlobals();
  });
});
