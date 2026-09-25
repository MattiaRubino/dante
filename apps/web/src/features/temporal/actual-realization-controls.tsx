import { useCallback, useEffect, useMemo, useState } from 'react';

import './actual-realization-controls.css';

import {
  createRemoteTemporalActualDataSource,
  type ActualSubjectKind,
  type TemporalActualView,
} from './remote-actual-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return `${fallback} ${error.message}`;
  }
  return fallback;
}

export function ActualRealizationControls({
  kind,
  subjectRef,
}: Readonly<{
  kind: ActualSubjectKind;
  subjectRef: string;
}>) {
  const source = useMemo(() => createRemoteTemporalActualDataSource(globalThis.fetch), []);
  const [actual, setActual] = useState<TemporalActualView | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const current = await source.get(kind, subjectRef);
    setActual(current);
    setLoaded(true);
    return current;
  }, [kind, source, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void source
      .get(kind, subjectRef)
      .then((current) => {
        if (!cancelled) {
          setActual(current);
          setLoaded(true);
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setLoaded(true);
          setMessage(rejection('Stato reale non disponibile.', error));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [kind, source, subjectRef]);

  const setRealization = (realizationOccurred: boolean) => {
    setPending(true);
    setMessage(null);
    void source
      .record(kind, subjectRef, {
        operationId: operationId(),
        expectedMaterialStateRef: actual?.materialStateRef ?? null,
        realizationOccurred,
      })
      .then((saved) => {
        setActual(saved);
        setLoaded(true);
        setMessage(
          realizationOccurred
            ? 'Stato reale registrato: avvenuto.'
            : 'Stato reale registrato: non avvenuto.',
        );
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento stato reale rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  const state = !loaded
    ? 'Stato reale: caricamento…'
    : actual === null
      ? 'Stato reale: sconosciuto'
      : actual.realizationOccurred
        ? 'Stato reale: avvenuto'
        : 'Stato reale: non avvenuto';

  const messageNode =
    message === null ? null : message.startsWith('Aggiornamento') ? (
      <span role="alert">{message}</span>
    ) : message.startsWith('Stato reale registrato') ? (
      <span role="status">{message}</span>
    ) : (
      <span>{message}</span>
    );

  return (
    <div
      className="timeline-actual-controls"
      data-timeline-actual-subject={subjectRef}
    >
      <strong>Realtà</strong>
      <p data-timeline-actual-state>{state}</p>
      <div className="timeline-actual-controls__actions">
        <button
          type="button"
          disabled={pending || !loaded || actual?.realizationOccurred === true}
          data-timeline-actual-set="occurred"
          onClick={() => setRealization(true)}
        >
          Segna avvenuto
        </button>
        <button
          type="button"
          disabled={pending || !loaded || actual?.realizationOccurred === false}
          data-timeline-actual-set="not-occurred"
          onClick={() => setRealization(false)}
        >
          Segna non avvenuto
        </button>
      </div>
      <small>
        “Sconosciuto” significa che non è ancora stato registrato un Actual; non equivale a
        “non avvenuto”.
      </small>
      {messageNode}
    </div>
  );
}
