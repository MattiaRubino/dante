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
const replacementPassword = 'replacement horse battery staple';
const sessionCookieName = '__Host-dante-session';
const repoRoot = resolve(
  dirname(fileURLToPath(import.meta.url)),
  '../../../..',
);

const projectEmailOffset: Readonly<Record<string, number>> = {
  chromium: 0,
  firefox: 10,
  webkit: 20,
};

type CapturedEmail = Readonly<{
  recipient: string;
  subject: string;
  body: string;
}>;

function projectOffset(testInfo: TestInfo): number {
  const offset = projectEmailOffset[testInfo.project.name];
  if (offset === undefined) {
    throw new Error(
      `Unsupported Access/Auth browser project: ${testInfo.project.name}`,
    );
  }
  return offset;
}

function emailFor(testInfo: TestInfo, slot: number) {
  return `synthetic.user+e2e-${String(projectOffset(testInfo) + slot).padStart(2, '0')}@example.com`;
}

function signupEmailFor(testInfo: TestInfo) {
  return `synthetic.signup+e2e-${String(projectOffset(testInfo) + 1).padStart(2, '0')}@example.com`;
}

function runHarnessCommand(args: readonly string[]): string {
  return execFileSync(
    'uv',
    [
      'run',
      '--project',
      'apps/backend',
      'python',
      'tooling/access-auth-e2e-control.py',
      ...args,
    ],
    {
      cwd: repoRoot,
      encoding: 'utf8',
      stdio: 'pipe',
      timeout: 30_000,
    },
  );
}

function runHarnessControl(action: string, value?: string) {
  const args = value === undefined ? [action] : [action, value];
  runHarnessCommand(args);
}

function capturedEmail(recipient: string, subject: string): CapturedEmail {
  const output = runHarnessCommand([
    'email-latest',
    recipient,
    '--subject',
    subject,
    '--wait-seconds',
    '10',
  ]);
  const parsed = JSON.parse(output) as unknown;
  if (
    typeof parsed !== 'object' ||
    parsed === null ||
    !('recipient' in parsed) ||
    !('subject' in parsed) ||
    !('body' in parsed) ||
    typeof parsed.recipient !== 'string' ||
    typeof parsed.subject !== 'string' ||
    typeof parsed.body !== 'string'
  ) {
    throw new Error('SMTP capture returned a malformed email payload.');
  }
  return parsed as CapturedEmail;
}

function verificationCode(email: CapturedEmail): string {
  const match = email.body.match(/verification code is ([0-9]{6})\./);
  if (!match?.[1]) {
    throw new Error(
      'Signup verification email did not contain a six-digit code.',
    );
  }
  return match[1];
}

