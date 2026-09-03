import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusEffectPresentation } from '../../model/world-focus-effect';
import { WorldFocusEffectStatus } from './world-focus-effect-presentation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 effect presentation', () => {
  it('renders partial-real and execution revalidation as orthogonal visible states', () => {
    render(
      <WorldFocusEffectStatus
        effect={createWorldFocusEffectPresentation({
          state: 'partial-real',
          executionRevalidation: 'required-before-execution',
          providerAck: true,
          receipt: 'must-not-leak',
        })}
      />,
    );

    expect(screen.getByText('Effetto parzialmente reale')).toBeTruthy();
    expect(screen.getByText('Ricontrollo richiesto prima di eseguire')).toBeTruthy();
    expect(screen.queryByText('must-not-leak')).toBeNull();
  });

  it('does not collapse reversed into compensated', () => {
    const { rerender } = render(
      <WorldFocusEffectStatus
        effect={createWorldFocusEffectPresentation({
          state: 'reversed',
          executionRevalidation: 'not-required',
        })}
      />,
    );
    expect(screen.getByText('Reverso')).toBeTruthy();

    rerender(
      <WorldFocusEffectStatus
        effect={createWorldFocusEffectPresentation({
          state: 'compensated',
          executionRevalidation: 'not-required',
        })}
      />,
    );
    expect(screen.getByText('Compensato')).toBeTruthy();
  });
});
