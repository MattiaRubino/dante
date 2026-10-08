// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { EventInspectorActions } from './event-inspector-actions';

const loadEvent = vi.fn();
const listExpectedParticipation = vi.fn();
const listPersonReferents = vi.fn();

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
});
