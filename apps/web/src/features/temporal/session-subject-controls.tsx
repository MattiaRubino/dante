import { useCallback, useEffect, useState } from 'react';

import './session-subject-controls.css';

import {
  createRemoteTemporalSessionDataSource,
  type SessionSubjectKind,
  type TemporalSessionView,
} from './remote-session-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function formatDuration(seconds: number): string {
  const total = Math.max(0, Math.floor(seconds));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const remainingSeconds = total % 60;
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
  }
  return `${minutes}:${String(remainingSeconds).padStart(2, '0')}`;
}

function formatInspectorDuration(seconds: number): string {
  const total = Math.max(0, Math.floor(seconds));
  return [Math.floor(total / 3600), Math.floor((total % 3600) / 60), total % 60]
    .map((part) => String(part).padStart(2, '0'))
    .join(':');
}

function sessionClock(
  instant: string,
  locale: string,
  timeZone?: string,
): string {
  return new Intl.DateTimeFormat(locale, {
    hour: '2-digit',
    minute: '2-digit',
    ...(timeZone ? { timeZone } : {}),
  }).format(new Date(instant));
}

function rejectionMessage(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return `${fallback} ${error.message}`;
  }
  return fallback;
}

function RuntimeButton({
  label,
  symbol,
  pending,
  interactive,
  onClick,
}: Readonly<{
  label: string;
  symbol: string;
  pending: boolean;
  interactive: boolean;
  onClick: () => void;
}>) {
  return (
    <button
      className="timeline-session-controls__runtime-button"
      type="button"
      aria-label={label}
      title={label}
      disabled={pending || !interactive}
      tabIndex={interactive ? undefined : -1}
      onClick={onClick}
    >
      <span aria-hidden="true">{symbol}</span>
    </button>
  );
}

