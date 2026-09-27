import { useCallback, useEffect, useMemo, useState } from 'react';

import './conditional-temporal-controls.css';

import {
  createRemoteConditionalTemporalDataSource,
  type ActualRealizationConditionView,
  type ConditionalEvaluationView,
  type ConditionalTemporalSubjectKind,
} from './remote-conditional-temporal-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) return `${fallback} ${error.message}`;
  return fallback;
}

function evaluationText(evaluation: ConditionalEvaluationView): string {
  if (evaluation.resultCode === 'satisfied') return 'Valutazione: soddisfatta → consenti';
  if (evaluation.resultCode === 'not_satisfied') return 'Valutazione: non soddisfatta → trattieni';
  return 'Valutazione: indeterminata → trattieni';
}

export function ConditionalTemporalControls({
  kind,
  subjectRef,
}: Readonly<{
  kind: ConditionalTemporalSubjectKind;
  subjectRef: string;
}>) {
  const source = useMemo(() => createRemoteConditionalTemporalDataSource(globalThis.fetch), []);
  const [condition, setCondition] = useState<ActualRealizationConditionView | null>(null);
  const [evaluation, setEvaluation] = useState<ConditionalEvaluationView | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const current = await source.find(kind, subjectRef);
    setCondition(current);
    setLoaded(true);
    return current;
  }, [kind, source, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void source
      .find(kind, subjectRef)
      .then((current) => {
        if (!cancelled) {
          setCondition(current);
          setLoaded(true);
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setLoaded(true);
          setMessage(rejection('Condizione Actual non disponibile.', error));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [kind, source, subjectRef]);

  const create = () => {
    setPending(true);
    setMessage(null);
    void source
      .create(kind, subjectRef, operationId())
      .then((created) => {
        setCondition(created);
        setMessage('Condizione Actual creata.');
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Creazione condizione rifiutata.', error))),
      )
      .finally(() => setPending(false));
  };

  const evaluate = () => {
    if (condition === null) return;
    setPending(true);
    setMessage(null);
    void source
      .evaluate(condition.conditionRef, operationId())
      .then((next) => {
        setEvaluation(next);
        setMessage('Valutazione registrata.');
      })
      .catch((error: unknown) =>
        setMessage(rejection('Valutazione condizione rifiutata.', error)),
      )
      .finally(() => setPending(false));
  };

  const state = !loaded
    ? 'Condizione Actual: caricamento…'
    : condition === null
      ? 'Condizione Actual: non configurata'
      : 'Condizione Actual: configurata';

  return (
    <section className="timeline-conditional-controls" data-timeline-conditional-subject={subjectRef}>
      <strong>Condizione Actual</strong>
      <p data-timeline-conditional-state>{state}</p>
      {evaluation === null ? null : <p>{evaluationText(evaluation)}</p>}
      {condition === null ? (
        <button type="button" disabled={pending || !loaded} onClick={create}>
          Crea condizione Actual
        </button>
      ) : (
        <button type="button" disabled={pending || !loaded} onClick={evaluate}>
          Valuta condizione Actual
        </button>
      )}
      <small>
        La valutazione legge l'Actual canonico e produce soltanto un segnale allow/withhold:
        non crea né modifica Schedule, Occurrence, Session o Actual.
      </small>
      {message === null ? null : message.endsWith('registrata.') || message.endsWith('creata.') ? (
        <span role="status">{message}</span>
      ) : (
        <span role="alert">{message}</span>
      )}
    </section>
  );
}
