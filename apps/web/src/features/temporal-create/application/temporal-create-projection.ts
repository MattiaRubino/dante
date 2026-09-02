import type { TemporalPlacement } from '../../temporal';
import {
  buildTemporalCreatePlacement,
  temporalCreateHasFlexibleIntent,
  validateTemporalCreateFields,
  type TemporalCreateAppearanceTone,
  type TemporalCreateFields,
} from '../model/temporal-create-session';
import type {
  TemporalCreateAppliedEffect,
  TemporalCreateMetadata,
} from './temporal-create-runtime';

export type TemporalCreateTimelineProjection = Readonly<{
  id: string;
  title: string;
  kind: 'activity' | 'event';
  contextId: string;
  appearanceTone: TemporalCreateAppearanceTone | null;
  dateKey: string | null;
  endDateExclusiveKey: string | null;
  startMinute: number | null;
  endMinute: number | null;
  allDay: boolean;
  flexible: boolean;
  recurring: boolean;
  preview: boolean;
}>;

function minuteOfDay(hour: number, minute: number): number {
  return hour * 60 + minute;
}

function projectPlacement(
  id: string,
  title: string,
  placement: TemporalPlacement | null,
  metadata: TemporalCreateMetadata,
  preview: boolean,
): TemporalCreateTimelineProjection {
  const specification = metadata.specification;
  const flexible = temporalCreateHasFlexibleIntent(specification);
  const recurring =
    specification.kind === 'event' &&
    specification.eventRecurrence.patternKind !== 'none';
  const appearanceTone = specification.appearanceTone;

  if (!placement) {
    return Object.freeze({
      id,
      title,
      kind: metadata.kind,
      contextId: metadata.contextId,
      appearanceTone,
      dateKey: null,
      endDateExclusiveKey: null,
      startMinute: null,
      endMinute: null,
      allDay: false,
      flexible,
      recurring,
      preview,
    });
  }

  if (placement.kind === 'date-span') {
    return Object.freeze({
      id,
      title,
      kind: metadata.kind,
      contextId: metadata.contextId,
      appearanceTone,
      dateKey: placement.startDate.toString(),
      endDateExclusiveKey: placement.endDateExclusive.toString(),
      startMinute: null,
      endMinute: null,
      allDay: true,
      flexible,
      recurring,
      preview,
    });
  }

  const start =
    placement.kind === 'absolute'
      ? placement.start.toZonedDateTimeISO(metadata.timeZoneId)
      : placement.start;
  const end =
    placement.kind === 'absolute'
      ? placement.end.toZonedDateTimeISO(metadata.timeZoneId)
      : placement.end;

  return Object.freeze({
    id,
    title,
    kind: metadata.kind,
    contextId: metadata.contextId,
    appearanceTone,
    dateKey: start.toPlainDate().toString(),
    endDateExclusiveKey: null,
    startMinute: minuteOfDay(start.hour, start.minute),
    endMinute: start.toPlainDate().equals(end.toPlainDate())
      ? Math.min(1440, minuteOfDay(end.hour, end.minute))
      : 1440,
    allDay: false,
    flexible,
    recurring,
    preview,
  });
}

export function temporalCreateTimelineProjectionFromEffect(
  effect: TemporalCreateAppliedEffect,
): TemporalCreateTimelineProjection {
  return projectPlacement(
    effect.projection.id,
    effect.projection.title,
    effect.projection.placement,
    effect.metadata,
    false,
  );
}

export function temporalCreateTimelinePreviewFromFields(
  fields: TemporalCreateFields,
): TemporalCreateTimelineProjection | null {
  if (
    fields.title.trim().length === 0 ||
    validateTemporalCreateFields(fields).length > 0
  ) {
    return null;
  }

  return projectPlacement(
    'temporal-create-preview',
    fields.title.trim(),
    buildTemporalCreatePlacement(fields),
    Object.freeze({
      kind: fields.kind,
      contextId: fields.contextId,
      notes: fields.notes.trim(),
      timeSemantics: fields.timeSemantics,
      timeZoneId: fields.timeZoneId,
      specification: fields,
    }),
    true,
  );
}
