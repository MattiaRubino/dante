import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Access stays outside the application shell', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('[data-app-region="topbar"]')).toHaveCount(0);
});

test('application navigation keeps one persistent Topbar and real browser history', async ({
  page,
}) => {
  await page.goto('/home');

  const topbar = page.locator('[data-app-region="topbar"]');
  await expect(topbar).toBeVisible();
  await expect(page.getByRole('main', { name: 'Home DANTE' })).toBeVisible();

  await page.getByRole('link', { name: 'Mondi' }).click();
  await expect(page).toHaveURL(/\/worlds$/);
  await expect(page.getByRole('heading', { name: 'Mondi' })).toBeVisible();
  await expect(topbar).toBeVisible();

  await page.goBack();
  await expect(page).toHaveURL(/\/home$/);
  await expect(page.getByRole('main', { name: 'Home DANTE' })).toBeVisible();
});

test('global search expands inline, focuses, searches, and routes truthfully', async ({
  page,
}) => {
  await page.goto('/home');

  const searchTrigger = page.getByRole('button', { name: 'Cerca in DANTE' });
  await expect(searchTrigger).toBeVisible();
  await searchTrigger.click();

  const searchSurface = page.getByRole('search', { name: 'Cerca in DANTE' });
  await expect(searchSurface).toBeVisible();
  await expect(
    page.getByRole('navigation', { name: 'Navigazione principale' }),
  ).toHaveCount(0);
  await expect(page.getByRole('dialog')).toHaveCount(0);

  const searchInput = page.getByRole('combobox', { name: 'Cerca in DANTE' });
  await expect(searchInput).toBeFocused();
  await searchInput.fill('impostazioni');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/settings$/);
  await expect(searchSurface).toHaveCount(0);
  await expect(
    page.getByRole('navigation', { name: 'Navigazione principale' }),
  ).toBeVisible();
});

for (const viewport of [
  { width: 1440, height: 900 },
  { width: 1024, height: 768 },
  { width: 760, height: 900 },
  { width: 390, height: 844 },
]) {
  test(`Topbar remains bounded at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto('/home');

    const topbar = page.locator('[data-app-region="topbar"]');
    await expect(topbar).toBeVisible();

    const overflow = await topbar.evaluate(
      (element) => element.scrollWidth - element.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);
  });
}

test('inline search remains bounded on the 390px mobile shell', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Cerca in DANTE' }).click();

  const searchSurface = page.getByRole('search', { name: 'Cerca in DANTE' });
  const resultsPanel = page.locator('.app-topbar-search-panel');
  await expect(searchSurface).toBeVisible();
  await expect(resultsPanel).toBeVisible();

  for (const locator of [searchSurface, resultsPanel]) {
    const box = await locator.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(390);
  }
});

test('Topbar including inline search has no detectable WCAG A/AA violations', async ({
  page,
}) => {
  await page.goto('/home');
  await page.getByRole('button', { name: 'Cerca in DANTE' }).click();
  await expect(page.getByRole('search', { name: 'Cerca in DANTE' })).toBeVisible();

  const results = await new AxeBuilder({ page })
    .include('[data-app-region="topbar"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
