// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomeCreateInteractionBridge } from '../../home/ui/home-create-interaction-bridge';
import type {
  TemporalAuthorActivityRequest,
  TemporalAuthorEventRequest,
  TemporalAuthoringDataSource,
  TemporalAuthoredActivityResult,
  TemporalAuthoredEventResult,
} from '../../temporal';
import { TEMPORAL_CREATE_RECENT_COLORS_KEY } from './temporal-create-recent-colors';
import { TemporalCreateEntry } from './temporal-create-entry';

const DEFAULT_COLOR = '#EA5C12';
const SCHEDULE_REF = '0199a111-1111-7111-8111-111111111120';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  window.localStorage.clear();
  vi.unstubAllGlobals();
});

function activityResult(
  title: string,
  scheduled = false,
): TemporalAuthoredActivityResult {
  return Object.freeze({
    item: Object.freeze({
      subjectRef: '0199a111-1111-7111-8111-111111111111',
      title,
      createdAt: Temporal.Instant.from('2026-09-30T19:00:00Z'),
      description: null,
      location: null,
      colorCode: null,
      lifeAreaRef: null,
      lifeAreaAssignmentRevision: null,
      lifeAreaColorCode: null,
      lifeAreaRevision: null,
    }),
    schedule: scheduled
      ? Object.freeze({
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: '0199a111-1111-7111-8111-111111111121',
          placement: Object.freeze({
            kind: 'absolute-interval' as const,
            startsAt: Temporal.Instant.from('2026-09-30T19:00:00Z'),
            endsAt: Temporal.Instant.from('2026-09-30T19:30:00Z'),
          }),
        })
      : null,
    sessionCaptureMode: 'record',
    childGuardMode: 'none',
    plannedSlices: Object.freeze([]),
    activityIntervals: Object.freeze([]),
    children: Object.freeze([]),
    replayed: false,
  });
}

function eventResult(
  title: string,
  scheduled = false,
): TemporalAuthoredEventResult {
  return Object.freeze({
    ...activityResult(title, scheduled),
    agendaRevision: 0,
    agendaParts: Object.freeze([]),
  });
}

function renderEntry(
  contexts: readonly {
    id: string;
    label: string;
    tone: 'personal';
    revision?: number;
    colorCode?: string | null;
  }[] = [],
  scheduledResult = false,
  defaultDate = '2026-09-30',
) {
  const activityRequests: TemporalAuthorActivityRequest[] = [];
  const eventRequests: TemporalAuthorEventRequest[] = [];
  const source: TemporalAuthoringDataSource = {
    authorActivity: vi.fn(async (request) => {
      activityRequests.push(request);
      return activityResult(request.title, scheduledResult);
    }),
    authorEvent: vi.fn(async (request) => {
      eventRequests.push(request);
      return eventResult(request.title, scheduledResult);
    }),
  };
  const rendered = render(
    <>
      <HomeCreateInteractionBridge />
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from(defaultDate)}
        contexts={contexts}
        authoringDataSource={source}
        onPreview={() => undefined}
        onApplied={() => false}
        creationEnabled={false}
      />
    </>,
  );
  const quickAdd = rendered.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!quickAdd) throw new Error('Expected Create trigger.');
  fireEvent.click(quickAdd);
  return { ...rendered, activityRequests, eventRequests };
}

