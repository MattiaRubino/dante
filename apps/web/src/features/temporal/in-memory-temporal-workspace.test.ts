import { Temporal } from '@dante/time';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { TemporalCommand } from './application';
import { InMemoryTemporalWorkspace } from './in-memory-temporal-workspace';
import {
  createDeterministicTemporalIdFactory,
  type TemporalIdFactory,
} from './model';

describe('InMemoryTemporalWorkspace F0 contract', () => {
  let ids: TemporalIdFactory;
  let workspace: InMemoryTemporalWorkspace;

  const issuedAt = Temporal.Instant.from('2026-08-04T08:00:00Z');

  beforeEach(() => {
    ids = createDeterministicTemporalIdFactory('workspace');
    workspace = new InMemoryTemporalWorkspace(ids);
  });

  function createCommand(
    title = 'Client call',
  ): Extract<TemporalCommand, { type: 'temporal.projection.create' }> {
    return {
      type: 'temporal.projection.create',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt,
      payload: {
        id: ids.projectionId(),
        subject: {
          source: 'native',
          kind: 'event',
          id: 'event:client-call',
        },
        title,
        placement: {
          kind: 'zoned',
          start: Temporal.ZonedDateTime.from(
            '2026-08-04T10:00:00+02:00[Europe/Rome]',
          ),
          end: Temporal.ZonedDateTime.from(
            '2026-08-04T10:45:00+02:00[Europe/Rome]',
          ),
        },
        capabilities: ['placement', 'notes'],
      },
    };
  }

  it('applies create once and makes retry idempotent by operation id', async () => {
    const command = createCommand();
    const first = await workspace.execute(command);
    const retry = await workspace.execute({ ...command });

    expect(first.status).toBe('applied');
    expect(retry).toBe(first);

    const list = await workspace.query({
      type: 'temporal.projection.list',
    });
    expect(list.status).toBe('ok');
    if (list.status === 'ok') {
      expect(list.snapshot.revision).toBe(1);
      expect(list.snapshot.items).toHaveLength(1);
    }
  });

  it('rejects the same operation id when the payload changes even if the command type is unchanged', async () => {
    const create = createCommand();
    const first = await workspace.execute(create);
    expect(first.status).toBe('applied');

    const collision = await workspace.execute({
      ...create,
      payload: {
        ...create.payload,
        title: 'Different intent with same idempotency key',
      },
    });

    expect(collision.status).toBe('rejected');
    if (collision.status === 'rejected') {
      expect(collision.code).toBe('operation-id-reused');
    }

    const list = await workspace.query({
      type: 'temporal.projection.list',
    });
    expect(list.snapshot.items).toHaveLength(1);
    expect(list.snapshot.items[0]?.title).toBe('Client call');
    expect(list.snapshot.revision).toBe(1);
  });

  it('rejects operation-id reuse across different command types', async () => {
    const create = createCommand();
    const created = await workspace.execute(create);
    expect(created.status).toBe('applied');

    const result = await workspace.execute({
      type: 'temporal.projection.remove',
      operationId: create.operationId,
      source: 'manual',
      issuedAt,
      payload: {
        id: create.payload.id,
        expectedRevision: 1,
      },
    });

    expect(result.status).toBe('rejected');
    if (result.status === 'rejected') {
      expect(result.code).toBe('operation-id-reused');
    }
  });

  it('keeps validation rejection side-effect free', async () => {
    const listener = vi.fn();
    workspace.subscribe(listener);

    const invalid = createCommand('   ');
    const result = await workspace.execute(invalid);

    expect(result.status).toBe('rejected');
    expect(listener).not.toHaveBeenCalled();

    const list = await workspace.query({
      type: 'temporal.projection.list',
    });
    if (list.status === 'ok') {
      expect(list.snapshot.revision).toBe(0);
      expect(list.snapshot.items).toHaveLength(0);
    }
  });

  it('enforces revision preconditions and reports no-op truthfully', async () => {
    const created = await workspace.execute(createCommand());
    expect(created.status).toBe('applied');
    if (created.status !== 'applied' || !created.item) {
      return;
    }

    const noOp = await workspace.execute({
      type: 'temporal.placement.replace',
      operationId: ids.operationId(),
      source: 'keyboard',
      issuedAt: issuedAt.add({ minutes: 1 }),
      payload: {
        id: created.item.id,
        expectedRevision: 1,
        placement: created.item.placement,
      },
    });

    expect(noOp.status).toBe('no-op');
    if (noOp.status === 'no-op') {
      expect(noOp.snapshotRevision).toBe(1);
      expect(noOp).not.toHaveProperty('undoToken');
    }

    const stale = await workspace.execute({
      type: 'temporal.placement.replace',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 2 }),
      payload: {
        id: created.item.id,
        expectedRevision: 99,
        placement: null,
      },
    });

    expect(stale.status).toBe('rejected');
    if (stale.status === 'rejected') {
      expect(stale.code).toBe('revision-conflict');
      expect(stale.currentRevision).toBe(1);
    }
  });

  it('uses monotonic revisioned Undo instead of restoring stale version numbers', async () => {
    const created = await workspace.execute(createCommand());
    expect(created.status).toBe('applied');
    if (created.status !== 'applied' || !created.item) {
      return;
    }

    const moved = await workspace.execute({
      type: 'temporal.placement.replace',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 1 }),
      payload: {
        id: created.item.id,
        expectedRevision: 1,
        placement: {
          kind: 'floating-local',
          start: Temporal.PlainDateTime.from('2026-08-04T11:00'),
          end: Temporal.PlainDateTime.from('2026-08-04T12:00'),
        },
      },
    });

    expect(moved.status).toBe('applied');
    if (moved.status !== 'applied' || !moved.item || !moved.undoToken) {
      return;
    }
    expect(moved.item.revision).toBe(2);

    const restored = await workspace.execute({
      type: 'temporal.operation.undo',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 2 }),
      payload: { undoToken: moved.undoToken },
    });

    expect(restored.status).toBe('applied');
    if (restored.status === 'applied' && restored.item) {
      expect(restored.item.revision).toBe(3);
      expect(restored.item.placement?.kind).toBe('zoned');
    }
  });

  it('refuses an older Undo after newer truth exists', async () => {
    const created = await workspace.execute(createCommand());
    expect(created.status).toBe('applied');
    if (created.status !== 'applied' || !created.item || !created.undoToken) {
      return;
    }

    await workspace.execute({
      type: 'temporal.placement.replace',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 1 }),
      payload: {
        id: created.item.id,
        expectedRevision: 1,
        placement: null,
      },
    });

    const undoCreate = await workspace.execute({
      type: 'temporal.operation.undo',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 2 }),
      payload: { undoToken: created.undoToken },
    });

    expect(undoCreate.status).toBe('rejected');
    if (undoCreate.status === 'rejected') {
      expect(undoCreate.code).toBe('undo-conflict');
      expect(undoCreate.currentRevision).toBe(2);
    }
  });

  it('undoes create idempotently and remove reversibly', async () => {
    const create = createCommand();
    const created = await workspace.execute(create);
    expect(created.status).toBe('applied');
    if (created.status !== 'applied' || !created.item || !created.undoToken) {
      return;
    }

    const remove = await workspace.execute({
      type: 'temporal.projection.remove',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 1 }),
      payload: {
        id: created.item.id,
        expectedRevision: 1,
      },
    });
    expect(remove.status).toBe('applied');

    if (remove.status !== 'applied' || !remove.undoToken) {
      return;
    }

    const restore = await workspace.execute({
      type: 'temporal.operation.undo',
      operationId: ids.operationId(),
      source: 'manual',
      issuedAt: issuedAt.add({ minutes: 2 }),
      payload: { undoToken: remove.undoToken },
    });
    expect(restore.status).toBe('applied');
    if (restore.status === 'applied' && restore.item) {
      expect(restore.item.id).toBe(created.item.id);
      expect(restore.item.revision).toBe(2);
    }
  });

  it('notifies only on applied mutations and sorts query projections deterministically', async () => {
    const listener = vi.fn();
    workspace.subscribe(listener);

    const zulu = createCommand('Zulu');
    const alpha = createCommand('Alpha');

    await workspace.execute(zulu);
    await workspace.execute(alpha);
    expect(listener).toHaveBeenCalledTimes(2);

    const list = await workspace.query({
      type: 'temporal.projection.list',
    });
    expect(list.status).toBe('ok');
    if (list.status === 'ok') {
      const idsInSnapshot = list.snapshot.items.map((item) => item.id);
      expect(idsInSnapshot).toEqual(
        [...idsInSnapshot].sort((left, right) => left.localeCompare(right)),
      );
      expect(list.snapshot.revision).toBe(2);
    }
  });

  it('isolates subscriber rendering failures from committed application state', async () => {
    workspace.subscribe(() => {
      throw new Error('render failed');
    });

    const result = await workspace.execute(createCommand());
    expect(result.status).toBe('applied');

    const list = await workspace.query({
      type: 'temporal.projection.list',
    });
    if (list.status === 'ok') {
      expect(list.snapshot.items).toHaveLength(1);
      expect(list.snapshot.revision).toBe(1);
    }
  });
});
