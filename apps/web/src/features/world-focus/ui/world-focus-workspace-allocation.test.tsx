import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
} from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';
import { WorldFocusWorkspace } from './world-focus-workspace';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

let observedInlineSize = 1280;
let resizeCallback: ResizeObserverCallback | null = null;

class TestResizeObserver implements ResizeObserver {
  constructor(callback: ResizeObserverCallback) {
    resizeCallback = callback;
  }

  disconnect() {}
  observe() {}
  unobserve() {}
}

const TEST_SURFACE_REGISTRY = new WorldFocusSurfaceRegistry<
  WorldFocusSurfaceRegistration
>([
  {
    kind: 'test-surface',
    render: ({ surface, onRequestClose }) => (
      <section data-testid={`surface-${surface.instanceId}`}>
        <span>{surface.presentation}</span>
        <button type="button" onClick={onRequestClose}>
          Close {surface.instanceId}
        </button>
      </section>
    ),
  },
]);

const TEST_RESIZE_OBSERVER: ResizeObserver = {
  disconnect() {},
  observe() {},
  unobserve() {},
};

function WorkspaceControls() {
  const workspace = useWorldFocusWorkspace();

  return (
    <div>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: 'dante:sidecar',
            kind: 'test-surface',
            depth: 'insight',
            presentation: 'sidecar',
            origin: 'user',
          })
        }
      >
        Open sidecar
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: 'confirm:modal',
            kind: 'test-surface',
            depth: 'insight',
            presentation: 'modal',
            origin: 'application',
          })
        }
      >
        Open modal
      </button>
    </div>
  );
}

function renderWorkspace() {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <WorldFocusWorkspace
        worldLabel="Musica"
        status="ready"
        context={<div>Orientation</div>}
        surfaces={<WorldFocusSurfaceLayer registry={TEST_SURFACE_REGISTRY} />}
      >
        <WorkspaceControls />
      </WorldFocusWorkspace>
    </WorldFocusWorkspaceHost>,
  );
}

function triggerResize(inlineSize: number) {
  observedInlineSize = inlineSize;
  const callback = resizeCallback;
  if (callback === null) {
    throw new Error('Expected World Focus ResizeObserver callback');
  }

  const entry: ResizeObserverEntry = {
    target: document.body,
    contentRect: document.body.getBoundingClientRect(),
    borderBoxSize: [],
    contentBoxSize: [],
    devicePixelContentBoxSize: [],
  };

  act(() => {
    callback([entry], TEST_RESIZE_OBSERVER);
  });
}

beforeEach(() => {
  observedInlineSize = 1280;
  resizeCallback = null;
  vi.stubGlobal('ResizeObserver', TestResizeObserver);
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(
    () => ({
      width: observedInlineSize,
      height: 720,
      x: 0,
      y: 0,
      top: 0,
      right: observedInlineSize,
      bottom: 720,
      left: 0,
      toJSON: () => ({}),
    }),
  );
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('WorldFocusWorkspace allocation integration', () => {
  it('allocates a wide sidecar without blocking the main plane', () => {
    const { container } = renderWorkspace();

    fireEvent.click(screen.getByRole('button', { name: 'Open sidecar' }));

    const workspace = container.querySelector('.world-focus-workspace');
    const mainPlane = container.querySelector('.world-focus-main-plane');
    const surface = screen.getByTestId('surface-dante:sidecar').parentElement;

    expect(workspace?.getAttribute('data-world-focus-main-allocation')).toBe(
      'split',
    );
    expect(workspace?.getAttribute('data-world-focus-top-layer')).toBe('none');
    expect(workspace?.getAttribute('data-world-focus-main-interaction')).toBe(
      'interactive',
    );
    expect(mainPlane?.hasAttribute('inert')).toBe(false);
    expect(surface?.getAttribute('data-world-focus-surface-slot')).toBe(
      'sidecar',
    );
    expect(surface?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'interactive',
    );
    expect(surface?.hasAttribute('inert')).toBe(false);
  });

  it('reallocates the same sidecar to a non-modal overlay when the measured workspace contracts', () => {
    const { container } = renderWorkspace();

    fireEvent.click(screen.getByRole('button', { name: 'Open sidecar' }));
    triggerResize(720);

    const workspace = container.querySelector('.world-focus-workspace');
    const mainPlane = container.querySelector('.world-focus-main-plane');
    const surface = screen.getByTestId('surface-dante:sidecar').parentElement;

    expect(workspace?.getAttribute('data-world-focus-main-allocation')).toBe(
      'full',
    );
    expect(workspace?.getAttribute('data-world-focus-top-layer')).toBe(
      'overlay',
    );
    expect(workspace?.getAttribute('data-world-focus-main-interaction')).toBe(
      'interactive',
    );
    expect(mainPlane?.hasAttribute('inert')).toBe(false);
    expect(surface?.getAttribute('data-world-focus-surface-slot')).toBe(
      'overlay',
    );
    expect(surface?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'interactive',
    );
    expect(surface?.hasAttribute('inert')).toBe(false);
  });

  it('keeps a wide sidecar allocated but inert underneath a modal while the modal remains interactive', () => {
    const { container } = renderWorkspace();

    fireEvent.click(screen.getByRole('button', { name: 'Open sidecar' }));
    fireEvent.click(screen.getByRole('button', { name: 'Open modal' }));

    const workspace = container.querySelector('.world-focus-workspace');
    const mainPlane = container.querySelector('.world-focus-main-plane');
    const sidecar = screen.getByTestId('surface-dante:sidecar').parentElement;
    const modal = screen.getByTestId('surface-confirm:modal').parentElement;

    expect(workspace?.getAttribute('data-world-focus-main-allocation')).toBe(
      'split',
    );
    expect(workspace?.getAttribute('data-world-focus-top-layer')).toBe(
      'overlay',
    );
    expect(workspace?.getAttribute('data-world-focus-main-interaction')).toBe(
      'inert',
    );
    expect(mainPlane?.hasAttribute('inert')).toBe(true);
    expect(sidecar?.getAttribute('data-world-focus-surface-slot')).toBe(
      'sidecar',
    );
    expect(sidecar?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'inert',
    );
    expect(sidecar?.hasAttribute('inert')).toBe(true);
    expect(modal?.getAttribute('data-world-focus-surface-slot')).toBe('overlay');
    expect(modal?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'interactive',
    );
    expect(modal?.hasAttribute('inert')).toBe(false);
  });

  it('keeps a narrow sidecar dormant while a newer modal owns the only overlay slot', () => {
    observedInlineSize = 720;
    const { container } = renderWorkspace();

    fireEvent.click(screen.getByRole('button', { name: 'Open sidecar' }));
    fireEvent.click(screen.getByRole('button', { name: 'Open modal' }));

    const workspace = container.querySelector('.world-focus-workspace');
    const mainPlane = container.querySelector('.world-focus-main-plane');
    const modal = screen.getByTestId('surface-confirm:modal').parentElement;

    expect(workspace?.getAttribute('data-world-focus-main-allocation')).toBe(
      'full',
    );
    expect(workspace?.getAttribute('data-world-focus-main-interaction')).toBe(
      'inert',
    );
    expect(mainPlane?.hasAttribute('inert')).toBe(true);
    expect(screen.queryByTestId('surface-dante:sidecar')).toBeNull();
    expect(modal?.getAttribute('data-world-focus-surface-slot')).toBe('overlay');
    expect(modal?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'interactive',
    );
  });
});
