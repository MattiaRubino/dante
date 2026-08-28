import { expect, test, type BrowserContext, type Page } from '@playwright/test';

const baseURL = 'https://127.0.0.1:4173';
const email = 'synthetic.user@example.com';
const password = 'correct horse battery staple';
const sessionCookieName = '__Host-dante-session';

async function signIn(page: Page, passwordValue = password) {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
  ).toBeVisible();

  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password', { exact: true }).fill(passwordValue);

  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/auth/signin') &&
      response.request().method() === 'POST',
  );
  await page.getByRole('button', { name: 'Accedi', exact: true }).click();
  return responsePromise;
}

async function expectAuthenticated(page: Page) {
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
  ).toBeVisible();
}

async function expectUnauthenticated(page: Page) {
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
  ).toBeVisible();
}

async function sessionCookie(context: BrowserContext) {
  const cookies = await context.cookies(baseURL);
  return cookies.find((cookie) => cookie.name === sessionCookieName);
}

test.describe('DANTE Access/Auth full-stack spine', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem('dante.locale', 'it');
    });
  });

  test('signs in through real HTTPS/FastAPI/PostgreSQL, reloads, and logs out', async ({
    context,
    page,
  }) => {
    const signin = await signIn(page);
    expect(signin.status()).toBe(200);
    expect(await signin.headerValue('cache-control')).toBe('no-store');
    expect(await signin.headerValue('x-request-id')).toBeTruthy();

    const setCookie = await signin.headerValue('set-cookie');
    expect(setCookie).not.toBeNull();
    expect(setCookie).toContain(`${sessionCookieName}=`);
    expect(setCookie).toContain('Secure');
    expect(setCookie).toContain('HttpOnly');
    expect(setCookie).toContain('Path=/');
    expect(setCookie?.toLowerCase()).toContain('samesite=lax');
    expect(setCookie).not.toContain('Domain=');

    await expectAuthenticated(page);

    const cookie = await sessionCookie(context);
    expect(cookie).toBeDefined();
    expect(cookie?.httpOnly).toBe(true);
    expect(cookie?.secure).toBe(true);
    expect(cookie?.sameSite).toBe('Lax');
    expect(cookie?.path).toBe('/');
    expect(cookie?.domain).toBe('127.0.0.1');

    let releaseSession!: () => void;
    const sessionGate = new Promise<void>((resolve) => {
      releaseSession = resolve;
    });
    const sessionRoute = '**/api/v1/auth/session';

    await page.route(sessionRoute, async (route) => {
      if (route.request().method() !== 'GET') {
        await route.continue();
        return;
      }

      await sessionGate;
      await route.continue();
    });

    await page.reload();
    await expect(page.locator('[data-access-session-bootstrap]')).toBeVisible();
    await expect(page.locator('#access-signin-title')).toBeHidden();

    releaseSession();
    await expectAuthenticated(page);
    await page.unroute(sessionRoute);

    const logoutPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/session') &&
        response.request().method() === 'DELETE',
    );
    await page.getByRole('button', { name: 'Esci' }).click();
    const logout = await logoutPromise;
    expect(logout.status()).toBe(204);
    expect(await logout.headerValue('cache-control')).toBe('no-store');

    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('keeps invalid credentials unauthenticated with safe public feedback', async ({
    context,
    page,
  }) => {
    const response = await signIn(page, 'definitely wrong credential value');
    expect(response.status()).toBe(401);
    expect(await response.headerValue('content-type')).toContain(
      'application/problem+json',
    );

    await expect(page.getByText('Accesso non riuscito.')).toBeVisible();
    await expect(
      page.getByText('Email o password non sono corretti.'),
    ).toBeVisible();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('keeps two browser sessions independent when one logs out', async ({
    browser,
  }) => {
    const contextA = await browser.newContext({ ignoreHTTPSErrors: true });
    const contextB = await browser.newContext({ ignoreHTTPSErrors: true });

    try {
      const pageA = await contextA.newPage();
      const pageB = await contextB.newPage();

      await pageA.addInitScript(() => {
        window.localStorage.setItem('dante.locale', 'it');
      });
      await pageB.addInitScript(() => {
        window.localStorage.setItem('dante.locale', 'it');
      });

      expect((await signIn(pageA)).status()).toBe(200);
      expect((await signIn(pageB)).status()).toBe(200);
      await expectAuthenticated(pageA);
      await expectAuthenticated(pageB);

      const cookieA = await sessionCookie(contextA);
      const cookieB = await sessionCookie(contextB);
      expect(cookieA?.value).toBeTruthy();
      expect(cookieB?.value).toBeTruthy();
      expect(cookieA?.value).not.toBe(cookieB?.value);

      const logoutPromise = pageA.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/auth/session') &&
          response.request().method() === 'DELETE',
      );
      await pageA.getByRole('button', { name: 'Esci' }).click();
      expect((await logoutPromise).status()).toBe(204);
      await expectUnauthenticated(pageA);

      await pageB.reload();
      await expectAuthenticated(pageB);
      expect(await sessionCookie(contextB)).toBeDefined();
    } finally {
      await contextA.close();
      await contextB.close();
    }
  });
});
