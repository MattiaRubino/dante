import { useTranslation } from 'react-i18next';

import type { WorldFocusAttentionPrimitive } from '../../model/world-focus-work-primitives';
import {
  assertWorldFocusDisplayBindingMatchesReference,
  type WorldFocusDisplayBinding,
} from './world-focus-display-bindings';
import {
  WorldFocusPresentationSection,
  WorldFocusPresentationState,
} from './world-focus-presentation-primitives';

type WorldFocusAttentionProps = Readonly<{
  primitive: WorldFocusAttentionPrimitive;
  matter: WorldFocusDisplayBinding;
  resolution: WorldFocusDisplayBinding | null;
  reasonText: string;
}>;

function normalizeReasonText(value: string): string {
  const normalized = value.trim();
  if (normalized.length === 0) {
    throw new Error('World Focus Attention reason text must not be empty');
  }
  return normalized;
}

export function WorldFocusAttention({
  primitive,
  matter,
  resolution,
  reasonText,
}: WorldFocusAttentionProps) {
  const { t } = useTranslation('common');
  assertWorldFocusDisplayBindingMatchesReference(
    matter,
    primitive.matterReference,
    'World Focus Attention matter',
  );

  if (primitive.resolutionReference === null) {
    if (resolution !== null) {
      throw new Error(
        'World Focus Attention resolution binding has no semantic reference',
      );
    }
  } else {
    if (resolution === null) {
      throw new Error('World Focus Attention resolution display binding is required');
    }
    assertWorldFocusDisplayBindingMatchesReference(
      resolution,
      primitive.resolutionReference,
      'World Focus Attention resolution',
    );
  }

  const stateLabel = t(
    ($) => $.common.worldFocus.presentation.attention.states[primitive.state],
  );

  return (
    <WorldFocusPresentationSection
      className="world-focus-attention"
      title={t(($) => $.common.worldFocus.presentation.attention.title)}
      data-world-focus-work-primitive="attention"
    >
      <div className="world-focus-presentation-row world-focus-attention-row">
        <div className="world-focus-presentation-row-copy">
          <p className="world-focus-presentation-row-title">{matter.label}</p>
          {matter.supportingText === undefined ? null : (
            <p className="world-focus-presentation-row-meta">
              {matter.supportingText}
            </p>
          )}
          <p className="world-focus-presentation-row-supporting">
            {normalizeReasonText(reasonText)}
          </p>
          {resolution === null ? null : (
            <p className="world-focus-presentation-row-meta">
              <span>
                {t(($) => $.common.worldFocus.presentation.attention.resolution)}
              </span>{' '}
              <span>{resolution.label}</span>
            </p>
          )}
        </div>
        <WorldFocusPresentationState state={primitive.state}>
          {stateLabel}
        </WorldFocusPresentationState>
      </div>
    </WorldFocusPresentationSection>
  );
}
