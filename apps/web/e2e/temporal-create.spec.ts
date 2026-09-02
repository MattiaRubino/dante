import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openCreate(page: Page) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  return dialog;
}

async function selectCreateContext(dialog: Locator, label: string) {
  const trigger = dialog.locator('.temporal-create-context-trigger');
  await trigger.click();
  const picker = dialog.locator('.temporal-create-context-popover');
  await expect(picker).toBeVisible();
  const option = picker.getByRole('option', { name: label });
  await expect(option).toBeVisible();
  await option.click();
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
        if (viewportBottom - viewportTop <= 80) {
          return null;
        }

        const viewportCenter = (viewportTop + viewportBottom) / 2;
        const candidates = sections.flatMap((section) => {
          if (!(section instanceof HTMLElement)) {
            return [];
          }
          const rect = section.getBoundingClientRect();
          const dateValue = section.dataset.timelineDate;
          const visibleTop = Math.max(rect.top, viewportTop);
          const visibleBottom = Math.min(rect.bottom, viewportBottom);
          if (
            !dateValue ||
            rect.height <= 0 ||
            visibleBottom - visibleTop <= 80
          ) {
            return [];
          }
          return [
            {
              date: dateValue,
              distance: Math.abs(
                (visibleTop + visibleBottom) / 2 - viewportCenter,
              ),
            },
          ];
        });
        candidates.sort((left, right) => left.distance - right.distance);
        return candidates[0]?.date ?? null;
      });

  await expect.poll(readVisibleDate).not.toBeNull();
  const date = await readVisibleDate();

  if (!date) {
    throw new Error('Expected a visible Timeline day section');
  }

  const section = page.locator(
    `.timeline-day-section[data-timeline-date="${date}"]`,
  );
  await expect(section).toBeVisible();

  const [box, gridBox, viewportHeight] = await Promise.all([
    section.boundingBox(),
    grid.boundingBox(),
    page.evaluate(() => window.innerHeight),
  ]);
  if (!box || !gridBox) {
    throw new Error('Expected visible Timeline interaction geometry');
  }

  const visibleViewportTop = Math.max(box.y, gridBox.y, 0);
  const visibleViewportBottom = Math.min(
    box.y + box.height,
    gridBox.y + gridBox.height,
    viewportHeight,
  );
  if (visibleViewportBottom - visibleViewportTop <= 80) {
    throw new Error('Expected useful visible Timeline day geometry');
  }

  return {
    section,
    box,
    visibleTop: visibleViewportTop - box.y,
    visibleBottom: visibleViewportBottom - box.y,
  };
}

test('Quick Create stays title-first, protects drafts, and restores opener focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const trigger = page.getByRole('button', { name: 'Aggiungi alla timeline' });
  const dialog = await openCreate(page);
  const title = dialog.getByRole('textbox', { name: 'Titolo' });

  await expect(title).toBeFocused();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'quick');
  await expect(dialog.getByLabel('Tipo')).toHaveValue('activity');
  await expect(dialog.locator('.temporal-create-context-trigger')).toBeVisible();
  await expectNoRawCreateKeys(page);

  await title.fill('Studiare inglese');
  await page.keyboard.press('Escape');
  const discardPrompt = dialog.getByRole('alertdialog');
  await expect(discardPrompt).toBeVisible();
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await expect(title).toHaveValue('Studiare inglese');

  const discardActions = discardPrompt.getByRole('button');
  await expect(discardActions.nth(0)).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(discardActions.nth(1)).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(discardActions.nth(0)).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(discardPrompt).toHaveCount(0);
  await expect(title).toBeFocused();
  await expect(title).toHaveValue('Studiare inglese');

  await page.locator('[data-temporal-create="backdrop"]').click({
    position: { x: 2, y: 2 },
  });
  await expect(dialog.getByText('Scartare questa bozza?')).toBeVisible();
  await dialog.getByRole('button', { name: 'Scarta' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test('Quick Create makes a fixed Activity, reveals it, and undoes through F0', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Nuova attività');
  await dialog.getByLabel('Ora').fill('13:30');
  await dialog.getByLabel('Durata prevista').selectOption('60');
  await selectCreateContext(dialog, 'Focus / lavoro profondo');
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);

  const card = page
    .locator('[data-temporal-create-projection]:not(.is-preview)')
    .filter({ hasText: 'Nuova attività' });
  await expect(card).toBeVisible();
  await expect(card).toBeFocused();

  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toContainText('Creato: Nuova attività');
  await toast.getByRole('button', { name: 'Annulla' }).click();
  await expect(card).toHaveCount(0);
});

