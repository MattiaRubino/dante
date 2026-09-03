import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusTrajectoryPrimitive } from '../../model/world-focus-work-primitives';
import { createWorldFocusDisplayBinding } from './world-focus-display-bindings';
import { WorldFocusTrajectory } from './world-focus-trajectory';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 Trajectory renderer', () => {
  const primitive = createWorldFocusTrajectoryPrimitive(
    {
      instanceId: 'trajectory-1',
      subjectReference: { kind: 'metric', key: 'sleep-internal' },
      axis: 'time',
      orderedPointReferences: [
        { kind: 'observation', key: 'day-1-internal' },
        { kind: 'observation', key: 'day-2-internal' },
      ],
      missingPositionReferences: [
        { kind: 'observation-slot', key: 'day-3-missing-internal' },
      ],
      orderingBasisReference: { kind: 'window', key: 'week-internal' },
      aggregationBasisReference: null,
    },
    { maxOrderedPointReferences: 6, maxMissingPositionReferences: 6 },
  );

  it('renders the ordered known sequence and missingness as separate semantics rather than a fake chart or zero', () => {
    const firstPointReference = primitive.orderedPointReferences[0];
    const secondPointReference = primitive.orderedPointReferences[1];
    const missingPositionReference = primitive.missingPositionReferences[0];
    if (
      firstPointReference === undefined ||
      secondPointReference === undefined ||
      missingPositionReference === undefined
    ) {
      throw new Error('Expected bounded Trajectory fixture references');
    }

    const { container } = render(
      <WorldFocusTrajectory
        primitive={primitive}
        subject={createWorldFocusDisplayBinding({
          reference: primitive.subjectReference,
          label: 'Durata del sonno',
        })}
        points={[
          createWorldFocusDisplayBinding({
            reference: firstPointReference,
            label: 'Lunedì',
            supportingText: '7 h 20 min',
          }),
          createWorldFocusDisplayBinding({
            reference: secondPointReference,
            label: 'Martedì',
            supportingText: '6 h 55 min',
          }),
        ]}
        missingPositions={[
          createWorldFocusDisplayBinding({
            reference: missingPositionReference,
            label: 'Mercoledì',
          }),
        ]}
        orderingBasis={createWorldFocusDisplayBinding({
          reference: primitive.orderingBasisReference!,
          label: 'Settimana corrente',
        })}
        aggregationBasis={null}
      />,
    );

    const points = Array.from(
      container.querySelectorAll('[data-world-focus-trajectory-point]'),
    ).map((node) => node.textContent ?? '');
    expect(points[0]).toContain('Lunedì');
    expect(points[1]).toContain('Martedì');
    expect(screen.getByText('Dati mancanti')).toBeTruthy();
    expect(screen.getByText('Mercoledì')).toBeTruthy();
    expect(screen.queryByText('0')).toBeNull();
    expect(container.querySelector('canvas')).toBeNull();
    expect(container.querySelector('svg')).toBeNull();
    expect(screen.queryByText('day-3-missing-internal')).toBeNull();
  });

  it('fails closed if a point binding order no longer matches the semantic trajectory order', () => {
    const firstPointReference = primitive.orderedPointReferences[0];
    const secondPointReference = primitive.orderedPointReferences[1];
    if (firstPointReference === undefined || secondPointReference === undefined) {
      throw new Error('Expected bounded Trajectory fixture references');
    }

    const first = createWorldFocusDisplayBinding({
      reference: firstPointReference,
      label: 'Lunedì',
    });
    const second = createWorldFocusDisplayBinding({
      reference: secondPointReference,
      label: 'Martedì',
    });

    expect(() =>
      render(
        <WorldFocusTrajectory
          primitive={primitive}
          subject={createWorldFocusDisplayBinding({
            reference: primitive.subjectReference,
            label: 'Durata del sonno',
          })}
          points={[second, first]}
          missingPositions={[]}
          orderingBasis={null}
          aggregationBasis={null}
        />,
      ),
    ).toThrow(/order|binding/i);
  });
});
