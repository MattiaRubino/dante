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

test('keyboard nudges keep moved and restored events inside the Timeline viewport', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const grid = page.locator('.timeline-grid');
  const lowerCard = page.locator('[data-timeline-event="12"]');
  await lowerCard.scrollIntoViewIfNeeded();
  await lowerCard.focus();

  for (let index = 0; index < 80; index += 1) {
    await lowerCard.press('Alt+ArrowDown');
  }
  await expectCardInsideTimelineViewport(lowerCard, grid);

  const beforeLastNudge = await lowerCard.getAttribute('aria-label');
  expect(beforeLastNudge).not.toBeNull();
  await lowerCard.press('Alt+ArrowDown');
  await expect(lowerCard).not.toHaveAttribute(
    'aria-label',
    beforeLastNudge ?? '',
  );
  await expectCardInsideTimelineViewport(lowerCard, grid);

  const undoButton = page.locator('.timeline-move-toast.is-on button');
  await expect(undoButton).toBeVisible();
  await undoButton.click();
  await expect(lowerCard).toHaveAttribute('aria-label', beforeLastNudge ?? '');
  await expectCardInsideTimelineViewport(lowerCard, grid);

  const upperCard = page.locator('[data-timeline-event="1"]');
  await upperCard.scrollIntoViewIfNeeded();
  await upperCard.focus();
  for (let index = 0; index < 70; index += 1) {
    await upperCard.press('Alt+ArrowUp');
  }
  await expectCardInsideTimelineViewport(upperCard, grid);
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
