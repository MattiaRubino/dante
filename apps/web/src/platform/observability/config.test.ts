import { describe, expect, it } from 'vitest';

import {
  readWebObservabilityConfig,
  WebObservabilityConfigurationError,
} from './config';

describe('web observability configuration', () => {
  it('stays disabled without requiring a collector', () => {
    const config = readWebObservabilityConfig({});

    expect(config).toEqual({
      enabled: false,
      environment: 'local',
      releaseSha: 'local',
      buildId: 'local',
      sessionSampleRate: 0.1,
    });
  });

  it('accepts an identified HTTPS production collector', () => {
    const config = readWebObservabilityConfig({
      VITE_DANTE_OBSERVABILITY_ENABLED: 'true',
      VITE_DANTE_ENV: 'prod',
      VITE_DANTE_RELEASE_SHA: '0123456789abcdef',
      VITE_DANTE_BUILD_ID: 'web-20260829.1',
      VITE_DANTE_FARO_COLLECTOR_URL: 'https://faro.example.test/collect',
      VITE_DANTE_FARO_SESSION_SAMPLE_RATE: '0.25',
    });

    expect(config).toMatchObject({
      enabled: true,
      environment: 'prod',
      releaseSha: '0123456789abcdef',
      buildId: 'web-20260829.1',
      collectorUrl: 'https://faro.example.test/collect',
      sessionSampleRate: 0.25,
    });
  });

  it.each([
    'http://telemetry.example.test/collect',
    'https://user:secret@telemetry.example.test/collect',
    'https://telemetry.example.test/collect?token=secret',
    'https://telemetry.example.test/collect#secret',
  ])('rejects an unsafe collector URL: %s', (collectorUrl) => {
    expect(() =>
      readWebObservabilityConfig({
        VITE_DANTE_OBSERVABILITY_ENABLED: 'true',
        VITE_DANTE_FARO_COLLECTOR_URL: collectorUrl,
      }),
    ).toThrow(WebObservabilityConfigurationError);
  });

  it('requires deployment identities outside local development', () => {
    expect(() =>
      readWebObservabilityConfig({
        VITE_DANTE_ENV: 'uat',
      }),
    ).toThrow(
      'Non-local observability requires real release and build identities.',
    );
  });

  it.each(['-0.01', '1.01', 'not-a-number'])(
    'rejects an invalid sample rate: %s',
    (sampleRate) => {
      expect(() =>
        readWebObservabilityConfig({
          VITE_DANTE_FARO_SESSION_SAMPLE_RATE: sampleRate,
        }),
      ).toThrow(WebObservabilityConfigurationError);
    },
  );
});
