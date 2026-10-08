import { createWebFetch } from '../../platform/api/web-fetch';
import { parseProfile, type ActivityProfile } from './remote-activity-inspector';
import { invalidateTemporalPlanningRead, invalidateTemporalTimelineRead } from './timeline-invalidation';
import {
  parseObjectiveView,
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
  zoneId: string | null;
}>;

export type ActivityEditSettings = Readonly<{
  capture: ActivityEditPolicy<SessionCaptureMode>;
  reality: ActivityEditPolicy<RealityMode>;
  schedules: readonly ActivityEditSchedule[];
  objectives: readonly ObjectiveView[];
  lifeAreaRef: string | null;
  placementProtected: boolean;
  reminderLeadMinutes: number | null;
  childGuardMode: 'none' | 'confirm' | 'block';
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
        zoneId: optionalText(row.zone_id),
      });
    }),
  );
}

export function createRemoteActivityEditSettings(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
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

  return Object.freeze({
    async load(ref: string): Promise<ActivityEditSettings> {
      const snapshot = object(await read(endpoint(ref, 'edit-snapshot')));
      if (snapshot.activity_ref !== ref || !Array.isArray(snapshot.objectives)) {
        throw new Error('Identità dell’attività non valida.');
      }
      const acceptedSchedules = schedules({
        parent_activity_ref: ref,
        schedules: snapshot.schedules,
      }, ref);
      if (
        !['none', 'confirm', 'block'].includes(
          String(snapshot.child_guard_mode),
        )
      ) {
        throw new Error('Regola dell’attività non valida.');
      }
      const lock = snapshot.placement_lock === null ? null : object(snapshot.placement_lock);
      const reminder = snapshot.reminder === null ? null : object(snapshot.reminder);
      const primary = acceptedSchedules.find((item) => item.role === 'envelope') ??
        acceptedSchedules.find((item) => item.role === null);
      if ((lock !== null && (lock.schedule_ref !== primary?.scheduleRef || typeof lock.locked !== 'boolean')) ||
          (reminder !== null && (typeof reminder.enabled !== 'boolean' ||
            !Number.isInteger(reminder.lead_minutes)))) {
        throw new Error('Blocco o promemoria dell’attività non valido.');
      }
      return Object.freeze({
        capture: capture(snapshot.execution_policy, ref),
        reality: reality(snapshot.reality_policy, ref),
        schedules: acceptedSchedules,
        objectives: Object.freeze(snapshot.objectives.map(parseObjectiveView)),
        lifeAreaRef: optionalText(snapshot.life_area_ref),
        placementProtected: lock?.locked === true,
        reminderLeadMinutes: reminder?.enabled === true ? Number(reminder.lead_minutes) : null,
        childGuardMode:
          snapshot.child_guard_mode as ActivityEditSettings['childGuardMode'],
      });
    },
    async saveCore(
      profile: ActivityProfile,
      settings: ActivityEditSettings,
      changes: Readonly<{
        profile?: Pick<ActivityProfile, 'title' | 'description' | 'location' | 'colorCode'>;
        capture?: SessionCaptureMode;
        reality?: RealityMode;
      }>,
      operationId: string,
    ): Promise<{ profile: ActivityProfile; settings: ActivityEditSettings }> {
      const response = await request(endpoint(profile.activityRef, 'core-edit'), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await csrf(),
        },
        body: JSON.stringify({
          operation_id: operationId,
          ...(changes.profile ? { profile: {
            expected_revision: profile.revision,
            title: changes.profile.title,
            description: changes.profile.description,
            location: changes.profile.location,
            color_code: changes.profile.colorCode,
          } } : {}),
          ...(changes.capture ? { capture: {
            mode_code: changes.capture,
            expected_state_ref: settings.capture.stateRef,
          } } : {}),
          ...(changes.reality ? { reality: {
            mode_code: changes.reality,
            expected_state_ref: settings.reality.stateRef,
          } } : {}),
        }),
      });
      if (!response.ok) throw new Error(response.status === 409
        ? 'L’attività è cambiata. Riapri Modifica e riprova.'
        : 'Impossibile salvare le impostazioni dell’attività.');
      const result = object(await response.json());
      const savedProfile = parseProfile(result.profile);
      if (savedProfile.activityRef !== profile.activityRef) {
        throw new Error('Identità dell’attività non valida.');
      }
      const savedSettings = Object.freeze({
        ...settings,
        capture: capture(result.capture, profile.activityRef),
        reality: reality(result.reality, profile.activityRef),
      });
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return { profile: savedProfile, settings: savedSettings };
    },
  });
}
