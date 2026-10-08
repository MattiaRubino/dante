import { createWebFetch } from '../../platform/api/web-fetch';
import { createRemoteTemporalEventAgendaDataSource } from './remote-event-agenda-data-source';
import type { TemporalEventDetailRecord } from './event-data-source';
import { invalidateTemporalPlanningRead, invalidateTemporalTimelineRead } from './timeline-invalidation';

export type EventProfileDraft = Readonly<{
  title: string;
  description: string | null;
  location: string | null;
  colorCode: string | null;
}>;

function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta profilo Event non valida.');
  }
  return value as Record<string, unknown>;
}

export function createRemoteEventProfileDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const eventSource = createRemoteTemporalEventAgendaDataSource(fetchFn);
  return Object.freeze({
    load: (eventRef: string): Promise<TemporalEventDetailRecord> =>
      eventSource.loadEvent(eventRef),
    async revise(
      eventRef: string, current: TemporalEventDetailRecord,
      next: EventProfileDraft, operationId: string,
    ): Promise<TemporalEventDetailRecord> {
      if (!Number.isSafeInteger(current.profileRevision) ||
          current.profileRevision === undefined || current.profileRevision < 0) {
        throw new Error('Revisione Event non disponibile: ricarica il profilo.');
      }
      const title = next.title.trim();
      const description = next.description?.trim() || null;
      const location = next.location?.trim() || null;
      if (!title || title.length > 300 ||
          (next.colorCode !== null && !/^#[0-9A-F]{6}$/.test(next.colorCode))) {
        throw new Error('Il titolo o i metadati Event non sono validi.');
      }
      const authResponse = await request('/api/v1/auth/session');
      const auth = object(await authResponse.json());
      if (!authResponse.ok || auth.authenticated !== true ||
          typeof auth.csrf_token !== 'string' || !auth.csrf_token) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(
        `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/profile`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json',
            'X-Dante-CSRF': auth.csrf_token },
          body: JSON.stringify({
            operation_id: operationId,
            expected_revision: current.profileRevision,
            title,
            description,
            location,
            color_code: next.colorCode,
          }),
        },
      );
      if (!response.ok) throw new Error(response.status === 409
        ? 'Il profilo Event è cambiato: ricarica e riprova.'
        : 'Impossibile modificare il profilo Event.');
      const accepted = object(await response.json());
      if (accepted.event_ref !== eventRef ||
          accepted.revision !== current.profileRevision + 1 ||
          accepted.title !== title ||
          accepted.description !== description ||
          accepted.location !== location ||
          accepted.color_code !== next.colorCode) {
        throw new Error('Conferma modifica Event non valida.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return eventSource.loadEvent(eventRef);
    },
  });
}
