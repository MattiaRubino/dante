import { describe, expect, it, vi } from 'vitest';

const faroMocks = vi.hoisted(() => ({
  addBeforeSendHooks: vi.fn(),
  defaultMetas: [vi.fn()],
  initializeFaro: vi.fn(),
  removeMeta: vi.fn(),
  pushError: vi.fn(),
  pushEvent: vi.fn(),
}));

vi.mock('@grafana/faro-web-sdk', () => {
  class FakeInstrumentation {}

  return {
    CSPInstrumentation: FakeInstrumentation,
    ErrorsInstrumentation: FakeInstrumentation,
    InternalLoggerLevel: { ERROR: 'error' },
    NavigationInstrumentation: FakeInstrumentation,
    SessionInstrumentation: FakeInstrumentation,
    ViewInstrumentation: FakeInstrumentation,
    WebVitalsInstrumentation: FakeInstrumentation,
    initializeFaro: faroMocks.initializeFaro,
  };
});

vi.mock('@grafana/faro-react', () => ({
  ReactIntegration: class ReactIntegration {},
}));

vi.mock('@grafana/faro-web-tracing', () => ({
  TracingInstrumentation: class TracingInstrumentation {},
}));

describe('Faro vendor runtime', () => {
  it('initializes with the governed privacy and delivery envelope', async () => {
    faroMocks.initializeFaro.mockReturnValue({
      api: {
        pushError: faroMocks.pushError,
        pushEvent: faroMocks.pushEvent,
      },
      transports: {
        addBeforeSendHooks: faroMocks.addBeforeSendHooks,
      },
      metas: {
        remove: faroMocks.removeMeta,
      },
      config: {
        metas: faroMocks.defaultMetas,
      },
    });
    const { initializeFaroRuntime } = await import('./runtime');
    const bridge = await import('./bridge');

    initializeFaroRuntime({
      enabled: true,
      environment: 'prod',
      releaseSha: '0123456789abcdef',
      buildId: 'web-20260830.1',
      collectorUrl: 'https://telemetry.example.test/collect',
      sessionSampleRate: 0.1,
      respectGlobalPrivacyControl: true,
    });

    expect(faroMocks.initializeFaro).toHaveBeenCalledWith(
      expect.objectContaining({
        batching: {
          enabled: true,
          itemLimit: 20,
          sendTimeout: 1_000,
        },
        preventGlobalExposure: true,
        sessionTracking: {
          enabled: true,
          persistent: false,
          samplingRate: 0.1,
        },
        trackGeolocation: false,
        trackResources: false,
        webVitalsInstrumentation: {
          reportAllChanges: false,
          trackAttributionSources: false,
        },
      }),
    );
    expect(faroMocks.initializeFaro.mock.calls[0]?.[0]).not.toHaveProperty(
      'experimental',
    );
    expect(faroMocks.addBeforeSendHooks).toHaveBeenCalledTimes(1);
    expect(faroMocks.removeMeta).toHaveBeenCalledWith(
      ...faroMocks.defaultMetas,
    );
    expect(faroMocks.removeMeta.mock.invocationCallOrder[0]).toBeLessThan(
      faroMocks.addBeforeSendHooks.mock.invocationCallOrder[0] ?? 0,
    );

    bridge.observeResolvedRoute('/access');
    bridge.observeRenderFailure(
      new Error('Render failed for private@example.test'),
    );

    expect(faroMocks.pushEvent).toHaveBeenCalledWith('dante.route.resolved', {
      route_id: '/access',
    });
    const reportedError = faroMocks.pushError.mock.calls[0]?.[0] as Error;
    expect(reportedError.name).toBe('ReactRenderError');
    expect(reportedError.message).not.toContain('private@example.test');
  });
});
