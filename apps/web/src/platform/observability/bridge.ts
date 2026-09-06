type WebTelemetryAdapter = Readonly<{
  observeResolvedRoute: (routeId: string) => void;
  observeRenderFailure: (error: Error, componentStack?: string) => void;
}>;

const MAX_ROUTE_ID_CHARACTERS = 160;

let activeAdapter: WebTelemetryAdapter | undefined;
let pendingRouteId: string | undefined;
let lastRouteId: string | undefined;
let waitingForAdapter = false;

function boundedRouteId(routeId: string): string {
  return routeId.startsWith('/')
    ? routeId.slice(0, MAX_ROUTE_ID_CHARACTERS)
    : 'unknown';
}

function safelyObserve(operation: VoidFunction): void {
  try {
    operation();
  } catch {
    // A telemetry adapter must never become a product failure.
  }
}

export function installWebTelemetryAdapter(adapter: WebTelemetryAdapter): void {
  activeAdapter = adapter;
  waitingForAdapter = false;
  if (pendingRouteId !== undefined) {
    const routeId = pendingRouteId;
    pendingRouteId = undefined;
    safelyObserve(() => adapter.observeResolvedRoute(routeId));
  }
}

export function beginWebTelemetryInitialization(): void {
  waitingForAdapter = true;
}

export function disableWebTelemetryAdapter(): void {
  waitingForAdapter = false;
  pendingRouteId = undefined;
}

export function observeResolvedRoute(routeId: string): void {
  const normalizedRouteId = boundedRouteId(routeId);
  if (normalizedRouteId === lastRouteId) {
    return;
  }
  lastRouteId = normalizedRouteId;

  if (activeAdapter === undefined) {
    if (waitingForAdapter) {
      pendingRouteId = normalizedRouteId;
    }
    return;
  }
  safelyObserve(() => activeAdapter?.observeResolvedRoute(normalizedRouteId));
}

export function observeRenderFailure(
  error: Error,
  componentStack?: string,
): void {
  safelyObserve(() =>
    activeAdapter?.observeRenderFailure(error, componentStack),
  );
}
