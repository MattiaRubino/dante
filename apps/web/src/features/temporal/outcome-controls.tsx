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

const CONTEXT_CODE = /^[a-z][a-z0-9._-]{0,99}$/;

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
  const [vocabularyCode, setVocabularyCode] = useState('');
  const [resultCode, setResultCode] = useState('');
  const [note, setNote] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const normalizedVocabulary = vocabularyCode.trim();
  const vocabularyValid = CONTEXT_CODE.test(normalizedVocabulary);
  const normalizedResult = resultCode.trim();
  const resultValid = CONTEXT_CODE.test(normalizedResult);

  const reload = async (vocabulary = normalizedVocabulary) => {
    const currentActual = await actualSource.get(kind, subjectRef);
    setActual(currentActual);
    setLoaded(true);
    if (currentActual === null || !CONTEXT_CODE.test(vocabulary)) {
      setOutcome(null);
      return { actual: currentActual, outcome: null } as const;
    }
    const currentOutcome = await outcomeSource.get(currentActual.actualRef, vocabulary);
    setOutcome(currentOutcome);
    if (currentOutcome !== null) {
      setResultCode(currentOutcome.resultCode);
      setNote(currentOutcome.note ?? '');
    }
    return { actual: currentActual, outcome: currentOutcome } as const;
  };

  const load = () => {
    if (!vocabularyValid) {
      setLoaded(true);
      setMessage('Inserisci un vocabulary code valido prima di caricare Outcome.');
      return;
    }
    setPending(true);
    setMessage(null);
    void reload(normalizedVocabulary)
      .then(({ actual: currentActual, outcome: currentOutcome }) => {
        if (currentActual === null) {
          setMessage('Outcome non disponibile: registra prima lo stato reale.');
        } else if (currentOutcome === null) {
          setResultCode('');
          setNote('');
          setMessage('Nessun Outcome registrato per questo Actual e vocabolario.');
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
    if (!vocabularyValid || !resultValid) return;
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
        const saved = await outcomeSource.record(currentActual.actualRef, normalizedVocabulary, {
          operationId: operationId(),
          expectedMaterialStateRef: outcome?.materialStateRef ?? null,
          resultCode: normalizedResult,
          note: note.trim() || null,
        });
        setOutcome(saved);
        setLoaded(true);
        setVocabularyCode(saved.vocabularyCode);
        setResultCode(saved.resultCode);
        setNote(saved.note ?? '');
        setMessage('Outcome registrato.');
      })
      .catch((error: unknown) =>
        reload(normalizedVocabulary)
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento Outcome rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-outcome-controls" data-timeline-outcome-subject={subjectRef}>
      <strong>Outcome</strong>
      <small>
        Outcome descrive un risultato contestuale di questo Actual. Vocabolario e risultato
        appartengono al dominio: non esiste uno stato Outcome universale.
      </small>
      {actual === null && loaded ? (
        <p data-timeline-outcome-state>Outcome: non disponibile senza Actual</p>
      ) : null}
      <label>
        Vocabolario
        <input
          aria-label="Vocabolario Outcome"
          value={vocabularyCode}
          disabled={pending}
          maxLength={100}
          placeholder="es. workout.execution"
          onChange={(event) => {
            setVocabularyCode(event.currentTarget.value);
            setOutcome(null);
            setLoaded(false);
          }}
        />
      </label>
      <button
        type="button"
        disabled={pending || !vocabularyValid}
        data-timeline-outcome-load
        onClick={load}
      >
        Carica Outcome
      </button>
      {loaded && actual !== null && vocabularyValid ? (
        <>
          <p data-timeline-outcome-state>
            {outcome === null ? 'Outcome: non registrato' : `Outcome: ${outcome.resultCode}`}
          </p>
          <label>
            Risultato
            <input
              aria-label="Risultato Outcome"
              value={resultCode}
              disabled={pending}
              maxLength={100}
              placeholder="es. completed"
              onChange={(event) => setResultCode(event.currentTarget.value)}
            />
          </label>
          <label>
            Nota opzionale
            <textarea
              aria-label="Nota Outcome"
              value={note}
              disabled={pending}
              maxLength={2000}
              onChange={(event) => setNote(event.currentTarget.value)}
            />
          </label>
          <button
            type="button"
            disabled={pending || !resultValid}
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