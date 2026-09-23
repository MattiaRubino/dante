import { Temporal } from '@dante/time';
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../bootstrap/i18n';
import { createDeterministicTemporalIdFactory } from './model';
import type {
  TemporalScheduleDataSource,
  TemporalScheduleRevisionRequest,
  TemporalScheduleUnscheduleRequest,
} from './schedule-data-source';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from './timeline-read';
import { subscribeTemporalTimelineInvalidation } from './timeline-invalidation';
import {
  TemporalTimelineRuntimeBoundary,
  useTemporalTimelineRuntime,
} from './timeline-runtime-boundary';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

function emptyWindow(): TemporalTimelineWindow {
  return {
    kind: 'empty',
    startDate: '2026-08-28',
    endDateExclusive: '2026-10-10',
    effectiveZoneId: 'Europe/Rome',
  };
}

const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const MATERIAL_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';
const NEXT_MATERIAL_STATE_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';

function RevisionProbe() {
  const { reviseSchedule } = useTemporalTimelineRuntime();
  const request: Omit<TemporalScheduleRevisionRequest, 'operationId'> = {
    scheduleRef: SCHEDULE_REF,
    expectedPlacementMaterialStateRef: MATERIAL_STATE_REF,
    placement: {
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00'),
    },
  };
  return (
    <button type="button" onClick={() => void reviseSchedule(request)}>
      revise
    </button>
  );
}

function UnscheduleProbe() {
  const { unscheduleSchedule, undoScheduleUnschedule } =
    useTemporalTimelineRuntime();
  const request: Omit<TemporalScheduleUnscheduleRequest, 'operationId'> = {
    scheduleRef: SCHEDULE_REF,
    expectedPlacementMaterialStateRef: MATERIAL_STATE_REF,
  };
  return (
    <>
      <button type="button" onClick={() => void unscheduleSchedule(request)}>
        unschedule
      </button>
      <button
        type="button"
        onClick={() =>
          void undoScheduleUnschedule({
            scheduleRef: SCHEDULE_REF,
            unscheduleOperationId: 'b02-d:operation:1',
          })
        }
      >
        undo-unschedule
      </button>
    </>
  );
}

