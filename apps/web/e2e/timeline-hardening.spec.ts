import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function expectCardInsideTimelineViewport(
  card: Locator,
  grid: Locator,
): Promise<void> {
  await expect
    .poll(async () => {
      const [cardBox, gridBox] = await Promise.all([
        card.boundingBox(),
        grid.boundingBox(),
      ]);
      if (!cardBox || !gridBox) {
        return false;
      }
      return (
        cardBox.y >= gridBox.y - 1 &&
        cardBox.y + cardBox.height <= gridBox.y + gridBox.height + 1
      );
    })
    .toBe(true);
}

async function timelineDateFor(card: Locator): Promise<string | null> {
  return card.evaluate(
    (element) =>
      element.closest<HTMLElement>('[data-timeline-date]')?.dataset
        .timelineDate ?? null,
  );
}

async function renderedTimelineDates(page: Page): Promise<string[]> {
  return page
    .locator('[data-timeline-date]')
    .evaluateAll((elements) =>
      elements
        .map((element) => (element as HTMLElement).dataset.timelineDate ?? '')
        .filter(Boolean),
    );
}

function dayDistance(fromDateKey: string, toDateKey: string): number {
  const millisecondsPerDay = 24 * 60 * 60 * 1000;
  return Math.round(
    (Date.parse(`${toDateKey}T00:00:00Z`) -
      Date.parse(`${fromDateKey}T00:00:00Z`)) /
      millisecondsPerDay,
  );
}

test('unchanged time save preserves the previous real move feedback and Undo', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  await expect(card).toHaveCount(1);

  const originalLabel = await card.getAttribute('aria-label');
  expect(originalLabel).not.toBeNull();

  await card.focus();
  await card.press('Alt+ArrowDown');
  await expect(card).not.toHaveAttribute('aria-label', originalLabel ?? '');

  const toast = page.locator('.timeline-move-toast.is-on');
  await expect(toast).toBeVisible();
  const moveFeedback = await toast.textContent();
  expect(moveFeedback).not.toBeNull();

  await card
    .getByRole('button', { name: 'Modifica orario di Promemoria' })
    .click();
  const dialog = page.getByRole('dialog', { name: 'Modifica orario' });
  await expect(dialog).toBeVisible();

  await dialog.getByRole('button', { name: 'Conferma' }).click();
  await expect(dialog).toHaveCount(0);

  await expect(toast).toBeVisible();
  await expect(toast).toHaveText(moveFeedback ?? '');

  await toast.getByRole('button', { name: 'Annulla' }).click();
  await expect(card).toHaveAttribute('aria-label', originalLabel ?? '');
});

test('keyboard nudge sequences stay visible and Undo returns to the sequence origin', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const lowerCard = page.locator('[data-timeline-event="12"]');
  await lowerCard.scrollIntoViewIfNeeded();
  const lowerOriginalLabel = await lowerCard.getAttribute('aria-label');
  expect(lowerOriginalLabel).not.toBeNull();
  await lowerCard.focus();

  for (let index = 0; index < 80; index += 1) {
    await lowerCard.press('Alt+ArrowDown');
  }
  await expect(lowerCard).not.toHaveAttribute(
    'aria-label',
    lowerOriginalLabel ?? '',
  );
  await expectCardInsideTimelineViewport(lowerCard, grid);

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();
  await expect(lowerCard).toHaveAttribute(
    'aria-label',
    lowerOriginalLabel ?? '',
  );
  await expectCardInsideTimelineViewport(lowerCard, grid);

  const upperCard = page.locator('[data-timeline-event="1"]');
  await upperCard.scrollIntoViewIfNeeded();
  const upperOriginalLabel = await upperCard.getAttribute('aria-label');
  expect(upperOriginalLabel).not.toBeNull();
  await upperCard.focus();
  for (let index = 0; index < 70; index += 1) {
    await upperCard.press('Alt+ArrowUp');
  }
  await expect(upperCard).not.toHaveAttribute(
    'aria-label',
    upperOriginalLabel ?? '',
  );
  await expectCardInsideTimelineViewport(upperCard, grid);

  await expect(undoButton).toBeVisible();
  await undoButton.click();
  await expect(upperCard).toHaveAttribute(
    'aria-label',
    upperOriginalLabel ?? '',
  );
  await expectCardInsideTimelineViewport(upperCard, grid);
});

