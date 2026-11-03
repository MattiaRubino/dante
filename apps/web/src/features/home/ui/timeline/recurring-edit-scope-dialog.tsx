import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import type { RecurringProfileEditPreview } from '../../../temporal/remote-recurring-profile-edit';

type RecurringEditScopeDialogProps = Readonly<{
  subjectLabel: 'attività' | 'Evento';
  selectedProtection: RecurringProfileEditPreview['selectedProtection'];
  busy?: boolean;
  dragNotice?: string;
  onOnlyThis: () => void;
  onFollowing: () => void;
  onCancel: () => void;
}>;

/**
 * Scope is chosen before opening either occurrence editor.  Keeping this
 * prompt outside the Inspector prevents the choice itself from looking like
 * one of the editable fields and makes the same decision available to a
 * drag-triggered edit.
 */
export function RecurringEditScopeDialog({
  subjectLabel,
  selectedProtection,
  busy = false,
  dragNotice,
  onOnlyThis,
  onFollowing,
  onCancel,
}: RecurringEditScopeDialogProps) {
  const firstChoiceRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    firstChoiceRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onCancel();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [onCancel]);

  const followingLabel = selectedProtection
    ? 'Dalla prossima istanza'
    : 'Questa e le successive';

  return createPortal(
    <div
      className="timeline-recurring-edit-scope-dialog__backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !busy) onCancel();
      }}
    >
      <section
        className="timeline-recurring-edit-scope-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="timeline-recurring-edit-scope-title"
        aria-describedby="timeline-recurring-edit-scope-description"
      >
        <h2 id="timeline-recurring-edit-scope-title">Modifica ricorrenza</h2>
        <p id="timeline-recurring-edit-scope-description">
          {subjectLabel === 'attività' ? 'Questa attività' : 'Questo Evento'} fa
          parte di una ricorrenza. Scegli quali istanze modificare.
        </p>
        {selectedProtection === 'registration' ? (
          <p className="timeline-recurring-edit-scope-dialog__fact-note">
            La registrazione di questa istanza rimane invariata.
          </p>
        ) : null}
        {selectedProtection === 'local_change' ||
        selectedProtection === 'legacy_unknown' ? (
          <p className="timeline-recurring-edit-scope-dialog__fact-note">
            Questa istanza ha modifiche proprie e resta invariata. L’editor
            della serie parte dalla regola generale: le modifiche locali non
            vengono copiate sulle successive.
          </p>
        ) : null}
        {dragNotice ? (
          <p className="timeline-recurring-edit-scope-dialog__fact-note">
            {dragNotice}
          </p>
        ) : null}
        <div className="timeline-recurring-edit-scope-dialog__choices">
          <button
            ref={firstChoiceRef}
            type="button"
            disabled={busy}
            onClick={onOnlyThis}
          >
            Solo questa istanza
          </button>
          <button type="button" disabled={busy} onClick={onFollowing}>
            {followingLabel}
          </button>
          <button type="button" disabled={busy} onClick={onCancel}>
            Annulla
          </button>
        </div>
      </section>
    </div>,
    document.body,
  );
}
