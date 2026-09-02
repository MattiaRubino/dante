import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function AllocatedSurfaceLayer({
  registry,
}: Readonly<{
  registry: WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>;
}>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, 1280);

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusSurfaceLayer registry={registry} />
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function SurfaceHarness({
  registry,
}: Readonly<{
  registry: WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>;
}>) {
  const workspace = useWorldFocusWorkspace();

  return (
    <>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: 'insight:1',
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
        Open insight
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.selectContext({ kind: 'projection', key: 'next-context' })
        }
      >
        Change context
      </button>
      <AllocatedSurfaceLayer registry={registry} />
    </>
  );
}

function UnknownHarness({
  registry,
  presentation,
}: Readonly<{
  registry: WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>;
  presentation: 'sidecar' | 'popover';
}>) {
  const workspace = useWorldFocusWorkspace();

  return (
    <>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: `future:${presentation}`,
            kind: 'future-specialist',
            depth: presentation === 'popover' ? 'peek' : 'explore',
            presentation,
            origin: 'application',
          })
        }
      >
        Open future
      </button>
      <AllocatedSurfaceLayer registry={registry} />
    </>
  );
}

describe('WorldFocusSurfaceLayer', () => {
  it('renders only registered shipped surface kinds and keeps the initiating generation visible after context changes', () => {
    const registry = new WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>([
      {
        kind: 'insight',
        render: ({ isCurrentGeneration, onRequestClose }) => (
          <section>
            <p>{isCurrentGeneration ? 'Current insight' : 'Bound insight'}</p>
            <button type="button" onClick={onRequestClose}>
              Close insight
            </button>
          </section>
        ),
      },
    ]);

    const { container } = render(
      <WorldFocusWorkspaceHost worldId="music">
        <SurfaceHarness registry={registry} />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Open insight' }));
    expect(screen.getByText('Current insight')).toBeTruthy();
    expect(
      container
        .querySelector('[data-world-focus-surface-id="insight:1"]')
        ?.getAttribute('data-world-focus-surface-current'),
    ).toBe('true');

    fireEvent.click(screen.getByRole('button', { name: 'Change context' }));
    expect(screen.getByText('Bound insight')).toBeTruthy();
    expect(
      container
        .querySelector('[data-world-focus-surface-id="insight:1"]')
        ?.getAttribute('data-world-focus-surface-current'),
    ).toBe('false');

    fireEvent.click(screen.getByRole('button', { name: 'Close insight' }));
    expect(screen.queryByText('Bound insight')).toBeNull();
  });

  it('degrades an unregistered sidecar locally and lets a dismissible surface close', () => {
    const registry = new WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>(
      [],
    );

    render(
      <WorldFocusWorkspaceHost worldId="travel">
        <UnknownHarness registry={registry} presentation="sidecar" />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Open future' }));
    expect(screen.getByText('Questo contenuto non è disponibile.')).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Chiudi' }));
    expect(screen.queryByText('Questo contenuto non è disponibile.')).toBeNull();
  });

  it('keeps an unregistered popover pointer-transparent outside its close control', () => {
    const registry = new WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>(
      [],
    );

    const { container } = render(
      <WorldFocusWorkspaceHost worldId="finance">
        <UnknownHarness registry={registry} presentation="popover" />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Open future' }));

    const fallback = container.querySelector<HTMLElement>(
      '[data-world-focus-surface-id="future:popover"]',
    );
    const close = screen.getByRole('button', { name: 'Chiudi' });

    expect(fallback?.dataset.worldFocusSurfacePresentation).toBe('popover');
    expect(fallback?.style.pointerEvents).toBe('none');
    expect(close.style.pointerEvents).toBe('auto');

    fireEvent.click(close);
    expect(screen.queryByText('Questo contenuto non è disponibile.')).toBeNull();
  });
});
