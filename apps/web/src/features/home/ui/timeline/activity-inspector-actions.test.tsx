// @vitest-environment jsdom
import { createRef } from 'react';
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityInspectorActions } from './activity-inspector-actions';
import { ActivityEditPanel } from './activity-edit-panel';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';

/** Vitest asymmetric matchers are typed as any; preserve their runtime
 * matching semantics without propagating any into the expected payload. */
function containing(expected: unknown): unknown {
  return expect.objectContaining(expected) as unknown;
}

function anyInstance(ctor: typeof String): unknown {
  return expect.any(ctor) as unknown;
}

function requiredRecord(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Expected an object in the mutation call.');
  }
  return value as Record<string, unknown>;
}

function requiredItems(value: unknown): readonly unknown[] {
  if (!Array.isArray(value)) {
    throw new Error('Expected a list in the mutation call.');
  }
  return value as unknown[];
}

const get = vi.fn();
const revise = vi.fn();
const retire = vi.fn();
const sessionImpact = vi.fn().mockResolvedValue({
  fingerprint: 'a'.repeat(64),
  attempts: [],
});
const deleteSessionAttempt = vi.fn();
const deleteHard = vi.fn();
const loadSettings = vi.fn();
const listActivitySessions = vi.fn().mockResolvedValue([]);
const loadChildCount = vi.fn().mockResolvedValue(0);
const saveCore = vi.fn();
const previewReplan = vi.fn();
const applyReplan = vi
  .fn()
  .mockImplementation((_ref: unknown, settings: unknown) =>
    Promise.resolve(settings),
  );
const loadLifeAreaChoice = vi.fn();
const createLifeArea = vi.fn();
const setLifeAreaAppearance = vi.fn();
const assignLifeArea = vi.fn();
const revisePlannedName = vi.fn();
const setPlacementProtected = vi.fn();
const addObjective = vi.fn();
const refreshObjectives = vi.fn();
const getDefinition = vi.fn();
const getSeriesState = vi.fn().mockResolvedValue(null);
const reviseDefinition = vi.fn();
const applyActivityEdits = vi.fn();
const correctResult = vi.fn();
const previewHardDeletion = vi.fn();
const confirmHardDeletion = vi.fn();

vi.mock('../../../temporal/remote-temporal-hard-deletion', () => ({
  createRemoteTemporalHardDeletion: () => ({
    preview: previewHardDeletion,
    deleteConfirmed: confirmHardDeletion,
  }),
}));

vi.mock('../../../temporal/remote-reality-objective-data-source', () => ({
  createRemoteRealityObjectiveDataSource: () => ({
    getDefinition,
    getSeriesState,
    reviseDefinition,
    applyActivityEdits,
    correctResult,
  }),
}));
const loadRecurringContext = vi.fn().mockResolvedValue(null);
const loadRecurringPreview = vi.fn().mockResolvedValue({
  fingerprint: 'a'.repeat(32),
  selectedProtection: null,
  targetOccurrenceRefs: [],
  protectedOccurrences: [],
});
const saveRecurringProfile = vi.fn();
vi.mock('../../../temporal/remote-recurring-profile-edit', () => ({
  createRemoteRecurringProfileEdit: () => ({
    loadActivityContext: loadRecurringContext,
    loadPreview: loadRecurringPreview,
    saveActivityProfile: saveRecurringProfile,
  }),
}));
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({
    get,
    revise,
    retire,
    sessionImpact,
    deleteSessionAttempt,
    deleteHard,
  }),
}));
vi.mock('../../../temporal/remote-session-data-source', () => ({
  createRemoteTemporalSessionDataSource: () => ({
    list: listActivitySessions,
  }),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: loadSettings,
    loadChildCount,
    saveCore,
    previewReplan,
    applyReplan,
    loadLifeAreaChoice,
    createLifeArea,
    setLifeAreaAppearance,
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
  await waitFor(() =>
    expect(
      screen.getByRole('button', { name: 'Salva modifiche' }),
    ).toHaveProperty('disabled', false),
  );
  fireEvent.click(screen.getByRole('button', { name: 'Salva modifiche' }));
}

function newIntervalRow(): HTMLElement {
  const row = document.querySelector<HTMLElement>(
    '.timeline-activity-editor__intervals .temporal-create-activity-interval',
  );
  if (!row) throw new Error('Expected the new interval controls.');
  return row;
}

function setNewIntervalTime(label: 'Inizio' | 'Fine', hour: string) {
  const row = within(newIntervalRow());
  fireEvent.change(row.getByRole('textbox', { name: `${label}: ore` }), {
    target: { value: hour },
  });
  fireEvent.change(row.getByRole('textbox', { name: `${label}: minuti` }), {
    target: { value: '00' },
  });
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
  options: [],
  currentRef: null,
  currentRevision: 0,
});

describe('Activity Inspector actions', () => {
  it('offers Bozze without exposing a second unplaced workflow', () => {
    get.mockResolvedValue(profile);
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={() => undefined}
      />,
    );
    expect(
      screen.getByRole('button', { name: 'Sposta in Bozze' }),
    ).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: /Rimuovi dalla Timeline/ }),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: /Annulla rimozione Timeline/ }),
    ).toBeNull();
  });
});

