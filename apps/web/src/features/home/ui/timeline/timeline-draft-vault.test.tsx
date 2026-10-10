// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TimelineDraftVault } from './timeline-draft-vault';

const sources = vi.hoisted(() => ({
  list: vi.fn(), remove: vi.fn(),
  legacy: vi.fn().mockResolvedValue([]),
}));
vi.mock('../../../temporal-create/application/remote-draft-vault', () => ({
  createRemoteDraftVault: () => ({ list: sources.list, remove: sources.remove }),
  DRAFT_VAULT_UPDATED: 'dante:draft-vault-updated',
}));
vi.mock('../../../temporal/remote-planning-tray-data-source', () => ({
  createRemoteTemporalPlanningTrayDataSource: () => ({ listItems: sources.legacy }),
}));

const draft = {
  draftRef: 'draft-1', title: 'Allenamento', subjectKind: 'activity' as const,
  payload: { version: 1 as const, fields: { title: 'Allenamento', kind: 'activity' },
    advanced: { objectives: [] }, surface: 'full' as const },
  revision: 1, createdAt: '2026-10-09T20:00:00Z',
  updatedAt: '2026-10-09T20:00:00Z',
};

afterEach(() => { cleanup(); vi.clearAllMocks(); });

describe('Timeline Draft Vault', () => {
  it('keeps a saved draft inert and offers resume and duplicate explicitly', async () => {
    sources.list.mockResolvedValueOnce([draft]);
    const onOpen = vi.fn();
    render(<><div className="dante-timeline-actions" />
      <TimelineDraftVault onOpen={onOpen} /></>);
    fireEvent.click(await screen.findByRole('button', { name: 'Apri Bozze' }));
    const trigger = screen.getByRole('button', { name: 'Apri Bozze' });
    const panel = screen.getByRole('complementary', { name: 'Bozze' });
    expect(panel.parentElement).toBe(trigger.parentElement);
    expect(trigger.getAttribute('data-timeline-tooltip')).toBe('Bozze');
    expect(await screen.findByText('Allenamento')).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Play' })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect(onOpen).toHaveBeenCalledWith(draft, true);
    fireEvent.click(screen.getByRole('button', { name: 'Apri Bozze' }));
    fireEvent.click(screen.getByRole('button', { name: 'Riprendi' }));
    expect(onOpen).toHaveBeenCalledWith(draft, false);
    expect(sources.remove).not.toHaveBeenCalled();
  });

  it('requires confirmation before deleting the inert vault row', async () => {
    sources.list.mockResolvedValueOnce([draft]);
    sources.remove.mockResolvedValueOnce(undefined);
    render(<><div className="dante-timeline-actions" />
      <TimelineDraftVault onOpen={() => undefined} /></>);
    fireEvent.click(await screen.findByRole('button', { name: 'Apri Bozze' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Elimina' }));
    expect(sources.remove).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Conferma eliminazione' }));
    await waitFor(() => expect(sources.remove).toHaveBeenCalledWith(draft));
  });
});

