import { Temporal } from '@dante/time';
import {
  expect,
  test,
  type Locator,
  type Page,
  type TestInfo,
} from '@playwright/test';

const password = 'correct horse battery staple';
const E2E_RESPONSE_TIMEOUT_MS = 10_000;
const B03_E2E_EMAIL = 'synthetic.user+e2e-64@example.com';

function requireClosureProject(testInfo: TestInfo): void {
  test.skip(
    testInfo.project.name === 'webkit',
    'B03-E closure requires Chromium and Firefox real-stack proof.',
  );
  if (!['chromium', 'firefox'].includes(testInfo.project.name)) {
    throw new Error(`Unsupported B03-E browser project: ${testInfo.project.name}`);
  }
}

async function useItalianLocale(page: Page): Promise<void> {
  await page.addInitScript(() => {
    window.localStorage.setItem('dante.locale', 'it');
  });
}

async function signIn(page: Page): Promise<void> {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
  ).toBeVisible();
  await page.getByLabel('Email').fill(B03_E2E_EMAIL);
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
  return page
    .waitForResponse(
      (response) =>
        response.url().includes('/api/v1/temporal/timeline/window') &&
        response.request().method() === 'GET',
      { timeout: E2E_RESPONSE_TIMEOUT_MS },
    )
    .then(async (response) => {
      const status = response.status();
      const payload = (await response.json()) as unknown;
      return {
        status: () => status,
        json: async () => payload,
      };
    });
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

async function openCreate(page: Page): Promise<Locator> {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await dialog.getByRole('radio', { name: 'Evento' }).click();
  await expect(dialog.getByRole('radio', { name: 'Evento' })).toHaveAttribute(
    'aria-checked',
    'true',
  );
  return dialog;
}

function uuidField(payload: Record<string, unknown>, field: string): string {
  const value = payload[field];
  expect(typeof value).toBe('string');
  if (typeof value !== 'string') {
    throw new Error(`${field} was not a string.`);
  }
  return value;
}

async function createScheduledEvent(
  page: Page,
  title: string,
  configure: (dialog: Locator) => Promise<void>,
): Promise<Record<string, unknown>> {
  const dialog = await openCreate(page);
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill(title);
  await configure(dialog);

  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/temporal/events/scheduled') &&
      response.request().method() === 'POST',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  const response = await responsePromise;
  expect(response.status()).toBe(201);
  await expect(dialog).toHaveCount(0);
  return (await response.json()) as Record<string, unknown>;
}

function addDays(date: string, days: number): string {
  return Temporal.PlainDate.from(date).add({ days }).toString();
}

