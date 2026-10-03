import { useEffect, useState } from 'react';

import { createWebFetch } from '../../platform/api/web-fetch';
import { ActualRealizationControls } from './actual-realization-controls';
import { SessionSubjectControls } from './session-subject-controls';

type CaptureMode = 'disabled' | 'record' | 'live' | 'record_and_live';

type Schedule = Readonly<{
  scheduleRef: string;
  temporalForm: string;
  start: string | null;
  end: string | null;
}>;

type Child = Readonly<{
  activityRef: string;
  title: string;
  requirement: 'required' | 'optional';
  order: number;
  captureMode: CaptureMode;
  schedules: readonly Schedule[];
}>;

type Structure = Readonly<{
  captureMode: CaptureMode;
  childGuardMode: 'none' | 'confirm' | 'block';
  schedules: readonly Schedule[];
  children: readonly Child[];
}>;

function object(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('La struttura Activity ricevuta non è valida.');
  }
  return value as Record<string, unknown>;
}

function schedule(value: unknown): Schedule {
  const row = object(value);
  if (
    typeof row.schedule_ref !== 'string' ||
    typeof row.temporal_form !== 'string'
  ) {
    throw new Error('Uno Schedule della struttura non è valido.');
  }
  const start =
    row.starts_local_at ?? row.starts_at ?? row.start_date ?? row.local_date;
  const end = row.ends_local_at ?? row.ends_at ?? row.end_date_exclusive;
  if (start !== null && start !== undefined && typeof start !== 'string') {
    throw new Error('La collocazione dello Schedule non è valida.');
  }
  if (end !== null && end !== undefined && typeof end !== 'string') {
    throw new Error('La fine dello Schedule non è valida.');
  }
  return Object.freeze({
    scheduleRef: row.schedule_ref,
    temporalForm: row.temporal_form,
    start: start ?? null,
    end: end ?? null,
  });
}

function captureMode(value: unknown): CaptureMode {
  if (
    value !== 'disabled' &&
    value !== 'record' &&
    value !== 'live' &&
    value !== 'record_and_live'
  ) {
    throw new Error('La policy Session corrente non è valida.');
  }
  return value;
}

function parseStructure(value: unknown, parentRef: string): Structure {
  const row = object(value);
  if (
    row.parent_activity_ref !== parentRef ||
    !Array.isArray(row.schedules) ||
    !Array.isArray(row.children) ||
    (row.child_guard_mode !== 'none' &&
      row.child_guard_mode !== 'confirm' &&
      row.child_guard_mode !== 'block')
  ) {
    throw new Error('La struttura Activity corrente non è disponibile.');
  }
  return Object.freeze({
    captureMode: captureMode(row.session_capture_mode),
    childGuardMode: row.child_guard_mode,
    schedules: Object.freeze(row.schedules.map(schedule)),
    children: Object.freeze(
      row.children.map((entry) => {
        const child = object(entry);
        if (
          typeof child.child_activity_ref !== 'string' ||
          typeof child.child_title !== 'string' ||
          (child.requirement_code !== 'required' &&
            child.requirement_code !== 'optional') ||
          typeof child.presentation_order !== 'number' ||
          !Array.isArray(child.schedules)
        ) {
          throw new Error('Una sotto-attività corrente non è valida.');
        }
        return Object.freeze({
          activityRef: child.child_activity_ref,
          title: child.child_title,
          requirement: child.requirement_code,
          order: child.presentation_order,
          captureMode: captureMode(child.session_capture_mode),
          schedules: Object.freeze(child.schedules.map(schedule)),
        });
      }),
    ),
  });
}

function Schedules({ rows }: Readonly<{ rows: readonly Schedule[] }>) {
  if (rows.length === 0) return <small>Nessuno Schedule corrente.</small>;
  return (
    <ul>
      {rows.map((row) => (
        <li key={row.scheduleRef}>
          Schedule · {row.temporalForm} · {row.start ?? 'senza inizio'}
          {row.end === null ? '' : ` → ${row.end}`}
        </li>
      ))}
    </ul>
  );
}

function CaptureControls({
  activityRef,
  title,
  mode,
}: Readonly<{
  activityRef: string;
  title: string;
  mode: CaptureMode;
}>) {
  return (
    <SessionSubjectControls
      kind="activity"
      subjectRef={activityRef}
      label={title}
      allowLive={mode === 'live' || mode === 'record_and_live'}
      allowManual={mode === 'record' || mode === 'record_and_live'}
    />
  );
}

function ChildDetail({ child }: Readonly<{ child: Child }>) {
  const [open, setOpen] = useState(false);
  return (
    <details
      data-activity-child={child.activityRef}
      onToggle={(event) => setOpen(event.currentTarget.open)}
    >
      <summary>
        {child.order}. {child.title} · {child.requirement}
      </summary>
      {open ? (
        <>
          <p>Sessioni: {child.captureMode}</p>
          <Schedules rows={child.schedules} />
          <CaptureControls
            activityRef={child.activityRef}
            title={child.title}
            mode={child.captureMode}
          />
          <ActualRealizationControls
            kind="activity"
            subjectRef={child.activityRef}
          />
        </>
      ) : null}
    </details>
  );
}

export function ActivityStructureReadback({
  activityRef,
}: Readonly<{ activityRef: string }>) {
  const [structure, setStructure] = useState<Structure | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    let cancelled = false;
    setStructure(null);
    setError(null);
    const webFetch = createWebFetch(globalThis.fetch);
    void webFetch(
      `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/children`,
    )
      .then(async (response) => {
        if (!response.ok)
          throw new Error(`Lettura struttura rifiutata (${response.status}).`);
        return parseStructure(await response.json(), activityRef);
      })
      .then((value) => {
        if (!cancelled) setStructure(value);
      })
      .catch((reason: unknown) => {
        if (!cancelled)
          setError(
            reason instanceof Error
              ? reason.message
              : 'Struttura non disponibile.',
          );
      });
    return () => {
      cancelled = true;
    };
  }, [activityRef]);

  return (
    <section
      className="timeline-activity-structure"
      data-activity-structure={activityRef}
    >
      <strong>Struttura Activity</strong>
      {error !== null ? <p role="alert">{error}</p> : null}
      {structure === null && error === null ? (
        <p>Caricamento struttura…</p>
      ) : null}
      {structure !== null ? (
        <>
          <p>
            Sessioni: {structure.captureMode} · Figli richiesti:{' '}
            {structure.childGuardMode}
          </p>
          <Schedules rows={structure.schedules} />
          <CaptureControls
            activityRef={activityRef}
            title="Activity"
            mode={structure.captureMode}
          />
          {structure.children.map((child) => (
            <ChildDetail key={child.activityRef} child={child} />
          ))}
        </>
      ) : null}
    </section>
  );
}
