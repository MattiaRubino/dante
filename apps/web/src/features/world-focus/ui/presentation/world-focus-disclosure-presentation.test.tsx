import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusDisclosureOutcome } from '../../model/world-focus-disclosure';
import { WorldFocusDisclosurePresentation } from './world-focus-disclosure-presentation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 disclosure presentation', () => {
  it('keeps available quiet because it is not a frontend authorization grant', () => {
    const { container } = render(
      <WorldFocusDisclosurePresentation
        disclosure={createWorldFocusDisclosureOutcome({ status: 'available' })}
      />,
    );

    expect(
      container.querySelector('[data-world-focus-disclosure-presentation]'),
    ).toBeNull();
  });

  it('renders restricted and unavailable as distinct sanitized states', () => {
    const { rerender } = render(
      <WorldFocusDisclosurePresentation
        disclosure={createWorldFocusDisclosureOutcome({
          status: 'restricted',
          policy: 'must-not-leak',
          recipient: 'must-not-leak',
        })}
      />,
    );
    expect(screen.getByText('Accesso limitato')).toBeTruthy();
    expect(screen.queryByText('must-not-leak')).toBeNull();

    rerender(
      <WorldFocusDisclosurePresentation
        disclosure={createWorldFocusDisclosureOutcome({ status: 'unavailable' })}
      />,
    );
    expect(screen.getByText('Non disponibile')).toBeTruthy();
  });
});
