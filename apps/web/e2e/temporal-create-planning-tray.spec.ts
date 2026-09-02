import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function createUnplacedActivity(
  page: Page,
  title: string,
  durationMinutes = 60,
) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill(title);
  await dialog
    .getByRole('radio', { name: 'Aperta, senza collocazione' })
    .click();
  await dialog.getByLabel('Durata prevista').selectOption(String(durationMinutes));
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);
}

async function openPlanningTray(page: Page) {
  const trigger = page.getByRole('button', {
    name: 'Apri attività da collocare',
  });
  await expect(trigger).toBeVisible();
  await trigger.click();
  const tray = page.locator('[data-timeline-planning-tray="true"]');
  await expect(tray).toBeVisible();
  return { trigger, tray };
}

function planningItem(tray: Locator, title: string) {
  return tray
    .locator('[data-timeline-planning-item]')
    .filter({ hasText: title });
}

async function visibleTimelineDropPoint(page: Page) {
  const grid = page.locator('.timeline-grid');
  await grid.scrollIntoViewIfNeeded();
  await expect(grid).toBeVisible();
  const candidate = await page
    .locator('.timeline-day-section[data-timeline-date]')
    .evaluateAll((sections) => {
      const timelineGrid = document.querySelector('.timeline-grid');
      if (!(timelineGrid instanceof HTMLElement)) {
        return null;
      }
      const gridRect = timelineGrid.getBoundingClientRect();
      const viewportTop = Math.max(0, gridRect.top);
      const viewportBottom = Math.min(window.innerHeight, gridRect.bottom);
      const center = (viewportTop + viewportBottom) / 2;
      const visible = sections.flatMap((section) => {
        if (!(section instanceof HTMLElement) || !section.dataset.timelineDate) {
          return [];
        }
        const rect = section.getBoundingClientRect();
        const top = Math.max(rect.top, viewportTop);
        const bottom = Math.min(rect.bottom, viewportBottom);
        if (bottom - top < 120) {
          return [];
        }
        return [
          {
            date: section.dataset.timelineDate,
            x: Math.max(rect.left + 180, Math.min(rect.right - 80, 620)),
            y: top + (bottom - top) * 0.46,
            distance: Math.abs((top + bottom) / 2 - center),
          },
        ];
      });
      visible.sort((left, right) => left.distance - right.distance);
      return visible[0] ?? null;
    });
  if (!candidate) {
    throw new Error('Expected a visible Timeline drop point');
  }
  return candidate;
}

async function undoPlanningMutation(page: Page) {
  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toBeVisible();
  await toast.getByRole('button', { name: 'Annulla' }).click();
}

test('an unplaced Activity lives in the tray, quick placement keeps identity, and Undo returns it', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  await createUnplacedActivity(page, 'Preparare portfolio', 60);
  await expect(
    page.locator('.timeline-event-card').filter({ hasText: 'Preparare portfolio' }),
  ).toHaveCount(0);

  const { trigger, tray } = await openPlanningTray(page);
  await expect(trigger).toContainText('1');
  const item = planningItem(tray, 'Preparare portfolio');
  await expect(item).toBeVisible();
  await expect(item).toContainText('60 min');

  const accessibility = await new AxeBuilder({ page })
    .include('[data-timeline-planning-tray="true"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);

  await item.locator('.timeline-planning-card__main').dblclick();
  const form = item.locator('.timeline-planning-quick-place');
  await expect(form).toBeVisible();
  const date = await form.getByLabel('Data').inputValue();
  await form.getByLabel('Ora').fill('13:15');
  await form.getByRole('button', { name: 'Colloca nella Timeline' }).click();

  await expect(planningItem(tray, 'Preparare portfolio')).toHaveCount(0);
  const card = page
    .locator('.timeline-event-card')
    .filter({ hasText: 'Preparare portfolio' });
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute('data-timeline-event');
  await expect(card).toContainText('13:15');
  await expect(trigger).not.toContainText('1');

  await undoPlanningMutation(page);
  await expect(card).toHaveCount(0);
  await expect(planningItem(tray, 'Preparare portfolio')).toBeVisible();
  await expect(trigger).toContainText('1');
  await expect(form.getByLabel('Data')).toHaveCount(0);
  expect(date).not.toBe('');
});

