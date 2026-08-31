import { expect, test, type Locator } from '@playwright/test';

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
      element.closest<HTMLElement>('[data-timeline-date]')?.dataset.timelineDate ??
      null,
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
  await expect(lowerCard).toHaveAttribute('aria-label', lowerOriginalLabel ?? '');
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
  await expect(upperCard).toHaveAttribute('aria-label', upperOriginalLabel ?? '');
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
