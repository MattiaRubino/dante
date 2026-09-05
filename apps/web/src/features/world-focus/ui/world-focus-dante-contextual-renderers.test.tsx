import { type ReactNode } from 'react';
import { cleanup, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { createWorldFocusEvidenceHistoryProjection } from '../model/world-focus-direct-projections';
import { createWorldFocusEvidenceReferenceFacet } from '../model/world-focus-evidence';
import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
} from '../model/world-focus-work-primitives';
import { WorldFocusDanteEntryProvider } from './world-focus-dante-entry';
import { WorldFocusWorkspaceHost } from './world-focus-workspace-host';
import { WorldFocusAttention } from './presentation/world-focus-attention';
import { WorldFocusComparison } from './presentation/world-focus-comparison';
import {
  createWorldFocusDisplayBinding,
  createWorldFocusDisplayBindingSet,
} from './presentation/world-focus-display-bindings';
import { WorldFocusEvidenceHistory } from './presentation/world-focus-evidence-history';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function D4RendererHarness({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <WorldFocusWorkspaceHost worldId="music">
      <WorldFocusDanteEntryProvider
        worldId="music"
        worldLabel="Musica"
        availability={{ status: 'available' }}
      >
        {children}
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceHost>
  );
}

describe('World Focus D4 contextual renderer entries', () => {
  it('materializes finite Attention and Comparison intents without exposing semantic coordinates', () => {
    const attention = createWorldFocusAttentionPrimitive({
      instanceId: 'attention-1',
      matterReference: { kind: 'invoice', key: 'invoice-internal-42' },
      reasonCode: 'deadline-risk-internal',
      resolutionReference: { kind: 'request', key: 'request-internal-7' },
      state: 'blocked',
    });
    const comparison = createWorldFocusComparisonPrimitive(
      {
        instanceId: 'comparison-1',
        mode: 'planned-actual',
        subjectReferences: [
          { kind: 'plan', key: 'planned-internal' },
          { kind: 'actual', key: 'actual-internal' },
        ],
        basisReference: { kind: 'period', key: 'period-internal' },
      },
      { maxSubjectReferences: 4 },
    );

    render(
      <D4RendererHarness>
        <WorldFocusAttention
          primitive={attention}
          matter={createWorldFocusDisplayBinding({
            reference: attention.matterReference,
            label: 'Pagamento fornitore',
          })}
          resolution={createWorldFocusDisplayBinding({
            reference: attention.resolutionReference!,
            label: 'Richiesta di chiarimento',
          })}
          reasonText="Serve una risposta prima della scadenza."
        />
        <WorldFocusComparison
          primitive={comparison}
          subjects={comparison.subjectReferences.map((reference, index) =>
            createWorldFocusDisplayBinding({
              reference,
              label: index === 0 ? 'Pianificato' : 'Reale',
            }),
          )}
          basis={createWorldFocusDisplayBinding({
            reference: comparison.basisReference!,
            label: 'Questa settimana',
          })}
        />
      </D4RendererHarness>,
    );

    expect(
      screen.getByRole('button', { name: 'Chiedi a DANTE: Perché?' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Chiedi a DANTE: Confronta' }),
    ).toBeTruthy();
    expect(screen.queryByText('invoice-internal-42')).toBeNull();
    expect(screen.queryByText('planned-internal')).toBeNull();
    expect(screen.queryByText('deadline-risk-internal')).toBeNull();
  });

  it('offers source opening only for Evidence and never collapses Provenance, Integrity or History into Evidence', () => {
    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [{ kind: 'observation', key: 'internal-evidence' }],
        provenanceReferences: [{ kind: 'provenance', key: 'internal-provenance' }],
        integrityAttestationReferences: [
          { kind: 'attestation', key: 'internal-attestation' },
        ],
      },
      {
        maxEvidenceReferences: 4,
        maxProvenanceReferences: 4,
        maxIntegrityAttestationReferences: 4,
      },
    );
    const projection = createWorldFocusEvidenceHistoryProjection({
      worldId: 'music',
      evidence,
      orderedHistoryReferences: [
        { kind: 'material-state', key: 'internal-history-1' },
      ],
    });
    const bindings = createWorldFocusDisplayBindingSet([
      { reference: evidence.evidenceReferences[0]!, label: 'Revisione mix' },
      { reference: evidence.provenanceReferences[0]!, label: 'Import studio' },
      {
        reference: evidence.integrityAttestationReferences[0]!,
        label: 'Verifica integrità',
      },
      {
        reference: projection.orderedHistoryReferences[0]!,
        label: 'Master v1',
      },
    ]);

    render(
      <D4RendererHarness>
        <WorldFocusEvidenceHistory projection={projection} bindings={bindings} />
      </D4RendererHarness>,
    );

    expect(
      within(screen.getByRole('group', { name: 'Evidenze' })).getByRole(
        'button',
        { name: 'Chiedi a DANTE: Apri fonte' },
      ),
    ).toBeTruthy();
    expect(
      within(screen.getByRole('group', { name: 'Provenienza' })).queryByRole(
        'button',
      ),
    ).toBeNull();
    expect(
      within(screen.getByRole('group', { name: 'Integrità' })).queryByRole(
        'button',
      ),
    ).toBeNull();
    expect(
      within(screen.getByRole('group', { name: 'Cronologia' })).queryByRole(
        'button',
      ),
    ).toBeNull();
  });
});
