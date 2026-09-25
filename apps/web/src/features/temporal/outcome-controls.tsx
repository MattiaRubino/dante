import { useMemo, useState } from 'react';

import './outcome-controls.css';

import {
  createRemoteTemporalActualDataSource,
  type ActualSubjectKind,
  type TemporalActualView,
} from './remote-actual-data-source';
import {
  createRemoteTemporalOutcomeDataSource,
  type TemporalOutcomeView,
} from './remote-outcome-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return `${fallback} ${error.message}`;
  }
  return fallback;
}

export function OutcomeControls({
  kind,
  subjectRef,
}: Readonly<{
  kind: ActualSubjectKind;
  subjectRef: string;
}>) {
  const actualSource = useMemo(
    () => createRemoteTemporalActualDataSource(globalThis.fetch),
    [],
  );
  const outcomeSource = useMemo(
    () => createRemoteTemporalOutcomeDataSource(globalThis.fetch),
    [],
  );
  const [actual, setActual] = useState<TemporalActualView | null>(null);
  const [outcome, setOutcome] = useState<TemporalOutcomeView | null>(null);
  const [dispositionCode, setDispositionCode] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const reload = async () => {
    const currentActual = await actualSource.get(kind, subjectRef);
    setActual(currentActual);
    setLoaded(true);
    if (currentActual === null) {
      setOutcome(null);
      setDispositionCode('');
      return { actual: null, outcome: null } as const;
    }
    const currentOutcome = await outcomeSource.get(currentActual.actualRef);
    setOutcome(currentOutcome);
    setDispositionCode(currentOutcome?.dispositionCode ?? '');
    return { actual: currentActual, outcome: currentOutcome } as const;
  };

  const load = () => {
    setPending(true);
    setMessage(null);
    void reload()
      .then(({ actual: currentActual, outcome: currentOutcome }) => {
        if (currentActual === null) {
          setMessage('Outcome non disponibile: registra prima lo stato reale.');
        } else if (currentOutcome === null) {
          setMessage('Nessun Outcome registrato per questo Actual.');
        } else {
          setMessage('Outcome corrente caricato.');
        }
      })
      .catch((error: unknown) => {
        setLoaded(true);
        setMessage(rejection('Outcome non disponibile.', error));
      })
      .finally(() => setPending(false));
  };

  const save = () => {
    const disposition = dispositionCode.trim();
    if (!disposition) return;
    setPending(true);
    setMessage(null);
    void actualSource
      .get(kind, subjectRef)
      .then(async (currentActual) => {
        if (currentActual === null) {
          setActual(null);
          setOutcome(null);
          setLoaded(true);
          setMessage('Outcome non disponibile: registra prima lo stato reale.');
          return;
        }
        setActual(currentActual);
        const saved = await outcomeSource.record(currentActual.actualRef, {
          operationId: operationId(),
          actualRealizationMaterialStateRef: currentActual.materialStateRef,
          expectedMaterialStateRef: outcome?.materialStateRef ?? null,
          dispositionCode: disposition,
        });
        setOutcome(saved);
        setLoaded(true);
        setDispositionCode(saved.dispositionCode);
        setMessage('Outcome registrato.');
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento Outcome rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-outcome-controls" data-timeline-outcome-subject={subjectRef}>
      <strong>Outcome</strong>
      <small>
        Outcome descrive il risultato o la disposizione di questo Actual. Il codice è
        contestuale al dominio: non esiste uno stato Outcome universale.
      </small>
      <button type="button" disabled={pending} data-timeline-outcome-load onClick={load}>
        Carica Outcome
      </button>
      {loaded ? (
        actual === null ? (
          <p data-timeline-outcome-state>Outcome: non disponibile senza Actual</p>
        ) : (
          <>
            <p data-timeline-outcome-state>
              {outcome === null
                ? 'Outcome: non registrato'
                : `Outcome: ${outcome.dispositionCode}`}
            </p>
            <label>
              Disposizione
              <input
                aria-label="Disposizione Outcome"
                value={dispositionCode}
                disabled={pending}
                maxLength={120}
                placeholder="es. decision.deferred"
                onChange={(event) => setDispositionCode(event.currentTarget.value)}
              />
            </label>
            <button
              type="button"
              disabled={pending || !dispositionCode.trim()}
              data-timeline-outcome-save
              onClick={save}
            >
              {outcome === null ? 'Registra Outcome' : 'Correggi Outcome'}
            </button>
          </>
        )
      ) : null}
      {message === null ? null : (
        <span role={message.startsWith('Aggiornamento') ? 'alert' : 'status'}>{message}</span>
      )}
    </div>
  );
}
