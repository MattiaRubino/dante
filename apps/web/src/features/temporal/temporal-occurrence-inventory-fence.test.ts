import { describe, expect, it, vi } from 'vitest';

import { createRemoteRecurringSeriesEdit } from './remote-recurring-series-edit';
import { createRemoteTemporalTimelineDataSource } from './remote-timeline-read';
import { withTemporalOccurrenceInventoryFence } from './temporal-occurrence-inventory-fence';

const SOURCE = '0199a111-1111-7111-8111-111111111111';
const SELECTED = '0199a222-2222-7222-8222-222222222222';
const STATE = '0199a333-3333-7333-8333-333333333333';
const WINDOW = {
  startDate: '2026-11-09',
  endDateExclusive: '2026-12-01',
  operationId: 'inventory-fence:window',
};
const INTENT = {
  selectedRef: SELECTED,
  source: {
    sourceRef: SOURCE,
    owner: 'routine' as const,
    selectedDate: '2026-11-16',
    editRevision: 1,
    recurrenceStateRef: STATE,
    title: 'Serie in modifica',
    description: null,
    location: null,
    colorCode: null,
    recurrence: { pattern_code: 'weekly_weekdays' },
    structure: { activity_template: {} },
  },
  scope: 'this_and_following' as const,
  recurrence: { pattern_code: 'weekly_weekdays' },
  structure: { activity_template: {} },
  profilePatch: { title: 'Titolo aggiornato' },
  operationId: 'inventory-fence:series',
};
const PREVIEW = {
  source_native_ref: SOURCE,
  owner_kind: 'routine',
  selected_occurrence_ref: SELECTED,
  fingerprint: 'a'.repeat(64),
  target_occurrence_refs: [SELECTED],
  new_expected_count: 1,
  protected_occurrences: [],
};
const CHECKPOINT = {
  start_date: WINDOW.startDate,
  end_date_exclusive: WINDOW.endDateExclusive,
  effective_zone_id: 'Europe/Rome',
  source_count: 1,
  occurrence_count: 36,
  replayed_source_count: 0,
};

function heldResponse() {
  let complete!: (response: Response) => void;
  const promise = new Promise<Response>((resolve) => {
    complete = resolve;
  });
  return { promise, complete };
}

async function flushMicrotasks(): Promise<void> {
  for (let i = 0; i < 8; i += 1) {
    await Promise.resolve();
  }
}

describe('recurring review and Timeline checkpoint admission', () => {
  it('waits for a running checkpoint before requesting a series preview', async () => {
    const checkpointResponse = heldResponse();
    const calls: string[] = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf-test' });
      }
      if (url.endsWith('/occurrences/checkpoint')) {
        calls.push('checkpoint');
        return checkpointResponse.promise;
      }
      if (url.endsWith('/series-edit-preview')) {
        calls.push('preview');
        return Response.json(PREVIEW);
      }
      throw new Error('Unexpected request: ' + url);
    });
    const timeline = createRemoteTemporalTimelineDataSource(fetchFn, () => 'Europe/Rome');
    const series = createRemoteRecurringSeriesEdit(fetchFn);
    if (!timeline.checkpointWindow) throw new Error('Checkpoint capability missing.');

    const checkpoint = timeline.checkpointWindow(WINDOW);
    await vi.waitFor(() => expect(calls).toContain('checkpoint'));
    const preview = series.preview(INTENT);
    await flushMicrotasks();
    expect(calls).toEqual(['checkpoint']);

    checkpointResponse.complete(Response.json(CHECKPOINT));
    await expect(checkpoint).resolves.toMatchObject({ occurrenceCount: 36 });
    await expect(preview).resolves.toMatchObject({ fingerprint: PREVIEW.fingerprint });
    expect(calls).toEqual(['checkpoint', 'preview']);
  });

  it('does not start a new checkpoint during an active series preview', async () => {
    const previewResponse = heldResponse();
    const calls: string[] = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf-test' });
      }
      if (url.endsWith('/series-edit-preview')) {
        calls.push('preview');
        return previewResponse.promise;
      }
      if (url.endsWith('/occurrences/checkpoint')) {
        calls.push('checkpoint');
        return Response.json(CHECKPOINT);
      }
      throw new Error('Unexpected request: ' + url);
    });
    const timeline = createRemoteTemporalTimelineDataSource(fetchFn, () => 'Europe/Rome');
    const series = createRemoteRecurringSeriesEdit(fetchFn);
    if (!timeline.checkpointWindow) throw new Error('Checkpoint capability missing.');

    const preview = series.preview(INTENT);
    await vi.waitFor(() => expect(calls).toContain('preview'));
    const checkpoint = timeline.checkpointWindow(WINDOW);
    await flushMicrotasks();
    expect(calls).toEqual(['preview']);

    previewResponse.complete(Response.json(PREVIEW));
    await expect(preview).resolves.toMatchObject({ fingerprint: PREVIEW.fingerprint });
    await expect(checkpoint).resolves.toMatchObject({ occurrenceCount: 36 });
    expect(calls).toEqual(['preview', 'checkpoint']);
  });

  it('releases subsequent operations after a failed checkpoint', async () => {
    await expect(
      withTemporalOccurrenceInventoryFence(() =>
        Promise.reject(new Error('checkpoint rejected')),
      ),
    ).rejects.toThrow('checkpoint rejected');
    await expect(
      withTemporalOccurrenceInventoryFence(() => Promise.resolve('preview permitted')),
    ).resolves.toBe('preview permitted');
  });

  it('preserves server 409 rejection, with no silent re-preview or retry', async () => {
    const checkpointResponse = heldResponse();
    const calls: string[] = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input) => {
      const url = String(input);
      if (url.endsWith('/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf-test' });
      }
      if (url.endsWith('/occurrences/checkpoint')) {
        calls.push('checkpoint');
        return checkpointResponse.promise;
      }
      if (url.endsWith('/series-edit')) {
        calls.push('accept');
        return Response.json({ detail: 'Stale series.' }, { status: 409 });
      }
      throw new Error('Unexpected request: ' + url);
    });
    const timeline = createRemoteTemporalTimelineDataSource(fetchFn, () => 'Europe/Rome');
    const series = createRemoteRecurringSeriesEdit(fetchFn);
    if (!timeline.checkpointWindow) throw new Error('Checkpoint capability missing.');

    const checkpoint = timeline.checkpointWindow(WINDOW);
    await vi.waitFor(() => expect(calls).toContain('checkpoint'));
    const accepted = series.accept(INTENT, {
      fingerprint: PREVIEW.fingerprint,
      targetRefs: [SELECTED],
      newExpectedCount: 1,
      protected: [],
    });
    await flushMicrotasks();
    expect(calls).toEqual(['checkpoint']);

    checkpointResponse.complete(Response.json(CHECKPOINT));
    await checkpoint;
    await expect(accepted).rejects.toThrow(
      'La ricorrenza o una delle istanze è cambiata.',
    );
    expect(calls).toEqual(['checkpoint', 'accept']);
  });
});
