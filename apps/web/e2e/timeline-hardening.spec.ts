import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('recurrence scope replaces the Inspector visually and remains interactive', async ({
  page,
}) => {
  await page.goto('/home');
  await expect(page.locator('.timeline-now-line').first()).toBeVisible();
  const visibility = await page.evaluate(() => {
    const inspector = document.createElement('div');
    inspector.className =
      'timeline-modal-backdrop timeline-modal-backdrop--inspector is-open';
    const scope = document.createElement('div');
    scope.className = 'timeline-recurring-edit-scope-dialog__backdrop';
    scope.innerHTML =
      '<section class="timeline-recurring-edit-scope-dialog"><h2>Modifica ricorrenza</h2><p>Questa attività fa parte di una ricorrenza.</p><button>Solo questa istanza</button></section>';
    document.body.append(inspector, scope);
    const inspectorStyle = getComputedStyle(inspector);
    const scopeStyle = getComputedStyle(scope);
    const dialog = scope.querySelector('section')!;
    const button = dialog.querySelector('button')!;
    const result = {
      inspector: inspectorStyle.visibility,
      scope: scopeStyle.visibility,
      onTop: Number(scopeStyle.zIndex) > Number(inspectorStyle.zIndex),
      dialogColor: getComputedStyle(dialog).color,
      dialogBackground: getComputedStyle(dialog).backgroundColor,
      buttonColor: getComputedStyle(button).color,
      buttonBackground: getComputedStyle(button).backgroundColor,
      centered:
        Math.abs(
          dialog.getBoundingClientRect().left +
            dialog.getBoundingClientRect().width / 2 -
            window.innerWidth / 2,
        ) < 2,
    };
    inspector.remove();
    scope.remove();
    return result;
  });
  expect(visibility).toEqual({
    inspector: 'hidden',
    scope: 'visible',
    onTop: true,
    dialogColor: 'rgb(242, 244, 242)',
    dialogBackground: 'rgb(25, 35, 40)',
    buttonColor: 'rgb(242, 244, 242)',
    buttonBackground: 'rgb(38, 52, 59)',
    centered: true,
  });
});

test('current-time marker keeps a visible line across the whole day', async ({
  page,
}) => {
  await page.goto('/home');
  for (const view of ['Timeline', 'Giorno', 'Timeline']) {
    await page.getByRole('button', { name: 'Scegli vista Timeline' }).click();
    await page.getByRole('menuitemradio', { name: view }).click();
    const line = page.locator('.timeline-now-line').first();
    await expect(line).toBeVisible();
    const style = await line.evaluate((element) => {
      const computed = getComputedStyle(element);
      return {
        image: computed.backgroundImage,
        color: computed.backgroundColor,
        height: element.getBoundingClientRect().height,
        width: element.getBoundingClientRect().width,
        viewport: element.closest('.timeline-grid')?.getBoundingClientRect()
          .width,
      };
    });
    expect(style.image).toBe('none');
    expect(style.color).not.toBe('rgba(0, 0, 0, 0)');
    expect(style.height).toBeGreaterThanOrEqual(2);
    expect(style.width).toBeGreaterThan(100);
    expect(style.width).toBeGreaterThan((style.viewport ?? 0) * 0.9);
  }
});

test('Inspector keeps its actions above the title and places date and Life Area on distinct rows', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');
  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  await card.locator('.timeline-event-card__title').click();
  const inspector = page.locator('.timeline-event-modal--inspector');
  await expect(inspector).toBeVisible();
  await expect(
    inspector.locator('.timeline-event-modal__header-actions'),
  ).toBeVisible();
  await expect(
    inspector.locator('.timeline-event-modal__schedule-row'),
  ).toBeVisible();
  await expect(
    inspector.locator('.timeline-event-modal__time'),
  ).not.toContainText('Europe/Rome');
  const order = await inspector.evaluate((element) => {
    const toolbar = element.querySelector('.timeline-event-modal__header');
    const title = element.querySelector('.timeline-event-modal__title');
    const schedule = element.querySelector(
      '.timeline-event-modal__schedule-row',
    );
    return [toolbar, title, schedule].map(
      (item) => item?.getBoundingClientRect().top ?? -1,
    );
  });
  expect(order[0]).toBeLessThan(order[1]!);
  expect(order[1]).toBeLessThan(order[2]!);
  const rect = await inspector.boundingBox();
  expect(rect).not.toBeNull();
  expect(rect!.x).toBeGreaterThanOrEqual(0);
  expect(rect!.x + rect!.width).toBeLessThanOrEqual(390);
});

