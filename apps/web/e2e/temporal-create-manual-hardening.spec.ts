import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('floating Create can move and Advanced expands inline without reviving Quick Expanded Full chrome', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.locator('.temporal-create-composer__close')).toHaveText('×');
  await expect(dialog.locator('.temporal-create-composer__header button')).toHaveCount(
    1,
  );

  const handle = dialog.locator('.temporal-create-composer__heading-copy');
  const initial = await dialog.boundingBox();
  const handleBox = await handle.boundingBox();
  if (!initial || !handleBox) {
    throw new Error('Expected floating Create geometry');
  }

  await page.mouse.move(
    handleBox.x + handleBox.width / 2,
    handleBox.y + Math.min(16, handleBox.height / 2),
  );
  await page.mouse.down();
  await page.mouse.move(
    handleBox.x + handleBox.width / 2 + 180,
    handleBox.y + Math.min(16, handleBox.height / 2) + 80,
    { steps: 5 },
  );
  await page.mouse.up();

  const moved = await dialog.boundingBox();
  if (!moved) {
    throw new Error('Expected moved Create geometry');
  }
  expect(moved.x).toBeGreaterThan(initial.x + 80);
  expect(moved.y).toBeGreaterThan(initial.y + 30);

  const advanced = dialog.getByRole('button', { name: 'Opzioni avanzate' });
  await expect(advanced).toHaveAttribute('aria-expanded', 'false');
  await advanced.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await expect(
    dialog.getByRole('button', { name: 'Nascondi opzioni avanzate' }),
  ).toHaveAttribute('aria-expanded', 'true');
  await expect(dialog.locator('[data-create-advanced="activity"]')).toBeVisible();

  const expanded = await dialog.boundingBox();
  if (!expanded) {
    throw new Error('Expected Advanced Create geometry');
  }
  expect(expanded.x).toBeGreaterThanOrEqual(0);
  expect(expanded.x + expanded.width).toBeLessThanOrEqual(1440.5);

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.locator('[data-create-advanced]')).toHaveCount(0);
  await expect(
    dialog.getByRole('button', { name: 'Opzioni avanzate' }),
  ).toBeVisible();
});
