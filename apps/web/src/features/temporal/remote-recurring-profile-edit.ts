import { createWebFetch } from '../../platform/api/web-fetch';
import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from './remote-activity-inspector';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type RecurringProfileEditScope = 'only_this' | 'this_and_following';

export type RecurringProfileContext = Readonly<{
  occurrenceRef: string;
  sourceRef: string;
  editRevision: number;
  recurrenceStateRef: string | null;
}>;

type ProfileChanges = Readonly<
  Partial<Pick<ActivityProfile, 'title' | 'description' | 'location' | 'colorCode'>>
>;

function record(value: unknown): Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as Record<string, unknown>
    : {};
}

export function createRemoteRecurringProfileEdit(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const inspector = createRemoteActivityInspector(fetchFn);

  async function read(path: string): Promise<Record<string, unknown>> {
    const result = await request(path);
    if (!result.ok) throw new Error('Impossibile verificare la ricorrenza.');
    return record(await result.json());
  }

  async function csrf(): Promise<string> {
    const response = await request('/api/v1/auth/session');
    const value = record(await response.json());
    if (!response.ok || value.authenticated !== true ||
        typeof value.csrf_token !== 'string') {
      throw new Error('Sessione non autenticata.');
    }
    return value.csrf_token;
  }

  return Object.freeze({
    async loadActivityContext(activityRef: string): Promise<RecurringProfileContext | null> {
      const origin = await read(
        `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/recurrence-origin`,
      );
      if (origin.activity_ref !== activityRef) {
        throw new Error('Identità dell’attività non coerente.');
      }
      if (origin.occurrence_ref === null) return null;
      if (typeof origin.occurrence_ref !== 'string') {
        throw new Error('Origine ricorrente non valida.');
      }
      const ref = origin.occurrence_ref;
      const state = await read(
        `/api/v1/temporal/occurrences/${encodeURIComponent(ref)}/profile-edit-state`,
      );
      if (state.selected_occurrence_ref !== ref ||
          typeof state.source_native_ref !== 'string' ||
          typeof state.edit_revision !== 'number' ||
          !Number.isSafeInteger(state.edit_revision) ||
          state.edit_revision < 0 ||
          (state.recurrence_state_ref !== null &&
            typeof state.recurrence_state_ref !== 'string')) {
        throw new Error('Versione ricorrente non valida.');
      }
      return {
        occurrenceRef: ref,
        sourceRef: state.source_native_ref,
        editRevision: state.edit_revision,
        recurrenceStateRef: state.recurrence_state_ref,
      };
    },

    async saveActivityProfile(
      activityRef: string,
      context: RecurringProfileContext,
      scope: RecurringProfileEditScope,
      changes: ProfileChanges,
      operationId: string,
    ): Promise<ActivityProfile> {
      const response = await request(
        `/api/v1/temporal/occurrences/${encodeURIComponent(context.occurrenceRef)}/profile-edit`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify({
            operation_id: operationId,
            expected_revision: context.editRevision,
            expected_recurrence_state_ref: context.recurrenceStateRef,
            scope_code: scope,
            profile_patch: {
              ...('title' in changes ? { title: changes.title } : {}),
              ...('description' in changes ? { description: changes.description } : {}),
              ...('location' in changes ? { location: changes.location } : {}),
              ...('colorCode' in changes ? { color_code: changes.colorCode } : {}),
            },
          }),
        },
      );
      if (!response.ok) {
        throw new Error(response.status === 409
          ? 'La ricorrenza o un’istanza futura è cambiata. Ricarica e verifica le modifiche.'
          : 'Non è stato possibile applicare le modifiche alla ricorrenza.');
      }
      const accepted = record(await response.json());
      if (accepted.selected_occurrence_ref !== context.occurrenceRef ||
          accepted.source_native_ref !== context.sourceRef ||
          !Array.isArray(accepted.target_occurrence_refs) ||
          !accepted.target_occurrence_refs.includes(context.occurrenceRef)) {
        throw new Error('La risposta della modifica non corrisponde all’istanza selezionata.');
      }
      const updated = await inspector.get(activityRef);
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return updated;
    },
  });
}
