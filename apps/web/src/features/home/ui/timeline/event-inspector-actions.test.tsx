// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { EventInspectorActions } from './event-inspector-actions';

const loadEvent = vi.fn();
const listExpectedParticipation = vi.fn();
const listPersonReferents = vi.fn();
const loadArea = vi.fn();
const loadProfile = vi.fn();
const reviseProfile = vi.fn();
const isRecurring = vi.fn().mockResolvedValue(false);
const assignArea = vi.fn();
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
  }),
}));
vi.mock('../../../temporal/remote-event-life-area-settings', () => ({
  createRemoteEventLifeAreaSettings: () => ({
    load: loadArea,
    assign: assignArea,
  }),
}));
vi.mock('../../../temporal/remote-event-agenda-data-source', () => ({
  createRemoteTemporalEventAgendaDataSource: () => ({ loadEvent }),
}));
vi.mock('../../../temporal/remote-responsibility-data-source', () => ({
  createRemoteTemporalResponsibilityDataSource: () => ({
    listExpectedParticipation,
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
});

describe('Event Inspector actions', () => {
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
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(new Response('[]', { status: 200 })),
    );
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
        eventParticipants: [
          { displayLabel: 'Collaboratore', requirementCode: 'required' },
        ],
      },
    });
  });

  it('updates the current Event Life Area without creating another Event', async () => {
    const area = {
      currentRef: '0199a222-2222-7222-8222-222222222222',
      currentRevision: 4,
      options: [
        { ref: '0199a222-2222-7222-8222-222222222222', name: 'Lavoro' },
      ],
    };
    loadArea.mockResolvedValue(area);
    assignArea.mockResolvedValue({
      ...area,
      currentRef: null,
      currentRevision: 5,
    });
    const onDuplicate = vi.fn();
    render(
      <EventInspectorActions
        eventRef={eventRef}
        placement={placement}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica Life Area' }));
    const select = await screen.findByRole('combobox', {
      name: 'Life Area Event',
    });
    fireEvent.change(select, { target: { value: '' } });
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva Life Area Event' }),
    );
    await waitFor(() =>
      expect(assignArea).toHaveBeenCalledWith(
        eventRef,
        area,
        null,
        expect.any(String),
      ),
    );
    expect(await screen.findByRole('status')).toHaveProperty(
      'textContent',
      'Life Area Event aggiornata.',
    );
    expect(onDuplicate).not.toHaveBeenCalled();
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
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva metadati Event' }),
    );
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
    expect(await screen.findByText('Metadati Event aggiornati.')).toBeTruthy();
    expect(onDuplicate).not.toHaveBeenCalled();
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
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva metadati Event' }),
    );
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
});
