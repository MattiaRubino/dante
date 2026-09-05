import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type { WorldFocusFeatureAvailability } from '../model/world-focus-platform';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import {
  WorldFocusDanteEntryProvider,
  WorldFocusDanteInvoke,
} from './world-focus-dante-entry';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const AVAILABLE: WorldFocusFeatureAvailability = Object.freeze({
  status: 'available',
});
const UNAVAILABLE: WorldFocusFeatureAvailability = Object.freeze({
  status: 'unavailable',
  reasonCode: 'pre_backend_unavailable',
  retryable: false,
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function DanteHarness({
  availability = AVAILABLE,
}: Readonly<{
  availability?: WorldFocusFeatureAvailability;
}>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, 1280);
  const activeSurface = workspace.state.surfaces.at(-1) ?? null;

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusDanteEntryProvider
        worldId="music"
        worldLabel="Musica"
        availability={availability}
      >
        <div data-testid="world-content">
          World content remains independently usable
        </div>
        <button
          type="button"
          data-testid="select-context"
          onClick={() =>
            workspace.selectContext({ kind: 'artifact', key: 'selected:1' })
          }
        >
          Select context
        </button>
        <output data-testid="surface-count">
          {workspace.state.surfaces.length}
        </output>
        <output data-testid="context-reference">
          {activeSurface === null
            ? 'none'
            : activeSurface.contextReference === null
              ? 'null'
              : 'bound'}
        </output>
        <WorldFocusDanteInvoke />
        <WorldFocusSurfaceLayer registry={getCoreWorldFocusSurfaceRegistry()} />
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderDanteEntry(
  availability: WorldFocusFeatureAvailability = AVAILABLE,
) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <DanteHarness availability={availability} />
    </WorldFocusWorkspaceHost>,
  );
}

describe('World Focus D1 contextual DANTE entry', () => {
  it('starts quiet, opens one non-modal composer and binds no implicit selected context', () => {
    const { container } = renderDanteEntry();

    const invoke = screen.getByRole('button', {
      name: 'Apri DANTE per il Mondo Musica',
    });
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(screen.getByTestId('surface-count').textContent).toBe('0');

    fireEvent.click(screen.getByTestId('select-context'));
    fireEvent.click(invoke);

    const dialog = screen.getByRole('dialog', { name: 'DANTE' });
    const textarea = screen.getByRole('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });
    const wrapper = container.querySelector(
      '[data-world-focus-surface-id="dante:composer"]',
    );

    expect(dialog.getAttribute('aria-modal')).toBe('false');
    expect(textarea).toBe(document.activeElement);
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
    expect(screen.getByTestId('context-reference').textContent).toBe('null');
    expect(wrapper?.getAttribute('data-world-focus-surface-presentation')).toBe(
      'popover',
    );
    expect(wrapper?.getAttribute('data-world-focus-surface-interaction')).toBe(
      'interactive',
    );
    expect((wrapper as HTMLElement | null)?.style.pointerEvents).toBe('none');
    expect(screen.getByTestId('world-content')).toBeTruthy();
    expect(invoke.getAttribute('disabled')).not.toBeNull();
  });

  it('preserves the draft and reports a truthful unavailable submit without inventing an answer', () => {
    renderDanteEntry();

    fireEvent.click(
      screen.getByRole('button', { name: 'Apri DANTE per il Mondo Musica' }),
    );
    const textarea = screen.getByRole('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });

    fireEvent.change(textarea, {
      target: { value: 'Perché questo progetto è in pausa?' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    expect((textarea as HTMLTextAreaElement).value).toBe(
      'Perché questo progetto è in pausa?',
    );
    expect(
      screen.getByText(
        'DANTE non è disponibile al momento. La richiesta è rimasta qui.',
      ),
    ).toBeTruthy();
    expect(screen.queryByText(/risposta di DANTE/i)).toBeNull();
    expect(textarea).toBe(document.activeElement);
  });

  it('renders a truthful unavailable entry state and focuses the close action', () => {
    renderDanteEntry(UNAVAILABLE);

    fireEvent.click(
      screen.getByRole('button', { name: 'Apri DANTE per il Mondo Musica' }),
    );

    const close = screen.getByRole('button', { name: 'Chiudi DANTE' });
    expect(screen.getByText('DANTE non è disponibile al momento.')).toBeTruthy();
    expect(
      screen.queryByRole('textbox', { name: 'Scrivi una richiesta per DANTE' }),
    ).toBeNull();
    expect(close).toBe(document.activeElement);
  });

  it('restores focus to the exact quiet invoke after explicit close', async () => {
    renderDanteEntry();

    const invoke = screen.getByRole('button', {
      name: 'Apri DANTE per il Mondo Musica',
    });
    invoke.focus();
    fireEvent.click(invoke);
    expect(
      screen.getByRole('textbox', { name: 'Scrivi una richiesta per DANTE' }),
    ).toBe(document.activeElement);

    fireEvent.click(screen.getByRole('button', { name: 'Chiudi DANTE' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).toBeNull();
      expect(invoke).toBe(document.activeElement);
    });
  });
});
