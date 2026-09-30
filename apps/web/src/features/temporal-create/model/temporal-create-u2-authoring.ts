import { Temporal } from '@dante/time';

import type { TemporalCreateFields } from './temporal-create-session';

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

export type TemporalCreateU2AuthoringDraft = Readonly<{
  endDate: string;
  lifeArea: TemporalCreateU2LifeAreaDraft;
  itemColorCode: string | null;
}>;

function inferredEndDate(fields: TemporalCreateFields): string {
  try {
    const start = Temporal.PlainDateTime.from(
      `${fields.date}T${fields.startTime}`,
    );
    return start.add({ minutes: fields.durationMinutes }).toPlainDate().toString();
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
    itemColorCode: null,
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
