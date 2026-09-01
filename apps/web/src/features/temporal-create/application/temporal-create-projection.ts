import type { TemporalPlacement } from '../../temporal';
import {
  buildTemporalCreatePlacement,
  validateTemporalCreateFields,
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
  dateKey: string | null;
  startMinute: number | null;
  endMinute: number | null;
  allDay: boolean;
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
  if (!placement) {
    return Object.freeze({
      id,
      title,
      kind: metadata.kind,
      contextId: metadata.contextId,
      dateKey: null,
      startMinute: null,
      endMinute: null,
      allDay: false,
      preview,
    });
  }

  if (placement.kind === 'date-span') {
    return Object.freeze({
      id,
      title,
      kind: metadata.kind,
      contextId: metadata.contextId,
      dateKey: placement.startDate.toString(),
      startMinute: null,
      endMinute: null,
      allDay: true,
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
    dateKey: start.toPlainDate().toString(),
    startMinute: minuteOfDay(start.hour, start.minute),
    endMinute: start.toPlainDate().equals(end.toPlainDate())
      ? Math.min(1440, minuteOfDay(end.hour, end.minute))
      : 1440,
    allDay: false,
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
    }),
    true,
  );
}
