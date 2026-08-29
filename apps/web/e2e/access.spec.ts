import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const signInHeading = 'Accedi a DANTE';
const requestId = '019d0000-0000-7000-8000-000000000001';
const signupRef = '00000000-0000-4000-8000-000000000003';
const recoveryRef = '00000000-0000-4000-8000-000000000004';

const releaseViewports = [
  {
    name: 'phone-390',
    width: 390,
    height: 844,
    brandStage: false,
    verticalFit: true,
  },
  {
    name: 'phone-430',
    width: 430,
    height: 932,
    brandStage: false,
    verticalFit: true,
  },
  {
    name: 'effective-css-viewport-720x450',
    width: 720,
    height: 450,
    brandStage: false,
    verticalFit: false,
  },
  {
    name: 'tablet-768',
    width: 768,
    height: 1024,
    brandStage: false,
    verticalFit: true,
  },
  {
    name: 'tablet-820',
    width: 820,
    height: 1180,
    brandStage: false,
    verticalFit: true,
  },
  {
    name: 'desktop-1024',
    width: 1024,
    height: 768,
    brandStage: true,
    verticalFit: true,
  },
  {
    name: 'desktop-1280',
    width: 1280,
    height: 800,
    brandStage: true,
    verticalFit: true,
  },
  {
    name: 'desktop-1536',
    width: 1536,
    height: 960,
    brandStage: true,
    verticalFit: true,
  },
  {
    name: 'large-desktop-1920',
    width: 1920,
    height: 1080,
    brandStage: true,
    verticalFit: true,
  },
] as const;

function governedHeaders(contentType: string | null = 'application/json') {
  const headers: Record<string, string> = {
    'cache-control': 'no-store',
    'x-request-id': requestId,
  };
  if (contentType !== null) {
    headers['content-type'] = contentType;
  }
  return headers;
}

async function mockUnauthenticatedSession(page: Page) {
  await page.route('**/api/v1/auth/session', async (route) => {
    if (route.request().method() !== 'GET') {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 200,
      headers: governedHeaders(),
      body: JSON.stringify({ authenticated: false }),
    });
  });
}

async function expectNoHorizontalOverflow(page: Page) {
  const hasOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth,
  );

  expect(hasOverflow).toBe(false);
}

async function expectNoVerticalOverflow(page: Page) {
  const hasOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollHeight >
      document.documentElement.clientHeight,
  );

  expect(hasOverflow).toBe(false);
}

async function expectPanelWithinViewport(page: Page) {
  const viewport = page.viewportSize();
  const panelBox = await page.locator('.access-panel').boundingBox();

  expect(viewport).not.toBeNull();
  expect(panelBox).not.toBeNull();

  if (!viewport || !panelBox) {
    throw new Error('Access panel geometry could not be measured.');
  }

  expect(panelBox.x).toBeGreaterThanOrEqual(-1);
  expect(panelBox.x + panelBox.width).toBeLessThanOrEqual(viewport.width + 1);
  expect(panelBox.width).toBeGreaterThan(0);
}

async function expectDesktopBrandStageOpen(page: Page) {
  const stageBox = await page.locator('.access-brand-stage').boundingBox();
  const mainBox = await page.locator('.access-main').boundingBox();
  const panelBox = await page.locator('.access-panel').boundingBox();

  expect(stageBox).not.toBeNull();
  expect(mainBox).not.toBeNull();
  expect(panelBox).not.toBeNull();

  if (!stageBox || !mainBox || !panelBox) {
    throw new Error('Desktop Access geometry could not be measured.');
  }

  expect(stageBox.x).toBeLessThanOrEqual(1);
  expect(stageBox.height).toBeGreaterThanOrEqual(mainBox.height - 1);
  expect(panelBox.x).toBeGreaterThan(page.viewportSize()!.width / 2);
}

async function expectResponsiveSignInShell(
  page: Page,
  brandStageExpected: boolean,
  verticalFitExpected: boolean,
) {
  await expect(page.locator('.access-brand-lockup')).toBeVisible();
  await expect(
    page.getByRole('heading', { level: 1, name: signInHeading }),
  ).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Continua con Google' }),
  ).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Continua con Apple' }),
  ).toBeVisible();
  await expect(page.getByLabel('Email')).toBeVisible();
  await expect(page.getByLabel('Password', { exact: true })).toBeVisible();

  if (brandStageExpected) {
    await expect(page.locator('.access-brand-stage')).toBeVisible();
  } else {
    await expect(page.locator('.access-brand-stage')).toBeHidden();
  }

  await expectPanelWithinViewport(page);
  await expectNoHorizontalOverflow(page);

  if (verticalFitExpected) {
    await expectNoVerticalOverflow(page);
  }
}

