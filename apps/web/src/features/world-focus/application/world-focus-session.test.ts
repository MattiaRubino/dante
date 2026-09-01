import { describe, expect, it } from 'vitest';

import { createWorldFocusTemporalLensCapability } from '../model/world-focus-lens';
import { createWorldFocusSessionSnapshot } from './world-focus-session';

describe('World Focus Session', () => {
  const capability = createWorldFocusTemporalLensCapability('30d', [
    '7d',
    '30d',
    '90d',
  ]);

  it('isolates scope identity by World and effective Lens', () => {
    const music = createWorldFocusSessionSnapshot({
      worldId: 'music',
      timeCapability: capability,
      requestedTimePreset: '90d',
    });
    const study = createWorldFocusSessionSnapshot({
      worldId: 'study',
      timeCapability: capability,
      requestedTimePreset: '90d',
    });

    expect(music.scopeKey).toBe('music|time:90d');
    expect(study.scopeKey).toBe('study|time:90d');
    expect(study.scopeKey).not.toBe(music.scopeKey);
  });

  it('uses the deterministic World default when URL state is absent or unsupported', () => {
    expect(
      createWorldFocusSessionSnapshot({
        worldId: 'music',
        timeCapability: capability,
        requestedTimePreset: undefined,
      }),
    ).toMatchObject({
      activeWorldId: 'music',
      lens: { time: { kind: 'relative', preset: '30d' } },
      scopeKey: 'music|time:30d',
    });

    expect(
      createWorldFocusSessionSnapshot({
        worldId: 'music',
        timeCapability: capability,
        requestedTimePreset: '1y',
      }).scopeKey,
    ).toBe('music|time:30d');
  });

  it('represents Worlds without a visible temporal Lens without inventing scope', () => {
    expect(
      createWorldFocusSessionSnapshot({
        worldId: 'relationships',
        timeCapability: undefined,
        requestedTimePreset: '30d',
      }),
    ).toEqual({
      activeWorldId: 'relationships',
      lens: {},
      scopeKey: 'relationships|time:none',
    });
  });
});
