import { Temporal, detectDeviceTimeZone, type PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import './timeline-runtime-boundary.css';

import { createRemoteTemporalTimelineDataSource } from './remote-timeline-read';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const INITIAL_WINDOW_PAST_DAYS = 7;
const INITIAL_WINDOW_FUTURE_DAYS = 35;

type TemporalTimelineRuntimeState =
  | Readonly<{ status: 'loading' }>
  | Readonly<{ status: 'ready'; effectiveZoneId: string }>
  | Readonly<{ status: 'error' }>;

type TemporalTimelineReadAttempt = Readonly<{
  request: TemporalTimelineWindowRequest;
  source: TemporalTimelineDataSource;
  retryRevision: number;
}>;

type TemporalTimelineSettledState =
  | Readonly<{
      attempt: TemporalTimelineReadAttempt;
      status: 'ready';
      effectiveZoneId: string;
    }>
  | Readonly<{
      attempt: TemporalTimelineReadAttempt;
      status: 'error';
    }>;

type TemporalTimelineRuntimeBoundaryProps = Readonly<{
  children: ReactNode;
  viewedDateIso?: string | undefined;
  dataSource?: TemporalTimelineDataSource | undefined;
  mode?: string | undefined;
}>;

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
    return { status: 'ready', effectiveZoneId: 'Etc/UTC' };
  }
  if (settledState?.attempt !== attempt) {
    return { status: 'loading' };
  }
  if (settledState.status === 'ready') {
    return {
      status: 'ready',
      effectiveZoneId: settledState.effectiveZoneId,
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
  mode = import.meta.env.MODE,
}: TemporalTimelineRuntimeBoundaryProps) {
  const { t } = useTranslation('common');
  const testMode = mode === 'test';
  const source = useMemo(
    () => dataSource ?? createRemoteTemporalTimelineDataSource(),
    [dataSource],
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
          effectiveZoneId: window.effectiveZoneId,
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

  const state = resolveRuntimeState(testMode, attempt, settledState);

  const retry = useCallback(() => {
    setRetryRevision((revision) => revision + 1);
  }, []);

  return (
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
          <button type="button" onClick={retry}>
            {t(($) => $.common.temporalRuntime.timeline.retry)}
          </button>
        </div>
      ) : null}
    </div>
  );
}
