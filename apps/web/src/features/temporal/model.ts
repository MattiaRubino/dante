import {
  Temporal,
  type Instant,
  type PlainDate,
  type PlainDateTime,
  type ZonedDateTime,
} from '@dante/time';

/* Identity ---------------------------------------------------------------- */

export type TemporalProjectionId = string & {
  readonly __brand: 'TemporalProjectionId';
};
export type TemporalOperationId = string & {
  readonly __brand: 'TemporalOperationId';
};
export type TemporalUndoToken = string & {
  readonly __brand: 'TemporalUndoToken';
};

export interface TemporalIdFactory {
  projectionId(): TemporalProjectionId;
  operationId(): TemporalOperationId;
  undoToken(): TemporalUndoToken;
}

function requireIdentifier(value: string, label: string): string {
  const normalized = value.trim();
  if (normalized.length === 0) {
    throw new Error(`${label} cannot be empty`);
  }
  return normalized;
}

export const temporalProjectionId = (value: string): TemporalProjectionId =>
  requireIdentifier(value, 'Temporal projection id') as TemporalProjectionId;

export const temporalOperationId = (value: string): TemporalOperationId =>
  requireIdentifier(value, 'Temporal operation id') as TemporalOperationId;

export const temporalUndoToken = (value: string): TemporalUndoToken =>
  requireIdentifier(value, 'Temporal undo token') as TemporalUndoToken;

export function createDeterministicTemporalIdFactory(
  seed = 'f0',
): TemporalIdFactory {
  const safeSeed = requireIdentifier(seed, 'Temporal id seed');
  let projection = 0;
  let operation = 0;
  let undo = 0;

  return {
    projectionId: () =>
      temporalProjectionId(`${safeSeed}:projection:${++projection}`),
    operationId: () =>
      temporalOperationId(`${safeSeed}:operation:${++operation}`),
    undoToken: () => temporalUndoToken(`${safeSeed}:undo:${++undo}`),
  };
}

export const systemTemporalIdFactory: TemporalIdFactory = {
  projectionId: () =>
    temporalProjectionId(`projection:${globalThis.crypto.randomUUID()}`),
  operationId: () =>
    temporalOperationId(`operation:${globalThis.crypto.randomUUID()}`),
  undoToken: () => temporalUndoToken(`undo:${globalThis.crypto.randomUUID()}`),
};

/* Clock ------------------------------------------------------------------- */

export interface TemporalClock {
  now(): Instant;
  timeZoneId(): string;
  today(timeZoneId?: string): PlainDate;
}

export const systemTemporalClock: TemporalClock = {
  now: () => Temporal.Now.instant(),
  timeZoneId: () => Temporal.Now.timeZoneId(),
  today: (timeZoneId) => {
    const now = Temporal.Now.instant();
    return now
      .toZonedDateTimeISO(timeZoneId ?? Temporal.Now.timeZoneId())
      .toPlainDate();
  },
};

export function createFixedTemporalClock(
  instant: Instant,
  timeZoneId: string,
): TemporalClock {
  const fixedInstant = Temporal.Instant.from(instant);
  const fixedZone = fixedInstant.toZonedDateTimeISO(timeZoneId).timeZoneId;

  return {
    now: () => fixedInstant,
    timeZoneId: () => fixedZone,
    today: (requestedZone) =>
      fixedInstant.toZonedDateTimeISO(requestedZone ?? fixedZone).toPlainDate(),
  };
}

/* Validation -------------------------------------------------------------- */

export type TemporalValidationIssue = Readonly<{
  code: string;
  path: readonly string[];
  severity: 'error' | 'warning';
  detail?: Readonly<Record<string, string | number | boolean>>;
}>;

export type TemporalValidationResult<T> =
  | Readonly<{
      valid: true;
      value: T;
      issues: readonly TemporalValidationIssue[];
    }>
  | Readonly<{
      valid: false;
      issues: readonly TemporalValidationIssue[];
    }>;

