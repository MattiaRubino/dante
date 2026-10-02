import { createWebFetch } from '../../../../platform/api/web-fetch';

export type ResolutionItem = Readonly<{
  reasonCode: 'reconciliation_open';
  subjectKind: 'activity' | 'event';
  subjectRef: string;
  title: string;
  reconciliationRef: string;
  outcomeRef: string;
  purposeCode: string;
}>;

export type ResolutionQueue = Readonly<{
  items: readonly ResolutionItem[];
  count: number;
}>;

export type ResolutionQueueSource = Readonly<{
  list: (signal?: AbortSignal) => Promise<ResolutionQueue>;
}>;

const uuid =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Risposta Da risolvere non valida.');
  }
  return value as Record<string, unknown>;
}

function parseItem(value: unknown): ResolutionItem {
  const item = record(value);
  if (
    item.reason_code !== 'reconciliation_open' ||
    (item.subject_kind !== 'activity' && item.subject_kind !== 'event') ||
    typeof item.subject_ref !== 'string' ||
    !uuid.test(item.subject_ref) ||
    typeof item.title !== 'string' ||
    !item.title.trim() ||
    typeof item.reconciliation_ref !== 'string' ||
    !uuid.test(item.reconciliation_ref) ||
    typeof item.outcome_ref !== 'string' ||
    !uuid.test(item.outcome_ref) ||
    typeof item.purpose_code !== 'string' ||
    !item.purpose_code.trim()
  ) {
    throw new Error('Elemento Da risolvere non valido.');
  }
  return {
    reasonCode: item.reason_code,
    subjectKind: item.subject_kind,
    subjectRef: item.subject_ref,
    title: item.title,
    reconciliationRef: item.reconciliation_ref,
    outcomeRef: item.outcome_ref,
    purposeCode: item.purpose_code,
  };
}

export function createResolutionQueueSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
): ResolutionQueueSource {
  const webFetch = createWebFetch(fetchFn);
  return {
    async list(signal?: AbortSignal): Promise<ResolutionQueue> {
      const response = await webFetch(
        '/api/v1/temporal/resolution-queue',
        signal === undefined ? undefined : { signal },
      );
      if (!response.ok)
        throw new Error(`Da risolvere: HTTP ${response.status}`);
      const payload: unknown = await response.json();
      const queue = record(payload);
      if (
        !Array.isArray(queue.items) ||
        typeof queue.count !== 'number' ||
        !Number.isSafeInteger(queue.count) ||
        queue.count < 0 ||
        queue.count !== queue.items.length
      ) {
        throw new Error('Risposta Da risolvere non valida.');
      }
      return { items: queue.items.map(parseItem), count: queue.count };
    },
  };
}
