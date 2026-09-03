export const WORLD_FOCUS_CONNECTIVITY_STATES = Object.freeze([
  'online',
  'offline',
] as const);

export type WorldFocusConnectivityState =
  (typeof WORLD_FOCUS_CONNECTIVITY_STATES)[number];

export const WORLD_FOCUS_REPLAY_STATES = Object.freeze([
  'idle',
  'pending',
] as const);

export type WorldFocusReplayState = (typeof WORLD_FOCUS_REPLAY_STATES)[number];

export const WORLD_FOCUS_PROVIDER_DELIVERY_STATES = Object.freeze([
  'nominal',
  'lagging',
  'unknown',
] as const);

export type WorldFocusProviderDeliveryState =
  (typeof WORLD_FOCUS_PROVIDER_DELIVERY_STATES)[number];

export const WORLD_FOCUS_REQUEST_TIMING_STATES = Object.freeze([
  'within-window',
  'timed-out',
  'unknown',
] as const);

export type WorldFocusRequestTimingState =
  (typeof WORLD_FOCUS_REQUEST_TIMING_STATES)[number];

export type WorldFocusSyncPresentation = Readonly<{
  connectivity: WorldFocusConnectivityState;
  replay: WorldFocusReplayState;
  providerDelivery: WorldFocusProviderDeliveryState;
  requestTiming: WorldFocusRequestTimingState;
}>;

function isRecord(value: unknown): value is Readonly<Record<string, unknown>> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isConnectivityState(
  value: unknown,
): value is WorldFocusConnectivityState {
  return value === 'online' || value === 'offline';
}

function isReplayState(value: unknown): value is WorldFocusReplayState {
  return value === 'idle' || value === 'pending';
}

function isProviderDeliveryState(
  value: unknown,
): value is WorldFocusProviderDeliveryState {
  return value === 'nominal' || value === 'lagging' || value === 'unknown';
}

function isRequestTimingState(
  value: unknown,
): value is WorldFocusRequestTimingState {
  return value === 'within-window' || value === 'timed-out' || value === 'unknown';
}

/**
 * Materializes a narrow, sanitized frontend presentation of platform/sync
 * conditions. The four axes are intentionally independent: being offline does
 * not imply that queued replay succeeded or failed, provider lag does not make
 * canonical data stale by itself, and a request timeout is not a semantic
 * negative result.
 *
 * Authoritative retry, replay, provider, conflict and synchronization behavior
 * remains outside this model. Extra input fields are deliberately not copied
 * across the frontend boundary.
 */
export function createWorldFocusSyncPresentation(
  input: unknown,
): WorldFocusSyncPresentation {
  if (!isRecord(input)) {
    throw new Error('World Focus sync presentation must be an object');
  }

  const { connectivity, replay, providerDelivery, requestTiming } = input;

  if (!isConnectivityState(connectivity)) {
    throw new Error('World Focus connectivity must be online or offline');
  }

  if (!isReplayState(replay)) {
    throw new Error('World Focus replay state must be idle or pending');
  }

  if (!isProviderDeliveryState(providerDelivery)) {
    throw new Error(
      'World Focus provider delivery must be nominal, lagging or unknown',
    );
  }

  if (!isRequestTimingState(requestTiming)) {
    throw new Error(
      'World Focus request timing must be within-window, timed-out or unknown',
    );
  }

  return Object.freeze({
    connectivity,
    replay,
    providerDelivery,
    requestTiming,
  });
}
