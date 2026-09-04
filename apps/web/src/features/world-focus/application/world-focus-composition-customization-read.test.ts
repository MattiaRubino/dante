import { describe, expect, it } from 'vitest';

import type { WorldFocusId } from '../model/world-focus-identity';
import type { WorldFocusScopedReader } from './world-focus-foundation';
import {
  createWorldFocusCompositionCustomizationReader,
  readWorldFocusCompositionCustomizationOpportunities,
} from './world-focus-composition-customization-read';

type EmptyResult = Readonly<{
  status: 'empty';
  worldId: WorldFocusId;
}>;

function emptyResult(worldId: WorldFocusId): EmptyResult {
  return Object.freeze({ status: 'empty' as const, worldId });
}

describe('World Focus composition customization read', () => {
  it('aggregates the seven existing M1 readers through one bounded opportunity seam', async () => {
    const calls: Array<Readonly<{ worldId: WorldFocusId; signal: AbortSignal }>> = [];
    const readEmpty: WorldFocusScopedReader<EmptyResult> = (
      worldId,
      signal,
    ) => {
      if (signal === undefined) {
        throw new Error('Expected bounded customization AbortSignal');
      }
      calls.push({ worldId, signal });
      return Promise.resolve(emptyResult(worldId));
    };
    const read = createWorldFocusCompositionCustomizationReader({
      readSituation: readEmpty,
      readContinuity: readEmpty,
      readAttention: readEmpty,
      readNext: readEmpty,
      readComparison: readEmpty,
      readTrajectory: readEmpty,
      readEvidenceHistory: readEmpty,
    });

    const result = await read('music');

    expect(result).toEqual({ worldId: 'music', opportunities: [] });
    expect(calls).toHaveLength(7);
    expect(calls.every((call) => call.worldId === 'music')).toBe(true);
    expect(calls.every((call) => call.signal === calls[0]?.signal)).toBe(true);
  });

  it('returns only bounded composition metadata from the real pre-backend readers', async () => {
    const result = await readWorldFocusCompositionCustomizationOpportunities('music');

    expect(result.worldId).toBe('music');
    expect(result.opportunities.length).toBeGreaterThan(0);
    for (const opportunity of result.opportunities) {
      expect(Object.keys(opportunity).sort()).toEqual([
        'defaultProminence',
        'footprint',
        'instanceId',
        'kind',
      ]);
      expect(opportunity).not.toHaveProperty('reasonCode');
      expect(opportunity).not.toHaveProperty('reference');
      expect(opportunity).not.toHaveProperty('payload');
      expect(opportunity).not.toHaveProperty('authorization');
    }
  });

  it('propagates cancellation to every owned read and never converts abort into an empty result', async () => {
    const internalSignals: AbortSignal[] = [];
    const pending: WorldFocusScopedReader<EmptyResult> = (worldId, signal) =>
      new Promise((resolve, reject) => {
        if (signal === undefined) {
          reject(new Error('Expected bounded customization AbortSignal'));
          return;
        }
        internalSignals.push(signal);
        if (signal.aborted) {
          const error = new Error('aborted');
          error.name = 'AbortError';
          reject(error);
          return;
        }
        signal.addEventListener(
          'abort',
          () => {
            const error = new Error('aborted');
            error.name = 'AbortError';
            reject(error);
          },
          { once: true },
        );
        void resolve;
        void worldId;
      });
    const read = createWorldFocusCompositionCustomizationReader({
      readSituation: pending,
      readContinuity: pending,
      readAttention: pending,
      readNext: pending,
      readComparison: pending,
      readTrajectory: pending,
      readEvidenceHistory: pending,
    });
    const outer = new AbortController();

    const result = read('music', outer.signal);
    outer.abort();

    await expect(result).rejects.toMatchObject({ name: 'AbortError' });
    expect(internalSignals).toHaveLength(7);
    expect(internalSignals.every((signal) => signal.aborted)).toBe(true);
  });
});
