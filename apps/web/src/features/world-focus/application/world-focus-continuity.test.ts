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
        threadReference: { kind: 'release', key: 'music-one' },
        checkpointReference: { kind: 'material-state', key: 'music-one-master-v1' },
        continuationReference: { kind: 'continuation-intent', key: 'music-one-next' },
        presentationState: 'active',
      },
    ],
  },
} as const;

describe('World Focus B2 continuity application boundary', () => {
  it('accepts a bounded, ordered continuity projection for the requested World', () => {
    const result = validateWorldFocusContinuityReadResult(READY_MUSIC_RESULT, 'music');

    expect(result.ok).toBe(true);
    if (result.ok && result.value.status === 'ready') {
      expect(result.value.projection.orderedItems[0]?.key).toBe('music-one');
      expect(result.value.projection.orderedItems[0]?.threadReference).toEqual({
        kind: 'release',
        key: 'music-one',
      });
      expect(result.value.projection.orderedItems[0]?.checkpointReference).toEqual({
        kind: 'material-state',
        key: 'music-one-master-v1',
      });
    }
  });

  it('rejects projection data from another World instead of attaching it locally', () => {
    expect(validateWorldFocusContinuityReadResult(READY_MUSIC_RESULT, 'travel').ok).toBe(false);
  });

  it('rejects duplicate keys, missing WP-01 references and unbounded first-open results', () => {
    const duplicate = {
      ...READY_MUSIC_RESULT,
      projection: {
        ...READY_MUSIC_RESULT.projection,
        orderedItems: [READY_MUSIC_RESULT.projection.orderedItems[0], READY_MUSIC_RESULT.projection.orderedItems[0]],
      },
    };
    const missingReference = {
      ...READY_MUSIC_RESULT,
      projection: {
        ...READY_MUSIC_RESULT.projection,
        orderedItems: [{ ...READY_MUSIC_RESULT.projection.orderedItems[0], threadReference: undefined }],
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
          threadReference: { kind: 'project', key: `thread-${index}` },
          checkpointReference: { kind: 'checkpoint', key: `checkpoint-${index}` },
          continuationReference: null,
          presentationState: 'active' as const,
        })),
      },
    };

    expect(validateWorldFocusContinuityReadResult(duplicate, 'music').ok).toBe(false);
    expect(validateWorldFocusContinuityReadResult(missingReference, 'music').ok).toBe(false);
    expect(validateWorldFocusContinuityReadResult(unbounded, 'music').ok).toBe(false);
  });

  it('turns invalid adapter payloads into the safe boundary validation error', async () => {
    const adapter: WorldFocusContinuityReadAdapter = {
      read: () => Promise.resolve({ status: 'ready', secret: 'do-not-leak' }),
    };
    const reader = createWorldFocusContinuityReader(adapter);

    await expect(reader('music')).rejects.toBeInstanceOf(WorldFocusBoundaryValidationError);
  });

  it('keeps intentionally sparse Worlds and unknown future Worlds empty', async () => {
    for (const worldId of ['finance', 'relationships', 'routine', 'apiary']) {
      await expect(readWorldFocusContinuity(worldId)).resolves.toEqual({
        status: 'empty',
        worldId,
      });
    }
  });

  it('provides deterministic positive continuity scenarios without backend claims', async () => {
    const music = await readWorldFocusContinuity('music');
    const travel = await readWorldFocusContinuity('travel');

    expect(music.status).toBe('ready');
    expect(travel.status).toBe('ready');
    if (music.status === 'ready') expect(music.projection.orderedItems).toHaveLength(2);
    if (travel.status === 'ready') expect(travel.projection.orderedItems).toHaveLength(1);
  });
});
