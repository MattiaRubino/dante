import { describe, expect, it } from 'vitest';

import {
  createWorldFocusDerivedWorkReaders,
  type WorldFocusDerivedWorkReadAdapter,
} from './world-focus-derived-work';
import {
  readWorldFocusAttention,
  readWorldFocusComparison,
  readWorldFocusTrajectory,
} from './world-focus-derived-work-runtime';
import { WorldFocusBoundaryValidationError } from './world-focus-foundation';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus M1-2 WP application seams', () => {
  it('materializes Attention, Comparison and Trajectory without requiring DANTE', async () => {
    const [attention, comparison, trajectory] = await Promise.all([
      readWorldFocusAttention('music'),
      readWorldFocusComparison('music'),
      readWorldFocusTrajectory('music'),
    ]);

    expect(attention.status).toBe('ready');
    expect(comparison.status).toBe('ready');
    expect(trajectory.status).toBe('ready');
  });

  it('keeps an unknown future World sparse instead of fabricating derived work', async () => {
    await expect(readWorldFocusAttention('apiary')).resolves.toEqual({
      status: 'empty',
      worldId: 'apiary',
    });
    await expect(readWorldFocusComparison('apiary')).resolves.toEqual({
      status: 'empty',
      worldId: 'apiary',
    });
    await expect(readWorldFocusTrajectory('apiary')).resolves.toEqual({
      status: 'empty',
      worldId: 'apiary',
    });
  });

  it('rejects notification-shaped Attention that lacks a material matter/reason contract', async () => {
    const adapter: WorldFocusDerivedWorkReadAdapter = {
      readAttention: () =>
        Promise.resolve({
          status: 'ready',
          projection: {
            schemaVersion: 1,
            worldId: 'music',
            orderedItems: [
              {
                instanceId: 'notification-only',
                kind: 'attention',
                notificationId: 'n-1',
                state: 'unresolved',
              },
            ],
          },
        }),
      readComparison: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
      readTrajectory: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
    };
    const readers = createWorldFocusDerivedWorkReaders(adapter);

    await expect(readers.readAttention('music')).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('rejects one-member Comparison and present-as-missing Trajectory mutations', async () => {
    const adapter: WorldFocusDerivedWorkReadAdapter = {
      readAttention: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
      readComparison: () =>
        Promise.resolve({
          status: 'ready',
          projection: {
            schemaVersion: 1,
            worldId: 'music',
            orderedItems: [
              {
                instanceId: 'bad-compare',
                kind: 'comparison',
                mode: 'difference',
                subjectReferences: [ref('material-state', 'master-v3')],
                basisReference: null,
              },
            ],
          },
        }),
      readTrajectory: () =>
        Promise.resolve({
          status: 'ready',
          projection: {
            schemaVersion: 1,
            worldId: 'music',
            orderedItems: [
              {
                instanceId: 'bad-trajectory',
                kind: 'trajectory',
                subjectReference: ref('release', 'single-1'),
                axis: 'time',
                orderedPointReferences: [
                  ref('observation', 'day-1'),
                  ref('observation', 'day-2'),
                ],
                missingPositionReferences: [ref('observation', 'day-2')],
                orderingBasisReference: null,
                aggregationBasisReference: null,
              },
            ],
          },
        }),
    };
    const readers = createWorldFocusDerivedWorkReaders(adapter);

    await expect(readers.readComparison('music')).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
    await expect(readers.readTrajectory('music')).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });
});
