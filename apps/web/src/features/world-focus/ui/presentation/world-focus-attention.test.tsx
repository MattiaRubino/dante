import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { createWorldFocusAttentionPrimitive } from '../../model/world-focus-work-primitives';
import { createWorldFocusDisplayBinding } from './world-focus-display-bindings';
import { WorldFocusAttention } from './world-focus-attention';

afterEach(cleanup);

describe('World Focus M2 Attention renderer', () => {
  const primitive = createWorldFocusAttentionPrimitive({
    instanceId: 'attention-1',
    matterReference: { kind: 'invoice', key: 'invoice-internal-42' },
    reasonCode: 'deadline-risk-internal',
    resolutionReference: { kind: 'request', key: 'request-internal-7' },
    state: 'blocked',
  });

  it('renders display-safe matter/reason/state without leaking internal references or reasonCode', () => {
    render(
      <WorldFocusAttention
        primitive={primitive}
        matter={createWorldFocusDisplayBinding({
          reference: primitive.matterReference,
          label: 'Pagamento fornitore',
        })}
        resolution={createWorldFocusDisplayBinding({
          reference: primitive.resolutionReference!,
          label: 'Richiesta di chiarimento',
        })}
        reasonText="Serve una risposta prima della scadenza."
      />,
    );

    expect(screen.getByText('Pagamento fornitore')).toBeTruthy();
    expect(screen.getByText('Serve una risposta prima della scadenza.')).toBeTruthy();
    expect(screen.getByText('Bloccato')).toBeTruthy();
    expect(screen.queryByText('invoice-internal-42')).toBeNull();
    expect(screen.queryByText('deadline-risk-internal')).toBeNull();
  });

  it('fails closed when a display binding does not match the semantic reference', () => {
    expect(() =>
      render(
        <WorldFocusAttention
          primitive={primitive}
          matter={createWorldFocusDisplayBinding({
            reference: { kind: 'invoice', key: 'different' },
            label: 'Wrong matter',
          })}
          resolution={null}
          reasonText="Serve una risposta."
        />,
      ),
    ).toThrow(/binding/i);
  });
});
