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
      realityMode: 'review_on_end',
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
    const lockCalls: string[] = [];
    const realitySource = {
      configureReality: (
        kind: 'activity' | 'event' | 'occurrence',
        activityRef: string,
        command: Readonly<{ operationId: string; mode: string }>,
      ) => {
        expect(kind).toBe('activity');
        realityCalls.push({
          activityRef,
          operationId: command.operationId,
          mode: command.mode,
        });
        return Promise.resolve();
      },
      createObjective: () => Promise.reject(new Error('not used')),
      listObjectives: () => Promise.resolve(Object.freeze([])),
      recordResult: () => Promise.reject(new Error('not used')),
    };
    const movementSource = {
      protect: (scheduleRef: string, operationId: string) => {
        movementCalls.push({ scheduleRef, operationId });
        return Promise.resolve({
          scheduleRef,
          materialStateRef: '0199eeee-eeee-7eee-8eee-eeeeeeeeeeee',
          replayed: movementCalls.length > 1,
        });
      },
    };
    const lockSource = {
      lock: (scheduleRef: string) => {
        lockCalls.push(scheduleRef);
        return Promise.resolve({ scheduleRef, locked: true, revision: 1 });
      },
    };

    const finalize = createTemporalCreateRealityFinalizer(
      authored,
      draft,
      realitySource as never,
      movementSource,
      lockSource as never,
    );
    await finalize();
    await finalize();

    expect(
      realityCalls.map(({ activityRef, mode }) => ({ activityRef, mode })),
    ).toEqual([
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
    expect(lockCalls).toEqual([
      '0199dddd-dddd-7ddd-8ddd-dddddddddddd',
      '0199dddd-dddd-7ddd-8ddd-dddddddddddd',
    ]);
    expect(realityCalls[0]?.operationId).toBe(realityCalls[1]?.operationId);
    expect(movementCalls[0]?.operationId).toBe(movementCalls[1]?.operationId);
  });

  it('persists independent Objective verification modes without changing completion mode', async () => {
    const base = createTemporalCreateU2AuthoringDraft(
      createTemporalCreateFields({ kind: 'activity' }),
    );
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      objectives: [
        {
          id: 'first',
          label: 'Correre',
          resultKind: 'quantity',
          comparatorCode: 'gte',
          targetValue: '5',
          targetMin: '',
          targetMax: '',
          unitCode: 'km',
          verificationMode: 'review_on_end',
        },
        {
          id: 'second',
          label: 'Stretching',
          resultKind: 'boolean',
          comparatorCode: null,
          targetValue: '',
          targetMin: '',
          targetMax: '',
          unitCode: '',
          verificationMode: 'none',
        },
      ],
    });
    const authored = {
      item: { subjectRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa' },
      schedule: null,
      children: [],
    } as unknown as TemporalAuthoredActivityResult;
    const calls: Array<{
      mode: string;
      label: string;
      operationId: string;
    }> = [];
    const realitySource = {
      configureReality: () =>
        Promise.reject(new Error('Completion mode must remain manual')),
      createObjective: (
        _kind: string,
        _ref: string,
        command: Readonly<{
          verificationMode: string;
          label: string;
          operationId: string;
        }>,
      ) => {
        calls.push({
          mode: command.verificationMode,
          label: command.label,
          operationId: command.operationId,
        });
        return Promise.resolve({});
      },
    };

    const finalize = createTemporalCreateRealityFinalizer(
      authored,
      draft,
      realitySource as never,
    );
    await finalize();
    expect(calls.map(({ label, mode }) => ({ label, mode }))).toEqual([
      { label: 'Correre', mode: 'review_on_end' },
      { label: 'Stretching', mode: 'none' },
    ]);
    const ids = calls.map(({ operationId }) => operationId);
    await finalize();
    expect(calls.slice(2).map(({ operationId }) => operationId)).toEqual(ids);
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
