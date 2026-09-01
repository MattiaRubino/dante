import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

function WorkspaceHarness() {
  const workspace = useWorldFocusWorkspace();

  return (
    <div>
      <output data-testid="generation">{workspace.state.generation}</output>
      <output data-testid="surface-count">
        {workspace.state.surfaces.length}
      </output>
      <output data-testid="selection">
        {workspace.state.selection?.key ?? 'none'}
      </output>
      <button
        type="button"
        onClick={() =>
          workspace.selectContext({ kind: 'projection', key: 'continuity:a' })
        }
      >
        Select
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: 'insight:a',
            kind: 'insight',
            depth: 'insight',
            presentation: 'sidecar',
            origin: 'dante',
            expectedGeneration: workspace.state.generation,
          })
        }
      >
        Open
      </button>
      <button type="button" onClick={() => workspace.requestEscape()}>
        Escape
      </button>
    </div>
  );
}

afterEach(() => cleanup());

describe('WorldFocusWorkspaceHost', () => {
  it('keeps transient selection and surfaces local to the mounted World workspace', () => {
    render(
      <WorldFocusWorkspaceHost worldId="music">
        <WorkspaceHarness />
      </WorldFocusWorkspaceHost>,
    );

    expect(screen.getByTestId('generation').textContent).toBe('0');
    expect(screen.getByTestId('selection').textContent).toBe('none');

    fireEvent.click(screen.getByRole('button', { name: 'Select' }));
    expect(screen.getByTestId('generation').textContent).toBe('1');
    expect(screen.getByTestId('selection').textContent).toBe('continuity:a');

    fireEvent.click(screen.getByRole('button', { name: 'Open' }));
    expect(screen.getByTestId('surface-count').textContent).toBe('1');

    fireEvent.click(screen.getByRole('button', { name: 'Escape' }));
    expect(screen.getByTestId('surface-count').textContent).toBe('0');
    expect(screen.getByTestId('selection').textContent).toBe('continuity:a');
  });

  it('fails fast when workspace hooks escape their owner', () => {
    function InvalidHarness() {
      useWorldFocusWorkspace();
      return null;
    }

    expect(() => render(<InvalidHarness />)).toThrowError(
      'useWorldFocusWorkspace must be used inside WorldFocusWorkspaceHost',
    );
  });
});
