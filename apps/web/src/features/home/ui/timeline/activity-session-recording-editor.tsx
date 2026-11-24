import { Temporal } from '@dante/time';
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import { createWebFetch } from '../../../../platform/api/web-fetch';
import {
  parsePlannedSessions,
  type PlannedSessionStructure,
} from '../../../temporal/activity-planned-sessions-card-detail';
import './activity-session-recording-editor.css';

type Pause = { started_at: string; ended_at: string | null };
type Attempt = {
  session_ref: string;
  planned_schedule_ref: string | null;
  timing_material_state_ref: string;
  started_at: string;
  ended_at: string | null;
  pause_ranges: Pause[];
};
type Row = {
  key: string;
  plannedRef: string | null;
  name: string;
  attempt: Attempt | null;
};
type Draft = {
  start: string;
  end: string;
  startChoice: ClockChoice;
  endChoice: ClockChoice;
  pauses: {
    start: string;
    end: string;
    startChoice: ClockChoice;
    endChoice: ClockChoice;
  }[];
};
type ClockChoice = 'reject' | 'earlier' | 'later';

function webFetch(path: string, init?: RequestInit): Promise<Response> {
  return createWebFetch(globalThis.fetch)(path, init);
}

function local(instant: string, zone: string): string {
  return Temporal.Instant.from(instant)
    .toZonedDateTimeISO(zone)
    .toPlainDateTime()
    .toString({ smallestUnit: 'second' });
}

function ambiguous(value: string, zone: string): boolean {
  if (!value) return false;
  try {
    const plain = Temporal.PlainDateTime.from(value);
    const earlier = plain.toZonedDateTime(zone, { disambiguation: 'earlier' });
    const later = plain.toZonedDateTime(zone, { disambiguation: 'later' });
    return (
      earlier.toPlainDateTime().equals(plain) &&
      later.toPlainDateTime().equals(plain) &&
      !earlier.toInstant().equals(later.toInstant())
    );
  } catch {
    return false;
  }
}

function choiceFor(value: string, zone: string): ClockChoice {
  const clock = local(value, zone);
  if (!ambiguous(clock, zone)) return 'reject';
  const first = Temporal.PlainDateTime.from(clock)
    .toZonedDateTime(zone, { disambiguation: 'earlier' })
    .toInstant();
  return first.equals(Temporal.Instant.from(value)) ? 'earlier' : 'later';
}

function instant(value: string, zone: string, choice: ClockChoice): string {
  if (ambiguous(value, zone) && choice === 'reject')
    throw new Error(
      'Scegli la prima o la seconda occorrenza dell’ora nel cambio di fuso.',
    );
  return Temporal.PlainDateTime.from(value)
    .toZonedDateTime(zone, { disambiguation: choice })
    .toInstant()
    .toString();
}

function draftFrom(attempt: Attempt | null, zone: string): Draft {
  return attempt
    ? {
        start: local(attempt.started_at, zone),
        end: attempt.ended_at ? local(attempt.ended_at, zone) : '',
        startChoice: choiceFor(attempt.started_at, zone),
        endChoice: attempt.ended_at
          ? choiceFor(attempt.ended_at, zone)
          : 'reject',
        pauses: attempt.pause_ranges
          .filter((pause) => pause.ended_at !== null)
          .map((pause) => ({
            start: local(pause.started_at, zone),
            end: local(pause.ended_at!, zone),
            startChoice: choiceFor(pause.started_at, zone),
            endChoice: choiceFor(pause.ended_at!, zone),
          })),
      }
    : {
        start: '',
        end: '',
        startChoice: 'reject',
        endChoice: 'reject',
        pauses: [],
      };
}

function ClockField({
  label,
  value,
  choice,
  zone,
  onChange,
}: Readonly<{
  label: string;
  value: string;
  choice: ClockChoice;
  zone: string;
  onChange: (value: string, choice: ClockChoice) => void;
}>) {
  return (
    <div className="timeline-session-editor__clock">
      <label>
        {label}
        <input
          aria-label={label}
          type="datetime-local"
          step="1"
          required
          value={value}
          onChange={(event) => onChange(event.target.value, 'reject')}
        />
      </label>
      {ambiguous(value, zone) ? (
        <label>
          Ora nel cambio d’ora
          <select
            aria-label={`${label} · occorrenza dell’ora`}
            required
            value={choice}
            onChange={(event) =>
              onChange(value, event.target.value as ClockChoice)
            }
          >
            <option value="reject" disabled>
              Scegli quale ora
            </option>
            <option value="earlier">Prima volta</option>
            <option value="later">Seconda volta</option>
          </select>
        </label>
      ) : null}
    </div>
  );
}

