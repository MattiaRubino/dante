import {
  expect,
  test,
  type Locator,
  type Page,
  type TestInfo,
} from '@playwright/test';

const password = 'correct horse battery staple';
const E2E_RESPONSE_TIMEOUT_MS = 10_000;
const BLUE = '#4285F4';
const DEFAULT_ORANGE = '#EA5C12';

const projectEmail: Readonly<Record<string, string>> = {
  chromium: 'synthetic.user+e2e-55@example.com',
  firefox: 'synthetic.user+e2e-56@example.com',
};

function requireGoldenProject(testInfo: TestInfo): void {
  test.skip(
    testInfo.project.name === 'webkit',
    'Life Area golden gate requires Chromium and Firefox real-stack proof.',
  );
  if (!['chromium', 'firefox'].includes(testInfo.project.name)) {
    throw new Error(
      `Unsupported Life Area golden browser project: ${testInfo.project.name}`,
    );
  }
}

function emailFor(testInfo: TestInfo): string {
  const email = projectEmail[testInfo.project.name];
  if (!email) {
    throw new Error(
      `Unsupported Life Area golden browser project: ${testInfo.project.name}`,
    );
  }
  return email;
}

async function useItalianLocale(page: Page): Promise<void> {
  await page.addInitScript(() => {
    window.localStorage.setItem('dante.locale', 'it');
  });
}

async function signIn(page: Page, email: string): Promise<void> {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
  ).toBeVisible();
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);

  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/auth/signin') &&
      response.request().method() === 'POST',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
  await page.getByRole('button', { name: 'Accedi', exact: true }).click();
  expect((await responsePromise).status()).toBe(200);
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
  ).toBeVisible();
}

function waitForTimelineRead(page: Page) {
  return page.waitForResponse(
    (response) =>
      response.url().includes('/api/v1/temporal/timeline/window') &&
      response.request().method() === 'GET',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
}

function waitForUnplacedRead(page: Page) {
  return page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/temporal/activities/unplaced') &&
      response.request().method() === 'GET',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
}

async function openHome(page: Page): Promise<void> {
  const timeline = waitForTimelineRead(page);
  const unplaced = waitForUnplacedRead(page);
  await page.goto('/home');
  expect((await timeline).status()).toBe(200);
  expect((await unplaced).status()).toBe(200);
  await expect(page.locator('[data-temporal-read-state="ready"]')).toBeVisible();
}

async function openCreate(page: Page, kind: 'activity' | 'event' = 'activity') {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  if (kind === 'event') {
    await dialog.getByRole('radio', { name: 'Evento' }).click();
  }
  return dialog;
}

async function readJson<T>(page: Page, path: string): Promise<T> {
  const result = await page.evaluate(async (requestPath) => {
    const response = await fetch(requestPath, {
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json, application/problem+json',
        'X-Dante-Client': 'web',
        'X-Dante-Time-Zone': 'Europe/Rome',
      },
    });
    return {
      status: response.status,
      payload: await response.json(),
    };
  }, path);
  expect(result.status).toBe(200);
  return result.payload as T;
}

function uuidField(payload: Record<string, unknown>, field: string): string {
  const value = payload[field];
  expect(typeof value).toBe('string');
  if (typeof value !== 'string') {
    throw new Error(`${field} was not a string.`);
  }
  return value;
}

async function chooseBlue(dialog: Locator): Promise<void> {
  await dialog
    .getByRole('button', { name: 'Colore attività o evento' })
    .click();
  const palette = dialog.page().getByRole('dialog', { name: 'Scegli colore' });
  await expect(palette).toBeVisible();
  await palette.getByRole('button', { name: 'Blu' }).click();
}

async function expectGroupColor(
  page: Page,
  lifeAreaRef: string,
  lifeAreaName: string,
  colorCode: string,
): Promise<void> {
  const chip = page.locator(
    `.dante-timeline-group-chip[data-group-id="${lifeAreaRef}"]`,
  );
  await expect(chip).toBeVisible();
  await expect(chip).toContainText(lifeAreaName);
  await expect
    .poll(() =>
      chip.evaluate((element) =>
        (element as HTMLElement).style
          .getPropertyValue('--timeline-group-color')
          .trim()
          .toUpperCase(),
      ),
    )
    .toBe(colorCode);
}

