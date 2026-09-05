import {
  readWebObservabilityConfig,
  WebObservabilityConfigurationError,
} from './config';
import {
  beginWebTelemetryInitialization,
  disableWebTelemetryAdapter,
} from './bridge';

let initialization: Promise<void> | undefined;

type PrivacyAwareNavigator = Navigator & {
  readonly globalPrivacyControl?: boolean;
};

function globalPrivacyControlEnabled(): boolean {
  return (
    (globalThis.navigator as PrivacyAwareNavigator | undefined)
      ?.globalPrivacyControl === true
  );
}

function boundedInitializationWarning(error: unknown): void {
  const failure =
    error instanceof WebObservabilityConfigurationError
      ? error.name
      : 'WebObservabilityInitializationError';
  globalThis.console.warn(`${failure}: browser telemetry is disabled.`);
}

export function initializeWebObservability(
  source: Readonly<Record<string, string | undefined>> = import.meta.env,
): Promise<void> {
  if (initialization !== undefined) {
    return initialization;
  }

  initialization = (async () => {
    try {
      const config = readWebObservabilityConfig(source);
      if (
        !config.enabled ||
        config.collectorUrl === undefined ||
        (config.respectGlobalPrivacyControl && globalPrivacyControlEnabled())
      ) {
        return;
      }

      beginWebTelemetryInitialization();
      const { initializeFaroRuntime } = await import('./runtime');
      initializeFaroRuntime(config);
    } catch (error) {
      disableWebTelemetryAdapter();
      boundedInitializationWarning(error);
    }
  })();

  return initialization;
}
