import { useEffect, useRef } from 'react';

/** One discard confirmation for both local Activity and Event editors. */
export function UnsavedChangesDialog({
  onDiscard,
  onContinue,
}: Readonly<{
  onDiscard: () => void;
  onContinue: () => void;
}>) {
  const discardRef = useRef<HTMLButtonElement | null>(null);
  const continueRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    discardRef.current?.focus();
  }, []);

  return (
    <div
      className="timeline-activity-editor__discard"
      role="alertdialog"
      aria-modal="true"
      aria-label="Modifiche non salvate"
      onKeyDown={(event) => {
        if (event.key !== 'Tab') return;
        if (event.shiftKey && document.activeElement === discardRef.current) {
          event.preventDefault();
          continueRef.current?.focus();
        } else if (
          !event.shiftKey &&
          document.activeElement === continueRef.current
        ) {
          event.preventDefault();
          discardRef.current?.focus();
        }
      }}
    >
      <p>Scartare le modifiche non salvate?</p>
      <button ref={discardRef} type="button" onClick={onDiscard}>
        Scarta modifiche
      </button>
      <button ref={continueRef} type="button" onClick={onContinue}>
        Continua a modificare
      </button>
    </div>
  );
}
