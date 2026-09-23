import { Temporal, validateNamedTimeZone } from '@dante/time';

import {
  createWebFetch,
  type DeviceTimeZoneResolver,
} from '../../platform/api/web-fetch';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineExpectedOccurrenceItem,
  TemporalTimelineItem,
  TemporalTimelineOccurrenceCoordinate,
  TemporalTimelineScheduledOccurrenceItem,
  TemporalTimelineScheduledItem,
  TemporalTimelineWindow,
  TemporalTimelineWindowCheckpointRequest,
  TemporalTimelineWindowCheckpointResult,
  TemporalTimelineWindowRequest,
} from './timeline-read';

const TEMPORAL_TIMELINE_WINDOW_ENDPOINT = '/api/v1/temporal/timeline/window';
const TEMPORAL_OCCURRENCE_WINDOW_CHECKPOINT_ENDPOINT =
  '/api/v1/temporal/occurrences/checkpoint';
const SESSION_ENDPOINT = '/api/v1/auth/session';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const MAX_TIMELINE_WINDOW_DAYS = 62;
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type TemporalTimelineRemoteFailureKind =
  'transport' | 'http' | 'protocol';

export class TemporalTimelineRemoteError extends Error {
  constructor(
    readonly kind: TemporalTimelineRemoteFailureKind,
    message: string,
    readonly status: number | null = null,
  ) {
    super(message);
    this.name = 'TemporalTimelineRemoteError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function requireExactKeys(
  payload: Record<string, unknown>,
  allowed: readonly string[],
  label: string,
): void {
  const allowedKeys = new Set(allowed);
  for (const key of Object.keys(payload)) {
    if (!allowedKeys.has(key)) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        `${label} contains unexpected field ${key}.`,
      );
    }
  }
  for (const key of allowed) {
    if (!(key in payload)) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        `${label} is missing required field ${key}.`,
      );
    }
  }
}

function parsePlainDate(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
  try {
    const parsed = Temporal.PlainDate.from(value);
    if (parsed.toString() !== value) {
      throw new RangeError('non-canonical PlainDate');
    }
    return parsed;
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainDate string.`,
    );
  }
}

function parsePlainDateKey(value: unknown, field: string): string {
  return parsePlainDate(value, field).toString();
}

function parseUuidV7(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseLocalDateTime(value: unknown, field: string) {
  if (
    typeof value !== 'string' ||
    /(?:Z|[+-]\d{2}:\d{2}|\[[^\]]+\])$/i.test(value)
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
  try {
    return Temporal.PlainDateTime.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a local date-time without zone or offset.`,
    );
  }
}

function parsePlainTime(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainTime string.`,
    );
  }
  try {
    return Temporal.PlainTime.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a canonical PlainTime string.`,
    );
  }
}

function parseInstant(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be an absolute instant.`,
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be an absolute instant.`,
    );
  }
}