function SessionSegmentPreview({
  draft,
  zone,
}: Readonly<{ draft: Draft; zone: string }>) {
  try {
    if (
      !draft.start ||
      !draft.end ||
      draft.pauses.some((pause) => !pause.start || !pause.end)
    )
      return null;
    const start = Temporal.Instant.from(
      instant(draft.start, zone, draft.startChoice),
    ).epochMilliseconds;
    const end = Temporal.Instant.from(
      instant(draft.end, zone, draft.endChoice),
    ).epochMilliseconds;
    if (end <= start) return null;
    const pauses = draft.pauses
      .map((pause) => ({
        start: Temporal.Instant.from(
          instant(pause.start, zone, pause.startChoice),
        ).epochMilliseconds,
        end: Temporal.Instant.from(instant(pause.end, zone, pause.endChoice))
          .epochMilliseconds,
      }))
      .sort((left, right) => left.start - right.start);
    if (
      pauses.some(
        (pause, index) =>
          pause.start < (index ? pauses[index - 1]!.end : start) ||
          pause.end <= pause.start ||
          pause.end > end,
      )
    )
      return null;
    const segments: { kind: 'active' | 'pause'; duration: number }[] = [];
    let cursor = start;
    for (const pause of pauses) {
      if (pause.start > cursor)
        segments.push({ kind: 'active', duration: pause.start - cursor });
      segments.push({ kind: 'pause', duration: pause.end - pause.start });
      cursor = pause.end;
    }
    if (cursor < end) segments.push({ kind: 'active', duration: end - cursor });
    const activeMinutes = Math.round(
      segments
        .filter((part) => part.kind === 'active')
        .reduce((total, part) => total + part.duration, 0) / 60000,
    );
    return (
      <div
        className="timeline-session-editor__preview"
        aria-label={`Tempo attivo ${activeMinutes} minuti; ${pauses.length} pause`}
      >
        <div className="timeline-session-editor__track" aria-hidden="true">
          {segments.map((part, index) => (
            <span
              key={index}
              className={`is-${part.kind}`}
              style={{ flexGrow: part.duration }}
            />
          ))}
        </div>
        <span>
          Tempo attivo {Math.floor(activeMinutes / 60)} h{' '}
          {String(activeMinutes % 60).padStart(2, '0')} min · {pauses.length}{' '}
          {pauses.length === 1 ? 'pausa' : 'pause'}
        </span>
      </div>
    );
  } catch {
    return null;
  }
}

function parseAttempts(value: unknown): Attempt[] {
  if (!Array.isArray(value)) throw new Error('Registrazioni non disponibili.');
  return value.map((row: unknown) => {
    if (
      typeof row !== 'object' ||
      row === null ||
      !('session_ref' in row) ||
      typeof row.session_ref !== 'string' ||
      !('started_at' in row) ||
      typeof row.started_at !== 'string' ||
      !('pause_ranges' in row) ||
      !Array.isArray(row.pause_ranges)
    ) {
      throw new Error('Registrazione non valida.');
    }
    return row as Attempt;
  });
}

async function readJson(path: string): Promise<unknown> {
  const response = await webFetch(path, { cache: 'no-store' });
  if (!response.ok)
    throw new Error('Impossibile caricare le Sessioni. Riprova.');
  return response.json();
}

