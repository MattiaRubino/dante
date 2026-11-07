// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import { EventInspectorActions } from './event-inspector-actions';
import { RecurringSeriesEditor } from './recurring-series-editor';
import { useTimelineCardDetails } from './timeline-card-details';
import type { TimelineEvent } from './model/timeline-types';
import { EventDetailDialog } from './timeline-overlays';

const loadEvent = vi.fn();
const loadOccurrenceEvent = vi.fn();
const listExpectedParticipation = vi.fn().mockResolvedValue([]);
const listOccurrenceExpectedParticipation = vi.fn().mockResolvedValue([]);
const listPersonReferents = vi.fn().mockResolvedValue([]);
const loadArea = vi.fn();
const loadProfile = vi.fn();
const reviseProfile = vi.fn();
const reviseAtomic = vi.fn();
const listObjectives = vi.fn().mockResolvedValue([]);
const getRealityPolicy = vi
  .fn()
  .mockResolvedValue({ mode: 'manual', stateRef: null });
const getDefinition = vi.fn();
const getReminder = vi.fn().mockResolvedValue(null);
const isRecurring = vi.fn().mockResolvedValue(false);
const eventSeed = vi.fn().mockResolvedValue(null);
const eventFirstOccurrence = vi.fn().mockResolvedValue(null);
const startExistingEvent = vi.fn().mockResolvedValue(undefined);
const previewHardDeletion = vi.fn();
const confirmHardDeletion = vi.fn();
const eventOccurrences = vi.fn();
const loadOccurrenceContext = vi.fn();
const loadOccurrencePatch = vi.fn();
const loadRecurringPreview = vi.fn();
const saveRecurringEvent = vi.fn();
const loadSeries = vi.fn();
const reviewSeries = vi.fn();
const acceptSeries = vi.fn();

vi.mock('../../../temporal/remote-recurring-series-edit', () => ({
  createRemoteRecurringSeriesEdit: () => ({
    load: loadSeries,
    preview: reviewSeries,
    accept: acceptSeries,
  }),
}));

vi.mock('../../../temporal/remote-recurring-profile-edit', () => ({
  createRemoteRecurringProfileEdit: () => ({
    loadOccurrenceContext,
    loadOccurrencePatch,
    loadPreview: loadRecurringPreview,
    saveEventProfile: saveRecurringEvent,
    saveEventLocal: saveRecurringEvent,
  }),
}));

vi.mock('../../../temporal/remote-temporal-hard-deletion', () => ({
  createRemoteTemporalHardDeletion: () => ({
    preview: previewHardDeletion,
    deleteConfirmed: confirmHardDeletion,
    eventOccurrences,
  }),
}));

vi.mock('../../../temporal/remote-event-recurrence-guard', () => ({
  createRemoteEventRecurrenceGuard: () => ({ isRecurring }),
}));
vi.mock('../../../temporal/remote-event-profile-data-source', () => ({
  createRemoteEventProfileDataSource: () => ({
    load: loadProfile,
    revise: reviseProfile,
    reviseAtomic,
  }),
}));
vi.mock('../../../temporal/remote-schedule-reminder-data-source', () => ({
  createRemoteScheduleReminderDataSource: () => ({ get: getReminder }),
}));
vi.mock(
  '../../../temporal/remote-reality-objective-data-source',
  async (importOriginal) => {
    const actual =
      await importOriginal<
        typeof import('../../../temporal/remote-reality-objective-data-source')
      >();
    return {
      ...actual,
      createRemoteRealityObjectiveDataSource: () => ({
        listObjectives,
        getDefinition,
        getRealityPolicy,
      }),
    };
  },
);
vi.mock('../../../temporal/remote-event-life-area-settings', () => ({
  createRemoteEventLifeAreaSettings: () => ({
    load: loadArea,
  }),
}));
vi.mock('../../../temporal/remote-event-agenda-data-source', () => ({
  createRemoteTemporalEventAgendaDataSource: () => ({
    loadEvent,
    loadOccurrenceEvent,
  }),
}));
vi.mock('../../../temporal/remote-existing-recurrence', () => ({
  createRemoteExistingRecurrence: () => ({
    eventSeed,
    eventFirstOccurrence,
    startEvent: startExistingEvent,
  }),
}));
vi.mock('../../../temporal/remote-responsibility-data-source', () => ({
  createRemoteTemporalResponsibilityDataSource: () => ({
    listExpectedParticipation,
    listOccurrenceExpectedParticipation,
    listPersonReferents,
  }),
}));

const placement = {
  kind: 'named-zone-local' as const,
  startsLocalAt: Temporal.PlainDateTime.from('2026-10-09T09:00'),
  endsLocalAt: Temporal.PlainDateTime.from('2026-10-09T10:30'),
  zoneId: 'Europe/Rome',
  resolvedStartAt: Temporal.Instant.from('2026-10-09T07:00:00Z'),
  resolvedEndAt: Temporal.Instant.from('2026-10-09T08:30:00Z'),
};
const eventRef = '0199a111-1111-7111-8111-111111111111';

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
  isRecurring.mockResolvedValue(false);
  eventSeed.mockResolvedValue(null);
  eventFirstOccurrence.mockResolvedValue(null);
  startExistingEvent.mockResolvedValue(undefined);
  getRealityPolicy.mockResolvedValue({ mode: 'manual', stateRef: null });
  getReminder.mockResolvedValue(null);
  listObjectives.mockResolvedValue([]);
  loadArea.mockResolvedValue({
    options: [],
    currentRef: null,
    currentRevision: 0,
  });
  listExpectedParticipation.mockResolvedValue([]);
  listOccurrenceExpectedParticipation.mockResolvedValue([]);
  listPersonReferents.mockResolvedValue([]);
});