describe('Recurring Activity profile scope', () => {
  it('renders the persisted Life Area colors in edit choices', async () => {
    loadLifeAreaChoice.mockResolvedValueOnce({
      currentRef: null,
      currentRevision: 0,
      options: [
        { ref: 'area-blue', name: 'test4', revision: 1, colorCode: '#4759CD' },
        { ref: 'area-green', name: 'test2', revision: 1, colorCode: '#2AB783' },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const select = await screen.findByRole('textbox', {
      name: 'Area assegnata',
    });
    fireEvent.focus(select);
    const blue = await screen.findByRole('option', { name: 'test4' });
    const green = await screen.findByRole('option', { name: 'test2' });
    const swatch = (option: HTMLElement) =>
      option.querySelector<HTMLElement>(
        '.temporal-create-life-area-field__swatch',
      )?.style.backgroundColor;
    expect(swatch(blue)).toBe('rgb(71, 89, 205)');
    expect(swatch(green)).toBe('rgb(42, 183, 131)');
  });

  it('labels retained named and generic attempts with their factual lifecycle state', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'named-schedule',
          role: 'planned',
          name: 'Ripasso',
          order: 1,
          placementStateRef: null,
          temporalForm: null,
          start: null,
          end: null,
          zoneId: null,
        },
      ],
    });
    listActivitySessions.mockResolvedValueOnce([
      {
        sessionRef: 'main',
        plannedScheduleRef: null,
        open: true,
        paused: false,
        startedAt: '2026-10-09T08:25:00Z',
        endedAt: null,
        activeSeconds: 180,
        evaluatedAt: '2026-10-09T08:28:00Z',
      },
      {
        sessionRef: 'named1',
        plannedScheduleRef: 'named-schedule',
        open: true,
        paused: true,
        startedAt: '2026-10-09T08:25:00Z',
        endedAt: null,
        activeSeconds: 120,
        evaluatedAt: '2026-10-09T08:28:00Z',
      },
      {
        sessionRef: 'named2',
        plannedScheduleRef: 'named-schedule',
        open: false,
        paused: false,
        startedAt: '2026-10-09T08:25:00Z',
        endedAt: '2026-10-09T08:28:00Z',
        activeSeconds: 180,
        evaluatedAt: '2026-10-09T08:28:00Z',
      },
    ]);
    const { container } = render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const mainStatus = await screen.findByRole('region', {
      name: 'Registrazioni Sessione attività',
    });
    expect(mainStatus.textContent).toContain('In corso');
    const namedRow = container.querySelector(
      '[data-edit-planned-session="named-schedule"]',
    );
    expect(namedRow).not.toBeNull();
    await waitFor(() => {
      expect(namedRow?.textContent).toContain('In pausa');
      expect(namedRow?.textContent).toContain('Totale attivo');
    });
    expect(listActivitySessions).toHaveBeenCalledWith('activity', ref);
  });

  it('locks timing and capture until the only recorded attempt is explicitly deleted', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      capture: { mode: 'live', stateRef: null },
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          order: 0,
          name: null,
          placementStateRef: 'state',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    listActivitySessions
      .mockResolvedValueOnce([
        {
          sessionRef: 'attempt',
          plannedScheduleRef: null,
          open: true,
          paused: true,
          startedAt: '2026-10-09T08:25:00Z',
          endedAt: null,
          activeSeconds: 180,
          evaluatedAt: '2026-10-09T08:28:00Z',
        },
      ])
      .mockResolvedValueOnce([]);
    sessionImpact.mockResolvedValueOnce({
      fingerprint: 'b'.repeat(64),
      attempts: [{ sessionRef: 'attempt' }],
    });
    deleteSessionAttempt.mockResolvedValueOnce(undefined);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const record = await screen.findByRole('region', {
      name: 'Registrazioni Sessione attività',
    });
    expect(record.textContent).toContain('In pausa 00:03:00');
    expect(screen.getByRole('button', { name: 'Orario' })).toHaveProperty(
      'disabled',
      true,
    );
    expect(
      screen.getByRole('button', { name: 'Tutto il giorno' }),
    ).toHaveProperty('disabled', true);
    expect(screen.getByRole('checkbox', { name: 'Sessione' })).toHaveProperty(
      'disabled',
      true,
    );
    fireEvent.click(
      within(record).getByRole('button', {
        name: 'Elimina registrazione attempt',
      }),
    );
    const confirmation = await screen.findByRole('alertdialog', {
      name: 'Elimina registrazione',
    });
    expect(deleteSessionAttempt).not.toHaveBeenCalled();
    fireEvent.click(
      within(confirmation).getByRole('button', {
        name: 'Elimina registrazione',
      }),
    );
    await waitFor(() =>
      expect(deleteSessionAttempt).toHaveBeenCalledWith(
        ref,
        'attempt',
        'b'.repeat(64),
      ),
    );
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'Orario' })).toHaveProperty(
        'disabled',
        false,
      ),
    );
    expect(screen.getByRole('checkbox', { name: 'Sessione' })).toHaveProperty(
      'disabled',
      false,
    );
  });

  it('allows replanning after only named Sessions have concluded but keeps capture locked', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          order: 0,
          name: null,
          placementStateRef: 'state',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'named',
          role: 'planned',
          order: 1,
          name: 'Ripasso',
          placementStateRef: null,
          temporalForm: null,
          start: null,
          end: null,
          zoneId: null,
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    listActivitySessions.mockResolvedValueOnce([
      {
        sessionRef: 'finished-child',
        plannedScheduleRef: 'named',
        open: false,
        paused: false,
        startedAt: '2026-10-09T08:25:00Z',
        endedAt: '2026-10-09T08:28:00Z',
        activeSeconds: 180,
        evaluatedAt: '2026-10-09T08:28:00Z',
      },
    ]);
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const named = await screen.findByRole('textbox', { name: 'Nome Sessione' });
    expect(named.closest('[data-edit-planned-session]')?.textContent).toContain(
      'conclusa',
    );
    expect(
      screen.getByText(/registrazioni concluse restano svolte/),
    ).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Orario' })).toHaveProperty(
      'disabled',
      false,
    );
    expect(
      screen.getByRole('button', { name: 'Tutto il giorno' }),
    ).toHaveProperty('disabled', false);
    expect(
      screen.getByRole('button', { name: 'Aggiungi intervallo' }),
    ).toHaveProperty('disabled', false);
    expect(screen.getByRole('checkbox', { name: 'Sessione' })).toHaveProperty(
      'disabled',
      true,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Tutto il giorno' }));
    await submitEditor();
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
    expect(saveCore).not.toHaveBeenCalled();
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it.each([
    [
      'paused child',
      {
        sessionRef: 'paused',
        plannedScheduleRef: 'named',
        open: true,
        paused: true,
      },
    ],
    [
      'completed main',
      {
        sessionRef: 'main',
        plannedScheduleRef: null,
        open: false,
        paused: false,
      },
    ],
  ])('keeps the plan locked with a %s attempt', async (_label, partial) => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          order: 0,
          name: null,
          placementStateRef: 'state',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    listActivitySessions.mockResolvedValueOnce([
      {
        ...partial,
        startedAt: '2026-10-09T08:25:00Z',
        endedAt: partial.open ? null : '2026-10-09T08:28:00Z',
        activeSeconds: 180,
        evaluatedAt: '2026-10-09T08:28:00Z',
      },
    ]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    await screen.findByRole('group', { name: 'Collocazione attuale' });
    await waitFor(() =>
      expect(screen.getByRole('checkbox', { name: 'Sessione' })).toHaveProperty(
        'disabled',
        true,
      ),
    );
    expect(screen.getByRole('button', { name: 'Orario' })).toHaveProperty(
      'disabled',
      true,
    );
    expect(
      screen.getByRole('button', { name: 'Tutto il giorno' }),
    ).toHaveProperty('disabled', true);
  });

  it('keeps the Advanced create order in the edit surface', async () => {
    const { container } = render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    await screen.findByRole('group', { name: 'Collocazione attuale' });
    const body = container.querySelector('.timeline-activity-editor__body');
    expect(body).not.toBeNull();
    const sections = [
      '.timeline-activity-editor__title-row',
      '[aria-label="Programmazione attuale"]',
      '.timeline-activity-editor__area-color',
      '[aria-label="Svolgimento e obiettivi"]',
      '.timeline-activity-editor__location',
      '.timeline-activity-editor__description',
    ].map((selector) => body?.querySelector(selector));
    expect(sections.every(Boolean)).toBe(true);
    for (let index = 1; index < sections.length; index += 1) {
      expect(
        sections[index - 1]?.compareDocumentPosition(sections[index]!),
      ).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    }
  });

  it('previews the selected and future clean instances before a series metadata save', async () => {
    const occurrenceRef = '0199a222-2222-7222-8222-222222222222';
    const recurrenceStateRef = '0199a333-3333-7333-8333-333333333333';
    const context = {
      occurrenceRef,
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef,
    };
    loadRecurringContext.mockResolvedValueOnce(context);
    const preview = {
      fingerprint: 'a'.repeat(32),
      selectedProtection: null,
      targetOccurrenceRefs: [occurrenceRef],
      protectedOccurrences: [],
    };
    loadRecurringPreview.mockResolvedValueOnce(preview);
    saveRecurringProfile.mockResolvedValue({ ...profile, title: 'Dopo' });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        initialScope="this_and_following"
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.change(await screen.findByRole('textbox', { name: 'Titolo' }), {
      target: { value: 'Dopo' },
    });
    expect(await screen.findByText('Questa e le successive')).toBeTruthy();
    await waitFor(() =>
      expect(loadRecurringPreview).toHaveBeenCalledWith(
        context,
        'this_and_following',
      ),
    );
    await submitEditor();
    await waitFor(() =>
      expect(saveRecurringProfile).toHaveBeenCalledWith(
        ref,
        context,
        'this_and_following',
        { title: 'Dopo' },
        expect.any(String),
        preview,
      ),
    );
    expect(saveCore).not.toHaveBeenCalled();
    await waitFor(() =>
      expect(onSaved).toHaveBeenCalledWith(containing({ title: 'Dopo' })),
    );
  });
});

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

