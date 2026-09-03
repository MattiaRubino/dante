import { useTranslation } from 'react-i18next';

import type { WorldFocusTrajectoryPrimitive } from '../../model/world-focus-work-primitives';
import {
  assertWorldFocusDisplayBindingMatchesReference,
  type WorldFocusDisplayBinding,
} from './world-focus-display-bindings';
import { WorldFocusPresentationSection } from './world-focus-presentation-primitives';

type WorldFocusTrajectoryProps = Readonly<{
  primitive: WorldFocusTrajectoryPrimitive;
  subject: WorldFocusDisplayBinding;
  points: readonly WorldFocusDisplayBinding[];
  missingPositions: readonly WorldFocusDisplayBinding[];
  orderingBasis: WorldFocusDisplayBinding | null;
  aggregationBasis: WorldFocusDisplayBinding | null;
}>;

function assertOptionalBinding(
  binding: WorldFocusDisplayBinding | null,
  reference: WorldFocusTrajectoryPrimitive['orderingBasisReference'],
  label: string,
): void {
  if (reference === null) {
    if (binding !== null) {
      throw new Error(`${label} binding has no semantic reference`);
    }
    return;
  }
  if (binding === null) {
    throw new Error(`${label} display binding is required`);
  }
  assertWorldFocusDisplayBindingMatchesReference(binding, reference, label);
}

export function WorldFocusTrajectory({
  primitive,
  subject,
  points,
  missingPositions,
  orderingBasis,
  aggregationBasis,
}: WorldFocusTrajectoryProps) {
  const { t } = useTranslation('common');

  assertWorldFocusDisplayBindingMatchesReference(
    subject,
    primitive.subjectReference,
    'World Focus Trajectory subject',
  );

  if (points.length !== primitive.orderedPointReferences.length) {
    throw new Error(
      'World Focus Trajectory display bindings must match semantic point count and order',
    );
  }
  points.forEach((point, index) => {
    const semanticReference = primitive.orderedPointReferences[index];
    if (semanticReference === undefined) {
      throw new Error(
        `World Focus Trajectory semantic point ${index} is unavailable`,
      );
    }
    assertWorldFocusDisplayBindingMatchesReference(
      point,
      semanticReference,
      `World Focus Trajectory point ${index} order`,
    );
  });

  if (missingPositions.length !== primitive.missingPositionReferences.length) {
    throw new Error(
      'World Focus Trajectory missing display bindings must match semantic missing positions',
    );
  }
  missingPositions.forEach((position, index) => {
    const semanticReference = primitive.missingPositionReferences[index];
    if (semanticReference === undefined) {
      throw new Error(
        `World Focus Trajectory missing semantic position ${index} is unavailable`,
      );
    }
    assertWorldFocusDisplayBindingMatchesReference(
      position,
      semanticReference,
      `World Focus Trajectory missing position ${index} order`,
    );
  });

  assertOptionalBinding(
    orderingBasis,
    primitive.orderingBasisReference,
    'World Focus Trajectory ordering basis',
  );
  assertOptionalBinding(
    aggregationBasis,
    primitive.aggregationBasisReference,
    'World Focus Trajectory aggregation basis',
  );

  const axisLabel = t(
    ($) => $.common.worldFocus.presentation.trajectory.axes[primitive.axis],
  );

  return (
    <WorldFocusPresentationSection
      className="world-focus-trajectory"
      title={t(($) => $.common.worldFocus.presentation.trajectory.title)}
      qualification={axisLabel}
      data-world-focus-work-primitive="trajectory"
    >
      <p className="world-focus-presentation-subject">{subject.label}</p>
      {subject.supportingText === undefined ? null : (
        <p className="world-focus-presentation-row-meta">
          {subject.supportingText}
        </p>
      )}

      <ol className="world-focus-trajectory-points">
        {points.map((point) => (
          <li
            className="world-focus-presentation-row world-focus-trajectory-point"
            data-world-focus-trajectory-point="true"
            key={`${point.reference.kind}:${point.reference.key}`}
          >
            <div className="world-focus-presentation-row-copy">
              <p className="world-focus-presentation-row-title">{point.label}</p>
              {point.supportingText === undefined ? null : (
                <p className="world-focus-presentation-row-meta">
                  {point.supportingText}
                </p>
              )}
            </div>
          </li>
        ))}
      </ol>

      {missingPositions.length === 0 ? null : (
        <div className="world-focus-trajectory-missing">
          <p className="world-focus-presentation-subheading">
            {t(($) => $.common.worldFocus.presentation.trajectory.missing)}
          </p>
          <ul className="world-focus-trajectory-missing-list">
            {missingPositions.map((position) => (
              <li key={`${position.reference.kind}:${position.reference.key}`}>
                {position.label}
              </li>
            ))}
          </ul>
        </div>
      )}

      {orderingBasis === null && aggregationBasis === null ? null : (
        <p className="world-focus-presentation-footnote">
          {orderingBasis === null ? null : <span>{orderingBasis.label}</span>}
          {orderingBasis === null || aggregationBasis === null ? null : (
            <span aria-hidden="true"> · </span>
          )}
          {aggregationBasis === null ? null : (
            <span>{aggregationBasis.label}</span>
          )}
        </p>
      )}
    </WorldFocusPresentationSection>
  );
}
