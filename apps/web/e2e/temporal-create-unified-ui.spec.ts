import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Advanced Create keeps its header aligned when the title is empty', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();

  const row = dialog.locator('.temporal-create-title-row');
  const error = dialog.locator(
    '.temporal-create-title-row + .temporal-create-field-error',
  );
  await expect(error).toContainText('Inserisci un titolo');
  const geometry = await row.evaluate((element) => {
    const title = element.querySelector(
      '.temporal-create-title-row__name input',
    );
    const tools = element.querySelector('.temporal-create-title-row__tools');
    if (!title || !tools) return null;
    const bar = element.getBoundingClientRect();
    const name = title.getBoundingClientRect();
    const actions = tools.getBoundingClientRect();
    return {
      height: bar.height,
      aligned: Math.abs(name.top - actions.top) < 10,
      inside: actions.right <= bar.right + 1,
    };
  });
  expect(geometry).not.toBeNull();
  expect(geometry?.height).toBeLessThan(80);
  expect(geometry?.aligned).toBe(true);
  expect(geometry?.inside).toBe(true);
});

/** Match the bare Edit arrows, not Create's obsolete bordered mini-buttons. */
async function expectEditStyleChevrons(
  when: import('@playwright/test').Locator,
) {
  const arrows = when.locator(
    ':scope > .temporal-create-time-control .temporal-create-time-segment > button',
  );
  await expect(arrows).toHaveCount(8);
  for (const arrow of await arrows.all()) {
    await expect(arrow).toHaveCSS('height', '8px');
    await expect(arrow).toHaveCSS('border-top-width', '0px');
    await expect(arrow).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
    await expect(arrow).toHaveCSS('font-size', '5px');
  }
}

test('Quick keeps its compact clock field while Advanced uses the Edit interval visual scale', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();

  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toHaveAttribute('data-temporal-create-surface', 'base');
  // Text sizing is independent of the fixed Quick panel dimensions.
  await expect(
    dialog.locator('.temporal-create-type-grid strong').first(),
  ).toHaveCSS('font-size', '14px');
  await expect(
    dialog.locator('.temporal-create-choice-row > button').first(),
  ).toHaveCSS('font-size', '13.5px');
  const footer = dialog.locator('.temporal-create-actions');
  for (const button of await footer.locator(':scope > button').all()) {
    await expect(button).toHaveCSS('font-size', '13px');
  }
  // The fixed footer and all three actions stay inside the Quick panel.
  const footerFits = await footer.evaluate((element) => {
    const modal = element.closest('.temporal-create-composer');
    if (!modal) return false;
    const frame = modal.getBoundingClientRect();
    return Array.from(element.querySelectorAll(':scope > button')).every(
      (button) => {
        const box = button.getBoundingClientRect();
        return box.left >= frame.left - 1 && box.right <= frame.right + 1;
      },
    );
  });
  expect(footerFits).toBe(true);
  const quickClocks = dialog.locator(
    '.temporal-create-u2-when > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(quickClocks).toHaveCount(2);
  for (const clock of await quickClocks.all()) {
    await expect(clock).toHaveCSS('min-height', '42px');
  }
  const quickWhen = dialog.locator('.temporal-create-u2-when');
  await expect(quickWhen).not.toHaveCSS('max-width', '820px');
  await expectEditStyleChevrons(quickWhen);

  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await expect(dialog).toHaveAttribute(
    'data-temporal-create-surface',
    'advanced',
  );
  const advancedWhen = dialog.locator('.temporal-create-u2-when');
  await expect(
    dialog.locator('.temporal-create-reality-mode > button').first(),
  ).toHaveCSS('font-size', '14px');
  // Advanced intentionally increases the footer labels from Quick's 13px.
  for (const button of await footer.locator(':scope > button').all()) {
    await expect(button).toHaveCSS('font-size', '14px');
  }
  await expect(advancedWhen).toHaveCSS('max-width', '820px');
  await expectEditStyleChevrons(advancedWhen);
  const advancedControls = advancedWhen.locator(
    ':scope > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(advancedControls).toHaveCount(2);
  for (const clock of await advancedControls.all()) {
    await expect(clock).toHaveCSS('min-height', '46px');
  }

  // A full objective form exists only in Advanced, and uses the shared row.
  await dialog.getByRole('button', { name: 'Aggiungi obiettivo' }).click();
  await expect(dialog.locator('.temporal-create-objective__row')).toHaveCount(
    1,
  );
  await expect(
    dialog.getByRole('textbox', { name: 'Obiettivo 1' }),
  ).toBeVisible();
});

test('Activity Edit applies readable font sizes rather than inherited tiny labels', async ({
  page,
}) => {
  await page.goto('/home');
  // The Edit stylesheet is imported by the lazy-loaded authenticated editor,
  // so an unauthenticated /home fixture will not have fetched it. Load the
  // actual repo stylesheet (not a mock) before measuring computed styles.
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });
  const fonts = await page.evaluate(() => {
    const root = document.createElement('div');
    root.className = 'timeline-event-modal--edit';
    root.innerHTML = `
      <div class="timeline-activity-editor__body">
        <div class="temporal-create-reality-objectives__block-copy">
          <strong>Svolgimento dell’attività</strong>
          <span>Come vuoi gestire la conferma?</span>
        </div>
        <div class="temporal-create-reality-mode">
          <button>Nessuna verifica</button>
        </div>
        <div class="timeline-activity-editor__repeat">Ripeti · Mai</div>
        <div class="temporal-create-objectives__root-actions">
          <button class="temporal-create-objectives__add">Aggiungi obiettivo</button>
        </div>
      </div>`;
    document.body.appendChild(root);
    const size = (selector: string) =>
      getComputedStyle(root.querySelector(selector)!).fontSize;
    const result = {
      primary: size('.temporal-create-reality-objectives__block-copy strong'),
      secondary: size('.temporal-create-reality-objectives__block-copy span'),
      verification: size('.temporal-create-reality-mode > button'),
      repeat: size('.timeline-activity-editor__repeat'),
      objective: size('.temporal-create-objectives__add'),
    };
    root.remove();
    return result;
  });
  expect(fonts).toEqual({
    primary: '14px',
    secondary: '13px',
    verification: '14px',
    repeat: '14px',
    objective: '14px',
  });
});

