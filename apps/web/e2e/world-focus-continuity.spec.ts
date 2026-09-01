import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Continuity surfaces meaningful in-motion threads without a fake Resume action', async ({
  page,
}) => {
  await page.goto('/worlds/music');

  const continuity = page.locator('.world-focus-continuity');
  await expect(continuity).toBeVisible();
  await expect(
    continuity.getByRole('heading', { level: 2, name: 'In movimento' }),
  ).toBeVisible();
  await expect(continuity.getByText('Neon Static')).toBeVisible();
  await expect(continuity.getByText('Master v3')).toBeVisible();
  await expect(continuity.getByText('Glass Signal')).toBeVisible();
  await expect(continuity.getByText('In pausa')).toBeVisible();
  await expect(page.getByRole('button', { name: /riprendi/i })).toHaveCount(0);
});

test('Body exposes one explicit bounded program rather than a generic health resume', async ({
  page,
}) => {
  await page.goto('/worlds/body');

  const continuity = page.locator('.world-focus-continuity');
  await expect(continuity).toBeVisible();
  await expect(
    continuity.getByRole('heading', { level: 2, name: 'In movimento' }),
  ).toBeVisible();
  await expect(continuity.getByText('Mobility Reset')).toBeVisible();
  await expect(continuity.getByText('Program')).toBeVisible();
  await expect(continuity.getByText('Week 3 · Session B')).toBeVisible();
  await expect(continuity.getByText('Attivo')).toBeVisible();
});

test('Continuity remains sparse where no justified thread exists', async ({ page }) => {
  for (const worldId of ['finance', 'relationships', 'routine'] as const) {
    await page.goto(`/worlds/${worldId}`);
    await expect(page.locator('.world-focus-continuity')).toHaveCount(0);
  }
});

test('Travel continuity represents planning rather than misclassifying the next segment', async ({
  page,
}) => {
  await page.goto('/worlds/travel');

  const continuity = page.locator('.world-focus-continuity');
  await expect(continuity.getByText('Japan 2027')).toBeVisible();
  await expect(continuity.getByText('Planning')).toBeVisible();
  await expect(continuity.getByText('Flight shortlist')).toBeVisible();
});

test('Continuity remains bounded in the compact World workspace', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const workspace = await page
    .locator('[data-world-focus-region="workspace"]')
    .boundingBox();
  const continuity = await page.locator('.world-focus-continuity').boundingBox();

  expect(workspace).not.toBeNull();
  expect(continuity).not.toBeNull();
  if (workspace === null || continuity === null) {
    throw new Error('Expected compact Continuity geometry');
  }

  expect(continuity.x).toBeGreaterThanOrEqual(workspace.x);
  expect(continuity.x + continuity.width).toBeLessThanOrEqual(
    workspace.x + workspace.width,
  );

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});
