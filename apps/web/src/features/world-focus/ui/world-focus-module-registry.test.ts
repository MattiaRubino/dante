import { describe, expect, it } from 'vitest';

import { WorldFocusModuleRegistry } from './world-focus-module-registry';

describe('WorldFocusModuleRegistry', () => {
  it('preserves deterministic registration order and resolves known kinds', () => {
    const metric = { kind: 'metric', marker: 1 } as const;
    const trend = { kind: 'trend', marker: 2 } as const;
    const registry = new WorldFocusModuleRegistry([metric, trend]);

    expect(registry.kinds).toEqual(['metric', 'trend']);
    expect(registry.resolve('metric')).toBe(metric);
    expect(registry.resolve('trend')).toBe(trend);
    expect(registry.has('metric')).toBe(true);
  });

  it('fails safely for an unknown future kind', () => {
    const registry = new WorldFocusModuleRegistry([{ kind: 'metric' }]);

    expect(registry.resolve('future-specialist')).toBeNull();
    expect(registry.has('future-specialist')).toBe(false);
  });

  it('rejects duplicate and empty module kinds before rendering begins', () => {
    expect(
      () =>
        new WorldFocusModuleRegistry([
          { kind: 'metric', marker: 1 },
          { kind: 'metric', marker: 2 },
        ]),
    ).toThrowError('Duplicate World Focus module kind: metric');

    expect(
      () => new WorldFocusModuleRegistry([{ kind: '   ' }]),
    ).toThrowError('World Focus module kind must not be empty');
  });
});
