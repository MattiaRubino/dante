import type { WorldFocusContinuityReadResult } from '../model/world-focus-continuity';
import type { WorldFocusCompositionConfig } from '../model/world-focus-composition-config';
import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionPlan,
  type WorldFocusCompositionPolicy,
} from '../model/world-focus-composition-plan';
import type { WorldFocusId } from '../model/world-focus-identity';
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
import type { WorldFocusContinuityReader } from './world-focus-continuity';
import { readWorldFocusContinuity } from './world-focus-continuity-runtime';
import {
  collectWorldFocusCompositionOpportunities,
  type WorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';
import {
  resolveWorldFocusCompositionCandidates,
  type WorldFocusCompositionCandidateResolution,
} from './world-focus-composition-resolver';
import type { WorldFocusScopedReader } from './world-focus-foundation';

export type WorldFocusAdaptiveCompositionReaders = Readonly<{
  readSituation: WorldFocusScopedReader<WorldFocusSituationReadResult>;
  readContinuity: WorldFocusContinuityReader;
  readAttention: WorldFocusScopedReader<WorldFocusAttentionReadResult>;
  readNext: WorldFocusScopedReader<WorldFocusNextReadResult>;
  readComparison: WorldFocusScopedReader<WorldFocusComparisonReadResult>;
  readTrajectory: WorldFocusScopedReader<WorldFocusTrajectoryReadResult>;
  readEvidenceHistory: WorldFocusScopedReader<WorldFocusEvidenceHistoryReadResult>;
}>;

export type WorldFocusAdaptiveCompositionSnapshot = Readonly<{
  worldId: WorldFocusId;
  situation: WorldFocusSituationReadResult;
  continuity: WorldFocusContinuityReadResult;
  attention: WorldFocusAttentionReadResult;
  next: WorldFocusNextReadResult;
  comparison: WorldFocusComparisonReadResult;
  trajectory: WorldFocusTrajectoryReadResult;
  evidenceHistory: WorldFocusEvidenceHistoryReadResult;
  opportunitySet: WorldFocusCompositionOpportunitySet;
}>;

export type WorldFocusAdaptiveCompositionReader = (
  worldId: WorldFocusId,
  signal?: AbortSignal,
) => Promise<WorldFocusAdaptiveCompositionSnapshot>;

export type WorldFocusAdaptiveCompositionResolution = Readonly<{
  candidateResolution: WorldFocusCompositionCandidateResolution;
  plan: WorldFocusCompositionPlan;
}>;

export const WORLD_FOCUS_ADAPTIVE_COMPOSITION_POLICY: WorldFocusCompositionPolicy =
  Object.freeze({
    maxAdaptiveEntries: 4,
    maxEphemeralEntries: 2,
  });

function createAbortError(): Error {
  const error = new Error('World Focus adaptive composition read aborted');
  error.name = 'AbortError';
  return error;
}

/**
 * Reads each already-owned M1 seam exactly once and retains one immutable
 * snapshot for both composition planning and rendering. No canonical Domain
 * truth, AuthZ decision, persistence state or renderer function enters config.
 */
export function createWorldFocusAdaptiveCompositionReader(
  readers: WorldFocusAdaptiveCompositionReaders,
): WorldFocusAdaptiveCompositionReader {
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

      if (controller.signal.aborted) {
        throw createAbortError();
      }

      const opportunitySet = collectWorldFocusCompositionOpportunities({
        worldId,
        situation,
        continuity,
        attention,
        next,
        comparison,
        trajectory,
        evidenceHistory,
      });

      return Object.freeze({
        worldId,
        situation,
        continuity,
        attention,
        next,
        comparison,
        trajectory,
        evidenceHistory,
        opportunitySet,
      });
    } catch (error) {
      controller.abort();
      throw error;
    } finally {
      signal?.removeEventListener('abort', abort);
    }
  };
}

export const readWorldFocusAdaptiveCompositionSnapshot =
  createWorldFocusAdaptiveCompositionReader({
    readSituation: readWorldFocusSituation,
    readContinuity: readWorldFocusContinuity,
    readAttention: readWorldFocusAttention,
    readNext: readWorldFocusNext,
    readComparison: readWorldFocusComparison,
    readTrajectory: readWorldFocusTrajectory,
    readEvidenceHistory: readWorldFocusEvidenceHistory,
  });

/**
 * M3-4 integration only. Value signals stay empty until a later explicitly
 * authorized owner supplies them; this function does not anticipate M4/DANTE.
 */
export function resolveWorldFocusAdaptiveComposition(
  snapshot: WorldFocusAdaptiveCompositionSnapshot,
  config: WorldFocusCompositionConfig,
): WorldFocusAdaptiveCompositionResolution {
  if (snapshot.worldId !== config.worldId) {
    throw new Error('World Focus adaptive composition config belongs to another World');
  }

  const candidateResolution = resolveWorldFocusCompositionCandidates({
    opportunitySet: snapshot.opportunitySet,
    config,
    valueSignals: [],
  });
  const plan = resolveWorldFocusCompositionPlan(
    candidateResolution.candidates,
    WORLD_FOCUS_ADAPTIVE_COMPOSITION_POLICY,
  );

  return Object.freeze({ candidateResolution, plan });
}
