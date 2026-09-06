import { describe, expect, it } from 'vitest';

import {
  createWorldFocusContextReferenceSet,
  sameWorldFocusContextReferenceSet,
} from './world-focus-context-reference';

describe('World Focus context reference ownership', () => {
  it('normalizes one primary plus ordered supporting references', () => {
    const references = createWorldFocusContextReferenceSet({
      primary: { kind: ' projection ', key: ' primary ' },
      supporting: [
        { kind: 'source', key: 'one' },
        { kind: 'source', key: 'two' },
      ],
    });

    expect(references).toEqual({
      primary: { kind: 'projection', key: 'primary' },
      supporting: [
        { kind: 'source', key: 'one' },
        { kind: 'source', key: 'two' },
      ],
    });
  });

  it('keeps supporting order semantically meaningful', () => {
    const left = createWorldFocusContextReferenceSet({
      primary: { kind: 'projection', key: 'primary' },
      supporting: [
        { kind: 'source', key: 'one' },
        { kind: 'source', key: 'two' },
      ],
    });
    const reordered = createWorldFocusContextReferenceSet({
      primary: { kind: 'projection', key: 'primary' },
      supporting: [
        { kind: 'source', key: 'two' },
        { kind: 'source', key: 'one' },
      ],
    });

    expect(sameWorldFocusContextReferenceSet(left, reordered)).toBe(false);
  });

  it('rejects duplicate and over-policy references', () => {
    expect(() =>
      createWorldFocusContextReferenceSet({
        primary: { kind: 'source', key: 'same' },
        supporting: [{ kind: 'source', key: 'same' }],
      }),
    ).toThrow(/must not contain duplicates/);

    expect(() =>
      createWorldFocusContextReferenceSet({
        primary: { kind: 'projection', key: 'primary' },
        supporting: [
          { kind: 'source', key: 'one' },
          { kind: 'source', key: 'two' },
        ],
        maxSupportingReferences: 1,
      }),
    ).toThrow(/exceed policy/);
  });
});
