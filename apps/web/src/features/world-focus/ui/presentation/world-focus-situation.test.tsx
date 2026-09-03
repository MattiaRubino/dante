import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusSituationProjection } from '../../model/world-focus-direct-projections';
import { createWorldFocusDisplayBindingSet } from './world-focus-display-bindings';
import { WorldFocusSituation } from './world-focus-situation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 Situation renderer', () => {
  const projection = createWorldFocusSituationProjection({
    worldId: 'future-world',
    orderedSituationReferences: [
      { kind: 'release', key: 'internal-release' },
      { kind: 'material-state', key: 'internal-master' },
    ],
  });

  it('renders in semantic order even when display bindings arrive in another order', () => {
    const bindings = createWorldFocusDisplayBindingSet([
      {
        reference: projection.orderedSituationReferences[1]!,
        label: 'Master approvato',
      },
      {
        reference: projection.orderedSituationReferences[0]!,
        label: 'Uscita Neon Static',
      },
    ]);

    render(<WorldFocusSituation projection={projection} bindings={bindings} />);

    expect(screen.getAllByRole('listitem').map((item) => item.textContent)).toEqual([
      'Uscita Neon Static',
      'Master approvato',
    ]);
    expect(screen.queryByText('internal-release')).toBeNull();
  });

  it('fails closed when a semantic reference has no display binding', () => {
    expect(() =>
      render(
        <WorldFocusSituation
          projection={projection}
          bindings={createWorldFocusDisplayBindingSet([
            {
              reference: projection.orderedSituationReferences[0]!,
              label: 'Solo una voce',
            },
          ])}
        />,
      ),
    ).toThrow(/binding/i);
  });
});
