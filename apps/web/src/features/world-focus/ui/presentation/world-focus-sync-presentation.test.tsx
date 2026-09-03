import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusSyncPresentation } from '../../model/world-focus-sync';
import { WorldFocusSyncStatus } from './world-focus-sync-presentation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 sync presentation', () => {
  it('stays quiet when all platform axes are nominal', () => {
    const { container } = render(
      <WorldFocusSyncStatus
        sync={createWorldFocusSyncPresentation({
          connectivity: 'online',
          replay: 'idle',
          providerDelivery: 'nominal',
          requestTiming: 'within-window',
        })}
      />,
    );

    expect(container.querySelector('[data-world-focus-sync-presentation]')).toBeNull();
  });

  it('renders degraded platform axes independently without turning them into content truth', () => {
    render(
      <WorldFocusSyncStatus
        sync={createWorldFocusSyncPresentation({
          connectivity: 'offline',
          replay: 'pending',
          providerDelivery: 'lagging',
          requestTiming: 'timed-out',
        })}
      />,
    );

    expect(screen.getByText('Offline')).toBeTruthy();
    expect(screen.getByText('Riproduzione in attesa')).toBeTruthy();
    expect(screen.getByText('Consegna in ritardo')).toBeTruthy();
    expect(screen.getByText('Richiesta scaduta')).toBeTruthy();
    expect(screen.queryByText(/contenuto non disponibile/i)).toBeNull();
  });
});
