// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
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

vi.mock('../../../temporal/remote-event-recurrence-guard', () => ({
  createRemoteEventRecurrenceGuard: () => ({ isRecurring }),
}));
vi.mock('../../../temporal/remote-event-profile-data-source', () => ({
  createRemoteEventProfileDataSource: () => ({ load: loadProfile, revise: reviseProfile }),
}));
vi.mock('../../../temporal/remote-event-life-area-settings', () => ({
  createRemoteEventLifeAreaSettings: () => ({ load: loadArea, assign: assignArea }),
}));
vi.mock('../../../temporal/remote-event-agenda-data-source', () => ({
  createRemoteTemporalEventAgendaDataSource: () => ({ loadEvent }),
}));
vi.mock('../../../temporal/remote-responsibility-data-source', () => ({
  createRemoteTemporalResponsibilityDataSource: () => ({
    listExpectedParticipation, listPersonReferents,
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
  vi.clearAllMocks();
  isRecurring.mockResolvedValue(false);
});

describe('Event Inspector duplication', () => {
  it('loads owner-scoped Agenda and Participation and opens a new draft without copying truth', async () => {
    loadEvent.mockResolvedValue({
      eventRef, title: 'Conferenza', agendaRevision: 3,
      agendaParts: ['Presentazione', 'Domande'],
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
      lifeAreaRef: '0199a222-2222-7222-8222-222222222222',
    });
    listExpectedParticipation.mockResolvedValue([{
      eventRef, participantPersonRef: '0199a333-3333-7333-8333-333333333333',
      participantIsSelf: false, requirementCode: 'required',
    }]);
    listPersonReferents.mockResolvedValue([{
      personRef: '0199a333-3333-7333-8333-333333333333',
      displayLabel: 'Collaboratore', revision: 1, replayed: false,
    }]);
    const onDuplicate = vi.fn();
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    await waitFor(() => expect(onDuplicate).toHaveBeenCalledOnce());
    expect(loadEvent).toHaveBeenCalledWith(eventRef);
    expect(listExpectedParticipation).toHaveBeenCalledWith(eventRef);
    expect(onDuplicate.mock.calls[0]?.[0]).toMatchObject({
      fields: {
        kind: 'event', title: 'Conferenza',
        event: { agendaParts: ['Presentazione', 'Domande'] },
        durationMinutes: 90,
      },
      advanced: {
        eventParticipants: [{ displayLabel: 'Collaboratore', requirementCode: 'required' }],
      },
    });
  });

  it('updates the current Event Life Area without creating another Event', async () => {
    const area = {
      currentRef: '0199a222-2222-7222-8222-222222222222',
      currentRevision: 4,
      options: [{ ref: '0199a222-2222-7222-8222-222222222222', name: 'Lavoro' }],
    };
    loadArea.mockResolvedValue(area);
    assignArea.mockResolvedValue({ ...area, currentRef: null, currentRevision: 5 });
    const onDuplicate = vi.fn();
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: 'Modifica Life Area' }));
    const select = await screen.findByRole('combobox', { name: 'Life Area Event' });
    fireEvent.change(select, { target: { value: '' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva Life Area Event' }));
    await waitFor(() => expect(assignArea).toHaveBeenCalledWith(
      eventRef, area, null, expect.any(String),
    ));
    expect(await screen.findByRole('status')).toHaveProperty(
      'textContent', 'Life Area Event aggiornata.',
    );
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('does not open an incomplete duplicate when an expected participant cannot be resolved', async () => {
    loadEvent.mockResolvedValue({
      eventRef, title: 'Conferenza', agendaRevision: 0,
      agendaParts: [], createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
      lifeAreaRef: null,
    });
    listExpectedParticipation.mockResolvedValue([{
      eventRef, participantPersonRef: '0199a333-3333-7333-8333-333333333333',
      participantIsSelf: false, requirementCode: 'required',
    }]);
    listPersonReferents.mockResolvedValue([]);
    const onDuplicate = vi.fn();
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('un partecipante non è più disponibile');
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('edits current Event metadata with canonical CAS and leaves the existing identity intact', async () => {
    const current = {
      eventRef, title: 'Conferenza', description: 'Prima', location: 'Roma',
      colorCode: '#ABCDEF', profileRevision: 2, agendaRevision: 1,
      agendaParts: ['Parte 1'], createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    };
    loadProfile.mockResolvedValue(current);
    reviseProfile.mockResolvedValue({ ...current, title: 'Incontro', profileRevision: 3 });
    const onDuplicate = vi.fn();
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    fireEvent.change(await screen.findByRole('textbox', { name: 'Titolo Event' }), {
      target: { value: 'Incontro' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva metadati Event' }));
    await waitFor(() => expect(reviseProfile).toHaveBeenCalledWith(
      eventRef,
      current,
      { title: 'Incontro', description: 'Prima', location: 'Roma', colorCode: '#ABCDEF' },
      expect.any(String),
    ));
    expect(await screen.findByText('Metadati Event aggiornati.')).toBeTruthy();
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('keeps the Event edit draft open on a canonical stale CAS conflict', async () => {
    const current = {
      eventRef, title: 'Conferenza', description: null, location: null,
      colorCode: null, profileRevision: 2, agendaRevision: 0,
      agendaParts: [], createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    };
    loadProfile.mockResolvedValue(current);
    reviseProfile.mockRejectedValue(new Error('Il profilo Event è cambiato: ricarica e riprova.'));
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /^Modifica$/ }));
    const title = await screen.findByRole('textbox', { name: 'Titolo Event' });
    fireEvent.change(title, { target: { value: 'Nuovo titolo' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva metadati Event' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('è cambiato');
    expect(screen.getByRole('textbox', { name: 'Titolo Event' }))
      .toHaveProperty('value', 'Nuovo titolo');
  });


  it('rejects flattening a recurring Event source into one standalone Event', async () => {
    loadEvent.mockResolvedValue({
      eventRef, title: 'Serie Eventi', agendaRevision: 1,
      agendaParts: ['Introduzione'], lifeAreaRef: null,
      createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    });
    listExpectedParticipation.mockResolvedValue([]);
    listPersonReferents.mockResolvedValue([]);
    isRecurring.mockResolvedValue(true);
    const onDuplicate = vi.fn();
    render(<EventInspectorActions eventRef={eventRef} placement={placement}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('sorgente ricorrente');
    expect(isRecurring).toHaveBeenCalledWith(eventRef);
    expect(onDuplicate).not.toHaveBeenCalled();
  });

});
