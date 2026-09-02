import { expect, test, type Page, type Response, type TestInfo } from '@playwright/test';

const password = 'correct horse battery staple';

const projectEmailOffset: Readonly<Record<string, number>> = {
  chromium: 30,
  firefox: 40,
  webkit: 50,
};

const methodsPath = '/api/v1/auth/methods';
const removePasswordPath = '/api/v1/auth/password';
const googleBeginPath = '/api/v1/auth/google/begin';
const appleBeginPath = '/api/v1/auth/apple/begin';
const passkeyAuthenticationBeginPath =
  '/api/v1/auth/passkeys/authentication/begin';
const passkeyRegistrationBeginPath = '/api/v1/auth/passkeys/registration/begin';

function projectOffset(testInfo: TestInfo): number {
  const offset = projectEmailOffset[testInfo.project.name];
  if (offset === undefined) {
    throw new Error(`Unsupported M5 browser project: ${testInfo.project.name}`);
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

async function signIn(page: Page, email: string): Promise<Response> {
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
  return response;
}

async function csrfToken(response: Response): Promise<string> {
  const payload = (await response.json()) as unknown;
  if (
    typeof payload !== 'object' ||
    payload === null ||
    !('csrf_token' in payload) ||
    typeof payload.csrf_token !== 'string' ||
    payload.csrf_token.length === 0
  ) {
    throw new Error('Authenticated response omitted its session CSRF token.');
  }
  return payload.csrf_token;
}

function problemCode(payload: unknown): string | null {
  if (
    typeof payload === 'object' &&
    payload !== null &&
    'code' in payload &&
    typeof payload.code === 'string'
  ) {
    return payload.code;
  }
  return null;
}

async function responseProblemCode(response: Response): Promise<string | null> {
  return problemCode((await response.json()) as unknown);
}

async function browserPostWithoutCsrf(
  page: Page,
  path: string,
  payload: Readonly<Record<string, string>>,
): Promise<Readonly<{ status: number; body: unknown }>> {
  return page.evaluate(
    async ({ requestPath, requestPayload }) => {
      const response = await fetch(requestPath, {
        method: 'POST',
        headers: {
          Accept: 'application/json, application/problem+json',
          'Content-Type': 'application/json',
          'X-Dante-Client': 'web',
        },
        body: JSON.stringify(requestPayload),
      });
      return {
        status: response.status,
        body: (await response.json()) as unknown,
      };
    },
    { requestPath: path, requestPayload: payload },
  );
}

async function openSecurity(page: Page): Promise<Response> {
  const methodsPromise = page.waitForResponse(
    (response) =>
      response.url().endsWith(methodsPath) &&
      response.request().method() === 'GET',
  );
  await page.goto('/security');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Sicurezza account' }),
  ).toBeVisible();
  return methodsPromise;
}

test.describe('DANTE Access/Auth M5 full-stack security surface', () => {
  test.beforeEach(async ({ page }) => {
    await useItalianLocale(page);
  });

  test('keeps /security behind the canonical authenticated session gate', async ({
    page,
  }) => {
    await page.goto('/security');

    await expect(
      page.getByRole('heading', {
        level: 1,
        name: 'Accedi per gestire la sicurezza dell’account.',
      }),
    ).toBeVisible();
    await expect(page.getByRole('link', { name: 'Accedi' })).toHaveAttribute(
      'href',
      '/',
    );
  });

  test('reads real authenticator inventory and enforces password anti-lockout', async ({
    page,
  }, testInfo) => {
    await signIn(page, emailFor(testInfo, 1));
    const methodsResponse = await openSecurity(page);

    expect(methodsResponse.status()).toBe(200);
    const methods = (await methodsResponse.json()) as {
      password_established: boolean;
      providers: unknown[];
      passkeys: unknown[];
      active_passkey_count: number;
      recovery_eligible_email_count: number;
    };
    expect(methods).toMatchObject({
      password_established: true,
      providers: [],
      passkeys: [],
      active_passkey_count: 0,
      recovery_eligible_email_count: 1,
    });

    const removalPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith(removePasswordPath) &&
        response.request().method() === 'DELETE',
    );
    await page.getByRole('button', { name: 'Rimuovi password' }).click();
    const removal = await removalPromise;

    expect(removal.status()).toBe(409);
    expect(await responseProblemCode(removal)).toBe(
      'auth.authenticator_removal_blocked',
    );
    await expect(
      page.getByText(
        'DANTE blocked this removal because it would leave the account without a safe authenticator.',
      ),
    ).toBeVisible();
  });

  test('keeps provider sign-in public but requires session CSRF before provider linking', async ({
    page,
  }, testInfo) => {
    await page.goto('/');

    const publicBegin = await browserPostWithoutCsrf(page, googleBeginPath, {
      purpose: 'sign_in',
      return_target: 'access',
    });
    expect(publicBegin.status).toBe(503);
    expect(problemCode(publicBegin.body)).toBe('dependency.provider_unavailable');

    const signInResponse = await signIn(page, emailFor(testInfo, 2));
    const currentCsrf = await csrfToken(signInResponse);
    await openSecurity(page);

    const missingCsrf = await browserPostWithoutCsrf(page, appleBeginPath, {
      purpose: 'link',
      return_target: 'security',
    });
    expect(missingCsrf.status).toBe(403);
    expect(problemCode(missingCsrf.body)).toBe('security.csrf_failed');

    const appleBeginPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith(appleBeginPath) &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Collega Apple' }).click();
    const appleBegin = await appleBeginPromise;

    expect(appleBegin.request().headers()['x-dante-csrf']).toBe(currentCsrf);
    expect(appleBegin.status()).toBe(503);
    expect(await responseProblemCode(appleBegin)).toBe(
      'dependency.provider_unavailable',
    );
    await expect(
      page.getByText('The authentication service is temporarily unavailable.'),
    ).toBeVisible();
  });

  test('keeps passkey sign-in public and protects registration with current session CSRF', async ({
    page,
  }, testInfo) => {
    await page.goto('/');

    const passkeySignInPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith(passkeyAuthenticationBeginPath) &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Accedi con passkey' }).click();
    const passkeySignIn = await passkeySignInPromise;

    expect(passkeySignIn.request().headers()['x-dante-csrf']).toBeUndefined();
    expect(passkeySignIn.status()).toBe(503);
    expect(await responseProblemCode(passkeySignIn)).toBe(
      'dependency.provider_unavailable',
    );
    await expect(
      page.getByText(
        'La passkey non ha completato l’accesso. Riprova o usa un altro metodo.',
      ),
    ).toBeVisible();

    const signInResponse = await signIn(page, emailFor(testInfo, 3));
    const currentCsrf = await csrfToken(signInResponse);
    await openSecurity(page);

    const missingCsrf = await browserPostWithoutCsrf(
      page,
      passkeyRegistrationBeginPath,
      {},
    );
    expect(missingCsrf.status).toBe(403);
    expect(problemCode(missingCsrf.body)).toBe('security.csrf_failed');

    const registrationPromise = page.waitForResponse(
      (response) =>
        response.url().endsWith(passkeyRegistrationBeginPath) &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Aggiungi passkey' }).click();
    const registration = await registrationPromise;

    expect(registration.request().headers()['x-dante-csrf']).toBe(currentCsrf);
    expect(registration.status()).toBe(503);
    expect(await responseProblemCode(registration)).toBe(
      'dependency.provider_unavailable',
    );
    await expect(
      page.getByText('The authentication service is temporarily unavailable.'),
    ).toBeVisible();
  });
});