export function SessionSubjectControls({
  kind,
  subjectRef,
  label,
  variant = 'detail',
  interactive = true,
  allowLive = true,
  allowManual = false,
  plannedScheduleRef = null,
  compactRuntime = false,
  visibleSessionRefs,
  onRecorded,
  inspectorSummary = false,
  showUnstartedStatus = false,
  hideRuntimeActions = false,
  locale = 'it-IT',
  timeZone,
}: Readonly<{
  kind: SessionSubjectKind;
  subjectRef: string;
  label: string;
  variant?: 'detail' | 'card';
  interactive?: boolean;
  allowLive?: boolean;
  allowManual?: boolean;
  plannedScheduleRef?: string | null;
  compactRuntime?: boolean;
  visibleSessionRefs?: readonly string[];
  onRecorded?: () => void;
  inspectorSummary?: boolean;
  showUnstartedStatus?: boolean;
  hideRuntimeActions?: boolean;
  locale?: string;
  timeZone?: string;
}>) {
  const [sessions, setSessions] = useState<readonly TemporalSessionView[]>([]);
  const [source] = useState(createRemoteTemporalSessionDataSource);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [manualOpen, setManualOpen] = useState(false);
  const [manualStart, setManualStart] = useState('');
  const [manualEnd, setManualEnd] = useState('');
  const [localSessionRef, setLocalSessionRef] = useState<string | null>(null);
  const [clockMs, setClockMs] = useState(() => Date.now());
  const visibleSessionKey = visibleSessionRefs?.join('|');

  const forThisCard = useCallback(
    (item: TemporalSessionView) =>
      (item.plannedScheduleRef ?? null) === plannedScheduleRef &&
      (visibleSessionKey === undefined ||
        visibleSessionKey.split('|').includes(item.sessionRef) ||
        item.sessionRef === localSessionRef),
    [plannedScheduleRef, visibleSessionKey, localSessionRef],
  );

  const reload = useCallback(async () => {
    const listed = await source.list(kind, subjectRef);
    setSessions(listed.filter(forThisCard));
    setClockMs(Date.now());
  }, [kind, subjectRef, forThisCard, source]);

  useEffect(() => {
    const refresh = (event: Event) => {
      if (event instanceof CustomEvent && event.detail === subjectRef) {
        void reload().catch(() => undefined);
      }
    };
    window.addEventListener('dante:session-changed', refresh);
    return () => window.removeEventListener('dante:session-changed', refresh);
  }, [reload, subjectRef]);

  const changed = () => {
    window.dispatchEvent(
      new CustomEvent('dante:session-changed', { detail: subjectRef }),
    );
    onRecorded?.();
    return reload();
  };

  useEffect(() => {
    let cancelled = false;
    void source
      .list(kind, subjectRef)
      .then((listed) => {
        if (!cancelled) {
          setSessions(listed.filter(forThisCard));
        }
      })
      .catch(() => {
        if (!cancelled) {
          setMessage('Sessione non disponibile.');
        }
      });
    return () => {
      cancelled = true;
    };
  }, [kind, subjectRef, forThisCard, source]);

  const openSession = sessions.find((session) => session.open) ?? null;
  const stopped =
    openSession === null && sessions.some((session) => !session.open);
  const durationSession = openSession ?? sessions[sessions.length - 1] ?? null;

  useEffect(() => {
    if (!inspectorSummary || openSession === null || openSession.paused) return;
    const timer = window.setInterval(() => setClockMs(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [inspectorSummary, openSession]);

  const evaluatedMs = openSession ? Date.parse(openSession.evaluatedAt) : 0;
  const activeSeconds = openSession
    ? openSession.activeSeconds +
      (!openSession.paused && Number.isFinite(evaluatedMs)
        ? Math.max(0, (clockMs - evaluatedMs) / 1000)
        : 0)
    : 0;

  const recoverAfterRejection = (fallback: string, error: unknown) =>
    reload()
      .catch(() => undefined)
      .then(() => setMessage(rejectionMessage(fallback, error)));

  const start = () => {
    if (!interactive || stopped) return;
    setPending(true);
    const command =
      plannedScheduleRef === null
        ? source.start(kind, subjectRef, operationId())
        : source.startPlanned(subjectRef, plannedScheduleRef, operationId());
    void command
      .then((saved) => {
        setLocalSessionRef(saved.sessionRef);
        setSessions((current) => [...current, saved]);
        window.dispatchEvent(
          new CustomEvent('dante:session-changed', { detail: subjectRef }),
        );
      })
      .then(() => setMessage(`Sessione avviata · ${label}`))
      .catch((error: unknown) =>
        recoverAfterRejection('Avvio sessione rifiutato.', error),
      )
      .finally(() => setPending(false));
  };

  const end = () => {
    if (!interactive || openSession === null) return;
    setPending(true);
    void source
      .end(
        openSession.sessionRef,
        openSession.timingMaterialStateRef,
        operationId(),
      )
      .then(changed)
      .then(() => setMessage(null))
      .catch((error: unknown) =>
        recoverAfterRejection('Chiusura sessione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  const pause = () => {
    if (!interactive || openSession === null) return;
    setPending(true);
    void source
      .pause(
        openSession.sessionRef,
        openSession.timingMaterialStateRef,
        operationId(),
      )
      .then(changed)
      .then(() => setMessage('Sessione in pausa · ' + label))
      .catch((error: unknown) =>
        recoverAfterRejection('Pausa sessione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  const resume = () => {
    if (!interactive || openSession === null) return;
    setPending(true);
    void source
      .resume(
        openSession.sessionRef,
        openSession.timingMaterialStateRef,
        operationId(),
      )
      .then(changed)
      .then(() => setMessage('Sessione ripresa · ' + label))
      .catch((error: unknown) =>
        recoverAfterRejection('Ripresa sessione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  const card = variant === 'card';

  const recordManual = () => {
    if (!interactive || kind !== 'activity') return;
    const started = new Date(manualStart);
    const ended = new Date(manualEnd);
    if (
      !Number.isFinite(started.getTime()) ||
      !Number.isFinite(ended.getTime()) ||
      started >= ended ||
      ended > new Date()
    ) {
      setMessage('Inserisci un inizio e una fine già trascorsi, in ordine.');
      return;
    }
    setPending(true);
    void source
      .recordManual(
        subjectRef,
        operationId(),
        started.toISOString(),
        ended.toISOString(),
      )
      .then(changed)
      .then(() => {
        setManualOpen(false);
        setManualStart('');
        setManualEnd('');
        setMessage(`Sessione registrata · ${label}`);
      })
      .catch((error: unknown) =>
        recoverAfterRejection('Registrazione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  if (card && stopped) return null;
  if (!allowLive && !allowManual && openSession === null) return null;

  return (
    <div
      className={`timeline-session-controls${card ? ' is-card' : ''}${inspectorSummary ? ' is-inspector-summary' : ''}`}
      data-timeline-session-subject={subjectRef}
    >
      <div
        className="timeline-session-controls__runtime-actions"
        aria-label={`Sessione · ${label}`}
      >
        {hideRuntimeActions ? null : allowLive && !stopped ? (
          <>
            <RuntimeButton
              label={
                openSession === null
                  ? 'Avvia'
                  : openSession.paused
                    ? 'Riprendi'
                    : compactRuntime
                      ? 'Pausa'
                      : 'Avvia'
              }
              symbol={
                compactRuntime && openSession !== null && !openSession.paused
                  ? '⏸'
                  : '▶'
              }
              pending={pending}
              interactive={
                interactive &&
                (compactRuntime || openSession === null || openSession.paused)
              }
              onClick={
                openSession === null
                  ? start
                  : openSession.paused
                    ? resume
                    : compactRuntime
                      ? pause
                      : start
              }
            />
            {compactRuntime ? null : (
              <RuntimeButton
                label="Pausa"
                symbol="⏸"
                pending={pending}
                interactive={
                  interactive && openSession !== null && !openSession.paused
                }
                onClick={pause}
              />
            )}
            <RuntimeButton
              label="Termina"
              symbol="■"
              pending={pending}
              interactive={interactive && openSession !== null}
              onClick={end}
            />
          </>
        ) : stopped ? null : openSession === null ? (
          allowLive ? (
            <RuntimeButton
              label="Avvia"
              symbol="▶"
              pending={pending}
              interactive={interactive}
              onClick={start}
            />
          ) : null
        ) : openSession.paused ? (
          <RuntimeButton
            label="Riprendi"
            symbol="▶"
            pending={pending}
            interactive={interactive}
            onClick={resume}
          />
        ) : (
          <>
            <RuntimeButton
              label="Pausa"
              symbol="⏸"
              pending={pending}
              interactive={interactive}
              onClick={pause}
            />
            <RuntimeButton
              label="Termina"
              symbol="■"
              pending={pending}
              interactive={interactive}
              onClick={end}
            />
          </>
        )}
        {!hideRuntimeActions &&
        allowManual &&
        !stopped &&
        kind === 'activity' ? (
          <button
            type="button"
            disabled={pending || !interactive}
            onClick={() => setManualOpen((value) => !value)}
          >
            Registra sessione
          </button>
        ) : null}
      </div>

      {manualOpen && allowManual && kind === 'activity' ? (
        <form
          className="timeline-session-controls__manual"
          aria-label={`Registra sessione · ${label}`}
          onSubmit={(event) => {
            event.preventDefault();
            recordManual();
          }}
        >
          <label>
            Inizio{' '}
            <input
              type="datetime-local"
              required
              value={manualStart}
              disabled={pending || !interactive}
              onChange={(event) => setManualStart(event.target.value)}
            />
          </label>
          <label>
            Fine{' '}
            <input
              type="datetime-local"
              required
              value={manualEnd}
              disabled={pending || !interactive}
              onChange={(event) => setManualEnd(event.target.value)}
            />
          </label>
          <button type="submit" disabled={pending || !interactive}>
            Salva sessione
          </button>
        </form>
      ) : null}

      {inspectorSummary && durationSession ? (
        <span
          className="timeline-session-controls__inspector-summary"
          aria-label="Stato sessione"
        >
          {durationSession.open ? (
            <>
              Avviata alle{' '}
              {sessionClock(durationSession.startedAt, locale, timeZone)}
              {' · '}
              {durationSession.paused ? 'In pausa' : 'In corso'}{' '}
              {formatInspectorDuration(activeSeconds)}
            </>
          ) : durationSession.endedAt ? (
            <>
              {sessionClock(durationSession.startedAt, locale, timeZone)}–
              {sessionClock(durationSession.endedAt, locale, timeZone)}
              {' · '}Totale attivo{' '}
              {formatInspectorDuration(durationSession.activeSeconds)}
            </>
          ) : null}
        </span>
      ) : inspectorSummary && showUnstartedStatus && !durationSession ? (
        <span className="timeline-session-controls__inspector-summary">
          Non avviata
        </span>
      ) : null}
      {card || inspectorSummary || openSession === null ? null : (
        <span
          className="timeline-session-duration"
          aria-label="Durata sessione"
        >
          Attiva {formatDuration(openSession.activeSeconds)} · Pausa{' '}
          {formatDuration(openSession.pausedSeconds)} · Totale{' '}
          {formatDuration(openSession.elapsedSeconds)}
        </span>
      )}
      {!inspectorSummary && stopped && durationSession ? (
        <span className="timeline-session-controls__recorded">
          Registrata · {formatDuration(durationSession.elapsedSeconds)}
        </span>
      ) : null}
      {message === null ? null : (
        <span
          role="status"
          className={
            card ? 'timeline-session-controls__card-status' : undefined
          }
        >
          {message}
        </span>
      )}
      {card || inspectorSummary
        ? null
        : durationSession?.durationEvaluations.map((item) => (
            <span
              className="timeline-session-duration-policy"
              data-session-duration-evaluation={item.evaluation}
              key={item.constraintRef}
            >
              Minimo attivo{' '}
              {formatDuration(item.minimumDurationMicroseconds / 1_000_000)} ·{' '}
              {item.evaluation === 'pending'
                ? 'in corso'
                : item.evaluation === 'satisfied'
                  ? 'raggiunto'
                  : 'non raggiunto'}
            </span>
          ))}
    </div>
  );
}
