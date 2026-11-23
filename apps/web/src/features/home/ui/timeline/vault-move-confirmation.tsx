import { useEffect, useRef, useState } from 'react';

import { TemporalDeleteDialog } from './temporal-delete-dialog';

import './vault-move-confirmation.css';

/** Replaces Inspector contents; only recorded facts require a second modal. */
export function VaultMoveConfirmation({
  subject,
  itemTitle,
  scheduleLabel,
  recordedSessions = 0,
  recordedObjectives = 0,
  busy,
  error,
  onConfirm,
  onCancel,
}: Readonly<{
  subject: 'attività' | 'evento';
  itemTitle: string;
  scheduleLabel?: string | undefined;
  recordedSessions?: number;
  recordedObjectives?: number;
  busy: boolean;
  error?: string;
  onConfirm: () => void;
  onCancel: () => void;
}>) {
  const [confirmLoss, setConfirmLoss] = useState(false);
  const cancelRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    const previousFocus = document.activeElement;
    cancelRef.current?.focus({ preventScroll: true });
    return () => {
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) {
        previousFocus.focus({ preventScroll: true });
      }
    };
  }, []);
  const hasRecordedFacts = recordedSessions > 0 || recordedObjectives > 0;
  const lostFacts = [
    recordedSessions > 0
      ? `${recordedSessions} ${recordedSessions === 1 ? 'Sessione' : 'Sessioni'}`
      : null,
    recordedObjectives > 0
      ? `${recordedObjectives} ${recordedObjectives === 1 ? 'risultato' : 'risultati'} di Obiettivi`
      : null,
  ].filter(Boolean).join(' e ');

  return (
    <section
      className="timeline-activity-inspector__confirmation timeline-vault-move-confirmation"
      role="region"
      aria-label={`Sposta ${subject} in Bozze`}
    >
      <h4>Spostare nelle Bozze?</h4>
      <strong className="timeline-vault-move-confirmation__item">{itemTitle}</strong>
      <p>La configurazione rimarrà nelle Bozze. L’originale verrà eliminato.</p>
      {hasRecordedFacts ? (
        <p className="timeline-vault-move-confirmation__warning" role="note">
          Attenzione: Eliminazione definitiva di {lostFacts}.
        </p>
      ) : null}
      {error ? (
        <p role="alert" className="timeline-vault-move-confirmation__warning">
          {error}
        </p>
      ) : null}
      <div className="timeline-vault-move-confirmation__actions">
        <button ref={cancelRef} type="button" disabled={busy} onClick={onCancel}>
          Annulla
        </button>
        <button
          type="button"
          className={`timeline-vault-move-confirmation__confirm${hasRecordedFacts ? ' is-destructive' : ''}`}
          disabled={busy}
          aria-label="Conferma spostamento in Bozze"
          onClick={() => {
            if (hasRecordedFacts) {
              setConfirmLoss(true);
            } else {
              onConfirm();
            }
          }}
        >
          {busy ? 'Spostamento…' : 'Sposta in Bozze'}
        </button>
      </div>
      {confirmLoss ? (
        <TemporalDeleteDialog
          subject={subject}
          itemTitle={itemTitle}
          {...(scheduleLabel ? { scheduleLabel } : {})}
          heading="Conferma perdita registrazioni"
          description="Questa operazione è irreversibile."
          note={`Eliminerai definitivamente ${lostFacts}. Nelle Bozze resterà solo la configurazione.`}
          busy={busy}
          error={error}
          choices={[
            {
              key: 'move-with-loss',
              label: 'Elimina registrazioni e sposta',
              onConfirm,
            },
          ]}
          onCancel={() => setConfirmLoss(false)}
        />
      ) : null}
    </section>
  );
}
