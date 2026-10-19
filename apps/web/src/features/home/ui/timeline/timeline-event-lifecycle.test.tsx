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

vi.mock('../../../temporal/remote-placement-lock-data-source', () => ({
  createRemotePlacementLockDataSource: () => ({
    get: (scheduleRef: string) =>
      Promise.resolve({ scheduleRef, locked: false, revision: 0 }),
  }),
}));

const EVENT_REF = '0199a8c0-7e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-7e72-7bc0-8ad0-a2f403f5617d';
const CURRENT_STATE_REF = '0199a8c0-7e73-7bc0-8ad0-a2f403f5617d';
const NEXT_STATE_REF = '0199a8c0-7e74-7bc0-8ad0-a2f403f5617d';

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

function eventWindow(
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
        kind: 'scheduled_event',
        eventRef: EVENT_REF,
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef,
        title: 'Evento governato B03-C',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from(startsLocalAt),
        endsLocalAt: Temporal.PlainDateTime.from(endsLocalAt),
      },
    ],
  };
}

function renderEventTimeline(
  dataSource: TemporalTimelineDataSource,
  scheduleDataSource: TemporalScheduleDataSource,
  seed: string,
) {
  return render(
    <TemporalTimelineRuntimeBoundary
      viewedDateIso="2026-09-09"
      dataSource={dataSource}
      scheduleDataSource={scheduleDataSource}
      ids={createDeterministicTemporalIdFactory(seed)}
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
}

describe('B03-C Event placement lifecycle from Timeline', () => {
  it('routes Event drag/keyboard reschedule through the shared Schedule CAS boundary', async () => {
    const revisedWindow = deferred<TemporalTimelineWindow>();
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockResolvedValueOnce(
        eventWindow('2026-09-09T10:00', '2026-09-09T11:00', CURRENT_STATE_REF),
      )
      .mockImplementationOnce(() => revisedWindow.promise);
    const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>(
      (request) => {
        if (request.placement.kind !== 'floating-local-interval') {
          return Promise.reject(
            new Error('Expected floating-local placement.'),
          );
        }
        return Promise.resolve({
          scheduleRef: request.scheduleRef,
          previousPlacementMaterialStateRef:
            request.expectedPlacementMaterialStateRef,
          placementMaterialStateRef: NEXT_STATE_REF,
          placement: request.placement,
          replayed: false,
        });
      },
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

    const { container } = renderEventTimeline(
      { loadWindow },
      scheduleDataSource,
      'b03-c-event-revision',
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
    const request = reviseSchedule.mock.calls[0]?.[0];
    expect(request).toMatchObject({
      operationId: 'b03-c-event-revision:operation:1',
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: CURRENT_STATE_REF,
    });
    if (!request || request.placement.kind !== 'floating-local-interval') {
      throw new Error('Expected floating-local Event revision.');
    }
    expect(request.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T10:15:00',
    );
    expect(request.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T11:15:00',
    );
    expect(card.getAttribute('aria-label')).toContain('10:00–11:00');
    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(2));
    const confirmation = await screen.findByText(
      'Evento riprogrammato per 9 set, 10:15–11:15',
    );
    expect(confirmation.parentElement?.getAttribute('role')).toBe('status');
    expect(
      confirmation.parentElement?.querySelector('button')?.textContent,
    ).toBe('Annulla');
    expect(container.querySelector('.timeline-move-toast.is-on')).toBeNull();

    revisedWindow.resolve(
      eventWindow('2026-09-09T10:15', '2026-09-09T11:15', NEXT_STATE_REF),
    );
    await waitFor(() => {
      expect(
        container
          .querySelector<HTMLElement>(`[data-timeline-event="${SCHEDULE_REF}"]`)
          ?.getAttribute('aria-label'),
      ).toContain('10:15–11:15');
    });
  });
});