function recoveryUrl(email: CapturedEmail): string {
  const match = email.body.match(
    /https:\/\/127\.0\.0\.1:4173\/\?recovery=[^\s#]+#[^\s]+/,
  );
  if (!match?.[0]) {
    throw new Error(
      'Recovery email did not contain the canonical recovery URL.',
    );
  }
  return match[0];
}

async function useItalianLocale(page: Page) {
  await page.addInitScript(() => {
    window.localStorage.setItem('dante.locale', 'it');
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
    await useItalianLocale(page);
  });

  test('signs in through real HTTPS/FastAPI/PostgreSQL, reloads, and logs out', async ({
    context,
    page,
  }, testInfo) => {
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

  test('keeps invalid credentials unauthenticated with safe public feedback', async ({
    context,
    page,
  }, testInfo) => {
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

  test('keeps two browser sessions independent when one logs out', async ({
    browser,
  }, testInfo) => {
    const contextA = await browser.newContext({ ignoreHTTPSErrors: true });
    const contextB = await browser.newContext({ ignoreHTTPSErrors: true });

    try {
      const pageA = await contextA.newPage();
      const pageB = await contextB.newPage();
      const email = emailFor(testInfo, 3);

      await useItalianLocale(pageA);
      await useItalianLocale(pageB);

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

  test('converges to unauthenticated after server-side session revocation', async ({
    context,
    page,
  }, testInfo) => {
    const signin = await signIn(page, emailFor(testInfo, 4));
    expect(signin.status()).toBe(200);
    await expectAuthenticated(page);

    const payload = (await signin.json()) as { auth_session_ref: string };
    runHarnessControl('revoke-session', payload.auth_session_ref);

    await page.reload();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('converges to unauthenticated after server-side session expiry', async ({
    context,
    page,
  }, testInfo) => {
    const signin = await signIn(page, emailFor(testInfo, 5));
    expect(signin.status()).toBe(200);
    await expectAuthenticated(page);

    const payload = (await signin.json()) as { auth_session_ref: string };
    runHarnessControl('expire-session', payload.auth_session_ref);

    await page.reload();
    await expectUnauthenticated(page);
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('does not invent authentication while PostgreSQL is unavailable', async ({
    context,
    page,
  }, testInfo) => {
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

  test('does not invent authentication when the real signin limiter rejects the request', async ({
    context,
    page,
  }, testInfo) => {
    const email = emailFor(testInfo, 7);

    expect(
      (await signIn(page, email, 'wrong password attempt one')).status(),
    ).toBe(401);
    expect(
      (await signIn(page, email, 'wrong password attempt two')).status(),
    ).toBe(401);

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

  test('creates a new password account only after real mailbox verification', async ({
    context,
    page,
  }, testInfo) => {
    const email = signupEmailFor(testInfo);
    runHarnessControl('email-clear');

    await page.goto('/');
    await page.getByRole('button', { name: 'Crea un account' }).click();
    await page.getByLabel('Email').fill(email);
    await page.getByRole('button', { name: 'Continua con email' }).click();
    await page.getByLabel('Password', { exact: true }).fill(password);

    const signupPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signup') &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Crea un account' }).click();
    const signup = await signupPromise;
    expect(signup.status()).toBe(200);
    expect(await signup.headerValue('cache-control')).toBe('no-store');
    expect(await signup.headerValue('x-request-id')).toBeTruthy();

    await expect(
      page.getByRole('heading', { name: 'Controlla la tua email' }),
    ).toBeVisible();
    expect(await sessionCookie(context)).toBeUndefined();

    const verificationEmail = capturedEmail(email, 'Verify your DANTE email');
    expect(verificationEmail.recipient).toBe(email);
    const code = verificationCode(verificationEmail);

    const verifyPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signup/verify') &&
        response.request().method() === 'POST',
    );
    await page.getByLabel('Codice di verifica').fill(code);
    await page.getByRole('button', { name: 'Verifica e continua' }).click();
    const verify = await verifyPromise;
    expect(verify.status()).toBe(200);
    expect(await verify.headerValue('cache-control')).toBe('no-store');
    expect((await verify.json()) as { outcome: string }).toMatchObject({
      outcome: 'authenticated',
    });

    await expect(
      page.getByRole('heading', { name: 'Come vuoi che DANTE ti chiami?' }),
    ).toBeVisible();
    expect(await sessionCookie(context)).toBeDefined();
  });

  test('verifies an existing mailbox without creating a new authenticated session', async ({
    context,
    page,
  }, testInfo) => {
    const email = emailFor(testInfo, 8);
    runHarnessControl('email-clear');

    await page.goto('/');
    await page.getByRole('button', { name: 'Crea un account' }).click();
    await page.getByLabel('Email').fill(email);
    await page.getByRole('button', { name: 'Continua con email' }).click();
    await page
      .getByLabel('Password', { exact: true })
      .fill('different strong password value');

    const signupPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signup') &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Crea un account' }).click();
    expect((await signupPromise).status()).toBe(200);

    const code = verificationCode(
      capturedEmail(email, 'Verify your DANTE email'),
    );
    const verifyPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signup/verify') &&
        response.request().method() === 'POST',
    );
    await page.getByLabel('Codice di verifica').fill(code);
    await page.getByRole('button', { name: 'Verifica e continua' }).click();
    const verify = await verifyPromise;
    expect(verify.status()).toBe(200);
    expect((await verify.json()) as { outcome: string }).toEqual({
      outcome: 'existing_account',
    });

    await expectUnauthenticated(page);
    await expect(page.getByText('Account già esistente.')).toBeVisible();
    expect(await sessionCookie(context)).toBeUndefined();
  });

  test('resets through a real recovery email, scrubs the bearer URL, and revokes every existing session', async ({
    browser,
  }, testInfo) => {
    test.setTimeout(90_000);

    const email = emailFor(testInfo, 9);
    const contextA = await browser.newContext({ ignoreHTTPSErrors: true });
    const contextB = await browser.newContext({ ignoreHTTPSErrors: true });
    const recoveryContext = await browser.newContext({
      ignoreHTTPSErrors: true,
    });

    try {
      const pageA = await contextA.newPage();
      const pageB = await contextB.newPage();
      const recoveryPage = await recoveryContext.newPage();
      await useItalianLocale(pageA);
      await useItalianLocale(pageB);
      await useItalianLocale(recoveryPage);

      expect((await signIn(pageA, email)).status()).toBe(200);
      expect((await signIn(pageB, email)).status()).toBe(200);
      await expectAuthenticated(pageA);
      await expectAuthenticated(pageB);
      expect(await sessionCookie(contextA)).toBeDefined();
      expect(await sessionCookie(contextB)).toBeDefined();

      runHarnessControl('email-clear');
      await recoveryPage.goto('/');
      await recoveryPage
        .getByRole('button', { name: 'Password dimenticata?' })
        .click();
      await recoveryPage.getByLabel('Email').fill(email);
      const recoveryRequestPromise = recoveryPage.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/auth/recovery') &&
          response.request().method() === 'POST',
      );
      await recoveryPage
        .getByRole('button', { name: 'Invia link di recupero' })
        .click();
      const recoveryRequest = await recoveryRequestPromise;
      expect(recoveryRequest.status()).toBe(202);
      expect(await recoveryRequest.json()).toEqual({ accepted: true });

      const emailPayload = capturedEmail(email, 'Reset your DANTE password');
      const url = recoveryUrl(emailPayload);
      const secret = new URL(url).hash.slice(1);
      expect(secret.length).toBeGreaterThan(0);

      const validationPromise = recoveryPage.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/auth/recovery/validate') &&
          response.request().method() === 'POST',
      );
      await recoveryPage.goto(url);
      const validation = await validationPromise;
      expect(validation.status()).toBe(200);
      expect(await validation.json()).toEqual({ valid: true });

      await expect(
        recoveryPage.getByRole('heading', { name: 'Crea una nuova password' }),
      ).toBeVisible();
      const validatedUrl = new URL(recoveryPage.url());
      expect(validatedUrl.hash).toBe('');
      expect(validatedUrl.searchParams.has('recovery')).toBe(true);

      const browserStorage = await recoveryPage.evaluate(() => {
        const values: string[] = [];
        for (const storage of [window.localStorage, window.sessionStorage]) {
          for (let index = 0; index < storage.length; index += 1) {
            const key = storage.key(index);
            if (key !== null) {
              values.push(`${key}=${storage.getItem(key) ?? ''}`);
            }
          }
        }
        return values.join('\n');
      });
      expect(browserStorage).not.toContain(secret);

      await recoveryPage
        .getByLabel('Nuova password', { exact: true })
        .fill(replacementPassword);
      await recoveryPage
        .getByLabel('Conferma password', { exact: true })
        .fill(replacementPassword);
      const resetPromise = recoveryPage.waitForResponse(
        (response) =>
          response.url().endsWith('/api/v1/auth/reset-password') &&
          response.request().method() === 'POST',
      );
      await recoveryPage
        .getByRole('button', { name: 'Aggiorna password' })
        .click();
      const reset = await resetPromise;
      expect(reset.status()).toBe(204);
      expect(await reset.headerValue('cache-control')).toBe('no-store');

      await expect(
        recoveryPage.getByRole('heading', { name: 'Password aggiornata' }),
      ).toBeVisible();
      const consumedUrl = new URL(recoveryPage.url());
      expect(consumedUrl.hash).toBe('');
      expect(consumedUrl.searchParams.has('recovery')).toBe(false);

      const notification = capturedEmail(
        email,
        'Your DANTE password was changed',
      );
      expect(notification.body).toContain(
        'All existing sessions were signed out.',
      );

      await pageA.reload();
      await pageB.reload();
      await expectUnauthenticated(pageA);
      await expectUnauthenticated(pageB);
      expect(await sessionCookie(contextA)).toBeUndefined();
      expect(await sessionCookie(contextB)).toBeUndefined();
    } finally {
      await contextA.close();
      await contextB.close();
      await recoveryContext.close();
    }
  });

  test('reauthenticates in the browser on the same AuthSession while rotating the bearer', async ({
    context,
    page,
  }, testInfo) => {
    const signin = await signIn(page, emailFor(testInfo, 10));
    expect(signin.status()).toBe(200);
    const session = (await signin.json()) as {
      auth_session_ref: string;
      csrf_token: string;
    };
    const beforeCookie = await sessionCookie(context);
    expect(beforeCookie?.value).toBeTruthy();

    const result = await page.evaluate(
      async ({ passwordValue, csrfToken }) => {
        const response = await window.fetch('/api/v1/auth/reauthenticate', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            Accept: 'application/json, application/problem+json',
            'Content-Type': 'application/json',
            'X-Dante-Client': 'web',
            'X-Dante-CSRF': csrfToken,
          },
          body: JSON.stringify({ password: passwordValue }),
        });
        return {
          status: response.status,
          cacheControl: response.headers.get('cache-control'),
          requestId: response.headers.get('x-request-id'),
          payload: (await response.json()) as {
            auth_session_ref: string;
            authenticated: boolean;
          },
        };
      },
      { passwordValue: password, csrfToken: session.csrf_token },
    );

    expect(result.status).toBe(200);
    expect(result.cacheControl).toBe('no-store');
    expect(result.requestId).toBeTruthy();
    expect(result.payload.authenticated).toBe(true);
    expect(result.payload.auth_session_ref).toBe(session.auth_session_ref);

    const afterCookie = await sessionCookie(context);
    expect(afterCookie?.value).toBeTruthy();
    expect(afterCookie?.value).not.toBe(beforeCookie?.value);

    await page.reload();
    await expectAuthenticated(page);
  });
});
