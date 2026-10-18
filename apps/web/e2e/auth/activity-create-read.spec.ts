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
  );
}

function readUnplaced(page: Page) {
  // Legacy canonical activity inventory is no longer fetched automatically
  // by Home. Exercise the authenticated endpoint explicitly after navigation.
  return page.request.get('/api/v1/temporal/activities/unplaced', {
    headers: { 'X-Dante-Time-Zone': 'Europe/Rome' },
  });
}
test.describe('Timeline B01 canonical Activity vertical', () => {
  test('creates one canonical unplaced Activity by U2 API and reviews it separately from Draft Vault', async ({
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

      const initialTimeline = waitForTimelineRead(page);
      await page.goto('/home');
      expect((await initialTimeline).status()).toBe(200);
      expect((await readUnplaced(page)).status()).toBe(200);
      await expect(
        page.locator('[data-temporal-read-state="ready"]'),
      ).toBeVisible();

      const title = `B01 Activity persistita ${testInfo.project.name}`;
      // U2 Quick Create no longer offers an unplaced mode. This scenario
      // explicitly proves canonical U2 authoring with placement=null,
      // then its isolation from the Timeline and Draft Vault.
      const authored = await page.evaluate(async (activityTitle) => {
        const sessionResponse = await fetch('/api/v1/auth/session', {
          credentials: 'same-origin',
        });
        const session = (await sessionResponse.json()) as {
          authenticated?: boolean;
          csrf_token?: string;
        };
        if (
          !sessionResponse.ok ||
          session.authenticated !== true ||
          !session.csrf_token
        ) {
          throw new Error('An authenticated CSRF session is required.');
        }
        const response = await fetch('/api/v1/temporal/authoring/activities', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-Client': 'web',
            'X-Dante-Time-Zone': 'Europe/Rome',
            'X-Dante-CSRF': session.csrf_token,
          },
          body: JSON.stringify({
            operation_id: `e2e:b01:${crypto.randomUUID()}`,
            title: activityTitle,
            placement: null,
          }),
        });
        return {
          status: response.status,
          payload: (await response.json()) as {
            activity_ref: string;
            title: string;
            replayed: boolean;
            schedule: unknown;
          },
        };
      }, title);
      expect(authored.status).toBe(201);
      const created = authored.payload;
      expect(created.title).toBe(title);
      expect(created.replayed).toBe(false);
      expect(created.schedule).toBeNull();
      expect(created.activity_ref).toMatch(/^[0-9a-f-]{36}$/i);

      // Direct API mutations do not emit Home's in-memory invalidation.
      const createdRead = waitForTimelineRead(page);
      await page.reload();
      expect((await createdRead).status()).toBe(200);
      const firstPlanningRead = await readUnplaced(page);
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

      // The legacy "Elementi preesistenti senza orario" panel was retired.
      // A canonical unplaced Activity remains real backend truth, NOT a
      // Timeline card and NOT an inert Draft. Check both boundaries directly.
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
      await page.getByRole('button', { name: 'Apri Bozze' }).click();
      await expect(
        page.locator('[data-timeline-draft-vault="true"] article').filter({
          hasText: title,
        }),
      ).toHaveCount(0);
      await page.getByRole('button', { name: 'Chiudi Bozze' }).click();
      await expect(
        page.getByRole('button', { name: 'Colloca', exact: true }),
      ).toHaveCount(0);

      const reloadTimeline = waitForTimelineRead(page);
      await page.reload();
      expect((await reloadTimeline).status()).toBe(200);
      const reloadRead = await readUnplaced(page);
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

      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
      await page.getByRole('button', { name: 'Apri Bozze' }).click();
      await expect(
        page.locator('[data-timeline-draft-vault="true"] article').filter({
          hasText: title,
        }),
      ).toHaveCount(0);
      await page.getByRole('button', { name: 'Chiudi Bozze' }).click();
      const discardedDraftTitle = `B01 bozza scartata ${testInfo.project.name}`;
      await page
        .getByRole('button', { name: 'Aggiungi alla timeline' })
        .click();
      const editor = page.locator('[data-temporal-create="composer"]');
      await editor
        .getByRole('textbox', { name: 'Titolo' })
        .fill(discardedDraftTitle);
      await editor.locator('.dante-temporal-panel-close').click();
      await expect(
        page.getByRole('alertdialog', { name: 'Scartare questa bozza?' }),
      ).toBeVisible();
      await page.getByRole('button', { name: 'Scarta', exact: true }).click();

      const discardReloadTimeline = waitForTimelineRead(page);
      await page.reload();
      expect((await discardReloadTimeline).status()).toBe(200);
      const discardReloadRead = await readUnplaced(page);
      expect(discardReloadRead.status()).toBe(200);
      const discardReloadPayload = (await discardReloadRead.json()) as {
        kind: string;
        items: { activity_ref: string; title: string }[];
      };
      expect(
        discardReloadPayload.items.filter(
          (item) => item.activity_ref === created.activity_ref,
        ),
      ).toHaveLength(1);
      expect(
        discardReloadPayload.items.filter(
          (item) => item.title === discardedDraftTitle,
        ),
      ).toHaveLength(0);

      // Closing an unsaved draft must neither create a new canonical
      // Activity nor mutate the previously persisted unplaced Activity.
      await expect(page.locator('[data-timeline-event]')).toHaveCount(0);
      await page.getByRole('button', { name: 'Apri Bozze' }).click();
      await expect(
        page.locator('[data-timeline-draft-vault="true"] article').filter({
          hasText: discardedDraftTitle,
        }),
      ).toHaveCount(0);
      await page.getByRole('button', { name: 'Chiudi Bozze' }).click();
    } finally {
      await context.close();
    }
  });
});
