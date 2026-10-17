import { expect, test, type Locator } from '@playwright/test';

test.use({ locale: 'it-IT' });

/** Hit a visible, real card surface, never an offscreen fixed-width lane.
 * Coordinates cached before a horizontal auto-scroll are not safe inputs. */
async function cardBodyPoint(card: Locator): Promise<{ x: number; y: number }> {
  await card.scrollIntoViewIfNeeded();
  return card.evaluate((element) => {
    const bounds = element.getBoundingClientRect();
    const grid = element.closest('.timeline-grid');
    const limit = grid?.getBoundingClientRect();
    if (!limit) throw new Error('Card missing Timeline grid.');
    const left = Math.max(bounds.left + 9, limit.left + 9, 9);
    const right = Math.min(
      bounds.right - 9,
      limit.right - 9,
      window.innerWidth - 9,
    );
    const top = Math.max(bounds.top + 9, limit.top + 9, 9);
    const bottom = Math.min(
      bounds.bottom - 9,
      limit.bottom - 9,
      window.innerHeight - 9,
    );
    if (right <= left || bottom <= top) {
      throw new Error('Timeline card not visible inside its scroll region.');
    }
    for (const yf of [0.7, 0.55, 0.4, 0.85, 0.2]) {
      for (const xf of [0.5, 0.8, 0.2]) {
        const x = left + (right - left) * xf;
        const y = top + (bottom - top) * yf;
        const hit = document.elementFromPoint(x, y);
        if (hit && element.contains(hit) && !hit.closest('button, input, a')) {
          return { x, y };
        }
      }
    }
    throw new Error('No unobstructed Timeline card-body interaction point.');
  });
}


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
  const first = await cardBodyPoint(focused);
  await page.mouse.click(first.x, first.y);
  await expect(focused).toHaveClass(/is-focused/);

  // The target may now occupy a horizontally scrollable lane. Reveal it
  // before taking coordinates, and verify the click target belongs to it.
  const point = await cardBodyPoint(target);
  await page.mouse.move(point.x, point.y);
  await page.mouse.down();
  await page.mouse.move(point.x, point.y + 52, { steps: 5 });

  const overlay = page.locator('.timeline-event-drag-overlay');
  await expect(overlay).toHaveCount(1);
  await expect(overlay).toContainText('Promemoria');

  await page.mouse.up();
  await expect(overlay).toHaveCount(0);
});

