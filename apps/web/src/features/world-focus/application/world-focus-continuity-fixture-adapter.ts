import type { WorldFocusContinuityReadAdapter } from './world-focus-continuity';
import type { WorldFocusContinuityItem } from '../model/world-focus-continuity';
import type { WorldFocusId } from '../model/world-focus-fixtures';

const CONTINUITY_FIXTURES: Partial<
  Readonly<Record<WorldFocusId, readonly WorldFocusContinuityItem[]>>
> = {
  music: [
    {
      key: 'music-neon-static',
      title: 'Neon Static',
      context: 'Release',
      checkpoint: 'Master v3',
      presentationState: 'active',
    },
    {
      key: 'music-glass-signal',
      title: 'Glass Signal',
      context: 'Song',
      checkpoint: 'Arrangement draft',
      presentationState: 'paused',
    },
  ],
  travel: [
    {
      key: 'travel-japan-2027',
      title: 'Japan 2027',
      context: 'Planning',
      checkpoint: 'Flight shortlist',
      presentationState: 'active',
    },
  ],
  study: [
    {
      key: 'study-english-b2',
      title: 'English B2',
      context: 'Course',
      checkpoint: 'Unit 4',
      presentationState: 'active',
    },
  ],
  work: [
    {
      key: 'work-launch-brief',
      title: 'Launch brief',
      context: 'Workstream',
      checkpoint: 'Review notes',
      presentationState: 'active',
    },
  ],
  projects: [
    {
      key: 'projects-portfolio-redesign',
      title: 'Portfolio redesign',
      context: 'Project',
      checkpoint: 'Wireframe pass',
      presentationState: 'active',
    },
    {
      key: 'projects-home-archive',
      title: 'Home archive',
      context: 'Project',
      checkpoint: 'Source cleanup',
      presentationState: 'blocked',
    },
  ],
};

function createAbortError() {
  const error = new Error('World Focus continuity read aborted');
  error.name = 'AbortError';
  return error;
}

/**
 * Deterministic pre-backend product adapter. The scenario data validates the
 * frontend contract and cross-World sparsity rules; it is not a backend DTO,
 * Domain owner model, database row set, or authorization source.
 */
export const worldFocusContinuityFixtureAdapter: WorldFocusContinuityReadAdapter =
  Object.freeze({
    read: async ({ worldId, signal }) => {
      await Promise.resolve();
      if (signal.aborted) {
        throw createAbortError();
      }

      const orderedItems = CONTINUITY_FIXTURES[worldId];
      if (orderedItems === undefined || orderedItems.length === 0) {
        return Object.freeze({ status: 'empty' as const, worldId });
      }

      return Object.freeze({
        status: 'ready' as const,
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId,
          orderedItems,
        }),
      });
    },
  });
