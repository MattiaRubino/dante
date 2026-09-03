import { describe, expect, it } from 'vitest';

import {
  createWorldFocusSyncPresentation,
  WORLD_FOCUS_CONNECTIVITY_STATES,
  WORLD_FOCUS_PROVIDER_DELIVERY_STATES,
  WORLD_FOCUS_REPLAY_STATES,
  WORLD_FOCUS_REQUEST_TIMING_STATES,
} from './world-focus-sync';

describe('World Focus sync presentation', () => {
  it('keeps connectivity, replay, provider delivery and request timing as independent finite axes', () => {
    expect(WORLD_FOCUS_CONNECTIVITY_STATES).toEqual(['online', 'offline']);
    expect(WORLD_FOCUS_REPLAY_STATES).toEqual(['idle', 'pending']);
    expect(WORLD_FOCUS_PROVIDER_DELIVERY_STATES).toEqual([
      'nominal',
      'lagging',
      'unknown',
    ]);
    expect(WORLD_FOCUS_REQUEST_TIMING_STATES).toEqual([
      'within-window',
      'timed-out',
      'unknown',
    ]);
  });

  it('represents offline state together with pending replay without pretending replay has completed', () => {
    expect(
      createWorldFocusSyncPresentation({
        connectivity: 'offline',
        replay: 'pending',
        providerDelivery: 'unknown',
        requestTiming: 'unknown',
      }),
    ).toEqual({
      connectivity: 'offline',
      replay: 'pending',
      providerDelivery: 'unknown',
      requestTiming: 'unknown',
    });
  });

  it('preserves provider lag and request timeout as distinct conditions that may coexist', () => {
    expect(
      createWorldFocusSyncPresentation({
        connectivity: 'online',
        replay: 'idle',
        providerDelivery: 'lagging',
        requestTiming: 'timed-out',
      }),
    ).toEqual({
      connectivity: 'online',
      replay: 'idle',
      providerDelivery: 'lagging',
      requestTiming: 'timed-out',
    });
  });

  it('does not turn timeout, offline or provider lag into a semantic negative or canonical freshness claim', () => {
    const result = createWorldFocusSyncPresentation({
      connectivity: 'offline',
      replay: 'pending',
      providerDelivery: 'lagging',
      requestTiming: 'timed-out',
      semanticNegative: true,
      canonicalFreshness: 'stale',
      result: false,
      sourceMissing: true,
    });

    expect(result).toEqual({
      connectivity: 'offline',
      replay: 'pending',
      providerDelivery: 'lagging',
      requestTiming: 'timed-out',
    });
    expect(Object.keys(result)).toEqual([
      'connectivity',
      'replay',
      'providerDelivery',
      'requestTiming',
    ]);
  });

  it('does not carry authoritative replay/provider implementation detail across the frontend boundary', () => {
    const result = createWorldFocusSyncPresentation({
      connectivity: 'online',
      replay: 'pending',
      providerDelivery: 'nominal',
      requestTiming: 'within-window',
      replayCursor: 'internal-42',
      providerAck: 'accepted',
      retryToken: 'secret',
      conflictResolution: 'last-write-wins',
      authorization: { actor: 'hidden' },
    });

    expect(result).toEqual({
      connectivity: 'online',
      replay: 'pending',
      providerDelivery: 'nominal',
      requestTiming: 'within-window',
    });
  });

  it('fails closed on collapsed or invented sync states and returns immutable outcomes', () => {
    expect(() => createWorldFocusSyncPresentation(null)).toThrow();
    expect(() => createWorldFocusSyncPresentation({})).toThrow();
    expect(() =>
      createWorldFocusSyncPresentation({
        connectivity: 'reconnecting',
        replay: 'pending',
        providerDelivery: 'nominal',
        requestTiming: 'within-window',
      }),
    ).toThrow();
    expect(() =>
      createWorldFocusSyncPresentation({
        connectivity: 'online',
        replay: 'replayed',
        providerDelivery: 'nominal',
        requestTiming: 'within-window',
      }),
    ).toThrow();

    const result = createWorldFocusSyncPresentation({
      connectivity: 'online',
      replay: 'idle',
      providerDelivery: 'unknown',
      requestTiming: 'unknown',
    });
    expect(Object.isFrozen(result)).toBe(true);
  });
});
