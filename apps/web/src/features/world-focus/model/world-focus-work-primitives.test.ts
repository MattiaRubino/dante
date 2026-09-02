import { describe, expect, it } from 'vitest';

import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
  createWorldFocusContinuityPrimitive,
  createWorldFocusTrajectoryPrimitive,
  getWorldFocusWorkPrimitiveReferences,
  WORLD_FOCUS_WORK_PRIMITIVE_KINDS,
} from './world-focus-work-primitives';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus WS6 work primitives', () => {
  it('keeps the finite WS6 catalog exact and AI-independent', () => {
    expect(WORLD_FOCUS_WORK_PRIMITIVE_KINDS).toEqual([
      'continuity',
      'attention',
      'comparison',
      'trajectory',
    ]);
  });

  it('constructs Continuity without collapsing recent/open state into resumability', () => {
    const continuity = createWorldFocusContinuityPrimitive({
      instanceId: 'continuity:release',
      threadReference: ref('activity', 'release-v2'),
      checkpointReference: ref('artifact', 'mix-v7'),
      continuationReference: ref('route', 'release-editor'),
      state: 'paused',
    });

    expect(continuity).toEqual({
      instanceId: 'continuity:release',
      kind: 'continuity',
      threadReference: { kind: 'activity', key: 'release-v2' },
      checkpointReference: { kind: 'artifact', key: 'mix-v7' },
      continuationReference: { kind: 'route', key: 'release-editor' },
      state: 'paused',
    });
    expect(getWorldFocusWorkPrimitiveReferences(continuity)).toHaveLength(3);
  });

  it('allows blocked Continuity without inventing a continuation destination', () => {
    const continuity = createWorldFocusContinuityPrimitive({
      instanceId: 'continuity:blocked',
      threadReference: ref('activity', 'publish'),
      checkpointReference: ref('decision', 'review-required'),
      continuationReference: null,
      state: 'blocked',
    });

    expect(continuity.continuationReference).toBeNull();
  });

  it('constructs Attention as unresolved work rather than notification/read state', () => {
    const attention = createWorldFocusAttentionPrimitive({
      instanceId: 'attention:deadline',
      matterReference: ref('obligation', 'filing-2026'),
      reasonCode: 'deadline-risk',
      resolutionReference: ref('request', 'review-filing'),
      state: 'awaiting-response',
    });

    expect(attention.kind).toBe('attention');
    expect(attention.reasonCode).toBe('deadline-risk');
    expect(attention.state).toBe('awaiting-response');
  });

  it('requires Comparison to have at least two distinct bounded subjects', () => {
    const comparison = createWorldFocusComparisonPrimitive({
      instanceId: 'comparison:plan-actual',
      mode: 'planned-actual',
      subjectReferences: [ref('schedule', 'planned'), ref('actual', 'observed')],
      basisReference: ref('window', 'week-36'),
    });

    expect(comparison.subjectReferences).toHaveLength(2);
    expect(() =>
      createWorldFocusComparisonPrimitive({
        instanceId: 'comparison:duplicate',
        mode: 'difference',
        subjectReferences: [ref('source', 'a'), ref('source', 'a')],
        basisReference: null,
      }),
    ).toThrow(/duplicate references/);
  });

  it('requires Trajectory to preserve ordered multi-point meaning', () => {
    const trajectory = createWorldFocusTrajectoryPrimitive({
      instanceId: 'trajectory:pace',
      subjectReference: ref('goal', 'exam'),
      axis: 'time',
      orderedPointReferences: [
        ref('observation', 'week-1'),
        ref('observation', 'week-2'),
        ref('observation', 'week-3'),
      ],
      orderingBasisReference: ref('window', 'exam-cycle'),
    });

    expect(trajectory.orderedPointReferences.map(({ key }) => key)).toEqual([
      'week-1',
      'week-2',
      'week-3',
    ]);
  });

  it('rejects structurally empty primitive identities and references', () => {
    expect(() =>
      createWorldFocusAttentionPrimitive({
        instanceId: '   ',
        matterReference: ref('source', 'x'),
        reasonCode: 'risk',
        resolutionReference: null,
        state: 'unresolved',
      }),
    ).toThrow(/instance id must not be empty/);

    expect(() =>
      createWorldFocusContinuityPrimitive({
        instanceId: 'continuity:x',
        threadReference: ref('', 'x'),
        checkpointReference: ref('source', 'checkpoint'),
        continuationReference: null,
        state: 'active',
      }),
    ).toThrow(/reference kind must not be empty/);
  });
});
