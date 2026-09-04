import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import type { ComponentProps } from 'react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import {
  applyWorldFocusCompositionDraft,
} from '../application/world-focus-composition-customization';
import type { WorldFocusCompositionCustomizationReader } from '../application/world-focus-composition-customization-read';
import {
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
} from '../application/world-focus-composition-opportunities';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import {
  WorldFocusCompositionCustomizationProvider,
  WorldFocusCompositionCustomizeInvoke,
} from './world-focus-composition-customization-context';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import { WorldFocusPage } from './world-focus-page';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspace } from './world-focus-workspace';
import { WorldFocusWorkspaceHost } from './world-focus-workspace-host';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function requireWorld() {
  const world = getWorldFocusWorld('music');
  if (world === undefined) {
    throw new Error('Missing World Focus music fixture');
  }
  return world;
}

function renderMusicWorld() {
  const onClose = vi.fn();
  const view = render(
    <WorldFocusPage
      world={requireWorld()}
      identity={createWorldFocusIdentityDescriptor({
        id: 'music',
        label: 'Musica',
        description: 'Il tuo mondo musicale',
      })}
      source="worlds"
      onClose={onClose}
    />,
  );
  return { ...view, onClose };
}

type CustomizationOverrides = Pick<
  ComponentProps<typeof WorldFocusCompositionCustomizationProvider>,
  'reader' | 'applyDraft'
>;

function deterministicReader(): WorldFocusCompositionCustomizationReader {
  return (worldId) =>
    Promise.resolve(
      createWorldFocusCompositionOpportunitySet({
        worldId,
        opportunities: [
          createWorldFocusCompositionOpportunity({
            instanceId: 'situation',
            kind: 'situation',
            defaultProminence: 'primary',
            footprint: 'standard',
          }),
          createWorldFocusCompositionOpportunity({
            instanceId: 'comparison:manual',
            kind: 'comparison',
            defaultProminence: 'supporting',
            footprint: 'standard',
          }),
        ],
      }),
    );
}

function emptyReader(): WorldFocusCompositionCustomizationReader {
  return (worldId) =>
    Promise.resolve(
      createWorldFocusCompositionOpportunitySet({
        worldId,
        opportunities: [],
      }),
    );
}

function renderCustomizationHarness(overrides: CustomizationOverrides = {}) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <WorldFocusCompositionCustomizationProvider
        worldId="music"
        worldLabel="Musica"
        reader={overrides.reader ?? deterministicReader()}
        applyDraft={overrides.applyDraft ?? applyWorldFocusCompositionDraft}
      >
        <WorldFocusWorkspace
          worldLabel="Musica"
          status="ready"
          surfaces={
            <>
              <WorldFocusCompositionCustomizeInvoke />
              <WorldFocusSurfaceLayer registry={getCoreWorldFocusSurfaceRegistry()} />
            </>
          }
        />
      </WorldFocusCompositionCustomizationProvider>
    </WorldFocusWorkspaceHost>,
  );
}

function openCustomization() {
  fireEvent.click(
    screen.getByRole('button', { name: 'Personalizza composizione' }),
  );
}

