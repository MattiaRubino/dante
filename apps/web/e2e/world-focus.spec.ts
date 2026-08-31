import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Home opens a centered World on the dedicated World Focus route', async ({
  page,
}) => {
  await page.goto('/home');

  const music = page.locator('.home-world[aria-label="Musica"]');
  await music.click();
  await expect(music).toHaveAttribute('aria-current', 'true');
  await music.click();

  await expect(page).toHaveURL(/\/worlds\/music$/);
  const focus = page.locator('.world-focus-shell');
  await expect(page.getByRole('main', { name: 'Mondo Musica' })).toBeVisible();
  await expect(focus).toHaveAttribute('data-world-focus-geometry-version', 'wf-g1');
  await expect(page.locator('[data-app-region="topbar"]')).toBeVisible();
  await expect(page.locator('.world-focus-guide-rail')).toHaveCount(2);
  await expect(page.locator('[data-guide-line]')).toHaveCount(6);
  await expect(page.locator('[data-world-focus-region="workspace"]')).toBeVisible();

  const background = await focus.evaluate(
    (element) => getComputedStyle(element).backgroundColor,
  );
  expect(background).toBe('rgb(255, 255, 255)');

  await page.goBack();
  await expect(page).toHaveURL(/\/home$/);
});

test('the initially centered World still requires two activations', async ({
  page,
}) => {
  await page.goto('/home');

  const body = page.locator('.home-world[aria-label="Corpo"]');
  await expect(body).toHaveAttribute('aria-current', 'true');

  await body.click();
  await expect(page).toHaveURL(/\/home$/);

  await body.click();
  await expect(page).toHaveURL(/\/worlds\/body$/);
});

test('dragging the active World does not enter World Focus', async ({ page }) => {
  await page.goto('/home');

  const body = page.locator('.home-world[aria-label="Corpo"]');
  const box = await body.boundingBox();
  expect(box).not.toBeNull();
  if (box === null) {
    throw new Error('Expected active World geometry');
  }

  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width / 2 + 46, box.y + box.height / 2);
  await page.mouse.up();

  await expect(page).toHaveURL(/\/home$/);
  await expect(page.locator('.world-focus-shell')).toHaveCount(0);
});

test('keyboard activation selects first and opens the centered World second', async ({
  page,
}) => {
  await page.goto('/home');

  const music = page.locator('.home-world[aria-label="Musica"]');
  await music.focus();
  await page.keyboard.press('Enter');
  await expect(music).toHaveAttribute('aria-current', 'true');

  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/worlds\/music$/);
});

test('direct World Focus URL opens the same geometry and has a safe close path', async ({
  page,
}) => {
  await page.goto('/worlds/travel');

  const focus = page.locator('.world-focus-shell');
  await expect(focus).toBeVisible();
  await expect(focus).toHaveAttribute('data-entry-origin', 'fallback');
  await expect(focus).toHaveAttribute('data-world-focus-geometry-version', 'wf-g1');
  await expect(page.locator('[data-app-region="topbar"]')).toBeVisible();

  await page.getByRole('button', { name: 'Torna indietro' }).click();
  await expect(page).toHaveURL(/\/worlds$/);
});

test('WF-G1 keeps the workspace between the side guide rails across desktop widths', async ({
  page,
}) => {
  for (const width of [1600, 1366, 1024, 901]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/worlds/music');

    const workspace = await page
      .locator('[data-world-focus-region="workspace"]')
      .boundingBox();
    const leftRail = await page
      .locator('.world-focus-guide-rail[data-side="left"]')
      .boundingBox();
    const rightRail = await page
      .locator('.world-focus-guide-rail[data-side="right"]')
      .boundingBox();

    expect(workspace).not.toBeNull();
    expect(leftRail).not.toBeNull();
    expect(rightRail).not.toBeNull();
    if (workspace === null || leftRail === null || rightRail === null) {
      throw new Error(`Missing WF-G1 geometry at ${width}px`);
    }

    expect(workspace.width).toBeGreaterThan(320);
    expect(workspace.x).toBeGreaterThanOrEqual(leftRail.x + leftRail.width);
    expect(workspace.x + workspace.width).toBeLessThanOrEqual(rightRail.x);
  }
});
