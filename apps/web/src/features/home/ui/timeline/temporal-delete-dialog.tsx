import { useEffect, useId, useRef, type KeyboardEvent as ReactKeyboardEvent } from 'react';
import { createPortal } from 'react-dom';

import './temporal-delete-dialog.css';

export type TemporalDeleteChoice = Readonly<{
  key: string;
  label: string;
  onConfirm: () => void;
}>;

/** Shared hard-deletion confirmation. Preview fingerprints remain owned by callers. */
export function TemporalDeleteDialog({
  subject,
  itemTitle,
  scheduleLabel,
  choices,
  note,
  error,
  busy,
  onCancel,
}: Readonly<{
  subject: 'attività' | 'evento';
  itemTitle: string;
  scheduleLabel?: string;
  choices: readonly TemporalDeleteChoice[];
  note?: string;
  error?: string;
  busy: boolean;
  onCancel: () => void;
}>) {
  const headingId = useId();
  const detailId = useId();
  const dialogRef = useRef<HTMLElement | null>(null);
  const cancelRef = useRef<HTMLButtonElement | null>(null);
  const triggerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    triggerRef.current = document.activeElement as HTMLElement | null;
    cancelRef.current?.focus();
    return () => triggerRef.current?.focus({ preventScroll: true });
  }, []);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!busy) onCancel();
    };
    // Inspector handles Escape in document capture; the modal owns it instead.
    window.addEventListener('keydown', handleEscape, true);
    return () => window.removeEventListener('keydown', handleEscape, true);
  }, [busy, onCancel]);

  const handleTab = (event: ReactKeyboardEvent<HTMLElement>) => {
    if (event.key !== 'Tab') return;
    const buttons = Array.from(
      dialogRef.current?.querySelectorAll<HTMLButtonElement>(
        'button:not(:disabled)',
      ) ?? [],
    );
    const first = buttons[0];
    const last = buttons[buttons.length - 1];
    if (!first || !last) {
      event.preventDefault();
    } else if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  return createPortal(
    <div
      className="timeline-delete-dialog__backdrop"
      onPointerDown={(event) => {
        if (event.target === event.currentTarget && !busy) onCancel();
      }}
    >
      <section
        ref={dialogRef}
        className="timeline-delete-dialog"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={headingId}
        aria-describedby={detailId}
        onKeyDown={handleTab}
      >
        <div className="timeline-delete-dialog__header">
          <h2 id={headingId}>Elimina {subject}</h2>
          <button
            type="button"
            className="timeline-delete-dialog__close"
            aria-label="Chiudi eliminazione"
            disabled={busy}
            onClick={onCancel}
          >
            ×
          </button>
        </div>
        <div className="timeline-delete-dialog__subject">
          <strong>{itemTitle}</strong>
          {scheduleLabel ? <span>{scheduleLabel}</span> : null}
        </div>
        <p id={detailId} className="timeline-delete-dialog__description">
          {choices.length > 1
            ? 'Scegli cosa eliminare. L’operazione è definitiva.'
            : 'L’eliminazione è definitiva.'}
        </p>
        {note ? <p className="timeline-delete-dialog__note">{note}</p> : null}
        {error ? <p role="alert">{error}</p> : null}
        <div className="timeline-delete-dialog__choices">
          {choices.map((choice) => (
            <button
              key={choice.key}
              type="button"
              disabled={busy}
              onClick={choice.onConfirm}
            >
              {choice.label}
            </button>
          ))}
        </div>
        <button
          ref={cancelRef}
          type="button"
          className="timeline-delete-dialog__cancel"
          disabled={busy}
          onClick={onCancel}
        >
          Annulla
        </button>
      </section>
    </div>,
    document.body,
  );
}
