import {
  systemTemporalIdFactory,
  type TemporalAuthoredActivityResult,
  type TemporalAuthoredEventResult,
} from '../../temporal';
import {
  createRemoteRealityObjectiveDataSource,
  type RealityMode,
} from '../../temporal/remote-reality-objective-data-source';
import { createRemoteScheduleMovementPolicyDataSource } from '../../temporal/remote-movement-policy-data-source';
import { createRemotePlacementLockDataSource } from '../../temporal/remote-placement-lock-data-source';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { buildTemporalCreateObjectiveTemplates } from './temporal-create-u2-submit';

type RealityObjectiveDataSource = ReturnType<
  typeof createRemoteRealityObjectiveDataSource
>;
type MovementPolicyDataSource = ReturnType<
  typeof createRemoteScheduleMovementPolicyDataSource
>;
type PlacementLockDataSource = ReturnType<typeof createRemotePlacementLockDataSource>;

type RealityPolicyTask = Readonly<{
  kind: 'activity' | 'event';
  subjectRef: string;
  operationId: string;
  mode: RealityMode;
}>;

type PlacementProtectionTask = Readonly<{
  scheduleRef: string;
  operationId: string;
}>;

function sharedTasks(
  kind: 'activity' | 'event',
  subjectRef: string,
  draft: TemporalCreateU2AuthoringDraft,
) {
  const realityTask: RealityPolicyTask | null =
    draft.realityMode === 'manual'
      ? null
      : Object.freeze({
          kind,
          subjectRef,
          operationId: systemTemporalIdFactory.operationId(),
          mode: draft.realityMode,
        });
  const objectives = buildTemporalCreateObjectiveTemplates(draft).map(
    (objective) =>
      Object.freeze({
        operationId: systemTemporalIdFactory.operationId(),
        objective,
      }),
  );
  return Object.freeze({ realityTask, objectives: Object.freeze(objectives) });
}

function sharedFinalizer(
  kind: 'activity' | 'event',
  subjectRef: string,
  draft: TemporalCreateU2AuthoringDraft,
  source: RealityObjectiveDataSource,
): () => Promise<void> {
  const tasks = sharedTasks(kind, subjectRef, draft);
  const objectiveTasks = tasks.objectives;
  return async () => {
    if (tasks.realityTask !== null) {
      await source.configureReality(kind, subjectRef, {
        operationId: tasks.realityTask.operationId,
        mode: tasks.realityTask.mode,
        expectedStateRef: null,
      });
    }
    for (const task of objectiveTasks) {
      await source.createObjective(kind, subjectRef, {
        operationId: task.operationId,
        label: task.objective.label,
        resultKind: task.objective.result_kind,
        comparatorCode: task.objective.comparator_code,
        targetValue: task.objective.target_value,
        targetMin: task.objective.target_min,
        targetMax: task.objective.target_max,
        unitCode: task.objective.unit_code,
        presentationOrder: task.objective.presentation_order,
      });
    }
  };
}

/**
 * Build idempotent post-authoring Reality/Objectives and Activity placement
 * policy work once, so retries never author a duplicate source.
 */
export function createTemporalCreateRealityFinalizer(
  authored: TemporalAuthoredActivityResult,
  draft: TemporalCreateU2AuthoringDraft,
  realitySource: RealityObjectiveDataSource = createRemoteRealityObjectiveDataSource(),
  movementSource: MovementPolicyDataSource = createRemoteScheduleMovementPolicyDataSource(),
  lockSource: PlacementLockDataSource = createRemotePlacementLockDataSource(),
): () => Promise<void> {
  if (authored.children.length !== draft.activityStructure.children.length) {
    throw new Error(
      'Created internal Activity children do not match the policy draft.',
    );
  }

  const rootFinalizer = sharedFinalizer(
    'activity',
    authored.item.subjectRef,
    draft,
    realitySource,
  );

  const childRealityTasks: RealityPolicyTask[] = [];
  authored.children.forEach((child, index) => {
    const mode =
      draft.activityStructure.children[index]?.realityMode ?? 'manual';
    if (mode === 'manual') return;
    childRealityTasks.push(
      Object.freeze({
        kind: 'activity',
        subjectRef: child.activityRef,
        operationId: systemTemporalIdFactory.operationId(),
        mode,
      }),
    );
  });

  const protectionTasks: PlacementProtectionTask[] = [];
  if (draft.activityStructure.placementProtected) {
    if (authored.schedule === null) {
      throw new Error(
        'Placement protection requires an accepted Activity Schedule.',
      );
    }
    for (const accepted of [
      authored.schedule,
      ...(authored.activityIntervals ?? []),
      ...(authored.plannedSlices ?? []),
      ...authored.children.flatMap((child) => [
        ...(child.schedule ? [child.schedule] : []),
        ...child.plannedSlices,
      ]),
    ]) {
      protectionTasks.push(
        Object.freeze({
          scheduleRef: accepted.scheduleRef,
          operationId: systemTemporalIdFactory.operationId(),
        }),
      );
    }
  }

  return async () => {
    await rootFinalizer();
    for (const task of childRealityTasks) {
      await realitySource.configureReality(task.kind, task.subjectRef, {
        operationId: task.operationId,
        mode: task.mode,
        expectedStateRef: null,
      });
    }
    for (const protectionTask of protectionTasks) {
      await movementSource.protect(
        protectionTask.scheduleRef,
        protectionTask.operationId,
      );
      await lockSource.lock(protectionTask.scheduleRef);
    }
  };
}

export function createTemporalCreateEventRealityFinalizer(
  authored: TemporalAuthoredEventResult,
  draft: TemporalCreateU2AuthoringDraft,
  realitySource: RealityObjectiveDataSource = createRemoteRealityObjectiveDataSource(),
): () => Promise<void> {
  return sharedFinalizer(
    'event',
    authored.item.subjectRef,
    draft,
    realitySource,
  );
}