test('a simple click on another card retargets focus without retaining stale selection', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const focused = page.locator('[data-timeline-event="7"]');
  const target = page.locator('[data-timeline-event="12"]');
  const first = await cardBodyPoint(focused);
  await page.mouse.click(first.x, first.y);
  await expect(focused).toHaveClass(/is-focused/);

  const second = await cardBodyPoint(target);
  await page.mouse.click(second.x, second.y);
  await expect(focused).not.toHaveClass(/is-focused/);
  await expect(target).toHaveClass(/is-focused/);

  const again = await cardBodyPoint(focused);
  await page.mouse.click(again.x, again.y);
  await expect(target).not.toHaveClass(/is-focused/);
  await expect(focused).toHaveClass(/is-focused/);
  await expect(page.locator('[data-timeline-event="12"]')).toHaveCount(1);
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
  // The fixed-width contract expands the scrollable canvas rather than
  // compressing concurrent cards into a 45%-of-viewport cluster.
  expect(studyBox.x + studyBox.width + 1).toBeLessThanOrEqual(conceptBox.x);
  expect(conceptBox.x + conceptBox.width + 1).toBeLessThanOrEqual(
    reminderBox.x,
  );
  for (const box of [studyBox, conceptBox, reminderBox]) {
    expect(box.width).toBeGreaterThanOrEqual(292);
    expect(box.width).toBeLessThanOrEqual(456);
  }
  const contentRight = reminderBox.x + reminderBox.width;
  const scrollableRight = await grid.evaluate(
    (element) =>
      element.getBoundingClientRect().x +
      element.scrollWidth -
      element.scrollLeft,
  );
  expect(scrollableRight).toBeGreaterThanOrEqual(contentRight);
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

    // The header covers a complete group, possibly containing several
    // fixed-width lanes. An individual card must fit INSIDE its group,
    // not stretch across the entire group header.
    expect(cardBox.x).toBeGreaterThanOrEqual(chipBox.x - 8);
    expect(cardBox.x + cardBox.width).toBeLessThanOrEqual(
      chipBox.x + chipBox.width + 8,
    );
    expect(cardBox.width).toBeGreaterThanOrEqual(292);
    expect(cardBox.width).toBeLessThanOrEqual(456);
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

test('a same-day drag commits once and Undo restores the exact event state', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  await expect(card).toHaveCount(1);

  const originalLabel = await card.getAttribute('aria-label');
  expect(originalLabel).not.toBeNull();

  const box = await card.boundingBox();
  expect(box).not.toBeNull();
  if (!box) {
    throw new Error('Expected same-day drag geometry');
  }

  const startX = box.x + Math.max(12, box.width - 16);
  const startY =
    box.y + Math.min(box.height - 12, Math.max(18, box.height * 0.62));

  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX, startY + 52, { steps: 5 });
  await expect(page.locator('.timeline-event-drag-overlay')).toHaveCount(1);
  await page.mouse.up();

  await expect(page.locator('.timeline-event-drag-overlay')).toHaveCount(0);
  await expect(card).toHaveCount(1);
  await expect(card).not.toHaveAttribute('aria-label', originalLabel ?? '');

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();

  await expect(card).toHaveCount(1);
  await expect(card).toHaveAttribute('aria-label', originalLabel ?? '');
  await expect(page.locator('.timeline-move-toast')).not.toHaveClass(/is-on/);
});

test('keyboard next-day move preserves identity and Undo restores the original day', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  await expect(card).toHaveCount(1);

  const originalLabel = await card.getAttribute('aria-label');
  expect(originalLabel).not.toBeNull();

  const originalDay = await card.evaluate(
    (element) =>
      element.closest<HTMLElement>('[data-timeline-date]')?.dataset
        .timelineDate ?? null,
  );
  expect(originalDay).toBe('2026-08-04');

  await card.focus();
  await card.press('Alt+ArrowRight');

  await expect(card).toHaveCount(1);
  await expect
    .poll(() =>
      card.evaluate(
        (element) =>
          element.closest<HTMLElement>('[data-timeline-date]')?.dataset
            .timelineDate ?? null,
      ),
    )
    .toBe('2026-08-05');
  await expect(card).toHaveAttribute('aria-label', originalLabel ?? '');

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();

  await expect(card).toHaveCount(1);
  await expect
    .poll(() =>
      card.evaluate(
        (element) =>
          element.closest<HTMLElement>('[data-timeline-date]')?.dataset
            .timelineDate ?? null,
      ),
    )
    .toBe('2026-08-04');
  await expect(card).toHaveAttribute('aria-label', originalLabel ?? '');
});

test('calendar keyboard navigation restores focus to its trigger on Escape', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Apri il calendario' });
  await trigger.click();

  const dialog = page.getByRole('dialog', { name: 'Vai a una data' });
  await expect(dialog).toBeVisible();

  const todayCell = page.locator('[data-calendar-date="2026-08-04"]');
  await expect(todayCell).toBeFocused();
  await todayCell.press('ArrowRight');
  await expect(page.locator('[data-calendar-date="2026-08-05"]')).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('Detail owns focus while open and returns it to the exact title opener', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  const titleButton = card.locator('.timeline-event-card__title');
  await titleButton.click();

  const dialog = page.getByRole('dialog', { name: 'Promemoria' });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole('button')).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(titleButton).toBeFocused();
});