function parseZoneId(value: unknown, field: string): string {
  if (typeof value !== 'string') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
    );
  }
  try {
    return validateNamedTimeZone(value);
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a named IANA timezone.`,
    );
  }
}

function validateWindowRequest(request: TemporalTimelineWindowRequest): void {
  const start = Temporal.PlainDate.from(request.startDate);
  const end = Temporal.PlainDate.from(request.endDateExclusive);
  const days = start.until(end, { largestUnit: 'days' }).days;
  if (days <= 0) {
    throw new RangeError('Timeline endDateExclusive must be after startDate.');
  }
  if (days > MAX_TIMELINE_WINDOW_DAYS) {
    throw new RangeError(
      `Timeline window cannot exceed ${MAX_TIMELINE_WINDOW_DAYS} local days.`,
    );
  }
}

function validateCheckpointRequest(
  request: TemporalTimelineWindowCheckpointRequest,
): void {
  validateWindowRequest(request);
  const operationId = request.operationId.trim();
  if (operationId.length === 0 || operationId.length > 200) {
    throw new RangeError(
      'Timeline checkpoint operation id must contain 1 to 200 characters.',
    );
  }
}

function parseOccurrenceCoordinate(
  payload: unknown,
): TemporalTimelineOccurrenceCoordinate {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Timeline Occurrence coordinate has an unsupported representation.',
    );
  }

  switch (payload.family_code) {
    case 'calendar_wall_clock': {
      requireExactKeys(
        payload,
        [
          'family_code',
          'generated_date',
          'generated_wall_time',
          'clock_basis_code',
          'zone_id',
          'resolved_at',
        ],
        'Timeline calendar Occurrence coordinate',
      );
      if (
        payload.clock_basis_code !== 'floating_local' &&
        payload.clock_basis_code !== 'named_zone' &&
        payload.clock_basis_code !== 'absolute_utc'
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline calendar Occurrence clock basis is unsupported.',
        );
      }
      const namedZone = payload.clock_basis_code === 'named_zone';
      if (namedZone !== (typeof payload.zone_id === 'string')) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline calendar Occurrence zone does not match its clock basis.',
        );
      }
      return Object.freeze({
        familyCode: 'calendar-wall-clock' as const,
        generatedDate: parsePlainDate(payload.generated_date, 'generated_date'),
        generatedWallTime:
          payload.generated_wall_time === null
            ? null
            : parsePlainTime(
                payload.generated_wall_time,
                'generated_wall_time',
              ),
        clockBasis:
          payload.clock_basis_code === 'floating_local'
            ? ('floating-local' as const)
            : payload.clock_basis_code === 'named_zone'
              ? ('named-zone' as const)
              : ('absolute-utc' as const),
        zoneId: namedZone ? parseZoneId(payload.zone_id, 'zone_id') : null,
        resolvedAt:
          payload.resolved_at === null
            ? null
            : parseInstant(payload.resolved_at, 'resolved_at'),
      });
    }
    case 'elapsed_interval':
      requireExactKeys(
        payload,
        ['family_code', 'expected_at'],
        'Timeline elapsed Occurrence coordinate',
      );
      return Object.freeze({
        familyCode: 'elapsed-interval' as const,
        expectedAt: parseInstant(payload.expected_at, 'expected_at'),
      });
    case 'quota_per_period': {
      requireExactKeys(
        payload,
        [
          'family_code',
          'period_start_date',
          'period_end_date_exclusive',
          'frame_code',
          'zone_id',
        ],
        'Timeline quota Occurrence coordinate',
      );
      if (
        payload.frame_code !== 'floating_local' &&
        payload.frame_code !== 'named_zone' &&
        payload.frame_code !== 'absolute_utc'
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline quota Occurrence frame is unsupported.',
        );
      }
      const periodStartDate = parsePlainDate(
        payload.period_start_date,
        'period_start_date',
      );
      const periodEndDateExclusive = parsePlainDate(
        payload.period_end_date_exclusive,
        'period_end_date_exclusive',
      );
      if (
        Temporal.PlainDate.compare(periodStartDate, periodEndDateExclusive) >= 0
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline quota Occurrence period must be a positive half-open range.',
        );
      }
      const namedZone = payload.frame_code === 'named_zone';
      if (namedZone !== (typeof payload.zone_id === 'string')) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline quota Occurrence zone does not match its frame.',
        );
      }
      return Object.freeze({
        familyCode: 'quota-per-period' as const,
        periodStartDate,
        periodEndDateExclusive,
        frame:
          payload.frame_code === 'floating_local'
            ? ('floating-local' as const)
            : payload.frame_code === 'named_zone'
              ? ('named-zone' as const)
              : ('absolute-utc' as const),
        zoneId: namedZone ? parseZoneId(payload.zone_id, 'zone_id') : null,
      });
    }
    case 'cyclic_positional':
      requireExactKeys(
        payload,
        ['family_code', 'generated_date', 'position_index'],
        'Timeline cyclic Occurrence coordinate',
      );
      if (
        typeof payload.position_index !== 'number' ||
        !Number.isInteger(payload.position_index) ||
        payload.position_index < 0
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline cyclic Occurrence position must be a non-negative integer.',
        );
      }
      return Object.freeze({
        familyCode: 'cyclic-positional' as const,
        generatedDate: parsePlainDate(payload.generated_date, 'generated_date'),
        positionIndex: payload.position_index,
      });
    default:
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Timeline Occurrence coordinate family is unsupported.',
      );
  }
}

type ParsedOwnerIdentity =
  | Readonly<{
      kind: 'scheduled_activity';
      activityRef: string;
      scheduleRef: string;
      placementMaterialStateRef: string;
      title: string;
      wireRefKey: 'activity_ref';
    }>
  | Readonly<{
      kind: 'scheduled_event';
      eventRef: string;
      scheduleRef: string;
      placementMaterialStateRef: string;
      title: string;
      wireRefKey: 'event_ref';
    }>;

function parseOwnerIdentity(
  payload: Record<string, unknown>,
): ParsedOwnerIdentity {
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline owner title must be a non-empty string.',
    );
  }
  const shared = {
    scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: parseUuidV7(
      payload.placement_material_state_ref,
      'placement_material_state_ref',
    ),
    title: payload.title,
  };

  if (payload.kind === 'scheduled_activity') {
    return Object.freeze({
      kind: 'scheduled_activity' as const,
      activityRef: parseUuidV7(payload.activity_ref, 'activity_ref'),
      ...shared,
      wireRefKey: 'activity_ref' as const,
    });
  }
  if (payload.kind === 'scheduled_event') {
    return Object.freeze({
      kind: 'scheduled_event' as const,
      eventRef: parseUuidV7(payload.event_ref, 'event_ref'),
      ...shared,
      wireRefKey: 'event_ref' as const,
    });
  }
  throw new TemporalTimelineRemoteError(
    'protocol',
    'Temporal Timeline item has an unsupported owner representation.',
  );
}

function publicIdentity(identity: ParsedOwnerIdentity) {
  if (identity.kind === 'scheduled_activity') {
    const { wireRefKey: _wireRefKey, ...result } = identity;
    return result;
  }
  const { wireRefKey: _wireRefKey, ...result } = identity;
  return result;
}

function parseScheduledItem(payload: unknown): TemporalTimelineScheduledItem {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline item has an unsupported representation.',
    );
  }

  const owner = parseOwnerIdentity(payload);
  const identity = publicIdentity(owner);
  const ownerLabel = owner.kind === 'scheduled_activity' ? 'Activity' : 'Event';
  const commonKeys = [
    'kind',
    owner.wireRefKey,
    'schedule_ref',
    'placement_material_state_ref',
    'title',
    'temporal_form',
  ] as const;

  switch (payload.temporal_form) {
    case 'date_span': {
      requireExactKeys(
        payload,
        [...commonKeys, 'start_date', 'end_date_exclusive'],
        `Temporal Timeline date-span ${ownerLabel}`,
      );
      const startDate = parsePlainDate(payload.start_date, 'start_date');
      const endDateExclusive = parsePlainDate(
        payload.end_date_exclusive,
        'end_date_exclusive',
      );
      if (Temporal.PlainDate.compare(startDate, endDateExclusive) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline date-span must be a positive half-open civil-date range.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'date-span' as const,
        startDate,
        endDateExclusive,
      });
    }

    case 'floating_local': {
      requireExactKeys(
        payload,
        [...commonKeys, 'starts_local_at', 'ends_local_at'],
        `Temporal Timeline floating-local ${ownerLabel}`,
      );
      const startsLocalAt = parseLocalDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        payload.ends_local_at,
        'ends_local_at',
      );
      if (Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline floating-local placement must be a positive interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'floating-local' as const,
        startsLocalAt,
        endsLocalAt,
      });
    }

    case 'named_zone_local': {
      requireExactKeys(
        payload,
        [
          ...commonKeys,
          'starts_local_at',
          'ends_local_at',
          'zone_id',
          'resolved_start_at',
          'resolved_end_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        `Temporal Timeline named-zone ${ownerLabel}`,
      );
      const startsLocalAt = parseLocalDateTime(
        payload.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        payload.ends_local_at,
        'ends_local_at',
      );
      const resolvedStartAt = parseInstant(
        payload.resolved_start_at,
        'resolved_start_at',
      );
      const resolvedEndAt = parseInstant(
        payload.resolved_end_at,
        'resolved_end_at',
      );
      if (
        Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
        Temporal.Instant.compare(resolvedStartAt, resolvedEndAt) >= 0
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline named-zone placement must retain a positive local and resolved interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'named-zone-local' as const,
        startsLocalAt,
        endsLocalAt,
        zoneId: parseZoneId(payload.zone_id, 'zone_id'),
        resolvedStartAt,
        resolvedEndAt,
        displayStartsLocalAt: parseLocalDateTime(
          payload.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          payload.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }

    case 'absolute': {
      requireExactKeys(
        payload,
        [
          ...commonKeys,
          'starts_at',
          'ends_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        `Temporal Timeline absolute ${ownerLabel}`,
      );
      const startsAt = parseInstant(payload.starts_at, 'starts_at');
      const endsAt = parseInstant(payload.ends_at, 'ends_at');
      if (Temporal.Instant.compare(startsAt, endsAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline absolute placement must be a positive interval.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'absolute' as const,
        startsAt,
        endsAt,
        displayStartsLocalAt: parseLocalDateTime(
          payload.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          payload.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }

    case 'coarse_local_period': {
      requireExactKeys(
        payload,
        [...commonKeys, 'local_date', 'period'],
        `Temporal Timeline coarse-period ${ownerLabel}`,
      );
      if (
        payload.period !== 'morning' &&
        payload.period !== 'afternoon' &&
        payload.period !== 'evening'
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Timeline coarse-period placement is outside the activated vocabulary.',
        );
      }
      return Object.freeze({
        ...identity,
        temporalForm: 'coarse-local-period' as const,
        localDate: parsePlainDate(payload.local_date, 'local_date'),
        period: payload.period,
      });
    }

    default:
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Temporal Timeline item has an unsupported temporal form.',
      );
  }
}

function parseScheduledOccurrence(
  payload: Record<string, unknown>,
): TemporalTimelineScheduledOccurrenceItem {
  requireExactKeys(
    payload,
    [
      'kind',
      'occurrence_ref',
      'source_kind',
      'source_native_ref',
      'title',
      'coordinate',
      'schedule_ref',
      'placement_material_state_ref',
      'placement',
    ],
    'Scheduled Timeline Occurrence',
  );
  if (payload.source_kind !== 'routine' && payload.source_kind !== 'event') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Scheduled Timeline Occurrence source kind is unsupported.',
    );
  }
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Scheduled Timeline Occurrence title must be a non-empty string.',
    );
  }
  if (!isRecord(payload.placement)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Scheduled Timeline Occurrence placement has an unsupported representation.',
    );
  }
  const common = {
    kind: 'scheduled_occurrence' as const,
    occurrenceRef: parseUuidV7(payload.occurrence_ref, 'occurrence_ref'),
    sourceKind: payload.source_kind as 'routine' | 'event',
    sourceNativeRef: parseUuidV7(
      payload.source_native_ref,
      'source_native_ref',
    ),
    title: payload.title,
    coordinate:
      payload.coordinate === null
        ? null
        : parseOccurrenceCoordinate(payload.coordinate),
    scheduleRef: parseUuidV7(payload.schedule_ref, 'schedule_ref'),
    placementMaterialStateRef: parseUuidV7(
      payload.placement_material_state_ref,
      'placement_material_state_ref',
    ),
  };
  const placement = payload.placement;

  switch (placement.temporal_form) {
    case 'date_span': {
      requireExactKeys(
        placement,
        ['temporal_form', 'start_date', 'end_date_exclusive'],
        'Scheduled Timeline Occurrence date-span placement',
      );
      const startDate = parsePlainDate(placement.start_date, 'start_date');
      const endDateExclusive = parsePlainDate(
        placement.end_date_exclusive,
        'end_date_exclusive',
      );
      if (Temporal.PlainDate.compare(startDate, endDateExclusive) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Scheduled Timeline Occurrence date span must be positive.',
        );
      }
      return Object.freeze({
        ...common,
        temporalForm: 'date-span' as const,
        startDate,
        endDateExclusive,
      });
    }
    case 'floating_local': {
      requireExactKeys(
        placement,
        ['temporal_form', 'starts_local_at', 'ends_local_at'],
        'Scheduled Timeline Occurrence floating placement',
      );
      const startsLocalAt = parseLocalDateTime(
        placement.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        placement.ends_local_at,
        'ends_local_at',
      );
      if (Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Scheduled Timeline Occurrence floating placement must be positive.',
        );
      }
      return Object.freeze({
        ...common,
        temporalForm: 'floating-local' as const,
        startsLocalAt,
        endsLocalAt,
      });
    }
    case 'named_zone_local': {
      requireExactKeys(
        placement,
        [
          'temporal_form',
          'starts_local_at',
          'ends_local_at',
          'zone_id',
          'resolved_start_at',
          'resolved_end_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        'Scheduled Timeline Occurrence named-zone placement',
      );
      const startsLocalAt = parseLocalDateTime(
        placement.starts_local_at,
        'starts_local_at',
      );
      const endsLocalAt = parseLocalDateTime(
        placement.ends_local_at,
        'ends_local_at',
      );
      const resolvedStartAt = parseInstant(
        placement.resolved_start_at,
        'resolved_start_at',
      );
      const resolvedEndAt = parseInstant(
        placement.resolved_end_at,
        'resolved_end_at',
      );
      if (
        Temporal.PlainDateTime.compare(startsLocalAt, endsLocalAt) >= 0 ||
        Temporal.Instant.compare(resolvedStartAt, resolvedEndAt) >= 0
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Scheduled Timeline Occurrence named-zone placement must be positive.',
        );
      }
      return Object.freeze({
        ...common,
        temporalForm: 'named-zone-local' as const,
        startsLocalAt,
        endsLocalAt,
        zoneId: parseZoneId(placement.zone_id, 'zone_id'),
        resolvedStartAt,
        resolvedEndAt,
        displayStartsLocalAt: parseLocalDateTime(
          placement.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          placement.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }
    case 'absolute': {
      requireExactKeys(
        placement,
        [
          'temporal_form',
          'starts_at',
          'ends_at',
          'display_starts_local_at',
          'display_ends_local_at',
        ],
        'Scheduled Timeline Occurrence absolute placement',
      );
      const startsAt = parseInstant(placement.starts_at, 'starts_at');
      const endsAt = parseInstant(placement.ends_at, 'ends_at');
      if (Temporal.Instant.compare(startsAt, endsAt) >= 0) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Scheduled Timeline Occurrence absolute placement must be positive.',
        );
      }
      return Object.freeze({
        ...common,
        temporalForm: 'absolute' as const,
        startsAt,
        endsAt,
        displayStartsLocalAt: parseLocalDateTime(
          placement.display_starts_local_at,
          'display_starts_local_at',
        ),
        displayEndsLocalAt: parseLocalDateTime(
          placement.display_ends_local_at,
          'display_ends_local_at',
        ),
      });
    }
    case 'coarse_local_period':
      requireExactKeys(
        placement,
        ['temporal_form', 'local_date', 'period'],
        'Scheduled Timeline Occurrence coarse placement',
      );
      if (
        placement.period !== 'morning' &&
        placement.period !== 'afternoon' &&
        placement.period !== 'evening'
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Scheduled Timeline Occurrence coarse period is unsupported.',
        );
      }
      return Object.freeze({
        ...common,
        temporalForm: 'coarse-local-period' as const,
        localDate: parsePlainDate(placement.local_date, 'local_date'),
        period: placement.period,
      });
    default:
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Scheduled Timeline Occurrence placement form is unsupported.',
      );
  }
}

function parseExpectedOccurrence(
  payload: Record<string, unknown>,
): TemporalTimelineExpectedOccurrenceItem {
  requireExactKeys(
    payload,
    [
      'kind',
      'occurrence_ref',
      'source_kind',
      'source_native_ref',
      'title',
      'coordinate',
    ],
    'Expected Timeline Occurrence',
  );
  if (payload.source_kind !== 'routine' && payload.source_kind !== 'event') {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Expected Timeline Occurrence source kind is unsupported.',
    );
  }
  if (typeof payload.title !== 'string' || payload.title.trim().length === 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Expected Timeline Occurrence title must be a non-empty string.',
    );
  }
  return Object.freeze({
    kind: 'expected_occurrence' as const,
    occurrenceRef: parseUuidV7(payload.occurrence_ref, 'occurrence_ref'),
    sourceKind: payload.source_kind,
    sourceNativeRef: parseUuidV7(
      payload.source_native_ref,
      'source_native_ref',
    ),
    title: payload.title,
    coordinate: parseOccurrenceCoordinate(payload.coordinate),
  });
}

function parseTimelineItem(payload: unknown): TemporalTimelineItem {
  if (isRecord(payload) && payload.kind === 'scheduled_occurrence') {
    return parseScheduledOccurrence(payload);
  }
  if (isRecord(payload) && payload.kind === 'expected_occurrence') {
    return parseExpectedOccurrence(payload);
  }
  return parseScheduledItem(payload);
}

function parseWindow(payload: unknown): TemporalTimelineWindow {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Temporal Timeline response has an unsupported representation.',
    );
  }

  if (payload.kind === 'empty') {
    requireExactKeys(
      payload,
      ['kind', 'start_date', 'end_date_exclusive', 'effective_zone_id'],
      'Temporal Timeline response',
    );
    return Object.freeze({
      kind: 'empty' as const,
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseZoneId(
        payload.effective_zone_id,
        'effective_zone_id',
      ),
    });
  }

  if (payload.kind === 'window') {
    requireExactKeys(
      payload,
      [
        'kind',
        'start_date',
        'end_date_exclusive',
        'effective_zone_id',
        'items',
      ],
      'Temporal Timeline response',
    );
    if (!Array.isArray(payload.items) || payload.items.length === 0) {
      throw new TemporalTimelineRemoteError(
        'protocol',
        'Populated Temporal Timeline window must contain at least one item.',
      );
    }
    return Object.freeze({
      kind: 'window' as const,
      startDate: parsePlainDateKey(payload.start_date, 'start_date'),
      endDateExclusive: parsePlainDateKey(
        payload.end_date_exclusive,
        'end_date_exclusive',
      ),
      effectiveZoneId: parseZoneId(
        payload.effective_zone_id,
        'effective_zone_id',
      ),
      items: Object.freeze(payload.items.map(parseTimelineItem)),
    });
  }

  throw new TemporalTimelineRemoteError(
    'protocol',
    'Temporal Timeline response has an unsupported representation.',
  );
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError';
}

async function fetchTimelineResponse(
  webFetch: typeof globalThis.fetch,
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<Response> {
  try {
    return await webFetch(input, init);
  } catch (error) {
    if (isAbortError(error)) {
      throw error;
    }
    throw new TemporalTimelineRemoteError(
      'transport',
      'Temporal Timeline request could not reach DANTE.',
    );
  }
}

async function responsePayload(
  response: Response,
  label: string,
): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${label} is not valid JSON.`,
      response.status,
    );
  }
}

