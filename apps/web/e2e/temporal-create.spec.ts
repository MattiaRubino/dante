import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

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
          if (!(section instanceof HTMLElement) || !section.dataset.timelineDate) {
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
  const visibleTop =
    Math.max(box.y + minuteZeroOffset, gridBox.y, 0) - box.y;
  const visibleBottom =
    Math.min(
      box.y + box.height,
      gridBox.y + gridBox.height,
      viewportHeight,
    ) - box.y;

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
  await expect(dialog.getByRole('radio', { name: 'Da collocare' })).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Opzioni avanzate' }),
  ).toHaveAttribute('aria-expanded', 'false');
  await expectNoRawCreateKeys(page);

  await title.fill('Studiare inglese');
  await page.keyboard.press('Escape');
  const discard = dialog.getByRole('alertdialog');
  await expect(discard).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');

  await page.keyboard.press('Escape');
  await expect(discard).toHaveCount(0);
  await expect(title).toBeFocused();

  await page.locator('[data-temporal-create="backdrop"]').click({
    position: { x: 2, y: 2 },
  });
  await dialog.getByRole('button', { name: 'Scarta' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('Activity Orario plus Divisibile remains placed and Undo removes the same created Activity', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Montare il video');
  await dialog.getByLabel('Ora').fill('14:30');
  await dialog.getByLabel('Durata prevista').selectOption('180');
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');

  await dialog
    .getByRole('combobox', { name: /Struttura di esecuzione/ })
    .selectOption('splittable');
  await dialog.getByLabel('Sessione minima (min)').fill('45');
  await dialog.getByLabel('Numero massimo di sessioni').fill('4');
  await expect(dialog.getByRole('radio', { name: 'Orario' })).toHaveAttribute(
    'aria-checked',
    'true',
  );
  await expect(dialog.getByLabel('Modello di ricorrenza')).toHaveCount(0);

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.getByLabel('Ora')).toHaveValue('14:30');
  await expect(dialog.getByLabel('Durata prevista')).toHaveValue('180');

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(
    dialog.getByRole('combobox', { name: /Struttura di esecuzione/ }),
  ).toHaveValue('splittable');
  await expect(dialog.getByLabel('Sessione minima (min)')).toHaveValue('45');
  await expect(dialog.getByLabel('Numero massimo di sessioni')).toHaveValue('4');

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('.timeline-event-card[data-temporal-create-projection]')
    .filter({ hasText: 'Montare il video' });
  await expect(card).toBeVisible();
  await expect(card).toContainText('14:30');
  await expect(
    page
      .locator('[data-timeline-planning-item]')
      .filter({ hasText: 'Montare il video' }),
  ).toHaveCount(0);

  await page
    .locator('.temporal-create-toast.is-on')
    .getByRole('button', { name: 'Annulla' })
    .click();
  await expect(card).toHaveCount(0);
});

test('Event Advanced preserves structured agenda, deep intent and provider requests without claiming provider execution', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Call cliente');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByLabel('Ora').fill('16:00');
  await dialog.getByLabel('Ripeti').selectOption('weekly');
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();

  await dialog.getByLabel('Scopo').fill('Definire il rilascio');
  await dialog.getByLabel('Risultato atteso').fill('Decisione sul piano finale');

  const agendaInput = dialog.getByLabel('Nuova voce agenda');
  for (const part of ['Rischi', 'Decisioni', 'Prossimi passi']) {
    await agendaInput.fill(part);
    await agendaInput.press('Enter');
  }
  await expect(dialog.locator('[data-temporal-create-agenda-part]')).toHaveCount(3);
  await dialog.getByLabel('Voce agenda 3').press('Alt+ArrowUp');
  await expect(dialog.getByLabel('Voce agenda 2')).toHaveValue('Prossimi passi');
  await dialog.getByRole('button', { name: 'Sposta voce 2 giù' }).click();
  await expect(dialog.getByLabel('Voce agenda 3')).toHaveValue('Prossimi passi');
  await agendaInput.fill('   ');
  await agendaInput.press('Enter');
  await expect(dialog.locator('[data-temporal-create-agenda-part]')).toHaveCount(3);
  await agendaInput.fill('');

  await dialog
    .getByRole('checkbox', { name: 'Da questo evento è attesa una decisione' })
    .check();
  await dialog.getByLabel('Partecipanti richiesti').fill('Cliente principale');
  await dialog.getByLabel('Sale e risorse').fill('Sala Atlas');
  await dialog.getByLabel('Pre-read / materiale da preparare').fill('Specifica v3');
  await dialog.getByLabel('Buffer di preparazione').selectOption('15');
  await dialog.getByLabel('Buffer di recupero').selectOption('10');
  await dialog.getByLabel('Videochiamata').selectOption('provider-default');
  await expect(dialog).toContainText(
    'Inviti, prenotazioni e link reali vengono eseguiti solo quando il provider/backend è collegato.',
  );
  await expect(dialog).toContainText(
    'Generazione delle Occurrence, checkpoint dell’evaluator, reconciliation e persistenza durevole',
  );
  await expectNoRawCreateKeys(page);

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);
  const card = page
    .locator('.timeline-event-card[data-temporal-create-projection]')
    .filter({ hasText: 'Call cliente' });
  await expect(card).toBeVisible();
  await expect(card).toContainText('Ricorrente');
  const expander = card.getByRole('button', { name: /3 sotto-attività/ });
  await expect(expander).toBeVisible();
  await expander.click();
  await expect(card).toContainText('Rischi');
  await expect(card).toContainText('Decisioni');
  await expect(card).toContainText('Prossimi passi');
});

