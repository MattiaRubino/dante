import { describe, expect, it } from 'vitest';

import type { TemporalAuthoredActivityResult } from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  patchTemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';
import { createTemporalCreateRealityFinalizer } from './temporal-create-reality-finalizer';

describe('Temporal Create Reality finalizer', () => {
  it('keeps root and child Reality independent and reuses operation ids on retry', async () => {
    const base = createTemporalCreateU2AuthoringDraft(
      createTemporalCreateFields({ kind: 'activity' }),
    );
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      activityStructure: Object.freeze({
        ...base.activityStructure,
        realityMode: 'review_on_end',
        children: Object.freeze([
          Object.freeze({
            id: 'child-1',
            title: 'One',
            requirementCode: 'required' as const,
            captureMode: 'disabled' as const,
            realityMode: 'auto_confirm_outcome' as const,
            scheduleEnabled: false,
            startDate: '2026-10-04',
            startTime: '09:00',
            endDate: '2026-10-04',
            endTime: '10:00',
            plannedSlices: Object.freeze([]),
          }),
          Object.freeze({
            id: 'child-2',
            title: 'Two',
            requirementCode: 'optional' as const,
            captureMode: 'disabled' as const,
            realityMode: 'manual' as const,
            scheduleEnabled: false,
            startDate: '2026-10-04',
            startTime: '10:00',
            endDate: '2026-10-04',
            endTime: '11:00',
            plannedSlices: Object.freeze([]),
          }),
        ]),
      }),
    });
    const authored = {
      item: { subjectRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa' },
      children: [
        { activityRef: '0199bbbb-bbbb-7bbb-8bbb-bbbbbbbbbbbb' },
        { activityRef: '0199cccc-cccc-7ccc-8ccc-cccccccccccc' },
      ],
    } as unknown as TemporalAuthoredActivityResult;

    const calls: Array<Readonly<{ activityRef: string; operationId: string; mode: string }>> = [];
    const dataSource = {
      get: async () => {
        throw new Error('not used');
      },
      configure: async (
        activityRef: string,
        command: Readonly<{ operationId: string; mode: string }>,
      ) => {
        calls.push({ activityRef, operationId: command.operationId, mode: command.mode });
        return {
          activityRef,
          stateRef: null,
          mode: command.mode,
          replayed: calls.length > 2,
        };
      },
    };

    const finalize = createTemporalCreateRealityFinalizer(
      authored,
      draft,
      dataSource as never,
    );
    await finalize();
    await finalize();

    expect(calls.map(({ activityRef, mode }) => ({ activityRef, mode }))).toEqual([
      {
        activityRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa',
        mode: 'review_on_end',
      },
      {
        activityRef: '0199bbbb-bbbb-7bbb-8bbb-bbbbbbbbbbbb',
        mode: 'auto_confirm_outcome',
      },
      {
        activityRef: '0199aaaa-aaaa-7aaa-8aaa-aaaaaaaaaaaa',
        mode: 'review_on_end',
      },
      {
        activityRef: '0199bbbb-bbbb-7bbb-8bbb-bbbbbbbbbbbb',
        mode: 'auto_confirm_outcome',
      },
    ]);
    expect(calls[0]?.operationId).toBe(calls[2]?.operationId);
    expect(calls[1]?.operationId).toBe(calls[3]?.operationId);
  });
});
