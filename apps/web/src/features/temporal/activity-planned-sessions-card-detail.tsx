import { useEffect, useState, type ReactNode } from 'react';

import { createWebFetch } from '../../platform/api/web-fetch';
import { subscribeTemporalPlanningInvalidation } from './timeline-invalidation';
import {
  createRemoteTemporalSessionDataSource,
  type TemporalSessionView,
} from './remote-session-data-source';
import { SessionSubjectControls } from './session-subject-controls';
import './activity-planned-sessions-card-detail.css';

type PlannedSession = Readonly<{
  scheduleRef: string;
  name: string;
  order: number;
}>;
export type ActivityScheduleInterval = Readonly<{
  scheduleRef: string;
  order: number;
  start: string;
  end: string;
  instant: boolean;
  zoneId: string | null;
}>;

type PlannedSessionStructure = Readonly<{
  rows: readonly PlannedSession[];
  intervals: readonly ActivityScheduleInterval[];
  independentChildren: boolean;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Struttura Activity non valida.');
  }
  return value as Record<string, unknown>;
}

function parsePlannedSessions(
  value: unknown,
  activityRef: string,
): PlannedSessionStructure {
  const payload = record(value);
  if (
    payload.parent_activity_ref !== activityRef ||
    !Array.isArray(payload.schedules)
  ) {
    throw new Error('Struttura Activity non valida.');
  }

  const schedules = payload.schedules.map(record);
  const placedIntervals = schedules.filter((row) => row.role_code === 'interval');
  const intervals = placedIntervals.flatMap(
    (row, index): ActivityScheduleInterval[] => {
      if (typeof row.schedule_ref !== 'string') return [];
      const instant =
        row.temporal_form === 'named_zone_local' ||
        row.temporal_form === 'absolute';
      const start = instant
        ? (row.resolved_start_at ?? row.starts_at)
        : row.starts_local_at;
      const end = instant
        ? (row.resolved_end_at ?? row.ends_at)
        : row.ends_local_at;
      if (typeof start !== 'string' || typeof end !== 'string') return [];
      return [
        {
          scheduleRef: row.schedule_ref,
          order:
            typeof row.presentation_order === 'number' &&
            Number.isInteger(row.presentation_order)
              ? row.presentation_order
              : index + 1,
          start,
          end,
          instant,
          zoneId: typeof row.zone_id === 'string' ? row.zone_id : null,
        },
      ];
    },
  );

  return Object.freeze({
    // Missing / unplaced placements may not masquerade as a complete schedule.
    intervals: Object.freeze(
      intervals.length === placedIntervals.length
        ? intervals.sort((left, right) => left.order - right.order)
        : [],
    ),
    // An absent capability cannot grant independent child Play.
    independentChildren:
      payload.session_capture_mode === 'disabled' ||
      payload.session_capture_mode === 'record',
    rows: Object.freeze(
      schedules
        .filter((row) => row.role_code === 'planned')
        .map((row, index) => {
          if (typeof row.schedule_ref !== 'string') {
            throw new Error('Sessione pianificata non valida.');
          }
          const order =
            typeof row.presentation_order === 'number' &&
            Number.isInteger(row.presentation_order)
              ? row.presentation_order
              : index + 1;
          return Object.freeze({
            scheduleRef: row.schedule_ref,
            name:
              typeof row.display_name === 'string' &&
              row.display_name.trim().length > 0
                ? row.display_name
                : `Sessione ${order}`,
            order,
          });
        })
        .sort((left, right) => left.order - right.order),
    ),
  });
}

/**
 * Planned Sessions are Activity-owned planning detail, never sibling Timeline
 * cards. The compact band exposes their count; detail controls are only
 * rendered in the Activity Inspector.
 */
type PlannedSessionCardProps = Readonly<{
  activityRef: string;
  visible: boolean;
  variant?: 'detail' | 'indicator';
  locale?: string;
  timeZone?: string;
  /** Inspector-only leading content shares this component's one /children read. */
  renderInspectorLeading?: (
    intervals: readonly ActivityScheduleInterval[],
  ) => ReactNode;
}>;

export function ActivityPlannedSessionsCardDetail(
  props: PlannedSessionCardProps,
) {
  // Hidden panels unmount instead of retaining a stale prior fetch or
  // resetting state synchronously inside an effect.
  if (!props.visible) return null;
  return <PlannedSessionCardContent key={props.activityRef} {...props} />;
}

