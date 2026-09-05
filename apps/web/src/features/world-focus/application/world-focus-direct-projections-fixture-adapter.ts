import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
} from '../model/world-focus-direct-projections';
import { createWorldFocusEvidenceReferenceFacet } from '../model/world-focus-evidence';
import { normalizeWorldFocusFixtureId } from '../model/world-focus-fixtures';
import type { WorldFocusId } from '../model/world-focus-identity';
import type { WorldFocusDirectProjectionReadAdapter } from './world-focus-direct-projections';

const ref = (kind: string, key: string) => Object.freeze({ kind, key });

function createAbortError() {
  const error = new Error('World Focus direct projection read aborted');
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

/** Deterministic pre-backend fixture binding; never an authority or Domain DTO. */
export const worldFocusDirectProjectionFixtureAdapter: WorldFocusDirectProjectionReadAdapter =
  Object.freeze({
    readSituation: async ({ worldId, signal }) => {
      await settle(signal);
      const fixtureId = normalizeWorldFocusFixtureId(worldId);
      if (fixtureId === 'travel') {
        return Object.freeze({
          status: 'ready' as const,
          projection: createWorldFocusSituationProjection({
            worldId,
            orderedSituationReferences: [
              ref('plan', 'japan-2027'),
              ref('checkpoint', 'japan-flight-shortlist'),
            ],
          }),
        });
      }
      if (fixtureId !== 'music') return empty(worldId);
      return Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusSituationProjection({
          worldId,
          orderedSituationReferences: [
            ref('release', 'neon-static'),
            ref('material-state', 'neon-static-master-v3'),
          ],
        }),
      });
    },
    readNext: async ({ worldId, signal }) => {
      await settle(signal);
      const fixtureId = normalizeWorldFocusFixtureId(worldId);
      if (fixtureId === 'travel') {
        return Object.freeze({
          status: 'ready' as const,
          projection: createWorldFocusNextProjection({
            worldId,
            orderedNextReferences: [
              ref('continuation-intent', 'japan-flight-review'),
            ],
          }),
        });
      }
      if (fixtureId !== 'music') return empty(worldId);
      return Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusNextProjection({
          worldId,
          orderedNextReferences: [
            ref('schedule', 'neon-static-release'),
            ref('dependency', 'neon-static-artwork-approval'),
          ],
        }),
      });
    },
    readEvidenceHistory: async ({ worldId, signal }) => {
      await settle(signal);
      const fixtureId = normalizeWorldFocusFixtureId(worldId);
      if (fixtureId === 'travel') {
        const evidence = createWorldFocusEvidenceReferenceFacet(
          {
            evidenceReferences: [
              ref('observation', 'japan-flight-price-check'),
            ],
            provenanceReferences: [
              ref('provenance', 'japan-flight-search-import'),
            ],
            integrityAttestationReferences: [],
          },
          {
            maxEvidenceReferences: 4,
            maxProvenanceReferences: 4,
            maxIntegrityAttestationReferences: 4,
          },
        );
        return Object.freeze({
          status: 'ready' as const,
          projection: createWorldFocusEvidenceHistoryProjection({
            worldId,
            evidence,
            orderedHistoryReferences: [
              ref('checkpoint', 'japan-flight-shortlist'),
            ],
          }),
        });
      }
      if (fixtureId !== 'music') return empty(worldId);
      const evidence = createWorldFocusEvidenceReferenceFacet(
        {
          evidenceReferences: [ref('observation', 'neon-static-mix-review')],
          provenanceReferences: [
            ref('provenance', 'neon-static-studio-import'),
          ],
          integrityAttestationReferences: [],
        },
        {
          maxEvidenceReferences: 4,
          maxProvenanceReferences: 4,
          maxIntegrityAttestationReferences: 4,
        },
      );
      return Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusEvidenceHistoryProjection({
          worldId,
          evidence,
          orderedHistoryReferences: [
            ref('material-state', 'neon-static-master-v2'),
          ],
        }),
      });
    },
  });
