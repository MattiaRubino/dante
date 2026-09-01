import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

const WORLD_ORIENTATION_CASES = [
  {
    id: 'music',
    title: 'Musica',
    description: 'Creatività, ascolto e progetti musicali.',
  },
  {
    id: 'finance',
    title: 'Finanza',
    description: 'Risorse, risparmio e obiettivi economici.',
  },
  {
    id: 'travel',
    title: 'Viaggi',
    description: 'Esperienze, luoghi e prossime partenze.',
  },
] as const;

test('World first-open presents orientation without a universal time Lens', async ({
  page,
}) => {
  for (const world of WORLD_ORIENTATION_CASES) {
    await page.goto(`/worlds/${world.id}`);

    const context = page.locator(
      `[data-world-focus-context-id="${world.id}"]`,
    );
    await expect(context).toBeVisible();
    await expect(context.getByRole('heading', { level: 1 })).toHaveText(
      world.title,
    );
    await expect(context).toContainText(world.description);
    await expect(context.locator('.world-focus-lens')).toHaveCount(0);
    await expect(context.locator('select')).toHaveCount(0);
  }
});

test('World orientation remains bounded inside the compact workspace', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const workspace = await page
    .locator('[data-world-focus-region="workspace"]')
    .boundingBox();
  const context = await page
    .locator('[data-world-focus-context-id="music"]')
    .boundingBox();

  expect(workspace).not.toBeNull();
  expect(context).not.toBeNull();
  if (workspace === null || context === null) {
    throw new Error('Expected compact World orientation geometry');
  }

  expect(context.x).toBeGreaterThanOrEqual(workspace.x);
  expect(context.x + context.width).toBeLessThanOrEqual(
    workspace.x + workspace.width,
  );

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});
