import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { Temporal } from '@dante/time';
import { expect, test, type Page, type Response, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';
const repoRoot = resolve(
  dirname(fileURLToPath(import.meta.url)),
  '../../../..',
);

const projectEmailBase: Readonly<Record<string, number>> = {
  chromium: 35,
  firefox: 45,
  webkit: 55,
};

function emailFor(testInfo: TestInfo, slot: 1 | 2 | 3): string {
  const base = projectEmailBase[testInfo.project.name];
  if (base === undefined) {
    throw new Error(
      `Unsupported temporal B00 browser project: ${testInfo.project.name}`,
    );
  }
  return `synthetic.user+e2e-${base + slot}@example.com`;
}

function runHarnessControl(action: 'database-stop' | 'database-start'): void {
  execFileSync(
    'uv',
    [
      'run',
      '--project',
      'apps/backend',
      'python',
      'tooling/access-auth-e2e-control.py',
      action,
    ],
    {
      cwd: repoRoot,
      encoding: 'utf8',
      stdio: 'pipe',
      timeout: 30_000,
    },
  );
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
  );
  await page.getByRole('button', { name: 'Accedi', exact: true }).click();
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
  ).toBeVisible();
}

async function openHomeAndWaitForTemporalRead(
  page: Page,
  target = '/home',
  timeoutMs = 20_000,
) {
  const temporalResponsePromise = page.waitForResponse(
    (response) =>
      response.url().includes('/api/v1/temporal/timeline/window') &&
      response.request().method() === 'GET',
    { timeout: timeoutMs },
  );
  await page.goto(target, {
    waitUntil: 'domcontentloaded',
    timeout: timeoutMs,
  });
  return await temporalResponsePromise;
}

