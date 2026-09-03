import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Continuity surfaces meaningful in-motion threads without a fake Resume action', async ({
  page,
}) => {
  await page.goto('/worlds/music');

  const continuity = page.locator('.world-focus-continuity');
  await expect(continuity).toBeVisible();
  await expect(continuity).toHaveAttribute(
    'data-world-focus-presentation',
    'section',
  );
  await expect(
    continuity.getByRole('heading', { level: 2, name: 'In movimento' }),
  ).toBeVisible();
  await expect(continuity.getByText('Neon Static')).toBeVisible();
  await expect(continuity.getByText('Master v3')).toBeVisible();
  await expect(continuity.getByText('Glass Signal')).toBeVisible();
  await expect(continuity.getByText('In pausa')).toBeVisible();
  await expect(page.getByRole('button', { name: /riprendi/i })).toHaveCount(0);
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

test('M2 Continuity presentation remains bounded across compact and 720px tuning pressure', async ({
  page,
}) => {
  for (const width of [720, 719, 390] as const) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/worlds/music');

    const workspaceLocator = page.locator(
      '[data-world-focus-region="workspace"]',
    );
    const continuityLocator = page.locator('.world-focus-continuity');

    await expect(continuityLocator).toBeVisible();
    await expect(continuityLocator).toHaveAttribute(
      'data-world-focus-presentation',
      'section',
    );

    const workspace = await workspaceLocator.boundingBox();
    const continuity = await continuityLocator.boundingBox();

    expect(workspace).not.toBeNull();
    expect(continuity).not.toBeNull();
    if (workspace === null || continuity === null) {
      throw new Error(`Expected Continuity geometry at ${width}px`);
    }

    expect(continuity.x).toBeGreaterThanOrEqual(workspace.x);
    expect(continuity.x + continuity.width).toBeLessThanOrEqual(
      workspace.x + workspace.width,
    );

    const hasHorizontalOverflow = await page.evaluate(
      () =>
        document.documentElement.scrollWidth >
        document.documentElement.clientWidth + 1,
    );
    expect(hasHorizontalOverflow).toBe(false);
  }
});
