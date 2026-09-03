import { describe, expect, it } from 'vitest';

import {
  createWorldFocusDirectProjectionReaders,
  type WorldFocusDirectProjectionReadAdapter,
} from './world-focus-direct-projections';
import {
  readWorldFocusEvidenceHistory,
  readWorldFocusNext,
  readWorldFocusSituation,
} from './world-focus-direct-projections-runtime';
import { WorldFocusBoundaryValidationError } from './world-focus-foundation';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus M1-2 direct projection application seams', () => {
  it('rejects a result bound to another World instead of attaching it locally', async () => {
    const adapter: WorldFocusDirectProjectionReadAdapter = {
      readSituation: () =>
        Promise.resolve({
          status: 'ready',
          projection: {
            schemaVersion: 1,
            worldId: 'travel',
            orderedSituationReferences: [ref('observation', 'trip-state')],
          },
        }),
      readNext: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
      readEvidenceHistory: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
    };
    const readers = createWorldFocusDirectProjectionReaders(adapter);

    await expect(readers.readSituation('music')).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('keeps an unknown future World valid and truthfully empty without fixture-catalog expansion', async () => {
    await expect(readWorldFocusSituation('apiary')).resolves.toEqual({ status: 'empty', worldId: 'apiary' });
    await expect(readWorldFocusNext('apiary')).resolves.toEqual({ status: 'empty', worldId: 'apiary' });
    await expect(readWorldFocusEvidenceHistory('apiary')).resolves.toEqual({ status: 'empty', worldId: 'apiary' });
  });

  it('provides a useful deterministic basic path without DANTE', async () => {
    const [situation, next, evidenceHistory] = await Promise.all([
      readWorldFocusSituation('music'),
      readWorldFocusNext('music'),
      readWorldFocusEvidenceHistory('music'),
    ]);

    expect(situation.status).toBe('ready');
    expect(next.status).toBe('ready');
    expect(evidenceHistory.status).toBe('ready');
  });

  it('propagates cancellation through the shared World-scoped read boundary', () => {
    let observedSignal: AbortSignal | null = null;
    const adapter: WorldFocusDirectProjectionReadAdapter = {
      readSituation: ({ signal }) => {
        observedSignal = signal;
        return new Promise(() => undefined);
      },
      readNext: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
      readEvidenceHistory: () => Promise.resolve({ status: 'empty', worldId: 'music' }),
    };
    const readers = createWorldFocusDirectProjectionReaders(adapter);
    const upstream = new AbortController();
    void readers.readSituation('music', upstream.signal);

    upstream.abort();

    expect(observedSignal?.aborted).toBe(true);
  });
});
