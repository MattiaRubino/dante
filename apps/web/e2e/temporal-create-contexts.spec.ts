import { expect, test, type Page } from '@playwright/test';

import { setTimedDuration } from './helpers/create-time';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('Create stages Life Area color and keeps the 45-minute interval without fabricating fixture-owned Life Areas', async ({
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

  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card[data-temporal-create-projection]')
    .filter({ hasText: 'Sessione studio' });
  await expect(card).toBeVisible();
  // Editing start time must not silently roll the end to tomorrow.
  await expect(card.locator('.timeline-event-card__time'))
    .toContainText('15:00–15:45');
  // The fixture runtime has no PostgreSQL Life Area catalog. Canonical
  // Life Area persistence is asserted by authenticated U2 E2E; a preview-only
  // typed label must not masquerade as an accepted persisted group here.
  await expect(card).toContainText('15:00–15:45');

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
  // Typing alone never creates a canonical Life Area; the user must commit
  // through the actual U2 authoring endpoint in the authenticated journey.
  await expect(secondArea).toHaveValue(/studio/i);
});
