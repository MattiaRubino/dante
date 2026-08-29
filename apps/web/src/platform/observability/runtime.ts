import {
  CSPInstrumentation,
  ErrorsInstrumentation,
  InternalLoggerLevel,
  NavigationInstrumentation,
  PerformanceInstrumentation,
  SessionInstrumentation,
  ViewInstrumentation,
  WebVitalsInstrumentation,
  initializeFaro,
  type Faro,
} from '@grafana/faro-web-sdk';
import { ReactIntegration } from '@grafana/faro-react';
import { TracingInstrumentation } from '@grafana/faro-web-tracing';

import {
  readWebObservabilityConfig,
  WebObservabilityConfigurationError,
} from './config';
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
    new PerformanceInstrumentation(),
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

export function initializeWebObservability(
  source: Readonly<Record<string, string | undefined>> = import.meta.env,
): Faro | undefined {
  if (webObservability !== undefined) {
    return webObservability;
  }

  try {
    const config = readWebObservabilityConfig(source);
    if (!config.enabled || config.collectorUrl === undefined) {
      return undefined;
    }

    webObservability = initializeFaro({
      url: config.collectorUrl,
      app: {
        name: 'dante-web',
        version: config.releaseSha,
        gitHash: config.releaseSha,
        release: config.buildId,
        environment: config.environment,
      },
      beforeSend: sanitizeTransportItem,
      instrumentations: instrumentations(),
      internalLoggerLevel: InternalLoggerLevel.ERROR,
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
      experimental: {
        fetchTransportV2: true,
      },
    });
    return webObservability;
  } catch (error) {
    const failure =
      error instanceof WebObservabilityConfigurationError
        ? error.name
        : 'WebObservabilityInitializationError';
    globalThis.console.warn(`${failure}: browser telemetry is disabled.`);
    return undefined;
  }
}

export function observeResolvedRoute(routeId: string): void {
  const boundedRouteId = routeId.startsWith('/')
    ? routeId.slice(0, 160)
    : 'unknown';
  try {
    webObservability?.api.pushEvent('dante.route.resolved', {
      route_id: boundedRouteId,
    });
  } catch {
    // A failed telemetry adapter cannot become a route-rendering failure.
  }
}

export function observeRenderFailure(
  error: Error,
  componentStack?: string,
): void {
  if (webObservability === undefined) {
    return;
  }

  try {
    const reportedError = new Error(sanitizeText(error.message));
    reportedError.name = 'ReactRenderError';
    reportedError.stack = sanitizeText(
      [error.stack, componentStack].filter(Boolean).join('\n'),
    );
    webObservability.api.pushError(reportedError, { type: 'react.render' });
  } catch {
    // Telemetry must never replace the product recovery surface with a failure.
  }
}
