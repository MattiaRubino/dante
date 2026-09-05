import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

async function selectCreateContext(dialog: Locator, label: string) {
  const trigger = dialog.locator('.temporal-create-context-trigger');
  await trigger.click();
  const picker = dialog.locator('.temporal-create-context-popover');
  await expect(picker).toBeVisible();
  await picker.getByRole('option', { name: label }).click();
}

test('item appearance inherits Context by default and an override remains presentation-only', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog
    .getByRole('textbox', { name: 'Titolo' })
    .fill('Deep work override');
  await dialog.getByLabel('Ora').fill('16:30');
  await dialog.getByLabel('Durata prevista').selectOption('60');
  await selectCreateContext(dialog, 'Focus / lavoro profondo');

  const preview = page.locator(
    '[data-temporal-create-projection="temporal-create-preview"]',
  );
  await expect(preview).toBeVisible();
  await expect(preview).toHaveAttribute('data-timeline-tone', 'focus');

  const advancedToggle = dialog.getByRole('button', {
    name: 'Opzioni avanzate',
  });
  await expect(advancedToggle).toHaveAttribute('aria-expanded', 'false');
  await advancedToggle.click();
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );
  await expect(dialog.getByText('Aspetto', { exact: true })).toBeVisible();

  const inherit = dialog.getByRole('radio', {
    name: /Eredita dal Contesto/,
  });
  const red = dialog.getByRole('radio', {
    name: /Colore personalizzato · Rosso/,
  });
  const redChoice = dialog.locator(
    '.temporal-create-appearance__tone[data-appearance-tone="urgent"]',
  );
  await expect(inherit).toBeChecked();
  await redChoice.click();
  await expect(red).toBeChecked();
  await expect(preview).toHaveAttribute('data-timeline-tone', 'urgent');

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.getByText('Aspetto', { exact: true })).toHaveCount(0);

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(red).toBeChecked();
  await expect(preview).toHaveAttribute('data-timeline-tone', 'urgent');

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card')
    .filter({ hasText: 'Deep work override' });
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute('data-temporal-create-projection');
  await expect(card).toHaveAttribute('data-timeline-tone', 'urgent');
  await expect(card).toContainText('Focus / lavoro profondo');

  const resetGroupsFocus = page.getByRole('button', {
    name: 'Ripristina gruppi e focus',
  });
  const urgentContext = page.locator(
    '.dante-timeline-group-chip[data-group-id="urgenze"]',
  );
  await urgentContext.click();
  await expect(urgentContext).toHaveAttribute('aria-pressed', 'true');
  await expect(card).toHaveCount(0);
  await resetGroupsFocus.click();
  await expect(card).toBeVisible();

  const focusContext = page.locator(
    '.dante-timeline-group-chip[data-group-id="focus"]',
  );
  await focusContext.click();
  await expect(focusContext).toHaveAttribute('aria-pressed', 'true');
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute('data-timeline-tone', 'urgent');
  await resetGroupsFocus.click();

  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toContainText('Deep work override');
  await toast.getByRole('button', { name: 'Annulla' }).click();
  await expect(card).toHaveCount(0);
});
