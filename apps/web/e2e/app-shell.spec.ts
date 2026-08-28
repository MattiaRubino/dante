import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Access stays outside the application shell', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('[data-app-region="topbar"]')).toHaveCount(0);
});

test('application navigation keeps one persistent Topbar and real browser history', async ({ page }) => {
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

test('global search works from the keyboard without pretending remote search exists', async ({ page }) => {
  await page.goto('/home');

  await page.keyboard.press('Control+K');
  const dialog = page.getByRole('dialog', { name: 'Cerca in DANTE' });
  await expect(dialog).toBeVisible();

  await page.getByRole('combobox', { name: 'Cerca in DANTE' }).fill('impostazioni');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/settings$/);
  await expect(dialog).toHaveCount(0);
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

test('Topbar shell has no detectable WCAG A/AA violations in isolation', async ({ page }) => {
  await page.goto('/home');

  const results = await new AxeBuilder({ page })
    .include('[data-app-region="topbar"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