async function expectTimedCardColor(
  page: Page,
  title: string,
  lifeAreaName: string | null,
  colorCode: string,
): Promise<void> {
  const card = page.locator('.timeline-event-card').filter({ hasText: title });
  await expect(card).toBeVisible();
  if (lifeAreaName === null) {
    await expect(card).not.toContainText(/Senza Life Area/);
  } else {
    await expect(card).toContainText(lifeAreaName);
  }
  await expect
    .poll(() =>
      card.evaluate((element) =>
        (element as HTMLElement).style
          .getPropertyValue('--timeline-group-color')
          .trim()
          .toUpperCase(),
      ),
    )
    .toBe(colorCode);
}

type LifeAreaRow = Readonly<{
  life_area_ref: string;
  name: string;
  revision: number;
  color_code: string | null;
}>;

type AssignmentRow = Readonly<{
  subject_kind: 'activity' | 'event';
  subject_native_ref: string;
  life_area_ref: string;
  assignment_revision: number;
}>;

type RoutineRow = Readonly<{
  routine_ref: string;
  title: string;
  life_area_ref: string | null;
  life_area_assignment_revision: number | null;
}>;

test.describe('Temporal Create Life Area golden gate', () => {
  test('one-off Activity/Event preserve create/existing/none Life Area truth and colours across reload', async ({
    browser,
  }, testInfo) => {
    requireGoldenProject(testInfo);
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo));
      await openHome(page);

      const tag = testInfo.project.name;
      const areaName = `Golden Corpo ${tag}`;
      const activityTitle = `Golden Activity area ${tag}`;
      const eventTitle = `Golden Event area ${tag}`;
      const noAreaActivityTitle = `Golden Activity no area ${tag}`;
      const noAreaEventTitle = `Golden Event no area ${tag}`;

      let dialog = await openCreate(page);
      await dialog.getByRole('textbox', { name: 'Titolo' }).fill(activityTitle);
      await dialog.getByLabel('Ora').fill('09:10');
      await chooseBlue(dialog);

      const lifeAreaInput = dialog.getByLabel('Life Area (opzionale)');
      await lifeAreaInput.fill(areaName);
      await expect(dialog.getByRole('listbox')).toHaveCount(0);
      await expect(dialog.getByText(/quando premi Aggiungi/i)).toHaveCount(0);

      const activityResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/activities/scheduled') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const activityResponse = await activityResponsePromise;
      expect(activityResponse.status()).toBe(201);
      const activity = (await activityResponse.json()) as Record<string, unknown>;
      const activityRef = uuidField(activity, 'activity_ref');
      const lifeAreaRef = uuidField(activity, 'life_area_ref');

      const areas = await readJson<LifeAreaRow[]>(
        page,
        '/api/v1/temporal/life-areas',
      );
      const area = areas.find((candidate) => candidate.life_area_ref === lifeAreaRef);
      expect(area).toMatchObject({
        name: areaName,
        color_code: BLUE,
      });

      const assignments = await readJson<AssignmentRow[]>(
        page,
        '/api/v1/temporal/life-area-assignments',
      );
      expect(assignments).toContainEqual(
        expect.objectContaining({
          subject_kind: 'activity',
          subject_native_ref: activityRef,
          life_area_ref: lifeAreaRef,
        }),
      );

      await expectGroupColor(page, lifeAreaRef, areaName, BLUE);
      await expectTimedCardColor(page, activityTitle, areaName, BLUE);

      dialog = await openCreate(page, 'event');
      await dialog.getByRole('textbox', { name: 'Titolo' }).fill(eventTitle);
      await dialog.getByLabel('Ora').fill('11:10');
      const eventLifeArea = dialog.getByLabel('Life Area (opzionale)');
      await eventLifeArea.focus();
      await expect(dialog.getByRole('listbox')).toBeVisible();
      await dialog.getByRole('option', { name: areaName }).click();

      const eventResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/events/scheduled') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const eventResponse = await eventResponsePromise;
      expect(eventResponse.status()).toBe(201);
      const event = (await eventResponse.json()) as Record<string, unknown>;
      const eventRef = uuidField(event, 'event_ref');
      expect(event.life_area_ref).toBe(lifeAreaRef);

      const eventAssignments = await readJson<AssignmentRow[]>(
        page,
        '/api/v1/temporal/life-area-assignments',
      );
      expect(eventAssignments).toContainEqual(
        expect.objectContaining({
          subject_kind: 'event',
          subject_native_ref: eventRef,
          life_area_ref: lifeAreaRef,
        }),
      );
      await expectTimedCardColor(page, eventTitle, areaName, BLUE);

      dialog = await openCreate(page);
      await dialog
        .getByRole('textbox', { name: 'Titolo' })
        .fill(noAreaActivityTitle);
      await dialog.getByLabel('Ora').fill('13:10');
      await expect(dialog.getByLabel('Life Area (opzionale)')).toHaveValue('');

      const noAreaActivityResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/activities/scheduled') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const noAreaActivityResponse = await noAreaActivityResponsePromise;
      expect(noAreaActivityResponse.status()).toBe(201);
      const noAreaActivity =
        (await noAreaActivityResponse.json()) as Record<string, unknown>;
      const noAreaActivityRef = uuidField(noAreaActivity, 'activity_ref');
      expect(noAreaActivity.life_area_ref ?? null).toBeNull();

      dialog = await openCreate(page, 'event');
      await dialog
        .getByRole('textbox', { name: 'Titolo' })
        .fill(noAreaEventTitle);
      await dialog.getByLabel('Ora').fill('15:10');

      const noAreaEventResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/events/scheduled') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const noAreaEventResponse = await noAreaEventResponsePromise;
      expect(noAreaEventResponse.status()).toBe(201);
      const noAreaEvent =
        (await noAreaEventResponse.json()) as Record<string, unknown>;
      const noAreaEventRef = uuidField(noAreaEvent, 'event_ref');
      expect(noAreaEvent.life_area_ref ?? null).toBeNull();

      const finalAssignments = await readJson<AssignmentRow[]>(
        page,
        '/api/v1/temporal/life-area-assignments',
      );
      expect(
        finalAssignments.some(
          (entry) =>
            entry.subject_kind === 'activity' &&
            entry.subject_native_ref === noAreaActivityRef,
        ),
      ).toBe(false);
      expect(
        finalAssignments.some(
          (entry) =>
            entry.subject_kind === 'event' &&
            entry.subject_native_ref === noAreaEventRef,
        ),
      ).toBe(false);

      await expectTimedCardColor(
        page,
        noAreaActivityTitle,
        null,
        DEFAULT_ORANGE,
      );
      await expectTimedCardColor(page, noAreaEventTitle, null, DEFAULT_ORANGE);

      const reloadTimeline = waitForTimelineRead(page);
      const reloadUnplaced = waitForUnplacedRead(page);
      await page.reload({
        waitUntil: 'domcontentloaded',
        timeout: E2E_RESPONSE_TIMEOUT_MS,
      });
      expect((await reloadTimeline).status()).toBe(200);
      expect((await reloadUnplaced).status()).toBe(200);

      await expectGroupColor(page, lifeAreaRef, areaName, BLUE);
      await expectTimedCardColor(page, activityTitle, areaName, BLUE);
      await expectTimedCardColor(page, eventTitle, areaName, BLUE);
      await expectTimedCardColor(
        page,
        noAreaActivityTitle,
        null,
        DEFAULT_ORANGE,
      );
      await expectTimedCardColor(page, noAreaEventTitle, null, DEFAULT_ORANGE);
    } finally {
      await context.close();
    }
  });

  test('recurring Activity/Event preserve Life Area presence or absence on canonical sources and materialized Timeline items', async ({
    browser,
  }, testInfo) => {
    requireGoldenProject(testInfo);
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo));
      await openHome(page);

      const tag = testInfo.project.name;
      const areaName = `Golden Routine Area ${tag}`;
      const routineTitle = `Golden Routine area ${tag}`;
      const recurringEventTitle = `Golden recurring Event area ${tag}`;
      const noAreaRoutineTitle = `Golden Routine no area ${tag}`;
      const noAreaEventTitle = `Golden recurring Event no area ${tag}`;

      let dialog = await openCreate(page);
      await dialog.getByRole('textbox', { name: 'Titolo' }).fill(routineTitle);
      await dialog.getByLabel('Ora').fill('08:20');
      await chooseBlue(dialog);
      await dialog.getByLabel('Life Area (opzionale)').fill(areaName);
      await expect(dialog.getByRole('listbox')).toHaveCount(0);
      await dialog.getByLabel('Ripeti').selectOption('daily');

      const routineResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/recurring/routines') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const routineResponse = await routineResponsePromise;
      expect(routineResponse.ok()).toBe(true);
      const routine = (await routineResponse.json()) as Record<string, unknown>;
      const routineRef = uuidField(routine, 'source_ref');

      const areas = await readJson<LifeAreaRow[]>(
        page,
        '/api/v1/temporal/life-areas',
      );
      const area = areas.find((candidate) => candidate.name === areaName);
      expect(area).toBeDefined();
      if (!area) throw new Error('Expected recurring Activity Life Area.');
      expect(area.color_code).toBe(BLUE);

      const routines = await readJson<RoutineRow[]>(
        page,
        '/api/v1/temporal/routines',
      );
      expect(routines).toContainEqual(
        expect.objectContaining({
          routine_ref: routineRef,
          title: routineTitle,
          life_area_ref: area.life_area_ref,
        }),
      );

      await expectGroupColor(page, area.life_area_ref, areaName, BLUE);
      await expectTimedCardColor(page, routineTitle, areaName, BLUE);

      dialog = await openCreate(page, 'event');
      await dialog
        .getByRole('textbox', { name: 'Titolo' })
        .fill(recurringEventTitle);
      await dialog.getByLabel('Ora').fill('10:20');
      const eventArea = dialog.getByLabel('Life Area (opzionale)');
      await eventArea.focus();
      await dialog.getByRole('option', { name: areaName }).click();
      await dialog.getByLabel('Ripeti').selectOption('daily');

      const recurringEventResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/recurring/events') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const recurringEventResponse = await recurringEventResponsePromise;
      expect(recurringEventResponse.ok()).toBe(true);
      const recurringEvent =
        (await recurringEventResponse.json()) as Record<string, unknown>;
      const recurringEventRef = uuidField(recurringEvent, 'source_ref');

      const assignments = await readJson<AssignmentRow[]>(
        page,
        '/api/v1/temporal/life-area-assignments',
      );
      expect(assignments).toContainEqual(
        expect.objectContaining({
          subject_kind: 'event',
          subject_native_ref: recurringEventRef,
          life_area_ref: area.life_area_ref,
        }),
      );
      await expectTimedCardColor(page, recurringEventTitle, areaName, BLUE);

      dialog = await openCreate(page);
      await dialog
        .getByRole('textbox', { name: 'Titolo' })
        .fill(noAreaRoutineTitle);
      await dialog.getByLabel('Ora').fill('12:20');
      await dialog.getByLabel('Ripeti').selectOption('daily');

      const noAreaRoutineResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/recurring/routines') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const noAreaRoutineResponse = await noAreaRoutineResponsePromise;
      expect(noAreaRoutineResponse.ok()).toBe(true);
      const noAreaRoutine =
        (await noAreaRoutineResponse.json()) as Record<string, unknown>;
      const noAreaRoutineRef = uuidField(noAreaRoutine, 'source_ref');

      const routinesAfterNoArea = await readJson<RoutineRow[]>(
        page,
        '/api/v1/temporal/routines',
      );
      expect(routinesAfterNoArea).toContainEqual(
        expect.objectContaining({
          routine_ref: noAreaRoutineRef,
          title: noAreaRoutineTitle,
          life_area_ref: null,
        }),
      );
      await expectTimedCardColor(
        page,
        noAreaRoutineTitle,
        null,
        DEFAULT_ORANGE,
      );

      dialog = await openCreate(page, 'event');
      await dialog
        .getByRole('textbox', { name: 'Titolo' })
        .fill(noAreaEventTitle);
      await dialog.getByLabel('Ora').fill('14:20');
      await dialog.getByLabel('Ripeti').selectOption('daily');

      const noAreaEventResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/recurring/events') &&
          response.request().method() === 'POST',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const noAreaEventResponse = await noAreaEventResponsePromise;
      expect(noAreaEventResponse.ok()).toBe(true);
      const noAreaEvent =
        (await noAreaEventResponse.json()) as Record<string, unknown>;
      const noAreaEventRef = uuidField(noAreaEvent, 'source_ref');

      const finalAssignments = await readJson<AssignmentRow[]>(
        page,
        '/api/v1/temporal/life-area-assignments',
      );
      expect(
        finalAssignments.some(
          (entry) =>
            entry.subject_kind === 'event' &&
            entry.subject_native_ref === noAreaEventRef,
        ),
      ).toBe(false);
      await expectTimedCardColor(page, noAreaEventTitle, null, DEFAULT_ORANGE);

      const reloadTimeline = waitForTimelineRead(page);
      const reloadUnplaced = waitForUnplacedRead(page);
      await page.reload({
        waitUntil: 'domcontentloaded',
        timeout: E2E_RESPONSE_TIMEOUT_MS,
      });
      expect((await reloadTimeline).status()).toBe(200);
      expect((await reloadUnplaced).status()).toBe(200);

      await expectGroupColor(page, area.life_area_ref, areaName, BLUE);
      await expectTimedCardColor(page, routineTitle, areaName, BLUE);
      await expectTimedCardColor(page, recurringEventTitle, areaName, BLUE);
      await expectTimedCardColor(
        page,
        noAreaRoutineTitle,
        null,
        DEFAULT_ORANGE,
      );
      await expectTimedCardColor(page, noAreaEventTitle, null, DEFAULT_ORANGE);
    } finally {
      await context.close();
    }
  });
});
