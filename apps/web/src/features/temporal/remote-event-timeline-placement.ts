import { createWebFetch } from '../../platform/api/web-fetch';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type EventTimelineSchedule = Readonly<{
  scheduleRef: string;
  subjectNativeRef: string;
  materialStateRef: string | null;
  displayLabel: string;
}>;

export type EventTimelineUndoReceipt = Readonly<{
  scheduleRef: string;
  unscheduleOperationId: string;
}>;

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta Schedule Event non valida.');
  }
  return value as Record<string, unknown>;
}

async function checked(response: Response): Promise<unknown> {
  const payload: unknown = await response.json();
  if (!response.ok) {
    throw new Error(
      response.status === 409
        ? 'La Schedule Event è cambiata. Ricarica prima di confermare.'
        : response.status === 404
          ? 'La Schedule Event non è più disponibile.'
          : 'La collocazione Event non può essere aggiornata.',
    );
  }
  return payload;
}

export function createRemoteEventTimelinePlacement(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const root = (ref: string) =>
    `/api/v1/temporal/events/${encodeURIComponent(ref)}`;

  async function csrf(): Promise<string> {
    const auth = record(await checked(await request('/api/v1/auth/session')));
    if (
      auth.authenticated !== true ||
      typeof auth.csrf_token !== 'string' ||
      !auth.csrf_token
    ) {
      throw new Error('Sessione non autenticata.');
    }
    return auth.csrf_token;
  }

  return Object.freeze({
    async list(eventRef: string): Promise<readonly EventTimelineSchedule[]> {
      const payload = await checked(
        await request(`${root(eventRef)}/timeline-schedules`),
      );
      if (!Array.isArray(payload)) {
        throw new Error('Elenco Schedule Event non valido.');
      }
      return payload.map((value: unknown) => {
        const row = record(value);
        if (
          typeof row.schedule_ref !== 'string' ||
          typeof row.subject_native_ref !== 'string' ||
          (row.material_state_ref !== null &&
            typeof row.material_state_ref !== 'string') ||
          typeof row.display_label !== 'string'
        ) {
          throw new Error('Identità della collocazione Event non valida.');
        }
        return {
          scheduleRef: row.schedule_ref,
          subjectNativeRef: row.subject_native_ref,
          materialStateRef: row.material_state_ref,
          displayLabel: row.display_label,
        };
      });
    },
    async listUndo(
      eventRef: string,
    ): Promise<readonly EventTimelineUndoReceipt[]> {
      const payload = await checked(
        await request(`${root(eventRef)}/timeline-undo-receipts`),
      );
      if (!Array.isArray(payload)) {
        throw new Error('Elenco ricevute Event non valido.');
      }
      return payload.map((value: unknown) => {
        const row = record(value);
        if (
          typeof row.schedule_ref !== 'string' ||
          typeof row.unschedule_operation_id !== 'string'
        ) {
          throw new Error('Ricevuta Undo Event non valida.');
        }
        return {
          scheduleRef: row.schedule_ref,
          unscheduleOperationId: row.unschedule_operation_id,
        };
      });
    },
    async unplace(
      selected: EventTimelineSchedule,
    ): Promise<EventTimelineUndoReceipt> {
      if (selected.materialStateRef === null) {
        throw new Error('Questa Schedule Event è già senza collocazione.');
      }
      const response = await request(
        `/api/v1/temporal/schedules/${encodeURIComponent(selected.scheduleRef)}/unschedule`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify({
            operation_id: crypto.randomUUID(),
            expected_placement_material_state_ref: selected.materialStateRef,
          }),
        },
      );
      const value = record(await checked(response));
      if (
        value.schedule_ref !== selected.scheduleRef ||
        typeof value.unschedule_operation_id !== 'string'
      ) {
        throw new Error('Conferma rimozione Schedule Event non coerente.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return {
        scheduleRef: selected.scheduleRef,
        unscheduleOperationId: value.unschedule_operation_id,
      };
    },
    async undo(receipt: EventTimelineUndoReceipt): Promise<void> {
      const response = await request(
        `/api/v1/temporal/schedules/${encodeURIComponent(receipt.scheduleRef)}/unschedule/undo`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify({
            operation_id: crypto.randomUUID(),
            unschedule_operation_id: receipt.unscheduleOperationId,
          }),
        },
      );
      const accepted = record(await checked(response));
      if (
        accepted.schedule_ref !== receipt.scheduleRef ||
        typeof accepted.placement_material_state_ref !== 'string'
      ) {
        throw new Error('Conferma ripristino Event non coerente.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
    },
  });
}
