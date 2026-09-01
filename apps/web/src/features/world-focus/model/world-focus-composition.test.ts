import { describe, expect, it } from 'vitest';

import { defineWorldFocusComposition } from './world-focus-composition';

describe('World Focus composition descriptors', () => {
  it('keeps ordered stable/adaptive/ephemeral ownership without turning kinds into ontology', () => {
    const composition = defineWorldFocusComposition([
      {
        instanceId: 'continuity',
        kind: 'continuity',
        ownership: {
          stability: 'adaptive',
          origin: 'application-derived',
        },
      },
      {
        instanceId: 'user-pinned-context',
        kind: 'collection',
        ownership: { stability: 'stable', origin: 'user' },
      },
    ] as const);

    expect(composition.map((entry) => entry.instanceId)).toEqual([
      'continuity',
      'user-pinned-context',
    ]);
    expect(composition[0]?.ownership).toEqual({
      stability: 'adaptive',
      origin: 'application-derived',
    });
  });

  it('rejects duplicate or empty presentation identities', () => {
    expect(() =>
      defineWorldFocusComposition([
        {
          instanceId: 'same',
          kind: 'continuity',
          ownership: {
            stability: 'adaptive',
            origin: 'application-derived',
          },
        },
        {
          instanceId: 'same',
          kind: 'collection',
          ownership: { stability: 'stable', origin: 'user' },
        },
      ]),
    ).toThrowError('Duplicate World Focus composition instance: same');

    expect(() =>
      defineWorldFocusComposition([
        {
          instanceId: ' ',
          kind: 'continuity',
          ownership: {
            stability: 'adaptive',
            origin: 'application-derived',
          },
        },
      ]),
    ).toThrowError('World Focus composition instance id must not be empty');
  });
});
