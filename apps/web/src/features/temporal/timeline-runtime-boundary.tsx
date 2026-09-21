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
  source: TemporalTimelineDataSource;
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
    return { status: 'loading' };
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
  const request = useMemo(
    () => (testMode ? null : temporalTimelineInitialWindow(viewedDateIso)),
    [testMode, viewedDateIso],
  );
  const [retryRevision, setRetryRevision] = useState(0);
  const attempt = useMemo<TemporalTimelineReadAttempt | null>(
    () =>
      testMode || request === null
        ? null
        : Object.freeze({
            request,
            source,
            retryRevision,
          }),
    [request, retryRevision, source, testMode],
  );
  const [settledState, setSettledState] =
    useState<TemporalTimelineSettledState | null>(null);

  useEffect(() => {
    if (attempt === null) {
      return;
    }

    const controller = new AbortController();
    let active = true;

    void attempt.source
      .loadWindow(attempt.request, controller.signal)
      .then((window) => {
        if (!active) {
          return;
        }
        setSettledState({
          attempt,
          status: 'ready',
          window,
        });
      })
      .catch(() => {
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
      refresh();
      return result;
    },
    [ids, mutationSource, refresh],
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
