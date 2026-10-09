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
const loadChildCount = vi.fn().mockResolvedValue(0);
const saveCore = vi.fn();
const previewReplan = vi.fn();
const applyReplan = vi.fn();
const loadLifeAreaChoice = vi.fn();
const assignLifeArea = vi.fn();
const revisePlannedName = vi.fn();
const setPlacementProtected = vi.fn();
const addObjective = vi.fn();
const refreshObjectives = vi.fn();
const getDefinition = vi.fn();
const getSeriesState = vi.fn().mockResolvedValue(null);
const reviseDefinition = vi.fn();
const correctResult = vi.fn();

vi.mock('../../../temporal/remote-reality-objective-data-source', () => ({
  createRemoteRealityObjectiveDataSource: () => ({
    getDefinition,
    getSeriesState,
    reviseDefinition,
    correctResult,
  }),
}));
const loadRecurringContext = vi.fn().mockResolvedValue(null);
const saveRecurringProfile = vi.fn();
vi.mock('../../../temporal/remote-recurring-profile-edit', () => ({
  createRemoteRecurringProfileEdit: () => ({
    loadActivityContext: loadRecurringContext,
    saveActivityProfile: saveRecurringProfile,
  }),
}));
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({ get, revise, retire }),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: loadSettings,
    loadChildCount,
    saveCore,
    previewReplan,
    applyReplan,
    loadLifeAreaChoice,
    assignLifeArea,
    revisePlannedName,
    setPlacementProtected,
    addObjective,
    refreshObjectives,
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

async function submitEditor() {
  await waitFor(() => expect(
    screen.getByRole('button', { name: 'Salva modifiche' }),
  ).toHaveProperty('disabled', false));
  fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
}

const currentSettings = {
  capture: { mode: 'disabled', stateRef: null },
  reality: { mode: 'manual', stateRef: null },
  schedules: [],
  objectives: [],
  lifeAreaRef: null,
  placementProtected: false,
  placementLockScheduleRef: null,
  placementLockRevision: null,
  reminderLeadMinutes: null,
  childGuardMode: 'none',
};

loadSettings.mockResolvedValue(currentSettings);
loadLifeAreaChoice.mockResolvedValue({
  options: [], currentRef: null, currentRevision: 0,
});

describe('Recurring Activity profile scope', () => {
  it('keeps the Advanced create order in the edit surface', async () => {
    const { container } = render(
      <ActivityEditPanel profile={profile} closeRequestRef={createRef()}
        onSaved={() => undefined} onCancel={() => undefined} />,
    );
    await screen.findByRole('group', { name: 'Collocazione attuale' });
    const body = container.querySelector('.timeline-activity-editor__body');
    expect(body).not.toBeNull();
    const sections = [
      '.timeline-activity-editor__kind',
      '.timeline-activity-editor__title-row',
      '[aria-label="Programmazione attuale"]',
      '.timeline-activity-editor__area-color',
      '[aria-label="Svolgimento e obiettivi"]',
      '.timeline-activity-editor__location',
      '.timeline-activity-editor__description',
    ].map((selector) => body?.querySelector(selector));
    expect(sections.every(Boolean)).toBe(true);
    for (let index = 1; index < sections.length; index += 1) {
      expect(sections[index - 1]?.compareDocumentPosition(sections[index]!))
        .toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    }
  });

  it('includes the clicked instance for both available save scopes', async () => {
    const occurrenceRef = '0199a222-2222-7222-8222-222222222222';
    const recurrenceStateRef = '0199a333-3333-7333-8333-333333333333';
    const context = {
      occurrenceRef, sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3, recurrenceStateRef,
    };
    loadRecurringContext.mockResolvedValueOnce(context);
    saveRecurringProfile.mockResolvedValue({ ...profile, title: 'Dopo' });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.change(await screen.findByRole('textbox', { name: 'Titolo' }), {
      target: { value: 'Dopo' },
    });
    expect(await screen.findByLabelText('Solo questa')).toBeTruthy();
    fireEvent.click(screen.getByLabelText('Questa e le prossime'));
    await submitEditor();
    await waitFor(() => expect(saveRecurringProfile).toHaveBeenCalledWith(
      ref, context, 'this_and_following', { title: 'Dopo' }, expect.any(String),
    ));
    expect(saveCore).not.toHaveBeenCalled();
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(
      expect.objectContaining({ title: 'Dopo' }),
    ));
  });
});

