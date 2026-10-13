import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

import { setTimedDuration } from './helpers/create-time';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

async function selectCreateContext(dialog: Locator, label: string) {
  const search = dialog.getByRole('textbox', { name: 'Life Area (opzionale)' });
  await search.fill(label);
  await dialog.getByRole('option', { name: label, exact: true }).click();
  await expect(search).toHaveValue(label);
}

test('Life Area selection and its colour survive Advanced round trips and Timeline filtering', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog
    .getByRole('textbox', { name: 'Titolo' })
    .fill('Deep work override');
  await dialog.getByRole('textbox', { name: 'Inizio: ore' }).fill('16');
  await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).fill('30');
  await setTimedDuration(dialog, 60);
  await selectCreateContext(dialog, 'Focus / lavoro profondo');

  const preview = page.locator(
    '[data-temporal-create-projection="temporal-create-preview"]',
  );
  // Preview is intentionally not rendered until U2 authoritative creation:
  // timeline-create-bridge.css hides .is-preview to avoid fabricated truth.
  // Still verify the staged Life Area tone before committing the item.
  await expect(preview).toBeHidden();
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
  const area = dialog.getByRole('textbox', { name: 'Life Area (opzionale)' });
  await expect(area).toHaveValue('Focus / lavoro profondo');
  const color = dialog.getByRole('button', { name: 'Colore Life Area' });
  await color.click();
  const palette = page.getByRole('dialog', { name: 'Scegli colore' });
  await expect(palette).toBeVisible();
  await palette.getByRole('button', { name: 'Rosso', exact: true }).click();
  await expect(color.locator('span')).toHaveCSS(
    'background-color',
    'rgb(213, 0, 0)',
  );

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(area).toHaveValue('Focus / lavoro profondo');

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(area).toHaveValue('Focus / lavoro profondo');
  await expect(color.locator('span')).toHaveCSS(
    'background-color',
    'rgb(213, 0, 0)',
  );

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);

  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card')
    .filter({ hasText: 'Deep work override' });
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute('data-temporal-create-projection');
  await expect(card).toHaveAttribute('data-timeline-tone', 'focus');
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
  await expect(card).toHaveAttribute('data-timeline-tone', 'focus');
  await resetGroupsFocus.click();

  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toContainText('Deep work override');
  await toast.getByRole('button', { name: 'Annulla' }).click();
  await expect(card).toHaveCount(0);
});
