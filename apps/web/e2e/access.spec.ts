import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const signInHeading = 'Accedi a DANTE';

async function expectNoHorizontalOverflow(page: Page) {
  const hasOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth,
  );

  expect(hasOverflow).toBe(false);
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

  test('switches to the narrow single-column composition', async ({ page }) => {
    await page.setViewportSize({ width: 800, height: 1000 });
    await page.goto('/');

    await expect(page.locator('.access-brand-stage')).toBeHidden();
    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();
    await expectNoHorizontalOverflow(page);
  });

  test('remains usable at a phone-width browser viewport', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');

    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Google' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Apple' }),
    ).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password', { exact: true })).toBeVisible();
    await expectNoHorizontalOverflow(page);
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

  test('has no automated WCAG A/AA violations on the sign-in surface', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
