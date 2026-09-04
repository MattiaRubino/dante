import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('Quick Create stays compact while Advanced has a persistent back path and no visible inner scrollbar', async ({
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

  const repeat = dialog.getByLabel('Ripeti');
  await expect(repeat.locator('option[value="custom"]')).toHaveText(
    'Personalizzata…',
  );
  await expect(
    dialog.getByRole('button', { name: 'Personalizza…' }),
  ).toHaveCount(0);

  const advanced = dialog.getByRole('button', { name: 'Opzioni avanzate' });
  await expect(advanced).toHaveAttribute('aria-expanded', 'false');
  const advancedBox = await advanced.boundingBox();
  expect(advancedBox).not.toBeNull();
  expect(advancedBox?.width ?? 999).toBeLessThan(220);
  expect(advancedBox?.height ?? 999).toBeLessThanOrEqual(36);

  await advanced.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await expect(dialog).toHaveClass(/is-full/);

  const back = dialog.getByRole('button', { name: 'Nascondi opzioni avanzate' });
  await expect(back).toBeVisible();
  await expect(back).toContainText('Torna alla creazione rapida');
  await expect(back).toHaveAttribute('aria-expanded', 'true');
  await expect(dialog.locator('[data-create-advanced="activity"]')).toBeVisible();

  const expanded = await dialog.boundingBox();
  if (!expanded) {
    throw new Error('Expected Advanced Create geometry');
  }
  expect(expanded.x).toBeGreaterThanOrEqual(0);
  expect(expanded.y).toBeGreaterThanOrEqual(0);
  expect(expanded.x + expanded.width).toBeLessThanOrEqual(1440.5);
  expect(expanded.y + expanded.height).toBeLessThanOrEqual(900.5);
  expect(Math.abs(expanded.x + expanded.width / 2 - 720)).toBeLessThan(2);
  expect(expanded.width).toBeGreaterThan(900);

  const body = dialog.locator('.temporal-create-composer__body');
  const scrollStyle = await body.evaluate((element) => {
    const style = getComputedStyle(element);
    return {
      overflowY: style.overflowY,
      scrollbarWidth: style.getPropertyValue('scrollbar-width'),
    };
  });
  expect(['auto', 'scroll']).toContain(scrollStyle.overflowY);
  expect(scrollStyle.scrollbarWidth).toBe('none');

  await body.evaluate((element) => {
    element.scrollTop = element.scrollHeight;
  });
  await expect(dialog.locator('.temporal-create-composer__close')).toBeInViewport();
  await expect(dialog.locator('.temporal-create-actions')).toBeInViewport();
  await expect(back).toBeInViewport();

  await back.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog).not.toHaveClass(/is-full/);
  await expect(dialog.locator('[data-create-advanced]')).toHaveCount(0);
  await expect(
    dialog.getByRole('button', { name: 'Opzioni avanzate' }),
  ).toBeVisible();

  await repeat.selectOption('custom');
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await expect(dialog.locator('[data-create-recurrence-owner="routine"]')).toBeInViewport();
  await expect(
    dialog.getByRole('button', { name: 'Nascondi opzioni avanzate' }),
  ).toBeVisible();
});
