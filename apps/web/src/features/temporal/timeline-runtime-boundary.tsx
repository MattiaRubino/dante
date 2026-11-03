import { Temporal, detectDeviceTimeZone, type PlainDate } from '@dante/time';
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import './timeline-runtime-boundary.css';

import { systemTemporalIdFactory, type TemporalIdFactory } from './model';
import { createRemoteTemporalScheduleDataSource } from './remote-schedule-data-source';
import { createRemoteTemporalTimelineDataSource } from './remote-timeline-read';
import type {
  TemporalScheduleDataSource,
  TemporalScheduleRevisionRequest,
  TemporalScheduleRevisionResult,
  TemporalScheduleUnscheduleRequest,
  TemporalScheduleUnscheduleResult,
  TemporalScheduleUnscheduleUndoRequest,
  TemporalScheduleUnscheduleUndoResult,
} from './schedule-data-source';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
  subscribeTemporalTimelineInvalidation,
} from './timeline-invalidation';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const INITIAL_WINDOW_PAST_DAYS = 7;
const INITIAL_WINDOW_FUTURE_DAYS = 35;
const PRIORITY_WINDOW_FUTURE_DAYS = 3;
const RETAIN_WINDOW_PAST_DAYS = 3;
const RETAIN_WINDOW_FUTURE_DAYS = 4;

export type TemporalTimelineRuntimeState =
  | Readonly<{ status: 'loading' }>
  | Readonly<{
      status: 'ready';
      effectiveZoneId: string;
      window: TemporalTimelineWindow | null;
    }>
  | Readonly<{ status: 'error' }>;

export type TemporalTimelineRuntimeContextValue = Readonly<{
  state: TemporalTimelineRuntimeState;
  refresh: () => void;
  reviseSchedule: (
    request: Omit<TemporalScheduleRevisionRequest, 'operationId'>,
  ) => Promise<TemporalScheduleRevisionResult>;
  unscheduleSchedule: (
    request: Omit<TemporalScheduleUnscheduleRequest, 'operationId'>,
  ) => Promise<TemporalScheduleUnscheduleResult>;
  undoScheduleUnschedule: (
    request: Omit<TemporalScheduleUnscheduleUndoRequest, 'operationId'>,
  ) => Promise<TemporalScheduleUnscheduleUndoResult>;
}>;

type TemporalTimelineReadAttempt = Readonly<{
  request: TemporalTimelineWindowRequest;
  priorityRequest: TemporalTimelineWindowRequest;
  source: TemporalTimelineDataSource;
  priorityOperationId: string | null;
  fullOperationId: string | null;
  retryRevision: number;
}>;

type TemporalTimelineSettledState =
  | Readonly<{
      attempt: TemporalTimelineReadAttempt;
      status: 'ready';
      window: TemporalTimelineWindow;
    }>
  | Readonly<{
      attempt: TemporalTimelineReadAttempt;
      status: 'error';
    }>;

type TemporalTimelineRuntimeBoundaryProps = Readonly<{
  children: ReactNode;
  viewedDateIso?: string | undefined;
  dataSource?: TemporalTimelineDataSource | undefined;
  scheduleDataSource?: TemporalScheduleDataSource | undefined;
  ids?: TemporalIdFactory | undefined;
  mode?: string | undefined;
}>;

const TemporalTimelineRuntimeContext =
  createContext<TemporalTimelineRuntimeContextValue | null>(null);

export function useTemporalTimelineRuntime(): TemporalTimelineRuntimeContextValue {
  const value = useContext(TemporalTimelineRuntimeContext);
  if (value === null) {
    throw new Error(
      'useTemporalTimelineRuntime must be used inside TemporalTimelineRuntimeBoundary.',
    );
  }
  return value;
}

function resolveAnchorDate(viewedDateIso: string | undefined): PlainDate {
  if (viewedDateIso !== undefined) {
    try {
      return Temporal.PlainDate.from(viewedDateIso);
    } catch {
      // Route/view state is defensive: an invalid external date must not poison
      // the authenticated temporal read. Fall back to the device-local today.
    }
  }

  const zoneId = detectDeviceTimeZone();
  return Temporal.Now.zonedDateTimeISO(zoneId).toPlainDate();
}

