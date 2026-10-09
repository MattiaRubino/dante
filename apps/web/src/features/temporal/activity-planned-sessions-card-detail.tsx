import { useEffect, useState } from 'react';

import { createWebFetch } from '../../platform/api/web-fetch';
import { SessionSubjectControls } from './session-subject-controls';
import './activity-planned-sessions-card-detail.css';

type PlannedSession = Readonly<{
  scheduleRef: string;
  name: string;
  start: string | null;
  end: string | null;
  order: number;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Struttura Activity non valida.');
  }
  return value as Record<string, unknown>;
}

function optionalString(value: unknown): string | null {
  return typeof value === 'string' ? value : null;
}

function parsePlannedSessions(
  value: unknown,
  activityRef: string,
): readonly PlannedSession[] {
  const payload = record(value);
  if (
    payload.parent_activity_ref !== activityRef ||
    !Array.isArray(payload.schedules)
  ) {
    throw new Error('Struttura Activity non valida.');
  }

  return Object.freeze(
      payload.schedules
        .map(record)
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
            start: optionalString(
              row.starts_local_at ??
                row.starts_at ??
                row.start_date ??
                row.local_date,
            ),
            end: optionalString(
              row.ends_local_at ?? row.ends_at ?? row.end_date_exclusive,
            ),
            order,
          });
        })
        .sort((left, right) => left.order - right.order),
  );
}

function compactTime(value: string | null): string {
  if (value === null) return '—';
  const match = value.match(/T(\d{2}:\d{2})/);
  return match?.[1] ?? value;
}

/**
 * Planned Sessions are Activity-owned planning detail, never sibling Timeline
 * cards. The compact band exposes their count; detail controls are only
 * rendered in the Activity Inspector.
 */
export function ActivityPlannedSessionsCardDetail({
  activityRef,
  visible,
  variant = 'detail',
}: Readonly<{
  activityRef: string;
  visible: boolean;
  variant?: 'detail' | 'indicator';
}>) {
  const [rows, setRows] = useState<readonly PlannedSession[] | null>(null);

  useEffect(() => {
    if (!visible) {
      setRows(null);
      return;
    }

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
          setRows(result);
        }
      })
      .catch(() => {
        if (!cancelled && !controller.signal.aborted)
          setRows(Object.freeze([]));
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [activityRef, visible]);

  if (!visible || rows === null || rows.length === 0) return null;

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

  return (
    <div
      className="timeline-activity-planned-sessions"
      data-activity-planned-sessions={activityRef}
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
            <span className="timeline-activity-planned-sessions__name">{row.name}</span>
            <span className="timeline-activity-planned-sessions__time">
              {compactTime(row.start)}–{compactTime(row.end)}
            </span>
          </span>
          <SessionSubjectControls
            kind="activity"
            subjectRef={activityRef}
            plannedScheduleRef={row.scheduleRef}
            label={row.name}
            variant="detail"
            compactRuntime
          />
        </div>
      ))}
    </div>
  );
}
