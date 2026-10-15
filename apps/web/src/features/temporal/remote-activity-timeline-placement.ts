import { createWebFetch } from '../../platform/api/web-fetch';
import { createRemoteActivityInspector } from './remote-activity-inspector';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type TimelineActivityPlacement = Readonly<{
  scheduleRef: string;
  expectedMaterialStateRef: string;
}>;

export type TimelineUndoReceipt = Readonly<{
  scheduleRef: string;
  unscheduleOperationId: string;
}>;

function record(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta della Timeline non valida.');
  }
  return value as Record<string, unknown>;
}

async function checked(response: Response): Promise<unknown> {
  const payload: unknown = await response.json();
  if (!response.ok) {
    throw new Error(
      response.status === 409
        ? 'La collocazione o le Sessioni sono cambiate: ricarica prima di confermare.'
        : response.status === 404
          ? 'Activity non più disponibile.'
          : 'Impossibile aggiornare la collocazione Activity.',
    );
  }
  return payload;
}

export function createRemoteActivityTimelinePlacement(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const inspector = createRemoteActivityInspector(fetchFn);
  const url = (activityRef: string) =>
    `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}`;

  async function token() {
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
    async current(activityRef: string): Promise<TimelineActivityPlacement> {
      const data = record(await checked(await request(`${url(activityRef)}/edit-snapshot`)));
      if (data.activity_ref !== activityRef || !Array.isArray(data.schedules)) {
        throw new Error('Identità Activity non coerente.');
      }
      const rows = data.schedules.map(record);
      const intervals = rows.filter((row) => row.role_code === 'interval');
      if (intervals.length !== 0) {
        throw new Error(
          'L’Activity contiene più intervalli: rimuovili dal piano con il replan coordinato.',
        );
      }
      const envelope = rows.find((row) => row.role_code === 'envelope');
      if (
        envelope === undefined ||
        typeof envelope.schedule_ref !== 'string' ||
        typeof envelope.placement_material_state_ref !== 'string'
      ) {
        throw new Error('Questa Activity non ha una collocazione attiva.');
      }
      return {
        scheduleRef: envelope.schedule_ref,
        expectedMaterialStateRef: envelope.placement_material_state_ref,
      };
    },

    async listUndo(activityRef: string): Promise<readonly TimelineUndoReceipt[]> {
      const body = await checked(
        await request(`${url(activityRef)}/timeline-undo-receipts`),
      );
      if (!Array.isArray(body)) {
        throw new Error('Elenco Undo non valido.');
      }
      return body.map((entry: unknown) => {
        const row = record(entry);
        if (
          typeof row.schedule_ref !== 'string' ||
          typeof row.unschedule_operation_id !== 'string'
        ) {
          throw new Error('Ricevuta Undo non valida.');
        }
        return {
          scheduleRef: row.schedule_ref,
          unscheduleOperationId: row.unschedule_operation_id,
        };
      });
    },

    async remove(
      activityRef: string,
      placement: TimelineActivityPlacement,
      disposition: 'keep' | 'delete' | null,
    ): Promise<TimelineUndoReceipt> {
      const currentImpact = await inspector.sessionImpact(activityRef);
      if (disposition === null && currentImpact.attempts.length !== 0) {
        throw new Error('Scegli Mantieni Sessioni, Elimina Sessioni o Annulla.');
      }
      const response = await request(`${url(activityRef)}/timeline-unplace`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await token(),
        },
        body: JSON.stringify({
          operation_id: crypto.randomUUID(),
          schedule_ref: placement.scheduleRef,
          expected_material_state_ref: placement.expectedMaterialStateRef,
          session_disposition: disposition,
          expected_session_fingerprint:
            disposition === null ? null : currentImpact.fingerprint,
        }),
      });
      const data = record(await checked(response));
      if (
        data.activity_ref !== activityRef ||
        data.schedule_ref !== placement.scheduleRef ||
        typeof data.operation_id !== 'string' ||
        data.placement_material_state_ref !== null
      ) {
        throw new Error('Conferma rimozione dalla Timeline non valida.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return {
        scheduleRef: placement.scheduleRef,
        unscheduleOperationId: data.operation_id,
      };
    },

    async undo(activityRef: string, receipt: TimelineUndoReceipt): Promise<void> {
      const impact = await inspector.sessionImpact(activityRef);
      const response = await request(`${url(activityRef)}/timeline-undo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await token(),
        },
        body: JSON.stringify({
          operation_id: crypto.randomUUID(),
          schedule_ref: receipt.scheduleRef,
          unschedule_operation_id: receipt.unscheduleOperationId,
          expected_session_fingerprint: impact.fingerprint,
        }),
      });
      const data = record(await checked(response));
      if (
        data.activity_ref !== activityRef ||
        data.schedule_ref !== receipt.scheduleRef ||
        typeof data.placement_material_state_ref !== 'string'
      ) {
        throw new Error('Conferma Undo non coerente.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
    },
  });
}
