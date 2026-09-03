import { describe, expect, it } from 'vitest';

import {
  createWorldFocusEffectPresentation,
  WORLD_FOCUS_EFFECT_STATES,
  WORLD_FOCUS_EXECUTION_REVALIDATION_STATES,
} from './world-focus-effect';

describe('World Focus effect presentation', () => {
  it('preserves the finite effect vocabulary without collapsing materially different outcomes', () => {
    expect(WORLD_FOCUS_EFFECT_STATES).toEqual([
      'pending',
      'ambiguous',
      'partial-real',
      'reconciliation-required',
      'reversed',
      'compensated',
    ]);

    const reversed = createWorldFocusEffectPresentation({
      state: 'reversed',
      executionRevalidation: 'not-required',
    });
    const compensated = createWorldFocusEffectPresentation({
      state: 'compensated',
      executionRevalidation: 'not-required',
    });

    expect(reversed.state).toBe('reversed');
    expect(compensated.state).toBe('compensated');
    expect(reversed).not.toEqual(compensated);
  });

  it('keeps execution-time revalidation orthogonal to the displayed effect state', () => {
    expect(WORLD_FOCUS_EXECUTION_REVALIDATION_STATES).toEqual([
      'not-required',
      'required-before-execution',
    ]);

    expect(
      createWorldFocusEffectPresentation({
        state: 'pending',
        executionRevalidation: 'not-required',
      }),
    ).toEqual({
      state: 'pending',
      executionRevalidation: 'not-required',
    });

    expect(
      createWorldFocusEffectPresentation({
        state: 'pending',
        executionRevalidation: 'required-before-execution',
      }),
    ).toEqual({
      state: 'pending',
      executionRevalidation: 'required-before-execution',
    });
  });

  it('retains partial-real and ambiguous states instead of rewriting them as failure or cancellation', () => {
    expect(
      createWorldFocusEffectPresentation({
        state: 'partial-real',
        executionRevalidation: 'required-before-execution',
      }).state,
    ).toBe('partial-real');

    expect(
      createWorldFocusEffectPresentation({
        state: 'ambiguous',
        executionRevalidation: 'not-required',
      }).state,
    ).toBe('ambiguous');
  });

  it('copies only sanitized presentation fields and does not leak execution/provider/authorization detail', () => {
    const result = createWorldFocusEffectPresentation({
      state: 'reconciliation-required',
      executionRevalidation: 'required-before-execution',
      providerAck: 'accepted',
      cancelled: true,
      refundStatus: 'requested',
      authorization: { actor: 'hidden' },
      receipt: { externalId: 'secret' },
      payload: { amount: 10_000 },
    });

    expect(result).toEqual({
      state: 'reconciliation-required',
      executionRevalidation: 'required-before-execution',
    });
    expect(Object.keys(result)).toEqual(['state', 'executionRevalidation']);
  });

  it('does not infer reverse or compensation from cancellation/provider-style inputs', () => {
    expect(() =>
      createWorldFocusEffectPresentation({
        state: 'cancelled',
        executionRevalidation: 'not-required',
      }),
    ).toThrow();

    expect(() =>
      createWorldFocusEffectPresentation({
        state: 'provider-acknowledged',
        executionRevalidation: 'not-required',
      }),
    ).toThrow();
  });

  it('fails closed on malformed presentation states and returns immutable outcomes', () => {
    expect(() => createWorldFocusEffectPresentation(null)).toThrow();
    expect(() => createWorldFocusEffectPresentation({})).toThrow();
    expect(() =>
      createWorldFocusEffectPresentation({
        state: 'pending',
        executionRevalidation: 'already-authorized',
      }),
    ).toThrow();

    const result = createWorldFocusEffectPresentation({
      state: 'pending',
      executionRevalidation: 'required-before-execution',
    });
    expect(Object.isFrozen(result)).toBe(true);
  });
});
