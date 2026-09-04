import type { WorldFocusAdaptiveCompositionSnapshot } from '../application/world-focus-adaptive-composition';
import type { WorldFocusId } from '../model/world-focus-identity';
import { type WorldFocusCompositionRegistration } from './world-focus-composition-host';
import { WorldFocusContinuityResult } from './world-focus-continuity';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';
import { WorldFocusAttention } from './presentation/world-focus-attention';
import { WorldFocusComparison } from './presentation/world-focus-comparison';
import { WorldFocusEvidenceHistory } from './presentation/world-focus-evidence-history';
import { WorldFocusNext } from './presentation/world-focus-next';
import {
  getWorldFocusPreBackendAttentionReasonText,
  getWorldFocusPreBackendDisplayBindings,
} from './presentation/world-focus-pre-backend-display-bindings';
import { WorldFocusSituation } from './presentation/world-focus-situation';
import { WorldFocusTrajectory } from './presentation/world-focus-trajectory';
import { requireWorldFocusDisplayBinding } from './presentation/world-focus-display-bindings';

function requireReady<T extends Readonly<{ status: string }>>(
  result: T,
  kind: string,
): Extract<T, { status: 'ready' }> {
  if (result.status !== 'ready') {
    throw new Error(`World Focus ${kind} renderer has no ready projection`);
  }
  return result as Extract<T, { status: 'ready' }>;
}

function requireItem<T extends Readonly<{ instanceId: string }>>(
  items: readonly T[],
  instanceId: string,
  prefix: string,
): T {
  const expected = `${prefix}:`;
  if (!instanceId.startsWith(expected)) {
    throw new Error(`World Focus ${prefix} instance id is malformed`);
  }
  const itemId = instanceId.slice(expected.length);
  const item = items.find((candidate) => candidate.instanceId === itemId);
  if (item === undefined) {
    throw new Error(`World Focus ${prefix} projection item is unavailable`);
  }
  return item;
}

/**
 * Finite M2 renderer vocabulary bound to one M1 snapshot. Instance ids remain
 * planner identities; renderer lookup stays kind-based and finite.
 */
export function createCoreWorldFocusModuleRegistry(
  snapshot: WorldFocusAdaptiveCompositionSnapshot,
) {
  const bindings = getWorldFocusPreBackendDisplayBindings(snapshot.worldId);

  return new WorldFocusModuleRegistry<
    WorldFocusCompositionRegistration<string, WorldFocusId>
  >([
    {
      kind: 'situation',
      render: () => {
        const result = requireReady(snapshot.situation, 'Situation');
        return <WorldFocusSituation projection={result.projection} bindings={bindings} />;
      },
    },
    {
      kind: 'continuity',
      render: () => <WorldFocusContinuityResult result={snapshot.continuity} />,
    },
    {
      kind: 'attention',
      render: ({ entry }) => {
        const result = requireReady(snapshot.attention, 'Attention');
        const primitive = requireItem(
          result.projection.orderedItems,
          entry.instanceId,
          'attention',
        );
        return (
          <WorldFocusAttention
            primitive={primitive}
            matter={requireWorldFocusDisplayBinding(bindings, primitive.matterReference)}
            resolution={
              primitive.resolutionReference === null
                ? null
                : requireWorldFocusDisplayBinding(
                    bindings,
                    primitive.resolutionReference,
                  )
            }
            reasonText={getWorldFocusPreBackendAttentionReasonText(
              snapshot.worldId,
              primitive.reasonCode,
            )}
          />
        );
      },
    },
    {
      kind: 'next',
      render: () => {
        const result = requireReady(snapshot.next, 'Next');
        return <WorldFocusNext projection={result.projection} bindings={bindings} />;
      },
    },
    {
      kind: 'comparison',
      render: ({ entry }) => {
        const result = requireReady(snapshot.comparison, 'Comparison');
        const primitive = requireItem(
          result.projection.orderedItems,
          entry.instanceId,
          'comparison',
        );
        return (
          <WorldFocusComparison
            primitive={primitive}
            subjects={primitive.subjectReferences.map((reference) =>
              requireWorldFocusDisplayBinding(bindings, reference),
            )}
            basis={
              primitive.basisReference === null
                ? null
                : requireWorldFocusDisplayBinding(bindings, primitive.basisReference)
            }
          />
        );
      },
    },
    {
      kind: 'trajectory',
      render: ({ entry }) => {
        const result = requireReady(snapshot.trajectory, 'Trajectory');
        const primitive = requireItem(
          result.projection.orderedItems,
          entry.instanceId,
          'trajectory',
        );
        return (
          <WorldFocusTrajectory
            primitive={primitive}
            subject={requireWorldFocusDisplayBinding(bindings, primitive.subjectReference)}
            points={primitive.orderedPointReferences.map((reference) =>
              requireWorldFocusDisplayBinding(bindings, reference),
            )}
            missingPositions={primitive.missingPositionReferences.map((reference) =>
              requireWorldFocusDisplayBinding(bindings, reference),
            )}
            orderingBasis={
              primitive.orderingBasisReference === null
                ? null
                : requireWorldFocusDisplayBinding(
                    bindings,
                    primitive.orderingBasisReference,
                  )
            }
            aggregationBasis={
              primitive.aggregationBasisReference === null
                ? null
                : requireWorldFocusDisplayBinding(
                    bindings,
                    primitive.aggregationBasisReference,
                  )
            }
          />
        );
      },
    },
    {
      kind: 'evidence-history',
      render: () => {
        const result = requireReady(snapshot.evidenceHistory, 'Evidence/History');
        return (
          <WorldFocusEvidenceHistory projection={result.projection} bindings={bindings} />
        );
      },
    },
  ]);
}
