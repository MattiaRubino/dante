import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Quick keeps its compact clock field while Advanced uses the Edit interval visual scale', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();

  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  const quickClocks = dialog.locator(
    '.temporal-create-u2-when > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(quickClocks).toHaveCount(2);
  for (const clock of await quickClocks.all()) {
    await expect(clock).toHaveCSS('min-height', '42px');
  }
  const quickWhen = dialog.locator('.temporal-create-u2-when');
  await expect(quickWhen).not.toHaveCSS('max-width', '820px');

  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');
  const advancedWhen = dialog.locator('.temporal-create-u2-when');
  await expect(advancedWhen).toHaveCSS('max-width', '820px');
  const advancedControls = advancedWhen.locator(
    ':scope > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(advancedControls).toHaveCount(2);
  for (const clock of await advancedControls.all()) {
    await expect(clock).toHaveCSS('min-height', '46px');
  }

  // A full objective form exists only in Advanced, and uses the shared row.
  await dialog.getByRole('button', { name: 'Aggiungi obiettivo' }).click();
  await expect(dialog.locator('.temporal-create-objective__row')).toHaveCount(1);
  await expect(
    dialog.getByRole('textbox', { name: 'Obiettivo 1' }),
  ).toBeVisible();
});
