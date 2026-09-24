import { useCallback, useEffect, useState } from 'react';

import {
  createRemoteTemporalSessionDataSource,
  type SessionSubjectKind,
  type TemporalSessionView,
} from './remote-session-data-source';

const source = createRemoteTemporalSessionDataSource();

function operationId(): string {
  return crypto.randomUUID();
}

export function SessionSubjectControls({
  kind,
  subjectRef,
  label,
}: Readonly<{
  kind: SessionSubjectKind;
  subjectRef: string;
  label: string;
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

  const start = () => {
    setPending(true);
    void source
      .start(kind, subjectRef, operationId())
      .then(() => reload())
      .then(() => setMessage(`Sessione avviata · ${label}`))
      .catch(() => setMessage('Avvio sessione rifiutato.'))
      .finally(() => setPending(false));
  };

  const end = () => {
    if (openSession === null) {
      return;
    }
    setPending(true);
    void source
      .end(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
      .then(() => setMessage(`Sessione chiusa · ${label}`))
      .catch(() => setMessage('Chiusura sessione rifiutata.'))
      .finally(() => setPending(false));
  };

  const pause = () => {
    if (openSession === null) {
      return;
    }
    setPending(true);
    void source
      .pause(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
      .then(() => setMessage('Sessione in pausa · ' + label))
      .catch(() => setMessage('Pausa sessione rifiutata.'))
      .finally(() => setPending(false));
  };

  const resume = () => {
    if (openSession === null) {
      return;
    }
    setPending(true);
    void source
      .resume(openSession.sessionRef, openSession.timingMaterialStateRef, operationId())
      .then(() => reload())
      .then(() => setMessage('Sessione ripresa · ' + label))
      .catch(() => setMessage('Ripresa sessione rifiutata.'))
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-session-controls" data-timeline-session-subject={subjectRef}>
      {openSession === null ? (
        <button type="button" disabled={pending} onClick={start}>
          Avvia
        </button>
      ) : (
        <>
          {openSession.paused ? (
            <button type="button" disabled={pending} onClick={resume}>
              Riprendi
            </button>
          ) : (
            <>
              <button type="button" disabled={pending} onClick={pause}>
                Pausa
              </button>
              <button type="button" disabled={pending} onClick={end}>
                Termina
              </button>
            </>
          )}
        </>
      )}
      {message === null ? null : <span role="status">{message}</span>}
    </div>
  );
}
