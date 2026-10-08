import { createWebFetch } from '../../platform/api/web-fetch';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from './timeline-invalidation';

export type EventLifeAreaChoice = Readonly<{
  options: readonly Readonly<{ ref: string; name: string }>[];
  currentRef: string | null;
  currentRevision: number;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Risposta Life Area Event non valida.');
  }
  return value as Record<string, unknown>;
}

export function createRemoteEventLifeAreaSettings(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const base = '/api/v1/temporal/life-area-assignments';

  async function read(path: string): Promise<unknown> {
    const response = await request(path);
    if (!response.ok) throw new Error('Lettura Life Area non disponibile.');
    return response.json();
  }

  return Object.freeze({
    async load(eventRef: string): Promise<EventLifeAreaChoice> {
      const [areas, assignments] = await Promise.all([
        read('/api/v1/temporal/life-areas'), read(base),
      ]);
      if (!Array.isArray(areas) || !Array.isArray(assignments)) {
        throw new Error('Catalogo Life Area Event non valido.');
      }
      const options = areas.map(record).filter((r) => r.archived === false)
        .map((r) => {
          if (typeof r.life_area_ref !== 'string' || typeof r.name !== 'string' ||
              !r.name.trim()) throw new Error('Life Area Event non valida.');
          return { ref: r.life_area_ref, name: r.name };
        });
      const owned = assignments.map(record).filter((r) =>
        r.subject_kind === 'event' && r.subject_native_ref === eventRef);
      if (owned.length > 1) throw new Error('Assegnazioni Event incoerenti.');
      const current = owned[0];
      if (current && (
        (current.life_area_ref !== null && typeof current.life_area_ref !== 'string') ||
        !Number.isSafeInteger(current.assignment_revision) ||
        Number(current.assignment_revision) < 1
      )) throw new Error('Revisione Life Area Event non valida.');
      return {
        options,
        currentRef: current?.life_area_ref == null ? null : String(current.life_area_ref),
        currentRevision: current ? Number(current.assignment_revision) : 0,
      };
    },
    async assign(
      eventRef: string, current: EventLifeAreaChoice,
      nextRef: string | null, operationId: string,
    ): Promise<EventLifeAreaChoice> {
      if (nextRef === current.currentRef) return current;
      if (nextRef && !current.options.some((opt) => opt.ref === nextRef)) {
        throw new Error('Seleziona una Life Area esistente.');
      }
      const sessionResponse = await request('/api/v1/auth/session');
      const session = record(await sessionResponse.json());
      if (!sessionResponse.ok || session.authenticated !== true ||
          typeof session.csrf_token !== 'string' || !session.csrf_token) {
        throw new Error('Sessione non autenticata.');
      }
      const response = await request(`${base}/events/${encodeURIComponent(eventRef)}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-Dante-CSRF': session.csrf_token,
        },
        body: JSON.stringify({
          operation_id: operationId,
          life_area_ref: nextRef,
          expected_assignment_revision: current.currentRevision,
        }),
      });
      if (!response.ok) throw new Error(response.status === 409
        ? 'La Life Area Event è cambiata. Ricarica e riprova.'
        : 'Modifica Life Area Event rifiutata.');
      const saved = record(await response.json());
      if (saved.subject_kind !== 'event' || saved.subject_native_ref !== eventRef ||
          saved.life_area_ref !== nextRef ||
          saved.assignment_revision !== current.currentRevision + 1) {
        throw new Error('Conferma Life Area Event non valida.');
      }
      invalidateTemporalPlanningRead();
      invalidateTemporalTimelineRead();
      return { ...current, currentRef: nextRef, currentRevision: current.currentRevision + 1 };
    },
  });
}
