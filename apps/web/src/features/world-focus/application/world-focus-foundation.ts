export type WorldFocusValidationIssue = Readonly<{
  code: string;
  path: readonly (string | number)[];
}>;

export type WorldFocusValidationResult<Value> =
  | Readonly<{ ok: true; value: Value }>
  | Readonly<{ ok: false; issues: readonly WorldFocusValidationIssue[] }>;

export type WorldFocusBoundaryValidator<Value> = (
  input: unknown,
) => WorldFocusValidationResult<Value>;

export class WorldFocusBoundaryValidationError extends Error {
  readonly code = 'WORLD_FOCUS_BOUNDARY_VALIDATION';
  readonly issueCount: number;

  constructor(issueCount: number) {
    super('World Focus boundary validation failed');
    this.name = 'WorldFocusBoundaryValidationError';
    this.issueCount = issueCount;
  }
}

/**
 * Keeps runtime validation owned by the adapter boundary without coupling World
 * Focus to one schema library. Zod/Valibot/generated validators can satisfy the
 * same contract later.
 */
export function validateWorldFocusBoundary<Value>(
  input: unknown,
  validator: WorldFocusBoundaryValidator<Value>,
): Value {
  const result = validator(input);
  if (result.ok) {
    return result.value;
  }

  throw new WorldFocusBoundaryValidationError(result.issues.length);
}

export type WorldFocusReadLease = Readonly<{
  generation: number;
  signal: AbortSignal;
  isCurrent: () => boolean;
  commit: <Value>(operation: () => Value) => Value | undefined;
  release: () => void;
}>;

type ActiveRead = {
  generation: number;
  controller: AbortController;
  cleanup: () => void;
};

/**
 * Coordinates latest-only frontend reads. Superseded or upstream-aborted work
 * cannot commit into the active World. This primitive is intentionally limited
 * to obsolete reads; durable backend/Intelligence runs are a different lifetime.
 */
export class WorldFocusLatestReadCoordinator {
  #generation = 0;
  #active: ActiveRead | null = null;

  begin(upstreamSignal?: AbortSignal): WorldFocusReadLease {
    this.cancelCurrent();

    const generation = this.#generation + 1;
    this.#generation = generation;

    const controller = new AbortController();
    let released = false;
    let detachUpstream: () => void = () => undefined;

    const active: ActiveRead = {
      generation,
      controller,
      cleanup: () => detachUpstream(),
    };
    this.#active = active;

    if (upstreamSignal !== undefined) {
      const handleUpstreamAbort = () => {
        if (this.#active === active) {
          this.#active = null;
        }
        detachUpstream();
        controller.abort();
      };

      detachUpstream = () => {
        upstreamSignal.removeEventListener('abort', handleUpstreamAbort);
      };

      if (upstreamSignal.aborted) {
        handleUpstreamAbort();
      } else {
        upstreamSignal.addEventListener('abort', handleUpstreamAbort, {
          once: true,
        });
      }
    }

    const isCurrent = () =>
      released === false &&
      this.#active === active &&
      controller.signal.aborted === false;

    const release = () => {
      if (released) {
        return;
      }
      released = true;
      active.cleanup();
      if (this.#active === active) {
        this.#active = null;
      }
    };

    return Object.freeze({
      generation,
      signal: controller.signal,
      isCurrent,
      commit: <Value>(operation: () => Value) =>
        isCurrent() ? operation() : undefined,
      release,
    });
  }

  cancelCurrent() {
    const active = this.#active;
    if (active === null) {
      return;
    }

    this.#active = null;
    active.cleanup();
    active.controller.abort();
  }
}

export const WORLD_FOCUS_PERFORMANCE_MEASURES = Object.freeze({
  openToUsable: 'dante.world-focus.open-to-usable',
} as const);

export type WorldFocusPerformanceMeasureName =
  (typeof WORLD_FOCUS_PERFORMANCE_MEASURES)[keyof typeof WORLD_FOCUS_PERFORMANCE_MEASURES];

export type WorldFocusPerformanceTarget = Readonly<{
  now: () => number;
  measure: (
    name: WorldFocusPerformanceMeasureName,
    options: Readonly<{ start: number; duration: number }>,
  ) => void;
}>;

export type WorldFocusPerformanceSpan = Readonly<{
  finish: () => number | null;
  cancel: () => void;
}>;

function getBrowserPerformanceTarget(): WorldFocusPerformanceTarget | null {
  if (typeof globalThis.performance === 'undefined') {
    return null;
  }

  return {
    now: () => globalThis.performance.now(),
    measure: (name, options) => globalThis.performance.measure(name, options),
  };
}

/**
 * Vendor-neutral User Timing span. Instrumentation is best-effort and must
 * never break product behavior if a browser/observer rejects a measurement.
 */
export function startWorldFocusPerformanceSpan(
  name: WorldFocusPerformanceMeasureName,
  target: WorldFocusPerformanceTarget | null = getBrowserPerformanceTarget(),
): WorldFocusPerformanceSpan {
  const start = target?.now() ?? null;
  let active = true;

  return Object.freeze({
    finish: () => {
      if (!active || target === null || start === null) {
        return null;
      }
      active = false;

      const duration = Math.max(0, target.now() - start);
      try {
        target.measure(name, { start, duration });
      } catch {
        // Observability is deliberately non-authoritative and non-blocking.
      }
      return duration;
    },
    cancel: () => {
      active = false;
    },
  });
}
