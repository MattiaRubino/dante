import { describe, expect, it } from 'vitest';

import {
  createWorldFocusContinuityReader,
  validateWorldFocusContinuityReadResult,
  type WorldFocusContinuityReadAdapter,
} from './world-focus-continuity';
import { readWorldFocusContinuity } from './world-focus-continuity-runtime';
import { WorldFocusBoundaryValidationError } from './world-focus-foundation';

const READY_MUSIC_RESULT = {
  status: 'ready',
  projection: {
    schemaVersion: 1,
    worldId: 'music',
    orderedItems: [
      {
        key: 'music-one',
        title: 'One',
        context: 'Release',
        checkpoint: 'Master v1',
        presentationState: 'active',
      },
    ],
  },
} as const;

describe('World Focus B2 continuity application boundary', () => {
  it('accepts a bounded, ordered continuity projection for the requested World', () => {
    const result = validateWorldFocusContinuityReadResult(
      READY_MUSIC_RESULT,
      'music',
    );

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.status).toBe('ready');
      if (result.value.status === 'ready') {
        expect(result.value.projection.orderedItems[0]?.key).toBe('music-one');
      }
    }
  });

  it('rejects projection data from another World instead of attaching it locally', () => {
    const result = validateWorldFocusContinuityReadResult(
      READY_MUSIC_RESULT,
      'travel',
    );

    expect(result.ok).toBe(false);
  });

  it('rejects duplicate keys and unbounded first-open result sets', () => {
    const duplicate = {
      ...READY_MUSIC_RESULT,
      projection: {
        ...READY_MUSIC_RESULT.projection,
        orderedItems: [
          READY_MUSIC_RESULT.projection.orderedItems[0],
          READY_MUSIC_RESULT.projection.orderedItems[0],
        ],
      },
    };
    const unbounded = {
      ...READY_MUSIC_RESULT,
      projection: {
        ...READY_MUSIC_RESULT.projection,
        orderedItems: Array.from({ length: 5 }, (_, index) => ({
          key: `item-${index}`,
          title: `Item ${index}`,
          context: 'Project',
          checkpoint: `Checkpoint ${index}`,
          presentationState: 'active' as const,
        })),
      },
    };

    expect(validateWorldFocusContinuityReadResult(duplicate, 'music').ok).toBe(
      false,
    );
    expect(validateWorldFocusContinuityReadResult(unbounded, 'music').ok).toBe(
      false,
    );
  });

  it('turns invalid adapter payloads into the safe boundary validation error', async () => {
    const adapter: WorldFocusContinuityReadAdapter = {
      read: () => Promise.resolve({ status: 'ready', secret: 'do-not-leak' }),
    };
    const reader = createWorldFocusContinuityReader(adapter);

    await expect(reader('music')).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('keeps intentionally sparse Worlds empty instead of fabricating continuity', async () => {
    await expect(readWorldFocusContinuity('finance')).resolves.toEqual({
      status: 'empty',
      worldId: 'finance',
    });
    await expect(readWorldFocusContinuity('relationships')).resolves.toEqual({
      status: 'empty',
      worldId: 'relationships',
    });
    await expect(readWorldFocusContinuity('routine')).resolves.toEqual({
      status: 'empty',
      worldId: 'routine',
    });
  });

  it('provides deterministic positive continuity scenarios without backend claims', async () => {
    const body = await readWorldFocusContinuity('body');
    const music = await readWorldFocusContinuity('music');
    const travel = await readWorldFocusContinuity('travel');

    expect(body.status).toBe('ready');
    expect(music.status).toBe('ready');
    expect(travel.status).toBe('ready');
    if (body.status === 'ready') {
      expect(body.projection.orderedItems).toHaveLength(1);
      expect(body.projection.orderedItems[0]?.key).toBe('body-mobility-reset');
    }
    if (music.status === 'ready') {
      expect(music.projection.orderedItems).toHaveLength(2);
    }
    if (travel.status === 'ready') {
      expect(travel.projection.orderedItems).toHaveLength(1);
    }
  });
});
