import { useMemo, useState } from 'react';

import './outcome-controls.css';

import {
  createRemoteTemporalActualDataSource,
  type ActualSubjectKind,
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
  const [actualRef, setActualRef] = useState<string | null>(null);
  const [outcome, setOutcome] = useState<TemporalOutcomeView | null>(null);
  const [vocabularyCode, setVocabularyCode] = useState('');
  const [resultCode, setResultCode] = useState('');
  const [note, setNote] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const resolveActual = async (): Promise<string | null> => {
    const actual = await actualSource.get(kind, subjectRef);
    if (actual === null) {
      setActualRef(null);
      setOutcome(null);
      setLoaded(true);
      setMessage('Esito non disponibile: registra prima lo stato reale.');
      return null;
    }
    setActualRef(actual.actualRef);
    return actual.actualRef;
  };

  const load = () => {
    const vocabulary = vocabularyCode.trim();
    if (!vocabulary) return;
    setPending(true);
    setMessage(null);
    void resolveActual()
      .then(async (resolvedActualRef) => {
        if (resolvedActualRef === null) return;
        const current = await outcomeSource.get(resolvedActualRef, vocabulary);
        setOutcome(current);
        setLoaded(true);
        if (current === null) {
          setResultCode('');
          setNote('');
          setMessage('Nessun Outcome registrato per questo vocabolario.');
        } else {
          setResultCode(current.resultCode);
          setNote(current.note ?? '');
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
    const vocabulary = vocabularyCode.trim();
    const result = resultCode.trim();
    if (!vocabulary || !result) return;
    setPending(true);
    setMessage(null);
    void (actualRef === null ? resolveActual() : Promise.resolve(actualRef))
      .then(async (resolvedActualRef) => {
        if (resolvedActualRef === null) return;
        const saved = await outcomeSource.record(resolvedActualRef, {
          operationId: operationId(),
          vocabularyCode: vocabulary,
          expectedMaterialStateRef: outcome?.materialStateRef ?? null,
          resultCode: result,
          note: note.trim() ? note.trim() : null,
        });
        setOutcome(saved);
        setLoaded(true);
        setResultCode(saved.resultCode);
        setNote(saved.note ?? '');
        setMessage('Outcome registrato.');
      })
      .catch((error: unknown) => {
        setMessage(rejection('Aggiornamento Outcome rifiutato.', error));
      })
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-outcome-controls" data-timeline-outcome-subject={subjectRef}>
      <strong>Outcome</strong>
      <small>
        Il risultato è contestuale: scegli un vocabolario adatto al dominio, non uno stato
        universale.
      </small>
      <label>
        Vocabolario
        <input
          aria-label="Vocabolario Outcome"
          value={vocabularyCode}
          disabled={pending}
          maxLength={100}
          placeholder="es. meeting.decision"
          onChange={(event) => {
            setVocabularyCode(event.currentTarget.value);
            setActualRef(null);
            setOutcome(null);
            setLoaded(false);
          }}
        />
      </label>
      <button
        type="button"
        disabled={pending || !vocabularyCode.trim()}
        data-timeline-outcome-load
        onClick={load}
      >
        Carica Outcome
      </button>
      {loaded && actualRef !== null ? (
        <>
          <p data-timeline-outcome-state>
            {outcome === null
              ? 'Outcome: non registrato'
              : `Outcome: ${outcome.resultCode}`}
          </p>
          <label>
            Risultato
            <input
              aria-label="Risultato Outcome"
              value={resultCode}
              disabled={pending}
              maxLength={100}
              placeholder="es. decision.deferred"
              onChange={(event) => setResultCode(event.currentTarget.value)}
            />
          </label>
          <label>
            Nota
            <input
              aria-label="Nota Outcome"
              value={note}
              disabled={pending}
              maxLength={2000}
              onChange={(event) => setNote(event.currentTarget.value)}
            />
          </label>
          <button
            type="button"
            disabled={pending || !resultCode.trim()}
            data-timeline-outcome-save
            onClick={save}
          >
            {outcome === null ? 'Registra Outcome' : 'Correggi Outcome'}
          </button>
        </>
      ) : null}
      {message === null ? null : (
        <span role={message.startsWith('Aggiornamento') ? 'alert' : 'status'}>{message}</span>
      )}
    </div>
  );
}
