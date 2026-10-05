import {
  systemTemporalIdFactory,
  type TemporalAuthoredActivityResult,
} from '../../temporal';
import {
  createRemoteActivityRealityPolicyDataSource,
  type ActivityRealityMode,
} from '../../temporal/remote-outcome-review-policy-data-source';
import { createRemoteScheduleMovementPolicyDataSource } from '../../temporal/remote-movement-policy-data-source';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';

type RealityPolicyDataSource = ReturnType<
  typeof createRemoteActivityRealityPolicyDataSource
>;
type MovementPolicyDataSource = ReturnType<
  typeof createRemoteScheduleMovementPolicyDataSource
>;

type RealityPolicyTask = Readonly<{
  activityRef: string;
  operationId: string;
  mode: ActivityRealityMode;
}>;

type PlacementProtectionTask = Readonly<{
  scheduleRef: string;
  operationId: string;
}>;

/**
 * Build idempotent post-authoring policy work once, so a transport failure can
 * retry only missing configuration without authoring a second Activity.
 *
 * `manual` is the canonical Reality default returned when no policy row exists.
 * Placement protection reuses B04 Movement Policy: `blocked + direct` means
 * solver/AI/automation movement is forbidden without inventing a second lock.
 */
export function createTemporalCreateRealityFinalizer(
  authored: TemporalAuthoredActivityResult,
  draft: TemporalCreateU2AuthoringDraft,
  dataSource: RealityPolicyDataSource = createRemoteActivityRealityPolicyDataSource(),
  movementSource: MovementPolicyDataSource = createRemoteScheduleMovementPolicyDataSource(),
): () => Promise<void> {
  if (authored.children.length !== draft.activityStructure.children.length) {
    throw new Error(
      'Created Sub-Activities do not match the Reality policy draft.',
    );
  }

  const tasks: RealityPolicyTask[] = [];
  const rootMode = draft.activityStructure.realityMode;
  if (rootMode !== 'manual') {
    tasks.push(
      Object.freeze({
        activityRef: authored.item.subjectRef,
        operationId: systemTemporalIdFactory.operationId(),
        mode: rootMode,
      }),
    );
  }

  authored.children.forEach((child, index) => {
    const mode =
      draft.activityStructure.children[index]?.realityMode ?? 'manual';
    if (mode === 'manual') return;
    tasks.push(
      Object.freeze({
        activityRef: child.activityRef,
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
    for (const task of tasks) {
      await dataSource.configure(task.activityRef, {
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
    }
  };
}
