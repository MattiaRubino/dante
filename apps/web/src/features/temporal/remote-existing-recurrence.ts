import { createWebFetch } from '../../platform/api/web-fetch';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';
import type { RecurringAuthoringCalendarRecurrence } from '../temporal-create/application/remote-recurring-authoring';

type StartActivityBasis = Readonly<{
  activityRef: string;
  expectedProfileRevision: number;
  envelopeScheduleRef: string;
  expectedPlacementStateRef: string;
}>;

type StartEventBasis = Readonly<{
  eventRef: string;
  expectedProfileRevision: number;
  scheduleRef: string;
  expectedPlacementStateRef: string;
}>;

export function createRemoteExistingRecurrence(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  return Object.freeze({
    async eventSeed(eventRef: string): Promise<string | null> {
      const response = await request(
        `/api/v1/temporal/recurring/events/${encodeURIComponent(eventRef)}/seed`,
      );
      if (!response.ok)
        throw new Error('Impossibile verificare la ripetizione Event.');
      const result: unknown = await response.json();
      if (result !== null && typeof result !== 'string') {
        throw new Error('Risposta ripetizione Event non valida.');
      }
      return result;
    },
    async eventFirstOccurrence(eventRef: string): Promise<string | null> {
      const response = await request(
        `/api/v1/temporal/recurring/events/${encodeURIComponent(eventRef)}/first-occurrence`,
      );
      if (!response.ok) {
        throw new Error('Impossibile verificare la prima istanza Event.');
      }
      const value: unknown = await response.json();
      if (value !== null && (typeof value !== 'string' || value.length !== 36)) {
        throw new Error('Identità della prima istanza Event non valida.');
      }
      return value;
    },
    async startActivity(
      basis: StartActivityBasis,
      recurrence: RecurringAuthoringCalendarRecurrence,
      operationId: string,
    ): Promise<void> {
      const session = await request('/api/v1/auth/session');
      const auth: unknown = await session.json();
      if (
        !session.ok ||
        !auth ||
        typeof auth !== 'object' ||
        !('csrf_token' in auth) ||
        typeof auth.csrf_token !== 'string'
      ) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(
        `/api/v1/temporal/recurring/activities/${encodeURIComponent(basis.activityRef)}/start`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': auth.csrf_token,
          },
          body: JSON.stringify({
            operation_id: operationId,
            expected_profile_revision: basis.expectedProfileRevision,
            envelope_schedule_ref: basis.envelopeScheduleRef,
            expected_placement_state_ref: basis.expectedPlacementStateRef,
            recurrence,
          }),
        },
      );
      if (!response.ok) {
        const problem: unknown = await response.json().catch(() => null);
        const detail =
          problem &&
          typeof problem === 'object' &&
          'detail' in problem &&
          typeof problem.detail === 'string'
            ? problem.detail
            : 'Non è stato possibile avviare la ripetizione. Riapri Modifica e riprova.';
        throw new Error(detail);
      }
      invalidateTemporalTimelineRead();
    },
    async startEvent(
      basis: StartEventBasis,
      recurrence: RecurringAuthoringCalendarRecurrence,
      operationId: string,
    ): Promise<void> {
      const session = await request('/api/v1/auth/session');
      const auth: unknown = await session.json();
      if (
        !session.ok ||
        !auth ||
        typeof auth !== 'object' ||
        !('csrf_token' in auth) ||
        typeof auth.csrf_token !== 'string'
      ) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(
        `/api/v1/temporal/recurring/events/${encodeURIComponent(basis.eventRef)}/start`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': auth.csrf_token,
          },
          body: JSON.stringify({
            operation_id: operationId,
            expected_profile_revision: basis.expectedProfileRevision,
            schedule_ref: basis.scheduleRef,
            expected_placement_state_ref: basis.expectedPlacementStateRef,
            recurrence,
          }),
        },
      );
      if (!response.ok) {
        const problem: unknown = await response.json().catch(() => null);
        const detail =
          problem &&
          typeof problem === 'object' &&
          'detail' in problem &&
          typeof problem.detail === 'string'
            ? problem.detail
            : 'Non è stato possibile avviare la ripetizione Event.';
        throw new Error(detail);
      }
      invalidateTemporalTimelineRead();
    },
  });
}
