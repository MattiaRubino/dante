import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { resolveWorldFocusCompositionPlan } from '../model/world-focus-composition-plan';
import {
  WorldFocusCompositionHost,
  type WorldFocusCompositionRegistration,
} from './world-focus-composition-host';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

const TEST_POLICY = Object.freeze({
  maxAdaptiveEntries: 4,
  maxEphemeralEntries: 2,
});

describe('WorldFocusCompositionHost', () => {
  it('renders resolved composition through finite registrations and exposes ownership/layout axes', () => {
    const plan = resolveWorldFocusCompositionPlan(
      [
        {
          instanceId: 'continuity',
          kind: 'continuity',
          ownership: {
            stability: 'adaptive',
            origin: 'application-derived',
          },
          prominence: 'primary',
          footprint: 'standard',
          order: 0,
        },
      ],
      TEST_POLICY,
    );
    const registry = new WorldFocusModuleRegistry<WorldFocusCompositionRegistration>([
      {
        kind: 'continuity',
        render: ({ worldId }) => <p>Continuity for {worldId}</p>,
      },
    ]);

    const { container } = render(
      <WorldFocusCompositionHost
        worldId="music"
        entries={plan.entries}
        registry={registry}
      />,
    );

    expect(screen.getByText('Continuity for music')).toBeTruthy();
    const item = container.querySelector(
      '[data-world-focus-composition-id="continuity"]',
    );
    expect(item?.getAttribute('data-world-focus-stability')).toBe('adaptive');
    expect(item?.getAttribute('data-world-focus-origin')).toBe(
      'application-derived',
    );
    expect(item?.getAttribute('data-world-focus-prominence')).toBe('primary');
    expect(item?.getAttribute('data-world-focus-footprint')).toBe('standard');
    expect(item?.getAttribute('data-world-focus-grid-span')).toBe('12');
    expect(item?.getAttribute('data-world-focus-grid-row')).toBe('0');
  });

  it('degrades an unknown future renderer locally instead of inventing UI', () => {
    const plan = resolveWorldFocusCompositionPlan(
      [
        {
          instanceId: 'future',
          kind: 'future-specialist',
          ownership: { stability: 'ephemeral', origin: 'dante-proposed' },
          prominence: 'primary',
          footprint: 'wide',
          order: 0,
        },
      ],
      TEST_POLICY,
    );
    const registry = new WorldFocusModuleRegistry<WorldFocusCompositionRegistration>(
      [],
    );

    const { container } = render(
      <WorldFocusCompositionHost
        worldId="travel"
        entries={plan.entries}
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
