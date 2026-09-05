import { type MouseEvent } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  WorldFocusDanteContextualIntent,
} from '../application/world-focus-dante-contextual-invocation';
import type { WorldFocusContextReferenceSet } from '../model/world-focus-context-reference';
import { isWorldFocusFeatureAvailable } from '../model/world-focus-platform';
import { useOptionalWorldFocusDanteEntry } from './world-focus-dante-entry';
import './world-focus-dante-contextual-entry.css';

type WorldFocusDanteContextualEntryProps = Readonly<{
  intent: WorldFocusDanteContextualIntent;
  contextReferences: WorldFocusContextReferenceSet;
  className?: string;
}>;

function useContextualPrompt(intent: WorldFocusDanteContextualIntent): string {
  const { t } = useTranslation('common');

  switch (intent) {
    case 'why':
      return t(($) => $.common.worldFocus.dante.contextual.why);
    case 'compare':
      return t(($) => $.common.worldFocus.dante.contextual.compare);
    case 'continue':
      return t(($) => $.common.worldFocus.dante.contextual.continue);
    case 'open-source':
      return t(($) => $.common.worldFocus.dante.contextual.openSource);
  }
}

/**
 * P2 explicit contextual entry. It passes only a bounded reference set and a
 * localized editable prompt into the existing D1 composer. It never submits,
 * retrieves a source, authorizes disclosure or creates another DANTE surface.
 */
export function WorldFocusDanteContextualEntry({
  intent,
  contextReferences,
  className,
}: WorldFocusDanteContextualEntryProps) {
  const { t } = useTranslation('common');
  const entry = useOptionalWorldFocusDanteEntry();
  const prompt = useContextualPrompt(intent);

  if (entry === null) {
    return null;
  }

  const available = isWorldFocusFeatureAvailable(entry.availability);
  const disabled = !available || !entry.canRequestComposer;
  const classes = ['world-focus-dante-contextual-entry', className]
    .filter(Boolean)
    .join(' ');

  const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
    entry.requestComposer({
      invoker: event.currentTarget,
      prompt,
      contextReferences,
    });
  };

  return (
    <button
      className={classes}
      type="button"
      aria-label={t(($) => $.common.worldFocus.dante.contextualAction, {
        prompt,
      })}
      disabled={disabled}
      data-world-focus-dante-contextual-intent={intent}
      onClick={handleClick}
    >
      <span aria-hidden="true" className="world-focus-dante-contextual-mark">
        D
      </span>
      <span>{prompt}</span>
    </button>
  );
}
