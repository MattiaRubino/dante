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

const get = vi.fn();
const revise = vi.fn();
const retire = vi.fn();
const loadSettings = vi.fn();
const setCapture = vi.fn();
const setReality = vi.fn();
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({ get, revise, retire }),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: loadSettings,
    setCapture,
    setReality,
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
      />,
    );
    expect(await screen.findByText('Nota')).toBeTruthy();
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

  it('saves policy changes with their current state and retries after a partial failure', async () => {
    setCapture.mockResolvedValue({ mode: 'live', stateRef: 'capture-1' });
    setReality
      .mockRejectedValueOnce(new Error('Connessione interrotta'))
      .mockResolvedValueOnce({ mode: 'review_on_end', stateRef: 'reality-1' });
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
      'Connessione interrotta',
    );
    expect(setCapture).toHaveBeenCalledWith(
      ref,
      currentSettings.capture,
      'live',
      expect.any(String),
    );
    expect(setReality).toHaveBeenCalledWith(
      ref,
      currentSettings.reality,
      'review_on_end',
      expect.any(String),
    );
    expect(onSaved).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(setCapture).toHaveBeenCalledTimes(1);
    expect(setReality).toHaveBeenCalledTimes(2);
    expect(setReality.mock.calls[1]?.[3]).toBe(setReality.mock.calls[0]?.[3]);
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