test('keyboard nudges cross midnight, retain focus, and Undo restores the origin', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const card = page.locator('[data-timeline-event="8"]');
  await card.scrollIntoViewIfNeeded();

  await card
    .getByRole('button', { name: 'Modifica orario di Revisione concept' })
    .click();
  const dialog = page.getByRole('dialog', { name: 'Modifica orario' });
  await expect(dialog).toBeVisible();
  await page.getByLabel('Inizio ore').fill('23');
  await page.getByLabel('Inizio minuti').fill('10');
  await page.getByLabel('Fine ore').fill('23');
  await page.getByLabel('Fine minuti').fill('55');
  await dialog.getByRole('button', { name: 'Conferma' }).click();
  await expect(dialog).toHaveCount(0);

  const sequenceOriginLabel = await card.getAttribute('aria-label');
  expect(sequenceOriginLabel).toContain('23:10–23:55');
  expect(await timelineDateFor(card)).toBe('2026-08-04');

  await card.focus();
  await card.press('Alt+ArrowDown');
  await expect(card).toHaveAttribute(
    'aria-label',
    /Revisione concept, 23:15–24:00/,
  );

  await page.keyboard.press('Alt+ArrowDown');
  await expect.poll(() => timelineDateFor(card)).toBe('2026-08-05');
  await expect(card).toHaveAttribute(
    'aria-label',
    /Revisione concept, 00:00–00:45/,
  );
  await expect(card).toBeFocused();
  await expectCardInsideTimelineViewport(card, grid);

  await expect
    .poll(() =>
      card.evaluate((element) => getComputedStyle(element).outlineOffset),
    )
    .toBe('-2px');

  const focusColors = await card.evaluate((element) => {
    const style = getComputedStyle(element);
    const probe = document.createElement('span');
    probe.style.color = style.getPropertyValue('--timeline-group-color');
    document.body.appendChild(probe);
    const groupColor = getComputedStyle(probe).color;
    probe.remove();
    return {
      outlineColor: style.outlineColor,
      groupColor,
    };
  });
  expect(focusColors.outlineColor).toBe(focusColors.groupColor);

  await page.keyboard.press('Alt+ArrowDown');
  await expect(card).toHaveAttribute(
    'aria-label',
    /Revisione concept, 00:05–00:50/,
  );
  await expect(card).toBeFocused();

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();

  await expect.poll(() => timelineDateFor(card)).toBe('2026-08-04');
  await expect(card).toHaveAttribute('aria-label', sequenceOriginLabel ?? '');
  await expectCardInsideTimelineViewport(card, grid);
});

test('relative temporal scrubber keeps advancing while held without a native-thumb reset', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const scrubber = page.locator('[data-temporal-scrubber="relative"]');
  const thumb = scrubber.locator('.timeline-temporal-scrubber__thumb');

  await expect(grid).toHaveAttribute('data-temporal-scroll', 'relative');
  await expect(scrubber).toHaveCount(1);
  await expect(thumb).toHaveCount(1);

  const initialDates = await renderedTimelineDates(page);
  const mountedCount = initialDates.length;
  const initialFirst = initialDates[0] ?? '';

  // The Timeline lives below the Home hero. Pointer coordinates are viewport-
  // relative, so bring the actual scrubber into the viewport before deriving
  // coordinates for the pointer-capture regression.
  await scrubber.scrollIntoViewIfNeeded();
  await expect(scrubber).toBeInViewport();

  const box = await scrubber.boundingBox();
  expect(box).not.toBeNull();
  if (!box) {
    return;
  }

  const x = box.x + box.width / 2;
  const neutralY = box.y + box.height * 0.34;
  const bottomY = box.y + box.height - 3;

  await page.mouse.move(x, neutralY);
  await page.mouse.down();
  await page.mouse.move(x, bottomY, { steps: 8 });
  await expect(scrubber).toHaveAttribute('data-active', 'true');

  await expect
    .poll(async () => (await renderedTimelineDates(page))[0] ?? '')
    .not.toBe(initialFirst);

  const firstAfterInitialAdvance = (await renderedTimelineDates(page))[0] ?? '';

  await expect
    .poll(async () => (await renderedTimelineDates(page))[0] ?? '')
    .not.toBe(firstAfterInitialAdvance);

  const firstWhileHeld = (await renderedTimelineDates(page))[0] ?? '';
  expect(dayDistance(initialFirst, firstWhileHeld)).toBeGreaterThan(2);
  expect(await renderedTimelineDates(page)).toHaveLength(mountedCount);

  await page.mouse.move(x, box.y + box.height + 100);
  const firstBeforeOutsideHold = (await renderedTimelineDates(page))[0] ?? '';
  await expect
    .poll(async () => (await renderedTimelineDates(page))[0] ?? '')
    .not.toBe(firstBeforeOutsideHold);

  await page.mouse.up();
  await expect(scrubber).not.toHaveAttribute('data-active', 'true');
  await expect
    .poll(() => thumb.evaluate((element) => element.style.transform))
    .toBe('');
  await expect(thumb).toHaveCount(1);

  await page.locator('.dante-timeline-now').click();
  await expect
    .poll(async () => renderedTimelineDates(page))
    .toContain('2026-08-04');
});