test('dragging from the tray foregrounds Timeline, previews a snapped slot, commits once, and Escape cancels', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await createUnplacedActivity(page, 'Scrivere proposta', 45);
  await createUnplacedActivity(page, 'Rivedere note', 30);

  const { tray } = await openPlanningTray(page);
  const first = planningItem(tray, 'Scrivere proposta');
  const dragHandle = first.locator('.timeline-planning-card__main');
  const itemBox = await dragHandle.boundingBox();
  if (!itemBox) {
    throw new Error('Expected Planning Tray card geometry');
  }
  const target = await visibleTimelineDropPoint(page);

  await page.mouse.move(
    itemBox.x + Math.min(80, itemBox.width / 2),
    itemBox.y + itemBox.height / 2,
  );
  await page.mouse.down();
  await page.mouse.move(target.x, target.y, { steps: 8 });

  await expect(page.locator('html')).toHaveAttribute(
    'data-timeline-planning-mode',
    'true',
  );
  const preview = page.locator('[data-timeline-planning-drop-preview="true"]');
  await expect(preview).toBeVisible();
  await expect(preview).toContainText('Rilascia qui');
  await expect(preview).toContainText(/\d{2}:\d{2}–\d{2}:\d{2}/);

  await page.mouse.up();
  await expect(page.locator('html')).not.toHaveAttribute(
    'data-timeline-planning-mode',
    'true',
  );
  await expect(preview).toHaveCount(0);
  await expect(planningItem(tray, 'Scrivere proposta')).toHaveCount(0);
  await expect(
    page.locator('.timeline-event-card').filter({ hasText: 'Scrivere proposta' }),
  ).toBeVisible();

  await undoPlanningMutation(page);
  await expect(planningItem(tray, 'Scrivere proposta')).toBeVisible();

  const second = planningItem(tray, 'Rivedere note').locator(
    '.timeline-planning-card__main',
  );
  const secondBox = await second.boundingBox();
  if (!secondBox) {
    throw new Error('Expected second Planning Tray card geometry');
  }
  await page.mouse.move(secondBox.x + 70, secondBox.y + secondBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(target.x, target.y, { steps: 8 });
  await expect(page.locator('html')).toHaveAttribute(
    'data-timeline-planning-mode',
    'true',
  );
  await page.keyboard.press('Escape');
  await expect(page.locator('html')).not.toHaveAttribute(
    'data-timeline-planning-mode',
    'true',
  );
  await page.mouse.up();
  await expect(planningItem(tray, 'Rivedere note')).toBeVisible();
  await expect(
    page.locator('.timeline-event-card').filter({ hasText: 'Rivedere note' }),
  ).toHaveCount(0);
});

test('tray delete is explicit and Undo restores the same unplaced Activity', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');
  await createUnplacedActivity(page, 'Pulire archivio', 30);
  const { tray } = await openPlanningTray(page);
  const item = planningItem(tray, 'Pulire archivio');

  await item.getByRole('button', { name: 'Elimina: Pulire archivio' }).click();
  const confirmation = item.getByRole('alertdialog');
  await expect(confirmation).toBeVisible();
  await expect(confirmation).toContainText('Eliminare questa attività?');
  await confirmation.getByRole('button', { name: 'Elimina' }).click();
  await expect(planningItem(tray, 'Pulire archivio')).toHaveCount(0);

  await undoPlanningMutation(page);
  await expect(planningItem(tray, 'Pulire archivio')).toBeVisible();
});

test('Planning Tray becomes a bounded bottom sheet on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');
  await createUnplacedActivity(page, 'Telefonare assicurazione', 30);
  const { tray } = await openPlanningTray(page);

  const box = await tray.boundingBox();
  expect(box).not.toBeNull();
  expect(box?.width ?? 999).toBeLessThanOrEqual(390.5);
  expect((box?.y ?? 0) + (box?.height ?? 0)).toBeGreaterThan(820);
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth <=
        document.documentElement.clientWidth,
    ),
  ).toBe(true);
  await expect(planningItem(tray, 'Telefonare assicurazione')).toBeVisible();
});
