import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../bootstrap/i18n';
import { ObservabilityErrorBoundary } from './error-boundary';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function BrokenSurface(): never {
  throw new Error('Intentional render failure.');
}

describe('ObservabilityErrorBoundary', () => {
  it('renders localized recovery actions and moves focus to the failure title', () => {
    vi.spyOn(globalThis.console, 'error').mockImplementation(() => {
      // React reports the intentional render failure; the assertions prove recovery.
    });

    render(
      <ObservabilityErrorBoundary>
        <BrokenSurface />
      </ObservabilityErrorBoundary>,
    );

    const heading = screen.getByRole('heading', {
      level: 1,
      name: 'Qualcosa non ha funzionato',
    });

    expect(document.activeElement).toBe(heading);
    expect(
      screen.getByRole<HTMLButtonElement>('button', { name: 'Riprova' })
        .disabled,
    ).toBe(false);
    expect(
      screen.getByRole<HTMLButtonElement>('button', {
        name: 'Ricarica pagina',
      }).disabled,
    ).toBe(false);
  });
});
