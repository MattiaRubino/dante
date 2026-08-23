import { describe, expect, it } from 'vitest';

import {
  instantToZonedDateTime,
  parseDuration,
  parseInstant,
  parsePlainDate,
  parsePlainDateTime,
  parsePlainTime,
  parseZonedDateTime,
  zonedDateTimeToInstant,
} from './index';

describe('@dante/time', () => {
  it('parses the supported Temporal semantic primitives', () => {
    expect(parseInstant('2026-08-22T18:00:00Z').toString()).toBe(
      '2026-08-22T18:00:00Z',
    );
    expect(parsePlainDate('2026-08-23').toString()).toBe('2026-08-23');
    expect(parsePlainTime('12:34:56').toString()).toBe('12:34:56');
    expect(parsePlainDateTime('2026-08-23T12:34:56').toString()).toBe(
      '2026-08-23T12:34:56',
    );
    expect(parseDuration('PT2H30M').toString()).toBe('PT2H30M');
  });

  it('preserves the Europe/Rome spring DST transition', () => {
    const before = instantToZonedDateTime(
      parseInstant('2026-03-29T00:30:00Z'),
      'Europe/Rome',
    );
    const after = instantToZonedDateTime(
      parseInstant('2026-03-29T01:30:00Z'),
      'Europe/Rome',
    );

    expect(before.hour).toBe(1);
    expect(before.minute).toBe(30);
    expect(before.offset).toBe('+01:00');

    expect(after.hour).toBe(3);
    expect(after.minute).toBe(30);
    expect(after.offset).toBe('+02:00');
  });

  it('round-trips an Instant through an IANA ZonedDateTime', () => {
    const original = parseInstant('2026-08-22T18:00:00Z');
    const zoned = instantToZonedDateTime(original, 'Europe/Rome');
    const roundTrip = zonedDateTimeToInstant(zoned);

    expect(zoned.timeZoneId).toBe('Europe/Rome');
    expect(zoned.offset).toBe('+02:00');
    expect(roundTrip.equals(original)).toBe(true);
  });

  it('performs PlainDateTime duration arithmetic without inventing a timezone', () => {
    const start = parsePlainDateTime('2026-08-23T10:15:00');
    const result = start.add(parseDuration('PT2H30M'));

    expect(result.year).toBe(2026);
    expect(result.month).toBe(8);
    expect(result.day).toBe(23);
    expect(result.hour).toBe(12);
    expect(result.minute).toBe(45);
  });

  it('parses a ZonedDateTime while preserving its instant semantics', () => {
    const zoned = parseZonedDateTime('2026-08-22T20:00:00+02:00[Europe/Rome]');

    expect(zoned.timeZoneId).toBe('Europe/Rome');
    expect(zoned.offset).toBe('+02:00');
    expect(zonedDateTimeToInstant(zoned).toString()).toBe(
      '2026-08-22T18:00:00Z',
    );
  });
});
