import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalHardDeletion } from './remote-temporal-hard-deletion';
import { createRemoteTemporalTimelineDataSource } from './remote-timeline-read';
import { holdTemporalOccurrenceInventoryReview } from './temporal-occurrence-inventory-fence';

const ACTIVITY = '0199a222-2222-7222-8222-222222222222';
const PREVIEW = {
  requestedRef: ACTIVITY,
  scope: 'activity_series' as const,
  fingerprint: 'a'.repeat(64),
};
const WINDOW = {
  operationId: 'hard-delete:checkpoint',
  startDate: '2026-11-09',
  endDateExclusive: '2026-12-01',
};
const CHECKPOINT = {
  start_date: WINDOW.startDate,
  end_date_exclusive: WINDOW.endDateExclusive,
  effective_zone_id: 'Europe/Rome',
  source_count: 1,
  occurrence_count: 37,
  replayed_source_count: 0,
};
const DELETED = {
  requested_ref: ACTIVITY,
  scope: 'activity_series',
  deleted_rows: 95,
};

function heldResponse() {
  let complete!: (response: Response) => void;
  const promise = new Promise<Response>((resolve) => {
    complete = resolve;
  });
  return { promise, complete };
}

function requestUrl(input: RequestInfo | URL): string {
  if (typeof input === 'string') return input;
  if (input instanceof URL) return input.href;
  return input.url;
}

function testFetch(
  calls: string[],
  checkpoint: () => Promise<Response>,
  deletion: () => Promise<Response>,
) {
  return vi.fn<typeof globalThis.fetch>((input, init) => {
    const url = requestUrl(input);
    if (url.endsWith('/auth/session')) {
      return Promise.resolve(
        Response.json({ authenticated: true, csrf_token: 'csrf-test' }),
      );
    }
    if (url.endsWith('/occurrences/checkpoint')) {
      calls.push('checkpoint');
      return checkpoint();
    }
    if (url.endsWith('/hard-deletion/' + ACTIVITY)) {
      expect(init?.method).toBe('DELETE');
      expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-test');
      calls.push('delete');
      return deletion();
    }
    throw new Error('Unexpected request: ' + url);
  });
}

describe('atomic recurring hard deletion versus Timeline checkpoint', () => {
  it('waits for a checkpoint before series deletion', async () => {
    const pending = heldResponse();
    const calls: string[] = [];
    const fetchFn = testFetch(
      calls,
      () => pending.promise,
      () => Promise.resolve(Response.json(DELETED)),
    );
    const timeline = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );
    const deletion = createRemoteTemporalHardDeletion(fetchFn);
    if (!timeline.checkpointWindow) {
      throw new Error('Checkpoint capability missing.');
    }

    const checkpoint = timeline.checkpointWindow(WINDOW);
    await vi.waitFor(() => expect(calls).toEqual(['checkpoint']));
    const deleted = deletion.deleteConfirmed(PREVIEW);
    await Promise.resolve();
    expect(calls).toEqual(['checkpoint']);

    pending.complete(Response.json(CHECKPOINT));
    await expect(checkpoint).resolves.toMatchObject({ occurrenceCount: 37 });
    await expect(deleted).resolves.toBeUndefined();
    expect(calls).toEqual(['checkpoint', 'delete']);
  });

  it('holds later checkpoints until deletion commits', async () => {
    const pending = heldResponse();
    const calls: string[] = [];
    const fetchFn = testFetch(
      calls,
      () => Promise.resolve(Response.json(CHECKPOINT)),
      () => pending.promise,
    );
    const timeline = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );
    const deletion = createRemoteTemporalHardDeletion(fetchFn);
    if (!timeline.checkpointWindow) {
      throw new Error('Checkpoint capability missing.');
    }

    const deleted = deletion.deleteConfirmed(PREVIEW);
    await vi.waitFor(() => expect(calls).toEqual(['delete']));
    const checkpoint = timeline.checkpointWindow(WINDOW);
    await Promise.resolve();
    expect(calls).toEqual(['delete']);

    pending.complete(Response.json(DELETED));
    await expect(deleted).resolves.toBeUndefined();
    await expect(checkpoint).resolves.toMatchObject({ occurrenceCount: 37 });
    expect(calls).toEqual(['delete', 'checkpoint']);
  });

  it('preserves 409 and releases the checkpoint queue', async () => {
    const calls: string[] = [];
    const fetchFn = testFetch(
      calls,
      () => Promise.resolve(Response.json(CHECKPOINT)),
      () =>
        Promise.resolve(
          Response.json({ detail: 'Stale graph' }, { status: 409 }),
        ),
    );
    const timeline = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );
    const deletion = createRemoteTemporalHardDeletion(fetchFn);
    if (!timeline.checkpointWindow) {
      throw new Error('Checkpoint capability missing.');
    }

    await expect(deletion.deleteConfirmed(PREVIEW)).rejects.toThrow(
      'La serie o le sue istanze sono cambiate.',
    );
    await expect(timeline.checkpointWindow(WINDOW)).resolves.toMatchObject({
      occurrenceCount: 37,
    });
    expect(calls).toEqual(['delete', 'checkpoint']);
  });
  it('keeps a confirmed whole-series delete consistent across human review', async () => {
    const waitingDelete = heldResponse();
    const calls: string[] = [];
    const fetchFn = testFetch(
      calls,
      () => Promise.resolve(Response.json(CHECKPOINT)),
      () => waitingDelete.promise,
    );
    const timeline = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );
    const deletion = createRemoteTemporalHardDeletion(fetchFn);
    if (!timeline.checkpointWindow) {
      throw new Error('Checkpoint capability missing.');
    }
    // Model the actual Activity/Event inspector: capture every preview
    // fingerprint under the same lease used by the confirmation.
    const { lease } = await holdTemporalOccurrenceInventoryReview(
      () => Promise.resolve(PREVIEW),
    );
    try {
      const checkpoint = timeline.checkpointWindow(WINDOW);
      await Promise.resolve();
      expect(calls).toEqual([]);
      const deleted = deletion.deleteConfirmed(PREVIEW, lease);
      await vi.waitFor(() => expect(calls).toEqual(['delete']));
      waitingDelete.complete(Response.json(DELETED));
      await expect(deleted).resolves.toBeUndefined();
      expect(calls).toEqual(['delete']);
      lease.release();
      await expect(checkpoint).resolves.toMatchObject({ occurrenceCount: 37 });
      expect(calls).toEqual(['delete', 'checkpoint']);
    } finally {
      waitingDelete.complete(Response.json(DELETED));
      lease.release();
    }
  });

});
