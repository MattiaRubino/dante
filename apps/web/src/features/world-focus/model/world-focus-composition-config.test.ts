import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCompositionConfig,
  inspectWorldFocusCompositionConfigVersion,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
} from './world-focus-composition-config';

describe('World Focus composition config', () => {
  it('creates an immutable current-schema snapshot without retaining arbitrary payload', () => {
    const config = createWorldFocusCompositionConfig({
      schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
      revision: 7,
      worldId: ' future-world ',
      entries: [
        {
          instanceId: ' situation ',
          kind: ' specialist-future ',
          visibility: 'visible',
          pinned: false,
          prominenceOverride: null,
          canonicalPayload: { secret: 'must-not-survive' },
        } as never,
      ],
    });

    expect(config).toEqual({
      schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
      revision: 7,
      worldId: 'future-world',
      entries: [
        {
          instanceId: 'situation',
          kind: 'specialist-future',
          visibility: 'visible',
          pinned: false,
          prominenceOverride: null,
        },
      ],
    });
    expect(config.entries[0]).not.toHaveProperty('canonicalPayload');
    expect(Object.isFrozen(config)).toBe(true);
    expect(Object.isFrozen(config.entries)).toBe(true);
    expect(Object.isFrozen(config.entries[0])).toBe(true);
  });

  it('rejects duplicate instances and invalid structural tokens instead of inventing identity', () => {
    expect(() =>
      createWorldFocusCompositionConfig({
        schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
        revision: 0,
        worldId: 'music',
        entries: [
          {
            instanceId: 'same',
            kind: 'situation',
            visibility: 'visible',
            pinned: false,
            prominenceOverride: null,
          },
          {
            instanceId: 'same',
            kind: 'unknown-future-kind',
            visibility: 'visible',
            pinned: false,
            prominenceOverride: null,
          },
        ],
      }),
    ).toThrow(/duplicate/i);

    expect(() =>
      createWorldFocusCompositionConfig({
        schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
        revision: -1,
        worldId: 'music',
        entries: [],
      }),
    ).toThrow(/revision/i);

    expect(() =>
      createWorldFocusCompositionConfig({
        schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
        revision: 0,
        worldId: '   ',
        entries: [],
      }),
    ).toThrow(/world/i);
  });

  it('classifies config schema compatibility explicitly without pretending to migrate', () => {
    expect(
      inspectWorldFocusCompositionConfigVersion(
        WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
      ),
    ).toEqual({ status: 'current' });
    expect(inspectWorldFocusCompositionConfigVersion(0)).toEqual({
      status: 'migration-required',
      fromVersion: 0,
    });
    expect(inspectWorldFocusCompositionConfigVersion(99)).toEqual({
      status: 'unsupported',
      schemaVersion: 99,
    });
    expect(inspectWorldFocusCompositionConfigVersion(Number.NaN)).toEqual({
      status: 'unsupported',
      schemaVersion: Number.NaN,
    });
  });

  it('keeps otherwise identical configuration snapshots isolated by open-ended World identity', () => {
    const base = {
      schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
      revision: 3,
      entries: [
        {
          instanceId: 'continuity',
          kind: 'continuity',
          visibility: 'visible' as const,
          pinned: true,
          prominenceOverride: null,
        },
      ],
    };

    const first = createWorldFocusCompositionConfig({ ...base, worldId: 'music' });
    const second = createWorldFocusCompositionConfig({
      ...base,
      worldId: 'future-world-2040',
    });

    expect(first.worldId).toBe('music');
    expect(second.worldId).toBe('future-world-2040');
    expect(first).not.toEqual(second);
  });
});
