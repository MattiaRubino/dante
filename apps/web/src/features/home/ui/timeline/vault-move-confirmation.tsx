import './vault-move-confirmation.css';

/** Inspector-local owner confirmation; deletion and Vault writes remain backend-atomic. */
export function VaultMoveConfirmation({
  subject,
  recordedSessions = 0,
  recordedObjectives = 0,
  busy,
  error,
  onConfirm,
  onCancel,
}: Readonly<{
  subject: 'attività' | 'evento';
  recordedSessions?: number;
  recordedObjectives?: number;
  busy: boolean;
  error?: string;
  onConfirm: () => void;
  onCancel: () => void;
}>) {
  const hasRecordedFacts = recordedSessions > 0 || recordedObjectives > 0;
  return (
    <section
      className="timeline-activity-inspector__confirmation timeline-vault-move-confirmation"
      role="region"
      aria-label={`Sposta ${subject} in Bozze`}
    >
      <strong>Sposta in Bozze</strong>
      <p>La configurazione verrà conservata. L’originale sarà eliminato.</p>
      {hasRecordedFacts ? (
        <p className="timeline-vault-move-confirmation__warning" role="note">
          Eliminazione definitiva di{' '}
          {[
            recordedSessions > 0
              ? `${recordedSessions} ${recordedSessions === 1 ? 'Sessione' : 'Sessioni'}`
              : null,
            recordedObjectives > 0
              ? `${recordedObjectives} ${recordedObjectives === 1 ? 'risultato' : 'risultati'} di Obiettivi`
              : null,
          ]
            .filter(Boolean)
            .join(' e ')}.
        </p>
      ) : null}
      {error ? <p role="alert" className="timeline-vault-move-confirmation__warning">{error}</p> : null}
      <div className="timeline-vault-move-confirmation__actions">
        <button type="button" disabled={busy} onClick={onCancel}>Annulla</button>
        <button
          type="button"
          className="timeline-vault-move-confirmation__confirm"
          disabled={busy}
          aria-label="Conferma spostamento in Bozze"
          onClick={onConfirm}
        >
          {busy ? 'Spostamento…' : 'Sposta in Bozze'}
        </button>
      </div>
    </section>
  );
}
