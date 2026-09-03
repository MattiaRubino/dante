import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { createWorldFocusTrajectoryPrimitive } from '../../model/world-focus-work-primitives';
import { createWorldFocusDisplayBinding } from './world-focus-display-bindings';
import { WorldFocusTrajectory } from './world-focus-trajectory';

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
    const { container } = render(
      <WorldFocusTrajectory
        primitive={primitive}
        subject={createWorldFocusDisplayBinding({
          reference: primitive.subjectReference,
          label: 'Durata del sonno',
        })}
        points={[
          createWorldFocusDisplayBinding({
            reference: primitive.orderedPointReferences[0],
            label: 'Lunedì',
            supportingText: '7 h 20 min',
          }),
          createWorldFocusDisplayBinding({
            reference: primitive.orderedPointReferences[1],
            label: 'Martedì',
            supportingText: '6 h 55 min',
          }),
        ]}
        missingPositions={[
          createWorldFocusDisplayBinding({
            reference: primitive.missingPositionReferences[0],
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
    const first = createWorldFocusDisplayBinding({
      reference: primitive.orderedPointReferences[0],
      label: 'Lunedì',
    });
    const second = createWorldFocusDisplayBinding({
      reference: primitive.orderedPointReferences[1],
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
