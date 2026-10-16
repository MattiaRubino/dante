import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

test('Create stays in the desktop Context Rail, keeps Timeline scroll available, and bounds Advanced', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  const rail = page.locator('[data-home-region="context-rail"]');
  const host = rail.locator('[data-home-context-create-host]');
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  expect(
    await host.evaluate((element) =>
      element.contains(
        document.querySelector('[data-temporal-create="composer"]'),
      ),
    ),
  ).toBe(true);

  const close = dialog.locator('.dante-temporal-panel-close');
  await expect(close).toBeVisible();
  await expect(close).toHaveAttribute('aria-label', /.+/);
  await expect(
    dialog.locator('.temporal-create-composer__header button'),
  ).toHaveCount(2);

  const railBox = await rail.boundingBox();
  const quickBox = await dialog.boundingBox();
  if (!railBox || !quickBox) {
    throw new Error('Expected rail-mounted Create geometry');
  }
  const hostBox = await host.boundingBox();
  const geometry = JSON.stringify({ railBox, hostBox, quickBox });
  // Quick Create replaces the Context Rail from the Timeline's own top edge.
  // It is not a viewport-fixed third panel above the Timeline.
  expect(
    await host.evaluate((element) => getComputedStyle(element).position),
  ).toBe('absolute');
  expect(Math.abs(quickBox.y - railBox.y), geometry).toBeLessThanOrEqual(2);
  expect(quickBox.x, geometry).toBeGreaterThanOrEqual(railBox.x - 1);
  expect(quickBox.x + quickBox.width, geometry).toBeLessThanOrEqual(
    railBox.x + railBox.width + 1,
  );
  expect(Math.abs(quickBox.height - railBox.height), geometry).toBeLessThanOrEqual(
    2,
  );

  const backdrop = page.locator('[data-temporal-create="backdrop"]');
  const backdropStyle = await backdrop.evaluate((element) => {
    const style = getComputedStyle(element);
    return {
      pointerEvents: style.pointerEvents,
      backgroundColor: style.backgroundColor,
    };
  });
  expect(backdropStyle.pointerEvents).toBe('none');
  expect(backdropStyle.backgroundColor).toBe('rgba(0, 0, 0, 0)');

  const pin = dialog.getByRole('button', {
    name: 'Mantieni aperto il pannello Crea',
  });
  await pin.click();
  await expect(
    dialog.getByRole('button', { name: 'Sblocca pannello Crea' }),
  ).toHaveAttribute('aria-pressed', 'true');

  const timeline = page.locator('.timeline-grid');
  await timeline.evaluate((element) => {
    element.scrollTop = 0;
  });
  const timelineBox = await timeline.boundingBox();
  if (!timelineBox) {
    throw new Error('Expected visible Timeline');
  }
  await page.mouse.move(
    timelineBox.x + timelineBox.width - 40,
    timelineBox.y + Math.min(180, timelineBox.height / 2),
  );
  await page.mouse.wheel(0, 520);
  await expect
    .poll(() => timeline.evaluate((element) => element.scrollTop))
    .toBeGreaterThan(0);
  await expect(dialog).toBeVisible();

  await dialog.getByRole('button', { name: 'Sblocca pannello Crea' }).click();
  const advanced = dialog.getByRole('button', { name: 'Opzioni avanzate' });
  await expect(advanced).toHaveAttribute('aria-expanded', 'false');
  await advanced.click();
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );
  await expect(
    dialog.locator('[data-create-advanced="activity"]'),
  ).toBeVisible();

  const expanded = await dialog.boundingBox();
  if (!expanded) {
    throw new Error('Expected Advanced Create geometry');
  }
  expect(expanded.x).toBeGreaterThanOrEqual(0);
  expect(expanded.y).toBeGreaterThanOrEqual(0);
  expect(expanded.x + expanded.width).toBeLessThanOrEqual(1440.5);
  expect(expanded.y + expanded.height).toBeLessThanOrEqual(900.5);

  const body = dialog.locator('.temporal-create-composer__body');
  await expect(body).toBeVisible();
  await body.evaluate((element) => {
    element.scrollTop = element.scrollHeight;
  });
  await expect(close).toBeInViewport();
  await expect(dialog.locator('.temporal-create-actions')).toBeInViewport();

  const back = dialog.getByRole('button', {
    name: 'Nascondi opzioni avanzate',
  });
  await expect(back).toHaveAttribute('aria-expanded', 'true');
  await back.click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.locator('[data-create-advanced]')).toHaveCount(0);

  // Recurrence has moved to Advanced; retain the custom-path assertion
  // without expecting a removed select in the quick surface.
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await dialog.getByLabel('Ripeti', { exact: true }).selectOption('custom');
  await expect(
    dialog.locator('[data-create-recurrence-owner="routine"]'),
  ).toBeVisible();
});

test('Quick Create keeps the Timeline rail origin and height while its fields change', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 1300 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  const timeline = page.locator('.home-timeline');
  const rail = page.locator('[data-home-region="context-rail"]');
  const assertRailGeometry = async () => {
    // The replacement must not shrink during the generic Create entrance.
    expect(
      await dialog.evaluate((element) => getComputedStyle(element).animationName),
    ).toBe('none');
    const [timelineBox, railBox, quickBox] = await Promise.all([
      timeline.boundingBox(),
      rail.boundingBox(),
      dialog.boundingBox(),
    ]);
    if (!timelineBox || !railBox || !quickBox) {
      throw new Error('Expected desktop Timeline and rail geometry');
    }
    expect(Math.abs(quickBox.y - timelineBox.y)).toBeLessThanOrEqual(2);
    expect(Math.abs(quickBox.y - railBox.y)).toBeLessThanOrEqual(2);
    expect(Math.abs(quickBox.height - railBox.height)).toBeLessThanOrEqual(2);
  };

  await assertRailGeometry();
  await dialog.getByRole('button', { name: 'Evento', exact: true }).click();
  await assertRailGeometry();
  await dialog.getByRole('button', { name: 'Attività', exact: true }).click();
  await assertRailGeometry();
});
