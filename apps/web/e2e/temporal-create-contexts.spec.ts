import { expect, test, type Page } from '@playwright/test';

import { setTimedDuration } from './helpers/create-time';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('Create stages a colored Life Area and reuses existing names case-insensitively', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  let dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Sessione studio');
  await dialog.getByRole('textbox', { name: 'Inizio: ore' }).fill('15');
  await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).fill('00');
  await setTimedDuration(dialog, 45);

  const area = dialog.getByRole('textbox', { name: 'Life Area (opzionale)' });
  await area.fill('Studio');
  await expect(area).toHaveValue('Studio');
  const color = dialog.getByRole('button', { name: 'Colore Life Area' });
  await color.click();
  await page.getByRole('dialog', { name: 'Scegli colore' })
    .getByRole('button', { name: 'Verde mela' }).click();
  await expect(color.locator('span')).toHaveCSS(
    'background-color',
    'rgb(124, 179, 66)',
  );
  await expect(area).toHaveValue('Studio');

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card[data-temporal-create-projection]')
    .filter({ hasText: 'Sessione studio' });
  await expect(card).toBeVisible();
  await expect(card).toContainText('Studio');

  await card.locator('.timeline-event-card__time').click();
  await expect(page.locator('.timeline-time-popover')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.timeline-time-popover')).toHaveCount(0);

  dialog = await openCreate(page);
  const secondArea = dialog.getByRole('textbox', {
    name: 'Life Area (opzionale)',
  });
  await secondArea.fill('studio');
  // A case-insensitive exact match must select the existing Life Area
  // instead of creating a second local group with the same name.
  await expect(secondArea).toHaveValue(/studio/i);
  await expect(
    page.locator('.dante-timeline-group-chip[data-group-id="local-context:studio"]'),
  ).toHaveCount(1);
});