describe('Event Inspector actions', () => {
  it('reads the selected Event occurrence for the card agenda and objective counters', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    loadOccurrenceEvent.mockResolvedValue({
      lifeAreaRef: null,
      agendaParts: ['Apertura', 'Chiusura'],
    });
    listObjectives.mockResolvedValue([{ label: 'Presenza' }]);
    const event = {
      id: 'selected-event-occurrence',
      canonicalBasis: {
        kind: 'scheduled-occurrence',
        sourceKind: 'event',
        sourceNativeRef: eventRef,
        occurrenceRef,
      },
    } as TimelineEvent;
    function CardDetailsProbe() {
      const details = useTimelineCardDetails(event);
      return (
        <output>
          {details
            ? `${details.agendaCount}/${details.objectiveCount}`
            : 'Caricamento'}
        </output>
      );
    }
    render(<CardDetailsProbe />);
    expect(await screen.findByText('2/1')).toBeTruthy();
    expect(loadOccurrenceEvent).toHaveBeenCalledWith(
      occurrenceRef,
      expect.any(AbortSignal),
    );
    expect(listObjectives).toHaveBeenCalledWith('occurrence', occurrenceRef);
    expect(loadEvent).not.toHaveBeenCalled();
  });

  it('shows inherited recurring Event agenda when the instance detail is temporarily unavailable', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    loadOccurrenceEvent.mockRejectedValue(new Error('temporary unavailable'));
    loadEvent.mockResolvedValue({
      lifeAreaRef: null,
      agendaParts: ['Apertura', 'Chiusura'],
    });
    const event = {
      id: 'recurring-event',
      canonicalBasis: {
        kind: 'scheduled-occurrence',
        sourceKind: 'event',
        sourceNativeRef: eventRef,
        occurrenceRef,
      },
    } as TimelineEvent;
    function CardDetailsProbe() {
      const details = useTimelineCardDetails(event);
      return (
        <output>
          {details ? `Scaletta ${details.agendaCount}` : 'Caricamento'}
        </output>
      );
    }
    render(<CardDetailsProbe />);
    expect(await screen.findByText('Scaletta 2')).toBeTruthy();
    expect(loadEvent).toHaveBeenCalledWith(eventRef, expect.any(AbortSignal));
  });

  it('refreshes Event agenda and objectives together after an accepted edit', async () => {
    loadEvent.mockResolvedValue({ lifeAreaRef: null, agendaParts: [] });
    const event = {
      id: 'updated-event',
      canonicalBasis: {
        kind: 'scheduled-event',
        eventRef,
      },
    } as TimelineEvent;
    function CardDetailsProbe() {
      const details = useTimelineCardDetails(event);
      return (
        <output>
          {details
            ? `Scaletta ${details.agendaCount} · Obiettivi ${details.objectiveCount}`
            : 'Caricamento'}
        </output>
      );
    }
    render(<CardDetailsProbe />);
    expect(await screen.findByText('Scaletta 0 · Obiettivi 0')).toBeTruthy();
    loadEvent.mockResolvedValue({
      lifeAreaRef: null,
      agendaParts: ['Apertura'],
    });
    listObjectives.mockResolvedValue([{ label: 'Presenza' }]);
    act(() => invalidateTemporalTimelineRead());
    expect(await screen.findByText('Scaletta 1 · Obiettivi 1')).toBeTruthy();
  });

  it('edits only the selected recurring Event profile without revising the source', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    const context = {
      occurrenceRef,
      sourceRef: eventRef,
      editRevision: 2,
      recurrenceStateRef: '0199a666-6666-7666-8666-666666666666',
    };
    isRecurring.mockResolvedValue(true);
    loadOccurrenceContext.mockResolvedValue(context);
    loadRecurringPreview.mockResolvedValue({
      selectedProtection: null,
      fingerprint: 'a'.repeat(32),
      targetOccurrenceRefs: [occurrenceRef],
      protectedOccurrences: [],
    });
    loadOccurrenceEvent.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      agendaParts: ['Scaletta locale'],
      lifeAreaRef: null,
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 0,
    });
    loadOccurrencePatch.mockResolvedValue({ title: 'Conferenza locale' });
    listOccurrenceExpectedParticipation.mockResolvedValue([
      {
        participantPersonRef: '0199a333-3333-7333-8333-333333333333',
        participantIsSelf: false,
        requirementCode: 'required',
      },
    ]);
    listPersonReferents.mockResolvedValue([
      {
        personRef: '0199a333-3333-7333-8333-333333333333',
        displayLabel: 'Ada',
      },
    ]);
    saveRecurringEvent.mockResolvedValue(undefined);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        occurrenceRef={occurrenceRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    fireEvent.click(
      await screen.findByRole('button', { name: 'Solo questa istanza' }),
    );
    const title = await screen.findByRole('textbox', { name: 'Titolo Event' });
    expect(title).toHaveProperty('value', 'Conferenza locale');
    expect(screen.queryByRole('button', { name: 'Duplica' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Copia in Bozze' })).toBeNull();
    expect(screen.queryByText('Ambito: solo questa istanza.')).toBeNull();
    const localAgenda = screen.getByRole('region', { name: 'Scaletta evento' });
    expect(
      localAgenda.querySelector('.temporal-create-activity-tree__spine'),
    ).not.toBeNull();
    expect(
      title.compareDocumentPosition(localAgenda) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      screen.getByRole('textbox', { name: 'Punto scaletta 1' }),
    ).toHaveProperty('value', 'Scaletta locale');
    expect(
      screen.getByRole('combobox', { name: 'Partecipazione di Ada' }),
    ).toHaveProperty('value', 'required');
    expect(listObjectives).toHaveBeenCalledWith('occurrence', occurrenceRef);
    expect(getRealityPolicy).toHaveBeenCalledWith('occurrence', occurrenceRef);
    fireEvent.change(title, {
      target: { value: 'Conferenza locale aggiornata' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(saveRecurringEvent).toHaveBeenCalledWith(
        context,
        { title: 'Conferenza locale aggiornata' },
        {
          agendaParts: ['Scaletta locale'],
          lifeAreaRef: null,
          participants: [
            {
              personRef: '0199a333-3333-7333-8333-333333333333',
              displayLabel: 'Ada',
              requirementCode: 'required',
            },
          ],
        },
        expect.objectContaining({ objectives: null, schedule: null }),
        expect.any(String),
      ),
    );
    expect(reviseProfile).not.toHaveBeenCalled();
    expect(acceptSeries).not.toHaveBeenCalled();
  });

  it('closes an unchanged selected recurring Event without revising the series or instance', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    isRecurring.mockResolvedValue(true);
    loadOccurrenceContext.mockResolvedValue({
      occurrenceRef,
      sourceRef: eventRef,
      editRevision: 2,
    });
    loadRecurringPreview.mockResolvedValue({
      selectedProtection: null,
      fingerprint: 'a'.repeat(32),
      targetOccurrenceRefs: [occurrenceRef],
      protectedOccurrences: [],
    });
    loadOccurrenceEvent.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      agendaParts: [],
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 0,
    });
    loadOccurrencePatch.mockResolvedValue({});
    render(
      <EventInspectorActions
        eventRef={eventRef}
        occurrenceRef={occurrenceRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    fireEvent.click(
      await screen.findByRole('button', { name: 'Solo questa istanza' }),
    );
    await screen.findByRole('textbox', { name: 'Titolo Event' });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(
        screen.queryByRole('textbox', { name: 'Titolo Event' }),
      ).toBeNull(),
    );
    expect(saveRecurringEvent).not.toHaveBeenCalled();
    expect(acceptSeries).not.toHaveBeenCalled();
  });

  it('chooses from-next for a recorded recurring Event and confirms a reviewed structural revision', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    const context = {
      occurrenceRef,
      sourceRef: eventRef,
      editRevision: 2,
      recurrenceStateRef: '0199a666-6666-7666-8666-666666666666',
    };
    const preview = {
      fingerprint: 'a'.repeat(32),
      selectedProtection: 'registration',
      targetOccurrenceRefs: [],
      protectedOccurrences: [],
    };
    isRecurring.mockResolvedValue(true);
    loadOccurrenceContext.mockResolvedValue(context);
    loadOccurrencePatch.mockResolvedValue({});
    loadRecurringPreview.mockResolvedValue(preview);
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 0,
    });
    const source = {
      sourceRef: eventRef,
      owner: 'event',
      selectedDate: '2027-01-02',
      editRevision: 2,
      recurrenceStateRef: context.recurrenceStateRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      recurrence: {
        family_code: 'calendar_wall_clock',
        range_kind: 'open',
        pattern_code: 'daily',
        interval_count: 1,
        wall_times: ['09:00:00'],
      },
      structure: {
        version: 1,
        placement_kind: 'timed',
        duration_minutes: 90,
        reminder_lead_minutes: null,
        reality_mode: 'manual',
        agenda_parts: ['Introduzione'],
        objectives: [],
        life_area_ref: null,
      },
    };
    const structuralReview = {
      fingerprint: 'a'.repeat(64),
      targetRefs: [],
      newExpectedCount: 1,
      protected: [
        {
          occurrenceRef,
          expectedAt: '2027-01-02T08:00:00Z',
          reason: 'registration',
        },
      ],
    };
    loadSeries.mockResolvedValue(source);
    reviewSeries.mockResolvedValue(structuralReview);
    acceptSeries.mockResolvedValue(undefined);
    const fetchAreas = vi.fn(
      (_input: RequestInfo | URL, init?: RequestInit) => {
        const headers = new Headers(init?.headers);
        return Promise.resolve(
          headers.get('X-Dante-Client') === 'web' &&
            headers.has('X-Dante-Time-Zone')
            ? Response.json([])
            : Response.json(
                { detail: 'Missing client context' },
                { status: 400 },
              ),
        );
      },
    );
    vi.stubGlobal('fetch', fetchAreas);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        occurrenceRef={occurrenceRef}
        placement={placement}
        onDuplicate={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    expect(
      await screen.findByRole('dialog', { name: 'Modifica ricorrenza' }),
    ).toBeTruthy();
    fireEvent.click(
      await screen.findByRole('button', { name: 'Dalla prossima istanza' }),
    );
    fireEvent.change(await screen.findByRole('textbox', { name: 'Titolo' }), {
      target: { value: 'Nuova conferenza' },
    });
    const seriesAgenda = screen.getByRole('region', {
      name: 'Scaletta evento',
    });
    const seriesTitle = screen.getByRole('textbox', { name: 'Titolo' });
    const seriesTiming = screen.getByRole('region', {
      name: 'Orario della serie',
    });
    expect(
      seriesAgenda.querySelector('.temporal-create-activity-tree__spine'),
    ).not.toBeNull();
    expect(
      seriesTitle.compareDocumentPosition(seriesAgenda) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      seriesAgenda.compareDocumentPosition(seriesTiming) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Duplica' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Copia in Bozze' })).toBeNull();
    expect(
      screen.getAllByRole('button', { name: /^Data inizio:/ }),
    ).toHaveLength(1);
    expect(screen.getAllByRole('button', { name: /^Data fine:/ })).toHaveLength(
      1,
    );
    expect(screen.getByRole('group', { name: 'Fine' })).toBeTruthy();
    expect(screen.queryByText('Durata in minuti')).toBeNull();
    const areaRequest = fetchAreas.mock.calls.find(
      ([url]) => url === '/api/v1/temporal/life-areas',
    );
    expect(areaRequest?.[1]?.credentials).toBe('same-origin');
    expect(new Headers(areaRequest?.[1]?.headers).get('X-Dante-Client')).toBe(
      'web',
    );
    expect(
      new Headers(areaRequest?.[1]?.headers).has('X-Dante-Time-Zone'),
    ).toBe(true);
    fireEvent.click(screen.getByRole('button', { name: 'Verifica modifiche' }));
    await waitFor(() =>
      expect(reviewSeries).toHaveBeenCalledWith(
        expect.objectContaining({
          selectedRef: occurrenceRef,
          scope: 'from_next',
          profilePatch: { title: 'Nuova conferenza' },
        }),
      ),
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Conferma modifiche' }),
    );
    await waitFor(() =>
      expect(acceptSeries).toHaveBeenCalledWith(
        expect.objectContaining({ scope: 'from_next' }),
        structuralReview,
      ),
    );
    expect(saveRecurringEvent).not.toHaveBeenCalled();
    expect(reviseProfile).not.toHaveBeenCalled();
  });
  it('offers a copy to Bozze without exposing canonical unplacement', () => {
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={() => undefined}
      />,
    );
    expect(screen.getByRole('button', { name: 'Copia in Bozze' })).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: /Rimuovi Event dalla Timeline/ }),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: /Annulla rimozione Event/ }),
    ).toBeNull();
  });

  it('loads owner-scoped Agenda and Participation and opens a new draft without copying truth', async () => {
    getRealityPolicy.mockResolvedValue({
      mode: 'review_on_end',
      stateRef: 'policy-state',
    });
    listObjectives.mockResolvedValue([
      {
        label: 'Intervento',
        resultKind: 'boolean',
        comparatorCode: null,
        targetValue: null,
        targetMin: null,
        targetMax: null,
        unitCode: null,
        presentationOrder: 0,
      },
    ]);
    loadEvent.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      agendaRevision: 3,
      agendaParts: ['Presentazione', 'Domande'],
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
      lifeAreaRef: '0199a222-2222-7222-8222-222222222222',
    });
    listExpectedParticipation.mockResolvedValue([
      {
        eventRef,
        participantPersonRef: '0199a333-3333-7333-8333-333333333333',
        participantIsSelf: false,
        requirementCode: 'required',
      },
    ]);
    listPersonReferents.mockResolvedValue([
      {
        personRef: '0199a333-3333-7333-8333-333333333333',
        displayLabel: 'Collaboratore',
        revision: 1,
        replayed: false,
      },
    ]);
    const onDuplicate = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    await waitFor(() => expect(onDuplicate).toHaveBeenCalledOnce());
    expect(loadEvent).toHaveBeenCalledWith(eventRef);
    expect(listExpectedParticipation).toHaveBeenCalledWith(eventRef);
    expect(onDuplicate.mock.calls[0]?.[0]).toMatchObject({
      fields: {
        kind: 'event',
        title: 'Conferenza',
        event: { agendaParts: ['Presentazione', 'Domande'] },
        durationMinutes: 90,
      },
      advanced: {
        realityMode: 'review_on_end',
        objectives: [{ label: 'Intervento', resultKind: 'boolean' }],
        eventParticipants: [
          { displayLabel: 'Collaboratore', requirementCode: 'required' },
        ],
      },
    });
  });

  it('does not open an incomplete duplicate when an expected participant cannot be resolved', async () => {
    loadEvent.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      agendaRevision: 0,
      agendaParts: [],
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
      lifeAreaRef: null,
    });
    listExpectedParticipation.mockResolvedValue([
      {
        eventRef,
        participantPersonRef: '0199a333-3333-7333-8333-333333333333',
        participantIsSelf: false,
        requirementCode: 'required',
      },
    ]);
    listPersonReferents.mockResolvedValue([]);
    const onDuplicate = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'un partecipante non è più disponibile',
    );
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('edits the original Event locally or its first canonical series Occurrence', async () => {
    const firstRef = '0199a111-1111-7111-8111-222222222222';
    const sourceRef = '0199a111-1111-7111-8111-333333333333';
    const context = {
      occurrenceRef: firstRef,
      sourceRef,
      editRevision: 0,
      recurrenceStateRef: '0199a111-1111-7111-8111-444444444444',
    };
    eventFirstOccurrence.mockResolvedValue(firstRef);
    loadOccurrenceContext.mockResolvedValue(context);
    loadRecurringPreview.mockResolvedValue({ selectedProtection: null });
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Primo Evento',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 0,
      agendaParts: [],
    });
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    await screen.findByRole('dialog', { name: 'Modifica ricorrenza' });
    expect(loadOccurrenceContext).toHaveBeenCalledWith(firstRef);
    expect(loadRecurringPreview).toHaveBeenCalledWith(context, 'only_this');
    expect(loadOccurrenceEvent).not.toHaveBeenCalled();

    fireEvent.click(
      screen.getByRole('button', { name: 'Solo questa istanza' }),
    );
    await waitFor(() => expect(loadProfile).toHaveBeenCalledWith(eventRef));
    expect(loadOccurrenceEvent).not.toHaveBeenCalled();
  });

  it('starts a future recurrence from the saved Event while retaining the first identity', async () => {
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Visita',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 2,
      agendaRevision: 0,
      agendaParts: [],
    });
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        scheduleRef="0199a777-7777-7777-8777-777777777777"
        placementMaterialStateRef="0199a888-8888-7888-8888-888888888888"
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.click(
      await screen.findByRole('button', { name: 'Ripeti · Mai' }),
    );
    fireEvent.click(
      screen.getByRole('button', {
        name: 'Avvia ripetizione da questo Evento',
      }),
    );
    await waitFor(() => expect(startExistingEvent).toHaveBeenCalledOnce());
    expect(startExistingEvent).toHaveBeenCalledWith(
      expect.objectContaining({ eventRef, expectedProfileRevision: 2 }),
      expect.objectContaining({
        effective_from: '2026-10-09',
        wall_times: ['09:00'],
        zone_id: 'Europe/Rome',
      }),
      expect.any(String),
    );
    expect(reviseAtomic).not.toHaveBeenCalled();
  });

  it('edits current Event metadata with canonical CAS and leaves the existing identity intact', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: 'Prima',
      location: 'Roma',
      colorCode: '#ABCDEF',
      profileRevision: 2,
      agendaRevision: 1,
      agendaParts: ['Parte 1'],
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    };
    loadProfile.mockResolvedValue(current);
    reviseProfile.mockResolvedValue({
      ...current,
      title: 'Incontro',
      profileRevision: 3,
    });
    const onDuplicate = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.change(
      await screen.findByRole('textbox', { name: 'Titolo Event' }),
      {
        target: { value: 'Incontro' },
      },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(reviseProfile).toHaveBeenCalledWith(
        eventRef,
        current,
        {
          title: 'Incontro',
          description: 'Prima',
          location: 'Roma',
          colorCode: '#ABCDEF',
        },
        expect.any(String),
      ),
    );
    expect(await screen.findByText('Evento aggiornato.')).toBeTruthy();
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('saves Event metadata, Scaletta and Life Area in one aggregate request', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 2,
      agendaParts: ['Apertura'],
      lifeAreaRef: null,
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [{ ref: 'area-1', name: 'Lavoro' }],
      currentRef: null,
      currentRevision: 0,
    });
    reviseAtomic.mockResolvedValue({
      ...current,
      title: 'Incontro',
      agendaParts: ['Apertura', 'Discussione'],
      lifeAreaRef: 'area-1',
    });
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.change(
      await screen.findByRole('textbox', { name: 'Titolo Event' }),
      { target: { value: 'Incontro' } },
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi punto alla scaletta' }),
    );
    fireEvent.change(
      screen.getByRole('textbox', { name: 'Punto scaletta 2' }),
      {
        target: { value: 'Discussione' },
      },
    );
    fireEvent.change(
      screen.getByRole('textbox', { name: 'Life Area (opzionale)' }),
      { target: { value: 'Area inesistente' } },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    expect(
      (await screen.findAllByText('Scegli una Life Area dall’elenco.')).length,
    ).toBeGreaterThan(0);
    expect(reviseAtomic).not.toHaveBeenCalled();
    fireEvent.change(
      screen.getByRole('textbox', { name: 'Life Area (opzionale)' }),
      { target: { value: 'Lavoro' } },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(reviseAtomic).toHaveBeenCalledWith(
        eventRef,
        current,
        {
          profile: {
            title: 'Incontro',
            description: null,
            location: null,
            colorCode: null,
          },
          agendaParts: ['Apertura', 'Discussione'],
          lifeArea: { ref: 'area-1', expectedRevision: 0 },
        },
        expect.any(String),
      ),
    );
    expect(reviseProfile).not.toHaveBeenCalled();
  });

  it('uses the Activity objective row and includes a new Event objective in Save', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 0,
      agendaParts: [],
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    reviseAtomic.mockResolvedValue(current);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.click(
      await screen.findByRole('button', { name: '＋ Aggiungi obiettivo' }),
    );
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Presentare il progetto' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(reviseAtomic).toHaveBeenCalledOnce());
    expect(reviseAtomic.mock.calls[0]?.[2]).toMatchObject({
      objectives: {
        add: [
          {
            label: 'Presentare il progetto',
            resultKind: 'boolean',
            presentationOrder: 0,
          },
        ],
        revise: [],
        retire: [],
      },
    });
  });

  it('saves a changed Event execution policy with its previous state reference', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 0,
      agendaParts: [],
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    getRealityPolicy.mockResolvedValue({
      mode: 'manual',
      stateRef: 'policy-state-1',
    });
    reviseAtomic.mockResolvedValue(current);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.click(
      await screen.findByRole('radio', { name: 'Chiedi al termine' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(reviseAtomic).toHaveBeenCalledOnce());
    expect(reviseAtomic.mock.calls[0]?.[2]).toEqual({
      reality: { mode: 'review_on_end', expectedStateRef: 'policy-state-1' },
    });
  });

  it('keeps the Event Schedule material revision in the same Save as metadata', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 0,
      agendaParts: [],
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    reviseAtomic.mockResolvedValue(current);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        scheduleRef="0199a333-3333-7333-8333-333333333333"
        placementMaterialStateRef="0199a444-4444-7444-8444-444444444444"
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.change(
      await screen.findByRole('textbox', { name: 'Titolo Event' }),
      {
        target: { value: 'Nuova conferenza' },
      },
    );
    const schedule = screen.getByRole('group', { name: 'Orario Evento' });
    fireEvent.click(
      within(schedule).getByRole('button', {
        name: /Fuso orario: Europe\/Rome/,
      }),
    );
    fireEvent.click(
      within(schedule).getByRole('button', { name: 'Ora locale' }),
    );
    const time = within(schedule).getByRole('textbox', { name: 'Fine: ore' });
    fireEvent.change(time, { target: { value: '11' } });
    fireEvent.blur(time);
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(reviseAtomic).toHaveBeenCalledOnce());
    expect(reviseAtomic.mock.calls[0]?.[2]).toMatchObject({
      profile: { title: 'Nuova conferenza' },
      schedule: {
        scheduleRef: '0199a333-3333-7333-8333-333333333333',
        expectedMaterialStateRef: '0199a444-4444-7444-8444-444444444444',
        placement: { kind: 'floating_local_interval' },
      },
    });
  });

  it('includes the Event reminder in the atomic Save instead of writing separately', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 0,
      agendaParts: [],
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    reviseAtomic.mockResolvedValue(current);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        scheduleRef="0199a333-3333-7333-8333-333333333333"
        placementMaterialStateRef="0199a444-4444-7444-8444-444444444444"
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    const select = await screen.findByRole('combobox', { name: 'Ricorda' });
    fireEvent.change(select, { target: { value: '15' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(reviseAtomic).toHaveBeenCalledOnce());
    expect(reviseAtomic.mock.calls[0]?.[2]).toEqual({
      reminder: {
        scheduleRef: '0199a333-3333-7333-8333-333333333333',
        expectedStateRef: null,
        enabled: true,
        leadMinutes: 15,
      },
    });
  });

  it('edits expected participants through the shared Create control and one atomic Save', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaRevision: 0,
      agendaParts: [],
    };
    loadProfile.mockResolvedValue(current);
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    listExpectedParticipation.mockResolvedValue([
      {
        participantPersonRef: '0199a777-7777-7777-8777-777777777777',
        participantIsSelf: true,
        requirementCode: 'required',
      },
    ]);
    reviseAtomic.mockResolvedValue(current);
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    const requirement = await screen.findByRole('combobox', {
      name: 'Partecipazione di Io',
    });
    fireEvent.change(requirement, { target: { value: 'optional' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(reviseAtomic).toHaveBeenCalledOnce());
    expect(reviseAtomic.mock.calls[0]?.[2]).toEqual({
      participants: [
        {
          participantRef: 'self',
          requirementCode: 'optional',
          expectedRequirementCode: 'required',
        },
      ],
    });
  });

  it('opens the Event profile editor as a centered, bounded modal', async () => {
    loadArea.mockResolvedValue({
      options: [],
      currentRef: null,
      currentRevision: 0,
    });
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
    });
    render(
      <EventDetailDialog
        detail={{
          title: 'Conferenza',
          startMinute: 540,
          endMinute: 630,
          groupLabel: 'Lavoro',
          ownerKind: 'event',
          eventRef,
          eventPlacement: placement,
        }}
        opener={null}
        onClose={vi.fn()}
      />,
    );
    expect(
      screen.queryByRole('button', { name: 'Modifica Life Area' }),
    ).toBeNull();
    const toolbar = document.querySelector(
      '.timeline-event-modal__owner-actions .timeline-activity-inspector__toolbar',
    );
    expect(toolbar).toBeTruthy();
    expect(
      within(toolbar as HTMLElement)
        .getAllByRole('button')
        .map((button) => button.getAttribute('aria-label')),
    ).toEqual(['Modifica', 'Duplica', 'Copia in Bozze', 'Elimina Event']);
    expect(
      within(toolbar as HTMLElement).queryByRole('button', {
        name: 'Modifica Life Area',
      }),
    ).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    expect(
      await screen.findByRole('textbox', { name: 'Titolo Event' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('textbox', { name: 'Life Area (opzionale)' }),
    ).toBeTruthy();
    const eventForm = document.querySelector('.timeline-event-profile-editor');
    expect(eventForm).not.toBeNull();
    const footer = eventForm!.querySelector(
      '.timeline-event-profile-editor__actions',
    );
    expect(footer?.classList.contains('dante-temporal-panel-actions')).toBe(
      true,
    );
    expect(
      within(footer as HTMLElement)
        .getByRole('button', { name: 'Salva modifiche' })
        .classList.contains('is-primary'),
    ).toBe(true);
    expect(
      within(eventForm as HTMLElement).queryByText('Cambio dell’ora'),
    ).toBeNull();
    const sections = [
      '.timeline-event-profile-editor__title-row',
      '.temporal-create-event-agenda',
      '.timeline-event-schedule-editor',
      '.timeline-activity-editor__area-color',
      '[aria-label="Svolgimento e obiettivi"]',
      '.timeline-activity-editor__location',
      '.temporal-create-event-participants',
      '.timeline-activity-editor__description',
    ].map((selector) => eventForm!.querySelector(selector));
    expect(sections.every(Boolean)).toBe(true);
    for (let index = 1; index < sections.length; index += 1) {
      expect(
        sections[index - 1]?.compareDocumentPosition(sections[index]!),
      ).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    }
    await waitFor(() =>
      expect(screen.getByRole('dialog').className).toContain(
        'timeline-event-modal--event-edit',
      ),
    );
    expect(screen.getByRole('dialog').className).toContain(
      'timeline-event-modal--edit',
    );
    expect(
      screen
        .getByRole('dialog')
        .querySelector('.timeline-event-modal__owner-actions'),
    ).toBeNull();
    expect(
      screen
        .getByRole('textbox', { name: 'Titolo Event' })
        .closest('.timeline-event-profile-editor__body'),
    ).toBeTruthy();
    expect(
      screen
        .getByRole('textbox', { name: 'Titolo Event' })
        .closest('.temporal-create-title-row'),
    ).toBeTruthy();
    const editor = screen
      .getByRole('textbox', { name: 'Titolo Event' })
      .closest('.timeline-event-profile-editor');
    expect(editor).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Duplica' })).toBeNull();
    const bodySections = Array.from(
      editor!.querySelectorAll(
        '.timeline-event-profile-editor__body > :is(div, section)',
      ),
    );
    expect(bodySections[0]?.className).toContain(
      'timeline-event-profile-editor__title-row',
    );
    expect(bodySections.at(-1)?.className).toContain(
      'timeline-activity-editor__description',
    );
    expect(screen.getByRole('dialog').style.left).toBe('');
    expect(screen.getByRole('dialog').textContent).toContain('Modifica evento');
  });

  it('uses the inline discard overlay for Event Cancel and the Inspector close button', async () => {
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
    });
    const confirm = vi.fn();
    vi.stubGlobal('confirm', confirm);
    const onClose = vi.fn();
    render(
      <EventDetailDialog
        detail={{
          title: 'Conferenza',
          startMinute: 540,
          endMinute: 630,
          groupLabel: 'Lavoro',
          ownerKind: 'event',
          eventRef,
          eventPlacement: placement,
        }}
        opener={null}
        onClose={onClose}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    const title = await screen.findByRole('textbox', { name: 'Titolo Event' });
    fireEvent.change(title, { target: { value: 'Conferenza nuova' } });
    fireEvent.click(screen.getByRole('button', { name: 'Chiudi Inspector' }));
    expect(screen.getByText('Scartare le modifiche non salvate?')).toBeTruthy();
    expect(title).toHaveProperty('value', 'Conferenza nuova');
    expect(onClose).not.toHaveBeenCalled();
    fireEvent.click(
      screen.getByRole('button', { name: 'Continua a modificare' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    expect(screen.getByText('Scartare le modifiche non salvate?')).toBeTruthy();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByText('Scartare le modifiche non salvate?')).toBeNull();
    expect(title).toHaveProperty('value', 'Conferenza nuova');
    fireEvent.click(screen.getByRole('button', { name: 'Chiudi Inspector' }));
    fireEvent.click(screen.getByRole('button', { name: 'Scarta modifiche' }));
    await waitFor(() =>
      expect(
        screen.queryByRole('textbox', { name: 'Titolo Event' }),
      ).toBeNull(),
    );
    expect(confirm).not.toHaveBeenCalled();
    expect(onClose).not.toHaveBeenCalled();
  });

  it('closes an unchanged Event editor without a mutation or error', async () => {
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
      agendaParts: [],
    });
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    await screen.findByRole('textbox', { name: 'Titolo Event' });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(
        screen.queryByRole('textbox', { name: 'Titolo Event' }),
      ).toBeNull(),
    );
    expect(reviseProfile).not.toHaveBeenCalled();
    expect(reviseAtomic).not.toHaveBeenCalled();
    expect(screen.queryByText('Nessuna modifica da salvare.')).toBeNull();
  });

  it('skips controls hidden by the Event editor when cycling keyboard focus', async () => {
    loadProfile.mockResolvedValue({
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 1,
    });
    render(
      <EventDetailDialog
        detail={{
          title: 'Conferenza',
          startMinute: 540,
          endMinute: 630,
          groupLabel: 'Lavoro',
          ownerKind: 'event',
          eventRef,
          eventPlacement: placement,
        }}
        opener={null}
        onClose={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    const title = await screen.findByRole('textbox', { name: 'Titolo Event' });
    const toolbar = document.querySelector<HTMLElement>(
      '.timeline-event-modal__owner-actions',
    );
    if (toolbar) toolbar.style.display = 'none';
    const close = screen.getByRole('button', { name: 'Chiudi Inspector' });
    close.focus();
    fireEvent.keyDown(document, { key: 'Tab' });
    expect(document.activeElement).toBe(title);
  });

  it('keeps the Event edit draft open on a canonical stale CAS conflict', async () => {
    const current = {
      eventRef,
      title: 'Conferenza',
      description: null,
      location: null,
      colorCode: null,
      profileRevision: 2,
      agendaRevision: 0,
      agendaParts: [],
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    };
    loadProfile.mockResolvedValue(current);
    reviseProfile.mockRejectedValue(
      new Error('Il profilo Event è cambiato: ricarica e riprova.'),
    );
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    const title = await screen.findByRole('textbox', { name: 'Titolo Event' });
    fireEvent.change(title, { target: { value: 'Nuovo titolo' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'è cambiato',
    );
    expect(
      screen.getByRole('textbox', { name: 'Titolo Event' }),
    ).toHaveProperty('value', 'Nuovo titolo');
  });

  it('rejects flattening a recurring Event source into one standalone Event', async () => {
    loadEvent.mockResolvedValue({
      eventRef,
      title: 'Serie Eventi',
      agendaRevision: 1,
      agendaParts: ['Introduzione'],
      lifeAreaRef: null,
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    });
    listExpectedParticipation.mockResolvedValue([]);
    listPersonReferents.mockResolvedValue([]);
    isRecurring.mockResolvedValue(true);
    const onDuplicate = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'sorgente ricorrente',
    );
    expect(isRecurring).toHaveBeenCalledWith(eventRef);
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('requires a fresh one-off Event preview and confirmation, while cancellation keeps the Event', async () => {
    const preview = {
      requestedRef: eventRef,
      scope: 'event_once',
      fingerprint: '3'.repeat(64),
    };
    previewHardDeletion.mockResolvedValue(preview);
    confirmHardDeletion.mockResolvedValue(undefined);
    const onDeleted = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDeleted={onDeleted}
        onDuplicate={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Elimina Event' }));
    await screen.findByRole('button', {
      name: 'Conferma eliminazione definitiva',
    });
    expect(previewHardDeletion).toHaveBeenCalledWith(eventRef, 'event_once');
    expect(eventOccurrences).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    expect(confirmHardDeletion).not.toHaveBeenCalled();
    expect(onDeleted).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Elimina Event' }));
    await screen.findByRole('button', {
      name: 'Conferma eliminazione definitiva',
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma eliminazione definitiva' }),
    );
    await waitFor(() =>
      expect(confirmHardDeletion).toHaveBeenCalledWith(preview),
    );
    expect(onDeleted).toHaveBeenCalledOnce();
  });

  it.each([
    ['Solo questa istanza', 'event_once'],
    ['Tutta la serie', 'event_series'],
  ] as const)(
    'offers %s when deleting the physical first Event of a recurring series',
    async (label, scope) => {
      const seededSource = '0199a111-1111-7111-8111-333333333333';
      const onlyThis = {
        requestedRef: eventRef,
        scope: 'event_once' as const,
        fingerprint: 'a'.repeat(64),
      };
      const series = {
        requestedRef: eventRef,
        scope: 'event_series' as const,
        fingerprint: 'b'.repeat(64),
      };
      eventSeed.mockResolvedValue(seededSource);
      previewHardDeletion.mockImplementation((_ref: string, kind: string) =>
        Promise.resolve(kind === 'event_once' ? onlyThis : series),
      );
      confirmHardDeletion.mockResolvedValue(undefined);
      const onDeleted = vi.fn();
      render(
        <EventInspectorActions
          eventRef={eventRef}
          placement={placement}
          onDeleted={onDeleted}
          onDuplicate={vi.fn()}
        />,
      );

      fireEvent.click(screen.getByRole('button', { name: 'Elimina Event' }));
      await screen.findByRole('button', { name: 'Solo questa istanza' });
      expect(screen.getByRole('button', { name: 'Tutta la serie' })).toBeTruthy();
      expect(previewHardDeletion).toHaveBeenCalledWith(eventRef, 'event_once');
      expect(previewHardDeletion).toHaveBeenCalledWith(eventRef, 'event_series');
      expect(eventOccurrences).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole('button', { name: label }));
      await waitFor(() =>
        expect(confirmHardDeletion).toHaveBeenCalledWith(
          scope === 'event_once' ? onlyThis : series,
        ),
      );
      expect(onDeleted).toHaveBeenCalledOnce();
    },
  );

  it('does not offer recurring Event instance deletion until an explicit Occurrence is selected', async () => {
    const occurrenceRef = '0199a222-2222-7222-8222-222222222222';
    const series = {
      requestedRef: eventRef,
      scope: 'event_series',
      fingerprint: '4'.repeat(64),
    };
    const instance = {
      requestedRef: occurrenceRef,
      scope: 'event_instance',
      fingerprint: '5'.repeat(64),
    };
    isRecurring.mockResolvedValue(true);
    previewHardDeletion.mockImplementation((ref: string, scope: string) =>
      Promise.resolve(
        ref === occurrenceRef && scope === 'event_instance' ? instance : series,
      ),
    );
    eventOccurrences.mockResolvedValue([
      { occurrenceRef, scheduleRef: null, displayLabel: '16 ottobre, 10:00' },
    ]);
    confirmHardDeletion.mockResolvedValue(undefined);
    const onDeleted = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDeleted={onDeleted}
        onDuplicate={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Elimina Event' }));
    await screen.findByRole('button', { name: 'Tutta la serie' });
    expect(
      screen.queryByRole('button', { name: 'Solo questa istanza' }),
    ).toBeNull();
    expect(confirmHardDeletion).not.toHaveBeenCalled();
    fireEvent.change(
      screen.getByRole('combobox', { name: 'Istanza Event da eliminare' }),
      { target: { value: occurrenceRef } },
    );
    await screen.findByRole('button', { name: 'Solo questa istanza' });
    expect(previewHardDeletion).toHaveBeenCalledWith(
      occurrenceRef,
      'event_instance',
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Solo questa istanza' }),
    );
    await waitFor(() =>
      expect(confirmHardDeletion).toHaveBeenCalledWith(instance),
    );
    expect(confirmHardDeletion).not.toHaveBeenCalledWith(series);
    expect(onDeleted).toHaveBeenCalledOnce();
  });

  it('edits following Activity instances with the shared date, Session and Objective controls', async () => {
    const occurrenceRef = '0199a555-5555-7555-8555-555555555555';
    loadSeries.mockResolvedValue({
      sourceRef: eventRef,
      owner: 'routine',
      selectedDate: '2026-10-23',
      editRevision: 2,
      recurrenceStateRef: '0199a666-6666-7666-8666-666666666666',
      title: 'Allenamento',
      description: null,
      location: null,
      colorCode: null,
      recurrence: {
        pattern_code: 'daily',
        interval_count: 1,
        range_kind: 'open',
        wall_times: ['17:15:00'],
        zone_id: 'Europe/Rome',
      },
      structure: {
        duration_minutes: 120,
        reminder_lead_minutes: null,
        activity_template: {
          root_window: { start_offset_minutes: 0, duration_minutes: 120 },
          activity_intervals: [
            { start_offset_minutes: 0, duration_minutes: 30 },
            { start_offset_minutes: 60, duration_minutes: 60 },
          ],
          planned_slices: [{ name: 'Stretching', time_enabled: false }],
          session_capture_mode: 'live',
          reality_mode: 'manual',
          objectives: [
            {
              label: 'Completato',
              result_kind: 'boolean',
              presentation_order: 0,
            },
          ],
        },
      },
    });
    reviewSeries.mockResolvedValue({
      fingerprint: 'a'.repeat(64),
      targetRefs: ['0199a555-5555-7555-8555-555555555555'],
      newExpectedCount: 0,
      protected: [
        {
          occurrenceRef: '0199a666-6666-7666-8666-666666666666',
          expectedAt: '2027-01-03T16:15:00Z',
          reason: 'local_change',
        },
      ],
    });
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(Response.json([])));
    render(
      <RecurringSeriesEditor
        occurrenceRef={occurrenceRef}
        scope="this_and_following"
        owner="routine"
        onSaved={vi.fn()}
        onCancel={vi.fn()}
      />,
    );
    expect(await screen.findByRole('textbox', { name: 'Titolo' })).toBeTruthy();
    expect(
      screen.getByRole('textbox', { name: 'Nome Sessione 1' }).closest('input')
        ?.value,
    ).toBe('Stretching');
    const sessionRow = screen
      .getByRole('textbox', { name: 'Nome Sessione 1' })
      .closest('.temporal-create-tree-item');
    expect(sessionRow).not.toBeNull();
    const editor = screen
      .getByRole('textbox', { name: 'Titolo' })
      .closest('.timeline-activity-editor') as HTMLElement;
    const form = editor.querySelector('.timeline-activity-editor__body')!;
    const formSections = [
      '.timeline-activity-editor__title-row',
      '.timeline-activity-editor__sessions',
      '[aria-label="Orario della serie"]',
      '.timeline-activity-editor__intervals',
      '.timeline-recurring-series-editor__repeat-panel',
      '[aria-label="Life Area"]',
      '[aria-label="Svolgimento e obiettivi"]',
      '.timeline-activity-editor__location',
      '.timeline-activity-editor__description',
      ':scope > .timeline-recurring-series-editor__advanced',
    ].map((selector) => form.querySelector(selector));
    expect(formSections.every(Boolean)).toBe(true);
    for (let index = 1; index < formSections.length; index += 1) {
      expect(
        formSections[index - 1]?.compareDocumentPosition(formSections[index]!),
      ).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    }
    expect(
      form.querySelector('.timeline-recurring-series-editor__scope'),
    ).toBeNull();
    expect(
      screen
        .getByRole('region', { name: 'Sessioni pianificate' })
        .querySelector('.temporal-create-activity-tree__root-sessions')
        ?.contains(sessionRow),
    ).toBe(true);
    expect(form.querySelector('.temporal-create-objective')).not.toBeNull();
    expect(
      screen
        .getByRole('region', { name: 'Sessioni pianificate' })
        .compareDocumentPosition(
          screen.getByRole('region', { name: 'Orario della serie' }),
        ) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      screen
        .getByRole('region', { name: 'Life Area' })
        .compareDocumentPosition(
          screen.getByRole('region', { name: 'Svolgimento e obiettivi' }),
        ) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      within(sessionRow as HTMLElement).queryByRole('checkbox'),
    ).toBeNull();
    fireEvent.click(screen.getByText('Opzioni avanzate della serie'));
    const sessionClock = screen.getByRole('checkbox', {
      name: 'Con orario Sessione 1',
    });
    const sessionOptions = sessionClock.closest(
      '.timeline-recurring-series-editor__session-options',
    ) as HTMLElement;
    fireEvent.click(sessionClock);
    expect(
      within(sessionOptions).getByRole('group', { name: 'Inizio' }),
    ).toBeTruthy();
    fireEvent.click(sessionClock);
    expect(
      within(sessionOptions).queryByRole('group', { name: 'Inizio' }),
    ).toBeNull();
    expect(
      screen.getAllByRole('button', { name: /^Data inizio:/ }),
    ).toHaveLength(2);
    expect(
      screen.getByRole('textbox', { name: 'Nome obiettivo' }).closest('input')
        ?.value,
    ).toBe('Completato');
    fireEvent.click(
      screen.getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Verifica modifiche' }));
    await waitFor(() => expect(reviewSeries).toHaveBeenCalled());
    const intent: unknown = reviewSeries.mock.lastCall?.[0];
    expect(intent).toMatchObject({
      structure: {
        activity_template: {
          activity_intervals: [
            { start_offset_minutes: 0, duration_minutes: 30 },
            { start_offset_minutes: 60, duration_minutes: 60 },
            { start_offset_minutes: 135, duration_minutes: 30 },
          ],
          root_window: { start_offset_minutes: 0, duration_minutes: 165 },
        },
      },
    });
    const confirmation = await screen.findByRole('dialog', {
      name: 'Controlla prima di salvare',
    });
    expect(confirmation.textContent).toContain('Da questa istanza');
    expect(confirmation.textContent).not.toContain(
      'istanza pianificata sarà sostituita',
    );
    expect(confirmation.textContent).toContain(
      'Modificata singolarmente: resta invariata',
    );
    expect(confirmation.textContent).not.toContain('local_change');
    expect(screen.queryByRole('group', { name: 'Tipo' })).toBeNull();
    fireEvent.click(
      within(confirmation).getByRole('button', { name: 'Torna alla modifica' }),
    );
    expect(acceptSeries).not.toHaveBeenCalled();
    expect(
      screen.queryByRole('dialog', { name: 'Controlla prima di salvare' }),
    ).toBeNull();
  });
});
