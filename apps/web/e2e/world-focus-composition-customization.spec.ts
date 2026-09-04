import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

const PRESSURE_WIDTHS = [
  1856, 1600, 1366, 1200, 1024, 901, 900, 760, 721, 720, 719, 390,
] as const;

test('M3-4 keeps customization explicit while accepted metadata governs the normal adaptive composition', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  const composition = page.locator('.world-focus-composition');
  const situation = page.locator(
    '[data-world-focus-composition-id="situation"]',
  );
  const invoke = page.getByRole('button', { name: 'Personalizza composizione' });
  await expect(composition).toHaveAttribute('data-world-focus-composition-count', '4');
  await expect(situation).toHaveAttribute(
    'data-world-focus-origin',
    'application-derived',
  );
  await expect(page.getByRole('dialog', { name: 'Personalizza Musica' })).toHaveCount(0);

  await invoke.focus();
  await invoke.click();

  const dialog = page.getByRole('dialog', { name: 'Personalizza Musica' });
  const surface = page.locator(
    '[data-world-focus-surface-id="composition:customize"]',
  );
  const workspace = page.locator('[data-world-focus-region="workspace"]');

  await expect(dialog).toBeVisible();
  await expect(dialog).toHaveAttribute('aria-modal', 'false');
  await expect(dialog).toBeFocused();
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(surface).toHaveAttribute('data-world-focus-surface-slot', 'sidecar');
  await expect(workspace).toHaveAttribute('data-world-focus-main-allocation', 'split');
  await expect(workspace).toHaveAttribute(
    'data-world-focus-main-interaction',
    'interactive',
  );
  await expect(dialog).toHaveAttribute('data-world-focus-customization-revision', '0');
  await expect(composition).toHaveAttribute('data-world-focus-composition-count', '4');

  const add = page.getByRole('button', { name: /^Aggiungi / }).first();
  await expect(add).toBeVisible();
  await add.click();

  await expect(dialog).toHaveAttribute('data-world-focus-customization-dirty', 'true');
  await expect(page.getByRole('button', { name: 'Applica' })).toBeEnabled();
  await page.getByRole('button', { name: 'Applica' }).click();

  await expect(dialog).toHaveCount(0);
  await expect(invoke).toBeFocused();
  await expect(composition).toHaveAttribute('data-world-focus-composition-count', '4');
  await expect(situation).toHaveAttribute('data-world-focus-origin', 'user');

  await invoke.click();
  const reopened = page.getByRole('dialog', { name: 'Personalizza Musica' });
  await expect(reopened).toHaveAttribute('data-world-focus-customization-revision', '1');
  await expect(
    reopened.locator('[data-world-focus-customization-entry]'),
  ).toHaveCount(1);
  await page.getByRole('button', { name: 'Annulla' }).click();
  await expect(invoke).toBeFocused();
});

test('M3-3 Cancel and Escape discard only the draft and keep the World route open', async ({
  page,
}) => {
  await page.goto('/worlds/music');
  const invoke = page.getByRole('button', { name: 'Personalizza composizione' });

  await invoke.click();
  const add = page.getByRole('button', { name: /^Aggiungi / }).first();
  await expect(add).toBeVisible();
  await add.click();
  await page.getByRole('button', { name: 'Annulla' }).click();

  await expect(page).toHaveURL(/\/worlds\/music$/);
  await expect(invoke).toBeFocused();

  await invoke.click();
  await expect(
    page.locator('[data-world-focus-customization-entry]'),
  ).toHaveCount(0);
  await page.keyboard.press('Escape');

  await expect(page.getByRole('dialog', { name: 'Personalizza Musica' })).toHaveCount(0);
  await expect(page).toHaveURL(/\/worlds\/music$/);
  await expect(invoke).toBeFocused();
});

test('M3-3 keeps its existing sidecar-to-overlay fallback usable across all contracted widths', async ({
  page,
}) => {
  for (const width of PRESSURE_WIDTHS) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/worlds/music');
    await page.getByRole('button', { name: 'Personalizza composizione' }).click();

    const workspace = page.locator('[data-world-focus-region="workspace"]');
    const dialog = page.getByRole('dialog', { name: 'Personalizza Musica' });
    const surface = page.locator(
      '[data-world-focus-surface-id="composition:customize"]',
    );
    await expect(dialog).toBeVisible();
    await expect(workspace).toHaveAttribute(
      'data-world-focus-main-interaction',
      'interactive',
    );

    const workspaceBox = await workspace.boundingBox();
    const dialogBox = await dialog.boundingBox();
    expect(workspaceBox).not.toBeNull();
    expect(dialogBox).not.toBeNull();
    if (workspaceBox === null || dialogBox === null) {
      throw new Error(`Missing M3-3 customization geometry at ${width}px`);
    }

    expect(dialogBox.x).toBeGreaterThanOrEqual(workspaceBox.x - 1);
    expect(dialogBox.x + dialogBox.width).toBeLessThanOrEqual(
      workspaceBox.x + workspaceBox.width + 1,
    );
    expect(dialogBox.y).toBeGreaterThanOrEqual(workspaceBox.y - 1);
    expect(dialogBox.y + dialogBox.height).toBeLessThanOrEqual(
      workspaceBox.y + workspaceBox.height + 1,
    );

    if (width === 390) {
      await expect(surface).toHaveAttribute('data-world-focus-surface-slot', 'overlay');
      const applyBox = await page.getByRole('button', { name: 'Applica' }).boundingBox();
      const cancelBox = await page.getByRole('button', { name: 'Annulla' }).boundingBox();
      expect(applyBox).not.toBeNull();
      expect(cancelBox).not.toBeNull();
      if (applyBox === null || cancelBox === null) {
        throw new Error('Expected compact M3-3 terminal actions');
      }
      expect(applyBox.height).toBeGreaterThanOrEqual(44);
      expect(cancelBox.height).toBeGreaterThanOrEqual(44);
    }

    const hasHorizontalOverflow = await page.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    );
    expect(hasHorizontalOverflow).toBe(false);
  }
});

test('M3-3 has no detectable axe violations at wide and compact allocations', async ({
  page,
}) => {
  for (const viewport of [
    { width: 1600, height: 900 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto('/worlds/music');
    await page.getByRole('button', { name: 'Personalizza composizione' }).click();
    await expect(page.getByRole('dialog', { name: 'Personalizza Musica' })).toBeVisible();

    const results = await new AxeBuilder({ page })
      .include('.world-focus-shell')
      .analyze();
    expect(results.violations).toEqual([]);
  }
});

test('M3-3 remains operable in forced colors', async ({ page }) => {
  await page.emulateMedia({ forcedColors: 'active' });
  await page.goto('/worlds/music');
  await page.getByRole('button', { name: 'Personalizza composizione' }).click();

  const dialog = page.getByRole('dialog', { name: 'Personalizza Musica' });
  await expect(dialog).toBeVisible();
  await expect(page.getByRole('button', { name: 'Annulla' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Applica' })).toBeVisible();
});
