import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

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
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('assigns Responsibility to the actor without sending a Person reference', async () => {
    let holder: string | null = null;
    const bodies: unknown[] = [];
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/person-referents')) return Response.json([]);
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
      if (url.endsWith('/person-referents')) return Response.json([]);
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
      if (url.endsWith('/person-referents')) return Response.json([]);
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
      expect(screen.getByRole('alert').textContent).toContain(
        'Responsibility holder changed since it was read.',
      );
    });
    expect(screen.getByText('Nessun responsabile')).toBeTruthy();
    vi.unstubAllGlobals();
  });

  it('does not offer Event Participation controls on an Activity', async () => {
    const fetchFn = vi.fn<Fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/person-referents')) return Response.json([]);
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
  it('uses a local Person referent for responsibility and expected Event participation', async () => {
    const OTHER = '01991f2a-1234-7abc-8def-1234567890ad';
    const commands: Array<Record<string, unknown>> = [];
    let holder: string | null = null;
    let requirement: 'required' | 'optional' | null = null;
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith('/person-referents')) {
        return Response.json([{
          person_ref: OTHER, display_label: 'Anna',
          revision: 1, replayed: false,
        }]);
      }
      if (url.endsWith('/expected-participation')) {
        if (init?.method === 'PUT') {
          const body = JSON.parse(String(init.body)) as Record<string, unknown>;
          commands.push(body);
          requirement = body.requirement_code as 'required' | 'optional';
        }
        return Response.json(
          init?.method === 'PUT'
            ? participation(requirement)
            : requirement === null
              ? []
              : [{
                  ...participation(requirement),
                  participant_person_ref: OTHER,
                  participant_is_self: false,
                }],
        );
      }
      if (init?.method === 'PUT') {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        commands.push(body);
        holder = OTHER;
      }
      return Response.json({
        ...responsibility(holder),
        responsible_is_self: false,
      });
    });
    vi.stubGlobal('fetch', fetchFn);
    render(<ResponsibilityControls kind="event" subjectRef={EVENT} />);
    await screen.findByRole('option', { name: 'Anna' });
    fireEvent.change(screen.getByRole('combobox', {
      name: 'Persona per responsabilità o partecipazione',
    }), { target: { value: OTHER } });
    fireEvent.click(screen.getByText('Assegna a Anna'));
    await screen.findByText('Responsabile: Anna');
    fireEvent.click(screen.getByText('Obbligatoria'));
    await waitFor(() => expect(commands).toHaveLength(2));
    expect(commands[0]).toMatchObject({ holder: OTHER, expected_holder: null });
    expect(commands[1]).toMatchObject({
      participant: OTHER, requirement_code: 'required',
      expected_requirement_code: null,
    });
  });


  it('persists a created Person through rename, role removal and participation removal', async () => {
    let created = false;
    let displayLabel = '';
    let revision = 0;
    let holder: string | null = null;
    let requirement: 'required' | 'optional' | null = null;
    const commands: Array<Record<string, unknown>> = [];
    const person = () => ({
      person_ref: PERSON,
      display_label: displayLabel,
      revision,
      replayed: false,
    });
    const fetchFn = vi.fn<Fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith('/person-referents')) {
        if (init?.method === 'POST') {
          const body = JSON.parse(String(init.body)) as Record<string, unknown>;
          commands.push(body);
          created = true;
          displayLabel = String(body.display_label);
          revision = 1;
          return Response.json(person(), { status: 201 });
        }
        return Response.json(created ? [person()] : []);
      }
      if (url.endsWith('/person-referents/' + PERSON) && init?.method === 'PATCH') {
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        commands.push(body);
        displayLabel = String(body.display_label);
        revision += 1;
        return Response.json(person());
      }
      if (url.endsWith('/expected-participation')) {
        if (init?.method === 'PUT') {
          const body = JSON.parse(String(init.body)) as Record<string, unknown>;
          commands.push(body);
          requirement = body.requirement_code as 'required' | 'optional' | null;
          return Response.json({
            ...participation(requirement),
            participant_is_self: false,
          });
        }
        return Response.json(requirement === null ? [] : [{
          ...participation(requirement),
          participant_is_self: false,
        }]);
      }
      if (url.endsWith('/responsibility')) {
        if (init?.method === 'PUT') {
          const body = JSON.parse(String(init.body)) as Record<string, unknown>;
          commands.push(body);
          holder = body.holder as string | null;
        }
        return Response.json({ ...responsibility(holder), responsible_is_self: false });
      }
      throw new Error('Unexpected request: ' + url);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ResponsibilityControls kind="event" subjectRef={EVENT} />);
    await screen.findByText('Nessun responsabile');
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome locale della persona' }), {
      target: { value: 'Anna' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi persona' }));
    await screen.findByRole('option', { name: 'Anna' });
    expect(screen.getByRole('status').textContent).toContain(
      'Per assegnarle la responsabilità, premi “Assegna a Anna”.',
    );
    expect(screen.getByText('Nessun responsabile')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Assegna a Anna' }));
    await screen.findByText('Responsabile: Anna');

    fireEvent.change(screen.getByRole('textbox', { name: 'Nome locale della persona' }), {
      target: { value: 'Anna Rossi' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Correggi nome' }));
    await screen.findByText('Responsabile: Anna Rossi');
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi responsabilità' }));
    await screen.findByText('Nessun responsabile');

    fireEvent.click(screen.getByRole('button', { name: 'Obbligatoria' }));
    await screen.findByText('Partecipazione attesa: obbligatoria');
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi partecipazione' }));
    await screen.findByText('Partecipazione attesa: non indicata');

    expect(commands).toHaveLength(6);
    expect(commands[0]).toMatchObject({ display_label: 'Anna' });
    expect(commands[1]).toMatchObject({ holder: PERSON, expected_holder: null });
    expect(commands[2]).toMatchObject({
      display_label: 'Anna Rossi', expected_revision: 1,
    });
    expect(commands[3]).toMatchObject({ holder: null, expected_holder: PERSON });
    expect(commands[4]).toMatchObject({
      participant: PERSON, requirement_code: 'required', expected_requirement_code: null,
    });
    expect(commands[5]).toMatchObject({
      participant: PERSON, requirement_code: null, expected_requirement_code: 'required',
    });
  });

});
