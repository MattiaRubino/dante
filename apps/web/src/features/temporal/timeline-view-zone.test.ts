import { Temporal } from '@dante/time';
import { afterEach, describe, expect, it } from 'vitest';

import type { TemporalTimelineWindow } from './timeline-read';
import {
  TIMELINE_VIEW_ZONE_STORAGE_KEY,
  TIMELINE_SECONDARY_ZONES_STORAGE_KEY,
  addTimelineSecondaryZone,
  normalizeTimelineSecondaryZones,
  readTimelineSecondaryZones,
  saveTimelineSecondaryZones,
  sameTimelineTimeZone,
  swapTimelinePrimaryZone,
  timelineSecondaryRulerTick,
  projectTimelineWindowInZone,
  readTimelineViewZonePreference,
  saveTimelineViewZonePreference,
  timelineViewZoneForInstant,
} from './timeline-view-zone';

afterEach(() => window.localStorage.removeItem(TIMELINE_VIEW_ZONE_STORAGE_KEY));
// The two view-only preferences must not leak across tests.
afterEach(() => window.localStorage.removeItem(TIMELINE_SECONDARY_ZONES_STORAGE_KEY));

describe('Timeline timezone projection and browser preference', () => {

  it('adds up to two secondary zones, ignores duplicates and swaps a selected secondary into primary', () => {
    const first = addTimelineSecondaryZone('Europe/Rome', [], 'America/New_York');
    expect(first).toEqual(['America/New_York']);
    expect(addTimelineSecondaryZone('Europe/Rome', first, 'Europe/Rome')).toEqual(first);
    expect(addTimelineSecondaryZone('Europe/Rome', first, 'America/New_York')).toEqual(first);
    const both = addTimelineSecondaryZone('Europe/Rome', first, 'Asia/Tokyo');
    expect(addTimelineSecondaryZone('Europe/Rome', both, 'Asia/Kolkata')).toEqual(both);
    expect(swapTimelinePrimaryZone('Europe/Rome', 'Asia/Tokyo', both))
      .toEqual(['America/New_York', 'Europe/Rome']);
    expect(swapTimelinePrimaryZone('Europe/Rome', 'Europe/London', both))
      .toEqual(both);
    expect(() => addTimelineSecondaryZone('Europe/Rome', [], '+09:00')).toThrow();
    expect(sameTimelineTimeZone('UTC', 'Etc/UTC')).toBe(true);
    expect(addTimelineSecondaryZone('Etc/UTC', [], 'UTC')).toEqual([]);
    expect(normalizeTimelineSecondaryZones('Etc/UTC', ['UTC', 'Asia/Tokyo']))
      .toEqual(['Asia/Tokyo']);
  });

  it('persists ordered secondary IANA zones, sanitizes bad browser state and rejects invalid writes', () => {
    saveTimelineSecondaryZones(['America/New_York', 'Asia/Kolkata']);
    expect(readTimelineSecondaryZones('Europe/Rome'))
      .toEqual(['America/New_York', 'Asia/Kolkata']);
    expect(readTimelineSecondaryZones('Asia/Kolkata')).toEqual(['America/New_York']);
    expect(() => saveTimelineSecondaryZones(['+09:00'])).toThrow();
    expect(readTimelineSecondaryZones('Europe/Rome'))
      .toEqual(['America/New_York', 'Asia/Kolkata']);
    window.localStorage.setItem(TIMELINE_SECONDARY_ZONES_STORAGE_KEY,
      JSON.stringify(['America/New_York', 'Unknown/Zone', 'America/New_York', 'Asia/Tokyo']));
    expect(readTimelineSecondaryZones('Europe/Rome'))
      .toEqual(['America/New_York', 'Asia/Tokyo']);
    window.localStorage.setItem(TIMELINE_SECONDARY_ZONES_STORAGE_KEY, '{broken');
    expect(readTimelineSecondaryZones('Europe/Rome')).toEqual([]);
    expect(normalizeTimelineSecondaryZones('Europe/Rome', ['Europe/Rome', null, 'UTC']))
      .toEqual(['UTC']);
  });

  it('aligns fractional-offset and cross-midnight secondary labels by primary instant', () => {
    expect(timelineSecondaryRulerTick('2026-11-19', 8 * 60, 'Europe/Rome', 'America/New_York'))
      .toMatchObject({ time: '02:00', date: '2026-11-19', dayDelta: 0 });
    expect(timelineSecondaryRulerTick('2026-11-19', 30, 'Europe/Rome', 'America/New_York'))
      .toMatchObject({ time: '18:30', date: '2026-11-18', dayDelta: -1 });
    expect(timelineSecondaryRulerTick('2026-11-19', 9 * 60, 'Europe/Rome', 'Asia/Kathmandu'))
      .toMatchObject({ time: '13:45', dayDelta: 0 });
    expect(timelineSecondaryRulerTick('2026-03-29', 2 * 60 + 30,
      'Europe/Rome', 'America/New_York'))
      .toMatchObject({ time: '—', missingPrimaryHour: true });
    expect(() => timelineSecondaryRulerTick('2026-11-19', 1441,
      'Europe/Rome', 'Asia/Tokyo')).toThrow();
  });
  it('converts both boundaries from canonical instants without altering source zones or Schedule identity', () => {
    const source: TemporalTimelineWindow = {
      kind: 'window',
      startDate: '2026-11-18',
      endDateExclusive: '2026-11-20',
      effectiveZoneId: 'Europe/Rome',
      items: [{
        kind: 'scheduled_activity',
        activityRef: 'activity',
        scheduleRef: 'schedule',
        placementMaterialStateRef: 'state',
        title: 'Test',
        temporalForm: 'named-zone-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-11-18T15:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-11-19T00:00'),
        zoneId: 'Europe/Rome',
        endZoneId: 'Asia/Tokyo',
        resolvedStartAt: Temporal.Instant.from('2026-11-18T14:00:00Z'),
        resolvedEndAt: Temporal.Instant.from('2026-11-18T15:00:00Z'),
        displayStartsLocalAt: Temporal.PlainDateTime.from('2026-11-18T15:00'),
        displayEndsLocalAt: Temporal.PlainDateTime.from('2026-11-18T16:00'),
      }],
    };
    const projected = projectTimelineWindowInZone(source, 'Asia/Tokyo');
    expect(projected.effectiveZoneId).toBe('Asia/Tokyo');
    if (projected.kind !== 'window' || source.kind !== 'window') throw new Error();
    const changed = projected.items[0];
    const original = source.items[0];
    if (changed?.kind === 'expected_occurrence' ||
        original?.kind === 'expected_occurrence' ||
        changed?.temporalForm !== 'named-zone-local' ||
        original?.temporalForm !== 'named-zone-local') throw new Error();
    expect(changed.scheduleRef).toBe('schedule');
    expect(changed.zoneId).toBe('Europe/Rome');
    expect(changed.endZoneId).toBe('Asia/Tokyo');
    expect(changed.endsLocalAt.toString()).toContain('00:00');
    expect(changed.startsLocalAt.toString()).toContain('15:00');
    expect(changed.displayStartsLocalAt.toString()).toContain('23:00');
    expect(changed.displayEndsLocalAt.toString()).toContain('00:00');
    expect(changed.displayEndsLocalAt.toPlainDate().toString()).toBe('2026-11-19');
    expect(original.displayStartsLocalAt.toString()).toContain('15:00');
  });

  it('keeps floating local clocks unchanged and projects the same instant across dates', () => {
    const source: TemporalTimelineWindow = {
      kind: 'window', startDate: '2026-11-18', endDateExclusive: '2026-11-20',
      effectiveZoneId: 'Europe/Rome',
      items: [{
        kind: 'scheduled_event', eventRef: 'event', scheduleRef: 'schedule',
        placementMaterialStateRef: 'state', title: 'Floating',
        temporalForm: 'floating-local',
        startsLocalAt: Temporal.PlainDateTime.from('2026-11-18T09:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-11-18T10:00'),
      }],
    };
    const projected = projectTimelineWindowInZone(source, 'Asia/Tokyo');
    if (projected.kind !== 'window') throw new Error();
    expect(projected.items[0]).toBe(source.items[0]);
    expect(timelineViewZoneForInstant('2026-11-18T14:00:00Z', 'Asia/Tokyo'))
      .toMatchObject({ date: '2026-11-18', minute: 23 * 60 });
    expect(timelineViewZoneForInstant('2026-11-18T16:00:00Z', 'Asia/Tokyo'))
      .toMatchObject({ date: '2026-11-19', minute: 60 });
  });

  it('stores a named zone rather than GMT offset and returns to automatic', () => {
    saveTimelineViewZonePreference('Asia/Tokyo');
    expect(window.localStorage.getItem(TIMELINE_VIEW_ZONE_STORAGE_KEY)).toBe('Asia/Tokyo');
    expect(readTimelineViewZonePreference()).toBe('Asia/Tokyo');
    expect(() => saveTimelineViewZonePreference('+09:00')).toThrow();
    expect(window.localStorage.getItem(TIMELINE_VIEW_ZONE_STORAGE_KEY))
      .toBe('Asia/Tokyo');
    saveTimelineViewZonePreference(null);
    expect(readTimelineViewZonePreference()).toBeNull();
    window.localStorage.setItem(TIMELINE_VIEW_ZONE_STORAGE_KEY, 'Unknown/Zone');
    expect(readTimelineViewZonePreference()).toBeNull();
  });

  it('projects spring DST gaps from instants rather than fabricating two hours of work', () => {
    const start = Temporal.Instant.from('2026-03-29T00:30:00Z');
    const end = Temporal.Instant.from('2026-03-29T01:30:00Z');
    const source: TemporalTimelineWindow = {
      kind: 'window',
      startDate: '2026-03-28',
      endDateExclusive: '2026-03-31',
      effectiveZoneId: 'Etc/UTC',
      items: [{
        kind: 'scheduled_event',
        eventRef: 'event',
        scheduleRef: 'spring-schedule',
        placementMaterialStateRef: 'state',
        title: 'DST',
        temporalForm: 'absolute',
        startsAt: start,
        endsAt: end,
        displayStartsLocalAt: start.toZonedDateTimeISO('Etc/UTC').toPlainDateTime(),
        displayEndsLocalAt: end.toZonedDateTimeISO('Etc/UTC').toPlainDateTime(),
      }],
    };
    const projected = projectTimelineWindowInZone(source, 'Europe/Rome');
    if (projected.kind !== 'window') throw new Error();
    const item = projected.items[0];
    if (item?.kind === 'expected_occurrence' || item?.temporalForm !== 'absolute') throw new Error();
    expect(item.displayStartsLocalAt.toString()).toContain('01:30');
    expect(item.displayEndsLocalAt.toString()).toContain('03:30');
    expect(item.endsAt.since(item.startsAt).total('minutes')).toBe(60);
    expect(item.startsAt).toBe(start);
    expect(item.endsAt).toBe(end);
  });
});
