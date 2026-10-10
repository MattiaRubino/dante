import { createWebFetch } from '../../../../platform/api/web-fetch';

export type FinishedWorkItem = Readonly<{
  subject_kind: 'activity' | 'event';
  subject_ref: string;
  title: string;
  session_ref: string | null;
  started_at: string | null;
  ended_at: string;
  record_kind: 'session_ended' | 'realization_occurred';
}>;

export type PendingObjectiveWork = Readonly<{
  objective_ref: string;
  subject_kind: 'activity' | 'event' | 'occurrence';
  subject_ref: string;
  subject_title: string;
  label: string;
  result_kind: 'boolean' | 'quantity' | 'range' | 'qualitative';
  presentation_order: number;
  draft_revision: number | null;
  draft_updated_at: string | null;
}>;

function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Risposta del riepilogo Home non valida.');
  }
  return value as Record<string, unknown>;
}

function text(value: unknown): string {
  if (typeof value !== 'string' || !value.trim()) {
    throw new Error('Dati del riepilogo Home non validi.');
  }
  return value;
}

function optionalText(value: unknown): string | null {
  return value === null ? null : text(value);
}

function finished(value: unknown): FinishedWorkItem {
  const v = record(value);
  if (!['activity', 'event'].includes(String(v.subject_kind)) ||
      !['session_ended', 'realization_occurred'].includes(String(v.record_kind))) {
    throw new Error('Tipologia di elemento concluso non valida.');
  }
  return {
    subject_kind: v.subject_kind as FinishedWorkItem['subject_kind'],
    subject_ref: text(v.subject_ref),
    title: text(v.title),
    session_ref: optionalText(v.session_ref),
    started_at: optionalText(v.started_at),
    ended_at: text(v.ended_at),
    record_kind: v.record_kind as FinishedWorkItem['record_kind'],
  };
}

function objective(value: unknown): PendingObjectiveWork {
  const v = record(value);
  if (!['activity','event','occurrence'].includes(String(v.subject_kind)) ||
      !['boolean','quantity','range','qualitative'].includes(String(v.result_kind)) ||
      typeof v.presentation_order !== 'number' ||
      (v.draft_revision !== null && typeof v.draft_revision !== 'number')) {
    throw new Error('Elemento Obiettivo del riepilogo non valido.');
  }
  return {
    objective_ref: text(v.objective_ref),
    subject_kind: v.subject_kind as PendingObjectiveWork['subject_kind'],
    subject_ref: text(v.subject_ref),
    subject_title: text(v.subject_title),
    label: text(v.label),
    result_kind: v.result_kind as PendingObjectiveWork['result_kind'],
    presentation_order: v.presentation_order,
    draft_revision: v.draft_revision as number | null,
    draft_updated_at: optionalText(v.draft_updated_at),
  };
}

export function createContextRailWorkSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  async function get<T>(
    uri: string, parse: (value: unknown) => T, signal?: AbortSignal,
  ): Promise<readonly T[]> {
    const response = await webFetch(uri, signal ? { signal } : undefined);
    if (!response.ok) throw new Error('Dati del riepilogo non disponibili.');
    const payload: unknown = await response.json();
    if (!Array.isArray(payload) || payload.length > 100) {
      throw new Error('Risposta del riepilogo troppo estesa o non valida.');
    }
    return Object.freeze(payload.map(parse));
  }
  return Object.freeze({
    listFinished: (signal?: AbortSignal) =>
      get('/api/v1/temporal/home/finished-work?limit=40', finished, signal),
    listObjectives: (signal?: AbortSignal) =>
      get('/api/v1/temporal/home/objective-work?limit=40', objective, signal),
  });
}