describe('Objective correction in Activity Editor', () => {
  const objective = {
    objectiveRef: '0199a567-8888-7888-8888-012345678901',
    label: 'Corsa 10 km',
    resultKind: 'quantity',
    comparatorCode: 'gte',
    targetValue: 10,
    targetMin: null,
    targetMax: null,
    unitCode: 'km',
    presentationOrder: 0,
    observationRef: '0199a567-8888-7888-8888-012345678902',
    observedBoolean: null,
    observedNumeric: 8,
    qualitativeCode: null,
    evaluationStateRef: '0199a567-8888-7888-8888-012345678903',
    assessmentCode: 'not_satisfied',
  } as const;

  it('modifies the existing logical Objective instead of adding a duplicate', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings, objectives: [objective],
    });
    getDefinition.mockResolvedValueOnce({
      ...objective, definitionRevision: 0,
    });
    reviseDefinition.mockResolvedValueOnce(undefined);
    refreshObjectives.mockResolvedValueOnce({
      ...currentSettings, objectives: [{ ...objective, label: 'Corsa 7 km', targetValue: 7 }],
    });
    render(
      <ActivityEditPanel profile={profile} closeRequestRef={createRef()}
        onSaved={() => undefined} onCancel={() => undefined} />,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Modifica obiettivo' }));
    fireEvent.change(await screen.findByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Corsa 7 km' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva obiettivo' }));
    await waitFor(() => expect(reviseDefinition).toHaveBeenCalledWith(
      objective.objectiveRef, expect.objectContaining({
        operationId: expect.any(String), expectedRevision: 0,
        scopeCode: 'only_this', seriesState: null,
        label: 'Corsa 7 km', targetValue: 10, presentationOrder: 0,
      }),
    ));
    expect(addObjective).not.toHaveBeenCalled();
    await waitFor(() => expect(screen.getByText(/Corsa 7 km/)).toBeTruthy());
  });

  it('applies selected-and-following only with authoritative generated lineage', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings, objectives: [objective],
    });
    getDefinition.mockResolvedValueOnce({ ...objective, definitionRevision: 1 });
    const seriesState = {
      sourceNativeRef: '0199a566-6666-7666-8666-666666666666',
      occurrenceRef: '0199a577-7777-7777-8777-777777777777',
      templateSlot: 0,
      sourceRevision: 2,
      recurrenceStateRef: '0199a588-8888-7888-8888-888888888888',
    };
    getSeriesState.mockResolvedValueOnce(seriesState);
    reviseDefinition.mockResolvedValueOnce(undefined);
    refreshObjectives.mockResolvedValueOnce({
      ...currentSettings, objectives: [{ ...objective, label: 'Corsa 7 km' }],
    });
    render(
      <ActivityEditPanel profile={profile} closeRequestRef={createRef()}
        onSaved={() => undefined} onCancel={() => undefined} />,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Modifica obiettivo' }));
    fireEvent.click(await screen.findByLabelText('Questa e le prossime'));
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Corsa 7 km' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva obiettivo' }));
    await waitFor(() => expect(reviseDefinition).toHaveBeenCalledWith(
      objective.objectiveRef, expect.objectContaining({
        scopeCode: 'this_and_following',
        seriesState,
        label: 'Corsa 7 km',
      }),
    ));
    expect(addObjective).not.toHaveBeenCalled();
  });

  it('corrects a measured result while keeping the same Objective identity', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings, objectives: [objective],
    });
    correctResult.mockResolvedValueOnce(undefined);
    refreshObjectives.mockResolvedValueOnce({
      ...currentSettings, objectives: [{
        ...objective, observedNumeric: 6, assessmentCode: 'not_satisfied',
      }],
    });
    render(
      <ActivityEditPanel profile={profile} closeRequestRef={createRef()}
        onSaved={() => undefined} onCancel={() => undefined} />,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Correggi risultato' }));
    fireEvent.change(screen.getByRole('spinbutton', { name: 'Risultato corretto' }), {
      target: { value: '6' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva rettifica' }));
    await waitFor(() => expect(correctResult).toHaveBeenCalledWith(
      objective.objectiveRef, {
        operationId: expect.any(String),
        expectedEvaluationStateRef: objective.evaluationStateRef,
        observedBoolean: null,
        observedNumeric: 6,
        qualitativeCode: null,
        assessmentCode: null,
      },
    ));
    expect(reviseDefinition).not.toHaveBeenCalled();
  });
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
    await screen.findByRole('checkbox', { name: 'Sessione' });
    await submitEditor();
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
    fireEvent.click(await screen.findByRole('checkbox', { name: 'Sessione' }));
    fireEvent.click(screen.getByRole('radio', { name: 'Chiedi al termine' }));
    await submitEditor();
    expect(await screen.findByRole('alert')).toHaveProperty(
      'textContent',
      expect.stringContaining('Connessione interrotta'),
    );
    expect(saveCore).toHaveBeenCalledWith(profile, currentSettings,
      { capture: 'live', reality: 'review_on_end' }, expect.any(String));
    expect(onSaved).not.toHaveBeenCalled();

    await submitEditor();
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(saveCore).toHaveBeenCalledTimes(2);
    expect(saveCore.mock.calls[1]?.[3]).toBe(saveCore.mock.calls[0]?.[3]);
    expect(revise).not.toHaveBeenCalled();
  });

  it('adds a post-create Objective with stable retry ID and readback', async () => {
    addObjective.mockRejectedValueOnce(new Error('Errore temporaneo'))
      .mockImplementationOnce(async (_ref, settings) => ({
        ...settings,
        objectives: [{ objectiveRef: 'new-objective', label: 'Percorrere 10 km',
          presentationOrder: 0, assessmentCode: null }],
      }));
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Apri nuovo obiettivo' }));
    const name = await screen.findByRole('textbox', { name: 'Nome obiettivo' });
    fireEvent.change(name, { target: { value: 'Percorrere 10 km' } });
    fireEvent.change(screen.getByRole('combobox', { name: 'Tipo obiettivo' }),
      { target: { value: 'quantity' } });
    fireEvent.change(screen.getByRole('spinbutton', { name: 'Valore obiettivo' }),
      { target: { value: '10' } });
    fireEvent.change(screen.getByRole('textbox', { name: 'Unità di misura' }),
      { target: { value: 'km' } });
    expect(screen.getByRole('button', { name: 'Salva modifiche' }))
      .toHaveProperty('disabled', true);
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi obiettivo' }));
    expect(await screen.findByRole('alert')).toHaveProperty('textContent',
      expect.stringContaining('Errore temporaneo'));
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi obiettivo' }));
    await waitFor(() => expect(addObjective).toHaveBeenCalledTimes(2));
    expect(addObjective.mock.calls[0]?.[3]).toEqual(addObjective.mock.calls[1]?.[3]);
    expect(addObjective.mock.calls[0]?.[2]).toMatchObject({
      label: 'Percorrere 10 km', resultKind: 'quantity',
      comparatorCode: 'gte', targetValue: 10, unitCode: 'km',
    });
    expect(await screen.findByText('Percorrere 10 km', { selector: 'li' })).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Apri nuovo obiettivo' })).toBeTruthy();
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
    fireEvent.click(screen.getByRole('button', { name: '＋ Sessione' }));
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

  it('edits the single overall interval of an Activity without role intervals', async () => {
    const settings = { ...currentSettings, schedules: [
      { scheduleRef: 'envelope', role: 'envelope', name: null, order: 0,
        placementStateRef: 'state-0', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00',
        zoneId: 'Europe/Rome' },
    ] };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([{ scheduleRef: 'envelope', role: 'envelope',
      previousStart: '2026-10-09T09:00:00', previousEnd: '2026-10-09T12:00:00',
      proposedStart: '2026-10-09T10:00:00', proposedEnd: '2026-10-09T13:00:00' }]);
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.change(await screen.findByLabelText('Inizio'),
      { target: { value: '2026-10-09T10:00' } });
    fireEvent.change(screen.getByLabelText('Fine'),
      { target: { value: '2026-10-09T13:00' } });
    fireEvent.click(screen.getByRole('button', { name: 'Verifica spostamento' }));
    await waitFor(() => expect(previewReplan).toHaveBeenCalledWith(ref, settings,
      expect.objectContaining({ times: expect.objectContaining({
        envelope: { start: '2026-10-09T10:00', end: '2026-10-09T13:00' },
      }) }), expect.any(String)));
    expect(screen.queryByRole('button', { name: 'Aggiungi intervallo' })).toBeNull();
  });

  it('persists protection only through the guarded separate action', async () => {
    const settings = { ...currentSettings, placementLockScheduleRef: 'envelope',
      placementLockRevision: 2 };
    loadSettings.mockResolvedValueOnce(settings);
    setPlacementProtected.mockResolvedValueOnce({
      ...settings, placementProtected: true, placementLockRevision: 3,
    });
    const onSaved = vi.fn();
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={onSaved} onCancel={() => undefined} />);
    const toggle = await screen.findByRole('button', { name: 'Blocca spostamenti' });
    fireEvent.click(toggle);
    expect(screen.getByRole('button', { name: 'Salva modifiche' }))
      .toHaveProperty('disabled', true);
    fireEvent.click(screen.getByRole('button', { name: 'Applica blocco spostamenti' }));
    await waitFor(() => expect(setPlacementProtected).toHaveBeenCalledWith(
      settings, true,
    ));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Sblocca spostamenti' })
      .getAttribute('aria-pressed')).toBe('true'));
    expect(onSaved).not.toHaveBeenCalled();
  });

  it('changes Life Area with the accepted assignment revision', async () => {
    const catalog = { currentRef: null, currentRevision: 0,
      options: [{ ref: 'new-area', name: 'Lavoro' }] };
    loadLifeAreaChoice.mockResolvedValueOnce(catalog);
    assignLifeArea.mockResolvedValueOnce({
      ...catalog, currentRef: 'new-area', currentRevision: 1,
    });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    const select = await screen.findByRole('combobox', { name: 'Area assegnata' });
    fireEvent.change(select, { target: { value: 'new-area' } });
    expect(screen.getByRole('button', { name: 'Salva modifiche' }))
      .toHaveProperty('disabled', true);
    fireEvent.click(screen.getByRole('button', { name: 'Applica Life Area' }));
    await waitFor(() => expect(assignLifeArea).toHaveBeenCalledWith(
      ref, catalog, 'new-area', expect.any(String),
    ));
  });

  it('previews replacing an Activity interval without deleting historical rows', async () => {
    const settings = { ...currentSettings, schedules: [
      { scheduleRef: 'envelope', role: 'envelope', name: null, order: 0,
        placementStateRef: 'state-0', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00', zoneId: 'Europe/Rome' },
      { scheduleRef: 'interval', role: 'interval', name: null, order: 1,
        placementStateRef: 'state-1', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00', zoneId: 'Europe/Rome' },
    ] };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([
      { scheduleRef: 'interval', clientRef: null, role: 'interval_removed',
        previousStart: '2026-10-09T09:00:00', previousEnd: '2026-10-09T12:00:00',
        proposedStart: null, proposedEnd: null },
      { scheduleRef: null, clientRef: 'new', role: 'interval_added',
        previousStart: null, previousEnd: null,
        proposedStart: '2026-10-09T10:00:00', proposedEnd: '2026-10-09T11:00:00' },
    ]);
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Rimuovi intervallo' }));
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi intervallo' }));
    fireEvent.change(screen.getByLabelText('Inizio nuovo intervallo'),
      { target: { value: '2026-10-09T10:00' } });
    fireEvent.change(screen.getByLabelText('Fine nuovo intervallo'),
      { target: { value: '2026-10-09T11:00' } });
    expect(screen.getByRole('button', { name: 'Salva modifiche' })).toHaveProperty('disabled', true);
    fireEvent.click(screen.getByRole('button', { name: 'Verifica spostamento' }));
    await waitFor(() => expect(previewReplan).toHaveBeenCalledWith(
      ref, settings, expect.objectContaining({
        removedIntervals: ['interval'],
        newIntervals: [expect.objectContaining({
          start: '2026-10-09T10:00', end: '2026-10-09T11:00',
        })],
      }), expect.any(String),
    ));
    expect(screen.getByText(/Intervallo rimosso/)).toBeTruthy();
    expect(screen.getByText(/Nuovo intervallo/)).toBeTruthy();
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

  it('refuses a recurring Activity duplicate instead of silently creating a one-off', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3, recurrenceStateRef: null,
    });
    const onDuplicate = vi.fn();
    render(<ActivityInspectorActions activityRef={ref}
      onEdit={() => undefined} onDeleted={() => undefined}
      onDuplicate={onDuplicate} />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('duplicazione fedele della ricorrenza');
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('refuses hidden Activity children even when the Timeline has no subitems', async () => {
    loadChildCount.mockResolvedValueOnce(1);
    const onDuplicate = vi.fn();
    render(<ActivityInspectorActions
      activityRef={ref}
      onEdit={() => undefined}
      onDeleted={() => undefined}
      onDuplicate={onDuplicate}
    />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('contiene sotto-attività');
    expect(loadChildCount).toHaveBeenCalledWith(ref);
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('refuses a deceptively incomplete duplicate when an Activity contains children', async () => {
    const onDuplicate = vi.fn();
    render(<ActivityInspectorActions
      activityRef={ref}
      subitemsCount={2}
      onEdit={() => undefined}
      onDeleted={() => undefined}
      onDuplicate={onDuplicate}
    />);
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent)
      .toContain('duplicazione fedele della struttura');
    expect(onDuplicate).not.toHaveBeenCalled();
    expect(loadSettings).not.toHaveBeenCalled();
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

  it('preserves an unsaved planned name instead of submitting unrelated core settings', async () => {
    loadSettings.mockResolvedValueOnce({ ...currentSettings, schedules: [{
      scheduleRef: 'planned-m3b', role: 'planned', name: 'Preparazione', order: 0,
      placementStateRef: 'placement-1', temporalForm: 'named_zone_local',
      start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00',
      zoneId: 'Europe/Rome',
    }] });
    const onSaved = vi.fn();
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={onSaved} onCancel={() => undefined} />);
    const name = await screen.findByRole('textbox', { name: 'Nome sessione pianificata' });
    fireEvent.change(name, { target: { value: 'Preparazione approfondita' } });
    expect(screen.getByRole('button', { name: 'Salva modifiche' }))
      .toHaveProperty('disabled', true);
    expect(saveCore).not.toHaveBeenCalled();
    expect(onSaved).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Salva nome sessione' }))
      .toHaveProperty('disabled', false);
  });

  it('does not turn a nonlocal temporal form into a local Schedule during edit', async () => {
    loadSettings.mockResolvedValueOnce({ ...currentSettings, schedules: [{
      scheduleRef: 'absolute-schedule', role: 'interval', name: null, order: 0,
      placementStateRef: 'state-absolute', temporalForm: 'absolute_instant',
      start: '2026-10-09T09:00:00Z', end: '2026-10-09T10:00:00Z',
      zoneId: null,
    }] });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    expect(await screen.findByText(/DANTE non le converte automaticamente/)).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Verifica spostamento' })).toBeNull();
    expect(screen.queryByRole('button', { name: '＋ Sessione' })).toBeNull();
    expect(applyReplan).not.toHaveBeenCalled();
  });

  it('blocks rescheduling until a planned-name draft is saved or discarded', async () => {
    loadSettings.mockResolvedValueOnce({ ...currentSettings, schedules: [
      {
        scheduleRef: 'envelope-replan', role: 'envelope', name: null, order: 0,
        placementStateRef: 'state-envelope', temporalForm: 'named_zone_local',
        start: '2026-10-09T08:00:00', end: '2026-10-09T11:00:00',
        zoneId: 'Europe/Rome',
      },
      {
        scheduleRef: 'interval-replan', role: 'interval', name: null, order: 0,
        placementStateRef: 'state-interval', temporalForm: 'named_zone_local',
        start: '2026-10-09T08:00:00', end: '2026-10-09T11:00:00',
        zoneId: 'Europe/Rome',
      },
      {
        scheduleRef: 'planned-replan', role: 'planned', name: 'Allenamento', order: 1,
        placementStateRef: 'state-3', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00',
        zoneId: 'Europe/Rome',
      },
    ] });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    const name = await screen.findByRole('textbox', { name: 'Nome sessione pianificata' });
    fireEvent.change(name, { target: { value: 'Allenamento lungo' } });
    fireEvent.change(screen.getAllByLabelText('Inizio')[0]!, {
      target: { value: '2026-10-09T07:30' },
    });
    expect(screen.getByText(/Salva prima i nomi delle Session/)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Verifica spostamento' }))
      .toHaveProperty('disabled', true);
    expect(previewReplan).not.toHaveBeenCalled();
    expect(applyReplan).not.toHaveBeenCalled();
  });

  it('discloses selected-only owner-domain editing even with no metadata change', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3, recurrenceStateRef: null,
    });
    loadSettings.mockResolvedValueOnce({ ...currentSettings, schedules: [{
      scheduleRef: 'planned-recurring', role: 'planned', name: 'Preparazione', order: 0,
      placementStateRef: 'placement-2', temporalForm: 'named_zone_local',
      start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00',
      zoneId: 'Europe/Rome',
    }] });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.change(await screen.findByRole('textbox', { name: 'Nome sessione pianificata' }), {
      target: { value: 'Ripasso' },
    });
    const thisScope = await screen.findByLabelText('Solo questa');
    const following = screen.getByLabelText('Questa e le prossime');
    expect(thisScope).toHaveProperty('checked', true);
    expect(following).toHaveProperty('disabled', true);
    expect(screen.getByText(/Life Area e nomi delle Session pianificate/)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Salva modifiche' }))
      .toHaveProperty('disabled', true);
    expect(saveRecurringProfile).not.toHaveBeenCalled();
  });

  it('never offers a following-series Life Area edit without a source-policy capability', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3, recurrenceStateRef: null,
    });
    loadSettings.mockResolvedValueOnce({ ...currentSettings, lifeAreaRef: 'area-1' });
    loadLifeAreaChoice.mockResolvedValueOnce({
      currentRef: 'area-1', currentRevision: 2,
      options: [{ ref: 'area-1', name: 'Lavoro' }],
    });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    fireEvent.change(await screen.findByRole('combobox', { name: 'Area assegnata' }), {
      target: { value: '' },
    });
    expect(await screen.findByLabelText('Solo questa')).toHaveProperty('checked', true);
    expect(screen.getByLabelText('Questa e le prossime')).toHaveProperty('disabled', true);
    expect(screen.getByText(/Life Area e nomi delle Session pianificate si salvano soltanto/)).toBeTruthy();
    expect(assignLifeArea).not.toHaveBeenCalled();
    expect(saveRecurringProfile).not.toHaveBeenCalled();
  });

  it('unassigns an existing Life Area using an explicit null target', async () => {
    const catalog = { currentRef: 'area-1', currentRevision: 4,
      options: [{ ref: 'area-1', name: 'Personale' }] };
    loadSettings.mockResolvedValueOnce({ ...currentSettings, lifeAreaRef: 'area-1' });
    loadLifeAreaChoice.mockResolvedValueOnce(catalog);
    assignLifeArea.mockResolvedValueOnce({
      ...catalog, currentRef: null, currentRevision: 5,
    });
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    const select = await screen.findByRole('combobox', { name: 'Area assegnata' });
    fireEvent.change(select, { target: { value: '' } });
    fireEvent.click(screen.getByRole('button', { name: 'Applica Life Area' }));
    await waitFor(() => expect(assignLifeArea).toHaveBeenCalledWith(
      ref, catalog, null, expect.any(String),
    ));
  });

  it('renames an existing planned Session without rescheduling it', async () => {
    loadSettings.mockResolvedValueOnce({ ...currentSettings, schedules: [
      { scheduleRef: 'planned', role: 'planned', name: 'Lettura', order: 1,
        placementStateRef: 'state-planned', temporalForm: 'named_zone_local',
        start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00',
        zoneId: 'Europe/Rome' },
    ] });
    revisePlannedName.mockResolvedValueOnce('Ripasso');
    render(<ActivityEditPanel profile={profile} closeRequestRef={createRef()}
      onSaved={() => undefined} onCancel={() => undefined} />);
    const field = await screen.findByRole('textbox', { name: 'Nome sessione pianificata' });
    fireEvent.change(field, { target: { value: 'Ripasso' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva nome sessione' }));
    await waitFor(() => expect(revisePlannedName).toHaveBeenCalledWith(
      ref, 'planned', 'Lettura', 'Ripasso',
    ));
    expect(applyReplan).not.toHaveBeenCalled();
  });

});
