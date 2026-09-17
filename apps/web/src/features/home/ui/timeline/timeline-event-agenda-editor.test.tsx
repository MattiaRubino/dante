import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type { TemporalEventAgendaDataSource } from '../../../temporal/event-data-source';
import { createDeterministicTemporalIdFactory } from '../../../temporal/model';
import { TemporalEventAgendaRemoteError } from '../../../temporal/remote-event-agenda-data-source';
import { TimelineEventAgendaEditor } from './timeline-event-agenda-editor';

const EVENT_REF = '0199a8c0-7e71-7bc0-8ad0-a2f403f5617d';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function record(revision: number, agendaParts: readonly string[]) {
  return Object.freeze({
    eventRef: EVENT_REF,
    title: 'Riunione B03-D',
    agendaRevision: revision,
    agendaParts: Object.freeze([...agendaParts]),
    createdAt: Temporal.Instant.from('2026-09-17T18:00:00Z'),
  });
}

describe('B03-D canonical Event Agenda editor', () => {
  it('reads backend truth and persists add, edit, reorder and remove through CAS', async () => {
    let serverRevision = 0;
    let serverParts: readonly string[] = ['Apertura', 'Decisione'];
    const loadEvent = vi.fn<TemporalEventAgendaDataSource['loadEvent']>(() =>
      Promise.resolve(record(serverRevision, serverParts)),
    );
    const replaceAgenda = vi.fn<TemporalEventAgendaDataSource['replaceAgenda']>(
      (request) => {
        expect(request.eventRef).toBe(EVENT_REF);
        expect(request.expectedRevision).toBe(serverRevision);
        serverRevision += 1;
        serverParts = [...request.agendaParts];
        return Promise.resolve({
          eventRef: EVENT_REF,
          agendaRevision: serverRevision,
          agendaParts: serverParts,
          replayed: false,
        });
      },
    );

    render(
      <TimelineEventAgendaEditor
        eventRef={EVENT_REF}
        dataSource={{ loadEvent, replaceAgenda }}
        ids={createDeterministicTemporalIdFactory('b03-d-agenda')}
      />,
    );

    expect(await screen.findByRole('button', { name: 'Apertura' })).toBeTruthy();
    expect(loadEvent).toHaveBeenCalledTimes(1);

    const newItem = screen.getByRole('textbox', { name: 'Nuova voce agenda' });
    fireEvent.change(newItem, { target: { value: 'Chiusura' } });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi voce' }));
    await waitFor(() => expect(replaceAgenda).toHaveBeenCalledTimes(1));
    expect(replaceAgenda.mock.calls[0]?.[0]).toMatchObject({
      operationId: 'b03-d-agenda:operation:1',
      expectedRevision: 0,
      agendaParts: ['Apertura', 'Decisione', 'Chiusura'],
    });
    expect(await screen.findByRole('button', { name: 'Chiusura' })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Decisione' }));
    const editor = screen.getByRole('textbox', { name: 'Voce agenda 2' });
    fireEvent.change(editor, { target: { value: 'Decisione finale' } });
    fireEvent.keyDown(editor, { key: 'Enter' });
    await waitFor(() => expect(replaceAgenda).toHaveBeenCalledTimes(2));
    expect(replaceAgenda.mock.calls[1]?.[0]).toMatchObject({
      operationId: 'b03-d-agenda:operation:2',
      expectedRevision: 1,
      agendaParts: ['Apertura', 'Decisione finale', 'Chiusura'],
    });

    fireEvent.click(screen.getByRole('button', { name: 'Sposta voce 3 su' }));
    await waitFor(() => expect(replaceAgenda).toHaveBeenCalledTimes(3));
    expect(replaceAgenda.mock.calls[2]?.[0]).toMatchObject({
      expectedRevision: 2,
      agendaParts: ['Apertura', 'Chiusura', 'Decisione finale'],
    });

    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi voce 2' }));
    await waitFor(() => expect(replaceAgenda).toHaveBeenCalledTimes(4));
    expect(replaceAgenda.mock.calls[3]?.[0]).toMatchObject({
      expectedRevision: 3,
      agendaParts: ['Apertura', 'Decisione finale'],
    });
    await waitFor(() =>
      expect(screen.queryByRole('button', { name: 'Chiusura' })).toBeNull(),
    );
  });

  it('fails closed on stale revision and reloads authoritative Agenda truth', async () => {
    const loadEvent = vi
      .fn<TemporalEventAgendaDataSource['loadEvent']>()
      .mockResolvedValueOnce(record(2, ['Locale']))
      .mockResolvedValueOnce(record(3, ['Remoto']));
    const replaceAgenda = vi.fn<TemporalEventAgendaDataSource['replaceAgenda']>(() =>
      Promise.reject(
        new TemporalEventAgendaRemoteError(
          'http',
          'conflict',
          409,
          'temporal.event.agenda_revision_conflict',
        ),
      ),
    );

    render(
      <TimelineEventAgendaEditor
        eventRef={EVENT_REF}
        dataSource={{ loadEvent, replaceAgenda }}
        ids={createDeterministicTemporalIdFactory('b03-d-conflict')}
      />,
    );

    expect(await screen.findByRole('button', { name: 'Locale' })).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi voce 1' }));

    await waitFor(() => expect(loadEvent).toHaveBeenCalledTimes(2));
    expect(await screen.findByRole('button', { name: 'Remoto' })).toBeTruthy();
    expect(
      screen.getByText(
        'L’Agenda è cambiata altrove. È stata ricaricata la versione corrente senza sovrascrivere nulla.',
      ),
    ).toBeTruthy();
  });
});
