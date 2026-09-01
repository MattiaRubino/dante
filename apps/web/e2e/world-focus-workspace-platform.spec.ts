import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('World Focus mounts current content through the controlled composition host', async ({
  page,
}) => {
  await page.goto('/worlds/music');

  const composition = page.locator('.world-focus-composition');
  await expect(composition).toBeVisible();
  await expect(composition).toHaveAttribute(
    'data-world-focus-composition-count',
    '1',
  );

  const continuity = composition.locator(
    '[data-world-focus-composition-id="continuity"]',
  );
  await expect(continuity).toHaveAttribute(
    'data-world-focus-module-kind',
    'continuity',
  );
  await expect(continuity).toHaveAttribute(
    'data-world-focus-stability',
    'adaptive',
  );
  await expect(continuity).toHaveAttribute(
    'data-world-focus-origin',
    'application-derived',
  );
  await expect(continuity.locator('.world-focus-continuity')).toBeVisible();

  await expect(page.locator('.world-focus-surface-layer')).toHaveCount(0);
});

test('Workspace platform wrappers do not change compact containment', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const workspace = await page
    .locator('[data-world-focus-region="workspace"]')
    .boundingBox();
  const composition = await page.locator('.world-focus-composition').boundingBox();

  expect(workspace).not.toBeNull();
  expect(composition).not.toBeNull();
  if (workspace === null || composition === null) {
    throw new Error('Expected compact workspace composition geometry');
  }

  expect(composition.x).toBeGreaterThanOrEqual(workspace.x);
  expect(composition.x + composition.width).toBeLessThanOrEqual(
    workspace.x + workspace.width,
  );

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});
