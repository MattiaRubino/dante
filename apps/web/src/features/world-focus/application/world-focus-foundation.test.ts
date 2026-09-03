import { describe, expect, it, vi } from 'vitest';

import {
  createWorldFocusScopedReader,
  startWorldFocusPerformanceSpan,
  validateWorldFocusBoundary,
  WORLD_FOCUS_PERFORMANCE_MEASURES,
  WorldFocusBoundaryValidationError,
  WorldFocusLatestReadCoordinator,
  type WorldFocusPerformanceTarget,
  type WorldFocusScopedReadAdapter,
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

  it('shares cancellation and validation mechanics without owning projection semantics', async () => {
    const observed: { signal: AbortSignal | null } = { signal: null };
    const adapter: WorldFocusScopedReadAdapter = ({ worldId, signal }) => {
      observed.signal = signal;
      return Promise.resolve({ worldId, value: 'bounded' });
    };
    const reader = createWorldFocusScopedReader(adapter, (input, expectedWorldId) => {
      if (
        typeof input === 'object' &&
        input !== null &&
        'worldId' in input &&
        input.worldId === expectedWorldId &&
        'value' in input &&
        input.value === 'bounded'
      ) {
        return { ok: true, value: input.value };
      }
      return { ok: false, issues: [{ code: 'invalid', path: [] }] };
    });
    const upstream = new AbortController();

    await expect(reader('apiary', upstream.signal)).resolves.toBe('bounded');
    expect(observed.signal?.aborted).toBe(false);
  });

  it('rejects a pre-aborted scoped read without invoking the adapter or validator', async () => {
    const adapter = vi.fn<WorldFocusScopedReadAdapter>(() =>
      Promise.resolve({ worldId: 'apiary', value: 'too-late' }),
    );
    const validator = vi.fn(() => ({ ok: true as const, value: 'too-late' }));
    const reader = createWorldFocusScopedReader(adapter, validator);
    const upstream = new AbortController();
    upstream.abort();

    await expect(reader('apiary', upstream.signal)).rejects.toMatchObject({
      name: 'AbortError',
    });
    expect(adapter).not.toHaveBeenCalled();
    expect(validator).not.toHaveBeenCalled();
  });

  it('rejects a late non-cooperative adapter result after upstream cancellation', async () => {
    let resolveLate!: (value: unknown) => void;
    const adapter: WorldFocusScopedReadAdapter = () =>
      new Promise((resolve) => {
        resolveLate = resolve;
      });
    const validator = vi.fn(() => ({ ok: true as const, value: 'late-result' }));
    const reader = createWorldFocusScopedReader(adapter, validator);
    const upstream = new AbortController();

    const pending = reader('apiary', upstream.signal);
    await Promise.resolve();
    upstream.abort();
    resolveLate({ worldId: 'apiary', value: 'late-result' });

    await expect(pending).rejects.toMatchObject({ name: 'AbortError' });
    expect(validator).not.toHaveBeenCalled();
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
