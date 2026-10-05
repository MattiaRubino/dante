import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

type Props = Readonly<{ fields: TemporalCreateFields }>;

const MODES: readonly TemporalCreateRealityMode[] = [
  'manual',
  'review_on_end',
  'auto_confirm_outcome',
];

export function TemporalCreateConfirmationFields({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (event.target instanceof Node && !rootRef.current?.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  if (fields.kind !== 'activity') return null;

  const structure = draft.activityStructure;
  const mode = structure.realityMode;
  const labels: Record<TemporalCreateRealityMode, string> = italian
    ? {
        manual: 'Manuale',
        review_on_end: 'Ricordami alla fine',
        auto_confirm_outcome: 'Conferma automaticamente',
      }
    : {
        manual: 'Manual',
        review_on_end: 'Remind me at the end',
        auto_confirm_outcome: 'Confirm automatically',
      };

  const choose = (realityMode: TemporalCreateRealityMode) => {
    const hasRequiredChild = structure.children.some(
      (child) => child.requirementCode === 'required',
    );
    patch({
      activityStructure: Object.freeze({
        ...structure,
        realityMode,
        childGuardMode:
          realityMode !== 'manual' && hasRequiredChild ? 'confirm' : 'none',
      }),
    });
    setOpen(false);
  };

  return (
    <section
      ref={rootRef}
      className="temporal-create-outcome-field"
      data-outcome-confirmation="activity"
      aria-label={italian ? 'Esito al termine' : 'Outcome at the end'}
      onKeyDown={(event) => {
        if (event.key === 'Escape') setOpen(false);
      }}
    >
      <button
        className="temporal-create-outcome-field__trigger"
        type="button"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
      >
        <span className="temporal-create-outcome-field__icon" aria-hidden="true">✓</span>
        <span className="temporal-create-outcome-field__label">
          {italian ? 'Esito al termine' : 'Outcome at the end'} · {labels[mode]}
        </span>
        <span className="temporal-create-outcome-field__chevron" aria-hidden="true">
          {open ? '⌃' : '⌄'}
        </span>
      </button>
      {open ? (
        <div
          className="temporal-create-outcome-field__options"
          role="group"
          aria-label={italian ? 'Modalità esito' : 'Outcome mode'}
        >
          {MODES.map((option) => (
            <button
              key={option}
              type="button"
              aria-pressed={mode === option}
              className={mode === option ? 'is-selected' : undefined}
              onClick={() => choose(option)}
            >
              {labels[option]}
            </button>
          ))}
        </div>
      ) : null}
    </section>
  );
}
