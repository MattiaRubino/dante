import { afterEach, describe, expect, it, vi } from 'vitest';

import { initializeWebObservability } from './runtime';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('browser observability runtime', () => {
  it('fails closed without exposing rejected configuration values', () => {
    const warn = vi.spyOn(globalThis.console, 'warn').mockImplementation(() => {
      // The assertion below verifies the bounded public diagnostic.
    });

    const result = initializeWebObservability({
      VITE_DANTE_OBSERVABILITY_ENABLED: 'true',
      VITE_DANTE_FARO_COLLECTOR_URL:
        'https://telemetry.example.test/collect?token=do-not-log-me',
    });

    expect(result).toBeUndefined();
    expect(warn).toHaveBeenCalledWith(
      'WebObservabilityConfigurationError: browser telemetry is disabled.',
    );
    expect(JSON.stringify(warn.mock.calls)).not.toContain('do-not-log-me');
  });
});