function PlannedSessionCardContent({
  activityRef,
  visible,
  variant = 'detail',
  locale,
  timeZone,
  renderInspectorLeading,
}: PlannedSessionCardProps) {
  const [structure, setStructure] = useState<PlannedSessionStructure | null>(
    null,
  );
  const [sessions, setSessions] = useState<
    readonly TemporalSessionView[] | null
  >(null);
  const [revision, setRevision] = useState(0);
  const [sessionRevision, setSessionRevision] = useState(0);

  useEffect(() => {
    const onChange = (event: Event) => {
      if (event instanceof CustomEvent && event.detail === activityRef) {
        setSessionRevision((value) => value + 1);
      }
    };
    window.addEventListener('dante:session-changed', onChange);
    return () => window.removeEventListener('dante:session-changed', onChange);
  }, [activityRef]);

  useEffect(() => {
    if (variant === 'indicator') return;
    let cancelled = false;
    const source = createRemoteTemporalSessionDataSource();
    void source
      .list('activity', activityRef)
      .then((next) => {
        if (!cancelled) setSessions(next);
      })
      .catch(() => {
        if (!cancelled) setSessions(null); // fail closed; no invalid Play
      });
    return () => {
      cancelled = true;
    };
  }, [activityRef, sessionRevision, variant]);

  useEffect(
    () =>
      subscribeTemporalPlanningInvalidation(() => setRevision((n) => n + 1)),
    [],
  );

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    const webFetch = createWebFetch(globalThis.fetch);
    void webFetch(
      `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/children`,
      { signal: controller.signal },
    )
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Activity detail rejected (${response.status}).`);
        }
        return parsePlannedSessions(await response.json(), activityRef);
      })
      .then((result) => {
        if (!cancelled) {
          setStructure(result);
        }
      })
      .catch(() => {
        if (!cancelled && !controller.signal.aborted) setStructure(null);
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [activityRef, visible, revision]);

  if (!visible) return null;
  const inspectorLeading = renderInspectorLeading?.(structure?.intervals ?? []);
  if (structure === null || structure.rows.length === 0) {
    // Keep the main Session subtree mounted across planning read refresh/failure.
    return inspectorLeading === undefined ? null : <>{inspectorLeading}</>;
  }
  const { rows, independentChildren } = structure;

  if (variant === 'indicator') {
    return (
      <div
        className="timeline-activity-planned-sessions__indicator"
        data-activity-planned-sessions={activityRef}
        aria-label={`${rows.length} sessioni pianificate`}
        title={`${rows.length} sessioni pianificate`}
      >
        <span>Sessioni</span>
        <strong>{rows.length}</strong>
      </div>
    );
  }

  const mainSessions = (sessions ?? []).filter(
    (session) => session.plannedScheduleRef == null,
  );
  const mainRunning = mainSessions.some(
    (session) => session.open && !session.paused,
  );
  const mainPaused = mainSessions.some(
    (session) => session.open && session.paused,
  );
  const mainStopped =
    mainSessions.length > 0 && !mainSessions.some((session) => session.open);

  return (
    <>
      {inspectorLeading}
      <div
        className="timeline-activity-planned-sessions"
        data-activity-planned-sessions={activityRef}
        role={rows.length > 4 ? 'region' : undefined}
        aria-label={rows.length > 4 ? 'Sessioni pianificate' : undefined}
        tabIndex={rows.length > 4 ? 0 : undefined}
      >
        <span className="timeline-activity-planned-sessions__label">
          Sessioni
        </span>
        {rows.map((row) => (
          <div
            className="timeline-activity-planned-sessions__row"
            key={row.scheduleRef}
          >
            <span className="timeline-activity-planned-sessions__summary">
              <span
                className="timeline-activity-planned-sessions__name"
                title={row.name}
              >
                {row.name}
              </span>
            </span>
            {independentChildren ||
            mainRunning ||
            mainPaused ||
            (sessions ?? []).some(
              (session) => session.plannedScheduleRef === row.scheduleRef,
            ) ? (
              <SessionSubjectControls
                kind="activity"
                subjectRef={activityRef}
                plannedScheduleRef={row.scheduleRef}
                label={row.name}
                variant="detail"
                compactRuntime
                inspectorSummary
                showUnstartedStatus
                unstartedStatus={
                  !independentChildren && mainPaused
                    ? 'Principale in pausa'
                    : 'Non avviata'
                }
                playEnabled={independentChildren || mainRunning}
                {...(locale ? { locale } : {})}
                {...(timeZone ? { timeZone } : {})}
              />
            ) : (
              <span className="timeline-activity-planned-sessions__state">
                {mainStopped
                  ? 'Da verificare'
                  : mainPaused
                    ? 'Principale in pausa'
                    : 'Avvia prima la principale'}
              </span>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
