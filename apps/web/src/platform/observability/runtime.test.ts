import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const { initializeFaroRuntime } = vi.hoisted(() => ({
  initializeFaroRuntime: vi.fn(),
}));

vi.mock('./runtime', () => ({ initializeFaroRuntime }));

const ENABLED_SOURCE = {
  VITE_DANTE_OBSERVABILITY_ENABLED: 'true',
  VITE_DANTE_FARO_COLLECTOR_URL: 'https://telemetry.example.test/collect',
} as const;

beforeEach(() => {
  vi.resetModules();
  initializeFaroRuntime.mockReset();
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe('browser observability runtime', () => {
  it('does not load the vendor runtime while telemetry is disabled', async () => {
    const { initializeWebObservability } = await import('./initialize');

    await initializeWebObservability({});

    expect(initializeFaroRuntime).not.toHaveBeenCalled();
  });

  it('initializes the vendor runtime exactly once under concurrent startup', async () => {
    const { initializeWebObservability } = await import('./initialize');

    await Promise.all([
      initializeWebObservability(ENABLED_SOURCE),
      initializeWebObservability(ENABLED_SOURCE),
    ]);

    expect(initializeFaroRuntime).toHaveBeenCalledTimes(1);
    expect(initializeFaroRuntime).toHaveBeenCalledWith(
      expect.objectContaining({
        collectorUrl: ENABLED_SOURCE.VITE_DANTE_FARO_COLLECTOR_URL,
        enabled: true,
      }),
    );
  });

  it('honors Global Privacy Control before initializing the vendor runtime', async () => {
    vi.stubGlobal('navigator', { globalPrivacyControl: true });
    const { initializeWebObservability } = await import('./initialize');

    await initializeWebObservability(ENABLED_SOURCE);

    expect(initializeFaroRuntime).not.toHaveBeenCalled();
  });

  it('fails closed without exposing rejected configuration values', async () => {
    const warn = vi.spyOn(globalThis.console, 'warn').mockImplementation(() => {
      // The assertion below verifies the bounded public diagnostic.
    });
    const { initializeWebObservability } = await import('./initialize');

    await initializeWebObservability({
      VITE_DANTE_OBSERVABILITY_ENABLED: 'true',
      VITE_DANTE_FARO_COLLECTOR_URL:
        'https://telemetry.example.test/collect?token=do-not-log-me',
    });

    expect(warn).toHaveBeenCalledWith(
      'WebObservabilityConfigurationError: browser telemetry is disabled.',
    );
    expect(JSON.stringify(warn.mock.calls)).not.toContain('do-not-log-me');
  });

  it('isolates a vendor initialization failure from application startup', async () => {
    initializeFaroRuntime.mockImplementationOnce(() => {
      throw new Error('private vendor failure details');
    });
    const warn = vi.spyOn(globalThis.console, 'warn').mockImplementation(() => {
      // The assertion below verifies the bounded public diagnostic.
    });
    const { initializeWebObservability } = await import('./initialize');

    await expect(
      initializeWebObservability(ENABLED_SOURCE),
    ).resolves.toBeUndefined();
    expect(warn).toHaveBeenCalledWith(
      'WebObservabilityInitializationError: browser telemetry is disabled.',
    );
    expect(JSON.stringify(warn.mock.calls)).not.toContain(
      'private vendor failure details',
    );
  });
});
