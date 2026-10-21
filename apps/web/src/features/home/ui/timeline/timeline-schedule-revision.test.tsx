import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import {
  afterEach,
  beforeAll,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type {
  ActivityEditSettings,
  ActivityReplanDraft,
} from '../../../temporal/remote-activity-edit-settings';
import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import { createDeterministicTemporalIdFactory } from '../../../temporal/model';
import type { TemporalScheduleDataSource } from '../../../temporal/schedule-data-source';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from '../../../temporal/timeline-read';
import { TemporalTimelineRuntimeBoundary } from '../../../temporal/timeline-runtime-boundary';
import { TimelineSurface } from './timeline-surface';

vi.mock('./activity-edit-panel', () => ({
  ActivityEditPanel: ({
    onCancel,
    initialScope,
  }: {
    onCancel: () => void;
    initialScope?: string;
  }) => (
    <div data-testid="activity-edit-panel" data-scope={initialScope}>
      Modifica attività
      <button type="button" onClick={onCancel}>
        Chiudi modifica di test
      </button>
    </div>
  ),
}));

const remote = vi.hoisted(() => ({
  load: vi.fn(),
  applyReplan: vi.fn(),
  sessionImpact: vi.fn(),
  get: vi.fn(),
  loadRecurring: vi.fn(),
  loadRecurringPreview: vi.fn(),
}));
vi.mock('../../../temporal/remote-activity-edit-settings', () => ({
  createRemoteActivityEditSettings: () => ({
    load: remote.load,
    applyReplan: remote.applyReplan,
  }),
}));
vi.mock('../../../temporal/remote-activity-inspector', () => ({
  createRemoteActivityInspector: () => ({
    sessionImpact: remote.sessionImpact,
    get: remote.get,
  }),
}));
vi.mock('../../../temporal/remote-recurring-profile-edit', () => ({
  createRemoteRecurringProfileEdit: () => ({
    loadActivityContext: remote.loadRecurring,
    loadPreview: remote.loadRecurringPreview,
  }),
}));

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const CURRENT_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';
const NEXT_STATE_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const fingerprint = 'a'.repeat(64);

function settings(): ActivityEditSettings {
  return {
    capture: { mode: 'live', stateRef: null },
    reality: { mode: 'manual', stateRef: null },
    schedules: [
      {
        scheduleRef: SCHEDULE_REF,
        role: 'envelope',
        name: null,
        order: 1,
        placementStateRef: CURRENT_STATE_REF,
        temporalForm: 'floating_local',
        start: '2026-09-09T10:00:00',
        end: '2026-09-09T11:00:00',
        zoneId: null,
      },
    ],
    objectives: [],
    lifeAreaRef: null,
    placementProtected: false,
    placementLockRevision: null,
    placementLockScheduleRef: null,
    reminderLeadMinutes: null,
    reminderScheduleRef: null,
    reminderStateRef: null,
    childGuardMode: 'none',
  };
}

function windowAt(
  start: string,
  end: string,
  state: string,
  placementLocked = false,
): TemporalTimelineWindow {
  return {
    kind: 'window',
    startDate: '2026-09-02',
    endDateExclusive: '2026-10-15',
    effectiveZoneId: 'Europe/Rome',
    items: [
      {
        kind: 'scheduled_activity',
        activityRef: ACTIVITY_REF,
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef: state,
        placementLocked,
        title: 'Attività coordinata',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from(start),
        endsLocalAt: Temporal.PlainDateTime.from(end),
      },
    ],
  };
}

function renderTimeline(placementLocked = false) {
  const loadWindow = vi
    .fn<TemporalTimelineDataSource['loadWindow']>()
    .mockResolvedValueOnce(
      windowAt(
        '2026-09-09T10:00',
        '2026-09-09T11:00',
        CURRENT_STATE_REF,
        placementLocked,
      ),
    )
    .mockResolvedValue(
      windowAt(
        '2026-09-09T10:15',
        '2026-09-09T11:15',
        NEXT_STATE_REF,
        placementLocked,
      ),
    );
  const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>();
  const scheduleDataSource: TemporalScheduleDataSource = {
    reviseSchedule,
    unscheduleSchedule: vi.fn(),
    undoScheduleUnschedule: vi.fn(),
  };
  const view = render(
    <TemporalTimelineRuntimeBoundary
      viewedDateIso="2026-09-09"
      dataSource={{ loadWindow }}
      scheduleDataSource={scheduleDataSource}
      ids={createDeterministicTemporalIdFactory('activity-timeline-replan')}
      mode="production"
    >
      <TimelineSurface
        expanded={false}
        viewedDateIso="2026-09-09"
        onExpandedChange={vi.fn()}
        onExpansionProgress={vi.fn()}
      />
    </TemporalTimelineRuntimeBoundary>,
  );
  return { ...view, loadWindow, reviseSchedule };
}

async function moveCard(container: HTMLElement) {
  const card = await waitFor(() => {
    const found = container.querySelector<HTMLElement>(
      `[data-timeline-event="${SCHEDULE_REF}"]`,
    );
    expect(found).toBeTruthy();
    return found!;
  });
  fireEvent.keyDown(card, { key: 'ArrowDown', altKey: true });
  return card;
}

async function dragCard(container: HTMLElement, sameSlot = false) {
  const card = await waitFor(() => {
    const found = container.querySelector<HTMLElement>(
      `[data-timeline-event="${SCHEDULE_REF}"]`,
    );
    expect(found).toBeTruthy();
    return found!;
  });
  const sections = Array.from(
    container.querySelectorAll<HTMLElement>('.timeline-day-section'),
  );
  const cardSection = card.closest<HTMLElement>('.timeline-day-section');
  const sectionIndex = sections.findIndex((section) => section === cardSection);
  const paintedTop =
    sections
      .slice(0, sectionIndex)
      .reduce((sum, section) => sum + parseFloat(section.style.height), 0) +
    parseFloat(card.style.top) -
    (container.querySelector<HTMLElement>('.timeline-grid')?.scrollTop ?? 0);
  const cardTop = sameSlot ? paintedTop : 120;
  const startY = cardTop + (sameSlot ? 20 : 0);
  const endY = sameSlot ? startY : 190;
  vi.spyOn(card, 'getBoundingClientRect').mockReturnValue({
    left: 100,
    right: 300,
    top: cardTop,
    bottom: cardTop + 80,
    width: 200,
    height: 80,
    x: 100,
    y: cardTop,
    toJSON: () => ({}),
  });
  const pointer = (
    type: string,
    target: Document | HTMLElement,
    clientY: number,
    clientX: number,
  ) => {
    const event = new MouseEvent(type, {
      bubbles: true,
      cancelable: true,
      button: 0,
      clientX,
      clientY,
    });
    Object.defineProperties(event, {
      pointerId: { value: 3 },
      pointerType: { value: 'mouse' },
      isPrimary: { value: true },
    });
    fireEvent(target, event);
  };
  pointer('pointerdown', card, startY, 140);
  pointer('pointermove', document, endY, sameSlot ? 160 : 140);
  pointer('pointerup', document, endY, sameSlot ? 160 : 140);
  return card;
}

beforeAll(async () => {
  await i18n.changeLanguage('it');
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    value: 1440,
    writable: true,
  });
});
beforeEach(() => {
  remote.get.mockReset().mockResolvedValue({
    activityRef: ACTIVITY_REF,
    title: 'Attività coordinata',
    description: null,
    location: null,
    colorCode: null,
    revision: 0,
  });
  remote.load.mockReset().mockResolvedValue(settings());
  remote.sessionImpact
    .mockReset()
    .mockResolvedValue({ fingerprint, attempts: [] });
  remote.loadRecurring.mockReset().mockResolvedValue(null);
  remote.loadRecurringPreview.mockReset().mockResolvedValue({
    fingerprint: 'a'.repeat(32),
    selectedProtection: null,
    targetOccurrenceRefs: [],
    protectedOccurrences: [],
  });
  remote.applyReplan.mockReset().mockImplementation((_ref, current, draft) => {
    invalidateTemporalTimelineRead();
    const next = draft as ActivityReplanDraft;
    const original = current as ActivityEditSettings;
    return Promise.resolve({
      ...original,
      schedules: original.schedules.map((row) => ({
        ...row,
        placementStateRef: NEXT_STATE_REF,
        start: next.times[row.scheduleRef]?.start ?? row.start,
        end: next.times[row.scheduleRef]?.end ?? row.end,
      })),
    });
  });
});
afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

