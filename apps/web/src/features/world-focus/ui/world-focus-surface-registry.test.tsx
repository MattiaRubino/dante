import { describe, expect, it } from 'vitest';

import { WorldFocusSurfaceRegistry } from './world-focus-surface-registry';

describe('WorldFocusSurfaceRegistry', () => {
  it('preserves deterministic order and resolves only shipped surface kinds', () => {
    const insight = {
      kind: 'insight',
      marker: 1,
      render: () => null,
    } as const;
    const explore = {
      kind: 'explore',
      marker: 2,
      render: () => null,
    } as const;
    const registry = new WorldFocusSurfaceRegistry([insight, explore]);

    expect(registry.kinds).toEqual(['insight', 'explore']);
    expect(registry.resolve('insight')).toBe(insight);
    expect(registry.resolve('explore')).toBe(explore);
    expect(registry.resolve('future-specialist')).toBeNull();
  });

  it('rejects duplicate and empty kinds before runtime presentation', () => {
    expect(
      () =>
        new WorldFocusSurfaceRegistry([
          { kind: 'insight', render: () => null },
          { kind: 'insight', render: () => null },
        ]),
    ).toThrowError('Duplicate World Focus surface kind: insight');

    expect(
      () =>
        new WorldFocusSurfaceRegistry([
          { kind: '   ', render: () => null },
        ]),
    ).toThrowError('World Focus surface kind must not be empty');
  });
});
