import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

test('Quick and Advanced titles center the same Activity and Event symbols', async ({
  page,
}) => {
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');

  for (const advanced of [false, true]) {
    if (advanced) {
      await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
    }
    for (const [kind, label, shape] of [
      ['activity', 'Attività', 'path'],
      ['event', 'Evento', 'circle'],
    ] as const) {
      await dialog.getByRole('radio', { name: label, exact: true }).click();
      const row = dialog.locator(`[data-authoring-title-kind="${kind}"]`);
      await expect(
        row.locator(`[data-temporal-kind-marker="${kind}"] ${shape}`),
      ).toHaveCount(1);
      const geometry = await row.evaluate((element) => {
        const cell = element.querySelector(
          '.temporal-authoring-title-row__marker',
        )!;
        const icon = cell.querySelector('svg')!;
        const title = element.querySelector('input')!;
        const cellBox = cell.getBoundingClientRect();
        const iconBox = icon.getBoundingClientRect();
        const titleBox = title.getBoundingClientRect();
        return {
          visible: iconBox.width > 0 && iconBox.height > 0,
          centered:
            Math.abs(
              iconBox.left +
                iconBox.width / 2 -
                (cellBox.left + cellBox.width / 2),
            ) < 1 &&
            Math.abs(
              iconBox.top +
                iconBox.height / 2 -
                (cellBox.top + cellBox.height / 2),
            ) < 1,
          beforeTitle: iconBox.right < titleBox.left,
          sameHeight: Math.abs(cellBox.height - titleBox.height) < 2,
        };
      });
      expect(geometry).toEqual({
        visible: true,
        centered: true,
        beforeTitle: true,
        sameHeight: true,
      });
    }
  }
});

test('Quick and Advanced all-day dates use the same bordered control', async ({ page }) => {
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();

  async function checkDates() {
    const dates = dialog.locator('.temporal-create-u2-all-day .temporal-create-date-picker__trigger');
    await expect(dates).toHaveCount(2);
    for (const date of await dates.all()) {
      await expect(date).toHaveCSS('border-top-width', '1px');
      await expect(date).not.toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
    }
    const boxes = await dates.evaluateAll((buttons) => buttons.map((button) => {
      const box = button.getBoundingClientRect();
      return { height: box.height, width: box.width };
    }));
    expect(boxes[0]?.width).toBeGreaterThan(100);
    expect(boxes[0]?.height).toBeGreaterThanOrEqual(44);
    expect(boxes[1]?.height).toBe(boxes[0]?.height);
  }

  await checkDates();
  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
  await checkDates();
  await dialog.getByRole('radio', { name: 'Evento', exact: true }).click();
  await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
  await checkDates();
});

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