function resolveRuntimeState(
  testMode: boolean,
  attempt: TemporalTimelineReadAttempt | null,
  settledState: TemporalTimelineSettledState | null,
): TemporalTimelineRuntimeState {
  if (testMode) {
    return { status: 'ready', effectiveZoneId: 'Etc/UTC', window: null };
  }
  if (settledState?.attempt !== attempt) {
    // Refreshes of the same window keep the last accepted Timeline visible
    // until the new authoritative read settles. A different date range or
    // source cannot borrow that window's truth.
    if (
      settledState?.status !== 'ready' ||
      attempt === null ||
      settledState.attempt.source !== attempt.source ||
      settledState.attempt.request.startDate !== attempt.request.startDate ||
      settledState.attempt.request.endDateExclusive !==
        attempt.request.endDateExclusive
    ) {
      return { status: 'loading' };
    }
  }
  if (settledState.status === 'ready') {
    return {
      status: 'ready',
      effectiveZoneId: settledState.window.effectiveZoneId,
      window: settledState.window,
    };
  }
  return { status: 'error' };
}

export function temporalTimelineInitialWindow(
  viewedDateIso: string | undefined,
): TemporalTimelineWindowRequest {
  const anchor = resolveAnchorDate(viewedDateIso);
  return {
    startDate: anchor.subtract({ days: INITIAL_WINDOW_PAST_DAYS }).toString(),
    endDateExclusive: anchor
      .add({ days: INITIAL_WINDOW_FUTURE_DAYS + 1 })
      .toString(),
  };
}

/** Scrolling within an already loaded window must not restart materialization. */
export function temporalTimelineWindowForView(
  viewedDateIso: string | undefined,
  previous: TemporalTimelineWindowRequest | null,
): TemporalTimelineWindowRequest {
  if (previous) {
    const viewed = resolveAnchorDate(viewedDateIso);
    const first = Temporal.PlainDate.from(previous.startDate).add({
      days: RETAIN_WINDOW_PAST_DAYS,
    });
    const last = Temporal.PlainDate.from(previous.endDateExclusive).subtract({
      days: RETAIN_WINDOW_FUTURE_DAYS,
    });
    if (
      Temporal.PlainDate.compare(viewed, first) >= 0 &&
      Temporal.PlainDate.compare(viewed, last) < 0
    ) {
      return previous;
    }
  }
  return temporalTimelineInitialWindow(viewedDateIso);
}

