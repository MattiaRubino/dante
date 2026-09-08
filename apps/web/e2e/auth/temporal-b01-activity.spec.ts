import { expect, test, type Page, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';

const projectEmail: Readonly<Record<string, string>> = {
  chromium: 'synthetic.user+e2e-61@example.com',
  firefox: 'synthetic.user+e2e-62@example.com',
  webkit: 'synthetic.user+e2e-63@example.com',
};

function emailFor(testInfo: TestInfo): string {
  const email = projectEmail[testInfo.project.name];
  if (!email) {
    throw new Error(
      `Unsupported temporal B01 browser project: ${testInfo.project.name}`,
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
  );
  await page.getByRole('button', { name: 'Continua', exact: true }).click();
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
  );
}

function waitForUnplacedRead(page: Page) {
  return page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/temporal/activities/unplaced') &&
      response.request().method() === 'GET',
  );
}

test.describe('Timeline B01 canonical Activity vertical', () => {
  test(
    'creates and reloads one canonical unplaced Activity',
    async ({ browser }, testInfo) => {
      const context = await browser.newContext({
        ignoreHTTPSErrors: true,
        timezoneId: 'Europe/Rome',
      });

      try {
        const page = await context.newPage();
        await useItalianLocale(page);
        await signIn(page, emailFor(testInfo));

        const initialTimeline = waitForTimelineRead(page);
        const initialUnplaced = waitForUnplacedRead(page);
        await page.goto('/home');
        expect((await initialTimeline).status()).toBe(200);
        expect((await initialUnplaced).status()).toBe(200);
        await expect(
          page.locator('[data-temporal-read-state="ready"]'),
        ).toBeVisible();

        const title = `B01 Activity persistita ${testInfo.project.name}`;
        await page
          .getByRole('button', { name: 'Aggiungi alla timeline' })
          .click();
        await expect(
          page.getByRole('radio', { name: 'Attività' }),
        ).toHaveAttribute('aria-checked', 'true');
        await page.getByLabel('Titolo').fill(title);

        const createResponsePromise = page.waitForResponse(
          (response) =>
            response.url().endsWith('/api/v1/temporal/activities') &&
            response.request().method() === 'POST',
        );
        await page
          .getByRole('button', { name: 'Aggiungi', exact: true })
          .click();
        const createResponse = await createResponsePromise;
        expect(createResponse.status()).toBe(201);
        const created = (await createResponse.json()) as {
          activity_ref: string;
          title: string;
          replayed: boolean;
        };
        expect(created.title).toBe(title);
        expect(created.replayed).toBe(false);

        const firstPlanningReadPromise = waitForUnplacedRead(page);
        await page
          .getByRole('button', { name: 'Apri attività da collocare' })
          .click();
        const firstPlanningRead = await firstPlanningReadPromise;
        expect(firstPlanningRead.status()).toBe(200);
        const firstPayload = (await firstPlanningRead.json()) as {
          kind: string;
          items: { activity_ref: string; title: string }[];
        };
        expect(firstPayload.kind).toBe('unplaced');
        expect(
          firstPayload.items.filter(
            (item) => item.activity_ref === created.activity_ref,
          ),
        ).toHaveLength(1);

        const firstCard = page.locator(
          `[data-temporal-activity-ref="${created.activity_ref}"]`,
        );
        await expect(firstCard).toHaveCount(1);
        await expect(firstCard).toContainText(title);
        await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
        await expect(
          page.getByRole('button', { name: 'Colloca', exact: true }),
        ).toHaveCount(0);

        const reloadTimeline = waitForTimelineRead(page);
        const reloadUnplaced = waitForUnplacedRead(page);
        await page.reload();
        expect((await reloadTimeline).status()).toBe(200);
        const reloadRead = await reloadUnplaced;
        expect(reloadRead.status()).toBe(200);
        const reloadPayload = (await reloadRead.json()) as {
          kind: string;
          items: { activity_ref: string; title: string }[];
        };
        expect(
          reloadPayload.items.filter(
            (item) => item.activity_ref === created.activity_ref,
          ),
        ).toHaveLength(1);

        const secondPlanningReadPromise = waitForUnplacedRead(page);
        await page
          .getByRole('button', { name: 'Apri attività da collocare' })
          .click();
        expect((await secondPlanningReadPromise).status()).toBe(200);

        const reloadedCard = page.locator(
          `[data-temporal-activity-ref="${created.activity_ref}"]`,
        );
        await expect(reloadedCard).toHaveCount(1);
        await expect(reloadedCard).toContainText(title);
        await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
      } finally {
        await context.close();
      }
    },
  );
});
