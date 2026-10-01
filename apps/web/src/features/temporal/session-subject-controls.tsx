import { useCallback, useEffect, useState } from 'react';

import './session-subject-controls.css';

import {
  createRemoteTemporalSessionDataSource,
  type SessionSubjectKind,
  type TemporalSessionView,
} from './remote-session-data-source';

const source = createRemoteTemporalSessionDataSource();

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
}: Readonly<{
  kind: SessionSubjectKind;
  subjectRef: string;
  label: string;
  variant?: 'detail' | 'card';
  interactive?: boolean;
}>) {
  const [sessions, setSessions] = useState<readonly TemporalSessionView[]>([]);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const listed = await source.list(kind, subjectRef);
    setSessions(listed);
  }, [kind, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void source
      .list(kind, subjectRef)
      .then((listed) => {
        if (!cancelled) {
          setSessions(listed);
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
  }, [kind, subjectRef]);

  const openSession = sessions.find((session) => session.open) ?? null;
  const durationSession = openSession ?? sessions[sessions.length - 1] ?? null;

  const recoverAfterRejection = (fallback: string, error: unknown) =>
    reload()
      .catch(() => undefined)
      .then(() => setMessage(rejectionMessage(fallback, error)));

  const start = () => {
    if (!interactive) return;
    setPending(true);
    void source
      .start(kind, subjectRef, operationId())
      .then(() => reload())
      .then(() => setMessage(`Sessione avviata · ${label}`))
      .catch((error: unknown) => recoverAfterRejection('Avvio sessione rifiutato.', error))
      .finally(() => setPending(false));
  };

  const end = () => {
    if (!interactive || openSession === null) return;
    setPending(true);
    void source
      .end(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
      .then(() => setMessage(`Sessione chiusa · ${label}`))
      .catch((error: unknown) =>
        recoverAfterRejection('Chiusura sessione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  const pause = () => {
    if (!interactive || openSession === null) return;
    setPending(true);
    void source
      .pause(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
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
      .resume(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
      .then(() => setMessage('Sessione ripresa · ' + label))
      .catch((error: unknown) =>
        recoverAfterRejection('Ripresa sessione rifiutata.', error),
      )
      .finally(() => setPending(false));
  };

  const card = variant === 'card';

  return (
    <div
      className={`timeline-session-controls${card ? ' is-card' : ''}`}
      data-timeline-session-subject={subjectRef}
    >
      <div className="timeline-session-controls__runtime-actions" aria-label={`Sessione · ${label}`}>
        {openSession === null ? (
          <RuntimeButton
            label="Avvia"
            symbol="▶"
            pending={pending}
            interactive={interactive}
            onClick={start}
          />
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
      </div>

      {card || openSession === null ? null : (
        <span className="timeline-session-duration" aria-label="Durata sessione">
          Attiva {formatDuration(openSession.activeSeconds)} · Pausa{' '}
          {formatDuration(openSession.pausedSeconds)} · Totale{' '}
          {formatDuration(openSession.elapsedSeconds)}
        </span>
      )}
      {message === null ? null : (
        <span role="status" className={card ? 'timeline-session-controls__card-status' : undefined}>
          {message}
        </span>
      )}
      {card
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
