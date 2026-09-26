import { useMemo, useState } from 'react';

import './confirmation-controls.css';

import {
  createRemoteTemporalActualDataSource,
  type ActualSubjectKind,
} from './remote-actual-data-source';
import {
  createRemoteTemporalConfirmationDataSource,
  type TemporalConfirmationView,
} from './remote-confirmation-data-source';
import {
  createRemoteTemporalOutcomeDataSource,
  type TemporalOutcomeView,
} from './remote-outcome-data-source';

const CONTEXT_CODE = /^[a-z0-9][a-z0-9._:-]{0,119}$/;

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return `${fallback} ${error.message}`;
  }
  return fallback;
}

export function ConfirmationControls({
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
  const confirmationSource = useMemo(
    () => createRemoteTemporalConfirmationDataSource(globalThis.fetch),
    [],
  );
  const [outcome, setOutcome] = useState<TemporalOutcomeView | null>(null);
  const [confirmations, setConfirmations] = useState<readonly TemporalConfirmationView[]>([]);
  const [purposeCode, setPurposeCode] = useState('');
  const [stanceCode, setStanceCode] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const normalizedPurpose = purposeCode.trim();
  const normalizedStance = stanceCode.trim();
  const codesValid = CONTEXT_CODE.test(normalizedPurpose) && CONTEXT_CODE.test(normalizedStance);
  const ownOnCurrent = confirmations.find(
    (item) =>
      item.confirmerIsSelf &&
      outcome !== null &&
      item.outcomeDispositionMaterialStateRef === outcome.materialStateRef &&
      (normalizedPurpose === '' || item.purposeCode === normalizedPurpose),
  );
  const othersOnCurrent = confirmations.filter(
    (item) =>
      !item.confirmerIsSelf &&
      outcome !== null &&
      item.outcomeDispositionMaterialStateRef === outcome.materialStateRef,
  );

  const reload = async () => {
    const currentActual = await actualSource.get(kind, subjectRef);
    if (currentActual === null) {
      setOutcome(null);
      setConfirmations([]);
      setLoaded(true);
      return { outcome: null, confirmations: [] as const };
    }
    const currentOutcome = await outcomeSource.get(currentActual.actualRef);
    setOutcome(currentOutcome);
    if (currentOutcome === null) {
      setConfirmations([]);
      setLoaded(true);
      return { outcome: currentOutcome, confirmations: [] as const };
    }
    const currentConfirmations = await confirmationSource.list(currentOutcome.outcomeRef);
    setConfirmations(currentConfirmations);
    setLoaded(true);
    const own = currentConfirmations.find(
      (item) =>
        item.confirmerIsSelf &&
        item.outcomeDispositionMaterialStateRef === currentOutcome.materialStateRef,
    );
    if (own !== undefined) {
      setPurposeCode(own.purposeCode);
      setStanceCode(own.stanceCode);
    }
    return { outcome: currentOutcome, confirmations: currentConfirmations } as const;
  };

  const load = () => {
    setPending(true);
    setMessage(null);
    void reload()
      .then(({ outcome: currentOutcome, confirmations: currentConfirmations }) => {
        if (currentOutcome === null) {
          setMessage('Confirmation non disponibile: registra prima un Outcome.');
        } else if (currentConfirmations.length === 0) {
          setMessage('Nessuna Confirmation registrata. Questo non significa che l’Outcome sia falso.');
        } else {
          setMessage('Confirmation caricate.');
        }
      })
      .catch((error: unknown) => {
        setLoaded(true);
        setMessage(rejection('Confirmation non disponibile.', error));
      })
      .finally(() => setPending(false));
  };

  const save = () => {
    if (!codesValid) return;
    setPending(true);
    setMessage(null);
    void actualSource
      .get(kind, subjectRef)
      .then(async (currentActual) => {
        if (currentActual === null) {
          setOutcome(null);
          setConfirmations([]);
          setLoaded(true);
          setMessage('Confirmation non disponibile: registra prima un Outcome.');
          return;
        }
        const currentOutcome = await outcomeSource.get(currentActual.actualRef);
        if (currentOutcome === null) {
          setOutcome(null);
          setConfirmations([]);
          setLoaded(true);
          setMessage('Confirmation non disponibile: registra prima un Outcome.');
          return;
        }
        setOutcome(currentOutcome);
        const currentConfirmations = await confirmationSource.list(currentOutcome.outcomeRef);
        const expected = currentConfirmations.find(
          (item) =>
            item.confirmerIsSelf &&
            item.outcomeDispositionMaterialStateRef === currentOutcome.materialStateRef &&
            item.purposeCode === normalizedPurpose,
        );
        const saved = await confirmationSource.record(currentOutcome.outcomeRef, {
          operationId: operationId(),
          outcomeDispositionMaterialStateRef: currentOutcome.materialStateRef,
          expectedMaterialStateRef: expected?.materialStateRef ?? null,
          purposeCode: normalizedPurpose,
          stanceCode: normalizedStance,
        });
        const refreshed = await confirmationSource.list(currentOutcome.outcomeRef);
        setConfirmations(refreshed.length === 0 ? [saved] : refreshed);
        setLoaded(true);
        setPurposeCode(saved.purposeCode);
        setStanceCode(saved.stanceCode);
        setMessage('Confirmation registrata.');
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento Confirmation rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-confirmation-controls" data-timeline-confirmation-subject={subjectRef}>
      <strong>Confirmation</strong>
      <small>
        Confirmation è un’attestazione contestuale e opzionale di una versione esatta dell’Outcome.
        Non è Outcome, autorità o verità universale. Assenza di Confirmation non significa falso.
      </small>
      {outcome === null && loaded ? (
        <p data-timeline-confirmation-state>Confirmation: non disponibile senza Outcome</p>
      ) : null}
      <button
        type="button"
        disabled={pending}
        data-timeline-confirmation-load
        onClick={load}
      >
        Carica Confirmation
      </button>
      {loaded && outcome !== null ? (
        <>
          <p data-timeline-confirmation-state>
            {ownOnCurrent === undefined
              ? 'Confirmation: nessuna Confirmation esplicita'
              : `Confirmation: ${ownOnCurrent.purposeCode} / ${ownOnCurrent.stanceCode}`}
          </p>
          {othersOnCurrent.length > 0 ? (
            <p data-timeline-confirmation-others>
              {`Altre Confirmation sullo stesso Outcome: ${othersOnCurrent.length}`}
            </p>
          ) : null}
          <label>
            Scopo
            <input
              aria-label="Scopo Confirmation"
              value={purposeCode}
              disabled={pending}
              maxLength={120}
              placeholder="es. review.personal"
              onChange={(event) => setPurposeCode(event.currentTarget.value)}
            />
          </label>
          <label>
            Attestazione
            <input
              aria-label="Attestazione Confirmation"
              value={stanceCode}
              disabled={pending}
              maxLength={120}
              placeholder="es. attested"
              onChange={(event) => setStanceCode(event.currentTarget.value)}
            />
          </label>
          <button
            type="button"
            disabled={pending || !codesValid}
            data-timeline-confirmation-save
            onClick={save}
          >
            {ownOnCurrent === null || ownOnCurrent === undefined
              ? 'Registra Confirmation'
              : 'Correggi Confirmation'}
          </button>
        </>
      ) : null}
      {message === null ? null : (
        <span role={message.startsWith('Aggiornamento') ? 'alert' : 'status'}>{message}</span>
      )}
    </div>
  );
}