test.describe('Timeline B00 real full-stack spine', () => {
  test('reads the production Home Timeline through auth, DanteContext, timezone and PostgreSQL without prototype cards', async ({
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

      const temporalResponse = await openHomeAndWaitForTemporalRead(page);

      expect(temporalResponse.status()).toBe(200);
      expect(await temporalResponse.headerValue('cache-control')).toBe(
        'no-store',
      );
      expect(
        (await temporalResponse.request().allHeaders())['x-dante-time-zone'],
      ).toBe('Europe/Rome');

      const payload = (await temporalResponse.json()) as unknown;
      expect(payload).toMatchObject({
        kind: 'empty',
        effective_zone_id: 'Europe/Rome',
      });
      expect(JSON.stringify(payload)).not.toContain('self_person_ref');

      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
      await expect(
        page.getByText('Redesign LifeOS — sessione focus'),
      ).toHaveCount(0);
    } finally {
      await context.close();
    }
  });

  test('creates one canonical scheduled Event without fabricating local truth', async ({
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

      // Keep this strict full-stack Create assertion on a real future date
      // and display that date in the Timeline being inspected.
      const eventDate = Temporal.Now.plainDateISO('Europe/Rome')
        .add({ days: 1 })
        .toString();
      expect(
        (await openHomeAndWaitForTemporalRead(page, `/home?date=${eventDate}`)).status(),
      ).toBe(200);
      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();

      await page
        .getByRole('button', { name: 'Aggiungi alla timeline' })
        .click();
      const dialog = page.locator('[data-temporal-create="composer"]');
      await expect(dialog).toBeVisible();
      await dialog.getByRole('radio', { name: 'Evento' }).click();
      await dialog.getByRole('radio', { name: 'Orario' }).click();
      await dialog.getByLabel('Titolo').fill('B00 Evento reale');
      // Current Create uses controlled date and segmented time widgets,
      // not editable native inputs. The routed day is the selected date.
      await expect(
        dialog.getByRole('button', { name: /^Data inizio:/ }),
      ).toHaveAttribute('data-temporal-date', eventDate);
      await dialog.getByRole('textbox', { name: 'Inizio: ore' }).fill('10');
      await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).fill('00');

      // Real-stack validation: the Event must exist in PostgreSQL before
      // the projection shows it, and the frontend cannot invent its ref.
      const createResponsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/temporal/authoring/events') &&
          response.request().method() === 'POST',
        { timeout: 20_000 },
      );
      const timelineRefresh = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/timeline/window') &&
          response.request().method() === 'GET',
        { timeout: 20_000 },
      );
      await dialog.getByRole('button', { name: 'Aggiungi', exact: true }).click();
      const created = await createResponsePromise;
      expect(created.status()).toBe(201);
      const data = (await created.json()) as {
        event_ref: string;
        schedule: null | { schedule_ref: string };
      };
      expect(data.event_ref).toMatch(/^[a-f0-9-]{36}$/i);
      expect(data.schedule).not.toBeNull();
      if (!data.schedule) {
        throw new Error('Timed Event authoring returned no canonical Schedule.');
      }
      expect(data.schedule.schedule_ref).toMatch(/^[a-f0-9-]{36}$/i);
      expect((await timelineRefresh).status()).toBe(200);
      await expect(dialog).toHaveCount(0);
      // The POST response is canonical DB truth, but the first invalidated
      // GET can complete before the React hydration pass. A fresh page load
      // explicitly proves durable readback rather than optimistic UI state.
      const readback = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/timeline/window') &&
          response.request().method() === 'GET',
      );
      await page.reload();
      const canonicalReadback = await readback;
      expect(canonicalReadback.status()).toBe(200);
      const payload = (await canonicalReadback.json()) as {
        items?: Array<{ schedule_ref?: string }>;
      };
      expect(payload.items?.some(
        (item) => item.schedule_ref === data.schedule?.schedule_ref,
      )).toBe(true);
      await expect(
        page.locator(`[data-timeline-event="${data.schedule.schedule_ref}"]`),
      ).toHaveCount(1);
    } finally {
      await context.close();
    }
  });

  test('shows a truthful temporal read failure during PostgreSQL outage and recovers only after explicit retry', async ({
    browser,
  }, testInfo) => {
    // A real Docker stop/restart plus a database connection-pool timeout can
    // legitimately take longer than the 60s limit used for normal UI cases.
    // Keep all 500/error/retry/200 assertions, with a bounded 2-minute budget.
    test.setTimeout(120_000);
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      timezoneId: 'Europe/Rome',
    });
    let databaseStopped = false;

    try {
      const page = await context.newPage();
      await useItalianLocale(page);
      await signIn(page, emailFor(testInfo, 3));

      expect((await openHomeAndWaitForTemporalRead(page)).status()).toBe(200);
      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();

      runHarnessControl('database-stop');
      databaseStopped = true;

      // The authoritative Timeline GET is deliberately preceded by a
      // GET /auth/session to obtain CSRF, then POST /occurrences/checkpoint.
      // With PostgreSQL stopped, the auth/session request itself can fail,
      // short-circuiting the checkpoint and the Timeline GET. Testing only
      // one downstream endpoint yields a false timeout. Preserve the real
      // outage by proving 5xx directly, then require the UI's error state.
      const probe = await page.request.get(
        '/api/v1/temporal/timeline/window?start_date=2034-02-17&end_date_exclusive=2034-02-18',
        {
          headers: { 'X-Dante-Time-Zone': 'Europe/Rome' },
          timeout: 12_000,
        },
      );
      expect(probe.status()).toBeGreaterThanOrEqual(500);

      const outageResponses: string[] = [];
      const observeOutage = (response: Response) => {
        const address = new URL(response.url());
        if (
          address.pathname.startsWith('/api/v1/auth/') ||
          address.pathname.startsWith('/api/v1/temporal/')
        ) {
          outageResponses.push(
            `${response.request().method()} ${address.pathname} ${response.status()}`,
          );
        }
      };
      page.on('response', observeOutage);
      const errorStatus = page.locator(
        '.temporal-timeline-runtime-status--error',
      );
      try {
        // Navigate inside the mounted, signed-in SPA so Timeline must
        // checkpoint a different window without repeating sign-in.
        await page.locator('.dante-timeline-week-step').last().click();
        await expect(errorStatus).toContainText(
          'Timeline non disponibile',
          { timeout: 15_000 },
        );
      } catch (cause) {
        throw new Error(
          'PostgreSQL outage did not surface the Timeline error after in-app navigation. Browser API responses: ' +
            (outageResponses.join('; ') || '(no API response)'),
          { cause },
        );
      } finally {
        page.off('response', observeOutage);
      }
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);

      runHarnessControl('database-start');
      databaseStopped = false;

      const recoveryResponsePromise = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/timeline/window') &&
          response.request().method() === 'GET',
        { timeout: 15_000 },
      );
      await errorStatus.getByRole('button', { name: 'Riprova' }).click();
      expect((await recoveryResponsePromise).status()).toBe(200);

      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();
      await expect(errorStatus).toHaveCount(0);
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
    } finally {
      if (databaseStopped) {
        runHarnessControl('database-start');
      }
      await context.close();
    }
  });
});
