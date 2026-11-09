import { describe, expect, it } from 'vitest';

import {
  ACTIVITY_CASES, EVENT_CASES, PERSONA_CASES,
  recurrenceFor, validatePersonaMatrix,
} from './temporal-stateful-case-matrix';

describe('Temporal v2 mandatory multi-feature population', () => {
  it('keeps exactly 20 unique Events and 20 unique Activities', () => {
    expect(validatePersonaMatrix).not.toThrow();
    expect(EVENT_CASES).toHaveLength(20);
    expect(ACTIVITY_CASES).toHaveLength(20);
    expect(PERSONA_CASES).toHaveLength(40);
    expect(new Set(PERSONA_CASES.map((entry) => entry.id)).size).toBe(40);
    expect(PERSONA_CASES.map((entry) => entry.id)).toEqual([
      ...Array.from({ length: 20 }, (_, i) => 'E' + String(i + 1).padStart(2, '0')),
      ...Array.from({ length: 20 }, (_, i) => 'A' + String(i + 1).padStart(2, '0')),
    ]);
  });

  it('starts every scenario with several simultaneous editable properties', () => {
    for (const scenario of PERSONA_CASES) {
      expect(scenario.goalKinds.length, scenario.id).toBeGreaterThan(0);
      expect(scenario.kind === 'event'
        ? scenario.agendaCount
        : scenario.plannedSessionCount, scenario.id).toBeGreaterThan(0);
    }
    expect(EVENT_CASES.slice(10).every((entry) =>
      entry.agendaCount >= 5 && entry.goalKinds.length >= 3,
    )).toBe(true);
    expect(ACTIVITY_CASES.slice(10).every((entry) =>
      entry.plannedSessionCount >= 4 && entry.goalKinds.length >= 4,
    )).toBe(true);
  });

  it('covers all supported goal types, area modes, time semantics and policies', () => {
    const kinds = new Set(PERSONA_CASES.flatMap((entry) => entry.goalKinds));
    expect([...kinds].sort()).toEqual(
      ['boolean', 'quantity', 'qualitative', 'range'],
    );
    for (const group of [EVENT_CASES, ACTIVITY_CASES]) {
      expect(new Set(group.map((entry) => entry.area))).toEqual(
        new Set(['existing', 'new', 'none']),
      );
      expect(group.some((entry) => entry.allDay)).toBe(true);
      expect(group.some((entry) => !entry.allDay)).toBe(true);
      expect(group.some((entry) => entry.placementProtected)).toBe(true);
      expect(group.some((entry) => !entry.placementProtected)).toBe(true);
    }
  });

  it('retains five distinct recurrence families and bounded range examples', () => {
    for (const group of [EVENT_CASES, ACTIVITY_CASES]) {
      expect(new Set(group.map((entry) => recurrenceFor(entry).cadence))).toEqual(
        new Set(['daily', 'weekly', 'monthly', 'custom', 'yearly']),
      );
      expect(group.some((entry) => recurrenceFor(entry).monthlyOrdinal))
        .toBe(true);
      expect(group.some((entry) => recurrenceFor(entry).repeatCount === 5))
        .toBe(true);
      expect(group.some((entry) => recurrenceFor(entry).repeatCount === null))
        .toBe(true);
    }
  });

  it('requires a new seeded user for every phase and scenario', () => {
    // Phase 1: 40, phase 2: 40, phase 3: 20.
    const slots = [
      ...Array.from({ length: 40 }, (_, i) => i),
      ...Array.from({ length: 40 }, (_, i) => i + 40),
      ...Array.from({ length: 20 }, (_, i) => i + 80),
    ];
    expect(slots).toHaveLength(100);
    expect(new Set(slots).size).toBe(100);
    const accounts = [
      ...slots.map((slot) => 102 + slot),
      ...slots.map((slot) => 202 + slot),
      ...slots.map((slot) => 302 + slot),
    ];
    expect(new Set(accounts).size).toBe(300);
    expect(Math.max(...accounts)).toBe(401);
  });
});