test('Inspector uses equal main and internal buttons without overflowing a long Objective', async ({
  page,
}) => {
  await page.setViewportSize({ width: 720, height: 840 });
  await page.goto('/home');
  for (const path of [
    'src/features/temporal/session-subject-controls.css',
    'src/features/temporal/activity-session-card-controls.css',
    'src/features/temporal/objective-controls.css',
    'src/features/home/ui/timeline/timeline.css',
  ]) {
    await page.addStyleTag({ path });
  }
  const geometry = await page.evaluate(() => {
    const root = document.createElement('div');
    root.className = 'timeline-event-modal timeline-event-modal--inspector';
    root.innerHTML = `<div class="timeline-event-modal__schedule-row">
      <p class="timeline-event-modal__time">Domenica 18 ottobre · 13:30–14:00</p>
      <div class="timeline-activity-session-card-controls"><div class="timeline-session-controls">
        <div class="timeline-session-controls__runtime-actions"><button class="timeline-session-controls__runtime-button">▶</button></div>
      </div></div>
    </div>
    <div class="timeline-activity-planned-sessions"><div class="timeline-activity-planned-sessions__row">
      <div class="timeline-activity-planned-sessions__summary">Sessione</div>
      <div class="timeline-session-controls__runtime-actions"><button class="timeline-session-controls__runtime-button">▶</button></div>
    </div></div>
    <div class="timeline-objective-controls"><div class="timeline-objective-controls__item">
      <div class="timeline-objective-controls__summary">
        <span class="timeline-objective-controls__name">${'Obiettivo lunghissimo '.repeat(15)}</span>
        <small>Obiettivo ≥ 12 mele</small>
      </div>
    </div></div>`;
    document.body.appendChild(root);
    const buttons = [
      ...root.querySelectorAll('.timeline-session-controls__runtime-button'),
    ].map((button) => button.getBoundingClientRect());
    const name = root
      .querySelector('.timeline-objective-controls__name')!
      .getBoundingClientRect();
    const target = root
      .querySelector('.timeline-objective-controls__summary small')!
      .getBoundingClientRect();
    const result = {
      buttonSizes: buttons.map((button) => [button.width, button.height]),
      nameFits: name.right <= target.left + 1,
      targetFits: target.right <= root.getBoundingClientRect().right + 1,
    };
    root.remove();
    return result;
  });
  expect(geometry).toEqual({
    buttonSizes: [
      [30, 30],
      [30, 30],
    ],
    nameFits: true,
    targetFits: true,
  });
});

test('Activity Edit keeps quantity fields on one row at desktop width', async ({
  page,
}) => {
  await page.setViewportSize({ width: 900, height: 800 });
  await page.goto('/home');
  await page.addStyleTag({
    path: 'src/features/temporal-create/ui/temporal-create-objectives.css',
  });
  const fields = await page.evaluate(() => {
    const root = document.createElement('div');
    root.style.width = '680px';
    root.innerHTML = `<div class="temporal-create-objective is-edit">
      <div class="temporal-create-objective__definition">
        <label><span>Risultato</span><select><option>Quantità</option></select></label>
        <label><span>Regola</span><select><option>≥</option></select></label>
        <label><span>Target</span><input type="number" /></label>
        <label><span>Unità</span><input value="mele" /></label>
      </div>
    </div>`;
    document.body.appendChild(root);
    const definition = root.querySelector(
      '.temporal-create-objective__definition',
    )!;
    const bounds = [...definition.querySelectorAll('label')].map((field) =>
      field.getBoundingClientRect(),
    );
    const right = definition.getBoundingClientRect().right;
    const result = {
      sameRow: bounds.every(
        (field) => Math.abs(field.top - bounds[0]!.top) < 1,
      ),
      fits: bounds.every((field) => field.right <= right + 1),
    };
    root.remove();
    return result;
  });
  expect(fields).toEqual({ sameRow: true, fits: true });
});

