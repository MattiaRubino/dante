import {
  CSPInstrumentation,
  ErrorsInstrumentation,
  InternalLoggerLevel,
  NavigationInstrumentation,
  SessionInstrumentation,
  ViewInstrumentation,
  WebVitalsInstrumentation,
  initializeFaro,
  type Faro,
} from '@grafana/faro-web-sdk';
import { ReactIntegration } from '@grafana/faro-react';
import { TracingInstrumentation } from '@grafana/faro-web-tracing';

import { installWebTelemetryAdapter } from './bridge';
import type { WebObservabilityConfig } from './config';
import { sanitizeText, sanitizeTransportItem } from './sanitize';

let webObservability: Faro | undefined;

function escapeRegularExpression(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function instrumentations(): NonNullable<
  Parameters<typeof initializeFaro>[0]['instrumentations']
> {
  const apiOriginPattern = new RegExp(
    `^${escapeRegularExpression(globalThis.location.origin)}/api/`,
  );
  return [
    new ErrorsInstrumentation(),
    new WebVitalsInstrumentation(),
    new SessionInstrumentation(),
    new ViewInstrumentation(),
    new NavigationInstrumentation(),
    new CSPInstrumentation(),
    new ReactIntegration(),
    new TracingInstrumentation({
      omitTraceContextForUnsampledSessions: true,
      instrumentationOptions: {
        propagateTraceHeaderCorsUrls: [apiOriginPattern],
      },
      resourceAttributes: {
        'service.name': 'dante-web',
      },
    }),
  ];
}

export function initializeFaroRuntime(config: WebObservabilityConfig): void {
  if (webObservability !== undefined) {
    return;
  }

  if (!config.enabled || config.collectorUrl === undefined) {
    return;
  }

  const faro = initializeFaro({
    url: config.collectorUrl,
    app: {
      name: 'dante-web',
      version: config.releaseSha,
      gitHash: config.releaseSha,
      release: config.buildId,
      environment: config.environment,
    },
    batching: {
      enabled: true,
      itemLimit: 20,
      sendTimeout: 1_000,
    },
    instrumentations: instrumentations(),
    internalLoggerLevel: InternalLoggerLevel.ERROR,
    preventGlobalExposure: true,
    sessionTracking: {
      enabled: true,
      persistent: false,
      samplingRate: config.sessionSampleRate,
    },
    trackGeolocation: false,
    trackResources: false,
    webVitalsInstrumentation: {
      reportAllChanges: false,
      trackAttributionSources: false,
    },
  });
  // Faro's default metadata producers are evaluated separately for every item.
  // Remove the complete vendor set at the source: an outbound hook cannot
  // reliably prevent a later producer from being serialized.
  faro.metas.remove(...faro.config.metas);
  // Faro registers instrumentation hooks while initializeFaro runs. Register the
  // privacy boundary afterwards so session/browser/page metadata added by those
  // hooks cannot bypass DANTE's outbound-data contract.
  faro.transports.addBeforeSendHooks(sanitizeTransportItem);
  webObservability = faro;

  installWebTelemetryAdapter({
    observeResolvedRoute(routeId) {
      faro.api.pushEvent('dante.route.resolved', { route_id: routeId });
    },
    observeRenderFailure(error, componentStack) {
      const reportedError = new Error(sanitizeText(error.message));
      reportedError.name = 'ReactRenderError';
      reportedError.stack = sanitizeText(
        [error.stack, componentStack].filter(Boolean).join('\n'),
      );
      faro.api.pushError(reportedError, { type: 'react.render' });
    },
  });
}
