import { Temporal } from '@dante/time';
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import { createWebFetch } from '../../../../platform/api/web-fetch';
import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import {
  parsePlannedSessions,
  type PlannedSessionStructure,
} from '../../../temporal/activity-planned-sessions-card-detail';
import './activity-session-recording-editor.css';
import '../../../temporal-create/ui/temporal-create-u1.css';
import '../../../temporal-create/ui/temporal-create-core-u2.css';
import '../../../temporal-create/ui/temporal-create-date-picker.css';

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
type ActiveInterval = {
  start: string;
  end: string;
  startChoice: ClockChoice;
  endChoice: ClockChoice;
};
type Draft = { intervals: ActiveInterval[] };
type ClockChoice = 'reject' | 'earlier' | 'later';
type Issue = Readonly<{ field: string; message: string }>;

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
  if (attempt?.ended_at) {
    return {
      intervals: activeSlices(
        attempt.started_at,
        attempt.ended_at,
        attempt.pause_ranges,
      ).map(({ start, end }) => {
        const startInstant = new Date(start).toISOString();
        const endInstant = new Date(end).toISOString();
        return {
          start: local(startInstant, zone),
          end: local(endInstant, zone),
          startChoice: choiceFor(startInstant, zone),
          endChoice: choiceFor(endInstant, zone),
        };
      }),
    };
  }
  return {
    intervals: [
      {
        start: local(
          Temporal.Now.instant().subtract({ minutes: 30 }).toString(),
          zone,
        ).slice(0, 16),
        end: local(Temporal.Now.instant().toString(), zone).slice(0, 16),
        startChoice: 'reject',
        endChoice: 'reject',
      },
    ],
  };
}

