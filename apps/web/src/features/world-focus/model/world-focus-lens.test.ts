import { describe, expect, it } from 'vitest';

import {
  createWorldFocusLens,
  createWorldFocusTemporalLensCapability,
  normalizeWorldFocusTimePreset,
  resolveWorldFocusTimePreset,
} from './world-focus-lens';

describe('World Focus Lens', () => {
  it('normalizes only the finite accepted preset vocabulary', () => {
    expect(normalizeWorldFocusTimePreset('7d')).toBe('7d');
    expect(normalizeWorldFocusTimePreset('all')).toBe('all');
    expect(normalizeWorldFocusTimePreset('banana')).toBeUndefined();
    expect(normalizeWorldFocusTimePreset(30)).toBeUndefined();
  });

  it('rejects invalid capability definitions instead of silently repairing them', () => {
    expect(() =>
      createWorldFocusTemporalLensCapability('30d', []),
    ).toThrow('at least one preset');
    expect(() =>
      createWorldFocusTemporalLensCapability('30d', ['7d', '7d']),
    ).toThrow('must be unique');
    expect(() =>
      createWorldFocusTemporalLensCapability('30d', ['7d', '90d']),
    ).toThrow('default must be available');
  });

  it('falls back to the World default when a requested preset is unsupported', () => {
    const capability = createWorldFocusTemporalLensCapability('30d', [
      '30d',
      '90d',
      '1y',
    ]);

    expect(resolveWorldFocusTimePreset(capability, '90d')).toBe('90d');
    expect(resolveWorldFocusTimePreset(capability, '7d')).toBe('30d');
    expect(resolveWorldFocusTimePreset(capability, undefined)).toBe('30d');
    expect(resolveWorldFocusTimePreset(undefined, '90d')).toBeUndefined();
  });

  it('keeps relative and all-time intent distinct without resolving fake dates', () => {
    const capability = createWorldFocusTemporalLensCapability('30d', [
      '30d',
      'all',
    ]);

    expect(createWorldFocusLens(capability, '30d')).toEqual({
      time: { kind: 'relative', preset: '30d' },
    });
    expect(createWorldFocusLens(capability, 'all')).toEqual({
      time: { kind: 'all-time', preset: 'all' },
    });
    expect(createWorldFocusLens(undefined, '30d')).toEqual({});
  });
});