async function save(
  activityRef: string,
  row: Row,
  draft: Draft,
  zone: string,
  operationId: string,
): Promise<void> {
  if (
    !draft.start ||
    !draft.end ||
    draft.pauses.some((pause) => !pause.start || !pause.end)
  ) {
    throw new Error('Inserisci inizio e fine di ogni intervallo.');
  }
  const start = instant(draft.start, zone, draft.startChoice);
  const end = instant(draft.end, zone, draft.endChoice);
  const pauses = draft.pauses.map((pause) => ({
    started_at: instant(pause.start, zone, pause.startChoice),
    ended_at: instant(pause.end, zone, pause.endChoice),
  }));
  const sorted = [...pauses].sort((a, b) =>
    a.started_at.localeCompare(b.started_at),
  );
  if (
    Temporal.Instant.compare(start, end) >= 0 ||
    Temporal.Instant.compare(end, Temporal.Now.instant()) > 0 ||
    sorted.some(
      (pause, index) =>
        Temporal.Instant.compare(
          pause.started_at,
          index ? sorted[index - 1]!.ended_at : start,
        ) <= 0 ||
        Temporal.Instant.compare(pause.started_at, pause.ended_at) >= 0 ||
        Temporal.Instant.compare(pause.ended_at, end) > 0,
    )
  ) {
    throw new Error(
      'Controlla inizio, fine e pause: devono essere nel passato e in ordine.',
    );
  }
  const csrfResponse = await webFetch('/api/v1/auth/session');
  if (!csrfResponse.ok) throw new Error('Sessione di accesso scaduta.');
  const authentication = (await csrfResponse.json()) as { csrf_token?: string };
  if (!authentication.csrf_token)
    throw new Error('Sessione di accesso scaduta.');
  const response = await webFetch(
    `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/sessions/editor`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Dante-CSRF': authentication.csrf_token,
      },
      body: JSON.stringify({
        operation_id: operationId,
        planned_schedule_ref: row.plannedRef,
        session_ref: row.attempt?.session_ref ?? null,
        expected_material_state_ref:
          row.attempt?.timing_material_state_ref ?? null,
        started_at: start,
        ended_at: end,
        pause_ranges: pauses,
      }),
    },
  );
  if (!response.ok) {
    const problem = (await response.json()) as { detail?: string };
    throw new Error(problem.detail || 'Registrazione non salvata. Riprova.');
  }
}

export async function activityHasSessionRecordings(
  activityRef: string,
): Promise<boolean> {
  const base = `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}`;
  const [structureValue, attemptsValue] = await Promise.all([
    readJson(`${base}/children`),
    readJson(`${base}/sessions/editor`),
  ]);
  const structure = parsePlannedSessions(structureValue, activityRef);
  const raw = structureValue as { session_capture_mode?: string };
  return (
    structure.rows.length > 0 ||
    (raw.session_capture_mode !== undefined &&
      raw.session_capture_mode !== 'disabled') ||
    parseAttempts(attemptsValue).length > 0
  );
}

