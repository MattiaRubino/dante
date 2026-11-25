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
  fieldPath,
  issue,
  onChange,
  onRemove,
}: Readonly<{
  interval: ActiveInterval;
  index: number;
  zone: string;
  fieldPath: string;
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
      onClickCapture={(event) => {
        if (!(event.target instanceof Element) ||
          !event.target.closest('.temporal-create-date-picker__trigger')) return;
        const intervalRoot = event.currentTarget;
        window.requestAnimationFrame?.(() => {
          // The picker lives inside our fixed-height scrolling region.
          // Scroll it into view rather than letting the footer clip it.
          const popover = intervalRoot.querySelector<HTMLElement>(
            '.temporal-create-date-picker__popover',
          );
          if (popover && typeof popover.scrollIntoView === 'function') {
            popover.scrollIntoView({ block: 'nearest', inline: 'nearest' });
          }
        });
      }}
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
          dataPath={fieldPath + '.' + index + '.start'}
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
          dataPath={fieldPath + '.' + index + '.end'}
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

function nextInterval(draft: Draft, zone: string): ActiveInterval {
  const last = draft.intervals.at(-1)!;
  const previousEnd = Temporal.Instant.from(
    instant(last.end, zone, last.endChoice),
  ).epochMilliseconds;
  const latestEnd =
    Math.floor(Temporal.Now.instant().epochMilliseconds / 60_000) * 60_000;
  // A new row is an editable draft, not yet a factual recording. When the
  // previous interval reaches "now", offer a past row that the user can
  // separate by adjusting the earlier interval before Save.
  const hasRoom = previousEnd + 60_000 < latestEnd;
  const start = hasRoom
    ? Math.min(previousEnd + 30 * 60_000, latestEnd - 60_000)
    : latestEnd - 30 * 60_000;
  const end = hasRoom ? Math.min(start + 60 * 60_000, latestEnd) : latestEnd;
  const startInstant = new Date(start).toISOString();
  const endInstant = new Date(end).toISOString();
  return {
    start: local(startInstant, zone),
    end: local(endInstant, zone),
    startChoice: choiceFor(startInstant, zone),
    endChoice: choiceFor(endInstant, zone),
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

function validateDraft(
  row: Row,
  draft: Draft,
  zone: string,
  main: Pick<Attempt, 'started_at' | 'ended_at' | 'pause_ranges'> | null,
  children: readonly Pick<
    Attempt,
    'started_at' | 'ended_at' | 'pause_ranges'
  >[],
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
  if (row.plannedRef !== null && main?.ended_at) {
    const slices = activeSlices(main.started_at, main.ended_at, main.pause_ranges);
    for (const [index, range] of ranges.entries()) {
      if (!slices.some((parent) =>
        range.start >= parent.start && range.end <= parent.end,
      )) {
        return {
          field: 'interval-' + index,
          message: 'Il tratto deve rientrare in un intervallo attivo della principale.',
        };
      }
    }
  }
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

type EditorPending = Record<string, Draft>;
type EditorIssues = Record<string, Issue>;

function safeRanges(
  draft: Draft | null | undefined,
  zone: string,
): ResolvedInterval[] {
  if (!draft) return [];
  try {
    const ranges = resolveIntervals(draft, zone);
    return ranges.every(
      (range, index) =>
        Number.isFinite(range.start) &&
        range.end > range.start &&
        (index === 0 || range.start > ranges[index - 1]!.end),
    )
      ? ranges
      : [];
  } catch {
    return [];
  }
}

async function saveEditorGroup(
  activityRef: string,
  updates: readonly { row: Row; draft: Draft }[],
  zone: string,
  operationId: string,
): Promise<Array<{ session_ref: string; timing_material_state_ref: string }>> {
  const auth = await webFetch('/api/v1/auth/session');
  if (!auth.ok) throw new Error('Sessione di accesso scaduta.');
  const session = (await auth.json()) as { csrf_token?: string };
  if (!session.csrf_token) throw new Error('Sessione di accesso scaduta.');
  const commands = updates.map(({ row, draft }, index) => ({
    operation_id: operationId + ':' + index,
    planned_schedule_ref: row.plannedRef,
    session_ref: row.attempt?.session_ref ?? null,
    expected_material_state_ref: row.attempt?.timing_material_state_ref ?? null,
    ...attemptFromRanges(resolveIntervals(draft, zone)),
  }));
  const response = await webFetch(
    '/api/v1/temporal/activities/' +
      encodeURIComponent(activityRef) +
      '/sessions/editor/batch',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Dante-CSRF': session.csrf_token,
      },
      body: JSON.stringify({ commands }),
    },
  );
  if (!response.ok) {
    const problem = (await response.json().catch(() => ({}))) as {
      detail?: string;
    };
    throw new Error(problem.detail || 'Registrazioni non salvate. Riprova.');
  }
  const receipts = (await response.json()) as unknown;
  if (
    !Array.isArray(receipts) ||
    receipts.length !== updates.length ||
    receipts.some((receipt: unknown) => {
      if (!receipt || typeof receipt !== 'object') return true;
      const value = receipt as Record<string, unknown>;
      return (
        typeof value.session_ref !== 'string' ||
        typeof value.timing_material_state_ref !== 'string'
      );
    })
  ) {
    throw new Error(
      'Risposta incompleta: ricarica le registrazioni prima di riprovare.',
    );
  }
  return receipts as Array<{
    session_ref: string;
    timing_material_state_ref: string;
  }>;
}

export function ActivitySessionRecordingEditor({
  activityRef,
  activityTitle,
  timeZone,
  onClose,
  onSaved,
}: Readonly<{
  activityRef: string;
  activityTitle: string;
  timeZone: string;
  onClose: () => void;
  onSaved?: () => void;
}>) {
  const [structure, setStructure] = useState<PlannedSessionStructure | null>(
    null,
  );
  const [mainEnabled, setMainEnabled] = useState(false);
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [pending, setPending] = useState<EditorPending>({});
  // The parent of an edited child slice is a UI identity, not something
  // recalculated on every keystroke from an incomplete clock value.
  const [assignments, setAssignments] = useState<Record<string, number[]>>({});
  const [issues, setIssues] = useState<EditorIssues>({});
  const [sessionMenu, setSessionMenu] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const operation = useRef<string | null>(null);
  const closeButton = useRef<HTMLButtonElement>(null);

  async function reload(publish = true) {
    const base =
      '/api/v1/temporal/activities/' + encodeURIComponent(activityRef);
    const [structureValue, attemptsValue] = await Promise.all([
      readJson(base + '/children'),
      readJson(base + '/sessions/editor'),
    ]);
    const configured = parsePlannedSessions(structureValue, activityRef);
    const raw = structureValue as { session_capture_mode?: string };
    const enabled =
      raw.session_capture_mode === 'live' ||
      raw.session_capture_mode === 'record_and_live';
    const recorded = parseAttempts(attemptsValue);
    if (publish) {
      setStructure(configured);
      setMainEnabled(enabled);
      setAttempts(recorded);
    }
    return { configured, enabled, recorded };
  }

  useEffect(() => {
    closeButton.current?.focus();
    let active = true;
    const base =
      '/api/v1/temporal/activities/' + encodeURIComponent(activityRef);
    void Promise.all([
      readJson(base + '/children'),
      readJson(base + '/sessions/editor'),
    ])
      .then(([value, attemptsValue]) => {
        if (!active) return;
        const configured = parsePlannedSessions(value, activityRef);
        const raw = value as { session_capture_mode?: string };
        const enabled =
          raw.session_capture_mode === 'live' ||
          raw.session_capture_mode === 'record_and_live';
        const recorded = parseAttempts(attemptsValue);
        setStructure(configured);
        setMainEnabled(enabled);
        setAttempts(recorded);
        const initial: EditorPending = {};
        if (
          enabled &&
          !recorded.some((item) => item.planned_schedule_ref === null)
        )
          initial.main = draftFrom(null, timeZone);
        if (!enabled) {
          for (const planned of configured.rows) {
            if (
              !recorded.some(
                (item) => item.planned_schedule_ref === planned.scheduleRef,
              )
            )
              initial[planned.scheduleRef] = draftFrom(null, timeZone);
          }
        }
        setPending(initial);
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
  }, [activityRef, timeZone]);

  const forConfigured = (plannedRef: string | null, name: string): Row[] => {
    const found = attempts.filter(
      (attempt) => attempt.planned_schedule_ref === plannedRef,
    );
    return found.length
      ? found.map((attempt) => ({
          key: attempt.session_ref,
          plannedRef,
          name,
          attempt,
        }))
      : [{ key: plannedRef ?? 'main', plannedRef, name, attempt: null }];
  };
  const mainRows =
    mainEnabled ||
    attempts.some((attempt) => attempt.planned_schedule_ref === null)
      ? forConfigured(null, 'Sessione attività')
      : [];
  const mainRow = mainRows[0] ?? null;
  const children: Row[] =
    structure?.rows.flatMap((planned) =>
      forConfigured(planned.scheduleRef, planned.name),
    ) ?? [];
  const allRows = [...mainRows, ...children];
  const mainRecorded = mainRows.find((row) => row.attempt?.ended_at) ?? null;
  const mainDraft = mainRow
    ? (pending[mainRow.key] ??
      (mainRecorded?.attempt?.ended_at
        ? draftFrom(mainRecorded.attempt, timeZone)
        : null))
    : null;
  // Preserve the index of every parent row even while its date/time is
  // temporarily invalid. safeRanges() intentionally rejects incomplete
  // drafts, but must never be used to decide which editor stays mounted.
  const invalidParent: ResolvedInterval = { start: Number.NaN, end: Number.NaN };
  const parentRanges: ResolvedInterval[] =
    mainDraft?.intervals.map((interval) => {
      try {
        return resolveIntervals({ intervals: [interval] }, timeZone)[0] ?? invalidParent;
      } catch {
        return invalidParent;
      }
    }) ?? [];
  const validParent = (index: number): boolean => {
    const range = parentRanges[index];
    return Boolean(range && Number.isFinite(range.start) &&
      Number.isFinite(range.end) && range.end > range.start);
  };
  const mainCanAcceptChildren = !mainEnabled || parentRanges.some((_, index) => validParent(index));
  const hasEdits = Object.keys(pending).length > 0;

  function changeDraft(row: Row, updated: Draft) {
    if (saving) return;
    if (JSON.stringify(pending[row.key]) === JSON.stringify(updated)) return;
    // Do not snap edited start/end values to a parent's boundary here.
    // TimeControl commits hours/minutes separately; changing a parent or
    // child clock may briefly invert or overlap ranges. Both inputs must
    // remain writable until the user finishes, then Save validates all.
    setPending((current) => ({ ...current, [row.key]: updated }));
    setIssues((current) => {
      const next = { ...current };
      delete next[row.key];
      return next;
    });
    setError('');
    operation.current = null;
  }

  function inferParent(interval: ActiveInterval): number {
    if (!parentRanges.length) return 0;
    try {
      const resolved = resolveIntervals({ intervals: [interval] }, timeZone)[0];
      if (resolved) {
        const index = parentRanges.findIndex(
          (parent, position) =>
            validParent(position) &&
            resolved.start >= parent.start && resolved.start < parent.end,
        );
        if (index >= 0) return index;
      }
    } catch {
      // Use the previous UI assignment while the clock is incomplete.
    }
    return 0;
  }

  function ownersFor(row: Row, draft: Draft): number[] {
    return assignments[row.key] ??
      draft.intervals.map((interval) => inferParent(interval));
  }

  function bindChildOwners(row: Row, draft: Draft) {
    if (!mainEnabled || row.plannedRef === null) return;
    if (!assignments[row.key]) {
      setAssignments((current) => ({
        ...current,
        [row.key]: draft.intervals.map((interval) => inferParent(interval)),
      }));
    }
  }

  function beginCorrection(row: Row) {
    if (!row.attempt?.ended_at) return;
    const existing = draftFrom(row.attempt, timeZone);
    if (row.plannedRef === null && mainEnabled) {
      // The main's boundaries can become temporarily invalid during typing.
      // Pin every already visible child before its parent values move.
      setAssignments((current) => {
        const next = { ...current };
        for (const child of children) {
          if (next[child.key]) continue;
          const childExisting = childDraft(child);
          if (!childExisting) continue;
          next[child.key] = childExisting.intervals.map((interval) => inferParent(interval));
        }
        return next;
      });
    } else {
      bindChildOwners(row, existing);
    }
    changeDraft(row, existing);
    setSessionMenu(null);
  }

  function cancelCorrection(row: Row) {
    if (!row.attempt) return;
    if (row.plannedRef === null && mainEnabled && row.attempt.ended_at) {
      // Removing a main slice remaps child UI owners. Undoing that
      // correction must also restore the original parent mapping.
      const original = resolveIntervals(draftFrom(row.attempt, timeZone), timeZone);
      setAssignments((current) => {
        const next = { ...current };
        for (const child of children) {
          const draft = childDraft(child);
          if (!draft) continue;
          next[child.key] = draft.intervals.map((interval, intervalIndex) => {
            try {
              const range = resolveIntervals({ intervals: [interval] }, timeZone)[0];
              if (range) {
                const index = original.findIndex(
                  (parent) => range.start >= parent.start && range.start < parent.end,
                );
                if (index >= 0) return index;
              }
            } catch {
              // Still editable on its previous parent if locally incomplete.
            }
            return current[child.key]?.[intervalIndex] ?? 0;
          });
        }
        delete next[row.key];
        return next;
      });
    } else {
      setAssignments((current) => {
        const copy = { ...current };
        delete copy[row.key];
        return copy;
      });
    }
    setPending((current) => {
      const copy = { ...current };
      delete copy[row.key];
      return copy;
    });
    setIssues((current) => {
      const copy = { ...current };
      delete copy[row.key];
      return copy;
    });
    operation.current = null;
  }

  function intervalWithinParent(parentIndex: number): ActiveInterval | null {
    const range = parentRanges[parentIndex];
    if (!range || !validParent(parentIndex)) return null;
    const start = new Date(range.start).toISOString();
    const end = new Date(range.end).toISOString();
    return {
      start: local(start, timeZone),
      end: local(end, timeZone),
      startChoice: choiceFor(start, timeZone),
      endChoice: choiceFor(end, timeZone),
    };
  }

  function insertChildInterval(
    row: Row,
    existing: Draft | null,
    parentIndex: number,
    added: ActiveInterval,
  ) {
    const intervals = [...(existing?.intervals ?? [])];
    const owners = existing ? [...ownersFor(row, existing)] : [];
    // Keep chronological/parent order without sorting controlled fields
    // while the user edits an individual hour or minute.
    const firstLater = owners.findIndex((owner) => owner > parentIndex);
    const at = firstLater < 0 ? intervals.length : firstLater;
    intervals.splice(at, 0, added);
    owners.splice(at, 0, parentIndex);
    setAssignments((current) => ({ ...current, [row.key]: owners }));
    changeDraft(row, { intervals });
  }

  function assignChild(row: Row, parentIndex: number) {
    const added = intervalWithinParent(parentIndex);
    if (!mainCanAcceptChildren || !added) return;
    const existing = pending[row.key] ??
      (row.attempt?.ended_at ? draftFrom(row.attempt, timeZone) : null);
    if ((existing?.intervals.length ?? 0) >= 100) {
      setError('Sono ammessi al massimo 100 intervalli per Sessione.');
      return;
    }
    insertChildInterval(row, existing, parentIndex, added);
    setSessionMenu(null);
  }

  function removeChildFromParent(row: Row, parentIndex: number) {
    const existing = pending[row.key];
    if (!existing || row.attempt) return;
    const owners = ownersFor(row, existing);
    const intervals = existing.intervals.filter((_, index) => owners[index] !== parentIndex);
    if (!intervals.length) {
      unassignChild(row);
      return;
    }
    setAssignments((current) => ({
      ...current,
      [row.key]: owners.filter((owner) => owner !== parentIndex),
    }));
    changeDraft(row, { intervals });
  }

  function unassignChild(row: Row) {
    if (row.attempt) return;
    setPending((current) => {
      const next = { ...current };
      delete next[row.key];
      return next;
    });
    setAssignments((current) => {
      const next = { ...current };
      delete next[row.key];
      return next;
    });
    setIssues((current) => {
      const next = { ...current };
      delete next[row.key];
      return next;
    });
    setError('');
    operation.current = null;
  }

  function updateInterval(row: Row, index: number, updated: ActiveInterval) {
    const existing = pending[row.key];
    if (!existing) return;
    changeDraft(row, {
      intervals: existing.intervals.map((item, position) =>
        position === index ? updated : item,
      ),
    });
  }

  function addInterval(row: Row, parentIndex?: number) {
    const existing = pending[row.key];
    if (!existing || existing.intervals.length >= 100) return;
    try {
      if (parentIndex === undefined || row.plannedRef === null || !mainEnabled) {
        const candidate = nextInterval(existing, timeZone);
        changeDraft(row, { intervals: [...existing.intervals, candidate] });
        return;
      }
      const parent = parentRanges[parentIndex];
      if (!parent || !validParent(parentIndex)) return;
      const owners = ownersFor(row, existing);
      const used = existing.intervals.flatMap((interval, index) => {
        if (owners[index] !== parentIndex) return [];
        try {
          const resolved = resolveIntervals({ intervals: [interval] }, timeZone)[0];
          return resolved && resolved.end > resolved.start ? [resolved] : [];
        } catch {
          return [];
        }
      });
      const latestEnd = used.length
        ? Math.max(...used.map((interval) => interval.end))
        : parent.start;
      const proposed = used.length ? latestEnd + 60_000 : latestEnd;
      // This is only a draft. If no room remains, the provisional row may
      // overlap until the user adjusts its times before Save.
      const start = proposed < parent.end
        ? proposed
        : Math.max(parent.start, parent.end - 30 * 60_000);
      const end = proposed < parent.end
        ? Math.min(parent.end, start + 30 * 60_000)
        : parent.end;
      const startIso = new Date(start).toISOString();
      const endIso = new Date(end).toISOString();
      insertChildInterval(row, existing, parentIndex, {
        start: local(startIso, timeZone),
        end: local(endIso, timeZone),
        startChoice: choiceFor(startIso, timeZone),
        endChoice: choiceFor(endIso, timeZone),
      });
    } catch (reason) {
      setError(reason instanceof Error
        ? reason.message
        : 'Completa gli intervalli prima di aggiungerne un altro.');
    }
  }

  function removeInterval(row: Row, index: number) {
    const existing = pending[row.key];
    if (!existing || existing.intervals.length <= 1) return;
    if (mainEnabled && row.plannedRef === null) {
      // Removing a main slice cannot silently detach its children.
      // Reattach their UI rows to the nearest remaining parent; Save
      // will reject any actual out-of-bounds values.
      setAssignments((current) => {
        const next = { ...current };
        for (const child of children) {
          const draft = childDraft(child);
          if (!draft) continue;
          const original = current[child.key] ??
            draft.intervals.map((item) => inferParent(item));
          next[child.key] = original.map((owner) =>
            owner > index ? owner - 1 :
            owner === index ? Math.min(index, existing.intervals.length - 2) : owner,
          );
        }
        return next;
      });
    } else if (mainEnabled && row.plannedRef !== null) {
      const owners = ownersFor(row, existing);
      setAssignments((current) => ({
        ...current,
        [row.key]: owners.filter((_, position) => position !== index),
      }));
    }
    changeDraft(row, {
      intervals: existing.intervals.filter((_, position) => index !== position),
    });
  }

  function fitChildToParent(row: Row, index: number, parentIndex: number) {
    const interval = pending[row.key]?.intervals[index];
    const parent = parentRanges[parentIndex];
    if (!interval || !parent || !validParent(parentIndex)) return;
    try {
      const resolved = resolveIntervals({ intervals: [interval] }, timeZone)[0];
      if (!resolved) return;
      const start = Math.max(parent.start, Math.min(resolved.start, parent.end));
      const end = Math.max(parent.start, Math.min(resolved.end, parent.end));
      // A range completely outside the parent is restored to the parent's
      // bounds rather than replaced by an invalid zero-duration interval.
      const safeStart = end > start ? start : parent.start;
      const safeEnd = end > start ? end : parent.end;
      const startInstant = new Date(safeStart).toISOString();
      const endInstant = new Date(safeEnd).toISOString();
      updateInterval(row, index, {
        start: local(startInstant, timeZone),
        end: local(endInstant, timeZone),
        startChoice: choiceFor(startInstant, timeZone),
        endChoice: choiceFor(endInstant, timeZone),
      });
    } catch {
      setError('Completa prima la data e l’orario dell’intervallo.');
    }
  }

  function renderRange(
    row: Row,
    index: number,
    interval: ActiveInterval,
    readonly: boolean,
    parentIndex?: number,
  ) {
    const issue = issues[row.key] ?? null;
    let outsideParent = false;
    if (
      !readonly && row.plannedRef !== null && mainEnabled &&
      parentIndex !== undefined && validParent(parentIndex)
    ) {
      try {
        const actual = resolveIntervals({ intervals: [interval] }, timeZone)[0];
        const parent = parentRanges[parentIndex]!;
        outsideParent = Boolean(actual &&
          (actual.start < parent.start || actual.end > parent.end));
      } catch {
        // An incomplete local-time value is validated when saved.
      }
    }
    return (
      <div
        key={index}
        className="timeline-session-editor__interval-block"
        data-invalid={
          issue?.field === 'interval-' + index || outsideParent || undefined
        }
      >
        {readonly ? (
          <div className="timeline-session-editor__recorded-interval">
            <strong>Intervallo {index + 1}</strong>
            <span>
              {interval.start.replace('T', ' ').slice(0, 16)}
              {' → '}
              {interval.end.replace('T', ' ').slice(0, 16)}
            </span>
            <button type="button" onClick={() => beginCorrection(row)}>
              Correggi
            </button>
          </div>
        ) : (
          <IntervalFields
            interval={interval}
            index={index}
            zone={timeZone}
            fieldPath={'session-recording.' + row.key}
            issue={issue?.field === 'interval-' + index ? issue : null}
            onChange={(updated) => updateInterval(row, index, updated)}
            onRemove={
              pending[row.key]?.intervals.length &&
              pending[row.key]!.intervals.length > 1
                ? () => removeInterval(row, index)
                : undefined
            }
          />
        )}
        {outsideParent ? (
          <div className="timeline-session-editor__clamp-note" role="status">
            <span>L’intervallo supera il tratto attivo della principale.</span>
            <button type="button" onClick={() => fitChildToParent(row, index, parentIndex!)}>
              Adatta ai limiti
            </button>
          </div>
        ) : null}
        {issue?.field === 'interval-' + index ? (
          <p className="timeline-session-editor__error" role="alert">
            {issue.message}
          </p>
        ) : null}
      </div>
    );
  }

  function childDraft(row: Row): Draft | null {
    return (
      pending[row.key] ??
      (row.attempt?.ended_at ? draftFrom(row.attempt, timeZone) : null)
    );
  }

  function parentOfChildInterval(
    row: Row, interval: ActiveInterval, intervalIndex: number,
  ): number {
    const fixed = assignments[row.key]?.[intervalIndex];
    if (fixed !== undefined) {
      return Math.min(fixed, Math.max(0, parentRanges.length - 1));
    }
    return inferParent(interval);
  }

  function childIndicesForParent(row: Row, parentIndex: number): number[] {
    const draft = childDraft(row);
    if (!draft) {
      if (!row.attempt || row.attempt.ended_at) return [];
      const started = Date.parse(row.attempt.started_at);
      const within = parentRanges.findIndex(
        (parent) => started >= parent.start && started < parent.end,
      );
      return within === parentIndex ? [0] : [];
    }
    return draft.intervals.flatMap((interval, index) =>
      parentOfChildInterval(row, interval, index) === parentIndex ? [index] : [],
    );
  }

  function renderChild(row: Row, parentIndex?: number) {
    const draft = pending[row.key];
    const readOnly = !draft && Boolean(row.attempt?.ended_at);
    const visible = childDraft(row);
    const indices =
      visible?.intervals.flatMap((interval, index) =>
        parentIndex === undefined ||
        parentOfChildInterval(row, interval, index) === parentIndex
          ? [index]
          : [],
      ) ?? [];
    const localDraft = visible
      ? { intervals: indices.map((index) => visible.intervals[index]!) }
      : null;
    return (
      <article
        key={row.key}
        className="timeline-session-editor__row is-child"
        data-recorded={readOnly || undefined}
      >
        <div className="timeline-session-editor__row-header">
          <div>
            <h3>{row.name}</h3>
          </div>
          {row.attempt?.ended_at && draft ? (
            <button type="button" onClick={() => cancelCorrection(row)}>
              Annulla
            </button>
          ) : !row.attempt &&
            draft &&
            mainEnabled &&
            parentIndex !== undefined ? (
            <button
              type="button"
              onClick={() => removeChildFromParent(row, parentIndex)}
              aria-label={
                'Rimuovi ' + row.name + ' da intervallo ' + (parentIndex + 1)
              }
            >
              ×
            </button>
          ) : null}
          {row.attempt && !row.attempt.ended_at ? (
            <small>In corso · usa i controlli live</small>
          ) : null}
        </div>
        {localDraft && localDraft.intervals.length > 0 ? (
          <div className="timeline-session-editor__intervals">
            {indices.map((index) =>
              renderRange(
                row,
                index,
                visible!.intervals[index]!,
                readOnly,
                parentIndex,
              ),
            )}
          </div>
        ) : null}
        {draft ? (
          <button
            type="button"
            className="timeline-session-editor__add-interval"
            disabled={draft.intervals.length >= 100}
            onClick={() => addInterval(row, parentIndex)}
          >
            ＋ Aggiungi intervallo
          </button>
        ) : null}
        {localDraft && localDraft.intervals.length > 0 ? (
          <SessionSegmentPreview draft={localDraft} zone={timeZone} />
        ) : null}
      </article>
    );
  }

  function renderChildSlot(index: number) {
    const allocated = children.filter(
      (row) => childIndicesForParent(row, index).length > 0,
    );
    const available = children.filter(
      (row) =>
        (!row.attempt || row.attempt.ended_at) &&
        childIndicesForParent(row, index).length === 0,
    );
    return (
      <div className="timeline-session-editor__child-slot">
        {allocated.map((row) => renderChild(row, index))}
        {available.length > 0 ? (
          <div className="timeline-session-editor__add-session">
            <button
              type="button"
              aria-expanded={sessionMenu === index}
              disabled={!mainCanAcceptChildren || !validParent(index)}
              onClick={() =>
                setSessionMenu((current) => (current === index ? null : index))
              }
            >
              ＋ Registra sessione
            </button>
            {sessionMenu === index ? (
              <div
                className="timeline-session-editor__session-options"
                role="group"
                aria-label={'Scegli Sessione per intervallo ' + (index + 1)}
              >
                {available.map((row) => (
                  <button
                    key={row.key}
                    type="button"
                    onClick={() => assignChild(row, index)}
                  >
                    {row.name}
                    {pending[row.key] || row.attempt ? ' · Riprendi' : ''}
                  </button>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}
      </div>
    );
  }

  function renderMain() {
    if (!mainRow) return null;
    // This callback runs on click; renderMain only creates the button.
    // eslint-disable-next-line react-hooks/refs
    const cancelMain = () => cancelCorrection(mainRow);
    const editing = pending[mainRow.key];
    const display =
      editing ??
      (mainRecorded?.attempt?.ended_at
        ? draftFrom(mainRecorded.attempt, timeZone)
        : null);
    const readonly = !editing && Boolean(mainRecorded?.attempt?.ended_at);
    return (
      <section className="timeline-session-editor__group has-main">
        <div className="timeline-session-editor__row-header">
          <h3>Sessione attività</h3>
          {editing && mainRow.attempt?.ended_at ? (
            <button type="button" onClick={cancelMain}>
              Annulla
            </button>
          ) : null}
          {mainRow.attempt && !mainRow.attempt.ended_at ? (
            <small>In corso · usa i controlli live</small>
          ) : null}
        </div>
        {display?.intervals.map((interval, index) => (
          <section
            className="timeline-session-editor__parent-interval"
            key={index}
          >
            {renderRange(mainRow, index, interval, readonly)}
            {renderChildSlot(index)}
          </section>
        ))}
        {editing ? (
          <button
            type="button"
            className="timeline-session-editor__add-interval"
            disabled={editing.intervals.length >= 100}
            onClick={() => addInterval(mainRow)}
          >
            ＋ Aggiungi intervallo
          </button>
        ) : null}
        {display ? (
          <SessionSegmentPreview draft={display} zone={timeZone} />
        ) : null}
        {!display && !mainRow.attempt ? (
          <button
            type="button"
            onClick={() => changeDraft(mainRow, draftFrom(null, timeZone))}
          >
            Registra
          </button>
        ) : null}
      </section>
    );
  }

  async function commitAll() {
    if (saving || !hasEdits) return;
    const changes = allRows
      .filter((row) => Boolean(pending[row.key]))
      .map((row) => ({ row, draft: pending[row.key]! }));
    const currentMainRanges =
      mainRow && pending[mainRow.key]
        ? safeRanges(pending[mainRow.key], timeZone)
        : [];
    const main = mainRow
      ? pending[mainRow.key]
        ? currentMainRanges.length
          ? attemptFromRanges(currentMainRanges)
          : null
        : (mainRecorded?.attempt ?? null)
      : null;
    const factualChildren: Array<
      Pick<Attempt, 'started_at' | 'ended_at' | 'pause_ranges'>
    > = [];
    for (const row of children) {
      if (pending[row.key]) {
        const ranges = safeRanges(pending[row.key], timeZone);
        if (ranges.length) factualChildren.push(attemptFromRanges(ranges));
      } else if (row.attempt?.ended_at) {
        factualChildren.push(row.attempt);
      }
    }
    const errors: EditorIssues = {};
    for (const { row, draft } of changes) {
      const issue = validateDraft(
        row,
        draft,
        timeZone,
        mainEnabled ? main : null,
        factualChildren,
      );
      if (issue) errors[row.key] = issue;
    }
    if (Object.keys(errors).length > 0) {
      setIssues(errors);
      setError('Controlla gli intervalli evidenziati in rosso.');
      return;
    }
    setSaving(true);
    setError('');
    operation.current ??= crypto.randomUUID();
    try {
      const receipts = await saveEditorGroup(
        activityRef,
        changes,
        timeZone,
        operation.current,
      );
      const { configured, enabled, recorded } = await reload(false);
      if (
        receipts.some(
          (receipt) =>
            !recorded.some(
              (attempt) =>
                attempt.session_ref === receipt.session_ref &&
                attempt.timing_material_state_ref ===
                  receipt.timing_material_state_ref,
            ),
        )
      ) {
        throw new Error(
          'Registrazione non confermata dalla rilettura: aggiorna il pannello.',
        );
      }
      setStructure(configured);
      setMainEnabled(enabled);
      setAttempts(recorded);
      setPending({});
      setIssues({});
      setAssignments({});
      setSessionMenu(null);
      operation.current = null;
      window.dispatchEvent(
        new CustomEvent('dante:session-changed', { detail: activityRef }),
      );
      if (onSaved) onSaved();
      else onClose();
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Registrazioni non salvate.',
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
        if (event.key !== 'Tab') return;
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
      }}
    >
      <section
        className="timeline-session-editor"
        role="dialog"
        aria-modal="true"
        aria-labelledby="session-editor-title"
      >
        <header className="timeline-session-editor__header">
          <h2 id="session-editor-title">Registrazioni delle Sessioni</h2>
          <button
            type="button"
            ref={closeButton}
            aria-label="Chiudi registrazioni"
            onClick={onClose}
            disabled={saving}
          >
            ×
          </button>
        </header>
        <div className="timeline-session-editor__content">
          <h3 className="timeline-session-editor__activity-name">
            {activityTitle}
          </h3>
          <div
            className="timeline-session-editor__scroll-area"
            role="region"
            aria-label="Intervalli e Sessioni"
            tabIndex={0}
          >
            {loading ? <p>Caricamento Sessioni…</p> : null}
            {!loading && allRows.length === 0 ? (
              <p>Nessuna Sessione configurata.</p>
            ) : null}
            {!loading && mainRow ? renderMain() : null}
            {!loading && !mainRow ? (
              <div className="timeline-session-editor__independent">
                {children.map((row) => renderChild(row))}
              </div>
            ) : null}
          </div>
        </div>
        {hasEdits || error ? (
          <footer className="timeline-session-editor__footer">
            {error ? (
              <p className="timeline-session-editor__error" role="alert">
                {error}
              </p>
            ) : (
              <span />
            )}
            {hasEdits ? (
              <div className="timeline-session-editor__save">
                <button
                  type="button"
                  disabled={saving || loading}
                  onClick={() => void commitAll()}
                >
                  {saving ? 'Salvataggio…' : 'Salva registrazioni'}
                </button>
              </div>
            ) : null}
          </footer>
        ) : null}
      </section>
    </div>,
    document.body,
  );
}