function IntervalFields({
  interval,
  index,
  zone,
  issue,
  onChange,
  onRemove,
}: Readonly<{
  interval: ActiveInterval;
  index: number;
  zone: string;
  issue: Issue | null;
  onChange: (interval: ActiveInterval) => void;
  onRemove?: (() => void) | undefined;
}>) {
  const label = `Intervallo ${index + 1}`;
  const invalid = issue?.field === `interval-${index}`;
  const patch = (field: keyof ActiveInterval, value: string) =>
    onChange({ ...interval, [field]: value });
  return (
    <div
      className="timeline-session-editor__interval"
      data-invalid={invalid || undefined}
    >
      <span className="timeline-session-editor__interval-label">{label}</span>
      <div className="timeline-session-editor__interval-fields temporal-schedule-time-grid">
        <TemporalCreateDatePicker
          label={`${label} · Data inizio`}
          locale="it"
          value={interval.start.slice(0, 10)}
          invalid={invalid}
          onChange={(date) =>
            onChange({
              ...interval,
              start: `${date}T${interval.start.slice(11)}`,
              startChoice: 'reject',
            })
          }
        />
        <TimeControl
          label={`${label} · Inizio`}
          value={interval.start.slice(11, 16)}
          dataPath={`session-recording.${index}.start`}
          invalid={invalid}
          onChange={(time) =>
            onChange({
              ...interval,
              start: `${interval.start.slice(0, 10)}T${time}:00`,
              startChoice: 'reject',
            })
          }
        />
        <span className="timeline-session-editor__arrow" aria-hidden="true">
          →
        </span>
        <TimeControl
          label={`${label} · Fine`}
          value={interval.end.slice(11, 16)}
          dataPath={`session-recording.${index}.end`}
          invalid={invalid}
          onChange={(time) =>
            onChange({
              ...interval,
              end: `${interval.end.slice(0, 10)}T${time}:00`,
              endChoice: 'reject',
            })
          }
        />
        <TemporalCreateDatePicker
          label={`${label} · Data fine`}
          align="end"
          locale="it"
          value={interval.end.slice(0, 10)}
          invalid={invalid}
          onChange={(date) =>
            onChange({
              ...interval,
              end: `${date}T${interval.end.slice(11)}`,
              endChoice: 'reject',
            })
          }
        />
        {onRemove ? (
          <button
            className="timeline-session-editor__remove"
            type="button"
            aria-label={`Rimuovi intervallo ${index + 1}`}
            onClick={onRemove}
          >
            ×
          </button>
        ) : null}
      </div>
      {ambiguous(interval.start, zone) ? (
        <label>
          {label} · Inizio nel cambio d’ora
          <select
            aria-label={`${label} · Inizio · occorrenza dell’ora`}
            required
            value={interval.startChoice}
            onChange={(event) => patch('startChoice', event.target.value)}
          >
            <option value="reject" disabled>
              Scegli quale ora
            </option>
            <option value="earlier">Prima volta</option>
            <option value="later">Seconda volta</option>
          </select>
        </label>
      ) : null}
      {ambiguous(interval.end, zone) ? (
        <label>
          {label} · Fine nel cambio d’ora
          <select
            aria-label={`${label} · Fine · occorrenza dell’ora`}
            required
            value={interval.endChoice}
            onChange={(event) => patch('endChoice', event.target.value)}
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

type ResolvedInterval = { start: number; end: number };

function resolveIntervals(draft: Draft, zone: string): ResolvedInterval[] {
  return draft.intervals.map((interval) => ({
    start: Temporal.Instant.from(
      instant(interval.start, zone, interval.startChoice),
    ).epochMilliseconds,
    end: Temporal.Instant.from(instant(interval.end, zone, interval.endChoice))
      .epochMilliseconds,
  }));
}

function nextInterval(draft: Draft): ActiveInterval {
  const last = draft.intervals.at(-1)!;
  const start = Temporal.PlainDateTime.from(last.end).add({ minutes: 30 });
  return {
    start: start.toString({ smallestUnit: 'minute' }),
    end: start.add({ hours: 1 }).toString({ smallestUnit: 'minute' }),
    startChoice: 'reject',
    endChoice: 'reject',
  };
}

function SessionSegmentPreview({
  draft,
  zone,
}: Readonly<{ draft: Draft; zone: string }>) {
  let ranges: ResolvedInterval[];
  try {
    ranges = resolveIntervals(draft, zone);
  } catch {
    return null;
  }
  if (
    !ranges.length ||
    ranges.some(
      (range, index) =>
        range.end <= range.start ||
        (index > 0 && range.start <= ranges[index - 1]!.end),
    )
  )
    return null;
  const start = ranges[0]!.start;
  const end = ranges.at(-1)!.end;
  const activeMinutes = Math.round(
    ranges.reduce((total, range) => total + range.end - range.start, 0) / 60000,
  );
  return (
    <div
      className="timeline-session-editor__preview"
      aria-label={`Tempo attivo ${activeMinutes} minuti; ${ranges.length - 1} pause`}
    >
      <div className="timeline-session-editor__track" aria-hidden="true">
        {ranges.map((range, index) => (
          <span
            key={index}
            className="is-active"
            style={{
              left: `${((range.start - start) / (end - start)) * 100}%`,
              width: `${((range.end - range.start) / (end - start)) * 100}%`,
            }}
          />
        ))}
      </div>
      <span>
        Tempo attivo {Math.floor(activeMinutes / 60)} h{' '}
        {String(activeMinutes % 60).padStart(2, '0')} min · {ranges.length - 1}{' '}
        {ranges.length === 2 ? 'pausa' : 'pause'}
      </span>
    </div>
  );
}

function activeSlices(
  start: string,
  end: string,
  pauses: readonly Pause[],
): Array<{ start: number; end: number }> {
  const result: Array<{ start: number; end: number }> = [];
  let cursor = Date.parse(start);
  for (const pause of pauses) {
    const pauseStart = Date.parse(pause.started_at);
    if (pauseStart > cursor) result.push({ start: cursor, end: pauseStart });
    cursor = Date.parse(pause.ended_at ?? end);
  }
  if (cursor < Date.parse(end))
    result.push({ start: cursor, end: Date.parse(end) });
  return result;
}

function SessionSharedTimeline({
  main,
  children,
  zone,
}: Readonly<{ main: Attempt; children: readonly Row[]; zone: string }>) {
  if (!main.ended_at) return null;
  const start = Date.parse(main.started_at);
  const duration = Date.parse(main.ended_at) - start;
  if (!Number.isFinite(duration) || duration <= 0) return null;
  const lanes = [
    { name: 'Sessione attività', attempt: main },
    ...children
      .filter((row) => row.attempt?.ended_at)
      .map((row) => ({ name: row.name, attempt: row.attempt! })),
  ];
  return (
    <div
      className="timeline-session-editor__shared"
      aria-label="Intervalli delle Sessioni sulla stessa scala oraria"
    >
      <div className="timeline-session-editor__shared-hours">
        <span>
          {local(main.started_at, zone).replace('T', ' ').slice(0, 16)}
        </span>
        <span>{local(main.ended_at, zone).replace('T', ' ').slice(0, 16)}</span>
      </div>
      {lanes.map(({ name, attempt }) => (
        <div
          className="timeline-session-editor__lane"
          key={attempt.session_ref}
        >
          <span title={name}>{name}</span>
          <div
            className="timeline-session-editor__lane-track"
            aria-label={`${name}: ${local(attempt.started_at, zone)} – ${local(attempt.ended_at!, zone)}`}
          >
            {activeSlices(
              attempt.started_at,
              attempt.ended_at!,
              attempt.pause_ranges,
            ).map((slice, index) => (
              <span
                key={index}
                className={attempt === main ? 'is-main' : 'is-child'}
                style={{
                  left: `${((slice.start - start) / duration) * 100}%`,
                  width: `${((slice.end - slice.start) / duration) * 100}%`,
                }}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function validateDraft(
  row: Row,
  draft: Draft,
  zone: string,
  main: Attempt | null,
  children: readonly Attempt[],
): Issue | null {
  if (!draft.intervals.length || draft.intervals.length > 100)
    return {
      field: 'interval-0',
      message: 'Sono ammessi da 1 a 100 intervalli.',
    };
  const ranges: ResolvedInterval[] = [];
  for (const [index, interval] of draft.intervals.entries()) {
    const field = `interval-${index}`;
    if (!interval.start || !interval.end)
      return { field, message: `Completa l’intervallo ${index + 1}.` };
    try {
      const [resolved] = resolveIntervals({ intervals: [interval] }, zone);
      if (!resolved) throw new Error('Orario non valido.');
      if (resolved.end <= resolved.start)
        return {
          field,
          message: `La fine dell’intervallo ${index + 1} deve seguire l’inizio.`,
        };
      if (resolved.end > Temporal.Now.instant().epochMilliseconds)
        return {
          field,
          message: 'Gli intervalli effettivi devono essere nel passato.',
        };
      if (ranges.length && resolved.start <= ranges.at(-1)!.end)
        return {
          field,
          message:
            'Gli intervalli devono essere ordinati e separati da una pausa.',
        };
      ranges.push(resolved);
    } catch (reason) {
      return {
        field,
        message:
          reason instanceof Error ? reason.message : 'Controlla gli orari.',
      };
    }
  }
  const candidate = attemptFromRanges(ranges);
  if (row.plannedRef !== null && main?.ended_at && !fitsMain(candidate, main))
    return {
      field: 'interval-0',
      message: 'La Sessione deve rientrare nei tratti attivi della principale.',
    };
  if (
    row.plannedRef === null &&
    children.some((child) => child.ended_at && !fitsMain(child, candidate))
  )
    return {
      field: 'interval-0',
      message: 'La correzione esclude una Sessione secondaria già registrata.',
    };
  return null;
}

function attemptFromRanges(ranges: readonly ResolvedInterval[]) {
  return {
    started_at: new Date(ranges[0]!.start).toISOString(),
    ended_at: new Date(ranges.at(-1)!.end).toISOString(),
    pause_ranges: ranges.slice(1).map((range, index) => ({
      started_at: new Date(ranges[index]!.end).toISOString(),
      ended_at: new Date(range.start).toISOString(),
    })),
  };
}

function fitsMain(
  child: Pick<Attempt, 'started_at' | 'ended_at' | 'pause_ranges'>,
  main: Pick<Attempt, 'started_at' | 'ended_at' | 'pause_ranges'>,
): boolean {
  if (
    !child.ended_at ||
    !main.ended_at ||
    Date.parse(child.started_at) < Date.parse(main.started_at) ||
    Date.parse(child.ended_at) > Date.parse(main.ended_at)
  )
    return false;
  return main.pause_ranges.every((pause) => {
    if (!pause.ended_at) return false;
    const from = Math.max(
      Date.parse(pause.started_at),
      Date.parse(child.started_at),
    );
    const to = Math.min(
      Date.parse(pause.ended_at),
      Date.parse(child.ended_at!),
    );
    return (
      from >= to ||
      child.pause_ranges.some(
        (own) =>
          own.ended_at &&
          Date.parse(own.started_at) <= from &&
          Date.parse(own.ended_at) >= to,
      )
    );
  });
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
  const candidate = attemptFromRanges(resolveIntervals(draft, zone));
  const start = candidate.started_at;
  const end = candidate.ended_at;
  const pauses = candidate.pause_ranges;
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
  const [structureResult, attemptsResult] = await Promise.allSettled([
    readJson(`${base}/children`),
    readJson(`${base}/sessions`),
  ]);
  if (structureResult.status === 'fulfilled') {
    const structure = parsePlannedSessions(structureResult.value, activityRef);
    const raw = structureResult.value as { session_capture_mode?: string };
    if (
      structure.rows.length > 0 ||
      (raw.session_capture_mode !== undefined &&
        raw.session_capture_mode !== 'disabled')
    )
      return true;
  }
  return (
    attemptsResult.status === 'fulfilled' &&
    Array.isArray(attemptsResult.value) &&
    attemptsResult.value.length > 0
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
  const [issue, setIssue] = useState<Issue | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [selectedParent, setSelectedParent] = useState<number | null>(null);
  const [sessionMenu, setSessionMenu] = useState<number | null>(null);
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
  const mainAttempt =
    attempts.find(
      (attempt) =>
        attempt.planned_schedule_ref === null && attempt.ended_at !== null,
    ) ?? null;
  const childAttempts = attempts.filter(
    (attempt) =>
      attempt.planned_schedule_ref !== null && attempt.ended_at !== null,
  );

  function choose(
    row: Row,
    parentIndex: number | null = null,
    parentRange?: ResolvedInterval,
  ) {
    if (row.attempt?.ended_at === null) return;
    setSelected(row.key);
    setSelectedParent(parentIndex);
    setSessionMenu(null);
    setDraft(
      parentRange && !row.attempt
        ? {
            intervals: [
              {
                start: local(
                  new Date(parentRange.start).toISOString(),
                  timeZone,
                ),
                end: local(new Date(parentRange.end).toISOString(), timeZone),
                startChoice: choiceFor(
                  new Date(parentRange.start).toISOString(),
                  timeZone,
                ),
                endChoice: choiceFor(
                  new Date(parentRange.end).toISOString(),
                  timeZone,
                ),
              },
            ],
          }
        : draftFrom(row.attempt, timeZone),
    );
    setError('');
    setIssue(null);
    operation.current = null;
  }

  function updateDraft(next: Draft) {
    setDraft(next);
    setError('');
    setIssue(null);
    operation.current = null;
  }

  async function commit(row: Row) {
    if (!draft || saving) return;
    const invalid = validateDraft(
      row,
      draft,
      timeZone,
      mainEnabled ? mainAttempt : null,
      childAttempts,
    );
    if (invalid) {
      setIssue(invalid);
      setError(invalid.message);
      return;
    }
    setSaving(true);
    setError('');
    setIssue(null);
    operation.current ??= crypto.randomUUID();
    try {
      await save(activityRef, row, draft, timeZone, operation.current);
      await reload();
      window.dispatchEvent(
        new CustomEvent('dante:session-changed', { detail: activityRef }),
      );
      setSelected(null);
      setSelectedParent(null);
      setDraft(null);
      setIssue(null);
      operation.current = null;
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Registrazione non salvata.',
      );
    } finally {
      setSaving(false);
    }
  }

  const children = rows.filter((row) => row.plannedRef !== null);
  const parentRanges = mainAttempt?.ended_at
    ? activeSlices(
        mainAttempt.started_at,
        mainAttempt.ended_at,
        mainAttempt.pause_ranges,
      )
    : [];
  const childParentIndex = (row: Row) => {
    if (!row.attempt) return selected === row.key ? selectedParent : null;
    const started = Date.parse(row.attempt.started_at);
    const index = parentRanges.findIndex(
      (range) => started >= range.start && started < range.end,
    );
    return index >= 0 ? index : 0;
  };

  function renderChildSlot(index: number, allowAdd: boolean) {
    const assigned = children.filter((row) => childParentIndex(row) === index);
    const remaining = children.filter(
      (row) => !row.attempt && row.key !== selected,
    );
    return (
      <div
        className="timeline-session-editor__child-slot"
        aria-label={`Sessioni nell’intervallo ${index + 1}`}
      >
        {assigned.map((row) => renderRow(row))}
        {allowAdd && remaining.length > 0 ? (
          <div className="timeline-session-editor__add-session">
            <button
              type="button"
              aria-expanded={sessionMenu === index}
              onClick={() =>
                setSessionMenu(sessionMenu === index ? null : index)
              }
            >
              + Sessione
            </button>
            {sessionMenu === index ? (
              <div
                className="timeline-session-editor__session-options"
                role="group"
                aria-label={`Scegli Sessione per intervallo ${index + 1}`}
              >
                {remaining.map((row) => (
                  <button
                    key={row.key}
                    type="button"
                    onClick={() => choose(row, index, parentRanges[index])}
                  >
                    {row.name}
                  </button>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}
      </div>
    );
  }

  function renderRow(row: Row) {
    const editing = selected === row.key && draft !== null;
    const mainRow = row.plannedRef === null;
    const waitingForMain = !mainRow && mainEnabled && !mainReady;
    return (
      <article
        key={row.key}
        className={`timeline-session-editor__row${mainRow ? ' is-main' : ' is-child'}${editing ? ' is-editing' : ''}`}
      >
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
              onClick={() => {
                if (editing) {
                  setSelected(null);
                  setDraft(null);
                  setSelectedParent(null);
                } else choose(row, mainRow ? null : childParentIndex(row));
              }}
            >
              {editing ? 'Annulla' : row.attempt ? 'Correggi' : 'Registra'}
            </button>
          )}
        </div>
        {!editing && mainRow && mainAttempt ? (
          <SessionSharedTimeline
            main={mainAttempt}
            children={children}
            zone={timeZone}
          />
        ) : !editing && row.attempt?.ended_at && !mainRow ? (
          <SessionSegmentPreview
            draft={draftFrom(row.attempt, timeZone)}
            zone={timeZone}
          />
        ) : null}
        {!editing && mainRow && mainAttempt ? (
          <div className="timeline-session-editor__parent-intervals">
            {parentRanges.map((range, index) => (
              <section
                key={index}
                className="timeline-session-editor__parent-interval"
              >
                <h4>
                  Intervallo {index + 1}{' '}
                  <span>
                    {local(
                      new Date(range.start).toISOString(),
                      timeZone,
                    ).replace('T', ' ')}{' '}
                    →{' '}
                    {local(new Date(range.end).toISOString(), timeZone).replace(
                      'T',
                      ' ',
                    )}
                  </span>
                </h4>
                {renderChildSlot(index, true)}
              </section>
            ))}
          </div>
        ) : null}
        {editing ? (
          <form
            onSubmit={(event) => {
              event.preventDefault();
              void commit(row);
            }}
          >
            <div className="timeline-session-editor__intervals">
              {draft.intervals.map((interval, index) => (
                <div
                  key={index}
                  className="timeline-session-editor__interval-block"
                >
                  <IntervalFields
                    interval={interval}
                    index={index}
                    zone={timeZone}
                    issue={issue}
                    onChange={(next) =>
                      updateDraft({
                        intervals: draft.intervals.map((item, position) =>
                          position === index ? next : item,
                        ),
                      })
                    }
                    onRemove={
                      draft.intervals.length > 1
                        ? () =>
                            updateDraft({
                              intervals: draft.intervals.filter(
                                (_, position) => position !== index,
                              ),
                            })
                        : undefined
                    }
                  />
                  {mainRow && mainReady ? renderChildSlot(index, false) : null}
                  {mainRow && !mainReady && children.length > 0 ? (
                    <div className="timeline-session-editor__child-slot">
                      <button
                        type="button"
                        disabled
                        title="Registra prima la Sessione attività"
                      >
                        + Sessione
                      </button>
                    </div>
                  ) : null}
                </div>
              ))}
              {draft.intervals.length < 100 ? (
                <button
                  className="timeline-session-editor__add-interval"
                  type="button"
                  onClick={() => {
                    try {
                      updateDraft({
                        intervals: [...draft.intervals, nextInterval(draft)],
                      });
                    } catch {
                      setError(
                        'Completa l’ultimo intervallo prima di aggiungerne un altro.',
                      );
                    }
                  }}
                >
                  ＋ Aggiungi intervallo
                </button>
              ) : null}
            </div>
            <SessionSegmentPreview draft={draft} zone={timeZone} />
            {error ? (
              <p className="timeline-session-editor__error" role="alert">
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
        {mainRow && !mainReady && children.length > 0 ? (
          <p className="timeline-session-editor__waiting">
            Dopo aver registrato la Sessione attività potrai collocare le
            secondarie nei suoi intervalli attivi.
          </p>
        ) : null}
      </article>
    );
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
          <div
            className={
              mainEnabled
                ? 'timeline-session-editor__group has-main'
                : 'timeline-session-editor__group'
            }
          >
            {mainEnabled
              ? rows.filter((row) => row.plannedRef === null).map(renderRow)
              : rows.map(renderRow)}
          </div>
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
