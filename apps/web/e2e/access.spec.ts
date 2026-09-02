import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const signInHeading = 'Accedi a DANTE';

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

  test('navigates signup locally and stops before fake account creation', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await page.getByRole('button', { name: 'Crea un account' }).click();
    await expect(
      page.getByRole('heading', { name: 'Crea il tuo account DANTE' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Google' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Apple' }),
    ).toBeVisible();

    const signupEmail = page.getByLabel('Email');
    await signupEmail.fill('person@example.com');
    await page.getByRole('button', { name: 'Continua con email' }).click();

    await expect(
      page.getByRole('heading', { name: 'Proteggi il tuo account' }),
    ).toBeVisible();
    await expect(page.getByText('person@example.com')).toBeVisible();

    const newPassword = page.getByLabel('Password', { exact: true });
    await newPassword.fill('too-short');
    await page.getByRole('button', { name: 'Crea un account' }).click();
    await expect(page.getByText('Usa almeno 12 caratteri.')).toBeVisible();

    await newPassword.fill('correct horse battery staple');
    await page.getByRole('button', { name: 'Crea un account' }).click();

    await expect(page.locator('.access-condition-notice')).toHaveCount(0);
    await expect(
      page.getByRole('heading', { name: 'Proteggi il tuo account' }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', { name: 'Controlla la tua email' }),
    ).toHaveCount(0);
  });

  test('navigates recovery locally without leaking account existence', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await page.getByRole('button', { name: 'Password dimenticata?' }).click();
    await expect(
      page.getByRole('heading', { name: 'Recupera l’accesso' }),
    ).toBeVisible();

    await expect(
      page.getByText(
        'Se l’indirizzo è associato a un account DANTE, riceverai un link per reimpostare la password.',
      ),
    ).toBeVisible();

    await page.getByLabel('Email').fill('person@example.com');
    await page.getByRole('button', { name: 'Invia link di recupero' }).click();

    await expect(page.locator('.access-condition-notice')).toHaveCount(0);
    await expect(
      page.getByRole('heading', { name: 'Recupera l’accesso' }),
    ).toBeVisible();
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

    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();
    await expect(localeButton).toBeVisible();
    await expect(localeButton).toBeEnabled();
    await expect(googleButton).toBeVisible();
    await expect(googleButton).toBeEnabled();

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
