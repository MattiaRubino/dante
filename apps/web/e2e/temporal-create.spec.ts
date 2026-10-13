import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

import { setTimedDuration, timedDurationMinutes } from './helpers/create-time';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

async function expectNoRawCreateKeys(page: Page) {
  await expect(page.locator('body')).not.toContainText('home.timeline.create.');
}

type VisibleTimelineDay = Readonly<{
  section: Locator;
  box: Readonly<{ x: number; y: number; width: number; height: number }>;
  visibleTop: number;
  visibleBottom: number;
}>;

async function visibleTimelineDay(page: Page): Promise<VisibleTimelineDay> {
  const grid = page.locator('.timeline-grid');
  await expect(grid).toBeVisible();
  await grid.scrollIntoViewIfNeeded();

  const readVisibleDate = async (): Promise<string | null> =>
    page
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
        const candidates = sections.flatMap((section) => {
          if (
            !(section instanceof HTMLElement) ||
            !section.dataset.timelineDate
          ) {
            return [];
          }

          const rect = section.getBoundingClientRect();
          const minuteZero = section.querySelector<HTMLElement>(
            '.timeline-hour-line',
          );
          const timedTop = minuteZero
            ? rect.top + Number.parseFloat(minuteZero.style.top)
            : rect.top;
          const top = Math.max(rect.top, timedTop, viewportTop);
          const bottom = Math.min(rect.bottom, viewportBottom);
          if (bottom - top <= 80) {
            return [];
          }
          return [
            {
              date: section.dataset.timelineDate,
              distance: Math.abs((top + bottom) / 2 - center),
            },
          ];
        });
        candidates.sort((left, right) => left.distance - right.distance);
        return candidates[0]?.date ?? null;
      });

  await expect.poll(readVisibleDate).not.toBeNull();
  const date = await readVisibleDate();
  if (!date) {
    throw new Error('Expected a visible Timeline day');
  }

  const section = page.locator(
    `.timeline-day-section[data-timeline-date="${date}"]`,
  );
  const [box, gridBox, viewportHeight] = await Promise.all([
    section.boundingBox(),
    grid.boundingBox(),
    page.evaluate(() => window.innerHeight),
  ]);
  if (!box || !gridBox) {
    throw new Error('Expected visible Timeline geometry');
  }

  const minuteZeroOffset = await section.evaluate((element) => {
    const line = element.querySelector<HTMLElement>('.timeline-hour-line');
    return line ? Number.parseFloat(line.style.top) : 0;
  });
  const visibleTop = Math.max(box.y + minuteZeroOffset, gridBox.y, 0) - box.y;
  const visibleBottom =
    Math.min(box.y + box.height, gridBox.y + gridBox.height, viewportHeight) -
    box.y;

  return { section, box, visibleTop, visibleBottom };
}

test('Create base is title-first, exposes actionable types, protects drafts, and restores opener focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Aggiungi alla timeline' });
  const dialog = await openCreate(page);
  const title = dialog.getByRole('textbox', { name: 'Titolo' });

  await expect(title).toBeFocused();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(
    dialog.locator('.temporal-create-type-grid [role="radio"]'),
  ).toHaveCount(2);
  await expect(dialog.getByRole('radio', { name: 'Attività' })).toHaveAttribute(
    'aria-checked',
    'true',
  );
  await expect(dialog.getByRole('radio', { name: 'Evento' })).toBeVisible();
  // The retired unplaced-authoring radio was replaced by a dedicated
  // inert Draft Vault save action, separate from canonical Create.
  await expect(
    dialog.getByRole('button', { name: 'Salva bozza' }),
  ).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Opzioni avanzate' }),
  ).toHaveAttribute('aria-expanded', 'false');
  await expectNoRawCreateKeys(page);

  await title.fill('Studiare inglese');
  await page.keyboard.press('Escape');
  const discard = page.getByRole('alertdialog');
  await expect(discard).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');

  await page.keyboard.press('Escape');
  await expect(discard).toHaveCount(0);
  await expect(title).toBeFocused();

  await dialog.locator('.dante-temporal-panel-close').click();
  await expect(discard).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');
  await discard.getByRole('button', { name: 'Scarta' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('Advanced planned Session is retained and never silently dropped by the in-memory fixture', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog
    .getByRole('textbox', { name: 'Titolo' })
    .fill('Montare il video');
  await dialog.getByRole('textbox', { name: 'Inizio: ore' }).fill('14');
  await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).fill('30');
  await setTimedDuration(dialog, 180);
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );

  // B14 now authors an Activity with optional planned root Sessions;
  // the legacy Splittable dropdown and duration-count fields were retired.
  await dialog.getByRole('checkbox', { name: 'Sessione' }).check();
  await dialog.locator('.temporal-create-tree-add').click();
  const planned = dialog.locator('[data-create-planned-session]');
  await expect(planned).toHaveCount(1);
  await planned
    .getByRole('textbox', { name: 'Nome Sessione' })
    .fill('Montaggio');
  await expect(dialog.getByRole('radio', { name: 'Orario' })).toHaveAttribute(
    'aria-checked',
    'true',
  );
  await expect(dialog.getByLabel('Modello di ricorrenza')).toHaveCount(0);

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(
    dialog.getByRole('textbox', { name: 'Inizio: ore' }),
  ).toHaveValue('14');
  await expect(
    dialog.getByRole('textbox', { name: 'Inizio: minuti' }),
  ).toHaveValue('30');
  expect(await timedDurationMinutes(dialog)).toBe(180);

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(
    dialog.getByRole('checkbox', { name: 'Sessione' }),
  ).toBeChecked();
  await expect(
    dialog
      .locator('[data-create-planned-session]')
      .getByRole('textbox', { name: 'Nome Sessione' }),
  ).toHaveValue('Montaggio');

  // The in-memory fixture does not persist U6 planned Sessions. Ensure it
  // refuses a fake "success" instead of dropping the Session silently;
  // actual atomic Activity + Session persistence is a real-stack contract.
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  await expect(dialog).toBeVisible();
  await expect(dialog).toContainText('non possono ancora essere combinate');
  await expect(dialog.locator('[data-create-planned-session]')).toHaveCount(1);
  await expect(
    page
      .locator('.timeline-event-card')
      .filter({ hasText: 'Montare il video' }),
  ).toHaveCount(0);
});

