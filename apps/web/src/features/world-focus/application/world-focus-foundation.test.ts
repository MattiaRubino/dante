import { describe, expect, it, vi } from 'vitest';

import {
  startWorldFocusPerformanceSpan,
  validateWorldFocusBoundary,
  WORLD_FOCUS_PERFORMANCE_MEASURES,
  WorldFocusBoundaryValidationError,
  WorldFocusLatestReadCoordinator,
  type WorldFocusPerformanceTarget,
} from './world-focus-foundation';

describe('World Focus B0 application foundation', () => {
  it('accepts only validated unknown boundary input', () => {
    const value = validateWorldFocusBoundary({ value: 7 }, (input) => {
      if (
        typeof input === 'object' &&
        input !== null &&
        'value' in input &&
        typeof input.value === 'number'
      ) {
        return { ok: true, value: input.value };
      }

      return {
        ok: false,
        issues: [{ code: 'invalid-value', path: ['value'] }],
      };
    });

    expect(value).toBe(7);
  });

  it('fails validation without leaking the rejected payload into the error', () => {
    expect(() =>
      validateWorldFocusBoundary('secret-payload', () => ({
        ok: false,
        issues: [{ code: 'invalid', path: [] }],
      })),
    ).toThrowError(WorldFocusBoundaryValidationError);

    try {
      validateWorldFocusBoundary('secret-payload', () => ({
        ok: false,
        issues: [{ code: 'invalid', path: [] }],
      }));
    } catch (error) {
      expect(error).toBeInstanceOf(WorldFocusBoundaryValidationError);
      expect(String(error)).not.toContain('secret-payload');
      if (error instanceof WorldFocusBoundaryValidationError) {
        expect(error.issueCount).toBe(1);
        expect(error.code).toBe('WORLD_FOCUS_BOUNDARY_VALIDATION');
      }
    }
  });

  it('prevents a superseded read from committing', () => {
    const coordinator = new WorldFocusLatestReadCoordinator();
    const first = coordinator.begin();
    const firstCommit = vi.fn(() => 'first');

    const second = coordinator.begin();

    expect(first.signal.aborted).toBe(true);
    expect(first.isCurrent()).toBe(false);
    expect(first.commit(firstCommit)).toBeUndefined();
    expect(firstCommit).not.toHaveBeenCalled();

    expect(second.isCurrent()).toBe(true);
    expect(second.commit(() => 'second')).toBe('second');
  });

  it('invalidates a read when its upstream lifecycle is aborted', () => {
    const coordinator = new WorldFocusLatestReadCoordinator();
    const upstream = new AbortController();
    const lease = coordinator.begin(upstream.signal);

    upstream.abort();

    expect(lease.signal.aborted).toBe(true);
    expect(lease.isCurrent()).toBe(false);
    expect(lease.commit(() => 'late')).toBeUndefined();
  });

  it('releases completed reads without turning completion into cancellation', () => {
    const coordinator = new WorldFocusLatestReadCoordinator();
    const lease = coordinator.begin();

    lease.release();

    expect(lease.signal.aborted).toBe(false);
    expect(lease.isCurrent()).toBe(false);
    expect(lease.commit(() => 'late')).toBeUndefined();
  });

  it('records a non-blocking User Timing span once', () => {
    let now = 10;
    const measure = vi.fn();
    const target: WorldFocusPerformanceTarget = {
      now: () => now,
      measure,
    };
    const span = startWorldFocusPerformanceSpan(
      WORLD_FOCUS_PERFORMANCE_MEASURES.openToUsable,
      target,
    );

    now = 34;
    expect(span.finish()).toBe(24);
    expect(span.finish()).toBeNull();
    expect(measure).toHaveBeenCalledWith(
      WORLD_FOCUS_PERFORMANCE_MEASURES.openToUsable,
      { start: 10, duration: 24 },
    );
  });

  it('lets instrumentation fail without breaking product behavior', () => {
    let now = 3;
    const target: WorldFocusPerformanceTarget = {
      now: () => now,
      measure: () => {
        throw new Error('observer unavailable');
      },
    };
    const span = startWorldFocusPerformanceSpan(
      WORLD_FOCUS_PERFORMANCE_MEASURES.openToUsable,
      target,
    );

    now = 8;
    expect(span.finish()).toBe(5);
  });
});
