import { describe, expect, it } from 'vitest';

import type { TemporalAuthoredActivityResult } from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  patchTemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';
import { createTemporalCreateRealityFinalizer } from './temporal-create-reality-finalizer';

describe('Temporal Create policy finalizer', () => {
  it('keeps policy operation ids stable across safe retry', async () => {
    const base = createTemporalCreateU2AuthoringDraft(
      createTemporalCreateFields({ kind: 'activity' }),
    );
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      activityStructure: Object.freeze({
        ...base.activityStructure,
        realityMode: 'review_on_end',
        placementProtected: true,
      }),
    });
    const authored = {
      item: { subjectRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa' },
      schedule: {
        scheduleRef: '0199dddd-dddd-7ddd-8ddd-dddddddddddd',
      },
      children: [],
    } as unknown as TemporalAuthoredActivityResult;

    const realityCalls: Array<
      Readonly<{ activityRef: string; operationId: string; mode: string }>
    > = [];
    const movementCalls: Array<
      Readonly<{ scheduleRef: string; operationId: string }>
    > = [];
    const realitySource = {
      get: async () => {
        throw new Error('not used');
      },
      configure: async (
        activityRef: string,
        command: Readonly<{ operationId: string; mode: string }>,
      ) => {
        realityCalls.push({
          activityRef,
          operationId: command.operationId,
          mode: command.mode,
        });
        return {
          activityRef,
          stateRef: null,
          mode: command.mode,
          replayed: realityCalls.length > 1,
        };
      },
    };
    const movementSource = {
      protect: async (scheduleRef: string, operationId: string) => {
        movementCalls.push({ scheduleRef, operationId });
        return {
          scheduleRef,
          materialStateRef: '0199eeee-eeee-7eee-8eee-eeeeeeeeeeee',
          replayed: movementCalls.length > 1,
        };
      },
    };

    const finalize = createTemporalCreateRealityFinalizer(
      authored,
      draft,
      realitySource as never,
      movementSource as never,
    );
    await finalize();
    await finalize();

    expect(realityCalls.map(({ activityRef, mode }) => ({ activityRef, mode }))).toEqual([
      {
        activityRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa',
        mode: 'review_on_end',
      },
      {
        activityRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa',
        mode: 'review_on_end',
      },
    ]);
    expect(movementCalls.map(({ scheduleRef }) => scheduleRef)).toEqual([
      '0199dddd-dddd-7ddd-8ddd-dddddddddddd',
      '0199dddd-dddd-7ddd-8ddd-dddddddddddd',
    ]);
    expect(realityCalls[0]?.operationId).toBe(realityCalls[1]?.operationId);
    expect(movementCalls[0]?.operationId).toBe(movementCalls[1]?.operationId);
  });

  it('refuses placement protection when authoring produced no Activity Schedule', () => {
    const base = createTemporalCreateU2AuthoringDraft(
      createTemporalCreateFields({ kind: 'activity' }),
    );
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      activityStructure: Object.freeze({
        ...base.activityStructure,
        placementProtected: true,
      }),
    });
    const authored = {
      item: { subjectRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa' },
      schedule: null,
      children: [],
    } as unknown as TemporalAuthoredActivityResult;

    expect(() => createTemporalCreateRealityFinalizer(authored, draft)).toThrow(
      'Placement protection requires an accepted Activity Schedule.',
    );
  });
});
