import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreatePreparedOperation,
} from './temporal-create-runtime';

function runtime() {
  const ids = createDeterministicTemporalIdFactory('c1-appearance');
  const clock = createFixedTemporalClock(
    Temporal.Instant.from('2026-09-01T08:00:00Z'),
    'Europe/Rome',
  );
  return createLocalTemporalCreateRuntime({
    ids,
    clock,
    workspace: new InMemoryTemporalWorkspace(ids),
  });
}

describe('Temporal Create appearance runtime boundary', () => {
  it('keeps appearance out of the F0 command while retaining it in rich manual specification', () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Deep work override',
        date: '2026-09-01',
        contextId: 'focus',
        appearanceTone: 'urgent',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    expect(preparation.prepared.metadata.specification.appearanceTone).toBe(
      'urgent',
    );
    expect(preparation.prepared.metadata.contextId).toBe('focus');
    expect(
      Object.prototype.hasOwnProperty.call(
        preparation.prepared.command.payload,
        'appearanceTone',
      ),
    ).toBe(false);
  });

  it('rejects operation-id reuse when only presentation appearance intent changes', async () => {
    const createRuntime = runtime();
    const originalFields = createTemporalCreateFields({
      title: 'Deep work override',
      date: '2026-09-01',
      contextId: 'focus',
      appearanceTone: null,
    });
    const preparation = createRuntime.prepare(originalFields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const first = await createRuntime.execute(preparation.prepared);
    expect(first.result.status).toBe('applied');

    const changedSpecification = createTemporalCreateFields({
      ...preparation.prepared.metadata.specification,
      appearanceTone: 'urgent',
    });
    const tampered = Object.freeze({
      ...preparation.prepared,
      metadata: Object.freeze({
        ...preparation.prepared.metadata,
        specification: changedSpecification,
      }),
    }) satisfies TemporalCreatePreparedOperation;

    const collision = await createRuntime.execute(tampered);
    const records = await createRuntime.listRecords();

    expect(collision.effect).toBeNull();
    expect(collision.result.status).toBe('rejected');
    if (collision.result.status === 'rejected') {
      expect(collision.result.code).toBe('operation-id-reused');
    }
    expect(records).toHaveLength(1);
    expect(records[0]?.metadata.contextId).toBe('focus');
    expect(records[0]?.metadata.specification.appearanceTone).toBeNull();
  });
});
