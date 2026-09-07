import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import {
  TemporalCreateContextCatalogProvider,
  temporalCreateLocalContextAuthoringEnabled,
  useTemporalCreateContextCreator,
} from './temporal-create-context-catalog';

function Probe() {
  const creator = useTemporalCreateContextCreator();
  return <output data-testid="creator-state">{creator ? 'available' : 'absent'}</output>;
}

describe('Temporal Create context catalog runtime boundary', () => {
  it('allows local context authoring only in explicit test mode', () => {
    expect(temporalCreateLocalContextAuthoringEnabled('test')).toBe(true);
    expect(temporalCreateLocalContextAuthoringEnabled('development')).toBe(
      false,
    );
    expect(temporalCreateLocalContextAuthoringEnabled('production')).toBe(false);
  });

  it('does not expose the local context creator in production runtime', () => {
    const creator = vi.fn(() => ({
      id: 'local-context:test',
      label: 'Test',
      tone: 'focus' as const,
      local: true,
    }));

    render(
      <TemporalCreateContextCatalogProvider
        mode="production"
        onCreateContext={creator}
      >
        <Probe />
      </TemporalCreateContextCatalogProvider>,
    );

    expect(screen.getByTestId('creator-state')).toHaveTextContent('absent');
    expect(creator).not.toHaveBeenCalled();
  });

  it('retains the local creator for explicit test-mode C1 regressions', () => {
    const creator = vi.fn(() => ({
      id: 'local-context:test',
      label: 'Test',
      tone: 'focus' as const,
      local: true,
    }));

    render(
      <TemporalCreateContextCatalogProvider mode="test" onCreateContext={creator}>
        <Probe />
      </TemporalCreateContextCatalogProvider>,
    );

    expect(screen.getByTestId('creator-state')).toHaveTextContent('available');
  });
});
