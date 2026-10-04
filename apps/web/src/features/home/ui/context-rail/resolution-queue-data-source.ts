import { createWebFetch } from '../../../../platform/api/web-fetch';

type ResolutionSubjectKind = 'activity' | 'event';
type ResolutionAction = 'open_reconciliation' | 'record_realization';

type ResolutionItemBase = Readonly<{
  subjectRef: string;
  title: string;
  summary: string;
  effectiveAt: string;
  purposeCode: string;
}>;

export type ReconciliationResolutionItem = ResolutionItemBase &
  Readonly<{
    reasonCode: 'reconciliation_open';
    subjectKind: ResolutionSubjectKind;
    reconciliationRef: string;
    outcomeRef: string;
    sessionRef: string | null;
    sessionTimingMaterialStateRef: string | null;
    actions: readonly ['open_reconciliation'];
  }>;

export type RealizationReviewResolutionItem = ResolutionItemBase &
  Readonly<{
    reasonCode: 'realization_review';
    subjectKind: 'activity';
    reconciliationRef: null;
    outcomeRef: null;
    sessionRef: string;
    sessionTimingMaterialStateRef: string;
    actions: readonly ['record_realization'];
  }>;

export type ResolutionItem =
  | ReconciliationResolutionItem
  | RealizationReviewResolutionItem;

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

function requiredUuid(value: unknown): string | null {
  return typeof value === 'string' && uuid.test(value) ? value : null;
}

function nullableUuid(value: unknown): string | null | undefined {
  if (value === null) return null;
  const parsed = requiredUuid(value);
  return parsed ?? undefined;
}

function requiredText(value: unknown): string | null {
  return typeof value === 'string' && value.trim() ? value : null;
}

function hasOnlyAction(
  value: unknown,
  expected: ResolutionAction,
): value is [ResolutionAction] {
  return Array.isArray(value) && value.length === 1 && value[0] === expected;
}

function parseItem(value: unknown): ResolutionItem {
  const item = record(value);
  const subjectRef = requiredUuid(item.subject_ref);
  const title = requiredText(item.title);
  const summary = requiredText(item.summary);
  const effectiveAt = requiredText(item.effective_at);
  const purposeCode = requiredText(item.purpose_code);
  const reconciliationRef = nullableUuid(item.reconciliation_ref);
  const outcomeRef = nullableUuid(item.outcome_ref);
  const sessionRef = nullableUuid(item.session_ref);
  const sessionTimingMaterialStateRef = nullableUuid(
    item.session_timing_material_state_ref,
  );

  if (
    subjectRef === null ||
    title === null ||
    summary === null ||
    effectiveAt === null ||
    purposeCode === null ||
    reconciliationRef === undefined ||
    outcomeRef === undefined ||
    sessionRef === undefined ||
    sessionTimingMaterialStateRef === undefined
  ) {
    throw new Error('Elemento Da risolvere non valido.');
  }

  if (
    item.reason_code === 'reconciliation_open' &&
    (item.subject_kind === 'activity' || item.subject_kind === 'event') &&
    reconciliationRef !== null &&
    outcomeRef !== null &&
    hasOnlyAction(item.actions, 'open_reconciliation')
  ) {
    return {
      reasonCode: 'reconciliation_open',
      subjectKind: item.subject_kind,
      subjectRef,
      title,
      summary,
      effectiveAt,
      reconciliationRef,
      outcomeRef,
      purposeCode,
      sessionRef,
      sessionTimingMaterialStateRef,
      actions: ['open_reconciliation'],
    };
  }

  if (
    item.reason_code === 'realization_review' &&
    item.subject_kind === 'activity' &&
    reconciliationRef === null &&
    outcomeRef === null &&
    sessionRef !== null &&
    sessionTimingMaterialStateRef !== null &&
    hasOnlyAction(item.actions, 'record_realization')
  ) {
    return {
      reasonCode: 'realization_review',
      subjectKind: 'activity',
      subjectRef,
      title,
      summary,
      effectiveAt,
      reconciliationRef: null,
      outcomeRef: null,
      purposeCode,
      sessionRef,
      sessionTimingMaterialStateRef,
      actions: ['record_realization'],
    };
  }

  throw new Error('Elemento Da risolvere non valido.');
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
