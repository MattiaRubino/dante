import { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';

type SessionAttemptDeleteDialogProps = Readonly<{
  sessionType: 'main' | 'named';
  inProgress: boolean;
  busy: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}>;

/**
 * One factual Session-attempt deletion, not Activity deletion or editor Save.
 * The portal is intentionally outside the scrolling Activity editor form.
 */
export function SessionAttemptDeleteDialog({
  sessionType,
  inProgress,
  busy,
  onConfirm,
  onCancel,
}: SessionAttemptDeleteDialogProps) {
  const titleId = useId();
  const detailsId = useId();
  const cancelRef = useRef<HTMLButtonElement | null>(null);
  const confirmRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    const previousFocus =
      document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;
    cancelRef.current?.focus();
    return () => {
      if (previousFocus?.isConnected) previousFocus.focus();
    };
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        // The underlying Inspector must never consume the same Escape.
        event.preventDefault();
        event.stopImmediatePropagation();
        if (!busy) onCancel();
      }
      if (event.key !== 'Tab') return;
      if (busy) {
        event.preventDefault();
        return;
      }
      const cancel = cancelRef.current;
      const confirm = confirmRef.current;
      if (!cancel || !confirm) return;
      if (event.shiftKey && document.activeElement === cancel) {
        event.preventDefault();
        confirm.focus();
      } else if (!event.shiftKey && document.activeElement === confirm) {
        event.preventDefault();
        cancel.focus();
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
        aria-describedby={detailsId}
      >
        <h2 id={titleId}>Eliminare la registrazione?</h2>
        <p id={detailsId}>
          {sessionType === 'main'
            ? 'Sessione principale.'
            : 'Sessione interna.'}{' '}
          Tempi e pause saranno cancellati definitivamente.
          {inProgress
            ? ' Il cronometro attivo o in pausa sarà interrotto.'
            : ''}
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
            className="timeline-session-attempt-delete__danger"
            disabled={busy}
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
