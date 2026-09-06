import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusComparisonPrimitive } from '../../model/world-focus-work-primitives';
import { createWorldFocusDisplayBinding } from './world-focus-display-bindings';
import { WorldFocusComparison } from './world-focus-comparison';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 Comparison renderer', () => {
  const primitive = createWorldFocusComparisonPrimitive(
    {
      instanceId: 'comparison-1',
      mode: 'planned-actual',
      subjectReferences: [
        { kind: 'plan', key: 'planned-internal' },
        { kind: 'actual', key: 'actual-internal' },
      ],
      basisReference: { kind: 'period', key: 'period-internal' },
    },
    { maxSubjectReferences: 4 },
  );

  const planned = createWorldFocusDisplayBinding({
    reference: primitive.subjectReferences[0],
    label: 'Pianificato',
    supportingText: '3 sessioni',
  });
  const actual = createWorldFocusDisplayBinding({
    reference: primitive.subjectReferences[1],
    label: 'Reale',
    supportingText: '2 sessioni',
  });

  it('preserves semantic subject order without inventing a winner or recommendation', () => {
    const { container } = render(
      <WorldFocusComparison
        primitive={primitive}
        subjects={[planned, actual]}
        basis={createWorldFocusDisplayBinding({
          reference: primitive.basisReference!,
          label: 'Questa settimana',
        })}
      />,
    );

    const subjects = Array.from(
      container.querySelectorAll('[data-world-focus-comparison-subject]'),
    ).map((node) => node.textContent ?? '');

    expect(subjects[0]).toContain('Pianificato');
    expect(subjects[1]).toContain('Reale');
    expect(screen.getByText('Pianificato vs reale')).toBeTruthy();
    expect(screen.getByText('Questa settimana')).toBeTruthy();
    expect(screen.queryByText(/migliore|vincitore|consigliato/i)).toBeNull();
    expect(screen.queryByText('planned-internal')).toBeNull();
  });

  it('fails closed when display bindings reorder the semantic subjects', () => {
    expect(() =>
      render(
        <WorldFocusComparison
          primitive={primitive}
          subjects={[actual, planned]}
          basis={null}
        />,
      ),
    ).toThrow(/order|binding/i);
  });
});
