import { Temporal } from '@dante/time';

import type {
  RecurringSeriesSource,
  SeriesScope,
} from '../../../temporal/remote-recurring-series-edit';

/**
 * The recurrence's expected_count is relative to effective_from, not
 * a permanent total. A partial edit keeps the original finite final
 * occurrence unless the user explicitly changes the count control.
 */
export function initialRecurrenceForScope(
  source: RecurringSeriesSource,
  scope: SeriesScope,
): Record<string, unknown> {
  const remaining = scope === 'from_next'
    ? source.remainingAfterSelected
    : source.remainingIncludingSelected;
  const finite = source.recurrence.range_kind === 'expected_count';
  if (
    finite &&
    (
      typeof remaining !== 'number' ||
      !Number.isSafeInteger(remaining) ||
      remaining < 0
    )
  ) {
    throw new Error('Limite della serie finita non disponibile.');
  }
  return {
    ...source.recurrence,
    effective_from: scope === 'from_next'
      ? Temporal.PlainDate.from(source.selectedDate)
        .add({ days: 1 }).toString()
      : source.selectedDate,
    ...(finite ? { expected_occurrence_count: remaining } : {}),
  };
}
