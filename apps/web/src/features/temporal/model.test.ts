import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  commitTemporalDraft,
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  createTemporalDraft,
  deserializeTemporalPlacement,
  normalizeTemporalCapabilities,
  resetTemporalDraft,
  serializeTemporalPlacement,
  sortTemporalValidationIssues,
  temporalPlacementEquals,
  temporalValidationIssue,
  updateTemporalDraft,
  validateTemporalPlacement,
  type TemporalPlacement,
} from './model';

describe('temporal F0 model contract', () => {
  it('projects one exact fixed clock into different local dates', () => {
    const clock = createFixedTemporalClock(
      Temporal.Instant.from('2026-08-04T22:30:00Z'),
      'Europe/Rome',
    );

    expect(clock.now().toString()).toBe('2026-08-04T22:30:00Z');
    expect(clock.timeZoneId()).toBe('Europe/Rome');
    expect(clock.today().toString()).toBe('2026-08-05');
    expect(clock.today('America/New_York').toString()).toBe('2026-08-04');
  });

  it('keeps identity classes deterministic and independent in tests', () => {
    const ids = createDeterministicTemporalIdFactory('contract');

    expect(ids.projectionId()).toBe('contract:projection:1');
    expect(ids.operationId()).toBe('contract:operation:1');
    expect(ids.operationId()).toBe('contract:operation:2');
    expect(ids.undoToken()).toBe('contract:undo:1');
    expect(ids.projectionId()).toBe('contract:projection:2');
  });

  it('round-trips every supported temporal form without collapsing semantics', () => {
    const placements: readonly TemporalPlacement[] = [
      {
        kind: 'date-span',
        startDate: Temporal.PlainDate.from('2026-08-04'),
        endDateExclusive: Temporal.PlainDate.from('2026-08-05'),
      },
      {
        kind: 'floating-local',
        start: Temporal.PlainDateTime.from('2026-08-04T09:00'),
        end: Temporal.PlainDateTime.from('2026-08-04T10:00'),
      },
      {
        kind: 'zoned',
        start: Temporal.ZonedDateTime.from(
          '2026-03-29T01:30:00+01:00[Europe/Rome]',
        ),
        end: Temporal.ZonedDateTime.from(
          '2026-03-29T03:30:00+02:00[Europe/Rome]',
        ),
      },
      {
        kind: 'absolute',
        start: Temporal.Instant.from('2026-08-04T07:00:00Z'),
        end: Temporal.Instant.from('2026-08-04T08:00:00Z'),
      },
    ];

    for (const placement of placements) {
      const restored = deserializeTemporalPlacement(
        serializeTemporalPlacement(placement),
      );
      expect(restored.kind).toBe(placement.kind);
      expect(temporalPlacementEquals(restored, placement)).toBe(true);
      expect(validateTemporalPlacement(restored).valid).toBe(true);
    }
  });

  it('keeps DST-aware exact ordering for zoned placements', () => {
    const placement: TemporalPlacement = {
      kind: 'zoned',
      start: Temporal.ZonedDateTime.from(
        '2026-03-29T01:30:00+01:00[Europe/Rome]',
      ),
      end: Temporal.ZonedDateTime.from(
        '2026-03-29T03:30:00+02:00[Europe/Rome]',
      ),
    };

    expect(
      placement.end.toInstant().since(placement.start.toInstant()).total({
        unit: 'minutes',
      }),
    ).toBe(60);
    expect(validateTemporalPlacement(placement).valid).toBe(true);
  });

  it('rejects zero or reversed ranges instead of normalizing them silently', () => {
    const invalid: readonly TemporalPlacement[] = [
      {
        kind: 'date-span',
        startDate: Temporal.PlainDate.from('2026-08-04'),
        endDateExclusive: Temporal.PlainDate.from('2026-08-04'),
      },
      {
        kind: 'floating-local',
        start: Temporal.PlainDateTime.from('2026-08-04T10:00'),
        end: Temporal.PlainDateTime.from('2026-08-04T09:00'),
      },
      {
        kind: 'absolute',
        start: Temporal.Instant.from('2026-08-04T10:00:00Z'),
        end: Temporal.Instant.from('2026-08-04T10:00:00Z'),
      },
    ];

    for (const placement of invalid) {
      const result = validateTemporalPlacement(placement);
      expect(result.valid).toBe(false);
      expect(result.issues).toHaveLength(1);
    }
  });

  it('normalizes capabilities while keeping distinct semantic axes', () => {
    expect(
      normalizeTemporalCapabilities([
        'actual',
        'placement',
        'execution',
        'actual',
      ]),
    ).toEqual(['placement', 'execution', 'actual']);
  });

  it('supports dirty/reset/commit draft lifecycle without owning form fields', () => {
    const initial: Readonly<{
      title: string;
      minutes: number;
    }> = Object.freeze({ title: 'Call', minutes: 30 });
    const draft = createTemporalDraft(initial);
    const edited = updateTemporalDraft(
      draft,
      Object.freeze({ title: 'Call', minutes: 45 }),
      (left, right) =>
        left.title === right.title && left.minutes === right.minutes,
    );

    expect(edited.dirty).toBe(true);
    expect(resetTemporalDraft(edited).current).toBe(initial);

    const committed = commitTemporalDraft(edited);
    expect(committed.dirty).toBe(false);
    expect(committed.baseline.minutes).toBe(45);
  });

  it('sorts machine-readable validation issues deterministically', () => {
    const issues = sortTemporalValidationIssues([
      temporalValidationIssue('z', ['title']),
      temporalValidationIssue('b', ['placement', 'end']),
      temporalValidationIssue('a', ['placement', 'end']),
    ]);

    expect(issues.map((issue) => issue.code)).toEqual(['a', 'b', 'z']);
  });
});
