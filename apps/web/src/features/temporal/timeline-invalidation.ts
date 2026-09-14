export type TemporalTimelineInvalidationListener = () => void;

const listeners = new Set<TemporalTimelineInvalidationListener>();

/**
 * Frontend read-model invalidation only. This is not a Domain Event, provider
 * event, Schedule history record or canonical mutation receipt.
 */
export function invalidateTemporalTimelineRead(): void {
  for (const listener of [...listeners]) {
    listener();
  }
}

export function subscribeTemporalTimelineInvalidation(
  listener: TemporalTimelineInvalidationListener,
): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

export type TemporalPlanningInvalidationListener = () => void;

const planningListeners = new Set<TemporalPlanningInvalidationListener>();

export function invalidateTemporalPlanningRead(): void {
  for (const listener of [...planningListeners]) {
    listener();
  }
}

export function subscribeTemporalPlanningInvalidation(
  listener: TemporalPlanningInvalidationListener,
): () => void {
  planningListeners.add(listener);
  return () => {
    planningListeners.delete(listener);
  };
}
