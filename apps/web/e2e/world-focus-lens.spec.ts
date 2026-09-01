import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('B1 exposes visible World context and restorable temporal Lens history', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/worlds/music');

  await expect(page.getByRole('heading', { level: 1, name: 'Musica' })).toBeVisible();
  await expect(
    page.getByText('Creatività, ascolto e progetti musicali.'),
  ).toBeVisible();

  const timeGroup = page.getByRole('group', { name: 'Periodo' });
  await expect(timeGroup).toBeVisible();
  await expect(
    timeGroup.getByRole('button', { name: '30 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');
  await expect(page).toHaveURL(/\/worlds\/music$/);

  await timeGroup.getByRole('button', { name: '90 giorni' }).click();
  await expect(page).toHaveURL(/\/worlds\/music\?time=90d$/);
  await expect(
    timeGroup.getByRole('button', { name: '90 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');
  await expect(
    page.locator('[data-world-focus-context="true"]'),
  ).toHaveAttribute('data-world-focus-scope-key', 'music|time:90d');

  await page.reload();
  await expect(
    page.getByRole('button', { name: '90 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');

  await page.goBack();
  await expect(page).toHaveURL(/\/worlds\/music$/);
  await expect(
    page.getByRole('button', { name: '30 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');
});

test('B1 falls back safely for malformed or unsupported Lens URL state', async ({
  page,
}) => {
  await page.goto('/worlds/music?time=banana');
  await expect(page.getByRole('heading', { name: 'Musica' })).toBeVisible();
  await expect(
    page.getByRole('button', { name: '30 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');

  await page.goto('/worlds/finance?time=7d');
  await expect(page.getByRole('heading', { name: 'Finanza' })).toBeVisible();
  await expect(page.getByRole('button', { name: '7 giorni' })).toHaveCount(0);
  await expect(
    page.getByRole('button', { name: '30 giorni' }),
  ).toHaveAttribute('aria-pressed', 'true');
});

test('B1 does not invent a temporal Lens for Worlds without that capability', async ({
  page,
}) => {
  await page.goto('/worlds/travel?time=90d');

  await expect(page.getByRole('heading', { level: 1, name: 'Viaggi' })).toBeVisible();
  await expect(page.locator('.world-focus-lens')).toHaveCount(0);
  await expect(
    page.locator('[data-world-focus-context="true"]'),
  ).toHaveAttribute('data-world-focus-scope-key', 'travel|time:none');
});

test('B1 uses the compact native selector without changing Lens semantics', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const select = page.getByRole('combobox', { name: 'Periodo' });
  await expect(select).toBeVisible();
  await expect(select).toHaveValue('30d');

  await select.selectOption('90d');
  await expect(page).toHaveURL(/\/worlds\/music\?time=90d$/);
  await expect(select).toHaveValue('90d');

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});