test('Activity Edit keeps Create clock controls contained and the series recurrence stacked', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const create = page.locator('[data-temporal-create="composer"]');
  await create.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await create.getByRole('button', { name: /Aggiungi intervallo/ }).click();
  const interval = create
    .locator('.temporal-create-activity-interval__fields')
    .first();
  await expect(interval).toBeVisible();
  const markup = await interval.evaluate((element) => element.outerHTML);

  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/timeline.css',
  });
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });
  const geometry = await page.evaluate((intervalMarkup) => {
    const modal = document.createElement('div');
    modal.className = 'timeline-event-modal timeline-event-modal--edit';
    modal.style.width = '1040px';
    modal.innerHTML = `<div class="timeline-activity-editor timeline-recurring-series-editor"><div class="timeline-activity-editor__body">
      <div class="temporal-create-activity-intervals timeline-activity-editor__intervals">${intervalMarkup}</div>
      <section class="temporal-create-repeat timeline-recurring-series-editor__recurrence timeline-activity-editor__repeat">
        <div class="temporal-create-repeat__row">Ripeti ogni giorno</div>
        <div class="temporal-create-repeat__end-row"><span class="temporal-create-repeat__row-label">Termina</span><div class="temporal-create-repeat__end-choices"><div class="temporal-create-repeat__end-option">Mai</div><div class="temporal-create-repeat__end-option">Data</div></div></div>
      </section></div></div>`;
    document.body.append(modal);
    const fields = modal.querySelector<HTMLElement>(
      '.temporal-create-activity-interval__fields',
    )!;
    const children = Array.from(fields.children).filter(
      (element) => getComputedStyle(element).display !== 'none',
    );
    const bounds = children.map((element) => element.getBoundingClientRect());
    const fieldBounds = fields.getBoundingClientRect();
    const timeInputs = Array.from(
      fields.querySelectorAll<HTMLInputElement>(
        '.temporal-create-time-segment input',
      ),
    );
    const arrows = Array.from(
      fields.querySelectorAll<HTMLButtonElement>(
        '.temporal-create-time-segment button',
      ),
    );
    const recurrence = modal.querySelector<HTMLElement>(
      '.timeline-recurring-series-editor__recurrence',
    )!;
    const repeatRow = recurrence.querySelector<HTMLElement>(
      '.temporal-create-repeat__row',
    )!;
    const endRow = recurrence.querySelector<HTMLElement>(
      '.temporal-create-repeat__end-row',
    )!;
    const result = {
      fieldsContained: bounds.every(
        (box) =>
          box.left >= fieldBounds.left - 1 &&
          box.right <= fieldBounds.right + 1,
      ),
      clockInputsCompact:
        timeInputs.length === 4 &&
        timeInputs.every(
          (input) =>
            input.getBoundingClientRect().width <= 42 &&
            getComputedStyle(input).paddingLeft === '0px',
        ),
      clockArrowsCompact:
        arrows.length === 8 &&
        arrows.every(
          (arrow) =>
            arrow.getBoundingClientRect().height <= 10 &&
            getComputedStyle(arrow).paddingLeft === '0px',
        ),
      recurrenceStacked:
        getComputedStyle(recurrence).display === 'grid' &&
        endRow.getBoundingClientRect().top >=
          repeatRow.getBoundingClientRect().bottom,
    };
    modal.remove();
    return result;
  }, markup);
  expect(geometry).toEqual({
    fieldsContained: true,
    clockInputsCompact: true,
    clockArrowsCompact: true,
    recurrenceStacked: true,
  });
});