test('Activity Edit places Add interval below the time row with a readable button', async ({
  page,
}) => {
  await page.goto('/home');
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });
  await page.addStyleTag({
    path: 'src/features/temporal-create/ui/temporal-create-activity-polish.css',
  });
  const geometry = await page.evaluate(() => {
    const root = document.createElement('section');
    root.className = 'timeline-event-modal--edit';
    root.style.width = '680px';
    root.innerHTML = `<section class="timeline-activity-editor__readback" aria-label="Programmazione attuale">
      <ul><li><div class="temporal-create-activity-interval__fields" style="height:46px">
        <button type="button" style="height:46px">19 ott</button>
      </div></li></ul>
      <div class="temporal-create-activity-intervals timeline-activity-editor__intervals">
        <button type="button" class="temporal-create-activity-intervals__add">
          <span aria-hidden="true">＋</span> Aggiungi intervallo
        </button>
      </div>
    </section>`;
    document.body.appendChild(root);
    const time = root.querySelector(
      '.temporal-create-activity-interval__fields',
    )!;
    const button = root.querySelector<HTMLButtonElement>(
      '.temporal-create-activity-intervals__add',
    )!;
    const result = {
      gap:
        button.getBoundingClientRect().top -
        time.getBoundingClientRect().bottom,
      height: button.getBoundingClientRect().height,
      fontSize: Number.parseFloat(getComputedStyle(button).fontSize),
      text: button.textContent?.trim(),
    };
    root.remove();
    return result;
  });
  expect(geometry.gap).toBeGreaterThanOrEqual(8);
  expect(geometry.height).toBeGreaterThanOrEqual(36);
  expect(geometry.fontSize).toBeGreaterThanOrEqual(12);
  expect(geometry.text).toContain('Aggiungi intervallo');
});

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

test('a long Activity title stays on one ellipsized line', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  // The non-auth /home fixture has generic Timeline cards but no persisted
  // scheduled-activity owner. Apply only the Activity presentation class to a
  // known fixture card: this checks the real browser CSS cascade without
  // relying on unavailable backend records or fabricating a Session.
  const card = page.locator('[data-timeline-event="7"]');
  await card.scrollIntoViewIfNeeded();
  await card.evaluate((element) => {
    element.classList.add('timeline-event-card--activity');
  });
  const title = card.locator('.timeline-event-card__title');
  await expect(title).toBeVisible();

  // Measure the production Activity style (not jsdom). The full title
  // remains accessible while its rendered preview is one ellipsized line.
  const result = await title.evaluate((element) => {
    element.textContent = 'L'.repeat(140);
    const css = getComputedStyle(element);
    return {
      whitespace: css.whiteSpace,
      overflow: css.overflow,
      textOverflow: css.textOverflow,
      height: element.getBoundingClientRect().height,
      lineHeight: Number.parseFloat(css.lineHeight),
      scrollWidth: element.scrollWidth,
      clientWidth: element.clientWidth,
    };
  });
  expect(result.whitespace).toBe('nowrap');
  expect(result.overflow).toBe('hidden');
  expect(result.textOverflow).toBe('ellipsis');
  expect(result.height).toBeLessThan(result.lineHeight * 1.5);
  expect(result.scrollWidth).toBeGreaterThan(result.clientWidth);
});

test('Session Objective and agenda indicators sit near the lower card edge', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const event = page.locator('[data-timeline-event="2"]');
  await event.scrollIntoViewIfNeeded();
  const footer = event.locator('.timeline-event-card__indicators');
  const agenda = footer.locator('.timeline-event-card__indicator');
  await expect(agenda).toContainText('Scaletta');
  const distanceFromBottom = await event.evaluate((element) => {
    const indicator = element.querySelector('.timeline-event-card__indicator');
    if (!indicator) return Infinity;
    return (
      element.getBoundingClientRect().bottom -
      indicator.getBoundingClientRect().bottom
    );
  });
  // With an Event expander, reserve 30px for its command at the bottom.
  expect(distanceFromBottom).toBeGreaterThanOrEqual(0);
  expect(distanceFromBottom).toBeLessThanOrEqual(38);
});

