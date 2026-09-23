import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalTimelineExpectedOccurrenceItem } from '../../../temporal/timeline-read';
import { expectedOccurrenceDateLaneItem } from './timeline-authoritative-hydration';

const OCCURRENCE_REF = '0199f5f0-6e71-7bc0-8ad0-a2f403f5617d';
const SOURCE_REF = '0199f5f0-6e72-7bc0-8ad0-a2f403f5617d';

function base(
  coordinate: TemporalTimelineExpectedOccurrenceItem['coordinate'],
): TemporalTimelineExpectedOccurrenceItem {
  return Object.freeze({
    kind: 'expected_occurrence' as const,
    occurrenceRef: OCCURRENCE_REF,
    sourceKind: 'routine' as const,
    sourceNativeRef: SOURCE_REF,
    title: 'Allenamento',
    coordinate,
  });
}

describe('expected Occurrence scheduling basis', () => {
  it('retains canonical calendar expected time only as an optional Schedule suggestion', () => {
    const item = expectedOccurrenceDateLaneItem(
      base(
        Object.freeze({
          familyCode: 'calendar-wall-clock' as const,
          generatedDate: Temporal.PlainDate.from('2026-10-05'),
          generatedWallTime: Temporal.PlainTime.from('08:30'),
          clockBasis: 'floating-local' as const,
          zoneId: null,
          resolvedAt: null,
        }),
      ),
      'Europe/Rome',
      'area-salute',
    );

    expect(item.occurrenceBasis).toEqual({
      occurrenceRef: OCCURRENCE_REF,
      sourceKind: 'routine',
      sourceNativeRef: SOURCE_REF,
      suggestedStartTime: '08:30',
    });
    expect(item).not.toHaveProperty('canonicalBasis');
  });

  it('does not invent a clock slot or duration for quota expectations', () => {
    const item = expectedOccurrenceDateLaneItem(
      base(
        Object.freeze({
          familyCode: 'quota-per-period' as const,
          periodStartDate: Temporal.PlainDate.from('2026-10-05'),
          periodEndDateExclusive: Temporal.PlainDate.from('2026-10-12'),
          frame: 'floating-local' as const,
          zoneId: null,
        }),
      ),
      'Europe/Rome',
      'area-salute',
    );

    expect(item.laneKind).toBe('flexible');
    expect(item.occurrenceBasis).toEqual({
      occurrenceRef: OCCURRENCE_REF,
      sourceKind: 'routine',
      sourceNativeRef: SOURCE_REF,
    });
    expect(item.occurrenceBasis).not.toHaveProperty('suggestedStartTime');
    expect(item).not.toHaveProperty('canonicalBasis');
  });
});
