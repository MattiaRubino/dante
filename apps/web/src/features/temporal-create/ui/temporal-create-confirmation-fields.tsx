import { useId, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

type TemporalCreateConfirmationFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch?: (patch: Partial<TemporalCreateFields>) => void;
  renderError?: (path: string) => React.ReactNode;
}>;

export function TemporalCreateConfirmationFields({
  fields,
}: TemporalCreateConfirmationFieldsProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const optionsId = useId();
  const radioName = useId();
  const [open, setOpen] = useState(false);
  const { draft, patch } = useTemporalCreateU2Draft();

  if (fields.kind !== 'activity') return null;

  const structure = draft.activityStructure;
  const enabled = structure.realityMode !== 'manual';

  const patchStructure = (
    changes: Partial<typeof structure>,
  ) =>
    patch({
      activityStructure: Object.freeze({ ...structure, ...changes }),
    });

  const setMode = (realityMode: TemporalCreateRealityMode) => {
    patchStructure({ realityMode });
    setOpen(false);
  };

  return (
    <section
      className={`temporal-create-reality-section${enabled ? ' is-enabled' : ''}`}
      data-outcome-confirmation="activity"
      aria-label={italian ? 'Conferma esito' : 'Outcome confirmation'}
    >
      <label className="temporal-create-reality-toggle">
        <input
          type="checkbox"
          checked={enabled}
          onChange={(event) => {
            const nextEnabled = event.currentTarget.checked;
            const hasRequiredChild = structure.children.some(
              (child) => child.requirementCode === 'required',
            );
            patchStructure({
              realityMode: nextEnabled ? 'review_on_end' : 'manual',
              childGuardMode:
                nextEnabled && hasRequiredChild ? 'confirm' : 'none',
            });
            setOpen(nextEnabled);
          }}
        />
        <span>{italian ? 'Conferma esito' : 'Confirm outcome'}</span>
      </label>

      {enabled ? (
        <button
          type="button"
          className="temporal-create-reality-options-trigger"
          aria-expanded={open}
          aria-controls={optionsId}
          aria-label={
            italian
              ? 'Scegli come confermare l’esito'
              : 'Choose how to confirm the outcome'
          }
          onClick={() => setOpen((current) => !current)}
        >
          <span aria-hidden="true">{open ? '⌃' : '⌄'}</span>
        </button>
      ) : null}

      {enabled && open ? (
        <div
          className="temporal-create-reality-options"
          id={optionsId}
          role="group"
          aria-label={italian ? 'Modalità conferma esito' : 'Outcome confirmation mode'}
        >
          <label>
            <input
              type="radio"
              name={radioName}
              value="review_on_end"
              checked={structure.realityMode === 'review_on_end'}
              onChange={() => setMode('review_on_end')}
            />
            <span>{italian ? 'Ricordami alla fine' : 'Remind me at the end'}</span>
          </label>
          <label>
            <input
              type="radio"
              name={radioName}
              value="auto_confirm_outcome"
              checked={structure.realityMode === 'auto_confirm_outcome'}
              onChange={() => setMode('auto_confirm_outcome')}
            />
            <span>
              {italian ? 'Conferma automaticamente' : 'Confirm automatically'}
            </span>
          </label>
        </div>
      ) : null}
    </section>
  );
}
