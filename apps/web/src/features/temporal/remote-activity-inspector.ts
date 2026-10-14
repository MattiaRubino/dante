import { createWebFetch } from '../../platform/api/web-fetch';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type ActivityProfile = Readonly<{
  activityRef: string;
  title: string;
  description: string | null;
  location: string | null;
  colorCode: string | null;
  revision: number;
}>;

export type ActivitySessionImpact = Readonly<{
  fingerprint: string;
  attempts: readonly Readonly<{
    sessionRef: string;
    plannedScheduleRef: string | null;
    timingMaterialStateRef: string;
    status: 'in corso' | 'in pausa' | 'conclusa';
  }>[];
}>;

function parseSessionImpact(value: unknown): ActivitySessionImpact {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Stato delle Sessioni non valido.');
  }
  const record = value as Record<string, unknown>;
  if (
    typeof record.fingerprint !== 'string' ||
    !/^[a-f0-9]{64}$/.test(record.fingerprint) ||
    !Array.isArray(record.attempts)
  ) {
    throw new Error('Stato delle Sessioni non valido.');
  }
  const attempts = record.attempts.map((item: unknown) => {
    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      throw new Error('Tentativo Sessione non valido.');
    }
    const row = item as Record<string, unknown>;
    if (
      typeof row.session_ref !== 'string' ||
      typeof row.timing_material_state_ref !== 'string' ||
      (row.planned_schedule_ref !== null &&
        typeof row.planned_schedule_ref !== 'string') ||
      (row.status !== 'in corso' &&
        row.status !== 'in pausa' &&
        row.status !== 'conclusa')
    ) {
      throw new Error('Tentativo Sessione non valido.');
    }
    const status: ActivitySessionImpact['attempts'][number]['status'] =
      row.status;
    return {
      sessionRef: row.session_ref,
      plannedScheduleRef: row.planned_schedule_ref,
      timingMaterialStateRef: row.timing_material_state_ref,
      status,
    };
  });
  return { fingerprint: record.fingerprint, attempts };
}

export function parseProfile(value: unknown): ActivityProfile {
  if (!value || typeof value !== 'object' || Array.isArray(value))
    throw new Error('Risposta non valida.');
  const row = value as Record<string, unknown>;
  if (
    typeof row.activity_ref !== 'string' ||
    typeof row.title !== 'string' ||
    typeof row.revision !== 'number' ||
    ![row.description, row.location, row.color_code].every(
      (field) => field === null || typeof field === 'string',
    )
  ) {
    throw new Error('Risposta non valida.');
  }
  return {
    activityRef: row.activity_ref,
    title: row.title,
    description: row.description as string | null,
    location: row.location as string | null,
    colorCode: row.color_code as string | null,
    revision: row.revision,
  };
}

async function checked(response: Response): Promise<unknown> {
  const body: unknown = await response.json();
  if (!response.ok) {
    const code =
      typeof body === 'object' && body !== null
        ? (body as Record<string, unknown>).code
        : null;
    throw new Error(
      code === 'temporal.activity_profile.active_session'
        ? 'Termina prima la sessione attiva su questa attività.'
        : code === 'temporal.activity_profile.recorded_truth'
          ? 'L’attività contiene sessioni o risultati registrati: correggi i dati storici senza eliminarli.'
          : response.status === 409
            ? 'L’attività è cambiata. Aggiorna e riprova.'
            : response.status === 404
              ? 'Attività non disponibile.'
              : 'Operazione non riuscita. Riprova.',
    );
  }
  return body;
}

export function createRemoteActivityInspector(
  fetchFn: typeof fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const url = (ref: string) =>
    `/api/v1/temporal/activities/${encodeURIComponent(ref)}`;
  async function csrf() {
    const session = (await checked(
      await request('/api/v1/auth/session'),
    )) as Record<string, unknown>;
    if (
      session.authenticated !== true ||
      typeof session.csrf_token !== 'string'
    ) {
      throw new Error('Sessione non autenticata.');
    }
    return session.csrf_token;
  }
  return {
    async get(ref: string): Promise<ActivityProfile> {
      return parseProfile(await checked(await request(`${url(ref)}/profile`)));
    },
    async revise(
      current: ActivityProfile,
      changed: Pick<
        ActivityProfile,
        'title' | 'description' | 'location' | 'colorCode'
      >,
    ) {
      const token = await csrf();
      const next = parseProfile(
        await checked(
          await request(`${url(current.activityRef)}/profile`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-Dante-CSRF': token,
            },
            body: JSON.stringify({
              operation_id: crypto.randomUUID(),
              expected_revision: current.revision,
              title: changed.title,
              description: changed.description,
              location: changed.location,
              color_code: changed.colorCode,
            }),
          }),
        ),
      );
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return next;
    },
    async sessionImpact(ref: string): Promise<ActivitySessionImpact> {
      return parseSessionImpact(
        await checked(await request(`${url(ref)}/session-impact`)),
      );
    },
    async deleteHard(ref: string, expectedSessionFingerprint: string) {
      const token = await csrf();
      await checked(
        await request(url(ref), {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': token,
          },
          body: JSON.stringify({
            expected_session_fingerprint: expectedSessionFingerprint,
          }),
        }),
      );
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
    },
    async retire(ref: string) {
      const token = await csrf();
      await checked(
        await request(`${url(ref)}/retire`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': token,
          },
          body: JSON.stringify({ operation_id: crypto.randomUUID() }),
        }),
      );
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
    },
  };
}
