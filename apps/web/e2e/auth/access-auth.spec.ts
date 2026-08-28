import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  expect,
  test,
  type BrowserContext,
  type Page,
  type TestInfo,
} from '@playwright/test';

const baseURL = 'https://127.0.0.1:4173';
const password = 'correct horse battery staple';
const sessionCookieName = '__Host-dante-session';
const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');

const projectEmailOffset: Readonly<Record<string, number>> = {
  chromium: 0,
  firefox: 10,
  webkit: 20,
};

function emailFor(testInfo: TestInfo, slot: number) {
  const offset = projectEmailOffset[testInfo.project.name];
  if (offset === undefined) {
    throw new Error(`Unsupported Access/Auth browser project: ${testInfo.project.name}`);
  }
  return `synthetic.user+e2e-${String(offset + slot).padStart(2, '0')}@example.com`;
}

function runHarnessControl(action: string, authSessionRef?: string) {
  const args = [
    'run',
    '--project',
    'apps/backend',
    'python',
    'tooling/access-auth-e2e-control.py',
    action,
  ];
  if (authSessionRef !== undefined) {
    args.push(authSessionRef);
  }
  execFileSync('uv', args, {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: 'pipe',
    timeout: 30_000,
  });
}

async function signIn(
  page: Page,
  emailValue: string,
  passwordValue = password,
) {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
  ).toBeVisible();

  await page.getByLabel('Email').fill(emailValue);
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

  test('signs in through real HTTPS/FastAPI/PostgreSQL, reloads, and logs out', async (
    { context, page },
    testInfo,
  ) => {
    const signin = await signIn(page, emailFor(testInfo, 1));
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
    let markSessionStarted!: () => void;
    const sessionGate = new Promise<void>((resolvePromise) => {
      releaseSession = resolvePromise;
    });
    const sessionStarted = new Promise<void>((resolvePromise) => {
      markSessionStarted = resolvePromise;
    });
    const sessionRoute = '**/api/v1/auth/session';

    await page.route(sessionRoute, async (route) => {
      if (route.request().method() !== 'GET') {
        await route.continue();
        return;
      }

      markSessionStarted();
      await sessionGate;
      await route.continue();
    });

    const reloadPromise = page.reload();
    await sessionStarted;
    await expect(page.locator('#access-signin-title')).toHaveCount(0);
    await expect(
      page.locator('#access-authenticated-return-title'),
    ).toHaveCount(0);

    releaseSession();
    await reloadPromise;
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

  test('keeps invalid credentials unauthenticated with safe public feedback', async (
    { context, page },
    testInfo,
  ) => {
    const response = await signIn(
      page,
      emailFor(testInfo, 2),
      'definitely wrong credential value',
    );
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

  test('keeps two browser sessions independent when one logs out', async (
    { browser },
    testInfo,
  ) => {
    const contextA = await browser.newContext({ ignoreHTTPSErrors: true });
    const contextB = await browser.newContext({ ignoreHTTPSErrors: true });

    try {
      const pageA = await contextA.newPage();
      const pageB = await contextB.newPage();
      const email = emailFor(testInfo, 3);

      await pageA.addInitScript(() => {
        window.localStorage.setItem('dante.locale', 'it');
      });
      await pageB.addInitScript(() => {
        window.localStorage.setItem('dante.locale', 'it');
      });

      expect((await signIn(pageA, email)).status()).toBe(200);
      expect((await signIn(pageB, email)).status()).toBe(200);
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

  test('converges to unauthenticated after server-side session revocation', async (
    { context, page },
    testInfo,
  ) => {
    const signin = await signIn(page, emailFor(testInfo, 4));
    expect(signin.status()).toBe(200);
    await expectAuthenticated(page);

    const payload = (await signin.json()) as { auth_session_ref: string };
    runHarnessControl('revoke-session', payload.auth_session_ref);

    await page.reload();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('converges to unauthenticated after server-side session expiry', async (
    { context, page },
    testInfo,
  ) => {
    const signin = await signIn(page, emailFor(testInfo, 5));
    expect(signin.status()).toBe(200);
    await expectAuthenticated(page);

    const payload = (await signin.json()) as { auth_session_ref: string };
    runHarnessControl('expire-session', payload.auth_session_ref);

    await page.reload();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('does not invent authentication while PostgreSQL is unavailable', async (
    { context, page },
    testInfo,
  ) => {
    await page.goto('/');
    await expectUnauthenticated(page);
    await page.getByLabel('Email').fill(emailFor(testInfo, 6));
    await page.getByLabel('Password', { exact: true }).fill(password);

    runHarnessControl('database-stop');
    try {
      const responsePromise = page.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/auth/signin') &&
          response.request().method() === 'POST',
      );
      await page.getByRole('button', { name: 'Accedi', exact: true }).click();
      const response = await responsePromise;

      expect(response.status()).toBe(503);
      expect(await response.headerValue('content-type')).toContain(
        'application/problem+json',
      );
      await expect(
        page.getByText('Servizio temporaneamente non disponibile.'),
      ).toBeVisible();
      await expectUnauthenticated(page);
      expect(await sessionCookie(context)).toBeUndefined();
    } finally {
      runHarnessControl('database-start');
    }
  });

  test('does not invent authentication when the real signin limiter rejects the request', async (
    { context, page },
    testInfo,
  ) => {
    const email = emailFor(testInfo, 7);

    expect((await signIn(page, email, 'wrong password attempt one')).status()).toBe(
      401,
    );
    expect((await signIn(page, email, 'wrong password attempt two')).status()).toBe(
      401,
    );

    const response = await signIn(page, email, 'wrong password attempt three');
    expect(response.status()).toBe(429);
    expect(await response.headerValue('content-type')).toContain(
      'application/problem+json',
    );
    expect(await response.headerValue('retry-after')).toBeTruthy();

    await expect(page.getByText('Troppi tentativi.')).toBeVisible();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });
});
