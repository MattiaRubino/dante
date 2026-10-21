import { createWebFetch } from '../../platform/api/web-fetch';
import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from './remote-activity-inspector';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type RecurringProfileEditScope =
  'only_this' | 'this_and_following' | 'from_next';

export type RecurringProfileEditPreview = Readonly<{
  fingerprint: string;
  editRevision: number;
  recurrenceStateRef: string | null;
  selectedProtection:
    'registration' | 'skipped' | 'local_change' | 'legacy_unknown' | null;
  targetOccurrenceRefs: readonly string[];
  protectedOccurrences: readonly Readonly<{
    occurrenceRef: string;
    expectedAt: string;
    reason: 'registration' | 'skipped' | 'local_change' | 'legacy_unknown';
  }>[];
}>;

export type RecurringProfileContext = Readonly<{
  occurrenceRef: string;
  sourceRef: string;
  editRevision: number;
  recurrenceStateRef: string | null;
}>;

type ProfileChanges = Readonly<
  Partial<
    Pick<ActivityProfile, 'title' | 'description' | 'location' | 'colorCode'>
  >
>;

function record(value: unknown): Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
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
    if (
      !response.ok ||
      value.authenticated !== true ||
      typeof value.csrf_token !== 'string'
    ) {
      throw new Error('Sessione non autenticata.');
    }
    return value.csrf_token;
  }

  async function acceptProfile(
    context: RecurringProfileContext,
    scope: RecurringProfileEditScope,
    changes: ProfileChanges,
    operationId: string,
    preview?: RecurringProfileEditPreview,
  ): Promise<void> {
    if (scope !== 'only_this' && !preview) {
      throw new Error('Controlla le istanze interessate prima di salvare.');
    }
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
          ...(preview
            ? { expected_preview_fingerprint: preview.fingerprint }
            : {}),
          profile_patch: {
            ...('title' in changes ? { title: changes.title } : {}),
            ...('description' in changes
              ? { description: changes.description }
              : {}),
            ...('location' in changes ? { location: changes.location } : {}),
            ...('colorCode' in changes
              ? { color_code: changes.colorCode }
              : {}),
          },
        }),
      },
    );
    if (!response.ok) {
      throw new Error(
        response.status === 409
          ? 'La ricorrenza o un’istanza futura è cambiata. Ricarica e verifica le modifiche.'
          : 'Non è stato possibile applicare le modifiche alla ricorrenza.',
      );
    }
    const accepted = record(await response.json());
    if (
      accepted.selected_occurrence_ref !== context.occurrenceRef ||
      accepted.source_native_ref !== context.sourceRef ||
      !Array.isArray(accepted.target_occurrence_refs) ||
      (scope === 'from_next'
        ? accepted.target_occurrence_refs.includes(context.occurrenceRef)
        : !accepted.target_occurrence_refs.includes(context.occurrenceRef))
    ) {
      throw new Error(
        'La risposta della modifica non corrisponde all’istanza selezionata.',
      );
    }
    invalidateTemporalTimelineRead();
    invalidateTemporalPlanningRead();
  }

  async function loadOccurrenceContext(
    occurrenceRef: string,
  ): Promise<RecurringProfileContext> {
    const state = await read(
      `/api/v1/temporal/occurrences/${encodeURIComponent(occurrenceRef)}/profile-edit-state`,
    );
    if (
      state.selected_occurrence_ref !== occurrenceRef ||
      typeof state.source_native_ref !== 'string' ||
      typeof state.edit_revision !== 'number' ||
      !Number.isSafeInteger(state.edit_revision) ||
      state.edit_revision < 0 ||
      (state.recurrence_state_ref !== null &&
        typeof state.recurrence_state_ref !== 'string')
    ) {
      throw new Error('Versione ricorrente non valida.');
    }
    return {
      occurrenceRef,
      sourceRef: state.source_native_ref,
      editRevision: state.edit_revision,
      recurrenceStateRef: state.recurrence_state_ref,
    };
  }

  return Object.freeze({
    loadOccurrenceContext,
    async loadOccurrencePatch(
      context: RecurringProfileContext,
    ): Promise<
      Readonly<
        Partial<
          Pick<
            ActivityProfile,
            'title' | 'description' | 'location' | 'colorCode'
          >
        >
      >
    > {
      const state = await read(
        `/api/v1/temporal/occurrences/${encodeURIComponent(context.occurrenceRef)}/profile-edit-state`,
      );
      if (
        state.source_native_ref !== context.sourceRef ||
        state.edit_revision !== context.editRevision ||
        state.recurrence_state_ref !== context.recurrenceStateRef
      ) {
        throw new Error(
          'La versione dell’istanza è cambiata. Riapri la modifica.',
        );
      }
      const patch = record(state.current_profile_patch);
      return {
        ...(typeof patch.title === 'string' ? { title: patch.title } : {}),
        ...('description' in patch
          ? { description: patch.description as string | null }
          : {}),
        ...('location' in patch
          ? { location: patch.location as string | null }
          : {}),
        ...('color_code' in patch
          ? { colorCode: patch.color_code as string | null }
          : {}),
      };
    },
    async loadActivityContext(
      activityRef: string,
    ): Promise<RecurringProfileContext | null> {
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
      return loadOccurrenceContext(origin.occurrence_ref);
    },

    async loadPreview(
      context: RecurringProfileContext,
      scope: RecurringProfileEditScope,
    ): Promise<RecurringProfileEditPreview> {
      const value = await read(
        `/api/v1/temporal/occurrences/${encodeURIComponent(context.occurrenceRef)}/profile-edit-preview?scope_code=${scope}`,
      );
      if (
        value.source_native_ref !== context.sourceRef ||
        value.edit_revision !== context.editRevision ||
        value.recurrence_state_ref !== context.recurrenceStateRef ||
        typeof value.fingerprint !== 'string' ||
        !/^[0-9a-f]{32}$/.test(value.fingerprint) ||
        !Array.isArray(value.target_occurrence_refs) ||
        !value.target_occurrence_refs.every((ref) => typeof ref === 'string') ||
        !Array.isArray(value.protected_occurrences) ||
        !value.protected_occurrences.every((row: unknown) => {
          const item = record(row);
          return (
            typeof item.occurrence_ref === 'string' &&
            typeof item.expected_at === 'string' &&
            typeof item.reason === 'string' &&
            [
              'registration',
              'skipped',
              'local_change',
              'legacy_unknown',
            ].includes(item.reason)
          );
        }) ||
        (value.selected_protection !== null &&
          ![
            'registration',
            'skipped',
            'local_change',
            'legacy_unknown',
          ].includes(value.selected_protection as string))
      ) {
        throw new Error('Anteprima ricorrenza cambiata: ricarica la modifica.');
      }
      return {
        fingerprint: value.fingerprint,
        editRevision: context.editRevision,
        recurrenceStateRef: context.recurrenceStateRef,
        selectedProtection:
          value.selected_protection as RecurringProfileEditPreview['selectedProtection'],
        targetOccurrenceRefs: value.target_occurrence_refs,
        protectedOccurrences: value.protected_occurrences.map(
          (row: unknown) => {
            const item = record(row);
            return {
              occurrenceRef: String(item.occurrence_ref),
              expectedAt: String(item.expected_at),
              reason: item.reason as
                'registration' | 'skipped' | 'local_change' | 'legacy_unknown',
            };
          },
        ),
      };
    },

    async saveActivityProfile(
      activityRef: string,
      context: RecurringProfileContext,
      scope: RecurringProfileEditScope,
      changes: ProfileChanges,
      operationId: string,
      preview?: RecurringProfileEditPreview,
    ): Promise<ActivityProfile> {
      await acceptProfile(context, scope, changes, operationId, preview);
      const updated = await inspector.get(activityRef);
      return updated;
    },
    saveEventProfile: acceptProfile,
  });
}