test('title drag previews the same 15-minute destination as drop', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  const title = card.locator('.timeline-event-card__title');
  await expect(title).toHaveCSS('cursor', 'default');
  const bounds = await title.boundingBox();
  expect(bounds).not.toBeNull();
  if (!bounds) return;

  const x = bounds.x + Math.min(bounds.width / 2, 28);
  const y = bounds.y + bounds.height / 2;
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x, y + 70, { steps: 8 });

  const overlay = page.locator('.timeline-event-drag-overlay');
  const marker = page.locator('[data-timeline-drag-ruler-marker]');
  await expect(overlay).toBeVisible();
  await expect(marker).toBeVisible();
  await expect(page.locator('[data-home-region="timeline"]')).toHaveAttribute(
    'data-timeline-card-dragging',
    'true',
  );

  const preview = await overlay.getAttribute('data-drag-preview-time');
  expect(preview).toMatch(/^\d{2}:\d{2}–\d{2}:\d{2}$/);
  if (!preview) return;
  const start = preview.slice(0, 5);
  const startMinute = Number(start.slice(0, 2)) * 60 + Number(start.slice(3));
  expect(startMinute % 15).toBe(0);
  await expect(marker).toHaveText(start);

  await page.mouse.up();
  await expect(overlay).toHaveCount(0);
  await expect(marker).toHaveCount(0);
  await expect(page.locator('[data-home-region="timeline"]')).toHaveAttribute(
    'data-timeline-card-dragging',
    'false',
  );
  await expect(card.locator('.timeline-event-card__time')).toContainText(
    preview,
  );
  await expect(page.locator('.timeline-event-modal--inspector')).toHaveCount(0);
});

test('card clock is informative rather than hover-editable', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const card = page.locator('[data-timeline-event="12"]');
  await card.scrollIntoViewIfNeeded();
  const clock = card.locator('.timeline-event-card__time');
  const color = await clock.evaluate(
    (element) => getComputedStyle(element).color,
  );
  await clock.hover();
  await expect(clock).toHaveCSS('cursor', 'default');
  await expect(clock).toHaveCSS('color', color);
});

test('a keyboard nudge preserves its feedback and Undo', async ({ page }) => {
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

test('temporal scrubber reads as a scrollbar handle and stays distinct from the expansion handle', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 760 });
  await page.goto('/home');

  const scrubber = page.locator('[data-temporal-scrubber="relative"]');
  const thumb = scrubber.locator('.timeline-temporal-scrubber__thumb');
  const expansionThumb = page.locator('.timeline-expansion-handle > span');

  await scrubber.scrollIntoViewIfNeeded();
  await expect(scrubber).toBeInViewport();
  await expect(thumb).toBeVisible();
  await expect(expansionThumb).toBeVisible();

  const thumbBox = await thumb.boundingBox();
  expect(thumbBox).not.toBeNull();
  if (!thumbBox) {
    return;
  }
  expect(thumbBox.width).toBeGreaterThanOrEqual(4);
  expect(thumbBox.height).toBeGreaterThanOrEqual(40);
  expect(thumbBox.height / thumbBox.width).toBeGreaterThan(7);

  const [scrubberColor, expansionColor, activeColor] = await Promise.all([
    thumb.evaluate((element) => getComputedStyle(element).backgroundColor),
    expansionThumb.evaluate(
      (element) => getComputedStyle(element).backgroundColor,
    ),
    page.evaluate(() => {
      const probe = document.createElement('span');
      probe.style.position = 'fixed';
      probe.style.visibility = 'hidden';
      probe.style.background = 'var(--dante-semantic-color-home-chrome-active)';
      document.body.append(probe);
      const color = getComputedStyle(probe).backgroundColor;
      probe.remove();
      return color;
    }),
  ]);

  expect(activeColor).not.toBe('');
  expect(activeColor).not.toBe('rgba(0, 0, 0, 0)');
  expect(expansionColor).toBe(activeColor);
  expect(scrubberColor).not.toBe(expansionColor);
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
