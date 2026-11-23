import { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';

import {
  DRAFT_VAULT_CAPACITY_MESSAGE,
} from '../application/remote-draft-vault';

import './draft-vault-capacity-dialog.css';

/** The form/Inspector remains mounted; dismiss never loses unsaved fields. */
export function DraftVaultCapacityDialog({
  onDismiss,
}: Readonly<{ onDismiss: () => void }>) {
  const titleId = useId();
  const detailId = useId();
  const closeRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    const previous = document.activeElement;
    closeRef.current?.focus({ preventScroll: true });
    return () => {
      if (previous instanceof HTMLElement && previous.isConnected) {
        previous.focus({ preventScroll: true });
      }
    };
  }, []);

  if (typeof document === 'undefined') return null;
  return createPortal(
    <div
      className="draft-vault-capacity__viewport"
      data-temporal-create-portal="vault-capacity"
      onKeyDown={(event) => {
        if (event.key === 'Escape') {
          event.preventDefault();
          event.stopPropagation();
          onDismiss();
        }
      }}
    >
      <section
        className="draft-vault-capacity__dialog"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={detailId}
      >
        <h2 id={titleId}>Spazio Bozze esaurito</h2>
        <p id={detailId}>{DRAFT_VAULT_CAPACITY_MESSAGE}</p>
        <div className="draft-vault-capacity__actions">
          <button ref={closeRef} type="button" onClick={onDismiss}>
            Chiudi
          </button>
        </div>
      </section>
    </div>,
    document.body,
  );
}
