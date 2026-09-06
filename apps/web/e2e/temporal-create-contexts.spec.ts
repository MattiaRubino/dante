import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('page-local contexts carry their tone into native Timeline cards and deduplicate by name', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  let dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Sessione studio');
  await dialog.getByLabel('Ora').fill('15:00');
  await dialog.getByLabel('Durata prevista').selectOption('45');

  const contextTrigger = dialog.locator('.temporal-create-context-trigger');
  await contextTrigger.click();
  const picker = dialog.locator('.temporal-create-context-popover');
  await expect(picker).toBeVisible();
  await picker.getByRole('searchbox').fill('Studio');
  await picker.locator('.temporal-create-context-new').click();

  const createPane = picker.locator('.temporal-create-context-create');
  const contextName = createPane.getByRole('textbox');
  await expect(contextName).toHaveValue('Studio');
  await createPane
    .locator('.temporal-create-context-tone-grid [data-context-tone="health"]')
    .click();
  await createPane
    .locator('.temporal-create-context-create__actions .is-primary')
    .click();

  await expect(contextTrigger).toContainText('Studio');
  await expect(
    contextTrigger.locator('.temporal-create-context-swatch'),
  ).toHaveAttribute('data-context-tone', 'health');

  const contextChip = page.locator(
    '.dante-timeline-group-chip[data-group-id="local-context:studio"]',
  );
  await expect(contextChip).toBeVisible();
  await expect(contextChip).toHaveAttribute('data-timeline-tone', 'health');
  await expect(contextChip).toContainText('Studio');

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card[data-temporal-create-projection]')
    .filter({ hasText: 'Sessione studio' });
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute('data-timeline-tone', 'health');
  await expect(card).toContainText('Studio');

  await card.locator('.timeline-event-card__time').click();
  await expect(page.locator('.timeline-time-popover')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.timeline-time-popover')).toHaveCount(0);

  dialog = await openCreate(page);
  const secondTrigger = dialog.locator('.temporal-create-context-trigger');
  await secondTrigger.click();
  const secondPicker = dialog.locator('.temporal-create-context-popover');
  await secondPicker.getByRole('searchbox').fill('studio');
  await secondPicker.locator('.temporal-create-context-new').click();

  const secondCreatePane = secondPicker.locator(
    '.temporal-create-context-create',
  );
  await secondCreatePane.getByRole('textbox').fill('  studio  ');
  await secondCreatePane
    .locator('.temporal-create-context-tone-grid [data-context-tone="urgent"]')
    .click();
  await secondCreatePane
    .locator('.temporal-create-context-create__actions .is-primary')
    .click();

  await expect(
    page.locator(
      '.dante-timeline-group-chip[data-group-id="local-context:studio"]',
    ),
  ).toHaveCount(1);
  await expect(secondTrigger).toContainText('Studio');
  await expect(
    secondTrigger.locator('.temporal-create-context-swatch'),
  ).toHaveAttribute('data-context-tone', 'health');
});
