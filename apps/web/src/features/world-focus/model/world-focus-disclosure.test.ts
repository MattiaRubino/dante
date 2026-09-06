import { describe, expect, it } from 'vitest';

import {
  createWorldFocusDisclosureOutcome,
  WORLD_FOCUS_DISCLOSURE_STATES,
} from './world-focus-disclosure';

describe('World Focus sanitized disclosure outcome', () => {
  it('keeps the production presentation vocabulary exact and intentionally small', () => {
    expect(WORLD_FOCUS_DISCLOSURE_STATES).toEqual([
      'available',
      'restricted',
      'unavailable',
    ]);
  });

  it('materializes an available outcome without inventing frontend authorization state', () => {
    const outcome = createWorldFocusDisclosureOutcome({
      status: 'available',
      authorized: true,
      principalId: 'principal-secret',
      actorId: 'actor-secret',
      recipientId: 'recipient-secret',
      purpose: 'whole-life',
      policyVersion: 'policy-secret',
      sourcePayload: { private: true },
    });

    expect(outcome).toEqual({ status: 'available' });
    expect(Object.isFrozen(outcome)).toBe(true);
    expect(outcome).not.toHaveProperty('authorized');
    expect(outcome).not.toHaveProperty('principalId');
    expect(outcome).not.toHaveProperty('actorId');
    expect(outcome).not.toHaveProperty('recipientId');
    expect(outcome).not.toHaveProperty('purpose');
    expect(outcome).not.toHaveProperty('policyVersion');
    expect(outcome).not.toHaveProperty('sourcePayload');
  });

  it('preserves restricted as a sanitized presentation result without leaking why or for whom', () => {
    const outcome = createWorldFocusDisclosureOutcome({
      status: 'restricted',
      reasonCode: 'purpose-recipient-mismatch:alice@example.com',
      recipient: 'alice@example.com',
      purpose: 'medical-review',
      worldRelevant: true,
      selected: true,
      resourceReference: { kind: 'record', key: 'sensitive-7' },
    });

    expect(outcome).toEqual({ status: 'restricted' });
    expect(outcome).not.toHaveProperty('reasonCode');
    expect(outcome).not.toHaveProperty('recipient');
    expect(outcome).not.toHaveProperty('purpose');
    expect(outcome).not.toHaveProperty('worldRelevant');
    expect(outcome).not.toHaveProperty('selected');
    expect(outcome).not.toHaveProperty('resourceReference');
  });

  it('keeps unavailable distinct from restricted and from provider/offline failure semantics', () => {
    const outcome = createWorldFocusDisclosureOutcome({
      status: 'unavailable',
      providerStatus: 'timeout',
      retryable: true,
      offline: true,
      reasonCode: 'provider-timeout',
    });

    expect(outcome).toEqual({ status: 'unavailable' });
    expect(outcome.status).not.toBe('restricted');
    expect(outcome).not.toHaveProperty('providerStatus');
    expect(outcome).not.toHaveProperty('retryable');
    expect(outcome).not.toHaveProperty('offline');
    expect(outcome).not.toHaveProperty('reasonCode');
  });

  it('does not let World relevance or interaction state widen an already-sanitized outcome', () => {
    const outcome = createWorldFocusDisclosureOutcome({
      status: 'restricted',
      worldId: 'future-unknown-world',
      worldRelevant: true,
      selected: true,
      primaryContextReference: { kind: 'asset', key: 'camera-a' },
    });

    expect(outcome).toEqual({ status: 'restricted' });
  });

  it('fails closed on malformed or non-finite disclosure states', () => {
    expect(() => createWorldFocusDisclosureOutcome(null)).toThrow(
      /disclosure outcome must be an object/,
    );
    expect(() => createWorldFocusDisclosureOutcome([])).toThrow(
      /disclosure outcome must be an object/,
    );
    expect(() => createWorldFocusDisclosureOutcome({})).toThrow(
      /disclosure status must be available, restricted or unavailable/,
    );
    expect(() =>
      createWorldFocusDisclosureOutcome({ status: 'allowed' }),
    ).toThrow(/disclosure status must be available, restricted or unavailable/);
    expect(() =>
      createWorldFocusDisclosureOutcome({ status: ' available ' }),
    ).toThrow(/disclosure status must be available, restricted or unavailable/);
  });
});
