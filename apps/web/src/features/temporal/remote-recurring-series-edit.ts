import { createWebFetch } from '../../platform/api/web-fetch';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type SeriesScope = 'this_and_following' | 'from_next';

export type RecurringSeriesSource = Readonly<{
  sourceRef: string;
  owner: 'routine' | 'event';
  selectedDate: string;
  editRevision: number;
  recurrenceStateRef: string;
  title: string;
  description: string | null;
  location: string | null;
  colorCode: string | null;
  recurrence: Record<string, unknown>;
  structure: Record<string, unknown>;
  remainingIncludingSelected?: number | null;
  remainingAfterSelected?: number | null;
}>;

export type RecurringSeriesReview = Readonly<{
  fingerprint: string;
  targetRefs: readonly string[];
  newExpectedCount: number;
  protected: readonly Readonly<{
    occurrenceRef: string;
    expectedAt: string;
    reason: string;
  }>[];
}>;

type Intent = Readonly<{
  selectedRef: string;
  source: RecurringSeriesSource;
  scope: SeriesScope;
  recurrence: Record<string, unknown>;
  structure: Record<string, unknown>;
  profilePatch: Record<string, string | null> | null;
  operationId: string;
}>;

function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta della ricorrenza non valida.');
  }
  return value as Record<string, unknown>;
}

function protectedRows(value: unknown): RecurringSeriesReview['protected'] {
  if (!Array.isArray(value)) throw new Error('Anteprima incompleta.');
  return value.map((raw: unknown) => {
    const row = object(raw);
    if (
      typeof row.occurrence_ref !== 'string' ||
      typeof row.expected_at !== 'string' ||
      typeof row.reason !== 'string'
    ) {
      throw new Error('Eccezione futura non valida.');
    }
    return {
      occurrenceRef: row.occurrence_ref,
      expectedAt: row.expected_at,
      reason: row.reason,
    };
  });
}

export function createRemoteRecurringSeriesEdit(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const path = (ref: string, action: string) =>
    `/api/v1/temporal/occurrences/${encodeURIComponent(ref)}/${action}`;

  async function read(response: Response): Promise<Record<string, unknown>> {
    const value = object(await response.json());
    if (!response.ok) {
      throw new Error(
        response.status === 409
          ? 'La ricorrenza o una delle istanze è cambiata. Riapri Modifica e controlla le eccezioni.'
          : typeof value.detail === 'string'
            ? value.detail
            : 'Impossibile leggere o salvare la ricorrenza.',
      );
    }
    return value;
  }

  async function csrf(): Promise<string> {
    const value = await read(await request('/api/v1/auth/session'));
    if (value.authenticated !== true || typeof value.csrf_token !== 'string') {
      throw new Error('Sessione non autenticata.');
    }
    return value.csrf_token;
  }

  function body(intent: Intent, fingerprint: string | null) {
    return {
      operation_id: intent.operationId,
      expected_revision: intent.source.editRevision,
      expected_recurrence_state_ref: intent.source.recurrenceStateRef,
      scope_code: intent.scope,
      recurrence: intent.recurrence,
      structure_snapshot: intent.structure,
      profile_patch: intent.profilePatch,
      ...(fingerprint ? { expected_preview_fingerprint: fingerprint } : {}),
    };
  }

  return Object.freeze({
    async load(selectedRef: string): Promise<RecurringSeriesSource> {
      const value = await read(
        await request(path(selectedRef, 'series-edit-source')),
      );
      if (
        typeof value.source_native_ref !== 'string' ||
        (value.owner_kind !== 'routine' && value.owner_kind !== 'event') ||
        typeof value.selected_date !== 'string' ||
        !Number.isSafeInteger(value.edit_revision) ||
        typeof value.recurrence_state_ref !== 'string' ||
        typeof value.title !== 'string'
      ) {
        throw new Error('Stato della serie incompleto.');
      }
      const finite = object(value.recurrence).range_kind === 'expected_count';
      const inclusive = value.remaining_including_selected;
      const exclusive = value.remaining_after_selected;
      if (
        finite &&
        (
          !Number.isSafeInteger(inclusive) ||
          !Number.isSafeInteger(exclusive) ||
          (inclusive as number) < 1 ||
          (exclusive as number) < 0 ||
          (inclusive as number) <= (exclusive as number)
        )
      ) {
        throw new Error('Limite della serie finita non coerente.');
      }
      if (
        !finite &&
        (
          (inclusive !== null && inclusive !== undefined) ||
          (exclusive !== null && exclusive !== undefined)
        )
      ) {
        throw new Error('Limite della serie non coerente.');
      }
      return {
        sourceRef: value.source_native_ref,
        owner: value.owner_kind,
        selectedDate: value.selected_date,
        editRevision: value.edit_revision as number,
        recurrenceStateRef: value.recurrence_state_ref,
        title: value.title,
        description:
          typeof value.description === 'string' ? value.description : null,
        location: typeof value.location === 'string' ? value.location : null,
        colorCode:
          typeof value.color_code === 'string' ? value.color_code : null,
        recurrence: object(value.recurrence),
        structure: object(value.structure_snapshot),
        remainingIncludingSelected: finite ? inclusive as number : null,
        remainingAfterSelected: finite ? exclusive as number : null,
      };
    },
    async preview(intent: Intent): Promise<RecurringSeriesReview> {
      const value = await read(
        await request(path(intent.selectedRef, 'series-edit-preview'), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify(body(intent, null)),
        }),
      );
      if (
        value.source_native_ref !== intent.source.sourceRef ||
        value.owner_kind !== intent.source.owner ||
        value.selected_occurrence_ref !== intent.selectedRef ||
        typeof value.fingerprint !== 'string' ||
        !/^[0-9a-f]{64}$/.test(value.fingerprint) ||
        !Array.isArray(value.target_occurrence_refs) ||
        !value.target_occurrence_refs.every(
          (ref: unknown) => typeof ref === 'string',
        ) ||
        !Number.isSafeInteger(value.new_expected_count)
      ) {
        throw new Error('Anteprima della serie non coerente.');
      }
      return {
        fingerprint: value.fingerprint,
        targetRefs: value.target_occurrence_refs,
        newExpectedCount: value.new_expected_count as number,
        protected: protectedRows(value.protected_occurrences),
      };
    },
    async accept(intent: Intent, review: RecurringSeriesReview): Promise<void> {
      const value = await read(
        await request(path(intent.selectedRef, 'series-edit'), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify(body(intent, review.fingerprint)),
        }),
      );
      // A converted Event's original physical first Occurrence remains
      // current, so it is targeted by the edit but not superseded. Only
      // an explicitly identified selected-first Event can reduce the count.
      const preserved = value.preserved_occurrence_ref;
      const preservedFirst =
        typeof preserved === 'string' &&
        intent.source.owner === 'event' &&
        intent.scope === 'this_and_following' &&
        preserved === intent.selectedRef &&
        review.targetRefs.filter((ref) => ref === preserved).length === 1;
      const preservationValid = preserved === null || preservedFirst;
      const expectedSuperseded =
        review.targetRefs.length - (preservedFirst ? 1 : 0);
      if (
        value.source_native_ref !== intent.source.sourceRef ||
        typeof value.recurrence_state_ref !== 'string' ||
        !preservationValid ||
        !Number.isSafeInteger(value.superseded_count) ||
        value.superseded_count !== expectedSuperseded ||
        value.protected_count !== review.protected.length
      ) {
        throw new Error(
          'Conferma della serie non coerente. Ricarica la Timeline.',
        );
      }
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
    },
  });
}
