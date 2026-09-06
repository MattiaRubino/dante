import { beforeEach, describe, expect, it, vi } from 'vitest';

beforeEach(() => {
  vi.resetModules();
});

describe('browser telemetry bridge', () => {
  it('buffers only the latest normalized route until the lazy adapter is ready', async () => {
    const bridge = await import('./bridge');
    const observeResolvedRoute = vi.fn();

    bridge.beginWebTelemetryInitialization();
    bridge.observeResolvedRoute('/access');
    bridge.observeResolvedRoute('/access');
    bridge.observeResolvedRoute('/today');
    bridge.installWebTelemetryAdapter({
      observeResolvedRoute,
      observeRenderFailure: vi.fn(),
    });

    expect(observeResolvedRoute).toHaveBeenCalledTimes(1);
    expect(observeResolvedRoute).toHaveBeenCalledWith('/today');
  });

  it('does not retain routes while browser telemetry is disabled', async () => {
    const bridge = await import('./bridge');
    const observeResolvedRoute = vi.fn();

    bridge.observeResolvedRoute('/access');
    bridge.installWebTelemetryAdapter({
      observeResolvedRoute,
      observeRenderFailure: vi.fn(),
    });

    expect(observeResolvedRoute).not.toHaveBeenCalled();
  });

  it('bounds invalid route identifiers and isolates adapter failures', async () => {
    const bridge = await import('./bridge');
    const observeResolvedRoute = vi.fn(() => {
      throw new Error('collector unavailable');
    });
    const observeRenderFailure = vi.fn(() => {
      throw new Error('collector unavailable');
    });
    bridge.installWebTelemetryAdapter({
      observeResolvedRoute,
      observeRenderFailure,
    });

    expect(() => bridge.observeResolvedRoute('private-route')).not.toThrow();
    expect(() =>
      bridge.observeRenderFailure(new Error('render failure')),
    ).not.toThrow();
    expect(observeResolvedRoute).toHaveBeenCalledWith('unknown');
    expect(observeRenderFailure).toHaveBeenCalledTimes(1);
  });
});
