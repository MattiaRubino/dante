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

const remote = vi.hoisted(() => ({
  load: vi.fn(),
  applyReplan: vi.fn(),
  sessionImpact: vi.fn(),
  loadRecurring: vi.fn(),
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
  }),
}));
vi.mock('../../../temporal/remote-recurring-profile-edit', () => ({
  createRemoteRecurringProfileEdit: () => ({
    loadActivityContext: remote.loadRecurring,
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
        title: 'Attività coordinata',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from(start),
        endsLocalAt: Temporal.PlainDateTime.from(end),
      },
    ],
  };
}

function renderTimeline() {
  const loadWindow = vi
    .fn<TemporalTimelineDataSource['loadWindow']>()
    .mockResolvedValueOnce(
      windowAt('2026-09-09T10:00', '2026-09-09T11:00', CURRENT_STATE_REF),
    )
    .mockResolvedValue(
      windowAt('2026-09-09T10:05', '2026-09-09T11:05', NEXT_STATE_REF),
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

beforeAll(async () => {
  await i18n.changeLanguage('it');
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    value: 1440,
    writable: true,
  });
});
beforeEach(() => {
  remote.load.mockReset().mockResolvedValue(settings());
  remote.sessionImpact
    .mockReset()
    .mockResolvedValue({ fingerprint, attempts: [] });
  remote.loadRecurring.mockReset().mockResolvedValue(null);
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
            start: '2026-09-09T10:05:00',
            end: '2026-09-09T11:05:00',
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
      ).toContain('10:05–11:05'),
    );
  });

  it('asks Keep/Delete/Cancel for real attempts before any write, and passes the fresh fingerprint', async () => {
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
    const { container, reviseSchedule } = renderTimeline();
    await moveCard(container);
    const confirmation = await screen.findByRole('alertdialog', {
      name: 'Conferma spostamento attività',
    });
    expect(remote.applyReplan).not.toHaveBeenCalled();
    fireEvent.click(
      within(confirmation).getByRole('button', { name: 'Annulla' }),
    );
    expect(remote.applyReplan).not.toHaveBeenCalled();
    await moveCard(container);
    fireEvent.click(
      await screen.findByRole('button', { name: 'Mantieni Sessioni' }),
    );
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    expect(remote.applyReplan.mock.calls[0]?.[4]).toEqual({
      mode: 'keep',
      expectedFingerprint: fingerprint,
    });
    expect(reviseSchedule).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    const undoConfirmation = await screen.findByRole('alertdialog', {
      name: 'Conferma spostamento attività',
    });
    expect(remote.applyReplan).toHaveBeenCalledTimes(1);
    fireEvent.click(
      within(undoConfirmation).getByRole('button', {
        name: 'Mantieni Sessioni',
      }),
    );
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(2));
    expect(remote.applyReplan.mock.calls[1]?.[4]).toEqual({
      mode: 'keep',
      expectedFingerprint: fingerprint,
    });
  });

  it('offers Delete, but a rejected coordinated mutation leaves the old card and does not reload', async () => {
    remote.sessionImpact.mockResolvedValue({
      fingerprint,
      attempts: [
        {
          sessionRef: 'session-2',
          plannedScheduleRef: null,
          timingMaterialStateRef: 'state-2',
          status: 'conclusa',
        },
      ],
    });
    remote.applyReplan.mockRejectedValue(
      new Error('Session attempts changed. Reload before confirming.'),
    );
    const { container, loadWindow } = renderTimeline();
    const card = await moveCard(container);
    fireEvent.click(
      await screen.findByRole('button', { name: 'Elimina Sessioni' }),
    );
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    expect(remote.applyReplan.mock.calls[0]?.[4]).toEqual({
      mode: 'delete',
      expectedFingerprint: fingerprint,
    });
    expect(
      await screen.findByText(
        'Session attempts changed. Reload before confirming.',
      ),
    ).toBeTruthy();
    expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    expect(loadWindow).toHaveBeenCalledTimes(1);
  });

  it('requires explicit single-instance scope for a recurring Activity, even without attempts', async () => {
    remote.loadRecurring.mockResolvedValue({
      occurrenceRef: 'occurrence-1',
      sourceRef: 'routine-1',
      editRevision: 0,
      recurrenceStateRef: null,
    });
    const { container, reviseSchedule } = renderTimeline();
    await moveCard(container);
    const dialog = await screen.findByRole('alertdialog', {
      name: 'Conferma spostamento attività',
    });
    expect(dialog.textContent).toContain('solo questa istanza');
    expect(remote.applyReplan).not.toHaveBeenCalled();
    fireEvent.click(
      within(dialog).getByRole('button', { name: 'Solo questa' }),
    );
    await waitFor(() => expect(remote.applyReplan).toHaveBeenCalledTimes(1));
    expect(reviseSchedule).not.toHaveBeenCalled();
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
