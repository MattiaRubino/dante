import { describe, expect, it } from 'vitest';

import {
  createWorldFocusIdentityDescriptor,
  normalizeWorldFocusId,
} from './world-focus-identity';

describe('World Focus production identity', () => {
  it('accepts an opaque future World id without declaring it routable', () => {
    expect(normalizeWorldFocusId('  future-craft  ')).toBe('future-craft');
    expect(normalizeWorldFocusId('   ')).toBeUndefined();
    expect(normalizeWorldFocusId(null)).toBeUndefined();
  });

  it('creates a normalized presentation descriptor independently from fixture taxonomy', () => {
    expect(
      createWorldFocusIdentityDescriptor({
        id: ' future-craft ',
        label: ' Craft ',
        description: ' Future continuity context ',
      }),
    ).toEqual({
      id: 'future-craft',
      label: 'Craft',
      description: 'Future continuity context',
    });
  });

  it('rejects incomplete descriptors instead of manufacturing fallback semantics', () => {
    expect(() =>
      createWorldFocusIdentityDescriptor({
        id: 'future-craft',
        label: ' ',
        description: 'Future continuity context',
      }),
    ).toThrow(/label must not be empty/);
  });
});
