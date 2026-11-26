import { describe, expect, it } from 'vitest';

import {
  nextFactualInterval,
  normalizeSessionBoundary,
  SESSION_MINUTE_MS,
  sessionBounds,
} from './session-recording-time-rules';

const m = SESSION_MINUTE_MS;

describe('Session recording temporal rules', () => {
  it('always creates a non-overlapping factual interval with a one-minute pause', () => {
    expect(nextFactualInterval({ previousEnd: 60 * m, now: 95 * m })).toEqual({
      start: 61 * m,
      end: 91 * m,
    });
  });

  it('does not invent a duplicate when the previous end is already near now', () => {
    expect(nextFactualInterval({ previousEnd: 94 * m, now: 95 * m })).toBeNull();
    expect(nextFactualInterval({ previousEnd: 95 * m, now: 95 * m })).toBeNull();
  });

  it('obeys parent maximum for a new named Session interval', () => {
    expect(nextFactualInterval({
      previousEnd: 12 * m,
      now: 100 * m,
      parentEnd: 16 * m,
    })).toEqual({ start: 13 * m, end: 16 * m });
    expect(nextFactualInterval({
      previousEnd: 15 * m,
      now: 100 * m,
      parentEnd: 16 * m,
    })).toBeNull();
  });

  it('normalizes only the changed start, using the previous end and current end', () => {
    const bounds = sessionBounds({
      boundary: 'start',
      current: { start: 15 * m, end: 27 * m },
      previous: { start: 0, end: 20 * m },
      now: 100 * m,
    });
    expect(bounds).toEqual({ min: 21 * m, max: 26 * m });
    expect(normalizeSessionBoundary(11 * m, bounds)).toBe(21 * m);
    expect(normalizeSessionBoundary(25 * m, bounds)).toBe(25 * m);
  });

  it('normalizes end against the next start even when edited bottom-to-top', () => {
    const bounds = sessionBounds({
      boundary: 'end',
      current: { start: 10 * m, end: 25 * m },
      next: { start: 20 * m, end: 29 * m },
      now: 100 * m,
    });
    expect(bounds).toEqual({ min: 11 * m, max: 19 * m });
    expect(normalizeSessionBoundary(25 * m, bounds)).toBe(19 * m);
  });

  it('caps a child to the main parent without affecting another child', () => {
    const bounds = sessionBounds({
      boundary: 'end',
      current: { start: 10 * m, end: 28 * m },
      parent: { start: 8 * m, end: 20 * m },
      now: 50 * m,
    });
    expect(normalizeSessionBoundary(28 * m, bounds)).toBe(20 * m);
  });

  it('reports no feasible value when a field has no minute of space', () => {
    expect(sessionBounds({
      boundary: 'start',
      current: { start: 10 * m, end: 11 * m },
      previous: { start: 1 * m, end: 10 * m },
      now: 20 * m,
    })).toBeNull();
  });

  it('creates only the available minute without modifying the previous interval', () => {
    expect(nextFactualInterval({ previousEnd: 10 * m, now: 12 * m })).toEqual({
      start: 11 * m,
      end: 12 * m,
    });
    expect(nextFactualInterval({ previousEnd: 10 * m, now: 11 * m })).toBeNull();
  });
});
