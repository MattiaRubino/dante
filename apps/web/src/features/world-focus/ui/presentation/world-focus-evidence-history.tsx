import { useTranslation } from 'react-i18next';

import type { WorldFocusContextReference } from '../../model/world-focus-context-reference';
import type { WorldFocusEvidenceHistoryProjection } from '../../model/world-focus-direct-projections';
import {
  requireWorldFocusDisplayBinding,
  type WorldFocusDisplayBinding,
  type WorldFocusDisplayBindingSet,
} from './world-focus-display-bindings';
import {
  WorldFocusPresentationSection,
  WorldFocusPresentationSubsection,
} from './world-focus-presentation-primitives';

function bindingKey(binding: WorldFocusDisplayBinding): string {
  return `${binding.reference.kind}\u0000${binding.reference.key}`;
}

function resolveBindings(
  bindings: WorldFocusDisplayBindingSet,
  references: readonly WorldFocusContextReference[],
): readonly WorldFocusDisplayBinding[] {
  return references.map((reference) =>
    requireWorldFocusDisplayBinding(bindings, reference),
  );
}

type EvidenceRoleProps = Readonly<{
  title: string;
  bindings: readonly WorldFocusDisplayBinding[];
}>;

function EvidenceRole({ title, bindings }: EvidenceRoleProps) {
  if (bindings.length === 0) return null;

  return (
    <WorldFocusPresentationSubsection
      className="world-focus-evidence-role"
      title={title}
    >
      <ul className="world-focus-direct-list">
        {bindings.map((binding) => (
          <li className="world-focus-direct-row" key={bindingKey(binding)}>
            <p className="world-focus-presentation-row-title">{binding.label}</p>
            {binding.supportingText === undefined ? null : (
              <p className="world-focus-presentation-row-supporting">
                {binding.supportingText}
              </p>
            )}
          </li>
        ))}
      </ul>
    </WorldFocusPresentationSubsection>
  );
}

type WorldFocusEvidenceHistoryProps = Readonly<{
  projection: WorldFocusEvidenceHistoryProjection;
  bindings: WorldFocusDisplayBindingSet;
}>;

export function WorldFocusEvidenceHistory({
  projection,
  bindings,
}: WorldFocusEvidenceHistoryProps) {
  const { t } = useTranslation('common');
  const evidenceBindings = resolveBindings(
    bindings,
    projection.evidence.evidenceReferences,
  );
  const provenanceBindings = resolveBindings(
    bindings,
    projection.evidence.provenanceReferences,
  );
  const integrityBindings = resolveBindings(
    bindings,
    projection.evidence.integrityAttestationReferences,
  );
  const historyBindings = resolveBindings(
    bindings,
    projection.orderedHistoryReferences,
  );

  return (
    <WorldFocusPresentationSection
      className="world-focus-direct-output world-focus-evidence-history"
      title={t(($) => $.common.worldFocus.presentation.evidenceHistory.title)}
      data-world-focus-direct-output="evidence-history"
    >
      <EvidenceRole
        title={t(($) => $.common.worldFocus.presentation.evidenceHistory.evidence)}
        bindings={evidenceBindings}
      />
      <EvidenceRole
        title={t(($) => $.common.worldFocus.presentation.evidenceHistory.provenance)}
        bindings={provenanceBindings}
      />
      <EvidenceRole
        title={t(($) => $.common.worldFocus.presentation.evidenceHistory.integrity)}
        bindings={integrityBindings}
      />
      <EvidenceRole
        title={t(($) => $.common.worldFocus.presentation.evidenceHistory.history)}
        bindings={historyBindings}
      />
    </WorldFocusPresentationSection>
  );
}
