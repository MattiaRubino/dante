import { useCallback, useEffect, useMemo, useState } from 'react';

import './actual-realization-controls.css';

import { ConfirmationControls } from './confirmation-controls';
import { OutcomeControls } from './outcome-controls';
import { ReconciliationControls } from './reconciliation-controls';
import {
  createRemoteTemporalActualDataSource,
  TemporalActualRemoteError,
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
  const source = useMemo(
    () => createRemoteTemporalActualDataSource(globalThis.fetch),
    [],
  );
  const [actual, setActual] = useState<TemporalActualView | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [needsParentAcknowledgement, setNeedsParentAcknowledgement] =
    useState(false);

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

  const setRealization = (
    realizationOccurred: boolean,
    acknowledge = false,
  ) => {
    setPending(true);
    setMessage(null);
    setNeedsParentAcknowledgement(false);
    void source
      .record(kind, subjectRef, {
        operationId: operationId(),
        expectedMaterialStateRef: actual?.materialStateRef ?? null,
        realizationOccurred,
        ...(acknowledge ? { acknowledgeUnresolvedChildren: true } : {}),
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
      .catch((error: unknown) => {
        if (
          error instanceof TemporalActualRemoteError &&
          error.code === 'temporal.actual.parent_ack_required'
        ) {
          setNeedsParentAcknowledgement(true);
          setMessage(
            'Una sotto-attività richiesta non risulta ancora avvenuta. Conferma esplicitamente per registrare comunque la realtà del padre.',
          );
          return;
        }
        return reload()
          .catch(() => undefined)
          .then(() =>
            setMessage(
              rejection('Aggiornamento stato reale rifiutato.', error),
            ),
          );
      })
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
      {needsParentAcknowledgement && kind === 'activity' ? (
        <div
          className="timeline-actual-controls__acknowledgement"
          role="group"
          aria-label="Conferma realtà del padre"
        >
          <button
            type="button"
            disabled={pending}
            onClick={() => setRealization(true, true)}
          >
            Conferma comunque
          </button>
          <button
            type="button"
            disabled={pending}
            onClick={() => {
              setNeedsParentAcknowledgement(false);
              setMessage(null);
            }}
          >
            Annulla
          </button>
        </div>
      ) : null}
      <small>
        “Sconosciuto” significa che non è ancora stato registrato un Actual; non
        equivale a “non avvenuto”.
      </small>
      {messageNode}
      <OutcomeControls kind={kind} subjectRef={subjectRef} />
      <ConfirmationControls kind={kind} subjectRef={subjectRef} />
      <ReconciliationControls kind={kind} subjectRef={subjectRef} />
    </div>
  );
}
