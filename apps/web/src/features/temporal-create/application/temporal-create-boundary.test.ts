import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

describe('Temporal Create application boundary snapshot', () => {
  it('owns a normalized immutable snapshot before execute so callers cannot mutate prepared intent', async () => {
    const ids = createDeterministicTemporalIdFactory('create-boundary');
    const clock = createFixedTemporalClock(
      Temporal.Instant.from('2026-09-02T08:00:00Z'),
      'Europe/Rome',
    );
    const runtime = createLocalTemporalCreateRuntime({
      ids,
      clock,
      workspace: new InMemoryTemporalWorkspace(ids),
    });
    const baseline = createTemporalCreateFields({
      title: 'Review cliente',
      kind: 'event',
      date: '2026-09-02',
      startTime: '16:00',
    });
    const input = {
      ...baseline,
      event: {
        ...baseline.event,
        purpose: 'Intent originale',
      },
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'cyclic-positional' as const,
        cycleLength: 4,
        cyclePositions: [1, 3],
      },
    };

    const preparation = runtime.prepare(input);
    if (preparation.status !== 'ready') {
      throw new Error('Expected a prepared Create operation');
    }

    input.title = 'Mutazione esterna';
    input.event.purpose = 'Mutazione esterna';
    input.eventRecurrence.cyclePositions.push(4);

    expect(preparation.prepared.command.payload.title).toBe('Review cliente');
    expect(preparation.prepared.metadata.specification.title).toBe(
      'Review cliente',
    );
    expect(preparation.prepared.metadata.specification.event.purpose).toBe(
      'Intent originale',
    );
    expect(
      preparation.prepared.metadata.specification.eventRecurrence
        .cyclePositions,
    ).toEqual([1, 3]);
    expect(Object.isFrozen(preparation.prepared.metadata.specification)).toBe(
      true,
    );
    expect(
      Object.isFrozen(
        preparation.prepared.metadata.specification.eventRecurrence,
      ),
    ).toBe(true);
    expect(
      Object.isFrozen(
        preparation.prepared.metadata.specification.eventRecurrence
          .cyclePositions,
      ),
    ).toBe(true);

    const execution = await runtime.execute(preparation.prepared);
    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.metadata.specification.title).toBe(
      'Review cliente',
    );
  });

  it('re-normalizes ownership before validation and capability projection', () => {
    const runtime = createLocalTemporalCreateRuntime();
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-09-02',
    });
    const contaminated = {
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'elapsed-interval' as const,
        elapsedIntervalMinutes: 1440,
      },
    };

    const preparation = runtime.prepare(contaminated);
    if (preparation.status !== 'ready') {
      throw new Error('Expected normalized Activity Create operation');
    }

    expect(
      preparation.prepared.metadata.specification.eventRecurrence.patternKind,
    ).toBe('none');
    expect(preparation.prepared.command.payload.capabilities).not.toContain(
      'recurrence',
    );
  });
});
