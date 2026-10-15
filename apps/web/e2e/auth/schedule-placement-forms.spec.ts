import { randomUUID } from 'node:crypto';

import { Temporal } from '@dante/time';
import { expect, test, type Page, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';
const E2E_RESPONSE_TIMEOUT_MS = 10_000;

// Dedicated accounts per scenario keep the two-sign-in limit active.
const projectEmailOffset: Readonly<Record<string, number>> = {
  chromium: 64,
  firefox: 68,
  webkit: 72,
};

function emailFor(testInfo: TestInfo, slot: 1 | 2 | 3 | 4): string {
  const offset = projectEmailOffset[testInfo.project.name];
  if (offset === undefined) {
    throw new Error(
      `Unsupported temporal B02 browser project: ${testInfo.project.name}`,
    );
  }
  return `synthetic.user+e2e-${offset + slot}@example.com`;
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
        json: () => Promise.resolve(payload),
      };
    });
}

function readUnplaced(page: Page) {
  // Legacy canonical activity inventory is no longer fetched automatically
  // by Home. Exercise the authenticated endpoint explicitly after navigation.
  return page.request.get('/api/v1/temporal/activities/unplaced', {
    headers: { 'X-Dante-Time-Zone': 'Europe/Rome' },
  });
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
          credentials: 'same-origin',
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
          throw new Error(
            'Expected an authenticated session with a CSRF token.',
          );
        }

        const response = await fetch(path, {
          method,
          credentials: 'same-origin',
          headers: {
            Accept: 'application/json, application/problem+json',
            'Content-Type': 'application/json',
            'X-Dante-Client': 'web',
            'X-Dante-Time-Zone': 'Europe/Rome',
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
          throw new Error(`Timed out ${method} ${path} after ${timeoutMs}ms`, {
            cause: error,
          });
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
  await page.goto('/home');
  expect((await timeline).status()).toBe(200);
  expect((await readUnplaced(page)).status()).toBe(200);
  await expect(
    page.locator('[data-temporal-read-state="ready"]'),
  ).toBeVisible();
}

async function createUnplacedActivity(
  page: Page,
  title: string,
): Promise<Readonly<{ activity_ref: string; title: string }>> {
  // The retired "Da collocare" Create mode is not a product action. The
  // canonical unplaced authoring endpoint remains supported and is exercised
  // directly; the user-visible legacy inventory is checked immediately after.
  const result = await authenticatedMutation(page, {
    method: 'POST',
    path: '/api/v1/temporal/authoring/activities',
    body: {
      operation_id: `e2e:b02:unplaced:${randomUUID()}`,
      title,
      placement: null,
    },
  });
  expect(result.status).toBe(201);
  expect(result.payload.title).toBe(title);
  expect(result.payload.schedule).toBeNull();
  return {
    activity_ref: uuidField(result.payload, 'activity_ref'),
    title,
  };
}

async function assertPlanningTrayContainsActivity(
  page: Page,
  activityRef: string,
): Promise<void> {
  await page.getByRole('button', { name: 'Apri Bozze' }).click();
  await page
    .getByRole('button', { name: 'Gestisci elementi già creati' })
    .click();
  const tray = page.locator('[data-timeline-planning-tray="true"]');
  await expect(tray).toBeVisible();
  await expect(
    tray.locator(`[data-temporal-subject-ref="${activityRef}"]`),
  ).toHaveCount(1);
}

function uuidField(payload: Record<string, unknown>, field: string): string {
  const value = payload[field];
  expect(typeof value).toBe('string');
  if (typeof value !== 'string') {
    throw new Error(`${field} was not a string.`);
  }
  return value;
}

type AcceptedAuthoringSchedule = Readonly<{
  schedule_ref: string;
  placement_material_state_ref: string;
  placement: Record<string, unknown>;
}>;

async function createScheduledActivity(
  page: Page,
  title: string,
  placement: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const accepted = await authenticatedMutation(page, {
    method: 'POST',
    path: '/api/v1/temporal/authoring/activities',
    body: {
      operation_id: `e2e:b02:schedule:${randomUUID()}`,
      title,
      placement,
    },
  });
  expect(accepted.status).toBe(201);
  expect(accepted.payload.title).toBe(title);
  const schedule = accepted.payload
    .schedule as AcceptedAuthoringSchedule | null;
  expect(schedule).not.toBeNull();
  if (!schedule) throw new Error('Authoring returned no canonical Schedule');
  const saved = schedule.placement;
  // Preserve exact database-contract checks against the accepted U2 record.
  return {
    ...accepted.payload,
    schedule_ref: schedule.schedule_ref,
    placement_material_state_ref: schedule.placement_material_state_ref,
    temporal_form:
      saved.kind === 'date_span'
        ? 'date_span'
        : saved.kind === 'coarse_local_period'
          ? 'coarse_local_period'
          : saved.kind === 'named_zone_local_interval'
            ? 'named_zone_local'
            : saved.kind === 'floating_local_interval'
              ? 'floating_local'
              : String(saved.kind),
    ...saved,
  };
}

test.describe('Timeline B02-E full-stack Schedule forms', () => {
  test('one-off Activity deletion requires confirmation and is absent after reload', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });
    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo, 1));
      const day = Temporal.Now.plainDateISO('Europe/Rome')
        .add({ days: 1 })
        .toString();
      const initialRead = waitForTimelineRead(page);
      await page.goto(`/home?date=${day}`);
      expect((await initialRead).status()).toBe(200);
      const title = `Activity delete ${randomUUID()}`;
      const created = await createScheduledActivity(page, title, {
        kind: 'floating_local_interval',
        starts_local_at: `${day}T13:00:00`,
        ends_local_at: `${day}T14:00:00`,
      });
      const activityRef = uuidField(created, 'activity_ref');
      const scheduleRef = uuidField(created, 'schedule_ref');
      const freshRead = waitForTimelineRead(page);
      await page.reload();
      expect((await freshRead).status()).toBe(200);
      const card = page.locator(`[data-timeline-event="${scheduleRef}"]`);
      await expect(card).toHaveCount(1);
      await card.getByRole('button', { name: title, exact: true }).click();
      const inspector = page.getByRole('dialog', { name: title });
      await inspector
        .getByRole('button', { name: 'Elimina', exact: true })
        .click();
      await expect(
        inspector.getByRole('button', {
          name: 'Conferma eliminazione definitiva',
        }),
      ).toBeVisible();
      await inspector
        .getByRole('button', { name: 'Annulla', exact: true })
        .click();
      expect(
        (
          await page.request.get(
            `/api/v1/temporal/activities/${activityRef}/profile`,
            { headers: { 'X-Dante-Time-Zone': 'Europe/Rome' } },
          )
        ).status(),
      ).toBe(200);

      await inspector
        .getByRole('button', { name: 'Elimina', exact: true })
        .click();
      const deleteResponse = page.waitForResponse(
        (response) =>
          response
            .url()
            .endsWith(`/api/v1/temporal/activities/${activityRef}`) &&
          response.request().method() === 'DELETE',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await inspector
        .getByRole('button', { name: 'Conferma eliminazione definitiva' })
        .click();
      const deleted = await deleteResponse;
      expect(deleted.status()).toBe(200);
      expect(deleted.request().postDataJSON()).toMatchObject({
        expected_session_fingerprint: expect.stringMatching(/^[a-f0-9]{64}$/),
      });
      await expect(inspector).toHaveCount(0);
      const persistedRead = waitForTimelineRead(page);
      await page.reload();
      const window = (await (await persistedRead).json()) as
        | { kind: 'empty' }
        | { kind: 'window'; items: Array<{ schedule_ref?: string }> };
      expect(window.kind).toMatch(/^(empty|window)$/);
      if (window.kind === 'window') {
        expect(
          window.items.some((item) => item.schedule_ref === scheduleRef),
        ).toBe(false);
      }
      await expect(card).toHaveCount(0);
      expect(
        (
          await page.request.get(
            `/api/v1/temporal/activities/${activityRef}/profile`,
            { headers: { 'X-Dante-Time-Zone': 'Europe/Rome' } },
          )
        ).status(),
      ).toBe(404);
    } finally {
      await context.close();
    }
  });

  test('Activity card move uses coordinated replan and survives reload', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });
    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo, 2));
      const day = Temporal.Now.plainDateISO('Europe/Rome')
        .add({ days: 1 })
        .toString();
      const initialRead = waitForTimelineRead(page);
      await page.goto(`/home?date=${day}`);
      expect((await initialRead).status()).toBe(200);
      const created = await createScheduledActivity(
        page,
        `Activity replan ${randomUUID()}`,
        {
          kind: 'floating_local_interval',
          starts_local_at: `${day}T10:00:00`,
          ends_local_at: `${day}T11:00:00`,
        },
      );
      const scheduleRef = uuidField(created, 'schedule_ref');
      const activityRef = uuidField(created, 'activity_ref');
      const freshRead = waitForTimelineRead(page);
      await page.reload();
      expect((await freshRead).status()).toBe(200);
      const card = page.locator(`[data-timeline-event="${scheduleRef}"]`);
      await expect(card).toHaveCount(1);
      await card.scrollIntoViewIfNeeded();

      const replanResponse = page.waitForResponse(
        (response) =>
          response
            .url()
            .endsWith(`/api/v1/temporal/activities/${activityRef}/replan`) &&
          response.request().method() === 'PUT',
        { timeout: E2E_RESPONSE_TIMEOUT_MS },
      );
      await card.press('Alt+ArrowDown');
      const accepted = await replanResponse;
      expect(accepted.status()).toBe(200);
      const body = accepted.request().postDataJSON() as Record<string, unknown>;
      expect(body.envelope).toMatchObject({
        schedule_ref: scheduleRef,
        expected_material_state_ref: created.placement_material_state_ref,
        starts_local_at: `${day}T10:05:00`,
        ends_local_at: `${day}T11:05:00`,
      });
      expect(body.session_disposition).toBeUndefined();

      const persistedRead = waitForTimelineRead(page);
      await page.reload();
      const window = (await (await persistedRead).json()) as {
        items?: Array<Record<string, unknown>>;
      };
      const persisted = window.items?.find(
        (item) => item.schedule_ref === scheduleRef,
      );
      expect(String(persisted?.starts_local_at)).toContain(`${day}T10:05`);
      expect(String(persisted?.ends_local_at)).toContain(`${day}T11:05`);
      await expect(card).toHaveAttribute('aria-label', /10:05/);
    } finally {
      await context.close();
    }
  });

  test('create unplaced → establish → move → cross-form revise → unschedule → Undo → reload stays monotonic', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo, 3));
      await openHome(page);

      const title = `B02 E4 governed loop ${testInfo.project.name}`;
      const activity = await createUnplacedActivity(page, title);
      expect(activity.title).toBe(title);
      // API-driven creation bypasses the SPA's optimistic invalidation.
      // Reload to prove that the legacy existing-item inventory hydrates
      // this canonical Activity from PostgreSQL, not from a stale client list.
      const inventoryRead = waitForTimelineRead(page);
      await page.reload();
      expect((await inventoryRead).status()).toBe(200);
      await assertPlanningTrayContainsActivity(page, activity.activity_ref);

      const today = Temporal.Now.plainDateISO('Europe/Rome').toString();
      const established = await authenticatedMutation(page, {
        method: 'POST',
        path: `/api/v1/temporal/activities/${activity.activity_ref}/schedule`,
        body: {
          operation_id: `e2e-b02-establish-${randomUUID()}`,
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: `${today}T10:00:00`,
            ends_local_at: `${today}T10:45:00`,
          },
        },
      });
      expect(established.status).toBe(201);
      expect(established.payload.temporal_form).toBe('floating_local');
      const scheduleRef = uuidField(established.payload, 'schedule_ref');
      const establishedState = uuidField(
        established.payload,
        'placement_material_state_ref',
      );

      const moved = await authenticatedMutation(page, {
        method: 'PATCH',
        path: `/api/v1/temporal/schedules/${scheduleRef}/placement`,
        body: {
          operation_id: `e2e-b02-move-${randomUUID()}`,
          expected_placement_material_state_ref: establishedState,
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: `${today}T11:00:00`,
            ends_local_at: `${today}T11:45:00`,
          },
        },
      });
      expect(moved.status).toBe(200);
      expect(moved.payload.temporal_form).toBe('floating_local');
      expect(moved.payload.schedule_ref).toBe(scheduleRef);
      expect(moved.payload.previous_placement_material_state_ref).toBe(
        establishedState,
      );
      const movedState = uuidField(
        moved.payload,
        'placement_material_state_ref',
      );

      const crossForm = await authenticatedMutation(page, {
        method: 'PATCH',
        path: `/api/v1/temporal/schedules/${scheduleRef}/placement`,
        body: {
          operation_id: `e2e-b02-cross-form-${randomUUID()}`,
          expected_placement_material_state_ref: movedState,
          placement: {
            kind: 'coarse_local_period',
            local_date: today,
            period: 'evening',
          },
        },
      });
      expect(crossForm.status).toBe(200);
      expect(crossForm.payload.temporal_form).toBe('coarse_local_period');
      expect(crossForm.payload.schedule_ref).toBe(scheduleRef);
      const coarseState = uuidField(
        crossForm.payload,
        'placement_material_state_ref',
      );

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

      const reloadTimeline = waitForTimelineRead(page);
      await page.reload({
        waitUntil: 'domcontentloaded',
        timeout: E2E_RESPONSE_TIMEOUT_MS,
      });
      const timelineResponse = await reloadTimeline;
      expect(timelineResponse.status()).toBe(200);
      expect((await readUnplaced(page)).status()).toBe(200);
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

  test('canonical date-span, coarse and named-zone forms survive real PostgreSQL reload', async ({
    browser,
  }, testInfo) => {
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo, 4));
      await openHome(page);
      const today = Temporal.Now.plainDateISO('Europe/Rome')
        .add({ days: 1 })
        .toString();

      const allDayTitle = `B02 E4 all-day ${testInfo.project.name}`;
      const allDay = await createScheduledActivity(page, allDayTitle, {
        kind: 'date_span',
        start_date: today,
        end_date_exclusive: Temporal.PlainDate.from(today)
          .add({ days: 1 })
          .toString(),
      });
      expect(allDay.temporal_form).toBe('date_span');
      expect(allDay.start_date).toBe(today);

      // Coarse placement no longer has a Create radio; its canonical
      // form is still an accepted, persisted Schedule contract.
      const coarseTitle = `B02 E4 coarse ${testInfo.project.name}`;
      const coarse = await createScheduledActivity(page, coarseTitle, {
        kind: 'coarse_local_period',
        local_date: today,
        period: 'afternoon',
      });
      expect(coarse.temporal_form).toBe('coarse_local_period');
      expect(coarse.local_date).toBe(today);
      expect(coarse.period).toBe('afternoon');

      const zonedTitle = `B02 E4 zoned ${testInfo.project.name}`;
      const zoned = await createScheduledActivity(page, zonedTitle, {
        kind: 'named_zone_local_interval',
        starts_local_at: `${today}T14:10:00`,
        ends_local_at: `${today}T14:40:00`,
        zone_id: 'Europe/Rome',
        disambiguation: 'reject',
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
      await page.reload({
        waitUntil: 'domcontentloaded',
        timeout: E2E_RESPONSE_TIMEOUT_MS,
      });
      const timelineResponse = await reloadTimeline;
      expect(timelineResponse.status()).toBe(200);
      expect((await readUnplaced(page)).status()).toBe(200);
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
