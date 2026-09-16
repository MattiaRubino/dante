import { describe, expect, it } from 'vitest';

import {
  temporalCreateDurationFromEndDateTime,
  temporalCreateEndDateTime,
} from './temporal-create-field-shared';

describe('Temporal Create Event end semantics', () => {
  it('keeps floating local time independent from zone transitions', () => {
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-03-29',
        '01:30',
        '2026-03-29',
        '03:30',
        'floating',
        'Europe/Rome',
      ),
    ).toBe(120);
    expect(
      temporalCreateEndDateTime(
        '2026-03-29',
        '01:30',
        120,
        'floating',
        'Europe/Rome',
      ),
    ).toEqual({ date: '2026-03-29', time: '03:30', dayOffset: 0 });
  });

  it('keeps named-zone authoring wall-clock based across the Europe/Rome spring-forward transition', () => {
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-03-29',
        '01:30',
        '2026-03-29',
        '03:30',
        'zoned',
        'Europe/Rome',
      ),
    ).toBe(120);
    expect(
      temporalCreateEndDateTime(
        '2026-03-29',
        '01:30',
        120,
        'zoned',
        'Europe/Rome',
      ),
    ).toEqual({ date: '2026-03-29', time: '03:30', dayOffset: 0 });
  });

  it('keeps named-zone authoring wall-clock based across the Europe/Rome fall-back transition', () => {
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-10-25',
        '01:30',
        '2026-10-25',
        '03:30',
        'zoned',
        'Europe/Rome',
      ),
    ).toBe(120);
    expect(
      temporalCreateEndDateTime(
        '2026-10-25',
        '01:30',
        120,
        'zoned',
        'Europe/Rome',
      ),
    ).toEqual({ date: '2026-10-25', time: '03:30', dayOffset: 0 });
  });

  it('preserves multi-day zoned Event end values', () => {
    expect(
      temporalCreateEndDateTime(
        '2026-08-04',
        '16:00',
        1080,
        'zoned',
        'Europe/Rome',
      ),
    ).toEqual({ date: '2026-08-05', time: '10:00', dayOffset: 1 });
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-08-04',
        '16:00',
        '2026-08-05',
        '10:00',
        'zoned',
        'Europe/Rome',
      ),
    ).toBe(1080);
  });

  it('rejects non-forward wall-clock values without performing zone validation', () => {
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-08-04',
        '16:00',
        '2026-08-04',
        '15:00',
        'zoned',
        'Europe/Rome',
      ),
    ).toBeNull();
    expect(
      temporalCreateDurationFromEndDateTime(
        '2026-08-04',
        '16:00',
        '2026-08-04',
        '17:00',
        'zoned',
        'Not/AZone',
      ),
    ).toBe(60);
  });
});
