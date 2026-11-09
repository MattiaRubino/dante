import { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';

type ObjectiveRecordingDeleteDialogProps = Readonly<{
  objectiveLabel: string;
  busy: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}>;

/**
 * A confirmed Observation/Evaluation is irreversibly deleted, not merely
 * hidden from the editor. The canonical Objective definition stays intact.
 * This portal does not participate in the parent's unsaved Edit transaction.
 */
export function ObjectiveRecordingDeleteDialog({
  objectiveLabel,
  busy,
  onConfirm,
  onCancel,
}: ObjectiveRecordingDeleteDialogProps) {
  const titleId = useId();
  const descriptionId = useId();
  const cancelRef = useRef<HTMLButtonElement | null>(null);
  const confirmRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    const prior =
      document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;
    cancelRef.current?.focus();
    return () => {
      if (prior?.isConnected) prior.focus();
    };
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        event.stopImmediatePropagation();
        if (!busy) onCancel();
      }
      if (event.key !== 'Tab') return;
      if (busy) {
        event.preventDefault();
        return;
      }
      if (event.shiftKey && document.activeElement === cancelRef.current) {
        event.preventDefault();
        confirmRef.current?.focus();
      } else if (!event.shiftKey &&
                 document.activeElement === confirmRef.current) {
        event.preventDefault();
        cancelRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown, true);
    return () => window.removeEventListener('keydown', handleKeyDown, true);
  }, [busy, onCancel]);

  return createPortal(
    <div className="timeline-session-attempt-delete__backdrop">
      <section
        className="timeline-session-attempt-delete__dialog"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <h2 id={titleId}>Eliminare la registrazione?</h2>
        <p id={descriptionId}>
          {objectiveLabel}: il risultato e tutte le sue registrazioni saranno
          cancellati definitivamente. L’obiettivo rimarrà disponibile in
          Modifica, senza risultati registrati.
        </p>
        <div className="timeline-session-attempt-delete__actions">
          <button
            ref={cancelRef}
            type="button"
            disabled={busy}
            onClick={onCancel}
          >
            Annulla
          </button>
          <button
            ref={confirmRef}
            type="button"
            disabled={busy}
            className="timeline-session-attempt-delete__danger"
            onClick={onConfirm}
          >
            {busy ? 'Eliminazione…' : 'Sì, elimina'}
          </button>
        </div>
      </section>
    </div>,
    document.body,
  );
}
