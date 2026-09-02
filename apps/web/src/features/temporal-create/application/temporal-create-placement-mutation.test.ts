import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

describe('Temporal Create governed projection mutations', () => {
  it('places one existing unscheduled Activity and Undo restores the same identity to null placement', async () => {
    const ids = createDeterministicTemporalIdFactory('planning-tray-place');
    const clock = createFixedTemporalClock(
      Temporal.Instant.from('2026-09-02T08:00:00Z'),
      'Europe/Rome',
    );
    const runtime = createLocalTemporalCreateRuntime({
      ids,
      clock,
      workspace: new InMemoryTemporalWorkspace(ids),
    });
    const fields = createTemporalCreateFields({
      title: 'Montare il video',
      kind: 'activity',
      date: '2026-09-02',
      timeSemantics: 'unscheduled',
      durationMinutes: 75,
      contextId: 'creative',
    });
    const preparation = runtime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected unscheduled Activity preparation');
    }

    const created = await runtime.execute(preparation.prepared);
    if (!created.effect) {
      throw new Error('Expected applied Create effect');
    }
    const projectionId = created.effect.projection.id;
    expect(created.effect.projection.placement).toBeNull();
    expect(created.effect.projection.revision).toBe(1);

    const start = Temporal.PlainDateTime.from('2026-09-03T14:15');
    const placed = await created.effect.replacePlacement(
      Object.freeze({
        kind: 'floating-local' as const,
        start,
        end: start.add({ minutes: 75 }),
      }),
    );

    expect(placed.result.status).toBe('applied');
    expect(placed.effect?.projection?.id).toBe(projectionId);
    expect(placed.effect?.projection?.revision).toBe(2);
    expect(placed.effect?.projection?.placement?.kind).toBe('floating-local');
    expect((await runtime.list()).map((item) => item.id)).toEqual([projectionId]);
    expect((await runtime.listRecords())[0]?.metadata.specification.title).toBe(
      'Montare il video',
    );

    const undone = await placed.effect?.undo();
    expect(undone?.status).toBe('applied');
    expect(undone?.status === 'applied' ? undone.item?.id : null).toBe(
      projectionId,
    );
    expect(
      undone?.status === 'applied' ? undone.item?.placement : undefined,
    ).toBeNull();
    expect((await runtime.list())[0]?.id).toBe(projectionId);
    expect((await runtime.list())[0]?.placement).toBeNull();
    expect((await runtime.listRecords())[0]?.metadata.specification.title).toBe(
      'Montare il video',
    );
  });

  it('removes an unscheduled Activity through F0 and Undo restores the same rich record', async () => {
    const ids = createDeterministicTemporalIdFactory('planning-tray-delete');
    const runtime = createLocalTemporalCreateRuntime({
      ids,
      workspace: new InMemoryTemporalWorkspace(ids),
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Archiviare documenti',
        kind: 'activity',
        date: '2026-09-02',
        timeSemantics: 'unscheduled',
        durationMinutes: 40,
        notes: 'Cartella personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected unscheduled Activity preparation');
    }
    const created = await runtime.execute(preparation.prepared);
    if (!created.effect) {
      throw new Error('Expected applied Create effect');
    }
    const projectionId = created.effect.projection.id;

    const removed = await created.effect.remove();
    expect(removed.result.status).toBe('applied');
    expect(await runtime.list()).toEqual([]);
    expect(await runtime.listRecords()).toEqual([]);

    const restored = await removed.effect?.undo();
    expect(restored?.status).toBe('applied');
    expect(restored?.status === 'applied' ? restored.item?.id : null).toBe(
      projectionId,
    );
    expect((await runtime.list())[0]?.id).toBe(projectionId);
    expect((await runtime.list())[0]?.placement).toBeNull();
    expect((await runtime.listRecords())[0]?.metadata.notes).toBe(
      'Cartella personale',
    );
  });
});