describe('Objective correction in Activity Editor', () => {
  it('modifies an expanded Objective directly with one final Save', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [objective],
    });
    getDefinition.mockResolvedValueOnce({
      ...objective,
      definitionRevision: 0,
    });
    applyActivityEdits.mockResolvedValueOnce([
      { ...objective, label: 'Corsa 7 km' },
    ]);
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.focus(
      await screen.findByRole('textbox', { name: 'Nome obiettivo' }),
    );
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Corsa 7 km' },
    });
    expect(applyActivityEdits).not.toHaveBeenCalled();
    expect(
      screen.queryByRole('button', { name: 'Salva obiettivo' }),
    ).toBeNull();
    expect(
      screen.getAllByRole('textbox', { name: 'Nome obiettivo' }),
    ).toHaveLength(1);
    expect(screen.queryByRole('button', { name: /^Corsa 10 km/ })).toBeNull();
    await submitEditor();
    await waitFor(() =>
      expect(applyActivityEdits).toHaveBeenCalledWith(ref, {
        add: [],
        revise: [
          containing({
            objectiveRef: objective.objectiveRef,
            change: containing({
              label: 'Corsa 7 km',
              resultKind: 'quantity',
              targetValue: 10,
              expectedRevision: 0,
              scopeCode: 'only_this',
            }),
          }),
        ],
        retire: [],
      }),
    );
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(reviseDefinition).not.toHaveBeenCalled();
    expect(addObjective).not.toHaveBeenCalled();
  });

  it('keeps following-series scope only for authoritative generated lineage', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [objective],
    });
    loadRecurringContext.mockResolvedValueOnce({ active: true });
    getDefinition.mockResolvedValueOnce({
      ...objective,
      definitionRevision: 1,
    });
    const seriesState = {
      sourceNativeRef: '0199a566-6666-7666-8666-666666666666',
      occurrenceRef: '0199a577-7777-7777-8777-777777777777',
      templateSlot: 0,
      sourceRevision: 2,
      recurrenceStateRef: '0199a588-8888-7888-8888-888888888888',
    };
    getSeriesState.mockResolvedValueOnce(seriesState);
    applyActivityEdits.mockResolvedValueOnce([
      { ...objective, label: 'Corsa 7 km' },
    ]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.focus(
      await screen.findByRole('textbox', { name: 'Nome obiettivo' }),
    );
    fireEvent.click(await screen.findByLabelText('Questa e le prossime'));
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Corsa 7 km' },
    });
    await submitEditor();
    await waitFor(() =>
      expect(applyActivityEdits).toHaveBeenCalledWith(
        ref,
        containing({
          revise: [
            containing({
              objectiveRef: objective.objectiveRef,
              change: containing({
                scopeCode: 'this_and_following',
                seriesState,
                label: 'Corsa 7 km',
              }),
            }),
          ],
        }),
      ),
    );
    expect(addObjective).not.toHaveBeenCalled();
  });

  it('corrects a measured result while keeping the same Objective identity', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [objective],
    });
    correctResult.mockResolvedValueOnce(undefined);
    refreshObjectives.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [
        {
          ...objective,
          observedNumeric: 6,
          assessmentCode: 'not_satisfied',
        },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Correggi risultato' }),
    );
    fireEvent.change(
      screen.getByRole('spinbutton', { name: 'Risultato corretto' }),
      {
        target: { value: '6' },
      },
    );
    fireEvent.click(screen.getByRole('button', { name: 'Salva rettifica' }));
    await waitFor(() =>
      expect(correctResult).toHaveBeenCalledWith(objective.objectiveRef, {
        operationId: anyInstance(String),
        expectedEvaluationStateRef: objective.evaluationStateRef,
        observedBoolean: null,
        observedNumeric: 6,
        qualitativeCode: null,
        assessmentCode: null,
      }),
    );
    expect(reviseDefinition).not.toHaveBeenCalled();
  });
});

