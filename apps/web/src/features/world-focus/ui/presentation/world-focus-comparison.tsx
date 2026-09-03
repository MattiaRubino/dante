import { useTranslation } from 'react-i18next';

import type { WorldFocusComparisonPrimitive } from '../../model/world-focus-work-primitives';
import {
  assertWorldFocusDisplayBindingMatchesReference,
  type WorldFocusDisplayBinding,
} from './world-focus-display-bindings';
import { WorldFocusPresentationSection } from './world-focus-presentation-primitives';

type WorldFocusComparisonProps = Readonly<{
  primitive: WorldFocusComparisonPrimitive;
  subjects: readonly WorldFocusDisplayBinding[];
  basis: WorldFocusDisplayBinding | null;
}>;

export function WorldFocusComparison({
  primitive,
  subjects,
  basis,
}: WorldFocusComparisonProps) {
  const { t } = useTranslation('common');

  if (subjects.length !== primitive.subjectReferences.length) {
    throw new Error(
      'World Focus Comparison display bindings must match semantic subject count',
    );
  }
  subjects.forEach((subject, index) => {
    const semanticReference = primitive.subjectReferences[index];
    if (semanticReference === undefined) {
      throw new Error(
        `World Focus Comparison semantic subject ${index} is unavailable`,
      );
    }
    assertWorldFocusDisplayBindingMatchesReference(
      subject,
      semanticReference,
      `World Focus Comparison subject ${index}`,
    );
  });

  if (primitive.basisReference === null) {
    if (basis !== null) {
      throw new Error(
        'World Focus Comparison basis binding has no semantic reference',
      );
    }
  } else {
    if (basis === null) {
      throw new Error('World Focus Comparison basis display binding is required');
    }
    assertWorldFocusDisplayBindingMatchesReference(
      basis,
      primitive.basisReference,
      'World Focus Comparison basis',
    );
  }

  const modeLabel = t(
    ($) => $.common.worldFocus.presentation.comparison.modes[primitive.mode],
  );

  return (
    <WorldFocusPresentationSection
      className="world-focus-comparison"
      title={t(($) => $.common.worldFocus.presentation.comparison.title)}
      qualification={modeLabel}
      data-world-focus-work-primitive="comparison"
    >
      <ol className="world-focus-comparison-subjects">
        {subjects.map((subject) => (
          <li
            className="world-focus-presentation-row world-focus-comparison-subject"
            data-world-focus-comparison-subject="true"
            key={`${subject.reference.kind}:${subject.reference.key}`}
          >
            <div className="world-focus-presentation-row-copy">
              <p className="world-focus-presentation-row-title">{subject.label}</p>
              {subject.supportingText === undefined ? null : (
                <p className="world-focus-presentation-row-meta">
                  {subject.supportingText}
                </p>
              )}
            </div>
          </li>
        ))}
      </ol>
      {basis === null ? null : (
        <p className="world-focus-presentation-footnote">
          <span>{t(($) => $.common.worldFocus.presentation.comparison.basis)}</span>{' '}
          <span>{basis.label}</span>
        </p>
      )}
    </WorldFocusPresentationSection>
  );
}
