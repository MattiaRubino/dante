import { cleanup, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import {
  createWorldFocusCoverageFacet,
  createWorldFocusFreshnessFacet,
  createWorldFocusMaterialPayloadFacet,
  createWorldFocusValidityFacet,
} from '../../model/world-focus-basis';
import { createWorldFocusDisclosureOutcome } from '../../model/world-focus-disclosure';
import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
} from '../../model/world-focus-direct-projections';
import { createWorldFocusEffectPresentation } from '../../model/world-focus-effect';
import { createWorldFocusEvidenceReferenceFacet } from '../../model/world-focus-evidence';
import { createWorldFocusSyncPresentation } from '../../model/world-focus-sync';
import { WorldFocusBasisPresentation } from './world-focus-basis-presentation';
import { WorldFocusDisclosurePresentation } from './world-focus-disclosure-presentation';
import {
  createWorldFocusDisplayBinding,
  createWorldFocusDisplayBindingSet,
} from './world-focus-display-bindings';
import { WorldFocusEffectStatus } from './world-focus-effect-presentation';
import { WorldFocusEvidenceHistory } from './world-focus-evidence-history';
import { WorldFocusNext } from './world-focus-next';
import { WorldFocusSituation } from './world-focus-situation';
import { WorldFocusSyncStatus } from './world-focus-sync-presentation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function expectQualifier(
  container: HTMLElement,
  axis: string,
  state: string,
): void {
  expect(
    container.querySelector(
      `[data-world-focus-qualifier-axis="${axis}"][data-world-focus-qualifier-state="${state}"]`,
    ),
  ).toBeTruthy();
}

