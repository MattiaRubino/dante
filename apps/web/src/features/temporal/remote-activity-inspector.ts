import { createWebFetch } from '../../platform/api/web-fetch';
import { invalidateTemporalPlanningRead, invalidateTemporalTimelineRead } from './timeline-invalidation';

export type ActivityProfile = Readonly<{
  activityRef: string;
  title: string;
  description: string | null;
  location: string | null;
  colorCode: string | null;
  revision: number;
}>;

function parseProfile(value: unknown): ActivityProfile {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Risposta non valida.');
  const row = value as Record<string, unknown>;
  if (typeof row.activity_ref !== 'string' || typeof row.title !== 'string' ||
      typeof row.revision !== 'number' ||
      ![row.description, row.location, row.color_code].every((field) =>
        field === null || typeof field === 'string')) {
    throw new Error('Risposta non valida.');
  }
  return {
    activityRef: row.activity_ref, title: row.title,
    description: row.description as string | null,
    location: row.location as string | null,
    colorCode: row.color_code as string | null,
    revision: row.revision,
  };
}

async function checked(response: Response): Promise<unknown> {
  const body: unknown = await response.json();
  if (!response.ok) {
    const code = typeof body === 'object' && body !== null
      ? (body as Record<string, unknown>).code : null;
    throw new Error(
      code === 'temporal.activity_profile.active_session'
        ? 'Termina prima la sessione attiva su questa attività.'
        : response.status === 409
          ? 'L’attività è cambiata. Aggiorna e riprova.'
          : response.status === 404
            ? 'Attività non disponibile.'
            : 'Operazione non riuscita. Riprova.',
    );
  }
  return body;
}

export function createRemoteActivityInspector(fetchFn: typeof fetch = globalThis.fetch) {
  const request = createWebFetch(fetchFn);
  const url = (ref: string) => `/api/v1/temporal/activities/${encodeURIComponent(ref)}`;
  async function csrf() {
    const session = (await checked(await request('/api/v1/auth/session'))) as Record<string, unknown>;
    if (session.authenticated !== true || typeof session.csrf_token !== 'string') {
      throw new Error('Sessione non autenticata.');
    }
    return session.csrf_token;
  }
  return {
    async get(ref: string): Promise<ActivityProfile> {
      return parseProfile(await checked(await request(`${url(ref)}/profile`)));
    },
    async revise(current: ActivityProfile, changed: Pick<ActivityProfile, 'title' | 'description' | 'location' | 'colorCode'>) {
      const token = await csrf();
      const next = parseProfile(await checked(await request(`${url(current.activityRef)}/profile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': token },
        body: JSON.stringify({
          operation_id: crypto.randomUUID(), expected_revision: current.revision,
          title: changed.title, description: changed.description,
          location: changed.location, color_code: changed.colorCode,
        }),
      })));
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
      return next;
    },
    async retire(ref: string) {
      const token = await csrf();
      await checked(await request(`${url(ref)}/retire`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': token },
        body: JSON.stringify({ operation_id: crypto.randomUUID() }),
      }));
      invalidateTemporalTimelineRead();
      invalidateTemporalPlanningRead();
    },
  };
}
