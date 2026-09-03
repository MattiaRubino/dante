import { cleanup, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { createWorldFocusEvidenceHistoryProjection } from '../../model/world-focus-direct-projections';
import { createWorldFocusEvidenceReferenceFacet } from '../../model/world-focus-evidence';
import { createWorldFocusDisplayBindingSet } from './world-focus-display-bindings';
import { WorldFocusEvidenceHistory } from './world-focus-evidence-history';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 Evidence/History renderer', () => {
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
    worldId: 'future-world',
    evidence,
    orderedHistoryReferences: [
      { kind: 'material-state', key: 'internal-history-1' },
      { kind: 'material-state', key: 'internal-history-2' },
    ],
  });

  it('keeps evidence, provenance, integrity and ordered history as separate roles', () => {
    const bindings = createWorldFocusDisplayBindingSet([
      { reference: evidence.evidenceReferences[0]!, label: 'Revisione mix' },
      { reference: evidence.provenanceReferences[0]!, label: 'Import studio' },
      {
        reference: evidence.integrityAttestationReferences[0]!,
        label: 'Verifica integrità',
      },
      {
        reference: projection.orderedHistoryReferences[1]!,
        label: 'Master v2',
      },
      {
        reference: projection.orderedHistoryReferences[0]!,
        label: 'Master v1',
      },
    ]);

    render(
      <WorldFocusEvidenceHistory projection={projection} bindings={bindings} />,
    );

    expect(within(screen.getByRole('group', { name: 'Evidenze' })).getByText('Revisione mix')).toBeTruthy();
    expect(within(screen.getByRole('group', { name: 'Provenienza' })).getByText('Import studio')).toBeTruthy();
    expect(within(screen.getByRole('group', { name: 'Integrità' })).getByText('Verifica integrità')).toBeTruthy();
    expect(
      within(screen.getByRole('group', { name: 'Cronologia' }))
        .getAllByRole('listitem')
        .map((item) => item.textContent),
    ).toEqual(['Master v1', 'Master v2']);
    expect(screen.queryByText('internal-evidence')).toBeNull();
  });

  it('fails closed when any evidence/history role is missing a display binding', () => {
    expect(() =>
      render(
        <WorldFocusEvidenceHistory
          projection={projection}
          bindings={createWorldFocusDisplayBindingSet([
            {
              reference: evidence.evidenceReferences[0]!,
              label: 'Solo evidenza',
            },
          ])}
        />,
      ),
    ).toThrow(/binding/i);
  });
});
