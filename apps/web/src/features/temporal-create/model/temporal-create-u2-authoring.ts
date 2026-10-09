import { Temporal } from '@dante/time';

import type { TemporalCreateFields } from './temporal-create-session';
import type { TemporalSessionCaptureMode } from '../../temporal/authoring-data-source';

export const TEMPORAL_CREATE_U2_DEFAULT_COLOR = '#EA5C12';

export type TemporalCreateRealityMode =
  'manual' | 'review_on_end' | 'auto_confirm_outcome';

export type TemporalCreateU2LifeAreaDraft =
  | Readonly<{ kind: 'none' }>
  | Readonly<{
      kind: 'existing';
      lifeAreaRef: string;
      label: string;
      expectedRevision: number;
      colorCode: string | null;
      colorChanged: boolean;
    }>
  | Readonly<{
      kind: 'new';
      name: string;
      colorCode: string | null;
    }>;

export type TemporalCreateEventParticipantDraft = Readonly<{
  personRef: string;
  displayLabel: string;
  requirementCode: 'required' | 'optional';
}>;

export type TemporalCreateObjectiveKind =
  | 'boolean'
  | 'quantity'
  | 'qualitative'
  | 'range';

export type TemporalCreateObjectiveComparator = 'eq' | 'gte' | 'lte' | 'between';

export type TemporalCreateObjectiveDraft = Readonly<{
  id: string;
  label: string;
  resultKind: TemporalCreateObjectiveKind;
  comparatorCode: TemporalCreateObjectiveComparator | null;
  targetValue: string;
  targetMin: string;
  targetMax: string;
  unitCode: string;
}>;

export type TemporalCreateU2AuthoringDraft = Readonly<{
  endDate: string;
  lifeArea: TemporalCreateU2LifeAreaDraft;
  itemColorCode: string | null;
  realityMode: TemporalCreateRealityMode;
  objectives: readonly TemporalCreateObjectiveDraft[];
  eventParticipants: readonly TemporalCreateEventParticipantDraft[];
  activityStructure: TemporalCreateActivityStructureDraft;
}>;

export type TemporalCreatePlannedSliceDraft = Readonly<{
  id: string;
  title: string;
  timeEnabled?: boolean;
  date: string;
  startTime: string;
  endTime: string;
}>;

/** Extra occupied Activity bands. The first band uses the main date/time fields. */
export type TemporalCreateActivityIntervalDraft = Readonly<{
  id: string;
  date: string;
  startTime: string;
  endDate: string;
  endTime: string;
}>;

export type TemporalCreateActivityChildDraft = Readonly<{
  id: string;
  title: string;
  requirementCode: 'required' | 'optional';
  captureMode: TemporalSessionCaptureMode;
  realityMode?: TemporalCreateRealityMode | undefined;
  scheduleEnabled: boolean;
  startDate: string;
  startTime: string;
  endDate: string;
  endTime: string;
  plannedSlices: readonly TemporalCreatePlannedSliceDraft[];
}>;

export type TemporalCreateActivityStructureDraft = Readonly<{
  captureMode: TemporalSessionCaptureMode;
  realityMode: TemporalCreateRealityMode;
  placementProtected: boolean;
  childGuardMode: 'none' | 'confirm' | 'block';
  children: readonly TemporalCreateActivityChildDraft[];
  plannedSlices: readonly TemporalCreatePlannedSliceDraft[];
  activityIntervals: readonly TemporalCreateActivityIntervalDraft[];
}>;

function inferredEndDate(fields: TemporalCreateFields): string {
  try {
    const start = Temporal.PlainDateTime.from(
      `${fields.date}T${fields.startTime}`,
    );
    return start
      .add({ minutes: fields.durationMinutes })
      .toPlainDate()
      .toString();
  } catch {
    return fields.date;
  }
}

export function createTemporalCreateU2AuthoringDraft(
  fields: TemporalCreateFields,
): TemporalCreateU2AuthoringDraft {
  return Object.freeze({
    endDate: inferredEndDate(fields),
    lifeArea: Object.freeze({ kind: 'none' as const }),
    itemColorCode: TEMPORAL_CREATE_U2_DEFAULT_COLOR,
    realityMode: 'manual' as const,
    objectives: Object.freeze([]),
    eventParticipants: Object.freeze([]),
    activityStructure: Object.freeze({
      captureMode: 'disabled' as const,
      realityMode: 'manual' as const,
      placementProtected: false,
      childGuardMode: 'none' as const,
      children: Object.freeze([]),
      plannedSlices: Object.freeze([]),
      activityIntervals: Object.freeze([]),
    }),
  });
}

export function normalizeTemporalCreateU2EndDate(
  startDate: string,
  requestedEndDate: string,
): string {
  try {
    const start = Temporal.PlainDate.from(startDate);
    const end = Temporal.PlainDate.from(requestedEndDate);
    return Temporal.PlainDate.compare(end, start) < 0
      ? start.toString()
      : end.toString();
  } catch {
    return startDate;
  }
}

export function patchTemporalCreateU2AuthoringDraft(
  current: TemporalCreateU2AuthoringDraft,
  patch: Partial<TemporalCreateU2AuthoringDraft>,
): TemporalCreateU2AuthoringDraft {
  return Object.freeze({ ...current, ...patch });
}

export function synchronizeTemporalCreateU2DraftWithFields(
  current: TemporalCreateU2AuthoringDraft,
  fields: TemporalCreateFields,
): TemporalCreateU2AuthoringDraft {
  return Object.freeze({
    ...current,
    endDate: normalizeTemporalCreateU2EndDate(fields.date, current.endDate),
  });
}
