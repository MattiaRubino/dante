export const WORLD_FOCUS_EFFECT_STATES = Object.freeze([
  'pending',
  'ambiguous',
  'partial-real',
  'reconciliation-required',
  'reversed',
  'compensated',
] as const);

export type WorldFocusEffectState = (typeof WORLD_FOCUS_EFFECT_STATES)[number];

export const WORLD_FOCUS_EXECUTION_REVALIDATION_STATES = Object.freeze([
  'not-required',
  'required-before-execution',
] as const);

export type WorldFocusExecutionRevalidationState =
  (typeof WORLD_FOCUS_EXECUTION_REVALIDATION_STATES)[number];

export type WorldFocusEffectPresentation = Readonly<{
  state: WorldFocusEffectState;
  executionRevalidation: WorldFocusExecutionRevalidationState;
}>;

function isRecord(value: unknown): value is Readonly<Record<string, unknown>> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isEffectState(value: unknown): value is WorldFocusEffectState {
  return (
    value === 'pending' ||
    value === 'ambiguous' ||
    value === 'partial-real' ||
    value === 'reconciliation-required' ||
    value === 'reversed' ||
    value === 'compensated'
  );
}

function isExecutionRevalidationState(
  value: unknown,
): value is WorldFocusExecutionRevalidationState {
  return value === 'not-required' || value === 'required-before-execution';
}

/**
 * Materializes a sanitized frontend presentation of an operation/effect state.
 * The caller must already have resolved the authoritative operation semantics;
 * this model does not execute, authorize, cancel, reverse, refund, compensate,
 * reconcile or infer canonical completion from provider acknowledgements.
 *
 * `state` and `executionRevalidation` are intentionally orthogonal. In
 * particular, a partial real effect cannot be erased as a generic failure, and
 * a cancellation signal cannot be reinterpreted as reversal or compensation.
 * Extra input fields are deliberately not copied across the frontend boundary.
 */
export function createWorldFocusEffectPresentation(
  input: unknown,
): WorldFocusEffectPresentation {
  if (!isRecord(input)) {
    throw new Error('World Focus effect presentation must be an object');
  }

  const { state, executionRevalidation } = input;

  if (!isEffectState(state)) {
    throw new Error(
      'World Focus effect state must be pending, ambiguous, partial-real, reconciliation-required, reversed or compensated',
    );
  }

  if (!isExecutionRevalidationState(executionRevalidation)) {
    throw new Error(
      'World Focus execution revalidation state must be not-required or required-before-execution',
    );
  }

  return Object.freeze({ state, executionRevalidation });
}