test('Event quick recurrence enters truthful CP6 authoring and survives base Advanced round trips', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Evento ciclico');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByLabel('Ripeti').selectOption('weekly');
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');

  const pattern = dialog.getByLabel('Modello di ricorrenza');
  await expect(pattern.locator('option')).toHaveCount(5);
  await expect(pattern).toHaveValue('calendar-wall-clock');
  await expect(dialog.getByLabel('Frequenza di calendario')).toHaveValue('weekly');

  await pattern.selectOption('elapsed-interval');
  await dialog.getByLabel('Intervallo trascorso (minuti)').fill('720');

  await pattern.selectOption('quota-per-period');
  await dialog.getByLabel('Occorrenze richieste').fill('3');
  await dialog.getByLabel('Periodo', { exact: true }).selectOption('week');
  await dialog.getByLabel('Confine del periodo').selectOption('named-zone');
  await dialog.getByLabel('Fuso del periodo').fill('Europe/Rome');

  await pattern.selectOption('cyclic-positional');
  await dialog.getByLabel('Lunghezza ciclo').fill('4');
  await dialog.getByLabel('Nuova posizione attiva').fill('2');
  await dialog.getByRole('button', { name: 'Aggiungi posizione' }).click();

  await dialog
    .getByRole('button', { name: 'Nascondi opzioni avanzate' })
    .click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  await expect(dialog.getByLabel('Ripeti')).toHaveValue('custom');

  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(pattern).toHaveValue('cyclic-positional');
  await expect(dialog.getByLabel('Lunghezza ciclo')).toHaveValue('4');
  await expect(
    dialog.getByRole('button', { name: 'Rimuovi posizione 2' }),
  ).toBeVisible();

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);
});

test('all-day date spans live inside each day before minute zero for Event and Activity', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  let dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Fiera');
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
  const startDate = await dialog.getByLabel('Data inizio').inputValue();
  const nextDate = await page.evaluate((value) => {
    const date = new Date(`${value}T12:00:00Z`);
    date.setUTCDate(date.getUTCDate() + 1);
    return date.toISOString().slice(0, 10);
  }, startDate);
  await dialog.getByLabel('Data fine').fill(nextDate);
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const startDay = page.locator(
    `.timeline-day-section[data-timeline-date="${startDate}"]`,
  );
  const endDay = page.locator(
    `.timeline-day-section[data-timeline-date="${nextDate}"]`,
  );
  const startItem = startDay
    .locator('.timeline-all-day-item[data-temporal-create-projection]')
    .filter({ hasText: 'Fiera' });
  const endItem = endDay
    .locator('.timeline-all-day-item[data-temporal-create-projection]')
    .filter({ hasText: 'Fiera' });

  await expect(startItem).toHaveAttribute('data-range-position', 'start');
  await expect(endItem).toHaveAttribute('data-range-position', 'end');
  const projectionId = await startItem.getAttribute(
    'data-temporal-create-projection',
  );
  expect(projectionId).not.toBeNull();
  await expect(endItem).toHaveAttribute(
    'data-temporal-create-projection',
    projectionId ?? '',
  );
  await expect(page.locator('[data-timeline-all-day-strip]')).toHaveCount(0);

  expect(
    await startDay.evaluate((section) => {
      const lane = section.querySelector<HTMLElement>('.timeline-all-day-lane');
      const minuteZero = section.querySelector<HTMLElement>('.timeline-hour-line');
      if (!lane || !minuteZero) {
        return false;
      }
      return (
        Math.abs(
          Number.parseFloat(minuteZero.style.top) -
            lane.getBoundingClientRect().height,
        ) <= 1
      );
    }),
  ).toBe(true);

  await startDay.locator('.timeline-all-day-lane__label').dblclick();
  await expect(page.locator('[data-temporal-create="composer"]')).toHaveCount(0);
  await page
    .locator('.temporal-create-toast.is-on')
    .getByRole('button', { name: 'Annulla' })
    .click();
  await expect(startItem).toHaveCount(0);
  await expect(endItem).toHaveCount(0);

  dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Giornata studio');
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
  const activityDate = await dialog.getByLabel('Data').inputValue();
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  const activity = page
    .locator(
      `.timeline-day-section[data-timeline-date="${activityDate}"] .timeline-all-day-item[data-temporal-create-projection]`,
    )
    .filter({ hasText: 'Giornata studio' });
  await expect(activity).toHaveAttribute('data-range-position', 'single');
  await page
    .locator('.temporal-create-toast.is-on')
    .getByRole('button', { name: 'Annulla' })
    .click();
  await expect(activity).toHaveCount(0);
});

test('Advanced validation focuses the invalid execution control without losing the draft', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Studio');
  await dialog.getByLabel('Durata prevista').selectOption('60');
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await dialog
    .getByRole('combobox', { name: /Struttura di esecuzione/ })
    .selectOption('splittable');
  await dialog.getByLabel('Sessione minima (min)').fill('120');
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();

  await expect(dialog.locator('.temporal-create-field-error').first()).toBeVisible();
  await expect(dialog.getByLabel('Sessione minima (min)')).toBeFocused();
  await expect(dialog.getByRole('textbox', { name: 'Titolo' })).toHaveValue(
    'Studio',
  );
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');
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
  await expect(dialog.getByLabel('Data')).not.toHaveValue('');
  await expect(dialog.getByLabel('Ora')).not.toHaveValue('');
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
  const duration = Number(await dialog.getByLabel('Durata prevista').inputValue());
  expect(duration).toBeGreaterThanOrEqual(30);
});

test('Advanced Create remains bounded on mobile without horizontal overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('button', { name: 'Opzioni avanzate' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'advanced');

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
