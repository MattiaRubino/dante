// @vitest-environment jsdom
import { createRef } from 'react';
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityInspectorActions } from './activity-inspector-actions';
import { ActivityEditPanel } from './activity-edit-panel';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';

const get = vi.fn();
const revise = vi.fn();
const retire = vi.fn();
const loadSettings = vi.fn();
const saveCore = vi.fn();
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({ get, revise, retire }),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: loadSettings,
    saveCore,
  }),
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

const currentSettings = {
  capture: { mode: 'disabled', stateRef: null },
  reality: { mode: 'manual', stateRef: null },
  schedules: [],
  objectives: [],
  lifeAreaRef: null,
  placementProtected: false,
  reminderLeadMinutes: null,
  childGuardMode: 'none',
};

loadSettings.mockResolvedValue(currentSettings);

describe('Activity Inspector', () => {
  it('opens the separate editor with the persisted profile', async () => {
    get.mockResolvedValue(profile);
    const onEdit = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={onEdit}
        onDeleted={() => undefined}
        onDuplicate={() => undefined}
      />,
    );
    expect(await screen.findByText('Nota')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    await waitFor(() => expect(onEdit).toHaveBeenCalledWith(profile));
    expect(screen.queryByRole('textbox', { name: 'Titolo' })).toBeNull();
  });

  it('saves changes in the editor and returns to the Inspector', async () => {
    saveCore.mockResolvedValue({ profile: { ...profile, title: 'Dopo', revision: 1 },
      settings: currentSettings });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const title = await screen.findByRole('textbox', { name: 'Titolo' });
    fireEvent.change(title, { target: { value: 'Dopo' } });
    await screen.findByRole('combobox', { name: 'Registrazione sessioni' });
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() =>
      expect(saveCore).toHaveBeenCalledWith(
        profile,
        currentSettings,
        { profile: { title: 'Dopo', description: 'Nota', location: 'Casa',
          colorCode: '#EA5C12' } },
        expect.any(String),
      ),
    );
    await waitFor(() =>
      expect(onSaved).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'Dopo', revision: 1 }),
      ),
    );
  });

  it('retries one atomic policy change with the same operation ID', async () => {
    saveCore.mockRejectedValueOnce(new Error('Connessione interrotta'))
      .mockResolvedValueOnce({ profile, settings: currentSettings });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.change(
      await screen.findByRole('combobox', { name: 'Registrazione sessioni' }),
      {
        target: { value: 'live' },
      },
    );
    fireEvent.change(
      screen.getByRole('combobox', { name: 'Verifica dello svolgimento' }),
      {
        target: { value: 'review_on_end' },
      },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    expect(await screen.findByRole('alert')).toHaveProperty(
      'textContent',
      expect.stringContaining('Connessione interrotta'),
    );
    expect(saveCore).toHaveBeenCalledWith(profile, currentSettings,
      { capture: 'live', reality: 'review_on_end' }, expect.any(String));
    expect(onSaved).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(saveCore).toHaveBeenCalledTimes(2);
    expect(saveCore.mock.calls[1]?.[3]).toBe(saveCore.mock.calls[0]?.[3]);
    expect(revise).not.toHaveBeenCalled();
  });

  it('guards unsaved changes for external close requests', () => {
    const onCancel = vi.fn();
    const closeRequestRef = createRef<(() => void) | null>();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={closeRequestRef}
        onSaved={() => undefined}
        onCancel={onCancel}
      />,
    );
    fireEvent.change(screen.getByRole('textbox', { name: 'Titolo' }), {
      target: { value: 'Bozza' },
    });
    act(() => closeRequestRef.current?.());
    expect(screen.getByText('Scartare le modifiche non salvate?')).toBeTruthy();
    expect(onCancel).not.toHaveBeenCalled();
    fireEvent.click(
      screen.getByRole('button', { name: 'Continua a modificare' }),
    );
    expect(screen.getByRole('textbox', { name: 'Titolo' })).toHaveProperty(
      'value',
      'Bozza',
    );
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    fireEvent.click(screen.getByRole('button', { name: 'Scarta modifiche' }));
    expect(onCancel).toHaveBeenCalledOnce();
  });

  it('requires confirmation before retirement', async () => {
    retire.mockResolvedValue(undefined);
    const onDeleted = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={onDeleted}
        onDuplicate={() => undefined}
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

  it('opens a new Advanced Create draft from persisted Activity settings', async () => {
    get.mockResolvedValue(profile);
    const onDuplicate = vi.fn<(seed: ActivityDuplicateSeed) => void>();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    await waitFor(() => expect(onDuplicate).toHaveBeenCalledOnce());
    expect(onDuplicate.mock.calls[0]?.[0].fields).toMatchObject({
      kind: 'activity',
      title: 'Prima',
      notes: 'Nota',
    });
    expect(loadSettings).toHaveBeenCalledWith(ref);
  });
});
