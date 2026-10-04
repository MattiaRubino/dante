import {
  systemTemporalIdFactory,
  type TemporalAuthoredActivityResult,
} from '../../temporal';
import {
  createRemoteActivityRealityPolicyDataSource,
  type ActivityRealityMode,
} from '../../temporal/remote-outcome-review-policy-data-source';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';

type RealityPolicyDataSource = ReturnType<
  typeof createRemoteActivityRealityPolicyDataSource
>;

type RealityPolicyTask = Readonly<{
  activityRef: string;
  operationId: string;
  mode: ActivityRealityMode;
}>;

/**
 * Build the idempotent post-authoring policy work once, so a transport failure
 * can retry only the missing configuration without authoring a second Activity.
 *
 * `manual` is the canonical default returned when no policy row exists, so a
 * new Activity needs an explicit write only for the two non-default modes.
 */
export function createTemporalCreateRealityFinalizer(
  authored: TemporalAuthoredActivityResult,
  draft: TemporalCreateU2AuthoringDraft,
  dataSource: RealityPolicyDataSource =
    createRemoteActivityRealityPolicyDataSource(),
): () => Promise<void> {
  if (authored.children.length !== draft.activityStructure.children.length) {
    throw new Error('Created Sub-Activities do not match the Reality policy draft.');
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
    const mode = draft.activityStructure.children[index]?.realityMode ?? 'manual';
    if (mode === 'manual') return;
    tasks.push(
      Object.freeze({
        activityRef: child.activityRef,
        operationId: systemTemporalIdFactory.operationId(),
        mode,
      }),
    );
  });

  return async () => {
    for (const task of tasks) {
      await dataSource.configure(task.activityRef, {
        operationId: task.operationId,
        mode: task.mode,
        expectedStateRef: null,
      });
    }
  };
}
