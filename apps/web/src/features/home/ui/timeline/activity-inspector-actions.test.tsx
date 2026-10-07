// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityInspectorActions } from './activity-inspector-actions';
import { ActivityEditPanel } from './activity-edit-panel';

const get = vi.fn();
const revise = vi.fn();
const retire = vi.fn();
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({ get, revise, retire }),
}));

const ref = '0199a111-1111-7111-8111-111111111111';
const profile = {
  activityRef: ref,
  title: 'Prima',
  description: 'Nota',
  location: 'Casa',
  colorCode: '#EA5C12',
  revision: 0,
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('Activity Inspector', () => {
  it('opens the separate editor with the persisted profile', async () => {
    get.mockResolvedValue(profile);
    const onEdit = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={onEdit}
        onDeleted={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    await waitFor(() => expect(onEdit).toHaveBeenCalledWith(profile));
    expect(screen.queryByRole('textbox', { name: 'Titolo' })).toBeNull();
  });

  it('saves changes in the editor and returns to the Inspector', async () => {
    revise.mockResolvedValue({ ...profile, title: 'Dopo', revision: 1 });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const title = await screen.findByRole('textbox', { name: 'Titolo' });
    fireEvent.change(title, { target: { value: 'Dopo' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(revise).toHaveBeenCalledWith(
        profile,
        expect.objectContaining({ title: 'Dopo', description: 'Nota' }),
      ),
    );
    await waitFor(() =>
      expect(onSaved).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'Dopo', revision: 1 }),
      ),
    );
  });

  it('requires confirmation before retirement', async () => {
    retire.mockResolvedValue(undefined);
    const onDeleted = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={onDeleted}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Elimina' }));
    expect(retire).not.toHaveBeenCalled();
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma eliminazione' }),
    );
    await waitFor(() => expect(retire).toHaveBeenCalledWith(ref));
    expect(onDeleted).toHaveBeenCalledOnce();
  });
});
