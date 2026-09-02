import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';
const projectEmailOffset: Readonly<Record<string, number>> = {
  chromium: 30,
  firefox: 40,
  webkit: 50,
};

function projectOffset(testInfo: TestInfo): number {
  const offset = projectEmailOffset[testInfo.project.name];
  if (offset === undefined) {
    throw new Error(
      `Unsupported M5 quality browser project: ${testInfo.project.name}`,
    );
  }
  return offset;
}

function emailFor(testInfo: TestInfo, slot: number): string {
  return `synthetic.user+e2e-${String(projectOffset(testInfo) + slot).padStart(2, '0')}@example.com`;
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

async function expectNoHorizontalOverflow(page: Page): Promise<void> {
  const hasOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
        document.documentElement.clientWidth ||
      document.body.scrollWidth > document.body.clientWidth,
  );
  expect(hasOverflow).toBe(false);
}

async function expectInsideViewport(
  page: Page,
  locator: ReturnType<Page['locator']>,
): Promise<void> {
  const viewport = page.viewportSize();
  const box = await locator.boundingBox();
  expect(viewport).not.toBeNull();
  expect(box).not.toBeNull();
  if (viewport === null || box === null) {
    return;
  }
  expect(box.x).toBeGreaterThanOrEqual(0);
  expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);
}

async function expectWcagAa(page: Page): Promise<void> {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
}

test.describe('DANTE Access/Auth M5 accessibility and responsive quality', () => {
  test.beforeEach(async ({ page }) => {
    await useItalianLocale(page);
  });

  test('meets WCAG AA on the unauthenticated Access surface', async ({ page }) => {
    await page.goto('/');
    await expect(
      page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
    ).toBeVisible();

    await expectWcagAa(page);
  });

  test('keeps the credential form keyboard order and visible focus deterministic', async ({
    page,
  }) => {
    await page.goto('/');

    const email = page.getByLabel('Email');
    const forgotPassword = page.getByRole('button', {
      name: 'Password dimenticata?',
    });
    const passwordInput = page.getByLabel('Password', { exact: true });
    const passwordToggle = page.getByRole('button', {
      name: 'Mostra password',
    });
    const submit = page.getByRole('button', {
      name: 'Continua',
      exact: true,
    });

    await email.focus();
    await expect(email).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(forgotPassword).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(passwordInput).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(passwordToggle).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(submit).toBeFocused();

    await page.keyboard.press('Shift+Tab');
    await expect(passwordToggle).toBeFocused();
  });

  test('keeps the Access surface inside a 320px mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 800 });
    await page.goto('/');

    const heading = page.getByRole('heading', {
      level: 1,
      name: 'Accedi a DANTE',
    });
    const email = page.getByLabel('Email');
    const passwordInput = page.getByLabel('Password', { exact: true });
    const submit = page.getByRole('button', {
      name: 'Continua',
      exact: true,
    });

    await expect(heading).toBeVisible();
    await expectNoHorizontalOverflow(page);
    await expectInsideViewport(page, heading);
    await expectInsideViewport(page, email);
    await expectInsideViewport(page, passwordInput);
    await expectInsideViewport(page, submit);
  });

  test('keeps authenticated /security WCAG AA and responsive at 360px', async ({
    page,
  }, testInfo) => {
    await page.setViewportSize({ width: 360, height: 800 });
    await signIn(page, emailFor(testInfo, 4));
    await page.goto('/security');

    const heading = page.getByRole('heading', {
      level: 1,
      name: 'Sicurezza account',
    });
    const reauthPassword = page.getByPlaceholder('Password');
    const reauthSubmit = page.getByRole('button', {
      name: 'Conferma con password',
    });
    const removePassword = page.getByRole('button', {
      name: 'Rimuovi password',
    });

    await expect(heading).toBeVisible();
    await expectNoHorizontalOverflow(page);
    await expectInsideViewport(page, heading);
    await expectInsideViewport(page, reauthPassword);
    await expectInsideViewport(page, reauthSubmit);
    await expectInsideViewport(page, removePassword);
    await expectWcagAa(page);
  });
});
