// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TimelineDraftVault } from './timeline-draft-vault';
import { createTemporalCreateFields } from '../../../temporal-create/model/temporal-create-session';

const sources = vi.hoisted(() => ({
  list: vi.fn(),
  remove: vi.fn(),
}));
vi.mock('../../../temporal-create/application/remote-draft-vault', () => ({
  createRemoteDraftVault: () => ({
    list: sources.list,
    remove: sources.remove,
  }),
  DRAFT_VAULT_UPDATED: 'dante:draft-vault-updated',
}));

const draft = {
  draftRef: 'draft-1',
  title: 'Allenamento',
  subjectKind: 'activity' as const,
  payload: {
    version: 1 as const,
    fields: createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-11-23',
      startTime: '10:00',
      durationMinutes: 30,
    }),
    advanced: { objectives: [] },
    surface: 'full' as const,
  },
  revision: 1,
  createdAt: '2026-10-09T20:00:00Z',
  updatedAt: '2026-10-09T20:00:00Z',
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('Timeline Draft Vault', () => {
  it('keeps a saved draft inert and offers resume and duplicate explicitly', async () => {
    sources.list.mockResolvedValueOnce([draft]);
    const onOpen = vi.fn();
    render(
      <>
        <div className="dante-timeline-actions" />
        <TimelineDraftVault onOpen={onOpen} />
      </>,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Apri Bozze' }));
    const trigger = screen.getByRole('button', { name: 'Apri Bozze' });
    const panel = screen.getByRole('complementary', { name: 'Bozze' });
    expect(panel.parentElement).toBe(trigger.parentElement);
    expect(trigger.getAttribute('data-timeline-tooltip')).toBe('Bozze');
    expect(await screen.findByText('Allenamento')).toBeTruthy();
    expect(panel.textContent).toContain('10:00–10:30 · 23 nov');
    expect(panel.querySelector('[data-temporal-kind-marker="activity"]')).toBeTruthy();
    expect(panel.querySelector('.timeline-event-card__heading')).toBeTruthy();
    expect(panel.querySelector('.timeline-event-card__time')).toBeTruthy();
    expect(panel.textContent).not.toContain('Non attiva');
    expect(screen.queryByRole('button', { name: 'Play' })).toBeNull();
    expect(
      screen.queryByRole('button', { name: /elementi già creati/i }),
    ).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect(onOpen).toHaveBeenCalledWith(draft, true);
    fireEvent.click(screen.getByRole('button', { name: 'Apri Bozze' }));
    fireEvent.click(screen.getByRole('button', { name: 'Riprendi' }));
    expect(onOpen).toHaveBeenCalledWith(draft, false);
    expect(sources.remove).not.toHaveBeenCalled();
  });

  it('filters saved activity and all-day event cards as the search changes', async () => {
    const event = {
      ...draft,
      draftRef: 'draft-2',
      title: 'Conferenza',
      subjectKind: 'event' as const,
      payload: {
        ...draft.payload,
        fields: createTemporalCreateFields({
          title: 'Conferenza',
          kind: 'event',
          date: '2026-11-24',
          timeSemantics: 'all-day',
        }),
      },
    };
    const overnight = {
      ...draft,
      draftRef: 'draft-3',
      title: 'Turno serale',
      payload: {
        ...draft.payload,
        fields: createTemporalCreateFields({
          title: 'Turno serale',
          kind: 'activity',
          date: '2026-11-23',
          startTime: '23:30',
          durationMinutes: 120,
        }),
      },
    };
    sources.list.mockResolvedValueOnce([draft, event, overnight]);
    render(
      <>
        <div className="dante-timeline-actions" />
        <TimelineDraftVault onOpen={() => undefined} />
      </>,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Apri Bozze' }));
    const panel = screen.getByRole('complementary', { name: 'Bozze' });
    expect(within(panel).getByRole('heading', { name: 'Bozze' })).toBeTruthy();
    expect(panel.textContent).not.toContain('DANTE · Cassaforte');
    expect(panel.textContent).toContain('Tutto il giorno · 24 nov');
    expect(panel.textContent).toContain('23:30–01:30 · 23 nov–24 nov');
    expect(panel.querySelector('[data-temporal-kind-marker="event"]')).toBeTruthy();

    fireEvent.change(within(panel).getByRole('searchbox', { name: 'Cerca Bozze' }), {
      target: { value: 'conf' },
    });
    expect(within(panel).getAllByRole('article')).toHaveLength(1);
    expect(within(panel).queryByText('Allenamento')).toBeNull();
    expect(within(panel).getByText('Conferenza')).toBeTruthy();
  });

  it('requires confirmation before deleting the inert vault row', async () => {
    sources.list.mockResolvedValueOnce([draft]);
    sources.remove.mockResolvedValueOnce(undefined);
    render(
      <>
        <div className="dante-timeline-actions" />
        <TimelineDraftVault onOpen={() => undefined} />
      </>,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Apri Bozze' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Elimina' }));
    expect(sources.remove).not.toHaveBeenCalled();
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma eliminazione' }),
    );
    await waitFor(() => expect(sources.remove).toHaveBeenCalledWith(draft));
  });
});