test('Advanced Activity and Event share one actual title rail without displaced controls', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();

  async function rail(kind: 'activity' | 'event') {
    const row = dialog.locator(
      `[data-authoring-title-kind="${kind}"].temporal-authoring-title-row.has-tools`,
    );
    await expect(row).toBeVisible();
    return row.evaluate((element) => {
      const marker = element.children.item(0) as HTMLElement | null;
      const name = element.children.item(1) as HTMLElement | null;
      const tools = element.children.item(2) as HTMLElement | null;
      const input = name?.querySelector<HTMLInputElement>('input');
      const lock = tools?.querySelector<HTMLButtonElement>(
        '.temporal-create-placement-lock',
      );
      const kind = element.getAttribute('data-authoring-title-kind');
      const add = element
        .closest('.temporal-create-composer')
        ?.querySelector<HTMLButtonElement>(
          kind === 'activity'
            ? '.temporal-create-activity-tree__root-actions .temporal-create-tree-add'
            : '.temporal-create-event-agenda__root-actions .temporal-create-tree-add',
        );
      if (!marker || !name || !tools || !input || !lock || !add) {
        throw new Error(
          'The shared title row, placement lock or first add action is missing.',
        );
      }
      const outer = element.getBoundingClientRect();
      const icon = marker.getBoundingClientRect();
      const title = name.getBoundingClientRect();
      const actions = tools.getBoundingClientRect();
      const inputBox = input.getBoundingClientRect();
      const lockBox = lock.getBoundingClientRect();
      const addBox = add.getBoundingClientRect();
      const lockStyle = getComputedStyle(lock);
      const addStyle = getComputedStyle(add);
      return {
        children: element.children.length,
        marker: marker
          .querySelector('[data-temporal-kind-marker]')
          ?.getAttribute('data-temporal-kind-marker'),
        centered: (() => {
          const shape = marker.querySelector('svg')?.getBoundingClientRect();
          return !!shape && Math.abs(shape.left + shape.width / 2 - (icon.left + icon.width / 2)) < 1;
        })(),
        height: outer.height,
        radius: getComputedStyle(element).borderRadius,
        fontSize: getComputedStyle(input).fontSize,
        markerWidth: icon.width,
        iconBeforeTitle: Math.abs(icon.right - title.left) <= 2,
        titleBeforeActions: Math.abs(title.right - actions.left) <= 2,
        titleNotOverlaid: inputBox.left >= icon.right - 2,
        actionsInside: actions.right <= outer.right + 1,
        commonBaseline:
          Math.abs(icon.top - title.top) <= 2 &&
          Math.abs(title.top - actions.top) <= 2 &&
          Math.abs(inputBox.top - title.top) <= 2,
        titleWidth: title.width,
        actionsWidth: actions.width,
        lockFontSize: lockStyle.fontSize,
        lockFontWeight: lockStyle.fontWeight,
        lockPadding: lockStyle.paddingInline,
        lockIconWidth: lock.querySelector('svg')?.getBoundingClientRect().width,
        lockHeight: lockBox.height,
        addFontSize: addStyle.fontSize,
        addPadding: addStyle.paddingInline,
        addHeight: addBox.height,
        addLeftOffset: addBox.left - outer.left,
        addTopGap: addBox.top - outer.bottom,
      };
    });
  }

  const objectivePanel = dialog.locator('.temporal-create-reality-objectives');
  const objectiveHeading = objectivePanel.locator(
    '.temporal-create-reality-objectives__block-copy strong',
  );
  await expect(objectiveHeading).toBeVisible();
  const activityHeadingTopGap = await objectiveHeading.evaluate((heading) => {
    const panel = heading.closest('.temporal-create-reality-objectives');
    if (!panel) throw new Error('Objective panel is missing.');
    return (
      heading.getBoundingClientRect().top - panel.getBoundingClientRect().top
    );
  });
  expect(activityHeadingTopGap).toBeGreaterThan(10);
  expect(activityHeadingTopGap).toBeLessThan(23);

  const activity = await rail('activity');
  const eventChoice = dialog.getByRole('radio', {
    name: 'Evento',
    exact: true,
  });
  await expect(eventChoice).toBeEnabled();
  await eventChoice.click();
  await expect(eventChoice).toHaveAttribute('aria-checked', 'true');
  const event = await rail('event');
  const eventHeadingTopGap = await objectiveHeading.evaluate((heading) => {
    const panel = heading.closest('.temporal-create-reality-objectives');
    if (!panel) throw new Error('Objective panel is missing.');
    return (
      heading.getBoundingClientRect().top - panel.getBoundingClientRect().top
    );
  });
  expect(eventHeadingTopGap).toBeCloseTo(activityHeadingTopGap, 0);
  expect(eventHeadingTopGap).toBeLessThan(23);

  for (const result of [activity, event]) {
    expect(result.children).toBe(3);
    expect(result.iconBeforeTitle).toBe(true);
    expect(result.titleBeforeActions).toBe(true);
    expect(result.titleNotOverlaid).toBe(true);
    expect(result.actionsInside).toBe(true);
    expect(result.commonBaseline).toBe(true);
    expect(result.centered).toBe(true);
    expect(result.titleWidth).toBeGreaterThan(200);
    expect(result.actionsWidth).toBeGreaterThan(40);
    expect(result.height).toBeGreaterThanOrEqual(50);
    expect(result.height).toBeLessThan(60);
  }

  expect(activity.marker).toBe('activity');
  expect(event.marker).toBe('event');
  expect(activity.height).toBeCloseTo(event.height, 0);
  expect(activity.markerWidth).toBe(event.markerWidth);
  expect(activity.radius).toBe(event.radius);
  expect(activity.fontSize).toBe(event.fontSize);
  for (const key of [
    'lockFontSize',
    'lockFontWeight',
    'lockPadding',
    'lockIconWidth',
    'lockHeight',
    'addFontSize',
    'addPadding',
    'addHeight',
  ] as const) {
    expect(activity[key]).toBe(event[key]);
  }
  expect(activity.lockFontSize).toBe('16px');
  expect(activity.addLeftOffset).toBeCloseTo(event.addLeftOffset, 0);
  expect(activity.addTopGap).toBeCloseTo(event.addTopGap, 0);
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
  // Both surfaces use the approved configurable authoring scale. Quick keeps
  // its compact geometry and smaller mode choices, not the retired tiny text.
  const authoringScale = await dialog.evaluate((element) => {
    const css = getComputedStyle(element);
    return {
      section: css.getPropertyValue('--dante-temporal-section-title-size').trim(),
      action: css.getPropertyValue('--dante-temporal-action-text-size').trim(),
      form: css.getPropertyValue('--dante-temporal-form-text-size').trim(),
    };
  });
  await expect(
    dialog.locator('.temporal-create-type-grid strong').first(),
  ).toHaveCSS('font-size', authoringScale.section);
  await expect(
    dialog.locator('.temporal-create-choice-row > button').first(),
  ).toHaveCSS('font-size', '13.5px');
  const footer = dialog.locator('.temporal-create-actions');
  for (const button of await footer.locator(':scope > button').all()) {
    await expect(button).toHaveCSS('font-size', authoringScale.action);
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
  const quickLayout = async () => dialog.locator('.temporal-create-u2-when').evaluate((element) => {
    const frame = element.getBoundingClientRect();
    const labels = Array.from(element.querySelectorAll<HTMLElement>(
      ':scope > .temporal-create-quick-timing-label',
    ));
    const dates = Array.from(element.querySelectorAll<HTMLElement>(
      ':scope > .temporal-create-u2-date-field .temporal-create-date-picker__trigger, :scope > .temporal-create-date-picker .temporal-create-date-picker__trigger',
    ));
    const clocks = Array.from(element.querySelectorAll<HTMLElement>(
      ':scope > .temporal-create-time-control .temporal-create-time-control__field',
    ));
    return {
      labels: labels.map((label) => label.textContent?.trim()),
      bandActions: element.querySelectorAll(':scope > .temporal-create-time-band-control').length,
      pairs: dates.map((button, index) => {
        const clock = clocks[index];
        const label = labels[index];
        if (!clock || !label) throw new Error('Quick timing pair is missing.');
        const date = button.getBoundingClientRect();
        const time = clock.getBoundingClientRect();
        return {
          date: button.textContent?.trim() ?? '',
          accessible: button.getAttribute('aria-label') ?? '',
          noInnerCaption: button.querySelector('.temporal-create-date-picker__caption') === null,
          aligned: Math.abs(date.top - time.top) <= 1,
          sameWidth: Math.abs(date.width - time.width) <= 1,
          sameHeight: Math.abs(date.height - time.height) <= 1,
          timeBeforeDate: time.right <= date.left,
          labelAbove: label.getBoundingClientRect().bottom <= time.top,
          fits: time.left >= frame.left - 1 && date.right <= frame.right + 1
            && button.scrollWidth <= button.clientWidth + 1
            && clock.scrollWidth <= clock.clientWidth + 1,
        };
      }),
    };
  });
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    const layout = await quickLayout();
    expect(layout.labels).toEqual(['Inizio', 'Fine']);
    expect(layout.bandActions).toBe(0);
    expect(layout.pairs).toHaveLength(2);
    for (const pair of layout.pairs) {
      expect(pair.date).toMatch(/^[^,]+, \d{1,2} [\p{L}]+(?: \d{4})?$/u);
      expect(pair.accessible).toMatch(/^(Data inizio|Data fine): [^,]+, /);
      expect(pair.noInnerCaption).toBe(true);
      expect(pair.aligned).toBe(true);
      expect(pair.sameWidth).toBe(true);
      expect(pair.sameHeight).toBe(true);
      expect(pair.timeBeforeDate).toBe(true);
      expect(pair.labelAbove).toBe(true);
      expect(pair.fits).toBe(true);
    }
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  const quickClocks = dialog.locator(
    '.temporal-create-u2-when > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(quickClocks).toHaveCount(2);
  for (const clock of await quickClocks.all()) {
    await expect(clock).toHaveCSS('min-height', '48px');
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
  await expect(advancedWhen.locator(':scope > .temporal-create-time-band-control'))
    .toHaveCount(1);
  await expect(
    dialog.getByRole('region', { name: 'Configurazione obiettivi' }),
  ).toBeVisible();
  await expect(dialog.locator('.temporal-create-reality-mode')).toHaveCount(0);
  await expect(
    dialog.locator('.temporal-create-choice-row > button').first(),
  ).toHaveCSS('font-size', authoringScale.form);
  // Both modes share the action scale while their panel geometry differs.
  for (const button of await footer.locator(':scope > button').all()) {
    await expect(button).toHaveCSS('font-size', authoringScale.action);
  }
  // The shared bordered timing section now uses its available width instead
  // of the retired 820px cap, keeping the primary and added interval aligned.
  await expect(advancedWhen).toHaveCSS('max-width', 'none');
  await expectEditStyleChevrons(advancedWhen);
  const advancedControls = advancedWhen.locator(
    ':scope > .temporal-create-time-control .temporal-create-time-control__field',
  );
  await expect(advancedControls).toHaveCount(2);
  for (const clock of await advancedControls.all()) {
    await expect(clock).toHaveCSS('min-height', '46px');
  }

  // A full objective form exists only in Advanced, and uses the shared row.
  await dialog.getByRole('button', { name: '+ Obiettivo', exact: true }).click();
  await expect(dialog.locator('.temporal-create-objective__row')).toHaveCount(
    1,
  );
  await expect(
    dialog.getByRole('textbox', { name: 'Obiettivo 1' }),
  ).toBeVisible();
  await expect(
    dialog.getByRole('combobox', { name: 'Verifica obiettivo 1' }),
  ).toBeVisible();

  // The same browser test already owns the Advanced form; check the
  // newly standardized remove-first behavior without another fixture run.
  await dialog.getByRole('button', { name: 'Aggiungi intervallo' }).click();
  await expect(dialog.getByRole('button', {
    name: 'Rimuovi intervallo 1',
  })).toBeVisible();
  await expect(dialog.getByRole('button', {
    name: 'Rimuovi intervallo 2',
  })).toBeVisible();
  await dialog.getByRole('button', { name: 'Rimuovi intervallo 1' }).click();
  await expect(dialog.getByRole('button', {
    name: /^Rimuovi intervallo/,
  })).toHaveCount(0);
  await expect(dialog.getByText('Intervallo 1', { exact: true }))
    .toHaveCount(0);

  // Once back to a single interval, dual-boundary timezone editing is
  // eligible. Cancel must discard the unsaved zone configuration.
  const zoneTrigger = dialog.getByRole('button', { name: /^Fuso orario:/ });
  await zoneTrigger.click();
  const zoneDialog = page.getByRole('dialog', { name: 'Imposta fuso orario' });
  await expect(zoneDialog).toHaveCSS('background-color', 'rgb(13, 21, 36)');
  await expect(
    zoneDialog.locator('.temporal-zone-dialog__choice').first(),
  ).toHaveCSS('background-color', 'rgb(23, 36, 56)');
  await zoneDialog.getByRole('checkbox', {
    name: 'Utilizza fusi orari diversi per inizio e fine',
  }).check();
  await expect(zoneDialog.getByText('Fuso orario di fine', { exact: true }))
    .toBeVisible();
  await zoneDialog.getByRole('button', { name: 'Annulla' }).click();
  await expect(zoneTrigger).not.toHaveAttribute('aria-label', /Personalizzato/);
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

test('Advanced Create only shows Sessioni attività after the first Session', async ({
  page,
}) => {
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();
  const heading = dialog.locator('.temporal-create-activity-tree__group-label');
  await expect(heading).toHaveCount(0);
  await dialog.getByRole('button', { name: 'Sessione', exact: true }).click();
  await expect(heading).toHaveText('Sessioni attività');
  await expect(heading).toHaveCSS('font-size', '15px');
  await expect(heading).toHaveCSS('text-transform', 'none');
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
    expect(surface.titleSize).toBe('18px');
    expect(surface.titleCase).toBe('none');
    expect(surface.titleWeight).toBe('650');
    expect(surface.actionSize).toBe('16px');
    expect(surface.actionHeight).toBeGreaterThanOrEqual(44);
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
      <section class="timeline-activity-editor__area-color" aria-label="Life Area"><input placeholder="Area (opzionale)" /></section>
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

test('Activity and Event repeat selectors stay inside one shared panel in Create and Edit CSS', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const create = page.locator('[data-temporal-create="composer"]');
  await create.getByRole('button', { name: /Opzioni avanzate/ }).click();

  async function checkRealPanel(kind: 'activity' | 'event') {
    const panel = create.getByRole('region', {
      name: 'Ripetizione',
      exact: true,
    });
    await expect(panel).toHaveAttribute('data-recurrence-owner', kind);
    const choice = panel.getByRole('combobox', { name: 'Ripeti' });
    await choice.selectOption('none');
    await expect(panel).toHaveAttribute('data-recurrence-expanded', 'false');
    await expect(
      panel.locator('.temporal-recurrence-panel__details'),
    ).toHaveCount(0);

    await choice.selectOption('weekly');
    await expect(panel).toHaveAttribute('data-recurrence-expanded', 'true');
    const details = panel.locator('.temporal-recurrence-panel__details');
    await expect(details).toBeVisible();
    await expect(details.locator('.temporal-create-repeat')).toHaveCount(1);
    await expect(panel).toHaveCSS('background-color', 'rgb(17, 28, 45)');
    await expect(choice).toHaveCSS('font-size', '17px');
    await expect(choice).toHaveCSS('background-color', 'rgb(17, 27, 45)');
    await expect(choice.locator('option').first()).toHaveCSS(
      'background-color',
      'rgb(17, 27, 45)',
    );
    await expect(choice.locator('option:checked')).toHaveCSS(
      'background-color',
      'rgb(44, 59, 83)',
    );
    await expect(
      details.locator('.temporal-create-repeat__row-label').first(),
    ).toHaveCSS('font-size', '17px');
    await expect(
      panel.getByRole('heading', { name: 'Ripetizione' }),
    ).toHaveCount(1);

    const layout = await panel.evaluate((element) => {
      const heading = element.querySelector<HTMLElement>(
        '.temporal-recurrence-panel__heading',
      )!;
      const selector = element.querySelector<HTMLElement>(
        '.temporal-recurrence-panel__choice',
      )!;
      const content = element.querySelector<HTMLElement>(
        '.temporal-recurrence-panel__details',
      )!;
      const end = content.querySelector<HTMLElement>(
        '.temporal-create-repeat__end-choices',
      )!;
      const bounds = element.getBoundingClientRect();
      const headingBox = heading.getBoundingClientRect();
      const selectorBox = selector.getBoundingClientRect();
      const contentBox = content.getBoundingClientRect();
      const endBox = end.getBoundingClientRect();
      return {
        headingBeforeSelector: headingBox.bottom <= selectorBox.top + 1,
        selectorBeforeDetails: selectorBox.bottom <= contentBox.top + 1,
        allInsidePanel: [headingBox, selectorBox, contentBox, endBox].every(
          (box) =>
            box.left >= bounds.left - 1 &&
            box.right <= bounds.right + 1 &&
            box.bottom <= bounds.bottom + 1,
        ),
        headingCount: element.querySelectorAll(
          '.temporal-recurrence-panel__heading',
        ).length,
        detailCardCount: element.querySelectorAll(
          '.temporal-recurrence-panel__details',
        ).length,
      };
    });
    expect(layout).toEqual({
      headingBeforeSelector: true,
      selectorBeforeDetails: true,
      allInsidePanel: true,
      headingCount: 1,
      detailCardCount: 1,
    });
    return panel.evaluate((element) => element.outerHTML);
  }

  const activityMarkup = await checkRealPanel('activity');
  await create.getByRole('radio', { name: 'Evento', exact: true }).click();
  const eventMarkup = await checkRealPanel('event');

  // The same actual component markup must also remain a single bounded rail
  // under both Edit modal styles. No synthetic legacy action buttons.
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });
  const editLayouts = await page.evaluate(
    ({ activityMarkup, eventMarkup }) =>
      (
        [
          ['activity', activityMarkup],
          ['event', eventMarkup],
        ] as const
      ).map(([kind, markup]) => {
        const modal = document.createElement('div');
        modal.className = 'timeline-event-modal timeline-event-modal--edit';
        modal.style.position = 'absolute';
        modal.style.left = '-2000px';
        modal.style.width = '820px';
        const editorClass =
          kind === 'activity'
            ? 'timeline-activity-editor'
            : 'timeline-event-profile-editor';
        const bodyClass =
          kind === 'activity'
            ? 'timeline-activity-editor__body'
            : 'timeline-event-profile-editor__body';
        modal.innerHTML = `<div class="${editorClass}"><div class="${bodyClass}">
          ${markup}
        </div></div>`;
        document.body.append(modal);
        try {
          const root = modal.querySelector<HTMLElement>(
            '.temporal-recurrence-panel',
          )!;
          const select = root.querySelector<HTMLSelectElement>(
            '.temporal-recurrence-panel__choice select',
          )!;
          const detail = root.querySelector<HTMLElement>(
            '.temporal-recurrence-panel__details',
          )!;
          const end = detail.querySelector<HTMLElement>(
            '.temporal-create-repeat__end-choices',
          )!;
          const box = root.getBoundingClientRect();
          const choiceBox = select.getBoundingClientRect();
          const detailBox = detail.getBoundingClientRect();
          const endBox = end.getBoundingClientRect();
          return {
            kind,
            hasSinglePanel:
              root.querySelectorAll('.temporal-recurrence-panel__heading')
                .length === 1,
            noExtraMutationAction:
              root.querySelectorAll('.timeline-existing-recurrence__actions')
                .length === 0,
            sectionBackground: getComputedStyle(root).backgroundColor,
            selectorFont: getComputedStyle(select).fontSize,
            selectorBackground: getComputedStyle(select).backgroundColor,
            selectedOptionBackground: getComputedStyle(
              select.selectedOptions[0]!,
            ).backgroundColor,
            unselectedOptionBackground: getComputedStyle(
              select.options[1]!,
            ).backgroundColor,
            settingFont: getComputedStyle(
              detail.querySelector<HTMLElement>(
                '.temporal-create-repeat__row-label',
              )!,
            ).fontSize,
            stacked: choiceBox.bottom <= detailBox.top,
            contained:
              choiceBox.left >= box.left - 1 &&
              detailBox.left >= box.left - 1 &&
              endBox.right <= box.right + 1 &&
              endBox.bottom <= box.bottom + 1,
          };
        } finally {
          modal.remove();
        }
      }),
    { activityMarkup, eventMarkup },
  );
  expect(editLayouts).toEqual([
    {
      kind: 'activity',
      hasSinglePanel: true,
      noExtraMutationAction: true,
      sectionBackground: 'rgb(17, 28, 45)',
      selectorFont: '17px',
      selectorBackground: 'rgb(17, 27, 45)',
      selectedOptionBackground: 'rgb(44, 59, 83)',
      unselectedOptionBackground: 'rgb(17, 27, 45)',
      settingFont: '17px',
      stacked: true,
      contained: true,
    },
    {
      kind: 'event',
      hasSinglePanel: true,
      noExtraMutationAction: true,
      sectionBackground: 'rgb(17, 28, 45)',
      selectorFont: '17px',
      selectorBackground: 'rgb(17, 27, 45)',
      selectedOptionBackground: 'rgb(44, 59, 83)',
      unselectedOptionBackground: 'rgb(17, 27, 45)',
      settingFont: '17px',
      stacked: true,
      contained: true,
    },
  ]);

  // Series Edit has different recurrence families, but the same visual scale
  // and native dropdown palette as Create and ordinary Edit.
  const seriesStyle = await page.evaluate(() => {
    const modal = document.createElement('div');
    modal.className = 'timeline-event-modal timeline-event-modal--edit';
    modal.style.position = 'absolute';
    modal.style.left = '-2000px';
    modal.innerHTML = `<div class="timeline-activity-editor timeline-recurring-series-editor">
      <div class="timeline-activity-editor__body">
        <section class="temporal-recurrence-panel">
          <h3 class="temporal-recurrence-panel__heading">Ripetizione</h3>
          <div class="temporal-recurrence-panel__choice">
            <div class="temporal-recurrence-panel__frequency">
              <select aria-label="Ripeti"><option>Ogni giorno</option><option>Ogni settimana</option></select>
            </div>
          </div>
          <div class="temporal-recurrence-panel__details">
            <section class="temporal-create-repeat timeline-recurring-series-editor__recurrence">
              <div class="temporal-create-repeat__row">
                <span class="temporal-create-repeat__row-label">Ripeti ogni</span>
                <input class="temporal-create-repeat__interval" type="number" value="1" />
              </div>
            </section>
          </div>
        </section>
      </div>
    </div>`;
    document.body.append(modal);
    try {
      const select = modal.querySelector<HTMLSelectElement>('select')!;
      const label = modal.querySelector<HTMLElement>(
        '.temporal-create-repeat__row-label',
      )!;
      const input = modal.querySelector<HTMLInputElement>('input')!;
      return {
        selectorFont: getComputedStyle(select).fontSize,
        selectorBackground: getComputedStyle(select).backgroundColor,
        selectedOptionBackground: getComputedStyle(
          select.selectedOptions[0]!,
        ).backgroundColor,
        unselectedOptionBackground: getComputedStyle(
          select.options[1]!,
        ).backgroundColor,
        settingFont: getComputedStyle(label).fontSize,
        inputFont: getComputedStyle(input).fontSize,
      };
    } finally {
      modal.remove();
    }
  });
  expect(seriesStyle).toEqual({
    selectorFont: '17px',
    selectorBackground: 'rgb(17, 27, 45)',
    selectedOptionBackground: 'rgb(44, 59, 83)',
    unselectedOptionBackground: 'rgb(17, 27, 45)',
    settingFont: '17px',
    inputFont: '17px',
  });
});

test('Quick Create and Inspector share the muted navy palette without recoloring Life Areas', async ({
  page,
}) => {
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const quick = page.locator('[data-temporal-create="composer"]');
  await expect(quick).toHaveCSS('background-color', 'rgb(13, 21, 36)');
  for (const selector of [
    '.temporal-create-date-picker__trigger',
    '.temporal-create-time-control__field',
    '.temporal-create-life-area-field__area-cell input',
    '.temporal-create-u2-location',
    '.temporal-create-quick-reminder',
  ]) {
    await expect(quick.locator(selector).first()).toHaveCSS(
      'background-color',
      'rgb(23, 36, 56)',
    );
  }

  // CSS fixture: backend-free presentation proof, including the live Area accent.
  const inspector = await page.evaluate(() => {
    const modal = document.createElement('div');
    modal.className = 'timeline-event-modal timeline-event-modal--inspector';
    modal.style.setProperty('--timeline-inspector-accent', '#14ab82');
    modal.innerHTML = `<div class="timeline-event-modal__header"></div>
      <div class="timeline-objective-controls__item">
        <input aria-label="Valore" />
        <select aria-label="Risultato"><option>Sì</option><option>No</option></select>
      </div>`;
    document.body.append(modal);
    try {
      return {
        surface: getComputedStyle(modal).backgroundColor,
        accent: getComputedStyle(modal).borderColor,
        header: getComputedStyle(modal.querySelector('.timeline-event-modal__header')!).backgroundColor,
        section: getComputedStyle(modal.querySelector('.timeline-objective-controls__item')!).backgroundColor,
        input: getComputedStyle(modal.querySelector('input')!).backgroundColor,
        selectedMenu: getComputedStyle(modal.querySelector('select option:checked')!)
          .backgroundColor,
        unselectedMenu: getComputedStyle(
          modal.querySelector('select option:not(:checked)')!,
        ).backgroundColor,
      };
    } finally {
      modal.remove();
    }
  });
  expect(inspector).toEqual({
    surface: 'rgb(13, 21, 36)',
    accent: 'rgb(20, 171, 130)',
    header: 'rgb(13, 21, 36)',
    section: 'rgb(17, 28, 45)',
    input: 'rgb(23, 36, 56)',
    selectedMenu: 'rgb(44, 59, 83)',
    unselectedMenu: 'rgb(17, 27, 45)',
  });
});

test('Advanced Activity and Event headings, Objectives and native menus share one readable scale', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog.getByRole('button', { name: /Opzioni avanzate/ }).click();

  for (const kind of ['Attività', 'Evento']) {
    await dialog.getByRole('radio', { name: kind, exact: true }).click();
    for (const heading of [
      dialog.locator('.temporal-recurrence-panel__heading'),
      dialog.locator('.temporal-editor-area-section > strong'),
      dialog.locator('.temporal-create-reality-objectives__block-copy strong'),
      dialog.locator('.temporal-create-description-section h3'),
    ]) {
      await expect(heading).toHaveCSS('font-size', '18px');
    }

    for (const section of [
      dialog.locator('.temporal-create-timing-section'),
      dialog.locator('.temporal-recurrence-panel'),
      dialog.locator('.temporal-editor-area-section'),
      dialog.locator('.temporal-create-reality-objectives'),
      dialog.locator('.temporal-create-description-section'),
    ]) {
      await expect(section).toHaveCSS('background-color', 'rgb(17, 28, 45)');
    }

    const location = dialog.getByRole('textbox', { name: 'Località' });
    const reminderFrame = dialog.locator('.temporal-create-quick-reminder');
    const description = dialog.locator('.temporal-create-description-section');
    const descriptionInput = description.locator(
      'textarea.temporal-create-advanced-description',
    );
    await expect(location).toHaveCSS('height', '44px');
    await expect(location).toHaveCSS('margin-top', '0px');
    await expect(location).toHaveCSS('font-size', '16px');
    await expect(location).toHaveCSS('background-color', 'rgb(23, 36, 56)');
    await expect(reminderFrame).toHaveCSS('min-height', '44px');
    await expect(reminderFrame).toHaveCSS('margin-top', '0px');
    await expect(reminderFrame).toHaveCSS('background-color', 'rgb(23, 36, 56)');
    await expect(description).toHaveCSS('padding-top', '10px');
    await expect(description).toHaveCSS('margin-top', '0px');
    await expect(description).toHaveCSS('background-color', 'rgb(17, 28, 45)');
    await expect(descriptionInput).toHaveCSS('min-height', '112px');
    await expect(descriptionInput).toHaveCSS('margin-top', '0px');
    await expect(descriptionInput).toHaveCSS('font-size', '16px');
    await expect(descriptionInput).toHaveCSS('background-color', 'rgb(23, 36, 56)');

    await dialog.getByRole('button', { name: '+ Obiettivo', exact: true }).click();
    const objective = dialog.locator('.temporal-create-objective').last();
    await expect(
      objective.locator('.temporal-create-objective__title'),
    ).toHaveCSS('font-size', '16px');
    const result = objective
      .locator('.temporal-create-objective__definition select')
      .first();
    await expect(result).toHaveCSS('font-size', '16px');
    await expect(
      objective.locator('.temporal-create-objective__definition label').first(),
    ).toHaveCSS('font-size', '14px');
    await expect(
      objective.locator('.temporal-create-objective__verification select'),
    ).toHaveCSS('font-size', '16px');
    await expect(
      objective.locator('.temporal-create-objective__definition'),
    ).toHaveCSS('background-color', 'rgb(17, 28, 45)');
    await expect(
      objective.locator('.temporal-create-objective__verification'),
    ).toHaveCSS('background-color', 'rgb(17, 28, 45)');
    const reminder = dialog.getByRole('combobox', { name: 'Ricorda' });
    await expect(reminder).toHaveCSS('font-size', '16px');
    await expect(result.locator('option:not(:checked)').first()).toHaveCSS(
      'background-color',
      'rgb(17, 27, 45)',
    );
    await expect(result.locator('option:checked')).toHaveCSS(
      'background-color',
      'rgb(44, 59, 83)',
    );
    await reminder.click();
    const reminderMenu = page.getByRole('listbox', { name: 'Ricorda' });
    await expect(
      reminderMenu.getByRole('option', { name: 'Ricorda · Nessuno' }),
    ).toHaveCSS(
      'background-color',
      'rgb(44, 59, 83)',
    );
    await expect(
      reminderMenu.getByRole('option', { name: 'Ricorda · 5 min prima' }),
    ).toHaveCSS(
      'background-color',
      'rgb(17, 27, 45)',
    );
    await reminder.press('Escape');
    await expect(reminderMenu).toHaveCount(0);
    await expect(dialog).toBeVisible();
    await reminder.click();
    await reminderMenu.getByRole('option', {
      name: 'Ricorda · 15 min prima',
    }).click();
    await expect(reminder).toContainText('15 min prima');

    await result.selectOption('quantity');
    await expect(
      objective.getByRole('spinbutton', {
        name: /Target obiettivo|Valore obiettivo/,
      }),
    ).toBeVisible();
    await result.selectOption('range');
    await expect(
      objective.getByRole('spinbutton', { name: 'Minimo obiettivo' }),
    ).toBeVisible();
    await result.selectOption('qualitative');
    await expect(
      objective.locator('.temporal-create-objective__hint'),
    ).toHaveCount(0);
    await result.selectOption('boolean');
    await expect(
      objective.locator('.temporal-create-objective__hint'),
    ).toHaveCount(0);
  }

  // Reuse the rendered controls under the Edit CSS without requiring a backend
  // fixture; this checks presentation, while Save behavior belongs to Edit E2E.
  await page.addStyleTag({
    path: 'src/features/home/ui/timeline/activity-edit-panel.css',
  });
  const editStyle = await page.evaluate(() => {
    const create = document.querySelector('[data-temporal-create="composer"]')!;
    const modal = document.createElement('div');
    modal.className = 'timeline-event-modal timeline-event-modal--edit';
    modal.style.position = 'absolute';
    modal.style.left = '-2000px';
    modal.innerHTML = `<div class="timeline-activity-editor"><div class="timeline-activity-editor__body">${[
      '.temporal-editor-area-section',
      '.temporal-create-reality-objectives',
      '.temporal-create-description-section',
      '.temporal-create-quick-reminder',
      '.temporal-create-u2-location',
    ]
      .map((selector) => create.querySelector(selector)!.outerHTML)
      .join('')}</div></div>`;
    document.body.append(modal);
    try {
      const style = (selector: string) =>
        getComputedStyle(modal.querySelector<HTMLElement>(selector)!).fontSize;
      return {
        area: style('.temporal-editor-area-section > strong'),
        objectives: style(
          '.temporal-create-reality-objectives__block-copy strong',
        ),
        description: style('.temporal-create-description-section h3'),
        result: style('.temporal-create-objective__definition select'),
        reminder: style('.temporal-create-quick-reminder > button'),
        areaSurface: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-editor-area-section')!,
        ).backgroundColor,
        objectiveSurface: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-create-reality-objectives')!,
        ).backgroundColor,
        descriptionSurface: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-create-description-section')!,
        ).backgroundColor,
        location: style('.temporal-create-u2-location'),
        descriptionInput: style(
          '.temporal-create-description-section textarea',
        ),
        locationHeight: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-create-u2-location')!,
        ).height,
        reminderHeight: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-create-quick-reminder')!,
        ).minHeight,
        descriptionPadding: getComputedStyle(
          modal.querySelector<HTMLElement>('.temporal-create-description-section')!,
        ).paddingTop,
      };
    } finally {
      modal.remove();
    }
  });
  expect(editStyle).toEqual({
    area: '18px',
    objectives: '18px',
    description: '18px',
    result: '16px',
    reminder: '16px',
    areaSurface: 'rgb(17, 28, 45)',
    objectiveSurface: 'rgb(17, 28, 45)',
    descriptionSurface: 'rgb(17, 28, 45)',
    location: '16px',
    descriptionInput: '16px',
    locationHeight: '44px',
    reminderHeight: '44px',
    descriptionPadding: '10px',
  });
});