export function TemporalTimelineRuntimeBoundary({
  children,
  viewedDateIso,
  dataSource,
  scheduleDataSource,
  ids = systemTemporalIdFactory,
  mode = import.meta.env.MODE,
}: TemporalTimelineRuntimeBoundaryProps) {
  const { t } = useTranslation('common');
  const testMode = mode === 'test';
  const source = useMemo(
    () => dataSource ?? createRemoteTemporalTimelineDataSource(),
    [dataSource],
  );
  const mutationSource = useMemo(
    () => scheduleDataSource ?? createRemoteTemporalScheduleDataSource(),
    [scheduleDataSource],
  );
  const [windowSelection, setWindowSelection] = useState(() => ({
    viewedDateIso,
    testMode,
    request: testMode ? null : temporalTimelineInitialWindow(viewedDateIso),
  }));
  let request = windowSelection.request;
  if (
    windowSelection.viewedDateIso !== viewedDateIso ||
    windowSelection.testMode !== testMode
  ) {
    request = testMode
      ? null
      : temporalTimelineWindowForView(viewedDateIso, request);
    setWindowSelection({ viewedDateIso, testMode, request });
  }
  const priorityRequest = useMemo(() => {
    if (request === null) return null;
    const anchor = Temporal.PlainDate.from(request.startDate).add({
      days: INITIAL_WINDOW_PAST_DAYS,
    });
    // The initial Timeline renders through day +3. Materialize that visible
    // range first so an early Session has its future planned source in view.
    return {
      startDate: anchor.subtract({ days: 1 }).toString(),
      endDateExclusive: anchor
        .add({ days: PRIORITY_WINDOW_FUTURE_DAYS + 1 })
        .toString(),
    };
  }, [request]);
  const [retryRevision, setRetryRevision] = useState(0);
  const attempt = useMemo<TemporalTimelineReadAttempt | null>(
    () =>
      testMode || request === null || priorityRequest === null
        ? null
        : Object.freeze({
            request,
            priorityRequest,
            source,
            priorityOperationId:
              source.checkpointWindow === undefined ? null : ids.operationId(),
            fullOperationId:
              source.checkpointWindow === undefined ? null : ids.operationId(),
            retryRevision,
          }),
    [ids, priorityRequest, request, retryRevision, source, testMode],
  );
  const [settledState, setSettledState] =
    useState<TemporalTimelineSettledState | null>(null);

  useEffect(() => {
    if (attempt === null) {
      return;
    }

    const controller = new AbortController();
    let active = true;

    // Read accepted Schedule truth immediately. Then checkpoint the visible
    // Timeline days before completing the full window, with a canonical read
    // after each stage. No browser-generated occurrence enters Timeline.
    let checkpointSettled = false;
    if (attempt.source.checkpointWindow !== undefined) {
      void attempt.source.loadWindow(attempt.request, controller.signal).then(
        (window) => {
          if (active && !checkpointSettled) {
            setSettledState({ attempt, status: 'ready', window });
          }
        },
        () => {
          // The checkpoint's governed read below remains authoritative. An
          // early read failure must not hide a successfully materialized view.
        },
      );
    }

    void (async () => {
      if (
        attempt.source.checkpointWindow !== undefined &&
        attempt.priorityOperationId !== null &&
        attempt.fullOperationId !== null
      ) {
        await attempt.source.checkpointWindow(
          {
            ...attempt.priorityRequest,
            operationId: attempt.priorityOperationId,
          },
          controller.signal,
        );
        checkpointSettled = true;
        const priorityWindow = await attempt.source.loadWindow(
          attempt.request,
          controller.signal,
        );
        if (!active) return;
        setSettledState({ attempt, status: 'ready', window: priorityWindow });

        await attempt.source.checkpointWindow(
          { ...attempt.request, operationId: attempt.fullOperationId },
          controller.signal,
        );
      }
      checkpointSettled = true;
      const window = await attempt.source.loadWindow(
        attempt.request,
        controller.signal,
      );
      if (active) setSettledState({ attempt, status: 'ready', window });
    })().catch(() => {
      checkpointSettled = true;
      if (!active || controller.signal.aborted) {
        return;
      }
      setSettledState({ attempt, status: 'error' });
    });

    return () => {
      active = false;
      controller.abort();
    };
  }, [attempt]);

  const refresh = useCallback(() => {
    if (!testMode) {
      setRetryRevision((revision) => revision + 1);
    }
  }, [testMode]);

  useEffect(() => {
    if (testMode) {
      return;
    }
    return subscribeTemporalTimelineInvalidation(refresh);
  }, [refresh, testMode]);

  const reviseSchedule = useCallback(
    async (
      revision: Omit<TemporalScheduleRevisionRequest, 'operationId'>,
    ): Promise<TemporalScheduleRevisionResult> => {
      const result = await mutationSource.reviseSchedule({
        ...revision,
        operationId: ids.operationId(),
      });
      // The Session panel also depends on this placement. Notify every
      // timeline read consumer after the accepted revision, not only this view.
      invalidateTemporalTimelineRead();
      return result;
    },
    [ids, mutationSource],
  );

  const unscheduleSchedule = useCallback(
    async (
      command: Omit<TemporalScheduleUnscheduleRequest, 'operationId'>,
    ): Promise<TemporalScheduleUnscheduleResult> => {
      const result = await mutationSource.unscheduleSchedule({
        ...command,
        operationId: ids.operationId(),
      });
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      refresh();
      return result;
    },
    [ids, mutationSource, refresh],
  );

  const undoScheduleUnschedule = useCallback(
    async (
      command: Omit<TemporalScheduleUnscheduleUndoRequest, 'operationId'>,
    ): Promise<TemporalScheduleUnscheduleUndoResult> => {
      const result = await mutationSource.undoScheduleUnschedule({
        ...command,
        operationId: ids.operationId(),
      });
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      refresh();
      return result;
    },
    [ids, mutationSource, refresh],
  );

  const state = resolveRuntimeState(testMode, attempt, settledState);
  const contextValue = useMemo<TemporalTimelineRuntimeContextValue>(
    () =>
      Object.freeze({
        state,
        refresh,
        reviseSchedule,
        unscheduleSchedule,
        undoScheduleUnschedule,
      }),
    [
      refresh,
      reviseSchedule,
      state,
      undoScheduleUnschedule,
      unscheduleSchedule,
    ],
  );

  return (
    <TemporalTimelineRuntimeContext.Provider value={contextValue}>
      <div
        className="temporal-timeline-runtime-boundary"
        data-temporal-read-state={state.status}
        data-temporal-effective-zone={
          state.status === 'ready' ? state.effectiveZoneId : undefined
        }
      >
        {children}

        {state.status === 'loading' ? (
          <div
            className="temporal-timeline-runtime-status"
            role="status"
            aria-live="polite"
          >
            {t(($) => $.common.temporalRuntime.timeline.loading)}
          </div>
        ) : null}

        {state.status === 'error' ? (
          <div
            className="temporal-timeline-runtime-status temporal-timeline-runtime-status--error"
            role="alert"
          >
            <strong>
              {t(($) => $.common.temporalRuntime.timeline.errorTitle)}
            </strong>
            <span>
              {t(($) => $.common.temporalRuntime.timeline.errorDescription)}
            </span>
            <button type="button" onClick={refresh}>
              {t(($) => $.common.temporalRuntime.timeline.retry)}
            </button>
          </div>
        ) : null}
      </div>
    </TemporalTimelineRuntimeContext.Provider>
  );
}
