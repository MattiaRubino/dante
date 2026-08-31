import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Home opens the centered World into the immersive focus and browser back preserves Home state', async ({
  page,
}) => {
  await page.goto('/home');

  await page.getByRole('button', { name: 'Comprimi assistente' }).click();
  const homeShell = page.locator('[data-home-region="shell"]');
  await expect(homeShell).toHaveAttribute('data-home-ai-state', 'collapsed');

  const music = page.locator('.home-world[aria-label="Musica"]');
  await music.click();
  await expect(music).toHaveAttribute('aria-current', 'true');

  await music.click();
  await expect(page).toHaveURL(/\/home\?focus=music$/);
  await expect(page.getByRole('main', { name: 'Mondo Musica' })).toBeVisible();
  await expect(page.locator('.world-focus-shell')).toHaveAttribute(
    'data-entry-origin',
    'live',
  );
  await expect(page.locator('.world-focus-shell')).toHaveAttribute(
    'data-world-focus-status',
    'ready',
  );
  await expect(page.locator('[data-app-region="topbar"]')).toBeHidden();

  await page.goBack();
  await expect(page).toHaveURL(/\/home$/);
  await expect(page.getByRole('main', { name: 'Mondo Musica' })).toHaveCount(0);
  await expect(homeShell).toHaveAttribute('data-home-ai-state', 'collapsed');
  await expect(music).toHaveAttribute('aria-current', 'true');
  await expect(music).toBeFocused();
  await expect(page.locator('[data-app-region="topbar"]')).toBeVisible();
});

test('dragging the active World does not enter World Focus', async ({ page }) => {
  await page.goto('/home');

  const body = page.locator('.home-world[aria-label="Corpo"]');
  await expect(body).toHaveAttribute('aria-current', 'true');
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

  const study = page.locator('.home-world[aria-label="Studio"]');
  await study.focus();
  await page.keyboard.press('Enter');
  await expect(study).toHaveAttribute('aria-current', 'true');

  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/home\?focus=study$/);
  await expect(page.getByRole('main', { name: 'Mondo Studio' })).toBeVisible();
});

test('direct World Focus URL has a safe fallback entry and close path', async ({
  page,
}) => {
  await page.goto('/home?focus=travel');

  const focus = page.locator('.world-focus-shell');
  await expect(focus).toBeVisible();
  await expect(focus).toHaveAttribute('data-entry-origin', 'fallback');
  await expect(focus).toHaveAttribute('data-world-focus-status', 'ready');
  await expect(page.getByRole('main', { name: 'Mondo Viaggi' })).toBeVisible();

  await page.getByRole('button', { name: 'Torna indietro' }).click();
  await expect(page).toHaveURL(/\/home$/);
  await expect(focus).toHaveCount(0);
});

test('reduced motion keeps World Focus usable without ornamental animation', async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/home?focus=music');

  const focus = page.locator('.world-focus-shell');
  await expect(focus).toBeVisible();
  const animationName = await focus.evaluate(
    (element) => getComputedStyle(element).animationName,
  );
  expect(animationName).toBe('none');

  await page.keyboard.press('Escape');
  await expect(page).toHaveURL(/\/home$/);
});
