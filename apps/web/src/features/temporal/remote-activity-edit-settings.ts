import { createWebFetch } from '../../platform/api/web-fetch';
import {
  createRemoteRealityObjectiveDataSource,
  type ObjectiveView,
  type RealityMode,
} from './remote-reality-objective-data-source';
import type { SessionCaptureMode } from './remote-session-capability-data-source';

export type ActivityEditPolicy<T extends string> = Readonly<{
  mode: T;
  stateRef: string | null;
}>;

export type ActivityEditSchedule = Readonly<{
  scheduleRef: string;
  role: 'envelope' | 'interval' | 'planned' | null;
  name: string | null;
  order: number | null;
  placementStateRef: string;
  temporalForm: string;
  start: string | null;
  end: string | null;
}>;

export type ActivityEditSettings = Readonly<{
  capture: ActivityEditPolicy<SessionCaptureMode>;
  reality: ActivityEditPolicy<RealityMode>;
  schedules: readonly ActivityEditSchedule[];
  objectives: readonly ObjectiveView[];
}>;

function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Le impostazioni dell’attività non sono leggibili.');
  }
  return value as Record<string, unknown>;
}

function optionalText(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  if (typeof value !== 'string') throw new Error('Valore attività non valido.');
  return value;
}

function state(value: unknown): string | null {
  return optionalText(value);
}

function capture(
  value: unknown,
  ref: string,
): ActivityEditPolicy<SessionCaptureMode> {
  const row = object(value);
  if (
    row.activity_ref !== ref ||
    !['disabled', 'record', 'live', 'record_and_live'].includes(
      String(row.mode_code),
    )
  ) {
    throw new Error('Modalità delle sessioni non valida.');
  }
  return {
    mode: row.mode_code as SessionCaptureMode,
    stateRef: state(row.state_ref),
  };
}

function reality(value: unknown, ref: string): ActivityEditPolicy<RealityMode> {
  const row = object(value);
  if (
    row.subject_kind !== 'activity' ||
    row.subject_native_ref !== ref ||
    !['manual', 'review_on_end', 'auto_confirm_outcome'].includes(
      String(row.mode_code),
    )
  ) {
    throw new Error('Verifica esito non valida.');
  }
  return { mode: row.mode_code as RealityMode, stateRef: state(row.state_ref) };
}

function schedules(
  value: unknown,
  ref: string,
): readonly ActivityEditSchedule[] {
  const payload = object(value);
  if (
    payload.parent_activity_ref !== ref ||
    !Array.isArray(payload.schedules)
  ) {
    throw new Error('Intervalli dell’attività non validi.');
  }
  return Object.freeze(
    payload.schedules.map((value: unknown) => {
      const row = object(value);
      if (
        typeof row.schedule_ref !== 'string' ||
        typeof row.placement_material_state_ref !== 'string' ||
        typeof row.temporal_form !== 'string' ||
        ![null, 'envelope', 'interval', 'planned'].includes(
          row.role_code as string | null,
        )
      ) {
        throw new Error('Schedule dell’attività non valido.');
      }
      return Object.freeze({
        scheduleRef: row.schedule_ref,
        role: row.role_code as ActivityEditSchedule['role'],
        name: optionalText(row.display_name),
        order:
          typeof row.presentation_order === 'number'
            ? row.presentation_order
            : null,
        placementStateRef: row.placement_material_state_ref,
        temporalForm: row.temporal_form,
        start: optionalText(
          row.starts_local_at ??
            row.starts_at ??
            row.start_date ??
            row.local_date,
        ),
        end: optionalText(
          row.ends_local_at ?? row.ends_at ?? row.end_date_exclusive,
        ),
      });
    }),
  );
}

export function createRemoteActivityEditSettings(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const objectiveSource = createRemoteRealityObjectiveDataSource(fetchFn);
  const endpoint = (ref: string, suffix: string) =>
    `/api/v1/temporal/activities/${encodeURIComponent(ref)}/${suffix}`;

  async function read(path: string): Promise<unknown> {
    const response = await request(path);
    if (!response.ok)
      throw new Error('Impossibile caricare le impostazioni dell’attività.');
    return response.json();
  }

  async function csrf(): Promise<string> {
    const response = await request('/api/v1/auth/session');
    const row = object(await response.json());
    if (
      !response.ok ||
      row.authenticated !== true ||
      typeof row.csrf_token !== 'string'
    ) {
      throw new Error('Sessione non autenticata.');
    }
    return row.csrf_token;
  }

  async function set<T extends string>(
    ref: string,
    suffix: string,
    mode: T,
    expectedStateRef: string | null,
    operationId: string,
  ): Promise<unknown> {
    const response = await request(endpoint(ref, suffix), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      },
      body: JSON.stringify({
        operation_id: operationId,
        mode_code: mode,
        expected_state_ref: expectedStateRef,
      }),
    });
    if (!response.ok) {
      throw new Error(
        response.status === 409
          ? 'Questa impostazione è cambiata. Riapri Modifica e riprova.'
          : 'Impossibile salvare le impostazioni dell’attività.',
      );
    }
    return response.json();
  }

  return Object.freeze({
    async load(ref: string): Promise<ActivityEditSettings> {
      const [capturePayload, realityPayload, schedulePayload, objectives] =
        await Promise.all([
          read(endpoint(ref, 'execution-policy')),
          read(endpoint(ref, 'reality-policy')),
          read(endpoint(ref, 'children')),
          objectiveSource.listObjectives('activity', ref),
        ]);
      return Object.freeze({
        capture: capture(capturePayload, ref),
        reality: reality(realityPayload, ref),
        schedules: schedules(schedulePayload, ref),
        objectives,
      });
    },
    async setCapture(
      ref: string,
      policy: ActivityEditPolicy<SessionCaptureMode>,
      mode: SessionCaptureMode,
      operationId: string,
    ) {
      return capture(
        await set(ref, 'execution-policy', mode, policy.stateRef, operationId),
        ref,
      );
    },
    async setReality(
      ref: string,
      policy: ActivityEditPolicy<RealityMode>,
      mode: RealityMode,
      operationId: string,
    ) {
      return reality(
        await set(ref, 'reality-policy', mode, policy.stateRef, operationId),
        ref,
      );
    },
  });
}