test('Expanded and Full Activity author DANTE planning without fake recurrence or placement', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Montare il video');
  await dialog.getByLabel('Durata prevista').selectOption('180');
  await dialog.getByRole('button', { name: /Dettagli e pianificazione/ }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'expanded');

  await dialog.getByLabel('Durata prevista (min)').fill('195');
  await dialog.getByLabel('Vincolo temporale').selectOption('bounded-window');
  await dialog.getByLabel('Politica di spostamento').selectOption('window');
  await dialog.getByLabel('Struttura di esecuzione').selectOption('splittable');
  await dialog.getByLabel('Sessione minima (min)').fill('45');
  await dialog.getByLabel('Esito non confermato').selectOption('daily-review');

  await expect(dialog.getByText('Routine e ripetizione')).toBeVisible();
  await expect(dialog).toContainText(
    'questo editor non finge una ricorrenza canonica dell’Attività',
  );
  await expect(dialog.getByLabel('Modello di ricorrenza')).toHaveCount(0);

  await dialog.getByRole('button', { name: 'Editor completo →' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'full');
  await expect(dialog.getByLabel('Durata prevista (min)')).toHaveValue('195');
  await dialog
    .getByLabel('Se il piano non è più fattibile')
    .selectOption('shorten-or-split');
  await dialog.getByLabel('Numero massimo di sessioni').fill('4');
  await dialog.getByLabel('Promemoria', { exact: true }).selectOption('60');
  await dialog.getByLabel('Esito non confermato').selectOption('infer-provisional');

  await expect(dialog).toContainText('Ogni risultato inferito resta provvisorio');
  await expect(dialog.getByRole('button', { name: /Progetto/ })).toBeDisabled();
  await expect(dialog.getByRole('button', { name: /Routine/ })).toBeDisabled();
  await expect(dialog.getByRole('button', { name: /Mondo/ })).toBeDisabled();
  await expect(dialog).toContainText('Richiede il verticale proprietario');
  await expect(dialog.getByLabel('Tag')).toHaveCount(0);
  await expectNoRawCreateKeys(page);

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);

  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(
    page
      .locator('[data-temporal-create-projection]:not(.is-preview)')
      .filter({ hasText: 'Montare il video' }),
  ).toHaveCount(0);
  const toast = page.locator('.temporal-create-toast.is-on');
  await expect(toast).toContainText('Montare il video');
  await expect(toast).toContainText('Da pianificare');
  await toast.getByRole('button', { name: 'Annulla' }).click();
});

test('Event Full Create preserves deep purpose, collaboration and provider intent without fake execution', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Call cliente');
  await dialog.getByLabel('Tipo').selectOption('event');
  await dialog.getByLabel('Ora').fill('16:00');
  await dialog.getByRole('button', { name: /Dettagli e pianificazione/ }).click();
  await dialog.getByRole('button', { name: 'Editor completo →' }).click();

  await expect(dialog.getByLabel('Vincolo temporale')).toHaveCount(0);
  await dialog.getByLabel('Data fine').fill('2026-08-05');
  await dialog.getByLabel('Ora fine').fill('10:00');
  await dialog.getByLabel('Luogo').fill('Studio / remoto');
  await dialog.getByLabel('Disponibilità').selectOption('busy');
  await dialog.getByLabel('Visibilità').selectOption('private');
  await dialog.getByLabel('Scopo').fill('Definire il rilascio');
  await dialog.getByLabel('Risultato atteso').fill('Decisione sul piano finale');
  await dialog.getByLabel('Agenda').fill('Rischi\nDecisioni\nProssimi passi');
  await dialog
    .getByRole('checkbox', { name: 'Da questo evento è attesa una decisione' })
    .check();

  await dialog.getByLabel('Modello di ricorrenza').selectOption('calendar-wall-clock');
  await dialog.getByLabel('Frequenza di calendario').selectOption('weekly');
  await dialog.getByRole('button', { name: 'Mar' }).click();
  await dialog.getByRole('button', { name: 'Gio' }).click();
  await dialog
    .getByLabel('Partecipanti richiesti')
    .fill('cliente@example.com');
  await dialog
    .getByLabel('Partecipanti opzionali')
    .fill('collega@example.com');
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
  const card = page
    .locator('[data-temporal-create-projection]:not(.is-preview)')
    .filter({ hasText: 'Call cliente' });
  await expect(card).toBeVisible();
  await expect(card).toContainText('Ricorrente');
});