export function temporalValidationIssue(
  code: string,
  path: readonly string[],
  severity: TemporalValidationIssue['severity'] = 'error',
  detail?: TemporalValidationIssue['detail'],
): TemporalValidationIssue {
  return Object.freeze({
    code,
    path: Object.freeze([...path]),
    severity,
    ...(detail ? { detail: Object.freeze({ ...detail }) } : {}),
  });
}

export function sortTemporalValidationIssues(
  issues: readonly TemporalValidationIssue[],
): readonly TemporalValidationIssue[] {
  return Object.freeze(
    [...issues].sort((left, right) => {
      const path =
        left.path.join('.').localeCompare(right.path.join('.')) ||
        left.code.localeCompare(right.code);
      return path || left.severity.localeCompare(right.severity);
    }),
  );
}

function validationResult<T>(
  value: T,
  issues: readonly TemporalValidationIssue[],
): TemporalValidationResult<T> {
  const sorted = sortTemporalValidationIssues(issues);
  return sorted.some((issue) => issue.severity === 'error')
    ? Object.freeze({ valid: false as const, issues: sorted })
    : Object.freeze({ valid: true as const, value, issues: sorted });
}

/* Placement --------------------------------------------------------------- */

export type TemporalPlacement =
  | Readonly<{
      kind: 'date-span';
      startDate: PlainDate;
      endDateExclusive: PlainDate;
    }>
  | Readonly<{
      kind: 'floating-local';
      start: PlainDateTime;
      end: PlainDateTime;
    }>
  | Readonly<{
      kind: 'zoned';
      start: ZonedDateTime;
      end: ZonedDateTime;
    }>
  | Readonly<{
      kind: 'absolute';
      start: Instant;
      end: Instant;
    }>;

export type SerializedTemporalPlacement =
  | Readonly<{
      kind: 'date-span';
      startDate: string;
      endDateExclusive: string;
    }>
  | Readonly<{
      kind: 'floating-local' | 'zoned' | 'absolute';
      start: string;
      end: string;
    }>;

export function serializeTemporalPlacement(
  placement: TemporalPlacement,
): SerializedTemporalPlacement {
  if (placement.kind === 'date-span') {
    return Object.freeze({
      kind: placement.kind,
      startDate: placement.startDate.toString(),
      endDateExclusive: placement.endDateExclusive.toString(),
    });
  }
  return Object.freeze({
    kind: placement.kind,
    start: placement.start.toString(),
    end: placement.end.toString(),
  });
}

export function deserializeTemporalPlacement(
  value: SerializedTemporalPlacement,
): TemporalPlacement {
  switch (value.kind) {
    case 'date-span':
      return Object.freeze({
        kind: value.kind,
        startDate: Temporal.PlainDate.from(value.startDate),
        endDateExclusive: Temporal.PlainDate.from(value.endDateExclusive),
      });
    case 'floating-local':
      return Object.freeze({
        kind: value.kind,
        start: Temporal.PlainDateTime.from(value.start),
        end: Temporal.PlainDateTime.from(value.end),
      });
    case 'zoned':
      return Object.freeze({
        kind: value.kind,
        start: Temporal.ZonedDateTime.from(value.start),
        end: Temporal.ZonedDateTime.from(value.end),
      });
    case 'absolute':
      return Object.freeze({
        kind: value.kind,
        start: Temporal.Instant.from(value.start),
        end: Temporal.Instant.from(value.end),
      });
  }
}

export function temporalPlacementEquals(
  left: TemporalPlacement,
  right: TemporalPlacement,
): boolean {
  return (
    JSON.stringify(serializeTemporalPlacement(left)) ===
    JSON.stringify(serializeTemporalPlacement(right))
  );
}