test('Timeline viewport remains keyboard-scrollable without relying on a native vertical thumb', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  await grid.focus();
  await expect(grid).toBeFocused();

  const before = await grid.evaluate((element) => element.scrollTop);
  await page.keyboard.press('PageDown');
  await expect
    .poll(() => grid.evaluate((element) => element.scrollTop))
    .toBeGreaterThan(before);

  const afterDown = await grid.evaluate((element) => element.scrollTop);
  await page.keyboard.press('ArrowUp');
  await expect
    .poll(() => grid.evaluate((element) => element.scrollTop))
    .toBeLessThan(afterDown);
});

test('continuous scroll recycles a bounded window far beyond the old hard limit and Now recovers', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  await expect(grid).toBeVisible();

  const initialDates = await renderedTimelineDates(page);
  expect(initialDates.length).toBeGreaterThan(0);
  const mountedCount = initialDates.length;
  const initialFirst = initialDates[0];
  expect(initialFirst).toBeTruthy();

  let previousFirst = initialFirst ?? '';
  for (let index = 0; index < 10; index += 1) {
    await grid.evaluate((element) => {
      element.scrollTop = Math.max(
        0,
        element.scrollHeight - element.clientHeight - 1,
      );
    });
    await expect
      .poll(async () => (await renderedTimelineDates(page))[0] ?? '')
      .not.toBe(previousFirst);

    const dates = await renderedTimelineDates(page);
    expect(dates).toHaveLength(mountedCount);
    previousFirst = dates[0] ?? '';
  }

  const futureDates = await renderedTimelineDates(page);
  const futureFirst = futureDates[0] ?? '';
  expect(dayDistance(initialFirst ?? '', futureFirst)).toBeGreaterThan(14);
  await expect(
    page.locator('.dante-timeline-week [aria-current="date"]'),
  ).toHaveCount(1);

  await page.locator('.dante-timeline-now').click();
  await expect
    .poll(async () => renderedTimelineDates(page))
    .toContain('2026-08-04');
  await expect(page.locator('.timeline-now-line')).toBeVisible();

  const resetDates = await renderedTimelineDates(page);
  previousFirst = resetDates[0] ?? '';
  for (let index = 0; index < 10; index += 1) {
    await grid.evaluate((element) => {
      element.scrollTop = 1;
    });
    await expect
      .poll(async () => (await renderedTimelineDates(page))[0] ?? '')
      .not.toBe(previousFirst);

    const dates = await renderedTimelineDates(page);
    expect(dates).toHaveLength(mountedCount);
    previousFirst = dates[0] ?? '';
  }

  const pastDates = await renderedTimelineDates(page);
  const pastFirst = pastDates[0] ?? '';
  expect(dayDistance(pastFirst, resetDates[0] ?? '')).toBeGreaterThan(14);

  await page.locator('.dante-timeline-now').click();
  await expect
    .poll(async () => renderedTimelineDates(page))
    .toContain('2026-08-04');
  await expect(page.locator('.timeline-now-line')).toBeVisible();
});

test('keyboard movement across a mounted-window edge reanchors without losing the card', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const card = page.locator('[data-timeline-event="302"]');
  await expect(card).toHaveCount(1);
  expect(await timelineDateFor(card)).toBe('2026-08-07');

  await card.evaluate((element) => {
    (element as HTMLElement).focus({
      preventScroll: true,
      focusVisible: true,
    });
  });
  await page.keyboard.press('Alt+ArrowRight');

  await expect.poll(() => timelineDateFor(card)).toBe('2026-08-08');
  await expect(card).toBeFocused();
  await expectCardInsideTimelineViewport(card, grid);
  await expect
    .poll(async () => renderedTimelineDates(page))
    .toContain('2026-08-08');

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();

  await expect.poll(() => timelineDateFor(card)).toBe('2026-08-07');
  await expectCardInsideTimelineViewport(card, grid);
});

test('reduced motion prevents imperative smooth Timeline navigation', async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  await expect(grid).toBeVisible();

  await grid.evaluate((element) => {
    const target = element as HTMLDivElement & {
      __timelineScrollToCalls?: number;
    };
    target.__timelineScrollToCalls = 0;
    Object.defineProperty(target, 'scrollTo', {
      configurable: true,
      value: () => {
        target.__timelineScrollToCalls =
          (target.__timelineScrollToCalls ?? 0) + 1;
      },
    });
  });

  await page.getByRole('button', { name: /5 agosto 2026/i }).click();

  await expect
    .poll(() =>
      grid.evaluate(
        (element) =>
          (element as HTMLDivElement & { __timelineScrollToCalls?: number })
            .__timelineScrollToCalls ?? 0,
      ),
    )
    .toBe(0);
});
