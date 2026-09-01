import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Quick Add protects draft state and restores opener focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Aggiungi alla timeline' });
  await trigger.click();

  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  const title = dialog.getByRole('textbox', { name: 'Titolo' });
  await expect(title).toBeFocused();
  await expect(dialog).not.toContainText('home.timeline.create.');

  await title.fill('Studiare inglese');
  await page.keyboard.press('Escape');
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');

  await page.keyboard.press('Escape');
  await expect(dialog.getByText('Scartare questa bozza?')).toHaveCount(0);
  await expect(title).toBeFocused();
  await expect(title).toHaveValue('Studiare inglese');

  await page.locator('[data-temporal-create="backdrop"]').click({
    position: { x: 2, y: 2 },
  });
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await dialog.getByRole('button', { name: 'Scarta' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('Quick Add creates a timed Activity, reveals its projection, and undoes it', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Nuova attività');
  await dialog.getByLabel('Ora').fill('13:30');
  await dialog.getByLabel('Durata').selectOption('60');
  await dialog.getByLabel('Contesto').selectOption('focus');

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page.locator(
    '[data-temporal-create-projection]:not(.is-preview)',
  ).filter({ hasText: 'Nuova attività' });
  await expect(card).toBeVisible();
  await expect(card).toBeFocused();

  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toContainText('Creato: Nuova attività');
  await toast.getByRole('button', { name: 'Annulla' }).click();
  await expect(card).toHaveCount(0);
});

test('Quick Add preserves Event/all-day and Activity/unscheduled semantics', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Aggiungi alla timeline' });
  await trigger.click();
  let dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Fiera');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();

  await expect(
    page.locator('.temporal-create-all-day').filter({ hasText: 'Fiera' }),
  ).toBeVisible();

  await trigger.click();
  dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Da organizzare');
  await dialog.getByRole('radio', { name: 'Da pianificare' }).click();
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(page.locator('.temporal-create-toast.is-on')).toContainText(
    'Da organizzare',
  );
});

test('Quick Add validates before commit and exposes progressive timezone details', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog.getByText('Inserisci un titolo.')).toBeVisible();
  await expect(dialog.getByRole('textbox', { name: 'Titolo' })).toBeFocused();

  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Call estera');
  await dialog.getByRole('button', { name: '+ Dettagli' }).click();
  await dialog.getByRole('radio', { name: 'Fuso orario' }).click();
  const zone = dialog.getByLabel('Fuso orario');
  await zone.fill('Europe/Rome');
  await expect(zone).toHaveValue('Europe/Rome');
});

test('double click on empty Timeline time opens contextual Create', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const section = page.locator('.timeline-day-section').first();
  const box = await section.boundingBox();
  if (!box) {
    throw new Error('Expected a visible Timeline day section');
  }
  await section.dblclick({
    position: { x: Math.min(600, box.width - 40), y: box.height * 0.52 },
  });

  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByLabel('Data')).not.toHaveValue('');
  await expect(dialog.getByLabel('Ora')).not.toHaveValue('');
});

test('Quick Add becomes a bounded mobile sheet without horizontal overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();

  const dialog = page.getByRole('dialog', { name: 'Aggiungi' });
  await expect(dialog).toBeVisible();
  const box = await dialog.boundingBox();
  expect(box).not.toBeNull();
  expect(box?.width ?? 999).toBeLessThanOrEqual(390);
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth <=
        document.documentElement.clientWidth,
    ),
  ).toBe(true);
});