import { randomUUID } from 'node:crypto';

import { Temporal } from '@dante/time';
import { expect, test, type Page, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';
const E2E_RESPONSE_TIMEOUT_MS = 10_000;

const projectEmail: Readonly<Record<string, string>> = {
  chromium: 'synthetic.user+e2e-58@example.com',
  firefox: 'synthetic.user+e2e-59@example.com',
  webkit: 'synthetic.user+e2e-60@example.com',
};

function emailFor(testInfo: TestInfo): string {
  const email = projectEmail[testInfo.project.name];
  if (!email) {
    throw new Error(`Unsupported temporal B02 browser project: ${testInfo.project.name}`);
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

type MutationResult = Readonly<{
  status: number;
  payload: Record<string, unknown>;
}>;

async function authenticatedMutation(
  page: Page,
  request: Readonly<{
    method: 'PATCH' | 'POST';
    path: string;
    body: Record<string, unknown>;
  }>,
): Promise<MutationResult> {
  return page.evaluate(
    async ({ method, path, body, timeoutMs }) => {
      const controller = new AbortController();
      const timer = window.setTimeout(() => controller.abort(), timeoutMs);
      try {
        const sessionResponse = await fetch('/api/v1/auth/session', {
          signal: controller.signal,
        });
        const session = (await sessionResponse.json()) as {
          authenticated?: boolean;
          csrf_token?: string;
        };
        if (
          !sessionResponse.ok ||
          session.authenticated !== true ||
          typeof session.csrf_token !== 'string' ||
          session.csrf_token.length === 0
        ) {
          throw new Error('Expected an authenticated session with a CSRF token.');
        }

        const response = await fetch(path, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': session.csrf_token,
          },
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        return {
          status: response.status,
          payload: (await response.json()) as Record<string, unknown>,
        };
      } catch (error) {
        if (controller.signal.aborted) {
          throw new Error(`Timed out ${method} ${path} after ${timeoutMs}ms`);
        }
        throw error;
      } finally {
        window.clearTimeout(timer);
      }
    },
    { ...request, timeoutMs: E2E_RESPONSE_TIMEOUT_MS },
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

async function createUnplacedActivity(
  page: Page,
  title: string,
): Promise<Readonly<{ activity_ref: string; title: string }>> {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await dialog.getByLabel('Titolo').fill(title);
  await dialog.getByRole('radio', { name: 'Da collocare' }).click();

  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/temporal/activities') &&
      response.request().method() === 'POST',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
  await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  const response = await responsePromise;
  expect(response.status()).toBe(201);
  return (await response.json()) as { activity_ref: string; title: string };
}

async function placeFromPlanningTray(
  page: Page,
  activityRef: string,
): Promise<Record<string, unknown>> {
  const trigger = page.getByRole('button', { name: 'Apri attività da collocare' });
  await trigger.click();
  const tray = page.locator('[data-timeline-planning-tray="true"]');
  await expect(tray).toBeVisible();
  const item = tray.locator(`[data-temporal-activity-ref="${activityRef}"]`);
  await expect(item).toHaveCount(1);
  await item.getByRole('button', { name: /^Colloca:/ }).click();
  const form = item.locator('.timeline-planning-quick-place');
  await expect(form).toBeVisible();
  await form.getByLabel('Inizio').fill('10:00');
  await form.getByLabel('Durata (minuti)').fill('45');

  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith(`/api/v1/temporal/activities/${activityRef}/schedule`) &&
      response.request().method() === 'POST',
    { timeout: E2E_RESPONSE_TIMEOUT_MS },
  );
  await form
    .getByRole('button', { name: 'Colloca in Timeline', exact: true })
    .click();
  const response = await responsePromise;
  expect(response.status()).toBe(201);
  return (await response.json()) as Record<string, unknown>;
}

function uuidField(payload: Record<string, unknown>, field: string): string {
  const value = payload[field];
  expect(typeof value).toBe('string');
  if (typeof value !== 'string') {
    throw new Error(`${field} was not a string.`);
  }
  return value;
}

test.describe('Timeline B02-E full-stack Schedule forms', () => {
  test('create → place → move → cross-form revise → unschedule → Undo → reload stays monotonic', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo));
      await openHome(page);

      const title = `B02 E4 governed loop ${testInfo.project.name}`;
      const activity = await createUnplacedActivity(page, title);
      expect(activity.title).toBe(title);

      const established = await placeFromPlanningTray(page, activity.activity_ref);
      expect(established.temporal_form).toBe('floating_local');
      const scheduleRef = uuidField(established, 'schedule_ref');
      const establishedState = uuidField(
        established,
        'placement_material_state_ref',
      );

      const today = Temporal.Now.plainDateISO('Europe/Rome');
      const moved = await authenticatedMutation(page, {
        method: 'PATCH',
        path: `/api/v1/temporal/schedules/${scheduleRef}/placement`,
        body: {
          operation_id: `e2e-b02-move-${randomUUID()}`,
          expected_placement_material_state_ref: establishedState,
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: `${today.toString()}T11:00:00`,
            ends_local_at: `${today.toString()}T11:45:00`,
          },
        },
      });
      expect(moved.status).toBe(200);
      expect(moved.payload.temporal_form).toBe('floating_local');
      expect(moved.payload.schedule_ref).toBe(scheduleRef);
      expect(moved.payload.previous_placement_material_state_ref).toBe(
        establishedState,
      );
      const movedState = uuidField(moved.payload, 'placement_material_state_ref');
      expect(movedState).not.toBe(establishedState);

      const crossForm = await authenticatedMutation(page, {
        method: 'PATCH',
        path: `/api/v1/temporal/schedules/${scheduleRef}/placement`,
        body: {
          operation_id: `e2e-b02-cross-form-${randomUUID()}`,
          expected_placement_material_state_ref: movedState,
          placement: {
            kind: 'coarse_local_period',
            local_date: today.toString(),
            period: 'evening',
          },
        },
      });
      expect(crossForm.status).toBe(200);
      expect(crossForm.payload.temporal_form).toBe('coarse_local_period');
      expect(crossForm.payload.schedule_ref).toBe(scheduleRef);
      expect(crossForm.payload.previous_placement_material_state_ref).toBe(
        movedState,
      );
      const coarseState = uuidField(
        crossForm.payload,
        'placement_material_state_ref',
      );
      expect(coarseState).not.toBe(movedState);

      const unscheduleOperationId = `e2e-b02-unschedule-${randomUUID()}`;
      const unscheduled = await authenticatedMutation(page, {
        method: 'POST',
        path: `/api/v1/temporal/schedules/${scheduleRef}/unschedule`,
        body: {
          operation_id: unscheduleOperationId,
          expected_placement_material_state_ref: coarseState,
        },
      });
      expect(unscheduled.status).toBe(200);
      expect(unscheduled.payload.schedule_ref).toBe(scheduleRef);
      expect(unscheduled.payload.previous_placement_material_state_ref).toBe(
        coarseState,
      );
      expect(unscheduled.payload.unschedule_operation_id).toBe(
        unscheduleOperationId,
      );

      const restored = await authenticatedMutation(page, {
        method: 'POST',
        path: `/api/v1/temporal/schedules/${scheduleRef}/unschedule/undo`,
        body: {
          operation_id: `e2e-b02-undo-${randomUUID()}`,
          unschedule_operation_id: unscheduleOperationId,
        },
      });
      expect(restored.status).toBe(200);
      expect(restored.payload.schedule_ref).toBe(scheduleRef);
      expect(restored.payload.temporal_form).toBe('coarse_local_period');
      expect(restored.payload.restored_from_placement_material_state_ref).toBe(
        coarseState,
      );
      const restoredState = uuidField(
        restored.payload,
        'placement_material_state_ref',
      );
      expect(restoredState).not.toBe(coarseState);

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
      const item = timeline.items?.find(
        (candidate) => candidate.schedule_ref === scheduleRef,
      );
      expect(item).toBeDefined();
      expect(item?.temporal_form).toBe('coarse_local_period');
      expect(item?.placement_material_state_ref).toBe(restoredState);
      expect(item?.period).toBe('evening');
      await expect(page.getByText(title)).toBeVisible();
    } finally {
      await context.close();
    }
  });

  test('product-exposed date-span, coarse and named-zone forms survive canonical reload', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo));
      await openHome(page);
      const today = Temporal.Now.plainDateISO('Europe/Rome').toString();

      const createScheduled = async (
        title: string,
        configure: (dialog: ReturnType<Page['locator']>) => Promise<void>,
      ) => {
        await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
        const dialog = page.locator('[data-temporal-create="composer"]');
        await expect(dialog).toBeVisible();
        await dialog.getByLabel('Titolo').fill(title);
        await configure(dialog);
        const responsePromise = page.waitForResponse(
          (response) =>
            response.url().endsWith('/api/v1/temporal/activities/scheduled') &&
            response.request().method() === 'POST',
          { timeout: E2E_RESPONSE_TIMEOUT_MS },
        );
        await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
        const response = await responsePromise;
        expect(response.status()).toBe(201);
        return (await response.json()) as Record<string, unknown>;
      };

      const allDayTitle = `B02 E4 all-day ${testInfo.project.name}`;
      const allDay = await createScheduled(allDayTitle, async (dialog) => {
        await dialog.getByRole('radio', { name: 'Tutto il giorno' }).click();
        await dialog.locator('[data-create-path="date"]').fill(today);
      });
      expect(allDay.temporal_form).toBe('date_span');
      expect(allDay.start_date).toBe(today);

      const coarseTitle = `B02 E4 coarse ${testInfo.project.name}`;
      const coarse = await createScheduled(coarseTitle, async (dialog) => {
        await dialog.getByRole('radio', { name: 'Fascia' }).click();
        await dialog.locator('[data-create-path="date"]').fill(today);
        await dialog
          .locator('[data-create-path="coarsePeriod"]')
          .selectOption('afternoon');
      });
      expect(coarse.temporal_form).toBe('coarse_local_period');
      expect(coarse.local_date).toBe(today);
      expect(coarse.period).toBe('afternoon');

      const zonedTitle = `B02 E4 zoned ${testInfo.project.name}`;
      const zoned = await createScheduled(zonedTitle, async (dialog) => {
        await dialog.getByRole('radio', { name: 'Orario' }).click();
        await dialog.locator('[data-create-path="date"]').fill(today);
        await dialog.locator('[data-create-path="startTime"]').fill('14:10');
        await dialog.locator('[data-create-path="endTime"]').fill('14:40');
        await dialog
          .locator('[data-create-path="timeMode"]')
          .selectOption('zoned');
        await dialog
          .locator('[data-create-path="timeZoneId"]')
          .fill('Europe/Rome');
        await dialog
          .locator('[data-create-path="timeDisambiguation"]')
          .selectOption('reject');
      });
      expect(zoned.temporal_form).toBe('named_zone_local');
      expect(zoned.zone_id).toBe('Europe/Rome');
      expect(String(zoned.starts_local_at)).toContain(`${today}T14:10`);

      const expected = new Map([
        [uuidField(allDay, 'schedule_ref'), 'date_span'],
        [uuidField(coarse, 'schedule_ref'), 'coarse_local_period'],
        [uuidField(zoned, 'schedule_ref'), 'named_zone_local'],
      ]);

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
      for (const [scheduleRef, temporalForm] of expected) {
        const item = timeline.items?.find(
          (candidate) => candidate.schedule_ref === scheduleRef,
        );
        expect(item).toBeDefined();
        expect(item?.temporal_form).toBe(temporalForm);
      }

      await expect(page.getByText(allDayTitle)).toBeVisible();
      await expect(page.getByText(coarseTitle)).toBeVisible();
      await expect(page.getByText(zonedTitle)).toBeVisible();
    } finally {
      await context.close();
    }
  });
});