export function validateTemporalPlacement(
  placement: TemporalPlacement,
): TemporalValidationResult<TemporalPlacement> {
  let invalid = false;

  switch (placement.kind) {
    case 'date-span':
      invalid =
        Temporal.PlainDate.compare(
          placement.startDate,
          placement.endDateExclusive,
        ) >= 0;
      break;
    case 'floating-local':
      invalid =
        Temporal.PlainDateTime.compare(placement.start, placement.end) >= 0;
      break;
    case 'zoned':
      invalid =
        Temporal.Instant.compare(
          placement.start.toInstant(),
          placement.end.toInstant(),
        ) >= 0;
      break;
    case 'absolute':
      invalid = Temporal.Instant.compare(placement.start, placement.end) >= 0;
      break;
  }

  return validationResult(
    placement,
    invalid
      ? [
          temporalValidationIssue(
            `temporal.placement.${placement.kind}.invalid_range`,
            ['placement', 'end'],
          ),
        ]
      : [],
  );
}

/* Capabilities ------------------------------------------------------------ */

export const TEMPORAL_CAPABILITIES = [
  'placement',
  'recurrence',
  'execution',
  'actual',
  'confirmation',
  'replanning',
  'history',
  'notes',
] as const;

export type TemporalCapability = (typeof TEMPORAL_CAPABILITIES)[number];

const capabilityOrder = new Map<TemporalCapability, number>(
  TEMPORAL_CAPABILITIES.map((capability, index) => [capability, index]),
);

export function normalizeTemporalCapabilities(
  capabilities: readonly TemporalCapability[],
): readonly TemporalCapability[] {
  return Object.freeze(
    [...new Set(capabilities)].sort(
      (left, right) =>
        (capabilityOrder.get(left) ?? Number.MAX_SAFE_INTEGER) -
        (capabilityOrder.get(right) ?? Number.MAX_SAFE_INTEGER),
    ),
  );
}

export function supportsTemporalCapability(
  capabilities: readonly TemporalCapability[],
  capability: TemporalCapability,
): boolean {
  return capabilities.includes(capability);
}

/* Draft ------------------------------------------------------------------- */

export type TemporalDraft<T> = Readonly<{
  baseline: T;
  current: T;
  dirty: boolean;
  editRevision: number;
}>;

export function createTemporalDraft<T>(value: T): TemporalDraft<T> {
  return Object.freeze({
    baseline: value,
    current: value,
    dirty: false,
    editRevision: 0,
  });
}

export function updateTemporalDraft<T>(
  draft: TemporalDraft<T>,
  next: T,
  equals: (left: T, right: T) => boolean = Object.is,
): TemporalDraft<T> {
  return Object.freeze({
    baseline: draft.baseline,
    current: next,
    dirty: !equals(draft.baseline, next),
    editRevision: draft.editRevision + 1,
  });
}

export function resetTemporalDraft<T>(
  draft: TemporalDraft<T>,
): TemporalDraft<T> {
  return Object.freeze({
    baseline: draft.baseline,
    current: draft.baseline,
    dirty: false,
    editRevision: draft.editRevision + 1,
  });
}

export function commitTemporalDraft<T>(
  draft: TemporalDraft<T>,
): TemporalDraft<T> {
  return Object.freeze({
    baseline: draft.current,
    current: draft.current,
    dirty: false,
    editRevision: draft.editRevision + 1,
  });
}

/* Application projection -------------------------------------------------- */

export type TemporalSubjectRef =
  | Readonly<{
      source: 'native';
      kind: string;
      id: string;
    }>
  | Readonly<{
      source: 'external';
      provider: string;
      kind: string;
      id: string;
    }>;

export type TemporalProjectionItem = Readonly<{
  id: TemporalProjectionId;
  subject: TemporalSubjectRef;
  title: string;
  placement: TemporalPlacement | null;
  capabilities: readonly TemporalCapability[];
  revision: number;
  createdAt: Instant;
  updatedAt: Instant;
  lastOperationId: TemporalOperationId;
}>;

export type TemporalWorkspaceSnapshot = Readonly<{
  revision: number;
  items: readonly TemporalProjectionItem[];
}>;

export function freezeTemporalProjectionItem(
  item: TemporalProjectionItem,
): TemporalProjectionItem {
  return Object.freeze({
    ...item,
    subject: Object.freeze({ ...item.subject }),
    capabilities: Object.freeze([...item.capabilities]),
  });
}
