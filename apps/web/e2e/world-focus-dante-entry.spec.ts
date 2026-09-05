import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('D1 keeps DANTE quiet until invoked, preserves the World, and restores focus on Escape', async ({
  page,
}) => {
  await page.goto('/worlds/music');

  const workspace = page.locator('[data-world-focus-region="workspace"]');
  const mainPlane = page.locator('.world-focus-main-plane');
  const invoke = page.getByRole('button', {
    name: 'Apri DANTE per il Mondo Musica',
  });

  await expect(invoke).toBeVisible();
  await expect(page.getByRole('dialog', { name: 'DANTE' })).toHaveCount(0);
  await expect(workspace).toHaveAttribute(
    'data-world-focus-main-interaction',
    'interactive',
  );
  await expect(mainPlane).not.toHaveAttribute('inert', '');

  await invoke.focus();
  await invoke.click();

  const dialog = page.getByRole('dialog', { name: 'DANTE' });
  const textarea = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  const surface = page.locator(
    '[data-world-focus-surface-id="dante:composer"]',
  );

  await expect(dialog).toBeVisible();
  await expect(dialog).toHaveAttribute('aria-modal', 'false');
  await expect(textarea).toBeFocused();
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'popover',
  );
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-interaction',
    'interactive',
  );
  await expect(workspace).toHaveAttribute(
    'data-world-focus-main-interaction',
    'interactive',
  );
  expect(
    await surface.evaluate((element) => getComputedStyle(element).pointerEvents),
  ).toBe('none');
  expect(
    await dialog.evaluate((element) => getComputedStyle(element).pointerEvents),
  ).toBe('auto');

  await textarea.fill('Bozza che non deve sparire prima dell’invio');
  await expect(textarea).toHaveValue('Bozza che non deve sparire prima dell’invio');

  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(invoke).toBeFocused();
  await expect(page).toHaveURL(/\/worlds\/music$/);
});

test('D1 remains contained and touch-usable in the contracted 390px World workspace', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const workspace = page.locator('[data-world-focus-region="workspace"]');
  const invoke = page.getByRole('button', {
    name: 'Apri DANTE per il Mondo Musica',
  });
  const invokeBox = await invoke.boundingBox();
  expect(invokeBox).not.toBeNull();
  if (invokeBox === null) {
    throw new Error('Expected compact DANTE invoke geometry');
  }
  expect(invokeBox.width).toBeGreaterThanOrEqual(44);
  expect(invokeBox.height).toBeGreaterThanOrEqual(44);

  await invoke.click();
  const dialog = page.getByRole('dialog', { name: 'DANTE' });
  await expect(dialog).toBeVisible();

  const workspaceBox = await workspace.boundingBox();
  const dialogBox = await dialog.boundingBox();
  expect(workspaceBox).not.toBeNull();
  expect(dialogBox).not.toBeNull();
  if (workspaceBox === null || dialogBox === null) {
    throw new Error('Expected compact DANTE workspace geometry');
  }

  expect(dialogBox.x).toBeGreaterThanOrEqual(workspaceBox.x);
  expect(dialogBox.x + dialogBox.width).toBeLessThanOrEqual(
    workspaceBox.x + workspaceBox.width + 1,
  );
  expect(dialogBox.y).toBeGreaterThanOrEqual(workspaceBox.y);
  expect(dialogBox.y + dialogBox.height).toBeLessThanOrEqual(
    workspaceBox.y + workspaceBox.height + 1,
  );

  const closeBox = await page
    .getByRole('button', { name: 'Chiudi DANTE' })
    .boundingBox();
  expect(closeBox).not.toBeNull();
  if (closeBox === null) {
    throw new Error('Expected compact DANTE close geometry');
  }
  expect(closeBox.width).toBeGreaterThanOrEqual(44);
  expect(closeBox.height).toBeGreaterThanOrEqual(44);

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});

test('D1 composer has no detectable axe violations at wide and compact widths', async ({
  page,
}) => {
  for (const viewport of [
    { width: 1600, height: 900 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto('/worlds/music');
    await page
      .getByRole('button', { name: 'Apri DANTE per il Mondo Musica' })
      .click();
    await expect(page.getByRole('dialog', { name: 'DANTE' })).toBeVisible();

    const results = await new AxeBuilder({ page })
      .include('.world-focus-shell')
      .analyze();

    expect(results.violations).toEqual([]);
  }
});