export function ActivitySessionRecordingEditor({
  activityRef,
  activityTitle,
  timeZone,
  onClose,
}: Readonly<{
  activityRef: string;
  activityTitle: string;
  timeZone: string;
  onClose: () => void;
}>) {
  const [structure, setStructure] = useState<PlannedSessionStructure | null>(
    null,
  );
  const [mainEnabled, setMainEnabled] = useState(false);
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<string | null>(null);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);
  const operation = useRef<string | null>(null);
  const closeButton = useRef<HTMLButtonElement>(null);

  async function reload() {
    const base = `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}`;
    const [structureValue, attemptsValue] = await Promise.all([
      readJson(`${base}/children`),
      readJson(`${base}/sessions/editor`),
    ]);
    const raw = structureValue as { session_capture_mode?: string };
    setMainEnabled(
      raw.session_capture_mode === 'live' ||
        raw.session_capture_mode === 'record_and_live',
    );
    setStructure(parsePlannedSessions(structureValue, activityRef));
    setAttempts(parseAttempts(attemptsValue));
  }

  useEffect(() => {
    closeButton.current?.focus();
    let active = true;
    const base = `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}`;
    void Promise.all([
      readJson(`${base}/children`),
      readJson(`${base}/sessions/editor`),
    ])
      .then(([structureValue, attemptsValue]) => {
        if (!active) return;
        const raw = structureValue as { session_capture_mode?: string };
        setMainEnabled(
          raw.session_capture_mode === 'live' ||
            raw.session_capture_mode === 'record_and_live',
        );
        setStructure(parsePlannedSessions(structureValue, activityRef));
        setAttempts(parseAttempts(attemptsValue));
      })
      .catch((reason: unknown) => {
        if (active)
          setError(
            reason instanceof Error
              ? reason.message
              : 'Caricamento non riuscito.',
          );
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [activityRef]);

  const forConfigured = (plannedRef: string | null, name: string): Row[] => {
    const matches = attempts.filter(
      (attempt) => attempt.planned_schedule_ref === plannedRef,
    );
    return matches.length
      ? matches.map((attempt) => ({
          key: attempt.session_ref,
          plannedRef,
          name,
          attempt,
        }))
      : [{ key: plannedRef ?? 'main', plannedRef, name, attempt: null }];
  };
  const rows: Row[] = [
    ...(mainEnabled ||
    attempts.some((attempt) => attempt.planned_schedule_ref === null)
      ? forConfigured(null, 'Sessione attività')
      : []),
    ...(structure?.rows.flatMap((planned) =>
      forConfigured(planned.scheduleRef, planned.name),
    ) ?? []),
  ];
  const mainReady = attempts.some(
    (attempt) =>
      attempt.planned_schedule_ref === null && attempt.ended_at !== null,
  );

  function choose(row: Row) {
    if (row.attempt?.ended_at === null) return;
    setSelected(row.key);
    setDraft(draftFrom(row.attempt, timeZone));
    setError('');
    operation.current = null;
  }

  function updateDraft(next: Draft) {
    setDraft(next);
    setError('');
    operation.current = null;
  }

  async function commit(row: Row) {
    if (!draft || saving) return;
    setSaving(true);
    setError('');
    operation.current ??= crypto.randomUUID();
    try {
      await save(activityRef, row, draft, timeZone, operation.current);
      await reload();
      window.dispatchEvent(
        new CustomEvent('dante:session-changed', { detail: activityRef }),
      );
      setSelected(null);
      setDraft(null);
      operation.current = null;
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Registrazione non salvata.',
      );
    } finally {
      setSaving(false);
    }
  }

  return createPortal(
    <div
      className="timeline-session-editor__backdrop"
      onKeyDown={(event) => {
        if (event.key === 'Escape' && !saving) onClose();
        if (event.key === 'Tab') {
          const dialog =
            event.currentTarget.querySelector<HTMLElement>('[role="dialog"]');
          const controls = Array.from(
            dialog?.querySelectorAll<HTMLElement>(
              'button:not(:disabled), input:not(:disabled), select:not(:disabled), [tabindex]:not([tabindex="-1"])',
            ) ?? [],
          );
          const first = controls[0];
          const last = controls.at(-1);
          if (event.shiftKey && document.activeElement === first && last) {
            event.preventDefault();
            last.focus();
          } else if (
            !event.shiftKey &&
            document.activeElement === last &&
            first
          ) {
            event.preventDefault();
            first.focus();
          }
        }
      }}
    >
      <section
        className="timeline-session-editor"
        role="dialog"
        aria-modal="true"
        aria-labelledby="session-editor-title"
      >
        <header className="timeline-session-editor__header">
          <div>
            <span className="timeline-session-editor__eyebrow">
              {activityTitle}
            </span>
            <h2 id="session-editor-title">Registrazioni delle Sessioni</h2>
          </div>
          <button
            ref={closeButton}
            type="button"
            aria-label="Chiudi registrazioni"
            onClick={onClose}
            disabled={saving}
          >
            ×
          </button>
        </header>
        <div className="timeline-session-editor__content">
          <p className="timeline-session-editor__zone">
            Orari in {timeZone}. La pianificazione resta invariata.
          </p>
          {loading ? <p>Caricamento Sessioni…</p> : null}
          {!loading && rows.length === 0 ? (
            <p>Nessuna Sessione configurata.</p>
          ) : null}
          {rows.map((row) => {
            const editing = selected === row.key && draft !== null;
            const waitingForMain =
              row.plannedRef !== null && mainEnabled && !mainReady;
            return (
              <article key={row.key} className="timeline-session-editor__row">
                <div className="timeline-session-editor__row-header">
                  <div>
                    <h3>{row.name}</h3>
                    <span>
                      {row.attempt?.ended_at
                        ? `${local(row.attempt.started_at, timeZone).replace('T', ' ')} – ${local(row.attempt.ended_at, timeZone).replace('T', ' ')}`
                        : row.attempt
                          ? 'In corso · termina la Sessione prima di correggerla'
                          : waitingForMain
                            ? 'Registra prima la Sessione attività'
                            : 'Da registrare'}
                    </span>
                  </div>
                  {row.attempt?.ended_at === null ? null : (
                    <button
                      type="button"
                      disabled={waitingForMain}
                      onClick={() =>
                        editing ? setSelected(null) : choose(row)
                      }
                    >
                      {editing
                        ? 'Annulla'
                        : row.attempt
                          ? 'Correggi'
                          : 'Registra'}
                    </button>
                  )}
                </div>
                {!editing && row.attempt?.pause_ranges.length ? (
                  <p className="timeline-session-editor__summary">
                    {row.attempt.pause_ranges.length}{' '}
                    {row.attempt.pause_ranges.length === 1
                      ? 'pausa registrata'
                      : 'pause registrate'}
                  </p>
                ) : null}
                {editing ? (
                  <form
                    onSubmit={(event) => {
                      event.preventDefault();
                      void commit(row);
                    }}
                  >
                    <div className="timeline-session-editor__time-grid">
                      <ClockField
                        label={`${row.name} · Inizio`}
                        value={draft.start}
                        choice={draft.startChoice}
                        zone={timeZone}
                        onChange={(start, startChoice) =>
                          updateDraft({ ...draft, start, startChoice })
                        }
                      />
                      <ClockField
                        label={`${row.name} · Fine`}
                        value={draft.end}
                        choice={draft.endChoice}
                        zone={timeZone}
                        onChange={(end, endChoice) =>
                          updateDraft({ ...draft, end, endChoice })
                        }
                      />
                    </div>
                    <div className="timeline-session-editor__pauses">
                      <div className="timeline-session-editor__pause-heading">
                        <strong>Pause</strong>
                        <button
                          type="button"
                          onClick={() =>
                            updateDraft({
                              ...draft,
                              pauses: [
                                ...draft.pauses,
                                {
                                  start: '',
                                  end: '',
                                  startChoice: 'reject',
                                  endChoice: 'reject',
                                },
                              ],
                            })
                          }
                        >
                          + Pausa
                        </button>
                      </div>
                      {draft.pauses.map((pause, index) => (
                        <div
                          className="timeline-session-editor__pause-row"
                          key={index}
                        >
                          <ClockField
                            label={`Pausa ${index + 1} · Da`}
                            value={pause.start}
                            choice={pause.startChoice}
                            zone={timeZone}
                            onChange={(start, startChoice) =>
                              updateDraft({
                                ...draft,
                                pauses: draft.pauses.map((p, i) =>
                                  i === index
                                    ? { ...p, start, startChoice }
                                    : p,
                                ),
                              })
                            }
                          />
                          <ClockField
                            label={`Pausa ${index + 1} · A`}
                            value={pause.end}
                            choice={pause.endChoice}
                            zone={timeZone}
                            onChange={(end, endChoice) =>
                              updateDraft({
                                ...draft,
                                pauses: draft.pauses.map((p, i) =>
                                  i === index ? { ...p, end, endChoice } : p,
                                ),
                              })
                            }
                          />
                          <button
                            type="button"
                            aria-label={`Rimuovi pausa ${index + 1}`}
                            onClick={() =>
                              updateDraft({
                                ...draft,
                                pauses: draft.pauses.filter(
                                  (_, i) => i !== index,
                                ),
                              })
                            }
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                    <SessionSegmentPreview draft={draft} zone={timeZone} />
                    {error ? (
                      <p
                        className="timeline-session-editor__error"
                        role="alert"
                      >
                        {error}
                      </p>
                    ) : null}
                    <div className="timeline-session-editor__save">
                      <button type="submit" disabled={saving}>
                        {saving ? 'Salvataggio…' : 'Salva registrazione'}
                      </button>
                    </div>
                  </form>
                ) : null}
              </article>
            );
          })}
          {error && selected === null ? (
            <p className="timeline-session-editor__error" role="alert">
              {error}
            </p>
          ) : null}
        </div>
      </section>
    </div>,
    document.body,
  );
}
