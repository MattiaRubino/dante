import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusNextProjection } from '../../model/world-focus-direct-projections';
import { createWorldFocusDisplayBindingSet } from './world-focus-display-bindings';
import { WorldFocusNext } from './world-focus-next';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 Next renderer', () => {
  const projection = createWorldFocusNextProjection({
    worldId: 'future-world',
    orderedNextReferences: [
      { kind: 'schedule', key: 'internal-release-schedule' },
      { kind: 'dependency', key: 'internal-artwork-dependency' },
    ],
  });

  it('preserves semantic order and never falls back to internal reference keys', () => {
    render(
      <WorldFocusNext
        projection={projection}
        bindings={createWorldFocusDisplayBindingSet([
          {
            reference: projection.orderedNextReferences[1]!,
            label: 'Approvazione copertina',
          },
          {
            reference: projection.orderedNextReferences[0]!,
            label: 'Programma uscita',
          },
        ])}
      />,
    );

    expect(screen.getAllByRole('listitem').map((item) => item.textContent)).toEqual([
      'Programma uscita',
      'Approvazione copertina',
    ]);
    expect(screen.queryByText('internal-release-schedule')).toBeNull();
  });
});