test('Event Advanced preserves Scaletta and refuses unsupported fixture persistence without losing input', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog
    .getByRole('textbox', { name: 'Titolo' })
    .fill('B14 Evento isolato con Scaletta');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByRole('radio', { name: 'Orario' }).click();
  await dialog.getByRole('textbox', { name: 'Inizio: ore' }).fill('16');
  await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).fill('00');
  await setTimedDuration(dialog, 60);
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();

  // The U2 product replaced legacy free-form provider instructions with
  // canonical run-of-show and person-referent authoring. Verify those current
  // controls instead of asserting removed Scopo/provider fields.
  const agenda = dialog.locator('[data-temporal-create-agenda]');
  const addPart = agenda.getByRole('button', {
    name: 'Aggiungi punto alla scaletta',
  });
  for (const part of ['Rischi', 'Decisioni', 'Prossimi passi']) {
    await addPart.click();
    await agenda
      .getByRole('textbox', {
        name: `Punto scaletta ${await agenda.locator('[data-temporal-create-agenda-part]').count()}`,
      })
      .fill(part);
  }
  await expect(
    agenda.locator('[data-temporal-create-agenda-part]'),
  ).toHaveCount(3);
  await agenda
    .getByRole('textbox', { name: 'Punto scaletta 3' })
    .press('Alt+ArrowUp');
  await expect(
    agenda.getByRole('textbox', { name: 'Punto scaletta 2' }),
  ).toHaveValue('Prossimi passi');
  await agenda
    .locator('[data-temporal-create-agenda-part]')
    .nth(1)
    .getByRole('button', { name: 'Sposta giù' })
    .click();
  await expect(
    agenda.getByRole('textbox', { name: 'Punto scaletta 3' }),
  ).toHaveValue('Prossimi passi');

  const description = dialog.getByRole('textbox', {
    name: 'Descrizione avanzata',
  });
  await description.fill(
    'Definire il rilascio con una decisione sul piano finale.',
  );
  const participants = dialog.locator('[data-create-event-participants]');
  await expect(participants).toContainText(
    'non concede accesso alla tua Timeline',
  );
  await participants
    .locator('.temporal-create-event-participants__add button')
    .click();
  await expect(
    participants.locator('.temporal-create-event-participants__list'),
  ).toContainText('Io');
  await expect(
    participants.getByRole('combobox', { name: 'Partecipazione di Io' }),
  ).toHaveValue('required');

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(description).toHaveValue(
    'Definire il rilascio con una decisione sul piano finale.',
  );
  await expect(
    agenda.locator('[data-temporal-create-agenda-part]'),
  ).toHaveCount(3);
  await expect(
    participants.locator('.temporal-create-event-participants__list'),
  ).toContainText('Io');

  // Notes are supported by U2 authoritative Event authoring. This isolated
  // legacy fixture intentionally has no Event persistence endpoint; the
  // form must remain intact and visibly refuse the unsupported submission.
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  await expect(dialog).toBeVisible();
  await expect(
    dialog.locator('.temporal-create-operation-error'),
  ).toBeVisible();
  await expect(description).toHaveValue(
    'Definire il rilascio con una decisione sul piano finale.',
  );
  await expect(
    page
      .locator('.timeline-event-card')
      .filter({ hasText: 'B14 Evento isolato con Scaletta' }),
  ).toHaveCount(0);
});