test('Event recurrence exposes CP6 families, precise calendar/quota/cycle semantics, and preserves them across surfaces', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1360, height: 860 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Evento ciclico');
  await dialog.getByLabel('Tipo').selectOption('event');
  await dialog.getByRole('button', { name: /Dettagli e pianificazione/ }).click();
  await dialog.getByRole('button', { name: 'Editor completo →' }).click();

  const pattern = dialog.getByLabel('Modello di ricorrenza');
  await expect(pattern.locator('option')).toHaveCount(5);

  await pattern.selectOption('calendar-wall-clock');
  const frequency = dialog.getByLabel('Frequenza di calendario');
  await expect(frequency.locator('option')).toHaveCount(5);
  await frequency.selectOption('monthly-ordinal');
  await dialog.getByLabel('Posizione nel mese').selectOption('-1');
  await dialog
    .getByLabel('Giorno della settimana · Mensile · giorno della settimana')
    .selectOption('FR');
  await frequency.selectOption('yearly');
  await expect(dialog).toContainText('resta l’ancora civile del pattern');

  await pattern.selectOption('elapsed-interval');
  await dialog.getByLabel('Intervallo trascorso (minuti)').fill('720');

  await pattern.selectOption('quota-per-period');
  await dialog.getByLabel('Occorrenze richieste').fill('3');
  const quotaPeriod = dialog.getByLabel('Periodo', { exact: true });
  await expect(quotaPeriod.locator('option')).toHaveCount(4);
  await quotaPeriod.selectOption('year');
  await quotaPeriod.selectOption('week');
  await dialog.getByLabel('Confine del periodo').selectOption('named-zone');
  await dialog.getByLabel('Inizio settimana').selectOption('MO');
  await dialog.getByLabel('Fuso del periodo').fill('Europe/Rome');
  await expect(dialog).toContainText('Non dipende implicitamente dal fuso del dispositivo');

  await pattern.selectOption('cyclic-positional');
  await dialog.getByLabel('Lunghezza ciclo').fill('4');
  await dialog.getByLabel('Nuova posizione attiva').fill('2');
  await dialog.getByRole('button', { name: 'Aggiungi posizione' }).click();
  await expect(
    dialog.getByRole('button', { name: 'Rimuovi posizione 1' }),
  ).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Rimuovi posizione 2' }),
  ).toBeVisible();
  await dialog.getByLabel('Scopo').fill('Conservare il ciclo operativo');

  await dialog.getByRole('button', { name: '← Dettagli' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'expanded');
  await dialog.getByRole('button', { name: 'Editor completo →' }).click();
  await expect(pattern).toHaveValue('cyclic-positional');
  await expect(dialog.getByLabel('Lunghezza ciclo')).toHaveValue('4');
  await expect(
    dialog.getByRole('button', { name: 'Rimuovi posizione 1' }),
  ).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Rimuovi posizione 2' }),
  ).toBeVisible();
  await expect(dialog.getByLabel('Scopo')).toHaveValue(
    'Conservare il ciclo operativo',
  );
  await expectNoRawCreateKeys(page);

  const accessibility = await new AxeBuilder({ page })
    .include('[data-temporal-create="composer"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);
});

