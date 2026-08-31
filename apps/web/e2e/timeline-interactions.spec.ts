import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('custom event dragging never falls back to a native browser drag ghost', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  await page.evaluate(() => {
    const target = window as typeof window & {
      __timelineNativeDragStarts?: number;
    };
    target.__timelineNativeDragStarts = 0;
    document.addEventListener(
      'dragstart',
      () => {
        target.__timelineNativeDragStarts =
          (target.__timelineNativeDragStarts ?? 0) + 1;
      },
      { capture: true },
    );
  });

  const grid = page.locator('.timeline-grid');
  const card = page.locator('[data-timeline-event="12"]');
  await expect(grid).toBeVisible();
  await card.scrollIntoViewIfNeeded();
  await expect(card).toBeVisible();

  for (let index = 0; index < 6; index += 1) {
    const box = await card.boundingBox();
    const gridBox = await grid.boundingBox();
    expect(box).not.toBeNull();
    expect(gridBox).not.toBeNull();
    if (!box || !gridBox) {
      throw new Error('Expected stable Timeline drag geometry');
    }

    const startX = box.x + Math.max(12, box.width - 16);
    const startY =
      box.y + Math.min(box.height - 12, Math.max(18, box.height * 0.62));
    const deltaY = index % 2 === 0 ? 52 : -52;

    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.mouse.move(startX, startY + deltaY, { steps: 5 });

    const overlay = page.locator('.timeline-event-drag-overlay');
    await expect(overlay).toHaveCount(1);
    await expect(overlay).toContainText('Promemoria');

    const overlayBox = await overlay.boundingBox();
    expect(overlayBox).not.toBeNull();
    if (!overlayBox) {
      throw new Error('Expected one-card Timeline drag overlay');
    }
    expect(overlayBox.width).toBeLessThan(gridBox.width * 0.55);

    await page.mouse.up();
    await expect(overlay).toHaveCount(0);
    await expect(card).not.toHaveClass(/is-drag-source/);
  }

  const nativeDragStarts = await page.evaluate(
    () =>
      (window as typeof window & { __timelineNativeDragStarts?: number })
        .__timelineNativeDragStarts ?? 0,
  );
  const selectedText = await page.evaluate(
    () => window.getSelection()?.toString() ?? '',
  );

  expect(nativeDragStarts).toBe(0);
  expect(selectedText).toBe('');
});

test('a focused card never consumes the first drag gesture on another card', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const focused = page.locator('[data-timeline-event="7"]');
  const target = page.locator('[data-timeline-event="12"]');
  await focused.scrollIntoViewIfNeeded();

  const focusedBox = await focused.boundingBox();
  expect(focusedBox).not.toBeNull();
  if (!focusedBox) {
    throw new Error('Expected focus-card geometry');
  }

  await page.mouse.click(
    focusedBox.x + Math.max(12, focusedBox.width - 16),
    focusedBox.y +
      Math.min(focusedBox.height - 12, Math.max(18, focusedBox.height * 0.62)),
  );
  await expect(focused).toHaveClass(/is-focused/);

  const targetBox = await target.boundingBox();
  expect(targetBox).not.toBeNull();
  if (!targetBox) {
    throw new Error('Expected drag-target geometry');
  }

  const startX = targetBox.x + Math.max(12, targetBox.width - 16);
  const startY =
    targetBox.y +
    Math.min(targetBox.height - 12, Math.max(18, targetBox.height * 0.62));

  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX, startY + 52, { steps: 5 });

  const overlay = page.locator('.timeline-event-drag-overlay');
  await expect(overlay).toHaveCount(1);
  await expect(overlay).toContainText('Promemoria');

  await page.mouse.up();
  await expect(overlay).toHaveCount(0);
});

test('compact overlap cards stay in a bounded cluster instead of jumping across the canvas', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const study = page.locator('[data-timeline-event="7"]');
  const concept = page.locator('[data-timeline-event="8"]');
  const reminder = page.locator('[data-timeline-event="12"]');

  await study.scrollIntoViewIfNeeded();
  const gridBox = await grid.boundingBox();
  const studyBox = await study.boundingBox();
  const conceptBox = await concept.boundingBox();
  const reminderBox = await reminder.boundingBox();

  expect(gridBox).not.toBeNull();
  expect(studyBox).not.toBeNull();
  expect(conceptBox).not.toBeNull();
  expect(reminderBox).not.toBeNull();
  if (!gridBox || !studyBox || !conceptBox || !reminderBox) {
    throw new Error('Expected compact overlap geometry');
  }

  expect(studyBox.x).toBeLessThan(conceptBox.x);
  expect(conceptBox.x).toBeLessThan(reminderBox.x);
  expect(reminderBox.x - studyBox.x).toBeLessThan(gridBox.width * 0.45);
  expect(studyBox.width).toBeLessThanOrEqual(480);
  expect(conceptBox.width).toBeLessThanOrEqual(480);
  expect(reminderBox.width).toBeLessThanOrEqual(480);
});

test('expanded group header, event columns and horizontal scroll stay mathematically aligned', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/home');

  await page.getByRole('button', { name: 'Separa per gruppi' }).click();
  const grid = page.locator('.timeline-grid');
  const groupScroller = page.locator('.dante-timeline-group-scroller');
  await expect(grid).toHaveClass(/is-expanded/);

  const chips = page.locator('.dante-timeline-group-chip');
  const samples = [
    { chip: 0, eventId: '7' },
    { chip: 3, eventId: '8' },
    { chip: 4, eventId: '12' },
  ] as const;

  for (const sample of samples) {
    const chipBox = await chips.nth(sample.chip).boundingBox();
    const cardBox = await page
      .locator(`[data-timeline-event="${sample.eventId}"]`)
      .boundingBox();
    expect(chipBox).not.toBeNull();
    expect(cardBox).not.toBeNull();
    if (!chipBox || !cardBox) {
      throw new Error('Expected expanded group alignment geometry');
    }

    expect(Math.abs(cardBox.x - chipBox.x)).toBeLessThanOrEqual(8);
    expect(Math.abs(cardBox.width - chipBox.width)).toBeLessThanOrEqual(10);
  }

  const maxGridScroll = await grid.evaluate(
    (element) => element.scrollWidth - element.clientWidth,
  );
  expect(maxGridScroll).toBeGreaterThan(0);

  const targetScroll = Math.min(120, maxGridScroll);
  await grid.evaluate((element, value) => {
    element.scrollLeft = value;
    element.dispatchEvent(new Event('scroll', { bubbles: true }));
  }, targetScroll);

  await expect
    .poll(() => groupScroller.evaluate((element) => element.scrollLeft))
    .toBeCloseTo(targetScroll, 0);
});