test('Event calendar recurrence preserves interval and end policy across Advanced round trips', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Evento ciclico');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByRole('radio', { name: 'Orario' }).click();
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await dialog.getByLabel('Ripeti', { exact: true }).selectOption('weekly');

  const recurrence = dialog.locator('[data-create-recurrence-owner="event"]');
  await expect(recurrence).toBeVisible();
  await recurrence
    .getByRole('spinbutton', { name: 'Intervallo di ripetizione' })
    .fill('2');
  await recurrence.getByRole('radio', { name: 'Dopo' }).click();
  await recurrence
    .getByRole('spinbutton', { name: 'Numero di occorrenze' })
    .fill('3');

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.getByLabel('Ripeti', { exact: true })).toHaveCount(0);

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog.getByLabel('Ripeti', { exact: true })).toHaveValue(
    'custom',
  );
  await expect(recurrence).toBeVisible();
  await expect(
    recurrence.getByRole('spinbutton', { name: 'Intervallo di ripetizione' }),
  ).toHaveValue('2');
  await expect(
    recurrence.getByRole('spinbutton', { name: 'Numero di occorrenze' }),
  ).toHaveValue('3');
  await expect(recurrence.getByRole('radio', { name: 'Dopo' })).toHaveAttribute(
    'aria-checked',
    'true',
  );

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);
});

test('all-day Event editor preserves a two-day date-span and never invents an accepted fixture Schedule', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Fiera');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
  const start = dialog.getByRole('button', { name: /^Data inizio:/ });
  const startDate = await start.getAttribute('data-temporal-date');
  expect(startDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  if (!startDate) throw new Error('Expected a selected start date');
  const nextDate = await page.evaluate((value) => {
    const date = new Date(`${value}T12:00:00Z`);
    date.setUTCDate(date.getUTCDate() + 1);
    return date.toISOString().slice(0, 10);
  }, startDate);
  await dialog.getByRole('button', { name: /^Data fine:/ }).click();
  await dialog
    .getByRole('dialog', { name: 'Data fine' })
    .locator(`[data-temporal-date="${nextDate}"]`)
    .click();
  await expect(
    dialog.getByRole('button', { name: /^Data fine:/ }),
  ).toHaveAttribute('data-temporal-date', nextDate);
  await expect(start).toHaveAttribute('data-temporal-date', startDate);

  // The isolated legacy runtime has no Event authoring backend. The actual
  // canonical multi-day creation + reload is tested in auth/event-create-read.
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  await expect(dialog).toBeVisible();
  await expect(
    page.locator('.timeline-all-day-item').filter({ hasText: 'Fiera' }),
  ).toHaveCount(0);
});

test('Advanced validation focuses the required title without discarding time or draft', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  const title = dialog.getByRole('textbox', { name: 'Titolo' });
  await title.fill('Studio');
  await setTimedDuration(dialog, 60);
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await title.fill('');
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();

  await expect(
    dialog.locator('.temporal-create-field-error').first(),
  ).toBeVisible();
  await expect(title).toBeFocused();
  expect(await timedDurationMinutes(dialog)).toBe(60);
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );
});

test('double-click and Shift-drag only use the timed canvas for contextual Create', async ({
  page,
}) => {
  const viewport = { width: 1440, height: 900 };
  await page.setViewportSize(viewport);
  await page.goto('/home');

  let target = await visibleTimelineDay(page);
  const emptyX = Math.min(600, target.box.width - 40);
  const emptyY =
    target.visibleTop + (target.visibleBottom - target.visibleTop) * 0.46;
  await target.section.dblclick({ position: { x: emptyX, y: emptyY } });

  let dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: /^Data inizio:/ }),
  ).toHaveAttribute('data-temporal-date', /^\d{4}-\d{2}-\d{2}$/);
  await expect(
    dialog.getByRole('textbox', { name: 'Inizio: ore' }),
  ).not.toHaveValue('');
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(page.locator('.timeline-grid')).toBeFocused();

  target = await visibleTimelineDay(page);
  const x = target.box.x + Math.min(600, target.box.width - 40);
  const top = target.box.y + target.visibleTop;
  const bottom = target.box.y + target.visibleBottom;
  const startY = top + (bottom - top) * 0.4;
  const endY = Math.min(bottom - 20, startY + 130);

  await page.keyboard.down('Shift');
  await page.mouse.move(x, startY);
  await page.mouse.down();
  await page.mouse.move(x, endY, { steps: 5 });
  await page.mouse.up();
  await page.keyboard.up('Shift');

  dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  const duration = await timedDurationMinutes(dialog);
  expect(duration).toBeGreaterThanOrEqual(30);
});

test('Advanced Create remains bounded on mobile without horizontal overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );

  const box = await dialog.boundingBox();
  expect(box).not.toBeNull();
  expect(box?.width ?? 999).toBeLessThanOrEqual(390.5);
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth <=
        document.documentElement.clientWidth,
    ),
  ).toBe(true);
  await expectNoRawCreateKeys(page);
});
