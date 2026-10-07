import type { ActivityDuplicateSeed } from '../application/activity-duplicate-seed';

const EVENT = 'dante:temporal-create-duplicate';

export function requestTemporalCreateDuplicate(
  seed: ActivityDuplicateSeed,
): void {
  window.dispatchEvent(
    new CustomEvent<ActivityDuplicateSeed>(EVENT, { detail: seed }),
  );
}

export function subscribeTemporalCreateDuplicate(
  onRequest: (seed: ActivityDuplicateSeed) => void,
): () => void {
  const listener = (event: Event) => {
    if (event instanceof CustomEvent)
      onRequest(event.detail as ActivityDuplicateSeed);
  };
  window.addEventListener(EVENT, listener);
  return () => window.removeEventListener(EVENT, listener);
}
