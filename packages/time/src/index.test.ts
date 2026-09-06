import { describe, expect, it } from 'vitest';

import {
  detectDeviceTimeZone,
  instantToZonedDateTime,
  parseDuration,
  parseInstant,
  parsePlainDate,
  parsePlainDateTime,
  parsePlainTime,
  parseZonedDateTime,
  resolveEffectiveTimeZone,
  validateNamedTimeZone,
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

  it('preserves both instants of the America/New_York autumn overlap', () => {
    const earlier = instantToZonedDateTime(
      parseInstant('2026-11-01T05:30:00Z'),
      'America/New_York',
    );
    const later = instantToZonedDateTime(
      parseInstant('2026-11-01T06:30:00Z'),
      'America/New_York',
    );

    expect(earlier.hour).toBe(1);
    expect(earlier.minute).toBe(30);
    expect(earlier.offset).toBe('-04:00');

    expect(later.hour).toBe(1);
    expect(later.minute).toBe(30);
    expect(later.offset).toBe('-05:00');
    expect(earlier.toInstant().equals(later.toInstant())).toBe(false);
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

  it('detects the current device timezone through an injectable resolver', () => {
    expect(detectDeviceTimeZone(() => 'Europe/Rome')).toBe('Europe/Rome');
    expect(detectDeviceTimeZone(() => 'America/New_York')).toBe(
      'America/New_York',
    );
  });

  it('resolves follow-device policy from the currently detected device timezone', () => {
    expect(
      resolveEffectiveTimeZone({ mode: 'follow_device' }, 'Europe/Rome'),
    ).toBe('Europe/Rome');
    expect(
      resolveEffectiveTimeZone({ mode: 'follow_device' }, 'America/New_York'),
    ).toBe('America/New_York');
  });

  it('keeps fixed policy independent from a changed device timezone', () => {
    expect(
      resolveEffectiveTimeZone(
        { mode: 'fixed', timeZone: 'Europe/Rome' },
        'America/New_York',
      ),
    ).toBe('Europe/Rome');
  });

  it('rejects fixed UTC offsets where a named IANA timezone is required', () => {
    expect(() => validateNamedTimeZone('+02:00')).toThrow(RangeError);
    expect(() => validateNamedTimeZone('-0500')).toThrow(RangeError);
  });

  it('rejects missing device timezone for follow-device policy', () => {
    expect(() =>
      resolveEffectiveTimeZone({ mode: 'follow_device' }, undefined),
    ).toThrow(RangeError);
  });
});
