export type WebObservabilityEnvironment = 'local' | 'dev' | 'uat' | 'prod';

export type WebObservabilityConfig = Readonly<{
  enabled: boolean;
  environment: WebObservabilityEnvironment;
  releaseSha: string;
  buildId: string;
  collectorUrl?: string;
  sessionSampleRate: number;
  respectGlobalPrivacyControl: boolean;
}>;

type EnvironmentSource = Readonly<Record<string, string | undefined>>;

const ENVIRONMENTS = new Set<WebObservabilityEnvironment>([
  'local',
  'dev',
  'uat',
  'prod',
]);

export class WebObservabilityConfigurationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'WebObservabilityConfigurationError';
  }
}

function requiredIdentity(
  source: EnvironmentSource,
  key: string,
  fallback: string,
): string {
  const value = source[key]?.trim() ?? fallback;
  if (!value) {
    throw new WebObservabilityConfigurationError(`${key} cannot be blank.`);
  }
  return value;
}

function parseEnvironment(
  source: EnvironmentSource,
): WebObservabilityEnvironment {
  const candidate = source.VITE_DANTE_ENV?.trim().toLowerCase() ?? 'local';
  if (!ENVIRONMENTS.has(candidate as WebObservabilityEnvironment)) {
    throw new WebObservabilityConfigurationError(
      'VITE_DANTE_ENV must be local, dev, uat or prod.',
    );
  }
  return candidate as WebObservabilityEnvironment;
}

function parseSampleRate(source: EnvironmentSource): number {
  const raw = source.VITE_DANTE_FARO_SESSION_SAMPLE_RATE?.trim() ?? '0.10';
  const value = Number(raw);
  if (!Number.isFinite(value) || value < 0 || value > 1) {
    throw new WebObservabilityConfigurationError(
      'VITE_DANTE_FARO_SESSION_SAMPLE_RATE must be between 0 and 1.',
    );
  }
  return value;
}

function parseEnabled(source: EnvironmentSource): boolean {
  const raw = source.VITE_DANTE_OBSERVABILITY_ENABLED?.trim() ?? 'false';
  if (raw !== 'true' && raw !== 'false') {
    throw new WebObservabilityConfigurationError(
      'VITE_DANTE_OBSERVABILITY_ENABLED must be true or false.',
    );
  }
  return raw === 'true';
}

function parseBoolean(
  source: EnvironmentSource,
  key: string,
  fallback: boolean,
): boolean {
  const raw = source[key]?.trim() ?? String(fallback);
  if (raw !== 'true' && raw !== 'false') {
    throw new WebObservabilityConfigurationError(
      `${key} must be true or false.`,
    );
  }
  return raw === 'true';
}

function isLoopback(hostname: string): boolean {
  return (
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    hostname === '[::1]' ||
    hostname === '::1'
  );
}

function collectorUrl(source: EnvironmentSource): string {
  const raw = source.VITE_DANTE_FARO_COLLECTOR_URL?.trim();
  if (!raw) {
    throw new WebObservabilityConfigurationError(
      'VITE_DANTE_FARO_COLLECTOR_URL is required when observability is enabled.',
    );
  }

  let parsed: URL;
  try {
    parsed = new URL(raw);
  } catch {
    throw new WebObservabilityConfigurationError(
      'VITE_DANTE_FARO_COLLECTOR_URL must be an absolute URL.',
    );
  }
  if (parsed.username || parsed.password || parsed.search || parsed.hash) {
    throw new WebObservabilityConfigurationError(
      'The Faro collector URL cannot contain credentials, query or fragment.',
    );
  }
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    throw new WebObservabilityConfigurationError(
      'The Faro collector URL must use HTTP or HTTPS.',
    );
  }
  if (parsed.protocol !== 'https:' && !isLoopback(parsed.hostname)) {
    throw new WebObservabilityConfigurationError(
      'A non-loopback Faro collector must use HTTPS.',
    );
  }
  return parsed.toString();
}

export function readWebObservabilityConfig(
  source: EnvironmentSource,
): WebObservabilityConfig {
  const enabled = parseEnabled(source);
  const environment = parseEnvironment(source);
  const releaseSha = requiredIdentity(
    source,
    'VITE_DANTE_RELEASE_SHA',
    'local',
  );
  const buildId = requiredIdentity(source, 'VITE_DANTE_BUILD_ID', 'local');

  if (
    environment !== 'local' &&
    (releaseSha === 'local' || buildId === 'local')
  ) {
    throw new WebObservabilityConfigurationError(
      'Non-local observability requires real release and build identities.',
    );
  }

  return {
    enabled,
    environment,
    releaseSha,
    buildId,
    ...(enabled ? { collectorUrl: collectorUrl(source) } : {}),
    sessionSampleRate: parseSampleRate(source),
    respectGlobalPrivacyControl: parseBoolean(
      source,
      'VITE_DANTE_FARO_RESPECT_GPC',
      true,
    ),
  };
}