async function checkpointCsrfToken(
  webFetch: typeof globalThis.fetch,
  signal?: AbortSignal,
): Promise<string> {
  const response = await fetchTimelineResponse(
    webFetch,
    SESSION_ENDPOINT,
    signal === undefined ? undefined : { signal },
  );
  const payload = await responsePayload(response, 'Auth session response');
  if (
    !response.ok ||
    !isRecord(payload) ||
    payload.authenticated !== true ||
    typeof payload.csrf_token !== 'string' ||
    payload.csrf_token.length === 0
  ) {
    throw new TemporalTimelineRemoteError(
      'http',
      'Timeline checkpoint requires an authenticated browser session.',
      response.status,
    );
  }
  return payload.csrf_token;
}

function checkpointCount(value: unknown, field: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      `${field} must be a non-negative integer.`,
    );
  }
  return value;
}

function parseWindowCheckpoint(
  payload: unknown,
  request: TemporalTimelineWindowCheckpointRequest,
): TemporalTimelineWindowCheckpointResult {
  if (!isRecord(payload)) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Timeline checkpoint response has an unsupported representation.',
    );
  }
  requireExactKeys(
    payload,
    [
      'start_date',
      'end_date_exclusive',
      'effective_zone_id',
      'source_count',
      'occurrence_count',
      'replayed_source_count',
    ],
    'Timeline checkpoint response',
  );
  const startDate = parsePlainDateKey(payload.start_date, 'start_date');
  const endDateExclusive = parsePlainDateKey(
    payload.end_date_exclusive,
    'end_date_exclusive',
  );
  if (
    startDate !== request.startDate ||
    endDateExclusive !== request.endDateExclusive
  ) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Timeline checkpoint response does not match the requested window.',
    );
  }
  const sourceCount = checkpointCount(payload.source_count, 'source_count');
  const occurrenceCount = checkpointCount(
    payload.occurrence_count,
    'occurrence_count',
  );
  const replayedSourceCount = checkpointCount(
    payload.replayed_source_count,
    'replayed_source_count',
  );
  if (replayedSourceCount > sourceCount) {
    throw new TemporalTimelineRemoteError(
      'protocol',
      'Timeline checkpoint replay count exceeds its source count.',
    );
  }
  return Object.freeze({
    startDate,
    endDateExclusive,
    effectiveZoneId: parseZoneId(
      payload.effective_zone_id,
      'effective_zone_id',
    ),
    sourceCount,
    occurrenceCount,
    replayedSourceCount,
  });
}

export function createRemoteTemporalTimelineDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
  resolveDeviceTimeZone?: DeviceTimeZoneResolver,
): TemporalTimelineDataSource {
  const webFetch = createWebFetch(fetchFn, resolveDeviceTimeZone);

  return Object.freeze({
    async checkpointWindow(
      request: TemporalTimelineWindowCheckpointRequest,
      signal?: AbortSignal,
    ): Promise<TemporalTimelineWindowCheckpointResult> {
      validateCheckpointRequest(request);
      const csrf = await checkpointCsrfToken(webFetch, signal);
      const response = await fetchTimelineResponse(
        webFetch,
        TEMPORAL_OCCURRENCE_WINDOW_CHECKPOINT_ENDPOINT,
        {
          method: 'POST',
          headers: new Headers({
            'Content-Type': 'application/json',
            [CSRF_HEADER_NAME]: csrf,
          }),
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            start_date: request.startDate,
            end_date_exclusive: request.endDateExclusive,
          }),
          ...(signal === undefined ? {} : { signal }),
        },
      );
      const payload = await responsePayload(
        response,
        'Timeline checkpoint response',
      );
      if (!response.ok) {
        throw new TemporalTimelineRemoteError(
          'http',
          `Timeline checkpoint failed with HTTP ${response.status}.`,
          response.status,
        );
      }
      return parseWindowCheckpoint(payload, request);
    },

    async loadWindow(
      request: TemporalTimelineWindowRequest,
      signal?: AbortSignal,
    ): Promise<TemporalTimelineWindow> {
      validateWindowRequest(request);
      const query = new URLSearchParams({
        start_date: request.startDate,
        end_date_exclusive: request.endDateExclusive,
      });

      const response = await fetchTimelineResponse(
        webFetch,
        `${TEMPORAL_TIMELINE_WINDOW_ENDPOINT}?${query.toString()}`,
        signal === undefined ? undefined : { signal },
      );

      if (!response.ok) {
        throw new TemporalTimelineRemoteError(
          'http',
          `Temporal Timeline request failed with HTTP ${response.status}.`,
          response.status,
        );
      }

      const payload = await responsePayload(
        response,
        'Temporal Timeline response',
      );

      const window = parseWindow(payload);
      if (
        window.startDate !== request.startDate ||
        window.endDateExclusive !== request.endDateExclusive
      ) {
        throw new TemporalTimelineRemoteError(
          'protocol',
          'Temporal Timeline response does not match the requested window.',
          response.status,
        );
      }
      return window;
    },
  });
}
