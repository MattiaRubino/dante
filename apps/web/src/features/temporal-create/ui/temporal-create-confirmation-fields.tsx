import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-outcome-dropdown.css';

type Props = Readonly<{ fields: TemporalCreateFields }>;

export function TemporalCreateConfirmationToggle({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const rootRef = useRef<HTMLElement | null>(null);
  const [open, setOpen] = useState(false);
  const structure = draft.activityStructure;
  const enabled = draft.realityMode !== 'manual';

  useEffect(() => {
    if (!open) return;

    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setOpen(false);
      }
    };

    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  const applyMode = (realityMode: TemporalCreateRealityMode) => {
    const hasRequiredChild = structure.children.some(
      (child) => child.requirementCode === 'required',
    );

    patch({
      realityMode,
      activityStructure: Object.freeze({
        ...structure,
        realityMode,
        childGuardMode:
          fields.kind === 'activity' &&
          realityMode !== 'manual' &&
          hasRequiredChild
            ? 'confirm'
            : 'none',
      }),
    });
  };

  const selectedMode = draft.realityMode;
  const selectedLabel =
    selectedMode === 'auto_confirm_outcome'
      ? italian
        ? 'Conferma automatica'
        : 'Confirm automatically'
      : italian
        ? 'Chiedi al termine'
        : 'Ask at the end';
  const alternateMode: TemporalCreateRealityMode =
    selectedMode === 'auto_confirm_outcome'
      ? 'review_on_end'
      : 'auto_confirm_outcome';
  const alternateLabel =
    alternateMode === 'auto_confirm_outcome'
      ? italian
        ? 'Conferma automatica'
        : 'Confirm automatically'
      : italian
        ? 'Chiedi al termine'
        : 'Ask at the end';

  return (
    <section
      ref={rootRef}
      className={`temporal-create-outcome-control${enabled ? ' is-enabled' : ''}`}
      data-reality-policy={fields.kind}
      aria-label={italian ? 'Verifica realtà' : 'Reality review'}
    >
      <label
        className="temporal-create-outcome-control__check"
        title={
          enabled
            ? italian
              ? 'Disabilita verifica realtà'
              : 'Disable reality review'
            : italian
              ? 'Abilita verifica realtà'
              : 'Enable reality review'
        }
      >
        <input
          type="checkbox"
          checked={enabled}
          aria-label={
            enabled
              ? italian
                ? 'Disabilita verifica realtà'
                : 'Disable reality review'
              : italian
                ? 'Abilita verifica realtà'
                : 'Enable reality review'
          }
          onChange={(event) => {
            const nextEnabled = event.currentTarget.checked;
            applyMode(nextEnabled ? 'review_on_end' : 'manual');
            setOpen(false);
          }}
        />
      </label>

      <button
        type="button"
        className="temporal-create-outcome-control__mode"
        aria-expanded={enabled ? open : undefined}
        aria-haspopup={enabled ? 'menu' : undefined}
        onClick={() => {
          if (!enabled) {
            applyMode('review_on_end');
            setOpen(false);
            return;
          }
          setOpen((current) => !current);
        }}
      >
        <span className="temporal-create-outcome-control__label">
          {enabled
            ? selectedLabel
            : italian
              ? 'Verifica realtà'
              : 'Review reality'}
        </span>
        {enabled ? (
          <span
            className="temporal-create-outcome-control__chevron"
            aria-hidden="true"
          >
            {open ? '⌃' : '⌄'}
          </span>
        ) : null}
      </button>

      {enabled && open ? (
        <div
          className="temporal-create-outcome-control__menu"
          role="menu"
          aria-label={
            italian ? 'Modalità verifica realtà' : 'Outcome review mode'
          }
        >
          <button
            type="button"
            role="menuitem"
            onClick={() => {
              applyMode(alternateMode);
              setOpen(false);
            }}
          >
            {alternateLabel}
          </button>
        </div>
      ) : null}
    </section>
  );
}

