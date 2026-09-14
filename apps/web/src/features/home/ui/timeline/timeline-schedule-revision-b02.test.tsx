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
import { TemporalScheduleRemoteError } from '../../../temporal/remote-schedule-data-source';
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
const NEXT_STATE_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';

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

type Deferred<T> = Readonly<{
  promise: Promise<T>;
  resolve: (value: T) => void;
}>;

function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((resolvePromise) => {
    resolve = resolvePromise;
  });
  return { promise, resolve };
}

function windowAt(
  startsLocalAt: string,
  endsLocalAt: string,
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
        title: 'Governed B02-C',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from(startsLocalAt),
        endsLocalAt: Temporal.PlainDateTime.from(endsLocalAt),
      },
    ],
  };
}

function renderGovernedTimeline(
  revisedWindow: Deferred<TemporalTimelineWindow>,
) {
  const loadWindow = vi
    .fn<TemporalTimelineDataSource['loadWindow']>()
    .mockResolvedValueOnce(
      windowAt('2026-09-09T10:00', '2026-09-09T11:00', CURRENT_STATE_REF),
    )
    .mockImplementationOnce(() => revisedWindow.promise);
  const dataSource: TemporalTimelineDataSource = { loadWindow };
  const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>(
    (request) =>
      Promise.resolve({
        scheduleRef: request.scheduleRef,
        previousPlacementMaterialStateRef:
          request.expectedPlacementMaterialStateRef,
        placementMaterialStateRef: NEXT_STATE_REF,
        placement: request.placement,
        replayed: false,
      }),
  );
  const scheduleDataSource: TemporalScheduleDataSource = {
    reviseSchedule,
    unscheduleSchedule: vi.fn(() =>
      Promise.reject(new Error('not expected')),
    ),
    undoScheduleUnschedule: vi.fn(() =>
      Promise.reject(new Error('not expected')),
    ),
  };
  const view = render(
    <TemporalTimelineRuntimeBoundary
      viewedDateIso="2026-09-09"
      dataSource={dataSource}
      scheduleDataSource={scheduleDataSource}
      ids={createDeterministicTemporalIdFactory('b02-c-ui')}
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

describe('B02-C governed Schedule revision from Timeline', () => {
  it('keeps a keyboard/drag move non-optimistic and reloads the new current state', async () => {
    const revisedWindow = deferred<TemporalTimelineWindow>();
    const { container, loadWindow, reviseSchedule } =
      renderGovernedTimeline(revisedWindow);
    const card = await waitFor(() => {
      const match = container.querySelector<HTMLElement>(
        `[data-timeline-event="${SCHEDULE_REF}"]`,
      );
      expect(match).toBeTruthy();
      return match as HTMLElement;
    });

    fireEvent.keyDown(card, { key: 'ArrowDown', altKey: true });

    await waitFor(() => expect(reviseSchedule).toHaveBeenCalledTimes(1));
    const request = reviseSchedule.mock.calls[0]?.[0];
    expect(request).toMatchObject({
      operationId: 'b02-c-ui:operation:1',
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: CURRENT_STATE_REF,
    });
    expect(request?.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T10:05:00',
    );
    expect(request?.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T11:05:00',
    );
    expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    expect(loadWindow).toHaveBeenCalledTimes(2);

    revisedWindow.resolve(
      windowAt('2026-09-09T10:05', '2026-09-09T11:05', NEXT_STATE_REF),
    );
    await waitFor(() => {
      expect(
        container
          .querySelector<HTMLElement>(`[data-timeline-event="${SCHEDULE_REF}"]`)
          ?.getAttribute('aria-label'),
      ).toContain('10:05–11:05');
    });
  });

  it('keeps current truth unchanged and does not reload after a stale conflict', async () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.resolve(
        windowAt('2026-09-09T10:00', '2026-09-09T11:00', CURRENT_STATE_REF),
      ),
    );
    const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>(
      () =>
        Promise.reject(
          new TemporalScheduleRemoteError(
            'http',
            'stale',
            409,
            'temporal.schedule.revision_conflict',
          ),
        ),
    );
    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={{ loadWindow }}
        scheduleDataSource={{
          reviseSchedule,
          unscheduleSchedule: vi.fn(() =>
            Promise.reject(new Error('not expected')),
          ),
          undoScheduleUnschedule: vi.fn(() =>
            Promise.reject(new Error('not expected')),
          ),
        }}
        ids={createDeterministicTemporalIdFactory('b02-c-stale')}
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

    fireEvent.keyDown(card, { key: 'ArrowDown', altKey: true });

    expect(
      await screen.findByText(
        'La pianificazione è cambiata altrove. Nessuna modifica è stata sovrascritta.',
      ),
    ).toBeTruthy();
    expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    expect(loadWindow).toHaveBeenCalledTimes(1);
  });

  it('routes the time editor through the same expected-state revision boundary', async () => {
    const revisedWindow = deferred<TemporalTimelineWindow>();
    const { container, reviseSchedule } = renderGovernedTimeline(revisedWindow);
    await screen.findByText('Governed B02-C');

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Modifica orario di Governed B02-C',
      }),
    );
    fireEvent.change(screen.getByLabelText('Inizio minuti'), {
      target: { value: '30' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva' }));

    await waitFor(() => expect(reviseSchedule).toHaveBeenCalledTimes(1));
    const request = reviseSchedule.mock.calls[0]?.[0];
    expect(request?.expectedPlacementMaterialStateRef).toBe(CURRENT_STATE_REF);
    expect(request?.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T10:30:00',
    );
    expect(request?.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T11:30:00',
    );
    expect(
      container
        .querySelector<HTMLElement>(`[data-timeline-event="${SCHEDULE_REF}"]`)
        ?.getAttribute('aria-label'),
    ).toContain('10:00–11:00');

    revisedWindow.resolve(
      windowAt('2026-09-09T10:30', '2026-09-09T11:30', NEXT_STATE_REF),
    );
    await waitFor(() => {
      expect(
        container
          .querySelector<HTMLElement>(`[data-timeline-event="${SCHEDULE_REF}"]`)
          ?.getAttribute('aria-label'),
      ).toContain('10:30–11:30');
    });
  });

  it('Undo revision writes a new monotonic state from the exact produced basis', async () => {
    const restoredStateRef = '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d';
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockResolvedValueOnce(
        windowAt('2026-09-09T10:00', '2026-09-09T11:00', CURRENT_STATE_REF),
      )
      .mockResolvedValueOnce(
        windowAt('2026-09-09T10:05', '2026-09-09T11:05', NEXT_STATE_REF),
      )
      .mockResolvedValueOnce(
        windowAt('2026-09-09T10:00', '2026-09-09T11:00', restoredStateRef),
      );
    const reviseSchedule = vi.fn<
      TemporalScheduleDataSource['reviseSchedule']
    >((request) =>
      Promise.resolve({
        scheduleRef: request.scheduleRef,
        previousPlacementMaterialStateRef:
          request.expectedPlacementMaterialStateRef,
        placementMaterialStateRef:
          request.expectedPlacementMaterialStateRef === CURRENT_STATE_REF
            ? NEXT_STATE_REF
            : restoredStateRef,
        placement: request.placement,
        replayed: false,
      }),
    );

    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={{ loadWindow }}
        scheduleDataSource={{
          reviseSchedule,
          unscheduleSchedule: vi.fn(() =>
            Promise.reject(new Error('not expected')),
          ),
          undoScheduleUnschedule: vi.fn(() =>
            Promise.reject(new Error('not expected')),
          ),
        }}
        ids={createDeterministicTemporalIdFactory('b02-c-undo')}
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

    fireEvent.keyDown(card, { key: 'ArrowDown', altKey: true });
    await waitFor(() => expect(reviseSchedule).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));

    await waitFor(() => expect(reviseSchedule).toHaveBeenCalledTimes(2));
    const undoRequest = reviseSchedule.mock.calls[1]?.[0];
    expect(undoRequest).toMatchObject({
      operationId: 'b02-c-undo:operation:2',
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: NEXT_STATE_REF,
    });
    expect(undoRequest?.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T10:00:00',
    );
    expect(undoRequest?.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T11:00:00',
    );
    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(3));
  });

});
