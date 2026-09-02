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
const COMPARISON_POLICY = Object.freeze({ maxSubjectReferences: 4 });
const TRAJECTORY_POLICY = Object.freeze({
  maxOrderedPointReferences: 8,
  maxMissingPositionReferences: 8,
});

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

  it('requires Comparison to have at least two distinct explicitly bounded subjects', () => {
    const comparison = createWorldFocusComparisonPrimitive(
      {
        instanceId: 'comparison:plan-actual',
        mode: 'planned-actual',
        subjectReferences: [
          ref('schedule', 'planned'),
          ref('actual', 'observed'),
        ],
        basisReference: ref('window', 'week-36'),
      },
      COMPARISON_POLICY,
    );

    expect(comparison.subjectReferences).toHaveLength(2);
    expect(() =>
      createWorldFocusComparisonPrimitive(
        {
          instanceId: 'comparison:duplicate',
          mode: 'difference',
          subjectReferences: [ref('source', 'a'), ref('source', 'a')],
          basisReference: null,
        },
        COMPARISON_POLICY,
      ),
    ).toThrow(/duplicate references/);

    expect(() =>
      createWorldFocusComparisonPrimitive(
        {
          instanceId: 'comparison:too-wide',
          mode: 'difference',
          subjectReferences: [
            ref('source', 'a'),
            ref('source', 'b'),
            ref('source', 'c'),
          ],
          basisReference: null,
        },
        { maxSubjectReferences: 2 },
      ),
    ).toThrow(/exceed configured maximum 2/);
  });

  it('requires Trajectory to preserve order, explicit missingness, aggregation basis and reference bounds', () => {
    const trajectory = createWorldFocusTrajectoryPrimitive(
      {
        instanceId: 'trajectory:pace',
        subjectReference: ref('goal', 'exam'),
        axis: 'time',
        orderedPointReferences: [
          ref('observation', 'week-1'),
          ref('observation', 'week-3'),
        ],
        missingPositionReferences: [ref('interval', 'week-2')],
        orderingBasisReference: ref('window', 'exam-cycle'),
        aggregationBasisReference: ref('aggregation', 'weekly-average'),
      },
      TRAJECTORY_POLICY,
    );

    expect(trajectory.orderedPointReferences.map(({ key }) => key)).toEqual([
      'week-1',
      'week-3',
    ]);
    expect(trajectory.missingPositionReferences).toEqual([
      { kind: 'interval', key: 'week-2' },
    ]);
    expect(trajectory.aggregationBasisReference).toEqual({
      kind: 'aggregation',
      key: 'weekly-average',
    });
    expect(getWorldFocusWorkPrimitiveReferences(trajectory)).toHaveLength(6);

    expect(() =>
      createWorldFocusTrajectoryPrimitive(
        {
          instanceId: 'trajectory:too-dense',
          subjectReference: ref('metric', 'pace'),
          axis: 'time',
          orderedPointReferences: [
            ref('observation', '1'),
            ref('observation', '2'),
            ref('observation', '3'),
          ],
          missingPositionReferences: [],
          orderingBasisReference: null,
          aggregationBasisReference: null,
        },
        {
          maxOrderedPointReferences: 2,
          maxMissingPositionReferences: 0,
        },
      ),
    ).toThrow(/exceed configured maximum 2/);
  });

  it('does not allow one trajectory reference to be both present and missing', () => {
    expect(() =>
      createWorldFocusTrajectoryPrimitive(
        {
          instanceId: 'trajectory:invalid-gap',
          subjectReference: ref('metric', 'pace'),
          axis: 'time',
          orderedPointReferences: [
            ref('interval', 'week-1'),
            ref('interval', 'week-2'),
          ],
          missingPositionReferences: [ref('interval', 'week-2')],
          orderingBasisReference: ref('window', 'month'),
          aggregationBasisReference: null,
        },
        TRAJECTORY_POLICY,
      ),
    ).toThrow(/present and missing references must be distinct/);
  });

  it('rejects invalid reference-bound policies rather than silently becoming unbounded', () => {
    expect(() =>
      createWorldFocusComparisonPrimitive(
        {
          instanceId: 'comparison:invalid-policy',
          mode: 'difference',
          subjectReferences: [ref('source', 'a'), ref('source', 'b')],
          basisReference: null,
        },
        { maxSubjectReferences: 1 },
      ),
    ).toThrow(/greater than or equal to 2/);

    expect(() =>
      createWorldFocusTrajectoryPrimitive(
        {
          instanceId: 'trajectory:invalid-policy',
          subjectReference: ref('metric', 'pace'),
          axis: 'time',
          orderedPointReferences: [
            ref('observation', '1'),
            ref('observation', '2'),
          ],
          missingPositionReferences: [],
          orderingBasisReference: null,
          aggregationBasisReference: null,
        },
        {
          maxOrderedPointReferences: Number.POSITIVE_INFINITY,
          maxMissingPositionReferences: 0,
        },
      ),
    ).toThrow(/must be an integer/);
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
