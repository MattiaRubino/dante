import { useMemo, useState } from 'react';

import './reconciliation-controls.css';

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
import {
  createRemoteTemporalReconciliationDataSource,
  type TemporalReconciliationAction,
  type TemporalReconciliationEvidenceView,
  type TemporalReconciliationView,
} from './remote-reconciliation-data-source';

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

function evidenceFor(
  action: TemporalReconciliationAction,
  confirmations: readonly TemporalConfirmationView[],
  selectedConfirmationRefs: ReadonlySet<string>,
): readonly TemporalReconciliationEvidenceView[] {
  return confirmations.map((item) => ({
    confirmationRef: item.confirmationRef,
    confirmationAttestationMaterialStateRef: item.materialStateRef,
    roleCode:
      (action === 'select' || action === 'accept_multiple') &&
      selectedConfirmationRefs.has(item.confirmationRef)
        ? 'selected'
        : 'considered',
  }));
}

export function ReconciliationControls({
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
  const reconciliationSource = useMemo(
    () => createRemoteTemporalReconciliationDataSource(globalThis.fetch),
    [],
  );

  const [outcome, setOutcome] = useState<TemporalOutcomeView | null>(null);
  const [confirmations, setConfirmations] = useState<readonly TemporalConfirmationView[]>([]);
  const [reconciliations, setReconciliations] = useState<readonly TemporalReconciliationView[]>([]);
  const [purposeCode, setPurposeCode] = useState('review.personal');
  const [actionCode, setActionCode] = useState<TemporalReconciliationAction>('unresolved');
  const [selectedConfirmationRefs, setSelectedConfirmationRefs] = useState<ReadonlySet<string>>(
    () => new Set(),
  );
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const normalizedPurpose = purposeCode.trim();
  const currentConfirmations = confirmations.filter(
    (item) =>
      outcome !== null &&
      item.outcomeDispositionMaterialStateRef === outcome.materialStateRef,
  );
  const currentReconciliation = reconciliations.find(
    (item) =>
      outcome !== null &&
      item.outcomeDispositionMaterialStateRef === outcome.materialStateRef &&
      item.purposeCode === normalizedPurpose,
  );
  const selectedCount = currentConfirmations.filter((item) =>
    selectedConfirmationRefs.has(item.confirmationRef),
  ).length;
  const actionValid =
    actionCode === 'select'
      ? selectedCount === 1
      : actionCode === 'accept_multiple'
        ? selectedCount >= 2
        : selectedCount === 0;
  const saveValid = CONTEXT_CODE.test(normalizedPurpose) && actionValid;

  const applyCurrent = (
    currentOutcome: TemporalOutcomeView,
    currentReconciliations: readonly TemporalReconciliationView[],
  ) => {
    const existing = currentReconciliations.find(
      (item) => item.outcomeDispositionMaterialStateRef === currentOutcome.materialStateRef,
    );
    if (existing === undefined) {
      setSelectedConfirmationRefs(new Set());
      return;
    }
    setPurposeCode(existing.purposeCode);
    setActionCode(existing.actionCode);
    setSelectedConfirmationRefs(
      new Set(
        existing.evidence
          .filter((item) => item.roleCode === 'selected')
          .map((item) => item.confirmationRef),
      ),
    );
  };

  const reload = async () => {
    const currentActual = await actualSource.get(kind, subjectRef);
    if (currentActual === null) {
      setOutcome(null);
      setConfirmations([]);
      setReconciliations([]);
      setLoaded(true);
      return { outcome: null, confirmations: [] as const, reconciliations: [] as const };
    }
    const currentOutcome = await outcomeSource.get(currentActual.actualRef);
    setOutcome(currentOutcome);
    if (currentOutcome === null) {
      setConfirmations([]);
      setReconciliations([]);
      setLoaded(true);
      return { outcome: null, confirmations: [] as const, reconciliations: [] as const };
    }
    const [currentConfirmationRows, currentReconciliationRows] = await Promise.all([
      confirmationSource.list(currentOutcome.outcomeRef),
      reconciliationSource.list(currentOutcome.outcomeRef),
    ]);
    setConfirmations(currentConfirmationRows);
    setReconciliations(currentReconciliationRows);
    applyCurrent(currentOutcome, currentReconciliationRows);
    setLoaded(true);
    return {
      outcome: currentOutcome,
      confirmations: currentConfirmationRows,
      reconciliations: currentReconciliationRows,
    } as const;
  };

  const load = () => {
    setPending(true);
    setMessage(null);
    void reload()
      .then(({ outcome: currentOutcome, reconciliations: currentRows }) => {
        if (currentOutcome === null) {
          setMessage('Reconciliation non disponibile: registra prima un Outcome.');
        } else if (currentRows.length === 0) {
          setMessage('Nessuna Reconciliation registrata. Il conflitto può restare esplicitamente irrisolto.');
        } else {
          setMessage('Reconciliation caricate.');
        }
      })
      .catch((error: unknown) => {
        setLoaded(true);
        setMessage(rejection('Reconciliation non disponibile.', error));
      })
      .finally(() => setPending(false));
  };

  const toggleEvidence = (confirmationRef: string) => {
    setSelectedConfirmationRefs((current) => {
      const next = new Set(current);
      if (next.has(confirmationRef)) next.delete(confirmationRef);
      else next.add(confirmationRef);
      return next;
    });
  };

  const changeAction = (nextAction: TemporalReconciliationAction) => {
    setActionCode(nextAction);
    if (nextAction === 'unresolved' || nextAction === 'defer' || nextAction === 'escalate') {
      setSelectedConfirmationRefs(new Set());
    }
  };

  const save = () => {
    if (!saveValid) return;
    setPending(true);
    setMessage(null);
    void actualSource
      .get(kind, subjectRef)
      .then(async (currentActual) => {
        if (currentActual === null) {
          setMessage('Reconciliation non disponibile: registra prima un Outcome.');
          return;
        }
        const currentOutcome = await outcomeSource.get(currentActual.actualRef);
        if (currentOutcome === null) {
          setMessage('Reconciliation non disponibile: registra prima un Outcome.');
          return;
        }
        const [currentConfirmationRows, currentReconciliationRows] = await Promise.all([
          confirmationSource.list(currentOutcome.outcomeRef),
          reconciliationSource.list(currentOutcome.outcomeRef),
        ]);
        const targetConfirmations = currentConfirmationRows.filter(
          (item) => item.outcomeDispositionMaterialStateRef === currentOutcome.materialStateRef,
        );
        const expected = currentReconciliationRows.find(
          (item) =>
            item.outcomeDispositionMaterialStateRef === currentOutcome.materialStateRef &&
            item.purposeCode === normalizedPurpose,
        );
        const saved = await reconciliationSource.record(currentOutcome.outcomeRef, {
          operationId: operationId(),
          outcomeDispositionMaterialStateRef: currentOutcome.materialStateRef,
          expectedMaterialStateRef: expected?.materialStateRef ?? null,
          purposeCode: normalizedPurpose,
          actionCode,
          evidence: evidenceFor(actionCode, targetConfirmations, selectedConfirmationRefs),
        });
        const refreshed = await reconciliationSource.list(currentOutcome.outcomeRef);
        setOutcome(currentOutcome);
        setConfirmations(currentConfirmationRows);
        setReconciliations(refreshed.length === 0 ? [saved] : refreshed);
        setLoaded(true);
        setPurposeCode(saved.purposeCode);
        setActionCode(saved.actionCode);
        setSelectedConfirmationRefs(
          new Set(
            saved.evidence
              .filter((item) => item.roleCode === 'selected')
              .map((item) => item.confirmationRef),
          ),
        );
        setMessage('Reconciliation registrata.');
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento Reconciliation rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  return (
    <div className="timeline-reconciliation-controls" data-timeline-reconciliation-subject={subjectRef}>
      <strong>Reconciliation</strong>
      <small>
        Reconciliation risolve contestualmente evidenze di Confirmation su una versione esatta
        dell’Outcome. Non riscrive Outcome o Confirmation e non stabilisce una verità universale.
      </small>
      {outcome === null && loaded ? (
        <p data-timeline-reconciliation-state>Reconciliation: non disponibile senza Outcome</p>
      ) : null}
      <button type="button" disabled={pending} data-timeline-reconciliation-load onClick={load}>
        Carica Reconciliation
      </button>
      {loaded && outcome !== null ? (
        <>
          <p data-timeline-reconciliation-state>
            {currentReconciliation === undefined
              ? 'Reconciliation: nessuna decisione contestuale registrata'
              : `Reconciliation: ${currentReconciliation.purposeCode} / ${currentReconciliation.actionCode}`}
          </p>
          <label>
            Scopo
            <input
              aria-label="Scopo Reconciliation"
              value={purposeCode}
              disabled={pending}
              maxLength={120}
              placeholder="es. review.personal"
              onChange={(event) => setPurposeCode(event.currentTarget.value)}
            />
          </label>
          <label>
            Azione
            <select
              aria-label="Azione Reconciliation"
              value={actionCode}
              disabled={pending}
              onChange={(event) => changeAction(event.currentTarget.value as TemporalReconciliationAction)}
            >
              <option value="unresolved">unresolved</option>
              <option value="select">select</option>
              <option value="accept_multiple">accept_multiple</option>
              <option value="defer">defer</option>
              <option value="escalate">escalate</option>
            </select>
          </label>
          {currentConfirmations.length === 0 ? (
            <small>Nessuna Confirmation sul MaterialState corrente dell’Outcome.</small>
          ) : (
            <ul className="timeline-reconciliation-evidence" aria-label="Evidenze Reconciliation">
              {currentConfirmations.map((item) => (
                <li key={item.confirmationRef}>
                  <label>
                    <input
                      type="checkbox"
                      aria-label={`Seleziona Confirmation ${item.confirmationRef}`}
                      checked={selectedConfirmationRefs.has(item.confirmationRef)}
                      disabled={
                        pending ||
                        actionCode === 'unresolved' ||
                        actionCode === 'defer' ||
                        actionCode === 'escalate'
                      }
                      onChange={() => toggleEvidence(item.confirmationRef)}
                    />
                    {`${item.purposeCode} / ${item.stanceCode}`}
                  </label>
                </li>
              ))}
            </ul>
          )}
          {!actionValid ? (
            <small role="status">
              {actionCode === 'select'
                ? 'select richiede esattamente una Confirmation selezionata.'
                : 'accept_multiple richiede almeno due Confirmation selezionate.'}
            </small>
          ) : null}
          <button
            type="button"
            disabled={pending || !saveValid}
            data-timeline-reconciliation-save
            onClick={save}
          >
            {currentReconciliation === undefined
              ? 'Registra Reconciliation'
              : 'Correggi Reconciliation'}
          </button>
        </>
      ) : null}
      {message === null ? null : (
        <span role={message.startsWith('Aggiornamento') ? 'alert' : 'status'}>{message}</span>
      )}
    </div>
  );
}