describe('World Focus M2 final hostile falsification', () => {
  it('keeps all degraded truthfulness axes orthogonal under simultaneous pressure without leaking private metadata', () => {
    const { container } = render(
      <>
        <WorldFocusBasisPresentation
          freshness={createWorldFocusFreshnessFacet({
            status: 'stale',
            asOf: '2026-09-01T12:00:00Z',
          })}
          validity={createWorldFocusValidityFacet({
            status: 'retracted',
            reasonCode: 'private-validity-code',
          })}
          coverage={createWorldFocusCoverageFacet({
            status: 'conflicted',
            reasonCode: 'private-coverage-code',
          })}
          materialPayload={createWorldFocusMaterialPayloadFacet({
            status: 'retired',
            materialStateReference: {
              kind: 'material-state',
              key: 'private-material-state-ref',
            },
            reasonCode: 'private-retirement-code',
            retiredAt: '2026-09-02T12:00:00Z',
          })}
        />
        <WorldFocusDisclosurePresentation
          disclosure={createWorldFocusDisclosureOutcome({
            status: 'restricted',
            policy: 'private-policy',
            recipient: 'private-recipient',
          })}
        />
        <WorldFocusEffectStatus
          effect={createWorldFocusEffectPresentation({
            state: 'partial-real',
            executionRevalidation: 'required-before-execution',
            providerAck: true,
            receipt: 'private-receipt',
          })}
        />
        <WorldFocusSyncStatus
          sync={createWorldFocusSyncPresentation({
            connectivity: 'offline',
            replay: 'pending',
            providerDelivery: 'lagging',
            requestTiming: 'timed-out',
          })}
        />
      </>,
    );

    expectQualifier(container, 'freshness', 'stale');
    expectQualifier(container, 'validity', 'retracted');
    expectQualifier(container, 'coverage', 'conflicted');
    expectQualifier(container, 'material-payload', 'retired');
    expectQualifier(container, 'disclosure', 'restricted');
    expectQualifier(container, 'effect-state', 'partial-real');
    expectQualifier(
      container,
      'execution-revalidation',
      'required-before-execution',
    );
    expectQualifier(container, 'connectivity', 'offline');
    expectQualifier(container, 'replay', 'pending');
    expectQualifier(container, 'provider-delivery', 'lagging');
    expectQualifier(container, 'request-timing', 'timed-out');

    for (const privateValue of [
      'private-validity-code',
      'private-coverage-code',
      'private-material-state-ref',
      'private-retirement-code',
      'private-policy',
      'private-recipient',
      'private-receipt',
    ]) {
      expect(screen.queryByText(privateValue)).toBeNull();
    }
    expect(screen.queryByText(/fallit/i)).toBeNull();
  });

  it('rejects pathological display copy instead of accepting an unbounded presentation payload', () => {
    expect(() =>
      createWorldFocusDisplayBinding({
        reference: { kind: 'observation', key: 'bounded-label-check' },
        label: 'x'.repeat(100_000),
      }),
    ).toThrow(/label|length|long|bound/i);

    expect(() =>
      createWorldFocusDisplayBinding({
        reference: { kind: 'observation', key: 'bounded-supporting-check' },
        label: 'Valid label',
        supportingText: 'y'.repeat(100_000),
      }),
    ).toThrow(/supporting|length|long|bound/i);
  });

  it('renders a future World through O2, O5 and O8 with long display-safe copy while preserving semantic order and role separation', () => {
    const worldId = 'future-world-2042-not-in-fixture-catalog';
    const situation = createWorldFocusSituationProjection({
      worldId,
      orderedSituationReferences: [
        { kind: 'observation', key: 'private-situation-1' },
        { kind: 'material-state', key: 'private-situation-2' },
      ],
    });
    const next = createWorldFocusNextProjection({
      worldId,
      orderedNextReferences: [
        { kind: 'schedule', key: 'private-next-1' },
        { kind: 'dependency', key: 'private-next-2' },
      ],
    });
    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [{ kind: 'observation', key: 'private-evidence' }],
        provenanceReferences: [{ kind: 'provenance', key: 'private-provenance' }],
        integrityAttestationReferences: [
          { kind: 'attestation', key: 'private-integrity' },
        ],
      },
      {
        maxEvidenceReferences: 4,
        maxProvenanceReferences: 4,
        maxIntegrityAttestationReferences: 4,
      },
    );
    const evidenceHistory = createWorldFocusEvidenceHistoryProjection({
      worldId,
      evidence,
      orderedHistoryReferences: [
        { kind: 'material-state', key: 'private-history-1' },
        { kind: 'material-state', key: 'private-history-2' },
      ],
    });
    const longButUsableLabel = `Contesto futuro ${'molto-dettagliato-'.repeat(8)}`;

    const { container } = render(
      <>
        <WorldFocusSituation
          projection={situation}
          bindings={createWorldFocusDisplayBindingSet([
            {
              reference: situation.orderedSituationReferences[1]!,
              label: 'Seconda situazione',
            },
            {
              reference: situation.orderedSituationReferences[0]!,
              label: longButUsableLabel,
            },
          ])}
        />
        <WorldFocusNext
          projection={next}
          bindings={createWorldFocusDisplayBindingSet([
            {
              reference: next.orderedNextReferences[1]!,
              label: 'Secondo passo',
            },
            {
              reference: next.orderedNextReferences[0]!,
              label: 'Primo passo',
            },
          ])}
        />
        <WorldFocusEvidenceHistory
          projection={evidenceHistory}
          bindings={createWorldFocusDisplayBindingSet([
            { reference: evidence.evidenceReferences[0]!, label: 'Evidenza A' },
            {
              reference: evidence.provenanceReferences[0]!,
              label: 'Provenienza A',
            },
            {
              reference: evidence.integrityAttestationReferences[0]!,
              label: 'Integrità A',
            },
            {
              reference: evidenceHistory.orderedHistoryReferences[1]!,
              label: 'Cronologia 2',
            },
            {
              reference: evidenceHistory.orderedHistoryReferences[0]!,
              label: 'Cronologia 1',
            },
          ])}
        />
      </>,
    );

    const situationSection = container.querySelector(
      '[data-world-focus-direct-output="situation"]',
    );
    const nextSection = container.querySelector(
      '[data-world-focus-direct-output="next"]',
    );
    expect(situationSection).toBeTruthy();
    expect(nextSection).toBeTruthy();
    expect(
      within(situationSection as HTMLElement)
        .getAllByRole('listitem')
        .map((item) => item.textContent),
    ).toEqual([longButUsableLabel, 'Seconda situazione']);
    expect(
      within(nextSection as HTMLElement)
        .getAllByRole('listitem')
        .map((item) => item.textContent),
    ).toEqual(['Primo passo', 'Secondo passo']);

    expect(
      within(screen.getByRole('group', { name: 'Evidenze' })).getByText(
        'Evidenza A',
      ),
    ).toBeTruthy();
    expect(
      within(screen.getByRole('group', { name: 'Provenienza' })).getByText(
        'Provenienza A',
      ),
    ).toBeTruthy();
    expect(
      within(screen.getByRole('group', { name: 'Integrità' })).getByText(
        'Integrità A',
      ),
    ).toBeTruthy();
    expect(
      within(screen.getByRole('group', { name: 'Cronologia' }))
        .getAllByRole('listitem')
        .map((item) => item.textContent),
    ).toEqual(['Cronologia 1', 'Cronologia 2']);

    for (const privateKey of [
      'private-situation-1',
      'private-situation-2',
      'private-next-1',
      'private-next-2',
      'private-evidence',
      'private-provenance',
      'private-integrity',
      'private-history-1',
      'private-history-2',
    ]) {
      expect(container.textContent).not.toContain(privateKey);
    }
  });

  it('fails closed when a convincing display label is bound to the wrong semantic reference', () => {
    const projection = createWorldFocusSituationProjection({
      worldId: 'future-world-binding-pressure',
      orderedSituationReferences: [
        { kind: 'observation', key: 'authoritative-reference' },
      ],
    });

    expect(() =>
      render(
        <WorldFocusSituation
          projection={projection}
          bindings={createWorldFocusDisplayBindingSet([
            {
              reference: { kind: 'observation', key: 'lookalike-reference' },
              label: 'Identical convincing label',
            },
          ])}
        />,
      ),
    ).toThrow(/binding/i);
  });

  it('keeps combined nominal basis, disclosure and sync state visually quiet instead of manufacturing status density', () => {
    const { container } = render(
      <>
        <WorldFocusBasisPresentation
          freshness={createWorldFocusFreshnessFacet({
            status: 'current',
            asOf: '2026-09-03T12:00:00Z',
          })}
          validity={createWorldFocusValidityFacet({ status: 'current' })}
          coverage={createWorldFocusCoverageFacet({ status: 'complete' })}
          materialPayload={createWorldFocusMaterialPayloadFacet({
            status: 'present',
            materialStateReference: {
              kind: 'material-state',
              key: 'private-present-material',
            },
          })}
        />
        <WorldFocusDisclosurePresentation
          disclosure={createWorldFocusDisclosureOutcome({ status: 'available' })}
        />
        <WorldFocusSyncStatus
          sync={createWorldFocusSyncPresentation({
            connectivity: 'online',
            replay: 'idle',
            providerDelivery: 'nominal',
            requestTiming: 'within-window',
          })}
        />
      </>,
    );

    expect(container.querySelector('.world-focus-qualifier-group')).toBeNull();
    expect(container.textContent).not.toContain('private-present-material');
  });
});
