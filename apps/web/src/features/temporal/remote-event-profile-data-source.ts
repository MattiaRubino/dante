import { createWebFetch } from '../../platform/api/web-fetch';
import { createRemoteTemporalEventAgendaDataSource } from './remote-event-agenda-data-source';
import type { TemporalEventDetailRecord } from './event-data-source';
import {
  serializeActivityObjectiveEdits,
  type ActivityObjectiveBatch,
  type RealityMode,
} from './remote-reality-objective-data-source';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type EventProfileDraft = Readonly<{
  title: string;
  description: string | null;
  location: string | null;
  colorCode: string | null;
}>;

export type EventSchedulePlacementInput =
  | Readonly<{
      kind: 'date_span';
      start_date: string;
      end_date_exclusive: string;
    }>
  | Readonly<{
      kind: 'floating_local_interval';
      starts_local_at: string;
      ends_local_at: string;
    }>
  | Readonly<{
      kind: 'named_zone_local_interval';
      starts_local_at: string;
      ends_local_at: string;
      zone_id: string;
      disambiguation: 'reject' | 'earlier' | 'later';
    }>;

export type EventAtomicDraft = Readonly<{
  profile?: EventProfileDraft;
  agendaParts?: readonly string[];
  lifeArea?: Readonly<{
    ref: string | null;
    expectedRevision: number;
  }>;
  objectives?: ActivityObjectiveBatch;
  reality?: Readonly<{ mode: RealityMode; expectedStateRef: string | null }>;
  placementLock?: Readonly<{
    scheduleRef: string;
    locked: boolean;
    expectedRevision: number;
  }>;
  schedule?: Readonly<{
    scheduleRef: string;
    expectedMaterialStateRef: string;
    placement: EventSchedulePlacementInput;
  }>;
  reminder?: Readonly<{
    scheduleRef: string;
    expectedStateRef: string | null;
    enabled: boolean;
    leadMinutes: number;
  }>;
  participants?: readonly Readonly<{
    participantRef: string;
    requirementCode: 'required' | 'optional' | null;
    expectedRequirementCode: 'required' | 'optional' | null;
  }>[];
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
    async reviseAtomic(
      eventRef: string,
      current: TemporalEventDetailRecord,
      changes: EventAtomicDraft,
      operationId: string,
    ): Promise<TemporalEventDetailRecord> {
      const profile = changes.profile;
      if (profile && !Number.isSafeInteger(current.profileRevision)) {
        throw new Error('Revisione del profilo Event non disponibile.');
      }
      if (
        changes.agendaParts &&
        !Number.isSafeInteger(current.agendaRevision)
      ) {
        throw new Error('Revisione della Scaletta non disponibile.');
      }
      if (
        changes.agendaParts?.some((part) => !part.trim() || part.length > 1000)
      ) {
        throw new Error('Completa ogni punto della Scaletta.');
      }
      const title = profile?.title.trim();
      const description = profile?.description?.trim() || null;
      const location = profile?.location?.trim() || null;
      if (
        profile &&
        (!title ||
          title.length > 300 ||
          (profile.colorCode !== null &&
            !/^#[0-9A-F]{6}$/.test(profile.colorCode)))
      ) {
        throw new Error('Il titolo o i metadati Event non sono validi.');
      }
      const authResponse = await request('/api/v1/auth/session');
      const auth = object(await authResponse.json());
      if (
        !authResponse.ok ||
        auth.authenticated !== true ||
        typeof auth.csrf_token !== 'string' ||
        !auth.csrf_token
      ) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(
        `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/atomic-edit`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': auth.csrf_token,
          },
          body: JSON.stringify({
            operation_id: operationId,
            ...(profile
              ? {
                  profile: {
                    operation_id: `${operationId}:profile`,
                    expected_revision: current.profileRevision,
                    title,
                    description,
                    location,
                    color_code: profile.colorCode,
                  },
                }
              : {}),
            ...(changes.agendaParts
              ? {
                  agenda: {
                    operation_id: `${operationId}:agenda`,
                    expected_revision: current.agendaRevision,
                    agenda_parts: changes.agendaParts,
                  },
                }
              : {}),
            ...(changes.lifeArea
              ? {
                  life_area: {
                    life_area_ref: changes.lifeArea.ref,
                    expected_assignment_revision:
                      changes.lifeArea.expectedRevision,
                  },
                }
              : {}),
            ...(changes.objectives
              ? {
                  objectives: serializeActivityObjectiveEdits(
                    changes.objectives,
                  ),
                }
              : {}),
            ...(changes.reality
              ? {
                  reality: {
                    operation_id: `${operationId}:reality`,
                    mode_code: changes.reality.mode,
                    expected_state_ref: changes.reality.expectedStateRef,
                  },
                }
              : {}),
            ...(changes.placementLock
              ? {
                  placement_lock: {
                    schedule_ref: changes.placementLock.scheduleRef,
                    locked: changes.placementLock.locked,
                    expected_revision: changes.placementLock.expectedRevision,
                  },
                }
              : {}),
            ...(changes.schedule
              ? {
                  schedule: {
                    schedule_ref: changes.schedule.scheduleRef,
                    expected_material_state_ref:
                      changes.schedule.expectedMaterialStateRef,
                    placement: changes.schedule.placement,
                  },
                }
              : {}),
            ...(changes.reminder
              ? {
                  reminder: {
                    schedule_ref: changes.reminder.scheduleRef,
                    expected_state_ref: changes.reminder.expectedStateRef,
                    enabled: changes.reminder.enabled,
                    lead_minutes: changes.reminder.leadMinutes,
                  },
                }
              : {}),
            ...(changes.participants
              ? {
                  participants: changes.participants.map((participant) => ({
                    participant_ref: participant.participantRef,
                    requirement_code: participant.requirementCode,
                    expected_requirement_code:
                      participant.expectedRequirementCode,
                  })),
                }
              : {}),
          }),
        },
      );
      if (!response.ok) {
        throw new Error(
          response.status === 409
            ? 'L’Evento è cambiato: riapri la modifica e riprova.'
            : 'Impossibile salvare le modifiche Event.',
        );
      }
      const accepted = object(await response.json());
      const event = object(accepted.event);
      if (event.event_ref !== eventRef) {
        throw new Error('Conferma modifica Event non valida.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return eventSource.loadEvent(eventRef);
    },
    async revise(
      eventRef: string,
      current: TemporalEventDetailRecord,
      next: EventProfileDraft,
      operationId: string,
    ): Promise<TemporalEventDetailRecord> {
      if (
        !Number.isSafeInteger(current.profileRevision) ||
        current.profileRevision === undefined ||
        current.profileRevision < 0
      ) {
        throw new Error(
          'Revisione Event non disponibile: ricarica il profilo.',
        );
      }
      const title = next.title.trim();
      const description = next.description?.trim() || null;
      const location = next.location?.trim() || null;
      if (
        !title ||
        title.length > 300 ||
        (next.colorCode !== null && !/^#[0-9A-F]{6}$/.test(next.colorCode))
      ) {
        throw new Error('Il titolo o i metadati Event non sono validi.');
      }
      const authResponse = await request('/api/v1/auth/session');
      const auth = object(await authResponse.json());
      if (
        !authResponse.ok ||
        auth.authenticated !== true ||
        typeof auth.csrf_token !== 'string' ||
        !auth.csrf_token
      ) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(
        `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/profile`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': auth.csrf_token,
          },
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
      if (!response.ok)
        throw new Error(
          response.status === 409
            ? 'Il profilo Event è cambiato: ricarica e riprova.'
            : 'Impossibile modificare il profilo Event.',
        );
      const accepted = object(await response.json());
      if (
        accepted.event_ref !== eventRef ||
        accepted.revision !== current.profileRevision + 1 ||
        accepted.title !== title ||
        accepted.description !== description ||
        accepted.location !== location ||
        accepted.color_code !== next.colorCode
      ) {
        throw new Error('Conferma modifica Event non valida.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return eventSource.loadEvent(eventRef);
    },
  });
}