test('all-day multi-day Event materializes one native date span while unscheduled Activity stays unplaced', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  let dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Fiera');
  await dialog.getByLabel('Tipo').selectOption('event');
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

  const allDaySegments = page
    .locator('.timeline-all-day-item[data-temporal-create-projection]')
    .filter({ hasText: 'Fiera' });
  await expect(allDaySegments).toHaveCount(2);
  await expect(allDaySegments.first()).toHaveAttribute('data-range-start', 'true');
  await expect(allDaySegments.last()).toHaveAttribute('data-range-end', 'true');
  await expect(page.locator('.temporal-create-all-day:not(.is-preview)')).toHaveCount(0);

  const allDayToast = page.locator('.temporal-create-toast.is-on');
  await expect(allDayToast).toContainText('Fiera');
  await allDayToast.getByRole('button', { name: 'Annulla' }).click();
  await expect(allDaySegments).toHaveCount(0);

  dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Da organizzare');
  await dialog.getByRole('radio', { name: 'Da pianificare' }).click();
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();
  await expect(dialog).toHaveCount(0);
  await expect(page.locator('.temporal-create-toast.is-on')).toContainText(
    'Da organizzare',
  );
  await expect(page.locator('.temporal-create-toast.is-on')).toContainText(
    'Da pianificare',
  );
});

test('advanced validation focuses the real invalid control without losing the draft', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill('Studio');
  await dialog.getByLabel('Durata prevista').selectOption('60');
  await dialog.getByRole('button', { name: /Dettagli e pianificazione/ }).click();
  await dialog.getByLabel('Struttura di esecuzione').selectOption('splittable');
  await dialog.getByLabel('Sessione minima (min)').fill('120');
  await dialog.getByRole('button', { name: 'Aggiungi' }).click();

  await expect(
    dialog.getByText(/sessione minima deve essere almeno 5 minuti/i),
  ).toBeVisible();
  await expect(dialog.getByLabel('Sessione minima (min)')).toBeFocused();
  await expect(dialog.getByRole('textbox', { name: 'Titolo' })).toHaveValue(
    'Studio',
  );
});

test('double-click and Shift-drag on empty Timeline create contextual defaults', async ({
  page,
}) => {
  const viewport = { width: 1440, height: 900 };
  await page.setViewportSize(viewport);
  await page.goto('/home');

  let target = await visibleTimelineDay(page);
  const section = target.section;
  expect(target.visibleBottom - target.visibleTop).toBeGreaterThan(80);

  const emptyX = Math.min(600, target.box.width - 40);
  const emptyY =
    target.visibleTop + (target.visibleBottom - target.visibleTop) * 0.46;
  await section.dblclick({ position: { x: emptyX, y: emptyY } });
  let dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await expect(dialog.getByLabel('Data')).not.toHaveValue('');
  await expect(dialog.getByLabel('Ora')).not.toHaveValue('');
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(page.locator('.timeline-grid')).toBeFocused();

  target = await visibleTimelineDay(page);
  expect(target.visibleBottom - target.visibleTop).toBeGreaterThan(80);

  const startX = target.box.x + Math.min(600, target.box.width - 40);
  const rangeVisibleTop = target.box.y + target.visibleTop;
  const rangeVisibleBottom = target.box.y + target.visibleBottom;
  const startY =
    rangeVisibleTop + (rangeVisibleBottom - rangeVisibleTop) * 0.4;
  const endY = Math.min(rangeVisibleBottom - 20, startY + 130);
  expect(startY).toBeGreaterThanOrEqual(0);
  expect(endY).toBeLessThanOrEqual(viewport.height);
  expect(endY - startY).toBeGreaterThanOrEqual(30);

  await page.keyboard.down('Shift');
  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX, endY, { steps: 5 });
  await page.mouse.up();
  await page.keyboard.up('Shift');

  dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  const duration = Number(await dialog.getByLabel('Durata prevista').inputValue());
  expect(duration).toBeGreaterThanOrEqual(30);
});

test('Full Create becomes a mobile full-screen editor with no horizontal overflow', async ({
  page,
}) => {
  const viewportWidth = 390;
  await page.setViewportSize({ width: viewportWidth, height: 844 });
  await page.goto('/home');

  const dialog = await openCreate(page);
  await dialog.getByRole('button', { name: /Dettagli e pianificazione/ }).click();
  await dialog.getByRole('button', { name: 'Editor completo →' }).click();
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'full');

  const box = await dialog.boundingBox();
  expect(box).not.toBeNull();
  expect(box?.width ?? 999).toBeLessThanOrEqual(viewportWidth + 0.5);
  expect(box?.height ?? 0).toBeGreaterThan(800);
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth <=
        document.documentElement.clientWidth,
    ),
  ).toBe(true);
  await expectNoRawCreateKeys(page);
});
