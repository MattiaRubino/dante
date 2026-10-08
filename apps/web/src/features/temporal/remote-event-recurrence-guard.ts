import { createWebFetch } from '../../platform/api/web-fetch';

/** Do not flatten a recurring Event template into an unrelated one-off duplicate. */
export function createRemoteEventRecurrenceGuard(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  return Object.freeze({
    async isRecurring(eventRef: string): Promise<boolean> {
      const response = await request(
        `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/recurrence`,
      );
      if (!response.ok) {
        throw new Error('Impossibile verificare la ricorrenza Event: duplicazione bloccata.');
      }
      let payload: unknown;
      try {
        payload = await response.json();
      } catch {
        throw new Error('Risposta ricorrenza Event non valida: duplicazione bloccata.');
      }
      if (payload === null) return false;
      if (typeof payload !== 'object' || Array.isArray(payload)) {
        throw new Error('Risposta ricorrenza Event non valida: duplicazione bloccata.');
      }
      return true;
    },
  });
}
