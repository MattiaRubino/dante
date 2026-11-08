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
    dialog.getByRole('region', { name: 'Configurazione obiettivi' }),
  ).toBeVisible();
  await expect(dialog.locator('.temporal-create-reality-mode')).toHaveCount(0);
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
  await expect(
    dialog.getByRole('combobox', { name: 'Verifica obiettivo 1' }),
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
  await page.addStyleTag({
    path: 'src/features/temporal-create/ui/temporal-editor-section-typography.css',
  });
  const fonts = await page.evaluate(() => {
    const root = document.createElement('div');
    root.className = 'timeline-event-modal--edit';
    root.innerHTML = `
      <div class="timeline-activity-editor__body">
        <div class="temporal-create-reality-objectives__block-copy">
          <strong class="temporal-editor-section-heading">Obiettivi</strong>
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
      repeat: size('.timeline-activity-editor__repeat'),
      objective: size('.temporal-create-objectives__add'),
    };
    root.remove();
    return result;
  });
  expect(fonts).toEqual({
    primary: '15px',
    repeat: '14px',
    objective: '14px',
  });
  const description = await page.evaluate(() => {
    const root = document.createElement('div');
    root.className = 'timeline-event-modal--edit';
    root.innerHTML =
      '<section class="timeline-activity-editor__description temporal-create-section is-wide temporal-create-description-section">' +
      '<h3>Descrizione</h3><textarea aria-label="Descrizione"></textarea></section>';
    document.body.appendChild(root);
    const section = root.querySelector('section')!;
    const heading = root.querySelector('h3')!;
    const result = {
      border: getComputedStyle(section).borderTopStyle,
      padding: getComputedStyle(section).paddingTop,
      titleSize: getComputedStyle(heading).fontSize,
    };
    root.remove();
    return result;
  });
  expect(description).toEqual({
    border: 'solid',
    padding: '14px',
    titleSize: '15px',
  });
});

test('Advanced Create and every Edit surface share section typography and control sizes', async ({
  page,
}) => {
  await page.goto('/home');
  // Use the actual shared stylesheet, independent of authenticated fixtures.
  await page.addStyleTag({
    path: 'src/features/temporal-create/ui/temporal-editor-section-typography.css',
  });
  const surfaces = await page.evaluate(() => {
    const root = document.createElement('div');
    root.innerHTML = [
      '<section class="temporal-create-composer is-advanced" data-surface="create">',
      '  <strong class="temporal-editor-section-heading">Obiettivi</strong>',
      '  <button class="temporal-create-tree-add">Sessione</button>',
      '</section>',
      '<section class="timeline-event-modal--edit" data-surface="activity">',
      '  <div class="timeline-activity-editor__body">',
      '    <strong class="temporal-editor-section-heading">Sessioni attività</strong>',
      '    <button class="temporal-create-tree-add">Sessione</button>',
      '  </div>',
      '</section>',
      '<section class="timeline-event-modal--edit" data-surface="event">',
      '  <div class="timeline-activity-editor__body">',
      '    <strong class="temporal-editor-section-heading">Scaletta</strong>',
      '    <button class="temporal-create-tree-add">Scaletta</button>',
      '  </div>',
      '</section>',
      '<section class="timeline-event-modal--edit" data-surface="series">',
      '  <div class="timeline-activity-editor__body">',
      '    <strong class="temporal-editor-section-heading">Obiettivi</strong>',
      '    <button class="temporal-create-tree-add">Sessione</button>',
      '  </div>',
      '</section>',
    ].join('');
    document.body.appendChild(root);
    const values = ['create', 'activity', 'event', 'series'].map((name) => {
      const surface = root.querySelector(`[data-surface="${name}"]`)!;
      const heading = getComputedStyle(
        surface.querySelector('.temporal-editor-section-heading')!,
      );
      const button = getComputedStyle(
        surface.querySelector('.temporal-create-tree-add')!,
      );
      return {
        name,
        titleSize: heading.fontSize,
        titleWeight: heading.fontWeight,
        titleCase: heading.textTransform,
        titleColor: heading.color,
        actionSize: button.fontSize,
        actionHeight: parseFloat(button.minHeight),
      };
    });
    root.remove();
    return values;
  });
  expect(surfaces.map(({ name }) => name)).toEqual([
    'create',
    'activity',
    'event',
    'series',
  ]);
  for (const surface of surfaces) {
    expect(surface.titleSize).toBe('15px');
    expect(surface.titleCase).toBe('none');
    expect(surface.titleWeight).toBe('650');
    expect(surface.actionSize).toBe('14px');
    expect(surface.actionHeight).toBeGreaterThanOrEqual(38);
  }
  expect(new Set(surfaces.map(({ titleColor }) => titleColor)).size).toBe(1);
});

test('Event Edit keeps its form scrollable and its Save action visible in the Activity modal shell', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto('/home');
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/timeline.css',
  });
  const geometry = await page.evaluate(() => {
    const modal = document.createElement('div');
    modal.className =
      'timeline-event-modal timeline-event-modal--edit timeline-event-modal--event-edit';
    modal.style.height = '600px';
    modal.innerHTML = `<div class="timeline-event-modal__header">Chiudi</div>
      <div class="timeline-event-modal__title-row">Modifica evento</div>
      <div class="timeline-activity-inspector__actions">
        <div class="timeline-event-profile-editor">
          <div class="timeline-event-profile-editor__body">
            <label>Titolo <input /></label>
            <div style="height: 1100px">Campi evento</div>
          </div>
          <div class="timeline-event-profile-editor__actions"><button>Salva modifiche</button></div>
        </div>
      </div>
      <div class="timeline-event-modal__schedule-row">Dettagli Inspector</div>`;
    document.body.append(modal);
    const body = modal.querySelector<HTMLElement>(
      '.timeline-event-profile-editor__body',
    )!;
    const footer = modal.querySelector<HTMLElement>(
      '.timeline-event-profile-editor__actions',
    )!;
    const result = {
      bodyScrollable: body.scrollHeight > body.clientHeight,
      footerInside:
        footer.getBoundingClientRect().bottom <=
        modal.getBoundingClientRect().bottom,
      inspectorHidden:
        getComputedStyle(
          modal.querySelector('.timeline-event-modal__schedule-row')!,
        ).display === 'none',
      modalWidth: modal.getBoundingClientRect().width,
    };
    modal.remove();
    return result;
  });
  expect(geometry.bodyScrollable).toBe(true);
  expect(geometry.footerInside).toBe(true);
  expect(geometry.inspectorHidden).toBe(true);
  expect(geometry.modalWidth).toBeGreaterThan(680);
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
    modal.style.height = '550px';
    modal.innerHTML = `<div class="timeline-activity-editor timeline-recurring-series-editor"><div class="timeline-activity-editor__body">
      <div class="temporal-create-activity-intervals timeline-activity-editor__intervals">${intervalMarkup.repeat(6)}</div>
      <details class="timeline-recurring-series-editor__repeat-panel" open><summary class="timeline-activity-editor__repeat">Ripeti · Serie attiva</summary>
        <section class="temporal-create-repeat timeline-recurring-series-editor__recurrence">
          <div class="temporal-create-repeat__row">Ripeti ogni giorno</div>
          <div class="temporal-create-repeat__end-row"><span class="temporal-create-repeat__row-label">Termina</span><div class="temporal-create-repeat__end-choices">
            <div class="temporal-create-repeat__end-option"><button class="temporal-create-repeat__end-choice">Mai</button></div>
            <div class="temporal-create-repeat__end-option"><button class="temporal-create-repeat__end-choice">Data</button><input type="date" /></div>
            <div class="temporal-create-repeat__end-option"><button class="temporal-create-repeat__end-choice">Dopo</button><input type="number" value="1" /></div>
          </div></div>
        </section>
      </details>
      <section class="timeline-activity-editor__area-color" aria-label="Life Area"><input placeholder="Life Area (opzionale)" /></section>
      <section class="temporal-create-reality-objectives timeline-activity-editor__outcome" aria-label="Configurazione obiettivi"><div class="timeline-activity-editor__objectives">Obiettivo</div></section>
      </div></div>`;
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
    const endChoices = recurrence.querySelector<HTMLElement>(
      '.temporal-create-repeat__end-choices',
    )!;
    const area = modal.querySelector<HTMLElement>('[aria-label="Life Area"]')!;
    const body = modal.querySelector<HTMLElement>(
      '.timeline-activity-editor__body',
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
      recurrenceContained:
        endChoices.getBoundingClientRect().bottom <=
          recurrence.getBoundingClientRect().bottom + 1 &&
        recurrence.getBoundingClientRect().bottom <=
          area.getBoundingClientRect().top,
      scrollableBody: body.scrollHeight > body.clientHeight,
      scrollbarAtModalEdge:
        Math.abs(
          body.getBoundingClientRect().right -
            modal.getBoundingClientRect().right,
        ) <= 2 &&
        body.getBoundingClientRect().right -
          area.getBoundingClientRect().right >=
          24,
    };
    modal.remove();
    return result;
  }, markup);
  expect(geometry).toEqual({
    fieldsContained: true,
    clockInputsCompact: true,
    clockArrowsCompact: true,
    recurrenceStacked: true,
    recurrenceContained: true,
    scrollableBody: true,
    scrollbarAtModalEdge: true,
  });
});

test('existing Activity and Event recurrence keep the Create layout without overlapping controls', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const create = page.locator('[data-temporal-create="composer"]');
  await create.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await create
    .locator('.temporal-create-u2-repeat select')
    .selectOption('weekly');
  const detail = create.locator('.temporal-create-repeat');
  await expect(detail).toBeVisible();
  const [selectMarkup, detailMarkup] = await Promise.all([
    create
      .locator('.temporal-create-u2-repeat')
      .evaluate((element) => element.outerHTML),
    detail.evaluate((element) => element.outerHTML),
  ]);
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/timeline.css',
  });
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });

  const outcomes = await page.evaluate(
    ({ selectMarkup, detailMarkup }) => {
      const original = document.querySelector<HTMLSelectElement>(
        '[data-temporal-create="composer"] .temporal-create-u2-repeat select',
      )!;
      const originalStyle = getComputedStyle(original);
      return (['activity', 'event'] as const).map((kind) => {
        const modal = document.createElement('div');
        modal.className = 'timeline-event-modal timeline-event-modal--edit';
        modal.style.position = 'absolute';
        modal.style.left = '-2000px';
        modal.style.width = '820px';
        modal.style.height = '640px';
        const editorClass =
          kind === 'activity'
            ? 'timeline-activity-editor'
            : 'timeline-event-profile-editor';
        const bodyClass =
          kind === 'activity'
            ? 'timeline-activity-editor__body'
            : 'timeline-event-profile-editor__body';
        modal.innerHTML = `<div class="${editorClass}"><div class="${bodyClass}">
          <section class="timeline-existing-recurrence">
            ${selectMarkup}${detailMarkup}
            <div class="timeline-existing-recurrence__actions"><button>Avvia ripetizione</button></div>
          </section></div></div>`;
        document.body.append(modal);
        const root = modal.querySelector<HTMLElement>(
          '.timeline-existing-recurrence',
        )!;
        const choice = root.querySelector<HTMLSelectElement>(
          '.temporal-create-u2-repeat select',
        )!;
        const panel = root.querySelector<HTMLElement>(
          '.temporal-create-repeat',
        )!;
        const options = panel.querySelector<HTMLElement>(
          '.temporal-create-repeat__end-choices',
        )!;
        const actions = root.querySelector<HTMLElement>(
          '.timeline-existing-recurrence__actions',
        )!;
        const rootBox = root.getBoundingClientRect();
        const choiceBox = choice.getBoundingClientRect();
        const panelBox = panel.getBoundingClientRect();
        const optionsBox = options.getBoundingClientRect();
        const actionsBox = actions.getBoundingClientRect();
        const style = getComputedStyle(choice);
        const output = {
          kind,
          createSelectorParity: {
            height: style.height === originalStyle.height,
            borderRadius: style.borderRadius === originalStyle.borderRadius,
            fontSize: style.fontSize === originalStyle.fontSize,
          },
          stacked:
            choiceBox.bottom + 8 <= panelBox.top &&
            panelBox.bottom + 8 <= actionsBox.top,
          fullWidth:
            choiceBox.width >= rootBox.width - 2 &&
            panelBox.width >= rootBox.width - 2,
          noOverflow:
            optionsBox.right <= panelBox.right + 1 &&
            optionsBox.bottom <= panelBox.bottom + 1 &&
            actionsBox.right <= rootBox.right + 1,
        };
        modal.remove();
        return output;
      });
    },
    { selectMarkup, detailMarkup },
  );

  expect(outcomes).toEqual([
    {
      kind: 'activity',
      createSelectorParity: {
        height: true,
        borderRadius: true,
        fontSize: true,
      },
      stacked: true,
      fullWidth: true,
      noOverflow: true,
    },
    {
      kind: 'event',
      createSelectorParity: {
        height: true,
        borderRadius: true,
        fontSize: true,
      },
      stacked: true,
      fullWidth: true,
      noOverflow: true,
    },
  ]);
});
