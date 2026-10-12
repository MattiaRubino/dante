import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import {
  clearWorldFocusEntry,
  primeWorldFocusEntry,
  readWorldFocusEntry,
} from './world-focus-transition';

const MUSIC_ORIGIN = Object.freeze({
  left: 420,
  top: 240,
  width: 120,
  height: 120,
});

describe('World Focus pre-M0 falsification — transient route handoff', () => {
  beforeEach(() => {
    clearWorldFocusEntry();
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-09-02T17:30:00Z'));
  });

  afterEach(() => {
    clearWorldFocusEntry();
    vi.useRealTimers();
  });

  it('does not resurrect a stale opener handoff after another World consumes the route boundary', () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: MUSIC_ORIGIN,
    });

    expect(readWorldFocusEntry('travel', 'worlds')).toBeNull();
    expect(readWorldFocusEntry('music', 'home')).toBeNull();
  });

  it('does not resurrect a stale opener handoff after the same World is entered from a different source', () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: MUSIC_ORIGIN,
    });

    expect(readWorldFocusEntry('music', 'worlds')).toBeNull();
    expect(readWorldFocusEntry('music', 'home')).toBeNull();
  });

  it('keeps token clearing monotonic when a newer opener supersedes an older one', () => {
    const first = primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: MUSIC_ORIGIN,
    });
    const second = primeWorldFocusEntry({
      worldId: 'travel',
      source: 'home',
      origin: { left: 80, top: 96, width: 88, height: 88 },
    });

    clearWorldFocusEntry(first.token);

    expect(readWorldFocusEntry('travel', 'home')).toEqual(second);
  });

  it('expires the handoff and keeps it expired instead of allowing later reuse', () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: MUSIC_ORIGIN,
    });

    vi.advanceTimersByTime(5_001);

    expect(readWorldFocusEntry('music', 'home')).toBeNull();
    vi.setSystemTime(new Date('2026-09-02T17:30:01Z'));
    expect(readWorldFocusEntry('music', 'home')).toBeNull();
  });

  it('normalizes non-finite and non-positive opener geometry at the transient boundary', () => {
    const entry = primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: {
        left: Number.NaN,
        top: Number.POSITIVE_INFINITY,
        width: 0,
        height: -20,
      },
    });

    expect(entry.origin).toEqual({ left: 0, top: 0, width: 1, height: 1 });
  });
});
