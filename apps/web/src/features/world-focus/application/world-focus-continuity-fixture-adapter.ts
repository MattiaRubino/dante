import type { WorldFocusContinuityReadAdapter } from './world-focus-continuity';
import type { WorldFocusContinuityItem } from '../model/world-focus-continuity';
import {
  normalizeWorldFocusFixtureId,
  type WorldFocusFixtureId,
} from '../model/world-focus-fixtures';

const CONTINUITY_FIXTURES: Partial<
  Readonly<Record<WorldFocusFixtureId, readonly WorldFocusContinuityItem[]>>
> = {
  music: [
    {
      key: 'music-neon-static',
      title: 'Neon Static',
      context: 'Release',
      checkpoint: 'Master v3',
      threadReference: { kind: 'release', key: 'neon-static' },
      checkpointReference: { kind: 'material-state', key: 'neon-static-master-v3' },
      continuationReference: { kind: 'continuation-intent', key: 'neon-static-release' },
      presentationState: 'active',
    },
    {
      key: 'music-glass-signal',
      title: 'Glass Signal',
      context: 'Song',
      checkpoint: 'Arrangement draft',
      threadReference: { kind: 'song', key: 'glass-signal' },
      checkpointReference: { kind: 'material-state', key: 'glass-signal-arrangement-draft' },
      continuationReference: null,
      presentationState: 'paused',
    },
  ],
  travel: [
    {
      key: 'travel-japan-2027',
      title: 'Japan 2027',
      context: 'Planning',
      checkpoint: 'Flight shortlist',
      threadReference: { kind: 'plan', key: 'japan-2027' },
      checkpointReference: { kind: 'checkpoint', key: 'japan-flight-shortlist' },
      continuationReference: { kind: 'continuation-intent', key: 'japan-flight-review' },
      presentationState: 'active',
    },
  ],
  study: [
    {
      key: 'study-english-b2',
      title: 'English B2',
      context: 'Course',
      checkpoint: 'Unit 4',
      threadReference: { kind: 'course', key: 'english-b2' },
      checkpointReference: { kind: 'checkpoint', key: 'english-b2-unit-4' },
      continuationReference: { kind: 'continuation-intent', key: 'english-b2-next-unit' },
      presentationState: 'active',
    },
  ],
  work: [
    {
      key: 'work-launch-brief',
      title: 'Launch brief',
      context: 'Workstream',
      checkpoint: 'Review notes',
      threadReference: { kind: 'workstream', key: 'launch-brief' },
      checkpointReference: { kind: 'checkpoint', key: 'launch-brief-review-notes' },
      continuationReference: null,
      presentationState: 'active',
    },
  ],
  projects: [
    {
      key: 'projects-portfolio-redesign',
      title: 'Portfolio redesign',
      context: 'Project',
      checkpoint: 'Wireframe pass',
      threadReference: { kind: 'project', key: 'portfolio-redesign' },
      checkpointReference: { kind: 'checkpoint', key: 'portfolio-wireframe-pass' },
      continuationReference: { kind: 'continuation-intent', key: 'portfolio-next-pass' },
      presentationState: 'active',
    },
    {
      key: 'projects-home-archive',
      title: 'Home archive',
      context: 'Project',
      checkpoint: 'Source cleanup',
      threadReference: { kind: 'project', key: 'home-archive' },
      checkpointReference: { kind: 'checkpoint', key: 'home-archive-source-cleanup' },
      continuationReference: null,
      presentationState: 'blocked',
    },
  ],
};

function createAbortError() {
  const error = new Error('World Focus continuity read aborted');
  error.name = 'AbortError';
  return error;
}

/** Deterministic pre-backend product adapter; fixture identity stays local here. */
export const worldFocusContinuityFixtureAdapter: WorldFocusContinuityReadAdapter =
  Object.freeze({
    read: async ({ worldId, signal }) => {
      await Promise.resolve();
      if (signal.aborted) throw createAbortError();

      const fixtureId = normalizeWorldFocusFixtureId(worldId);
      const orderedItems = fixtureId === undefined ? undefined : CONTINUITY_FIXTURES[fixtureId];
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
