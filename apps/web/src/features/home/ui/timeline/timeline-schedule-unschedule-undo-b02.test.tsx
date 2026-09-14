import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createDeterministicTemporalIdFactory } from '../../../temporal/model';
import type { TemporalScheduleDataSource } from '../../../temporal/schedule-data-source';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from '../../../temporal/timeline-read';
import { TemporalTimelineRuntimeBoundary } from '../../../temporal/timeline-runtime-boundary';
import { TimelineSurface } from './timeline-surface';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const CURRENT_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';
const RESTORED_STATE_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';

beforeAll(async () => {
  await i18n.changeLanguage('it');
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    value: 1440,
    writable: true,
  });
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

function scheduledWindow(
  placementMaterialStateRef: string,
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
        placementMaterialStateRef,
        title: 'Governed B02-D',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T10:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T11:00'),
      },
    ],
  };
}

function emptyWindow(): TemporalTimelineWindow {
  return {
    kind: 'empty',
    startDate: '2026-09-02',
    endDateExclusive: '2026-10-15',
    effectiveZoneId: 'Europe/Rome',
  };
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((resolvePromise) => {
    resolve = resolvePromise;
  });
  return { promise, resolve };
}

describe('B02-D governed Schedule unschedule and Undo', () => {
  it('waits for authoritative absence, then restores through a new state', async () => {
    const unscheduledWindow = deferred<TemporalTimelineWindow>();
    const restoredWindow = deferred<TemporalTimelineWindow>();
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockResolvedValueOnce(scheduledWindow(CURRENT_STATE_REF))
      .mockImplementationOnce(() => unscheduledWindow.promise)
      .mockImplementationOnce(() => restoredWindow.promise);
    const unscheduleSchedule = vi.fn<
      TemporalScheduleDataSource['unscheduleSchedule']
    >((request) =>
      Promise.resolve({
        scheduleRef: request.scheduleRef,
        previousPlacementMaterialStateRef:
          request.expectedPlacementMaterialStateRef,
        unscheduleOperationId: request.operationId,
        replayed: false,
      }),
    );
    const undoScheduleUnschedule = vi.fn<
      TemporalScheduleDataSource['undoScheduleUnschedule']
    >((request) =>
      Promise.resolve({
        scheduleRef: request.scheduleRef,
        restoredFromPlacementMaterialStateRef: CURRENT_STATE_REF,
        placementMaterialStateRef: RESTORED_STATE_REF,
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T10:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T11:00'),
        },
        replayed: false,
      }),
    );
    const scheduleDataSource: TemporalScheduleDataSource = {
      reviseSchedule: vi.fn(() => Promise.reject(new Error('not expected'))),
      unscheduleSchedule,
      undoScheduleUnschedule,
    };

    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={{ loadWindow }}
        scheduleDataSource={scheduleDataSource}
        ids={createDeterministicTemporalIdFactory('b02-d-ui')}
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
    const card = await waitFor(() => {
      const match = container.querySelector<HTMLElement>(
        `[data-timeline-event="${SCHEDULE_REF}"]`,
      );
      expect(match).toBeTruthy();
      return match as HTMLElement;
    });

    fireEvent.click(card);
    fireEvent.click(
      await screen.findByRole('button', { name: 'Governed B02-D' }),
    );
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Riporta nel Planning Tray',
      }),
    );

    await waitFor(() => expect(unscheduleSchedule).toHaveBeenCalledTimes(1));
    expect(unscheduleSchedule).toHaveBeenCalledWith({
      operationId: 'b02-d-ui:operation:1',
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: CURRENT_STATE_REF,
    });
    expect(
      container.querySelector(`[data-timeline-event="${SCHEDULE_REF}"]`),
    ).toBeTruthy();
    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(2));

    unscheduledWindow.resolve(emptyWindow());
    await waitFor(() => {
      expect(
        container.querySelector(`[data-timeline-event="${SCHEDULE_REF}"]`),
      ).toBeNull();
    });

    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    await waitFor(() =>
      expect(undoScheduleUnschedule).toHaveBeenCalledWith({
        operationId: 'b02-d-ui:operation:2',
        scheduleRef: SCHEDULE_REF,
        unscheduleOperationId: 'b02-d-ui:operation:1',
      }),
    );
    expect(
      container.querySelector(`[data-timeline-event="${SCHEDULE_REF}"]`),
    ).toBeNull();

    restoredWindow.resolve(scheduledWindow(RESTORED_STATE_REF));
    await waitFor(() => {
      expect(
        container.querySelector(`[data-timeline-event="${SCHEDULE_REF}"]`),
      ).toBeTruthy();
    });
    expect(RESTORED_STATE_REF).not.toBe(CURRENT_STATE_REF);
    expect(loadWindow).toHaveBeenCalledTimes(3);
  });
});
