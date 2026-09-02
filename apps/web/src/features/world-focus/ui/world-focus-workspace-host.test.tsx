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
      <output data-testid="world-id">{workspace.state.worldId}</output>
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
            expectedWorkspace: {
              worldId: workspace.state.worldId,
              generation: workspace.state.generation,
            },
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

    expect(screen.getByTestId('world-id').textContent).toBe('music');
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

  it('resets transient state synchronously when worldId changes even without an external React key', () => {
    const { rerender } = render(
      <WorldFocusWorkspaceHost worldId="music">
        <WorkspaceHarness />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Select' }));
    fireEvent.click(screen.getByRole('button', { name: 'Open' }));
    expect(screen.getByTestId('generation').textContent).toBe('1');
    expect(screen.getByTestId('surface-count').textContent).toBe('1');

    rerender(
      <WorldFocusWorkspaceHost worldId="travel">
        <WorkspaceHarness />
      </WorldFocusWorkspaceHost>,
    );

    expect(screen.getByTestId('world-id').textContent).toBe('travel');
    expect(screen.getByTestId('generation').textContent).toBe('0');
    expect(screen.getByTestId('selection').textContent).toBe('none');
    expect(screen.getByTestId('surface-count').textContent).toBe('0');
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
