import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('floating Create can move, uses header +/- for depth, and Full stays centered with a clear return path', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
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

  const expand = dialog.getByRole('button', {
    name: 'Dettagli e pianificazione',
  });
  await expect(expand).toHaveText('+');
  await expand.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'expanded');

  const expanded = await dialog.boundingBox();
  if (!expanded) {
    throw new Error('Expected Expanded Create geometry');
  }
  expect(expanded.x).toBeGreaterThan(15);
  expect(expanded.y).toBeGreaterThan(15);

  const collapse = dialog.getByRole('button', { name: 'Nascondi dettagli' });
  await expect(collapse).toHaveText('−');
  await expect(dialog.getByRole('button', { name: 'Riduci' })).toHaveCount(0);
  await collapse.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'quick');

  await dialog
    .getByRole('button', { name: 'Dettagli e pianificazione' })
    .click();
  await dialog.getByRole('button', { name: 'Editor completo →' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'full');

  const full = await dialog.boundingBox();
  if (!full) {
    throw new Error('Expected Full Create geometry');
  }
  expect(Math.abs(full.x + full.width / 2 - 720)).toBeLessThanOrEqual(2);
  expect(full.x).toBeGreaterThan(20);
  expect(full.width).toBeLessThan(1440 - 40);

  const backToDetails = dialog.getByRole('button', { name: '← Dettagli' });
  await expect(backToDetails).toBeVisible();
  await backToDetails.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'expanded');
  await expect(
    dialog.getByRole('button', { name: 'Nascondi dettagli' }),
  ).toBeVisible();
});
