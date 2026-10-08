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
  placementLockRevision: number | null;
  placementLockScheduleRef: string | null;
  reminderLeadMinutes: number | null;
  reminderScheduleRef: string | null;
  reminderStateRef: string | null;
  childGuardMode: 'none' | 'confirm' | 'block';
}>;

export type ActivityLifeAreaChoice = Readonly<{
  options: readonly Readonly<{ ref: string; name: string }>[];
  currentRef: string | null;
  currentRevision: number;
}>;

export type ActivityReplanTime = Readonly<{ start: string; end: string }>;
export type ActivityNewPlanned = Readonly<ActivityReplanTime & { clientRef: string; name: string }>;
export type ActivityNewInterval = Readonly<ActivityReplanTime & { clientRef: string }>;
export type ActivityReplanDraft = Readonly<{
  times: Record<string, ActivityReplanTime>;
  removedIntervals: readonly string[];
  newIntervals: readonly ActivityNewInterval[];
  removedPlanned: readonly string[];
  newPlanned: readonly ActivityNewPlanned[];
}>;
export type ActivityReplanChange = Readonly<{
  scheduleRef: string | null;
  clientRef: string | null;
  role: string;
  previousStart: string | null;
  previousEnd: string | null;
  proposedStart: string | null;
  proposedEnd: string | null;
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

  function parseSnapshot(ref: string, value: unknown): ActivityEditSettings {
      const snapshot = object(value);
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
          (reminder !== null && (reminder.schedule_ref !== primary?.scheduleRef ||
            typeof reminder.material_state_ref !== 'string' ||
            typeof reminder.enabled !== 'boolean' ||
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
        placementLockRevision: lock === null ? null : Number(lock.revision),
        placementLockScheduleRef: lock === null ? null : String(lock.schedule_ref),
        reminderLeadMinutes: reminder?.enabled === true ? Number(reminder.lead_minutes) : null,
        reminderScheduleRef: primary?.role === 'envelope' &&
          ['named_zone_local', 'absolute'].includes(primary.temporalForm)
          ? primary.scheduleRef : null,
        reminderStateRef: reminder ? state(reminder.material_state_ref) : null,
        childGuardMode:
          snapshot.child_guard_mode as ActivityEditSettings['childGuardMode'],
      });
  }

  function replanBody(
    settings: ActivityEditSettings,
    draft: ActivityReplanDraft,
    operationId: string,
  ) {
    const row = (item: ActivityEditSchedule) => ({
      schedule_ref: item.scheduleRef,
      expected_material_state_ref: item.placementStateRef,
      starts_local_at: draft.times[item.scheduleRef]?.start,
      ends_local_at: draft.times[item.scheduleRef]?.end,
    });
    return {
      operation_id: operationId,
      intervals: settings.schedules.filter((item) =>
        item.role === 'interval' && !draft.removedIntervals.includes(item.scheduleRef)).map(row),
      remove_intervals: settings.schedules.filter((item) =>
        item.role === 'interval' && draft.removedIntervals.includes(item.scheduleRef)).map(row),
      new_intervals: draft.newIntervals.map((item) => ({
        client_ref: item.clientRef,
        starts_local_at: item.start, ends_local_at: item.end,
      })),
      planned_sessions: settings.schedules.filter((item) =>
        item.role === 'planned' && !draft.removedPlanned.includes(item.scheduleRef)).map(row),
      remove_planned_sessions: settings.schedules.filter((item) =>
        item.role === 'planned' && draft.removedPlanned.includes(item.scheduleRef)).map(row),
      new_planned_sessions: draft.newPlanned.map((item) => ({
        client_ref: item.clientRef, name: item.name.trim() || null,
        starts_local_at: item.start, ends_local_at: item.end,
      })),
    };
  }

  return Object.freeze({
    async load(ref: string): Promise<ActivityEditSettings> {
      return parseSnapshot(ref, await read(endpoint(ref, 'edit-snapshot')));
    },
    async previewReplan(
      ref: string, settings: ActivityEditSettings,
      draft: ActivityReplanDraft,
      operationId: string,
    ): Promise<readonly ActivityReplanChange[]> {
      const response = await request(endpoint(ref, 'replan-preview'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
        body: JSON.stringify(replanBody(settings, draft, operationId)),
      });
      if (!response.ok) throw new Error(response.status === 409
        ? 'La programmazione è cambiata. Riapri Modifica e riprova.'
        : 'La proposta non è valida. Controlla gli intervalli e le sessioni.');
      const result = object(await response.json());
      if (result.activity_ref !== ref || !Array.isArray(result.changes)) {
        throw new Error('Anteprima della programmazione non valida.');
      }
      return result.changes.map((value: unknown) => {
        const row = object(value);
        if ((row.schedule_ref != null && typeof row.schedule_ref !== 'string') ||
            (row.client_ref != null && typeof row.client_ref !== 'string') ||
            typeof row.role !== 'string' ||
            (row.previous_start != null && typeof row.previous_start !== 'string') ||
            (row.previous_end != null && typeof row.previous_end !== 'string') ||
            (row.proposed_start != null && typeof row.proposed_start !== 'string') ||
            (row.proposed_end != null && typeof row.proposed_end !== 'string')) {
          throw new Error('Riga dell’anteprima non valida.');
        }
        return {
          scheduleRef: optionalText(row.schedule_ref), clientRef: optionalText(row.client_ref), role: row.role,
          previousStart: optionalText(row.previous_start), previousEnd: optionalText(row.previous_end),
          proposedStart: optionalText(row.proposed_start), proposedEnd: optionalText(row.proposed_end),
        };
      });
    },
    async applyReplan(
      ref: string, settings: ActivityEditSettings,
      draft: ActivityReplanDraft,
      operationId: string,
    ): Promise<ActivityEditSettings> {
      const response = await request(endpoint(ref, 'replan'), {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
        body: JSON.stringify(replanBody(settings, draft, operationId)),
      });
      if (!response.ok) throw new Error(response.status === 409
        ? 'La programmazione è cambiata o è protetta. Riapri Modifica e riprova.'
        : 'Impossibile salvare la programmazione.');
      const saved = parseSnapshot(ref, await response.json());
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return saved;
    },
    async loadLifeAreaChoice(ref: string): Promise<ActivityLifeAreaChoice> {
      const [rawAreas, rawAssignments] = await Promise.all([
        read('/api/v1/temporal/life-areas'),
        read('/api/v1/temporal/life-area-assignments'),
      ]);
      if (!Array.isArray(rawAreas) || !Array.isArray(rawAssignments)) {
        throw new Error('Catalogo Life Area non valido.');
      }
      const options = rawAreas.map(object)
        .filter((item) => item.archived === false)
        .map((item) => {
          if (typeof item.life_area_ref !== 'string' ||
              typeof item.name !== 'string' || !item.name.trim()) {
            throw new Error('Life Area non valida.');
          }
          return Object.freeze({ ref: item.life_area_ref, name: item.name });
        });
      const rows = rawAssignments.map(object).filter((item) =>
        item.subject_kind === 'activity' && item.subject_native_ref === ref);
      if (rows.length > 1) {
        throw new Error('Assegnazioni Life Area incoerenti.');
      }
      const current = rows[0];
      if (current && (typeof current.life_area_ref !== 'string' ||
          typeof current.assignment_revision !== 'number' ||
          !Number.isSafeInteger(current.assignment_revision) ||
          current.assignment_revision < 1)) {
        throw new Error('Revisione Life Area non valida.');
      }
      return Object.freeze({
        options: Object.freeze(options),
        currentRef: current ? String(current.life_area_ref) : null,
        currentRevision: current ? Number(current.assignment_revision) : 0,
      });
    },
    async assignLifeArea(
      ref: string,
      current: ActivityLifeAreaChoice,
      nextRef: string,
      operationId: string,
    ): Promise<ActivityLifeAreaChoice> {
      if (!current.options.some((area) => area.ref === nextRef)) {
        throw new Error('Seleziona una Life Area valida.');
      }
      const response = await request(
        `/api/v1/temporal/life-area-assignments/activities/${encodeURIComponent(ref)}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify({
            operation_id: operationId,
            life_area_ref: nextRef,
            expected_assignment_revision: current.currentRevision,
          }),
        },
      );
      if (!response.ok) {
        throw new Error(response.status === 409
          ? 'La Life Area è cambiata. Ricarica l’attività e riprova.'
          : 'Impossibile aggiornare la Life Area.');
      }
      const saved = object(await response.json());
      if (saved.subject_kind !== 'activity' || saved.subject_native_ref !== ref ||
          saved.life_area_ref !== nextRef ||
          !Number.isSafeInteger(saved.assignment_revision) ||
          Number(saved.assignment_revision) <= current.currentRevision) {
        throw new Error('Assegnazione Life Area non valida.');
      }
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return Object.freeze({
        ...current,
        currentRef: nextRef,
        currentRevision: Number(saved.assignment_revision),
      });
    },
    async setPlacementProtected(
      settings: ActivityEditSettings,
      locked: boolean,
    ): Promise<ActivityEditSettings> {
      if (!settings.placementLockScheduleRef || settings.placementLockRevision === null) {
        throw new Error('La protezione non è disponibile per questa attività.');
      }
      const scheduleRef = settings.placementLockScheduleRef;
      const response = await request(
        `/api/v1/temporal/schedules/${encodeURIComponent(scheduleRef)}/placement-lock`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          },
          body: JSON.stringify({
            locked,
            expected_revision: settings.placementLockRevision,
          }),
        },
      );
      if (!response.ok) {
        throw new Error(response.status === 409
          ? 'La protezione è cambiata. Ricarica l’attività e riprova.'
          : 'Impossibile aggiornare la protezione della collocazione.');
      }
      const saved = object(await response.json());
      if (saved.schedule_ref !== scheduleRef ||
          saved.locked !== locked ||
          !Number.isInteger(saved.revision)) {
        throw new Error('Risposta non valida per la protezione della collocazione.');
      }
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return Object.freeze({
        ...settings,
        placementProtected: locked,
        placementLockRevision: Number(saved.revision),
      });
    },
    async saveCore(
      profile: ActivityProfile,
      settings: ActivityEditSettings,
      changes: Readonly<{
        profile?: Pick<ActivityProfile, 'title' | 'description' | 'location' | 'colorCode'>;
        capture?: SessionCaptureMode;
        reality?: RealityMode;
        reminderLeadMinutes?: number | null;
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
          ...('reminderLeadMinutes' in changes && settings.reminderScheduleRef ? {
            reminder: {
              schedule_ref: settings.reminderScheduleRef,
              expected_state_ref: settings.reminderStateRef,
              enabled: changes.reminderLeadMinutes !== null,
              lead_minutes: changes.reminderLeadMinutes ?? 0,
            },
          } : {}),
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
        ...('reminderLeadMinutes' in changes ? {
          reminderLeadMinutes: changes.reminderLeadMinutes ?? null,
          reminderStateRef: state(object(result.reminder).material_state_ref),
        } : {}),
      });
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return { profile: savedProfile, settings: savedSettings };
    },
  });
}