describe('TemporalTimelineRuntimeBoundary', () => {
  it('completes the explicit occurrence checkpoint before reading Timeline truth', async () => {
    const order: string[] = [];
    const checkpoint = deferred<{
      startDate: string;
      endDateExclusive: string;
      effectiveZoneId: string;
      sourceCount: number;
      occurrenceCount: number;
      replayedSourceCount: number;
    }>();
    const checkpointWindow = vi.fn<
      NonNullable<TemporalTimelineDataSource['checkpointWindow']>
    >((request) => {
      order.push('checkpoint');
      return checkpoint.promise.then((result) => {
        order.push('checkpoint-complete');
        return result;
      });
    });
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() => {
      order.push('read');
      return Promise.resolve(emptyWindow());
    });

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={{ checkpointWindow, loadWindow }}
        ids={createDeterministicTemporalIdFactory('b06-d')}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(checkpointWindow).toHaveBeenCalledWith(
      {
        operationId: 'b06-d:operation:1',
        startDate: '2026-08-28',
        endDateExclusive: '2026-10-10',
      },
      expect.any(AbortSignal),
    );
    expect(loadWindow).not.toHaveBeenCalled();

    await act(async () => {
      checkpoint.resolve({
        startDate: '2026-08-28',
        endDateExclusive: '2026-10-10',
        effectiveZoneId: 'Europe/Rome',
        sourceCount: 2,
        occurrenceCount: 7,
        replayedSourceCount: 0,
      });
      await checkpoint.promise;
    });

    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(1));
    expect(order).toEqual(['checkpoint', 'checkpoint-complete', 'read']);
  });

  it('keeps the product visible while truthfully exposing an in-flight real read', async () => {
    const pending = deferred<TemporalTimelineWindow>();
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(
      () => pending.promise,
    );
    const source: TemporalTimelineDataSource = { loadWindow };
    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(screen.getByText('product-shell')).toBeTruthy();
    expect(screen.getByRole('status').textContent).toContain(
      'Caricamento timeline',
    );
    expect(loadWindow).toHaveBeenCalledTimes(1);

    await act(async () => {
      pending.resolve(emptyWindow());
      await pending.promise;
    });

    await waitFor(() => {
      expect(screen.queryByRole('status')).toBeNull();
    });
    expect(
      container.querySelector('[data-temporal-read-state="ready"]'),
    ).toBeTruthy();
    expect(
      container
        .querySelector('[data-temporal-read-state="ready"]')
        ?.getAttribute('data-temporal-effective-zone'),
    ).toBe('Europe/Rome');
  });

  it('surfaces backend failure instead of replacing it with fake Timeline success', async () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.reject(new Error('offline')),
    );
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    const alert = await screen.findByRole('alert');
    expect(alert.textContent).toContain('Timeline non disponibile');
    expect(alert.textContent).toContain('Nessun dato finto');
    expect(screen.getByText('product-shell')).toBeTruthy();
  });

  it('retries the same governed read only after an explicit user retry', async () => {
    const first = deferred<TemporalTimelineWindow>();
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockImplementationOnce(() => first.promise)
      .mockImplementationOnce(() => Promise.resolve(emptyWindow()));
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    await act(async () => {
      first.reject(new Error('offline'));
      await first.promise.catch(() => undefined);
    });
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(loadWindow).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));

    await waitFor(() => {
      expect(loadWindow).toHaveBeenCalledTimes(2);
      expect(screen.queryByRole('alert')).toBeNull();
    });
  });

  it('generates one operation id and reloads authoritative truth once after revision', async () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.resolve(emptyWindow()),
    );
    const dataSource: TemporalTimelineDataSource = { loadWindow };
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
          placementMaterialStateRef: NEXT_MATERIAL_STATE_REF,
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

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={dataSource}
        scheduleDataSource={scheduleDataSource}
        ids={createDeterministicTemporalIdFactory('b02-c')}
        mode="production"
      >
        <RevisionProbe />
      </TemporalTimelineRuntimeBoundary>,
    );

    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole('button', { name: 'revise' }));

    await waitFor(() => {
      expect(reviseSchedule).toHaveBeenCalledWith({
        operationId: 'b02-c:operation:1',
        scheduleRef: SCHEDULE_REF,
        expectedPlacementMaterialStateRef: MATERIAL_STATE_REF,
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00'),
        },
      });
      expect(loadWindow).toHaveBeenCalledTimes(2);
    });
  });

  it('keeps frozen UI regression tests explicitly outside the real transport path', () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.resolve(emptyWindow()),
    );
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary dataSource={source} mode="test">
        <div>fixture-product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(screen.getByText('fixture-product-shell')).toBeTruthy();
    expect(screen.queryByRole('status')).toBeNull();
    expect(screen.queryByRole('alert')).toBeNull();
    expect(loadWindow).not.toHaveBeenCalled();
  });

  it('uses fresh operation ids and reloads Timeline once for unschedule and Undo', async () => {
    const invalidated = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidated);
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.resolve(emptyWindow()),
    );
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
        restoredFromPlacementMaterialStateRef: MATERIAL_STATE_REF,
        placementMaterialStateRef: NEXT_MATERIAL_STATE_REF,
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

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={{ loadWindow }}
        scheduleDataSource={scheduleDataSource}
        ids={createDeterministicTemporalIdFactory('b02-d')}
        mode="production"
      >
        <UnscheduleProbe />
      </TemporalTimelineRuntimeBoundary>,
    );

    await waitFor(() => expect(loadWindow).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole('button', { name: 'unschedule' }));
    await waitFor(() => {
      expect(unscheduleSchedule).toHaveBeenCalledWith({
        operationId: 'b02-d:operation:1',
        scheduleRef: SCHEDULE_REF,
        expectedPlacementMaterialStateRef: MATERIAL_STATE_REF,
      });
      expect(loadWindow).toHaveBeenCalledTimes(2);
      expect(invalidated).toHaveBeenCalledTimes(1);
    });

    fireEvent.click(screen.getByRole('button', { name: 'undo-unschedule' }));
    await waitFor(() => {
      expect(undoScheduleUnschedule).toHaveBeenCalledWith({
        operationId: 'b02-d:operation:2',
        scheduleRef: SCHEDULE_REF,
        unscheduleOperationId: 'b02-d:operation:1',
      });
      expect(loadWindow).toHaveBeenCalledTimes(3);
      expect(invalidated).toHaveBeenCalledTimes(2);
    });
    unsubscribe();
  });
});
