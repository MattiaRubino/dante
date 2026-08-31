import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('group filters and reset preserve the accepted focus grammar', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const focusChip = page.locator('[data-group-id="focus"]');
  const reset = page.getByRole('button', {
    name: 'Ripristina gruppi e focus',
  });
  const focusCard = page.locator('[data-timeline-event="7"]');
  const personalCard = page.locator('[data-timeline-event="12"]');

  await focusCard.scrollIntoViewIfNeeded();
  await expect(focusChip).toHaveAttribute('aria-pressed', 'false');
  await expect(focusCard).toHaveCount(1);
  await expect(personalCard).toHaveCount(1);

  const focusBox = await focusCard.boundingBox();
  expect(focusBox).not.toBeNull();
  if (!focusBox) {
    throw new Error('Expected Timeline focus-card geometry');
  }
  await page.mouse.click(
    focusBox.x + Math.max(12, focusBox.width - 16),
    focusBox.y +
      Math.min(focusBox.height - 12, Math.max(18, focusBox.height * 0.62)),
  );
  await expect(focusCard).toHaveClass(/is-focused/);

  await focusChip.click();
  await expect(focusChip).toHaveAttribute('aria-pressed', 'true');
  await expect(focusCard).toHaveCount(1);
  await expect(personalCard).toHaveCount(0);

  await reset.click();
  await expect(focusChip).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('[data-timeline-event="7"]')).not.toHaveClass(
    /is-focused/,
  );
  await expect(page.locator('[data-timeline-event="12"]')).toHaveCount(1);
});

test('keyboard group reorder moves exactly one slot and remains reversible', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const chips = page.locator('.dante-timeline-group-chip');
  const readOrder = () =>
    chips.evaluateAll((elements) =>
      elements.map((element) => element.getAttribute('data-group-id')),
    );

  const initialOrder = await readOrder();
  expect(initialOrder).toEqual([
    'focus',
    'riunioni',
    'salute',
    'creativita',
    'personale',
    'urgenze',
  ]);

  const creativity = page.locator('[data-group-id="creativita"]');
  await creativity.focus();
  await expect(creativity).toBeFocused();
  await creativity.press('Alt+ArrowRight');

  await expect
    .poll(readOrder)
    .toEqual([
      'focus',
      'riunioni',
      'salute',
      'personale',
      'creativita',
      'urgenze',
    ]);
  await expect(creativity).toBeFocused();

  await creativity.press('Alt+ArrowLeft');
  await expect.poll(readOrder).toEqual(initialOrder);
  await expect(creativity).toBeFocused();
});

test('view options toggle real Timeline layers, reset defaults, and restore trigger focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Vista e legenda' });
  const nowLine = page.locator('.timeline-now-line');
  const milestones = page.locator('.timeline-milestone');
  const margins = page.locator('.timeline-margin-label');

  await expect(nowLine).toHaveCount(1);
  expect(await milestones.count()).toBeGreaterThan(0);
  expect(await margins.count()).toBeGreaterThan(0);

  await trigger.click();
  const dialog = page.getByRole('dialog', { name: 'Vista e legenda' });
  await expect(dialog).toBeVisible();

  const marginsOption = dialog.getByRole('checkbox', {
    name: 'Margini tra impegni',
  });
  const nowOption = dialog.getByRole('checkbox', { name: 'Ora corrente' });
  const milestonesOption = dialog.getByRole('checkbox', {
    name: 'Milestone sul percorso',
  });

  await expect(marginsOption).toBeChecked();
  await expect(nowOption).toBeChecked();
  await expect(milestonesOption).toBeChecked();

  await nowOption.uncheck();
  await expect(nowLine).toHaveCount(0);

  await milestonesOption.uncheck();
  await expect(milestones).toHaveCount(0);

  await marginsOption.uncheck();
  await expect(margins).toHaveCount(0);

  await dialog
    .getByRole('button', { name: 'Ripristina vista predefinita' })
    .click();
  await expect(marginsOption).toBeChecked();
  await expect(nowOption).toBeChecked();
  await expect(milestonesOption).toBeChecked();
  await expect(nowLine).toHaveCount(1);
  expect(await milestones.count()).toBeGreaterThan(0);
  expect(await margins.count()).toBeGreaterThan(0);

  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('split and merge remain reversible without mutating group order', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const chips = page.locator('.dante-timeline-group-chip');
  const readOrder = () =>
    chips.evaluateAll((elements) =>
      elements.map((element) => element.getAttribute('data-group-id')),
    );
  const initialOrder = await readOrder();

  const split = page.getByRole('button', { name: 'Separa per gruppi' });
  await split.click();
  await expect(grid).toHaveClass(/is-expanded/);
  await expect(
    page.getByRole('button', { name: 'Riunisci nella timeline' }),
  ).toHaveAttribute('aria-pressed', 'true');
  expect(await readOrder()).toEqual(initialOrder);

  await page.getByRole('button', { name: 'Riunisci nella timeline' }).click();
  await expect(grid).not.toHaveClass(/is-expanded/);
  await expect(
    page.getByRole('button', { name: 'Separa per gruppi' }),
  ).toHaveAttribute('aria-pressed', 'false');
  expect(await readOrder()).toEqual(initialOrder);
});
