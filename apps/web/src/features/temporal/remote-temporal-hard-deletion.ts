import { createWebFetch } from '../../platform/api/web-fetch';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type TemporalHardDeletionScope =
  | 'activity_instance'
  | 'activity_series'
  | 'event_once'
  | 'event_instance'
  | 'event_series';

export type TemporalHardDeletionPreview = Readonly<{
  requestedRef: string;
  scope: TemporalHardDeletionScope;
  fingerprint: string;
}>;

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta di eliminazione non valida.');
  }
  return value as Record<string, unknown>;
}

export function createRemoteTemporalHardDeletion(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const url = (ref: string) =>
    `/api/v1/temporal/hard-deletion/${encodeURIComponent(ref)}`;

  return Object.freeze({
    async preview(
      ref: string,
      scope: TemporalHardDeletionScope,
    ): Promise<TemporalHardDeletionPreview> {
      const response = await request(
        `${url(ref)}/preview?scope=${encodeURIComponent(scope)}`,
      );
      if (!response.ok) {
        throw new Error(
          response.status === 404
            ? 'L’istanza o la serie non è più disponibile.'
            : 'Non è stato possibile verificare i dati collegati.',
        );
      }
      const value = record(await response.json());
      if (
        value.requested_ref !== ref ||
        value.scope !== scope ||
        typeof value.fingerprint !== 'string' ||
        !/^[a-f0-9]{64}$/.test(value.fingerprint)
      ) {
        throw new Error('Identità o versione della cancellazione non valida.');
      }
      return { requestedRef: ref, scope, fingerprint: value.fingerprint };
    },
    async deleteConfirmed(preview: TemporalHardDeletionPreview): Promise<void> {
      const authResponse = await request('/api/v1/auth/session');
      const auth = record(await authResponse.json());
      if (
        !authResponse.ok ||
        auth.authenticated !== true ||
        typeof auth.csrf_token !== 'string' ||
        !auth.csrf_token
      ) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(url(preview.requestedRef), {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-Dante-CSRF': auth.csrf_token,
        },
        body: JSON.stringify({
          scope: preview.scope,
          expected_fingerprint: preview.fingerprint,
        }),
      });
      if (!response.ok) {
        throw new Error(
          response.status === 409
            ? 'La serie o le sue istanze sono cambiate. Ricarica prima di eliminare.'
            : response.status === 404
              ? 'L’elemento non esiste più o non è disponibile.'
              : 'Eliminazione non riuscita: nessuna cancellazione parziale accettata.',
        );
      }
      const accepted = record(await response.json());
      if (
        accepted.requested_ref !== preview.requestedRef ||
        accepted.scope !== preview.scope ||
        typeof accepted.deleted_rows !== 'number' ||
        !Number.isSafeInteger(accepted.deleted_rows) ||
        accepted.deleted_rows < 1
      ) {
        throw new Error('Conferma eliminazione non coerente con la selezione.');
      }
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
    },
  });
}
