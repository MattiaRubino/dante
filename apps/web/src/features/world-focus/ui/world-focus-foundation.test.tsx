import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { WorldFocusRenderBoundary } from './world-focus-render-boundary';
import { WorldFocusRouteError } from './world-focus-route-error';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe('World Focus B0 UI foundation', () => {
  it('isolates a render failure without exposing raw error text in fallback UI', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined);
    const onError = vi.fn();
    let shouldThrow = true;

    function MaybeBroken() {
      if (shouldThrow) {
        throw new Error('sensitive-render-detail');
      }
      return <p>Recovered</p>;
    }

    render(
      <WorldFocusRenderBoundary
        resetKey="music"
        onError={onError}
        fallback={({ reset }) => (
          <button type="button" onClick={reset}>
            Riprova modulo
          </button>
        )}
      >
        <MaybeBroken />
      </WorldFocusRenderBoundary>,
    );

    expect(screen.queryByText('sensitive-render-detail')).toBeNull();
    expect(onError).toHaveBeenCalledTimes(1);

    shouldThrow = false;
    fireEvent.click(screen.getByRole('button', { name: 'Riprova modulo' }));
    expect(screen.getByText('Recovered')).toBeTruthy();
    expect(consoleError).toHaveBeenCalled();
  });

  it('renders a localized route failure and retries without echoing raw errors', () => {
    const reset = vi.fn();

    render(
      <WorldFocusRouteError
        error={new Error('private-route-detail')}
        reset={reset}
      />,
    );

    expect(
      screen.getByRole('heading', { name: 'Impossibile aprire questo Mondo' }),
    ).toBeTruthy();
    expect(screen.queryByText('private-route-detail')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));
    expect(reset).toHaveBeenCalledTimes(1);
  });
});
