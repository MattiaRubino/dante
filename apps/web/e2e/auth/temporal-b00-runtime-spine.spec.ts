import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { expect, test, type Page, type TestInfo } from '@playwright/test';

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
  await page.getByRole('button', { name: 'Continua', exact: true }).click();
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
  ).toBeVisible();
}

async function openHomeAndWaitForTemporalRead(page: Page, target = '/home') {
  const temporalResponsePromise = page.waitForResponse(
    (response) =>
      response.url().includes('/api/v1/temporal/timeline/window') &&
      response.request().method() === 'GET',
  );
  await page.goto(target);
  return temporalResponsePromise;
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

  test('fails closed for unsupported Event Create', async ({
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

      expect((await openHomeAndWaitForTemporalRead(page)).status()).toBe(200);
      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();

      await page
        .getByRole('button', { name: 'Aggiungi alla timeline' })
        .click();
      await page.getByRole('radio', { name: 'Evento' }).click();
      await page.getByLabel('Titolo').fill('B00 non deve fingere un Evento');
      await page.getByRole('button', { name: 'Aggiungi', exact: true }).click();

      await expect(
        page.getByText(
          'Non è stato possibile applicare la creazione. La bozza è ancora qui.',
        ),
      ).toBeVisible();
      await expect(page.getByLabel('Titolo')).toHaveValue(
        'B00 non deve fingere un Evento',
      );
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
    } finally {
      await context.close();
    }
  });

  test('shows a truthful temporal read failure during PostgreSQL outage and recovers only after explicit retry', async ({
    browser,
  }, testInfo) => {
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

      const failedRead = await openHomeAndWaitForTemporalRead(
        page,
        '/home?date=2034-02-17',
      );
      expect(failedRead.status()).toBeGreaterThanOrEqual(500);

      const errorStatus = page.locator(
        '.temporal-timeline-runtime-status--error',
      );
      await expect(errorStatus).toContainText('Timeline non disponibile');
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);

      runHarnessControl('database-start');
      databaseStopped = false;

      const recoveryResponsePromise = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/timeline/window') &&
          response.request().method() === 'GET',
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
