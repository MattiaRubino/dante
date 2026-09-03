import { describe, expect, it } from 'vitest';

import {
  createWorldFocusReferenceResolution,
  WORLD_FOCUS_REFERENCE_RESOLUTION_STATES,
} from './world-focus-reference-resolution';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus reference resolution', () => {
  it('keeps the finite presentation vocabulary exact', () => {
    expect(WORLD_FOCUS_REFERENCE_RESOLUTION_STATES).toEqual([
      'usable',
      'unresolved',
      'retired',
    ]);
  });

  it('preserves a usable reference without creating authority or successor state', () => {
    const resolution = createWorldFocusReferenceResolution({
      status: 'usable',
      reference: ref('activity', 'release-v2'),
    });

    expect(resolution).toEqual({
      status: 'usable',
      reference: { kind: 'activity', key: 'release-v2' },
    });
    expect(Object.isFrozen(resolution)).toBe(true);
    expect(Object.isFrozen(resolution.reference)).toBe(true);
    expect(resolution).not.toHaveProperty('authorized');
    expect(resolution).not.toHaveProperty('successorReference');
  });

  it('keeps ambiguous identity unresolved instead of inferring a successor', () => {
    const resolution = createWorldFocusReferenceResolution({
      status: 'unresolved',
      reference: ref('person', 'legacy-ref'),
      reasonCode: 'ambiguous-successor',
    });

    expect(resolution).toEqual({
      status: 'unresolved',
      reference: { kind: 'person', key: 'legacy-ref' },
      reasonCode: 'ambiguous-successor',
    });
    expect(resolution).not.toHaveProperty('successorReference');
  });

  it('preserves retired identity as a historical reference rather than never-existed', () => {
    const resolution = createWorldFocusReferenceResolution({
      status: 'retired',
      reference: ref('native-ref', 'retired-7'),
      reasonCode: 'retired-canonical-reference',
    });

    expect(resolution.reference).toEqual({
      kind: 'native-ref',
      key: 'retired-7',
    });
    expect(resolution.status).toBe('retired');
    expect(resolution.reasonCode).toBe('retired-canonical-reference');
  });

  it('normalizes bounded tokens and strips unrelated frontend authority/provider fields', () => {
    const input = {
      status: 'unresolved' as const,
      reference: ref('  asset  ', '  camera-a  '),
      reasonCode: '  split-ambiguous  ',
      authorized: true,
      providerStatus: 'online',
      successorReference: ref('asset', 'camera-b'),
    };

    const resolution = createWorldFocusReferenceResolution(input);

    expect(resolution).toEqual({
      status: 'unresolved',
      reference: { kind: 'asset', key: 'camera-a' },
      reasonCode: 'split-ambiguous',
    });
    expect(resolution).not.toHaveProperty('authorized');
    expect(resolution).not.toHaveProperty('providerStatus');
    expect(resolution).not.toHaveProperty('successorReference');
  });

  it('fails closed on empty references and empty reason codes', () => {
    expect(() =>
      createWorldFocusReferenceResolution({
        status: 'usable',
        reference: ref('', 'x'),
      }),
    ).toThrow(/reference kind must not be empty/);

    expect(() =>
      createWorldFocusReferenceResolution({
        status: 'unresolved',
        reference: ref('source', 'x'),
        reasonCode: '   ',
      }),
    ).toThrow(/reason code must not be empty/);
  });
});