describe('Activity Inspector', () => {
  it('offers the next instance when the selected recurring Activity has a registration', async () => {
    get.mockResolvedValue(profile);
    const context = {
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    };
    loadRecurringContext.mockResolvedValueOnce(context);
    loadRecurringPreview.mockResolvedValueOnce({
      fingerprint: 'a'.repeat(32),
      selectedProtection: 'registration',
      targetOccurrenceRefs: [context.occurrenceRef],
      protectedOccurrences: [],
    });
    const onEdit = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={onEdit}
        onDeleted={() => undefined}
        onDuplicate={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    const dialog = await screen.findByRole('dialog', {
      name: 'Ambito modifica ricorrenza',
    });
    expect(dialog.parentElement?.parentElement).toBe(document.body);
    expect(onEdit).not.toHaveBeenCalled();
    fireEvent.click(
      within(dialog).getByRole('button', { name: 'Dalla prossima istanza' }),
    );
    expect(onEdit).toHaveBeenCalledWith(profile, 'from_next');
  });
  it('cancels the recurring scope dialog without opening Edit', async () => {
    get.mockResolvedValue(profile);
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    const onEdit = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={onEdit}
        onDeleted={() => undefined}
        onDuplicate={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Modifica' }));
    const dialog = await screen.findByRole('dialog', {
      name: 'Ambito modifica ricorrenza',
    });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Annulla' }));
    expect(
      screen.queryByRole('dialog', { name: 'Ambito modifica ricorrenza' }),
    ).toBeNull();
    expect(onEdit).not.toHaveBeenCalled();
  });

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
    await waitFor(() =>
      expect(onEdit).toHaveBeenCalledWith(profile, 'only_this'),
    );
    expect(screen.queryByRole('textbox', { name: 'Titolo' })).toBeNull();
  });

  it('saves changes in the editor and returns to the Inspector', async () => {
    saveCore.mockResolvedValue({
      profile: { ...profile, title: 'Dopo', revision: 1 },
      settings: currentSettings,
    });
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
        {
          profile: {
            title: 'Dopo',
            description: 'Nota',
            location: 'Casa',
            colorCode: '#EA5C12',
          },
        },
        expect.any(String),
      ),
    );
    await waitFor(() =>
      expect(onSaved).toHaveBeenCalledWith(
        containing({ title: 'Dopo', revision: 1 }),
      ),
    );
  });

  it('retries one atomic policy change with the same operation ID', async () => {
    saveCore
      .mockRejectedValueOnce(new Error('Connessione interrotta'))
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
    expect(saveCore).toHaveBeenCalledWith(
      profile,
      currentSettings,
      { capture: 'live', reality: 'review_on_end' },
      expect.any(String),
    );
    expect(onSaved).not.toHaveBeenCalled();

    await submitEditor();
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(saveCore).toHaveBeenCalledTimes(2);
    expect(saveCore.mock.calls[1]?.[3]).toBe(saveCore.mock.calls[0]?.[3]);
    expect(revise).not.toHaveBeenCalled();
  });

  it('stages Objective additions and preserves retry identity after one Save error', async () => {
    applyActivityEdits
      .mockRejectedValueOnce(new Error('Errore temporaneo'))
      .mockResolvedValueOnce([
        {
          objectiveRef: 'new-objective',
          label: 'Percorrere 10 km',
          resultKind: 'quantity',
          comparatorCode: 'gte',
          targetValue: 10,
          targetMin: null,
          targetMax: null,
          unitCode: 'km',
          presentationOrder: 0,
          observationRef: null,
          observedBoolean: null,
          observedNumeric: null,
          qualitativeCode: null,
          evaluationStateRef: null,
          assessmentCode: null,
        },
      ]);
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: /Aggiungi obiettivo/ }),
    );
    fireEvent.change(screen.getByRole('textbox', { name: 'Nome obiettivo' }), {
      target: { value: 'Percorrere 10 km' },
    });
    fireEvent.change(screen.getByRole('combobox', { name: 'Tipo obiettivo' }), {
      target: { value: 'quantity' },
    });
    expect(
      screen
        .getByRole('textbox', { name: 'Unità di misura' })
        .closest('.temporal-create-objective')
        ?.classList.contains('is-edit'),
    ).toBe(true);
    fireEvent.change(
      screen.getByRole('spinbutton', { name: 'Valore obiettivo' }),
      { target: { value: '10' } },
    );
    fireEvent.change(screen.getByRole('textbox', { name: 'Unità di misura' }), {
      target: { value: 'km' },
    });
    expect(applyActivityEdits).not.toHaveBeenCalled();
    await submitEditor();
    expect(await screen.findByRole('alert')).toHaveProperty(
      'textContent',
      expect.stringContaining('Errore temporaneo'),
    );
    expect(onSaved).not.toHaveBeenCalled();
    await submitEditor();
    await waitFor(() => expect(applyActivityEdits).toHaveBeenCalledTimes(2));
    const firstAdds = requiredItems(
      requiredRecord(applyActivityEdits.mock.calls[0]?.[1]).add,
    );
    const secondAdds = requiredItems(
      requiredRecord(applyActivityEdits.mock.calls[1]?.[1]).add,
    );
    const firstAdded = requiredRecord(firstAdds[0]);
    const secondAdded = requiredRecord(secondAdds[0]);
    expect(firstAdded.operationId).toEqual(secondAdded.operationId);
    expect(firstAdded).toMatchObject({
      label: 'Percorrere 10 km',
      resultKind: 'quantity',
      comparatorCode: 'gte',
      targetValue: 10,
      unitCode: 'km',
    });
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
  });

  it('removes a staged Objective via X and defers persisted retirement until Save', async () => {
    const unobserved = {
      ...objective,
      observationRef: null,
      evaluationStateRef: null,
      observedNumeric: null,
      assessmentCode: null,
    };
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [unobserved],
    });
    getDefinition.mockResolvedValueOnce({
      ...unobserved,
      definitionRevision: 3,
    });
    applyActivityEdits.mockResolvedValueOnce([]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Rimuovi obiettivo Corsa 10 km',
      }),
    );
    expect(applyActivityEdits).not.toHaveBeenCalled();
    expect(
      screen.queryByRole('button', { name: 'Rimuovi obiettivo Corsa 10 km' }),
    ).toBeNull();
    await submitEditor();
    await waitFor(() =>
      expect(applyActivityEdits).toHaveBeenCalledWith(ref, {
        add: [],
        revise: [],
        retire: [
          containing({
            objectiveRef: objective.objectiveRef,
            expectedRevision: 3,
          }),
        ],
      }),
    );
  });

  it('allows undo of a pending removal before saving', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      objectives: [objective],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Rimuovi obiettivo Corsa 10 km',
      }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Ripristina obiettivi rimossi' }),
    );
    expect(
      screen.getByRole('button', { name: 'Rimuovi obiettivo Corsa 10 km' }),
    ).toBeTruthy();
    expect(applyActivityEdits).not.toHaveBeenCalled();
  });

  it('adds a named Session without a separate time while preserving the protected Activity', async () => {
    const settings = {
      ...currentSettings,
      placementProtected: true,
      placementLockScheduleRef: 'envelope',
      placementLockRevision: 1,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope' as const,
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    applyReplan.mockResolvedValueOnce(settings);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(await screen.findByRole('button', { name: /＋ Sessione/ }));
    const input = await screen.findByRole('textbox', {
      name: 'Nome Sessione',
    });
    fireEvent.change(input, { target: { value: 'Nuova Sessione' } });
    expect(
      screen
        .getByRole('button', { name: 'Orario' })
        .getAttribute('aria-pressed'),
    ).toBe('true');
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          newPlanned: [
            containing({
              name: 'Nuova Sessione',
            }),
          ],
        }),
        expect.any(String),
      ),
    );
    expect(setPlacementProtected).not.toHaveBeenCalled();
  });

  it('saves a planning change directly from Salva modifiche', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'interval',
          role: 'interval',
          name: null,
          order: 1,
          placementStateRef: 'state-1',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([
      {
        scheduleRef: 'interval',
        role: 'interval',
        previousStart: '2026-10-09T09:00:00',
        previousEnd: '2026-10-09T10:00:00',
        proposedStart: '2026-10-09T10:00:00',
        proposedEnd: '2026-10-09T11:00:00',
      },
    ]);
    applyReplan.mockResolvedValueOnce(settings);
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      (
        await screen.findAllByRole('button', { name: 'Inizio: aumenta ora' })
      )[0]!,
    );
    expect(
      screen
        .getAllByRole('group', { name: 'Fine' })[0]!
        .querySelector('.temporal-create-time-raw-input'),
    ).toHaveProperty('value', '10:00');
    fireEvent.click(
      screen.getAllByRole('button', { name: 'Fine: aumenta ora' })[0]!,
    );
    expect(
      screen.queryByRole('button', { name: 'Verifica spostamento' }),
    ).toBeNull();
    await submitEditor();
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
    const placementTimes = requiredRecord(
      requiredRecord(applyReplan.mock.calls[0]?.[2]).times,
    );
    expect(placementTimes.interval).toEqual({
      start: '2026-10-09T10:00',
      end: '2026-10-09T11:00',
    });
    expect(previewReplan).not.toHaveBeenCalled();
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('saves additions and removals of planned Sessions in one action', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'interval',
          role: 'interval',
          name: null,
          order: 1,
          placementStateRef: 'state-1',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'planned',
          role: 'planned',
          name: 'Prima',
          order: 1,
          placementStateRef: 'state-2',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([
      {
        scheduleRef: 'planned',
        clientRef: null,
        role: 'planned_removed',
        previousStart: '2026-10-09T09:00:00',
        previousEnd: '2026-10-09T10:00:00',
        proposedStart: null,
        proposedEnd: null,
      },
    ]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      (await screen.findByRole('textbox', { name: 'Nome Sessione' }))
        .closest('[data-edit-planned-session]')!
        .querySelector('button[aria-label="Rimuovi Sessione"]')!,
    );
    fireEvent.click(screen.getByRole('button', { name: '＋ Sessione' }));
    const newSession = document.querySelector('[data-edit-new-session]')!;
    fireEvent.change(
      newSession.querySelector('[aria-label="Nome Sessione"]')!,
      { target: { value: 'Seconda' } },
    );
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          deletedPlanned: ['planned'],
          newPlanned: [
            containing({
              name: 'Seconda',
            }),
          ],
        }),
        expect.any(String),
      ),
    );
    expect(previewReplan).not.toHaveBeenCalled();
  });

  it('retires an existing planned Session separately from clearing its time', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'planned',
          role: 'planned',
          name: 'Prima',
          order: 1,
          placementStateRef: 'state-2',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    applyReplan.mockResolvedValueOnce({
      ...settings,
      schedules: settings.schedules.filter((row) => row.role !== 'planned'),
    });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const remove = await screen.findByRole('button', {
      name: 'Rimuovi Sessione',
    });
    fireEvent.click(remove);
    expect(screen.queryByRole('textbox', { name: 'Nome Sessione' })).toBeNull();
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          deletedPlanned: ['planned'],
          removedPlanned: [],
        }),
        expect.any(String),
      ),
    );
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('cancels a named Session removal without sending any mutation', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'named',
          role: 'planned',
          name: 'Studio',
          order: 1,
          placementStateRef: null,
          temporalForm: null,
          start: null,
          end: null,
          zoneId: null,
        },
      ],
    });
    const onCancel = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={onCancel}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Rimuovi Sessione' }),
    );
    expect(screen.queryByRole('textbox', { name: 'Nome Sessione' })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    fireEvent.click(screen.getByRole('button', { name: 'Scarta modifiche' }));
    expect(onCancel).toHaveBeenCalledOnce();
    expect(applyReplan).not.toHaveBeenCalled();
    expect(revisePlannedName).not.toHaveBeenCalled();
  });

  it('edits the single overall interval of an Activity without role intervals', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([
      {
        scheduleRef: 'envelope',
        role: 'envelope',
        previousStart: '2026-10-09T09:00:00',
        previousEnd: '2026-10-09T12:00:00',
        proposedStart: '2026-10-09T10:00:00',
        proposedEnd: '2026-10-09T13:00:00',
      },
    ]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Inizio: aumenta ora' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta ora' }));
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          times: containing({
            envelope: { start: '2026-10-09T10:00', end: '2026-10-09T13:00' },
          }),
        }),
        expect.any(String),
      ),
    );
    expect(
      screen.getByRole('button', { name: 'Aggiungi intervallo' }),
    ).toBeTruthy();
  });

  it('converts one timed period to an inclusive all-day date range', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Tutto il giorno' }),
    );
    expect(screen.queryByText('Da collocare')).toBeNull();
    expect(
      screen
        .getByRole('button', { name: 'Tutto il giorno' })
        .getAttribute('aria-pressed'),
    ).toBe('true');
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          dateSpan: { startDate: '2026-10-09', endDateExclusive: '2026-10-10' },
        }),
        expect.any(String),
      ),
    );
  });

  it('splits an existing single period when adding a second interval', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi intervallo' }),
    );
    const row = newIntervalRow();
    expect(
      row.querySelector('.temporal-create-activity-interval__fields'),
    ).toBeTruthy();
    expect(
      within(row).getByRole('button', { name: 'Rimuovi intervallo 2' }),
    ).toBeTruthy();
    for (const label of ['Data inizio', 'Data fine']) {
      fireEvent.click(
        within(row).getByRole('button', { name: new RegExp(`^${label}:`) }),
      );
      fireEvent.click(
        within(screen.getByRole('dialog', { name: label })).getByRole(
          'button',
          { name: '10' },
        ),
      );
    }
    setNewIntervalTime('Inizio', '09');
    setNewIntervalTime('Fine', '10');
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          splitEnvelope: true,
          newIntervals: [
            containing({ start: '2026-10-10T09:00', end: '2026-10-10T10:00' }),
          ],
        }),
        expect.any(String),
      ),
    );
  });

  it('converts an existing all-day period back to a timed period', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'date_span',
          start: '2026-10-09',
          end: '2026-10-11',
          zoneId: null,
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    render(
      <ActivityEditPanel
        profile={profile}
        timeZone="Europe/Rome"
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    expect(
      (
        await screen.findByRole('button', { name: 'Tutto il giorno' })
      ).getAttribute('aria-pressed'),
    ).toBe('true');
    expect(
      screen.queryByRole('button', { name: 'Aggiungi intervallo' }),
    ).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Orario' }));
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          targetZoneId: 'Europe/Rome',
          times: containing({
            envelope: { start: '2026-10-09T09:00', end: '2026-10-09T10:00' },
          }),
        }),
        expect.any(String),
      ),
    );
  });

  it('edits the inclusive final date of an existing all-day period', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'date_span',
          start: '2026-10-09',
          end: '2026-10-11',
          zoneId: null,
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    const { container } = render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(await screen.findByRole('button', { name: /^Data fine:/ }));
    const selected = container.querySelector<HTMLButtonElement>(
      'button[data-temporal-date="2026-10-12"]',
    );
    expect(selected).toBeTruthy();
    fireEvent.click(selected!);
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          dateSpan: { startDate: '2026-10-09', endDateExclusive: '2026-10-13' },
        }),
        expect.any(String),
      ),
    );
  });

  it('marks the incorrect time and leaves Save usable while the interval is invalid', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T21:30:00',
          end: '2026-10-09T22:30:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Fine: diminuisci ora' }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Fine: diminuisci ora' }),
    );
    expect(
      screen.getByRole('button', { name: 'Salva modifiche' }),
    ).toHaveProperty('disabled', false);
    const time = document.querySelector(
      '.timeline-activity-editor__interval-fields',
    )!;
    expect(time.getAttribute('data-edit-invalid')).toBe('true');
    expect(time.textContent).toContain('La fine deve seguire l’inizio.');
    await submitEditor();
    expect(applyReplan).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta ora' }));
    fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta ora' }));
    fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta ora' }));
    expect(time.getAttribute('data-edit-invalid')).toBe('false');
    await submitEditor();
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
  });

  it('keeps a legacy named Session free from its old time when editing the Activity', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'planned',
          role: 'planned',
          name: 'Studio',
          order: 1,
          placementStateRef: 'state-1',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T10:00:00',
          end: '2026-10-09T11:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    await screen.findByRole('textbox', { name: 'Nome Sessione' });
    expect(
      document.querySelector(
        '[data-edit-planned-session] .temporal-create-tree-time-editor',
      ),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Fine Sessione: aumenta ora' }),
    ).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta ora' }));
    await submitEditor();
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
    expect(
      requiredRecord(applyReplan.mock.calls[0]?.[2]).deletedPlanned,
    ).toEqual([]);
  });

  it('retries a failed time save without losing the edited time', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    applyReplan
      .mockRejectedValueOnce(new Error('Connessione interrotta'))
      .mockResolvedValueOnce(settings);
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Fine: aumenta ora' }),
    );
    await submitEditor();
    expect(await screen.findByRole('alert')).toHaveProperty(
      'textContent',
      'Connessione interrotta',
    );
    expect(onSaved).not.toHaveBeenCalled();
    expect(
      screen.getByRole('button', { name: 'Salva modifiche' }),
    ).toHaveProperty('disabled', false);
    await submitEditor();
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
    expect(applyReplan.mock.calls[1]?.[3]).toBe(applyReplan.mock.calls[0]?.[3]);
  });

  it('persists protection from Salva modifiche', async () => {
    const settings = {
      ...currentSettings,
      placementLockScheduleRef: 'envelope',
      placementLockRevision: 2,
    };
    loadSettings.mockResolvedValueOnce(settings);
    setPlacementProtected.mockResolvedValueOnce({
      ...settings,
      placementProtected: true,
      placementLockRevision: 3,
    });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const toggle = await screen.findByRole('button', {
      name: 'Blocca spostamenti',
    });
    fireEvent.click(toggle);
    await submitEditor();
    await waitFor(() =>
      expect(setPlacementProtected).toHaveBeenCalledWith(settings, true),
    );
    await waitFor(() =>
      expect(
        screen
          .getByRole('button', { name: 'Sblocca spostamenti' })
          .getAttribute('aria-pressed'),
      ).toBe('true'),
    );
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('changes Life Area with the accepted assignment revision', async () => {
    const catalog = {
      currentRef: null,
      currentRevision: 0,
      options: [{ ref: 'new-area', name: 'Lavoro' }],
    };
    loadLifeAreaChoice.mockResolvedValueOnce(catalog);
    assignLifeArea.mockResolvedValueOnce({
      ...catalog,
      currentRef: 'new-area',
      currentRevision: 1,
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const area = await screen.findByRole('textbox', { name: 'Area assegnata' });
    fireEvent.change(area, { target: { value: 'Lavoro' } });
    fireEvent.click(screen.getByRole('option', { name: 'Lavoro' }));
    await submitEditor();
    await waitFor(() =>
      expect(assignLifeArea).toHaveBeenCalledWith(
        ref,
        catalog,
        'new-area',
        expect.any(String),
      ),
    );
  });

  it('saves a replacement Activity interval without deleting historical rows', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-0',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'interval',
          role: 'interval',
          name: null,
          order: 1,
          placementStateRef: 'state-1',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([
      {
        scheduleRef: 'interval',
        clientRef: null,
        role: 'interval_removed',
        previousStart: '2026-10-09T09:00:00',
        previousEnd: '2026-10-09T12:00:00',
        proposedStart: null,
        proposedEnd: null,
      },
      {
        scheduleRef: null,
        clientRef: 'new',
        role: 'interval_added',
        previousStart: null,
        previousEnd: null,
        proposedStart: '2026-10-09T10:00:00',
        proposedEnd: '2026-10-09T11:00:00',
      },
    ]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Rimuovi intervallo 1' }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi intervallo' }),
    );
    setNewIntervalTime('Inizio', '10');
    setNewIntervalTime('Fine', '11');
    await submitEditor();
    await waitFor(() =>
      expect(applyReplan).toHaveBeenCalledWith(
        ref,
        settings,
        containing({
          removedIntervals: ['interval'],
          newIntervals: [
            containing({
              start: '2026-10-09T10:00',
              end: '2026-10-09T11:00',
            }),
          ],
        }),
        expect.any(String),
      ),
    );
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

  it('hard-deletes an Activity only after showing real attempts and confirming its fingerprint', async () => {
    const fingerprint = 'b'.repeat(64);
    sessionImpact.mockResolvedValueOnce({
      fingerprint,
      attempts: [
        { sessionRef: 'attempt', status: 'in pausa', plannedScheduleRef: null },
      ],
    });
    deleteHard.mockResolvedValueOnce(undefined);
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
    expect(deleteHard).not.toHaveBeenCalled();
    expect(
      (await screen.findByText(/1 Sessioni registrate/)).textContent,
    ).toContain('in pausa');
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma eliminazione definitiva' }),
    );
    await waitFor(() =>
      expect(deleteHard).toHaveBeenCalledWith(ref, fingerprint),
    );
    expect(retire).not.toHaveBeenCalled();
    expect(onDeleted).toHaveBeenCalledOnce();
  });

  it('cancelling Activity deletion leaves recorded Sessions untouched', async () => {
    sessionImpact.mockResolvedValueOnce({
      fingerprint: 'c'.repeat(64),
      attempts: [
        { sessionRef: 'live', status: 'in corso', plannedScheduleRef: null },
      ],
    });
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Elimina' }));
    await screen.findByRole('button', {
      name: 'Conferma eliminazione definitiva',
    });
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    expect(deleteHard).not.toHaveBeenCalled();
    expect(retire).not.toHaveBeenCalled();
  });

  it('requires an explicit recurring Activity scope and never routes it through one-off deletion', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    });
    const instance = {
      requestedRef: ref,
      scope: 'activity_instance',
      fingerprint: '1'.repeat(64),
    };
    const series = {
      requestedRef: ref,
      scope: 'activity_series',
      fingerprint: '2'.repeat(64),
    };
    previewHardDeletion.mockImplementation((_ref: string, scope: string) =>
      Promise.resolve(scope === 'activity_instance' ? instance : series),
    );
    confirmHardDeletion.mockResolvedValue(undefined);
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
    await screen.findByRole('button', { name: 'Solo questa istanza' });
    expect(screen.getByRole('button', { name: 'Tutta la serie' })).toBeTruthy();
    expect(previewHardDeletion).toHaveBeenCalledWith(ref, 'activity_instance');
    expect(previewHardDeletion).toHaveBeenCalledWith(ref, 'activity_series');
    expect(deleteHard).not.toHaveBeenCalled();
    expect(confirmHardDeletion).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    expect(confirmHardDeletion).not.toHaveBeenCalled();
    expect(onDeleted).not.toHaveBeenCalled();

    loadRecurringContext.mockResolvedValueOnce({
      sourceRef: series.requestedRef,
    });
    fireEvent.click(screen.getByRole('button', { name: 'Elimina' }));
    await screen.findByRole('button', { name: 'Tutta la serie' });
    fireEvent.click(screen.getByRole('button', { name: 'Tutta la serie' }));
    await waitFor(() =>
      expect(confirmHardDeletion).toHaveBeenCalledWith(series),
    );
    expect(confirmHardDeletion).toHaveBeenCalledTimes(1);
    expect(deleteHard).not.toHaveBeenCalled();
    expect(onDeleted).toHaveBeenCalledOnce();
  });

  it('refuses a recurring Activity duplicate instead of silently creating a one-off', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    });
    const onDuplicate = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'duplicazione fedele della ricorrenza',
    );
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('refuses hidden Activity children even when the Timeline has no subitems', async () => {
    loadChildCount.mockResolvedValueOnce(1);
    const onDuplicate = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'contiene sotto-attività',
    );
    expect(loadChildCount).toHaveBeenCalledWith(ref);
    expect(onDuplicate).not.toHaveBeenCalled();
  });

  it('refuses a deceptively incomplete duplicate when an Activity contains children', async () => {
    const onDuplicate = vi.fn();
    render(
      <ActivityInspectorActions
        activityRef={ref}
        subitemsCount={2}
        onEdit={() => undefined}
        onDeleted={() => undefined}
        onDuplicate={onDuplicate}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Duplica' }));
    expect((await screen.findByRole('alert')).textContent).toContain(
      'duplicazione fedele della struttura',
    );
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

  it('saves a planned Session name from the main button', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'planned-m3b',
          role: 'planned',
          name: 'Preparazione',
          order: 0,
          placementStateRef: 'placement-1',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    const name = await screen.findByRole('textbox', { name: 'Nome Sessione' });
    const sessions = document.querySelector(
      '.timeline-activity-editor__sessions',
    )!;
    const title = document.querySelector(
      '.timeline-activity-editor__title-row',
    )!;
    const schedule = document.querySelector(
      '[aria-label="Programmazione attuale"]',
    )!;
    expect(
      title.compareDocumentPosition(sessions) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      sessions.compareDocumentPosition(schedule) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(schedule.querySelector('[data-edit-planned-session]')).toBeNull();
    expect(
      sessions.querySelectorAll('[data-edit-planned-session]'),
    ).toHaveLength(1);
    expect(
      sessions.querySelector('.temporal-create-tree-time-editor'),
    ).toBeNull();
    expect(
      sessions.querySelector(
        'button[aria-controls="edit-session:planned-m3b:time"]',
      ),
    ).toBeNull();
    fireEvent.change(name, { target: { value: 'Preparazione approfondita' } });
    revisePlannedName.mockResolvedValueOnce('Preparazione approfondita');
    await submitEditor();
    await waitFor(() =>
      expect(revisePlannedName).toHaveBeenCalledWith(
        ref,
        'planned-m3b',
        'Preparazione',
        'Preparazione approfondita',
      ),
    );
    expect(saveCore).not.toHaveBeenCalled();
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('renames an untimed named Session without changing its identity or Activity time', async () => {
    const settings = {
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'envelope-state',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'untimed',
          role: 'planned',
          name: 'Studio',
          order: 1,
          placementStateRef: null,
          temporalForm: null,
          start: null,
          end: null,
          zoneId: null,
        },
      ],
    };
    loadSettings.mockResolvedValueOnce(settings);
    previewReplan.mockResolvedValueOnce([]);
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const name = await screen.findByRole('textbox', { name: 'Nome Sessione' });
    expect(
      name
        .closest('[data-edit-planned-session]')
        ?.getAttribute('data-edit-planned-session'),
    ).toBe('untimed');
    expect(
      name
        .closest('[data-edit-planned-session]')
        ?.querySelector('button[aria-controls]'),
    ).toBeNull();
    fireEvent.change(name, { target: { value: 'Studio intenso' } });
    revisePlannedName.mockResolvedValueOnce('Studio intenso');
    await submitEditor();
    await waitFor(() =>
      expect(revisePlannedName).toHaveBeenCalledWith(
        ref,
        'untimed',
        'Studio',
        'Studio intenso',
      ),
    );
    expect(applyReplan).not.toHaveBeenCalled();
  });

  it('does not turn a nonlocal temporal form into a local Schedule during edit', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'absolute-schedule',
          role: 'interval',
          name: null,
          order: 0,
          placementStateRef: 'state-absolute',
          temporalForm: 'absolute_instant',
          start: '2026-10-09T09:00:00Z',
          end: '2026-10-09T10:00:00Z',
          zoneId: null,
        },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    expect(
      await screen.findByText(/DANTE non le converte automaticamente/),
    ).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: 'Verifica spostamento' }),
    ).toBeNull();
    expect(screen.queryByRole('button', { name: '＋ Sessione' })).toBeNull();
    expect(applyReplan).not.toHaveBeenCalled();
  });

  it('saves the planned name and time in the same submission', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'envelope-replan',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'state-envelope',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T08:00:00',
          end: '2026-10-09T11:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'interval-replan',
          role: 'interval',
          name: null,
          order: 0,
          placementStateRef: 'state-interval',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T08:00:00',
          end: '2026-10-09T11:00:00',
          zoneId: 'Europe/Rome',
        },
        {
          scheduleRef: 'planned-replan',
          role: 'planned',
          name: 'Allenamento',
          order: 1,
          placementStateRef: 'state-3',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const name = await screen.findByRole('textbox', { name: 'Nome Sessione' });
    fireEvent.change(name, { target: { value: 'Allenamento lungo' } });
    fireEvent.click(
      screen.getAllByRole('button', { name: 'Inizio: diminuisci ora' })[0]!,
    );
    revisePlannedName.mockResolvedValueOnce('Allenamento lungo');
    await submitEditor();
    await waitFor(() => expect(applyReplan).toHaveBeenCalledOnce());
    await waitFor(() =>
      expect(revisePlannedName).toHaveBeenCalledWith(
        ref,
        'planned-replan',
        'Allenamento',
        'Allenamento lungo',
      ),
    );
    expect(previewReplan).not.toHaveBeenCalled();
  });

  it('discloses selected-only owner-domain editing even with no metadata change', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    });
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'planned-recurring',
          role: 'planned',
          name: 'Preparazione',
          order: 0,
          placementStateRef: 'placement-2',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.change(
      await screen.findByRole('textbox', { name: 'Nome Sessione' }),
      {
        target: { value: 'Ripasso' },
      },
    );
    expect(await screen.findByText('Solo questa istanza')).toBeTruthy();
    expect(screen.queryByText('Questa e le successive')).toBeNull();
    expect(
      screen.getByRole('button', { name: 'Salva modifiche' }),
    ).toHaveProperty('disabled', false);
    expect(saveRecurringProfile).not.toHaveBeenCalled();
  });

  it('never offers a following-series Life Area edit without a source-policy capability', async () => {
    loadRecurringContext.mockResolvedValueOnce({
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    });
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      lifeAreaRef: 'area-1',
    });
    loadLifeAreaChoice.mockResolvedValueOnce({
      currentRef: 'area-1',
      currentRevision: 2,
      options: [{ ref: 'area-1', name: 'Lavoro' }],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Rimuovi Life Area' }),
    );
    expect(await screen.findByText('Solo questa istanza')).toBeTruthy();
    expect(screen.queryByText('Questa e le successive')).toBeNull();
    expect(assignLifeArea).not.toHaveBeenCalled();
    expect(saveRecurringProfile).not.toHaveBeenCalled();
  });

  it('refuses a mixed series title and Life Area save before any instance write', async () => {
    const context = {
      occurrenceRef: '0199a222-2222-7222-8222-222222222222',
      sourceRef: '0199a444-4444-7444-8444-444444444444',
      editRevision: 3,
      recurrenceStateRef: null,
    };
    loadRecurringContext.mockResolvedValueOnce(context);
    loadRecurringPreview.mockResolvedValueOnce({
      fingerprint: 'a'.repeat(32),
      selectedProtection: null,
      targetOccurrenceRefs: [context.occurrenceRef],
      protectedOccurrences: [],
    });
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      lifeAreaRef: 'area-1',
    });
    loadLifeAreaChoice.mockResolvedValueOnce({
      currentRef: 'area-1',
      currentRevision: 2,
      options: [{ ref: 'area-1', name: 'Lavoro' }],
    });
    render(
      <ActivityEditPanel
        profile={profile}
        initialScope="this_and_following"
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    fireEvent.change(await screen.findByRole('textbox', { name: 'Titolo' }), {
      target: { value: 'Nuovo titolo' },
    });
    fireEvent.click(
      await screen.findByRole('button', { name: 'Rimuovi Life Area' }),
    );
    await submitEditor();
    expect((await screen.findByRole('alert')).textContent).toContain(
      'non è ancora disponibile',
    );
    expect(assignLifeArea).not.toHaveBeenCalled();
    expect(saveRecurringProfile).not.toHaveBeenCalled();
  });

  it('unassigns an existing Life Area using an explicit null target', async () => {
    const catalog = {
      currentRef: 'area-1',
      currentRevision: 4,
      options: [{ ref: 'area-1', name: 'Personale' }],
    };
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      lifeAreaRef: 'area-1',
    });
    loadLifeAreaChoice.mockResolvedValueOnce(catalog);
    assignLifeArea.mockResolvedValueOnce({
      ...catalog,
      currentRef: null,
      currentRevision: 5,
    });
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    await screen.findByRole('textbox', { name: 'Area assegnata' });
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi Life Area' }));
    await submitEditor();
    await waitFor(() =>
      expect(assignLifeArea).toHaveBeenCalledWith(
        ref,
        catalog,
        null,
        expect.any(String),
      ),
    );
  });

  it('creates and assigns a new Life Area while saving the Activity', async () => {
    const catalog = { currentRef: null, currentRevision: 0, options: [] };
    loadLifeAreaChoice.mockResolvedValueOnce(catalog);
    createLifeArea.mockResolvedValueOnce({
      ref: 'area-new',
      name: 'Studio',
      revision: 1,
      iconCode: null,
      colorCode: null,
    });
    setLifeAreaAppearance.mockResolvedValueOnce({
      ref: 'area-new',
      name: 'Studio',
      revision: 2,
      colorCode: '#EA5C12',
      iconCode: null,
    });
    assignLifeArea.mockResolvedValueOnce({
      currentRef: 'area-new',
      currentRevision: 1,
      options: [
        {
          ref: 'area-new',
          name: 'Studio',
          revision: 2,
          iconCode: null,
          colorCode: '#EA5C12',
        },
      ],
    });
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
      await screen.findByRole('textbox', { name: 'Area assegnata' }),
      { target: { value: 'Studio' } },
    );
    expect(screen.getByText(/La nuova Life Area verrà creata/)).toBeTruthy();
    await submitEditor();
    await waitFor(() =>
      expect(createLifeArea).toHaveBeenCalledWith('Studio', expect.any(String)),
    );
    expect(setLifeAreaAppearance).toHaveBeenCalledWith(
      containing({ ref: 'area-new', revision: 1 }),
      '#EA5C12',
      expect.any(String),
    );
    expect(assignLifeArea).toHaveBeenCalledWith(
      ref,
      containing({
        currentRevision: 0,
        options: [
          containing({
            ref: 'area-new',
            revision: 2,
            colorCode: '#EA5C12',
          }),
        ],
      }),
      'area-new',
      expect.any(String),
    );
    expect(onSaved).toHaveBeenCalledWith(profile);
  });

  it('changes the persisted Life Area color without rewriting its assignment', async () => {
    const area = {
      ref: 'area-1',
      name: 'Lavoro',
      revision: 1,
      iconCode: null,
      colorCode: null,
    };
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      lifeAreaRef: 'area-1',
    });
    loadLifeAreaChoice.mockResolvedValueOnce({
      currentRef: 'area-1',
      currentRevision: 1,
      options: [area],
    });
    setLifeAreaAppearance.mockResolvedValueOnce({
      ...area,
      revision: 2,
      colorCode: '#33B679',
    });
    const onSaved = vi.fn();
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={onSaved}
        onCancel={() => undefined}
      />,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Colore Life Area' }),
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Verde menta' }));
    await submitEditor();
    await waitFor(() =>
      expect(setLifeAreaAppearance).toHaveBeenCalledWith(
        area,
        '#33B679',
        expect.any(String),
      ),
    );
    expect(assignLifeArea).not.toHaveBeenCalled();
    await waitFor(() => expect(onSaved).toHaveBeenCalledWith(profile));
  });

  it('renames an existing planned Session without rescheduling it', async () => {
    loadSettings.mockResolvedValueOnce({
      ...currentSettings,
      schedules: [
        {
          scheduleRef: 'planned',
          role: 'planned',
          name: 'Lettura',
          order: 1,
          placementStateRef: 'state-planned',
          temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00',
          end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    });
    revisePlannedName.mockResolvedValueOnce('Ripasso');
    render(
      <ActivityEditPanel
        profile={profile}
        closeRequestRef={createRef()}
        onSaved={() => undefined}
        onCancel={() => undefined}
      />,
    );
    const field = await screen.findByRole('textbox', { name: 'Nome Sessione' });
    fireEvent.change(field, { target: { value: 'Ripasso' } });
    await submitEditor();
    await waitFor(() =>
      expect(revisePlannedName).toHaveBeenCalledWith(
        ref,
        'planned',
        'Lettura',
        'Ripasso',
      ),
    );
    expect(applyReplan).not.toHaveBeenCalled();
  });
});