async function switchToEnglish(page: Page) {
  await page
    .getByRole('button', {
      name: 'Cambia lingua. Lingua attuale: Italiano',
    })
    .click();
  await page
    .getByRole('group', { name: 'Lingue disponibili' })
    .getByRole('button', { name: /English/ })
    .click();

  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
}

async function expectNoAutomatedAxeViolations(page: Page) {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();

  expect(results.violations).toEqual([]);
}

test.describe('DANTE Access', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      if (!window.localStorage.getItem('dante.locale')) {
        window.localStorage.setItem('dante.locale', 'it');
      }
    });
    await mockUnauthenticatedSession(page);
  });

  test('renders the hardened desktop sign-in shell', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await expect(page.locator('html')).toHaveAttribute('lang', 'it');
    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(
      page.getByRole('button', {
        name: 'Cambia lingua. Lingua attuale: Italiano',
      }),
    ).toHaveText('IT');

    const brandHeading = page.getByRole('heading', {
      level: 2,
      name: 'Comprendi la vita. Dai forma al prossimo passo.',
    });
    await expect(brandHeading).toBeVisible();

    const brandHeadingMetrics = await brandHeading.evaluate((element) => {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();

      return {
        fontSize: Number.parseFloat(style.fontSize),
        height: rect.height,
      };
    });

    expect(brandHeadingMetrics.fontSize).toBeLessThanOrEqual(70);
    expect(brandHeadingMetrics.height).toBeLessThanOrEqual(300);

    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Google' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Apple' }),
    ).toBeVisible();
    await expect(page.getByLabel('Email')).toHaveAttribute(
      'autocomplete',
      'email',
    );
    await expect(page.getByLabel('Email')).toHaveAttribute(
      'placeholder',
      'nome@esempio.com',
    );
    await expect(page.getByLabel('Password', { exact: true })).toHaveAttribute(
      'autocomplete',
      'current-password',
    );
    await expect(page.locator('.access-brand-stage')).toBeVisible();
    await expect(page.locator('.access-panel')).toHaveCSS(
      'border-radius',
      '26px',
    );
    await expectDesktopBrandStageOpen(page);
    await expectNoHorizontalOverflow(page);
  });

  test('switches and persists the selected language', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await switchToEnglish(page);

    await expect(
      page.getByRole('heading', { level: 1, name: 'Sign in to DANTE' }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', {
        level: 2,
        name: 'Understand life. Shape what comes next.',
      }),
    ).toBeVisible();
    await expect(page.getByLabel('Email')).toHaveAttribute(
      'placeholder',
      'name@example.com',
    );
    await expect(
      page.getByRole('button', {
        name: 'Change language. Current language: English',
      }),
    ).toHaveText('EN');

    await page.reload();

    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    await expect(
      page.getByRole('heading', { level: 1, name: 'Sign in to DANTE' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', {
        name: 'Change language. Current language: English',
      }),
    ).toHaveText('EN');
  });

  test('toggles password visibility without changing the field value', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const passwordInput = page.getByLabel('Password', { exact: true });
    await passwordInput.fill('Dante-password-example');
    await expect(passwordInput).toHaveAttribute('type', 'password');

    await page.getByRole('button', { name: 'Mostra password' }).click();
    await expect(passwordInput).toHaveAttribute('type', 'text');
    await expect(passwordInput).toHaveValue('Dante-password-example');

    await page.getByRole('button', { name: 'Nascondi password' }).click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
    await expect(passwordInput).toHaveValue('Dante-password-example');
  });

  test('wires signup to governed server outcomes without inventing account creation', async ({
    page,
  }) => {
    await page.route('**/api/v1/auth/signup', async (route) => {
      expect(route.request().method()).toBe('POST');
      expect(route.request().postDataJSON()).toEqual({
        email: 'person@example.com',
        password: 'correct horse battery staple',
      });
      await route.fulfill({
        status: 200,
        headers: governedHeaders(),
        body: JSON.stringify({
          signup_ref: signupRef,
          signup_expires_at: '2026-08-29T20:00:00Z',
          verification_expires_at: '2026-08-29T19:15:00Z',
          verification_required: true,
        }),
      });
    });
    await page.route('**/api/v1/auth/signup/verify', async (route) => {
      expect(route.request().method()).toBe('POST');
      expect(route.request().postDataJSON()).toEqual({
        signup_ref: signupRef,
        code: '654321',
      });
      await route.fulfill({
        status: 200,
        headers: governedHeaders(),
        body: JSON.stringify({
          outcome: 'authenticated',
          authenticated: true,
          account_ref: '00000000-0000-4000-8000-000000000001',
          auth_session_ref: '00000000-0000-4000-8000-000000000002',
          recent_auth_at: '2026-08-29T18:00:00Z',
          expires_at: '2026-09-28T18:00:00Z',
          csrf_token: 'csrf-token',
        }),
      });
    });

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await page.getByRole('button', { name: 'Crea un account' }).click();
    await expect(
      page.getByRole('heading', { name: 'Crea il tuo account DANTE' }),
    ).toBeVisible();

    await page.getByLabel('Email').fill('person@example.com');
    await page.getByRole('button', { name: 'Continua con email' }).click();

    await expect(
      page.getByRole('heading', { name: 'Proteggi il tuo account' }),
    ).toBeVisible();
    const newPassword = page.getByLabel('Password', { exact: true });
    await newPassword.fill('too-short');
    await page.getByRole('button', { name: 'Crea un account' }).click();
    await expect(page.getByText('Usa almeno 15 caratteri.')).toBeVisible();

    await newPassword.fill('correct horse battery staple');
    await page.getByRole('button', { name: 'Crea un account' }).click();

    await expect(
      page.getByRole('heading', { name: 'Controlla la tua email' }),
    ).toBeVisible();
    await page.getByLabel('Codice di verifica').fill('654321');
    await page.getByRole('button', { name: 'Verifica e continua' }).click();

    await expect(
      page.getByRole('heading', { name: 'Come vuoi che DANTE ti chiami?' }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', { name: 'Accesso confermato' }),
    ).toHaveCount(0);
  });

  test('keeps password recovery neutral after the governed 202 response', async ({
    page,
  }) => {
    await page.route('**/api/v1/auth/recovery', async (route) => {
      expect(route.request().method()).toBe('POST');
      expect(route.request().postDataJSON()).toEqual({
        email: 'unknown@example.com',
      });
      await route.fulfill({
        status: 202,
        headers: governedHeaders(),
        body: JSON.stringify({ accepted: true }),
      });
    });

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');
    await page.getByRole('button', { name: 'Password dimenticata?' }).click();

    await expect(
      page.getByText(
        'Se l’indirizzo è associato a un account DANTE, riceverai un link per reimpostare la password.',
      ),
    ).toBeVisible();

    await page.getByLabel('Email').fill('unknown@example.com');
    await page.getByRole('button', { name: 'Invia link di recupero' }).click();

    await expect(
      page.getByRole('heading', { name: 'Controlla la tua email' }),
    ).toBeVisible();
    await expect(
      page.getByText(
        'Se esiste un account associato all’indirizzo indicato, riceverai le istruzioni per recuperare l’accesso.',
      ),
    ).toBeVisible();
  });

  test('scrubs recovery bearer fragments before reset and never persists the secret', async ({
    page,
  }) => {
    const secret = 'browser-only-recovery-secret';
    await page.route('**/api/v1/auth/recovery/validate', async (route) => {
      expect(route.request().postDataJSON()).toEqual({
        password_recovery_ref: recoveryRef,
        secret,
      });
      await route.fulfill({
        status: 200,
        headers: governedHeaders(),
        body: JSON.stringify({ valid: true }),
      });
    });
    await page.route('**/api/v1/auth/reset-password', async (route) => {
      expect(route.request().postDataJSON()).toEqual({
        password_recovery_ref: recoveryRef,
        secret,
        new_password: 'new correct horse battery staple',
      });
      await route.fulfill({
        status: 204,
        headers: governedHeaders(null),
        body: '',
      });
    });

    await page.goto(`/?recovery=${recoveryRef}#${secret}`);
    await expect(
      page.getByRole('heading', { name: 'Crea una nuova password' }),
    ).toBeVisible();

    const validatedUrl = new URL(page.url());
    expect(validatedUrl.searchParams.get('recovery')).toBe(recoveryRef);
    expect(validatedUrl.hash).toBe('');

    const storageValues = await page.evaluate(() => {
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
    expect(storageValues).not.toContain(secret);

    await page
      .getByLabel('Nuova password', { exact: true })
      .fill('new correct horse battery staple');
    await page
      .getByLabel('Conferma password', { exact: true })
      .fill('new correct horse battery staple');
    await page.getByRole('button', { name: 'Aggiorna password' }).click();

    await expect(
      page.getByRole('heading', { name: 'Password aggiornata' }),
    ).toBeVisible();
    const consumedUrl = new URL(page.url());
    expect(consumedUrl.searchParams.has('recovery')).toBe(false);
    expect(consumedUrl.hash).toBe('');
  });

  test('surfaces browser offline as transport state rather than credential failure', async ({
    context,
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();

    await context.setOffline(true);

    await expect(page.getByText('Sei offline.')).toBeVisible();
    await expect(page.getByText('Riconnettiti per continuare.')).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();

    await context.setOffline(false);
    await expect(page.locator('.access-condition-notice')).toHaveCount(0);
  });

  for (const viewport of releaseViewports) {
    test(`keeps release geometry stable at ${viewport.name}`, async ({
      page,
    }) => {
      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height,
      });
      await page.goto('/');

      await expectResponsiveSignInShell(
        page,
        viewport.brandStage,
        viewport.verticalFit,
      );
    });
  }

  for (const viewport of [
    { name: 'phone-430', width: 430, height: 932 },
    { name: 'desktop-1024', width: 1024, height: 768 },
  ] as const) {
    test(`keeps English signup copy stable at ${viewport.name}`, async ({
      page,
    }) => {
      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height,
      });
      await page.goto('/');
      await switchToEnglish(page);

      await expect(
        page.getByRole('heading', { level: 1, name: 'Sign in to DANTE' }),
      ).toBeVisible();
      await page.getByRole('button', { name: 'Create account' }).click();
      await expect(
        page.getByRole('heading', { name: 'Create your DANTE account' }),
      ).toBeVisible();
      await expectNoHorizontalOverflow(page);

      await page.getByLabel('Email').fill('person@example.com');
      await page.getByRole('button', { name: 'Continue with email' }).click();

      await expect(
        page.getByRole('heading', { name: 'Protect your account' }),
      ).toBeVisible();
      await expect(page.getByText('person@example.com')).toBeVisible();
      await expectNoHorizontalOverflow(page);
      await expectPanelWithinViewport(page);
    });
  }

  test('honors the reduced-motion preference on Access transitions', async ({
    page,
  }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const transitionDurations = await Promise.all([
      page
        .getByRole('button', { name: 'Continua con Google' })
        .evaluate(
          (element) => window.getComputedStyle(element).transitionDuration,
        ),
      page
        .getByRole('button', { name: 'Accedi', exact: true })
        .evaluate(
          (element) => window.getComputedStyle(element).transitionDuration,
        ),
      page
        .getByLabel('Email')
        .evaluate(
          (element) => window.getComputedStyle(element).transitionDuration,
        ),
      page
        .locator('.access-locale-chevron')
        .evaluate(
          (element) => window.getComputedStyle(element).transitionDuration,
        ),
    ]);

    for (const durationList of transitionDurations) {
      const allDurationsAreZero = durationList
        .split(',')
        .every((duration) => Number.parseFloat(duration) === 0);

      expect(allDurationsAreZero).toBe(true);
    }
  });

  test('exposes a keyboard-operable locale and sign-in path', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const localeButton = page.getByRole('button', {
      name: 'Cambia lingua. Lingua attuale: Italiano',
    });
    const googleButton = page.getByRole('button', {
      name: 'Continua con Google',
    });

    await page.keyboard.press('Tab');
    await expect(localeButton).toBeFocused();

    await page.keyboard.press('ArrowDown');
    const selectedLocale = page
      .getByRole('group', { name: 'Lingue disponibili' })
      .getByRole('button', { name: /Italiano/ });
    await expect(selectedLocale).toBeFocused();

    await page.keyboard.press('Escape');
    await expect(localeButton).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(googleButton).toBeFocused();
  });

  test('has no automated WCAG A/AA violations on the desktop sign-in surface', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await expectNoAutomatedAxeViolations(page);
  });

  test('has no automated WCAG A/AA violations on the English phone signup password surface', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 430, height: 932 });
    await page.goto('/');
    await switchToEnglish(page);

    await page.getByRole('button', { name: 'Create account' }).click();
    await page.getByLabel('Email').fill('person@example.com');
    await page.getByRole('button', { name: 'Continue with email' }).click();

    await expect(
      page.getByRole('heading', { name: 'Protect your account' }),
    ).toBeVisible();
    await expectNoHorizontalOverflow(page);
    await expectNoAutomatedAxeViolations(page);
  });
});