describe('World Focus M3-3 manual composition customization', () => {
  it('keeps View mode distinct from Customize mode until explicit invocation', () => {
    const { container } = renderMusicWorld();

    expect(
      screen.getByRole('button', { name: 'Personalizza composizione' }),
    ).toBeTruthy();
    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(
      container.querySelector('[data-world-focus-composition-count]')?.getAttribute(
        'data-world-focus-composition-count',
      ),
    ).toBe('1');
  });

  it('opens an isolated non-modal Customize surface without changing the accepted View composition', () => {
    const { container } = renderMusicWorld();

    openCustomization();

    const dialog = screen.getByRole('dialog', { name: 'Personalizza Musica' });
    expect(dialog).toBeTruthy();
    expect(dialog.getAttribute('aria-modal')).toBe('false');
    expect(
      container.querySelector('[data-world-focus-composition-count]')?.getAttribute(
        'data-world-focus-composition-count',
      ),
    ).toBe('1');
  });

  it('exposes explicit Apply and Cancel terminals only after Customize begins', () => {
    renderMusicWorld();

    expect(screen.queryByRole('button', { name: 'Applica' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Annulla' })).toBeNull();

    openCustomization();

    expect(screen.getByRole('button', { name: 'Applica' })).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Annulla' })).toBeTruthy();
  });

  it('Cancel closes the draft surface, leaves the World open, and restores focus to the exact invoker', () => {
    const { onClose } = renderMusicWorld();
    const customize = screen.getByRole('button', {
      name: 'Personalizza composizione',
    });

    customize.focus();
    fireEvent.click(customize);
    expect(
      screen.getByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));

    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(document.activeElement).toBe(customize);
    expect(onClose).not.toHaveBeenCalled();
  });

  it('Escape closes Customize before the World and restores focus to the invoker', () => {
    const { onClose } = renderMusicWorld();
    const customize = screen.getByRole('button', {
      name: 'Personalizza composizione',
    });

    customize.focus();
    fireEvent.click(customize);
    fireEvent.keyDown(document, { key: 'Escape' });

    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(document.activeElement).toBe(customize);
    expect(onClose).not.toHaveBeenCalled();
  });

  it('routes adopt, pin, hide, promote and restore through the canonical draft without inventing live composition', async () => {
    const { container } = renderCustomizationHarness();
    openCustomization();

    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );

    const entrySelector = '[data-world-focus-customization-entry="situation"]';
    const entry = container.querySelector(entrySelector);
    expect(entry).toBeTruthy();
    if (!(entry instanceof HTMLElement)) {
      throw new Error('Expected adopted Situation customization entry');
    }

    expect(screen.getByRole('dialog', { name: 'Personalizza Musica' }).getAttribute(
      'data-world-focus-customization-dirty',
    )).toBe('true');
    expect(within(entry).queryByText('Fissato')).toBeNull();
    expect(within(entry).queryByText('Nascosto')).toBeNull();
    expect(within(entry).queryByText('In evidenza')).toBeNull();

    fireEvent.click(within(entry).getByRole('button', { name: 'Fissa' }));
    expect(within(entry).getByText('Fissato')).toBeTruthy();

    fireEvent.click(within(entry).getByRole('button', { name: 'Sblocca' }));
    expect(within(entry).queryByText('Fissato')).toBeNull();

    fireEvent.click(within(entry).getByRole('button', { name: 'Nascondi' }));
    expect(within(entry).getByText('Nascosto')).toBeTruthy();

    fireEvent.click(within(entry).getByRole('button', { name: 'Mostra' }));
    expect(within(entry).queryByText('Nascosto')).toBeNull();

    fireEvent.click(
      within(entry).getByRole('button', { name: 'Metti in evidenza' }),
    );
    expect(within(entry).getByText('In evidenza')).toBeTruthy();

    fireEvent.click(within(entry).getByRole('button', { name: 'Ripristina' }));
    expect(container.querySelector(entrySelector)).toBeNull();
  });

  it('provides deterministic keyboard reorder, keeps focus on the moved item, and announces its position', async () => {
    const { container } = renderCustomizationHarness();
    openCustomization();

    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Confronto' }),
    );

    const situationSelector =
      '[data-world-focus-customization-entry="situation"]';
    const situation = container.querySelector(situationSelector);
    expect(situation).toBeTruthy();
    if (!(situation instanceof HTMLElement)) {
      throw new Error('Expected Situation customization entry');
    }

    fireEvent.click(within(situation).getByRole('button', { name: 'Sposta giù' }));

    const entries = Array.from(
      container.querySelectorAll('[data-world-focus-customization-entry]'),
    );
    expect(
      entries.map((entry) => entry.getAttribute('data-world-focus-customization-entry')),
    ).toEqual(['comparison:manual', 'situation']);

    await waitFor(() => {
      expect(document.activeElement).toBe(container.querySelector(situationSelector));
    });
    expect(screen.getByText('Situazione, posizione 2 di 2')).toBeTruthy();
  });

  it('applies exactly once, advances the accepted revision once, and still leaves normal composition to M3-4', async () => {
    const applyDraft = vi.fn(applyWorldFocusCompositionDraft);
    renderCustomizationHarness({ applyDraft });
    openCustomization();

    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Applica' }));

    expect(applyDraft).toHaveBeenCalledTimes(1);
    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();

    openCustomization();
    const reopened = screen.getByRole('dialog', { name: 'Personalizza Musica' });
    expect(reopened.getAttribute('data-world-focus-customization-revision')).toBe('1');
    expect(
      reopened.querySelectorAll('[data-world-focus-customization-entry]'),
    ).toHaveLength(1);
  });

  it('surfaces revision conflicts without merging, rebasing or mutating the accepted config', async () => {
    const conflictApply: NonNullable<CustomizationOverrides['applyDraft']> = (
      current,
      draft,
    ) => ({
      status: 'revision-conflict',
      baseRevision: draft.baseRevision,
      currentRevision: current.revision + 1,
    });
    renderCustomizationHarness({ applyDraft: conflictApply });
    openCustomization();

    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Applica' }));

    const dialog = screen.getByRole('dialog', { name: 'Personalizza Musica' });
    expect(dialog.getAttribute('data-world-focus-customization-revision')).toBe('0');
    expect(
      screen.getByText(
        'La composizione è cambiata da quando hai iniziato. Le modifiche non sono state applicate.',
      ),
    ).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    openCustomization();
    expect(
      screen
        .getByRole('dialog', { name: 'Personalizza Musica' })
        .querySelectorAll('[data-world-focus-customization-entry]'),
    ).toHaveLength(0);
  });

  it('fails closed on an invalid apply state and preserves the review surface', async () => {
    const invalidApply: NonNullable<CustomizationOverrides['applyDraft']> = () => {
      throw new Error('invalid base snapshot');
    };
    renderCustomizationHarness({ applyDraft: invalidApply });
    openCustomization();

    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Applica' }));

    const dialog = screen.getByRole('dialog', { name: 'Personalizza Musica' });
    expect(dialog.getAttribute('data-world-focus-customization-revision')).toBe('0');
    expect(
      screen.getByText(
        'Questa bozza non è più valida. Nessuna modifica è stata applicata.',
      ),
    ).toBeTruthy();
  });

  it('keeps a sparse World sparse instead of manufacturing customization rows', async () => {
    renderCustomizationHarness({ reader: emptyReader() });
    openCustomization();

    expect(
      await screen.findByText(
        'Nessun altro elemento significativo è disponibile adesso.',
      ),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: /^Aggiungi / })).toBeNull();
    expect(
      screen
        .getByRole('dialog', { name: 'Personalizza Musica' })
        .querySelectorAll('[data-world-focus-customization-entry]'),
    ).toHaveLength(0);
  });
});
