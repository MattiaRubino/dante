import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import {
  createWorldFocusCoverageFacet,
  createWorldFocusFreshnessFacet,
  createWorldFocusMaterialPayloadFacet,
  createWorldFocusValidityFacet,
} from '../../model/world-focus-basis';
import { WorldFocusBasisPresentation } from './world-focus-basis-presentation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('World Focus M2 basis presentation', () => {
  it('keeps freshness, validity, coverage and material retirement visually distinct without leaking reasonCode', () => {
    render(
      <WorldFocusBasisPresentation
        freshness={createWorldFocusFreshnessFacet({
          status: 'stale',
          asOf: '2026-09-01T12:00:00Z',
        })}
        validity={createWorldFocusValidityFacet({
          status: 'retracted',
          reasonCode: 'internal-retraction-code',
        })}
        coverage={createWorldFocusCoverageFacet({
          status: 'incomplete',
          reasonCode: 'internal-coverage-code',
        })}
        materialPayload={createWorldFocusMaterialPayloadFacet({
          status: 'retired',
          materialStateReference: {
            kind: 'material-state',
            key: 'internal-material-state',
          },
          reasonCode: 'internal-retirement-code',
          retiredAt: '2026-09-02T12:00:00Z',
        })}
      />,
    );

    expect(screen.getByText('Non aggiornato')).toBeTruthy();
    expect(screen.getByText('Ritirato')).toBeTruthy();
    expect(screen.getByText('Incompleto')).toBeTruthy();
    expect(screen.getByText('Contenuto ritirato')).toBeTruthy();
    expect(screen.queryByText('internal-retraction-code')).toBeNull();
    expect(screen.queryByText('internal-coverage-code')).toBeNull();
    expect(screen.queryByText('internal-retirement-code')).toBeNull();
    expect(screen.queryByText('internal-material-state')).toBeNull();
  });

  it('stays quiet when every presented basis axis is nominal', () => {
    const { container } = render(
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
            key: 'internal-current-material',
          },
        })}
      />,
    );

    expect(
      container.querySelector('[data-world-focus-basis-presentation]'),
    ).toBeNull();
  });
});