describe('Activity Timeline coordinated replan', () => {
  it('moves through the whole Activity plan and waits for accepted current truth', async () => {
    const { container, loadWindow, reviseSchedule } = renderTimeline();
    const card = await moveCard(container);
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    expect(remote.load).toHaveBeenCalledWith(ACTIVITY_REF);
    expect(remote.applyReplan.mock.calls[0]?.slice(0, 3)).toEqual([
      ACTIVITY_REF,
      settings(),
      {
        times: {
          [SCHEDULE_REF]: {
            start: '2026-09-09T10:15:00',
            end: '2026-09-09T11:15:00',
          },
        },
        removedIntervals: [],
        newIntervals: [],
        removedPlanned: [],
        deletedPlanned: [],
        newPlanned: [],
      },
    ]);
    expect(remote.applyReplan.mock.calls[0]?.[4]).toBeUndefined();
    expect(reviseSchedule).not.toHaveBeenCalled();
    expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(2));
    await waitFor(() =>
      expect(
        container
          .querySelector<HTMLElement>(`[data-timeline-event="${SCHEDULE_REF}"]`)
          ?.getAttribute('aria-label'),
      ).toContain('10:15–11:15'),
    );
    const confirmation = await screen.findByText(
      'Attività riprogrammata per 9 set, 10:15–11:15',
    );
    expect(confirmation.parentElement?.getAttribute('role')).toBe('status');
    expect(
      confirmation.parentElement?.querySelector('button')?.textContent,
    ).toBe('Annulla');
    expect(container.querySelector('.timeline-move-toast.is-on')).toBeNull();
  });

  it.each([
    ['principale', null, 'in corso'],
    ['interna', 'planned-1', 'in pausa'],
    ['conclusa', null, 'conclusa'],
  ])(
    'opens Edit after a drag with a %s registration and does not move the plan',
    async (_label, plannedScheduleRef, status) => {
      remote.sessionImpact.mockResolvedValue({
        fingerprint,
        attempts: [
          {
            sessionRef: 'session-1',
            plannedScheduleRef,
            timingMaterialStateRef: 'state-1',
            status,
          },
        ],
      });
      const { container, reviseSchedule } = renderTimeline();
      const card = await moveCard(container);
      await screen.findByTestId('activity-edit-panel');
      expect(remote.applyReplan).not.toHaveBeenCalled();
      expect(reviseSchedule).not.toHaveBeenCalled();
      expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    },
  );

  it('asks for the recurring scope before opening Edit after a recorded drag', async () => {
    remote.loadRecurring.mockResolvedValue({
      occurrenceRef: 'occurrence-1',
      sourceRef: 'routine-1',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    remote.sessionImpact.mockResolvedValue({
      fingerprint,
      attempts: [
        {
          sessionRef: 'session-1',
          plannedScheduleRef: null,
          timingMaterialStateRef: 'state-1',
          status: 'in corso',
        },
      ],
    });
    const { container } = renderTimeline();
    await dragCard(container);
    const scope = await screen.findByRole('dialog', {
      name: 'Modifica ricorrenza',
    });
    expect(scope.textContent).toContain('Solo questa istanza');
    expect(screen.queryByTestId('activity-edit-panel')).toBeNull();
    fireEvent.click(
      within(scope).getByRole('button', { name: 'Solo questa istanza' }),
    );
    await screen.findByTestId('activity-edit-panel');
    expect(remote.applyReplan).not.toHaveBeenCalled();
  });

  it('closes the Inspector when a recorded drag scope choice is cancelled', async () => {
    remote.loadRecurring.mockResolvedValue({
      occurrenceRef: 'occurrence-1',
      sourceRef: 'routine-1',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    remote.sessionImpact.mockResolvedValue({
      fingerprint,
      attempts: [
        {
          sessionRef: 'session-1',
          plannedScheduleRef: null,
          timingMaterialStateRef: 'state-1',
          status: 'in corso',
        },
      ],
    });
    const { container } = renderTimeline();
    await dragCard(container);
    const scope = await screen.findByRole('dialog', {
      name: 'Modifica ricorrenza',
    });
    fireEvent.click(within(scope).getByRole('button', { name: 'Annulla' }));
    await waitFor(() =>
      expect(
        screen.queryByRole('dialog', { name: 'Modifica ricorrenza' }),
      ).toBeNull(),
    );
    expect(
      screen.queryByRole('button', { name: 'Chiudi Inspector' }),
    ).toBeNull();
    expect(remote.applyReplan).not.toHaveBeenCalled();
  });

  it.each([
    ['principale conclusa', null, 'conclusa'],
    ['sola sottosessione attiva', 'planned-1', 'in corso'],
  ])(
    'routes a pointer drag to Edit with a %s',
    async (_label, plannedScheduleRef, status) => {
      remote.sessionImpact.mockResolvedValue({
        fingerprint,
        attempts: [
          {
            sessionRef: 'session-1',
            plannedScheduleRef,
            timingMaterialStateRef: 'state-1',
            status,
          },
        ],
      });
      const { container, reviseSchedule } = renderTimeline();
      await dragCard(container);
      await screen.findByTestId('activity-edit-panel');
      expect(remote.applyReplan).not.toHaveBeenCalled();
      expect(reviseSchedule).not.toHaveBeenCalled();
    },
  );

  it('opens Edit for a recorded Activity even when its placement is manually locked', async () => {
    remote.sessionImpact.mockResolvedValue({
      fingerprint,
      attempts: [
        {
          sessionRef: 'session-1',
          plannedScheduleRef: 'planned-1',
          timingMaterialStateRef: 'state-1',
          status: 'in pausa',
        },
      ],
    });
    const { container } = renderTimeline(true);
    await dragCard(container);
    await screen.findByTestId('activity-edit-panel');
    expect(remote.applyReplan).not.toHaveBeenCalled();
  });

  it('still refuses replanning a manually locked Activity without recordings', async () => {
    const { container } = renderTimeline(true);
    await dragCard(container);
    const notice = await screen.findByRole('alert');
    expect(notice.textContent).toContain(
      'Sblocca gli spostamenti prima di modificare l’orario.',
    );
    expect(remote.applyReplan).not.toHaveBeenCalled();
  });

  it.each([false, true])(
    'does not persist an unchanged snapped slot (recorded: %s)',
    async (recorded) => {
      if (recorded) {
        remote.sessionImpact.mockResolvedValue({
          fingerprint,
          attempts: [
            {
              sessionRef: 'session-1',
              plannedScheduleRef: null,
              timingMaterialStateRef: 'state-1',
              status: 'conclusa',
            },
          ],
        });
      }
      const { container } = renderTimeline();
      await dragCard(container, true);
      if (recorded) {
        await screen.findByTestId('activity-edit-panel');
      } else {
        await waitFor(() =>
          expect(remote.sessionImpact).toHaveBeenCalledOnce(),
        );
        expect(screen.queryByTestId('activity-edit-panel')).toBeNull();
      }
      expect(remote.applyReplan).not.toHaveBeenCalled();
    },
  );

  it.each([
    ['principale conclusa', null, 'conclusa'],
    ['sola sottosessione attiva', 'planned-1', 'in corso'],
  ])(
    'opens Edit again after a prior drag when the remaining registration is %s',
    async (_label, plannedScheduleRef, status) => {
      remote.sessionImpact.mockResolvedValueOnce({
        fingerprint,
        attempts: [
          {
            sessionRef: 'session-1',
            plannedScheduleRef: null,
            timingMaterialStateRef: 'state-1',
            status: 'in corso',
          },
        ],
      });
      remote.sessionImpact.mockResolvedValue({
        fingerprint,
        attempts: [
          {
            sessionRef: 'session-2',
            plannedScheduleRef,
            timingMaterialStateRef: 'state-2',
            status,
          },
        ],
      });
      const { container, reviseSchedule } = renderTimeline();
      await moveCard(container);
      await screen.findByTestId('activity-edit-panel');
      fireEvent.click(
        screen.getByRole('button', { name: 'Chiudi modifica di test' }),
      );
      fireEvent.click(
        await screen.findByRole('button', { name: 'Chiudi Inspector' }),
      );
      await waitFor(() =>
        expect(screen.queryByTestId('activity-edit-panel')).toBeNull(),
      );

      await moveCard(container);
      await waitFor(() =>
        expect(remote.sessionImpact).toHaveBeenCalledTimes(2),
      );
      await screen.findByTestId('activity-edit-panel');
      expect(remote.applyReplan).not.toHaveBeenCalled();
      expect(reviseSchedule).not.toHaveBeenCalled();
    },
  );

  it('asks for the recurring scope before moving an unrecorded instance', async () => {
    remote.loadRecurring.mockResolvedValue({
      occurrenceRef: 'occurrence-1',
      sourceRef: 'routine-1',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    const { container, reviseSchedule } = renderTimeline();
    await moveCard(container);
    const dialog = await screen.findByRole('dialog', {
      name: 'Modifica ricorrenza',
    });
    expect(dialog.textContent).toContain('Questa e le successive');
    expect(remote.applyReplan).not.toHaveBeenCalled();
    fireEvent.click(
      within(dialog).getByRole('button', { name: 'Solo questa istanza' }),
    );
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    expect(reviseSchedule).not.toHaveBeenCalled();
  });

  it('opens series Edit without silently applying a drag to one instance', async () => {
    remote.loadRecurring.mockResolvedValue({
      occurrenceRef: 'occurrence-1',
      sourceRef: 'routine-1',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    const { container } = renderTimeline();
    await moveCard(container);
    const dialog = await screen.findByRole('dialog', {
      name: 'Modifica ricorrenza',
    });
    expect(dialog.textContent).toContain('il trascinamento non verrà salvato');
    fireEvent.click(
      within(dialog).getByRole('button', { name: 'Questa e le successive' }),
    );
    const editor = await screen.findByTestId('activity-edit-panel');
    expect(editor.getAttribute('data-scope')).toBe('this_and_following');
    expect(remote.applyReplan).not.toHaveBeenCalled();
  });

  it('Undo coordinates the prior Activity times from the new revision basis', async () => {
    const { container, reviseSchedule } = renderTimeline();
    await moveCard(container);
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(2));
    expect(
      (remote.applyReplan.mock.calls[1]?.[1] as ActivityEditSettings)
        .schedules[0]?.placementStateRef,
    ).toBe(NEXT_STATE_REF);
    expect(
      (remote.applyReplan.mock.calls[1]?.[2] as ActivityReplanDraft).times[
        SCHEDULE_REF
      ],
    ).toEqual({
      start: '2026-09-09T10:00:00',
      end: '2026-09-09T11:00:00',
    });
    expect(reviseSchedule).not.toHaveBeenCalled();
  });
});
