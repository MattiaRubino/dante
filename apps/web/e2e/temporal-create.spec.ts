import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('C1-A quick add owns a clean draft lifecycle and restores opener focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Aggiungi alla timeline' });
  await expect(trigger).toBeEnabled();
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');

  await trigger.click();

  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  const title = dialog.getByRole('textbox', { name: 'Titolo' });
  await expect(dialog).toBeVisible();
  await expect(trigger).toHaveAttribute('aria-expanded', 'true');
  await expect(title).toBeFocused();
  await expect(title).toHaveValue('');

  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  await expect(trigger).toBeFocused();

  await trigger.click();
  await title.fill('Studiare inglese');
  await page.keyboard.press('Escape');

  await expect(dialog).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Continua a modificare' }),
  ).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(dialog.getByText('Scartare questa bozza?')).toHaveCount(0);
  await expect(title).toBeFocused();
  await expect(title).toHaveValue('Studiare inglese');

  const backdrop = page.locator('[data-temporal-create="backdrop"]');
  await backdrop.click({ position: { x: 2, y: 2 } });
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');

  await dialog.getByRole('button', { name: 'Scarta' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();

  await trigger.click();
  const reopened = page.getByRole('dialog', { name: 'Aggiungi' });
  await expect(reopened.getByRole('textbox', { name: 'Titolo' })).toHaveValue(
    '',
  );
});

test('C1-A close button cannot silently destroy a dirty title', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('/home');

  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  const title = dialog.getByRole('textbox', { name: 'Titolo' });

  await title.fill('Fotografare il tramonto');
  await dialog.getByRole('button', { name: 'Chiudi creazione' }).click();

  await expect(dialog).toBeVisible();
  await expect(title).toHaveValue('Fotografare il tramonto');
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();

  await dialog.getByRole('button', { name: 'Continua a modificare' }).click();
  await expect(title).toBeFocused();
  await expect(title).toHaveValue('Fotografare il tramonto');
});