test.describe('Timeline B03-E real-stack Event closure', () => {
  test('create, reschedule, all-day, multi-day and reload preserve canonical Event truth', async ({
    browser,
  }, testInfo) => {
    requireClosureProject(testInfo);
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page);
      await openHome(page);

      const today = Temporal.Now.plainDateISO('Europe/Rome').toString();
      const browserTag = testInfo.project.name;

      const timedTitle = `B03 E timed ${browserTag}`;
      const timed = await createScheduledEvent(page, timedTitle, async (dialog) => {
        await dialog.locator('[data-create-path="date"]').fill(today);
        await dialog.locator('[data-create-path="startTime"]').fill('10:00');
      });
      expect(timed.temporal_form).toBe('floating_local');
      const timedEventRef = uuidField(timed, 'event_ref');
      const timedScheduleRef = uuidField(timed, 'schedule_ref');
      const initialStateRef = uuidField(timed, 'placement_material_state_ref');

      const timedCard = page.locator(
        `[data-timeline-event="${timedScheduleRef}"]`,
      );
      await expect(timedCard).toHaveCount(1);
      await timedCard.scrollIntoViewIfNeeded();
      await expect(timedCard).toBeVisible();

      const revisionResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith(
            `/api/v1/temporal/schedules/${timedScheduleRef}/placement`,
          ) && response.request().method() === 'PATCH',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await timedCard.press('Alt+ArrowDown');
      const revisionResponse = await revisionResponsePromise;
      expect(revisionResponse.status()).toBe(200);
      const revised = (await revisionResponse.json()) as Record<string, unknown>;
      expect(revised.schedule_ref).toBe(timedScheduleRef);
      expect(revised.previous_placement_material_state_ref).toBe(initialStateRef);
      const revisedStateRef = uuidField(
        revised,
        'placement_material_state_ref',
      );
      expect(revisedStateRef).not.toBe(initialStateRef);
      await expect(timedCard).toHaveAttribute('aria-label', /10:05/);

      const singleDayTitle = `B03 E all-day ${browserTag}`;
      const singleDay = await createScheduledEvent(
        page,
        singleDayTitle,
        async (dialog) => {
          await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
          await dialog.locator('[data-create-path="date"]').fill(today);
          await dialog
            .locator('[data-create-path="event.allDayEndDate"]')
            .fill(today);
        },
      );
      expect(singleDay.temporal_form).toBe('date_span');
      expect(singleDay.start_date).toBe(today);
      expect(singleDay.end_date_exclusive).toBe(addDays(today, 1));
      const singleDayEventRef = uuidField(singleDay, 'event_ref');
      const singleDayScheduleRef = uuidField(singleDay, 'schedule_ref');

      const multiStart = addDays(today, 1);
      const multiEndInclusive = addDays(today, 3);
      const multiDayTitle = `B03 E multi-day ${browserTag}`;
      const multiDay = await createScheduledEvent(
        page,
        multiDayTitle,
        async (dialog) => {
          await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
          await dialog.locator('[data-create-path="date"]').fill(multiStart);
          await dialog
            .locator('[data-create-path="event.allDayEndDate"]')
            .fill(multiEndInclusive);
        },
      );
      expect(multiDay.temporal_form).toBe('date_span');
      expect(multiDay.start_date).toBe(multiStart);
      expect(multiDay.end_date_exclusive).toBe(addDays(multiEndInclusive, 1));
      const multiDayEventRef = uuidField(multiDay, 'event_ref');
      const multiDayScheduleRef = uuidField(multiDay, 'schedule_ref');

      const reloadTimeline = waitForTimelineRead(page);
      const reloadUnplaced = waitForUnplacedRead(page);
      await page.reload({
        waitUntil: 'domcontentloaded',
        timeout: E2E_RESPONSE_TIMEOUT_MS,
      });
      const timelineResponse = await reloadTimeline;
      expect(timelineResponse.status()).toBe(200);
      expect((await reloadUnplaced).status()).toBe(200);
      const timeline = (await timelineResponse.json()) as {
        items?: Array<Record<string, unknown>>;
      };

      const expected = [
        {
          eventRef: timedEventRef,
          scheduleRef: timedScheduleRef,
          stateRef: revisedStateRef,
          form: 'floating_local',
        },
        {
          eventRef: singleDayEventRef,
          scheduleRef: singleDayScheduleRef,
          stateRef: uuidField(singleDay, 'placement_material_state_ref'),
          form: 'date_span',
        },
        {
          eventRef: multiDayEventRef,
          scheduleRef: multiDayScheduleRef,
          stateRef: uuidField(multiDay, 'placement_material_state_ref'),
          form: 'date_span',
        },
      ] as const;

      for (const witness of expected) {
        const item = timeline.items?.find(
          (candidate) => candidate.schedule_ref === witness.scheduleRef,
        );
        expect(item).toBeDefined();
        expect(item?.kind).toBe('scheduled_event');
        expect(item?.event_ref).toBe(witness.eventRef);
        expect(item?.placement_material_state_ref).toBe(witness.stateRef);
        expect(item?.temporal_form).toBe(witness.form);
        expect('activity_ref' in (item ?? {})).toBe(false);
      }

      await expect(
        page.locator(`[data-timeline-event="${timedScheduleRef}"]`),
      ).toHaveCount(1);
      await expect(
        page.locator('.timeline-all-day-item').filter({ hasText: singleDayTitle }),
      ).toHaveCount(1);
      await expect(
        page.locator('.timeline-all-day-item').filter({ hasText: multiDayTitle }),
      ).toHaveCount(3);
    } finally {
      await context.close();
    }
  });
});
