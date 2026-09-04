import type { WorldFocusContinuityReader } from './world-focus-continuity';
import { readWorldFocusContinuity } from './world-focus-continuity-runtime';
import {
  collectWorldFocusCompositionOpportunities,
  type WorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';
import type {
  WorldFocusAttentionReadResult,
  WorldFocusComparisonReadResult,
  WorldFocusTrajectoryReadResult,
} from './world-focus-derived-work';
import {
  readWorldFocusAttention,
  readWorldFocusComparison,
  readWorldFocusTrajectory,
} from './world-focus-derived-work-runtime';
import type {
  WorldFocusEvidenceHistoryReadResult,
  WorldFocusNextReadResult,
  WorldFocusSituationReadResult,
} from './world-focus-direct-projections';
import {
  readWorldFocusEvidenceHistory,
  readWorldFocusNext,
  readWorldFocusSituation,
} from './world-focus-direct-projections-runtime';
import type { WorldFocusScopedReader } from './world-focus-foundation';
import type { WorldFocusId } from '../model/world-focus-identity';

export type WorldFocusCompositionCustomizationReaders = Readonly<{
  readSituation: WorldFocusScopedReader<WorldFocusSituationReadResult>;
  readContinuity: WorldFocusContinuityReader;
  readAttention: WorldFocusScopedReader<WorldFocusAttentionReadResult>;
  readNext: WorldFocusScopedReader<WorldFocusNextReadResult>;
  readComparison: WorldFocusScopedReader<WorldFocusComparisonReadResult>;
  readTrajectory: WorldFocusScopedReader<WorldFocusTrajectoryReadResult>;
  readEvidenceHistory: WorldFocusScopedReader<WorldFocusEvidenceHistoryReadResult>;
}>;

export type WorldFocusCompositionCustomizationReader = (
  worldId: WorldFocusId,
  signal?: AbortSignal,
) => Promise<WorldFocusCompositionOpportunitySet>;

function createAbortError(): Error {
  const error = new Error('World Focus composition customization read aborted');
  error.name = 'AbortError';
  return error;
}

/**
 * Reads the already-owned M1 projection seams and reduces them immediately to
 * M3 composition opportunity metadata. References, payloads, reason codes and
 * disclosure/authorization state never enter the returned value.
 */
export function createWorldFocusCompositionCustomizationReader(
  readers: WorldFocusCompositionCustomizationReaders,
): WorldFocusCompositionCustomizationReader {
  return async (worldId, signal) => {
    if (signal?.aborted === true) {
      throw createAbortError();
    }

    const controller = new AbortController();
    const abort = () => controller.abort();
    signal?.addEventListener('abort', abort, { once: true });

    try {
      const [
        situation,
        continuity,
        attention,
        next,
        comparison,
        trajectory,
        evidenceHistory,
      ] = await Promise.all([
        readers.readSituation(worldId, controller.signal),
        readers.readContinuity(worldId, controller.signal),
        readers.readAttention(worldId, controller.signal),
        readers.readNext(worldId, controller.signal),
        readers.readComparison(worldId, controller.signal),
        readers.readTrajectory(worldId, controller.signal),
        readers.readEvidenceHistory(worldId, controller.signal),
      ]);

      if (signal?.aborted === true) {
        throw createAbortError();
      }

      return collectWorldFocusCompositionOpportunities({
        worldId,
        situation,
        continuity,
        attention,
        next,
        comparison,
        trajectory,
        evidenceHistory,
      });
    } catch (error) {
      controller.abort();
      throw error;
    } finally {
      signal?.removeEventListener('abort', abort);
    }
  };
}

export const readWorldFocusCompositionCustomizationOpportunities =
  createWorldFocusCompositionCustomizationReader({
    readSituation: readWorldFocusSituation,
    readContinuity: readWorldFocusContinuity,
    readAttention: readWorldFocusAttention,
    readNext: readWorldFocusNext,
    readComparison: readWorldFocusComparison,
    readTrajectory: readWorldFocusTrajectory,
    readEvidenceHistory: readWorldFocusEvidenceHistory,
  });
