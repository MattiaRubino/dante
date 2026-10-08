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
const previewReplan = vi.fn();
const applyReplan = vi.fn();
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({ get, revise, retire }),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: loadSettings,
    saveCore,
    previewReplan,
    applyReplan,
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

  it('requires an explicit preview before applying a planning change', async () => {
    const settings = { ...currentSettings, schedules: [
      { scheduleRef: 'envelope', role: 'envelope', name: null, order: 0,
        placementStateRef: 'state-0', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00', zoneId: 'Europe/Rome' },
      { scheduleRef: 'interval', role: 'interval', name: null, order: 1,
        placementStateRef: 'state-1', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00', zoneId: 'Europe/Rome' },
    ] };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([{ scheduleRef: 'interval', role: 'interval',
      previousStart: '2026-10-09T09:00:00', previousEnd: '2026-10-09T10:00:00',
      proposedStart: '2026-10-09T10:00:00', proposedEnd: '2026-10-09T11:00:00' }]);
    applyReplan.mockResolvedValueOnce(settings);
    const onSaved = vi.fn();
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={onSaved} onCancel={() => undefined} />);
    fireEvent.change((await screen.findAllByLabelText('Inizio'))[0]!,
      { target: { value: '2026-10-09T10:00' } });
    fireEvent.change(screen.getAllByLabelText('Fine')[0]!,
      { target: { value: '2026-10-09T11:00' } });
    expect(screen.getByRole('button', { name: 'Salva modifiche' })).toHaveProperty('disabled', true);
    fireEvent.click(screen.getByRole('button', { name: 'Verifica spostamento' }));
    await waitFor(() => expect(previewReplan).toHaveBeenCalledOnce());
    expect(screen.getByText('Modifiche proposte')).toBeTruthy();
    expect(applyReplan).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Applica programmazione' }));
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
    expect(applyReplan.mock.calls[0]?.[3]).toBe(previewReplan.mock.calls[0]?.[3]);
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('previews additions and removals of planned Sessions before applying', async () => {
    const settings = { ...currentSettings, schedules: [
      { scheduleRef: 'envelope', role: 'envelope', name: null, order: 0,
        placementStateRef: 'state-0', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00', zoneId: 'Europe/Rome' },
      { scheduleRef: 'interval', role: 'interval', name: null, order: 1,
        placementStateRef: 'state-1', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00', zoneId: 'Europe/Rome' },
      { scheduleRef: 'planned', role: 'planned', name: 'Prima', order: 1,
        placementStateRef: 'state-2', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00', zoneId: 'Europe/Rome' },
    ] };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([{ scheduleRef: 'planned', clientRef: null,
      role: 'planned_removed', previousStart: '2026-10-09T09:00:00',
      previousEnd: '2026-10-09T10:00:00', proposedStart: null, proposedEnd: null }]);
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Rimuovi sessione' }));
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi sessione pianificata' }));
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome sessione' }),
      { target: { value: 'Seconda' } });
    fireEvent.change(screen.getAllByLabelText('Inizio').at(-1)!,
      { target: { value: '2026-10-09T10:00' } });
    fireEvent.change(screen.getAllByLabelText('Fine').at(-1)!,
      { target: { value: '2026-10-09T11:00' } });
    fireEvent.click(screen.getByRole('button', { name: 'Verifica spostamento' }));
    await waitFor(() => expect(previewReplan).toHaveBeenCalledWith(ref, settings,
      expect.objectContaining({ removedPlanned: ['planned'], newPlanned: [
        expect.objectContaining({ name: 'Seconda', start: '2026-10-09T10:00',
          end: '2026-10-09T11:00' }),
      ] }), expect.any(String)));
    expect(applyReplan).not.toHaveBeenCalled();
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
