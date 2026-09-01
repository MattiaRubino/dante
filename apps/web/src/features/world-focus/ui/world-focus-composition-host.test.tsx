import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { defineWorldFocusComposition } from '../model/world-focus-composition';
import {
  WorldFocusCompositionHost,
  type WorldFocusCompositionRegistration,
} from './world-focus-composition-host';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

describe('WorldFocusCompositionHost', () => {
  it('renders resolved composition through finite registrations and exposes ownership axes', () => {
    const entries = defineWorldFocusComposition([
      {
        instanceId: 'continuity',
        kind: 'continuity',
        ownership: {
          stability: 'adaptive',
          origin: 'application-derived',
        },
      },
    ]);
    const registry = new WorldFocusModuleRegistry<WorldFocusCompositionRegistration>([
      {
        kind: 'continuity',
        render: ({ worldId }) => <p>Continuity for {worldId}</p>,
      },
    ]);

    const { container } = render(
      <WorldFocusCompositionHost
        worldId="music"
        entries={entries}
        registry={registry}
      />,
    );

    expect(screen.getByText('Continuity for music')).toBeTruthy();
    const item = container.querySelector('[data-world-focus-composition-id="continuity"]');
    expect(item?.getAttribute('data-world-focus-stability')).toBe('adaptive');
    expect(item?.getAttribute('data-world-focus-origin')).toBe(
      'application-derived',
    );
  });

  it('degrades an unknown future renderer locally instead of inventing UI', () => {
    const entries = defineWorldFocusComposition([
      {
        instanceId: 'future',
        kind: 'future-specialist',
        ownership: { stability: 'ephemeral', origin: 'dante-proposed' },
      },
    ]);
    const registry = new WorldFocusModuleRegistry<WorldFocusCompositionRegistration>(
      [],
    );

    const { container } = render(
      <WorldFocusCompositionHost
        worldId="travel"
        entries={entries}
        registry={registry}
      />,
    );

    expect(screen.getByText('Questo contenuto non è disponibile.')).toBeTruthy();
    expect(
      container
        .querySelector('[data-world-focus-composition-id="future"]')
        ?.getAttribute('data-world-focus-module-status'),
    ).toBe('unsupported');
  });
});
