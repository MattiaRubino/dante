import { normalizeWorldFocusFixtureId } from '../model/world-focus-fixtures';
import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
  createWorldFocusTrajectoryPrimitive,
} from '../model/world-focus-work-primitives';
import type { WorldFocusId } from '../model/world-focus-identity';
import type { WorldFocusDerivedWorkReadAdapter } from './world-focus-derived-work';

const ref = (kind: string, key: string) => Object.freeze({ kind, key });

function createAbortError() {
  const error = new Error('World Focus derived work read aborted');
  error.name = 'AbortError';
  return error;
}

async function settle(signal: AbortSignal) {
  await Promise.resolve();
  if (signal.aborted) throw createAbortError();
}

function empty(worldId: WorldFocusId) {
  return Object.freeze({ status: 'empty' as const, worldId });
}

function musicOnly(worldId: WorldFocusId) {
  return normalizeWorldFocusFixtureId(worldId) === 'music';
}

/** Deterministic pre-backend WP seam fixtures; no canonical/effect ownership. */
export const worldFocusDerivedWorkFixtureAdapter: WorldFocusDerivedWorkReadAdapter =
  Object.freeze({
    readAttention: async ({ worldId, signal }) => {
      await settle(signal);
      if (!musicOnly(worldId)) return empty(worldId);
      return Object.freeze({
        status: 'ready' as const,
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId,
          orderedItems: Object.freeze([
            createWorldFocusAttentionPrimitive({
              instanceId: 'music-artwork-attention',
              matterReference: ref('dependency', 'neon-static-artwork-approval'),
              reasonCode: 'release-blocked',
              resolutionReference: ref('request', 'artwork-review-request'),
              state: 'awaiting-response',
            }),
          ]),
        }),
      });
    },
    readComparison: async ({ worldId, signal }) => {
      await settle(signal);
      if (!musicOnly(worldId)) return empty(worldId);
      return Object.freeze({
        status: 'ready' as const,
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId,
          orderedItems: Object.freeze([
            createWorldFocusComparisonPrimitive(
              {
                instanceId: 'music-master-change',
                mode: 'change',
                subjectReferences: [
                  ref('material-state', 'neon-static-master-v2'),
                  ref('material-state', 'neon-static-master-v3'),
                ],
                basisReference: ref('comparison-basis', 'master-review'),
              },
              { maxSubjectReferences: 4 },
            ),
          ]),
        }),
      });
    },
    readTrajectory: async ({ worldId, signal }) => {
      await settle(signal);
      if (!musicOnly(worldId)) return empty(worldId);
      return Object.freeze({
        status: 'ready' as const,
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId,
          orderedItems: Object.freeze([
            createWorldFocusTrajectoryPrimitive(
              {
                instanceId: 'music-release-observation-trajectory',
                subjectReference: ref('release', 'neon-static'),
                axis: 'time',
                orderedPointReferences: [
                  ref('observation', 'release-day-minus-1'),
                  ref('observation', 'release-day'),
                ],
                missingPositionReferences: [],
                orderingBasisReference: ref('window', 'release-window'),
                aggregationBasisReference: null,
              },
              {
                maxOrderedPointReferences: 8,
                maxMissingPositionReferences: 8,
              },
            ),
          ]),
        }),
      });
    },
  });