describe('Temporal Create U2 entry', () => {
  it('submits named future Session planning without exposing Sub-Activities', async () => {
    const { activityRequests } = renderEntry([], false, '2132-03-06');
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Progetto' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Opzioni avanzate/ }));

    expect(screen.queryByText('Sotto-attività')).toBeNull();

    const settings = document.querySelector('[data-create-structure-actions]');
    if (!settings) throw new Error('Expected Activity settings.');
    fireEvent.click(within(settings as HTMLElement).getByLabelText('Sessione'));

    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi Sessione pianificata' }),
    );
    const planned = document.querySelector('[data-create-planned-session]');
    if (!planned) throw new Error('Expected planned Session.');
    fireEvent.change(
      within(planned as HTMLElement).getByLabelText('Nome Sessione'),
      {
        target: { value: 'Ricerca fonti' },
      },
    );
    fireEvent.click(within(planned as HTMLElement).getByRole('button', { name: 'Orario' }));
    fireEvent.change(
      within(planned as HTMLElement).getByLabelText('Inizio Sessione'),
      {
        target: { value: '09:15' },
      },
    );
    fireEvent.change(
      within(planned as HTMLElement).getByLabelText('Fine Sessione'),
      {
        target: { value: '09:30' },
      },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.sessionCaptureMode).toBe('record_and_live');
    expect(activityRequests[0]?.plannedSliceNames).toEqual(['Ricerca fonti']);
    expect(activityRequests[0]?.plannedSlices).toHaveLength(1);
    expect(activityRequests[0]?.children).toEqual([]);
  });

  it('creates an Activity without requiring any Life Area and persists the DANTE default color', async () => {
    const { activityRequests } = renderEntry();

    expect(screen.getByRole('option', { name: 'Ripeti · Mai' })).toBeTruthy();
    expect(
      (screen.getByLabelText('Ricorda') as HTMLSelectElement).disabled,
    ).toBe(false);
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Passeggiata' },
    });
    fireEvent.change(screen.getByLabelText('Località'), {
      target: { value: 'Lungofiume' },
    });
    fireEvent.change(screen.getByLabelText('Descrizione'), {
      target: { value: 'Lungo il fiume' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.lifeArea).toBeUndefined();
    expect(activityRequests[0]?.itemColorCode).toBe(DEFAULT_COLOR);
    expect(activityRequests[0]?.location).toBe('Lungofiume');
    expect(activityRequests[0]?.description).toBe('Lungo il fiume');
  });

  it('never exposes the presentation-only unassigned Timeline bucket as a selectable Life Area', () => {
    renderEntry([
      {
        id: 'legacy-unassigned',
        label: 'Senza Life Area',
        tone: 'personal',
      },
      {
        id: '0199a111-1111-7111-8111-111111111130',
        label: 'Corpo',
        tone: 'personal',
        revision: 1,
        colorCode: '#8E24AA',
      },
    ]);

    fireEvent.focus(screen.getByLabelText('Life Area (opzionale)'));

    expect(
      screen.getByRole('option', { name: 'Nessuna Life Area' }),
    ).toBeTruthy();
    expect(screen.getByRole('option', { name: 'Corpo' })).toBeTruthy();
    expect(
      screen.queryByRole('option', { name: 'Senza Life Area' }),
    ).toBeNull();
  });

  it('stages a new Life Area locally and sends the real default orange only with accepted Add', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Studio' },
    });
    fireEvent.change(screen.getByLabelText('Life Area (opzionale)'), {
      target: { value: 'Formazione' },
    });

    expect(activityRequests).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.lifeArea).toEqual({
      newName: 'Formazione',
      colorCode: DEFAULT_COLOR,
    });
  });

  it('preserves the selected item color when typing a new Life Area name', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.click(
      screen.getByRole('button', { name: 'Colore attività o evento' }),
    );
    const palette = screen.getByRole('dialog', { name: 'Scegli colore' });
    fireEvent.click(within(palette).getByRole('button', { name: 'Blu' }));

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Studio blu' },
    });
    fireEvent.change(screen.getByLabelText('Life Area (opzionale)'), {
      target: { value: 'Formazione blu' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.lifeArea).toEqual({
      newName: 'Formazione blu',
      colorCode: '#4285F4',
    });
  });

  it('keeps curated colors and the custom picker inside one floating popup without dismissing Create', () => {
    renderEntry();

    fireEvent.click(
      screen.getByRole('button', { name: 'Colore attività o evento' }),
    );
    const palette = screen.getByRole('dialog', { name: 'Scegli colore' });

    expect(palette.classList.contains('is-floating')).toBe(true);
    expect(document.querySelector('input[type="color"]')).toBeNull();
    expect(within(palette).getByRole('button', { name: 'Rosso' })).toBeTruthy();
    expect(
      within(palette).getByRole('button', { name: 'Giallo' }),
    ).toBeTruthy();
    expect(within(palette).getByRole('button', { name: 'Blu' })).toBeTruthy();
    expect(within(palette).getByTitle('Arancione DANTE')).toBeTruthy();

    fireEvent.pointerDown(within(palette).getByRole('button', { name: 'Blu' }));
    fireEvent.click(within(palette).getByRole('button', { name: 'Blu' }));
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeTruthy();

    fireEvent.click(
      within(palette).getByRole('button', { name: 'Colore personalizzato' }),
    );
    expect(
      within(palette).getByLabelText('Selettore colore personalizzato'),
    ).toBeTruthy();
    expect(within(palette).getByLabelText('Codice colore HEX')).toBeTruthy();
    expect(palette.querySelector('.react-colorful')).toBeTruthy();
    expect(
      screen.queryByRole('dialog', { name: 'Colore personalizzato' }),
    ).toBeNull();
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeTruthy();
  });

  it('remembers only colors actually used when Add is submitted, not colors merely inspected', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.click(
      screen.getByRole('button', { name: 'Colore attività o evento' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Blu' }));
    expect(
      window.localStorage.getItem(TEMPORAL_CREATE_RECENT_COLORS_KEY),
    ).toBeNull();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Blu usato' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(
      JSON.parse(
        window.localStorage.getItem(TEMPORAL_CREATE_RECENT_COLORS_KEY) ?? '[]',
      ),
    ).toEqual(['#4285F4']);
  });

  it('configures B11 reminder only after accepted scheduled U2 authoring', async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.endsWith('/api/v1/auth/session')) {
          return new Response(
            JSON.stringify({ authenticated: true, csrf_token: 'csrf-test' }),
            { status: 200, headers: { 'Content-Type': 'application/json' } },
          );
        }
        if (
          url.includes(`/api/v1/temporal/schedules/${SCHEDULE_REF}/reminder`)
        ) {
          expect(init?.method).toBe('PUT');
          const body = JSON.parse(String(init?.body ?? '{}')) as Record<
            string,
            unknown
          >;
          expect(body.enabled).toBe(true);
          expect(body.lead_minutes).toBe(15);
          return new Response(
            JSON.stringify({
              reminder_ref: '0199a111-1111-7111-8111-111111111122',
              schedule_ref: SCHEDULE_REF,
              material_state_ref: '0199a111-1111-7111-8111-111111111123',
              enabled: true,
              lead_minutes: 15,
              schedule_starts_at: '2026-09-30T19:00:00Z',
              due_at: '2026-09-30T18:45:00Z',
              disposition_code: 'pending',
              replayed: false,
            }),
            { status: 200, headers: { 'Content-Type': 'application/json' } },
          );
        }
        throw new Error(`Unexpected fetch ${url}`);
      },
    );
    vi.stubGlobal('fetch', fetchMock);

    const { activityRequests } = renderEntry([], true);
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Dentista' },
    });
    fireEvent.change(screen.getByLabelText('Ricorda'), {
      target: { value: '15' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeNull();
  });

  it('routes a scheduled Event through the U2 Event endpoint', async () => {
    const { eventRequests } = renderEntry();

    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Workshop' },
    });
    fireEvent.change(screen.getByLabelText('Località'), {
      target: { value: 'Sala A' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(eventRequests).toHaveLength(1));
    expect(eventRequests[0]?.title).toBe('Workshop');
    expect(eventRequests[0]?.itemColorCode).toBe(DEFAULT_COLOR);
    expect(eventRequests[0]?.location).toBe('Sala A');
    expect(eventRequests[0]?.placement).toBeDefined();
  });

  it('persists Event expected participation through the proven B09 vertical', async () => {
    const eventRef = '0199a111-1111-7111-8111-111111111111';
    const participationBodies: Record<string, unknown>[] = [];
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.endsWith('/api/v1/temporal/person-referents')) {
          return new Response(JSON.stringify([]), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          });
        }
        if (url.endsWith('/api/v1/auth/session')) {
          return new Response(
            JSON.stringify({ authenticated: true, csrf_token: 'csrf-test' }),
            { status: 200, headers: { 'Content-Type': 'application/json' } },
          );
        }
        if (
          url.endsWith(
            `/api/v1/temporal/events/${eventRef}/expected-participation`,
          )
        ) {
          expect(init?.method).toBe('PUT');
          const body = JSON.parse(String(init?.body ?? '{}')) as Record<
            string,
            unknown
          >;
          participationBodies.push(body);
          return new Response(
            JSON.stringify({
              event_ref: eventRef,
              participant_person_ref: eventRef,
              participant_is_self: true,
              requirement_code: body.requirement_code,
              established_at: '2026-10-06T12:00:00Z',
              replayed: false,
            }),
            { status: 200, headers: { 'Content-Type': 'application/json' } },
          );
        }
        throw new Error(`Unexpected fetch ${url}`);
      },
    );
    vi.stubGlobal('fetch', fetchMock);

    const { eventRequests } = renderEntry();
    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Riunione partecipata' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Opzioni avanzate/ }));

    fireEvent.click(await screen.findByRole('button', { name: '＋ Aggiungi' }));
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(eventRequests).toHaveLength(1));
    await waitFor(() => expect(participationBodies).toHaveLength(1));
    expect(participationBodies[0]).toMatchObject({
      participant: 'self',
      requirement_code: 'required',
      expected_requirement_code: null,
    });
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeNull();
  });

  it('shows the same explicit all-day start/end date controls for Activity and Event', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.click(screen.getByRole('radio', { name: 'Tutto il giorno' }));
    expect(screen.getByRole('button', { name: /Data inizio:/ })).toBeTruthy();
    expect(screen.getByRole('button', { name: /Data fine:/ })).toBeTruthy();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Giornata fotografica' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    const placement = activityRequests[0]?.placement;
    expect(placement?.kind).toBe('date-span');
    if (placement?.kind !== 'date-span') {
      throw new Error('Expected all-day date-span placement.');
    }
    expect(placement.startDate.toString()).toBe('2026-09-30');
    expect(placement.endDateExclusive.toString()).toBe('2026-10-01');
    expect(screen.queryByText(/Schedule non è confermato/i)).toBeNull();
  });

  it('creates an Event in Da collocare without recurrence, reminder or an invented Schedule placement', async () => {
    const { eventRequests } = renderEntry();

    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
    fireEvent.change(screen.getByLabelText('Ripeti'), {
      target: { value: 'daily' },
    });
    fireEvent.click(screen.getByRole('radio', { name: 'Da collocare' }));
    expect(screen.queryByRole('option', { name: 'Ripeti · Mai' })).toBeNull();
    expect(screen.queryByLabelText('Ricorda')).toBeNull();

    fireEvent.click(screen.getByRole('radio', { name: 'Orario' }));
    expect((screen.getByLabelText('Ripeti') as HTMLSelectElement).value).toBe(
      'none',
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Da collocare' }));

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Cena da organizzare' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(eventRequests).toHaveLength(1));
    expect(eventRequests[0]?.title).toBe('Cena da organizzare');
    expect(eventRequests[0]?.placement).toBeUndefined();
  });
});
