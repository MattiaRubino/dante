import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

import type { RecurringProfileEditScope } from '../../../temporal/remote-recurring-profile-edit';

export function RecurringEditScopeDialog({
  owner,
  selectedHasFacts,
  busy,
  onSelect,
  onCancel,
}: Readonly<{
  owner: 'Activity' | 'Event';
  selectedHasFacts: boolean;
  busy: boolean;
  onSelect: (scope: RecurringProfileEditScope) => void;
  onCancel: () => void;
}>) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const cancelRef = useRef(onCancel);
  const busyRef = useRef(busy);
  cancelRef.current = onCancel;
  busyRef.current = busy;

  useEffect(() => {
    const previousFocus =
      document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;
    dialogRef.current?.querySelector<HTMLButtonElement>('button')?.focus();
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        event.stopImmediatePropagation();
        if (!busyRef.current) cancelRef.current();
      } else if (event.key === 'Tab') {
        const buttons = Array.from(
          dialogRef.current?.querySelectorAll<HTMLButtonElement>(
            'button:not([disabled])',
          ) ?? [],
        );
        if (buttons.length === 0) return;
        event.preventDefault();
        const current = buttons.indexOf(
          document.activeElement as HTMLButtonElement,
        );
        const next =
          (current + (event.shiftKey ? -1 : 1) + buttons.length) %
          buttons.length;
        buttons[next]?.focus();
      }
    };
    document.addEventListener('keydown', handleKeyDown, true);
    return () => {
      document.removeEventListener('keydown', handleKeyDown, true);
      if (previousFocus?.isConnected) {
        previousFocus.focus({ preventScroll: true });
      }
    };
  }, []);

  return createPortal(
    <div className="timeline-recurring-edit-scope-backdrop">
      <div
        ref={dialogRef}
        className="timeline-recurring-edit-scope-dialog"
        role="dialog"
        aria-modal="true"
        aria-label="Ambito modifica ricorrenza"
        data-recurring-edit-scope-dialog
      >
        <h2>Modifica {owner} ricorrente</h2>
        <p>Quali istanze vuoi modificare?</p>
        {selectedHasFacts ? (
          <p>
            Questa istanza contiene registrazioni: resterà invariata se
            modifichi la serie dalla prossima.
          </p>
        ) : null}
        <div className="timeline-recurring-edit-scope-dialog__actions">
          <button
            type="button"
            disabled={busy}
            onClick={() => onSelect('only_this')}
          >
            Solo questa istanza
          </button>
          <button
            type="button"
            disabled={busy}
            onClick={() =>
              onSelect(selectedHasFacts ? 'from_next' : 'this_and_following')
            }
          >
            {selectedHasFacts
              ? 'Dalla prossima istanza'
              : 'Questa e le successive'}
          </button>
          <button type="button" disabled={busy} onClick={onCancel}>
            Annulla
          </button>
        </div>
      </div>
    </div>,
    document.body,
  );
}
