import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCoverageFacet,
  createWorldFocusFreshnessFacet,
  createWorldFocusMaterialPayloadFacet,
  createWorldFocusValidityFacet,
  WORLD_FOCUS_COVERAGE_STATES,
  WORLD_FOCUS_FRESHNESS_STATES,
  WORLD_FOCUS_MATERIAL_PAYLOAD_STATES,
  WORLD_FOCUS_VALIDITY_STATES,
} from './world-focus-basis';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus M1-2 basis facets', () => {
  it('keeps freshness, validity, coverage and payload lifecycle as separate finite vocabularies', () => {
    expect(WORLD_FOCUS_FRESHNESS_STATES).toEqual([
      'current',
      'stale',
      'unknown',
    ]);
    expect(WORLD_FOCUS_VALIDITY_STATES).toEqual([
      'current',
      'superseded',
      'retracted',
      'unresolved',
    ]);
    expect(WORLD_FOCUS_COVERAGE_STATES).toEqual([
      'complete',
      'incomplete',
      'conflicted',
      'unknown',
    ]);
    expect(WORLD_FOCUS_MATERIAL_PAYLOAD_STATES).toEqual([
      'present',
      'retired',
    ]);
  });

  it('distinguishes stale freshness from superseded and retracted validity', () => {
    const stale = createWorldFocusFreshnessFacet({
      status: 'stale',
      asOf: '2026-09-01T12:30:00Z',
    });
    const superseded = createWorldFocusValidityFacet({
      status: 'superseded',
      reasonCode: 'newer-material-state',
    });
    const retracted = createWorldFocusValidityFacet({
      status: 'retracted',
      reasonCode: 'source-retraction',
    });

    expect(stale.status).toBe('stale');
    expect(superseded.status).toBe('superseded');
    expect(retracted.status).toBe('retracted');
    expect(stale).not.toHaveProperty('reasonCode');
    expect(superseded).not.toHaveProperty('asOf');
  });

  it('keeps unknown freshness distinct from stale/current instead of inventing an as-of instant', () => {
    const freshness = createWorldFocusFreshnessFacet({ status: 'unknown' });

    expect(freshness).toEqual({ status: 'unknown' });
    expect(freshness).not.toHaveProperty('asOf');
  });

  it('keeps incomplete and conflicted coverage distinct from empty or false', () => {
    const incomplete = createWorldFocusCoverageFacet({
      status: 'incomplete',
      reasonCode: 'partial-source-window',
    });
    const conflicted = createWorldFocusCoverageFacet({
      status: 'conflicted',
      reasonCode: 'material-source-disagreement',
    });

    expect(incomplete.status).toBe('incomplete');
    expect(conflicted.status).toBe('conflicted');
    expect(incomplete).not.toHaveProperty('value');
    expect(conflicted).not.toHaveProperty('winner');
  });

  it('preserves MaterialState reference continuity when protected payload is retired', () => {
    const payload = createWorldFocusMaterialPayloadFacet({
      status: 'retired',
      materialStateReference: ref('material-state', '018f-retired'),
      reasonCode: 'redacted',
      retiredAt: '2026-08-30T09:15:00Z',
    });

    expect(payload).toEqual({
      status: 'retired',
      materialStateReference: {
        kind: 'material-state',
        key: '018f-retired',
      },
      reasonCode: 'redacted',
      retiredAt: '2026-08-30T09:15:00.000Z',
    });
    expect(payload).not.toHaveProperty('payload');
    expect(payload).not.toHaveProperty('authorized');
    expect(payload).not.toHaveProperty('providerStatus');
    expect(Object.isFrozen(payload)).toBe(true);
    expect(Object.isFrozen(payload.materialStateReference)).toBe(true);
  });

  it('represents present payload without treating availability as disclosure authorization', () => {
    const input = {
      status: 'present' as const,
      materialStateReference: ref('material-state', '018f-current'),
      authorized: true,
      providerStatus: 'online',
      payload: { secret: 'must-not-cross-facet' },
    };

    const payload = createWorldFocusMaterialPayloadFacet(input);

    expect(payload).toEqual({
      status: 'present',
      materialStateReference: {
        kind: 'material-state',
        key: '018f-current',
      },
    });
    expect(payload).not.toHaveProperty('authorized');
    expect(payload).not.toHaveProperty('providerStatus');
    expect(payload).not.toHaveProperty('payload');
  });

  it('fails closed on malformed as-of/retirement instants and empty reason codes', () => {
    expect(() =>
      createWorldFocusFreshnessFacet({
        status: 'stale',
        asOf: 'not-an-instant',
      }),
    ).toThrow(/as-of must be a valid instant/);

    expect(() =>
      createWorldFocusMaterialPayloadFacet({
        status: 'retired',
        materialStateReference: ref('material-state', 'x'),
        reasonCode: 'redacted',
        retiredAt: 'not-an-instant',
      }),
    ).toThrow(/retired-at must be a valid instant/);

    expect(() =>
      createWorldFocusValidityFacet({
        status: 'unresolved',
        reasonCode: '   ',
      }),
    ).toThrow(/reason code must not be empty/);

    expect(() =>
      createWorldFocusCoverageFacet({
        status: 'conflicted',
        reasonCode: '',
      }),
    ).toThrow(/reason code must not be empty/);
  });
});
